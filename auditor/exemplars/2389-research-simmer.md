---
slug: 2389-research-simmer
repo: 2389-research/simmer
audited: 2026-05-13
commit_sha: bf58540cf5d5e26f27f4f50d2bc924bfbf004f00
score: 93
exemplifies:
  - R04
  - R06
  - R07
  - R08
  - R49
---

# Exemplar: 2389-research/simmer

**Score**: 93/100  |  **Date**: 2026-05-13  |  **Commit**: `bf58540cf5d5e26f27f4f50d2bc924bfbf004f00`

A five-subskill iterative-refinement plugin whose orchestrator description packs 8 trigger phrases and 4 artifact-class distinctions in 9 lines, and whose subskills use problem/fix anti-pattern blocks rather than prose advice.

## Per-rule evidence

### R04 — Description as trigger

The orchestrator description doubles as an invocation guide: it names 7 specific user phrases, states what the loop does in one sentence, lists the 4 artifact classes it handles, and identifies 3 evaluation modes. Every sentence removes ambiguity about when to load the skill.

> Real quote from `skills/SKILL.md:3-11`:
>
> ```
> Use when user says "simmer this", "refine this", "hone this", "iterate on this",
> or asks to improve a specific artifact over multiple rounds. Runs an iterative
> refinement loop with investigation-first judges that read the code, understand
> the problem, and propose evidence-based improvements. Auto-selects single judge
> or multi-judge board based on complexity. Works on any artifact type: documents,
> prompts, specs, emails, creative writing, API designs, pipelines, codebases.
> Supports multi-file workspace targets, runnable evaluators, and open-ended
> optimization (model selection, pipeline topology, prompt tuning).
> ```

The subskill descriptions extend this pattern. Subskill descriptions include a scope boundary ("Do not invoke directly — dispatched as a subagent by the simmer orchestrator") that prevents mistaken direct invocation — combining a trigger with an explicit anti-trigger. A weaker description would say "Generator for simmer" and leave the loading model to guess whether direct invocation is valid.

### R06 — Code examples must be runnable

Both example flows show real inputs, real bash commands, and real trajectory tables with numeric scores. The pipeline example includes model names, actual evaluator commands, and composite scores per iteration — enough to reproduce the run without inference.

> Real quote from `skills/SKILL.md:510-548`:
>
> ```
> User: "Simmer this pipeline — find the best model and prompt setup"
>
> Claude: I'm using the simmer skill to set up iterative refinement.
>
> [Invokes simmer-setup]
>
> Setup identifies: workspace at ./pipeline/
> Evaluator: python evaluate.py --input output.json
> Background: "Available models: claude-sonnet, gpt-4o-mini, llama-8b, llama-70b.
>             Topologies: single-call, multi-step chain, parallel fan-out.
>             Budget: <$0.01/call, <2s latency."
> Criteria: accuracy, cost efficiency, latency
> Iterations: 5
>
> [Iteration 0: Run evaluator on seed, judge scores — 3.7/10]
>   accuracy: 6/10, cost: 2/10, latency: 3/10
>   ASI: "Using claude-sonnet for a simple extraction task. The model is
>        overkill — accuracy is fine but cost is 5x over budget. Switch to
>        gpt-4o-mini which handles extraction well at 1/10th the cost."
>
> [Iteration 1: Generator swaps model + adjusts prompt → 5.3/10]
>   accuracy: 5/10, cost: 8/10, latency: 7/10
>   ASI: "Cost and latency are great now but accuracy dropped on multi-step
>        reasoning tasks (cases 7, 12). Split into two calls — extraction
>        on mini, reasoning on sonnet — to get accuracy back without
>        blowing the budget."
> ```

The example demonstrates the compound loop behaviour (tradeoff between cost and accuracy, 2-step resolution) rather than a toy case that only shows the happy path. A reader who has never seen simmer can infer the generator prompt format, the ASI semantics, and the evaluator integration from this single example.

### R07 — Scope note when related skills exist

