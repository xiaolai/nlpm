# NLPM Audit: blader/humanizer
**Date**: 2026-04-06  |  **Artifacts**: 1  |  **Strategy**: single
**NL Score**: 98/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 1  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| SKILL.md | skill | 98 | Vague quantifier "some" in instructional prose (line 79) |

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
| 1 | SKILL.md | Vague quantifier "some" in instructional prose at line 79: "Let some mess in." The following sentences clarify the intent (tangents, asides, half-formed thoughts), which limits the ambiguity, but "some" is mechanically flagged. | -2 |

## Cross-Component

Single-artifact repository. No cross-component references to verify. The `Reference` section at the end of SKILL.md links to `https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing` — an external URL, not a repo-internal reference, so no broken-reference risk.

The `allowed-tools` list includes `AskUserQuestion`, which is not explicitly invoked by name in the instructional prose. The Voice Calibration section is passive ("If the user provides a writing sample") rather than directive ("Use AskUserQuestion to request one"). In practice the tool could still be used legitimately for open-ended clarification, so this does not rise to a bug, but it is worth noting as a minor consistency gap.

## Recommendation

CLEAR — no bugs, no security findings, and a single low-weight quality issue (one vague quantifier, -2). No PRs are needed; the repository is in excellent shape. If the maintainer wants to push the score to 100, replacing "Let some mess in" with a more concrete directive (e.g., "Include tangents, asides, or self-corrections where they fit") would close the remaining gap.
