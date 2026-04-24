# NLPM Re-Audit: shanraisshan/claude-code-best-practice

**Date**: 2026-04-24  |  **Artifacts**: 43  |  **Strategy**: batched
**NL Score**: 88/100
**Bugs**: 6  |  **Quality Issues**: 22

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `.claude/agents/workflows/best-practice/workflow-claude-settings-agent.md` | Agent | 66 | No examples (-15), read-only agent declares Write/Edit (-10), 3 vague quantifiers (-6) |
| `.claude/agents/weather-agent.md` | Agent | 69 | No examples (-15), read-only body declares Write/Edit (-10), multiple unused tools (-5) |
| `.claude/agents/time-agent.md` | Agent | 69 | No examples (-15), read-only body declares Write/Edit (-10), unused tools (-6) |
| `.claude/agents/development-workflows-research-agent.md` | Agent | 70 | No examples (-15), read-only body declares Write/Edit (-10) |
| `.claude/agents/workflows/best-practice/workflow-claude-subagents-agent.md` | Agent | 72 | No examples (-15), read-only body declares Write/Edit (-10) |
| `.claude/agents/workflows/best-practice/workflow-claude-skills-agent.md` | Agent | 72 | No examples (-15), read-only body declares Write/Edit (-10) |
| `.claude/agents/workflows/best-practice/workflow-concepts-agent.md` | Agent | 72 | No examples (-15), read-only body declares Write/Edit (-10) |
| `.claude/agents/workflows/best-practice/workflow-claude-commands-agent.md` | Agent | 72 | No examples (-15), read-only body declares Write/Edit (-10) |
| `development-workflows/rpi/.claude/agents/technical-cto-advisor.md` | Agent | 75 | No examples (-15), 5 vague quantifiers (-10) |
| `development-workflows/rpi/.claude/agents/constitutional-validator.md` | Agent | 75 | No examples (-15), 5 vague quantifiers (-10) |
| `development-workflows/rpi/.claude/agents/requirement-parser.md` | Agent | 76 | No examples (-15), no tools in frontmatter (-5), 2 vague quantifiers (-4) |
| `development-workflows/rpi/.claude/agents/documentation-analyst-writer.md` | Agent | 79 | No examples (-15), 3 vague quantifiers (-6) |
| `CLAUDE.md` | CLAUDE.md | 80 | No build/run command (-10), no test command (-5), no prerequisites section (-5) |
| `.claude/agents/presentation-learning-journey.md` | Agent | 81 | No examples (-15), 2 vague quantifiers (-4) |
| `.claude/agents/presentation-vibe-coding.md` | Agent | 85 | No examples (-15) |
| `development-workflows/rpi/.claude/agents/ux-designer.md` | Agent | 85 | No examples (-15) |
| `development-workflows/rpi/.claude/agents/product-manager.md` | Agent | 85 | No examples (-15) |
| `development-workflows/rpi/.claude/agents/senior-software-engineer.md` | Agent | 85 | No examples (-15) |
| `development-workflows/rpi/.claude/agents/code-reviewer.md` | Agent | 85 | No examples (-15) |
| `agent-teams/.claude/agents/time-agent.md` | Agent | 85 | No examples (-15) |
| `development-workflows/rpi/.claude/commands/rpi/implement.md` | Command | 92 | 4 vague quantifiers (-8) |
| `.claude/skills/weather-svg-creator/SKILL.md` | Skill | 95 | No inline code examples (-5) |
| `.claude/commands/workflows/best-practice/workflow-claude-settings.md` | Command | 96 | 2 vague quantifiers (-4) |
| `development-workflows/rpi/.claude/commands/rpi/plan.md` | Command | 96 | 2 vague quantifiers (-4) |
| `.claude/skills/time-skill/SKILL.md` | Skill | 97 | No scope note/cross-references (-3) |
| `.claude/skills/presentation/presentation-styling/SKILL.md` | Skill | 97 | No scope note/cross-references (-3) |
| `.claude/skills/presentation/presentation-structure/SKILL.md` | Skill | 97 | No scope note/cross-references (-3) |
| `.claude/skills/weather-fetcher/SKILL.md` | Skill | 97 | No scope note/cross-references (-3) |
| `agent-teams/.claude/skills/time-svg-creator/SKILL.md` | Skill | 97 | No scope note/cross-references (-3) |
| `agent-teams/.claude/skills/time-fetcher/SKILL.md` | Skill | 97 | No scope note/cross-references (-3) |
| `development-workflows/rpi/.claude/commands/rpi/research.md` | Command | 98 | 1 vague quantifier (-2) |
| `.claude/commands/time-command.md` | Command | 100 | None |
| `.claude/commands/workflows/development-workflows.md` | Command | 100 | None |
| `.claude/commands/workflows/best-practice/workflow-claude-skills.md` | Command | 100 | None |
| `.claude/commands/workflows/best-practice/workflow-claude-commands.md` | Command | 100 | None |
| `.claude/commands/workflows/best-practice/workflow-claude-subagents.md` | Command | 100 | None |
| `.claude/commands/workflows/best-practice/workflow-concepts.md` | Command | 100 | None |
| `.claude/commands/weather-orchestrator.md` | Command | 100 | None |
| `agent-teams/.claude/commands/time-orchestrator.md` | Command | 100 | None |
| `.claude/hooks/config/hooks-config.json` | Hook config | 100 | None |
| `.codex/hooks/config/hooks-config.json` | Hook config | 100 | None |
| `.claude/skills/agent-browser/SKILL.md` | Skill | 100 | None |
| `.claude/skills/presentation/vibe-to-agentic-framework/SKILL.md` | Skill | 100 | None |

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `.claude/agents/development-workflows-research-agent.md` | Write and Edit declared in `allowedTools` but body explicitly states "DO NOT modify any local files" — read-only agent with write-capable tools | Agent could silently edit files; misleading capability declaration |
| 2 | `.claude/agents/weather-agent.md` | Write and Edit declared in `allowedTools` but body states "not to write files or create outputs" — read-only operation declares write tools | Agent could silently modify files contrary to stated intent |
| 3 | `.claude/agents/time-agent.md` | Write, Edit, Glob, Grep, WebFetch, WebSearch, Agent, NotebookEdit, mcp__* declared but body uses only Bash — massive tool over-declaration on a trivial agent | Security surface area far exceeds task requirements |
| 4 | `.claude/agents/workflows/best-practice/workflow-claude-subagents-agent.md` | Write and Edit declared but body says "Do NOT modify any files" | Read-only research agent with write tools |
| 5 | `.claude/agents/workflows/best-practice/workflow-claude-skills-agent.md` | Write and Edit declared but body says "Do NOT modify any files" | Read-only research agent with write tools |
| 6 | `.claude/agents/workflows/best-practice/workflow-claude-commands-agent.md` | Write and Edit declared but body says "Do NOT modify any files" | Read-only research agent with write tools |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | All 19 agents | Zero `<example>` blocks — triggering is unreliable without examples | -15 each |
| 2 | `.claude/agents/workflows/best-practice/workflow-concepts-agent.md` | Write and Edit declared but body is read-only | -10 |
| 3 | `.claude/agents/workflows/best-practice/workflow-claude-settings-agent.md` | Write and Edit declared but body is read-only; 3 vague quantifiers ("appropriate", "relevant", "comprehensive") | -10, -6 |
| 4 | `development-workflows/rpi/.claude/agents/technical-cto-advisor.md` | 5 vague quantifiers ("appropriate", "relevant", "comprehensive", "several", "various") | -10 |
| 5 | `development-workflows/rpi/.claude/agents/constitutional-validator.md` | 5 vague quantifiers ("appropriate", "relevant", "sufficient", "several", "various") | -10 |
| 6 | `CLAUDE.md` | No build/run command (reference repo, but rubric applies); no test command; no prerequisites section | -20 total |
| 7 | `development-workflows/rpi/.claude/agents/requirement-parser.md` | Tools listed in body text but no `tools:` or `allowedTools:` frontmatter field; 2 vague quantifiers | -5, -4 |
| 8 | `development-workflows/rpi/.claude/agents/documentation-analyst-writer.md` | 3 vague quantifiers ("appropriate", "relevant", "comprehensive") | -6 |
| 9 | `development-workflows/rpi/.claude/commands/rpi/implement.md` | 4 vague quantifiers ("appropriate", "relevant", "sufficient", "several") | -8 |
| 10 | `.claude/commands/workflows/best-practice/workflow-claude-settings.md` | 2 vague quantifiers | -4 |
| 11 | `development-workflows/rpi/.claude/commands/rpi/plan.md` | 2 vague quantifiers | -4 |
| 12 | `development-workflows/rpi/.claude/commands/rpi/research.md` | 1 vague quantifier | -2 |
| 13 | `.claude/agents/presentation-learning-journey.md` | 2 vague quantifiers ("appropriate", "relevant") | -4 |
| 14 | `.claude/skills/weather-svg-creator/SKILL.md` | No inline code examples — references external reference.md instead of showing patterns inline | -5 |
| 15 | `.claude/skills/time-skill/SKILL.md` | No scope note / cross-references to related skills | -3 |
| 16 | `.claude/skills/presentation/presentation-styling/SKILL.md` | No scope note linking to presentation-structure or vibe-to-agentic-framework | -3 |
| 17 | `.claude/skills/presentation/presentation-structure/SKILL.md` | No scope note linking to presentation-styling or vibe-to-agentic-framework | -3 |
| 18 | `.claude/skills/weather-fetcher/SKILL.md` | No scope note / cross-references (e.g., "For SVG output, see weather-svg-creator") | -3 |
| 19 | `agent-teams/.claude/skills/time-svg-creator/SKILL.md` | No scope note / cross-references | -3 |
| 20 | `agent-teams/.claude/skills/time-fetcher/SKILL.md` | No scope note / cross-references | -3 |
| 21 | `development-workflows/rpi/.claude/agents/technical-cto-advisor.md` | No `tools:` or `allowedTools:` frontmatter; agent does complex analysis but tools are not bounded | No penalty (tools absent = inherits all, rubric only penalizes declared unused) |
| 22 | `.claude/agents/development-workflows-research-agent.md` | `NotebookEdit` declared but body never mentions notebook operations | -3 |

