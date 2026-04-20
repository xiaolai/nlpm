# NLPM Audit: jnMetaCode/superpowers-zh
**Date**: 2026-04-20  |  **Artifacts**: 27  |  **Strategy**: batched
**NL Score**: 95/100
**Security**: CLEAR
**Bugs**: 3  |  **Quality Issues**: 8  |  **Security Findings**: 2

## NL Score Summary

> Non-NL artifacts (hooks.json, hooks-cursor.json, plugin.json) are listed in the security inventory below; they are excluded from NL scoring. The 24 NL artifacts produce a weighted mean of **94.75 → 95/100**.

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/brainstorm.md | command | 60 | Missing `name` frontmatter; deprecated stub lacking allowed-tools & empty-input guard |
| commands/write-plan.md | command | 60 | Missing `name` frontmatter; deprecated stub lacking allowed-tools & empty-input guard |
| commands/execute-plan.md | command | 60 | Missing `name` frontmatter; deprecated stub lacking allowed-tools & empty-input guard |
| agents/code-reviewer.md | agent | 94 | Three vague quantifiers 恰当/适当 (-6 total) |
| skills/brainstorming/SKILL.md | skill | 100 | None |
| skills/chinese-code-review/SKILL.md | skill | 100 | None |
| skills/chinese-commit-conventions/SKILL.md | skill | 100 | None |
| skills/chinese-documentation/SKILL.md | skill | 100 | None |
| skills/chinese-git-workflow/SKILL.md | skill | 100 | None |
| skills/dispatching-parallel-agents/SKILL.md | skill | 100 | None |
| skills/executing-plans/SKILL.md | skill | 100 | None |
| skills/finishing-a-development-branch/SKILL.md | skill | 100 | None |
| skills/mcp-builder/SKILL.md | skill | 100 | None |
| skills/receiving-code-review/SKILL.md | skill | 100 | None |
| skills/requesting-code-review/SKILL.md | skill | 100 | None |
| skills/subagent-driven-development/SKILL.md | skill | 100 | None |
| skills/systematic-debugging/SKILL.md | skill | 100 | None |
| skills/test-driven-development/SKILL.md | skill | 100 | None |
| skills/using-git-worktrees/SKILL.md | skill | 100 | None |
| skills/using-superpowers/SKILL.md | skill | 100 | None |
| skills/verification-before-completion/SKILL.md | skill | 100 | None |
| skills/workflow-runner/SKILL.md | skill | 100 | None |
| skills/writing-plans/SKILL.md | skill | 100 | None |
| skills/writing-skills/SKILL.md | skill | 100 | None |

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 2 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hook config (Claude Code) | hooks/hooks.json |
| Hook config (Cursor) | hooks/hooks-cursor.json |
| Hook launcher (cross-platform wrapper) | hooks/run-hook.cmd |
| Hook script (bash) | hooks/session-start |
| Package manifest | package.json |
| MCP configs | none |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Low | package.json | 4 | Unpinned version constraint | `"node": ">=14.0.0"` is very permissive; any Node ≥ 14 is accepted, including EOL versions with known CVEs. |
| 2 | Low | hooks/session-start | 18 | File read injected into session context | `cat "${PLUGIN_ROOT}/skills/using-superpowers/SKILL.md"` output is embedded verbatim in every session's context. If the SKILL.md were tampered (supply-chain), it would be injected into every AI session. Mitigated by: path is inside the plugin install dir, content is properly JSON-escaped, no network calls involved. |

**Detailed notes on hook scripts:**
- `hooks/run-hook.cmd`: Cross-platform polyglot (batch + bash). Script name is hard-coded in hooks.json as `"session-start"` — no user-controlled argument. The `exec bash "${SCRIPT_DIR}/${SCRIPT_NAME}" "$@"` on line 43 passes remaining args safely via `"$@"`. No injection risk.
- `hooks/session-start`: Uses `set -euo pipefail`. JSON-escapes output via bash parameter substitution (no eval). No network calls. No credential access. No sudo. Well-written.

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/brainstorm.md | Missing `name` field in YAML frontmatter | NLPM convention violation; name-based plugin discovery may fail |
| 2 | commands/write-plan.md | Missing `name` field in YAML frontmatter | Same as above |
| 3 | commands/execute-plan.md | Missing `name` field in YAML frontmatter | Same as above |

