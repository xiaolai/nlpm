# NLPM Audit: googleworkspace/cli
**Date**: 2026-04-06  |  **Artifacts**: 96  |  **Strategy**: progressive
**NL Score**: 99/100
**Security**: REVIEW
**Bugs**: 2  |  **Quality Issues**: 10  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/recipe-collect-form-responses/SKILL.md | recipe | 88 | Step 1 calls `gws forms forms list` — `list` not in Forms API |
| skills/recipe-post-mortem-setup/SKILL.md | recipe | 88 | Step 1 uses `--title`/`--body`; gws-docs-write requires `--document`/`--text` |
| skills/gws-modelarmor/SKILL.md | api-skill | 95 | No API Resources section — raw API surface undiscoverable |
| skills/recipe-compare-sheet-tabs/SKILL.md | recipe | 95 | Step 3 has no concrete CLI command |
| skills/recipe-create-events-from-sheet/SKILL.md | recipe | 95 | Step 2 implies row loop but shows only one hardcoded example |
| skills/recipe-draft-email-from-doc/SKILL.md | recipe | 95 | Step 2 is manual-only ("copy the text") — no CLI command |
| skills/recipe-find-large-files/SKILL.md | recipe | 95 | Step 2 has no concrete action command |
| skills/recipe-review-overdue-tasks/SKILL.md | recipe | 95 | Step 3 has no concrete action command |
| skills/recipe-create-doc-from-template/SKILL.md | recipe | 98 | Uses `--document-id`; gws-docs-write documents `--document` |
| skills/recipe-create-shared-drive/SKILL.md | recipe | 98 | "appropriate roles" vague quantifier in description |
| skills/recipe-generate-report-from-sheet/SKILL.md | recipe | 98 | Uses `--document-id`; gws-docs-write documents `--document` |
| skills/recipe-save-email-to-doc/SKILL.md | recipe | 98 | Uses `--document-id`; gws-docs-write documents `--document` |
| CLAUDE.md | project-instruction | 100 | — |
| skills/gws-admin-reports/SKILL.md | api-skill | 100 | — |
| skills/gws-calendar-agenda/SKILL.md | helper-skill | 100 | — |
| skills/gws-calendar-insert/SKILL.md | helper-skill | 100 | — |
| skills/gws-calendar/SKILL.md | api-skill | 100 | — |
| skills/gws-chat-send/SKILL.md | helper-skill | 100 | — |
| skills/gws-chat/SKILL.md | api-skill | 100 | — |
| skills/gws-classroom/SKILL.md | api-skill | 100 | — |
| skills/gws-docs-write/SKILL.md | helper-skill | 100 | — |
| skills/gws-docs/SKILL.md | api-skill | 100 | — |
| skills/gws-drive-upload/SKILL.md | helper-skill | 100 | — |
| skills/gws-drive/SKILL.md | api-skill | 100 | — |
| skills/gws-events-renew/SKILL.md | helper-skill | 100 | — |
| skills/gws-events-subscribe/SKILL.md | helper-skill | 100 | — |
| skills/gws-events/SKILL.md | api-skill | 100 | — |
| skills/gws-forms/SKILL.md | api-skill | 100 | — |
| skills/gws-gmail-forward/SKILL.md | helper-skill | 100 | — |
| skills/gws-gmail-read/SKILL.md | helper-skill | 100 | — |
| skills/gws-gmail-reply-all/SKILL.md | helper-skill | 100 | — |
| skills/gws-gmail-reply/SKILL.md | helper-skill | 100 | — |
| skills/gws-gmail-send/SKILL.md | helper-skill | 100 | — |
| skills/gws-gmail-triage/SKILL.md | helper-skill | 100 | — |
| skills/gws-gmail-watch/SKILL.md | helper-skill | 100 | — |
| skills/gws-gmail/SKILL.md | api-skill | 100 | — |
| skills/gws-keep/SKILL.md | api-skill | 100 | — |
| skills/gws-meet/SKILL.md | api-skill | 100 | — |
| skills/gws-modelarmor-create-template/SKILL.md | helper-skill | 100 | — |
| skills/gws-modelarmor-sanitize-prompt/SKILL.md | helper-skill | 100 | — |
| skills/gws-modelarmor-sanitize-response/SKILL.md | helper-skill | 100 | — |
| skills/gws-people/SKILL.md | api-skill | 100 | — |
| skills/gws-script-push/SKILL.md | helper-skill | 100 | — |
| skills/gws-script/SKILL.md | api-skill | 100 | — |
| skills/gws-shared/SKILL.md | shared-skill | 100 | — |
| skills/gws-sheets-append/SKILL.md | helper-skill | 100 | — |
| skills/gws-sheets-read/SKILL.md | helper-skill | 100 | — |
| skills/gws-sheets/SKILL.md | api-skill | 100 | — |
| skills/gws-slides/SKILL.md | api-skill | 100 | — |
| skills/gws-tasks/SKILL.md | api-skill | 100 | — |
| skills/gws-workflow-email-to-task/SKILL.md | workflow-skill | 100 | — |
| skills/gws-workflow-file-announce/SKILL.md | workflow-skill | 100 | — |
| skills/gws-workflow-meeting-prep/SKILL.md | workflow-skill | 100 | — |
| skills/gws-workflow-standup-report/SKILL.md | workflow-skill | 100 | — |
| skills/gws-workflow-weekly-digest/SKILL.md | workflow-skill | 100 | — |
| skills/gws-workflow/SKILL.md | api-skill | 100 | — |
| skills/persona-content-creator/SKILL.md | persona | 100 | — |
| skills/persona-customer-support/SKILL.md | persona | 100 | — |
| skills/persona-event-coordinator/SKILL.md | persona | 100 | — |
| skills/persona-exec-assistant/SKILL.md | persona | 100 | — |
| skills/persona-hr-coordinator/SKILL.md | persona | 100 | — |
| skills/persona-it-admin/SKILL.md | persona | 100 | — |
| skills/persona-project-manager/SKILL.md | persona | 100 | — |
| skills/persona-researcher/SKILL.md | persona | 100 | — |
| skills/persona-sales-ops/SKILL.md | persona | 100 | — |
| skills/persona-team-lead/SKILL.md | persona | 100 | — |
| skills/recipe-backup-sheet-as-csv/SKILL.md | recipe | 100 | — |
| skills/recipe-batch-invite-to-event/SKILL.md | recipe | 100 | — |
| skills/recipe-block-focus-time/SKILL.md | recipe | 100 | — |
| skills/recipe-bulk-download-folder/SKILL.md | recipe | 100 | — |
| skills/recipe-copy-sheet-for-new-month/SKILL.md | recipe | 100 | — |
| skills/recipe-create-classroom-course/SKILL.md | recipe | 100 | — |
| skills/recipe-create-expense-tracker/SKILL.md | recipe | 100 | — |
| skills/recipe-create-feedback-form/SKILL.md | recipe | 100 | — |
| skills/recipe-create-gmail-filter/SKILL.md | recipe | 100 | — |
| skills/recipe-create-meet-space/SKILL.md | recipe | 100 | — |
| skills/recipe-create-presentation/SKILL.md | recipe | 100 | — |
| skills/recipe-create-task-list/SKILL.md | recipe | 100 | — |
| skills/recipe-create-vacation-responder/SKILL.md | recipe | 100 | — |
| skills/recipe-email-drive-link/SKILL.md | recipe | 100 | — |
| skills/recipe-find-free-time/SKILL.md | recipe | 100 | — |
| skills/recipe-forward-labeled-emails/SKILL.md | recipe | 100 | — |
| skills/recipe-label-and-archive-emails/SKILL.md | recipe | 100 | — |
| skills/recipe-log-deal-update/SKILL.md | recipe | 100 | — |
| skills/recipe-organize-drive-folder/SKILL.md | recipe | 100 | — |
| skills/recipe-plan-weekly-schedule/SKILL.md | recipe | 100 | — |
| skills/recipe-reschedule-meeting/SKILL.md | recipe | 100 | — |
| skills/recipe-review-meet-participants/SKILL.md | recipe | 100 | — |
| skills/recipe-save-email-attachments/SKILL.md | recipe | 100 | — |
| skills/recipe-schedule-recurring-event/SKILL.md | recipe | 100 | — |
| skills/recipe-send-team-announcement/SKILL.md | recipe | 100 | — |
| skills/recipe-share-doc-and-notify/SKILL.md | recipe | 100 | — |
| skills/recipe-share-event-materials/SKILL.md | recipe | 100 | — |
| skills/recipe-share-folder-with-team/SKILL.md | recipe | 100 | — |
| skills/recipe-sync-contacts-to-sheet/SKILL.md | recipe | 100 | — |
| skills/recipe-watch-drive-changes/SKILL.md | recipe | 100 | — |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 (false positive) |
| Medium | 1 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none |
| Scripts | scripts/version-sync.sh, scripts/coverage.sh, scripts/tag-release.sh, scripts/show-art.sh |
| MCP configs | none |
| Package manifests | package.json |
| Requirements | none |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH* | scripts/show-art.sh | 17 | unvalidated-file-arg | `cat "$1"` reads any path supplied as $1 with no validation — path traversal if called from automation. *False positive: dev-only ASCII art utility; no automated call surface. |
| 2 | MEDIUM | scripts/coverage.sh | 22 | runtime-package-install | `cargo install cargo-llvm-cov` downloads and installs a package from crates.io at runtime — version not pinned by hash. |
| 3 | LOW | package.json | 54 | unpinned-semver | devDependencies use `^` semver (`@changesets/cli ^2.29.8`, `lefthook ^2.1.2`) — minor/patch updates apply automatically. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | skills/recipe-post-mortem-setup/SKILL.md | Step 1 calls `gws docs +write --title ... --body ...`; gws-docs-write requires `--document <ID>` and `--text <TEXT>`. `--title` and `--body` are not valid flags; both required flags are absent. Command will fail. | Recipe is broken and cannot be executed as written. |
| 2 | skills/recipe-collect-form-responses/SKILL.md | Step 1 calls `gws forms forms list`; the Google Forms API v1 has no `list` method on the `forms` resource (only `create`, `get`, `batchUpdate`, `setPublishSettings`). | Step fails at runtime; users cannot discover form IDs via this recipe. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/coverage.sh | Runtime `cargo install` at line 22 pulls from crates.io without a hash pin. | Pre-install in CI image or pin with `cargo install --locked cargo-llvm-cov@<exact-version>`. |
| 2 | package.json | `^` semver for devDependencies allows unreviewed minor updates. | Pin to exact versions (`"@changesets/cli": "2.29.8"`) or use a lockfile-only install policy. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/recipe-create-shared-drive/SKILL.md | "appropriate roles" in description is a vague quantifier; prefer "writer, reader, or commenter roles" | -2 |
| 2 | skills/gws-modelarmor/SKILL.md | Missing `## API Resources` section present on every other gws-* API skill; raw API methods are undiscoverable without --help | -5 |
| 3 | skills/recipe-compare-sheet-tabs/SKILL.md | Step 3 ("Compare the data and identify changes") has no CLI command; leaves agent without concrete next action | -5 |
| 4 | skills/recipe-draft-email-from-doc/SKILL.md | Step 2 ("Copy the text from the body content") is a manual action with no CLI command | -5 |
| 5 | skills/recipe-create-events-from-sheet/SKILL.md | Step 2 says "for each row" but shows only one hardcoded calendar insert; loop mechanism not demonstrated | -5 |
| 6 | skills/recipe-review-overdue-tasks/SKILL.md | Step 3 ("Review due dates and prioritize overdue items") has no CLI command | -5 |
| 7 | skills/recipe-find-large-files/SKILL.md | Step 2 ("Review the output and identify files to archive or move") has no CLI command | -5 |
| 8 | skills/recipe-save-email-to-doc/SKILL.md | Uses `--document-id` flag; gws-docs-write documents `--document` — flag name inconsistency | -2 |
| 9 | skills/recipe-generate-report-from-sheet/SKILL.md | Uses `--document-id` flag; gws-docs-write documents `--document` — flag name inconsistency | -2 |
| 10 | skills/recipe-create-doc-from-template/SKILL.md | Uses `--document-id` flag; gws-docs-write documents `--document` — flag name inconsistency | -2 |

