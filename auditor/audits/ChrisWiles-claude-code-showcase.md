# NLPM Audit: ChrisWiles/claude-code-showcase
**Date**: 2026-04-12  |  **Artifacts**: 17  |  **Strategy**: single
**NL Score**: 81/100
**Security**: CLEAR
**Bugs**: 8  |  **Quality Issues**: 13  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/commands/onboard.md | command | 23 | No frontmatter at all; missing name, description, allowed-tools; bullets not steps |
| .claude/commands/ticket.md | command | 61 | Missing `name` frontmatter; no empty-input guard; vague "relevant"/"related" |
| .claude/commands/code-quality.md | command | 65 | Missing `name` frontmatter; no empty-input guard for $ARGUMENTS |
| .claude/commands/pr-review.md | command | 65 | Missing `name` frontmatter; no empty-input guard for $ARGUMENTS |
| .claude/commands/pr-summary.md | command | 71 | Missing `name` frontmatter; vague "brief"/"significant" |
| .claude/commands/docs-sync.md | command | 75 | Missing `name` frontmatter |
| .claude/hooks/skill-rules.json | config | 80 | 13 skill references with no corresponding SKILL.md files |
| ./CLAUDE.md | config | 85 | Minor; well-structured, no critical issues |
| .claude/agents/github-workflow.md | agent | 90 | No explicit output format section |
| .claude/hooks/skill-rules.schema.json | config | 95 | Well-formed; no issues |
| .claude/skills/core-components/SKILL.md | skill | 95 | None |
| .claude/skills/formik-patterns/SKILL.md | skill | 95 | None |
| .claude/skills/graphql-schema/SKILL.md | skill | 95 | None |
| .claude/skills/react-ui-patterns/SKILL.md | skill | 95 | None |
| .claude/skills/systematic-debugging/SKILL.md | skill | 95 | None |
| .claude/skills/testing-patterns/SKILL.md | skill | 95 | None |
| .claude/agents/code-reviewer.md | agent | 95 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks (scripts) | `.claude/hooks/skill-eval.sh`, `.claude/hooks/skill-eval.js` |
| MCP configs | `.mcp.json` |
| Inline hook commands | `.claude/settings.json` (4 PostToolUse + 1 PreToolUse + 1 UserPromptSubmit) |
| Package manifests | None (no `package.json` or `requirements.txt` in repo root) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | `.mcp.json` | 35-42 | broad MCP permissions | `@anthropic/mcp-postgres` grants full database read/write access with no permission scoping. Any Claude session with this config can query or modify the entire database. |
| 2 | Medium | `.mcp.json` | 2-74 | runtime package install | All 7 MCP servers use `npx -y @anthropic/mcp-*` without pinning a package version. A malicious or hijacked npm publish to any `@anthropic/mcp-*` package is silently adopted on next run. |
| 3 | Low | `.claude/commands/pr-review.md` | 11 | unquoted $ARGUMENTS in shell | `gh pr view $ARGUMENTS` — if `$ARGUMENTS` contains shell metacharacters or extra tokens the AI constructs a literal shell invocation, bypassing the `Bash(gh:*)` restriction intent. |
| 4 | Low | `.claude/commands/code-quality.md` | 12 | unquoted $ARGUMENTS in shell | `npm run lint -- $ARGUMENTS` — same unquoted expansion risk; malformed input could inject extra flags into the npm invocation. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `.claude/commands/code-quality.md` | Missing `name` frontmatter field | Command cannot be registered by name; breaks `/code-quality` invocation |
| 2 | `.claude/commands/docs-sync.md` | Missing `name` frontmatter field | Command cannot be registered by name; breaks `/docs-sync` invocation |
| 3 | `.claude/commands/onboard.md` | Missing `name` frontmatter field | Command cannot be registered by name; breaks `/onboard` invocation |
| 4 | `.claude/commands/onboard.md` | Missing `description` frontmatter field | No description for UI or discovery; treated as anonymous artifact |
| 5 | `.claude/commands/onboard.md` | Missing `allowed-tools` frontmatter field | Claude has no declared tool boundary; may use arbitrary tools |
| 6 | `.claude/commands/pr-review.md` | Missing `name` frontmatter field | Command cannot be registered by name; breaks `/pr-review` invocation |
| 7 | `.claude/commands/pr-summary.md` | Missing `name` frontmatter field | Command cannot be registered by name; breaks `/pr-summary` invocation |
| 8 | `.claude/commands/ticket.md` | Missing `name` frontmatter field | Command cannot be registered by name; breaks `/ticket` invocation |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `.mcp.json` | `npx -y` without version pins across all 7 MCP servers | Pin each package: `"args": ["-y", "@anthropic/mcp-jira@1.x.x"]`; use `npm install` + lockfile or `npx @anthropic/mcp-jira@<exact-version>` |
| 2 | `.mcp.json` | postgres MCP has full DB access, no permission scoping | Document clearly that the token/URL should be a read-only role; add a comment in the JSON or a companion `.mcp.README.md` warning that DATABASE_URL must not be a superuser credential |
| 3 | `.claude/commands/pr-review.md` | Unquoted `$ARGUMENTS` in `gh pr view $ARGUMENTS` | Change to `gh pr view "$ARGUMENTS"` (quoted) to prevent word-splitting |
| 4 | `.claude/commands/code-quality.md` | Unquoted `$ARGUMENTS` in `npm run lint -- $ARGUMENTS` | Change to `npm run lint -- "$ARGUMENTS"` |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `.claude/agents/github-workflow.md` | No explicit output format section — checklist covers what to do, not how the agent formats its response | -10 |
| 2 | `.claude/commands/code-quality.md` | No empty-input guard: if `$ARGUMENTS` is blank, `npm run lint --` runs on no path | -10 |
| 3 | `.claude/commands/pr-review.md` | No empty-input guard: `gh pr view` without PR number fails or prompts interactively | -10 |
| 4 | `.claude/commands/ticket.md` | No empty-input guard: ticket workflow with no ticket ID would stall at step 1 | -10 |
| 5 | `.claude/commands/onboard.md` | Instructions use bullet points, not numbered steps — harder to follow procedurally | -10 |
| 6 | `.claude/commands/onboard.md` | No empty-input guard: `$ARGUMENTS` used as "context" with no fallback if absent | -10 |
| 7 | `.claude/commands/onboard.md` | Vague quantifier: "make sure it's comprehensive" gives no measurable criterion | -2 |
| 8 | `.claude/commands/ticket.md` | Vague: "check relevant skills" (step 4) — relevant to what? | -2 |
| 9 | `.claude/commands/ticket.md` | Vague: "Link it to the current ticket if related" (step 7) — no definition of "related" | -2 |
| 10 | `.claude/commands/pr-summary.md` | Vague: "Brief description" and "significant changes" without thresholds | -4 |
| 11 | `.claude/hooks/skill-rules.json` | References 13 skills with no corresponding SKILL.md: `navigation-architecture`, `i18n-translations`, `state-management`, `github-actions`, `analytics-tracking`, `list-pagination`, `modal-actionsheet`, `maestro-e2e`, `receiving-code-review`, `documentation`, `typescript-conventions`, `verification-before-completion`, `defense-in-depth`. Hook will suggest skills Claude cannot load. | -20 (cap) |
| 12 | `.claude/agents/github-workflow.md` | Vague: "Brief description" in PR body template | -2 |
| 13 | `.github/workflows/pr-claude-code-review.yml` | References `claude-opus-4-5-20251101` model — this model ID predates the current Claude family (4.6); should use `claude-opus-4-6` or latest stable | informational |

