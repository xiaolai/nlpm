# NLPM Audit: mksglu/context-mode
**Date**: 2026-04-26  |  **Artifacts**: 11  |  **Strategy**: single
**NL Score**: 92/100
**Security**: BLOCKED
**Bugs**: 1  |  **Quality Issues**: 1  |  **Security Findings**: 8

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| CLAUDE.md | CLAUDE.md | 75 | Tool names omit ctx_ prefix (execute vs ctx_execute throughout) |
| skills/context-mode-ops/SKILL.md | Skill | 90 | No invocation examples; dense cross-references to sub-docs |
| configs/claude-code/CLAUDE.md | CLAUDE.md | 92 | File is 300+ lines; dense but well-structured |
| skills/context-mode/SKILL.md | Skill | 92 | "UNSURE" vague qualifier in decision tree |
| hooks/hooks.json | Hook Config | 93 | Repetitive PreToolUse entries (one per matcher, same script) |
| skills/ctx-doctor/SKILL.md | Skill | 95 | None |
| skills/ctx-insight/SKILL.md | Skill | 95 | None |
| skills/ctx-upgrade/SKILL.md | Skill | 95 | None |
| skills/ctx-stats/SKILL.md | Skill | 96 | None |
| skills/ctx-purge/SKILL.md | Skill | 96 | None |
| .claude-plugin/plugin.json | Plugin Manifest | 100 | None |

**Weighted average**: (75+90+92+92+93+95+95+95+96+96+100) / 11 = **92/100**

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 |
| Medium | 4 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hook scripts | hooks/pretooluse.mjs, hooks/posttooluse.mjs, hooks/sessionstart.mjs, hooks/precompact.mjs, hooks/userpromptsubmit.mjs, hooks/ensure-deps.mjs |
| Shell scripts | scripts/ctx-debug.sh, scripts/install-openclaw-plugin.sh, scripts/test-openclaw-e2e.sh |
| MCP config | .mcp.json |
| Package manifests | package.json (has postinstall) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | hooks/ensure-deps.mjs | 58 | SEC-shell-true | execSync with `shell: true` and interpolated `${pkg}` variable; `pkg` is hardcoded "better-sqlite3" but shell: true creates injection surface; replace with execFile + array args |
| 2 | High | package.json | 95 | SEC-postinstall-script | postinstall lifecycle hook auto-executes scripts/postinstall.mjs on every `npm install`; script invokes system commands (where, mklink) on Windows; no user confirmation |
| 3 | Medium | hooks/ensure-deps.mjs | 54 | SEC-runtime-package-install | npm install executed at hook runtime when better-sqlite3 is missing; installs packages without explicit user consent inside the agent's event loop |
| 4 | Medium | hooks/ensure-deps.mjs | 129 | SEC-shell-true | Second execSync with `shell: true` for `npm rebuild better-sqlite3`; hardcoded args reduce actual risk but pattern is dangerous |
| 5 | Medium | hooks/pretooluse.mjs | 88 | SEC-writes-outside-repo | Self-heal block writes installed_plugins.json and settings.json in ~/.claude/ (user home directory); modifies Claude Code configuration outside the project repo |
| 6 | Medium | scripts/ctx-debug.sh | 175 | SEC-path-modification | Unconditionally exports NODE_PATH with plugin's node_modules prepended; affects all child Node.js processes spawned during the diagnostic |
| 7 | Low | hooks/ensure-deps.mjs | 155 | SEC-shell-interpolation | execSync(`codesign --sign - --force "${binaryPath}"`) runs through system shell with path derived from CLAUDE_PLUGIN_ROOT env var; quotes protect against typical injection but env var source is untrusted |
| 8 | Low | package.json | null | SEC-unpinned-semver | Core and native dependencies use `^` semver ranges (better-sqlite3 ^12.6.2, @modelcontextprotocol/sdk ^1.26.0, zod ^3.25.0); native module especially risky as patch updates can introduce ABI breaks or supply-chain compromise |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | CLAUDE.md | Root CLAUDE.md uses unprefixed tool names (`execute`, `search`, `batch_execute`, `execute_file`, `fetch_and_index`) throughout "Tool Selection" and "Rules" sections, but actual MCP tool names have `ctx_` prefix (`ctx_execute`, `ctx_search`, etc.) as confirmed by hooks.json matchers and configs/claude-code/CLAUDE.md | Claude follows root CLAUDE.md and attempts to call non-existent tools, failing silently or falling back to native tools (the opposite of intended behavior) |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | hooks/ensure-deps.mjs | shell: true at lines 58 and 129 | Replace execSync template literals with execFile(['npm', 'install', pkg, ...]) and execFile(['npm', 'rebuild', 'better-sqlite3', ...]) to eliminate shell injection surface |
| 2 | hooks/ensure-deps.mjs | Runtime npm install at line 54 | Gate the install behind a user-visible warning or a flag; at minimum log to stderr so the user is aware of the network call |
| 3 | hooks/pretooluse.mjs | Writes to ~/.claude/ config files | Scope the self-heal to read-only verification and emit a console warning instead of silently rewriting configuration; or add a opt-out env var |
| 4 | scripts/ctx-debug.sh | NODE_PATH modification at line 175 | Use a subshell or pass as env prefix to the specific node invocation rather than exporting globally |
| 5 | package.json | Unpinned semver for native module | Pin better-sqlite3 to exact version (e.g., "12.6.2") and use lockfile (pnpm-lock.yaml is present) to enforce; consider npm audit in CI |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/context-mode/SKILL.md | "UNSURE" at line 50 in decision tree branch condition is vague; a more precise condition (e.g., "output may exceed 20 lines") would eliminate ambiguity for borderline cases | -2 |

