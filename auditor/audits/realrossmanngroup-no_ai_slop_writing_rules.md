# NLPM Audit: realrossmanngroup/no_ai_slop_writing_rules
**Date**: 2026-04-06  |  **Artifacts**: 5  |  **Strategy**: single
**NL Score**: 98/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 4  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/skills/no-ai-slop/SKILL.md | Skill | 97 | Missing scope note cross-referencing companion skill `rossmann-voice` (R07) |
| .claude/skills/rossmann-voice/SKILL.md | Skill | 97 | Missing scope note cross-referencing companion skill `no-ai-slop` (R07) |
| skills/no-ai-slop/SKILL.md | Skill | 97 | Missing scope note cross-referencing companion skill `rossmann-voice` (R07) |
| skills/rossmann-voice/SKILL.md | Skill | 97 | Missing scope note cross-referencing companion skill `no-ai-slop` (R07) |
| CLAUDE.md | Memory/entrypoint | 100 | None |

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
| Hooks (`hooks/**`) | none found |
| Scripts (`scripts/**/*.{sh,py,js}`) | none found |
| MCP configs (`.mcp.json`) | none found |
| Package manifests (`package.json`, `requirements.txt`) | none found |
| Commands (`commands/*.md`) | none found |

The repository contains no executable surface at all: it is five markdown/YAML-frontmatter files (two skill pairs mirrored between `skills/` and `.claude/skills/`, plus `CLAUDE.md`), a `README.md`, an `AGENTS.md`, and a `.claude-plugin/marketplace.json` manifest. No hooks, scripts, MCP servers, dependencies, or slash commands exist to scan.

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| — | — | — | — | — | No security findings. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | — | No bugs found. Frontmatter is present and valid on both skills, `name:` matches each parent directory, all cross-file references resolve (CLAUDE.md → `.claude/skills/*`, README.md → `skills/*`, `marketplace.json` → `./skills/no-ai-slop`, `./skills/rossmann-voice`), and the `skills/` / `.claude/skills/` mirrors are byte-identical as AGENTS.md requires. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| — | — | — | None — no execution surface exists to fix. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/skills/no-ai-slop/SKILL.md | No scope note pointing to the companion skill `rossmann-voice`, even though `CLAUDE.md` and `README.md` present the two skills as a pair that is always loaded together (R07) | -3 |
| 2 | .claude/skills/rossmann-voice/SKILL.md | No scope note pointing to the companion skill `no-ai-slop` (R07) | -3 |
| 3 | skills/no-ai-slop/SKILL.md | No scope note pointing to the companion skill `rossmann-voice` (R07) | -3 |
| 4 | skills/rossmann-voice/SKILL.md | No scope note pointing to the companion skill `no-ai-slop` (R07) | -3 |

## Cross-Component
- **Mirror sync: clean.** `skills/no-ai-slop/SKILL.md` ↔ `.claude/skills/no-ai-slop/SKILL.md`, `skills/rossmann-voice/SKILL.md` ↔ `.claude/skills/rossmann-voice/SKILL.md`, and the two `references/ai-writing-detection.md` copies are byte-identical, satisfying the synchronization instruction in `AGENTS.md` ("Keep the skill content synchronized when changing either published skill.").
- **Manifest-vs-disk: clean.** `.claude-plugin/marketplace.json`'s `plugins[0].skills` array (`./skills/no-ai-slop`, `./skills/rossmann-voice`) matches the two skill directories on disk exactly; no `plugin.json` exists, which is valid since the Claude Code plugin manifest is fully optional and components auto-discover from conventional paths.
- **CLAUDE.md → SKILL.md rule numbering: consistent.** Every numbered rule cited in `.claude/skills/no-ai-slop/SKILL.md` ("Rule 1", "Rule 4", "Rule 5", "Rule 7", "Rule 11", "Rule 13", "Rule 15", "Rule 16", "Rule 19") matches the same-numbered rule's subject in `CLAUDE.md`'s canonical 24-rule list.
- **Minor structural note (informational, not scored):** `no-ai-slop/SKILL.md`'s "Root-cause differentiation" section sits in the same heading position as the numbered "Rule N" sections but carries no rule number and has no corresponding entry among `CLAUDE.md`'s 24 canonical rules. This reads as an intentional supplementary pattern rather than a numbering error, but a reader skimming for "which of the 24 rules have worked examples" could mistake it for one. Low confidence this is a real defect versus deliberate design.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes. There are no bugs and no security fixes to submit; the only findings are two informational scope-note additions (R07, -3 each, applied identically to both the published and `.claude/`-mirrored copies of each skill). Given the small size and low severity, these are optional style nits rather than PR-worthy defects.
