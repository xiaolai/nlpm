# NLPM Audit: memvid/claude-brain
**Date**: 2026-04-30  |  **Artifacts**: 10  |  **Strategy**: single
**NL Score**: 96/100
**Security**: BLOCKED
**Bugs**: 3  |  **Quality Issues**: 7  |  **Security Findings**: 6

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `commands/ask.md` | Command | 88 | No empty-input handling; vague "when applicable" |
| `commands/search.md` | Command | 90 | No empty-input handling; broken limit arg parsing |
| `skills/memory/SKILL.md` | Skill | 93 | File path typo `.mind.mv2`; duplicate of mind/SKILL.md |
| `skills/mind/SKILL.md` | Skill | 93 | File path typo `.mind.mv2`; duplicate of memory/SKILL.md |
| `hooks/hooks.json` | Hook config | 95 | Stop timeout (10 s) mismatches src/dist (30 s) |
| `commands/recent.md` | Command | 98 | Vague "when helpful" |
| `commands/stats.md` | Command | 98 | Vague "when appropriate" |
| `.claude-plugin/plugin.json` | Plugin manifest | 100 | — |
| `dist/hooks/hooks.json` | Hook config | 100 | — |
| `src/hooks/hooks.json` | Hook config | 100 | — |

**Weighted average**: (88+90+93+93+95+98+98+100+100+100) / 10 = **955 / 10 = 96/100**

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 3 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hook configs | `hooks/hooks.json`, `dist/hooks/hooks.json`, `src/hooks/hooks.json` |
| Hook scripts (TypeScript source) | `src/hooks/smart-install.ts`, `src/hooks/session-start.ts`, `src/hooks/post-tool-use.ts`, `src/hooks/stop.ts` |
| Scripts (TypeScript source) | `src/scripts/ask.ts`, `src/scripts/find.ts`, `src/scripts/stats.ts`, `src/scripts/timeline.ts`, `src/scripts/utils.ts` |
| Package manifest | `package.json` |
| MCP configs | none |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | `commands/recent.md` | 15 | unquoted-arguments | `${ARGUMENTS:-20}` is unquoted in bash; user-supplied input expands without word-splitting protection, enabling shell injection (e.g. `/mind:recent $(id)`) |
| 2 | Medium | `src/hooks/smart-install.ts` | 78 | runtime-package-install | `execSync("npm install …")` runs a live npm install on every SessionStart; any compromised registry entry for `@memvid/sdk` executes in the user's environment |
| 3 | Medium | `src/scripts/ask.ts` | 23 | runtime-package-install | Same `execSync("npm install …")` pattern at script invocation time |
| 4 | Medium | `src/scripts/find.ts` | 23 | runtime-package-install | Same `execSync("npm install …")` pattern at script invocation time |
| 5 | Low | `package.json` | 47 | unpinned-semver | `@memvid/sdk: "^2.0.149"` — caret range allows automatic minor/patch upgrades; pin to exact version for reproducible installs |
| 6 | Low | `package.json` | 48 | unpinned-semver | `proper-lockfile: "^4.1.2"` — same caret-range concern |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `commands/search.md` | `"$ARGUMENTS"` quoted as a single token passes `<query> [limit]` as one string to `find.js`; the hardcoded `10` on the bash line is always used as the limit — the user-supplied limit is silently ignored | The `[limit]` documented in `argument-hint` has no effect; users who type `/mind:search auth 20` always get 10 results |
| 2 | `skills/memory/SKILL.md` | Line 71: references `.mind.mv2` but the actual file is stored at `.claude/mind.mv2` | Users who follow the "Sharing" tip will look for the wrong filename |
| 3 | `skills/mind/SKILL.md` | Line 71: same `.mind.mv2` typo (this file is a duplicate of `skills/memory/SKILL.md` with only the `name` field differing) | Same sharing confusion; duplicate maintenance surface |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `src/scripts/ask.ts` | Runtime `npm install` in user-facing script | Check for `@memvid/sdk` before each script invocation is redundant given `smart-install.ts` already handles this at SessionStart; remove the duplicate install-guard from `ask.ts` and `find.ts` |
| 2 | `src/scripts/find.ts` | Same runtime `npm install` pattern | Same as above |
| 3 | `package.json` | `@memvid/sdk: "^2.0.149"` unpinned | Pin to `"2.0.149"` (exact) and commit `package-lock.json` to eliminate supply-chain drift |
| 4 | `package.json` | `proper-lockfile: "^4.1.2"` unpinned | Pin to `"4.1.2"` |

> **Note**: Finding #1 (HIGH — unquoted ARGUMENTS in `commands/recent.md`) requires **private disclosure**, not a public PR. Do not open a public issue or PR for this finding.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `commands/ask.md` | No empty-input handling: invoking `/mind:ask` with no arguments passes an empty string to `ask.js`, which exits with an unhelpful usage error; the command should describe this behaviour | -10 |
| 2 | `commands/ask.md` | Vague quantifier: "Reference specific memories **when applicable**" — "when applicable" is undefined | -2 |
| 3 | `commands/search.md` | No empty-input handling: invoking `/mind:search` with no arguments produces a bare usage error from `find.js` | -10 |
| 4 | `commands/recent.md` | Vague quantifier: "Group by session or time period **when helpful**" — "when helpful" is undefined | -2 |
| 5 | `commands/stats.md` | Vague quantifier: "Summarize key findings in a table **when appropriate**" — "when appropriate" is undefined | -2 |
| 6 | `skills/memory/SKILL.md` | Exact duplicate of `skills/mind/SKILL.md` (only `name` differs); creates dual maintenance burden and risks divergence | informational |
| 7 | `hooks/hooks.json` | Stop hook `timeout` is 10 s here vs 30 s in `src/hooks/hooks.json` and `dist/hooks/hooks.json`; if this file is the runtime-active one the Stop hook may time out before finishing the session summary | informational |

## Cross-Component
**CC-1 — Duplicate skill content**: `skills/memory/SKILL.md` and `skills/mind/SKILL.md` are byte-for-byte identical except for the `name` field (`memory` vs `mind`). If both are loaded, Claude sees two skills with different names but the same instructions, which is wasteful and likely to diverge as the plugin evolves. One of them should be removed, or the content should be shared via a single canonical file.

**CC-2 — hooks/hooks.json timeout drift**: The `hooks/` directory appears to be a manually maintained source copy, while `dist/hooks/` is generated by `cp src/hooks/hooks.json dist/hooks/` at build time. The Stop hook timeout is 10 s in `hooks/hooks.json` but 30 s in both `src/hooks/hooks.json` and `dist/hooks/hooks.json`. If Claude Code loads `dist/hooks/hooks.json` (the build output), the runtime timeout is 30 s; if it loads the root `hooks/hooks.json`, it is 10 s. The discrepancy should be resolved and the stale copy removed.

**CC-3 — search.md argument-hint contradicts implementation**: The `argument-hint: <query> [limit]` documents a two-argument interface, but the bash invocation `node "…/find.js" "$ARGUMENTS" 10` always passes 10 as the limit regardless of user input. The hint either needs to be changed to `<query>` or the bash line needs to pass the limit separately (`"$1"` and `"$2"` instead of `"$ARGUMENTS"`).

## Recommendation
BLOCKED — do not submit PRs. File a private security report for finding #1 (HIGH: unquoted `${ARGUMENTS:-20}` in `commands/recent.md` enables shell injection). Once that is addressed, submit public PRs for the 3 NL bugs and 4 medium/low security fixes.
