# NLPM Audit: EveryInc/compound-engineering-plugin
**Date**: 2026-04-12  |  **Artifacts**: 114  |  **Strategy**: full-read
**NL Score**: 84/100
**Security**: CLEAR
**Bugs**: 10  |  **Quality Issues**: 22  |  **Security Findings**: 3

## NL Score Summary

Only artifacts scoring below 95 are listed (items at 95+ have no notable issues).

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| plugins/coding-tutor/commands/sync-tutorials.md | command | 40 | No YAML frontmatter (missing name, description, allowed-tools, multi-step without numbered steps) |
| plugins/coding-tutor/commands/teach-me.md | command | 45 | No YAML frontmatter (missing name, description, allowed-tools) |
| plugins/coding-tutor/commands/quiz-me.md | command | 45 | No YAML frontmatter (missing name, description, allowed-tools) |
| tests/fixtures/custom-paths/agents/default-agent.md | agent | 55 | Missing description (-25), missing examples (-15), missing model (-5) |
| tests/fixtures/custom-paths/commands/default-command.md | command | 70 | Missing description (-25), missing allowed-tools (-5) |
| tests/fixtures/custom-paths/custom-skills/custom-skill/SKILL.md | skill | 75 | Missing description (-25) |
| tests/fixtures/custom-paths/skills/default-skill/SKILL.md | skill | 75 | Missing description (-25) |
| plugins/compound-engineering/skills/git-worktree/SKILL.md | skill | 75 | Uses ${CLAUDE_PLUGIN_ROOT} throughout without fallback (violates cross-platform variable rules) |
| plugins/coding-tutor/skills/coding-tutor/SKILL.md | skill | 75 | Uses ${CLAUDE_PLUGIN_ROOT} throughout without fallback (violates cross-platform variable rules) |
| tests/fixtures/sample-plugin/agents/agent-one.md | agent | 75 | Frontmatter name is `repo-research-analyst` but filename is `agent-one.md` (mismatch); no examples (-15) |
| plugins/compound-engineering/agents/research/learnings-researcher.md | agent | 75 | Cross-skill reference `../../skills/ce-compound/references/yaml-schema.md` violates self-contained skill rules; no examples (-15) |
| plugins/compound-engineering/agents/review/data-integrity-guardian.md | agent | 75 | No output format (-10), no examples (-15) |
| plugins/compound-engineering/agents/review/security-sentinel.md | agent | 75 | No output format (-10), no examples (-15) |
| plugins/compound-engineering/agents/review/cli-agent-readiness-reviewer.md | agent | 80 | Missing model field (-5), no examples (-15) |
| plugins/compound-engineering/agents/docs/ankane-readme-writer.md | agent | 75 | No output format (-10), no examples (-15) |
| plugins/compound-engineering/agents/document-review/coherence-reviewer.md | agent | 75 | No output format section (-10), no examples (-15) |
| plugins/compound-engineering/agents/document-review/design-lens-reviewer.md | agent | 75 | No output format section (-10), no examples (-15) |
| plugins/compound-engineering/agents/document-review/feasibility-reviewer.md | agent | 75 | No output format section (-10), no examples (-15) |
| plugins/compound-engineering/agents/document-review/security-lens-reviewer.md | agent | 75 | No output format section (-10), no examples (-15) |
| plugins/compound-engineering/agents/document-review/scope-guardian-reviewer.md | agent | 75 | No output format section (-10), no examples (-15) |
| plugins/compound-engineering/agents/document-review/adversarial-document-reviewer.md | agent | 75 | No output format section (-10), no examples (-15) |
| plugins/compound-engineering/agents/document-review/product-lens-reviewer.md | agent | 75 | No output format section (-10), no examples (-15) |
| plugins/compound-engineering/agents/review/data-migration-expert.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/architecture-strategist.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/correctness-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/pattern-recognition-specialist.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/security-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/cli-readiness-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/kieran-rails-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/schema-drift-detector.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/adversarial-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/performance-oracle.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/code-simplicity-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/data-migrations-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/deployment-verification-agent.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/agent-native-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/kieran-python-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/reliability-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/testing-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/maintainability-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/performance-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/previous-comments-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/project-standards-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/dhh-rails-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/kieran-typescript-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/api-contract-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/review/julik-frontend-races-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/research/best-practices-researcher.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/research/slack-researcher.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/research/repo-research-analyst.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/research/session-historian.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/research/framework-docs-researcher.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/research/issue-intelligence-analyst.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/research/git-history-analyzer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/design/design-implementation-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/design/figma-design-sync.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/design/design-iterator.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/workflow/spec-flow-analyzer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/agents/workflow/pr-comment-resolver.md | agent | 85 | No examples (-15) |
| tests/fixtures/sample-plugin/agents/security-reviewer.md | agent | 85 | No examples (-15) |
| plugins/compound-engineering/skills/deploy-docs/SKILL.md | skill | 85 | Uses shell `ls \| wc -l` for file counting instead of native file-search tools (violates AGENTS.md native tool preference) |
| plugins/compound-engineering/skills/git-clean-gone-branches/SKILL.md | skill | 87 | Uses markdown link `[scripts/clean-gone](./scripts/clean-gone)` instead of backtick path (violates AGENTS.md skill compliance checklist) |
| plugins/compound-engineering/skills/changelog/SKILL.md | skill | 88 | Outbound Discord webhook curl call (medium security surface) |
| plugins/compound-engineering/skills/lfg/SKILL.md | skill | 88 | Minor: refers to `/todo-resolve` with slash syntax instead of semantic skill reference |
| plugins/compound-engineering/skills/ce-update/SKILL.md | skill | 88 | ce_platforms:[claude] restricts to Claude Code only; cross-platform portability limited |
| plugins/compound-engineering/skills/claude-permissions-optimizer/SKILL.md | skill | 88 | Minor: only runs on Claude Code sessions by design; no explicit cross-platform note |
| plugins/compound-engineering/skills/ce-compound/SKILL.md | skill | 92 | None significant |
| plugins/compound-engineering/skills/resolve-pr-feedback/SKILL.md | skill | 92 | None significant |
| plugins/compound-engineering/skills/proof/SKILL.md | skill | 92 | None significant |
| plugins/compound-engineering/skills/git-commit-push-pr/SKILL.md | skill | 92 | None significant |
| plugins/compound-engineering/skills/ce-review/SKILL.md | skill | 92 | None significant |
| plugins/compound-engineering/skills/ce-debug/SKILL.md | skill | 92 | None significant |
| plugins/compound-engineering/skills/document-review/SKILL.md | skill | 92 | None significant |
| plugins/compound-engineering/skills/ce-work/SKILL.md | skill | 92 | None significant |
| plugins/compound-engineering/skills/report-bug-ce/SKILL.md | skill | 92 | None significant |
| plugins/compound-engineering/skills/todo-create/SKILL.md | skill | 92 | None significant |
| plugins/compound-engineering/.claude-plugin/plugin.json | json | 95 | None significant |
| .claude-plugin/marketplace.json | json | 95 | None significant |
| tests/fixtures/sample-plugin/hooks/hooks.json | hook | 90 | Valid config; broad trigger scope (all 13 event types) — higher hook noise surface |
| tests/fixtures/custom-paths/hooks/hooks.json | hook | 95 | Valid minimal config |

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
| Hooks JSON | tests/fixtures/sample-plugin/hooks/hooks.json, tests/fixtures/custom-paths/hooks/hooks.json |
| Python scripts (coding-tutor) | plugins/coding-tutor/skills/coding-tutor/scripts/create_tutorial.py, setup_tutorials.py, quiz_priority.py, index_tutorials.py |
| Python scripts (session history) | plugins/compound-engineering/agents/research/session-history-scripts/extract-metadata.py, extract-errors.py, extract-skeleton.py |
| Shell scripts | plugins/compound-engineering/agents/research/session-history-scripts/discover-sessions.sh, plugins/compound-engineering/skills/git-worktree/scripts/worktree-manager.sh, plugins/compound-engineering/skills/ce-review/references/resolve-base.sh |
| Python scripts (gemini-imagegen) | plugins/compound-engineering/skills/gemini-imagegen/scripts/gemini_images.py, compose_images.py, multi_turn_chat.py, edit_image.py, generate_image.py |
| Python script (capture-demo) | plugins/compound-engineering/skills/ce-demo-reel/scripts/capture-demo.py |
| Node scripts | plugins/compound-engineering/skills/claude-permissions-optimizer/scripts/extract-commands.mjs, normalize.mjs, plugins/compound-engineering/skills/onboarding/scripts/inventory.mjs |
| MCP config (fixture) | tests/fixtures/mcp-file/.mcp.json |

