# NLPM Audit: thedotmack/claude-mem
**Date**: 2026-04-07  |  **Artifacts**: 39  |  **Strategy**: batched
**NL Score**: 97/100
**Security**: BLOCKED
**Bugs**: 5  |  **Quality Issues**: 3  |  **Security Findings**: 12

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `.claude/commands/anti-pattern-czar.md` | Command | 35 | Missing frontmatter name+description (-50), no allowed-tools (-5), no empty input handling (-10) |
| `openclaw/SKILL.md` | Skill | 50 | Missing frontmatter name+description (-50) |
| `CLAUDE.md` | Context | 98 | "relevant" vague quantifier (-2) |
| `plugin/skills/version-bump/SKILL.md` | Skill | 100 | None |
| `plugin/skills/do/SKILL.md` | Skill | 100 | None |
| `plugin/skills/smart-explore/SKILL.md` | Skill | 100 | None |
| `plugin/skills/make-plan/SKILL.md` | Skill | 100 | None |
| `plugin/skills/mem-search/SKILL.md` | Skill | 100 | None |
| `plugin/skills/timeline-report/SKILL.md` | Skill | 100 | None |
| `plugin/hooks/hooks.json` | Hook Config | 100 | None |
| `ragtime/CLAUDE.md` | Context | 100 | None |
| `plugin/scripts/CLAUDE.md` | Context | 100 | None |
| `plugin/hooks/CLAUDE.md` | Context | 100 | None |
| `plugin/CLAUDE.md` | Context | 100 | None |
| `plugin/ui/CLAUDE.md` | Context | 100 | None |
| `plugin/.claude-plugin/CLAUDE.md` | Context | 100 | None |
| `scripts/anti-pattern-test/CLAUDE.md` | Context | 100 | None |
| `scripts/CLAUDE.md` | Context | 100 | None |
| `.claude/skills/CLAUDE.md` | Context | 100 | None |
| `tests/infrastructure/CLAUDE.md` | Context | 100 | None |
| `tests/CLAUDE.md` | Context | 100 | None |
| `tests/utils/CLAUDE.md` | Context | 100 | None |
| `src/cli/handlers/CLAUDE.md` | Context | 100 | None |
| `src/cli/CLAUDE.md` | Context | 100 | None |
| `src/cli/adapters/CLAUDE.md` | Context | 100 | None |
| `src/shared/CLAUDE.md` | Context | 100 | None |
| `src/CLAUDE.md` | Context | 100 | None |
| `src/utils/CLAUDE.md` | Context | 100 | None |
| `src/services/infrastructure/CLAUDE.md` | Context | 100 | None |
| `src/services/worker/CLAUDE.md` | Context | 100 | None |
| `src/services/domain/CLAUDE.md` | Context | 100 | None |
| `src/services/CLAUDE.md` | Context | 100 | None |
| `src/services/sqlite/CLAUDE.md` | Context | 100 | None |
| `src/ui/viewer/constants/CLAUDE.md` | Context | 100 | None |
| `docs/CLAUDE.md` | Context | 100 | None |
| `docs/public/CLAUDE.md` | Context | 100 | None |
| `.claude-plugin/CLAUDE.md` | Context | 100 | None |
| `plugin/.claude-plugin/plugin.json` | Metadata | 100 | None |
| `.claude-plugin/plugin.json` | Metadata | 100 | Version mismatch with plugin/.claude-plugin/plugin.json |

