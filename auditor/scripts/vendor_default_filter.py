#!/usr/bin/env python3
"""Vendor-default exclusion filter for discovery.

Drops candidate repos whose owner is on a list of orgs the contribute
pipeline cannot meaningfully ship PRs to:

  - **DENY_OWNERS** (no-external-PRs): repos owned by orgs whose policy
    forbids external PR contributions outright. anthropics/* is the
    canonical case — 3 of 3 prior NLPM PRs against it were rejected as
    a policy matter, not on technical merit.
  - **CLA_REQUIRED_OWNERS**: orgs requiring a signed CLA on every
    commit. Without `vars.GOOGLE_CLA_SIGNED == 'true'` + the
    CONTRIBUTE_AUTHOR_* identity matching the CLA signer, PRs land but
    stall on `cla/google` FAILURE indefinitely (see the auditor-
    contribute policy gates).
  - **ECOSYSTEM_VENDORS**: AI/CLI ecosystem owners whose plugins are
    typically reference implementations or first-party tooling, not
    third-party plugin authoring. Auditing them produces low-signal
    findings the maintainer was already aware of.

NLPM's contribute workflow has runtime policy gates for the first two
categories (policy_denied, policy_cla_required) — but those fire LATE,
after the audit cost has been paid. Filtering at discovery time saves
the API calls + LLM tokens entirely.

This file is the single source of truth. The lists are intentionally
short — broad denylists cause silent drops of repos that would have
been good audits. Add an owner only when there's a documented reason
the contribute pipeline cannot land a PR there.

Usage (CLI, for piping JSONL through):

    cat candidates.jsonl | \\
      python3 auditor/scripts/vendor_default_filter.py > kept.jsonl

    # Or in dry-mode for inspection:
    cat candidates.jsonl | \\
      python3 auditor/scripts/vendor_default_filter.py --report

Library:

    from vendor_default_filter import is_vendor_default
    skip, reason = is_vendor_default("anthropics/claude-code")
"""
from __future__ import annotations

import argparse
import json
import sys


# Hard policy: these orgs reject external PRs as a stated policy.
# Confirmed empirically per NLPM's auditor-contribute policy gate.
DENY_OWNERS: frozenset[str] = frozenset({
    "anthropics",
})

# Repo-specific hard deny (finer than owner-wide). Use when one repo
# under an owner blocks contribution but the owner's other repos don't.
#
#   - openai/codex, openai/codex-action: per docs/contributing.md +
#     close-stale-contributor-prs.yml, OpenAI AUTO-CLOSES unsolicited
#     external PRs (14-day stale auto-close). nlpm's PRs are unsolicited
#     by definition, so they'd be closed unreviewed regardless of the
#     CLA. (The repos ALSO require a signed CLA — status check named
#     `cla`, exact match, comment-based not commit-author-based — but
#     the auto-close is the dominant blocker.) Researched 2026-05-26;
#     sources: openai/codex docs/CLA.md, docs/contributing.md,
#     .github/workflows/cla.yml. Owner-wide deny is wrong here:
#     openai/openai-python etc. have no CLA and aren't NL-artifact repos
#     anyway, so they'd never pass the artifact probe.
DENY_REPOS: frozenset[str] = frozenset({
    "openai/codex",
    "openai/codex-action",
})

# CLA-gated: PRs land but block on signed-commit verification unless
# the contribute identity matches the CLA signer. The current GHA
# setup uses claude-code-action's bot identity which is not CLA-
# signed, so PRs to these orgs stall by default. See AGENTS.md
# "Policy Gates" section.
CLA_REQUIRED_OWNERS: frozenset[str] = frozenset({
    "google",
    "google-gemini",
    "googleworkspace",
    "google-labs-code",
    "googleapis",
    "googlecloudplatform",
    # Google-operated org under a non-"google*" name. Confirmed
    # 2026-05-26: ChromeDevTools/chrome-devtools-mcp PR #2122 was gated
    # by `cla/google` — the org uses Google's CLA bot despite the name.
    # The maintainer signs the CONTRIBUTE_AUTHOR identity is CLA-covered
    # (so PRs CAN pass), but the policy choice is to keep Google orgs
    # filtered at discovery (conservative — avoid unsolicited PRs to a
    # major vendor). Add other Google-operated orgs here as encountered
    # (e.g. GoogleChrome, googlemaps) — keep the list documented, not
    # speculative.
    "chromedevtools",
})

# First-party / reference-implementation owners. Auditing produces
# findings the maintainer already knows about; rejected on signal
# grounds rather than policy.
#
# Empty for now — left as a documented hook. NLPM's contribute history
# has not yet justified adding any specific owner here.
ECOSYSTEM_VENDORS: frozenset[str] = frozenset()


def is_vendor_default(repo: str) -> tuple[bool, str]:
    """Decide whether `repo` (owner/name) should be dropped at discovery.

    Returns `(should_drop, reason)`. `reason` is empty when not dropping.
    `reason` is short and intended for logs / event records.
    """
    if "/" not in repo:
        return False, ""
    if repo.lower() in DENY_REPOS:
        return True, f"deny-repo:{repo.lower()} (unsolicited external PRs auto-closed)"
    owner = repo.split("/", 1)[0].lower()
    if owner in DENY_OWNERS:
        return True, f"deny:{owner} (policy: no external PRs)"
    if owner in CLA_REQUIRED_OWNERS:
        return True, f"cla-required:{owner} (commits must be CLA-signed)"
    if owner in ECOSYSTEM_VENDORS:
        return True, f"vendor:{owner} (first-party / reference)"
    return False, ""


def _iter_jsonl(stream) -> "list[dict]":
    """Read JSONL from `stream`, skipping blank and malformed lines.

    Returns the accumulated records. Malformed lines emit a warning to
    stderr and are dropped — matching the rest of NLPM's JSONL readers.
    """
    out: list[dict] = []
    for i, line in enumerate(stream, 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as exc:
            print(f"WARN stdin:{i} malformed JSON: {exc}", file=sys.stderr)
    return out


def _extract_repo(record: dict) -> str | None:
    """Read the owner/name key out of a candidate record.

    Accepts either `fullName` (the gh-search shape used by NLPM's
    discover workflow) or `repo_name` (the BQ shape). Returns None
    when neither is present.
    """
    return record.get("fullName") or record.get("repo_name")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--report", action="store_true",
                        help="emit a stderr summary of dropped owners")
    args = parser.parse_args(argv)

    records = _iter_jsonl(sys.stdin)

    kept: list[dict] = []
    drop_counts: dict[str, int] = {}
    for rec in records:
        repo = _extract_repo(rec)
        if not repo:
            # Unknown shape — pass through. Better to let the
            # downstream artifact-probe see it than to silently drop.
            kept.append(rec)
            continue
        skip, reason = is_vendor_default(repo)
        if skip:
            drop_counts[reason] = drop_counts.get(reason, 0) + 1
            continue
        kept.append(rec)

    for rec in kept:
        print(json.dumps(rec, ensure_ascii=False))

    if drop_counts or args.report:
        print(
            f"vendor-default filter: kept {len(kept)} of {len(records)}; "
            f"dropped {len(records) - len(kept)}",
            file=sys.stderr,
        )
        for reason, n in sorted(drop_counts.items(), key=lambda kv: -kv[1]):
            print(f"  {n:>4}  {reason}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
