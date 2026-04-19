# NLPM Audit: superset-sh/superset
**Date**: 2026-04-19  |  **Artifacts**: 13  |  **Strategy**: single
**NL Score**: 64/100
**Security**: BLOCKED
**Bugs**: 11  |  **Quality Issues**: 10  |  **Security Findings**: 9

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .agents/commands/create-plan.md | command | 15 | No frontmatter at all (name, description, allowed-tools missing); vague quantifier cap hit |
| .agents/commands/create-pr.md | command | 25 | No frontmatter at all (name, description, allowed-tools missing); vague quantifier cap hit |
| .agents/commands/task.md | command | 63 | Missing `name`; no empty-input handling for required Description arg |
| .agents/commands/task-run.md | command | 63 | Missing `name`; no empty-input handling for required Description arg |
| .agents/commands/deslop.md | command | 63 | Missing `name`; no output format section |
| .agents/commands/respond-to-pr-comments.md | command | 63 | Missing `name`; no output format section |
| .agents/commands/clean-neon-branches.md | command | 65 | Missing `name`; no explicit output format section |
| .agents/commands/refresh-compare-pages.md | command | 69 | Missing `name`; vague quantifiers ("obviously", "relevant", "concise") |
| .agents/commands/ci-check.md | command | 75 | Missing `name` frontmatter |
| .claude/agents/project-structure-validator.md | agent | 80 | Missing `model` declaration; zero example interaction blocks |
| CLAUDE.md | context | 85 | Single-line `@AGENTS.md` import only; no direct guidance |
| apps/desktop/CLAUDE.md | context | 85 | Single-line `@AGENTS.md` import only |
| apps/mobile/CLAUDE.md | context | 85 | Single-line `@AGENTS.md` import only |

