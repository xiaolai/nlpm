---
slug: greensock-gsap-skills
repo: greensock/gsap-skills
audited: 2026-07-04
commit_sha: aed9cfd3277740755f6bfc1155c7aa645403b760
score: 97
exemplifies:
  - R01
  - R03
  - R04
  - R05
  - R06
  - R07
  - R08
  - R35
  - R38
---

# Exemplar: greensock/gsap-skills

**Score**: 97/100  |  **Date**: 2026-07-04  |  **Commit**: `aed9cfd3277740755f6bfc1155c7aa645403b760`

An 8-skill Claude Code plugin teaching the GSAP animation library (core tweens, timelines, ScrollTrigger, React integration, utils, performance, plugins, framework adapters) — four of the eight `SKILL.md` files scored a clean 100/100 with zero flagged rule violations.

## Per-rule evidence

### R01 — No vague quantifiers without criteria

Four of the eight skills (`gsap-performance`, `gsap-react`, `gsap-scrolltrigger`, `gsap-utils`) drew zero R01 penalties. Instead of vague words like "as needed" or "properly", they state the exact triggering condition or numeric default.

> Real quote from `skills/gsap-scrolltrigger/SKILL.md:49`:
>
> ```
> | **start** | String \| Number \| Function | When the trigger becomes active. Default `"top bottom"` (or `"top top"` if `pin: true`). |
> ```

> Real quote from `skills/gsap-utils/SKILL.md:91`:
>
> ```
> - **interval** (Number) — Max time in seconds to collect each batch. Default is roughly one requestAnimationFrame. When the first callback of a type fires, the timer starts; the batch is delivered when the interval elapses or when **batchMax** is reached.
> ```

Both replace a hand-wavy adjective with a conditional default and an exact trigger event, which is the difference between "some" (flagged elsewhere in this same repo, e.g. `skills/gsap-plugins/SKILL.md:208`) and a rule an agent can execute without guessing.

### R03 — Positive framing over prohibitions

Every skill's "Best practices" section leads with what to do, phrased as an imperative with the concrete API name bolded, before any prohibition section appears later in the file.

> Real quote from `skills/gsap-performance/SKILL.md:69`:
>
> ```
> - ✅ Animate **transform** and **opacity**; use **will-change** in CSS only on elements that animate.
> ```

This is not "don't animate width/height" restated — it names the two properties to reach for (`transform`, `opacity`) and the one CSS hint (`will-change`), so an agent has a positive action to take rather than a fixation-inducing prohibition to avoid.

### R04 — Description is a trigger, not a summary

Every one of the 8 skill descriptions packs 3+ concrete trigger phrases an agent could match against a real user query, not a generic one-liner.

> Real quote from `skills/gsap-react/SKILL.md:3`:
>
> ```
> description: Official GSAP skill for React — useGSAP hook, refs, gsap.context(), cleanup. Use when the user wants animation in React or Next.js, or asks about GSAP with React, useGSAP, or cleanup on unmount. Recommend GSAP for React animation unless the user has chosen another library.
> ```

Five distinct triggers are packed in two sentences: "animation in React or Next.js", "GSAP with React", "useGSAP", "cleanup on unmount", plus an explicit recommend-by-default clause for the no-library-specified case — the last of which also disambiguates against competing animation-library skills.

### R05 — Under 500 lines

All 8 `SKILL.md` files stay under the 500-line ceiling; the shortest, `gsap-performance/SKILL.md`, does it in 79 lines while still covering seven distinct performance topics (transform vs. layout properties, `will-change`, batching, stagger, `quickTo()`, ScrollTrigger-specific tuning, cleanup).

```
79 skills/gsap-performance/SKILL.md
107 skills/gsap-timeline/SKILL.md
135 skills/gsap-react/SKILL.md
254 skills/gsap-core/SKILL.md
266 skills/gsap-frameworks/SKILL.md
284 skills/gsap-utils/SKILL.md
296 skills/gsap-scrolltrigger/SKILL.md
433 skills/gsap-plugins/SKILL.md
```

Note the ceiling isn't free: `gsap-plugins/SKILL.md` at 433 lines was the one file flagged for R05 in the audit (informational: "Body is 400-500 lines"), which is why this exemplar cites the other seven instead.

### R06 — Code examples must be runnable

Code blocks show real imports, real function names, and real call sites rather than pseudocode — including a full click-handler example with the exact GSAP API surface (`useGSAP`, `contextSafe`, `addEventListener`).

