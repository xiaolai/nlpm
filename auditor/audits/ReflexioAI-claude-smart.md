# NLPM Audit: ReflexioAI/claude-smart
**Date**: 2026-04-06  |  **Artifacts**: 32  |  **Strategy**: batched
**NL Score**: 92/100
**Security**: REVIEW
**Bugs**: 6  |  **Quality Issues**: 14  |  **Security Findings**: 4

> Note: The 32-artifact list contains 6 duplicate paths (the 6 `.claude/commands/` files appear twice). Scoring covers 26 unique artifacts. The `.agents/skills/` directory contains separate copies of the `.claude/skills/` files (not symlinks), and the two copies of `sync-agent-instructions` have diverged.

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `plugin/commands/restart.md` | command | 75 | Missing `name` frontmatter |
| `plugin/commands/learn.md` | command | 75 | Missing `name` frontmatter |
| `plugin/commands/clear-all.md` | command | 75 | Missing `name` frontmatter |
| `plugin/commands/show.md` | command | 75 | Missing `name` frontmatter |
| `plugin/commands/dashboard.md` | command | 75 | Missing `name` frontmatter |
| `.claude/commands/commit/SKILL.md` | command | 83 | No allowed-tools + no empty-input handling + vague "relevant" |
| `.agents/skills/sync-agent-instructions/SKILL.md` | skill | 90 | Broken filenames (CLAUDE.md replaced by AGENTS.md in step 1 and description) |
| `plugin/hooks/hooks.json` | hook config | 90 | Executable artifact; scant prose context |
| `plugin/.claude-plugin/plugin.json` | manifest | 90 | Does not enumerate skills/commands/hooks |
| `.claude/commands/review/SKILL.md` | command | 91 | No allowed-tools; vague "appropriate", "actionable" |
| `.claude/commands/create-pr/SKILL.md` | command | 93 | No allowed-tools; vague "relevant" |
| `.claude/commands/update-pr/SKILL.md` | command | 93 | No allowed-tools; vague "relevant" |
| `.claude/commands/check-and-test/SKILL.md` | command | 95 | No allowed-tools |
| `.claude/commands/run-services/SKILL.md` | command | 95 | No allowed-tools |
| `.agents/skills/prd/SKILL.md` | skill | 98 | Vague "suitable" in opening description |
| `.claude/skills/prd/SKILL.md` | skill | 98 | Vague "suitable" in opening description |
| `.agents/skills/agent-browser/SKILL.md` | skill | 100 | Clean |
| `.agents/skills/update-public-docs/SKILL.md` | skill | 100 | Clean |
| `.agents/skills/fastapi/SKILL.md` | skill | 100 | Clean |
| `.agents/skills/ralph/SKILL.md` | skill | 100 | Clean |
| `.claude/skills/sync-agent-instructions/SKILL.md` | skill | 100 | Clean |
| `.claude/skills/agent-browser/SKILL.md` | skill | 100 | Clean |
| `.claude/skills/update-public-docs/SKILL.md` | skill | 100 | Clean |
| `.claude/skills/fastapi/SKILL.md` | skill | 100 | Clean |
| `.claude/skills/ralph/SKILL.md` | skill | 100 | Clean |
| `plugin/skills/claude-smart/SKILL.md` | skill | 100 | Clean |

**Weighted average**: 2391 / 26 = **92/100**

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 confirmed (2 pre-scan unverified — see note) |
| High | 0 |
| Medium | 1 |
| Low | 3 |

