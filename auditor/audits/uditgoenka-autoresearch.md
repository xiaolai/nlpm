# NLPM Audit: uditgoenka/autoresearch
**Date**: 2026-04-06  |  **Artifacts**: 36  |  **Strategy**: batched
**NL Score**: 88/100
**Security**: CLEAR
**Bugs**: 3  |  **Quality Issues**: 5  |  **Security Findings**: 5

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .opencode/agents/docs-manager.md | Agent | 55 | Missing `name` frontmatter; no model declared; no examples |
| .opencode/commands/autoresearch.md | Command | 75 | Missing `name` frontmatter |
| .opencode/commands/autoresearch_debug.md | Command | 75 | Missing `name` frontmatter |
| .opencode/commands/autoresearch_fix.md | Command | 75 | Missing `name` frontmatter |
| .opencode/commands/autoresearch_learn.md | Command | 75 | Missing `name` frontmatter |
| .opencode/commands/autoresearch_plan.md | Command | 75 | Missing `name` frontmatter |
| .opencode/commands/autoresearch_predict.md | Command | 75 | Missing `name` frontmatter |
| .opencode/commands/autoresearch_reason.md | Command | 75 | Missing `name` frontmatter |
| .opencode/commands/autoresearch_scenario.md | Command | 75 | Missing `name` frontmatter |
| .opencode/commands/autoresearch_security.md | Command | 75 | Missing `name` frontmatter |
| .opencode/commands/autoresearch_ship.md | Command | 75 | Missing `name` frontmatter |
| .agents/skills/autoresearch/SKILL.md | Skill | 88 | Mixed command syntax in description (`/autoresearch` vs `$autoresearch plan`) |
| .claude/skills/autoresearch/SKILL.md | Skill | 88 | Embedded post-completion star-repo social prompt |
| .opencode/skills/autoresearch/SKILL.md | Skill | 88 | Embedded post-completion star-repo social prompt |
| claude-plugin/skills/autoresearch/SKILL.md | Skill | 88 | Embedded post-completion star-repo social prompt |
| .claude/commands/autoresearch.md | Command | 95 | Missing `allowed-tools` declaration |
| .claude/commands/autoresearch/debug.md | Command | 95 | Missing `allowed-tools` declaration |
| .claude/commands/autoresearch/fix.md | Command | 95 | Missing `allowed-tools` declaration |
| .claude/commands/autoresearch/learn.md | Command | 95 | Missing `allowed-tools` declaration |
| .claude/commands/autoresearch/plan.md | Command | 95 | Missing `allowed-tools` declaration |
| .claude/commands/autoresearch/predict.md | Command | 95 | Missing `allowed-tools` declaration |
| .claude/commands/autoresearch/reason.md | Command | 95 | Missing `allowed-tools` declaration |
| .claude/commands/autoresearch/scenario.md | Command | 95 | Missing `allowed-tools` declaration |
| .claude/commands/autoresearch/security.md | Command | 95 | Missing `allowed-tools` declaration |
| .claude/commands/autoresearch/ship.md | Command | 95 | Missing `allowed-tools` declaration |
| claude-plugin/commands/autoresearch.md | Command | 95 | Missing `allowed-tools` declaration |
| claude-plugin/commands/autoresearch/debug.md | Command | 95 | Missing `allowed-tools` declaration |
| claude-plugin/commands/autoresearch/fix.md | Command | 95 | Missing `allowed-tools` declaration |
| claude-plugin/commands/autoresearch/learn.md | Command | 95 | Missing `allowed-tools` declaration |
| claude-plugin/commands/autoresearch/plan.md | Command | 95 | Missing `allowed-tools` declaration |
| claude-plugin/commands/autoresearch/predict.md | Command | 95 | Missing `allowed-tools` declaration |
| claude-plugin/commands/autoresearch/reason.md | Command | 95 | Missing `allowed-tools` declaration |
| claude-plugin/commands/autoresearch/scenario.md | Command | 95 | Missing `allowed-tools` declaration |
| claude-plugin/commands/autoresearch/security.md | Command | 95 | Missing `allowed-tools` declaration |
| claude-plugin/commands/autoresearch/ship.md | Command | 95 | Missing `allowed-tools` declaration |
| claude-plugin/.claude-plugin/plugin.json | Manifest | 100 | None — structurally complete |

