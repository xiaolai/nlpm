---
slug: ciembor-agent-rules-books
repo: ciembor/agent-rules-books
audited: 2026-09-30
commit_sha: 893a88a6fce3a80c565bf39ac65021b43a8b2990
score: 100
exemplifies:
  - R04
  - R05
  - R07
  - R08
---

# Exemplar: ciembor/agent-rules-books

**Score**: 100/100  |  **Date**: 2026-09-30  |  **Commit**: `893a88a6fce3a80c565bf39ac65021b43a8b2990`

A collection of 14 skills, one per software-engineering book. Each `SKILL.md` is an 11-line router that names its trigger situations and points to a 47-64 line `.mini.md` rule set, with a full-length `.md` held back as a fallback reference.

## Per-rule evidence

### R04 — Description as trigger

Every one of the 14 descriptions opens with the verb "Apply" and lists concrete situations that match user queries, not a summary of the book. `clean-code` lists five (readability, naming, function design, responsibilities, testable code). `release-it` lists six (failure handling, timeouts, retries, circuit breakers, observability, deployment behavior).

> Real quote from `clean-code/SKILL.md:3`:
>
> ```
> description: Apply Robert C. Martin-inspired clean code rules when improving readability, naming, function design, responsibilities, or testable everyday code.
> ```

> Real quote from `release-it/SKILL.md:3`:
>
> ```
> description: Apply Michael T. Nygard-inspired production reliability rules when designing failure handling, timeouts, retries, circuit breakers, observability, or deployment behavior.
> ```

The trigger terms are nouns a user would type ("timeouts", "circuit breakers", "aggregates"), so matching works on the task wording instead of the book title.

### R05 — Body length

The 500-line limit is met by a wide margin: each `SKILL.md` is 11 lines. The long material lives in sibling files, and the body tells the agent to read the short one first and the long one only on demand.

> Real quote from `clean-code/SKILL.md:11`:
>
> ```
> Before making design or code decisions, read and apply [clean-code.mini.md](clean-code.mini.md). Use [clean-code.md](clean-code.md) only as a deeper reference when the mini rules are not enough for the current code-quality tradeoff.
> ```

`clean-code.md` is 297 lines and `refactoring-guru.md` is 765, yet neither is loaded by default. The 765-line file would breach R05 if inlined; the conditional "only as a deeper reference" clause keeps it out of context.

### R07 — Scope note when related skills exist

Two skills overlap on refactoring and three on DDD (`refactoring`, `refactoring-guru`; `domain-driven-design`, `domain-driven-design-distilled`, `implementing-domain-driven-design`). The repo separates them through the trigger sentence in each body, each naming a distinct situation, rather than through `[[other-skill]]` cross-references.

> Real quote from `refactoring-guru/SKILL.md:9`:
>
> ```
> Use this skill when a task involves diagnosing smells, choosing targeted refactoring treatments, preserving behavior, applying a refactoring catalog, or avoiding uncontrolled redesign.
> ```

> Real quote from `refactoring/SKILL.md:9`:
>
> ```
> Use this skill when a task involves behavior-preserving code improvement, code smells, small refactoring steps, test-backed cleanup, or separating refactoring from feature changes.
> ```

The two bodies diverge on catalog-driven diagnosis versus test-backed stepwise change. This is a partial fit for R07: the split is real, but no sentence says "for X, see Y".

### R08 — Patterns over theory

The `.mini.md` files are written as situation-to-action rules. Each has a "Decision rules" section of imperative lines and a "Trigger rules" section of "When X, do Y" lines, and each opens by naming the one bias the rules correct.

> Real quote from `clean-code/clean-code.mini.md:7-9`:
>
> ```
> ## Primary bias to correct
>
> Working code is not automatically clean code.
> ```

> Real quote from `clean-code/clean-code.mini.md:18-19`:
>
> ```
> - Separate commands from queries and eliminate hidden side effects. A function that answers should not also mutate behind the reader's back.
> - Keep the happy path readable. Isolate error handling, invalid-state handling, and cleanup; prefer explicit optionality or typed results over null-like sentinel flow when the language supports it.
> ```

> Real quote from `clean-code/clean-code.mini.md:30` (under "## Trigger rules"):
>
> ```
> - When a function mixes setup, validation, computation, and side effects, split the phases.
> ```

Each rule names an observable code condition and the action to take, so an agent can apply it while reading a diff without knowing the book.

## Worth adopting

Pattern: Tiered reference files (`nano` / `mini` / full) with a read-order instruction in the router. Evidence: `clean-code/SKILL.md:11`, plus `clean-code/clean-code.nano.md` (32 lines), `clean-code/clean-code.mini.md` (47 lines) and `clean-code/clean-code.md` (297 lines). Why it would be a useful rule: "When reference material exceeds 100 lines, ship a short default file and a full file, and have the router say which to read first and when to escalate" gives R05 a concrete way to split long content.
