# NLPM Audit: agent-sh/enhance
**Date**: 2026-04-27  |  **Artifacts**: 20  |  **Strategy**: single
**NL Score**: 86/100
**Security**: CLEAR
**Bugs**: 2  |  **Quality Issues**: 22  |  **Security Findings**: 2

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/claudemd-enhancer.md | Agent | 73 | No examples (-15), no output format (-10), vague description (-2) |
| agents/cross-file-enhancer.md | Agent | 73 | No examples (-15), no output format (-10), "complex" vague (-2) |
| agents/docs-enhancer.md | Agent | 73 | No examples (-15), no output format (-10), "balance" vague (-2) |
| agents/hooks-enhancer.md | Agent | 73 | No examples (-15), no output format (-10), "cautious" vague (-2) |
| agents/skills-enhancer.md | Agent | 73 | No examples (-15), no output format (-10), "consider" vague (-2) |
| agents/agent-enhancer.md | Agent | 75 | No examples (-15), no output format (-10) |
| agents/plugin-enhancer.md | Agent | 75 | No examples (-15), no output format (-10) |
| agents/prompt-enhancer.md | Agent | 75 | No examples (-15), no output format (-10) |
| CLAUDE.md | Project memory | 90 | Critical rules lack WHY explanations |
| skills/enhance-hooks/SKILL.md | Skill | 92 | Four vague terms: "complex", "simple", "unreasonably", "cautious" (-8) |
| commands/enhance.md | Command | 93 | Missing allowed-tools in frontmatter (-5), "relevant" vague (-2) |
| skills/enhance-plugins/SKILL.md | Skill | 94 | "relevant", "consider", "large" vague (-6) |
| .claude-plugin/plugin.json | Plugin manifest | 95 | Version 5.1.0 out of sync with package.json 1.0.0 |
| skills/enhance-claude-memory/SKILL.md | Skill | 95 | Missing argument-hint; "consider", "may" vague (-4) |
| skills/enhance-cross-file/SKILL.md | Skill | 95 | No examples block for a complex multi-pattern skill |
| skills/enhance-orchestrator/SKILL.md | Skill | 95 | No examples block for complex multi-phase orchestration |
| skills/enhance-skills/SKILL.md | Skill | 96 | "consider", "clearly" vague (-4) |
| skills/enhance-agent-prompts/SKILL.md | Skill | 98 | "consider" in constraints (-2) |
| skills/enhance-docs/SKILL.md | Skill | 98 | "balance" in guidance (-2) |
| skills/enhance-prompts/SKILL.md | Skill | 98 | "if needed" in examples guidance (-2) |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts | 1 (scripts/setup-hooks.sh) |
| JS libs (execution surfaces) | 92 files in lib/ |
| MCP configs | 0 |
| Package manifests | 2 (package.json, lib/package.json) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | lib/binary/index.js | 188 | network-download-exec | Runtime binary download from GitHub releases (`agent-sh/agent-analyzer`). Binary is fetched via HTTPS, SHA-256-verified, optionally SLSA-attested, then executed. Security hardening is solid but this is a supply chain surface: a compromised GitHub release token plus matching SHA-256 sidecar would bypass the checksum gate (only SLSA closes that hole). |
| 2 | Low | lib/binary/index.js | 679 | soft-attestation-default | SLSA attestation is soft-fail by default. When `gh` CLI is absent, verification is skipped with a warning and the binary executes on SHA-256 alone. A `stolen-release-token + attacker-sha256` attack would succeed in any environment without `gh`. Set `AGENT_ANALYZER_REQUIRE_ATTESTATION=1` to harden. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/enhance.md | Missing `allowed-tools` field in frontmatter | Command permission model broken; Claude Code cannot determine which tools to pre-authorise when dispatching the command |
| 2 | .claude-plugin/plugin.json | Version `5.1.0` does not match `package.json` version `1.0.0` | Plugin's own `enhance-plugins` skill flags this as a HIGH-certainty structural bug; confuses version-pinning consumers |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | lib/binary/index.js | SLSA attestation soft-fail default | Document `AGENT_ANALYZER_REQUIRE_ATTESTATION=1` prominently in README and recommend enabling it in any CI environment that runs the plugin |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/agent-enhancer.md | No examples block in agent body | -15 |
| 2 | agents/claudemd-enhancer.md | No examples block in agent body | -15 |
| 3 | agents/cross-file-enhancer.md | No examples block in agent body | -15 |
| 4 | agents/docs-enhancer.md | No examples block in agent body | -15 |
| 5 | agents/hooks-enhancer.md | No examples block in agent body | -15 |
| 6 | agents/plugin-enhancer.md | No examples block in agent body | -15 |
| 7 | agents/prompt-enhancer.md | No examples block in agent body | -15 |
| 8 | agents/skills-enhancer.md | No examples block in agent body | -15 |
| 9 | agents/agent-enhancer.md | No explicit output format specification (delegates entirely to skill) | -10 |
| 10 | agents/claudemd-enhancer.md | No explicit output format specification | -10 |
| 11 | agents/cross-file-enhancer.md | No explicit output format specification | -10 |
| 12 | agents/docs-enhancer.md | No explicit output format specification | -10 |
| 13 | agents/hooks-enhancer.md | No explicit output format specification | -10 |
| 14 | agents/plugin-enhancer.md | No explicit output format specification | -10 |
| 15 | agents/prompt-enhancer.md | No explicit output format specification | -10 |
| 16 | agents/skills-enhancer.md | No explicit output format specification | -10 |
| 17 | agents/claudemd-enhancer.md | Description uses "better AI understanding" — vague outcome claim | -2 |
| 18 | agents/cross-file-enhancer.md | "no complex reasoning needed" — "complex" is vague | -2 |
| 19 | agents/docs-enhancer.md | "Balance AI optimization with human readability" — "balance" is vague | -2 |
| 20 | agents/hooks-enhancer.md | "Be cautious about security patterns" — "cautious" gives no measurable direction | -2 |
| 21 | agents/skills-enhancer.md | "Consider skill context when evaluating trigger quality" — "consider" is vague | -2 |
| 22 | CLAUDE.md | Critical Rules section (8 rules) has no WHY explanations — reduces compliance | -10 |