### Security Findings

| # | Severity | File | Pattern | Description |
|---|----------|------|---------|-------------|
| 1 | MEDIUM | plugins/compound-engineering/skills/ce-demo-reel/scripts/capture-demo.py | External upload (catbox.moe/litterbox) | Script uploads captured evidence artifacts to catbox.moe (permanent) and litterbox.catbox.moe (1h expiry). Content uploaded is user-initiated demo recordings, not session data, but represents an unmediated third-party data transfer surface. No credential exfil risk; no user-controlled input fed unsanitized to the upload. Low practical risk but worth documenting for users who work in air-gapped or data-sensitive environments. |
| 2 | MEDIUM | plugins/compound-engineering/agents/research/session-history-scripts/discover-sessions.sh | Session data access | Reads `~/.claude/projects/*.jsonl`, `~/.codex/sessions/*.jsonl`, and `~/.cursor/projects/*/agent-transcripts/*.jsonl` — full session transcript files from three AI coding agents. This is the intended behavior for the `session-historian` research agent. Risk is contextual: if a developer has sensitive prompts or keys in session history, this script surfaces them to the AI agent reading them. No exfiltration — data stays local. |
| 3 | LOW | plugins/compound-engineering/skills/changelog/SKILL.md | Outbound network call (Discord webhook) | Skill documents a `curl` POST to a Discord webhook URL as part of the changelog notification workflow. The URL is expected to be user-configured; no hardcoded tokens observed. Low risk; documented behavior. |

