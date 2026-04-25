# NLPM Audit: upstash/context7
**Date**: 2026-04-06  |  **Artifacts**: 9  |  **Strategy**: single
**NL Score**: 82/100
**Security**: CLEAR
**Bugs**: 2  |  **Quality Issues**: 16  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| plugins/claude/context7/commands/docs.md | Command | 46 | Missing `name` frontmatter (-25) |
| plugins/cursor/context7/agents/docs-researcher.md | Agent | 60 | No examples (-15), no model (-5), no output format (-10) |
| plugins/claude/context7/agents/docs-researcher.md | Agent | 65 | No examples (-15), no output format (-10) |
| plugins/claude/context7/skills/context7-mcp/SKILL.md | Skill | 94 | Vague quantifiers (-6) |
| plugins/cursor/context7/skills/context7-mcp/SKILL.md | Skill | 94 | Vague quantifiers (-6) |
| skills/context7-mcp/SKILL.md | Skill | 94 | Vague quantifiers (-6) |
| skills/find-docs/SKILL.md | Skill | 92 | Vague quantifiers (-8) |
| skills/context7-cli/SKILL.md | Skill | 96 | Vague quantifiers (-4) |
| plugins/claude/context7/.claude-plugin/plugin.json | Plugin Manifest | 95 | Missing recommended `version` field (-5) |

**Weighted average**: 82/100  (736 points across 9 artifacts)

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
| Hooks | none |
| Scripts (eslint.config.js) | eslint.config.js, packages/mcp/eslint.config.js, packages/sdk/eslint.config.js, packages/tools-ai-sdk/eslint.config.js, packages/cli/eslint.config.js |
| MCP configs | plugins/claude/context7/.mcp.json, plugins/cursor/context7/mcp.json |
| Package manifests | package.json, packages/mcp/package.json, packages/sdk/package.json, packages/tools-ai-sdk/package.json, packages/cli/package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | plugins/claude/context7/.mcp.json | 3 | external-http-mcp | MCP server is an external HTTP endpoint (https://mcp.context7.com/mcp); all tool calls route over the network to a third-party service. Users should be aware of data-sharing implications. |
| 2 | Medium | plugins/cursor/context7/mcp.json | 3 | external-http-mcp | MCP server is an external HTTP OAuth endpoint (https://mcp.context7.com/mcp/oauth); same external data-routing concern as the Claude variant. |
| 3 | Low | package.json | null | unpinned-semver | All devDependencies use `^` (caret) ranges, allowing minor/patch drift on reinstall, which could introduce undiscovered vulnerabilities. |
| 4 | Low | packages/cli/package.json | null | unpinned-semver | All production dependencies use `^` ranges (e.g. `commander ^13.1.0`, `open ^10.1.0`), allowing minor version drift in CLI distribution. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | plugins/claude/context7/commands/docs.md | Missing `name` frontmatter field | Command may fail registration in strict plugin systems that require an explicit name; discovery via `/help` is unreliable. |
| 2 | plugins/claude/context7/commands/docs.md | `allowed-tools` not declared; command calls `resolve-library-id` and `query-docs` | Tool permission checks may reject MCP calls at runtime if the host enforces declared-tool allowlists. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | plugins/claude/context7/.mcp.json | External HTTP MCP endpoint routes all queries to third-party service | Add a note in the plugin README that usage sends library queries to mcp.context7.com; no code change needed, just transparency. |
| 2 | plugins/cursor/context7/mcp.json | Same as above, OAuth variant | Same disclosure approach as #1. |
| 3 | package.json | Unpinned `^` devDependencies | Add `--frozen-lockfile` to CI install step; no version pinning change required in package.json itself. |
| 4 | packages/cli/package.json | Unpinned `^` production dependencies | Pin exact versions for production dependencies distributed via npm, or enforce lockfile in publish pipeline. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | plugins/claude/context7/agents/docs-researcher.md | Zero `<example>` blocks (R09 requires minimum 2 with Context + user msg + assistant response) | -15 |
| 2 | plugins/cursor/context7/agents/docs-researcher.md | Zero `<example>` blocks (same as #1) | -15 |
| 3 | plugins/claude/context7/agents/docs-researcher.md | No output format template (R12); guidelines list content but no structure | -10 |
| 4 | plugins/cursor/context7/agents/docs-researcher.md | No output format template (R12); same as #3 | -10 |
| 5 | plugins/cursor/context7/agents/docs-researcher.md | `model` not declared in frontmatter (R10); Claude variant declares `model: sonnet` | -5 |
| 6 | plugins/claude/context7/commands/docs.md | No empty input handling (R15); no behavior defined when `$ARGUMENTS` is blank | -10 |
| 7 | plugins/claude/context7/commands/docs.md | No output format template (R16); "Results include code examples and explanations" is not a structured template | -10 |
| 8 | plugins/claude/context7/agents/docs-researcher.md | Vague quantifiers (R01): "concise", "actionable" (L11), "focused" (L5), "relevant" (L26), "appropriate" (L24) — 5 instances | -10 |
| 9 | plugins/cursor/context7/agents/docs-researcher.md | Vague quantifiers (R01): same 5 instances as #8 (identical content) | -10 |
| 10 | plugins/claude/context7/commands/docs.md | Vague quantifiers (R01): "best" (L33), "relevant" (L33) — 2 instances | -4 |
| 11 | plugins/claude/context7/skills/context7-mcp/SKILL.md | Vague quantifiers (R01): "better" (L30, L55), "closest" (L39) — 3 instances | -6 |
| 12 | plugins/cursor/context7/skills/context7-mcp/SKILL.md | Vague quantifiers (R01): same 3 instances as #11 (identical content) | -6 |
| 13 | skills/context7-mcp/SKILL.md | Vague quantifiers (R01): same 3 instances as #11 (identical content) | -6 |
| 14 | skills/context7-cli/SKILL.md | Vague quantifiers (R01): "best" (L50), "closest" (L101) — 2 instances | -4 |
| 15 | skills/find-docs/SKILL.md | Vague quantifiers (R01): "best" (L50), "relevant" (L80, L116), "closest" (L101) — 4 instances | -8 |
| 16 | plugins/claude/context7/.claude-plugin/plugin.json | Missing recommended `version` field (R48 marks version as recommended; R50 requires bumping in four places on release) | -5 |

## Cross-Component
**Triplication of context7-mcp/SKILL.md**: The files at `plugins/claude/context7/skills/context7-mcp/SKILL.md`, `plugins/cursor/context7/skills/context7-mcp/SKILL.md`, and `skills/context7-mcp/SKILL.md` are byte-for-byte identical. Any fix — including resolving the 3 vague quantifier findings above — must be applied in three places. The canonical copy should live under `skills/` and be referenced or symlinked from the plugin directories, or the duplication should be called out explicitly in a scope note (R07).

**Cursor agent drift from Claude agent**: `plugins/cursor/context7/agents/docs-researcher.md` is a copy of the Claude variant but is missing the `model: sonnet` declaration present in the original. There is no mechanism to keep the two in sync; this is the first visible drift.

**commands/docs.md undeclared tools**: The command references `resolve-library-id` and `query-docs` in its workflow steps but declares neither in `allowed-tools`. The MCP config (`.mcp.json`) exposes the `context7` server which provides these tools, so the tool names are valid — the gap is purely in the command manifest.

## Recommendation
CLEAR — submit PRs for the 2 command frontmatter bugs (missing `name` and `allowed-tools`). Flag the external MCP endpoint findings in a tracking issue so maintainers can add a disclosure note to the README. No Critical or High security findings; the repo is safe to contribute to.
