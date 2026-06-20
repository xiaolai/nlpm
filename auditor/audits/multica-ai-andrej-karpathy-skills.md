# NLPM Audit: multica-ai/andrej-karpathy-skills
**Date**: 2026-04-06  |  **Artifacts**: 3  |  **Strategy**: single
**NL Score**: 98/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 1  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| CLAUDE.md | project-instructions | 95/100 | Content duplicates skill body without @import (drift risk) |
| .claude-plugin/plugin.json | plugin-manifest | 100/100 | None |
| skills/karpathy-guidelines/SKILL.md | skill | 100/100 | None |

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
No security fixes needed.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | CLAUDE.md | Content is a near-duplicate of `skills/karpathy-guidelines/SKILL.md` without `@import`. If the skill is updated, CLAUDE.md will drift silently. Consider replacing the body with `@skills/karpathy-guidelines`. | −5 |

## Cross-Component
- `plugin.json` `skills` array references `./skills/karpathy-guidelines` — directory exists and contains `SKILL.md`. Reference is valid.
- CLAUDE.md and SKILL.md carry identical behavioral guidelines. No semantic contradiction, but no import link either. Informational only.
- No commands or agents declared; no broken references to check.
- No orphaned components.

## Recommendation
CLEAR — submit PRs for any bugs (none found this audit). The single quality issue (CLAUDE.md content duplication) is informational; a follow-up PR replacing the duplicated body with `@skills/karpathy-guidelines` would eliminate future drift risk.
