#!/usr/bin/env bash
# Resolve merge conflicts for auditor-managed files using the right strategy per file.
#
# Called while a rebase (or merge) of this workflow's commit onto the latest
# main is stopped on conflicts: by commit-via-pr.sh's reconcile loop,
# unstick-bot-prs.sh and git-push-with-retry.sh. "Mine" below means the
# commit this workflow is trying to land; "upstream" means what already
# reached main.
#
# Strategies:
#   auditor/registry/repos.json  → 3-way merge (mine wins on overlap, union on additions)
#   append-only *.jsonl logs     → line union (upstream lines first, then mine; dedupe)
#   auditor/exemplars/README.md  → regenerate from disk
#   everything else              → mine (keep this commit's work; never silently revert to upstream)
#
# Why "mine" as default: the previous default silently dropped the current
# workflow's own data whenever a concurrent push beat it to main. Lost
# pipeline_prs on wshobson/agents #488-#492 is a concrete example.
#
# Stage mapping — the part that is easy to get backwards. Git's :2/--ours and
# :3/--theirs are relative to the operation, not to "this workflow":
#   merge  (git pull --no-rebase): :2/--ours = mine,     :3/--theirs = upstream
#   rebase (git pull --rebase, git rebase origin/main):
#                                  :2/--ours = upstream, :3/--theirs = mine
# Every caller rebases. Until 2026-09-30 this script assumed the merge
# mapping, so during those rebases the registry's "ours wins on overlap" and
# the "--ours for everything else" default both kept upstream and silently
# discarded the bot commit's own version. The mapping is now detected below.

set -euo pipefail

# Use a per-run temp directory so concurrent resolver runs (multiple
# auditor workflows hitting a push-conflict at the same instant) can't
# stomp on each other's /tmp/reg-*.json or /tmp/log-*.jsonl staging files.
RESOLVE_TMPDIR=$(mktemp -d -t nlpm-resolve.XXXXXX)
trap 'rm -rf "$RESOLVE_TMPDIR"' EXIT

conflicted_paths() {
  git diff --name-only --diff-filter=U 2>/dev/null || true
}

# Detect whether we are inside a rebase and map stages accordingly (see header).
if [ -d "$(git rev-parse --git-path rebase-merge)" ] || [ -d "$(git rev-parse --git-path rebase-apply)" ]; then
  MINE_STAGE=3; UPSTREAM_STAGE=2; MINE_SIDE=--theirs
else
  MINE_STAGE=2; UPSTREAM_STAGE=3; MINE_SIDE=--ours
fi

# Registry: 3-way merge preserves remote updates to entries this workflow
# didn't touch. The previous strategy (`jq -s '.[0] * .[1]' theirs ours`)
# was a 2-way recursive merge with ours-wins, which silently reverted
# remote updates whenever this workflow's checkout was stale. Concrete
# symptom: audit commits flipping unrelated entries (e.g.,
# kepano/obsidian-skills) back to status=discovered/score=null on every
# concurrent push. The 3-way merge uses git's BASE (:1) to distinguish
# "current workflow changed this field" from "field is the same as
# checkout-time." Only fields the current workflow actually modified
# come from ours; everything else takes the remote version.
#
# Validate the merged result before writing — a malformed merge would
# silently corrupt the registry on disk (observed 2026-04-28: an
# unguarded merge produced two concatenated top-level objects).
if conflicted_paths | grep -qx "auditor/registry/repos.json"; then
  echo "Resolving auditor/registry/repos.json via 3-way merge"
  git show :1:auditor/registry/repos.json > "$RESOLVE_TMPDIR/reg-base.json"   # merge base
  git show ":${MINE_STAGE}:auditor/registry/repos.json" > "$RESOLVE_TMPDIR/reg-ours.json"       # this commit
  git show ":${UPSTREAM_STAGE}:auditor/registry/repos.json" > "$RESOLVE_TMPDIR/reg-theirs.json" # upstream
  python3 auditor/scripts/three-way-merge-registry.py \
      "$RESOLVE_TMPDIR/reg-base.json" "$RESOLVE_TMPDIR/reg-ours.json" "$RESOLVE_TMPDIR/reg-theirs.json" \
      > "$RESOLVE_TMPDIR/reg.json" \
    || { echo "ERROR: three-way merge failed; refusing to write"; exit 1; }
  REG_TMP="$RESOLVE_TMPDIR/reg.json" bash auditor/scripts/atomic-registry-write.sh
  git add auditor/registry/repos.json
fi

# Append-only logs: union both sides, dedupe identical lines.
#
# Why findings.jsonl was added 2026-05-01: per-audit sidecars contained
# 2,279 finding entries cumulatively, but only 644 (28%) had reached the
# global log. Investigation traced the gap to the same race that
# previously corrupted the registry: two parallel audits both append
# findings, the loser pulls and runs this resolver, the previous
# `--ours` fallback dropped the remote's appended findings entirely.
# Result: rule-health metrics systematically undercounted by ~3-4×,
# every per-rule precision number was wrong, BUG-missing-frontmatter
# and SEC-curl-pipe-sh false-positive ratios were wildly off.
#
# disagreements.jsonl has the same shape and the same race, so it
# joins the union list defensively rather than waiting for a similar
# investigation to surface a similar gap.
for log in auditor/logs/events.jsonl auditor/findings.jsonl auditor/disagreements.jsonl; do
  if conflicted_paths | grep -qx "$log"; then
    echo "Resolving $log via line union"
    git show ":${MINE_STAGE}:$log" > "$RESOLVE_TMPDIR/log-mine.jsonl"
    git show ":${UPSTREAM_STAGE}:$log" > "$RESOLVE_TMPDIR/log-upstream.jsonl"
    cat "$RESOLVE_TMPDIR/log-upstream.jsonl" "$RESOLVE_TMPDIR/log-mine.jsonl" | awk '!seen[$0]++' > "$log"
    git add "$log"
  fi
done

# Exemplar gallery: regenerate from disk. The gallery is deterministic
# from the auditor/exemplars/ directory — running build-exemplar-gallery.py
# after the rebase has staged both sides' new exemplar files produces the
# correct union view. Picking --ours here would silently revert exemplar
# entries from concurrent runs (observed during the 2026-05-13 bulk-seed:
# the gallery committed by the last winning push said "Total exemplars: 8"
# while disk had 61 because each parallel run kept its own snapshot).
if conflicted_paths | grep -qx "auditor/exemplars/README.md"; then
  echo "Resolving auditor/exemplars/README.md via regenerate-from-disk"
  # Accept either side's blob temporarily to clear the conflict, then
  # overwrite with the freshly regenerated gallery.
  git checkout "$MINE_SIDE" auditor/exemplars/README.md
  python3 auditor/scripts/build-exemplar-gallery.py >/dev/null
  git add auditor/exemplars/README.md
fi

# Everything else: prefer mine so the current workflow's work survives
conflicted_paths | while read -r f; do
  [ -z "$f" ] && continue
  echo "Resolving $f via $MINE_SIDE (this commit's version)"
  git checkout "$MINE_SIDE" "$f"
  git add "$f"
done
