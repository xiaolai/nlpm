---
name: writing-agents
description: "How to write Claude Code agent definitions — trigger examples, model selection, tool permissions, output format specs, and system prompt structure. Use when creating, improving, or reviewing agents, configuring sub-agent dispatch, writing agent prompts, agent YAML, or setting up agentic workflows."
version: 0.1.0
---

# Writing Agents

> Scope: covers agent `.md` file authoring. For multi-agent orchestration, see [[orchestration]]. For plugin architecture, see [[writing-plugins]].

## 1. Example Blocks Make or Break Triggering

Without `<example>` blocks, Claude guesses when to dispatch your agent. With them, it pattern-matches against real scenarios.

**Minimum**: 2 examples. **Ideal**: 3 -- one obvious trigger, one edge case, one non-obvious.

### Example Block Anatomy

```xml
<example>
Context: [what the user is doing -- not just "user needs help"]
user: "[realistic user message that should trigger this agent]"
assistant: "[what Claude says when dispatching -- shows the decision logic]"
</example>
```

### Bad Example (too vague -- 40% trigger accuracy)

```xml
<example>
Context: User needs code review
user: "review my code"
assistant: "I'll use the reviewer agent."
</example>
```

**Why it fails**: generic context with no decision logic shown.

### Good Example (specific scenario -- 92% trigger accuracy)

```xml
<example>
Context: User just pushed changes to the authentication module and wants feedback before merging
user: "Can you check if the auth changes look good before I create the PR?"
assistant: "I'll dispatch the security-reviewer agent to check the auth changes for vulnerabilities, token handling, and session management best practices."
</example>
```

**Why it works**: specific context (auth module, pre-PR), realistic query (how users actually talk), decision logic visible (what the agent will check).

### The Three-Example Pattern

| Example | Purpose | What it demonstrates |
|---------|---------|---------------------|
| 1. Obvious trigger | Baseline dispatch | User explicitly asks for what the agent does |
| 2. Edge case | Boundary behavior | User asks something adjacent -- agent should still trigger |
| 3. Non-obvious | Discovery | User doesn't know the agent exists but their need matches |

Example for a "performance-profiler" agent:

```xml
<!-- Example 1: Obvious -->
<example>
Context: User wants to profile their API
user: "Profile the /api/users endpoint, it's slow"
assistant: "I'll dispatch the performance-profiler to trace the /api/users endpoint..."
</example>

<!-- Example 2: Edge case -->
<example>
Context: User notices high memory usage but doesn't mention profiling
user: "The app uses 2GB of RAM after running for an hour, is there a leak?"
assistant: "I'll dispatch the performance-profiler to analyze memory allocation patterns..."
</example>

<!-- Example 3: Non-obvious -->
<example>
Context: User is comparing two implementation approaches
user: "Should I use a JOIN here or two separate queries?"
assistant: "I'll dispatch the performance-profiler to benchmark both approaches..."
</example>
```

## 2. Model Selection

| Task type | Model | Signal words in body | Examples |
|-----------|-------|---------------------|----------|
| Mechanical / parsing / formatting / counting | haiku | count, list, extract, format, parse, scan | scanner, parser, formatter, counter, lister |
| Analysis / reasoning / moderate judgment | sonnet | analyze, review, evaluate, summarize, compare | linter, reviewer, extractor, summarizer |
| Complex judgment / orchestration / multi-agent | opus | coordinate, decide, assess, synthesize, architect | QC coordinator, architect, strategy planner |

### Quick Heuristic

Count the instruction lines in your agent body. Then check for judgment words.

```
< 20 instruction lines AND no judgment words → haiku
20-50 instruction lines OR judgment words → sonnet
> 50 instruction lines OR coordination logic → opus
```

Judgment words: evaluate, decide, assess, determine, weigh, prioritize, recommend, judge, infer, synthesize.

### Cost Impact

| Model | Relative cost | When to upgrade |
|-------|--------------|-----------------|
| haiku | 1x | Agent produces wrong output on edge cases |
| sonnet | 10x | Agent produces wrong output on easy cases |
| opus | 30x | Agent coordinates other agents or makes architectural decisions |

**Rule**: start with haiku, upgrade only when output quality requires it.

## 3. Tool Least-Privilege

Only list tools the agent body actually references. Every extra tool is a potential misuse vector.

### Common Mistakes

| Agent type | Common over-grant | Correct tools |
|-----------|-------------------|---------------|
| Audit/review agent | Write, Edit, Bash | Read, Glob, Grep |
| Code generator | Read, Grep (unused) | Write, Edit, Bash |
| Orchestrator | Read, Write (does no IO) | Task |
| Scanner | Bash (uses grep) | Grep, Glob, Read |

### Tool Reference

| Tool | When to include |
|------|----------------|
| Read | Agent reads file contents |
| Write | Agent creates new files |
| Edit | Agent modifies existing files |
| Glob | Agent searches for files by pattern |
| Grep | Agent searches file contents |
| Bash | Agent runs shell commands (linters, tests, builds) |
| Task | Agent dispatches sub-agents |
| Fetch | Agent makes HTTP requests |

## 4. Output Format

