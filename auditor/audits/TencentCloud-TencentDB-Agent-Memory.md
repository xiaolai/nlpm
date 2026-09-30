# NLPM Audit: TencentCloud/TencentDB-Agent-Memory
**Date**: 2026-04-06  |  **Artifacts**: 20  |  **Strategy**: single
**NL Score**: 91/100
**Security**: BLOCKED
**Bugs**: 1  |  **Quality Issues**: 5  |  **Security Findings**: 10

## NL Score Summary
Only `MemoryCore/SKILL.md` and `agents/skills/setup-proxy/SKILL.md` are registrable NL artifacts (skills). The other 18 files are plain README/how-to documents with no frontmatter and are scored as documentation, not as agents or commands. `agents/skills/setup-proxy/SKILL.md` appeared twice in the input list, so there are 19 unique files.

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/skills/setup-proxy/SKILL.md | skill | 88 | No output format or empty-input handling; `triggers` is not a standard skill key |
| agents/adapter-agent-development.md | doc | 90 | Vague quantifiers ("常见", "相关"); no frontmatter (plain doc) |
| agents/README.md | doc | 90 | Says "7 类" agents, but `agents/opencode/` also exists and is not in the table |
| agents/opencode/README.md | doc | 90 | No `asset-import.md` sibling and not listed in `agents/README.md` |
| agents/dsh/README.md | doc | 92 | Plain doc, no frontmatter |
| agents/claude-code/README.md | doc | 92 | Plain doc, no frontmatter |
| agents/codebuddy/README.md | doc | 92 | Plain doc, no frontmatter |
| agents/codex/README.md | doc | 92 | Plain doc, no frontmatter |
| agents/hermes/README.md | doc | 92 | Plain doc, no frontmatter |
| agents/openclaw/README.md | doc | 92 | Plain doc, no frontmatter |
| agents/workbuddy/README.md | doc | 92 | Plain doc, no frontmatter |
| agents/claude-code/asset-import.md | doc | 93 | Plain doc, no frontmatter |
| agents/codebuddy/asset-import.md | doc | 93 | Plain doc, no frontmatter |
| agents/codex/asset-import.md | doc | 93 | Plain doc, no frontmatter |
| agents/dsh/asset-import.md | doc | 93 | Plain doc, no frontmatter |
| agents/hermes/asset-import.md | doc | 93 | Plain doc, no frontmatter |
| agents/openclaw/asset-import.md | doc | 93 | Plain doc, no frontmatter |
| agents/workbuddy/asset-import.md | doc | 93 | Plain doc, no frontmatter |
| MemoryCore/SKILL.md | skill | 94 | `name` (openclaw-memory-tencentdb-setup) does not match directory (MemoryCore) |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 7 |
| High | 3 |
| Medium | 0 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none |
| MCP configs | none |
| Shell scripts (repo) | `agents/setup-proxy.sh`, `agents/skills/setup-proxy/setup-proxy.sh`, `MemoryCore/scripts/install-hermes-plugin.sh`, `MemoryCore/scripts/install_hermes_memory_tencentdb.sh`, `MemoryCore/scripts/install-openclaw-plugin.sh`, `MemoryProxy/scripts/proxy.sh`, `MemoryProxy/scripts/setup-claude-code.sh`, `deploy/**/*.sh`, `MemoryKnowledge/docker/*.sh`, `MemoryPanel/scripts/*.sh` (~55 script files in total, including the Python ones) |
| Python scripts | `MemoryCore/scripts/import-opik-to-memory-skill-py/import_opik.py`, `MemoryCore/scripts/migrate-v2-to-v3/v2-to-v3-migrate.py`, `MemoryProxy/scripts/qa/*.py`, `MemoryCore/hermes-plugin/**`, `sdk/memory-core/python/**` |
| Package manifests | `MemoryCore/package.json` (has `postinstall`), `MemoryCore/openclaw-plugin/package.json`, `MemoryCore/pi-plugin/package.json`, `MemoryPanel/package.json`, `MemoryPanel/web/package.json`, `MemoryKnowledge/package.json`, `MemoryProxy/package.json`, `sdk/memory-core/typescript/package.json` |

