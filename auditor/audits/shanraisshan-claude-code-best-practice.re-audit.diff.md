# Re-Audit: shanraisshan/claude-code-best-practice

**Date**: 2026-04-24  |  **Before**: `unknown` (88/100)  |  **After**: `13cbf08` (88/100)

## Summary

| Outcome | Count |
|---------|------:|
| fixed — our PR merged | 6 |
| fixed — upstream, not via our PR | 21 |
| newly introduced (regressions) | 50 |

## Original findings — verification

| # | File | Line | Rule | Pattern | Outcome | PR |
|---|------|------|------|---------|---------|----|
| 1 | `agent-teams/.claude/commands/time-orchestrator.md` | — | BUG-missing-frontmatter | `missing-description` | fixed — our PR merged | #63 |
| 2 | `.claude/agents/development-workflows-research-agent.md` | — | CC-name-collision | `name-collision` | fixed — upstream, not via our PR | #64 |
| 3 | `.claude/agents/workflows/development-workflows-research-agent.md` | — | CC-name-collision | `name-collision` | fixed — upstream, not via our PR |  |
| 4 | `.claude/agents/time-agent.md` | — | BUG-unclassified | `both-declare-name-time-agent-with-differ` | fixed — our PR merged | #65 |
| 5 | `agent-teams/.claude/agents/time-agent.md` | — | BUG-unclassified | `both-declare-name-time-agent-with-differ` | fixed — upstream, not via our PR |  |
| 6 | `.mcp.json` | — | SEC-unknown | `npx-y-playwright-mcp-no-version-pin` | fixed — our PR merged | #67 |
| 7 | `.mcp.json` | — | SEC-unknown | `npx-y-deepwiki-mcp-unknown-package-no-pi` | fixed — our PR merged | #67 |
| 8 | `.claude/hooks/scripts/hooks.py` | — | SEC-unknown | `subprocess-popen-resolves-audio-player-f` | fixed — upstream, not via our PR |  |
| 9 | `.claude/hooks/scripts/hooks.py` | — | SEC-unknown | `hook-log-may-persist-sensitive-tool-inpu` | fixed — upstream, not via our PR |  |
| 10 | `All 20 agents` | — | R09 | `no-examples` | fixed — upstream, not via our PR |  |
| 11 | `.claude/agents/development-workflows-research-agent.md` | — | BUG-read-only-write | `write-edit-on-readonly` | fixed — upstream, not via our PR | #64 |
| 12 | `.claude/agents/weather-agent.md` | — | UNCLASSIFIED | `body-says-not-to-write-files-or-create-o` | fixed — upstream, not via our PR |  |
| 13 | `.claude/agents/time-agent.md` | — | UNCLASSIFIED | `single-purpose-time-agent-runs-one-bash` | fixed — our PR merged | #65 |
| 14 | `workflows/best-practice/*-agent.md` | — | UNCLASSIFIED | `all-five-workflow-research-agents-declar` | fixed — upstream, not via our PR |  |
| 15 | `.claude/agents/presentation-vibe-coding.md` | — | BUG-unused-tool | `unused-tools` | fixed — upstream, not via our PR |  |
| 16 | `.claude/agents/presentation-learning-journey.md` | — | BUG-unused-tool | `unused-tools` | fixed — upstream, not via our PR |  |
| 17 | `agent-teams/.claude/commands/time-orchestrator.md` | — | BUG-undeclared-tool | `missing-allowed-tools` | fixed — our PR merged | #63 |
| 18 | `All 8 standalone commands` | — | BUG-undeclared-tool | `missing-allowed-tools` | fixed — upstream, not via our PR |  |
| 19 | `development-workflows/rpi/.claude/commands/rpi/plan.md` | — | R01 | `vague-quantifiers` | fixed — upstream, not via our PR |  |
| 20 | `development-workflows/rpi/.claude/commands/rpi/research.md` | — | R01 | `vague-quantifiers` | fixed — upstream, not via our PR |  |
| 21 | `development-workflows/rpi/.claude/commands/rpi/implement.md` | — | R01 | `vague-quantifiers` | fixed — upstream, not via our PR |  |
| 22 | `development-workflows/rpi/.claude/agents/requirement-parser.md` | — | R01 | `vague-quantifiers` | fixed — upstream, not via our PR |  |
| 23 | `development-workflows/rpi/.claude/agents/technical-cto-advisor.md` | — | R01 | `vague-quantifiers` | fixed — upstream, not via our PR |  |
| 24 | `development-workflows/rpi/.claude/agents/constitutional-validator.md` | — | R01 | `vague-quantifiers` | fixed — upstream, not via our PR |  |
| 25 | `development-workflows/rpi/.claude/agents/documentation-analyst-writer.md` | — | R01 | `vague-quantifiers` | fixed — upstream, not via our PR |  |
| 26 | `development-workflows/rpi/.claude/agents/*.md` | — | UNCLASSIFIED | `no-allowedtools-in-frontmatter-tools-ava` | fixed — upstream, not via our PR |  |
| 27 | `Repo-wide agents` | — | UNCLASSIFIED | `inconsistent-frontmatter-format-root-sco` | fixed — upstream, not via our PR |  |

