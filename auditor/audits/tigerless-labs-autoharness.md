# NLPM Audit: tigerless-labs/autoharness
**Date**: 2026-04-06  |  **Artifacts**: 5  |  **Strategy**: single
**NL Score**: 87/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 5  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/curator.md | agent | 70 | No example blocks (-15) |
| agents/reflector.md | agent | 70 | No example blocks (-15) |
| skills/learn/SKILL.md | skill | 95 | No output format for the final report |
| .claude-plugin/plugin.json | manifest | 100 | None |
| hooks/hooks.json | hooks | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | hooks/hooks.json (SessionStart, Stop, PreToolUse and SessionEnd run `python3 -m autoharness.hook.dispatch`) |
| Scripts | Python sources under src/autoharness and tools/ (there is no scripts/ directory) |
| MCP configs | .mcp.json (stage_skill server, a local python module, PYTHONPATH from CLAUDE_PLUGIN_ROOT) |
| Package manifests | None (no package.json or requirements.txt) |

### Security Findings
No security findings.

The pre-scan's 2 Critical matches are in `src/autoharness/lib/skills_guard.py` (lines 17-18 and 42). They are regex detection patterns (`curl ... | sh`, `wget ... | sh`, `/dev/tcp/`) that the plugin uses to block malicious skills. They are not executed behaviour, so they are false positives. Subprocess calls in dispatch.py, spawn.py, layer.py and notify.py pass argv lists, and none uses `shell=True`. I grepped for these patterns but did not read every one of the 65 script files in full.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
No bugs found.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
None.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/curator.md | No example blocks | -15 |
| 2 | agents/curator.md | Description names no situation the agent is not for | -5 |
| 3 | agents/curator.md | No explicit output format section | -10 |
| 4 | agents/reflector.md | No example blocks (-15), no "not for" in description (-5), no output format (-10) | -30 |
| 5 | skills/learn/SKILL.md | No output format for the final report | -5 |

## Cross-Component
- The tool `mcp__plugin_autoharness_stage_skill__stage_skill` matches plugin name `autoharness` and the `.mcp.json` server `stage_skill`, so the reference resolves.
- Both agents declare only tools they use. `learn` references `stage_skill` but declares no tools, which skills don't require.
- hooks.json calls the `autoharness.hook.dispatch` module, which exists under src/.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes. No bugs or security fixes were found, so the quality issues are informational only.