**Weighted average**: (35 + 50 + 98 + 36×100) / 39 = 3783/39 = **97/100**

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 8 |
| High | 1 |
| Medium | 2 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hook configs | `plugin/hooks/hooks.json` |
| Scripts (JS) | `scripts/smart-install.js`, `scripts/build-hooks.js`, `scripts/build-worker-binary.js`, `scripts/discord-release-notify.js`, `scripts/generate-changelog.js`, `scripts/publish.js`, `scripts/analyze-transformations-smart.js`, `scripts/endless-mode-token-calculator.js`, `scripts/build-viewer.js` |
| Scripts (Shell) | `scripts/find-silent-failures.sh`, `scripts/sync-to-marketplace.sh` |
| Scripts (Python) | `scripts/extraction/extract-all-xml.py`, `scripts/extraction/filter-actual-xml.py` |
| MCP configs | `.mcp.json` (empty), `plugin/.mcp.json` (mcp-server.cjs) |
| Package manifest | `package.json` |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | CRITICAL | `openclaw/SKILL.md` | 9 | curl-pipe-sh | Skill's "Quick Install" instructs users to pipe curl output directly to bash (`curl -fsSL https://install.cmem.ai/openclaw.sh \| bash`). No checksum or signature verification. Domain compromise executes arbitrary code on user machines. |
| 2 | CRITICAL | `openclaw/SKILL.md` | 20 | curl-pipe-sh + API key in args | Same curl-pipe-sh with `--api-key=YOUR_KEY` passed as command-line argument. API keys in process args are visible to other processes via `/proc` and `ps`. |
| 3 | CRITICAL | `openclaw/SKILL.md` | 24 | curl-pipe-sh | Non-interactive variant of curl-pipe-sh install, same unverified remote execution risk. |
| 4 | CRITICAL | `openclaw/SKILL.md` | 28 | curl-pipe-sh | Upgrade variant of curl-pipe-sh install, same risk. |
| 5 | CRITICAL | `scripts/smart-install.js` | 163 | PowerShell IEX | Windows Bun install executes `powershell -c "irm bun.sh/install.ps1 \| iex"` — PowerShell Invoke-Expression on remote content; equivalent to curl-pipe-sh. Executed at plugin setup time via the Setup hook. |
| 6 | CRITICAL | `scripts/smart-install.js` | 169 | curl-pipe-sh (runtime) | Linux/macOS Bun auto-install executes `curl -fsSL https://bun.sh/install \| bash` via `execSync` at runtime during plugin setup. Runs whenever Bun is not found on the user's system. |
| 7 | CRITICAL | `scripts/smart-install.js` | 207 | PowerShell IEX + ExecutionPolicy Bypass | Windows uv install uses `powershell -ExecutionPolicy ByPass` to bypass system security policy, then executes remote script via IEX. Double security violation. |
| 8 | CRITICAL | `scripts/smart-install.js` | 213 | curl-pipe-sh (runtime) | Linux/macOS uv auto-install executes `curl -LsSf https://astral.sh/uv/install.sh \| sh` at runtime. Same unverified remote execution as finding #6. |
| 9 | HIGH | `scripts/generate-changelog.js` | 32 | Command injection | `release.tagName` from GitHub API is interpolated directly into shell command: `` exec(`gh release view ${release.tagName} --json body --jq '.body'`) ``. A maliciously crafted release tag (e.g., `; rm -rf ~`) would execute arbitrary shell commands. |
| 10 | MEDIUM | `package.json` | 111–149 | Unpinned dependencies | All production and dev dependencies use `^` (caret) semver ranges (e.g., `"express": "^4.18.2"`). Any minor/patch update to a dependency can introduce malicious code without explicit approval. |
| 11 | MEDIUM | `scripts/discord-release-notify.js` | 95 | External network call | Reads Discord webhook URL from `.env` file and POSTs release data. If `.env` is misconfigured or leaked, data is sent to an attacker-controlled endpoint. Low operational risk but worth noting. |
| 12 | LOW | `plugin/hooks/hooks.json` | 10 | Environment variable in hook command | Hook commands use `${CLAUDE_PLUGIN_ROOT}` shell variable expansion. Expected behavior for Claude Code plugins, but establishes an environment-variable dependency on untrusted shell expansion. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `.claude/commands/anti-pattern-czar.md` | Missing `name` field in frontmatter (no YAML block at all) | Command cannot be registered by Claude Code; breaks discovery |
| 2 | `.claude/commands/anti-pattern-czar.md` | Missing `description` field in frontmatter | Command missing searchable description; breaks marketplace listing |
| 3 | `openclaw/SKILL.md` | Missing `name` field in frontmatter (file begins with `#` heading, no YAML block) | Skill cannot be auto-loaded by name reference |
| 4 | `openclaw/SKILL.md` | Missing `description` field in frontmatter | Skill missing description; not discoverable |
| 5 | `.claude-plugin/plugin.json` vs `plugin/.claude-plugin/plugin.json` | Version mismatch: root plugin.json declares `10.4.1`, plugin/.claude-plugin/plugin.json declares `11.0.1` | Marketplace and local install show different versions; could cause failed or inconsistent installs |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `package.json` | All dependencies use `^` caret ranges allowing auto-upgrades | Pin all production dependencies to exact versions (remove `^`) and use a lockfile; audit upgrades explicitly via `npm update` + diff |
| 2 | `scripts/discord-release-notify.js` | Discord webhook URL read from `.env`; if misconfigured sends release info externally | Validate URL format before sending; add `DISCORD_UPDATES_WEBHOOK` to `.gitignore` docs/examples with a placeholder |
| 3 | `plugin/hooks/hooks.json` | Hook command relies on `${CLAUDE_PLUGIN_ROOT}` which must be set by caller | Document the expected env var, and add a fallback guard that exits with a clear error message if neither `CLAUDE_PLUGIN_ROOT` nor the default path exists |

