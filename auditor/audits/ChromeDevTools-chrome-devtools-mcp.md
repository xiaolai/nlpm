# NLPM Audit: ChromeDevTools/chrome-devtools-mcp
**Date**: 2026-04-06  |  **Artifacts**: 7  |  **Strategy**: single
**NL Score**: 94/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 3  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `.claude-plugin/plugin.json` | plugin-manifest | 92 | Uses `@latest` unpinned version in MCP server args |
| `skills/a11y-debugging/SKILL.md` | skill | 93 | "standard" used vaguely in troubleshooting section |
| `skills/memory-leak-debugging/SKILL.md` | skill | 93 | Minor: "extremely large" is imprecise |
| `skills/troubleshooting/SKILL.md` | skill | 93 | Clean; minor imprecision in step descriptions |
| `skills/chrome-devtools/SKILL.md` | skill | 94 | No material issues |
| `skills/chrome-devtools-cli/SKILL.md` | skill | 95 | No material issues |
| `skills/debug-optimize-lcp/SKILL.md` | skill | 96 | Exemplary specificity; concrete metrics throughout |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts (JS) | `scripts/eslint_rules/enforce-zod-schema-rule.js`, `scripts/eslint_rules/no-direct-third-party-imports-rule.js`, `scripts/eslint_rules/local-plugin.js`, `scripts/eslint_rules/check-license-rule.js` |
| MCP configs | `.claude-plugin/plugin.json` (mcpServers declaration) |
| Package manifests | `package.json` |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | `package.json` | 27 | SEC-postinstall-script | `prepare` script runs `node --experimental-strip-types scripts/prepare.ts` automatically on `npm install` and `npm publish`, executing arbitrary TypeScript before the build is inspected |
| 2 | Low | `.claude-plugin/plugin.json` | 9 | SEC-unpinned-semver | MCP server configured to run `chrome-devtools-mcp@latest` via `npx`; version floats on every MCP client restart, creating supply-chain risk |
| 3 | Low | `package.json` | 49–83 | SEC-unpinned-semver | Most `devDependencies` use `^` semver ranges (e.g., `"@eslint/js": "^9.35.0"`), allowing automatic minor/patch updates on each `npm install` |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No bugs found | All required frontmatter present; all internal references verified on disk |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `package.json` | `prepare` script runs implicitly on install | Rename to `prepack` or add inline comment; document what it does in README so contributors understand the side-effect |
| 2 | `.claude-plugin/plugin.json` | `chrome-devtools-mcp@latest` is unpinned | Pin to a specific release, e.g., `chrome-devtools-mcp@1.0.1`, and update alongside `package.json` version bumps |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `skills/a11y-debugging/SKILL.md` | "standard a11y queries" (line 87) — "standard" is vague; reader cannot determine which tools or calls qualify | -2 |
| 2 | `skills/memory-leak-debugging/SKILL.md` | "they are extremely large" (line 13) — "extremely" is an imprecise intensifier; a concrete size hint (e.g., ">100 MB") would make the constraint actionable | -2 |
| 3 | `.claude-plugin/plugin.json` | No explicit `skills` array; relies on auto-discovery of the `skills/` subdirectory. If the Claude Code plugin loader changes its discovery logic, skills will silently disappear from the plugin | -2 |

## Cross-Component
All six SKILL.md files are internally consistent: each references only MCP tools provided by the `chrome-devtools` MCP server declared in `.claude-plugin/plugin.json`. All internal relative references (`references/a11y-snippets.md`, `references/installation.md`, `references/lcp-snippets.md`, `references/memlab.md`, `references/common-leaks.md`, `references/compare_snapshots.js`) were confirmed present on disk.

The plugin `mcpServers` key (`chrome-devtools`) matches the MCP server name implied by the skills. No orphaned components, stale counts, or terminology drift detected across the corpus.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

No Critical or High security findings were detected. The NL quality is high across all six skills (93–96 range), with the plugin manifest pulling the weighted average down slightly to 94. Two low-severity security fixes (pin the npx version, document the prepare script) are safe to open as public PRs. The three quality issues are informational and unlikely to affect runtime behavior.
