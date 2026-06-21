---
slug: multica-ai-andrej-karpathy-skills
repo: multica-ai/andrej-karpathy-skills
audited: 2026-06-21
commit_sha: 2c606141936f1eeef17fa3043a72095b4765b9c2
score: 98
exemplifies:
  - R02
  - R04
  - R05
  - R06
  - R08
  - R49
---

# Exemplar: multica-ai/andrej-karpathy-skills

**Score**: 98/100  |  **Date**: 2026-06-21  |  **Commit**: `2c606141936f1eeef17fa3043a72095b4765b9c2`

A single-skill Claude Code plugin encoding four coding-behavior guidelines derived from Andrej Karpathy's observations on LLM pitfalls; notable for a 68-line skill body, trigger-rich description, and clean separation between the Claude-facing SKILL.md and the human-facing README.

## Per-rule evidence

### R02 — Every line must earn its tokens

The `SKILL.md` delivers four behavior-shaping principles in 68 lines, including the frontmatter. No section repeats another, no paragraph explains what the heading already says, and there is no "Introduction" or "Overview" preamble. The tradeoff note at line 12 is the only meta-commentary — and it changes behavior (it scopes when the rules apply):

> From `skills/karpathy-guidelines/SKILL.md:12`:
>
> ```
> **Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.
> ```

A token-tax version of this file would open with a paragraph describing what LLM coding pitfalls are and why Karpathy's observations matter. It doesn't. It opens at the first rule.

### R04 — Description is a trigger, not a summary

The frontmatter description packs five distinct trigger phrases into 41 words:

> From `skills/karpathy-guidelines/SKILL.md:3`:
>
> ```
> description: Behavioral guidelines to reduce common LLM coding mistakes. Use when writing,
> reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface
> assumptions, and define verifiable success criteria.
> ```

Each phrase maps to a real user query: someone asking Claude to "review my code" hits "reviewing", someone saying "refactor this" hits "refactoring code", someone frustrated by bloated output hits "overcomplication". The description would fail R04 if it read "Guidelines for better Claude Code behavior" — that's a summary. This reads like a query index.

### R05 — Under 500 lines

The skill body is 68 lines covering four principles, each with concrete criteria. The README, which is human-facing, spans 172 lines and contains the same content rephrased for readability, installation instructions, a motivation section, and a customization guide. The SKILL.md is the distillation; the README is the exposition. They do not collapse into one file.

> From `skills/karpathy-guidelines/SKILL.md` (full file): 68 lines.
> From `README.md` (full file): 172 lines.

Keeping the skill at 68 lines means every Claude interaction loads 68 tokens of instruction, not 172. The information lost from the README (motivation, install steps, customization guide) is information Claude doesn't need at inference time.

### R06 — Code examples must be runnable

Section 4 ("Goal-Driven Execution") includes a plan template and a transformation table with real syntax — not pseudocode:

> From `skills/karpathy-guidelines/SKILL.md:57-66`:
>
> ```
> Transform tasks into verifiable goals:
> - "Add validation" → "Write tests for invalid inputs, then make them pass"
> - "Fix the bug" → "Write a test that reproduces it, then make it pass"
> - "Refactor X" → "Ensure tests pass before and after"
>
> For multi-step tasks, state a brief plan:
> ```
> 1. [Step] → verify: [check]
> 2. [Step] → verify: [check]
> 3. [Step] → verify: [check]
> ```
> ```

The `→ verify: [check]` template is something Claude can populate and follow mechanically. The before/after transformation pairs let Claude pattern-match a user's imperative ("Fix the bug") to a testable goal form. Pseudocode equivalents ("Write verifiable steps") would require Claude to invent the format from scratch each time.

### R08 — Patterns over theory

Sections 2 and 3 teach behavior via a named self-check test rather than an abstract principle:

> From `skills/karpathy-guidelines/SKILL.md:33`:
>
> ```
> Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.
> ```

> From `skills/karpathy-guidelines/SKILL.md:49`:
>
> ```
> The test: Every changed line should trace directly to the user's request.
> ```

Both tests are binary: either the answer is yes/no or a line either traces to the request or it doesn't. Claude can apply a binary test in a loop. The theoretical framing would be "avoid overengineering" — a vague quantifier (R01 violation) that produces inconsistent application. The test form produces consistent application.

### R49 — CLAUDE.md for Claude, README for humans

`CLAUDE.md` is 62 lines of pure behavioral instructions. It contains no install steps, no motivation section, no links. It opens immediately with the tradeoff note and proceeds to the four principles. The closing line is the only evaluative statement, and it is evaluative *for Claude*:

> From `CLAUDE.md:63-65`:
>
> ```
> **These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to
> overcomplication, and clarifying questions come before implementation rather than after mistakes.
> ```

`README.md`, by contrast, contains an "Install" section with `curl` commands and `/plugin install` instructions, a "The Problems" section with Karpathy quotes to motivate the reader, a "Customization" section showing how to append project-specific rules, and a "How to Know It's Working" section rephrasing the same success criteria in human-readable table form. Nothing in the README instructs Claude. Nothing in the CLAUDE.md explains the plugin to a human.

## Worth adopting

**Pattern: Behavioral success marker in the memory file.** Evidence: `CLAUDE.md:63-65` (`**These guidelines are working if:** fewer unnecessary changes in diffs…`). Why it would be a useful rule: a CLAUDE.md that tells Claude *what compliance looks like* gives Claude a self-monitoring signal without adding a separate rule file. The marker is instructive (Claude checks against it) rather than descriptive (it doesn't just restate what the guidelines say). Candidate rule form: "**Include a behavioral success marker.** One sentence stating what correct behavior looks like in output or diffs. Lets Claude self-check compliance without an external reviewer."
