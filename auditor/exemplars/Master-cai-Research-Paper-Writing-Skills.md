---
slug: Master-cai-Research-Paper-Writing-Skills
repo: Master-cai/Research-Paper-Writing-Skills
audited: 2026-06-20
commit_sha: 9ee5eddc10068cc52590b3a68a827d3a387f5af9
score: 90
exemplifies:
  - R04
  - R06
  - R07
  - R08
---

# Exemplar: Master-cai/Research-Paper-Writing-Skills

**Score**: 90/100  |  **Date**: 2026-06-20  |  **Commit**: `9ee5eddc10068cc52590b3a68a827d3a387f5af9`

A single-skill Codex plugin for ML/CV/NLP academic writing that earns its score through a dense trigger description, an explicit lazy-loading rule, versioned sentence-skeleton patterns, and a 20-file example bank — all referenced by name rather than inlined.

## Per-rule evidence

### R04 — Description as trigger

The description field packs 6 explicit trigger conditions into 2 sentences, so the agent can decide to load this skill without reading the body.

> Real quote from `research-paper-writing/SKILL.md:3`:
>
> ```
> description: Improve academic paper writing quality for ML/CV/NLP-style papers with clear
> section structure, paragraph flow, and reviewer-facing presentation. Use when drafting or
> revising Abstract, Introduction, Related Work, Method, Experiments, or Conclusion;
> polishing figures/tables; checking claim-support alignment; or performing self-review
> before submission.
> ```

The trigger list is exhaustive but not open-ended: 6 named sections plus 3 distinct task types (polish, check, self-review) give the agent unambiguous activation conditions without hedging phrases like "various writing tasks."

### R06 — Runnable examples

Every pattern in the introduction guide ships with a `Local cite:` pointer to an actual file containing a worked example. The examples/ directory holds 20+ of these files, organized by version label (version-1-task-then-application, pipeline-version-2-two-contributions, etc.) and indexed at `references/examples/index.md`.

> Real quote from `research-paper-writing/references/introduction.md:93-97`:
>
> ```
> Local cite:
>
> 1. `references/examples/introduction/version-1-task-then-application.md`
> ```

And the index states the intended use:

> Real quote from `research-paper-writing/references/examples/index.md:19-20`:
>
> ```
> 2. Open the matching examples file.
> 3. Reuse the sentence logic, not exact wording.
> ```

The distinction "reuse the logic, not the wording" prevents verbatim copying while still giving the agent a concrete model — exactly the output a skill's examples should produce.

### R07 — Scope notes

The skill states the loading constraint twice: once in the Section Guides block and again as an explicit Execution Rule, making it enforceable rather than advisory.

> Real quote from `research-paper-writing/SKILL.md:56`:
>
> ```
> Load only the needed section file:
> ```

> Real quote from `research-paper-writing/SKILL.md:90`:
>
> ```
> Do not load all section references (Introduction/Abstract/Related Work/Method/Experiments/
> Conclusion) at once; load only the specific section guide needed for the current edit target.
> ```

Two separate statements — one in the section index, one in Execution Rules — eliminate the "did the agent read that?" ambiguity. When a scope constraint matters enough to repeat, placing it both at the point of use and in the rule list is the correct pattern.

### R08 — Patterns over theory

The introduction guide is structured as a versioned pattern library, not a prose essay on good writing. Each version has a writing structure list, a sentence skeleton with placeholder tokens, and a `Local cite:` pointer. The sentence skeletons use angle-bracket tokens (`[xxx task]`, `[xxx output]`) that the agent can fill directly.

> Real quote from `research-paper-writing/references/introduction.md:85-96`:
>
> ```
> Writing structure:
>
> 1. Define the task in one clear sentence (`what output` from `what input`).
> 2. Briefly explain the task objective or scope (optional).
> 3. Introduce application value with 2-3 representative scenarios.
>
> Sentence skeleton:
>
> 1. `[xxx task] targets at recovering/reconstructing/estimating [xxx output] from [xxx input].`
> 2. `[xxx task] has a variety of applications such as [xxx], [xxx], and [xxx].`
>
> Local cite:
>
> 1. `references/examples/introduction/version-1-task-then-application.md`
> ```

The skeleton is machine-fillable: an agent copying the sentence structure and substituting the bracketed tokens will produce a grammatically correct first draft without inventing the logical order. This is the difference between a pattern and advice.

## Worth adopting

Pattern: **Anti-pattern section with a named label**. Evidence: `research-paper-writing/references/introduction.md:366-384`, section "Not Recommended Writing" with `Not recommended:` label and a three-point explanation of why the pattern fails ("can erase reader curiosity", "make the idea look straightforward"). Why it would be a useful rule: codifying a mandatory anti-pattern section alongside each pattern group prevents skill consumers from accidentally selecting a known-bad approach, which positive-only pattern lists cannot do.

Pattern: **Output contract with a structured format token**. Evidence: `research-paper-writing/SKILL.md:94-99` — the Output Contract ends with `Claim: ... | Evidence: ... | Status: supported/needs evidence`, a machine-parseable format embedded in the skill body that the agent can echo verbatim. Why it would be a useful rule: an output contract that includes a literal format token (not just a prose description of the format) lets downstream tools parse the agent's output without a separate schema file.
