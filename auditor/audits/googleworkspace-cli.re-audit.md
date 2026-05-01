# NLPM Re-Audit: googleworkspace/cli

**Date**: 2026-05-01  |  **Artifacts**: 96  |  **Strategy**: progressive
**NL Score**: 89/100
**Bugs**: 1  |  **Quality Issues**: 24

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| CLAUDE.md | CLAUDE.md | 65 | No actionable guidance; no build/run, test, or architecture sections |
| skills/gws-gmail/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-forms/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-calendar/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-drive/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-sheets/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-docs/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-slides/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-chat/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-tasks/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-meet/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-keep/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-script/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-people/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-classroom/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-events/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-workflow/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-gmail-send/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-sheets-read/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/gws-calendar-insert/SKILL.md | SKILL.md | 82 | Generic description (1 phrase); no scope note |
| skills/recipe-create-shared-drive/SKILL.md | SKILL.md | 95 | Vague quantifier "appropriate" in description; no scope note |
| skills/gws-gmail-read/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-gmail-triage/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-gmail-forward/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-gmail-reply/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-gmail-reply-all/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-gmail-watch/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-sheets-append/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-docs-write/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-chat-send/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-calendar-agenda/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-drive-upload/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-events-subscribe/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-events-renew/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-script-push/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-modelarmor/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-modelarmor-sanitize-prompt/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-modelarmor-sanitize-response/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-modelarmor-create-template/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-admin-reports/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-shared/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-workflow-standup-report/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-workflow-weekly-digest/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-workflow-meeting-prep/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-workflow-email-to-task/SKILL.md | SKILL.md | 97 | No scope note |
| skills/gws-workflow-file-announce/SKILL.md | SKILL.md | 97 | No scope note |
| skills/persona-hr-coordinator/SKILL.md | SKILL.md | 97 | No scope note |
| skills/persona-project-manager/SKILL.md | SKILL.md | 97 | No scope note |
| skills/persona-sales-ops/SKILL.md | SKILL.md | 97 | No scope note |
| skills/persona-exec-assistant/SKILL.md | SKILL.md | 97 | No scope note |
| skills/persona-it-admin/SKILL.md | SKILL.md | 97 | No scope note |
| skills/persona-team-lead/SKILL.md | SKILL.md | 97 | No scope note |
| skills/persona-event-coordinator/SKILL.md | SKILL.md | 97 | No scope note |
| skills/persona-researcher/SKILL.md | SKILL.md | 97 | No scope note |
| skills/persona-content-creator/SKILL.md | SKILL.md | 97 | No scope note |
| skills/persona-customer-support/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-watch-drive-changes/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-reschedule-meeting/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-create-presentation/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-batch-invite-to-event/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-organize-drive-folder/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-save-email-attachments/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-block-focus-time/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-create-meet-space/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-save-email-to-doc/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-create-task-list/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-send-team-announcement/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-create-doc-from-template/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-forward-labeled-emails/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-backup-sheet-as-csv/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-share-doc-and-notify/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-share-event-materials/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-compare-sheet-tabs/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-find-free-time/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-draft-email-from-doc/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-copy-sheet-for-new-month/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-plan-weekly-schedule/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-create-vacation-responder/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-find-large-files/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-create-feedback-form/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-create-events-from-sheet/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-log-deal-update/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-bulk-download-folder/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-post-mortem-setup/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-sync-contacts-to-sheet/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-review-overdue-tasks/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-review-meet-participants/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-collect-form-responses/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-share-folder-with-team/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-generate-report-from-sheet/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-create-classroom-course/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-schedule-recurring-event/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-create-expense-tracker/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-label-and-archive-emails/SKILL.md | SKILL.md | 97 | No scope note |
| skills/recipe-email-drive-link/SKILL.md | SKILL.md | 97 | No scope note |

## Bugs (PR-worthy)

