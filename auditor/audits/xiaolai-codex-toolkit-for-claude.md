# NLPM Audit: xiaolai/codex-toolkit-for-claude
**Date**: 2026-04-06  |  **Artifacts**: 30  |  **Strategy**: batched
**NL Score**: 96/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 26  |  **Security Findings**: 4

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/refresh-knowledge.md | command | 93 | No allowed-tools; "relevant" vague quantifier (ln 136) |
| commands/audit-skill.md | command | 95 | No allowed-tools declared |
| commands/audit-plugin.md | command | 95 | No allowed-tools declared |
| commands/cancel.md | command | 95 | No allowed-tools declared |
| commands/result.md | command | 95 | No allowed-tools declared |
| commands/audit-agent.md | command | 95 | No allowed-tools declared |
| commands/review-plan.md | command | 95 | No allowed-tools declared |
| commands/setup.md | command | 95 | No allowed-tools declared |
| commands/init.md | command | 95 | No allowed-tools declared |
| commands/audit-command.md | command | 95 | No allowed-tools declared |
| commands/audit.md | command | 95 | No allowed-tools declared |
| commands/implement.md | command | 95 | No allowed-tools declared |
| commands/verify.md | command | 95 | No allowed-tools declared |
| commands/status.md | command | 95 | No allowed-tools; unquoted $ARGUMENTS in bash subshell |
| commands/audit-rules.md | command | 95 | No allowed-tools declared |
| commands/continue.md | command | 95 | No allowed-tools declared |
| commands/bug-analyze.md | command | 95 | No allowed-tools declared |
| commands/preflight.md | command | 95 | No allowed-tools declared |
| commands/audit-nlp.md | command | 95 | No allowed-tools declared |
| commands/audit-fix.md | command | 95 | No allowed-tools declared |
| hooks/hooks.json | hook | 95 | Undocumented `description` field |
| CLAUDE.md | project doc | 95 | Reference doc; minor structural concerns |
| commands/shared/plugin-discover.md | shared | 97 | No name field (valid for shared partials) |
| commands/shared/scope-parse.md | shared | 97 | "purely mechanical" subjective in trivial check |
| skills/codex-toolkit/claude-code-conventions/SKILL.md | skill | 97 | Trigger description could have more specific auto-load phrases |
| agents/cross-validator.md | agent | 97 | Minor: "If uncertain, say so" in Important section |
| commands/shared/fallback.md | shared | 98 | Very minor vagueness ("same standard") |
| commands/shared/codex-call.md | shared | 98 | None |
| commands/shared/model-selection.md | shared | 98 | None |
| .claude-plugin/plugin.json | manifest | 100 | None |

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
| Hooks | hooks/hooks.json (SessionStart, SessionEnd, Stop) |
| Scripts | scripts/codex-preflight.sh, scripts/codex-runner.mjs, scripts/session-lifecycle-hook.mjs, scripts/stop-review-gate-hook.mjs, scripts/lib/state.mjs, scripts/lib/job-control.mjs, scripts/lib/workspace.mjs, scripts/lib/process.mjs, scripts/lib/render.mjs |
| MCP configs | .mcp.json (registers `codex mcp-server`) |
| Package manifests | package.json (no dependencies, no postinstall) |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | scripts/codex-preflight.sh | 200-203 | Python inline code with variable interpolation | `MODELS_DETAIL` (parsed from `~/.codex/models_cache.json`) is interpolated into a `python3 -c` triple-quoted string: `'''$MODELS_DETAIL'''`. A triple-quote sequence in the JSON data would break out of the string literal and allow arbitrary Python execution. Mitigated by the fact that the source file is the user's own local cache, not remote or user-input data. |
| 2 | Medium | commands/status.md | 24 | Unquoted `$ARGUMENTS` in bash subshell | `$(/bin/echo $ARGUMENTS \| grep -o '\-\-all' \|\| true)` passes `$ARGUMENTS` unquoted through echo, enabling word splitting and glob expansion. The grep output limits the final value to `--all` or empty, but the unquoted expansion still occurs in the subshell and can cause unexpected behavior with specially crafted input. |
| 3 | Medium | .mcp.json | 1-8 | Broad MCP server permissions | The `codex` MCP server is registered with no explicit permission scoping. It spawns an external OpenAI process (`codex mcp-server`) with access to Claude's tool execution context. This is inherent to the design but deserves disclosure. |
| 4 | Low | scripts/codex-preflight.sh | 78 | Predictable temp file path | Preflight cache is written to `${TMPDIR:-/tmp}/codex-preflight-cache.json` — a predictable filename in a world-writable directory. On systems without sticky-bit enforcement, this is theoretically vulnerable to a symlink attack or cache poisoning by another local user. |

