# NLPM Audit: alexgreensh/token-optimizer
**Date**: 2026-04-29  |  **Artifacts**: 9  |  **Strategy**: single
**NL Score**: 98/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 5  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/quick.md | command | 93 | Missing allowed-tools (-5); vague "some bloat" (-2) |
| commands/health.md | command | 95 | Missing allowed-tools (-5) |
| skills/token-optimizer/SKILL.md | skill | 96 | Vague "Some optimizations" (-2); vague "appropriate models" (-2) |
| .claude-plugin/plugin.json | plugin manifest | 100 | None |
| hooks/hooks.json | hook config | 100 | None |
| openclaw/skills/token-optimizer/SKILL.md | skill | 100 | None |
| skills/fleet-auditor/SKILL.md | skill | 100 | None |
| skills/token-coach/SKILL.md | skill | 100 | None |
| skills/token-dashboard/SKILL.md | skill | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 (both false positives after manual review) |
| Medium | 1 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks (hooks.json) | hooks/hooks.json |
| Hook scripts | hooks/python-launcher.sh, hooks/run.py |
| Installer | install.sh |
| Python scripts (token-optimizer) | skills/token-optimizer/scripts/measure.py, bash_hook.py, archive_result.py, bash_compress.py, context_intel.py, read_cache.py, session_store.py, injection.py, hook_io.py, plugin_env.py, delta_diff.py, structure_map.py, structure_replay.py, activity_tracker.py, and detectors/ (11 files) |
| Python scripts (fleet-auditor) | skills/fleet-auditor/scripts/fleet.py, shared.py |
| Package manifest (OpenClaw) | openclaw/package.json |
| MCP configs | None |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH | skills/fleet-auditor/scripts/fleet.py | 2523 | SEC-shell-true | `subprocess.run(["start", str(path)], shell=True)` — FALSE POSITIVE: Windows cmd.exe built-in `start` requires shell=True; argument is hardcoded to FLEET_DASHBOARD_PATH (internal path, no user input) |
| 2 | HIGH | skills/token-optimizer/scripts/measure.py | 7210 | SEC-shell-true | `subprocess.run(["powershell", "-Command", ps_cmd])` with dynamically constructed ps_cmd — FALSE POSITIVE: `int(pid)` cast on all user-derived values prevents injection; standard process introspection pattern |
| 3 | MEDIUM | skills/fleet-auditor/scripts/fleet.py | 1811 | SEC-external-resource | Generated dashboard HTML hard-embeds Google Fonts CDN link (`fonts.googleapis.com`, `fonts.gstatic.com`); browser makes external network request whenever user views the fleet dashboard |
| 4 | LOW | hooks/hooks.json | null | SEC-verbose-hooks | Hooks registered on 10+ event types (PreToolUse/Read, PreToolUse/Bash, PreToolUse/Agent\|Task, PreCompact ×3, SessionStart ×4, Stop, SessionEnd, StopFailure, UserPromptSubmit, PostToolUse ×3, PostCompact, CwdChanged); broad execution surface means any bug in hook scripts runs frequently |

## Bugs (PR-worthy)
No bugs found. All referenced files resolve. Required frontmatter fields present for each artifact type.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/fleet-auditor/scripts/fleet.py | External Google Fonts CDN in generated dashboard HTML causes third-party network request on every view | Bundle the two fonts locally (download woff2 files into assets/) or use a system font stack instead of fetching from fonts.googleapis.com |
| 2 | hooks/hooks.json | Broad multi-event hook surface; any exception in hook scripts affects all 10+ trigger paths | No structural change needed — the hooks are intentionally comprehensive; document the broad surface in PRIVACY.md or README so users understand the execution scope |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/health.md | No `allowed-tools` frontmatter field; body uses Bash (shell code blocks), which should be declared per R11 least-privilege | -5 |
| 2 | commands/quick.md | No `allowed-tools` frontmatter field; body uses Bash, which should be declared per R11 | -5 |
| 3 | commands/quick.md | Vague quantifier "some" in user-facing output string: "Context is good but has some bloat" (R01) | -2 |
| 4 | skills/token-optimizer/SKILL.md | Vague quantifier "Some" in instruction: "⚠️ Some optimizations have side effects" — replace with an explicit enumeration of which do (R01) | -2 |
| 5 | skills/token-optimizer/SKILL.md | Vague quantifier "appropriate" in Core Rules: "Use appropriate models (with fallbacks)" — the Model Selection table already specifies the mapping; the prose rule is redundant and vague (R01) | -2 |

## Cross-Component
All internal references resolve:
- fleet-auditor/SKILL.md → `references/fleet-systems.md`, `references/waste-patterns.md` ✓
- token-coach/SKILL.md → all four reference files + three example files ✓
- token-optimizer/SKILL.md → all four reference files + examples/ ✓
- hooks/hooks.json → all six Python scripts under skills/token-optimizer/scripts/ ✓

No orphaned components. No broken relative paths. No naming drift between plugin.json manifest and skill directory names.

**Informational note**: skills/fleet-auditor/SKILL.md embeds security claims about a third-party platform (OpenClaw CVE-2026-25253, "ClawJacked", "ClawHavoc campaign") that are not verifiable from this repo. This is narrative instructional content for Claude and poses no risk to the plugin itself, but maintainers should keep these claims up-to-date as the OpenClaw ecosystem evolves.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

No confirmed high or critical security findings (both pre-scan HIGH matches are false positives on review). Two medium/low security improvements are worth opening PRs for, particularly the Google Fonts CDN removal in the fleet dashboard. NL quality is excellent at 98/100; the five quality issues are minor and concentrated in two files.
