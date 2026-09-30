# NLPM Audit: hex/claude-council
**Date**: 2026-04-06  |  **Artifacts**: 17  |  **Strategy**: single
**NL Score**: 95/100
**Security**: REVIEW
**Bugs**: 0  |  **Quality Issues**: 5  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/status.md | command | 85 | Two-stage flow (status, then jobs) without numbered steps; no argument handling |
| commands/ask.md | command | 88 | Very long (16.7 KB); broad allowed-tools list |
| commands/advise.md | command | 92 | Long description; no explicit empty-argument handling |
| skills/council-execution/SKILL.md | skill | 95 | Description lists a stale provider set |
| agents/council-advisor.md | agent | 95 | Description over 1,200 characters with examples |
| commands/result.md | command | 97 | No numbered steps across list/cancel/fetch branches |
| skills/deep-execution/SKILL.md | skill | 97 | Long (10 KB) |
| skills/local-council-execution/SKILL.md | skill | 97 | Long (6.5 KB) |
| skills/provider-integration/SKILL.md | skill | 98 | None significant |
| mods/council-pane/specialists/test-pruner/SKILL.md | skill | 98 | None significant |
| mods/council-pane/specialists/test-writer/SKILL.md | skill | 98 | None significant |
| mods/council-pane/specialists/bug-fixer/SKILL.md | skill | 98 | None significant |
| mods/council-pane/specialists/ci-fixer/SKILL.md | skill | 98 | None significant |
| mods/council-pane/specialists/docs-updater/SKILL.md | skill | 98 | None significant |
| mods/council-pane/specialists/refactorer/SKILL.md | skill | 98 | None significant |
| .claude-plugin/plugin.json | manifest | 100 | None |
| hooks/hooks.json | hooks | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | hooks/hooks.json (Stop -> scripts/stop-review-gate.sh; module mods/council-pane/hooks/pane.tsx) |
| Scripts | 42 files under scripts/ (providers/*.sh, lib/*.sh, lib/render.py, lib/render.pl, run-council.sh, query-council.sh, check-status.sh, specialist.sh, release.sh, ...) |
| MCP configs | none |
| Package manifests | none (no package.json / requirements.txt) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | scripts/check-status.sh | 145 | network call (curl) | Probes provider APIs; keys go via a mode-600 curl config file, not argv. Expected for the plugin's purpose. |
| 2 | Medium | scripts/stop-review-gate.sh | 53 | diff sent to third-party provider | Opt-in Stop hook (needs .claude/council-stop-gate.json) sends `git diff HEAD` to an external provider. Provider name is allowlisted; fails open. |
| 3 | Medium | scripts/providers/*.sh | - | env var access (API keys) | Provider scripts read API keys from the environment and send them only to their own endpoints. No exfiltration found. |
| 4 | Low | scripts/lib/cache.sh | 102 | rm -rf glob | `rm -rf "${COUNCIL_CACHE_DIR:?}"/*` is guarded against an empty variable. specialist.sh:228 also removes a derived worktree state dir. |

No curl-to-shell, eval with variables, os.system, shell=True, sudo, PATH modification or postinstall scripts were found. The pre-scan High match was not reproduced; the closest candidates are the guarded `rm -rf` uses above. Commands pass `$ARGUMENTS` only into allowlisted `bash */scripts/...` patterns.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
No bugs found.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
No PR-worthy security fixes; the findings above are by design.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/status.md | Multi-step command (status, then jobs) without numbered steps | -10 |
| 2 | commands/status.md | No argument handling declared | -5 |
| 3 | agents/council-advisor.md | Description over 1,200 characters with examples | -5 |
| 4 | skills/council-execution/SKILL.md | Description lists only four providers; the plugin supports more | -5 |
| 5 | commands/ask.md | Oversized command body and broad allowed-tools | -12 |

## Cross-Component
- plugin.json declares no component arrays, so auto-discovery applies. Four commands, one agent and four skills were found on disk, and no manifest-vs-disk gap exists.
- Specialist SKILL.md files live under mods/, not skills/, so they are not auto-discovered. This is presumably intentional (loaded by the pane module).
- Provider lists are inconsistent: council-execution and council-advisor name four providers, while plugin.json and ask.md name more.
- The plugin.json userConfig references a `/specialists` command, but no commands/specialists.md exists. It may be provided by the mod, so this is unverified.

## Recommendation
REVIEW — no Critical or High findings. Medium findings are expected network and credential use by design. Submit NL quality PRs if desired; no bugs qualify.
