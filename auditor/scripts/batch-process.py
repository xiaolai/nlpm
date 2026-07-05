#!/usr/bin/env python3
"""Run the auditor batch-processor phases.

Phases (in order):
  1. Promote audit-complete issues to contribute-approved (if security gate passes)
  1.2 Drain contribute-approved backlog (issues whose label event missed)
  1.5 Reopen wrongly-closed audit-candidate issues
  2. Pick next batch of audit-candidate → audit-ready (FIFO, capped by BATCH_SIZE - RUNNING)
  3. Re-trigger stuck audit-ready issues (whose label event missed)

Each phase is its own function — fail-soft (failures in one phase don't
block later phases). All gh-CLI interactions go through subprocess.run.

Args / env:
  --batch-size N    max concurrent audits (default $BATCH_SIZE env or 5)
  --dry-run         print actions without dispatching
  $REGISTRY_PATH    default: auditor/registry/repos.json
  $GITHUB_REPOSITORY (read but unused — kept for parity with bash version)

Extracted from auditor-batch-processor.yml in v0.8.12 (was a 240-line
inline bash block with 5 phases).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


REGISTRY_PATH = Path(os.environ.get("REGISTRY_PATH", "auditor/registry/repos.json"))
DRAIN_LIMIT = 5
RETRIGGER_FAILURE_CAP = 3
DISPATCH_SLEEP = 2.0
# v0.8.17 — score threshold for the always-clean exemplar path.
# Audits at or above this score with security != BLOCKED and no existing
# exemplar get labeled `case-study-clean`, which fires auditor-exemplar.yml.
EXEMPLAR_THRESHOLD = int(os.environ.get("EXEMPLAR_THRESHOLD", "90"))

# v0.8.23 — low-landing-rate rule suppression.
#
# Some rules have high verify_rate (they correctly identify real bugs)
# but consistently fail to land via our PRs — maintainers fix the bug
# their own way (`applied_separately`) or close the PR with
# `context_missed` dissent. Promoting an audit whose only high-confidence
# findings are on those rules ships PRs that won't merge.
#
# A rule is flagged "low-landing" when:
#   hits >= LANDING_MIN_HITS                 (volume — enough data to judge)
#   contributed >= LANDING_MIN_CONTRIBUTED   (we've actually tried PR'ing it)
#   merged / contributed < LANDING_MERGE_THRESHOLD
#   state NOT IN {noisy, disputed}           (those go through refinement)
#
# Found empirically on 2026-05-20 inspecting BUG-broken-reference:
#   76 hits, 12 contributed, 0 merged, verify_rate 100%, state=healthy.
# Rule-health classified it healthy on verify_rate, but the PR delivery
# was wasted effort. Suppression catches this class without touching the
# rulebook itself.
LANDING_MIN_HITS = int(os.environ.get("NLPM_LANDING_MIN_HITS", "20"))
LANDING_MIN_CONTRIBUTED = int(os.environ.get("NLPM_LANDING_MIN_CONTRIBUTED", "5"))
LANDING_MERGE_THRESHOLD = float(os.environ.get("NLPM_LANDING_MERGE_THRESHOLD", "0.15"))
LANDING_SUPPRESSION_DISABLED = (
    os.environ.get("NLPM_DISABLE_LOW_LANDING_SUPPRESSION", "").lower() in ("1", "true", "yes")
)
RULE_HEALTH_SCRIPT = Path("auditor/scripts/rule-health.py")


def gh(args: list[str], check: bool = False) -> tuple[int, str]:
    """Run `gh` and return (rc, stdout)."""
    try:
        proc = subprocess.run(
            ["gh", *args], capture_output=True, text=True, check=check
        )
        return proc.returncode, proc.stdout
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout or ""


def registry_status(repo: str) -> str:
    """Read the registry status for `repo`. Returns 'none' on absence."""
    try:
        data = json.loads(REGISTRY_PATH.read_text())
    except (OSError, json.JSONDecodeError):
        return "none"
    return (data.get("repos", {}).get(repo) or {}).get("status") or "none"


def registry_security(repo: str) -> str:
    try:
        data = json.loads(REGISTRY_PATH.read_text())
    except (OSError, json.JSONDecodeError):
        return "UNKNOWN"
    return (data.get("repos", {}).get(repo) or {}).get("security") or "UNKNOWN"


def registry_score(repo: str) -> int:
    """Read the registry score for `repo`. Returns 0 on absence."""
    try:
        data = json.loads(REGISTRY_PATH.read_text())
    except (OSError, json.JSONDecodeError):
        return 0
    val = (data.get("repos", {}).get(repo) or {}).get("score")
    try:
        return int(val) if val is not None else 0
    except (TypeError, ValueError):
        return 0


_low_landing_cache: set[str] | None = None


def low_landing_rules() -> set[str]:
    """Return the set of rule_ids in the "high-precision, low-landing" bucket.

    Defined as: a rule that has been hit enough times to judge,
    contributed in enough PRs to have actual data, but merges below
    LANDING_MERGE_THRESHOLD — AND isn't already classified noisy/
    disputed (those have their own refinement path). The classic case
    on 2026-05-20: BUG-broken-reference, 76 hits, 12 PRs, 0 merged,
    yet healthy by verify_rate.

    The function shells out to `auditor/scripts/rule-health.py` to
    compute current metrics from the append-only logs. Cached after
    first call for the duration of the batch-process run.

    Fail-soft: any failure returns the empty set, which disables
    suppression. Logs the reason to stderr.

    Opt-out: NLPM_DISABLE_LOW_LANDING_SUPPRESSION=1 returns empty
    without invoking rule-health.
    """
    global _low_landing_cache
    if _low_landing_cache is not None:
        return _low_landing_cache
    if LANDING_SUPPRESSION_DISABLED:
        _low_landing_cache = set()
        return _low_landing_cache
    if not RULE_HEALTH_SCRIPT.exists():
        print(
            f"WARN low_landing_rules: {RULE_HEALTH_SCRIPT} not found; "
            f"suppression disabled this run",
            file=sys.stderr,
        )
        _low_landing_cache = set()
        return _low_landing_cache

    out_path = Path("/tmp/batch-process-rule-health.json")
    try:
        proc = subprocess.run(
            [sys.executable, str(RULE_HEALTH_SCRIPT), str(out_path)],
            capture_output=True, text=True, check=False, timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(
            f"WARN low_landing_rules: rule-health invocation failed: {exc}; "
            f"suppression disabled this run",
            file=sys.stderr,
        )
        _low_landing_cache = set()
        return _low_landing_cache
    if proc.returncode != 0:
        print(
            f"WARN low_landing_rules: rule-health exited {proc.returncode}; "
            f"suppression disabled this run. stderr:",
            file=sys.stderr,
        )
        if proc.stderr:
            print(proc.stderr.rstrip(), file=sys.stderr)
        _low_landing_cache = set()
        return _low_landing_cache

    try:
        data = json.loads(out_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(
            f"WARN low_landing_rules: cannot read rule-health output: {exc}; "
            f"suppression disabled this run",
            file=sys.stderr,
        )
        _low_landing_cache = set()
        return _low_landing_cache

    rules: set[str] = set()
    metrics = data.get("rule_metrics", {}) or {}
    for rule_id, m in metrics.items():
        if not isinstance(m, dict):
            continue
        # State-based pre-filter — refinement handles noisy/disputed.
        if m.get("state") in ("noisy", "disputed"):
            continue
        hits = int(m.get("hits") or 0)
        contributed = int(m.get("contributed") or 0)
        merged = int(m.get("merged") or 0)
        if hits < LANDING_MIN_HITS:
            continue
        if contributed < LANDING_MIN_CONTRIBUTED:
            continue
        rate = merged / contributed if contributed else 0.0
        if rate < LANDING_MERGE_THRESHOLD:
            rules.add(rule_id)

    if rules:
        joined = ", ".join(sorted(rules))
        print(
            f"low_landing_rules: {len(rules)} rule(s) under suppression — {joined}",
            file=sys.stderr,
        )
    else:
        print("low_landing_rules: no rules meet suppression criteria", file=sys.stderr)
    _low_landing_cache = rules
    return _low_landing_cache


def audit_high_conf_bug_count(
    repo: str, *, excluded_rules: set[str] | None = None,
) -> int:
    """Count high-confidence PR-worthy findings in the per-audit sidecar.

    The contribute workflow only ships findings with `confidence == "high"`,
    so an audit with zero high-confidence bugs has nothing to contribute.
    Promoting such an audit to `contribute-approved` would fire a workflow
    that does no useful work and leaves the issue stuck at that label
    forever (no phase transitions it forward).

    When `excluded_rules` is provided, findings whose `rule_id` is in
    that set are not counted. Used by the v0.8.23 low-landing-rate
    suppression: a repo whose only high-confidence findings sit on
    low-landing rules is treated as "nothing worth shipping" and skips
    promotion. The findings still exist in the sidecar — only the
    promotion decision changes.

    Returns -1 if the sidecar is missing (signal: cannot determine, fall
    back to old behavior of promoting). Returns 0 or more otherwise.
    """
    excluded_rules = excluded_rules or set()
    slug = repo.replace("/", "-")
    sidecar = Path("auditor/audits") / f"{slug}.findings.jsonl"
    if not sidecar.exists():
        return -1
    n = 0
    malformed = 0
    try:
        for i, line in enumerate(sidecar.read_text().splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as exc:
                # A malformed sidecar line means we cannot count this finding;
                # warn loudly. Promotion that depends on the count should not
                # silently proceed against incomplete data.
                malformed += 1
                print(f"WARN {sidecar}:{i} malformed JSON: {exc}", file=sys.stderr)
                continue
            if rec.get("confidence") != "high":
                continue
            if rec.get("category") not in ("bug", "security", "cross_component"):
                continue
            rule_id = rec.get("rule_id") or ""
            if rule_id in excluded_rules:
                continue
            n += 1
    except OSError:
        return -1
    if malformed:
        # Mirror the missing-sidecar signal: treat a sidecar with any
        # malformed lines as "cannot determine". Better to delay promotion
        # than to promote on under-counted data.
        print(
            f"WARN {sidecar} has {malformed} malformed line(s); "
            f"returning -1 to defer promotion decision.",
            file=sys.stderr,
        )
        return -1
    return n


def registry_exemplar_published(repo: str) -> bool:
    """True if this repo already has an exemplar."""
    try:
        data = json.loads(REGISTRY_PATH.read_text())
    except (OSError, json.JSONDecodeError):
        return False
    return bool((data.get("repos", {}).get(repo) or {}).get("exemplar_published"))


def issue_to_repo(title: str) -> str:
    """`Audit candidate: owner/name` → `owner/name`."""
    prefix = "Audit candidate: "
    return title[len(prefix):] if title.startswith(prefix) else title


def list_open_issues(label: str, json_fields: list[str]) -> list[dict]:
    # CRITICAL: `gh issue list` defaults to --limit 30. Without an
    # explicit higher limit, any label with >30 open issues silently
    # truncates — the batch-processor would invisibly skip work.
    # The daily-report had the same bug; both fixed 2026-05-12.
    #
    # We bypass the gh() helper here because we need stderr too. The
    # earlier `rc != 0 → []` reduction made auth/API errors look like
    # "no work to do" — invisible failure. On a non-zero rc we now log
    # the stderr explicitly and STILL return [] so the caller can fail
    # soft (the batch processor is a cron; missing one tick is preferable
    # to crashing). The visible stderr is what lets the failure be noticed.
    try:
        proc = subprocess.run(
            ["gh", "issue", "list", "--label", label, "--state", "open",
             "--limit", "1000", "--json", ",".join(json_fields)],
            capture_output=True, text=True, check=False,
        )
    except OSError as exc:
        print(
            f"WARN list_open_issues({label}): gh launch failed: {exc}",
            file=sys.stderr,
        )
        return []
    if proc.returncode != 0:
        print(
            f"WARN list_open_issues({label}): gh exited {proc.returncode}; "
            f"this run will see no work for label={label!r}. stderr below:",
            file=sys.stderr,
        )
        if proc.stderr:
            print(proc.stderr.rstrip(), file=sys.stderr)
        return []
    if not proc.stdout.strip():
        return []
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        print(
            f"WARN list_open_issues({label}): unparseable gh JSON: {exc}",
            file=sys.stderr,
        )
        return []


def workflow_active_count(workflow: str) -> int:
    rc, out = gh([
        "run", "list", "--workflow", workflow, "--status", "in_progress",
        "--json", "databaseId", "--jq", "length",
    ])
    try:
        return int((out or "0").strip())
    except ValueError:
        return 0


# ----- Phase implementations -----

def phase0_label_exemplars(dry_run: bool) -> int:
    """Label audit-complete issues with `case-study-clean` when they qualify.

    Qualification rule (v0.8.17):
      - score >= EXEMPLAR_THRESHOLD (default 90)
      - security != BLOCKED
      - registry has no `exemplar_published: true` for this repo
      - issue doesn't already have `case-study-clean` or `exemplar-published`

    Labels with `case-study-clean` AND dispatches `auditor-exemplar.yml`
    directly. The label is for visibility — both because the label is
    documented as the trigger in the workflow's `if:` clause, and because
    rule-health / future queries filter on it. The dispatch is because
    `gh issue edit` authenticated with GITHUB_TOKEN does NOT fire issue
    events (GHA security: tokens can't trigger workflows). The 2026-05-13
    v0.8.18 first deploy hit exactly this — 48 labels applied, zero
    exemplar workflows ever fired. phase1_promote dispatches contribute
    the same way for the same reason.

    We do NOT remove audit-complete or interfere with phase1's promotion
    to contribute-approved — the exemplar and contribute paths are
    parallel and both can be in flight on the same issue.
    """
    print("--- Phase 0: Label qualifying audits as exemplars ---")
    labeled = 0
    issues = list_open_issues("audit-complete", ["number", "title", "labels"])
    for issue in issues:
        labels = {l["name"] for l in issue.get("labels", [])}
        if "case-study-clean" in labels or "exemplar-published" in labels:
            continue
        num = issue["number"]
        repo = issue_to_repo(issue["title"])
        if registry_exemplar_published(repo):
            continue
        security = registry_security(repo)
        if security == "BLOCKED":
            continue
        score = registry_score(repo)
        if score < EXEMPLAR_THRESHOLD:
            continue
        print(f"  EXEMPLAR #{num} ({repo}): score={score} security={security} → case-study-clean + dispatch")
        if not dry_run:
            rc, _ = gh(["issue", "edit", str(num), "--add-label", "case-study-clean"])
            if rc != 0:
                print(f"    WARNING: failed to label {repo}")
                continue
            rc, _ = gh([
                "workflow", "run", "auditor-exemplar.yml",
                "-f", f"repo={repo}",
                "-f", f"issue_number={num}",
            ])
            if rc != 0:
                print(f"    WARNING: failed to dispatch exemplar for {repo}")
            time.sleep(DISPATCH_SLEEP)
        labeled += 1
    print(f"Labeled+dispatched: {labeled} audits as case-study-clean\n")
    return labeled


def phase1_promote(dry_run: bool) -> int:
    print("--- Phase 1: Promote completed audits to contribution ---")
    promoted = 0
    # v0.8.23 — compute the low-landing-rate rule set once per run.
    # Repos whose only findings are on these rules get skipped from
    # promotion. Empty set when suppression is disabled or the
    # rule-health computation fails (fail-soft).
    excluded = low_landing_rules()
    issues = list_open_issues("audit-complete", ["number", "title", "labels"])
    for issue in issues:
        labels = {l["name"] for l in issue.get("labels", [])}
        if "security-blocked" in labels or "contribute-approved" in labels \
                or "prs-submitted" in labels:
            continue
        num = issue["number"]
        repo = issue_to_repo(issue["title"])
        security = registry_security(repo)
        if security == "BLOCKED":
            print(f"  SKIP #{num} ({repo}): security BLOCKED")
            continue
        if security not in ("CLEAR", "REVIEW"):
            print(f"  SKIP #{num} ({repo}): security={security} (unknown/not audited)")
            continue

        # v0.8.21 — promote only when there's something to contribute. The
        # contribute workflow ships only `confidence == "high"` findings, so
        # an audit with zero of those would fire a workflow that does no
        # useful work and leaves the issue stuck at `contribute-approved`
        # forever. The 2026-05-19 status check found leowux/pony (#165)
        # stuck this way: score=91, no bugs, exemplar already published,
        # still promoted to contribute. -1 (no sidecar) keeps the old
        # promote-anyway behavior so older entries pre-sidecar don't get
        # silently skipped.
        #
        # v0.8.23 — `excluded` carries the low-landing-rate rule set, so
        # bug_count_eff reflects "findings worth shipping" rather than
        # raw count. We also compute the raw count for the log line, so
        # an operator can see when suppression is what dropped the audit.
        bug_count_raw = audit_high_conf_bug_count(repo)
        bug_count_eff = audit_high_conf_bug_count(repo, excluded_rules=excluded)
        if bug_count_eff == 0 and bug_count_raw == 0:
            print(f"  SKIP #{num} ({repo}): security={security} but 0 high-conf bugs — nothing to contribute")
            continue
        if bug_count_eff == 0 and bug_count_raw > 0:
            print(
                f"  SUPPRESS #{num} ({repo}): security={security}, "
                f"{bug_count_raw} high-conf bug(s) but ALL on low-landing-rate rules — "
                f"skipping promotion (NLPM_DISABLE_LOW_LANDING_SUPPRESSION=1 to override)"
            )
            continue

        eff_note = "?" if bug_count_eff < 0 else str(bug_count_eff)
        suppr_note = (
            f" (suppressed {bug_count_raw - bug_count_eff})"
            if bug_count_eff >= 0 and bug_count_raw > bug_count_eff
            else ""
        )
        print(
            f"  PROMOTE #{num} ({repo}): security={security}, "
            f"high-conf bugs={eff_note}{suppr_note} → contribute-approved"
        )
        if not dry_run:
            gh(["issue", "edit", str(num), "--add-label", "contribute-approved"])
            rc, _ = gh([
                "workflow", "run", "auditor-contribute.yml",
                "-f", f"repo={repo}",
                "-f", f"issue_number={num}",
            ])
            if rc != 0:
                print(f"    WARNING: failed to dispatch contribute for {repo}")
            time.sleep(DISPATCH_SLEEP)
        promoted += 1
    print(f"Promoted: {promoted} issues to contribute-approved\n")
    return promoted


def phase1_2_drain_contribute(dry_run: bool) -> int:
    print("--- Phase 1.2: Drain contribute-approved backlog ---")
    drained = 0
    failures = 0
    issues = list_open_issues("contribute-approved", ["number", "title", "labels"])
    # FIFO: smallest issue number first
    issues.sort(key=lambda i: i.get("number", 0))
    for issue in issues:
        if drained >= DRAIN_LIMIT:
            print(f"  STOP: drain limit {DRAIN_LIMIT} reached")
            break
        if failures >= 3:
            print(f"  ABORT: {failures} consecutive failures")
            break
        labels = {l["name"] for l in issue.get("labels", [])}
        if "prs-submitted" in labels:
            continue
        active = workflow_active_count("auditor-contribute.yml")
        if active >= DRAIN_LIMIT:
            print(f"  PAUSE: {active} contribute workflows already running, at capacity")
            break
        num = issue["number"]
        repo = issue_to_repo(issue["title"])
        print(f"  DISPATCH #{num} ({repo}) via workflow_dispatch")
        if not dry_run:
            rc, _ = gh([
                "workflow", "run", "auditor-contribute.yml",
                "-f", f"repo={repo}",
                "-f", f"issue_number={num}",
            ])
            if rc == 0:
                drained += 1
                failures = 0
                time.sleep(DISPATCH_SLEEP)
            else:
                print(f"    FAILED to dispatch contribute for {repo}")
                failures += 1
        else:
            drained += 1
    print(f"Drained: {drained} contribute-approved issues (failures: {failures})\n")
    return drained


def phase1_5_reopen_wrong(dry_run: bool) -> int:
    print("--- Phase 1.5: Reopen wrongly-closed discovered repos ---")
    reopened = 0
    rc, out = gh([
        "issue", "list", "--label", "audit-candidate", "--state", "closed",
        "--limit", "1000",
        "--json", "number,title",
    ])
    if rc != 0 or not out.strip():
        print("Reopened: 0 wrongly-closed issues\n")
        return 0
    try:
        issues = json.loads(out)
    except json.JSONDecodeError:
        issues = []
    for issue in issues:
        num = issue["number"]
        repo = issue_to_repo(issue["title"])
        if registry_status(repo) == "discovered":
            print(f"  REOPEN #{num} ({repo}): was closed but still status=discovered")
            if not dry_run:
                gh(["issue", "reopen", str(num)])
            reopened += 1
    print(f"Reopened: {reopened} wrongly-closed issues\n")
    return reopened


def phase2_pick_next(dry_run: bool, batch_size: int) -> tuple[int, int]:
    """Returns (picked, available)."""
    print("--- Phase 2: Pick next audit batch ---")
    running = workflow_active_count("auditor-audit.yml")
    print(f"Currently running audits: {running}")
    available = batch_size - running
    if available <= 0:
        print(f"Already {running} audits running (batch size {batch_size}). Skipping this cycle.")
        return 0, 0
    print(f"Will pick up to {available} new repos")

    rc, out = gh([
        "issue", "list", "--label", "audit-candidate", "--state", "open",
        "--limit", "1000",
        "--json", "number,title", "--jq", "sort_by(.number)",
    ])
    if rc != 0 or not out.strip():
        print("Picked: 0 repos for audit\n")
        return 0, available
    try:
        issues = json.loads(out)
    except json.JSONDecodeError:
        issues = []

    picked = 0
    for issue in issues:
        if picked >= available:
            break
        num = issue["number"]
        repo = issue_to_repo(issue["title"])
        status = registry_status(repo)
        if status not in ("none", "discovered"):
            print(f"  SKIP #{num} ({repo}): already in registry (status={status})")
            if not dry_run:
                gh([
                    "issue", "close", str(num),
                    "--comment", f"Already processed (status: {status}). Closing duplicate.",
                ])
            continue
        print(f"  PICK #{num} ({repo}) → audit-ready")
        if not dry_run:
            gh([
                "issue", "edit", str(num),
                "--add-label", "audit-ready",
                "--remove-label", "audit-candidate",
            ])
            rc, _ = gh([
                "workflow", "run", "auditor-audit.yml",
                "-f", f"repo={repo}",
                "-f", f"issue_number={num}",
            ])
            if rc != 0:
                print(f"    WARNING: failed to dispatch audit for {repo}")
            time.sleep(DISPATCH_SLEEP)
        picked += 1
    print(f"Picked: {picked} repos for audit\n")
    return picked, available


def phase3_retrigger_stuck(dry_run: bool, batch_size: int, available: int, picked: int) -> int:
    print("--- Phase 3: Re-trigger stuck audit-ready repos ---")
    limit = max(0, available - picked)
    if limit == 0:
        print("Re-triggered: 0 stuck audit-ready repos (no capacity)\n")
        return 0

    issues = list_open_issues("audit-ready", ["number", "title", "labels"])
    issues.sort(key=lambda i: i.get("number", 0))

    retriggered = 0
    failures = 0
    for issue in issues:
        if retriggered >= limit:
            break
        if failures >= RETRIGGER_FAILURE_CAP:
            print(f"  ABORT: {failures} consecutive failures, likely permissions issue")
            break
        labels = {l["name"] for l in issue.get("labels", [])}
        if "audit-complete" in labels:
            continue
        num = issue["number"]
        repo = issue_to_repo(issue["title"])
        # Terminal state: the auditor model refused this repo (offensive-
        # security content trips the model's cybersecurity safeguards, so no
        # report is ever produced). Never re-trigger — retrying always
        # refuses and burns a full audit run. The audit workflow removes
        # `audit-ready` when it marks a repo unsupported, so this normally
        # won't be listed here; guard anyway in case that removal failed,
        # and clean up the stale label so the dashboard stops counting it.
        if "audit-unsupported" in labels:
            print(f"  SKIP #{num} ({repo}): audit-unsupported (model refusal, terminal)")
            if not dry_run and "audit-ready" in labels:
                gh(["issue", "edit", str(num), "--remove-label", "audit-ready"])
            continue
        status = registry_status(repo)
        if status not in ("none", "discovered"):
            # The audit already ran for this repo (registry shows it
            # moved past `discovered`). The `audit-ready` label is
            # stale — the audit workflow's `--remove-label audit-ready`
            # call failed at some point, leaving the label stuck. Now
            # clean it up so the dashboard doesn't keep showing 12
            # "stuck" issues that are actually done.
            print(f"  SKIP #{num} ({repo}): already past audit (status={status}); cleaning stale audit-ready label")
            if not dry_run:
                gh([
                    "issue", "edit", str(num),
                    "--remove-label", "audit-ready",
                ])
            continue
        active = workflow_active_count("auditor-audit.yml")
        if active >= batch_size:
            print(f"  PAUSE: {active} audits running, at capacity")
            break
        print(f"  RETRIGGER #{num} ({repo}) via workflow_dispatch")
        if not dry_run:
            rc, _ = gh([
                "workflow", "run", "auditor-audit.yml",
                "-f", f"repo={repo}",
                "-f", f"issue_number={num}",
            ])
            if rc == 0:
                retriggered += 1
                failures = 0
                time.sleep(DISPATCH_SLEEP)
            else:
                print(f"    FAILED to trigger audit for {repo}")
                failures += 1
        else:
            retriggered += 1
    print(f"Re-triggered: {retriggered} stuck audit-ready repos (failures: {failures})\n")
    return retriggered


def print_summary() -> None:
    print("--- Summary ---")
    labels = [
        ("audit-candidate", "audit-candidate"),
        ("audit-ready", "audit-ready"),
        ("audit-complete", "audit-complete"),
        ("contribute-approved", "contribute-approved"),
        ("prs-submitted", "prs-submitted"),
    ]
    print("Pipeline state:")
    for label, name in labels:
        rc, out = gh([
            "issue", "list", "--label", label, "--state", "open",
            "--json", "number", "--jq", "length",
        ])
        count = (out or "?").strip() if rc == 0 else "?"
        print(f"  {name:21}: {count}")


def main() -> int:
    p = argparse.ArgumentParser()
    default_batch = int(os.environ.get("BATCH_SIZE", "5"))
    p.add_argument("--batch-size", type=int, default=default_batch)
    p.add_argument("--dry-run", action="store_true",
                   default=os.environ.get("DRY_RUN", "false") == "true")
    args = p.parse_args()

    if not (1 <= args.batch_size <= 50):
        print(f"ERROR: --batch-size must be in [1, 50] (got: {args.batch_size})",
              file=sys.stderr)
        return 1

    print("=== NLPM Batch Processor ===")
    print(f"Batch size: {args.batch_size} | Dry run: {args.dry_run}\n")

    phase0_label_exemplars(args.dry_run)
    phase1_promote(args.dry_run)
    phase1_2_drain_contribute(args.dry_run)
    phase1_5_reopen_wrong(args.dry_run)
    picked, available = phase2_pick_next(args.dry_run, args.batch_size)
    phase3_retrigger_stuck(args.dry_run, args.batch_size, available, picked)
    print_summary()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