**Score calculation:** (55×1 + 75×10 + 88×4 + 95×20 + 100×1) ÷ 36 = 3157 ÷ 36 = **87.7 → 88**

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 2 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks | None |
| Scripts | scripts/install.sh, scripts/sync-codex.sh, scripts/sync-opencode.sh, scripts/release.sh |
| MCP Configs | None |
| Package Manifests | None |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | MEDIUM | scripts/sync-codex.sh | 59 | `python3 -c` with bash variable interpolation | `$DST` is expanded into a Python string literal. A repo path containing `'` or `\n` would corrupt the inline Python script. Risk low in practice (path derived from `BASH_SOURCE[0]`), but fragile. |
| 2 | MEDIUM | scripts/sync-opencode.sh | 53 | `python3 -c` with bash variable interpolation | Identical pattern to sync-codex.sh. `$DST/SKILL.md` embedded in Python string; same path-injection risk. |
| 3 | MEDIUM | .claude/skills/autoresearch/SKILL.md | 719 | Network call to external API via `gh api` | Post-completion social prompt instructs the AI to run `gh api -X PUT /user/starred/uditgoenka/autoresearch` on the user's GitHub account. Action is user-approved and idempotent, but it is an uncontrolled network side-effect written into skill behavior. Duplicated across all four SKILL.md copies. |
| 4 | LOW | scripts/install.sh | 156 | `rm -rf` with variable path | `sync_dir()` runs `rm -rf "$2"` on the destination directory before copying. Path is validated from `REPO_ROOT`, so injection is unlikely, but a misconfigured `CONFIG_DIR` could target unexpected locations. |
| 5 | LOW | scripts/release.sh | 197, 262, 269, 276 | External network calls | Script pushes to `origin`, creates PRs, and publishes GitHub releases. Expected for a release workflow but worth noting as network-touching operations for supply-chain auditors. |

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .opencode/agents/docs-manager.md | Missing `name` field in frontmatter | Agent registration may fail or fall back to filename; breaks any reference by name in orchestration |
| 2 | .opencode/commands/autoresearch*.md (all 10 files) | Missing `name` field in frontmatter | All OpenCode commands lack `name`; registration depends on filename inference, which is not guaranteed by the OpenCode spec |
| 3 | .claude/commands/autoresearch*.md and claude-plugin/commands/autoresearch*.md (all 20 command files) | Missing `allowed-tools` declaration | Commands invoke AskUserQuestion, Bash, and file-read tools but do not declare them; Claude Code may restrict tool access or prompt the user unexpectedly at execution time |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/sync-codex.sh | `python3 -c` with bash-expanded path variable (line 59) | Write the Python script to a temp file first (`mktemp`) and pass the target path as a CLI argument via `sys.argv[1]`, eliminating string interpolation |
| 2 | scripts/sync-opencode.sh | Same pattern as sync-codex.sh (line 53) | Same fix: use a temp file or pass path as `sys.argv[1]` |
| 3 | scripts/install.sh | `rm -rf "$2"` in `sync_dir` with no guard (line 156) | Add a safety check: verify `"$2"` is a subdirectory of a known root before removal, e.g. `[[ "$2" == "$REPO_ROOT"/* ]] || die "unsafe target"` |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .opencode/agents/docs-manager.md | No model tier declared; no examples | -5 (no model) + -15 (zero examples) = -20 |
| 2 | .opencode/commands/autoresearch*.md (all 10) | `argument-hint` field absent; present in equivalent .claude/ versions | Reduces discoverability; no numeric penalty in current rubric but informational gap |
| 3 | .agents/skills/autoresearch/SKILL.md | Description mixes `/autoresearch` (Claude syntax) and `$autoresearch plan` (Codex syntax) in the same sentence | Inconsistent UX signal for Codex users who read the description |
| 4 | All four SKILL.md copies | Post-completion social prompt asks users to star the repo via `gh api`; embedded as a behavioral directive in every SKILL.md | Not a rule violation but creates an implicit side-effect in every completed autoresearch run; unusual for a productivity tool |
| 5 | .claude/commands/autoresearch.md | SKILL.md "Interactive Setup" section is referenced in the command body but the skill file is not declared as a dependency or loaded via `allowed-tools`; the command relies on the AI to self-load it | Creates a soft dependency that could be missed in restricted environments |

## Cross-Component

**Consistency across distributions:** The repo maintains four parallel distributions (.claude, .opencode, .agents, claude-plugin) synchronized by `scripts/sync-codex.sh` and `scripts/sync-opencode.sh`. The sync scripts correctly adapt command syntax and tool names. The canonical source is `.claude/skills/autoresearch/SKILL.md`; all four SKILL.md copies were verified to be functionally equivalent with appropriate platform adaptations.

**Reference integrity:** All commands reference workflow files under `*/skills/autoresearch/references/*.md` (e.g., `autonomous-loop-protocol.md`, `debug-workflow.md`). These files are NOT in the audited artifact list — they exist but were out of scope. If any reference file is missing, the command silently fails at step 1 of execution. No broken references were detected within the audited file set itself.

**Docs-manager coupling:** `.opencode/commands/autoresearch_learn.md` spawns `docs-manager` by identity. The `docs-manager.md` agent exists in `.opencode/agents/` and is correctly installed by `scripts/install.sh`. The coupling is valid but fragile — renaming the agent without updating the learn workflow would silently break documentation generation.

**OpenCode vs Claude schema divergence:** The .opencode commands use `agent: build` (OpenCode model selector) rather than `allowed-tools`. This is correct for OpenCode's schema. The `name` absence appears deliberate (OpenCode infers names from filenames), but it leaves the commands non-compliant with the NLPM name requirement and is worth confirming against the OpenCode spec.

## Recommendation

Security is CLEAR — no Critical or High findings were detected in hooks, scripts, or configs.

**CLEAR — submit PRs for all bugs and medium/low security fixes.**

Priority order:
1. **Add `name` field** to `docs-manager.md` and all 10 `.opencode/commands/*.md` files (Bug #1, #2) — low effort, high correctness value
2. **Add `allowed-tools`** to all 20 Claude command files (Bug #3) — ensures predictable tool access in restricted Claude Code environments
3. **Fix `python3 -c` path interpolation** in `sync-codex.sh` and `sync-opencode.sh` (Security Fix #1, #2) — use temp file or sys.argv to eliminate string injection risk
4. **Add safety guard to `sync_dir`** in `install.sh` (Security Fix #3) — belt-and-suspenders for `rm -rf` with user-supplied paths
5. **Consider moving the star-repo prompt** out of SKILL.md and into the command layer with an explicit user confirmation gate, so it appears at most once per session rather than being embedded in the shared skill knowledge base (Quality #4)
