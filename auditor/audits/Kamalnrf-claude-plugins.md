# NLPM Audit: Kamalnrf/claude-plugins
**Date**: 2026-06-20  |  **Artifacts**: 3  |  **Strategy**: single
**NL Score**: 98/100
**Security**: CLEAR
**Bugs**: 1  |  **Quality Issues**: 4  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/skills-discovery/SKILL.md | skill | 94 | Vague quantifiers: "relevant", "good", "best practices" (−6) |
| CLAUDE.md | project-memory | 100 | None |
| packages/cli/CLAUDE.md | project-memory | 100 | Duplicate of root CLAUDE.md |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | None |
| Scripts | None |
| MCP configs | None |
| Package manifests | package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | skills/skills-discovery/SKILL.md | 99 | SEC-unpinned-semver | `npx skills-installer install` runs the latest unpinned version of skills-installer from npm; a compromised release executes arbitrary code in the user's environment |
| 2 | Medium | skills/skills-discovery/SKILL.md | 32 | SEC-external-network-call | Skill instructs Claude to issue curl GET requests to an external registry (claude-plugins.dev); outbound network call from agent context |
| 3 | Low | package.json | 16 | SEC-unpinned-semver | `"@types/bun": "latest"` — floating `latest` tag means the devDependency can change on every fresh install |
| 4 | Low | package.json | 19 | SEC-unpinned-semver | `"typescript": "^5"` — broad semver range in peerDependencies allows any future 5.x version without explicit review |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | skills/skills-discovery/SKILL.md | Inconsistent API endpoint: discovery workflow body (line 32) uses `/api/skills?q=QUERY` but the API Reference table (line 178) documents the search endpoint as `/api/skills/search?q=QUERY`; one path will return 404 | Users following the body example may hit a different endpoint than documented in the reference table, causing silent failures |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/skills-discovery/SKILL.md | `npx skills-installer` unversioned | Change to `npx skills-installer@<pinned-version>` or document required version; add a note to verify the package on npmjs.com before running |
| 2 | package.json | `"@types/bun": "latest"` | Pin to a specific version (e.g., `"@types/bun": "1.2.x"`) to prevent unexpected devDependency churn |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/skills-discovery/SKILL.md | Vague quantifier "relevant" at line 136: "Show 3-5 most relevant results" — no criterion defined for what makes a result relevant | −2 |
| 2 | skills/skills-discovery/SKILL.md | Vague quantifier "good" at line 141: "Offer to help directly if no good skill exists" — "good" is undefined | −2 |
| 3 | skills/skills-discovery/SKILL.md | Vague quantifier "best practices" at line 21: "where best practices matter (testing, deployment, APIs, documentation)" — the parenthetical helps but the phrase itself is still underspecified | −2 |
| 4 | packages/cli/CLAUDE.md | Content is byte-for-byte identical to root CLAUDE.md; no package-cli-specific overrides. This causes silent drift risk if either file is updated independently | informational |

## Cross-Component
- **Duplicate CLAUDE.md**: `CLAUDE.md` (root) and `packages/cli/CLAUDE.md` are identical in full content. If the cli package has different Bun API constraints or testing requirements from other packages, this duplication will cause one file to go stale. Recommend either deleting the cli-level file and relying on root inheritance, or diverging it with cli-specific additions.
- **Inconsistent API endpoint** (also filed as Bug #1): The discovery workflow code block and the API Reference table within the same SKILL.md document two different paths for the skills search endpoint. A reader following the body example (`/api/skills?q=`) will behave differently than a reader consulting the reference table (`/api/skills/search?q=`). No cross-file reference issue — this is self-contradictory within a single file.
- No orphaned components, broken inter-file references, or missing skill cross-links detected.

## Recommendation
CLEAR — submit PRs for Bug #1 (inconsistent API path) and Security Fixes #1–2 (npx version pinning, @types/bun pinning). The quality issues are informational only. No private disclosure needed.
