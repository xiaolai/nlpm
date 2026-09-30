# NLPM Audit: ayghri/i-have-adhd
**Date**: 2026-04-06  |  **Artifacts**: 4  |  **Strategy**: single
**NL Score**: 97/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 2  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/i-have-adhd/SKILL.md | skill | 94 | Vague quantifier "relevant" (3x, lines 105 and 107) |
| .cursor/skills/i-have-adhd/SKILL.md | skill (mirror) | 94 | Same as canonical skill (identical copy) |
| .claude-plugin/plugin.json | manifest | 100 | None |
| hooks/hooks.json | hooks | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | hooks/hooks.json, hooks/always-on.mjs, hooks/always-on.sh, hooks/always-on.ps1 |
| Scripts | scripts/check_context_compat.ts, scripts/check_pi_extension.py, scripts/run_scenario_eval.py, scripts/run_evals.py, scripts/judge.py |
| MCP configs | none |
| Package manifests | package.json (private, no install scripts, no dependencies) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | hooks/always-on.mjs | 16 | env var access | Reads CLAUDE_CONFIG_DIR to locate opt-in flag file. Read-only, no network, benign. |
| 2 | Medium | scripts/check_pi_extension.py | 159 | env var access | Iterates os.environ and filters out *_API_KEY variables before passing env to a child process. Defensive, not exfiltration. |
| 3 | Low | hooks/hooks.json | 6 | verbose hook trigger | SessionStart matcher fires on startup, resume, clear and compact. Hook exits immediately unless opt-in flag exists. |

Notes: subprocess calls in scripts/judge.py, run_evals.py, run_scenario_eval.py and check_pi_extension.py use argument lists with no shell=True. No eval, curl, wget, sudo, base64 or network calls found.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| - | - | No bugs found | - |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| - | - | None needed; findings are benign | - |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/i-have-adhd/SKILL.md | Vague quantifier "relevant" used 3 times in Rule 9 (lines 105, 107), undefined ranking criterion | -6 |
| 2 | .cursor/skills/i-have-adhd/SKILL.md | Mirror of the same text, same vague quantifier | -6 |

## Cross-Component
- hooks.json references hooks/always-on.mjs, which exists. The .sh and .ps1 fallbacks exist but are not referenced by hooks.json (documented as fallbacks in the file headers).
- .cursor mirror is byte-identical to the canonical skill. No drift.
- plugin.json version (0.3.0) matches package.json.

## Recommendation
CLEAR — no bugs and no actionable security findings. Optional: replace "relevant" in Rule 9 with a concrete ranking criterion (e.g. "most urgent for the reader's current task").
