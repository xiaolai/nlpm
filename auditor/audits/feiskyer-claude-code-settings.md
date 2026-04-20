# NLPM Audit: feiskyer/claude-code-settings
**Date**: 2026-04-20  |  **Artifacts**: 45  |  **Strategy**: batched
**NL Score**: 85/100
**Security**: CLEAR
**Bugs**: 6  |  **Quality Issues**: 35  |  **Security Findings**: 4

---

## NL Score Summary

Score covers 35 NL content files (agents, commands, skills). Config files (hooks.json × 3, plugin.json × 7) scored separately at 100 each; overall across all 45 artifacts ≈ 88/100.

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/skill-creator/agents/analyzer.md | Agent | 45 | Missing `name` + `description` frontmatter |
| skills/skill-creator/agents/grader.md | Agent | 45 | Missing `name` + `description` frontmatter |
| skills/skill-creator/agents/comparator.md | Agent | 45 | Missing `name` + `description` frontmatter |
| agents/ui-engineer.md | Agent | 70 | No examples; vague language × 5 |
| agents/instruction-reflector.md | Agent | 80 | No model declared; no examples |
| agents/deep-reflector.md | Agent | 80 | No model declared; no examples |
| agents/insight-documenter.md | Agent | 80 | No model declared; no examples |
| agents/pr-reviewer.md | Agent | 80 | No model declared; no examples |
| agents/command-creator.md | Agent | 80 | No model declared; no examples |
| agents/github-issue-fixer.md | Agent | 80 | No model declared; no examples |
| skills/skill-creator/SKILL.md | Skill | 80 | Vague quantifiers ×10+ (capped penalty) |
| plugins/kiro-skill/commands/kiro/vibe.md | Command | 85 | No `allowed-tools`; no empty input handling |
| plugins/kiro-skill/commands/kiro/spec.md | Command | 85 | No `allowed-tools`; no empty input handling |
| plugins/kiro-skill/commands/kiro/task.md | Command | 85 | No `allowed-tools`; no empty input handling |
| plugins/kiro-skill/commands/kiro/execute.md | Command | 85 | No `allowed-tools`; no empty input handling |
| plugins/kiro-skill/commands/kiro/design.md | Command | 85 | No `allowed-tools`; no empty input handling |
| skills/command-creator/SKILL.md | Skill | 88 | Vague language × 6 ("appropriate", "proper", "relevant") |
| plugins/spec-kit-skill/skills/spec-kit-skill/SKILL.md | Skill | 92 | Vague language × 4 |
| skills/deep-research/SKILL.md | Skill | 92 | Vague language × 4 |
| skills/spec-kit-skill/SKILL.md | Skill | 92 | Vague language × 4 |
| skills/github-review-pr/SKILL.md | Skill | 92 | Vague language × 4 ("appropriate", "relevant") |
| skills/reflection/SKILL.md | Skill | 92 | Vague language × 4 |
| skills/github-fix-issue/SKILL.md | Skill | 92 | Vague language × 4 |
| plugins/codex-skill/skills/codex-skill/SKILL.md | Skill | 94 | Vague language × 3 |
| plugins/autonomous-skill/skills/autonomous-skill/SKILL.md | Skill | 94 | Vague language × 3 |
| skills/codex-skill/SKILL.md | Skill | 94 | Vague language × 3 |
| skills/eureka/SKILL.md | Skill | 94 | Vague language × 3 |
| skills/autonomous-skill/SKILL.md | Skill | 94 | Vague language × 3 |
| plugins/kiro-skill/skills/kiro-skill/SKILL.md | Skill | 96 | Minor vague language × 2 |
| skills/kiro-skill/SKILL.md | Skill | 96 | Minor vague language × 2 |
| plugins/nanobanana-skill/skills/nanobanana-skill/SKILL.md | Skill | 98 | Vague language × 1 |
| plugins/youtube-transcribe-skill/skills/youtube-transcribe-skill/SKILL.md | Skill | 98 | Minor vague language |
| skills/nanobanana-skill/SKILL.md | Skill | 98 | Minor vague language |
| skills/youtube-transcribe-skill/SKILL.md | Skill | 98 | Minor vague language |
| skills/translate/SKILL.md | Skill | 100 | None |
| plugins/autonomous-skill/skills/autonomous-skill/hooks/hooks.json | Hook | 100 | None |
| skills/autonomous-skill/hooks/hooks.json | Hook | 100 | None |
| hooks/hooks.json | Hook | 100 | None |
| plugins/codex-skill/.claude-plugin/plugin.json | Manifest | 100 | None |
| plugins/nanobanana-skill/.claude-plugin/plugin.json | Manifest | 100 | None |
| plugins/spec-kit-skill/.claude-plugin/plugin.json | Manifest | 100 | None |
| plugins/youtube-transcribe-skill/.claude-plugin/plugin.json | Manifest | 100 | None |
| plugins/kiro-skill/.claude-plugin/plugin.json | Manifest | 100 | None |
| plugins/autonomous-skill/.claude-plugin/plugin.json | Manifest | 100 | None |
| .claude-plugin/plugin.json | Manifest | 100 | None |

