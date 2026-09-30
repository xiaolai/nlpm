# NLPM Audit: danny-avila/LibreChat
**Date**: 2026-04-06  |  **Artifacts**: 5  |  **Strategy**: single
**NL Score**: 97/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 2  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/skills/improve-codebase-architecture/SKILL.md | skill | 94 | Vague phrases ("a good stretch of the commit history", "explore organically") |
| .claude/skills/codebase-design/SKILL.md | skill | 98 | Minor vague wording; otherwise clean |
| e2e/fixtures/deployment-skills/e2e-deployment-skill/SKILL.md | skill (test fixture) | 100 | None |
| packages/api/src/agents/openai/README.md | documentation | 100 | None (not an NL artifact requiring frontmatter) |
| packages/api/src/agents/triggers/README.md | documentation | 100 | None (not an NL artifact requiring frontmatter) |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 3 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none |
| Scripts (top-level scripts/) | scripts/redis-mode.sh, scripts/static-checks.mts, scripts/sort-imports.mts, scripts/merge-locize-download.mjs, scripts/validate-locize-download.mjs, scripts/activity-labels/*.mts |
| MCP configs | none |
| Package manifests | package.json |

The pre-scan's Critical/High matches were reviewed: no curl-pipe-shell, eval, reverse shell, or credential exfiltration was found in scripts/ or package.json. The pre-scan's 733 script count includes files outside the top-level scripts/ directory, which were not individually read.

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Low | scripts/static-checks.mts | 321 | shell: true | Windows-only `npm.cmd` spawn with fixed command and no user input; not injectable |
| 2 | Low | scripts/redis-mode.sh | 13 | sudo | `sudo apt-get install` appears only inside an echoed help message, not executed |
| 3 | Low | package.json | 15 | prepare script | `prepare` runs husky init with errors swallowed; standard git-hook setup |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| - | - | No bugs found. Relative links (DEEPENING.md, DESIGN-IT-TWICE.md, HTML-REPORT.md) resolve. | - |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| - | - | Low findings are benign and need no fix | None |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/skills/improve-codebase-architecture/SKILL.md | Vague quantifier "a good stretch of the commit history" (line 23) and "organically" (line 27) | -4 |
| 2 | .claude/skills/improve-codebase-architecture/SKILL.md | No explicit output format for the sub-agent's exploration notes | -2 |

## Cross-Component
- codebase-design and improve-codebase-architecture cross-reference each other consistently.
- improve-codebase-architecture references the `/grilling` and `/domain-modeling` skills, which are not present in `.claude/skills/` (may be user-level skills). Unverifiable, so low confidence.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes. (No high-confidence bugs found, so nothing is PR-worthy.)
