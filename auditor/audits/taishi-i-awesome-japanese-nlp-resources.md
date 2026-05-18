# NLPM Audit: taishi-i/awesome-japanese-nlp-resources
**Date**: 2026-04-06  |  **Artifacts**: 5  |  **Strategy**: single
**NL Score**: 98/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 6  |  **Security Findings**: 5

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/search/SKILL.md | skill | 96 | R01 vague: "generally", "significantly" (−4) |
| skills/research-trends/SKILL.md | skill | 96 | R01 vague: "high-value", "relevant" (−4) |
| skills/find-new-resources/SKILL.md | skill | 98 | R01 vague: "manageable" (−2) |
| skills/research-issues/SKILL.md | skill | 98 | R01 vague: "high-value" (−2) |
| .claude-plugin/plugin.json | manifest | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 4 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts | 0 |
| MCP configs | 0 |
| Package manifests | 0 |
| Inline Bash/Python blocks (in skill bodies) | 4 skills |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | skills/find-new-resources/SKILL.md | 124 | file-write-outside-repo | Python block writes URL cache to `/tmp/awesome_ja_nlp_existing_urls.txt` — outside the repo tree. Content is benign (URL strings only) but /tmp is world-readable and persists across invocations. |
| 2 | Low | skills/find-new-resources/SKILL.md | 58 | env-var-access | Bash `find` command reads `${HOME}` to locate plugin data directory. |
| 3 | Low | skills/research-issues/SKILL.md | 42 | env-var-access | Bash `find` command reads `${HOME}` to locate plugin data directory. |
| 4 | Low | skills/research-trends/SKILL.md | 42 | env-var-access | Bash `find` command reads `${HOME}` to locate plugin data directory. |
| 5 | Low | skills/search/SKILL.md | 67 | env-var-access | Bash `find` command reads `${HOME}` to locate plugin data directory. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No bugs found | — |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/find-new-resources/SKILL.md | /tmp file is world-readable; name collision possible between concurrent users | Use `mktemp` or a unique filename like `/tmp/awesome_ja_nlp_existing_urls_$$.txt` and clean up after the step |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/find-new-resources/SKILL.md | Line 157: "To keep latency manageable" — "manageable" is vague without a criterion (R01) | −2 |
| 2 | skills/research-issues/SKILL.md | Line 144: "a specific high-value URL surfaces" — "high-value" is undefined (R01) | −2 |
| 3 | skills/research-trends/SKILL.md | Line 142: "a specific high-value URL surfaces" — "high-value" is undefined (R01) | −2 |
| 4 | skills/research-trends/SKILL.md | Line 154: "confirm the survey's top items remain relevant" — "relevant" is in the R01 vague-word list | −2 |
| 5 | skills/search/SKILL.md | Line 197: "generally signal battle-tested, well-documented tools" — "generally" is vague without qualifier (R01) | −2 |
| 6 | skills/search/SKILL.md | Line 204: "when `sc` is significantly higher among otherwise-similar items" — "significantly" lacks a threshold (R01) | −2 |

## Cross-Component
All four skills cross-reference each other correctly via invocation syntax (`/awesome-japanese-nlp-resources:find-new-resources`, `/awesome-japanese-nlp-resources:search`). The plugin.json manifest does not enumerate skills explicitly, which is consistent with Claude Code's convention of deriving skill names from directory paths. No orphaned components or broken references detected.

The `find-new-resources` skill references the `search` skill at the end of its empty-result output block — the referenced skill exists and the invocation path is valid.

## Recommendation
CLEAR — no bugs to submit PRs for. The medium security finding (predictable /tmp filename) is low-risk but fixable in a single-line change. Quality issues are minor vague-word cleanups; the plugin is otherwise exceptionally well-structured with thorough empty-input handling, bilingual output templates, numbered steps, and explicit output formats in all four skills.