---

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 2 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks (Stop event) | hooks/hooks.json, plugins/autonomous-skill/skills/autonomous-skill/hooks/hooks.json, skills/autonomous-skill/hooks/hooks.json → all invoke stop-hook.sh |
| Shell scripts | skills/autonomous-skill/scripts/run-session.sh, skills/autonomous-skill/scripts/setup-loop.sh, skills/autonomous-skill/hooks/stop-hook.sh, plugins/autonomous-skill/skills/autonomous-skill/scripts/run-session.sh, plugins/autonomous-skill/skills/autonomous-skill/scripts/setup-loop.sh, plugins/autonomous-skill/skills/autonomous-skill/hooks/stop-hook.sh, skills/spec-kit-skill/scripts/detect-phase.sh, plugins/spec-kit-skill/skills/spec-kit-skill/scripts/detect-phase.sh, scripts/update-cc-plugins.sh, status-line.sh |
| Python scripts | skills/nanobanana-skill/nanobanana.py, plugins/nanobanana-skill/skills/nanobanana-skill/nanobanana.py, skills/skill-creator/scripts/*.py (9 files) |
| MCP configs | .mcp.json (chrome-devtools-mcp server) |
| Package manifests | None (no package.json or requirements.txt in repo root) |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | skills/autonomous-skill/scripts/run-session.sh | 27 | `bypassPermissions` default | `DEFAULT_PERMISSION_MODE="bypassPermissions"` sets all spawned `claude -p` child sessions to bypass all permission prompts automatically. Any task executed via this script — including user-supplied task descriptions — runs without any confirmation gates for file system writes, git operations, or Bash commands. |
| 2 | Medium | .mcp.json | 4 | Unpinned MCP + browser access | `npx chrome-devtools-mcp@latest` uses an unpinned `@latest` version, pulling whatever is published at install time. Additionally `--autoConnect` grants the MCP server automatic browser session access, which can read and manipulate open browser sessions including authenticated ones. |
| 3 | Low | skills/autonomous-skill/scripts/run-session.sh | 295–297 | Unsanitized prompt interpolation | Task description (`$task_desc`) and prompt template content are string-interpolated directly into the `claude -p "..."` argument. While properly shell-quoted (no OS injection risk), an adversarial task prompt could embed prompt-injection content targeting the child Claude session operating under `bypassPermissions`. |
| 4 | Low | hooks/hooks.json | 7 | Unpinned hook script path | All three hooks.json files reference `${CLAUDE_PLUGIN_ROOT}/skills/autonomous-skill/hooks/stop-hook.sh` without version pinning. If the plugin root is replaced or a symlink is manipulated, a different script could be executed at every session stop. |

---

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | skills/skill-creator/agents/analyzer.md | Missing `name` frontmatter field | Agent cannot register by name; skill-creator SKILL.md references this agent by path but `name` is required for proper Claude Code agent registration |
| 2 | skills/skill-creator/agents/analyzer.md | Missing `description` frontmatter field | Agent has no trigger description; invocation context is lost |
| 3 | skills/skill-creator/agents/grader.md | Missing `name` frontmatter field | Same registration failure — grader called by skill-creator skill but lacks proper frontmatter |
| 4 | skills/skill-creator/agents/grader.md | Missing `description` frontmatter field | No trigger description; context missing |
| 5 | skills/skill-creator/agents/comparator.md | Missing `name` frontmatter field | Comparator subagent unregistrable by name |
| 6 | skills/skill-creator/agents/comparator.md | Missing `description` frontmatter field | No trigger description |

---

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/autonomous-skill/scripts/run-session.sh | `bypassPermissions` is the hardcoded default permission mode | Change `DEFAULT_PERMISSION_MODE` to `"default"` or `"acceptEdits"`. Document `--permission-mode bypassPermissions` as an opt-in flag with a warning in the help text and SKILL.md. Users who need fully autonomous operation can still pass the flag explicitly. |
| 2 | .mcp.json | `chrome-devtools-mcp@latest` is unpinned and auto-connects | Pin to a specific version (e.g., `chrome-devtools-mcp@0.3.2`) and remove `--autoConnect`, requiring explicit browser attachment. Add a comment explaining what browser capabilities are granted. |
| 3 | skills/autonomous-skill/scripts/run-session.sh | Unsanitized task description passes into `bypassPermissions` child session | Add explicit warning in help text and SKILL.md that user-supplied task descriptions run under elevated permissions. Low priority given that bypassPermissions fix (finding #1) mitigates most of the risk. |

---

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/instruction-reflector.md | No `model` field declared | -5 |
| 2 | agents/instruction-reflector.md | Zero example blocks | -15 |
| 3 | agents/deep-reflector.md | No `model` field declared | -5 |
| 4 | agents/deep-reflector.md | Zero example blocks | -15 |
| 5 | agents/ui-engineer.md | No `model` field declared | -5 |
| 6 | agents/ui-engineer.md | Zero example blocks | -15 |
| 7 | agents/ui-engineer.md | Vague quantifiers: "appropriate" ×3, "relevant" ×1, "beneficial" ×1 | -10 |
| 8 | agents/insight-documenter.md | No `model` field declared | -5 |
| 9 | agents/insight-documenter.md | Zero example blocks | -15 |
| 10 | agents/pr-reviewer.md | No `model` field declared | -5 |
| 11 | agents/pr-reviewer.md | Zero example blocks | -15 |
| 12 | agents/command-creator.md | No `model` field declared | -5 |
| 13 | agents/command-creator.md | Zero example blocks | -15 |
| 14 | agents/github-issue-fixer.md | No `model` field declared | -5 |
| 15 | agents/github-issue-fixer.md | Zero example blocks | -15 |
| 16 | plugins/kiro-skill/commands/kiro/vibe.md | No `allowed-tools` in frontmatter | -5 |
| 17 | plugins/kiro-skill/commands/kiro/vibe.md | No empty-argument handling | -10 |
| 18 | plugins/kiro-skill/commands/kiro/spec.md | No `allowed-tools` in frontmatter | -5 |
| 19 | plugins/kiro-skill/commands/kiro/spec.md | No empty-argument handling | -10 |
| 20 | plugins/kiro-skill/commands/kiro/task.md | No `allowed-tools` in frontmatter | -5 |
| 21 | plugins/kiro-skill/commands/kiro/task.md | No empty-argument handling | -10 |
| 22 | plugins/kiro-skill/commands/kiro/execute.md | No `allowed-tools` in frontmatter | -5 |
| 23 | plugins/kiro-skill/commands/kiro/execute.md | No empty-argument handling | -10 |
| 24 | plugins/kiro-skill/commands/kiro/design.md | No `allowed-tools` in frontmatter | -5 |
| 25 | plugins/kiro-skill/commands/kiro/design.md | No empty-argument handling | -10 |
| 26 | skills/skill-creator/SKILL.md | Vague quantifiers ×10+ ("appropriate", "relevant", "realistic") | -20 (capped) |
| 27 | skills/command-creator/SKILL.md | Vague quantifiers ×6 ("appropriate" ×3, "proper" ×2, "relevant" ×1) | -12 |
| 28 | skills/github-review-pr/SKILL.md | Vague quantifiers ×4 ("appropriate", "relevant") | -8 |
| 29 | skills/reflection/SKILL.md | Vague quantifiers ×4 ("appropriate", "comprehensive", "thorough") | -8 |
| 30 | skills/deep-research/SKILL.md | Vague quantifiers ×4 ("appropriate" in Chinese context, "relevant") | -8 |
| 31 | skills/autonomous-skill/SKILL.md | Vague quantifiers ×3 ("appropriate", "relevant") | -6 |
| 32 | skills/eureka/SKILL.md | Vague quantifiers ×3 ("relevant" ×2, "appropriate" ×1) | -6 |
| 33 | skills/codex-skill/SKILL.md | Vague quantifiers ×3 ("appropriate", "relevant") | -6 |
| 34 | skills/github-fix-issue/SKILL.md | Vague quantifiers ×4 ("appropriate", "relevant", "thorough") | -8 |
| 35 | skills/spec-kit-skill/SKILL.md | Vague quantifiers ×4 ("appropriate", "relevant") | -8 |

---

## Cross-Component

**Duplicate SKILL.md files**: Six skills are mirrored exactly between `skills/X/SKILL.md` and `plugins/X/skills/X/SKILL.md` (codex-skill, nanobanana-skill, spec-kit-skill, youtube-transcribe-skill, kiro-skill, autonomous-skill). This is intentional for dual deployment (standalone + plugin). No inconsistencies found — files are byte-identical.

**Triplicate hooks**: `hooks/hooks.json`, `plugins/autonomous-skill/skills/autonomous-skill/hooks/hooks.json`, and `skills/autonomous-skill/hooks/hooks.json` are all identical Stop hooks pointing to `stop-hook.sh`. The root `hooks/hooks.json` appears to serve as the project-level hook while the plugin-level copies are for when the skill is installed as a plugin. No contradiction, but the root-level hook means any user of this repo gets the autonomous loop hook globally, even without the autonomous-skill explicitly loaded.

**Broken helper references**:
- `skills/kiro-skill/SKILL.md` and `plugins/kiro-skill/skills/kiro-skill/SKILL.md` reference `helpers/kiro-identity.md` and `helpers/workflow-diagrams.md` — these files were not present in the scanned paths.
- `skills/spec-kit-skill/SKILL.md` references `helpers/detection-logic.md` — not present in the scanned paths.
These may exist in unscanned subdirectories; if absent, the links are broken references.

**Sub-agent frontmatter gap**: `skill-creator/agents/analyzer.md`, `grader.md`, `comparator.md` are loaded by the skill-creator skill via explicit path (`agents/grader.md`, etc.) rather than by name lookup, so they function operationally. However, they lack proper YAML frontmatter, making them invisible to NLPM scanners and Claude Code's agent registry.

---

## Recommendation

CLEAR — submit PRs for all bugs and medium/low security fixes.

**Priority order for PRs**:
1. Add YAML frontmatter to the three skill-creator sub-agents (analyzer, grader, comparator) — straightforward 3-line additions.
2. Fix `bypassPermissions` default in `run-session.sh` — change default to `"default"` and make bypass an explicit opt-in.
3. Pin `chrome-devtools-mcp` version in `.mcp.json` and remove `--autoConnect`.
4. Add `allowed-tools` declarations to the five kiro commands.
5. Add `model` declarations to the seven root agents (haiku for mechanical agents, sonnet for complex ones).
6. Add one example block each to the seven root agents.
