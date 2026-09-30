---
artifact: agents/scanner.md
type: agent
min_score: 85
---

## Frontmatter Valid

Required fields:
- description: present with at least one example block and a "Not for" sentence, ≤ 1,200 characters
- model: haiku
- tools: includes Read, Glob (no Write, Edit, or Grep — scanner uses Glob for discovery and Read for line counting; grep-style content matching is not required)
- skills: includes nlpm:conventions

## Triggers On

Queries that SHOULD trigger this agent:

- "discover NL artifacts in this project"
- "inventory all plugin components"
- "find all agents and commands in this directory"
- "scan this repo for NL programming artifacts"
- "what NL artifacts exist here"

## Does Not Trigger On

Queries that should NOT trigger this agent:

- "score this file"
- "fix the issues in my agent"
- "check cross-component consistency"
- "write a new skill"

## Output Contains

Expected elements in the output:

- Category A / Category B breakdown
- File count per component type (commands, agents, skills, hooks)
- Line counts per file
- Estimated token counts
- Total summary line