**Weighted average**: (15+25+63+63+63+63+65+69+75+80+85+85+85) / 13 = **64/100**

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 3 |
| Medium | 3 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts (.sh) | 21 (scripts/, .superset/lib/, apps/desktop/create-release.sh, apps/marketing/public/cli/install.sh, apps/desktop/src/.../templates/*.template.sh) |
| Script templates (.js) | 7 (opencode-plugin.template.js, browser-extension/*.js, babel.config.js, metro.config.js, index.js) |
| MCP configs | 0 |
| Package manifests | package.json (root), apps/docs/package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | CRITICAL | apps/marketing/public/cli/install.sh | 6 | curl-pipe-sh | Script is designed for `curl -fsSL https://superset.sh/cli/install.sh \| sh` execution. No checksum or signature verification on downloaded tarballs from GitHub releases; a compromised CDN or MITM could execute arbitrary code on installation. |
| 2 | HIGH | apps/marketing/public/cli/install.sh | 110–125 | PATH modification | Writes `export PATH="$bin_dir:\$PATH"` to user shell profiles (~/.zshrc, ~/.bashrc, ~/.bash_profile, ~/.config/fish/config.fish). Path value is derived from `$INSTALL_DIR` which defaults to `$SUPERSET_HOME` or `$HOME/superset`; an attacker controlling `SUPERSET_HOME` could inject a path containing a malicious binary. |
| 3 | HIGH | package.json | 33 | postinstall script | `"postinstall": "./scripts/postinstall.sh"` — runs a shell script automatically on every `bun install`. The script invokes `sherif`, then `electron-builder install-app-deps` (native rebuild), which spawns nested Bun installs. Any compromise of the install chain would silently execute on developer machines. |
| 4 | HIGH | apps/docs/package.json | 11 | postinstall script | `"postinstall": "fumadocs-mdx"` — executes a third-party npm package in a postinstall hook. Package compromise would execute arbitrary code on every install with no prompt. |
| 5 | MEDIUM | .superset/lib/setup/steps.sh | 113 | jq injection | `jq -r ".[] | select(.name == \"$WORKSPACE_NAME\") | .id // empty"` — `$WORKSPACE_NAME` is interpolated directly into the jq filter string via double-quoting. A workspace name containing jq metacharacters (e.g., `") | @sh |`) could break out of the string context and execute injected jq expressions. |
| 6 | MEDIUM | .superset/lib/setup/steps.sh | 18 | source untrusted path | `source "$SUPERSET_ROOT_PATH/.env"` — sources an .env file from an externally supplied path without validating that the path is within expected bounds. A symlink or injected path could cause arbitrary shell code in a crafted .env to execute. |
| 7 | MEDIUM | apps/desktop/src/main/lib/agent-setup/templates/{copilot,cursor,notify,gemini}-hook.template.sh | various | network calls with env vars | All four hook templates call `curl -sG "http://127.0.0.1:${SUPERSET_PORT}/hook/complete"` with `$SUPERSET_TAB_ID`, `$SUPERSET_PANE_ID`, `$SUPERSET_WORKSPACE_ID`, and `$SUPERSET_ENV` passed as query parameters via `--data-urlencode`. If any of these env vars were poisoned, they could exfiltrate data or cause unexpected server-side behavior, though the target is localhost. |
| 8 | LOW | package.json | 9 | unpinned dependency | `"dotenv-cli": "^11.0.0"` — semver caret allows automatic minor and patch upgrades, introducing supply-chain risk on fresh installs. |
| 9 | LOW | package.json | 11 | unpinned dependency | `"sherif": "^1.10.0"` — same semver caret issue; sherif runs in postinstall on every developer install. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .agents/commands/ci-check.md | Missing `name` frontmatter field | Command identity incomplete; may not register correctly in tooling that requires explicit name |
| 2 | .agents/commands/clean-neon-branches.md | Missing `name` frontmatter field | Same as above |
| 3 | .agents/commands/create-plan.md | No frontmatter block at all — `name`, `description`, and `allowed-tools` all absent | Command not discoverable; no tool permissions declared; model cannot enforce tool constraints |
| 4 | .agents/commands/create-pr.md | No frontmatter block — `name`, `description`, and `allowed-tools` all absent | Same triple missing; this command actively uses Bash and git operations but declares no tools |
| 5 | .agents/commands/deslop.md | Missing `name` frontmatter field | Registration incomplete |
| 6 | .agents/commands/refresh-compare-pages.md | Missing `name` frontmatter field | Registration incomplete |
| 7 | .agents/commands/respond-to-pr-comments.md | Missing `name` frontmatter field | Registration incomplete |
| 8 | .agents/commands/task-run.md | Missing `name` frontmatter field | Registration incomplete |
| 9 | .agents/commands/task.md | Missing `name` frontmatter field | Registration incomplete |
| 10 | .agents/commands/create-plan.md | Missing `description` frontmatter | Command absent from `/help` output; not discoverable by users |
| 11 | .agents/commands/create-pr.md | Missing `description` frontmatter | Same — a heavily-used workflow command with no discoverable description |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | .superset/lib/setup/steps.sh | Line 113: `$WORKSPACE_NAME` interpolated into jq filter | Use `jq --arg name "$WORKSPACE_NAME" '.[] | select(.name == $arg) | .id // empty'` — the `--arg` form safely escapes the value |
| 2 | package.json | `dotenv-cli: "^11.0.0"` unpinned | Pin to exact version: `"dotenv-cli": "11.0.0"` (or current latest) |
| 3 | package.json | `sherif: "^1.10.0"` unpinned (runs in postinstall) | Pin to exact version: `"sherif": "1.10.0"` — especially important for a postinstall-executed tool |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/agents/project-structure-validator.md | No `model` declaration | -5 |
| 2 | .claude/agents/project-structure-validator.md | Zero example interaction blocks | -15 |
| 3 | .agents/commands/clean-neon-branches.md | No explicit `## Output` section; step 8 says "Report results" but no format specified | -10 |
| 4 | .agents/commands/deslop.md | No `## Output` section; no indication of what the final output looks like | -10 |
| 5 | .agents/commands/respond-to-pr-comments.md | No `## Output` section; step 3 ends with an inline summary note | -10 |
| 6 | .agents/commands/task.md | `Description` is a required argument but no empty-input handling ("If no arguments provided, ask…") | -10 |
| 7 | .agents/commands/task-run.md | Same — `Description` required, no empty-input guard | -10 |
| 8 | .agents/commands/create-plan.md | Vague quantifiers throughout the body: "appropriate location", "thorough", "relevant", "necessary", etc. — cap reached | -20 |
| 9 | .agents/commands/create-pr.md | Vague quantifiers: "meaningful risk" (×3), "appropriate" (×3), "relevant" (×2), "brief", "concise" — cap reached | -20 |
| 10 | .agents/commands/refresh-compare-pages.md | Vague quantifiers: "obviously stale", "relevant", "concise summary" | -6 |

## Cross-Component
- All three `CLAUDE.md` files (root, apps/desktop, apps/mobile) consist solely of `@AGENTS.md` — a valid import directive. They delegate entirely to sibling `AGENTS.md` files, which exist and contain comprehensive guidance. No broken references.
- `refresh-compare-pages.md` references `.agents/commands/create-pr.md` at line 76 — file exists ✓.
- `create-plan.md` references `AGENTS.md` (root) multiple times — file exists ✓.
- `project-structure-validator.md` references `AGENTS.md` for rules — file exists ✓.
- No orphaned components or circular references detected.
- **Pattern inconsistency**: 9 of 9 commands are missing `name` in frontmatter, suggesting a convention gap rather than individual oversights. The project may not use `name` in command frontmatter intentionally (Claude Code resolves command names from filenames). However, the scoring rubric flags these as bugs.
- `create-plan.md` and `create-pr.md` are substantive workflow documents that grew into long reference guides; they lack frontmatter entirely, making them structural outliers among the commands.

## Recommendation

**BLOCKED — do not submit PRs. File private security report.**

The CRITICAL finding (`apps/marketing/public/cli/install.sh` designed for `curl | sh` with no tarball integrity verification) and three HIGH findings (PATH modification, two postinstall hooks) require private disclosure to the maintainers before any NL fix PRs are submitted.

**After the security gate clears:**
- Submit NL bug PRs adding `name` frontmatter to all 9 commands, and full frontmatter to `create-plan.md` and `create-pr.md`.
- Submit Medium/Low security fix PRs: jq injection fix in `setup/steps.sh` and dependency pinning in `package.json`.
- Quality improvements (examples for `project-structure-validator.md`, output format sections, empty-input guards) are lower priority but straightforward.
