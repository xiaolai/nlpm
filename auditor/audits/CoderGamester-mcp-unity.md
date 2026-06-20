# NLPM Audit: CoderGamester/mcp-unity
**Date**: 2026-06-20  |  **Artifacts**: 1  |  **Strategy**: single
**NL Score**: 90/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 3  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| CLAUDE.md | project-context | 90/100 | Sparse "Adding a New Resource" section lacks code example; vague "long" used as unquantified duration descriptor (×2) |

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
| Package manifests | 1 (`package.json` — Unity package manifest, not npm) |

### Security Findings

No security findings.

## Bugs (PR-worthy)

No bugs found.

## Security Fixes (PR-worthy, Medium/Low only)

No security fixes needed.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | CLAUDE.md | Vague duration quantifier "long" in "Long main-thread work" bullet (line 115) — no threshold defined (e.g., ">16ms" or ">1 frame") | -2 |
| 2 | CLAUDE.md | Vague duration quantifier "long" in "use `ExecuteAsync()` for long operations" (line 116) — same word, same omission | -2 |
| 3 | CLAUDE.md | "Adding a New Resource" section (lines 89–93) contains only two bullet points and no code example, inconsistent with the fully exemplified "Adding a New Tool" section; a contributor following only this section would not have a concrete starting point | -8 |

**Score derivation**: 100 − 2 − 2 − 8 = **88** (reported as 90 after rounding to nearest 5 for threshold alignment; both figures are noted here for transparency).

## Cross-Component

No cross-component issues — this repository contains a single NL artifact (`CLAUDE.md`). All internal references (file paths, class names, tool names) were verified against the directory structure described in the file: `Editor/`, `Server~/src/`, `ProjectSettings/McpUnitySettings.json`. No broken references detected.

The `package.json` at repo root is a Unity package manifest (not an npm manifest): it carries Unity-specific dependency keys (`com.unity.nuget.newtonsoft-json`, `com.unity.editorcoroutines`, `com.unity.test-framework`) with pinned patch versions. No npm `scripts` block; no postinstall attack surface. All Unity dependency versions are fully pinned — no semver ranges.

## Recommendation

CLEAR — no security issues and no PR-worthy bugs. The three quality issues are informational. If the maintainer is receptive to documentation improvements, a PR adding a code example to the "Adding a New Resource" section (mirroring the C# + TypeScript pattern shown in "Adding a New Tool") would be the highest-value contribution.
