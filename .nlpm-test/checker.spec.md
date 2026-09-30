---
artifact: agents/checker.md
type: agent
min_score: 85
---

## Frontmatter Valid

Required fields:
- description: present with at least one example block and a "Not for" sentence, ≤ 1,200 characters
- model: sonnet
- tools: includes Read, Glob, Grep (no Write or Edit)
- skills: includes nlpm:conventions

## Triggers On

Queries that SHOULD trigger this agent:

- "check cross-component consistency"
- "find broken references in this plugin"
- "are there orphaned partials"
- "verify all skill references resolve"

## Does Not Trigger On

Queries that should NOT trigger this agent:

- "score this file"
- "discover all artifacts"
- "fix the issues in my command"
- "count vague words"

## Output Contains

Expected elements in the output:

- Reference integrity section with checked/broken counts
- Orphaned components section
- Contradictions section
- Terminology section
- Verdict line (CLEAN or N issues found)
