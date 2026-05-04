#!/usr/bin/env python3
"""Compute per-rule health metrics from the structured auditor logs.

Runs SCHEMAS §Learning query over the three append-only logs and
classifies every rule_id as healthy, noisy, dormant, or disputed.

Inputs (paths are relative to the repo root):
    auditor/findings.jsonl          — one record per finding
    auditor/logs/events.jsonl       — finding_outcome + finding_verified + finding_introduced events (filtered)
    auditor/disagreements.jsonl     — self_fp, maintainer_rejected, pr_comments_snapshot, downstream_suppression
    auditor/registry/repos.json     — rule-adopted repos, total repos audited

Output (argv[1] or stdout): a JSON blob with
    summary.*            — PR scorecard numbers (drop-in replacement for the old feedback-summary.json)
    rule_metrics[rid]    — hits, contributed, merged, closed_unmerged, open, self_fp,
                           maintainer_rejected, downstream_suppressions, dissent_types,
                           verified_fixed, verified_persists, verify_rate, introduced, state
    dormant_rules[]      — R* rules in the catalog with zero hits
    unclassified_ids[]   — non-catalog rule_ids seen in findings (SEC-*, BUG-*, CC-*)
    metadata.*           — totals, updated_at

The `verified_*` metrics come from finding_verified events emitted by the
post-merge re-audit (auditor-case-study.yml). They give effect-level
precision: `merged / contributed` says "maintainer accepted our PR";
`verified_fixed / verified_total` says "re-running the scorer confirms
the rule's target is actually gone from the code". When both are present,
rule state classification weights the verified signal above the merged one.

All reads are tolerant: missing files produce zeros, malformed JSONL
lines are skipped with a warning to stderr.
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

FINDINGS_PATH = Path("auditor/findings.jsonl")
EVENTS_PATH = Path("auditor/logs/events.jsonl")
DISAGREEMENTS_PATH = Path("auditor/disagreements.jsonl")
REGISTRY_PATH = Path("auditor/registry/repos.json")
RULES_CATALOG = Path("skills/nlpm/rules/SKILL.md")


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    with path.open() as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(f"WARN {path}:{i} malformed JSON: {exc}", file=sys.stderr)
    return records


def load_catalog_rules() -> set[str]:
    if not RULES_CATALOG.exists():
        return set()
    text = RULES_CATALOG.read_text()
    return set(re.findall(r"\bR\d{2}\b", text))


def classify_rule(metrics: dict) -> str:
    hits = metrics["hits"]
    contributed = metrics["contributed"]
    self_fp = metrics["self_fp"]
    maintainer_rejected = metrics["maintainer_rejected"]
    downstream = metrics["downstream_suppressions"]
    merged = metrics["merged"]
    applied_separately = metrics.get("applied_separately", 0)
    closed_unmerged = metrics.get("closed_unmerged", 0)
    verified_total = metrics.get("verified_total", 0)
    verified_fixed = metrics.get("verified_fixed", 0)

    # Disputed first — downstream suppressions and maintainer rejection outrank
    # self-precision, since those represent external dissent the auditor
    # can't resolve alone.
    if downstream >= 2:
        return "disputed"
    if contributed >= 3 and maintainer_rejected / contributed > 0.3:
        return "disputed"

    # Noisy: high false-positive rate (self-known or externally inferred).
    if hits >= 3 and self_fp / hits > 0.2:
        return "noisy"

    # Verified signal — when the re-audit has run for enough findings,
    # weight it above the merged signal. A PR that merged but left the
    # finding in place (persists_*) counts against the rule here, where
    # `merged / contributed` would have counted it for.
    if verified_total >= 3:
        if verified_fixed / verified_total < 0.5:
            return "noisy"
    else:
        # Fall back to PR-level signal when re-audit hasn't accumulated yet.
        # Use resolved-only rate so that open PRs don't count against the
        # rule. `applied_separately` PRs count alongside merged — both are
        # positive maintainer judgments ("the bug is real"), they just took
        # different paths to land. Concrete case: avifenesh closed three
        # CC-stale-count PRs with "the issue you flagged is real. Closing
        # in favor of the consolidated structural fix in #840" — that is a
        # win, not a failure.
        accepted = merged + applied_separately
        resolved = accepted + closed_unmerged
        if resolved >= 3 and accepted / resolved < 0.5:
            return "noisy"

    return "healthy"


def main() -> int:
    findings = load_jsonl(FINDINGS_PATH)
    events = load_jsonl(EVENTS_PATH)
    disagreements = load_jsonl(DISAGREEMENTS_PATH)

    try:
        with REGISTRY_PATH.open() as fh:
            registry = json.load(fh)
    except (OSError, json.JSONDecodeError):
        registry = {"repos": {}}

    # Index finding_outcome events by fingerprint. When a fingerprint appears
    # multiple times (e.g., open → merged), the LAST entry wins. events.jsonl
    # is append-only and chronologically ordered, so a simple final-write loop
    # gives the latest state.
    outcome_by_fp: dict[str, str] = {}
    for e in events:
        if e.get("event") != "finding_outcome":
            continue
        data = e.get("data", {})
        state = data.get("pr_state")
        if not state:
            continue
        for fp in data.get("fingerprints", []) or []:
            outcome_by_fp[fp] = state

    # The SCHEMAS pr_state enum is {merged, closed_unmerged, open, stale_90d,
    # cla_blocked} — `applied_separately` is NOT in the enum. The track
    # workflow maps both `rejected` and `applied_separately` outcomes to
    # `closed_unmerged` for event emission, which loses the positive signal
    # for rule-health. Cross-reference the registry's authoritative
    # `prs[].outcome` field to recover the distinction. Findings whose
    # fingerprint maps to a PR with outcome=applied_separately get
    # reclassified into a separate bucket that the classifier credits as
    # positive (alongside merged), not as a failure.
    #
    # Concrete case: agent-sh/agnix #828/#829/#830 closed_unmerged but
    # applied separately in #840 (avifenesh: "the issue you flagged is
    # real. Closing in favor of the consolidated structural fix in #840").
    # CC-stale-count was being classified noisy because rule-health saw
    # 4 closed_unmerged with 0 merged. After this fix, three of those four
    # become applied_separately and the rule clears.
    applied_separately_by_fp: set[str] = set()
    for slug, repo_data in registry.get("repos", {}).items():
        for pr in repo_data.get("prs") or []:
            if pr.get("outcome") != "applied_separately":
                continue
            for fp in pr.get("fingerprints") or []:
                applied_separately_by_fp.add(fp)

    # Index finding_verified events by fingerprint. Same last-write-wins rule
    # applies — a finding can be re-audited more than once (e.g., a case
    # study is regenerated after a new maintainer commit). The verify
    # outcome is an enum documented in SCHEMAS.md §finding_verified.
    FIXED_OUTCOMES = {
        "fixed_and_merged",
        "fixed_applied_separately",
        "fixed_upstream_not_merged",
    }
    PERSISTS_OUTCOMES = {"persists_identically", "persists_line_shifted"}
    verified_by_fp: dict[str, str] = {}
    for e in events:
        if e.get("event") != "finding_verified":
            continue
        data = e.get("data", {})
        fp = data.get("fingerprint")
        outcome = data.get("outcome")
        if fp and outcome:
            verified_by_fp[fp] = outcome

    # Count finding_introduced events per rule. These are NOT in findings.jsonl
    # (by design — re-audit findings don't inflate reach), so they need a
    # separate aggregation path.
    introduced_by_rule: Counter[str] = Counter()
    for e in events:
        if e.get("event") != "finding_introduced":
            continue
        rid = e.get("data", {}).get("rule_id")
        if rid:
            introduced_by_rule[rid] += 1

    self_fp_fps = {
        d.get("fingerprint")
        for d in disagreements
        if d.get("event") == "self_false_positive" and d.get("fingerprint")
    }

    rejected_by_fp: dict[str, list[dict]] = defaultdict(list)
    for d in disagreements:
        if d.get("event") not in ("maintainer_rejected", "maintainer_pushback"):
            continue
        for fp in d.get("fingerprints", []) or []:
            rejected_by_fp[fp].append(d)

    suppressions_by_rule: dict[str, list[dict]] = defaultdict(list)
    for d in disagreements:
        if d.get("event") != "downstream_suppression":
            continue
        rid = d.get("rule_id")
        if rid:
            suppressions_by_rule[rid].append(d)

    findings_by_rule: dict[str, list[dict]] = defaultdict(list)
    for f in findings:
        rid = f.get("rule_id")
        if rid:
            findings_by_rule[rid].append(f)

    rule_metrics: dict[str, dict] = {}
    for rid, fs in findings_by_rule.items():
        unique_fps = {f["fingerprint"] for f in fs if f.get("fingerprint")}
        contributed = sum(1 for fp in unique_fps if fp in outcome_by_fp)
        merged = sum(1 for fp in unique_fps if outcome_by_fp.get(fp) == "merged")
        applied_separately = len(unique_fps & applied_separately_by_fp)
        # Don't double-count: a fingerprint marked applied_separately in
        # the registry will also have pr_state=closed_unmerged in events
        # (until the SCHEMAS enum gets extended). Subtract from the
        # closed_unmerged bucket to keep the totals consistent.
        closed_unmerged = sum(
            1 for fp in unique_fps if outcome_by_fp.get(fp) == "closed_unmerged"
        ) - applied_separately
        open_count = sum(1 for fp in unique_fps if outcome_by_fp.get(fp) == "open")
        self_fp = len(unique_fps & self_fp_fps)
        maintainer_rejected = sum(1 for fp in unique_fps if fp in rejected_by_fp)

        # Verified metrics — finding_verified events joined on fingerprint.
        verified_outcomes = [
            verified_by_fp[fp] for fp in unique_fps if fp in verified_by_fp
        ]
        verified_total = len(verified_outcomes)
        verified_fixed = sum(1 for o in verified_outcomes if o in FIXED_OUTCOMES)
        verified_persists = sum(1 for o in verified_outcomes if o in PERSISTS_OUTCOMES)
        verify_rate = (
            verified_fixed / verified_total if verified_total else None
        )

        dissent_types: Counter[str] = Counter()
        for fp in unique_fps:
            for d in rejected_by_fp.get(fp, []):
                dt = d.get("dissent_type")
                if dt:
                    dissent_types[dt] += 1

        metrics = {
            "hits": len(fs),
            "unique_fingerprints": len(unique_fps),
            "contributed": contributed,
            "merged": merged,
            "applied_separately": applied_separately,
            "closed_unmerged": closed_unmerged,
            "open": open_count,
            "self_fp": self_fp,
            "maintainer_rejected": maintainer_rejected,
            "downstream_suppressions": len(suppressions_by_rule.get(rid, [])),
            "dissent_types": dict(dissent_types),
            "verified_total": verified_total,
            "verified_fixed": verified_fixed,
            "verified_persists": verified_persists,
            "verify_rate": verify_rate,
            "introduced": introduced_by_rule.get(rid, 0),
        }
        metrics["state"] = classify_rule(metrics)
        rule_metrics[rid] = metrics

    # A rule might fire ONLY in a post-merge re-audit (finding_introduced
    # with no prior finding in findings.jsonl). Surface those too, with
    # hits=0 so consumers see the introduced-only signal without conflating
    # it with reach.
    for rid, introduced_count in introduced_by_rule.items():
        if rid in rule_metrics:
            continue
        rule_metrics[rid] = {
            "hits": 0,
            "unique_fingerprints": 0,
            "contributed": 0,
            "merged": 0,
            "closed_unmerged": 0,
            "open": 0,
            "self_fp": 0,
            "maintainer_rejected": 0,
            "downstream_suppressions": len(suppressions_by_rule.get(rid, [])),
            "dissent_types": {},
            "verified_total": 0,
            "verified_fixed": 0,
            "verified_persists": 0,
            "verify_rate": None,
            "introduced": introduced_count,
            "state": "healthy",  # nothing to judge yet — introduced-only
        }

    # Dormant: catalog R* rules with zero findings. SEC/BUG/CC namespaces are
    # dynamic — no authoritative inventory — so dormant detection is catalog-only.
    catalog = load_catalog_rules()
    dormant_rules = sorted(catalog - set(rule_metrics.keys()))

    # Non-catalog rule_ids that appeared in findings — useful for spotting
    # new SEC-* patterns or UNCLASSIFIED drift.
    unclassified_ids = sorted(set(rule_metrics.keys()) - catalog)

    # PR scorecard from the registry (drop-in for the old summary).
    all_prs = []
    for _, v in registry.get("repos", {}).items():
        all_prs.extend(v.get("prs", []) or [])

    merged_prs = [p for p in all_prs if p.get("outcome") == "merged"]
    applied_prs = [p for p in all_prs if p.get("outcome") == "applied_separately"]
    rejected_prs = [p for p in all_prs if p.get("outcome") == "rejected"]
    open_prs = [p for p in all_prs if p.get("outcome") == "open"]
    accepted = len(merged_prs) + len(applied_prs)
    resolved = accepted + len(rejected_prs)

    rule_adopted = [
        k for k, v in registry.get("repos", {}).items() if v.get("rule_adopted") is True
    ]

    # Top rules for the report's Rule Frequency table — ordered by hits.
    top_rules = sorted(
        rule_metrics.items(), key=lambda kv: -kv[1]["hits"]
    )[:10]

    summary = {
        "prs_total": len(all_prs),
        "prs_merged": len(merged_prs),
        "prs_applied_separately": len(applied_prs),
        "prs_rejected": len(rejected_prs),
        "prs_pending": len(open_prs),
        "acceptance_rate": f"{accepted / resolved * 100:.0f}%" if resolved else "N/A",
        "merge_only_rate": f"{len(merged_prs) / resolved * 100:.0f}%" if resolved else "N/A",
        "rule_adopted_repos": rule_adopted,
        "top_rules": [(rid, m["hits"]) for rid, m in top_rules],
        "rule_metrics": rule_metrics,
        "dormant_rules": dormant_rules,
        "unclassified_ids": unclassified_ids,
        "state_counts": dict(
            Counter(m["state"] for m in rule_metrics.values())
        ),
        "dormant_count": len(dormant_rules),
    }

    # Mirror into auditor/feedback/log.json so the legacy shape continues
    # to carry the fields older tooling might read. Only the fields that
    # the old pipeline wrote are kept here.
    feedback_path = Path("auditor/feedback/log.json")
    if feedback_path.exists():
        try:
            with feedback_path.open() as fh:
                feedback = json.load(fh)
        except (OSError, json.JSONDecodeError):
            feedback = {"metadata": {}, "rule_stats": {}}
    else:
        feedback = {"metadata": {}, "rule_stats": {}}

    feedback.setdefault("metadata", {}).update({
        "total_prs_submitted": len(all_prs),
        "total_prs_merged": len(merged_prs),
        "total_prs_applied_separately": len(applied_prs),
        "total_prs_rejected": len(rejected_prs),
        "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    })
    feedback.setdefault("rule_stats", {})
    for rid, m in rule_metrics.items():
        feedback["rule_stats"].setdefault(
            rid, {"total_hits": 0, "led_to_merged_pr": 0, "led_to_rejected_pr": 0}
        )
        feedback["rule_stats"][rid].update({
            "total_hits": m["hits"],
            "led_to_merged_pr": m["merged"],
            "led_to_rejected_pr": m["closed_unmerged"],
            "self_false_positive": m["self_fp"],
            "maintainer_rejected": m["maintainer_rejected"],
            "downstream_suppressions": m["downstream_suppressions"],
            "verified_fixed": m["verified_fixed"],
            "verified_persists": m["verified_persists"],
            "verify_rate": m["verify_rate"],
            "introduced_since_audit": m["introduced"],
            "state": m["state"],
        })
    with feedback_path.open("w") as fh:
        json.dump(feedback, fh, indent=2)

    out = json.dumps(summary, indent=2)
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(out)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
