---
artifact: agents/scorer.md
type: agent
min_score: 90
---

## Frontmatter Valid

Required fields:
- description: present and trigger-style with 3+ specific phrases
- model: sonnet
- tools: includes Read, Glob, Grep (no Write or Edit)
- skills: includes nlpm:scoring, nlpm:conventions

## Triggers On

Queries that SHOULD trigger this agent:

- "score this agent file"
- "check the quality of my skill"
- "what's the score of commands/fix.md"
- "run quality analysis on this plugin"
- "score all artifacts in this directory"
- "identify issues in this command file"

## Does Not Trigger On

Queries that should NOT trigger this agent:

- "discover all NL artifacts in this repo"
- "check cross-component consistency"
- "write a new agent for dependency scanning"
- "run my test specs"
- "count vague words in this file"

## Output Contains

Expected elements in the output:

- Score out of 100 (e.g., "85/100")
- Severity classification (HIGH, MEDIUM, LOW)
- Rule numbers (R01-R51)
- Line numbers for each issue
- Penalty values
- Suggested fixes
- Table format with columns for severity, rule, line, issue, penalty, fix

## Does Not Invent Findings

Regression scenarios for hallucinated penalty categories. Each was observed
in the 2026-04-24 marketplace-wide audit; the rubric has no backing for any
of them.

### Scenario: Does not invent `namespace:` finding
Given a skill with valid frontmatter but no `namespace:` field
When scored
Then no finding mentions `namespace`
And final score is not reduced for missing namespace

### Scenario: Does not flag AskUserQuestion as undocumented
Given a command with `allowed-tools: AskUserQuestion, Read`
When scored
Then no finding flags AskUserQuestion
And tools field is treated as valid

### Scenario: Respects documented intentional omissions
Given agent X with no `skills:` field
And CLAUDE.md states "agent X has no skills by design"
When scored
Then no finding penalizes the missing skills field

### Scenario: Treats plugin.json component fields as paths
Given plugin.json with `"hooks": "hooks/hooks.json"` (a string, not an array)
When scored
Then no finding requests inline hook registration blocks

### Scenario: Does not require engines/minClaudeVersion/main in plugin.json
Given plugin.json without `engines:`, `minClaudeVersion:`, or `main:`
When scored
Then no finding requests any of these fields
And they are treated as undefined-in-schema (not "missing")
