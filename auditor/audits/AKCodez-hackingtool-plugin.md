# NLPM Audit: AKCodez/hackingtool-plugin
**Date**: 2026-04-06  |  **Artifacts**: 2  |  **Strategy**: single
**NL Score**: 88/100
**Security**: BLOCKED
**Bugs**: 1  |  **Quality Issues**: 0  |  **Security Findings**: 5

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| plugins/hackingtool/.claude-plugin/plugin.json | plugin manifest | 75 | Missing `skills` array — pentest skill on disk is unregistered |
| plugins/hackingtool/skills/pentest/SKILL.md | skill | 100 | Clean — no penalties |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 |
| Medium | 2 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Scripts | `plugins/hackingtool/scripts/ht_run.py`, `ht_env.py`, `ht_preflight.py`, `ht_search.py`, `ht_index.py`, `build_readme_table.py` |
| Hooks | none |
| MCP configs | none |
| Package manifests | none |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | `scripts/ht_run.py` | 204–216, 347–348 | `bash-lc-string-concat` | `run_native` and `run_wsl` pass a concatenated command string (`cmds[0] + " " + args.args`) directly to `bash -lc`; user-supplied `--args` (e.g., target hostnames) land in that string unquoted, enabling shell injection via embedded metacharacters |
| 2 | High | `scripts/ht_run.py` | 204, 210, 386–407 | `sudo-auto-escalation` | On any `permission_denied` error, the runner automatically retries the full command with `sudo -n` without explicit per-invocation user consent; a tool that fails due to unrelated issues could escalate privileges silently |
| 3 | Medium | `scripts/ht_run.py` | 379 | `arbitrary-docker-image` | `--docker-image` argument is accepted and written directly into the image override map with no allowlist check; an attacker-controlled image name could execute a malicious container |
| 4 | Medium | `scripts/ht_preflight.py` | 44–48 | `external-network-call` | Preflight makes an outbound `socket.create_connection(("1.1.1.1", 443), timeout=3)` on every session start; the target IP is hardcoded and the connection is undisclosed to the user |
| 5 | Low | `scripts/ht_index.py` | 302 | `file-write-user-path` | `--output` argument allows writing `tools.json` to any filesystem path without boundary validation; risk is low because `ht_index.py` is a developer/build tool not called by the skill at runtime |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `plugins/hackingtool/.claude-plugin/plugin.json` | No `skills` array declared; `skills/pentest/SKILL.md` exists on disk but is not registered in the manifest | Claude Code cannot auto-load the pentest skill when the plugin is installed; the plugin installs silently but provides no skill to agents |

## Security Fixes (PR-worthy, Medium/Low only)
> **Hold**: Do not open PRs until the two HIGH findings above are addressed via private disclosure.
> The fixes below are ready once the security review clears.

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `scripts/ht_run.py` | `--docker-image` accepts arbitrary image names | Validate against `DOCKER_IMAGE_OVERRIDES` values or require an explicit allowlist flag |
| 2 | `scripts/ht_preflight.py` | Hardcoded external IP for internet check | Make the connectivity target configurable or document the outbound connection in the plugin README |
| 3 | `scripts/ht_index.py` | `--output` path unconstrained | Validate that `--output` resolves within the plugin directory tree |

## Quality Issues (informational)
No quality issues found. Both artifacts are well-structured; SKILL.md has complete frontmatter, a numbered golden path, concrete code examples, and valid cross-references to on-disk files.

## Cross-Component
- **Unregistered skill**: `plugin.json` declares no `skills` array, but `skills/pentest/SKILL.md` is present on disk. The Claude Code plugin loader will not auto-discover or surface this skill without an explicit registration entry. This is the root cause of Bug #1 and is also reflected in the 25-point deduction on the plugin.json score.
- **References valid**: All `${CLAUDE_PLUGIN_ROOT}`-relative paths in `SKILL.md` resolve to existing files (`scripts/ht_preflight.py`, `scripts/ht_search.py`, `scripts/ht_run.py`, `skills/pentest/reference/workflows.md`, `skills/pentest/reference/runtime-fallbacks.md`).
- **Homepage drift**: `plugin.json` `homepage` points to `https://github.com/Z4nzu/hackingtool` (the upstream tool repo), not the plugin repo itself. Advisory only — no penalty, but may confuse installers looking for plugin-specific docs.

## Recommendation
BLOCKED — do not submit PRs. File private security report.

Two HIGH security findings require private disclosure before any public contribution:
1. **Shell injection via `bash -lc` + `--args`** (`ht_run.py` lines 204–216, 347–348): user-supplied target data flows into an unquoted shell command string. Mitigation: apply `shlex.quote()` to each user-supplied argument, or validate that `--args` contains no shell metacharacters before interpolation.
2. **Automatic `sudo` escalation** (`ht_run.py` lines 204, 210, 386–407): permission errors trigger an unconditional `sudo -n` retry. Mitigation: gate auto-escalation behind an explicit `--allow-sudo` flag rather than triggering on any `permission_denied` result.

Once the HIGH findings are resolved, Bug #1 (missing `skills` array in `plugin.json`) and the three Medium/Low security fixes above are straightforward PRs.