> **Context:** All three are intentional deprecation-notice commands (one-liners telling the user to use the corresponding skill instead). Adding `name` is a mechanical fix with no behavioral change.

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | package.json | Loose Node version constraint `>=14.0.0` | Tighten to `>=18.0.0` (LTS, actively maintained) to exclude EOL versions with known vulnerabilities |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/code-reviewer.md | "**恰当**" (appropriate) at line 20: "检查错误处理、类型安全和防御性编程是否**恰当**" | -2 |
| 2 | agents/code-reviewer.md | "**恰当**" (appropriate) at line 27: "检查关注点分离和松耦合是否**恰当**" | -2 |
| 3 | agents/code-reviewer.md | "**适当的**" (appropriate) at line 33: "验证代码包含**适当的**注释和文档" | -2 |
| 4 | agents/code-reviewer.md | `model: inherit` — delegates model selection to caller rather than declaring an explicit tier; harder to discover intent | informational |
| 5 | skills/writing-skills/SKILL.md | References `@testing-skills-with-subagents.md`, `anthropic-best-practices.md`, `render-graphs.js`, `persuasion-principles.md` via `@`-syntax inline loads — these files are not present in this zh fork | informational |
| 6 | skills/systematic-debugging/SKILL.md | References `root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md` in the same skill directory — not confirmed present in this fork | informational |
| 7 | skills/subagent-driven-development/SKILL.md | References `./implementer-prompt.md`, `./spec-reviewer-prompt.md`, `./code-quality-reviewer-prompt.md` as prompt templates — not present in listed artifacts | informational |
| 8 | skills/test-driven-development/SKILL.md | References `@testing-anti-patterns.md` via inline load — not confirmed present in this fork | informational |

## Cross-Component

**Orphaned references (zh fork vs upstream):**  
This repo is a Chinese adaptation of the upstream `superpowers` plugin. Several skills contain `@`-syntax references to supporting files that exist upstream but are not confirmed to be present here:
- `writing-skills` → 4 upstream support files
- `systematic-debugging` → 3 companion `.md` files (root-cause-tracing, defense-in-depth, condition-based-waiting)  
- `subagent-driven-development` → 3 prompt template files
- `test-driven-development` → `testing-anti-patterns.md`

If these files were not ported, the `@` inline-load calls will silently fail or error at runtime.

**Verified references:**
- `requesting-code-review` → `agents/code-reviewer.md` ✓ (agent present and scored)
- `brainstorming` → `writing-plans` skill ✓ (present)
- `subagent-driven-development` → `finishing-a-development-branch`, `using-git-worktrees`, `requesting-code-review`, `writing-plans` ✓ (all present)
- `executing-plans` → `finishing-a-development-branch`, `using-git-worktrees`, `writing-plans` ✓ (all present)

**Deprecated command stubs (brainstorm, write-plan, execute-plan):**  
All three deprecated commands correctly point to their successor skills (`brainstorming`, `writing-plans`, `executing-plans`), which exist in the `skills/` directory. The migration path is valid; only the frontmatter is incomplete.

**Structural summary:**  
The skill graph is well-connected for the core development workflow (brainstorm → write-plan → execute/subagent → finish). Chinese-specific skills (chinese-code-review, chinese-commit-conventions, chinese-documentation, chinese-git-workflow) are self-contained and do not depend on missing upstream files. The main gap is the ~10 supporting reference files that appear to have been left behind from the translation effort.

## Recommendation

CLEAR — submit PRs for all bugs and medium/low security fixes.

**Priority order:**
1. **Add `name` to three deprecated commands** (1-line fix each, purely mechanical)
2. **Tighten Node version in package.json** (`>=14.0.0` → `>=18.0.0`)
3. **Investigate orphaned `@`-references** — either port the missing supporting files from upstream or replace references with inline content; this is the largest usability risk for users trying to follow the cross-skill links

The skill library is high quality: 20 of 24 NL artifacts score 100/100. The Chinese-original skills (chinese-code-review, chinese-commit-conventions, chinese-documentation, chinese-git-workflow, mcp-builder, workflow-runner) are well-structured, specific, and actionable with no scoring penalties.
