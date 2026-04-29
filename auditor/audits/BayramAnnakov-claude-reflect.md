# NLPM Audit: BayramAnnakov/claude-reflect
**Date**: 2026-04-06  |  **Artifacts**: 8  |  **Strategy**: single
**NL Score**: 99/100
**Security**: CLEAR
**Bugs**: 1  |  **Quality Issues**: 4  |  **Security Findings**: 1

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/reflect.md | command | 94 | Vague quantifiers: "appropriate heading", "relevant section header", "makes semantic sense" (-6) |
| commands/view-queue.md | command | 97 | `Read` declared in allowed-tools but never used (-3) |
| commands/reflect-skills.md | command | 98 | "Relevant tools based on workflow" in template instruction (-2) |
| commands/skip-reflect.md | command | 100 | None |
| SKILL.md | skill | 100 | None |
| CLAUDE.md | context | 100 | None |
| hooks/hooks.json | config | 100 | None |
| .claude-plugin/plugin.json | manifest | 100 | None (cross-component issue flagged separately) |

**Weighted average**: (94 + 97 + 98 + 100 + 100 + 100 + 100 + 100) / 8 = **99/100**

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
| Hooks config | hooks/hooks.json (4 hook entries) |
| Python scripts (active) | scripts/capture_learning.py, scripts/check_learnings.py, scripts/post_commit_reminder.py, scripts/session_start_reminder.py, scripts/extract_session_learnings.py, scripts/extract_tool_errors.py, scripts/extract_tool_rejections.py, scripts/compare_detection.py, scripts/read_queue.py, scripts/lib/reflect_utils.py, scripts/lib/semantic_detector.py, scripts/lib/__init__.py |
| Legacy bash scripts | scripts/legacy/capture-learning.sh, scripts/legacy/check-learnings.sh, scripts/legacy/extract-session-learnings.sh, scripts/legacy/extract-tool-rejections.sh, scripts/legacy/post-commit-reminder.sh |
| MCP configs | None |
| Package manifests | None (Python stdlib only, no pip requirements) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | scripts/lib/semantic_detector.py | 77–83 | subprocess-user-content | `subprocess.run(["claude", "-p", ...])` is called with user message text from session JSONL files interpolated into the prompt. Malicious content in a session file could attempt prompt injection against the Claude API call. The list-form subprocess prevents shell injection; the risk is inherent to the design (semantic analysis of user messages). |
| 2 | Low | scripts/legacy/capture-learning.sh | 13 | unquoted-variable-echo | `PROMPT="$(echo "$INPUT" | jq -r ...)"` stores arbitrary user text. Used only in grep comparisons downstream (no eval/exec), but if PROMPT contains embedded newlines the echo may behave unexpectedly on some shells. Replaced by capture_learning.py which uses json.loads safely. |
| 3 | Low | scripts/legacy/post-commit-reminder.sh | 14 | unquoted-variable-echo | `COMMAND="$(echo "$INPUT" | jq -r '.tool_input.command // empty')"` captures Bash tool command from hook input into a variable used only in string comparison (`[[ "$COMMAND" == *"git commit"* ]]`), never eval'd. No direct risk but unquoted `$INPUT` in echo is fragile. Replaced by post_commit_reminder.py. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .claude-plugin/plugin.json | Missing `hooks` field pointing to `hooks/hooks.json`. The CLAUDE.md description states the manifest "points to hooks" but no such field exists in plugin.json. If Claude Code does not auto-discover hooks by convention from the plugin root, all 4 hooks (SessionStart, UserPromptSubmit, PreCompact, PostToolUse) will silently fail to register. | High: core self-learning capture would not function on fresh installs |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/lib/semantic_detector.py | User session content flows into Claude CLI prompt without content boundary markers | Add a clear content delimiter in ANALYSIS_PROMPT (e.g., `<user_message>…</user_message>`) to reduce prompt injection surface; document this as an accepted design risk |
| 2 | scripts/legacy/capture-learning.sh | Unquoted variable in `echo "$INPUT"` pipeline | These legacy scripts are superseded by Python equivalents; add `# DEPRECATED — use capture_learning.py` comment header and consider removing to reduce surface |
| 3 | scripts/legacy/post-commit-reminder.sh | Same unquoted variable pattern | Same: add DEPRECATED notice or remove |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/reflect.md | Vague quantifier: "Append the learning as a bullet point under an **appropriate** heading" (Step 7a.1) | -2 |
| 2 | commands/reflect.md | Vague quantifier: "Add after the **relevant** section header" (Step 7a) | -2 |
| 3 | commands/reflect.md | Vague quantifier: "Add learnings where they **make semantic sense**" (Step 7b) | -2 |
| 4 | commands/reflect.md | Context injection `!python3 "$(dirname "$(dirname "$(readlink -f "$0")")")/scripts/read_queue.py"` uses `$0` to resolve plugin root. In a Claude Code `!` context, `$0` is typically the shell interpreter path, not the skill file path, making the path resolution fragile. Falls back to `|| echo "[]"` so it fails silently rather than erroring. Other commands (skip-reflect.md) correctly use `CLAUDE_PLUGIN_ROOT`. | informational |
| 5 | commands/reflect-skills.md | Vague quantifier in template guidance: "allowed-tools: [**Relevant** tools based on workflow]" (Step 6) — instructs Claude to pick tools vaguely when generating child skill files | -2 |
| 6 | commands/view-queue.md | `Read` declared in `allowed-tools` but all implementation steps use `Bash` only (`python3 scripts/read_queue.py`). No `Read` tool call is specified anywhere in the task steps. | -3 |
| 7 | commands/reflect.md | Import path inconsistency in inline examples: some snippets use `from lib.semantic_detector import` while others use `from scripts.lib.reflect_utils import`. If Claude follows these verbatim, the short form (`from lib.*`) would fail unless `scripts/` is on `sys.path`. | informational |

## Cross-Component
**plugin.json ↔ hooks/hooks.json**: The plugin manifest at `.claude-plugin/plugin.json` contains no field linking to `hooks/hooks.json`. The CLAUDE.md description ("Plugin manifest, points to hooks") implies a link should exist but doesn't. Whether Claude Code auto-discovers hooks files by convention (e.g., looking for `hooks/hooks.json` relative to plugin root) is undocumented in this repo. If auto-discovery is not guaranteed, hook registration will silently fail — see Bug #1.

**commands/reflect.md ↔ CLAUDE_PLUGIN_ROOT convention**: `skip-reflect.md` and `reflect-skills.md` consistently use `${CLAUDE_PLUGIN_ROOT}` to locate scripts. `reflect.md`'s context injection uses a different `$0`-based approach. The two patterns are inconsistent; `CLAUDE_PLUGIN_ROOT` is the more robust pattern.

**hooks/hooks.json ↔ scripts/**: All 4 script paths referenced in hooks.json (`capture_learning.py`, `check_learnings.py`, `post_commit_reminder.py`, `session_start_reminder.py`) exist and are correctly named. No broken references.

**CLAUDE.md hook table ↔ hooks/hooks.json**: CLAUDE.md documents 4 hooks (SessionStart, UserPromptSubmit, PreCompact, PostToolUse/Bash). hooks.json registers exactly those 4 events. No drift.

## Recommendation
CLEAR — submit PRs for Bug #1 (missing hooks field in plugin.json) and the Medium/Low security fixes. The plugin is high quality overall with a well-structured multi-stage workflow, cross-platform Python scripts, and thoughtful hook design. The missing hooks manifest reference is the only issue with user-visible impact.
