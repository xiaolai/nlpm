# NLPM Audit: YishenTu/claudian
**Date**: 2026-06-20  |  **Artifacts**: 6  |  **Strategy**: single
**NL Score**: 100/100
**Security**: REVIEW
**Bugs**: 0  |  **Quality Issues**: 0  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| CLAUDE.md | Project Context | 100 | — |
| src/core/CLAUDE.md | Module Context | 100 | — |
| src/features/chat/CLAUDE.md | Feature Context | 100 | — |
| src/providers/claude/CLAUDE.md | Provider Context | 100 | — |
| src/providers/codex/CLAUDE.md | Provider Context | 100 | — |
| src/style/CLAUDE.md | Style Guide | 100 | — |

All six files are well-structured, concrete, and free of vague quantifiers. No frontmatter penalty applies — CLAUDE.md files are project-context documents and do not carry a required YAML schema in the Claude Code convention. Code examples, dependency diagrams, and gotcha sections are present where relevant. The audit applied no deductions.

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
| Hooks | 0 (none found) |
| Scripts | `scripts/sync-version.js`, `scripts/rendererSafeUnref.js`, `scripts/run-jest.js`, `scripts/build.mjs`, `scripts/build-css.mjs`, `scripts/postinstall.mjs` |
| MCP configs | 0 (no `.mcp.json` at repo root) |
| Package manifests | `package.json` |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | `package.json` | 10 | postinstall-script | `postinstall` lifecycle hook runs `node scripts/postinstall.mjs` automatically on every `npm install`. Content is benign (CI guard + file copy) but the hook provides an arbitrary-code execution surface at install time. |
| 2 | Medium | `scripts/build.mjs` | 19 | execSync-shell-injection | `process.argv.slice(2).join(' ')` is interpolated unquoted into an `execSync` template literal. Node's `execSync(string)` invokes `sh -c`, so shell metacharacters in CLI args (`;`, `&&`, `|`) would be interpreted. Developer-only build path, but the pattern is exploitable if build args come from an untrusted source (e.g., CI matrix variable). |
| 3 | Low | `package.json` | 44 | unpinned-floating-tag | `"obsidian": "latest"` resolves to the current npm latest at install time. A future major obsidian release could silently introduce breaking API changes. |
| 4 | Low | `package.json` | 31 | unpinned-semver | Most `devDependencies` use `^` (patch+minor free). Supply-chain risk if any devDependency is compromised in a minor release. A committed `package-lock.json` with `npm ci` mitigates this. |

## Bugs (PR-worthy)
No NL bugs found.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `scripts/build.mjs` | Shell injection via unquoted args in `execSync` template literal | Replace with `spawnSync('node', ['esbuild.config.mjs', ...process.argv.slice(2)], { cwd: ROOT, stdio: 'inherit' })` to avoid shell interpretation |
| 2 | `package.json` | `"obsidian": "latest"` floating tag | Pin to a concrete semver range (e.g. `"^1.8.0"`) and update deliberately on new releases |

## Quality Issues (informational)
No quality issues found.

## Cross-Component
The root `CLAUDE.md` architecture table lists `features/inline-edit` and `features/settings` as distinct modules but neither has a corresponding `CLAUDE.md` sub-file. The four other modules with sub-files all follow the established pattern. This is a documentation coverage gap, not a broken reference — those rows carry inline descriptions rather than links. Adding `src/features/inline-edit/CLAUDE.md` and `src/features/settings/CLAUDE.md` would complete the pattern.

All cross-file references within the audited set resolve correctly:
- Root `CLAUDE.md` links to `src/core/CLAUDE.md`, `src/providers/claude/CLAUDE.md`, `src/providers/codex/CLAUDE.md`, `src/features/chat/CLAUDE.md`, and `src/style/CLAUDE.md` — all present.
- No terminology drift detected: `ProviderRegistry`, `ProviderWorkspaceRegistry`, `ChatRuntime`, `providerId`, `providerState` are used consistently across all files.
- `Conversation.providerState` is correctly described as opaque in the feature layer (chat CLAUDE.md) and typed behind provider-specific helpers (provider files) — consistent.
- The `Bang-bash` / `$` skills / `#` instruction mode feature split described in the chat file matches the Codex provider file's capability list.

## Recommendation
REVIEW — Security findings are Medium/Low only (no critical or high after detailed content analysis). The pre-scan HIGH signal was the `postinstall` script pattern; detailed review confirms benign content. No NL fix PRs are needed (zero bugs). Submit security-fix PRs for the `execSync` shell-injection pattern and the `obsidian: latest` pin.
