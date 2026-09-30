---
slug: danny-avila-LibreChat
repo: danny-avila/LibreChat
audited: 2026-09-30
commit_sha: 14f7b2865692d27364c934ecb9912496371018bb
score: 97
exemplifies:
  - R04
  - R05
  - R06
  - R07
  - R08
---

# Exemplar: danny-avila/LibreChat

**Score**: 97/100  |  **Date**: 2026-09-30  |  **Commit**: `14f7b2865692d27364c934ecb9912496371018bb`

Two project skills under `.claude/skills/` (`codebase-design`, `improve-codebase-architecture`): the first defines a shared glossary and lists terms to avoid, the second is a command-style skill that loads that glossary and hands deeper material to sibling files by relative link.

## Per-rule evidence

### R04 — Description as trigger

`codebase-design` lists five situations that should load it, phrased as things a user would ask for, and names a sixth case: another skill needing the vocabulary.

> Real quote from `.claude/skills/codebase-design/SKILL.md:3`:
>
> ```
> description: Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.
> ```

It opens with what the skill is, then gives "Use when" with five action phrases (design/improve an interface, find deepening opportunities, decide where a seam goes, make code testable or AI-navigable) rather than restating the title.

### R05 — Body length

Both skills stay far under the 500-line limit by pushing detail into sibling files instead of one long body.

> Real quote from `wc -l .claude/skills/*/*.md`:
>
> ```
>  37 codebase-design/DEEPENING.md
>  44 codebase-design/DESIGN-IT-TWICE.md
> 114 codebase-design/SKILL.md
> 123 improve-codebase-architecture/HTML-REPORT.md
>  71 improve-codebase-architecture/SKILL.md
> ```

The largest file is 123 lines; the HTML scaffold for `improve-codebase-architecture` lives in `HTML-REPORT.md` and is reached by a single link (`SKILL.md:58`), so the main body carries only the process.

### R06 — Runnable examples

The testability section shows each bad/good pair as real TypeScript in fenced blocks, with the testable and hard-to-test versions side by side.

> Real quote from `.claude/skills/codebase-design/SKILL.md:71-80`:
>
> ```
> 1. **Accept dependencies, don't create them.**
>
>    ```typescript
>    // Testable
>    function processOrder(order, paymentGateway) {}
>
>    // Hard to test
>    function processOrder(order) {
>      const gateway = new StripeGateway();
>    }
>    ```
> ```

Each pair is labelled with its outcome ("Testable" / "Hard to test") so the contrast is the lesson. The bodies are empty stubs, so this is at the edge of "runnable"; the value is that the signature-level difference is real syntax.

### R07 — Scope notes

`improve-codebase-architecture` states which skill owns the vocabulary and which owns the domain glossary, and `codebase-design` routes deeper topics to named sibling files. Claude is told which artifact to load for which question.

> Real quote from `.claude/skills/improve-codebase-architecture/SKILL.md:11-14`:
>
> ```
> This command is _informed_ by the project's domain model and built on a shared design vocabulary:
>
> - Run the `/codebase-design` skill for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Use these terms exactly in every suggestion — don't drift into "component," "service," "API," or "boundary."
> - The domain language in `CONTEXT.md` gives names to good seams; ADRs in `docs/adr/` record decisions this command should not re-litigate.
> ```

> Real quote from `.claude/skills/codebase-design/SKILL.md:111-114`:
>
> ```
> ## Going deeper
>
> - **Deepening a cluster given its dependencies** — see [DEEPENING.md](DEEPENING.md): dependency categories, seam discipline, and replace-don't-layer testing.
> - **Exploring alternative interfaces** — see [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md): spin up parallel sub-agents to design the interface several radically different ways, then compare on depth, locality, and seam placement.
> ```

Each pointer states what the target file covers, and the audit confirmed all three relative links resolve. The domain vocabulary (`CONTEXT.md`) and the architecture vocabulary (`/codebase-design`) are assigned separate jobs.

### R08 — Patterns over theory

Abstract principles are each paired with an operational test Claude can run, and rejected alternatives are listed so it does not slip back to them.

> Real quote from `.claude/skills/codebase-design/SKILL.md:63-65`:
>
> ```
> - **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
> - **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape.
> - **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a seam unless something actually varies across it.
> ```

Each principle ends in a decision Claude can make on a specific module (delete it mentally, count adapters), not a definition to recite.

## Worth adopting

Pattern: Glossary with an `_Avoid_:` list per term. Evidence: `.claude/skills/codebase-design/SKILL.md:14` (`**Module** — ... _Avoid_: unit, component, service.`) and `SKILL.md:16`, `:22`. Why it would be a useful rule: a skill that defines vocabulary should name the synonyms it replaces, so Claude and downstream skills do not drift back to them (R01 covers vague words, not competing terms).

Pattern: "Rejected framings" section. Evidence: `.claude/skills/codebase-design/SKILL.md:105-109`. Why it would be a useful rule: recording alternatives already considered and why they lost stops Claude from re-proposing them, which R08 alone does not cover.