## Bugs (PR-worthy)

No NL-level bugs found. All required frontmatter fields are present on every artifact. All cross-references (shared partials, scripts, skill paths) resolve correctly.

| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No bugs found | — |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/codex-preflight.sh | Python triple-quote injection via `$MODELS_DETAIL` (lines 200-203) | Write `$MODELS_DETAIL` to a temp file and pass the path to python3 instead of interpolating inline. Alternative: use `python3 -c "import json,sys; [print(m['slug']) for m in json.load(open(sys.argv[1])).get('models',[])]" "$MODELS_CACHE"` eliminating the intermediate variable entirely. |
| 2 | commands/status.md | Unquoted `$ARGUMENTS` in bash subshell (line 24) | Quote the variable: `"$(/bin/echo "$ARGUMENTS" \| grep -o '\-\-all' \|\| true)"` |
| 3 | scripts/codex-preflight.sh | Predictable temp file path (line 78) | Use `mktemp -u` with a randomised suffix, or store in `$XDG_CACHE_HOME/codex-toolkit/` which is user-owned. |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/audit-skill.md | No `allowed-tools` declared — command uses AskUserQuestion, Read, Bash, and MCP tools but doesn't restrict them | -5 |
| 2 | commands/audit-plugin.md | No `allowed-tools` declared | -5 |
| 3 | commands/cancel.md | No `allowed-tools` declared — command executes bash kill commands but doesn't restrict tools | -5 |
| 4 | commands/result.md | No `allowed-tools` declared | -5 |
| 5 | commands/audit-agent.md | No `allowed-tools` declared | -5 |
| 6 | commands/review-plan.md | No `allowed-tools` declared | -5 |
| 7 | commands/setup.md | No `allowed-tools` declared | -5 |
| 8 | commands/refresh-knowledge.md | No `allowed-tools` declared; "relevant" used without concrete criteria (ln 136: "also update the relevant command files") | -5, -2 |
| 9 | commands/init.md | No `allowed-tools` declared | -5 |
| 10 | commands/audit-command.md | No `allowed-tools` declared | -5 |
| 11 | commands/audit.md | No `allowed-tools` declared | -5 |
| 12 | commands/implement.md | No `allowed-tools` declared | -5 |
| 13 | commands/verify.md | No `allowed-tools` declared | -5 |
| 14 | commands/status.md | No `allowed-tools` declared | -5 |
| 15 | commands/audit-rules.md | No `allowed-tools` declared | -5 |
| 16 | commands/continue.md | No `allowed-tools` declared | -5 |
| 17 | commands/bug-analyze.md | No `allowed-tools` declared | -5 |
| 18 | commands/preflight.md | No `allowed-tools` declared | -5 |
| 19 | commands/audit-nlp.md | No `allowed-tools` declared | -5 |
| 20 | commands/audit-fix.md | No `allowed-tools` declared | -5 |
| 21 | hooks/hooks.json | Top-level `description` field is not in the documented hooks.json schema (harmless but non-standard) | -5 |
| 22 | commands/shared/scope-parse.md | "purely mechanical" in trivial-scope classification is subjective without concrete enumeration of all qualifying change types | -2 |
| 23 | commands/shared/plugin-discover.md | Cross-reference map scan patterns only cover `.md` references by plain file-path match; glob or regex patterns in command bodies referencing partials may be missed | -3 |
| 24 | skills/codex-toolkit/claude-code-conventions/SKILL.md | Description trigger phrase ("Canonical reference for Claude Code plugin artifact schemas…") describes content rather than usage scenario; weaker for auto-loading heuristics. Should include action phrases like "Use when auditing Claude Code plugins" | -3 |
| 25 | agents/cross-validator.md | "If uncertain, say so. Don't guess." — good practice, but "uncertain" lacks a threshold definition; the CONFIRMED/DISPUTED/UNCERTAIN classification would benefit from criteria for when UNCERTAIN applies | -2 |
| 26 | CLAUDE.md | "Adding new commands" section (step 7) says "Update README.md commands table" — the README exists but this creates an implicit external dependency not tracked in the plugin's own artifact set | -2 |

