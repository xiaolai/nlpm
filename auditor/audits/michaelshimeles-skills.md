# NLPM Audit: michaelshimeles/skills
**Date**: 2026-04-06  |  **Artifacts**: 7  |  **Strategy**: single
**NL Score**: 95/100
**Security**: REVIEW
**Bugs**: 1  |  **Quality Issues**: 2  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| greploop-apps/SKILL.md | skill | 92 | allowed-tools omits jq/sleep/grep used in bash blocks |
| before-and-after/SKILL.md | skill | 93 | "Never use `before-and-after`" contradicts every command in the file |
| greploop/SKILL.md | skill | 93 | allowed-tools omits jq/sleep/grep used in bash blocks |
| code-structure/SKILL.md | skill | 96 | No explicit output format |
| new-feature/SKILL.md | skill | 96 | No handling of missing git remote / gh |
| evidence-driven-testing/SKILL.md | skill | 97 | No allowed-tools declared (optional) |
| unslop/SKILL.md | skill | 97 | No output format |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none |
| Scripts | before-and-after/scripts/capture.sh, before-and-after/scripts/upload-and-copy.sh, before-and-after/scripts/adapters/0x0st.sh, before-and-after/scripts/adapters/gist.sh, before-and-after/scripts/adapters/blob.sh, evidence-driven-testing/scripts/evidence.py, tests/test_evidence.py |
| MCP configs | none |
| Package manifests | none |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | before-and-after/scripts/adapters/0x0st.sh | 28 | network upload (curl -F) | Default adapter uploads screenshots to public third-party host 0x0.st; may leak sensitive UI |
| 2 | Medium | before-and-after/scripts/adapters/gist.sh | 36 | public gist | `gh gist create --public` publishes images publicly |
| 3 | Medium | before-and-after/scripts/adapters/blob.sh | 39 | network upload to env-controlled URL | curl POSTs file to $BLOB_UPLOAD_URL with no scheme/host validation |
| 4 | Low | before-and-after/scripts/upload-and-copy.sh | 69 | path traversal | IMAGE_ADAPTER interpolated into an executed script path with no name validation |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | before-and-after/SKILL.md | Line 22 says "Never use `before-and-after` (wrong package)" while all commands use `before-and-after` | Contradictory instruction confuses the agent |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | before-and-after/scripts/adapters/gist.sh | Public gist by default | Use secret gist (omit `--public`) or make it opt-in |
| 2 | before-and-after/scripts/upload-and-copy.sh | Unvalidated IMAGE_ADAPTER | Restrict to `^[A-Za-z0-9_]+$` before building path |
| 3 | before-and-after/scripts/adapters/blob.sh | Unvalidated upload URL | Require https:// in BLOB_UPLOAD_URL |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | greploop/SKILL.md | Bash blocks use jq, sleep, grep, echo not covered by allowed-tools (line 13) | -3 |
| 2 | greploop-apps/SKILL.md | Same allowed-tools gap (line 14) | -3 |

## Cross-Component
- before-and-after/scripts/capture.sh is not referenced by SKILL.md and calls `agent-browser:open`-style commands that are not valid shell commands (orphaned, likely broken).
- greploop and greploop-apps are near-duplicates by design; drift risk (apps adds a huge-PR fallback).

## Recommendation
REVIEW — submit NL fix PRs, flag security findings in issue.