## Cross-Component
**Broken skill references in skill-rules.json**: The hook engine (skill-eval.js) matches 13 skill names (`navigation-architecture`, `i18n-translations`, `state-management`, `github-actions`, `analytics-tracking`, `list-pagination`, `modal-actionsheet`, `maestro-e2e`, `receiving-code-review`, `documentation`, `typescript-conventions`, `verification-before-completion`, `defense-in-depth`) that have no SKILL.md counterpart in `.claude/skills/`. When the hook fires and surfaces these names, Claude will attempt to invoke skills that don't exist, silently failing or confusing the developer.

**Intact references**:
- `pr-review.md` → `.claude/agents/code-reviewer.md` ✓
- `CLAUDE.md` skill activation table → all 5 skills present ✓
- `.claude/settings.json` hook → `.claude/hooks/skill-eval.sh` ✓
- `skill-eval.sh` → `skill-eval.js` ✓
- `skill-rules.json` `$schema` → `skill-rules.schema.json` ✓

**Inconsistency**: `skill-rules.json` has `directoryMappings` for `src/screens` and `src/navigation` pointing to `navigation-architecture`, and `src/graphql` pointing to `graphql-schema`. The `graphql-schema` skill exists; the navigation mapping is orphaned.

**GitHub Actions model drift**: All four workflows pin `model: claude-opus-4-5-20251101`. The project's `.claude/agents/code-reviewer.md` correctly specifies `model: opus`, but the workflows hardcode an older model ID string. These should be kept in sync.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

Priority order:
1. **Bug batch PR** — Add `name` frontmatter to all 6 commands; add `description` and `allowed-tools` to `onboard.md`. This unblocks command registration for all 6 slash commands.
2. **Security PR** — Pin MCP package versions in `.mcp.json`; quote `$ARGUMENTS` in `pr-review.md` and `code-quality.md`; add a postgres permission warning comment.
3. **Skill stub PR** — Either create stub SKILL.md files for the 13 referenced-but-missing skills, or remove the orphaned entries from `skill-rules.json` so the hook doesn't surface dead skill names.
4. **Quality PR** — Add empty-input guards to `code-quality.md`, `pr-review.md`, `ticket.md`, `onboard.md`; add numbered steps to `onboard.md`; add output format section to `github-workflow.md`.
