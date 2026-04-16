---
name: patterns
description: "Use when writing or reviewing NL artifacts (skills, agents, prompts, rules, hooks) and need to check for anti-patterns — vague quantifiers, prohibitions without alternatives, oversized skills, write-on-read-only agents, monolithic prompts, or linter-duplicating rules. Also useful for prompt review, skill file review, or prompt quality checks."
version: 0.1.0
---

# NL Programming Patterns

Best practices and anti-patterns for writing Claude Code plugin components. Each pattern includes a rationale and a concrete example. Use this skill when authoring or reviewing skills, agents, commands, rules, or hooks.

### Quick Review Checklist

When reviewing an artifact, check in this order:
1. Scan for anti-patterns A1–A9 — fix any violations
2. Verify patterns P1–P9 are applied where applicable
3. Cross-reference with `nlpm:scoring` rubric for penalty impact

---

## Patterns (Use These)

### P1: Trigger-Optimized Descriptions (R04)

Write agent and skill descriptions with 3+ specific trigger phrases rather than a single generic one-liner. Claude uses description text to decide when to invoke an agent; richer vocabulary improves recall.

**Good:**
```yaml
description: |
  Lints NL artifacts for quality issues. Use this agent when scoring plugin
  components, running static analysis on prompts, checking command completeness,
  or auditing skill descriptions for vagueness.
```

**Bad:**
```yaml
description: "Analyzes files"
```

The bad example won't trigger reliably — "analyzes files" matches too broadly and too vaguely.

---

### P2: Example-Driven Agents (R09)

Include 2+ `<example>` blocks in agent descriptions with realistic Context, user turn, and assistant response. Examples anchor the agent's behavior and dramatically improve triggering consistency.

**Minimum structure per example:**
```
<example>
Context: <situation that would trigger this agent>
user: <what the user or command says>
assistant: <what this agent does in response>
</example>
```

**Diverse scenarios:** Cover at least one user-direct invocation and one command-as-orchestrator invocation if applicable.

---

### P3: Imperative + Rationale Rules (R03, R21)

Write rules as "**Do X** because Y" not "Don't do Z". Prohibitions without alternatives are hard to follow under inference load.

**Good:**
```markdown
**Use `${CLAUDE_PLUGIN_ROOT}` for all intra-plugin file references.**

Because absolute paths break when the plugin is installed by different users
or on different machines, portable path variables ensure the plugin works
everywhere it is installed.
```

**Bad:**
```markdown
Don't hardcode absolute paths in hooks or scripts.
```

---

### P4: Layered Prompts (R40)