## Cross-Component
**Terminology drift — root CLAUDE.md vs all other artifacts**: The root `CLAUDE.md` documents the tool API using bare names (`execute`, `search`, `batch_execute`, `execute_file`, `fetch_and_index`) while every other artifact uses `ctx_`-prefixed names. Evidence that the ctx_ form is canonical:

- `configs/claude-code/CLAUDE.md` uses `ctx_execute`, `ctx_search`, `ctx_batch_execute`, `ctx_execute_file`, `ctx_fetch_and_index`, `ctx_index`, `ctx_purge`, `ctx_stats`, `ctx_upgrade` throughout.
- `hooks/hooks.json` matchers include `mcp__plugin_context-mode_context-mode__ctx_execute`, `mcp__plugin_context-mode_context-mode__ctx_execute_file`, `mcp__plugin_context-mode_context-mode__ctx_batch_execute`.
- `skills/context-mode/SKILL.md` uses ctx_-prefixed names in all tool reference tables.

The root CLAUDE.md appears to be a stale copy that predates the `ctx_` prefix convention introduced with the multi-adapter architecture. It is likely what gets injected into user projects as a global context file, making this the highest-impact artifact to fix.

**Hook configuration consistency**: `hooks/hooks.json` defines five separate PreToolUse matchers each pointing to the same `pretooluse.mjs` script. This is functionally correct (each matcher has different tool-filter logic handled inside the script) but creates maintenance burden — any hook path change requires updating all five entries. The hooks.json structure is otherwise consistent with the plugin.json registration.

**Skill cross-references**: `skills/context-mode-ops/SKILL.md` references `validation.md`, `tdd.md`, `agent-teams.md`, `communication.md`, `marketing.md`, `triage-issue.md`, `review-pr.md`, `release.md` as relative links. All eight files are confirmed present in the `skills/context-mode-ops/` directory. No broken references.

## Recommendation

**BLOCKED — do not submit PRs. File private security report.**

Two HIGH security findings are present:
1. `hooks/ensure-deps.mjs` uses `execSync` with `shell: true` and a variable-interpolated command string (finding #1). Risk is currently mitigated because `${pkg}` is drawn from a hardcoded constant, but the pattern is dangerous and must be refactored to eliminate the shell injection surface before contributing.
2. `package.json` auto-executes `scripts/postinstall.mjs` as an npm lifecycle hook (finding #2). The script invokes system commands on Windows without user consent. Disclosure note: neither finding involves credential exfiltration or remote code execution from external input, so private disclosure to the maintainer is appropriate (not a CVE-class issue), but NL fix PRs should wait until the security posture is addressed.

Once HIGH findings are resolved (refactor shell: true → execFile; document or restrict postinstall behavior), the repo qualifies for REVIEW-level contribution: the NL bug (root CLAUDE.md tool names) is a high-value, clearly correct fix.
