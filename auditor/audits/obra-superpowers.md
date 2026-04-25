# NLPM Audit: obra/superpowers
**Date**: 2026-04-06  |  **Artifacts**: 22  |  **Strategy**: batched
**NL Score**: 92/100
**Security**: CLEAR
**Bugs**: 3  |  **Quality Issues**: 6  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/brainstorm.md | command | 60 | Missing `name` frontmatter (-25), no allowed-tools (-5), no empty input handling (-10) |
| commands/write-plan.md | command | 60 | Missing `name` frontmatter (-25), no allowed-tools (-5), no empty input handling (-10) |
| commands/execute-plan.md | command | 60 | Missing `name` frontmatter (-25), no allowed-tools (-5), no empty input handling (-10) |
| agents/code-reviewer.md | agent | 84 | Missing explicit output format section (-10); vague quantifiers: "proper"×2, "appropriate"×1 (-6) |
| CLAUDE.md | project-doc | 85 | No frontmatter (file type does not conventionally require it; minor deduction) |
| hooks/hooks.json | hook-config | 90 | `matcher` field on SessionStart hook is non-standard and likely silently ignored |
| hooks/hooks-cursor.json | hook-config | 95 | No issues found; minor deduction for format divergence from hooks.json |
| skills/brainstorming/SKILL.md | skill | 98 | "appropriately-scoped" vague quantifier (-2) |
| skills/using-git-worktrees/SKILL.md | skill | 100 | None |
| skills/receiving-code-review/SKILL.md | skill | 100 | None |
| skills/executing-plans/SKILL.md | skill | 100 | None |
| skills/subagent-driven-development/SKILL.md | skill | 100 | None |
| skills/test-driven-development/SKILL.md | skill | 100 | None |
| skills/finishing-a-development-branch/SKILL.md | skill | 100 | None |
| skills/dispatching-parallel-agents/SKILL.md | skill | 100 | None |
| skills/using-superpowers/SKILL.md | skill | 100 | None |
| skills/systematic-debugging/SKILL.md | skill | 100 | None |
| skills/writing-skills/SKILL.md | skill | 100 | None |
| skills/verification-before-completion/SKILL.md | skill | 100 | None |
| skills/requesting-code-review/SKILL.md | skill | 100 | None |
| skills/writing-plans/SKILL.md | skill | 100 | None |
| .claude-plugin/plugin.json | manifest | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hook configs | hooks/hooks.json, hooks/hooks-cursor.json |
| Hook scripts | hooks/run-hook.cmd (polyglot), hooks/session-start (bash) |
| Shell scripts | scripts/bump-version.sh, scripts/sync-to-codex-plugin.sh |
| MCP configs | none |
| Package manifests | package.json (no scripts/dependencies), tests/brainstorm-server/package.json (not audited) |

### Security Findings
No security findings.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/brainstorm.md | Missing `name` field in frontmatter | Command registration may fail or fall back to filename; canonical name not declared |
| 2 | commands/write-plan.md | Missing `name` field in frontmatter | Command registration may fail or fall back to filename; canonical name not declared |
| 3 | commands/execute-plan.md | Missing `name` field in frontmatter | Command registration may fail or fall back to filename; canonical name not declared |

**Notes on deprecated commands:** All three missing-name commands are intentional deprecation stubs whose only function is to redirect users to the corresponding skill. Even so, the `name` field is a required frontmatter field per the schema; without it the command entry is malformed. Fix: add `name: brainstorm`, `name: write-plan`, and `name: execute-plan` to the respective frontmatter blocks.

## Security Fixes (PR-worthy, Medium/Low only)
No security findings requiring fixes.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/code-reviewer.md | No explicit output format section; output structure is described only in prose ("structured, actionable, and focused") | -10 |
| 2 | agents/code-reviewer.md | Vague quantifier "proper" in "proper error handling, type safety, and defensive programming" (L20) | -2 |
| 3 | agents/code-reviewer.md | Vague quantifier "proper" in "proper separation of concerns and loose coupling" (L28) | -2 |
| 4 | agents/code-reviewer.md | Vague quantifier "appropriate" in "code includes appropriate comments and documentation" (L34) | -2 |
| 5 | skills/brainstorming/SKILL.md | Vague quantifier "appropriately-scoped" in "For appropriately-scoped projects" (L75) | -2 |
| 6 | hooks/hooks.json | `matcher: "startup\|clear\|compact"` on a SessionStart hook — matchers are defined for PostToolUse to filter tool names; for SessionStart there is no tool invocation to match against. This field is likely silently ignored by Claude Code. hooks-cursor.json omits the matcher correctly. | 0 (info) |

## Cross-Component
All cross-referenced companion files were verified to exist:
- `skills/brainstorming/visual-companion.md` ✓
- `skills/brainstorming/spec-document-reviewer-prompt.md` ✓
- `skills/subagent-driven-development/implementer-prompt.md` ✓
- `skills/subagent-driven-development/spec-reviewer-prompt.md` ✓
- `skills/subagent-driven-development/code-quality-reviewer-prompt.md` ✓
- `skills/requesting-code-review/code-reviewer.md` ✓
- `skills/writing-skills/testing-skills-with-subagents.md` ✓
- `skills/writing-skills/graphviz-conventions.dot` ✓
- `skills/writing-skills/persuasion-principles.md` ✓
- `skills/systematic-debugging/root-cause-tracing.md` ✓
- `skills/systematic-debugging/defense-in-depth.md` ✓
- `skills/systematic-debugging/condition-based-waiting.md` ✓

All three deprecated commands (brainstorm, write-plan, execute-plan) correctly reference their successor skills (superpowers:brainstorming, superpowers:writing-plans, superpowers:executing-plans), and all three target skills exist.

The skills/ library is internally consistent: integration references between executing-plans, subagent-driven-development, writing-plans, using-git-worktrees, finishing-a-development-branch, test-driven-development, systematic-debugging, requesting-code-review, and verification-before-completion all resolve to existing files.

**No broken references, orphaned components, or terminology contradictions detected.**

## Recommendation
CLEAR — submit PRs for all three bugs (missing `name` in deprecated command stubs). The fix is a one-line frontmatter addition per file and is low-risk. No security findings; no security-related PRs needed.
