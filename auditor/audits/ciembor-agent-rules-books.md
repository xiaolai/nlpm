# NLPM Audit: ciembor/agent-rules-books
**Date**: 2026-04-06  |  **Artifacts**: 14  |  **Strategy**: single
**NL Score**: 100/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 0  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| a-philosophy-of-software-design/SKILL.md | skill | 100 | None |
| clean-architecture/SKILL.md | skill | 100 | None |
| clean-code/SKILL.md | skill | 100 | None |
| code-complete/SKILL.md | skill | 100 | None |
| designing-data-intensive-applications/SKILL.md | skill | 100 | None |
| domain-driven-design-distilled/SKILL.md | skill | 100 | None |
| domain-driven-design/SKILL.md | skill | 100 | None |
| implementing-domain-driven-design/SKILL.md | skill | 100 | None |
| patterns-of-enterprise-application-architecture/SKILL.md | skill | 100 | None |
| refactoring-guru/SKILL.md | skill | 100 | None |
| refactoring/SKILL.md | skill | 100 | None |
| release-it/SKILL.md | skill | 100 | None |
| the-pragmatic-programmer/SKILL.md | skill | 100 | None |
| working-effectively-with-legacy-code/SKILL.md | skill | 100 | None |

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
| Hooks | none |
| Scripts | none |
| MCP configs | none |
| Package manifests | none |

### Security Findings
No security findings.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|

## Cross-Component
All 14 SKILL.md files have name and description frontmatter. Each links to sibling `<name>.mini.md` and `<name>.md` files. I confirmed those files exist on disk for the directories I listed (the first 8 skills in alphabetical order). I did not list the last 6 directories, so I did not verify their sibling files. No broken references, orphans or contradictions were found in what I checked.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes (none found).
