# NLPM Audit: openai/codex-plugin-cc
**Date**: 2026-04-06  |  **Artifacts**: 13  |  **Strategy**: single
**NL Score**: 93/100
**Security**: REVIEW
**Bugs**: 4  |  **Quality Issues**: 10  |  **Security Findings**: 6

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| plugins/codex/agents/codex-rescue.md | Agent | 80 | No model declared; no example blocks |
| plugins/codex/commands/adversarial-review.md | Command | 90 | Multi-step flow without numbered steps |
| plugins/codex/commands/cancel.md | Command | 90 | No explicit empty-input handling |
| plugins/codex/commands/rescue.md | Command | 90 | Multi-step flow without numbered steps |
| plugins/codex/commands/result.md | Command | 90 | No explicit empty-input handling |
| plugins/codex/commands/review.md | Command | 90 | Multi-step flow without numbered steps |
| plugins/codex/commands/setup.md | Command | 90 | Multi-step flow without numbered steps |
| plugins/codex/skills/codex-cli-runtime/SKILL.md | Skill | 98 | Vague quantifier: "better" |
| plugins/codex/skills/codex-result-handling/SKILL.md | Skill | 98 | Vague quantifier: "actionable" |
| plugins/codex/skills/gpt-5-4-prompting/SKILL.md | Skill | 98 | Vague quantifier: "better" |
| plugins/codex/.claude-plugin/plugin.json | Manifest | 100 | None |
| plugins/codex/commands/status.md | Command | 100 | None |
| plugins/codex/hooks/hooks.json | Hook config | N/A | JSON config, not NL artifact |

**Weighted average** (12 scoreable artifacts): (80+90+90+90+90+90+90+98+98+98+100+100) / 12 = **93/100**

