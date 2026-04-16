# NLPM Audit: muratcankoylan/ralph-wiggum-marketer
**Date**: 2026-04-16  |  **Artifacts**: 7  |  **Strategy**: single
**NL Score**: 90/100
**Security**: CLEAR
**Bugs**: 1  |  **Quality Issues**: 9  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/ralph-status.md | Command | 77 | No output format; multi-step without numbered steps; unused `Read` tool |
| commands/ralph-init.md | Command | 81 | No output format; unused `Write`, `Read`, `Glob` tools |
| commands/ralph-cancel.md | Command | 87 | No output format; unused `Write` tool |
| commands/ralph-marketer.md | Command | 88 | Missing step to create loop state file; vague "great content" |
| skills/copywriter/SKILL.md | Skill | 98 | Vague "genuinely good" |
| hooks/hooks.json | Hook config | 100 | None (JSON config, no NL penalties) |
| .claude-plugin/plugin.json | Plugin manifest | 100 | None (JSON config, no NL penalties) |

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
| Hooks | hooks/hooks.json, hooks/stop-hook.sh |
| Scripts | scripts/src/db/init.js, scripts/src/db/seed.js, scripts/src/db/status.js, scripts/src/db/query.js, scripts/src/content/list.js, scripts/src/test.js |
| MCP configs | None |
| Package manifests | package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | hooks/stop-hook.sh | 96–101 | Unescaped variable in JSON heredoc | `$SYSTEM_MSG` (which embeds `$PROMPT` read from `scripts/ralph/prompt.md`) is interpolated directly into a JSON heredoc without escaping. Unescaped double-quotes or embedded newlines in the prompt file produce malformed JSON output, breaking the stop-hook decision and potentially silencing the loop permanently. |
| 2 | Medium | hooks/stop-hook.sh | 47 | Unsanitized variable in grep pattern | `$COMPLETION_PROMISE` (parsed from `.claude/ralph-marketer-loop.local.md`) is passed as an unquoted grep regex pattern. A value containing regex metacharacters (`.`, `*`, `[`) changes matching semantics; a value containing shell-special characters can cause unexpected grep behaviour. |
| 3 | Low | package.json | 27 | Unpinned major version | `"better-sqlite3": "^11.0.0"` allows automatic upgrades across all minor/patch releases. A future breaking or malicious patch would be silently accepted on `npm install`. Pin to an exact version (e.g. `"11.9.1"`) or at minimum a minor range. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/ralph-marketer.md | No step to create `.claude/ralph-marketer-loop.local.md`. The stop hook (hooks/stop-hook.sh:21) checks for this file to determine whether a loop is active; ralph-cancel.md also deletes it. Nothing in the plugin writes it. | The entire loop mechanism never activates — stop-hook.sh always exits 0 (allow), the agent terminates after its first pass, and `/ralph-cancel` has nothing to remove. The plugin's core autonomous-loop feature is non-functional as shipped. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | hooks/stop-hook.sh | Lines 96–101: `$SYSTEM_MSG` interpolated into JSON heredoc without escaping | Use `jq -n --arg decision "block" --arg message "$SYSTEM_MSG" '{decision: $decision, message: $message}'` to produce correctly-escaped JSON instead of the heredoc. |
| 2 | hooks/stop-hook.sh | Line 47: `$COMPLETION_PROMISE` used as bare grep pattern | Quote and escape: `grep -qF "<promise>${COMPLETION_PROMISE}</promise>"` (use `-F` for fixed-string matching to prevent regex injection). |
| 3 | package.json | Line 27: `better-sqlite3: "^11.0.0"` unpinned | Pin to exact installed version, e.g. `"better-sqlite3": "11.9.1"`. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/ralph-cancel.md | No output format section — the command's user-facing response is described in plain prose, not a defined format | −10 |
| 2 | commands/ralph-cancel.md | `Write` declared in `allowed-tools` but the command body performs no Write tool calls (file removal is done via Bash `rm`) | −3 |
| 3 | commands/ralph-init.md | No output format section | −10 |
| 4 | commands/ralph-init.md | `Write`, `Read`, and `Glob` declared in `allowed-tools` but all file operations are done inside a single Bash heredoc; none of these tools are invoked in the command instructions | −9 (−3 each) |
| 5 | commands/ralph-status.md | No output format section — "Summarize the status" is listed as bullets but not as a formal output spec | −10 |
| 6 | commands/ralph-status.md | Multi-step command (run bash status commands, then summarize) without numbered steps for the agent to follow | −10 |
| 7 | commands/ralph-status.md | `Read` declared in `allowed-tools` but all file reads are done via `cat`/`tail` in the Bash block | −3 |
| 8 | commands/ralph-marketer.md | Vague quantifier: "Ship great content" (line 82) | −2 |
| 9 | skills/copywriter/SKILL.md | Vague quantifier: "genuinely good" (line 8) | −2 |

## Cross-Component
**Broken loop contract (Bug #1):** `ralph-marketer.md` is the command that starts the loop, but contains no step to write `.claude/ralph-marketer-loop.local.md`. `stop-hook.sh` requires this file to exist (line 21) before it will block Claude's exit and re-inject the prompt. `ralph-cancel.md` removes this same file. The three components form a coherent design but the creation side is missing — the loop state file is never initialised, so `stop-hook.sh` always falls through to `exit 0`.

**Args-to-hook data path undocumented:** `ralph-marketer.md` documents `--max-iterations` and `--completion-promise` arguments, and `stop-hook.sh` reads `max_iterations` and `completion_promise` keys from the loop state file frontmatter. There is no command or documented step that serialises the parsed CLI arguments into that frontmatter. The connection is implicit and fragile.

**ralph-init.md copies `src/test.js` from plugin root but path in package.json is `scripts/src/test.js`:** The `cp "$PLUGIN_ROOT/scripts/src/test.js" src/` step copies to `src/test.js` in the target project; `package.json` "test" script runs `node scripts/src/test.js`. These paths don't align — `npm test` will fail after initialisation unless the copy destination is corrected to `scripts/src/`.

**No orphaned components or contradictions detected** beyond those noted above.

## Recommendation

CLEAR — submit PRs for Bug #1 (missing loop state file creation in `ralph-marketer.md`) and all three Medium/Low security fixes. The loop state PR is the highest-value fix: without it the plugin's flagship autonomous-loop feature never activates. The `npm test` path mismatch (ralph-init.md vs package.json) should be bundled into the same PR. Security fixes are low-risk one-liners suitable for a follow-up PR.
