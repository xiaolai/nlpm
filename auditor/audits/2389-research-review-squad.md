# NLPM Audit: 2389-research/review-squad
**Date**: 2026-04-06  |  **Artifacts**: 6  |  **Strategy**: single
**NL Score**: 96/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 4  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| CLAUDE.md | Overview doc | 80 | No frontmatter; no invocation examples |
| skills/experts/SKILL.md | Skill | 98 | Vague quantifier "relevant" (L95) |
| skills/normies/SKILL.md | Skill | 99 | Clean |
| skills/regulars/SKILL.md | Skill | 99 | Clean |
| skills/well-actually/SKILL.md | Skill | 99 | Clean |
| .claude-plugin/plugin.json | Manifest | 100 | N/A |

Weighted average: (80 + 98 + 99 + 99 + 99 + 100) / 6 = **96/100**

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
No bugs found. All skill files have valid frontmatter, no broken references, no undeclared tools.

## Security Fixes (PR-worthy, Medium/Low only)
No security fixes needed.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | CLAUDE.md | Missing YAML frontmatter — `name` and `description` fields absent, making the file non-machine-readable by NLPM scanners | -10 |
| 2 | CLAUDE.md | No worked invocation examples — the overview describes each skill in prose but shows no concrete user-prompt → Claude-behavior mapping | -5 |
| 3 | CLAUDE.md | Skill descriptions are brief summaries rather than behavioral specifications; standalone CLAUDE.md is under-informative without the skill files | -5 |
| 4 | skills/experts/SKILL.md | Vague quantifier "relevant" at L95: "always suggest what's relevant" — no criteria defined for relevance | -2 |

## Cross-Component
All internal references are consistent:

- **Dispatch modes** match across CLAUDE.md and skill files: experts is parallel, normies/regulars/well-actually are sequential. The CLAUDE.md note "Sequential for browser-using agents; code-only agents can run in parallel" correctly reflects `well-actually/SKILL.md` L97.
- **Browser MCP scope**: CLAUDE.md states three of four skills use browser MCP (normies, regulars, well-actually). Confirmed: experts reads code independently; the other three all include browser MCP guidance.
- **No-code guards**: CLAUDE.md documents "No-Code Guards" for normies and regulars. Both skill files include the guard verbatim in their agent prompt templates.
- **plugin.json commands: []**: Correct — this plugin exposes four skills, no slash commands. The empty array is intentional.
- **Relationship block** in CLAUDE.md references `fresh-eyes-review` and `scenario-testing` as complementary plugins. These are external references; no broken paths in-repo.
- No orphaned components, no terminology drift, no stale counts.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

No bugs were found, so no PR-worthy NL fixes. The quality issues above are informational improvements that would raise the score from 96 toward 99:

1. Add YAML frontmatter to CLAUDE.md (highest ROI — enables NLPM scanners)
2. Add a worked invocation example block to CLAUDE.md
3. Replace "suggest what's relevant" in `experts/SKILL.md` L95 with explicit selection criteria
