---
slug: Jeffallan-claude-skills
repo: Jeffallan/claude-skills
audited: 2026-05-13
commit_sha: HEAD
score: 92
exemplifies:
  - R04
  - R05
  - R06
  - R07
  - R08
---

# Exemplar: Jeffallan/claude-skills

**Score**: 92/100  |  **Date**: 2026-05-13  |  **Commit**: `HEAD`

A 66-skill fullstack-developer plugin that achieves 51 perfect-score skills through a consistent three-layer architecture: precise trigger descriptions, sub-100-line SKILL.md bodies, and deep reference files loaded on demand.

## Per-rule evidence

### R04 — Description as trigger

Every skill description in this repo packs multiple specific action phrases, not a generic capability statement. The repo's `CLAUDE.md` codifies this as "The Description Trap" and the CI script `scripts/validate-skills.py` enforces it mechanically (description must contain the substring `"Use when"`).

> Real quote from `skills/rust-engineer/SKILL.md:3`:
>
> ```
> description: Writes, reviews, and debugs idiomatic Rust code with memory safety and
> zero-cost abstractions. Implements ownership patterns, manages lifetimes, designs trait
> hierarchies, builds async applications with tokio, and structures error handling with
> Result/Option. Use when building Rust applications, solving ownership or borrowing issues,
> designing trait-based APIs, implementing async/await concurrency, creating FFI bindings,
> or optimizing for performance and memory safety. Invoke for Rust, Cargo, ownership,
> borrowing, lifetimes, async Rust, tokio, zero-cost abstractions, memory safety, systems
> programming.
> ```

What makes this exemplary: the description names six distinct trigger scenarios in a single sentence ("Use when building … solving … designing … implementing … creating … or optimizing"), leaving no ambiguity about when this skill activates versus, say, `devops-engineer` or `embedded-systems`.

The repo also documents the inverse — what to avoid — in `CLAUDE.md`:

> Real quote from `CLAUDE.md` (The Description Trap section):
>
> ```
> BAD - Process steps in description:
> description: Use for debugging. First investigate root cause, then analyze
> patterns, test hypotheses, and implement fixes with tests.
>
> GOOD - Capability + trigger:
> description: Diagnoses bugs through root cause analysis and pattern matching.
> Use when encountering errors or unexpected behavior requiring investigation.
> ```

The explicit BAD/GOOD contrast is rare in skill collections and prevents future contributors from accidentally polluting descriptions with workflow steps.

---

### R05 — Body length

The repo formalizes a two-tier architecture: SKILL.md stays at 80–100 lines, and deep content lives in `references/` subdirectories loaded on demand. The plugin ships 355 reference files alongside 66 SKILL.md files.

> Real quote from `CLAUDE.md` (Progressive Disclosure Architecture section):
>
> ```
> Tier 1 - SKILL.md (~80-100 lines)
> - Role definition and expertise level
> - When-to-use guidance (triggers)
> - Core workflow (5 steps)
> - Constraints (MUST DO / MUST NOT DO)
> - Routing table to references
>
> Tier 2 - Reference Files (100-600 lines each)
> - Deep technical content
> - Complete code examples
> - Edge cases and anti-patterns
> - Loaded only when context requires
>
> Goal: 50% token reduction through selective loading.
> ```

Measured against live files: `skills/rust-engineer/SKILL.md` is 170 lines, `skills/react-expert/SKILL.md` is 152 lines, `skills/prompt-engineer/SKILL.md` is 137 lines — all comfortably under the 500-line ceiling. The constraint is documented, enforced in authorship standards, and visibly followed across all 51 perfect-score skills.

---

### R06 — Code examples must be runnable

Every code block in the 100-score skills uses real imports, real types, and real syntax — no pseudocode or placeholder logic. The standard is "complete, working code examples with TypeScript types" (CLAUDE.md, Reference File Standards).

> Real quote from `skills/react-expert/SKILL.md:56-75`:
>
> ```tsx
> // app/users/page.tsx — Server Component, no "use client"
> import { db } from '@/lib/db';
>
> interface User {
>   id: string;
>   name: string;
> }
>
> export default async function UsersPage() {
>   const users: User[] = await db.user.findMany();
>
>   return (
>     <ul>
>       {users.map((user) => (
>         <li key={user.id}>{user.name}</li>
>       ))}
>     </ul>
>   );
> }
> ```

The example names the exact file path (`app/users/page.tsx`), uses real imports (`@/lib/db`), declares the TypeScript interface, and shows the async Server Component pattern — copyable into a Next.js App Router project as-is. No ellipsis, no `// ...rest of implementation`.