> **Pre-scan note**: The automated pre-scan reported 2 critical-pattern matches across 83 script files. My detailed scan covered the 5 files in `scripts/` plus `plugin/hooks/hooks.json` and `plugin/hooks/codex-hooks.json`. The 83-file count indicates a large script surface in `plugin/scripts/` and `bin/` that was outside the explicit Glob scope (`target-repo/scripts/**/*.{sh,py,js}`). The 2 critical matches are likely in those uninspected files. **Manual review of `plugin/scripts/` and `bin/claude-smart.js` is required before clearing this audit.**

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks (Claude Code) | `plugin/hooks/hooks.json` |
| Hooks (Codex) | `plugin/hooks/codex-hooks.json` |
| Python scripts | `scripts/check-reflexio-lock.py`, `scripts/sync-reflexio-dep.py`, `scripts/vendor-reflexio.py` |
| Bash scripts | `scripts/setup-claude-smart.sh`, `scripts/release-with-reflexio.sh` |
| MCP configs | None found |
| Package manifests | `package.json` (no postinstall) |
| Uninspected (pre-scan scope) | `plugin/scripts/` (~78 files), `bin/claude-smart.js` |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | `scripts/sync-reflexio-dep.py` | 77 | SEC-network-request | `urllib.request.urlopen` to external PyPI URL; URL is hardcoded but function is callable with user-supplied version strings at runtime |
| 2 | Low | `scripts/vendor-reflexio.py` | 138 | SEC-path-traversal | `tar.extractall(vendor_dest)` without a member filter; mitigated in practice because the tarball is produced by `git archive` on a local trusted repo |
| 3 | Low | `scripts/setup-claude-smart.sh` | 103–107 | SEC-credential-storage | API key collected interactively and appended to `~/.reflexio/.env` in plaintext; mitigated by `chmod 600` immediately after write |
| 4 | Low | `plugin/hooks/codex-hooks.json` | 9 | SEC-dynamic-source | Plugin root discovered via `ls -dt ... \| head -n 1` and the resulting path is `source`d (`. "${_R%/}/scripts/_codex_env.sh"`); if the plugin cache directory were writable by an attacker, arbitrary scripts could execute |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `.agents/skills/sync-agent-instructions/SKILL.md` | Description frontmatter and Step 1 both list `AGENTS.md` twice; `CLAUDE.md` is absent. The `git diff` command will never detect changes to `CLAUDE.md`. | Skill silently fails to sync CLAUDE.md; the `.claude/skills/` copy is correct and unaffected |
| 2 | `plugin/commands/restart.md` | Missing required `name` frontmatter field | Command may not be registered with a predictable slash-command name |
| 3 | `plugin/commands/learn.md` | Missing required `name` frontmatter field | Command may not be registered with a predictable slash-command name |
| 4 | `plugin/commands/clear-all.md` | Missing required `name` frontmatter field | Command may not be registered with a predictable slash-command name |
| 5 | `plugin/commands/show.md` | Missing required `name` frontmatter field | Command may not be registered with a predictable slash-command name |
| 6 | `plugin/commands/dashboard.md` | Missing required `name` frontmatter field | Command may not be registered with a predictable slash-command name |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `scripts/vendor-reflexio.py` | `tar.extractall()` without member filter (Python 3.12 deprecation warning; theoretical path-traversal via crafted archive) | Add `tar.extractall(vendor_dest, filter='data')` (Python ≥3.12) or validate each member path before extraction |
| 2 | `scripts/sync-reflexio-dep.py` | Outbound network call at import-level concern; timeout is fixed at 15s | Add user-visible logging before the request; document that this function requires network access |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `.claude/commands/create-pr/SKILL.md` | No `allowed-tools` declared | -5 |
| 2 | `.claude/commands/create-pr/SKILL.md` | Vague quantifier: "relevant modified/untracked files" (Step 2) | -2 |
| 3 | `.claude/commands/update-pr/SKILL.md` | No `allowed-tools` declared | -5 |
| 4 | `.claude/commands/update-pr/SKILL.md` | Vague quantifier: "links to relevant issues/docs" (Step 4 guidelines) | -2 |
| 5 | `.claude/commands/check-and-test/SKILL.md` | No `allowed-tools` declared | -5 |
| 6 | `.claude/commands/review/SKILL.md` | No `allowed-tools` declared | -5 |
| 7 | `.claude/commands/review/SKILL.md` | Vague quantifier: "only report findings that are actionable" | -2 |
| 8 | `.claude/commands/review/SKILL.md` | Vague quantifier: "Is retry logic appropriate and bounded?" (3.5) | -2 |
| 9 | `.claude/commands/commit/SKILL.md` | No `allowed-tools` declared | -5 |
| 10 | `.claude/commands/commit/SKILL.md` | No explicit empty-input handling: does not say what to do if there is nothing to commit | -10 |
| 11 | `.claude/commands/commit/SKILL.md` | Vague quantifier: "relevant untracked/modified files" (Step 3) | -2 |
| 12 | `.claude/commands/run-services/SKILL.md` | No `allowed-tools` declared | -5 |
| 13 | `.agents/skills/prd/SKILL.md` | Vague quantifier: "suitable for implementation" (opening description) | -2 |
| 14 | `.claude/skills/prd/SKILL.md` | Vague quantifier: "suitable for implementation" (opening description) | -2 |

## Cross-Component
**CC-1 — `.agents/skills/` copies have diverged from `.claude/skills/`**
Per `AGENTS.md`, `.agents/skills/` is documented as a symlink to `.claude/skills/`. In this repo they are separate file copies. Five of the six skill pairs are byte-identical (`agent-browser`, `prd`, `update-public-docs`, `fastapi`, `ralph`). However, `sync-agent-instructions` has diverged: the `.agents/skills/` copy contains the `AGENTS.md`/`AGENTS.md` bug (Bug #1 above) while the `.claude/skills/` copy is correct. If these are ever converted to real symlinks the correct version will win, but until then the divergence is a maintenance risk.

**CC-2 — `plugin.json` does not enumerate hooks, skills, or commands**
`plugin/.claude-plugin/plugin.json` contains only name/version/description/author/keywords. There is no reference to `plugin/hooks/hooks.json`, the `plugin/commands/` command files, or the `plugin/skills/` skill. Claude Code may auto-discover these by convention, but the manifest provides no explicit cross-references for tooling validation.

**CC-3 — Audit target list contained 6 duplicate paths**
The 6 `.claude/commands/` files were listed twice (positions 1–6 and 18–23 in the audit task). This inflated the stated artifact count from 26 unique files to 32. Scoring uses 26.

## Recommendation
REVIEW — submit PRs for the 6 NL bugs (missing `name` frontmatter in plugin/commands/ and the `CLAUDE.md`→`AGENTS.md` error in `.agents/skills/sync-agent-instructions/SKILL.md`). The Low/Medium security fixes are safe to PR as well.

**Before contributing any PRs**: manually inspect `plugin/scripts/` and `bin/claude-smart.js` to resolve the 2 pre-scan critical-pattern matches. If those hits are confirmed as true positives (e.g., `curl | bash` in `smart-install.sh`), escalate to private security disclosure instead of opening a public PR and upgrade this verdict to BLOCKED.