## Cross-Component

**References: All resolved.** Every cross-reference verified:
- All 5 shared partials (`model-selection.md`, `codex-call.md`, `scope-parse.md`, `fallback.md`, `plugin-discover.md`) are referenced by multiple commands and exist at their stated paths.
- `hooks/hooks.json` references `scripts/session-lifecycle-hook.mjs` and `scripts/stop-review-gate-hook.mjs` — both exist.
- `agents/cross-validator.md` references skill `codex-toolkit:claude-code-conventions` — `skills/codex-toolkit/claude-code-conventions/SKILL.md` exists.
- `commands/codex-call.md` injects `${CLAUDE_PLUGIN_ROOT}/skills/codex-toolkit/claude-code-conventions/SKILL.md` — exists.
- `commands/setup.md` and `commands/status.md` reference `${CLAUDE_PLUGIN_ROOT}/scripts/lib/state.mjs` — exists.
- `.mcp.json` registers `codex mcp-server` — external binary, assumed present post-install.

**Consistency observation:** `commands/audit-plugin.md` intentionally bypasses Codex and performs direct analysis (noted in CLAUDE.md as an exception). This is architecturally sound and well-documented. The other 19 commands follow the Codex-delegating pattern uniformly.

**Potential contradiction:** `commands/codex-call.md` says "Run Codex calls one at a time" but `commands/bug-analyze.md` Step 2 performs Grep/Glob reconnaissance with Claude directly before the Codex call. This is not a contradiction — Claude tools run in parallel, only Codex calls are sequential. The distinction is clear in context.

**Systemic quality note:** The universal absence of `allowed-tools` in all 20 commands is a deliberate architectural choice — commands are complex workflows that use many different tools dynamically. While this violates least-privilege, it is not a bug and may be the correct trade-off for a plugin that orchestrates MCP, Bash, Read, Edit, AskUserQuestion, and Task tools situationally. Consider adding `allowed-tools` only to the simplest commands (e.g., `cancel`, `result`, `status`, `preflight`) where the tool set is stable.

## Recommendation

CLEAR — submit PRs for all bugs and medium/low security fixes.

No Critical or High security findings. No NL artifact registration bugs. The plugin is well-architected with consistent patterns, thorough fallback handling, and a sophisticated three-layer knowledge architecture (skill → inject → cross-validate) that cleanly solves the cross-provider knowledge gap.

**Recommended PRs:**
1. Fix `scripts/codex-preflight.sh` Python triple-quote interpolation (Security Finding #1) — eliminate `'''$MODELS_DETAIL'''` pattern
2. Quote `$ARGUMENTS` in `commands/status.md:24` bash subshell (Security Finding #2)
3. Address predictable temp file in `scripts/codex-preflight.sh:78` (Security Finding #4)
4. Add `allowed-tools` to the simplest commands: `cancel`, `result`, `status`, `preflight` (Quality) — these have stable, bounded tool sets
5. Improve SKILL.md trigger description to include action phrases for better auto-loading (Quality)