## Cross-Component

**Read-only pattern inconsistency**: The workflow research agents (workflow-claude-subagents-agent, workflow-claude-skills-agent, workflow-claude-concepts-agent, workflow-claude-settings-agent, workflow-claude-commands-agent, development-workflows-research-agent, weather-agent) all declare Write and Edit in `allowedTools` despite their bodies explicitly prohibiting file modification. This appears to be a copy-paste default tool list applied to all agents rather than per-agent least-privilege lists.

**Agent tool list standardization**: All agents in `.claude/agents/` share an identical boilerplate `allowedTools` block (Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Agent, NotebookEdit, mcp__*). The tool set is never tailored to the agent's actual needs. This increases security surface area and introduces the Read-only/Write contradiction pattern.

**Missing examples across the board**: None of the 19 agents have `<example>` blocks. This is a systemic gap, not isolated failures. Without examples, Claude Code auto-invocation is unreliable for all agents.

**RPI workflow agent coordination**: The `development-workflows/rpi/` workflow correctly chains requirement-parser → product-manager → senior-software-engineer → technical-cto-advisor → documentation-analyst-writer. All agents are defined and cross-referenced consistently. No broken agent references detected.

**Presentation skill cross-references**: `presentation-vibe-coding` agent correctly references `presentation/vibe-to-agentic-framework`, `presentation/presentation-structure`, and `presentation/presentation-styling` skills. All three skills exist at the expected paths.

**Weather workflow**: Command → agent → skill chain (`weather-orchestrator` → `weather-agent` → `weather-fetcher` + `weather-svg-creator`) is fully consistent. All referenced files exist.

**Time workflow**: `time-orchestrator` → `time-agent` (agent-teams) → `time-fetcher` skill; `time-svg-creator` skill. All files present and consistent.

## Recommendation

The command and skill layers are excellent (averaging 98/100) but all 19 agents lack `<example>` blocks and the boilerplate allowedTools lists contradict the read-only intent of research agents — fixing examples and applying least-privilege tool lists to each agent would bring the portfolio above 92/100.
