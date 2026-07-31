#!/usr/bin/env bash
# commit-via-pr.sh — commit staged auditor changes via a PR (auto-merged)
# instead of pushing directly to main.
#
# Why this exists:
#   Classic branch protection blocks any push that does not satisfy
#   required status checks — including bot pushes via GITHUB_TOKEN.
#   The auditor pipeline pushes to main every few hours (track,
#   daily-report, dashboard, audit findings, etc.); with protection,
#   those pushes are rejected (GH006). Opening a PR per bot commit
#   threads the change through the same gate as humans. The gate's
#   "Detect release-bearing change" step makes this cheap: non-release
#   PRs (bot or human) skip the heavy LLM step and pass in seconds.
#
# Required environment:
#   GITHUB_REPOSITORY, GITHUB_WORKFLOW, GITHUB_RUN_ID — set by Actions.
#   PAT_TOKEN — repo PAT. Required so the bot PR triggers downstream
#               workflows (PRs opened by GITHUB_TOKEN do NOT trigger
#               them, by GitHub anti-recursion design). Falls back to
#               GH_TOKEN if PAT_TOKEN is empty, but emits a warning:
#               without PAT_TOKEN the gate workflow will not run on
#               bot PRs, and once branch protection requires `gate`
#               those PRs will sit unmerged.
#
# Usage:
#   git add <files>
#   bash auditor/scripts/commit-via-pr.sh "<commit message>"
#
# Sequential calls in one job:
#   The commit advances HEAD and is NOT reset afterward, so a second call in
#   the same job commits on top of the first — its PR branch then contains
#   both commits. This is safe: the two PRs merge idempotently (the shared
#   append-only logs union and the registry 3-way merges via
#   resolve-merge-conflicts.sh), so main converges to the same state
#   regardless of merge order. The one hazard — a rebase that finds the
#   commit already upstream and empties the branch — is handled explicitly
#   in the reconcile loop below (the PR is closed as redundant, never left
#   as a zero-commit stuck PR).
#
# Behavior:
#   - No-op (exit 0) if nothing is staged.
#   - Otherwise: branch off origin/main, commit as nlpm-auditor[bot],
#     push the branch (3 retries), open a PR labeled `auditor-bot`,
#     enable auto-merge (merge-commit method).
#
# Concurrency:
#   Each bot run gets its own branch (auditor/bot/<workflow>/<run_id>),
#   so branch pushes never conflict between concurrent runs. Two bot PRs
#   that touch the same file (e.g. events.jsonl, repos.json) DO conflict
#   at merge time: the first auto-merges, the second goes CONFLICTING and
#   its auto-merge stalls. Once every auditor workflow commits through
#   this script, those shared-log collisions are frequent, so the stall
#   is no longer "rare" — left unhandled it recreates the exact bot-PR
#   pileup this flow was meant to avoid.
#
#   The reconcile loop below fixes it: after enabling auto-merge, the
#   script briefly watches the PR; if it goes CONFLICTING it rebases the
#   bot branch onto latest main — unioning append-only logs and 3-way
#   merging the registry via resolve-merge-conflicts.sh, the SAME resolver
#   git-push-with-retry.sh uses for direct pushes — then force-pushes so
#   auto-merge resumes. Fail-soft: on timeout or a resolver failure it
#   leaves the PR open with auto-merge enabled; the auditor-unstick-bot-prs
#   janitor reconciles anything that conflicts after this job exits.

set -euo pipefail

MSG="${1:?usage: commit-via-pr.sh <commit message>}"

# --- precondition: something staged? ---
if git diff --cached --quiet; then
  echo "commit-via-pr: nothing staged — skipping"
  exit 0
fi

# --- choose the token. PAT_TOKEN preferred (so the bot PR triggers
#     downstream workflows including the gate); fall back to GH_TOKEN
#     with a warning. ---
TOKEN="${PAT_TOKEN:-${GH_TOKEN:-}}"
if [ -z "$TOKEN" ]; then
  echo "::error::commit-via-pr requires PAT_TOKEN or GH_TOKEN in env" >&2
  exit 1
fi
if [ -z "${PAT_TOKEN:-}" ]; then
  echo "::warning::commit-via-pr: PAT_TOKEN missing — using GH_TOKEN. Bot PR will not trigger workflows; the gate will not run on it."
fi

# --- commit the staged tree on top of current HEAD as the bot identity.
#     Actions/checkout leaves us at origin/main, so this commit is
#     correctly parented on main. ---
git -c user.name="nlpm-auditor[bot]" \
    -c user.email="nlpm-auditor[bot]@users.noreply.github.com" \
    commit -m "$MSG"
HEAD_AFTER=$(git rev-parse HEAD)

# --- create the bot branch pointing at the new commit ---
SAFE_WF=$(echo "${GITHUB_WORKFLOW:-unknown-workflow}" | tr -c 'a-zA-Z0-9._-' '-')
RUN_ID="${GITHUB_RUN_ID:-$(date +%s)}"
BRANCH="auditor/bot/${SAFE_WF}/${RUN_ID}"
git branch -f "$BRANCH" "$HEAD_AFTER"

