# NLPM Audit: kepano/obsidian-skills
**Date**: 2026-04-26  |  **Artifacts**: 6  |  **Strategy**: single
**NL Score**: 100/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 1  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `.claude-plugin/plugin.json` | Plugin manifest | 100 | None |
| `skills/defuddle/SKILL.md` | Skill | 100 | Minimal content (informational) |
| `skills/json-canvas/SKILL.md` | Skill | 100 | None |
| `skills/obsidian-bases/SKILL.md` | Skill | 100 | None |
| `skills/obsidian-cli/SKILL.md` | Skill | 100 | None |
| `skills/obsidian-markdown/SKILL.md` | Skill | 100 | None |

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

### Security Findings
No security findings.

## Bugs (PR-worthy)
No bugs found.

## Security Fixes (PR-worthy, Medium/Low only)
No security fixes required.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `skills/defuddle/SKILL.md` | Minimal skill — no troubleshooting or error-handling section for a CLI dependency. Silent install failure (e.g., npm not present) is unaddressed. | 0 (informational) |

## Cross-Component
All inter-file references resolved:
- `skills/json-canvas/SKILL.md` → `references/EXAMPLES.md` ✓
- `skills/obsidian-bases/SKILL.md` → `references/FUNCTIONS_REFERENCE.md` ✓
- `skills/obsidian-markdown/SKILL.md` → `references/EMBEDS.md`, `references/CALLOUTS.md`, `references/PROPERTIES.md` ✓

`plugin.json` is well-formed: valid semver (`1.0.1`), `name`, `description`, `author`, `repository`, `license`, `keywords` all present. No skill paths are declared in the manifest (plugins load skills by convention, not by explicit listing), so no orphan-component risk exists.

No terminology drift, orphaned components, or contradictions found.

## Recommendation
CLEAR — no bugs, no security findings. The plugin is exemplary: all five skill files carry complete frontmatter, include concrete worked examples, avoid vague quantifiers, and cross-reference only files that exist. The sole informational note on `skills/defuddle/SKILL.md` (absent troubleshooting for a missing `npm`/`defuddle` dependency) is not PR-worthy on its own but would round out the skill if the author wishes to address it.
