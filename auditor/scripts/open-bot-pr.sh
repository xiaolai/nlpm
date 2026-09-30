# shellcheck shell=bash
# open-bot-pr.sh — sourced helper: open the auditor-bot PR for a pushed branch.
#
# Shared by commit-via-pr.sh (a run opening the PR for the commit it just
# pushed) and unstick-bot-prs.sh (the janitor opening one for a pushed bot
# branch whose run died before it could). One path, so both get the same
# label, the same adopt-on-error handling and the same retries.
#
# Usage (after `source auditor/scripts/open-bot-pr.sh`):
#   open_bot_pr <branch> <title> <body>
# Needs TOKEN and GITHUB_REPOSITORY. Sets PR_URL. Returns 0 once an open PR
# for <branch> exists, 1 after 3 failed attempts.
# Optional: OPEN_BOT_PR_RETRY_SLEEP — seconds per attempt number between retries (5).

open_bot_pr() {
  local branch="$1" title="$2" body="$3" attempt
  PR_URL=""
  # `gh pr create` opens the PR and then labels it. A 5xx between the two
  # (Write Exemplar run 36713682847: HTTP 502) leaves an open, unlabelled PR
  # and a failed call. So on failure, adopt an open PR for this branch if one
  # exists and make sure it carries the label; otherwise retry the create.
  for attempt in 1 2 3; do
    if PR_URL=$(GH_TOKEN="$TOKEN" gh pr create \
        --repo "$GITHUB_REPOSITORY" \
        --base main --head "$branch" \
        --title "$title" --body "$body" \
        --label "auditor-bot"); then
      echo "open-bot-pr: opened $PR_URL"
      return 0
    fi
    PR_URL=$(GH_TOKEN="$TOKEN" gh pr list --repo "$GITHUB_REPOSITORY" \
      --head "$branch" --state open --json url --jq '.[0].url // empty') || PR_URL=""
    if [ -n "$PR_URL" ]; then
      echo "open-bot-pr: create reported an error but $PR_URL is open for $branch; adopting it"
      # REST, not `gh pr edit`: pr edit also reads reviewer logins, which needs
      # the read:org scope this token lacks, so it always failed here.
      GH_TOKEN="$TOKEN" gh api --silent -X POST "repos/${GITHUB_REPOSITORY}/issues/${PR_URL##*/}/labels" -f "labels[]=auditor-bot" \
        || echo "::warning::open-bot-pr: could not label $PR_URL; unstick-bot-prs.sh adds it on its next sweep"
      return 0
    fi
    if [ "$attempt" -lt 3 ]; then
      echo "open-bot-pr: PR create attempt ${attempt}/3 for $branch failed; retrying"
      sleep $((attempt * ${OPEN_BOT_PR_RETRY_SLEEP:-5}))
    fi
  done
  PR_URL=""
  return 1
}
