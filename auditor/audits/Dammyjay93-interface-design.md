# NLPM Audit: Dammyjay93/interface-design
**Date**: 2026-04-27  |  **Artifacts**: 7  |  **Strategy**: single
**NL Score**: 94/100
**Security**: CLEAR
**Bugs**: 3  |  **Quality Issues**: 7  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/commands/critique.md | command | 85 | No empty input handling (-10) + missing allowed-tools (-5) |
| .claude-plugin/plugin.json | manifest | 95 | CalVer version format (informational) |
| .claude/commands/audit.md | command | 95 | Missing allowed-tools (-5) |
| .claude/commands/extract.md | command | 95 | Missing allowed-tools (-5) |
| .claude/commands/init.md | command | 95 | Missing allowed-tools (-5) |
| .claude/commands/status.md | command | 95 | Missing allowed-tools (-5) |
| .claude/skills/interface-design/SKILL.md | skill | 98 | Vague quantifier: "some" (-2) |

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
| Hooks | 0 |
| Scripts | 0 |
| MCP configs | 0 |
| Package manifests | 0 |

No execution surfaces found. The plugin is pure markdown with no shell scripts, hooks, MCP configs, or package manifests.

### Security Findings
No security findings.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .claude/skills/interface-design/SKILL.md | References `references/principles.md` (Deep Dives section, line 381) — file does not exist in the plugin | Users following the deep-dive link get a missing-file error; code examples and dark mode detail are unreachable |
| 2 | .claude/skills/interface-design/SKILL.md | References `references/validation.md` (Deep Dives section, line 382) — file does not exist | Memory management and system.md update guidance is inaccessible |
| 3 | .claude/skills/interface-design/SKILL.md | References `references/critique.md` (Deep Dives section, line 383) — file does not exist | Post-build critique protocol detail is inaccessible |

## Security Fixes (PR-worthy, Medium/Low only)
No security fixes required.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/commands/audit.md | No `allowed-tools` in frontmatter; command reads files and compares against system.md but declares no tool access | -5 |
| 2 | .claude/commands/critique.md | No `allowed-tools` in frontmatter; command reads and rewrites UI files but declares no tool access | -5 |
| 3 | .claude/commands/critique.md | No empty input handling; assumes a file was just built — does not state what to do if invoked with no recent build context | -10 |
| 4 | .claude/commands/extract.md | No `allowed-tools` in frontmatter; Implementation explicitly calls for `Glob` but no tools are declared | -5 |
| 5 | .claude/commands/init.md | No `allowed-tools` in frontmatter; reads skills file and may write system.md but declares no tool access | -5 |
| 6 | .claude/commands/status.md | No `allowed-tools` in frontmatter; reads system.md file but declares no tool access | -5 |
| 7 | .claude/skills/interface-design/SKILL.md | Vague quantifier: "some decisions are creative and others are structural" — "some" is imprecise | -2 |

## Cross-Component
**Broken deep-dive references (3):** SKILL.md lines 381–383 point to `references/principles.md`, `references/validation.md`, and `references/critique.md`. None of these files are present in the plugin. The `references/` subdirectory does not exist. These are the only three broken paths; all other internal references check out.

**Undefined external plugin reference:** SKILL.md Scope section (line 14) redirects non-interface-design requests to `/frontend-design`. No `frontend-design` command or plugin is defined in this repo, and the NLPM plugin registry shows no companion plugin. This may be intentional if the user is expected to install a separate plugin, but it is undocumented.

**Orphaned command:** `interface-design:init` (`.claude/commands/init.md`) is the primary entry point for this plugin but is absent from the Commands listing at the bottom of SKILL.md (lines 388–391). The listing documents `status`, `audit`, `extract`, and `critique` but omits `init`, which is the command that loads the skill. A reader consulting SKILL.md's Commands section would not discover `init`.

**Consistency check — init.md → SKILL.md path:** `init.md` loads `../skills/interface-design/SKILL.md` (relative to `.claude/commands/`), resolving to `.claude/skills/interface-design/SKILL.md`. Correct. ✓

**plugin.json command/skill declarations** point to `./.claude/commands` and `./.claude/skills` respectively, matching actual file locations. ✓

**Command names** are all correctly namespaced as `interface-design:<name>`. ✓

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

The three broken `references/` links (bugs 1–3) are the highest-value fixes: create the missing `references/principles.md`, `references/validation.md`, and `references/critique.md` files, or replace the dead links in SKILL.md with inline content. The missing `allowed-tools` declarations across all five commands are low-effort quality improvements. Overall this is a high-quality, well-structured plugin with an unusually thoughtful skill document; the NL score of 94/100 reflects that.