# --- push the branch via the chosen token ---
git remote set-url origin "https://x-access-token:${TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
for attempt in 1 2 3; do
  if git push -u origin "$BRANCH"; then
    break
  fi
  if [ "$attempt" -eq 3 ]; then
    echo "::error::commit-via-pr: push of $BRANCH failed after 3 attempts" >&2
    exit 1
  fi
  echo "commit-via-pr: push attempt ${attempt}/3 failed; retrying"
  sleep $((attempt * 3))
done

# --- open PR + enable auto-merge ---
RUN_URL="https://github.com/${GITHUB_REPOSITORY}/actions/runs/${RUN_ID}"
BODY=$(printf 'Automated bot commit from `%s` ([run %s](%s)).\n\nMerged via the auditor PR-flow (see `auditor/scripts/commit-via-pr.sh`).' \
       "${GITHUB_WORKFLOW:-unknown}" "$RUN_ID" "$RUN_URL")

PR_URL=$(GH_TOKEN="$TOKEN" gh pr create \
  --repo "$GITHUB_REPOSITORY" \
  --base main --head "$BRANCH" \
  --title "$MSG" --body "$BODY" \
  --label "auditor-bot")
echo "commit-via-pr: opened $PR_URL"

# Auto-merge: lands as soon as required checks (if any) pass. When no
# checks are required on main, --auto merges effectively immediately.
if ! GH_TOKEN="$TOKEN" gh pr merge "$PR_URL" --auto --merge; then
  echo "::warning::commit-via-pr: --auto unavailable (auto-merge disabled on repo?); attempting direct merge"
  GH_TOKEN="$TOKEN" gh pr merge "$PR_URL" --merge \
    || echo "::warning::commit-via-pr: direct merge failed; the reconcile loop will retry"
fi

# --- reconcile loop: unstick a PR that conflicts with main -------------
# Watch the PR briefly. On CONFLICTING (mergeStateStatus=DIRTY), rebase the
# bot branch onto latest main using the shared resolver, force-push, and
# re-assert auto-merge. Mirrors git-push-with-retry.sh's proven
# rebase+resolve sequence, so the conflict-stage semantics match. Fail-soft
# throughout: a resolver failure or timeout leaves the PR open with
# auto-merge enabled for the janitor to finish — a stuck bot PR must never
# fail the workflow that opened it.
MAX_WATCH="${COMMIT_VIA_PR_MAX_WATCH:-8}"
for i in $(seq 1 "$MAX_WATCH"); do
  if [ "$i" -lt 4 ]; then sleep 5; else sleep 15; fi
  STATE=$(GH_TOKEN="$TOKEN" gh pr view "$PR_URL" \
            --json state,mergeStateStatus \
            --jq '.state + " " + .mergeStateStatus' 2>/dev/null || echo "UNKNOWN UNKNOWN")
  PR_STATE="${STATE%% *}"
  MERGE_STATE="${STATE##* }"
  echo "commit-via-pr: watch ${i}/${MAX_WATCH} — state=$PR_STATE merge=$MERGE_STATE"
  case "$PR_STATE" in
    MERGED) echo "commit-via-pr: merged $PR_URL"; exit 0 ;;
    CLOSED) echo "::warning::commit-via-pr: $PR_URL closed unmerged"; exit 0 ;;
  esac
  [ "$MERGE_STATE" = "DIRTY" ] || continue

  echo "commit-via-pr: $PR_URL conflicts with main — rebasing $BRANCH"
  git fetch origin main
  # HEAD is the bot commit (== branch tip; we never left it). Rebase onto
  # latest main; on conflict, resolve with the shared per-file strategy.
  if ! git rebase origin/main; then
    if ! bash auditor/scripts/resolve-merge-conflicts.sh; then
      git rebase --abort || true
      echo "::warning::commit-via-pr: resolver failed; leaving $PR_URL for the janitor"
      exit 0
    fi
    if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
      # git rebase --continue opens $GIT_EDITOR; pin to true so it accepts
      # the existing message non-interactively (see git-push-with-retry.sh).
      GIT_EDITOR=true git rebase --continue || {
        git rebase --abort || true
        echo "::warning::commit-via-pr: rebase --continue failed; leaving $PR_URL for the janitor"
        exit 0
      }
    fi
  fi
  # If the rebase left nothing (this commit already reached main — e.g. a
  # sibling PR that carried it merged first; see the sequential-call note in
  # the header), the branch is now empty. Force-pushing it would leave a
  # zero-commit PR that can never auto-merge — the exact stuck-PR state this
  # flow avoids. Close it as redundant instead.
  if git diff --quiet "origin/main..HEAD"; then
    echo "commit-via-pr: rebase emptied $BRANCH (changes already on main); closing redundant $PR_URL"
    GH_TOKEN="$TOKEN" gh pr close "$PR_URL" --delete-branch \
      --comment "Closing as redundant — these changes already reached main via a sibling bot PR." || true
    exit 0
  fi
  git branch -f "$BRANCH" HEAD
  if ! git push --force-with-lease origin "$BRANCH"; then
    echo "::warning::commit-via-pr: force-push after rebase failed; leaving $PR_URL for the janitor"
    exit 0
  fi
  # Force-push can drop the auto-merge enablement; re-assert it.
  GH_TOKEN="$TOKEN" gh pr merge "$PR_URL" --auto --merge || true
done

echo "::warning::commit-via-pr: $PR_URL not merged within the watch window; auto-merge stays enabled (auditor-unstick-bot-prs will finish it)"
exit 0
