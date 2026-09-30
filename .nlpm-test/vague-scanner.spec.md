---
artifact: agents/vague-scanner.md
type: agent
min_score: 85
---

## Frontmatter Valid

Required fields:
- description: present with at least one example block and a "Not for" sentence, ≤ 1,200 characters
- model: haiku
- tools: includes Read, Grep (no Write, Edit, or Glob)

## Triggers On

Queries that SHOULD trigger this agent:

- "scan for vague quantifiers"
- "count vague words in this file"
- "check for vague language"

## Does Not Trigger On

Queries that should NOT trigger this agent:

- "score this file on the 100-point scale"
- "check cross-component references"
- "discover all artifacts"
- "fix issues in my agent"

## Output Contains

Expected elements in the output:

- Per-file vague quantifier count
- Penalty calculation (-2 each, capped at -20)
- Line numbers for each occurrence
- The matched word
- Full line text for context
- Total summary across all files
