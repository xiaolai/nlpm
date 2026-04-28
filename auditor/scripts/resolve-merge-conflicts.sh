#!/usr/bin/env bash
# Resolve merge conflicts for auditor-managed files using the right strategy per file.
#
# Called by push-retry loops in auditor-audit.yml, auditor-contribute.yml,
# and auditor-daily-report.yml after `git pull` when a concurrent push has
# created conflicts. Uses :2 (ours = this commit) and :3 (theirs = remote).
#
# Strategies:
#   auditor/registry/repos.json  → jq deep merge (ours wins on overlap, union on additions)
#   auditor/logs/events.jsonl    → line union (concat + dedupe, preserves events from both sides)
#   everything else              → --ours (keep this commit's work; never silently revert to remote)
#
# Why `--ours` as default: the previous `--theirs` default silently dropped
# the current workflow's own data whenever a concurrent push beat it to main.
# Lost pipeline_prs on wshobson/agents #488-#492 is a concrete example.

set -euo pipefail

conflicted_paths() {
  git diff --name-only --diff-filter=U 2>/dev/null || true
}

# Registry: deep merge preserves fields from both sides.
# Validate the merged result before writing — a malformed merge would
# silently corrupt the registry on disk (observed 2026-04-28: an
# unguarded merge produced two concatenated top-level objects).
if conflicted_paths | grep -qx "auditor/registry/repos.json"; then
  echo "Resolving auditor/registry/repos.json via jq deep merge"
  git show :2:auditor/registry/repos.json > /tmp/reg-ours.json
  git show :3:auditor/registry/repos.json > /tmp/reg-theirs.json
  jq -s '.[0] * .[1]' /tmp/reg-theirs.json /tmp/reg-ours.json > /tmp/reg.json
  REG_TMP=/tmp/reg.json bash auditor/scripts/atomic-registry-write.sh
  git add auditor/registry/repos.json
fi

# Event log: append-union of both sides
if conflicted_paths | grep -qx "auditor/logs/events.jsonl"; then
  echo "Resolving auditor/logs/events.jsonl via line union"
  git show :2:auditor/logs/events.jsonl > /tmp/ev-ours.jsonl
  git show :3:auditor/logs/events.jsonl > /tmp/ev-theirs.jsonl
  cat /tmp/ev-theirs.jsonl /tmp/ev-ours.jsonl | awk '!seen[$0]++' > auditor/logs/events.jsonl
  git add auditor/logs/events.jsonl
fi

# Everything else: prefer ours so the current workflow's work survives
conflicted_paths | while read -r f; do
  [ -z "$f" ] && continue
  echo "Resolving $f via --ours"
  git checkout --ours "$f"
  git add "$f"
done
