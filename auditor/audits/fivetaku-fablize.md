# NLPM Audit: fivetaku/fablize
**Date**: 2026-04-06  |  **Artifacts**: 4  |  **Strategy**: single
**NL Score**: 95/100
**Security**: CLEAR
**Bugs**: 1  |  **Quality Issues**: 3  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `.claude-plugin/plugin.json` | plugin manifest | 90 | Missing `commands` array — `commands/setup.md` exists on disk but is not registered |
| `commands/setup.md` | command | 93 | Missing `allowed-tools` in frontmatter |
| `skills/fablize/SKILL.md` | skill | 96 | Vague quantifier "genuinely" used twice in §4 |
| `hooks/hooks.json` | hook config | 100 | None |

**Weighted average**: (90 + 93 + 96 + 100) / 4 = **95/100**

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hook scripts | `hooks/router.sh`, `hooks/finish-the-work.sh`, `hooks/gate_prompt.py`, `hooks/gate_post_tool.py`, `hooks/gate_stop.py` |
| Gate scripts | `scripts/gate/classify_task.py`, `scripts/gate/ledger.py`, `scripts/gate/parse_tool_result.py`, `scripts/gate/verify_state.py` |
| Goal engine | `scripts/goals.py` |
| Shadow / measurement scripts | `scripts/shadow/shadow_logger.py`, `scripts/shadow/shadow_collect.py`, `scripts/shadow/outcome_collect.py`, `scripts/shadow/analyze.py` |
| MCP configs | None |
| Package manifests | None |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | `hooks/finish-the-work.sh` | 15–16 | path-traversal | `transcript_path` is extracted from hook-supplied JSON and passed directly to `open()` in Python without constraining the value to an expected directory; a compromised hook input could redirect reads to arbitrary files |
| 2 | Low | `scripts/gate/ledger.py` | 66 | env-controlled-path | `FABLIZE_DATA` env var overrides the data root, allowing the write path for ledger files to be redirected outside `~/.fablize` |
| 3 | Low | `scripts/shadow/shadow_logger.py` | 63–69 | out-of-repo-write | Measurement telemetry is appended to `~/.fablize/history/events.jsonl` without a documented opt-out or disclosure notice to the end user |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `.claude-plugin/plugin.json` | `commands` array is absent; `commands/setup.md` exists on disk but is never registered with the Claude Code plugin system | The `/setup` command is not callable after `claude plugin install`; setup must be run manually from outside the plugin surface |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `hooks/finish-the-work.sh` | `transcript_path` from hook JSON is used as a file path without directory validation | After extracting `tpath`, assert it begins with a known safe prefix (e.g., `$TMPDIR` or `$HOME`) before passing it to `python3` |
| 2 | `scripts/shadow/shadow_logger.py` | Out-of-band telemetry written to home directory without user disclosure | Add a one-time notice to setup.sh or the SKILL.md install section disclosing that session measurement events are collected locally |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `commands/setup.md` | No `allowed-tools:` in frontmatter; command invokes `AskUserQuestion` and `Bash` without declaring them | −5 |
| 2 | `commands/setup.md` | Vague quantifier "briefly" in "Report the result briefly" — no measurable output scope | −2 |
| 3 | `skills/fablize/SKILL.md` | Vague quantifier "genuinely" used twice in §4 ("overlap only when genuinely multi-category", "use it for a genuinely stuck slice") — no measurable threshold | −4 |

## Cross-Component
`hooks/finish-the-work.sh` is declared a Stop hook in its own file header (`# finish-the-work.sh — Stop hook`) and is explicitly called a companion to `gate_stop.py` in that file's module docstring ("Runs alongside finish-the-work.sh … the two cover different failure modes"). However, `hooks/hooks.json` registers only `gate_stop.py` in the `Stop` event; `finish-the-work.sh` has no entry. If setup.sh does not inject a second Stop hook via CLAUDE.md injection, the promise-no-act guard is silently absent. Confidence: medium (setup.sh was not in scope for this audit).

References: `hooks/hooks.json` Stop section vs `hooks/finish-the-work.sh` line 1, `hooks/gate_stop.py` module docstring.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

Priority order:
1. **Bug PR**: Add `"commands": ["./commands/setup"]` to `.claude-plugin/plugin.json` so the `/setup` command is reachable after installation.
2. **Security PR (Medium)**: Validate `transcript_path` in `hooks/finish-the-work.sh` before using it as a file path.
3. **Cross-component investigation**: Confirm whether setup.sh registers `finish-the-work.sh` as a second Stop hook; if not, add it to `hooks/hooks.json`.
4. **Quality PRs**: Add `allowed-tools:` to `commands/setup.md`; replace vague quantifiers with measurable conditions.