## Cross-Component
**Version drift**: `.claude-plugin/plugin.json` declares `version: "5.1.0"` while `package.json` declares `version: "1.0.0"`. All 9 SKILL.md files use `version: 5.1.0` in their frontmatter, aligning with the plugin manifest but not the npm package. The plugin's own `enhance-plugins` skill documents this as a HIGH-certainty bug and offers an auto-fix (sync both to the same value).

**Agent write-capability gap**: All 8 enhancer agents advertise `--fix` apply behaviour in their body but none declare `Write` or `Edit` in their `tools:` list. Only `Skill`, `Read`, `Glob`, `Grep`, and `Bash(git:*)` or `Bash(node:*)` are declared. Whether skills can bypass agent-level tool restrictions at runtime is not documented. If they cannot, auto-fix functionality is silently broken for all agents.

**Bash(git:*) may be unused in 6 agents**: `agent-enhancer`, `claudemd-enhancer`, `docs-enhancer`, `hooks-enhancer`, `plugin-enhancer`, and `skills-enhancer` declare `Bash(git:*)` but their bodies contain no git operations. Only `cross-file-enhancer` and `prompt-enhancer` demonstrate actual use of `Bash(node:*)`. Unused tools inflate the declared surface unnecessarily (-3 each under R-unused-tools, not applied above pending verification).

**CLAUDE.md description narrow vs command scope**: CLAUDE.md's plugin description matches `plugin.json` ("Plugin structure and tool use analyzer") but `commands/enhance.md` covers 8 enhancer types including docs, hooks, and CLAUDE.md analysis. The top-level description underrepresents the plugin's breadth; this is informational only.

## Recommendation
CLEAR — submit PRs for the two bugs (missing `allowed-tools` in command frontmatter, version sync between plugin.json and package.json). File the Medium security finding as an issue with suggestion to document `AGENT_ANALYZER_REQUIRE_ATTESTATION=1` more prominently. Agent quality (missing examples and output format) is a systematic pattern across all 8 agents and should be addressed in a single batch PR.
