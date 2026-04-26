# NLPM Audit: kbwo/ccmanager
**Date**: 2026-04-26  |  **Artifacts**: 11  |  **Strategy**: single
**NL Score**: 83/100
**Security**: BLOCKED
**Bugs**: 3  |  **Quality Issues**: 18  |  **Security Findings**: 7

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/commands/kiro/spec-design.md | command | 67 | Vague quantifiers (capped -20) + unused `Update` tool + no empty-input guard |
| .claude/commands/kiro/spec-status.md | command | 79 | Unused `Update` tool + no empty-input guard + vague language |
| .claude/commands/kiro/steering.md | command | 80 | Vague quantifiers throughout (capped -20) |
| .claude/commands/kiro/validate-design.md | command | 80 | No empty-input guard + vague language |
| .claude/commands/kiro/validate-gap.md | command | 80 | No empty-input guard + vague language |
| .claude/commands/kiro/spec-requirements.md | command | 81 | Unused `Update` tool + no empty-input guard + vague language |
| .claude/commands/kiro/spec-tasks.md | command | 82 | No empty-input guard + vague language |
| .claude/commands/kiro/spec-init.md | command | 86 | No empty-input guard + mild vague language |
| .claude/commands/kiro/spec-impl.md | command | 88 | No empty-input guard |
| .claude/commands/kiro/steering-custom.md | command | 92 | Mild vague language |
| CLAUDE.md | project doc | 96 | Minor vague language |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 4 |
| Medium | 1 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | None |
| Scripts | `.devcontainer/init-firewall.sh`, `scripts/setup-submodule-test.sh`, `bin/cli.js` |
| MCP configs | None |
| Package manifests | `package.json` |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | .claude/commands/kiro/spec-requirements.md | 21 | SEC-shell-injection | `!bash -c 'ls -la .kiro/specs/$1/'` embeds user-supplied argument directly in shell command without sanitization; crafted feature name (e.g. `foo'; cat ~/.ssh/id_rsa; echo`) executes arbitrary shell commands |
| 2 | High | .claude/commands/kiro/spec-status.md | 13 | SEC-shell-injection | `!bash -c 'ls -la .kiro/specs/$1/ 2>/dev/null'` embeds user argument directly in bash -c context command; same injection risk as finding #1 |
| 3 | High | .claude/commands/kiro/validate-gap.md | 21 | SEC-shell-injection | `!bash -c 'ls -la .kiro/specs/$1/ 2>/dev/null'` embeds user argument in shell without sanitization |
| 4 | High | scripts/setup-submodule-test.sh | 22 | SEC-path-traversal | `rm -rf "$PARENT_DIR"` where PARENT_DIR is derived directly from the user-supplied positional argument $1; empty-string guard present but value is not path-restricted, allowing deletion of arbitrary directories outside the repository |
| 5 | Medium | .devcontainer/init-firewall.sh | 34 | SEC-network-call | `curl -s https://api.github.com/meta` fetches external data to populate firewall allowlist; if GitHub API is compromised or returns malicious CIDR ranges the ipset could be populated with attacker-controlled routes (mitigated by validation on lines 47-49) |
| 6 | Low | package.json | 54 | SEC-unpinned-semver | devDependencies use caret ranges (e.g. `"^9.28.0"`) rather than exact pins, allowing patch/minor version drift on fresh installs; production optionalDependencies are correctly pinned to `4.1.8` |
| 7 | Low | bin/cli.js | 78 | SEC-env-passthrough | `execFileSync(binaryPath, args, { env: process.env })` forwards the complete process environment (including any secrets in env vars) to the platform-specific native binary subprocess |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .claude/commands/kiro/spec-design.md | `Update` is not a recognized Claude Code tool declared in `allowed-tools` (line 3) | Depending on runtime version, unrecognized tool names in the manifest may be silently ignored or cause registration warnings; at minimum it creates misleading capability claims |
| 2 | .claude/commands/kiro/spec-requirements.md | `Update` declared in `allowed-tools` (line 3) — same as bug #1 | Same impact |
| 3 | .claude/commands/kiro/spec-status.md | `Update` declared in `allowed-tools` (line 3) — same as bug #1 | Same impact |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | .devcontainer/init-firewall.sh | curl without timeout on line 34 and 115 fetches external data that populates firewall allowlist | Add `--max-time 10 --retry 2` and pin the GitHub meta URL; verify TLS certificate (`--fail-with-body`); consider caching the response |
| 2 | package.json | devDependencies use semver caret ranges (lines 54-68) | Pin exact versions with `npm ci` or use a lock-file-only policy; at minimum add a renovate/dependabot config to control update cadence |
| 3 | bin/cli.js | Full `process.env` forwarded to native binary (line 78) | Build an explicit allowlist of required env vars (e.g. PATH, HOME, TERM) rather than forwarding all; avoids leaking API keys or credentials present in the calling shell |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/commands/kiro/spec-design.md | No guard for empty `$1` argument; command silently references undefined feature name throughout | -10 |
| 2 | .claude/commands/kiro/spec-design.md | Vague quantifiers throughout 460-line body: "comprehensive", "thorough", "appropriate", "relevant", "key" (10+ instances, capped) | -20 |
| 3 | .claude/commands/kiro/spec-impl.md | No guard for empty `$1` argument | -10 |
| 4 | .claude/commands/kiro/spec-init.md | No guard for empty `$ARGUMENTS`; feature name generation would silently receive an empty string | -10 |
| 5 | .claude/commands/kiro/spec-requirements.md | No guard for empty `$1` argument | -10 |
| 6 | .claude/commands/kiro/spec-requirements.md | Vague quantifiers: "comprehensive" (description), "appropriate subject" (line 35), "concise" (line 36) (~3 instances) | -6 |
| 7 | .claude/commands/kiro/spec-status.md | No guard for empty `$1` argument | -10 |
| 8 | .claude/commands/kiro/spec-status.md | Vague quantifiers: "comprehensive" (line 24), "appropriate" (line 73), "clear" (line 79) (~4 instances) | -8 |
| 9 | .claude/commands/kiro/spec-tasks.md | No guard for empty `$1` argument | -10 |
| 10 | .claude/commands/kiro/spec-tasks.md | Vague quantifiers: "comprehensive context" (line 30), "appropriate" (line 72), "relevant" (lines 76, 108) (~4 instances) | -8 |
| 11 | .claude/commands/kiro/steering.md | Vague quantifiers throughout: "comprehensive" ×4, "significant" ×4, "relevant" ×2, "major" ×3 (13+ instances, capped) | -20 |
| 12 | .claude/commands/kiro/validate-design.md | No guard for empty `$1` argument | -10 |
| 13 | .claude/commands/kiro/validate-design.md | Vague quantifiers: "acceptable" (line 116), "manageable" (line 116), "significant" (line 115), "thorough" (line 88), "appropriate" (line 164) (~5 instances) | -10 |
| 14 | .claude/commands/kiro/validate-gap.md | No guard for empty `$1` argument | -10 |
| 15 | .claude/commands/kiro/validate-gap.md | Vague quantifiers: "comprehensive" (line 7), "relevant" (lines 35, 40), "appropriate" (line 95), "thorough" (implied line 33) (~5 instances) | -10 |
| 16 | .claude/commands/kiro/steering-custom.md | Vague quantifiers: "appropriate" (line 82), "clear" (line 98), "unique value" (line 150), "relevant" (line 102) (~4 instances) | -8 |
| 17 | .claude/commands/kiro/steering-custom.md | Bare `ultrathink` directive on final line (line 153) — internal model-hint leaked into the command body; should be removed or placed in a dedicated metacognitive section | -0 (informational) |
| 18 | CLAUDE.md | Minor vague quantifiers: "focused updates" (line 5), "rapid feedback" (line 10), "signal-rich" (line 30) (~3 instances) | -4 |

