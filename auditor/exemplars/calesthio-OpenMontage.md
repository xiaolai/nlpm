---
slug: calesthio-OpenMontage
repo: calesthio/OpenMontage
audited: 2026-09-30
commit_sha: 4eab34c5cfcccaa4f1970554928feccce73ee930
score: 95
exemplifies:
  - R04
  - R07
  - R03
  - R05
---

# Exemplar: calesthio/OpenMontage

**Score**: 95/100  |  **Date**: 2026-09-30  |  **Commit**: `4eab34c5cfcccaa4f1970554928feccce73ee930`

A video-production repo with about 85 skills under `.agents/skills/`, about 48 of them mirrored into `.claude/skills/`. Its strongest artifacts pair trigger-phrase descriptions with explicit scope boundaries, and route model behavior through a one-paragraph `CLAUDE.md` pointer.

## Per-rule evidence

### R04 — Description as trigger

`manimce-best-practices` lists four numbered trigger conditions (user phrases, code imports, CLI commands, class names) and then a negative trigger. The description names the exact tokens that should load the skill, so activation does not depend on inference.

> Real quote from `.agents/skills/manimce-best-practices/SKILL.md:3-8`:
>
> ```
> description: |
>   Trigger when: (1) User mentions "manim" or "Manim Community" or "ManimCE", (2) Code contains `from manim import *`, (3) User runs `manim` CLI commands, (4) Working with Scene, MathTex, Create(), or ManimCE-specific classes.
>
>   Best practices for Manim Community Edition - the community-maintained Python animation engine. Covers Scene structure, animations, LaTeX/MathTex, 3D with ThreeDScene, camera control, styling, and CLI usage.
>
>   NOT for ManimGL/3b1b version (which uses `manimlib` imports and `manimgl` CLI).
> ```

Triggers are observable strings (`from manim import *`, `manim` CLI), not topics, and the exclusion separates two libraries whose names differ by one suffix.

The `gsap-*` family uses a shorter form, with a "Use when" clause that lists concrete user intents:

> Real quote from `.agents/skills/threejs-lighting/SKILL.md:3`:
>
> ```
> description: Three.js lighting - light types, shadows, environment lighting. Use when adding lights, configuring shadows, setting up IBL, or optimizing lighting performance.
> ```

The description is one line: a noun-phrase summary, then four task verbs a user would actually type.

### R07 — Scope notes

Two separate scope mechanisms appear. `manimce-best-practices` puts the exclusion in the description (quoted above) and repeats it in a pitfalls list in the body. `gsap-core` adds a "Related skills" line that routes adjacent requests to sibling skills.

> Real quote from `.agents/skills/manimce-best-practices/SKILL.md:125-128`:
>
> ```
> ### Common Pitfalls to Avoid
>
> 1. **Version confusion** - Ensure you're using `manim` (Community), not `manimgl` (3b1b version)
> 2. **Check imports** - `from manim import *` is ManimCE; `from manimlib import *` is ManimGL
> ```

> Real quote from `.agents/skills/gsap-core/SKILL.md:13`:
>
> ```
> **Related skills:** For sequencing multiple steps use **gsap-timeline**; for scroll-linked animation use **gsap-scrolltrigger**; for React use **gsap-react**; for plugins (Flip, Draggable, etc.) use **gsap-plugins**; for helpers (clamp, mapRange, etc.) use **gsap-utils**; for performance use **gsap-performance**.
> ```

The boundary is given as a detection rule (which import belongs to which library) and as a hand-off list naming six sibling skills, so the agent is told where to go when a request falls outside scope.

### R03 — Positive framing

`gsap-core` ends with a "Do Not" section, but each prohibition carries its replacement in the same bullet, so the agent is told what to do instead.

> Real quote from `.agents/skills/gsap-core/SKILL.md:248-252`:
>
> ```
> ## Do Not
>
> - ❌ Animate layout-heavy properties (e.g. `width`, `height`, `top`, `left`) when transform aliases (`x`, `y`, `scale`, `rotation`) can achieve the same effect; prefer transforms for better performance.
> - ❌ Use both **svgOrigin** and **transformOrigin** on the same SVG element; only one applies.
> - ❌ Rely on the default **immediateRender: true** when stacking multiple **from()** or **fromTo()** tweens on the same property of the same target; set **immediateRender: false** on the later tweens so they animate correctly.
> ```

Each bullet names the forbidden property and the substitute (`x`, `y`, `scale`, `rotation`; `immediateRender: false`), with a reason after the semicolon.

### R05 — Body length

The audit scored the skills below at 100/100, and they keep the body short by indexing into rule files. `manimce-best-practices` is 151 lines and links 23 files under `rules/`, each labeled with its content in one clause.

> Real quote from `.agents/skills/manimce-best-practices/SKILL.md:11-18`:
>
> ```
> ## How to use
>
> Read individual rule files for detailed explanations and code examples:
>
> ### Core Concepts
> - [rules/scenes.md](rules/scenes.md) - Scene structure, construct method, and scene types
> - [rules/mobjects.md](rules/mobjects.md) - Mobject types, VMobject, Groups, and positioning
> - [rules/animations.md](rules/animations.md) - Animation classes, playing animations, and timing
> ```

The SKILL.md body stays at 151 lines because detail is loaded on demand from linked files, and each link has a label that tells the agent when to open it.

The root memory file takes the same idea further:

> Real quote from `CLAUDE.md:1-9`:
>
> ```
> # OpenMontage
>
> **MANDATORY: Read [`AGENT_GUIDE.md`](AGENT_GUIDE.md) before responding to ANY user message.**
>
> Do not act on the user's request until you have read AGENT_GUIDE.md.
> It contains routing rules that determine your first action based on what the user asked.
> Skipping it WILL cause you to take the wrong action.
>
> There are no instructions in this file. All instructions are in AGENT_GUIDE.md.
> ```

`CLAUDE.md` is 9 lines and holds one pointer, so the instructions live in a single file (`AGENT_GUIDE.md`, which the audit confirmed resolves) and are not duplicated across `AGENTS.md`, `CODEX.md`, `COPILOT.md` and `CURSOR.md`.

## Worth adopting

Pattern: Single-pointer memory file. Evidence: `CLAUDE.md:1-9`. Why it would be a useful rule: a memory file that states "there are no instructions in this file" and defers to one guide prevents the drift that appears when the same routing rules are copied across per-tool memory files.

Pattern: Negative trigger in the description. Evidence: `.agents/skills/manimce-best-practices/SKILL.md:8`. Why it would be a useful rule: when two libraries share a name stem (`manim`/`manimgl`), a `NOT for <sibling> (which uses <distinguishing token>)` line in the description stops the wrong skill from loading at trigger time, before the body is read.
