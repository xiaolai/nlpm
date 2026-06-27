# NLPM Audit: mlunato47/claude-grc-plugin
**Date**: 2026-04-06  |  **Artifacts**: 27  |  **Strategy**: batched
**NL Score**: 68/100
**Security**: CLEAR
**Bugs**: 2  |  **Quality Issues**: 30  |  **Security Findings**: 2

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| grc/agents/grc-researcher.md | agent | 35 | No YAML frontmatter at all (name −25, description −25); no model; no output format |
| grc/commands/poam-help.md | command | 60 | Missing name −25; no allowed-tools −5; output format is "Varies by action" with no template −10 |
| grc/.claude-plugin/plugin.json | plugin manifest | 65 | No commands, agents, or skills arrays; plugin artifacts are not registered |
| grc/commands/tabletop-scenario.md | command | 66 | Missing name −25; no allowed-tools −5; "appropriate" used twice −4 |
| grc/commands/review-poam.md | command | 68 | Missing name −25; no allowed-tools −5; "appropriate" −2 |
| grc/commands/score-maturity.md | command | 68 | Missing name −25; no allowed-tools −5; "appropriate" −2 |
| grc/commands/review-crm.md | command | 68 | Missing name −25; no allowed-tools −5; "appropriate" −2 |
| grc/commands/multi-framework.md | command | 68 | Missing name −25; no allowed-tools −5; "appropriate" −2 |
| grc/commands/sar-response.md | command | 68 | Missing name −25; no allowed-tools −5; "appropriate" −2 |
| grc/commands/review-ssp.md | command | 68 | Missing name −25; no allowed-tools −5; "appropriate" −2 |
| grc/commands/significant-change.md | command | 68 | Missing name −25; no allowed-tools −5; "appropriate" −2 |
| grc/commands/review-narrative.md | command | 68 | Missing name −25; no allowed-tools −5; "appropriate" −2 |
| grc/commands/boundary-guidance.md | command | 68 | Missing name −25; no allowed-tools −5; "appropriate" −2 |
| grc/commands/review-policy.md | command | 68 | Missing name −25; no allowed-tools −5; "appropriate" −2 |
| grc/commands/inheritance.md | command | 68 | Missing name −25; no allowed-tools −5; "appropriate" −2 |
| grc/commands/oscal-guide.md | command | 68 | Missing name −25; no allowed-tools −5; "appropriate" −2 |
| grc/commands/audit-prep.md | command | 70 | Missing name −25; no allowed-tools −5 |
| grc/commands/control-lookup.md | command | 70 | Missing name −25; no allowed-tools −5 |
| grc/commands/ssp-section.md | command | 70 | Missing name −25; no allowed-tools −5 |
| grc/commands/deviation-request.md | command | 70 | Missing name −25; no allowed-tools −5 |
| grc/commands/conmon-guide.md | command | 70 | Missing name −25; no allowed-tools −5 |
| grc/commands/evidence-checklist.md | command | 70 | Missing name −25; no allowed-tools −5 |
| grc/commands/compliance-calendar.md | command | 70 | Missing name −25; no allowed-tools −5 |
| grc/commands/gap-analysis.md | command | 70 | Missing name −25; no allowed-tools −5 |
| grc/commands/rev5-transition.md | command | 70 | Missing name −25; no allowed-tools −5 |
| grc/commands/map-controls.md | command | 70 | Missing name −25; no allowed-tools −5 |
| grc/skills/grc-knowledge/SKILL.md | skill | 98 | "appropriate" vague quantifier −2 |

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
| Hooks | 0 (none found) |
| Scripts (JS) | 1 — `.opencode/plugins/grc.js` |
| MCP configs | 0 (no `.mcp.json`) |
| Package manifests | 0 (no `package.json`, `requirements.txt`) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | .opencode/plugins/grc.js | 16 | SEC-system-prompt-injection | `readFileSync(skillPath)` reads SKILL.md verbatim and injects full content into the AI system prompt via `experimental.chat.system.transform`. If SKILL.md is tampered with (e.g., by a malicious PR merged without review), arbitrary system prompt instructions are injected into every conversation. No sanitization or size cap is applied. |
| 2 | Low | .opencode/plugins/grc.js | 49 | SEC-unstable-api | Uses `experimental.chat.system.transform` — an unstable OpenCode API. No fallback if the key is removed or renamed in a future release; the plugin silently loses all GRC context. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | grc/agents/grc-researcher.md | No YAML frontmatter block at all — `name` and `description` are absent | Agent cannot be registered, discovered, or referenced by name in any orchestrating command or skill declaration |
| 2 | grc/.claude-plugin/plugin.json | No `commands`, `agents`, or `skills` arrays declared | Claude Code plugin installation registers no artifacts; all 24 commands, the agent, and the skill are effectively invisible to the plugin system unless Claude Code auto-discovers from directory structure |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | .opencode/plugins/grc.js | SKILL.md content injected into system prompt without size cap or sanitization; tampering with SKILL.md would propagate to all sessions | Add a max-length guard (e.g., truncate `skillContent` at 20 000 chars) and strip any `<IMPORTANT>` or `</IMPORTANT>` tags from the content before injection |
| 2 | .opencode/plugins/grc.js | Depends on `experimental.chat.system.transform` with no fallback | Add a try/catch around the transform registration and log a clear warning if the key is not available, so failures are visible rather than silent |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | All 24 commands | Missing `name:` field in YAML frontmatter; every command has `description:` but not `name:` | −25 per file |
| 2 | All 24 commands | No `allowed-tools:` declaration; commands reference Read, Glob, and (for OSCAL lookups) large JSON files but declare no tool contract | −5 per file |
| 3 | grc/agents/grc-researcher.md | No `model:` declaration; agent tier and capability profile are unspecified | −5 |
| 4 | grc/agents/grc-researcher.md | No `## Output Format` section; six example input queries are listed but no response structure is defined | −10 |
| 5 | grc/commands/poam-help.md | Output Format section says "Varies by action" with only a bullet list of included categories — no concrete template for any of the 6 actions | −10 |
| 6 | 13 commands + SKILL.md | Vague quantifier "appropriate" in "Read the appropriate reference files"; each occurrence of "appropriate" without further qualification is penalizable | −2 per occurrence |
| 7 | grc/commands/tabletop-scenario.md | Two distinct "appropriate" occurrences: "Read the appropriate reference files" (line 39) and "A realistic scenario appropriate to the type and system context" (line 45) | −4 total |

