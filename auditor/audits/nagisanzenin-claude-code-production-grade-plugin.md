# NLPM Audit: nagisanzenin/claude-code-production-grade-plugin
**Date**: 2026-04-06  |  **Artifacts**: 16  |  **Strategy**: single
**NL Score**: 93/100
**Security**: REVIEW
**Bugs**: 2  |  **Quality Issues**: 10  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/production-grade/SKILL.md | skill / orchestrator | 80 | Vague quantifiers "sensible defaults" 7+ times, capped at -20; references non-standard tools TeamCreate/TeamDelete |
| hooks/hooks.json | hook config | 90 | Fallback path hardcoded without version pin |
| .claude-plugin/plugin.json | plugin manifest | 90 | No `skills` array listing bundled skill paths |
| skills/code-reviewer/SKILL.md | skill | 92 | "appropriate" used without definition 3× (-6) |
| skills/frontend-engineer/SKILL.md | skill | 93 | "sensible defaults" + "appropriate" + "reasonable" (-6) |
| skills/polymath/SKILL.md | skill | 93 | "relevant", "appropriate", "good" vague 3× (-6); smart_outline reference |
| skills/software-engineer/SKILL.md | skill | 93 | "appropriate", "sensible defaults", "relevant" 3× (-6) |
| skills/solution-architect/SKILL.md | skill | 93 | "appropriate", "relevant", "sensible" 3× (-6) |
| skills/product-manager/SKILL.md | skill | 94 | "appropriate", "relevant", "good" 3× (-4 to -6) |
| skills/qa-engineer/SKILL.md | skill | 94 | "sensible coverage targets" + "appropriate" (-4) |
| skills/skill-maker/SKILL.md | skill | 94 | Hardcoded "nagisanzenin" author in generated templates |
| skills/devops/SKILL.md | skill | 95 | "sensible defaults" + "appropriate" 2× (-4) |
| skills/security-engineer/SKILL.md | skill | 95 | "appropriate" + "relevant" 2× (-4) |
| skills/data-scientist/SKILL.md | skill | 96 | "sensible defaults" + "relevant" 2× (-4); best-documented skill |
| skills/sre/SKILL.md | skill | 96 | "sensible defaults" + "appropriate" 2× (-4) |
| skills/technical-writer/SKILL.md | skill | 98 | "appropriate" 1× (-2); cleanest file |