## Cross-Component
**CC-1: `gws docs +write` flag name inconsistency**

`skills/gws-docs-write/SKILL.md` documents the required flag as `--document <ID>`. Three recipes use `--document-id` instead:
- `skills/recipe-save-email-to-doc/SKILL.md` line 27
- `skills/recipe-generate-report-from-sheet/SKILL.md` line 28
- `skills/recipe-create-doc-from-template/SKILL.md` line 27

Given that all three recipes independently use `--document-id`, the actual CLI binary may accept `--document-id` and the skill file may be wrong. Verify with `gws docs +write --help` and align both the skill file and the recipes.

**CC-2: recipe-post-mortem-setup references non-existent `gws docs +write` flags**

Beyond the `--document-id` vs `--document` ambiguity, recipe-post-mortem-setup uses `--title` and `--body` which appear in neither the documented nor the inferred flag set. This is unambiguously wrong (see Bug #1).

**No orphaned components or broken relative paths detected.** All `See Also` links in helper skills resolve to existing skill files. All persona and recipe `skills:` prerequisites reference valid skill directories.

## Recommendation

REVIEW — submit NL fix PRs for Bug #1 and Bug #2. Resolve the `--document` vs `--document-id` cross-component inconsistency (CC-1) by running `gws docs +write --help` and updating either the skill file or the three recipes accordingly. Flag the MEDIUM security finding (runtime `cargo install`) in a GitHub issue; the HIGH finding is a false positive. Quality issues are informational and do not block contribution.
