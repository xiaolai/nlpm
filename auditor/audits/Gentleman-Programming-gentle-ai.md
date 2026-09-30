# NLPM Audit: Gentleman-Programming/gentle-ai
**Date**: 2026-04-06  |  **Artifacts**: 64  |  **Strategy**: progressive
**NL Score**: 78/100
**Security**: BLOCKED
**Bugs**: 2  |  **Quality Issues**: 5  |  **Security Findings**: 7

Scoring notes: scores are estimated from a frontmatter, example and vague-word sweep plus targeted reads. They were not computed file by file. The 10 OpenCode agent files and 2 OpenCode command files use a host-specific format: the agent bodies have no frontmatter and the commands use `description`/`agent`/`subtask`. Their low scores may reflect a format mismatch rather than a defect. The Claude, Kiro, Cursor and Kimi agents use `{{...}}` placeholders that the installer substitutes, so I treated them as templates.

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| internal/assets/opencode/agents/gentle-ai-explore.md | agent | 35 | No frontmatter (name/description/model), no examples |
| internal/assets/opencode/agents/gentle-ai-verify.md | agent | 35 | No frontmatter, no examples |
| internal/assets/opencode/agents/gentle-ai-worker.md | agent | 35 | No frontmatter, vague quantifiers |
| internal/assets/opencode/agents/jd-fix-agent.md | agent | 35 | No frontmatter |
| internal/assets/opencode/agents/jd-judge-a.md | agent | 35 | No frontmatter |
| internal/assets/opencode/agents/jd-judge-b.md | agent | 35 | No frontmatter |
| internal/assets/opencode/agents/review-readability.md | agent | 35 | No frontmatter |
| internal/assets/opencode/agents/review-reliability.md | agent | 35 | No frontmatter |
| internal/assets/opencode/agents/review-resilience.md | agent | 35 | No frontmatter |
| internal/assets/opencode/agents/review-risk.md | agent | 35 | No frontmatter |
| internal/assets/opencode/commands/skill-creator.md | command | 65 | No `name`, no empty-input handling |
| internal/assets/opencode/commands/skill-registry.md | command | 65 | No `name`, no empty-input handling |
| internal/assets/claude/agents/*.md (8 files: review-readability, review-refuter, review-reliability, review-resilience, review-risk, jd-fix-agent, jd-judge-a, jd-judge-b) | agent | 80 | No example blocks; description names no "not for" situation |
| internal/assets/kiro/agents/*.md (8 files, same set) | agent | 80 | No example blocks; no "not for" |
| internal/assets/cursor/agents/*.md (5 review-* files) | agent | 80 | No example blocks; no "not for" |
| internal/assets/kimi/agents/*.md (5 review-* files) | agent | 80 | No example blocks; no "not for" |
| skills/gentle-ai-collab-perfect/SKILL.md | skill | 88 | Vague quantifiers (3) |
| internal/assets/skills/issue-creation/SKILL.md | skill | 90 | Vague quantifiers (2) |
| internal/assets/skills/skill-registry/SKILL.md | skill | 90 | Vague quantifiers (2) |
| skills/branch-pr/SKILL.md, skills/work-unit-commits/SKILL.md | skill | 94 | Vague quantifier (1) |
| internal/assets/skills/{work-unit-commits,go-testing,hermes-ephemeral-delegation}/SKILL.md | skill | 94 | Vague quantifier (1) |
| Remaining 17 skills (skills/* and internal/assets/skills/*, including judgment-day, skill-creator, skill-improver, chained-pr, cognitive-doc-design, comment-writer, systemic-issue-triage, gentle-ai-bench, rdd-*, issue-root-resolution) | skill | 96 | Frontmatter valid; no significant issues found |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 2 |
| Medium | 3 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none |
| Scripts | 21 `*.sh` files outside node_modules: scripts/*.sh (14), e2e/*.sh (3), deploy/telemetry/install.sh, deploy/telemetry/gentle-telemetry-backup.test.sh, internal/assets/gga/pr_mode.sh (pre-scan counted 26 scripts) |
| MCP configs | none |
| Package manifests | package.json (no install scripts, no dependencies) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | deploy/telemetry/install.sh | 215 | curl piped to shell | Fallback `curl -fsS https://rclone.org/install.sh \| bash` runs a remote script as root, with no checksum or pin, when `dnf install rclone` fails. |
| 2 | High | scripts/install.sh | 565 | sudo usage | `sudo -- bash -c 'install ... && mv ...'` runs when the install dir is not writable. Arguments are quoted positionals, so it looks safe but is still privilege escalation. |
| 3 | High | e2e/lib.sh | 139 | PATH modification | Test helper prepends a fake bin dir to PATH. This is scoped to the test harness. |
| 4 | Medium | scripts/install.sh | 283, 312, 433, 473, 488 | network calls (curl) | Downloads release archive and checksums from GitHub. Checksum verification exists, but line 488 tolerates a missing checksums file. |
| 5 | Medium | scripts/install.sh | 99 | checksum bypass flag | `--insecure` skips checksum verification. It is documented as not recommended. |
| 6 | Medium | deploy/telemetry/install.sh | 184, 373 | network calls (curl) | Downloads binaries as root. Line 374 fetches checksums, but line 184 has no visible verification. |
| 7 | Low | scripts/install.sh | 9, 108 | curl piped to shell (documentation) | The documented `curl ... \| bash` one-liner sits in a comment and a help heredoc. It is not executed by the script. Some of the pre-scan's Critical matches are probably these. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | internal/assets/opencode/agents/*.md (10 files) | No YAML frontmatter, so no `name`, `description` or `model`. | Probably intentional, since OpenCode may take metadata from JSON config. Confidence is medium. |
| 2 | internal/assets/opencode/commands/skill-creator.md, skill-registry.md | No `name`; `allowed-tools` also missing. | Probably filename-derived in OpenCode. Confidence is low. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/install.sh | Checksums file fetch tolerates failure (line 488). | Fail closed unless `--insecure` is passed. |
| 2 | deploy/telemetry/install.sh | Binary download at line 184 has no visible checksum verification. | Verify against the release checksums file, as done at lines 373-374. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | internal/assets/{claude,kiro,cursor,kimi}/agents/*.md (26 files) | No example blocks in agent descriptions or bodies. | -15 each |
| 2 | Same 26 files | Description names no situation the agent is not for. | -5 each |
| 3 | internal/assets/opencode/agents/gentle-ai-worker.md | Vague quantifiers (4). | -8 |
| 4 | skills/gentle-ai-collab-perfect/SKILL.md | Vague quantifiers (3). | -6 |
| 5 | internal/assets/skills/{issue-creation,skill-registry}/SKILL.md | Vague quantifiers (2 each). | -4 each |

## Cross-Component
- `skills/` and `internal/assets/skills/` hold duplicate copies of 8 skills (branch-pr, chained-pr, cognitive-doc-design, comment-writer, gentle-ai-bench, rdd-defect-workflow, systemic-issue-triage, work-unit-commits). Content drift is possible. I did not diff the pairs.
- AGENTS.md skill names (`gentle-ai-branch-pr`, `gentle-ai-chained-pr`) match the SKILL.md `name` fields. The `issue-creation` path resolves.
- Reviewer prompts are duplicated per host (claude, kiro, cursor, kimi, opencode), so edits must be applied in five places.

## Recommendation
BLOCKED — do not submit PRs. File private security report. One Critical finding: a curl-to-bash fallback in `deploy/telemetry/install.sh:215`. The other pre-scan Critical matches appear to be documentation strings.
