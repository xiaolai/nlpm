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
    rc, out = gh([
        "issue", "list", "--label", label, "--state", "open",
        "--limit", "1000",
        "--json", ",".join(json_fields),
    ])
    if rc != 0 or not out.strip():
        return []
    try:
        return json.loads(out)
    except json.JSONDecodeError:
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
        elif security in ("CLEAR", "REVIEW"):
            print(f"  PROMOTE #{num} ({repo}): security={security} → contribute-approved")
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
        else:
            print(f"  SKIP #{num} ({repo}): security={security} (unknown/not audited)")
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
