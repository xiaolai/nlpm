#!/usr/bin/env python3
"""Render the auditor's cross-repo aggregate HTML dashboard.

Aggregates the append-only logs (findings.jsonl, vocab-advisories.jsonl,
events.jsonl) and the repos registry into a single self-contained HTML
file under `auditor/reports/dashboard.html`. Uses the same templates and
vendored G6 as the per-repo `/nlpm:report` command — assets are copied
out so the dashboard works under `file://`.

Stdlib only. Run from the repository root:

    python3 auditor/scripts/render-dashboard.py
    python3 auditor/scripts/render-dashboard.py --since 2026-05-01
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = ROOT / "templates" / "report"
AUDITOR = ROOT / "auditor"
DOCS_BUILDER = ROOT / "bin" / "nlpm-build-docs"


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def filter_since(records: list[dict], since: str | None, field: str = "timestamp") -> list[dict]:
    if not since:
        return records
    return [r for r in records if r.get(field, "") >= since]


def build_repo_table(findings: list[dict], advisories: list[dict], registry: dict) -> list[dict]:
    """Per-repo row: latest score, security, finding count, vocab drift count."""
    repo_findings: dict[str, list[dict]] = defaultdict(list)
    for f in findings:
        repo_findings[f.get("repo", "?")].append(f)

    repo_advisories: dict[str, list[dict]] = defaultdict(list)
    for a in advisories:
        repo_advisories[a.get("repo", "?")].append(a)

    repos = registry.get("repos", {}) if isinstance(registry, dict) else {}
    seen: set[str] = set()
    rows: list[dict] = []

    # Start from registry order (deterministic) plus any repos seen only in findings.
    iter_keys = list(repos.keys()) if isinstance(repos, dict) else []
    iter_keys += [r for r in repo_findings.keys() if r not in iter_keys]

    for repo in iter_keys:
        info = repos.get(repo, {}) if isinstance(repos, dict) else {}
        repo_f = repo_findings.get(repo, [])
        repo_a = repo_advisories.get(repo, [])
        high = sum(1 for f in repo_f if f.get("confidence") == "high")
        med = sum(1 for f in repo_f if f.get("confidence") == "medium")
        rows.append({
            "repo": repo,
            "status": info.get("status", "unknown") if isinstance(info, dict) else "unknown",
            "stars": info.get("stars") if isinstance(info, dict) else None,
            "score": info.get("score") if isinstance(info, dict) else None,
            "security": info.get("security") if isinstance(info, dict) else None,
            "total_findings": len(repo_f),
            "high_findings": high,
            "medium_findings": med,
            "vocab_drift_count": len(repo_a),
            "vocab_drift_high": sum(1 for a in repo_a if a.get("confidence") == "high"),
        })
        seen.add(repo)
    rows.sort(key=lambda r: (-(r["total_findings"] or 0), r["repo"]))
    return rows


def build_rule_distribution(findings: list[dict]) -> list[dict]:
    """Top rules by occurrence across all repos."""
    counts: Counter[str] = Counter()
    repos_per_rule: dict[str, set[str]] = defaultdict(set)
    for f in findings:
        rule = f.get("rule_id") or "UNCLASSIFIED"
        counts[rule] += 1
        repos_per_rule[rule].add(f.get("repo", "?"))
    out = []
    for rule, total in counts.most_common(25):
        out.append({
            "rule_id": rule,
            "total": total,
            "repos_affected": len(repos_per_rule[rule]),
        })
    return out


def build_drift_network(advisories: list[dict]) -> dict:
    """Cross-repo vocab-drift graph.

    Each unique term becomes a node. Two terms get an edge when they
    co-occur in at least one drift cluster (in any repo). Edge weight is
    the number of repos that share the cluster.
    """
    term_freq: Counter[str] = Counter()
    term_repos: dict[str, set[str]] = defaultdict(set)
    pair_repos: dict[tuple[str, str], set[str]] = defaultdict(set)

    for a in advisories:
        repo = a.get("repo", "?")
        terms = sorted(set(a.get("terms", [])))
        for t in terms:
            term_freq[t] += 1
            term_repos[t].add(repo)
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                pair_repos[(terms[i], terms[j])].add(repo)

    nodes = [
        {"id": t, "label": t, "freq": c, "repos": sorted(term_repos[t])}
        for t, c in term_freq.most_common(60)
    ]
    node_ids = {n["id"] for n in nodes}
    edges = []
    for (a, b), repos in pair_repos.items():
        if a in node_ids and b in node_ids and len(repos) >= 1:
            edges.append({
                "source": a,
                "target": b,
                "weight": len(repos),
                "repos": sorted(repos),
            })
    edges.sort(key=lambda e: -e["weight"])
    return {"nodes": nodes, "edges": edges}


def build_activity_timeline(events: list[dict]) -> list[dict]:
    """Daily counts of audits, contributions, advisories."""
    by_day: dict[str, Counter[str]] = defaultdict(Counter)
    for e in events:
        ts = e.get("timestamp", "")
        if not ts or len(ts) < 10:
            continue
        day = ts[:10]
        ev = e.get("event", "?")
        by_day[day][ev] += 1
    out = []
    for day in sorted(by_day.keys()):
        out.append({"day": day, "counts": dict(by_day[day])})
    return out


def build_summary(findings: list[dict], advisories: list[dict], rows: list[dict]) -> dict:
    return {
        "total_repos": len(rows),
        "total_findings": len(findings),
        "high_findings": sum(1 for f in findings if f.get("confidence") == "high"),
        "total_advisories": len(advisories),
        "high_advisories": sum(1 for a in advisories if a.get("confidence") == "high"),
        "repos_with_drift": sum(1 for r in rows if r["vocab_drift_count"] > 0),
        "repos_blocked": sum(1 for r in rows if (r.get("security") or "").upper() == "BLOCKED"),
    }


def render(data: dict, out_dir: Path) -> Path:
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Copy vendor + assets next to the dashboard so it works under file://
    vendor_dst = out_dir / "vendor"
    assets_dst = out_dir / "assets"
    if vendor_dst.exists():
        shutil.rmtree(vendor_dst)
    if assets_dst.exists():
        shutil.rmtree(assets_dst)
    shutil.copytree(TEMPLATE_DIR / "vendor", vendor_dst)
    shutil.copytree(TEMPLATE_DIR / "assets", assets_dst)

    template = (TEMPLATE_DIR / "dashboard.html").read_text(encoding="utf-8")
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    ts = data.get("generated_at") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    html = (
        template
        .replace("{{GENERATED_AT}}", ts)
        .replace("{{DATA_JSON}}", data_json)
    )
    target = out_dir / "dashboard.html"
    target.write_text(html, encoding="utf-8")

    # Build docs alongside so the dashboard's rule_id badges resolve to
    # anchored sections in the framework guide.
    try:
        subprocess.run(
            [sys.executable, str(DOCS_BUILDER), "--out", str(out_dir / "docs")],
            check=False, capture_output=True,
        )
    except Exception as e:
        print(f"warning: docs build failed: {e}", file=sys.stderr)

    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--since", default=None, help="ISO date (YYYY-MM-DD) — drop records older than this")
    parser.add_argument("--out", default=str(AUDITOR / "reports"), help="Output directory for dashboard.html")
    args = parser.parse_args(argv)

    findings = read_jsonl(AUDITOR / "findings.jsonl")
    advisories = read_jsonl(AUDITOR / "vocab-advisories.jsonl")
    events = read_jsonl(AUDITOR / "logs" / "events.jsonl")
    registry = read_json(AUDITOR / "registry" / "repos.json", {})

    if args.since:
        findings = filter_since(findings, args.since)
        advisories = filter_since(advisories, args.since)
        events = filter_since(events, args.since)

    rows = build_repo_table(findings, advisories, registry)
    summary = build_summary(findings, advisories, rows)

    data = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "since": args.since,
        "summary": summary,
        "repo_rows": rows,
        "rule_distribution": build_rule_distribution(findings),
        "drift_network": build_drift_network(advisories),
        "activity_timeline": build_activity_timeline(events),
    }

    result = render(data, Path(args.out))
    print(f"Wrote {result}")
    print(f"  Repos: {summary['total_repos']}")
    print(f"  Findings: {summary['total_findings']} ({summary['high_findings']} high)")
    print(f"  Vocab advisories: {summary['total_advisories']} ({summary['high_advisories']} high)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
