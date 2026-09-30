---
artifact: agents/tester.md
type: agent
min_score: 85
---

## Frontmatter Valid

Required fields:
- description: present with at least one example block and a "Not for" sentence, ≤ 1,200 characters
- model: sonnet
- tools: includes Read, Glob, Grep (no Write or Edit)
- skills: includes nlpm:testing, nlpm:conventions, nlpm:scoring

## Triggers On

Queries that SHOULD trigger this agent:

- "run NL artifact tests"
- "check if my specs pass"
- "evaluate this agent against its test spec"
- "run the TDD specs"
- "test my artifacts against their specifications"

## Does Not Trigger On

Queries that should NOT trigger this agent:

- "score this file"
- "discover all artifacts"
- "fix the issues in my command"
- "check cross-component references"

## Output Contains

Expected elements in the output:

- PASS / FAIL / RED status per spec
- Score comparison (actual vs min_score)
- Check count (passed/total)
- Failed check details with fix suggestions
- Overall summary line
