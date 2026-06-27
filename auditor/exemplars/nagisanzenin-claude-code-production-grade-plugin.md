---
slug: nagisanzenin-claude-code-production-grade-plugin
repo: nagisanzenin/claude-code-production-grade-plugin
audited: 2026-06-27
commit_sha: 64795da2f91aa7b1c57b55e3b0fb1980cb2076b2
score: 93
exemplifies:
  - R04
  - R05
  - R07
  - R08
  - R43
---

# Exemplar: nagisanzenin/claude-code-production-grade-plugin

**Score**: 93/100  |  **Date**: 2026-06-27  |  **Commit**: `64795da2f91aa7b1c57b55e3b0fb1980cb2076b2`

A 15-skill Claude Code plugin that wraps a full software-delivery pipeline (PM → architect → engineer → QA → SRE → tech-writer) in a single production-grade orchestrator. Notable for compact per-skill SKILL.md files that stay under 250 lines by delegating phase detail to sub-files, explicit parallel execution blocks with real Agent() calls, and a Common Mistakes table in every skill with concrete failure/fix pairs.

## Per-rule evidence

### R04 — Description as trigger

R04 requires at least 3 specific action phrases matching real user queries. This repo's descriptions consistently name the concrete task the skill handles, not a category label.

> `skills/code-reviewer/SKILL.md:3-7`:
>
> ```
> description: >
>   [production-grade internal] Reviews code for quality — architecture
>   conformance, anti-patterns, performance issues, maintainability.
>   Read-only analysis, never modifies code.
>   Routed via the production-grade orchestrator.
> ```

> `skills/polymath/SKILL.md:3-7`:
>
> ```
> description: >
>   [production-grade internal] Thinking partner when you're unsure what to
>   build or how — explores ideas, researches options, helps decide before
>   committing to code. Routed via the production-grade orchestrator.
> ```

> `skills/technical-writer/SKILL.md:3-6`:
>
> ```
> description: >
>   [production-grade internal] Generates documentation when you need to
>   explain code — API references, developer guides, READMEs, architecture
>   overviews. Routed via the production-grade orchestrator.
> ```

Each description packs 3–5 distinct trigger phrases into one or two lines: "architecture conformance, anti-patterns, performance issues, maintainability" hits four separate user search intentions. The `[production-grade internal]` prefix is a consistent scope signal that tells the orchestrator these skills are not standalone — a disambiguation technique that avoids false positives when Claude matches skills against user queries.

### R05 — Body length

R05 caps SKILL.md files at 500 lines to avoid context bloat. Every skill in this repo hits the constraint by splitting phase detail into sub-files loaded on demand. The technical-writer skill covers 4 phases of documentation generation (content audit, API reference, developer guides, Docusaurus scaffold) in 202 lines; the data-scientist skill covers 6 phases of AI/ML optimization in 206 lines; the SRE skill covers 5 phases in 210 lines.

The dispatch protocol that makes this work:

> `skills/technical-writer/SKILL.md:110-111`:
>
> ```
> Read the relevant phase file before starting that phase. Never read all phases at once —
> each is loaded on demand to minimize token usage.
> ```

> `skills/data-scientist/SKILL.md:126-134` (Phase Index table, abbreviated):
>
> ```
> | Phase | File                          | When to Load              | Purpose |
> |-------|-------------------------------|---------------------------|---------|
> | 1     | phases/01-system-audit.md     | Always first              | Detect AI/ML/LLM usage ... |
> | 2     | phases/02-llm-optimization.md | After phase 1 (if LLM...) | Prompt engineering ...    |
> ...
> | 6     | phases/06-cost-modeling.md    | After all prior phases    | API cost analysis ...     |
> ```

The Phase Index table serves as an in-SKILL.md navigation layer: the condition column (`After phase 1 if LLM usage found`, `After phase 3`) encodes the dependency graph without requiring Claude to load six files to understand the flow. The result is that every skill's SKILL.md is a compact dispatcher — not a monolith.

### R07 — Scope note when related skills exist

R07 requires a scope note when related skills exist, so Claude knows which skill owns which concern. The code-reviewer skill draws a hard boundary with its adjacent security-engineer skill:

> `skills/code-reviewer/SKILL.md:93-95`:
>
> ```
> ## Security Scope
>
> Security analysis: see security-engineer findings. Code reviewer does NOT perform OWASP or
> security review.
> ```

The SRE skill draws a similar boundary against DevOps with a responsibility matrix:

> `skills/sre/SKILL.md:94`:
>
> ```
> You are the SRE (Site Reliability Engineering) Specialist. SOLE authority on SLO
> definitions, error budgets, runbooks, capacity planning. DevOps does NOT define SLOs —
> they implement the thresholds SRE defines.
> ```

Both scope notes name the adjacent skill and state the partition explicitly ("Code reviewer does NOT", "DevOps does NOT define SLOs"). That specificity is what makes a scope note useful — "this skill does not handle security" is ambiguous; "see security-engineer findings" is not.