**Weighted average**: 1486 / 16 = **93/100**

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 2 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | hooks/hooks.json, hooks/session-guard.sh |
| Scripts | (none — no scripts/ directory) |
| MCP configs | (none — no .mcp.json) |
| Package manifests | (none — no package.json / requirements.txt) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH | skills/production-grade/SKILL.md | ~336–342 | file-write-outside-repo | Auto-update flow instructs Claude to `git clone` from GitHub to /tmp, then `cp -r` into `~/.claude/plugins/cache/` and overwrite `~/.claude/plugins/installed_plugins.json` — system-directory writes with no hash/signature verification of retrieved code |
| 2 | MEDIUM | skills/production-grade/SKILL.md | ~318 | network-call | Version check fetches `https://raw.githubusercontent.com/nagisanzenin/claude-code-production-grade-plugin/main/.claude-plugin/plugin.json` to compare versions; response is trusted without integrity check |
| 3 | MEDIUM | skills/production-grade/SKILL.md | ~336 | network-call | `git clone --depth 1 https://github.com/nagisanzenin/claude-code-production-grade-plugin.git /tmp/pg-update` — fetches arbitrary code from the network; cloned content is subsequently copied to the user's Claude plugin cache |
| 4 | LOW | hooks/hooks.json | 10 | unpinned-path | Fallback path `$HOME/.claude/plugins/cache/nagisanzenin/production-grade` has no version component; if auto-update installs to a versioned subdirectory and `CLAUDE_PLUGIN_ROOT` is unset, the hook may execute a stale or missing script |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | skills/production-grade/SKILL.md | References `TeamCreate(team_name=...)` and `TeamDelete(team_name=...)` — these are not standard Claude Code tools; the Full Build Pipeline will error at the team creation/cleanup steps | Pipeline breaks silently when orchestrator tries to create or delete the `"production-grade"` team |
| 2 | skills/production-grade/SKILL.md + fallback blocks across all SKILL.md files | References `smart_outline` and `smart_search` as tools to call for codebase exploration; neither is a built-in Claude Code tool, and no dependency is declared | Claude cannot call these tools; skill fallback guidance and polymath's tool-usage section point to non-existent tools |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | hooks/hooks.json | Fallback path has no version pin; may target wrong or missing session-guard.sh after auto-update | Append version to fallback: `$HOME/.claude/plugins/cache/nagisanzenin/production-grade/${PLUGIN_VERSION:-current}` or read version from installed_plugins.json |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/production-grade/SKILL.md | "sensible defaults" (7+ occurrences), "appropriate" (5+), "relevant" (4+), "reasonable" (2+) — vague quantifiers throughout | -20 (capped) |
| 2 | skills/code-reviewer/SKILL.md | "appropriate level" (line 225), "appropriate layer" (line 228) used without defining what "appropriate" means in each context | -6 |
| 3 | skills/frontend-engineer/SKILL.md | "sensible defaults", "appropriate", "reasonable" used without specifying what values qualify | -6 |
| 4 | skills/polymath/SKILL.md | "relevant artifacts", "appropriate depth", "good options" used as undefined criteria | -6 |
| 5 | skills/software-engineer/SKILL.md | "appropriate error level", "sensible defaults", "relevant phase file" used without definition | -6 |
| 6 | skills/solution-architect/SKILL.md | "appropriate" (3×), "sensible" used as vague criteria in fitness-function table | -6 |
| 7 | skills/product-manager/SKILL.md | "appropriate" (2×), "relevant" — minor vague usage | -4 |
| 8 | skills/qa-engineer/SKILL.md | "sensible coverage targets" in Express mode description | -4 |
| 9 | skills/skill-maker/SKILL.md | README template and marketplace config hardcode `nagisanzenin` as the author; adopting the plugin to a different author requires manually editing generated output | informational |
| 10 | Most SKILL.md files | Only data-scientist/SKILL.md includes `version`, `author`, and `tags` in frontmatter; the other 13 skill files omit these fields, creating inconsistency and hindering discoverability | informational |

## Cross-Component
**Phase file references**: Seven SKILL.md files (data-scientist, frontend-engineer, software-engineer, solution-architect, security-engineer, sre, technical-writer) dispatch to `phases/NN-name.md` sub-files within their skill directories. These phase files are referenced as mandatory ("Read the relevant phase file before starting that phase. Never read all phases at once") but were not included in the audit scope. If these phase files are absent from the installed plugin, the affected skills will fail at the dispatch step. Confidence: low — phase files likely exist in the repo but could not be verified in this audit pass.

**Plugin manifest**: `.claude-plugin/plugin.json` does not enumerate the bundled skills array. If the Claude Code plugin loader uses this field to determine what to register, a manifest-vs-disk drift could leave skills unregistered after updates. The skill-maker template also omits a `skills` array, suggesting this field may not be required by the plugin spec.

**Cross-skill protocol consistency**: All 14 skill SKILL.md files reference the same `Claude-Production-Grade-Suite/.protocols/` path for shared protocols (ux-protocol.md, input-validation.md, etc.). These protocol files are written at pipeline bootstrap by the production-grade orchestrator; skills that are invoked standalone (without the orchestrator running first) will fall through to the inline fallback text, which is present and coherent. Consistent design.

**Terminology**: The production-grade orchestrator's Task Dependency Graph refers to phases T1–T13 but only names 13 distinct skill tasks; the numbering is consistent with the Context Bridging table. No terminology drift detected.

## Recommendation
REVIEW — submit NL fix PRs for bugs and quality issues (TeamCreate/TeamDelete reference, smart_outline reference, vague quantifiers). The HIGH security finding (auto-update system write without hash verification) requires private disclosure to the maintainer rather than a public PR; only the LOW severity hooks fallback-path issue is suitable for a public security fix PR.
