# NLPM Audit: matt1398/claude-devtools
**Date**: 2026-04-06  |  **Artifacts**: 17  |  **Strategy**: single
**NL Score**: 91/100
**Security**: REVIEW
**Bugs**: 1  |  **Quality Issues**: 14  |  **Security Findings**: 2

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| src/CLAUDE.md | CLAUDE.md | 70 | IPC table stale: Sessions/Config counts wrong, 6 domains (ssh, updater, context, httpServer, memory, windowControls) undocumented |
| src/main/CLAUDE.md | CLAUDE.md | 78 | 5 undocumented `ipc/` handler files + missing `http/` directory |
| .claude/commands/devtools/markdown-search-logic.md | command | 88 | Missing `allowed-tools`; frontmatter `name` mismatches file path |
| src/main/services/CLAUDE.md | CLAUDE.md | 88 | ~14 services added under discovery/infrastructure/parsing not documented |
| claude-md-auditor.md | agent | 90 | 5 vague quantifiers ("significant" x2, "correctly", "relevant" x2) |
| src/main/ipc/CLAUDE.md | CLAUDE.md | 90 | Structure list omits context.ts, memory.ts, ssh.ts, updater.ts, window.ts |
| src/preload/CLAUDE.md | CLAUDE.md | 90 | ElectronAPI Organization omits 6 whole API groups (ssh, updater, context, httpServer, memory, windowControls) |
| src/renderer/store/CLAUDE.md | CLAUDE.md | 90 | "Slices (12 total)" stale — disk has 16 |
| explain-visible-context.md | command | 91 | Missing `allowed-tools`; 2 vague quantifiers |
| quality-fixer.md | agent | 92 | 4 vague quantifiers |
| chatgroup-architecture.md | command | 95 | Missing `allowed-tools` |
| design-system.md | command | 95 | Missing `allowed-tools` |
| navigation-scroll.md | command | 95 | Missing `allowed-tools` |
| src/renderer/CLAUDE.md | CLAUDE.md | 98 | Utils list omits dateGrouping.ts, keyboardUtils.ts, sessionExporter.ts |
| src/renderer/components/CLAUDE.md | CLAUDE.md | 98 | 1 vague quantifier ("appropriate") |
| src/shared/CLAUDE.md | CLAUDE.md | 98 | Utils list omits memoryIndex.ts, sessionDetailResponse.ts, sessionIdValidator.ts |
| CLAUDE.md | CLAUDE.md | 100 | none |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none |
| Scripts | `resources/afterInstall.sh`, `scripts/notarize.cjs`, `postcss.config.cjs` |
| MCP configs | none |
| Package manifests | `package.json` |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | Medium | resources/afterInstall.sh | 8-9 | SEC-privileged-file-permission | electron-builder `afterInstall` (.deb) hook runs `chown root:root` + `chmod 4755` (SUID) on `/opt/${productFilename}/chrome-sandbox`. This is the documented, standard Electron Linux sandbox fix (electron/electron#17972) — the path is templated by electron-builder's own `productFilename`, not attacker-controlled input, and the script guards with `[ -f "$SANDBOX_PATH" ]` first. |
| 2 | Medium | scripts/notarize.cjs | 7, 14-20 | SEC-env-credential-network | electron-builder `afterSign` hook reads `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD`, `APPLE_TEAM_ID` from the environment and passes them to the official `@electron/notarize` package, which performs a network call to Apple's `notarytool` service. Legitimate build-time credential usage for code-signing; no exfiltration to a non-Apple endpoint. |

No Critical or High findings. No `eval`, no curl-pipe-sh, no reverse shells, no `subprocess(shell=True)`/`os.system`, no `sudo`, no postinstall npm script, no unpinned (`*`/`latest`) dependency versions — all `package.json` dependencies use caret ranges, which is standard practice, not a drift signal.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .claude/commands/devtools/markdown-search-logic.md | Frontmatter `name: claude-devtools:markdown-search` does not match the file's path-derived identity (`markdown-search-logic.md`); every sibling command in the same directory has a `name:` that matches its filename exactly (e.g. `chatgroup-architecture.md` → `claude-devtools:chatgroup-architecture`) | Command may register or display under a name inconsistent with its invocation path, confusing discovery/`/help` listing |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | resources/afterInstall.sh | SUID root permission grant during package post-install | No code fix needed — required for the Chromium sandbox on Linux. Consider a one-line note in SECURITY.md so future auditors don't re-flag it. |
| 2 | scripts/notarize.cjs | Reads Apple signing credentials from env for a notarization network call | No code fix needed — standard `@electron/notarize` flow. Ensure `APPLE_APP_SPECIFIC_PASSWORD` is only ever injected as a CI secret and never logged (`console.log` in this file only logs the *absence* of credentials, not their value — already safe). |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/agents/claude-md-auditor.md | Vague quantifiers: "significant" (x2, line 3), "correctly" (line 99), "relevant" (x2, lines 157, 180) | -10 |
| 2 | .claude/agents/quality-fixer.md | Vague quantifiers: "properly" (lines 33, 57), "relevant" (line 54), "some" (line 61) | -8 |
| 3 | .claude/commands/devtools/explain-visible-context.md | Vague quantifiers: "various" (line 12), "significant" (line 28) | -4 |
| 4 | .claude/commands/devtools/markdown-search-logic.md | Vague quantifier: "relevant" (line 174) | -2 |
| 5 | src/main/CLAUDE.md | Vague quantifier: "appropriate" (line 28) | -2 |
| 6 | src/main/services/CLAUDE.md | Vague quantifier: "appropriate" (line 57) | -2 |
| 7 | src/renderer/components/CLAUDE.md | Vague quantifier: "appropriate" (line 66) | -2 |
| 8 | .claude/commands/devtools/chatgroup-architecture.md | Missing `allowed-tools` frontmatter field | -5 |
| 9 | .claude/commands/devtools/design-system.md | Missing `allowed-tools` frontmatter field | -5 |
| 10 | .claude/commands/devtools/explain-visible-context.md | Missing `allowed-tools` frontmatter field | -5 |
| 11 | .claude/commands/devtools/markdown-search-logic.md | Missing `allowed-tools` frontmatter field | -5 |
| 12 | .claude/commands/devtools/navigation-scroll.md | Missing `allowed-tools` frontmatter field | -5 |
| 13 | src/renderer/CLAUDE.md | Utils list (line 40) omits `dateGrouping.ts`, `keyboardUtils.ts`, `sessionExporter.ts` present on disk | -2 |
| 14 | src/shared/CLAUDE.md | Utils list (line 17) omits `memoryIndex.ts`, `sessionDetailResponse.ts`, `sessionIdValidator.ts` present on disk | -2 |

## Cross-Component
A single root cause explains most of the drift below: the app grew an SSH remote-connection feature, an embedded HTTP server, an auto-updater, window controls, a memory/notes feature, and per-turn context tracking on the IPC/store layer — and none of the affected CLAUDE.md files were updated to match. `.claude/agents/claude-md-auditor.md` exists specifically to prevent this class of drift; it does not appear to have been run since these features landed.

| Finding | Detail |
|---------|--------|
| CC-stale-count — src/CLAUDE.md:22 | "Sessions \| 10 \|..." — `src/preload/index.ts` actually exposes 14 session-related methods (missing from the doc: `searchAllProjects`, `findSessionById`, `findSessionsByPartialId`, `getSessionGroups`) |
| CC-stale-count — src/CLAUDE.md:26 | "Config \| 16 \|..." — the `config: {}` block in `src/preload/index.ts` has 24 methods (missing e.g. `hideSession`, `unhideSession`, `hideSessions`, `unhideSessions`, `selectClaudeRootFolder`, `getClaudeRootInfo`, `findWslClaudeRoots`) |
| CC-orphan-component — src/CLAUDE.md:20 | IPC Communication table has no row for the `ssh`, `windowControls`, `updater`, `context`, `httpServer`, or `memory` API groups, all present in `src/preload/index.ts` |
| CC-orphan-component — src/main/CLAUDE.md:14 | "IPC Organization" list covers 8 files; `src/main/ipc/` also has `context.ts`, `memory.ts`, `ssh.ts`, `updater.ts`, `window.ts` |
| CC-orphan-component — src/main/CLAUDE.md:7 | Structure list omits the `http/` directory that exists directly under `src/main/` |
| CC-orphan-component — src/main/ipc/CLAUDE.md:7 | Structure tree lists 8 files; disk also has `context.ts`, `memory.ts`, `ssh.ts`, `updater.ts`, `window.ts` |
| CC-orphan-component — src/main/services/CLAUDE.md:26 | Key Services list omits ~14 files added under `discovery/` (`MemoryReader.ts`, `SearchTextCache.ts`, `SearchTextExtractor.ts`), `infrastructure/` (`FileSystemProvider.ts`, `HttpServer.ts`, `LocalFileSystemProvider.ts`, `ServiceContext.ts`, `ServiceContextRegistry.ts`, `SshConfigParser.ts`, `SshConnectionManager.ts`, `SshFileSystemProvider.ts`, `SshHostResolver.ts`, `UpdaterService.ts`), and `parsing/` (`AgentConfigReader.ts`) |
| CC-orphan-component — src/preload/CLAUDE.md:9 | ElectronAPI Organization section has no entry for the `windowControls`, `updater`, `ssh`, `context`, `httpServer`, or `memory` objects defined in `src/preload/index.ts` |
| CC-stale-count — src/renderer/store/CLAUDE.md:11 | "Slices (12 total)" — `src/renderer/store/slices/` has 16 files (missing: `connectionSlice`, `contextSlice`, `memorySlice`, `updateSlice`) |
| CC-orphan-component — src/renderer/CLAUDE.md:40 (low severity) | Utils list is illustrative rather than exhaustive; 3 newer files not mentioned |
| CC-orphan-component — src/shared/CLAUDE.md:17 (low severity) | Utils list is illustrative rather than exhaustive; 3 newer files not mentioned |

No orphaned/dangling references were found in the other direction (i.e., no CLAUDE.md pointed at a file, export, or command that no longer exists) — all drift found was one-directional (new code undocumented), not stale-pointer breakage.

## Recommendation
REVIEW — submit NL fix PRs (the 9 cross-component doc-drift items plus the 1 named bug), and flag the 2 Medium security findings in an issue for maintainer awareness rather than a PR (both are legitimate, expected patterns with no code change needed).