Every agent MUST define its output format in the body. Without it, output varies between invocations -- making results unparseable by parent agents.

### Pattern: Structured Report

```markdown
## Output Format

### {Section Title}
| Column1 | Column2 | Column3 |
|---------|---------|---------|
| ...     | ...     | ...     |

### Summary
- Total items: {N}
- Issues found: {N}
- Pass/Fail: {verdict}
```

### Pattern: Severity-Tagged Findings

```markdown
## Output Format

For each finding, output:

**[SEVERITY] Finding title**
- File: `path/to/file`
- Line: {N}
- Issue: {description}
- Fix: {concrete suggestion}

Severity levels: CRITICAL > HIGH > MEDIUM > LOW > INFO
```

### Pattern: Pass/Fail Gate

```markdown
## Output Format

Final line must be exactly one of:
- `PASS: All checks passed`
- `WARN: {N} warnings found (see above)`
- `FAIL: {N} errors found (see above)`
```

## 5. System Prompt Structure

Order matters. Claude reads top-to-bottom and front-loads early instructions.

### The Five Sections

```markdown
## Mission
[1-2 sentences: what this agent does and WHY it exists]

## Instructions
1. [First step]
2. [Second step]
3. [Third step]
...

## Boundaries
- Do NOT [thing that would be harmful]
- Do NOT [thing that's out of scope]
- If [ambiguous situation], then [explicit resolution]

## Output Format
[Exact template -- see section 4 above]

## Error Handling
- If no files found: report "No matching files" and exit
- If tool fails: report the error and continue with remaining work
- If scope is unclear: analyze the narrower interpretation
```

### Section Sizing

| Section | Target lines | Over-budget signal |
|---------|-------------|-------------------|
| Mission | 2-3 | More than one paragraph |
| Instructions | 5-15 | More than 20 numbered steps |
| Boundaries | 3-7 | More than 10 "Do NOT" items |
| Output Format | 5-15 | Defining more than 3 output sections |
| Error Handling | 3-5 | More than 5 error cases |

Total agent body: aim for 25-45 lines. Over 60 lines means the agent is doing too much -- split it.

## 6. Worked Example

### Before

```yaml
---
name: code-checker
description: Check code
model: opus
tools: [Read, Write, Edit, Bash, Grep, Glob, Task]
---
```

```markdown
You are a code checker. Check the user's code for issues.
Look at the files and find problems. Report what you find.
```

**Problems:**
- Description: 0 trigger phrases, no "Use when..." (-30)
- Model: opus for a simple review task (-10)
- Tools: 7 tools granted, body uses maybe 3 (-10)
- No examples: unreliable triggering (-15)
- No output format: inconsistent results (-15)
- No boundaries: scope creep (-10)
- No error handling: silent failures (-10)

### After

```yaml
---
name: code-checker
description: "Static analysis agent — checks code for bugs, type errors, and anti-patterns. Use when reviewing code quality, running pre-commit checks, or validating changes before PR."
model: sonnet
tools: [Read, Glob, Grep]
---
```

```markdown
## Mission
Analyze source code files for bugs, type errors, and anti-patterns.
Produce a structured report with severity-tagged findings.

## Instructions
1. Use Glob to discover files matching the target pattern
2. Use Read to examine each file
3. Use Grep to cross-reference imports and usage patterns
4. For each issue found, classify severity and provide a concrete fix
5. Produce the output report

## Boundaries
- Do NOT modify any files (read-only analysis)
- Do NOT run shell commands
- Do NOT report style issues (defer to linter)
- If no target pattern specified, analyze all files in src/

## Output Format

For each finding:

**[SEVERITY] Issue title**
- File: `path/to/file`
- Line: {N}
- Issue: {description}
- Fix: {concrete fix}

Final line:
- `PASS: No issues found`
- `WARN: {N} warnings found`
- `FAIL: {N} errors found`

## Error Handling
- If no files match the pattern: report "No matching files for pattern: {X}"
- If a file cannot be read: skip it and note in the report
```

```xml
<example>
Context: User just finished implementing a new feature and wants a quality check
user: "Check the auth module for any bugs before I push"
assistant: "I'll dispatch the code-checker agent to analyze src/auth/ for bugs, type errors, and anti-patterns."
</example>

<example>
Context: User is debugging a production issue and suspects a code defect
user: "Something's wrong with the payment flow, can you scan it?"
assistant: "I'll dispatch the code-checker to analyze the payment module for potential bugs and logic errors."
</example>
```

Key improvements: added trigger-rich description, downgraded to sonnet with read-only tools, and added examples, output format, boundaries, and error handling.

## 7. Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| No examples | 40% trigger accuracy | Add 2-3 specific scenario examples |
| Opus for mechanical work | 30x cost for same result | Use haiku for parsing, sonnet for analysis |
| All tools granted | Agent writes when it should only read | List only tools the body references |
| No output format | Different format each run | Define exact output template |
| Body over 60 lines | Agent is doing too much | Split into focused sub-agents |
| "Be thorough" in body | Meaningless filler | Replace with specific instructions |
| No error handling | Silent failures | Add 3-5 error cases with resolution |
