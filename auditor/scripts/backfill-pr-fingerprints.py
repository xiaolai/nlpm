#!/usr/bin/env python3
"""Backfill `prs[].fingerprints[]` for pre-v0.7.7 engagements.

Legacy PRs submitted before the `nlpm-metadata` block shipped have
empty `fingerprints` arrays in `auditor/registry/repos.json`. Without
them, `diff-findings.py` cannot attribute a fixed finding to the PR
that fixed it — every resolution lands on `fixed_upstream_not_merged`,
flattening the case-study story.

This backfill does imperfect but honest file-level attribution: for
each PR, fetch its changed-files list from GitHub. For every finding
in the synthesized sidecar whose `file` path matches a changed file,
add that finding's fingerprint to the PR's list. If two PRs touched
the same file, both get the fingerprint — the diff's precedence rules
handle tie-breaking (merged > applied_separately > open > rejected).

This overclaims: a PR that changed `agents/foo.md` for reason A will
get credited for finding B in the same file. But the alternative —
crediting no PR for anything — is a worse misrepresentation. The
case-study writer prompt acknowledges the looseness in the Limitations
section.

Usage:
    backfill-pr-fingerprints.py --repo owner/name
    backfill-pr-fingerprints.py --all

--all walks every repo in the registry that has PRs but no
fingerprints AND has a findings sidecar available.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


REGISTRY = Path("auditor/registry/repos.json")
AUDITS_DIR = Path("auditor/audits")


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text())


def save_registry(registry: dict) -> None:
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n")


def compute_fingerprint(repo: str, finding: dict) -> str:
    """Must match auditor/scripts/compute-fingerprint.sh exactly.
    See SCHEMAS.md §fingerprint — payload includes trailing newline."""
    def _stringify(v, if_falsy=""):
        if v is None or v is False:
            return if_falsy
        if v is True:
            return "true"
        if isinstance(v, int):
            return str(v)
        if isinstance(v, float):
            return str(int(v)) if v.is_integer() else repr(v)
        if isinstance(v, str):
            return v
        return str(v)

    file_ = _stringify(finding.get("file"))
    rule_id = _stringify(finding.get("rule_id"))
    pattern = _stringify(finding.get("pattern"))
    line_str = _stringify(finding.get("line"), "null")
    payload = f"{repo}|{file_}|{rule_id}|{pattern}|{line_str}\n"
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_sidecar_findings(slug: str) -> list[dict]:
    path = AUDITS_DIR / f"{slug}.findings.jsonl"
    if not path.exists():
        return []
    records = []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return records


def fetch_pr_files(repo: str, pr_number: int) -> list[str]:
    """Return the list of file paths a PR touched.

    Uses `gh pr view --json files` which returns a paginated list.
    Large PRs (>100 files) may be truncated — gh handles pagination
    transparently up to a cap. For legacy cleanup PRs this is fine;
    they touch a handful of files each."""
    try:
        result = subprocess.run(
            ["gh", "pr", "view", str(pr_number), "--repo", repo,
             "--json", "files"],
            capture_output=True, text=True, check=True, timeout=30,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"WARN: gh pr view failed for {repo}#{pr_number}: {e}",
              file=sys.stderr)
        return []
    data = json.loads(result.stdout)
    return [f.get("path", "") for f in data.get("files", []) if f.get("path")]


def normalize_path(path: str) -> str:
    """Strip leading './' and compare case-sensitively. The synthesizer
    sometimes records paths with leading dots or trailing slashes
    (e.g., `agents/droids/` for 'all files in this dir')."""
    return path.lstrip("./").rstrip("/")


def _path_tail_match(shorter: str, longer: str) -> bool:
    """True if `shorter` is a suffix of `longer` at directory boundaries,
    AND the overlap contains at least one directory separator (so a bare
    `README.md` doesn't false-match every README in the tree).

    Real case: sidecar records `antigravity-awesome-skills/skills/foo/SKILL.md`
    because that's how the audit saw it (repo is an aggregator with per-plugin
    subdirs). A PR touched `skills/foo/SKILL.md` (post-restructure, or from
    a different vantage). Both refer to the same file."""
    if not shorter or not longer:
        return False
    if "/" not in shorter:
        return False
    if not longer.endswith(shorter):
        return False
    # Longer must have a `/` immediately before the start of `shorter`
    # so we don't false-match partial filenames.
    prefix_len = len(longer) - len(shorter)
    if prefix_len == 0:
        return True  # exact match
    return longer[prefix_len - 1] == "/"


def find_matching_findings(
    pr_files: list[str],
    sidecar_findings: list[dict],
) -> list[dict]:
    """Return every sidecar finding whose `file` path matches a file
    the PR touched. Match rules, in order of strictness:

      1. Exact normalized match.
      2. PR file falls under a sidecar descriptive directory prefix
         (e.g., sidecar `agents/droids/` matches PR `agents/droids/foo.md`).
      3. Glob-like sidecar path (`workflows/best-practice/*-agent.md`)
         matches any PR file conforming to that glob.
      4. Path-tail match in EITHER direction — the shorter path (with
         at least one `/`) is a suffix of the longer at a directory
         boundary. Covers aggregator repos where sidecar has an extra
         leading subdir (or PR does).
    """
    pr_set = {normalize_path(p) for p in pr_files}
    matches: list[dict] = []
    for f in sidecar_findings:
        fpath = normalize_path(f.get("file", ""))
        if not fpath:
            continue
        # Rule 1: exact match.
        if fpath in pr_set:
            matches.append(f)
            continue
        # Rule 2: descriptive prefix.
        if any(p.startswith(fpath + "/") for p in pr_set):
            matches.append(f)
            continue
        # Rule 3: glob.
        if "*" in fpath:
            glob_regex = re.escape(fpath).replace(r"\*", r"[^/]*")
            if any(re.fullmatch(glob_regex, p) for p in pr_set):
                matches.append(f)
                continue
        # Rule 4: path-tail match in either direction.
        if any(
            _path_tail_match(fpath, p) or _path_tail_match(p, fpath)
            for p in pr_set
        ):
            matches.append(f)
    return matches


def backfill_one(repo: str, registry: dict, dry_run: bool = False) -> int:
    """Mutate registry in place for one repo. Returns the number of
    fingerprints attributed."""
    slug = repo.replace("/", "-")
    repo_entry = registry.get("repos", {}).get(repo)
    if not repo_entry:
        print(f"SKIP {repo}: not in registry")
        return 0

    prs = repo_entry.get("prs", []) or []
    if not prs:
        print(f"SKIP {repo}: no PRs")
        return 0

    # If ANY PR already has fingerprints, this repo was post-v0.7.7
    # and we should leave it alone.
    if any(pr.get("fingerprints") for pr in prs):
        print(f"SKIP {repo}: already has fingerprints")
        return 0

    sidecar_findings = load_sidecar_findings(slug)
    if not sidecar_findings:
        print(f"SKIP {repo}: no sidecar at {AUDITS_DIR}/{slug}.findings.jsonl")
        return 0

    total_attributed = 0
    for pr in prs:
        pr_number = pr.get("number")
        if not isinstance(pr_number, int):
            continue
        pr_files = fetch_pr_files(repo, pr_number)
        if not pr_files:
            continue
        matches = find_matching_findings(pr_files, sidecar_findings)
        if not matches:
            continue
        fingerprints = [compute_fingerprint(repo, f) for f in matches]
        rule_ids = [f.get("rule_id", "UNCLASSIFIED") for f in matches]
        # Preserve any existing entries (there won't be any for legacy
        # PRs but belt-and-suspenders).
        pr["fingerprints"] = list(dict.fromkeys(
            (pr.get("fingerprints") or []) + fingerprints
        ))
        pr["rule_ids"] = list(dict.fromkeys(
            (pr.get("rule_ids") or []) + rule_ids
        ))
        pr["fingerprints_backfilled"] = True  # provenance flag
        total_attributed += len(fingerprints)
        print(f"  PR #{pr_number}: {len(pr_files)} files touched → "
              f"{len(matches)} findings attributed")

    if dry_run:
        print(f"{repo}: {total_attributed} fingerprints would be attributed "
              f"(dry-run, not saved)")
    else:
        print(f"{repo}: {total_attributed} fingerprints attributed")
    return total_attributed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="Single repo (owner/name)")
    parser.add_argument("--all", action="store_true",
                        help="Backfill every pre-v0.7.7 legacy engagement")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.repo and not args.all:
        parser.error("Specify --repo or --all")

    registry = load_registry()

    if args.repo:
        backfill_one(args.repo, registry, dry_run=args.dry_run)
    else:
        # Walk every repo with PRs but no fingerprints AND an available sidecar.
        candidates = []
        for repo, entry in registry.get("repos", {}).items():
            prs = entry.get("prs") or []
            if not prs:
                continue
            if any(pr.get("fingerprints") for pr in prs):
                continue
            slug = repo.replace("/", "-")
            if (AUDITS_DIR / f"{slug}.findings.jsonl").exists():
                candidates.append(repo)
        print(f"Candidates for backfill: {len(candidates)}")
        total = 0
        for repo in candidates:
            total += backfill_one(repo, registry, dry_run=args.dry_run)
        print(f"\nTotal: {total} fingerprints attributed across "
              f"{len(candidates)} repos")

    if not args.dry_run:
        save_registry(registry)
        print(f"Registry saved → {REGISTRY}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
