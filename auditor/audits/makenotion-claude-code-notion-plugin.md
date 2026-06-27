# NLPM Audit: makenotion/claude-code-notion-plugin
**Date**: 2026-04-06  |  **Artifacts**: 15  |  **Strategy**: single
**NL Score**: 77/100
**Security**: CLEAR
**Bugs**: 2  |  **Quality Issues**: 21  |  **Security Findings**: 1

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude-plugin/plugin.json | plugin manifest | 50 | Missing `commands` and `skills` arrays — plugin registers nothing on install |
| commands/search.md | command | 71 | Missing allowed-tools; no empty-input handling; multi-step without numbered steps; 2 vague quantifiers |
| commands/find.md | command | 73 | Missing allowed-tools; no empty-input handling; multi-step without numbered steps; "best" vague |
| commands/create-task.md | command | 79 | Missing allowed-tools; no empty-input handling; 3 vague quantifiers |
| commands/tasks/explain-diff.md | command | 79 | Missing allowed-tools; multi-step without numbered process steps; 3 vague quantifiers |
| commands/tasks/plan.md | command | 79 | Missing allowed-tools; no empty-input handling; 3 vague quantifiers |
| skills/notion/knowledge-capture/SKILL.md | skill | 80 | Vague quantifiers at penalty cap ("appropriate", "relevant", "properly", "periodically") |
| skills/notion/meeting-intelligence/SKILL.md | skill | 80 | Vague quantifiers at penalty cap ("relevant", "recent", "important", "thoughtfully") |
| skills/notion/research-documentation/SKILL.md | skill | 80 | Vague quantifiers at penalty cap ("relevant", "appropriate", "recent") |
| skills/notion/spec-to-implementation/SKILL.md | skill | 80 | Vague quantifiers at penalty cap ("relevant", "appropriate") |
| commands/create-page.md | command | 81 | Missing allowed-tools; no empty-input handling; "sensible"/"brief" vague |
| commands/database-query.md | command | 81 | Missing allowed-tools; no empty-input handling; "reasonable"/"compact" vague |
| commands/tasks/build.md | command | 81 | Missing allowed-tools; no empty-input handling; "short generic"/"brief" vague |
| commands/tasks/setup.md | command | 83 | Missing allowed-tools; multi-step wizard without numbered steps; "helpful" vague |
| commands/create-database-row.md | command | 85 | Missing allowed-tools; no empty-input handling |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | None found |
| Scripts | None found |
| MCP configs | .mcp.json |
| Package manifests | None found |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | .mcp.json | 3 | external-http-mcp | MCP server uses HTTP transport to `https://mcp.notion.com/mcp`; workspace content (page text, database rows) traverses Notion's cloud API endpoint. Expected behavior for this integration but implies data leaves the local environment. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .claude-plugin/plugin.json | Missing `commands` array — 10 command files exist in `commands/` but none are declared in the manifest | Plugin installs without registering any slash commands; `claude plugin install` succeeds but `/notion:*` commands are unavailable |
| 2 | .claude-plugin/plugin.json | Missing `skills` array — 4 SKILL.md files exist in `skills/notion/*/` but none are declared in the manifest | Plugin installs without loading any skills; Notion workspace skill context is unavailable to agents |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | .mcp.json / README | External HTTP MCP transport sends workspace data to `mcp.notion.com`; no documentation of data flow | Add a note in README (or plugin description) that Notion workspace content traverses Notion's MCP API endpoint; link to Notion's data handling policy |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | All 10 commands | No `allowed-tools` field in frontmatter; any tool may be invoked without declaration | -5 each (×10) |
| 2 | commands/create-database-row.md | No handling for empty `$ARGUMENTS` — command proceeds to resolve a database with no input | -10 |
| 3 | commands/create-page.md | No handling for empty `$ARGUMENTS`; "sensible default structure" and "brief clarification question" — vague quantifiers | -10, -4 |
| 4 | commands/create-task.md | No handling for empty `$ARGUMENTS`; "appropriate Tasks database", "confidently identified", "concise clarification" — vague quantifiers | -10, -6 |
| 5 | commands/database-query.md | No handling for empty `$ARGUMENTS`; "reasonable number of rows", "compact table-like format" — vague quantifiers | -10, -4 |
| 6 | commands/find.md | No handling for empty `$ARGUMENTS`; multi-step Behavior listed as bullets without numbered steps; "best matches" — vague | -10, -10, -2 |
| 7 | commands/search.md | No handling for empty `$ARGUMENTS`; multi-step Behavior listed as bullets without numbered steps; "high-signal tools", "short, scannable list" — vague | -10, -10, -4 |
| 8 | commands/tasks/build.md | No handling for empty `$ARGS` (Notes handles invalid URL but not absent input); "short generic text description", "brief" — vague | -10, -4 |
| 9 | commands/tasks/explain-diff.md | Execution flow has no numbered steps — Sections describe output structure, not the process; "broadly explore", "use figures liberally", "medium difficulty" — vague | -10, -6 |
| 10 | commands/tasks/plan.md | No handling for empty `$ARGS`; "ask just a few questions", "too many questions", "briefly tell the user" — vague | -10, -6 |
| 11 | commands/tasks/setup.md | Two-path wizard uses `###` headers + bullets with no numbered top-level steps; "Be conversational and helpful" — "helpful" vague | -10, -2 |
| 12 | skills/notion/knowledge-capture/SKILL.md | Vague quantifiers at or above penalty cap: "appropriate" (×5+), "relevant" (×4+), "properly connected", "periodically" | -20 cap |
| 13 | skills/notion/meeting-intelligence/SKILL.md | Vague quantifiers at penalty cap: "relevant" (×10+), "recent updates", "important meetings", "Enrich thoughtfully" | -20 cap |
| 14 | skills/notion/research-documentation/SKILL.md | Vague quantifiers at penalty cap: "relevant" (×8+), "appropriate documentation template", "recent" | -20 cap |
| 15 | skills/notion/spec-to-implementation/SKILL.md | Vague quantifiers at penalty cap: "relevant" (×6+), "appropriate location", "relevant resources" | -20 cap |

## Cross-Component
**MCP server naming inconsistency**: `.mcp.json` registers the server as `"notion"` (lowercase). Commands describe it as `"notionApi MCP server"`. SKILL.md files reference tools as `Notion:notion-search`, `Notion:notion-fetch`, `Notion:notion-create-pages` (capital-N prefix). Three different labels for the same server increase contributor confusion; the capital-N tool prefix in SKILL.md suggests the server may self-identify as `Notion` rather than the `notion` key used in `.mcp.json`.

**Internal cross-reference intact**: `commands/tasks/build.md` step 4 references `/notion:tasks:explain-diff` — that command exists at `commands/tasks/explain-diff.md` ✅

**Plugin manifest gap**: `plugin.json` has no `commands` or `skills` arrays, so the 10 commands and 4 skills are invisible to `claude plugin install`. This is also recorded as Bugs #1 and #2 above.

**Reference files verified**: All `reference/` and `examples/` files linked from the four SKILL.md files exist on disk ✅

## Recommendation
CLEAR — submit PRs for bugs #1 and #2 (add `commands` and `skills` arrays to `plugin.json`). Address the medium security finding by adding a data-flow note to the README. Quality fixes (allowed-tools, empty-input handling, numbered steps, vague quantifiers) are high-value but non-blocking.
