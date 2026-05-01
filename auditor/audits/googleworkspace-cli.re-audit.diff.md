# Re-Audit: googleworkspace/cli

**Date**: 2026-05-01  |  **Before**: `a3768d0` (99/100)  |  **After**: `a3768d0` (89/100)

## Summary

| Outcome | Count |
|---------|------:|
| fixed — upstream, not via our PR | 16 |
| newly introduced (regressions) | 121 |

## Original findings — verification

| # | File | Line | Rule | Pattern | Outcome | PR |
|---|------|------|------|---------|---------|----|
| 1 | `skills/recipe-post-mortem-setup/SKILL.md` | 26 | BUG-broken-reference | `wrong-cli-flags` | fixed — upstream, not via our PR | #757 |
| 2 | `skills/recipe-collect-form-responses/SKILL.md` | 22 | BUG-broken-reference | `nonexistent-api-method` | fixed — upstream, not via our PR | #758 |
| 3 | `scripts/show-art.sh` | 17 | SEC-path-traversal | `unvalidated-file-arg` | fixed — upstream, not via our PR |  |
| 4 | `scripts/coverage.sh` | 22 | SEC-runtime-package-install | `runtime-package-install` | fixed — upstream, not via our PR | #759 |
| 5 | `package.json` | 54 | SEC-unpinned-semver | `unpinned-semver` | fixed — upstream, not via our PR | #760 |
| 6 | `skills/recipe-create-shared-drive/SKILL.md` | 3 | R30 | `vague-quantifier` | fixed — upstream, not via our PR |  |
| 7 | `skills/gws-modelarmor/SKILL.md` | — | R05 | `missing-required-section` | fixed — upstream, not via our PR |  |
| 8 | `skills/recipe-compare-sheet-tabs/SKILL.md` | 25 | R22 | `vague-step-no-command` | fixed — upstream, not via our PR |  |
| 9 | `skills/recipe-draft-email-from-doc/SKILL.md` | 24 | R22 | `vague-step-no-command` | fixed — upstream, not via our PR |  |
| 10 | `skills/recipe-create-events-from-sheet/SKILL.md` | 26 | R22 | `incomplete-loop-step` | fixed — upstream, not via our PR |  |
| 11 | `skills/recipe-review-overdue-tasks/SKILL.md` | 26 | R22 | `vague-step-no-command` | fixed — upstream, not via our PR |  |
| 12 | `skills/recipe-find-large-files/SKILL.md` | 25 | R22 | `vague-step-no-command` | fixed — upstream, not via our PR |  |
| 13 | `skills/recipe-save-email-to-doc/SKILL.md` | 27 | R17 | `flag-inconsistency` | fixed — upstream, not via our PR |  |
| 14 | `skills/recipe-generate-report-from-sheet/SKILL.md` | 28 | R17 | `flag-inconsistency` | fixed — upstream, not via our PR |  |
| 15 | `skills/recipe-create-doc-from-template/SKILL.md` | 27 | R17 | `flag-inconsistency` | fixed — upstream, not via our PR |  |
| 16 | `skills/gws-docs-write/SKILL.md` | — | CC-terminology-drift | `flag-name-drift` | fixed — upstream, not via our PR |  |

## Findings introduced since audit

These findings appear in the re-audit but were not in the original audit. They may be true regressions (new commits introduced them) or artifacts of scoring drift.