## Cross-Component
- **plugin.json ↔ commands/agents/skills**: The plugin manifest at `grc/.claude-plugin/plugin.json` declares `name`, `description`, `version`, `author`, `repository`, `license`, and `keywords` but no `commands`, `agents`, or `skills` arrays. None of the 24 commands, the `grc-researcher` agent, or the `grc-knowledge` skill are registered. If Claude Code requires explicit registration (rather than purely directory-based discovery), installation of this plugin via `claude plugin install` would succeed but expose no slash commands.
- **Agent path references**: `grc/agents/grc-researcher.md` lists reference files as `skills/grc-knowledge/frameworks/nist-800-53.md` etc. — paths relative to the plugin root. The `.opencode/plugins/grc.js` adapter resolves these correctly via `referenceBasePath` using absolute paths injected into the system prompt. For native Claude Code invocation (without the OpenCode adapter), path resolution depends on whether Claude Code sets the working directory to the plugin root or the user project root; if the latter, all reference file reads would fail silently.
- **SKILL.md ↔ reference file list**: The Reference Navigation table in `SKILL.md` references 40+ subordinate files (`frameworks/*.md`, `mappings/*.md`, `conmon/*.md`, `audits/*.md`, `oscal/*.json`). Directory listing confirms the OSCAL JSON files and tooling directory are present. The framework/mapping/audit markdown files are referenced but not directly verified here; their presence is assumed from the plugin's complete structure.
- **No orphaned components detected**: Every command maps to behaviors that reference well-defined skill files; no command references a skill, agent, or file that appears to be absent.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

Priority order:
1. **Bug fix (high impact)**: Add YAML frontmatter (`name:`, `description:`, `model:`) to `grc/agents/grc-researcher.md`.
2. **Bug fix (high impact)**: Add `commands`, `agents`, and `skills` arrays to `grc/.claude-plugin/plugin.json`.
3. **Security fix (medium)**: Add size cap and tag stripping to `grc.js` before system prompt injection.
4. **Quality sweep**: Add `name:` field to all 24 command frontmatter blocks (filename already serves as the command identifier, so this is low-risk to add).
5. **Quality sweep**: Add `allowed-tools:` declarations to all 24 commands.
6. **Quality**: Add concrete per-action output templates to `grc/commands/poam-help.md`.
