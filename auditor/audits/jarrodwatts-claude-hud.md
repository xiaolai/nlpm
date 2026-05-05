# NLPM Audit: jarrodwatts/claude-hud
**Date**: 2026-04-06  |  **Artifacts**: 4  |  **Strategy**: single
**NL Score**: 92/100
**Security**: CLEAR
**Bugs**: 1  |  **Quality Issues**: 3  |  **Security Findings**: 5

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `CLAUDE.md` | Project Instructions | 88 | Developer docs only; no NL-artifact-specific structure |
| `commands/configure.md` | Command | 90 | Minor: no preview example of question prompts as rendered |
| `commands/setup.md` | Command | 91 | BUG: `Write` not in `allowed-tools`; Step 4 creates new config.json |
| `.claude-plugin/plugin.json` | Plugin Manifest | 100 | Clean — all required fields present |

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
| Hooks | 0 (none found) |
| Scripts (src/*.ts compiled to dist/*.js) | 42 JS + 21 TS = 63 |
| MCP configs | 0 |
| Package manifests | `package.json` |

No `hooks/` directory, no `.mcp.json`, no `requirements.txt`.

The 63 "script files" reported by the pre-scan are the compiled `dist/*.js` and `src/*.ts` TypeScript sources — not shell scripts. No hook or MCP execution surfaces exist.

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | `src/extra-cmd.ts` | 81 | `exec()` with user shell string | `execAsync(cmd)` runs a shell command sourced from `--extra-cmd` CLI arg. Uses `exec` (shell=true) rather than `execFile`. By-design feature; user controls their own shell. Output is sanitized before display. Practical risk is self-inflicted. |
| 2 | Low | `commands/setup.md` | 312 | Network call to external service | `gh repo star jarrodwatts/claude-hud` / `gh api -X PUT /user/starred/...` executes a GitHub API mutation. User must explicitly consent ("if they agree"). No credential exfiltration; stars their own account. |
| 3 | Low | `package.json` | 33 | Unpinned semver range | `@types/node: ^25.6.0` — caret range allows minor/patch updates |
| 4 | Low | `package.json` | 34 | Unpinned semver range | `c8: ^11.0.0` — caret range allows minor/patch updates |
| 5 | Low | `package.json` | 35 | Unpinned semver range | `typescript: ^6.0.3` — caret range allows minor/patch updates |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `commands/setup.md` | `Write` tool not declared in `allowed-tools`; Step 4 instructs Claude to create `plugins/claude-hud/config.json` (new file creation). `Edit` is declared but cannot create new files in Claude Code. | Step 4 config write will fail if user selects optional features and config.json does not already exist |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `src/extra-cmd.ts` | `exec()` (shell=true) used instead of `execFile`. While intentional per security comment, `execFile` with a parsed argv array would eliminate the shell layer entirely. | Parse the `--extra-cmd` string into `[file, ...args]` and call `execFile` instead; document that compound shell pipelines are not supported |
| 2 | `package.json` | Dev dependencies use `^` semver ranges. For a published plugin, reproducible installs matter. | Pin all devDependencies to exact versions or use `package-lock.json` with `npm ci` only (already present) |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `commands/setup.md` | Vague quantifier: "within a few seconds" (line 233) — no guidance on when to treat slow output as a failure | -2 |
| 2 | `commands/setup.md` | Vague quantifier: "most common cause on macOS" (line 316) — implies ordering that isn't justified | -2 |
| 3 | `commands/setup.md` | Description `Configure claude-hud as your statusline` is terse — does not hint at cross-platform detection, ghost-install cleanup, or runtime discovery that the command actually performs | -1 (informational) |

## Cross-Component
- `plugin.json` `commands` array references `./commands/setup.md` and `./commands/configure.md` — both files exist ✓
- `setup.md` and `configure.md` are clearly separated in purpose (initial setup vs. ongoing reconfiguration) ✓
- `CLAUDE.md` accurately describes the plugin architecture (dist/src layout, statusLine config path, runtime options) ✓
- No orphaned components, no broken relative paths, no stale counts

No cross-component issues found.

## Recommendation
CLEAR — submit PRs for the bug (add `Write` to `setup.md` `allowed-tools`) and the medium-severity `exec`→`execFile` refactor. Low-severity unpinned deps are housekeeping. No Critical or High security findings; no private disclosure needed.