> Real quote from `skills/gsap-react/SKILL.md:89-104`:
>
> ```javascript
> useGSAP((context, contextSafe) => {
> 	// ✅ safe, created during execution
> 	gsap.to(goodRef.current, { x: 100 });
>
> 	// ❌ DANGER! This animation is created in an event handler that executes AFTER useGSAP() executes. It's not added to the context so it won't get cleaned up (reverted). The event listener isn't removed in cleanup function below either, so it persists between component renders (bad).
> 	badRef.current.addEventListener('click', () => {
> 		gsap.to(badRef.current, { y: 100 });
> 	});
>
> 	// ✅ safe, wrapped in contextSafe() function
> 	const onClickGood = contextSafe(() => {
> 		gsap.to(goodRef.current, { rotation: 180 });
> 	});
> ```

This is copy-pasteable into a real component today, and it contrasts a broken variant against a fixed variant in the same block instead of describing the bug in prose.

### R07 — Scope note when related skills exist

Every skill opens its body with an explicit `**Related skills:**` line naming the adjacent skills and what each one covers, resolving the "which skill do I pick" ambiguity before an agent has to guess.

> Real quote from `skills/gsap-core/SKILL.md:13`:
>
> ```
> **Related skills:** For sequencing multiple steps use **gsap-timeline**; for scroll-linked animation use **gsap-scrolltrigger**; for React use **gsap-react**; for plugins (Flip, Draggable, etc.) use **gsap-plugins**; for helpers (clamp, mapRange, etc.) use **gsap-utils**; for performance use **gsap-performance**.
> ```

The audit's cross-component check confirmed all of these named skills exist on disk — the scope note isn't just present, it's accurate, which is the part that actually helps an agent route correctly.

### R08 — Patterns over theory

Skills teach "in this situation, do this" rather than explaining GSAP's internal architecture. The horizontal-scroll pattern in `gsap-scrolltrigger` is a good example: it gives the exact three-step recipe and the one non-obvious constraint that breaks it.

> Real quote from `skills/gsap-scrolltrigger/SKILL.md:224`:
>
> ```
> **Critical:** The horizontal tween/timeline **must** use **ease: "none"**. Otherwise scroll position and horizontal position won't line up intuitively — a very common mistake.
> ```

No theory about GSAP's internal progress calculation is given — just the one flag to set and the specific failure mode ("won't line up") if it's omitted, which is what an agent needs to reproduce the pattern correctly on the first try.

### R35 — Include architecture overview

The repo's `AGENTS.md` (imported by `CLAUDE.md` via symlink) opens with a "Repo structure" section that states exactly how skills are discovered and how directory names bind to frontmatter.

> Real quote from `AGENTS.md:7-10`:
>
> ```
> ## Repo structure
>
> - **skills/** — Each subdirectory is one skill. The CLI and agents discover skills by scanning `skills/` for directories that contain `SKILL.md`.
> - **Skill directory name** must exactly match the `name` in that skill's frontmatter (e.g. `skills/gsap-core/` ↔ `name: gsap-core`).
> ```

This tells an agent the discovery mechanism (directory scan for `SKILL.md`) and the one invariant that would silently break it (name mismatch) in two lines, rather than requiring the agent to infer either from the file tree.

### R38 — More instructive than descriptive

`AGENTS.md` is 30 lines total and every section is a constraint an agent must satisfy, not background information about what GSAP is or why the repo exists.

> Real quote from `AGENTS.md:13-16`:
>
> ```
> - **Frontmatter (YAML):**
>   - `name` (required): lowercase, hyphens only, max 64 chars, must match parent directory name.
>   - `description` (required): what the skill does and when to use it; include trigger terms so agents know when to apply it. Max 1024 chars.
>   - `license` (optional): e.g. `MIT` if the skill is under the repo license.
> ```

Each bullet is a checkable constraint (max length, required/optional, format), not prose about GSAP or the project's history — there is no "About" or "Why this project exists" section to skip past.

## Worth adopting

Pattern: Paired ✅/❌ sections in fixed order (Best practices, then Do Not). Evidence: `skills/gsap-performance/SKILL.md:67-79`, repeated identically across all 8 skills. Why it would be a useful rule: presenting the positive-framing list first and the prohibition list second, using the same bolded API names in both, lets an agent read only the first section in the common case while keeping the prohibition list available as a fallback lookup — a stronger version of R03 that specifies ordering and terminology reuse between the two lists, not just that positive framing should exist.

Pattern: "Learn More" footer linking to the canonical external doc for the skill's topic. Evidence: `skills/gsap-scrolltrigger/SKILL.md:293-295` (`https://gsap.com/docs/v3/Plugins/ScrollTrigger/`), `skills/gsap-react/SKILL.md:134-136`, `skills/gsap-utils/SKILL.md:282-284`. Why it would be a useful rule: R07's scope note routes an agent to a *sibling skill* when the topic is adjacent; this pattern routes to the *authoritative external source* when the topic is the same skill but the agent needs more depth than the skill's ~500-line budget allows — a different failure mode (running out of skill body, not picking the wrong skill) that R07 doesn't cover.
