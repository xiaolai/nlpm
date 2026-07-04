---
slug: bergside-awesome-design-skills
repo: bergside/awesome-design-skills
audited: 2026-07-04
commit_sha: f631a09b4fcc0166f2e2c1a8c81906ef680c57e8
score: 98
exemplifies:
  - R04
  - R02
  - R03
  - R05
  - R08
---

# Exemplar: bergside/awesome-design-skills

**Score**: 98/100  |  **Date**: 2026-07-04  |  **Commit**: `f631a09b4fcc0166f2e2c1a8c81906ef680c57e8`

A registry of 67 machine-generated `SKILL.md` design-system guideline files (one per visual style — "brutalism", "glassmorphism", "minimal", etc.), each paired with a human-facing `DESIGN.md` sidecar and indexed by `skills/index.json`; every file shares one template, so a single R01 line (`"as relevant"`) is the corpus's only quality flag across all 67 artifacts.

## Per-rule evidence

### R04 — Description is a trigger, not a summary

With 67 skills covering overlapping visual territory (bold vs. dramatic vs. artistic; retro vs. vintage vs. pacman), the description is the only signal a picker has to disambiguate them. Each one packs concrete, differentiating nouns instead of generic praise:

> Real quotes from `skills/*/SKILL.md` frontmatter:
>
> ```
> skills/pacman/SKILL.md:      description: Retro arcade-inspired design with pixel fonts, dotted borders, playful high-contrast colors, and 8-bit game aesthetics.
> skills/claymorphism/SKILL.md: description: Soft, rounded 3D-like shapes mimicking malleable clay with playful, puffy elements and colorful surfaces.
> skills/agentic/SKILL.md:      description: Conversational AI-first interface with minimal controls, clear outcomes, and delegated task flows for agentic workflows.
> ```

None of these read as "helpful design skill." Each names the specific visual mechanics (pixel fonts, dotted borders, puffy elements, delegated task flows) that separate it from its 66 siblings — the test a trigger description has to pass when the corpus is this dense.

### R02 — Every line must earn its tokens

`## Style Foundations` states tokens as data, not prose. From `skills/agentic/SKILL.md:19-23`:

> ```
> - Visual style: modern, bold
> - Typography scale: 14/16/18/24/32/40 | Fonts: primary=Playfair Display, display=Playfair Display, mono=JetBrains Mono | weights=100, 200, 300, 400, 500, 600, 700, 800, 900
> - Color palette: surface/subtle layers | Tokens: primary=#FF5701, secondary=#F6F6F1, success=#16A34A, warning=#D97706, danger=#DC2626, surface=#FFFFFF, text=#111827
> - Spacing scale: 8pt baseline grid
> ```

There's no "our typography system is carefully considered for maximum readability" filler — every token is a literal value (`#FF5701`, `14/16/18/24/32/40`) an agent can act on directly, with no interpretation step in between.

### R03 — Positive framing over prohibitions

`## Rules: Do` leads every skill and outnumbers `## Rules: Don't`. From `skills/agentic/SKILL.md:32-38`:

> ```
> ## Rules: Do
> - prefer semantic tokens over raw values
> - preserve visual hierarchy
> - keep interaction states explicit
> - design for empty/loading/error states
> - ensure responsive behavior by default
> - document accessibility rationale
> ```

Six affirmative actions before a single prohibition appears. Compare a weak version — "don't use raw hex values, don't skip empty states, don't forget accessibility" — which reads as a checklist of things to avoid rather than a spec for what to build.

### R05 — Under 500 lines

Every one of the 67 `SKILL.md` files runs 83–90 lines total (frontmatter through the closing `<!-- TYPEUI_SH_MANAGED_END -->` marker) — `skills/minimal/SKILL.md` ends at line 83, `skills/agentic/SKILL.md` at line 89. At 67 files that could have been one 6,000-line mega-skill, the corpus instead stays scoped one style per file, each a sixth of the 500-line ceiling.

### R08 — Patterns over theory

`## Quality Gates` and `## Guideline Authoring Workflow` tell the *generating* agent to anchor rules in specifics rather than restate design theory. From `skills/agentic/SKILL.md:78-82`:

> ```
> ## Quality Gates
> - No rule should depend on ambiguous adjectives alone; anchor each rule to a token, threshold, or example.
> - Every accessibility statement must be testable in implementation.
> - Prefer system consistency over one-off local optimizations.
> - Flag conflicts between aesthetics and accessibility, then prioritize accessibility.
> ```

This is a skill file instructing its own consumer to avoid the exact defect class R01 penalizes ("ambiguous adjectives alone") — a template that teaches the anti-vagueness pattern it (mostly) follows itself, rather than asserting "write good accessibility rules" and leaving the standard implicit.

## Worth adopting

Pattern: machine/human file split with a manifest cross-check. Evidence: `skills/agentic/SKILL.md` (agent-facing instructions) is paired 1:1 with `skills/agentic/DESIGN.md` (human-facing rationale — same color tokens restated as prose: `` **Primary (#FF5701):** Token from style foundations. ``), and `skills/index.json` maps `skillPath`/`designPath` for both. The audit report confirms zero drift: "all 67 keys match all 67 `skills/*/SKILL.md` directories exactly." Why it would be a useful rule: when a skill's tokens/values need a human-readable rationale doc alongside the agent-facing spec, a manifest that enumerates both paths per entry gives a cheap, deterministic way to catch drift between the two — the same check nlpm's checker already runs for cross-component consistency, but expressed here as a single JSON file instead of prose cross-references.
