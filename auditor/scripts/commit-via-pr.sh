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
# Behavior:
#   - No-op (exit 0) if nothing is staged.
#   - Otherwise: branch off origin/main, commit as nlpm-auditor[bot],
#     push the branch (3 retries), open a PR labeled `auditor-bot`,
#     enable auto-merge (merge-commit method).
#
# Concurrency note:
#   Each bot run gets its own branch (auditor/bot/<workflow>/<run_id>),
#   so branch pushes do not conflict between concurrent runs. Two bot
#   PRs that touch the same file (e.g. events.jsonl) will conflict at
#   merge time; the second auto-merge will sit until manually resolved
#   or until the conflict clears. A future revision may add an
#   auto-rebase loop here; for now, rare conflicts are accepted.

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
if GH_TOKEN="$TOKEN" gh pr merge "$PR_URL" --auto --merge; then
  echo "commit-via-pr: auto-merge enabled for $PR_URL"
else
  echo "::warning::commit-via-pr: --auto unavailable (auto-merge disabled on repo?); attempting direct merge"
  GH_TOKEN="$TOKEN" gh pr merge "$PR_URL" --merge \
    || { echo "::error::commit-via-pr: PR not merged — $PR_URL" >&2; exit 1; }
fi
