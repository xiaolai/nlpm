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
#   It also merges bot PRs that are already mergeable (CLEAN). Auto-merge
#   is disabled on xiaolai/nlpm (allow_auto_merge=false), so a bot PR that
#   commit-via-pr.sh could not merge inside its watch window — or that this
#   sweep just rebased — otherwise stays open forever. Observed 2026-09-30:
#   19 CLEAN bot PRs open, the oldest from 2026-08-05, i.e. audit, track and
#   contribute output that never reached main. Only PRs younger than
#   UNSTICK_MERGE_MAX_AGE_HOURS (default 48) are merged: an older PR's
#   snapshot of shared state (registry statuses, track counts) may have been
#   superseded by later commits in ways git cannot see as a conflict, so
#   merging it is a human decision. Those are listed as a warning instead.
#
# Required environment (set by Actions):
#   GITHUB_REPOSITORY
#   PAT_TOKEN (preferred) or GH_TOKEN — repo token for gh + push.
# Optional:
#   UNSTICK_MERGE_MAX_AGE_HOURS — merge CLEAN bot PRs up to this age (48).
#   UNSTICK_UNKNOWN_WAIT_SECS   — pause before each re-check of an UNKNOWN merge state (5).
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

MAX_AGE_HOURS="${UNSTICK_MERGE_MAX_AGE_HOURS:-48}"
case "$MAX_AGE_HOURS" in
  ''|*[!0-9]*) echo "::error::UNSTICK_MERGE_MAX_AGE_HOURS must be a whole number of hours" >&2; exit 1 ;;
esac

# One snapshot of every open auditor-bot PR:
# "<number> <branch> <mergeStateStatus> <age in whole hours>" per line.
# Fail loud if the listing itself fails — an empty list must mean "no PRs",
# never "gh errored".
if ! OPEN_PRS=$(GH_TOKEN="$TOKEN" gh pr list \
  --repo "$GITHUB_REPOSITORY" --label auditor-bot --state open --limit 100 \
  --json number,headRefName,mergeStateStatus,createdAt \
  --jq '.[] | "\(.number) \(.headRefName) \(.mergeStateStatus) \(((now - (.createdAt | fromdateiso8601)) / 3600) | floor)"'); then
  echo "::error::unstick-bot-prs: could not list auditor-bot PRs" >&2
  exit 1
fi

# --- resolve UNKNOWN merge states ------------------------------------------
# After main moves, GitHub recomputes every open PR's mergeability and
# `gh pr list` reports UNKNOWN until that finishes. A sweep shortly after a
# merge would otherwise skip every PR (the 2026-09-30 09:51 sweep merged none
# of four CLEAN ones). Asking for one PR's state starts its computation, so
# re-query each UNKNOWN one a few times before giving up on it for this sweep.
UNKNOWN_WAIT_SECS="${UNSTICK_UNKNOWN_WAIT_SECS:-5}"
resolved=""
while read -r NUM BRANCH STATE AGE; do
  [ -z "${NUM:-}" ] && continue
  tries=0
  while [ "$STATE" = "UNKNOWN" ] && [ "$tries" -lt 3 ]; do
    sleep "$UNKNOWN_WAIT_SECS"
    STATE=$(GH_TOKEN="$TOKEN" gh pr view "$NUM" --repo "$GITHUB_REPOSITORY" \
      --json mergeStateStatus --jq .mergeStateStatus) || STATE=UNKNOWN
    tries=$((tries + 1))
  done
  [ "$STATE" = "UNKNOWN" ] && echo "  #$NUM merge state still UNKNOWN after $tries re-checks; the next sweep retries"
  resolved+="$NUM $BRANCH $STATE $AGE"$'\n'
done <<< "$OPEN_PRS"
OPEN_PRS="$resolved"

# --- merge bot PRs that are already mergeable ---------------------------
merged=0
stale=()
while read -r NUM _BRANCH STATE AGE; do
  [ -z "${NUM:-}" ] && continue
  case "$STATE" in CLEAN|HAS_HOOKS) ;; *) continue ;; esac
  if [ "$AGE" -ge "$MAX_AGE_HOURS" ]; then
    stale+=("#$NUM (${AGE}h)")
    continue
  fi
  # A sibling merged earlier in this loop can make this one conflict;
  # GitHub then refuses the merge and the next sweep rebases it.
  if GH_TOKEN="$TOKEN" gh pr merge "$NUM" --repo "$GITHUB_REPOSITORY" --merge; then
    echo "unstick-bot-prs: merged mergeable PR #$NUM"
    merged=$((merged + 1))
  else
    echo "  could not merge #$NUM yet; the next sweep retries"
  fi
done <<< "$OPEN_PRS"
echo "unstick-bot-prs: merged ${merged} mergeable bot PR(s)"
if [ "${#stale[@]}" -gt 0 ]; then
  echo "::warning::unstick-bot-prs: ${#stale[@]} mergeable bot PR(s) older than ${MAX_AGE_HOURS}h left for a human (their state snapshot may be superseded): ${stale[*]}"
fi

# --- rebase bot PRs that conflict with main -----------------------------
# "<number> <branch>" per line.
mapfile -t PRS < <(awk '$3 == "DIRTY" { print $1, $2 }' <<< "$OPEN_PRS")

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
