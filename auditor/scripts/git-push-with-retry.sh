#!/bin/bash
# Push HEAD to origin with up to N retry attempts.
#
# On failure, rebases against origin/<current-branch>. If the rebase
# hits a conflict, delegates to auditor/scripts/resolve-merge-conflicts.sh
# (which knows the per-file strategy: 3-way merge for the registry,
# line-union for append-only logs, this commit's version for everything
# else).
#
# Usage:
#   bash auditor/scripts/git-push-with-retry.sh [max_attempts]
#
# The caller MUST have already done `git add` + `git commit`. This
# script only handles the push and reconciliation against concurrent
# remote writes (the cron-driven auditor pipeline has many concurrent
# committers on main).
#
# Replaces the duplicated retry loops previously inlined in:
#   auditor-contribute.yml, auditor-discover.yml, auditor-suppressions.yml,
#   auditor-track.yml, auditor-classify.yml, nlpm-self-check.yml
# Plus several smaller places. Centralizing means the retry policy is
# one code path that all workflows benefit from improving.

set -e

MAX_ATTEMPTS="${1:-3}"

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  if git push; then
    exit 0
  fi
  echo "git-push-with-retry: attempt $attempt/$MAX_ATTEMPTS failed; reconciling..."
  if git pull --rebase; then
    continue
  fi
  echo "git-push-with-retry: rebase hit conflicts; invoking resolver"
  bash auditor/scripts/resolve-merge-conflicts.sh
  # If the rebase is still in progress after the resolver, complete it.
  if git status --porcelain=v1 | grep -q '^UU\|^AA\|^DD\|^AU\|^UA\|^DU\|^UD' ; then
    echo "git-push-with-retry: ERROR — unresolved conflicts remain"
    exit 1
  fi
  if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
    # `git rebase --continue` invokes $GIT_EDITOR for the commit message.
    # In CI there is no terminal and EDITOR is unset, so the editor call
    # fails with "Terminal is dumb, but EDITOR unset". Pin GIT_EDITOR to
    # `true` so it accepts the existing message non-interactively.
    # The 2026-05-13 v0.8.18 bulk-seed hit this: 50+ exemplar runs
    # cleared the merge conflicts via resolve-merge-conflicts.sh, then
    # this step exited 1 because the editor couldn't open.
    GIT_EDITOR=true git rebase --continue || {
      echo "git-push-with-retry: ERROR — git rebase --continue failed"
      exit 1
    }
  fi
done

echo "git-push-with-retry: ERROR — push failed after $MAX_ATTEMPTS attempts"
exit 1