## Findings introduced since audit

These findings appear in the re-audit but were not in the original audit. They may be true regressions (new commits introduced them) or artifacts of scoring drift.

| # | File | Line | Rule | Pattern | Description |
|---|------|------|------|---------|-------------|
| 1 | `.claude/agents/development-workflows-research-agent.md` | 8 | R11 | `allowedTools includes Write and Edit; body states 'DO NOT modify any local files'` | Read-only research agent declares Write and Edit in allowedTools, contradicting the body's explicit prohibition on file modification. This is a least-privilege violation. |
| 2 | `.claude/agents/weather-agent.md` | 8 | R11 | `allowedTools includes Write and Edit; body states 'not to write files or create outputs'` | Read-only data-fetching agent declares Write and Edit in allowedTools despite body explicitly stating 'your job is to fetch and return the temperature — not to write files or create outputs'. |
| 3 | `.claude/agents/time-agent.md` | 8 | R11 | `allowedTools contains 11 tools; body only uses Bash` | Trivial time-fetching agent (runs one bash command) declares Write, Edit, Glob, Grep, WebFetch, WebSearch, Agent, NotebookEdit, mcp__* — all unused. Write and Edit on a body-level read-only agent violates R11. |
| 4 | `.claude/agents/workflows/best-practice/workflow-claude-subagents-agent.md` | 8 | R11 | `allowedTools includes Write and Edit; body says 'Do NOT modify any files'` | Read-only drift-detection research agent declares Write and Edit in allowedTools, contradicting the body's explicit no-modification instruction. |
| 5 | `.claude/agents/workflows/best-practice/workflow-claude-skills-agent.md` | 8 | R11 | `allowedTools includes Write and Edit; body says 'Do NOT modify any files'` | Read-only drift-detection research agent declares Write and Edit in allowedTools, contradicting the body's explicit no-modification instruction. |
| 6 | `.claude/agents/workflows/best-practice/workflow-claude-commands-agent.md` | 8 | R11 | `allowedTools includes Write and Edit; body says 'Do NOT modify any files'` | Read-only drift-detection research agent declares Write and Edit in allowedTools, contradicting the body's explicit no-modification instruction. |
| 7 | `.claude/agents/development-workflows-research-agent.md` | — | R09 | `Zero <example> blocks in agent frontmatter/description` | No <example> blocks found. Without at least 2 examples showing context, user message, and assistant response, auto-triggering is unreliable. |
| 8 | `.claude/agents/presentation-vibe-coding.md` | — | R09 | `Zero <example> blocks` | No <example> blocks found. This presentation-editing agent has complex trigger conditions but no examples to guide auto-invocation. |
| 9 | `.claude/agents/presentation-learning-journey.md` | — | R09 | `Zero <example> blocks` | No <example> blocks found. The description says 'PROACTIVELY use this agent' but without examples the triggering criteria are ambiguous. |
| 10 | `.claude/agents/weather-agent.md` | — | R09 | `Zero <example> blocks` | No <example> blocks found in weather-agent. The description says 'Use this agent PROACTIVELY' but without examples triggering may be unreliable. |
| 11 | `.claude/agents/time-agent.md` | — | R09 | `Zero <example> blocks` | No <example> blocks found in root-scope time-agent. |
| 12 | `.claude/agents/workflows/best-practice/workflow-claude-subagents-agent.md` | — | R09 | `Zero <example> blocks` | Research agent with no examples. Triggering is unreliable. |
| 13 | `.claude/agents/workflows/best-practice/workflow-claude-skills-agent.md` | — | R09 | `Zero <example> blocks` | Research agent with no examples. Triggering is unreliable. |
| 14 | `.claude/agents/workflows/best-practice/workflow-concepts-agent.md` | — | R09 | `Zero <example> blocks` | Research agent with no examples. Triggering is unreliable. |
| 15 | `.claude/agents/workflows/best-practice/workflow-claude-settings-agent.md` | — | R09 | `Zero <example> blocks` | Research agent with no examples. Triggering is unreliable. |
| 16 | `.claude/agents/workflows/best-practice/workflow-claude-commands-agent.md` | — | R09 | `Zero <example> blocks` | Research agent with no examples. Triggering is unreliable. |
| 17 | `development-workflows/rpi/.claude/agents/ux-designer.md` | — | R09 | `Zero <example> blocks` | No <example> blocks found. This agent has a minimal body and no examples. |
| 18 | `development-workflows/rpi/.claude/agents/technical-cto-advisor.md` | — | R09 | `Zero <example> blocks` | No <example> blocks found in technical-cto-advisor. Despite detailed body content, the triggering description lacks usage examples. |
| 19 | `development-workflows/rpi/.claude/agents/documentation-analyst-writer.md` | — | R09 | `Zero <example> blocks` | No <example> blocks found. Triggering is unreliable without examples. |
| 20 | `development-workflows/rpi/.claude/agents/product-manager.md` | — | R09 | `Zero <example> blocks` | No <example> blocks found. Triggering is unreliable without examples. |
| 21 | `development-workflows/rpi/.claude/agents/senior-software-engineer.md` | — | R09 | `Zero <example> blocks` | No <example> blocks found. Triggering is unreliable without examples. |
| 22 | `development-workflows/rpi/.claude/agents/code-reviewer.md` | — | R09 | `Zero <example> blocks` | No <example> blocks found. Triggering is unreliable without examples. |
| 23 | `development-workflows/rpi/.claude/agents/constitutional-validator.md` | — | R09 | `Zero <example> blocks` | No <example> blocks found. The extensive body defines a validation process but no triggering examples. |
| 24 | `development-workflows/rpi/.claude/agents/requirement-parser.md` | — | R09 | `Zero <example> blocks in description field (Scenarios in body do not count as <example> blocks)` | Body contains Scenario examples but these are not `<example>` blocks in the description field. Without `<example>` blocks, auto-triggering is unreliable. |
| 25 | `agent-teams/.claude/agents/time-agent.md` | — | R09 | `Zero <example> blocks` | No <example> blocks found. Triggering is unreliable without examples. |
| 26 | `.claude/agents/workflows/best-practice/workflow-concepts-agent.md` | 8 | R11 | `Write and Edit declared; body is read-only research` | Body explicitly states 'Do NOT take any actions or modify files' but Write and Edit appear in allowedTools. NotebookEdit also declared with no notebook operations in body. |
| 27 | `.claude/agents/workflows/best-practice/workflow-claude-settings-agent.md` | 8 | R11 | `Write and Edit declared; body is read-only research` | Body explicitly states 'Do NOT take any actions or modify files' but Write and Edit appear in allowedTools. |
| 28 | `.claude/agents/workflows/best-practice/workflow-claude-settings-agent.md` | — | R01 | `Vague quantifiers: 'appropriate', 'relevant', 'comprehensive'` | 3 occurrences of vague quantifiers without measurable criteria. |
| 29 | `development-workflows/rpi/.claude/agents/technical-cto-advisor.md` | — | R01 | `Vague quantifiers: 'appropriate', 'relevant', 'comprehensive', 'several', 'various' — 5 occurrences` | 5 vague quantifiers without measurable criteria, capped at -10. |
| 30 | `development-workflows/rpi/.claude/agents/constitutional-validator.md` | — | R01 | `Vague quantifiers: 'appropriate', 'relevant', 'sufficient', 'several', 'various' — 5 occurrences` | 5 vague quantifiers without measurable criteria, capped at -10. |
| 31 | `development-workflows/rpi/.claude/agents/requirement-parser.md` | — | R11 | `Tools listed in body text but no tools: or allowedTools: frontmatter field` | Body section 'Tools Available' lists Read, Grep, Glob, WebFetch but no tools frontmatter field is declared. Without frontmatter declaration, Claude Code cannot enforce tool restrictions. |
| 32 | `development-workflows/rpi/.claude/agents/requirement-parser.md` | — | R01 | `Vague quantifiers: 'appropriate', 'relevant' — 2 occurrences` | 2 vague quantifiers without measurable criteria. |
| 33 | `development-workflows/rpi/.claude/agents/documentation-analyst-writer.md` | — | R01 | `Vague quantifiers: 'appropriate', 'relevant', 'comprehensive' — 3 occurrences` | 3 vague quantifiers without measurable criteria. |
| 34 | `.claude/agents/presentation-learning-journey.md` | — | R01 | `Vague quantifiers: 'appropriate', 'relevant' — 2 occurrences` | 2 vague quantifiers without measurable criteria. |
| 35 | `CLAUDE.md` | — | R33 | `No build/run command documented` | CLAUDE.md does not include a build or run command. The repo is a reference implementation rather than an application, but the rubric applies regardless. No setup or run instructions present. |
| 36 | `CLAUDE.md` | — | R34 | `No test command documented` | CLAUDE.md has no instructions for running tests. No test command or test runner is mentioned. |
| 37 | `CLAUDE.md` | — | R35 | `No prerequisites section` | CLAUDE.md does not have a dedicated prerequisites section covering required tools, versions, or setup steps. |
| 38 | `development-workflows/rpi/.claude/commands/rpi/implement.md` | — | R01 | `Vague quantifiers: 'appropriate', 'relevant', 'sufficient', 'several' — 4 occurrences` | 4 vague quantifiers without measurable criteria. |
| 39 | `.claude/commands/workflows/best-practice/workflow-claude-settings.md` | — | R01 | `Vague quantifiers: 2 occurrences` | 2 vague quantifiers without measurable criteria. |
| 40 | `development-workflows/rpi/.claude/commands/rpi/plan.md` | — | R01 | `Vague quantifiers: 'appropriate', 'relevant' — 2 occurrences` | 2 vague quantifiers without measurable criteria. |
| 41 | `development-workflows/rpi/.claude/commands/rpi/research.md` | — | R01 | `Vague quantifier: 1 occurrence` | 1 vague quantifier without measurable criteria. |
| 42 | `.claude/skills/weather-svg-creator/SKILL.md` | — | R06 | `No inline code examples — references external reference.md` | The skill body delegates all examples to external reference.md and examples.md files rather than including inline runnable examples. For a technical SVG-creation skill this reduces standalone usability. |
| 43 | `.claude/skills/time-skill/SKILL.md` | — | R07 | `No scope note or cross-references to related skills` | Skill does not reference related skills (time-fetcher, time-svg-creator) or explain scope boundaries. |
| 44 | `.claude/skills/presentation/presentation-styling/SKILL.md` | — | R07 | `No scope note or cross-references` | Skill covers CSS classes but does not reference presentation-structure or vibe-to-agentic-framework skills. |
| 45 | `.claude/skills/presentation/presentation-structure/SKILL.md` | — | R07 | `No scope note or cross-references` | Skill covers slide format but does not reference presentation-styling or vibe-to-agentic-framework. |
| 46 | `.claude/skills/weather-fetcher/SKILL.md` | — | R07 | `No scope note or cross-references` | Skill fetches weather data but does not reference weather-svg-creator or weather-agent for the downstream workflow. |
| 47 | `agent-teams/.claude/skills/time-svg-creator/SKILL.md` | — | R07 | `No scope note or cross-references` | No scope note linking to time-fetcher or time-orchestrator workflow. |
| 48 | `agent-teams/.claude/skills/time-fetcher/SKILL.md` | — | R07 | `No scope note or cross-references` | No scope note linking to time-svg-creator or time-agent as downstream consumers. |
| 49 | `.claude/agents/` | — | CC-tool-list | `Boilerplate allowedTools block (11 tools) reused verbatim across all .claude/agents/ files` | All agents in .claude/agents/ share an identical allowedTools list. Multiple agents that are read-only by design declare Write and Edit. This is a systemic copy-paste pattern rather than per-agent least-privilege design. |
| 50 | `.claude/agents/` | — | CC-examples | `Zero <example> blocks across all 19 agents in the repository` | No agent in the entire repository defines <example> blocks. This is a systemic gap affecting all agents' reliability for auto-invocation by Claude Code. |

