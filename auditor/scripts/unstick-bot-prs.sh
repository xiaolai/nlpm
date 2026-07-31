#!/usr/bin/env bash
# unstick-bot-prs.sh — reconcile any open auditor-bot PR that conflicts
# with main, so shared-log collisions never pile up.
#
# Why this exists:
#   commit-via-pr.sh opens one bot PR per auditor commit and auto-merges
#   it. Two bot PRs that touch the same append-only file (events.jsonl,
#   repos.json, findings.jsonl, …) conflict at merge time: the first
#   merges, the second goes CONFLICTING and its auto-merge stalls.
#   commit-via-pr.sh's own reconcile loop clears conflicts that appear
#   while the opening job is still running, but a PR that opens clean and
#   only conflicts AFTER that job exits (a sibling merges minutes later)
#   has no one to unstick it. This janitor is that someone: a cron sweep
#   that rebases every DIRTY bot PR onto latest main using the shared
#   per-file resolver, then force-pushes so auto-merge resumes.
#
# Required environment (set by Actions):
#   GITHUB_REPOSITORY
#   PAT_TOKEN (preferred) or GH_TOKEN — repo token for gh + push.
#
# Usage:
#   bash auditor/scripts/unstick-bot-prs.sh
#
# Fail-soft: a PR that cannot be reconciled (resolver failure, force-push
# rejection) is logged and skipped, never fatal — one stuck PR must not
# block the others or fail the sweep.

set -uo pipefail

TOKEN="${PAT_TOKEN:-${GH_TOKEN:-}}"
if [ -z "$TOKEN" ]; then
  echo "::error::unstick-bot-prs requires PAT_TOKEN or GH_TOKEN in env" >&2
  exit 1
fi
: "${GITHUB_REPOSITORY:?unstick-bot-prs requires GITHUB_REPOSITORY}"

git config user.name "nlpm-auditor[bot]"
git config user.email "nlpm-auditor[bot]@users.noreply.github.com"
git remote set-url origin "https://x-access-token:${TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
git fetch origin main

# Open auditor-bot PRs that conflict with main, "<number> <branch>" per line.
mapfile -t PRS < <(GH_TOKEN="$TOKEN" gh pr list \
  --repo "$GITHUB_REPOSITORY" --label auditor-bot --state open --limit 100 \
  --json number,headRefName,mergeStateStatus \
  --jq '.[] | select(.mergeStateStatus == "DIRTY") | "\(.number) \(.headRefName)"')

if [ "${#PRS[@]}" -eq 0 ]; then
  echo "unstick-bot-prs: no conflicting auditor-bot PRs"
  exit 0
fi
echo "unstick-bot-prs: ${#PRS[@]} conflicting bot PR(s) to reconcile"

reconciled=0
for entry in "${PRS[@]}"; do
  NUM="${entry%% *}"
  BRANCH="${entry#* }"
  echo "unstick-bot-prs: reconciling PR #$NUM ($BRANCH)"

  if ! git fetch origin "$BRANCH"; then
    echo "  skip #$NUM: cannot fetch $BRANCH"
    continue
  fi
  git checkout -B "$BRANCH" "origin/$BRANCH"

  if ! git rebase origin/main; then
    if ! bash auditor/scripts/resolve-merge-conflicts.sh; then
      git rebase --abort || true
      echo "  skip #$NUM: resolver failed on $BRANCH"
      git checkout --force main >/dev/null 2>&1 || true
      continue
    fi
    if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
      # git rebase --continue opens $GIT_EDITOR; pin to true (see
      # git-push-with-retry.sh) so it accepts the existing message.
      if ! GIT_EDITOR=true git rebase --continue; then
        git rebase --abort || true
        echo "  skip #$NUM: rebase --continue failed"
        git checkout --force main >/dev/null 2>&1 || true
        continue
      fi
    fi
  fi

  # A rebase that dropped this branch's only commit (already on main via a
  # sibling PR) leaves it empty; force-pushing that yields a zero-commit PR
  # that can never merge. Close it as redundant instead.
  if git diff --quiet "origin/main..HEAD"; then
    echo "  closing #$NUM: rebase emptied $BRANCH (changes already on main)"
    GH_TOKEN="$TOKEN" gh pr close "$NUM" --repo "$GITHUB_REPOSITORY" --delete-branch \
      --comment "Closing as redundant — changes already reached main via a sibling bot PR." || true
    git checkout --force main >/dev/null 2>&1 || true
    continue
  fi
  if git push --force-with-lease origin "$BRANCH"; then
    GH_TOKEN="$TOKEN" gh pr merge "$NUM" --repo "$GITHUB_REPOSITORY" --auto --merge || true
    echo "  reconciled PR #$NUM"
    reconciled=$((reconciled + 1))
  else
    echo "  skip #$NUM: force-push failed for $BRANCH"
  fi
  git checkout --force main >/dev/null 2>&1 || true
done

echo "unstick-bot-prs: reconciled ${reconciled}/${#PRS[@]} conflicting bot PR(s)"