I did not read every one of the ~55 scripts line by line. I pattern-searched all of them and read the flagged sites.

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | MemoryCore/scripts/install-openclaw-plugin.sh | 247 | curl-pipe-sh | `curl -fsSL https://get.openclaw.dev \| bash`, run when `INSTALL_OPENCLAW=1`. It is opt-in and uses HTTPS, but there is no checksum or pin. |
| 2 | Critical | MemoryCore/scripts/install-hermes-plugin.sh | 11 | eval-variable | `eval echo "~$USERNAME"`. `USERNAME` comes from `INSTALL_AS_USER` or `SUDO_USER`, so a crafted value runs arbitrary commands. Often runs as root. |
| 3 | Critical | MemoryCore/scripts/install_hermes_memory_tencentdb.sh | 47 | eval-variable | `eval echo ~$USERNAME`, same issue with unquoted input. |
| 4 | Critical | agents/setup-proxy.sh | 27 | eval-variable | `prompt_input` runs `eval "$varname=\"${val:-$default}\""` on interactive input. `$(...)` or backticks in the answer are executed. |
| 5 | Critical | agents/setup-proxy.sh | 31 | eval-variable | `eval "$varname=\"$val\""` on user-typed input, same issue. |
| 6 | Critical | agents/skills/setup-proxy/setup-proxy.sh | 27 | eval-variable | Duplicate of #4 in the skill copy. |
| 7 | Critical | agents/skills/setup-proxy/setup-proxy.sh | 31 | eval-variable | Duplicate of #5 in the skill copy. |
| 8 | High | MemoryCore/scripts/install_hermes_memory_tencentdb.sh | 271 | sudo / write outside repo | `sudo tee /etc/profile.d/memory-tencentdb-env.sh` writes a system-wide profile script that is sourced by every login shell. `GATEWAY_CMD` is interpolated unescaped. |
| 9 | High | MemoryCore/package.json | 48 | postinstall-script | `postinstall` runs `bash scripts/openclaw-after-tool-call-messages.patch.sh 2>/dev/null \|\| true`. The script is not in the repo (see Bug #1), and the error suppression hides that. If a file with this name is ever added, it runs on every consumer's install. |
| 10 | High | MemoryProxy/scripts/proxy.sh | 47 | eval-variable | `eval "$(fnm env)"` executes the output of an external binary found on PATH. This is the common fnm idiom, so it is low-risk in practice. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | MemoryCore/package.json | `postinstall` (line 48) and the `files` array (line 66) reference `scripts/openclaw-after-tool-call-messages.patch.sh`, but `MemoryCore/scripts/` has no such file. | The script never runs and `2>/dev/null \|\| true` hides the failure. The published package's `files` entry matches nothing. |

Bug #1 touches an executable-surface file and is also security finding #9, so it stays under the BLOCKED recommendation.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| – | – | No Medium/Low findings. | – |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/skills/setup-proxy/SKILL.md | No output format or completion criteria; no handling for empty input or an unknown agent name. | -10 |
| 2 | agents/skills/setup-proxy/SKILL.md | Non-standard `triggers:` frontmatter key. It is not in the SKILL.md spec, so `description` should carry the trigger phrases. | -2 |
| 3 | MemoryCore/SKILL.md | Frontmatter `name` is `openclaw-memory-tencentdb-setup` but the directory is `MemoryCore/`. It also sits at the package root next to a large codebase rather than in a skills directory. | -6 |
| 4 | agents/README.md | Says 7 agent clients but `agents/opencode/` exists and is not in the table. | -2 |
| 5 | agents/adapter-agent-development.md | Vague quantifiers ("常见", "相关") in the checklist prose. | -10 |

## Cross-Component
| # | File | Issue |
|---|------|-------|
| 1 | agents/README.md | The "7 类" count and client table omit OpenCode, which has `agents/opencode/README.md` (no `asset-import.md`) and an `adapters/opencode/` directory. |
| 2 | agents/setup-proxy.sh vs agents/skills/setup-proxy/setup-proxy.sh | The two scripts are duplicated, so the eval fix has to be applied twice. Symlink or dedupe them. |
| 3 | agents/skills/setup-proxy/SKILL.md | The skill's table covers 4 of the 7 agents listed in its intro (claude-code, codebuddy, codex, workbuddy). It omits dsh, Hermes and OpenClaw, which the intro names. |

All relative markdown links in `agents/**` and `MemoryCore/SKILL.md` resolve.

## Recommendation
BLOCKED — do not submit PRs. File private security report.

Critical findings: unsanitised `eval` on user or environment input in 4 script files, and an opt-in `curl | bash` installer. The `postinstall` script reference is also broken. Critical and High findings go to a private report. The NL quality and cross-component issues can be raised after that is resolved.