Structure complex command and agent bodies in this order:
1. Role/persona
2. Context (what you know, what you've been given)
3. Task (specific action)
4. Constraints (limits, edge cases, what to avoid)
5. Output format (exact structure)

Mixing these layers — especially burying the task in the middle of constraints — reduces response quality.

---

### P5: Graduated Model Selection (R10)

Match model tier to task complexity:

| Model | Best for |
|-------|---------|
| `haiku` | Parsing, formatting, file discovery, classification, pattern matching |
| `sonnet` | Analysis, reasoning, code review, multi-step judgment, scoring |
| `opus` | Complex judgment requiring deep synthesis, orchestration of many agents |

Using opus for a file-glob scan wastes tokens with no quality improvement. Using haiku for nuanced quality scoring produces unreliable results.

---

### P6: Scoped Skills (R05, R07)

Keep each skill under 500 lines with a clearly bounded scope. Include a "Scope Note" section at the bottom stating what the skill covers and what it does NOT cover, with cross-references to related skills (`plugin:skill` format).

Benefits:
- Prevents context bloat when multiple skills are loaded simultaneously
- Makes skills easier to update without cascading effects
- Enables precise skill selection in agent frontmatter

---

### P7: Least-Privilege Tools (R11)

Only list tools in `allowed-tools` (commands) or `tools` (agents) that the body actually uses. Declaring unused tools is misleading and may grant unintended capabilities.

**Good:**
```yaml
tools: ["Glob", "Read"]
```
(for a scanner that only discovers and reads files)

**Bad:**
```yaml
tools: ["Glob", "Read", "Write", "Edit", "Bash", "WebSearch"]
```
(for the same scanner)

---

### P8: Explicit Output Formats (R12, R16, R41)

Every command and agent body should define the exact output structure. Don't leave format to inference — specify section names, table columns, score display format, and summary location.

**Example output format spec in a command body:**
```
Report format:
## Summary
Total artifacts: N | Pass (≥70): N | Fail (<70): N

## Results
| File | Type | Score | Top Issues |
|------|------|-------|------------|
| path/to/file.md | agent | 87 | ... |

## Details
One subsection per file with full penalty breakdown.
```

---

### P9: Error Path Coverage (R17)

Handle the three failure modes explicitly in every command and agent:
1. **Empty input** — no files found, no argument provided
2. **Missing files** — referenced file doesn't exist
3. **Malformed data** — YAML parse errors, invalid JSON, truncated content

Each failure mode should produce a clear, actionable error message — not a silent no-op or a generic "something went wrong."

---

## Anti-Patterns (Avoid These)

### A1: Vague Quantifiers (R01)

Words like "appropriate", "relevant", "as needed", "sufficient", "adequate", "reasonable" without measurable criteria are lint targets. They make rules and instructions unenforceable.

**Penalty:** -2 per occurrence in NLPM scoring, capped at -20.

**Fix:** Replace with specific criteria.
- "appropriate length" → "under 500 lines"
- "relevant tools" → "only tools called in the body"
- "as needed" → "when the input path is a directory"

---

### A2: Prohibitions Without Alternatives (R03)

"Don't use X" without explaining what to use instead violates P3 and leaves the reader with no actionable path.

**Fix:** Always pair a prohibition with an alternative:
- "Don't hardcode paths" → "Use `${CLAUDE_PLUGIN_ROOT}` instead of absolute paths, because..."
- "Don't use passive voice" → "Use imperative verbs (Use, Run, Check, Return) because they reduce ambiguity"

---

### A3: Oversized Skills (R05)

Skills over 500 lines become context bloat. When multiple oversized skills are loaded together, the effective context for the actual task shrinks.

**Fix:** Split by responsibility. If a skill covers both "what the schema looks like" and "how to evaluate quality," those are two skills: `conventions` and `scoring`.

---

### A4: Write/Edit on Read-Only Agents (R11)

Audit, review, and analysis agents should never declare `Write` or `Edit` in their tools list. Read-only agents that can modify files create unexpected side effects.

**Principle:** Agents with names like `linter`, `scanner`, `reviewer`, `auditor`, `inspector` should be read-only. Modification is a separate agent responsibility.

---

### A5: Monolithic Prompts (R13, R40)

A single unstructured block of instructions — no headings, no sections, no numbered steps — is hard to follow for complex tasks and produces inconsistent output.

**Fix:** Use markdown headings and numbered steps. Group related instructions. Put the output format spec at the end, not the beginning.

---

### A6: Rules Duplicating Linters (R24)

If eslint, ruff, clippy, or another static analysis tool already catches a code-level issue, a Claude rule that re-states it is redundant noise. Rules should cover intent, architecture, and NL artifact quality — things linters can't check.

**Fix:** Reference the tool instead: "Run `ruff check` before committing — it enforces all formatting rules."

---

### A7: Agents Without Examples (R09)

An agent description with no `<example>` blocks has unreliable triggering. Without examples, Claude must infer invocation criteria from the description alone, which degrades with ambiguous wording.

**NLPM penalty:** -15 for zero examples on an agent.

---

### A8: Opus for Mechanical Tasks (R10)

File discovery, JSON parsing, pattern matching, line counting — these are haiku tasks. Using opus for them is a 10-30x token cost increase with no quality benefit.

**Decision rule:** If the task has a deterministic correct answer that doesn't require judgment, use haiku. If it requires nuanced evaluation, use sonnet. Reserve opus for tasks where sonnet demonstrably fails.

---

### A9: Hardcoded Paths (R30)

Absolute paths in hooks, scripts, or plugin configs break across environments.

**Fix:** Use `${CLAUDE_PLUGIN_ROOT}` for paths within a plugin. Use relative paths where the base is well-defined.

---

## Scope Note

This skill covers NL programming patterns and anti-patterns for Claude Code artifacts. It does NOT cover:
- Exact schema fields and syntax → see `nlpm:conventions`
- Scoring rubric with penalty tables → see `nlpm:scoring`
- General software engineering patterns outside Claude Code