| # | File | Issue | Confidence | Evidence | Impact |
|---|------|-------|------------|----------|--------|
| 1 | CLAUDE.md | Entire CLAUDE.md is a single line pointing to AGENTS.md with no project guidance | high | File is 2 lines: "When contributing to this repository, you must strictly follow all guidelines outlined in the AGENTS.md file." — no build/run, test instructions, architecture, or prerequisites | Agents loading this CLAUDE.md receive no project context, no build commands, no test commands, and no architecture overview |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | CLAUDE.md | No actionable guidance (content is a single redirect, no instructions) | -10 |
| 2 | CLAUDE.md | No build/run instructions | -10 |
| 3 | CLAUDE.md | No test instructions | -5 |
| 4 | CLAUDE.md | No architecture overview | -5 |
| 5 | CLAUDE.md | No prerequisites section | -5 |
| 6 | skills/gws-gmail/SKILL.md | Generic description (≤1 specific phrase): "Gmail: Send, read, and manage email." | -15 |
| 7 | skills/gws-forms/SKILL.md | Generic description: "Read and write Google Forms." | -15 |
| 8 | skills/gws-calendar/SKILL.md | Generic description: "Google Calendar: Manage calendars and events." | -15 |
| 9 | skills/gws-drive/SKILL.md | Generic description: "Google Drive: Manage files, folders, and shared drives." | -15 |
| 10 | skills/gws-sheets/SKILL.md | Generic description: "Google Sheets: Read and write spreadsheets." | -15 |
| 11 | skills/gws-docs/SKILL.md | Generic description: "Read and write Google Docs." | -15 |
| 12 | skills/gws-slides/SKILL.md | Generic description: "Google Slides: Read and write presentations." | -15 |
| 13 | skills/gws-chat/SKILL.md | Generic description: "Google Chat: Manage Chat spaces and messages." | -15 |
| 14 | skills/gws-tasks/SKILL.md | Generic description: "Google Tasks: Manage task lists and tasks." | -15 |
| 15 | skills/gws-meet/SKILL.md | Generic description: "Manage Google Meet conferences." | -15 |
| 16 | skills/gws-keep/SKILL.md | Generic description: "Manage Google Keep notes." | -15 |
| 17 | skills/gws-script/SKILL.md | Generic description: "Manage Google Apps Script projects." | -15 |
| 18 | skills/gws-people/SKILL.md | Generic description: "Google People: Manage contacts and profiles." | -15 |
| 19 | skills/gws-classroom/SKILL.md | Generic description: "Google Classroom: Manage classes, rosters, and coursework." | -15 |
| 20 | skills/gws-events/SKILL.md | Generic description: "Subscribe to Google Workspace events." | -15 |
| 21 | skills/gws-workflow/SKILL.md | Generic description: "Google Workflow: Cross-service productivity workflows." | -15 |
| 22 | skills/gws-gmail-send/SKILL.md | Generic description: "Gmail: Send an email." | -15 |
| 23 | skills/gws-sheets-read/SKILL.md | Generic description: "Google Sheets: Read values from a spreadsheet." | -15 |
| 24 | skills/gws-calendar-insert/SKILL.md | Generic description: "Google Calendar: Create a new event." | -15 |
| 25 | skills/recipe-create-shared-drive/SKILL.md | Vague quantifier "appropriate" in description | -2 |
| 26–95 | (all 95 SKILL.md files) | No scope note / cross-references section | -3 each |

## Cross-Component

- `CLAUDE.md` delegates entirely to `AGENTS.md` without embedding any of its own project context. Agents that don't also read `AGENTS.md` get zero guidance from `CLAUDE.md`. While `AGENTS.md` exists, this creates a single point of failure where any agent loading only `CLAUDE.md` (the standard entry point) gets no actionable information.
- All 95 SKILL.md files reference `../gws-shared/SKILL.md` in their prerequisite note. The shared skill exists at `skills/gws-shared/SKILL.md`, so no broken cross-references.
- Recipe skills declare `requires.skills` in frontmatter (e.g., `gws-calendar`, `gws-drive`). All referenced skill slugs map to existing directories in `skills/`, so no orphaned skill dependencies found.

## Recommendation

The 95 SKILL.md files are well-structured with correct frontmatter, concrete code examples, and working cross-references, but the project needs scope notes on every skill and richer descriptions on the 19 top-level API skills — the CLAUDE.md also needs to be expanded beyond its current single-line delegation to AGENTS.md.