| # | File | Line | Rule | Pattern | Description |
|---|------|------|------|---------|-------------|
| 1 | `CLAUDE.md` | — | BUG-no-actionable-guidance | `CLAUDE.md contains only a redirect to another file with no project context` | CLAUDE.md provides no actionable guidance for contributors or agents — it is a single line delegating to AGENTS.md |
| 2 | `CLAUDE.md` | — | R09 | `no_actionable_guidance` | CLAUDE.md contains no actionable guidance, only a redirect |
| 3 | `CLAUDE.md` | — | R10 | `no_build_run_instructions` | CLAUDE.md has no build/run instructions |
| 4 | `CLAUDE.md` | — | R11 | `no_test_instructions` | CLAUDE.md has no test instructions |
| 5 | `CLAUDE.md` | — | R12 | `no_architecture_overview` | CLAUDE.md has no architecture overview |
| 6 | `CLAUDE.md` | — | R13 | `no_prerequisites_section` | CLAUDE.md has no prerequisites section |
| 7 | `skills/gws-gmail/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase; lacks trigger conditions and specificity |
| 8 | `skills/gws-gmail/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 9 | `skills/gws-forms/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 10 | `skills/gws-forms/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 11 | `skills/gws-calendar/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 12 | `skills/gws-calendar/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 13 | `skills/gws-drive/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 14 | `skills/gws-drive/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 15 | `skills/gws-sheets/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 16 | `skills/gws-sheets/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 17 | `skills/gws-docs/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 18 | `skills/gws-docs/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 19 | `skills/gws-slides/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 20 | `skills/gws-slides/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 21 | `skills/gws-chat/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 22 | `skills/gws-chat/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 23 | `skills/gws-tasks/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 24 | `skills/gws-tasks/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 25 | `skills/gws-meet/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 26 | `skills/gws-meet/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 27 | `skills/gws-keep/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 28 | `skills/gws-keep/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 29 | `skills/gws-script/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 30 | `skills/gws-script/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 31 | `skills/gws-people/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 32 | `skills/gws-people/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 33 | `skills/gws-classroom/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 34 | `skills/gws-classroom/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 35 | `skills/gws-events/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 36 | `skills/gws-events/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 37 | `skills/gws-workflow/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 38 | `skills/gws-workflow/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 39 | `skills/gws-gmail-send/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 40 | `skills/gws-gmail-send/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 41 | `skills/gws-sheets-read/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 42 | `skills/gws-sheets-read/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 43 | `skills/gws-calendar-insert/SKILL.md` | 3 | R03 | `generic_description` | Description has only one specific phrase |
| 44 | `skills/gws-calendar-insert/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 45 | `skills/recipe-create-shared-drive/SKILL.md` | 3 | R06 | `vague_quantifier` | Vague quantifier 'appropriate' found in description |
| 46 | `skills/recipe-create-shared-drive/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 47 | `skills/gws-gmail-read/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 48 | `skills/gws-gmail-triage/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 49 | `skills/gws-gmail-forward/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 50 | `skills/gws-gmail-reply/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 51 | `skills/gws-gmail-reply-all/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 52 | `skills/gws-gmail-watch/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 53 | `skills/gws-sheets-append/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 54 | `skills/gws-docs-write/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 55 | `skills/gws-chat-send/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 56 | `skills/gws-calendar-agenda/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 57 | `skills/gws-drive-upload/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 58 | `skills/gws-events-subscribe/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 59 | `skills/gws-events-renew/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 60 | `skills/gws-script-push/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 61 | `skills/gws-modelarmor/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 62 | `skills/gws-modelarmor-sanitize-prompt/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 63 | `skills/gws-modelarmor-sanitize-response/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 64 | `skills/gws-modelarmor-create-template/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 65 | `skills/gws-admin-reports/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 66 | `skills/gws-shared/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 67 | `skills/gws-workflow-standup-report/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 68 | `skills/gws-workflow-weekly-digest/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 69 | `skills/gws-workflow-meeting-prep/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 70 | `skills/gws-workflow-email-to-task/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 71 | `skills/gws-workflow-file-announce/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 72 | `skills/persona-hr-coordinator/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 73 | `skills/persona-project-manager/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 74 | `skills/persona-sales-ops/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 75 | `skills/persona-exec-assistant/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 76 | `skills/persona-it-admin/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 77 | `skills/persona-team-lead/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 78 | `skills/persona-event-coordinator/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 79 | `skills/persona-researcher/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 80 | `skills/persona-content-creator/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 81 | `skills/persona-customer-support/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 82 | `skills/recipe-watch-drive-changes/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 83 | `skills/recipe-reschedule-meeting/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 84 | `skills/recipe-create-presentation/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 85 | `skills/recipe-batch-invite-to-event/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 86 | `skills/recipe-organize-drive-folder/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 87 | `skills/recipe-save-email-attachments/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 88 | `skills/recipe-block-focus-time/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 89 | `skills/recipe-create-meet-space/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 90 | `skills/recipe-save-email-to-doc/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 91 | `skills/recipe-create-task-list/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 92 | `skills/recipe-send-team-announcement/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 93 | `skills/recipe-create-doc-from-template/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 94 | `skills/recipe-forward-labeled-emails/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 95 | `skills/recipe-backup-sheet-as-csv/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 96 | `skills/recipe-share-doc-and-notify/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 97 | `skills/recipe-share-event-materials/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 98 | `skills/recipe-compare-sheet-tabs/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 99 | `skills/recipe-find-free-time/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 100 | `skills/recipe-draft-email-from-doc/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 101 | `skills/recipe-copy-sheet-for-new-month/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 102 | `skills/recipe-plan-weekly-schedule/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 103 | `skills/recipe-create-vacation-responder/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 104 | `skills/recipe-find-large-files/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 105 | `skills/recipe-create-feedback-form/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 106 | `skills/recipe-create-events-from-sheet/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 107 | `skills/recipe-log-deal-update/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 108 | `skills/recipe-bulk-download-folder/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 109 | `skills/recipe-post-mortem-setup/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 110 | `skills/recipe-sync-contacts-to-sheet/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 111 | `skills/recipe-review-overdue-tasks/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 112 | `skills/recipe-review-meet-participants/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 113 | `skills/recipe-collect-form-responses/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 114 | `skills/recipe-share-folder-with-team/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 115 | `skills/recipe-generate-report-from-sheet/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 116 | `skills/recipe-create-classroom-course/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 117 | `skills/recipe-schedule-recurring-event/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 118 | `skills/recipe-create-expense-tracker/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 119 | `skills/recipe-label-and-archive-emails/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 120 | `skills/recipe-email-drive-link/SKILL.md` | — | R08 | `no_scope_note` | No scope note or cross-reference section present |
| 121 | `CLAUDE.md` | — | CC-claude-md-delegation | `claude_md_delegates_entirely_to_other_file` | CLAUDE.md delegates all project context to AGENTS.md; agents relying on CLAUDE.md as the project entry point receive no architectural guidance |

