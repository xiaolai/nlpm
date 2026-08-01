---
name: testing
description: "Use when writing test specs for NL artifacts, running /nlpm:test, or setting up TDD workflows for skills, agents, commands, rules, hooks, and prompts."
version: 0.1.0
---

## The NL-TDD Cycle

```
1. Write spec (.nlpm-test/artifact-name.spec.md)     — define expectations
2. /nlpm:test                                         — RED: spec fails (artifact doesn't exist)
3. Write the artifact                                 — create the NL artifact
4. /nlpm:test                                         — check if it passes
5. /nlpm:score                                        — check quality score
6. Iterate until GREEN: all specs pass + score ≥ threshold
```

## Spec File Format

Location: `.nlpm-test/` directory in the project root (or alongside the artifact).

Filename convention: `<artifact-name>.spec.md` — matches the artifact filename without path.

```yaml
---
artifact: agents/my-agent.md          # path to the artifact being tested
type: agent                           # agent | skill | command | rule | hook | prompt
min_score: 85                         # minimum /nlpm:score threshold for this artifact
---
```

Body sections (all optional — include what matters for this artifact):

### triggers_on (skills and agents)

```markdown
## Triggers On

Queries that SHOULD trigger this artifact:

- "review my database migrations before deploying"
- "check if these schema changes are safe"
- "audit the migration for breaking changes"
```

### does_not_trigger_on (skills and agents)

```markdown
## Does Not Trigger On

Queries that should NOT trigger this artifact:

- "write a migration for adding a users table"
- "help me with CSS styling"
- "deploy to production"
```

### output_contains (agents and commands)

```markdown
## Output Contains

Expected elements in the output:

- "## Migration Review" (heading present)
- "| Table | Change | Risk |" (table structure)
- severity classification (CRITICAL/HIGH/MEDIUM/LOW)
```

### output_format (agents and commands)

```markdown
## Output Format

The output should be a markdown report with:
1. Summary section with counts
2. Findings table with columns: File, Issue, Severity
3. Action items list
```

### handles_input (commands)

```markdown
## Handles Input

| Input | Expected Behavior |
|-------|------------------|
| (empty) | Score all artifacts in cwd |
| directory path | Score artifacts in that directory |
| nonexistent path | Error: "Directory not found: {path}" |
| file path | Score that single file |
```

### follows_rules (rules)

```markdown
## Follows Rules

Code that SHOULD comply:
```python
result: Result[User, AppError] = get_user(id)
```

Code that SHOULD violate:
```python
user = get_user(id).unwrap()  # should be flagged
```
```

### frontmatter_valid (all types)

```markdown
## Frontmatter Valid

Required fields:
- description: present and trigger-style ("Use when...")
- model: sonnet
- tools: [Read, Glob, Grep]
- skills: [nlpm:conventions, nlpm:scoring]
```

## Test Results Format

```
NLPM Test Report

Spec                              Artifact                    Result   Details
─────────────────────────────────────────────────────────────────────────────────
my-agent.spec.md                  agents/my-agent.md          PASS     5/5 checks
my-skill.spec.md                  skills/core/SKILL.md        FAIL     3/5 checks
  ✗ Trigger: "optimize React hooks" → predicted NO trigger (expected YES)
  ✗ Score: 68/100 (min: 85)

Overall: 1 passed, 1 failed (50%)

RED items (fix these):
  1. skills/core/SKILL.md — trigger gap: "optimize React hooks" not covered by description
  2. skills/core/SKILL.md — score 68 < min 85: missing <example> blocks (-15)
```

## Best Practices for Specs

- Write specs BEFORE writing the artifact (TDD discipline)
- 5-10 trigger queries for skills/agents (mix positive and negative)
- Include edge cases in `handles_input` for commands
- `min_score` should match your project's threshold (default 85 for new artifacts, 70 for legacy)
- Specs are living documents — update when behavior requirements change

## Spec File Discovery

The tester discovers specs by:
1. Looking in `.nlpm-test/` directory
2. Matching spec filename to artifact filename: `my-agent.spec.md` → `agents/my-agent.md` (uses the `artifact:` frontmatter field)
3. If `artifact` path doesn't exist → spec is RED by default (artifact not yet created — this is the TDD "write test first" state)

## Worked Example: TDD Cycle

1. **RED — write the spec first.** Create `.nlpm-test/my-agent.spec.md` with `artifact: agents/my-agent.md` and a `triggers_on:` block listing 5 user queries the agent should match. The artifact does not exist yet — `/nlpm:test` reports RED with one failure: `artifact not found`.

2. **GREEN — write the artifact.** Create `agents/my-agent.md` with frontmatter (name, description, model, tools) and a body. The description must be specific enough that the listed trigger queries land on it. Re-run `/nlpm:test`: the agent now exists, the tester predicts triggers, and the spec passes.

3. **REFACTOR — change the body, re-run the spec.** Edit the artifact's behavior. The same spec runs unchanged; if a refactor breaks a trigger query or violates a `handles_input` case, the test goes RED. Fix forward, re-run.

This is the natural-language analogue of `pytest` or `jest` — specs are the contract; artifacts are the implementation.

## Scope Note

This skill covers the spec format and runner contract for NL-TDD. For the
scoring rubric the tester compares against, see `nlpm:scoring`. For the
schemas of artifact frontmatter the spec checks, see `nlpm:conventions`.