### R08 — Patterns over theory

R08 says to teach what to do in specific situations, not abstract concepts. Every skill in this repo includes a Common Mistakes table that pairs a named failure mode with a concrete corrective action. The code-reviewer table runs to 16 rows; the data-scientist table to 15; the SRE table to 9. Two representative rows:

> `skills/data-scientist/SKILL.md:151-152`:
>
> ```
> | 1 | Optimizing prompts without measuring baseline quality | ALWAYS measure baseline
>     tokens, cost, latency, AND quality before changes. |
> | 5 | Caching LLM responses with high temperature | ONLY cache responses with
>     temperature <= 0.5. |
> ```

> `skills/sre/SKILL.md:173-177`:
>
> ```
> | Setting SLOs at 99.99% for every service | Leaves near-zero error budget,
>   blocks all deployments | Set SLOs based on user-observable impact. Start
>   with 99.5% and tighten. |
> | Writing generic runbooks ("check the logs") | On-call engineer at 3 AM cannot
>   figure out WHICH logs | Include exact commands with real metric names, real
>   pod labels, decision trees. |
> ```

The data-scientist table is especially precise: `temperature <= 0.5` is a verifiable threshold, not a guideline. "ONLY cache responses with temperature <= 0.5" changes Claude's behavior in a specific, testable way; "be careful with caching" does not. The SRE table applies the same discipline: "Start with 99.5% and tighten" is an actionable starting point; "choose an appropriate SLO" is not.

### R43 — Parallel when independent, sequential when dependent

R43 requires parallel execution when tasks have no data dependency. Three skills in this repo include explicit parallel execution blocks with real `Agent()` calls annotated with the dependency rationale:

> `skills/technical-writer/SKILL.md:115-127`:
>
> ```python
> Agent(prompt="Generate API reference documentation following Phase 2. Read OpenAPI specs
>       from api/. Write to docs/api-reference/.", ...)
> Agent(prompt="Generate developer guides following Phase 3. Read architecture and source
>       code. Write to docs/getting-started/, docs/guides/, docs/operations/.", ...)
>
> # Execution order:
> # 1. Phase 1: Content Audit (sequential — establishes doc sitemap)
> # 2. Phases 2-3: API Reference + Developer Guides (PARALLEL)
> # 3. Phase 4: Docusaurus Scaffold (sequential — needs all docs)
> ```

> `skills/code-reviewer/SKILL.md:155-165`:
>
> ```python
> Agent(prompt="Review architecture conformance following Phase 1 checklist...", ...)
> Agent(prompt="Review code quality following Phase 2 checklist (SOLID, DRY, complexity)...", ...)
> Agent(prompt="Review performance following Phase 3 checklist (N+1, caching, bundle size)...", ...)
> Agent(prompt="Review test quality following Phase 4 checklist...", ...)
>
> # Wait for all 4 agents, then run Phase 5 (Review Report) sequentially —
> # it compiles all findings.
> ```

> `skills/sre/SKILL.md:138-147`:
>
> ```python
> Agent(prompt="Design chaos engineering scenarios following Phase 3...", ...)
> Agent(prompt="Define incident management procedures following Phase 4...", ...)
> Agent(prompt="Create capacity planning models following Phase 5...", ...)
>
> # Execution order:
> # 1. Phase 1: Readiness Review (sequential — foundational assessment)
> # 2. Phase 2: SLO Definition (sequential — all other phases reference SLOs)
> # 3. Phases 3-5: Chaos + Incidents + Capacity (PARALLEL)
> ```

What makes these exemplary: the sequencing rationale is embedded in a comment next to the code ("sequential — establishes doc sitemap", "it compiles all findings"). Claude reading the skill knows not just that the parallelism is intentional, but why the pre- and post-barrier phases must be sequential. That annotation prevents accidental re-serialization by a future modifier who doesn't understand the dependency structure.

## Worth adopting

**Pattern: Engagement mode table.** Every skill defines a four-row table (Express / Standard / Thorough / Meticulous) describing how the skill's behavior scales with desired oversight level. Evidence: `skills/code-reviewer/SKILL.md:31-35`, `skills/technical-writer/SKILL.md:37-40`, `skills/data-scientist/SKILL.md:32-35`. Why it would be a useful rule: skills that omit a depth-calibration mechanism produce the same output regardless of whether the user wants a fast scan or an exhaustive review; an explicit mode table makes the calibration observable and editable without touching business logic.

**Pattern: Completion summary sentinel with concrete-number enforcement.** Every skill specifies a completion summary template that explicitly requires concrete numbers — `{N} docs generated`, `{M} experiments designed` — with the annotation `MUST include concrete numbers`. Evidence: `skills/technical-writer/SKILL.md:75-78`, `skills/data-scientist/SKILL.md:87-90`. Why it would be a useful rule: completion summaries that allow vague totals ("documentation generated") produce output that cannot be audited or compared across runs; a template with required numeric slots enforces measurability at the output boundary without adding a separate verification step.