The orchestrator opens with a three-row comparison table that positions simmer relative to two sibling skills. Each row is a decision rule: one clause captures the condition, the other names the skill. A reader deciding between the three skills can resolve the choice without loading all three.

> Real quote from `skills/SKILL.md:18-21`:
>
> ```
> **Related skills (test-kitchen family):**
> - `test-kitchen:omakase-off` — don't know what you want → parallel designs → react → pick
> - `test-kitchen:cookoff` — know what you want, it's code → parallel implementations → fixed criteria → steal the best
> - `simmer` — know what you want, it's anything → user-defined criteria → iterate until good
> ```

The scope note inside the "Not simmer" guard on `skills/SKILL.md:84` reinforces this: "If the artifact is code and the user wants parallel implementations, use cookoff instead." Two points of disambiguation, both naming the alternative rather than leaving the model to search.

### R08 — Patterns over theory

Every subskill ends with a "Common Mistakes" section structured as named anti-patterns, each with a two-line problem/fix pair. The section teaches the execution pattern directly — no abstract principles about "how generators work". Each entry is a concrete failure mode with a concrete correction.

> Real quote from `skills/simmer-generator/SKILL.md:89-101`:
>
> ```
> ## Common Mistakes
>
> **Rewriting from scratch**
> - Problem: Loses good parts of the current candidate, introduces regressions
> - Fix: Targeted edits based on ASI, preserve everything else
>
> **Making only one tiny change in workspace mode**
> - Problem: ASI describes a coordinated direction but generator only does part of it
> - Fix: Execute the full direction — if the ASI says "swap model + adjust prompt + update config," do all three
>
> **Making unrelated changes in workspace mode**
> - Problem: Generator "improves" things the ASI didn't mention, introducing noise
> - Fix: Stay focused on the ASI direction. Don't refactor, reorganize, or optimize things that aren't part of the current move.
> ```

Five of the six skill files carry this section. The reflect skill (`skills/simmer-reflect/SKILL.md:157-178`) adds "Dumping evaluator output into the trajectory table" and "Modifying the ASI" — both workspace-mode failure modes that a theory-first skill would address as general principles but that only cause problems in specific execution contexts.

### R49 — CLAUDE.md for Claude, README for humans

The plugin's CLAUDE.md focuses entirely on what Claude needs to understand the system: key design decisions (why context discipline matters, how seed calibration works, ASI semantics), component roles, artifact modes, and evaluation modes. It contains no installation instructions, no marketing copy, and no getting-started prose.

> Real quote from `CLAUDE.md` (Key Design Decisions section):
>
> ```
> **Context discipline:** Generator doesn't see scores (avoids optimizing for numbers). Judge doesn't see
> intermediate scores (avoids anchoring). Reflect is the only subskill that sees the full trajectory.
>
> **Seed calibration:** Judge receives the seed artifact + iteration-0 scores on every iteration as a fixed
> calibration reference. Can score above or below the seed. This compresses score variance across runs.
>
> **ASI (Actionable Side Information):** Judge identifies the highest-leverage direction each round. For
> single-file targets, this is a single focused fix. For workspace targets, this is a single strategic
> direction that may involve coordinated changes across multiple files.
> ```

Each Key Design Decision explains WHY the constraint exists, not just WHAT it is — giving Claude enough context to apply the rule correctly in edge cases the skill doesn't enumerate. A README-style entry for context discipline would say "don't share scores with the generator"; the CLAUDE.md version explains the failure mode (optimizing for numbers), which lets Claude recognize related violations the rule doesn't explicitly cover.

## Worth adopting

**Pattern: Information-boundary table for multi-agent subskills.** Evidence: `skills/SKILL.md:424-429` — the "Context Discipline" table explicitly lists, per subskill, what it receives and what it intentionally does NOT receive, with a one-sentence rationale per row. Why it would be a useful rule: orchestrations with 3+ subskills need a canonical place to state information-flow constraints; a table forces the author to enumerate every agent's view and makes violations visible during review. Proposed rule shape: "**Document information boundaries in a table when orchestrating 3+ subskills.** Without it, subagents receive undeclared context from the prompt, making isolation assumptions implicit and fragile."
