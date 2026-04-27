# NLPM Audit: firetiger-oss/claude-plugin
**Date**: 2026-04-27  |  **Artifacts**: 8  |  **Strategy**: single
**NL Score**: 84/100
**Security**: CLEAR
**Bugs**: 2  |  **Quality Issues**: 19  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/firetiger.md | AGENT | 35 | Missing name and description frontmatter (-50), no model declared (-5), no output format (-10) |
| commands/query.md | COMMAND | 85 | Missing output format (-10), missing allowed-tools (-5) |
| commands/setup.md | COMMAND | 87 | Missing allowed-tools (-5), four vague quantifiers (-8) |
| commands/instrument.md | COMMAND | 91 | Missing allowed-tools (-5), vague "quickly" and "minimal" (-4) |
| commands/investigate.md | COMMAND | 91 | Missing allowed-tools (-5), vague "Relevant" and "Detailed" (-4) |
| commands/create-agent.md | COMMAND | 93 | Missing allowed-tools (-5), vague "fully configured" (-2) |
| commands/monitor-deploy.md | COMMAND | 93 | Missing allowed-tools (-5), vague "targeted" (-2) |
| .claude-plugin/plugin.json | MANIFEST | 95 | No commands/agents registry listing |

**Weighted average (equal weights):** (35 + 85 + 87 + 91 + 91 + 93 + 93 + 95) / 8 = **84/100**

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | None found |
| Scripts | None found |
| MCP Configs | `.mcp.json` |
| Package Manifests | None found |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | .mcp.json | 5 | external-http-mcp | MCP server is a remote HTTP endpoint (`https://api.cloud.firetiger.com/mcp/v1`). No credentials are hardcoded and the server is the plugin vendor's own endpoint, but all telemetry data and credential responses traverse this external connection. |
| 2 | Medium | commands/monitor-deploy.md | 39 | user-content-in-shell | The command instructs Claude to run `gh pr comment <PR_NUMBER> --body "@firetiger <monitoring context>"` where `<monitoring context>` is assembled from user suggestions plus PR diff analysis. If the user-supplied text contains unescaped shell metacharacters (double quotes, backticks, `$(...)`), they could escape the `--body` argument boundary before gh receives it. |
| 3 | Low | commands/setup.md | 282 | open-external-url | The command instructs Claude to run `open "URL"` (macOS) or `xdg-open "URL"` (Linux) with a URL returned by the `get_checkout_url` MCP tool. The URL source is the vendor's own MCP server, so the trust level is already established, but `open`/`xdg-open` can handle `file://` and other non-http schemes if the server ever returns them. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | agents/firetiger.md | Missing `name` field in YAML frontmatter — the file has no `---` frontmatter block at all | Claude Code cannot register or discover this agent by name; the plugin loses its primary context document |
| 2 | agents/firetiger.md | Missing `description` field in YAML frontmatter | No description surfaced in agent listings or help output; breaks the agent registry entry |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | commands/monitor-deploy.md | User-influenced content interpolated into a bare shell command string | Pass the `--body` value through a heredoc or use `printf '%s'` to avoid shell word-splitting: `gh pr comment "$PR_NUMBER" --body "$(printf '%s' "@firetiger $CONTEXT")"`, or instruct Claude to always write the body to a temp file and use `--body-file` |
| 2 | commands/setup.md | `open`/`xdg-open` called with an MCP-supplied URL | Add a guard that validates the URL scheme is `https://` before opening; document in the command that only `https://` URLs from `get_checkout_url` should be opened |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/firetiger.md | Model not declared — no frontmatter means no model tier specified | -5 |
| 2 | agents/firetiger.md | No output format — agent has no section describing what format its responses should take | -10 |
| 3 | commands/create-agent.md | No `allowed-tools` declaration | -5 |
| 4 | commands/create-agent.md | Vague quantifier: "fully configured" (step 3) — completion criterion is undefined | -2 |
| 5 | commands/instrument.md | No `allowed-tools` declaration; command writes files (needs Write/Edit) and may run npm/pip (needs Bash) | -5 |
| 6 | commands/instrument.md | Vague quantifier: "Quickly identify" (step 2) — no time bound or scan depth specified | -2 |
| 7 | commands/instrument.md | Vague quantifier: "minimal instrumentation" (step 4) — what counts as minimal is not defined | -2 |
| 8 | commands/investigate.md | No `allowed-tools` declaration | -5 |
| 9 | commands/investigate.md | Vague quantifier: "Relevant services" (create fields) — no criteria for relevance | -2 |
| 10 | commands/investigate.md | Vague quantifier: "Detailed context" (create fields) — depth of detail unspecified | -2 |
| 11 | commands/monitor-deploy.md | No `allowed-tools` declaration; command runs Bash (gh CLI) | -5 |
| 12 | commands/monitor-deploy.md | Vague quantifier: "targeted monitoring plan" (line 13) — targeting criteria not defined | -2 |
| 13 | commands/query.md | No `allowed-tools` declaration | -5 |
| 14 | commands/query.md | Missing output format — the guide shows how to write SQL queries but never specifies how results should be presented to the user | -10 |
| 15 | commands/setup.md | No `allowed-tools` declaration; command runs Bash extensively (curl, aws, gcloud, wrangler, open) | -5 |
| 16 | commands/setup.md | Vague quantifier: "minimal user interaction" (line 9) — no threshold defined | -2 |
| 17 | commands/setup.md | Vague quantifier: "Proactively connect" (line 67) — what triggers proactive action is unclear | -2 |
| 18 | commands/setup.md | Vague quantifier: "some connections were skipped" (line 87) — "some" is non-specific | -2 |
| 19 | commands/setup.md | Vague quantifier: "genuinely uncertain" (line 327) — no criteria for genuine uncertainty | -2 |

## Cross-Component
**CC-1 — Orphaned resource in agent context:** `agents/firetiger.md` lists the supported MCP resource collections as `agents`, `known-issues`, `connections`, `runbooks`, and `triggers` (lines 30–35). The `investigations` collection is absent from this list. However, `commands/investigate.md` implements a full investigations workflow (create, get, update, list, schema). Users relying on the agent context file to discover available resources will not know that investigations exist.

**CC-2 — Cross-reference is consistent:** `commands/instrument.md` (line 8) correctly notes "use `/firetiger:setup` for the full setup including agent creation," and `agents/firetiger.md` (line 63) correctly references `/firetiger:setup`. The command namespace `firetiger:*` matches `plugin.json` `"name": "firetiger"`.

**CC-3 — Auth flow coverage gap:** `commands/setup.md` (step 1) handles the case where MCP tools are not yet loaded and prompts the user through the `/mcp` auth flow. No other command includes this guard. Commands like `commands/query.md`, `commands/investigate.md`, and `commands/create-agent.md` will silently fail if the MCP server is not authenticated; they should either include an auth fallback or reference the setup command.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes. Fix the two frontmatter bugs on `agents/firetiger.md` (add a YAML `---` block with `name` and `description`) and address the two security fixes (shell escaping in monitor-deploy, URL scheme guard in setup). The quality issues (missing `allowed-tools`, vague quantifiers, missing output format on query) are informational improvements worth a follow-up PR.