## Bugs (PR-worthy)

Bugs 7–10 are in `tests/fixtures/custom-paths/` — these appear to be **intentional incomplete fixtures** for testing the converter/validator (the repo contains a full test suite). They should not be treated as production defects requiring a PR. Bugs 1–6 are production issues.

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | plugins/coding-tutor/commands/teach-me.md | No YAML frontmatter — missing name, description, allowed-tools | Command cannot be registered; `/teach-me` will fail to resolve from the plugin registry |
| 2 | plugins/coding-tutor/commands/sync-tutorials.md | No YAML frontmatter — missing name, description, allowed-tools | Command cannot be registered; `/sync-tutorials` will fail to resolve |
| 3 | plugins/coding-tutor/commands/quiz-me.md | No YAML frontmatter — missing name, description, allowed-tools | Command cannot be registered; `/quiz-me` will fail to resolve |
| 4 | plugins/compound-engineering/agents/research/learnings-researcher.md | Cross-skill path reference `../../skills/ce-compound/references/yaml-schema.md` violates AGENTS.md self-contained-skill rule | Path will not resolve at runtime (CWD is never the skill directory); path also breaks after install because versioned marketplace cache paths differ. Referenced file is inaccessible to the agent. |
| 5 | plugins/compound-engineering/skills/git-worktree/SKILL.md | Uses `${CLAUDE_PLUGIN_ROOT}` in all script invocations without fallback | Skill is Claude Code-only by accident: `${CLAUDE_PLUGIN_ROOT}` is unset in Codex, Gemini CLI, and other platforms, causing all `worktree-manager.sh` calls to expand to blank paths and fail silently. AGENTS.md explicitly forbids this without a fallback. |
| 6 | plugins/coding-tutor/skills/coding-tutor/SKILL.md | Uses `${CLAUDE_PLUGIN_ROOT}` in all script invocations without fallback | Same issue as Bug #5: all `python3 ${CLAUDE_PLUGIN_ROOT}/skills/coding-tutor/scripts/*.py` invocations will fail on non-Claude-Code platforms. |
| 7 | tests/fixtures/custom-paths/commands/default-command.md | Missing description field | Fixture: breaks registration in converter output; likely intentional test case |
| 8 | tests/fixtures/custom-paths/agents/default-agent.md | Missing description field | Fixture: breaks registration in converter output; likely intentional test case |
| 9 | tests/fixtures/custom-paths/custom-skills/custom-skill/SKILL.md | Missing description field | Fixture: breaks registration in converter output; likely intentional test case |
| 10 | tests/fixtures/custom-paths/skills/default-skill/SKILL.md | Missing description field | Fixture: breaks registration in converter output; likely intentional test case |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | ALL 52 agents (compound-engineering + fixtures) | Zero concrete examples in every agent definition — no input/output samples showing expected behavior | -15 each |
| 2 | plugins/compound-engineering/agents/document-review/coherence-reviewer.md | No output format section | -10 |
| 3 | plugins/compound-engineering/agents/document-review/design-lens-reviewer.md | No output format section | -10 |
| 4 | plugins/compound-engineering/agents/document-review/feasibility-reviewer.md | No output format section | -10 |
| 5 | plugins/compound-engineering/agents/document-review/security-lens-reviewer.md | No output format section | -10 |
| 6 | plugins/compound-engineering/agents/document-review/scope-guardian-reviewer.md | No output format section | -10 |
| 7 | plugins/compound-engineering/agents/document-review/adversarial-document-reviewer.md | No output format section | -10 |
| 8 | plugins/compound-engineering/agents/document-review/product-lens-reviewer.md | No output format section | -10 |
| 9 | plugins/compound-engineering/agents/review/data-integrity-guardian.md | No output format section | -10 |
| 10 | plugins/compound-engineering/agents/review/security-sentinel.md | No output format section | -10 |
| 11 | plugins/compound-engineering/agents/docs/ankane-readme-writer.md | No output format section | -10 |
| 12 | plugins/compound-engineering/agents/review/cli-agent-readiness-reviewer.md | No model field (not even `model: inherit`) | -5 |
| 13 | tests/fixtures/sample-plugin/agents/agent-one.md | Frontmatter `name: repo-research-analyst` does not match filename `agent-one.md` | Confusing for tooling that keys on filename vs name field |
| 14 | plugins/compound-engineering/skills/deploy-docs/SKILL.md | Uses `ls | wc -l` shell commands for counting agents/skills instead of native file-search tools | Violates AGENTS.md native tool preference; causes unnecessary permission prompts in sub-agent workflows |
| 15 | plugins/compound-engineering/skills/git-clean-gone-branches/SKILL.md | References script with markdown link `[scripts/clean-gone](./scripts/clean-gone)` instead of backtick path | Violates AGENTS.md skill compliance checklist: "Do NOT use markdown links" for file references |
| 16 | plugins/compound-engineering/skills/lfg/SKILL.md | References `/todo-resolve` with slash syntax inside a pass-through SKILL.md | Per AGENTS.md, slash syntax inside pass-through skills may not be remapped for other platforms; prefer semantic reference "load the `todo-resolve` skill" |
| 17 | plugins/compound-engineering/skills/changelog/SKILL.md | Outbound Discord webhook curl in skill body with no user-configuration note | Medium privacy/network surface (noted in Security Findings #3); also a quality issue as the webhook URL is presented as a hardcoded example |
| 18 | plugins/compound-engineering/skills/ce-update/SKILL.md | `ce_platforms: [claude]` restricts to Claude Code only — not cross-platform | Intentional but undocumented: no note in skill body explaining why it's Claude-only or what to do on other platforms |
| 19 | plugins/compound-engineering/agents/review/security-sentinel.md | Uses `grep -r` shell commands for pattern scanning instead of native content-search tools | Minor: should prefer the native content-search/Grep tool to avoid shell permission prompts |
| 20 | tests/fixtures/sample-plugin/hooks/hooks.json | Registers hooks for all 13 event types (PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest, UserPromptSubmit, Notification, SessionStart, SessionEnd, Stop, PreCompact, Setup, SubagentStart, SubagentStop) | Broad hook coverage is likely a completeness fixture, but in production would add noise and increase prompt-injection surface from hook event data |
| 21 | plugins/coding-tutor/commands/teach-me.md | Multi-step command body with no numbered steps | -10 (in addition to no-frontmatter bugs) |
| 22 | plugins/coding-tutor/commands/sync-tutorials.md | Multi-step command body with no numbered steps | -10 (in addition to no-frontmatter bugs) |
