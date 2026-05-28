---
name: patterns
description: "Use when writing or reviewing NL artifacts and need to check for anti-patterns — vague quantifiers, prohibitions without alternatives, oversized skills, write-on-read-only agents, monolithic prompts, or linter-duplicating rules."
version: 0.1.0
---

# NL Programming Patterns

Best practices and anti-patterns for writing NL programming artifacts (Claude Code, Codex CLI, Antigravity). Each pattern includes a rationale and a concrete example. The patterns are tool-agnostic — they describe how to write effective natural-language instructions, not tool-specific schemas. Use this skill when authoring or reviewing skills, agents, commands, rules, or hooks.

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

Write rules as "**Do X** because Y" not "Don't do Z". The Pink Elephant effect: telling someone not to think of a pink elephant makes them think of it. Prohibitions without alternatives are hard to follow under inference load.

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

### P10: Numeric Anchoring of Subjective Principles (R22)

When stating a principle that has a subjective threshold ("simpler is better", "small change", "meaningful improvement"), follow it immediately with one or more numeric examples that cover the trade-space corners (best case, worst case, neutral case). The principle becomes testable instead of aspirational.

**Example** (from karpathy/autoresearch `program.md:37`, scored 90/100 — see [`auditor/exemplars/karpathy-autoresearch.md`](../../../auditor/exemplars/karpathy-autoresearch.md) for the full audit):

> "All else being equal, simpler is better. … A 0.001 val_bpb improvement that adds 20 lines of hacky code? Probably not worth it. A 0.001 val_bpb improvement from deleting code? Definitely keep. An improvement of ~0 but much simpler code? Keep."

The principle "simpler is better" alone fails R22 enforceability — different agents weigh "simpler" differently. The three anchored examples define the trade-space (gain × complexity-cost) by worked corner cases, so any agent following the rule reaches the same call on a borderline case.

**Apply when** writing rules, agent constraints, or workflow instructions that include a subjective judgment word (small, meaningful, ugly, reasonable, simple, clean). Don't strip the subjective word — anchor it.

---

### P11: Paired CAN/CANNOT Contract (R03)

When prohibitions are non-trivial, present capabilities and prohibitions as a paired list — "What you CAN do" / "What you CANNOT do" — rather than a stream of `do not`s. Each prohibition gains a positive complement; the agent reads both halves of the boundary in one pass.

**Example** (from karpathy/autoresearch `program.md:25-31`):

```
**What you CAN do:**
- Modify `train.py` — this is the only file you edit. Everything is fair game: model
  architecture, optimizer, hyperparameters, training loop, batch size, model size, etc.

**What you CANNOT do:**
- Modify `prepare.py`. It is read-only…
- Install new packages or add dependencies…
- Modify the evaluation harness…
```

What makes this strong: prohibitions without alternatives are A2's Pink Elephant trap; the paired pattern structurally avoids it. The "CAN" half also doubles as a positive scope statement ("Everything is fair game") that prevents the agent from being overly conservative.

**Apply when** an instruction set has more than two prohibitions on the same subject (file boundaries, tool boundaries, behavior boundaries). For a single prohibition, an inline "do X instead of Y" (P3) is enough.

---

### P12: Autonomy Instruction + Rationale + Fallback Ladder (R03, R17)

When telling an agent to act autonomously, three pieces are required for the instruction to actually produce autonomous behavior: (1) state the rule clearly with example forbidden questions, (2) explain *why* in concrete terms the agent can reason about, (3) name the failure mode the agent is most likely to hit and give a numbered list of recovery moves *before* it encounters them. Bare "be autonomous" instructions produce timid agents that ask for permission.

**Example** (from karpathy/autoresearch `program.md:112`, scored 90/100 — see [`auditor/exemplars/karpathy-autoresearch.md`](../../../auditor/exemplars/karpathy-autoresearch.md)):

> "Once the experiment loop has begun (after the initial setup), do NOT pause to ask the human if you should continue. Do NOT ask 'should I keep going?' or 'is this a good stopping point?'. The human might be asleep, or gone from a computer and expects you to continue working *indefinitely* until you are manually stopped. You are autonomous. If you run out of ideas, think harder — read papers referenced in the code, re-read the in-scope files for new angles, try combining previous near-misses, try more radical architectural changes."

What makes this strong: the rule names the failure mode by quoting it ("'should I keep going?'"), the rationale grounds it in a concrete world-state ("human might be asleep"), and the four recovery moves (read papers / re-read files / combine near-misses / radical changes) cover the trade-space when the agent's first instinct (ask) is removed.

**Apply when** writing any instruction that asks an agent to operate without per-step human approval — long-running loops, overnight runs, batch processing, recursive workflows. Without the fallback ladder, the agent silently halts the first time it runs out of obvious moves.

---

### P13: Vivid Closing Use-Case (R16, R35)

End a workflow document with a one-paragraph concrete scenario — named persona, named time of day, calculated quantity — that makes the workflow's duty cycle tangible. Agents follow workflows more reliably when they have a mental model of what success looks like in the wild, not just the per-step instructions.

**Example** (from karpathy/autoresearch `program.md:114`):

> "As an example use case, a user might leave you running while they sleep. If each experiment takes you ~5 minutes then you can run approx 12/hour, for a total of about 100 over the duration of the average human sleep. The user then wakes up to experimental results, all completed by you while they slept!"

What makes this strong: it names the actor ("a user"), the time-of-day ("while they sleep"), and does the arithmetic explicitly (12/hour × ~8 hours ≈ 100 runs). The agent now has a vivid mental model — "I should produce ~100 experiment results overnight" — that the per-step instructions alone don't convey.

**Apply when** a workflow document specifies a process whose value emerges from repetition or duration, not from a single execution. The closing use-case answers "what does success look like at scale?" — a question the per-step instructions implicitly assume but never state.

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

Absolute paths in hooks, scripts, or plugin configs break when:
- A different user installs the plugin
- The project is moved
- CI/CD runs in a container

**Fix:** Use `${CLAUDE_PLUGIN_ROOT}` for paths within a plugin. Use relative paths where the base is well-defined.

---

## Scope Note

This skill covers NL programming patterns and anti-patterns for artifacts across Claude Code, Codex CLI, and Antigravity. It does NOT cover:
- Exact schema fields and syntax → see `nlpm:conventions`
- Scoring rubric with penalty tables → see `nlpm:scoring`
- General software engineering patterns outside NL programming artifacts