---

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 5 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hook configs | plugins/codex/hooks/hooks.json |
| Hook scripts | plugins/codex/scripts/session-lifecycle-hook.mjs, plugins/codex/scripts/stop-review-gate-hook.mjs |
| Main runtime | plugins/codex/scripts/codex-companion.mjs, plugins/codex/scripts/app-server-broker.mjs |
| Library scripts | plugins/codex/scripts/lib/*.mjs (13 files) |
| Package manifest | package.json |
| MCP configs | None found |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | plugins/codex/commands/cancel.md | 8 | Unquoted $ARGUMENTS in shell `!` command | `cancel $ARGUMENTS` lacks quoting; shell metacharacters in user-supplied job-id expand before Node receives them. Contrast: review.md and adversarial-review.md both wrap `"$ARGUMENTS"` in double quotes. |
| 2 | Medium | plugins/codex/commands/result.md | 8 | Unquoted $ARGUMENTS in shell `!` command | `result $ARGUMENTS` — same issue; a crafted argument like `task-123; malicious-cmd` would be split by the shell and execute the trailing command. |
| 3 | Medium | plugins/codex/commands/status.md | 8 | Unquoted $ARGUMENTS in shell `!` command | `status $ARGUMENTS` — same issue; three `!`-prefix commands are affected while the Bash code-block commands in review/adversarial-review correctly quote the argument. |
| 4 | Medium | plugins/codex/scripts/lib/process.mjs | 11 | `shell: process.platform === "win32"` | `runCommand` enables shell mode on Windows. When this utility is called with args derived from user input (e.g., model names, cwd paths), Windows shell expansion could allow injection on that platform. |
| 5 | Medium | plugins/codex/scripts/session-lifecycle-hook.mjs | 38 | Write to environment file outside repo | `appendFileSync(process.env.CLAUDE_ENV_FILE, ...)` exports session-scoped env vars into a file Claude Code will source. The written values include `input.session_id` from hook input and `process.env[PLUGIN_DATA_ENV]`; `shellEscape` is applied but the write surface itself is noteworthy. |
| 6 | Low | package.json | 15–16 | Unpinned devDependency versions | `@types/node: "^25.5.0"` and `typescript: "^6.0.2"` allow any compatible minor/patch bump on install, increasing reproducibility risk in CI. |

---

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | plugins/codex/agents/codex-rescue.md | Missing `model` frontmatter field | Agent runs on whatever Claude Code assigns by default; no tier guarantee, undeclared cost profile. |
| 2 | plugins/codex/commands/cancel.md | Unquoted `$ARGUMENTS` in `!` command (line 8) | Shell metacharacters in a user-supplied job-id are expanded before the Node script receives them; inconsistent with how review.md and adversarial-review.md handle `"$ARGUMENTS"`. |
| 3 | plugins/codex/commands/result.md | Unquoted `$ARGUMENTS` in `!` command (line 8) | Same as cancel.md; the three simple `!`-prefix commands all share this defect while the more complex commands with Bash code blocks get it right. |
| 4 | plugins/codex/commands/status.md | Unquoted `$ARGUMENTS` in `!` command (line 8) | Same as cancel.md. |

---

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | plugins/codex/commands/cancel.md | Unquoted `$ARGUMENTS` (Medium) | Change line 8 to: `` !`node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" cancel "$ARGUMENTS"` `` |
| 2 | plugins/codex/commands/result.md | Unquoted `$ARGUMENTS` (Medium) | Change line 9 to: `` !`node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" result "$ARGUMENTS"` `` |
| 3 | plugins/codex/commands/status.md | Unquoted `$ARGUMENTS` (Medium) | Change line 8 to: `` !`node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" status "$ARGUMENTS"` `` |
| 4 | plugins/codex/scripts/lib/process.mjs | Conditional shell mode on Windows (Medium) | Pass args as an array and avoid `shell: true` on Windows; if a shell is needed for PATH resolution, use `where.exe` or `which` first to resolve the binary path, then spawn without shell. |
| 5 | plugins/codex/scripts/session-lifecycle-hook.mjs | Write to CLAUDE_ENV_FILE (Medium) | Validate that `CLAUDE_ENV_FILE` points inside expected directories before writing; add bounds checking on variable names and values before appending. |
| 6 | package.json | Unpinned devDependency versions (Low) | Pin to exact versions (`25.5.0`, `6.0.2`) or use a lockfile-only policy; add a `package-lock.json` CI check. |

---

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | plugins/codex/agents/codex-rescue.md | No example blocks (zero examples) | −15 |
| 2 | plugins/codex/commands/adversarial-review.md | Multi-step foreground/background flows described as unordered bullets; numbered steps would make sequential order unambiguous | −10 |
| 3 | plugins/codex/commands/rescue.md | Six-step orchestration flow (flag detection → resume check → AskUserQuestion → subagent routing) uses conditional prose rather than numbered steps | −10 |
| 4 | plugins/codex/commands/review.md | Multi-step foreground/background flows without numbered steps (same structure as adversarial-review.md) | −10 |
| 5 | plugins/codex/commands/setup.md | Five-step conditional install flow (run setup → check result → ask user → install → rerun) described as unordered bullets | −10 |
| 6 | plugins/codex/commands/cancel.md | No explicit empty-input clause; `argument-hint` marks `[job-id]` optional but the command body does not describe fallback behavior (cancel latest? list cancelable jobs? error?) | −10 |
| 7 | plugins/codex/commands/result.md | No explicit empty-input clause; `argument-hint` marks `[job-id]` optional but the command body gives no guidance for the no-args case | −10 |
| 8 | plugins/codex/skills/codex-cli-runtime/SKILL.md | Vague quantifier: "tighten the user's request into a **better** Codex prompt" | −2 |
| 9 | plugins/codex/skills/codex-result-handling/SKILL.md | Vague quantifier: "include the most **actionable** stderr lines" | −2 |
| 10 | plugins/codex/skills/gpt-5-4-prompting/SKILL.md | Vague quantifier: "Prefer **better** prompt contracts over vague nudges" | −2 |

---

## Cross-Component

**References verified clean:**
- `codex-rescue.md` declares skills `codex-cli-runtime` and `gpt-5-4-prompting` → both exist at `skills/codex-cli-runtime/SKILL.md` and `skills/gpt-5-4-prompting/SKILL.md` ✓
- `rescue.md` routes to `codex:codex-rescue` subagent → `agents/codex-rescue.md` exists ✓
- `hooks/hooks.json` references `scripts/session-lifecycle-hook.mjs` and `scripts/stop-review-gate-hook.mjs` → both exist ✓
- `gpt-5-4-prompting/SKILL.md` references `references/prompt-blocks.md`, `references/codex-prompt-recipes.md`, `references/codex-prompt-antipatterns.md` → all three exist inside the skill directory ✓
- `codex-companion.mjs` references `prompts/adversarial-review.md` and `prompts/stop-review-gate.md` via `loadPromptTemplate` → both exist at `plugins/codex/prompts/` ✓

**Potential consistency issue:**
- `codex-rescue.md` (agent) and `codex-cli-runtime/SKILL.md` both document the `task` runtime contract; they are largely consistent but the agent body duplicates the skill content (routing flags, model/effort handling, --resume/--fresh semantics). If the runtime contract changes, both files need updating — a single authoritative source would reduce drift risk.

**No orphaned components detected.**

---

## Recommendation

REVIEW — submit PRs for all 4 bugs (model declaration in codex-rescue.md and the three unquoted-$ARGUMENTS fixes); include the Medium/Low security fixes in those same PRs since they are the same files. No Critical or High findings; security surface is CLEAR from external threats but Medium-level shell hygiene issues should be fixed before wider distribution.

**Priority order:**
1. Fix unquoted `$ARGUMENTS` in cancel.md, result.md, status.md (bug + security fix, same change)
2. Add `model: haiku` (or appropriate tier) to `codex-rescue.md`
3. Add numbered steps to adversarial-review.md, rescue.md, review.md, setup.md
4. Add empty-input clauses to cancel.md and result.md
5. Address process.mjs Windows shell mode and session-lifecycle-hook.mjs env-file bounds in a follow-up PR
6. Pin devDependency versions in package.json