## Cross-Component
**CC-1 — bun dependency undocumented (CLAUDE.md ↔ package.json)**: CLAUDE.md instructs users to run `npm run dev`, `npm run test`, etc. (lines 10–14) but every script in `package.json` delegates to `bun` (`bun run tsc`, `bun run eslint`, etc.). Users who lack `bun` in their PATH will see cryptic failures. CLAUDE.md should list `bun` as a prerequisite alongside the npm commands.

**CC-2 — Unsanitized `$1` pattern repeated across three commands**: `spec-requirements.md`, `spec-status.md`, and `validate-gap.md` all share the identical `!bash -c 'ls -la .kiro/specs/$1/...'` shell injection pattern. This is a cross-cutting defect; a single shared fix (sanitize `$1` at the top of each command, e.g., validate against `^[a-zA-Z0-9_-]+$` before the bash inline) should be applied uniformly.

**CC-3 — `Update` tool declared inconsistently**: Three commands (`spec-design.md`, `spec-requirements.md`, `spec-status.md`) declare `Update` in `allowed-tools`; the remaining seven commands do not. If `Update` were a valid alias for an existing operation, it should appear wherever that operation is needed. Its selective appearance suggests it was copy-pasted from an early template draft and not removed when other commands were finalized.

## Recommendation
BLOCKED — do not submit PRs. File private security report for the three shell-injection findings (HIGH) in the NL command files and the path-traversal risk in `scripts/setup-submodule-test.sh`. Once those four HIGH findings are remediated, the remaining NL bugs (invalid `Update` tool declarations) and the CLAUDE.md/bun discrepancy are clean PR candidates.