*Note: Findings #1–8 (Critical) and Finding #9 (High) require private security disclosure, not public PRs.*

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `.claude/commands/anti-pattern-czar.md` | No `allowed-tools` declaration; command calls Bash and Read tools implicitly | -5 |
| 2 | `.claude/commands/anti-pattern-czar.md` | No empty input handling (no guidance on what to do if user invokes command with no context) | -10 |
| 3 | `CLAUDE.md` (root) | "inject **relevant** context into future sessions" — "relevant" is a vague quantifier | -2 |

## Cross-Component

**Version drift** is the primary cross-component issue:
- `package.json`: `11.0.1`
- `plugin/.claude-plugin/plugin.json`: `11.0.1`
- `.claude-plugin/plugin.json`: `10.4.1` ← stale

The root `.claude-plugin/plugin.json` is one major version behind. This is likely a forgotten sync step. The `version-bump/SKILL.md` skill explicitly lists updating all three config files, but this one was missed.

**Skill/hook reference integrity**: The MCP config at `plugin/.mcp.json` references `${CLAUDE_PLUGIN_ROOT}/scripts/mcp-server.cjs`. This compiled artifact is generated by `scripts/build-hooks.js`. The build script verifies `plugin/hooks/hooks.json` and key SKILL.md files exist but does not verify `mcp-server.cjs` presence. If a build fails mid-way, the MCP config references a missing file.

**openclaw/SKILL.md vs plugin skills**: The six skills in `plugin/skills/` all have proper YAML frontmatter. `openclaw/SKILL.md` sits outside that directory and has none — it was likely written as documentation and not converted to a proper skill file when promoted to `SKILL.md`.

**anti-pattern-czar.md isolation**: The command references `scripts/anti-pattern-test/detect-error-handling-antipatterns.ts` in its first step. This file path is hardcoded in the command body. No cross-reference validation; if the script is renamed or moved the command silently breaks.

## Recommendation

**BLOCKED — do not submit PRs. File private security report.**

Eight critical-severity findings exist in `openclaw/SKILL.md` and `scripts/smart-install.js`. The smart-install.js findings are the most severe: this file executes curl-pipe-shell and PowerShell IEX at plugin setup time (triggered by the Setup hook in `plugin/hooks/hooks.json`) on every user machine where Bun or uv is not already installed. A compromise of `bun.sh`, `astral.sh`, or the CDN delivering `install.cmem.ai/openclaw.sh` would result in arbitrary code execution on all installing users.

**Immediate actions needed (private disclosure):**
1. Replace `curl | bash` Bun install in `smart-install.js` with a verified binary download (checksum + GPG signature) or direct users to install Bun via their system package manager
2. Same for uv auto-install
3. Replace `install.cmem.ai/openclaw.sh | bash` recommendation in `openclaw/SKILL.md` with a signed installer or documented manual steps
4. Fix command injection in `generate-changelog.js:32` by shell-quoting `release.tagName` or using `execSync` with an argv array instead of a shell string

**NL fix PRs (safe to open after security issues are resolved):**
- Add YAML frontmatter to `.claude/commands/anti-pattern-czar.md`
- Add YAML frontmatter to `openclaw/SKILL.md`
- Sync `.claude-plugin/plugin.json` version to match `plugin/.claude-plugin/plugin.json`