> Real quote from `skills/rust-engineer/SKILL.md:79-96`:
>
> ```rust
> use thiserror::Error;
>
> #[derive(Debug, Error)]
> pub enum AppError {
>     #[error("I/O error: {0}")]
>     Io(#[from] std::io::Error),
>     #[error("parse error for value `{value}`: {reason}")]
>     Parse { value: String, reason: String },
> }
>
> // ? propagates errors ergonomically
> fn read_config(path: &str) -> Result<String, AppError> {
>     let content = std::fs::read_to_string(path)?;  // Io variant via #[from]
>     Ok(content)
> }
> ```

This pattern shows problem (Io error mapping) and solution (`#[from]` + `?`) in real Rust with a real crate import.

---

### R07 — Scope note when related skills exist

Every SKILL.md declares a `related-skills` frontmatter field listing peer skills by directory name. The field is validated by `scripts/validate-skills.py` (referenced skill directories must exist). This gives Claude a machine-readable cross-reference before it reads a single line of the body.

> Real quote from `skills/prompt-engineer/SKILL.md:13`:
>
> ```yaml
> related-skills: test-master, rag-architect, debugging-wizard
> ```

> Real quote from `skills/rust-engineer/SKILL.md:13`:
>
> ```yaml
> related-skills: test-master
> ```

> Real quote from `skills/debugging-wizard/SKILL.md:13`:
>
> ```yaml
> related-skills: test-master, fullstack-guardian, monitoring-expert
> ```

What makes this strong: the scope note is in frontmatter, not prose. Claude reads frontmatter first, so the cross-reference is available even if the body is partially loaded. The repo also adds inline scope notes in body text for longer skills (e.g., `prompt-engineer`'s "Coverage Note" section at line 130: "Reference files cover major prompting techniques… Consult the relevant reference before designing for a specific model or pattern.").

---

### R08 — Patterns over theory

Every SKILL.md centers a "Key Patterns" or "Core Workflow" section that teaches Claude what to do in a named situation, not abstract advice. The reference guide tables make the routing explicit: here is the situation, here is the file to load.

> Real quote from `skills/prompt-engineer/SKILL.md:43-52` (Reference Guide table):
>
> ```
> | Topic              | Reference                            | Load When                                      |
> |--------------------|--------------------------------------|------------------------------------------------|
> | Prompt Patterns    | `references/prompt-patterns.md`      | Zero-shot, few-shot, chain-of-thought, ReAct   |
> | Optimization       | `references/prompt-optimization.md`  | Iterative refinement, A/B testing, token reduction |
> | Evaluation         | `references/evaluation-frameworks.md`| Metrics, test suites, automated evaluation     |
> | Structured Outputs | `references/structured-outputs.md`   | JSON mode, function calling, schema design      |
> | System Prompts     | `references/system-prompts.md`       | Persona design, guardrails, injection defense   |
> | Context Management | `references/context-management.md`   | Attention budget, degradation patterns, context optimization |
> ```

Each row maps a concrete situation ("Persona design, guardrails, injection defense") to a specific reference file. Claude doesn't have to guess which reference applies — the table makes the decision policy explicit.

> Real quote from `skills/prompt-engineer/SKILL.md:56-98` (Before/After Optimization):
>
> ```
> Before (vague, inconsistent outputs):
> Summarize this document.
> {{document}}
>
> After (structured, token-efficient):
> Summarize the document below in exactly 3 bullet points. Each bullet must be one
> sentence and start with an action verb. Do not include opinions or information not
> present in the document.
> ```

The before/after pattern teaches the rule by contrast, not by stating it as a principle.

---

## Worth adopting

**Pattern: Routing table (situation → reference file).** Evidence: `skills/rust-engineer/SKILL.md:30-38`, `skills/react-expert/SKILL.md:41-52`, `skills/prompt-engineer/SKILL.md:43-52`, and all other 100-score skills. Every skill body opens with a two-column table: `Topic | Reference | Load When`. This externalizes deep content into lazy-loaded files while keeping the SKILL.md body token-efficient. Why it would be a useful rule: the current rules cap body length (R05) and require scope notes (R07), but do not specify a mechanism for managing deep sub-topic content. A rule of the form "**Use a routing table when a skill covers 3+ sub-topics.** Without it, either the body bloats past 500 lines or Claude must guess which reference to consult" would codify a pattern that 51 repos already use consistently and that demonstrably keeps SKILL.md files under 180 lines across a 66-skill collection.

**Pattern: CI enforcement of description format.** Evidence: `scripts/validate-skills.py` exits 1 if `description` does not contain `"Use when"`. This makes R04 compliance a hard gate, not a style suggestion. Why it would be a useful rule: no current rule specifies that R04 should be machine-verified. A note in R04 — "Enforce with CI: reject descriptions lacking at least one 'Use when' clause" — would shift R04 from advisory to gate-enforced across plugin ecosystems.
