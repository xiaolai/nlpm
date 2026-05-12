# NLPM Audit: forrestchang/andrej-karpathy-skills
**Date**: 2026-04-06  |  **Artifacts**: 3  |  **Strategy**: single
**NL Score**: 99/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 1  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| CLAUDE.md | project-instructions | 98/100 | R01 vague quantifier "as needed" (line 3) |
| .claude-plugin/plugin.json | plugin-manifest | 100/100 | — |
| skills/karpathy-guidelines/SKILL.md | skill | 100/100 | — |

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
| Hooks | 0 (only `.git/hooks/*.sample` inert templates) |
| Scripts | 0 |
| MCP configs | 0 |
| Package manifests | 0 |

### Security Findings
No security findings.

## Bugs (PR-worthy)
No bugs found.

## Security Fixes (PR-worthy, Medium/Low only)
No security fixes needed.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | CLAUDE.md:3 | R01 vague quantifier: "as needed" — "Merge with project-specific instructions as needed" lacks criteria for when merging is warranted | -2 |

## Cross-Component
- `plugin.json` `skills` array references `"./skills/karpathy-guidelines"` → resolves correctly to `skills/karpathy-guidelines/SKILL.md` ✓
- Plugin package name (`andrej-karpathy-skills`) differs from skill identifier (`karpathy-guidelines`); this is normal practice — no conflict.
- `CLAUDE.md` and `SKILL.md` carry near-identical content by design: `CLAUDE.md` delivers project-level instructions when the plugin is installed; `SKILL.md` makes the same content loadable by agents. Intentional and consistent.
- No broken references, orphaned components, or contradictions detected.

## Recommendation
CLEAR — submit a PR for the single quality fix: replace "as needed" on CLAUDE.md line 3 with specific criteria (e.g., "when this conflicts with project-specific guidelines, project rules take precedence"). No security or structural issues.
