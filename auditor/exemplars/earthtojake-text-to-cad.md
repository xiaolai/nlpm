---
slug: earthtojake-text-to-cad
repo: earthtojake/text-to-cad
audited: 2026-07-20
commit_sha: fdbb4b4fb62d95ae298cfe9a46fdc7092bdaf423
score: 95
exemplifies:
  - R01
  - R04
  - R05
  - R06
  - R07
  - R08
  - R16
  - R34
  - R35
  - R36
---

# Exemplar: earthtojake/text-to-cad

**Score**: 95/100  |  **Date**: 2026-07-20  |  **Commit**: `fdbb4b4fb62d95ae298cfe9a46fdc7092bdaf423`

An 11-skill CAD/robotics plugin (STEP, DXF, G-code, URDF/SRDF/SDF, a live 3D viewer) built on a single canonical `AGENTS.md`, with two skills (`cad-viewer`, `dxf`) scoring 100/100 on this rubric.

## Per-rule evidence

### R01 — No vague quantifiers without criteria

Of the 11 skills, `cad-viewer/SKILL.md` and `dxf/SKILL.md` are the only two with zero vague-quantifier hits in the audit (the other nine were penalized for `relevant`, `appropriate`, `as needed`). `dxf/SKILL.md` replaces vague hedges with named, checkable criteria wherever a lesser skill would reach for "as needed":

> Real quote from `skills/dxf/SKILL.md:77`:
>
> ```
> Verify the generated file with targeted `ezdxf` checks instead of eyeballing: entity counts by type and layer, closed flags on cut profiles, drawing extents, and every dimension the user specified.
> ```

"Instead of eyeballing" plus a concrete enumerated checklist is the R01-compliant substitute for a vaguer instruction like "validate the output as appropriate" — there is nothing left for the agent to guess.

### R04 — Description is a trigger, not a summary

`cad-viewer/SKILL.md`'s frontmatter packs a verb, a file-extension list, and a handoff clause into one sentence — matching real invocation phrasing ("review this .step file") rather than describing the skill in the abstract:

> Real quote from `skills/cad-viewer/SKILL.md:3`:
>
> ```
> description: Start or reuse CAD Viewer and return review links for explicit CAD, implicit CAD, robot-description, and G-code files. Use when visually reviewing `.step`, `.stp`, `.implicit.js`, `.implicit.mjs`, `.glb`, `.stl`, `.3mf`, `.gcode`, `.dxf`, `.urdf`, `.srdf`, or `.sdf` files, especially when handed off from CAD, implicit-cad, G-code, URDF, SRDF, or SDF generation skills.
> ```

Every file extension listed is a literal trigger match against a user's file path, and "especially when handed off from" tells the matcher this skill also fires as a *second* step after another skill runs — not just as an entry point.

### R05 — Under 500 lines

All 11 `SKILL.md` files stay between 66 and 209 lines despite covering dense domains (SendCutSend fabrication preflight, MoveIt2 IK, DXF/STEP projection math):

> Real measurement (`wc -l skills/*/SKILL.md`):
>
> ```
>   209 skills/bambu-labs/SKILL.md
>    95 skills/cad-viewer/SKILL.md
>   102 skills/cad/SKILL.md
>    94 skills/dxf/SKILL.md
>   137 skills/gcode/SKILL.md
>   169 skills/implicit-cad/SKILL.md
>   104 skills/sdf/SKILL.md
>   122 skills/sendcutsend/SKILL.md
>    77 skills/srdf/SKILL.md
>    70 skills/step-parts/SKILL.md
>    66 skills/urdf/SKILL.md
> ```

Domain detail that doesn't need to be in the main body — MoveIt2 server setup, viewer feature lists, URDF frame semantics — is pushed to `references/*.md` (44 cross-checked citations, 0 missing per the audit's Cross-Component section) instead of inflating the skill file itself.

### R06 — Code examples must be runnable

`dxf/SKILL.md` shows the exact function signature a generator source must implement, then the exact CLI invocation to run it, then the exact Python to verify the result — no pseudocode at any step:

> Real quote from `skills/dxf/SKILL.md:50-54,67-70,79-86`:
>
> ```
> def gen_dxf():
>     ...
>     return document
> ```
> ```
> python scripts/dxf path/to/source.py
> python scripts/dxf path/to/source.py -o path/to/output.dxf
> python scripts/dxf path/to/a.py=out/a.dxf path/to/b.py=out/b.dxf
> ```
> ```
> import ezdxf
>
> doc = ezdxf.readfile("path/to/output.dxf")
> msp = doc.modelspace()
> profiles = [e for e in msp.query("LWPOLYLINE") if e.closed]
> holes = msp.query('CIRCLE[layer=="0"]')
> ```

Each block is copy-pasteable against the real `ezdxf`/`scripts/dxf` interfaces, not a stand-in like `# generate the file` — an agent following this skill can run these lines verbatim.

### R07 — Scope note when related skills exist

`dxf/SKILL.md` draws an explicit boundary against the two skills it's most likely to be confused with, naming which one owns which responsibility:

> Real quote from `skills/dxf/SKILL.md:25`:
>
> ```
> Use `$cad` for the 3D part or assembly a DXF derives from. Use `$sendcutsend` for SendCutSend-specific upload preflight.
> ```

The `$skill-name` syntax is used consistently across all 11 skills (verified in the audit: `$cad`, `$cad-viewer`, `$dxf`, `$gcode`, `$bambu-labs`, `$sdf`, `$srdf`, `$step-parts`, `$sendcutsend` all resolve to real sibling directories) — so this scope note isn't just prose, it's a resolvable pointer.

### R08 — Patterns over theory

`dxf/SKILL.md`'s Workflow section is five numbered, situational steps — not an explanation of DXF format theory or ezdxf's API surface:

> Real quote from `skills/dxf/SKILL.md:60-66`:
>
> ```
> 1. Convert the request into a short brief: outline dimensions, holes and slots, layers, units, output path, and validation targets.
> 2. For CAD projections, generate and validate the STEP geometry with `$cad` first, then add or update `gen_dxf()` in the same source. When possible, derive the DXF from in-memory STEP/solid topology rather than duplicating geometry formulas, so the DXF remains a direct projection/unfold of the part being exported.
> 3. Write or edit the Python source with meaningful dimensions as named parameters.
> 4. Run `scripts/dxf` on explicit Python source targets only; do not run directory-wide generation.
> ```

Step 2 in particular encodes a specific engineering judgment call (project from real topology instead of duplicating geometry formulas) as an imperative, not as a paragraph explaining why duplicated geometry drifts.

### R16 — Define output format

`dxf/SKILL.md` closes with an explicit response-shape line instead of leaving the report format to the agent's discretion:

> Real quote from `skills/dxf/SKILL.md:94`:
>
> ```
> Final responses should include generated files, returned viewer links, validation actually run, and assumptions.
> ```

"Validation actually run" (not just "validation") forecloses the failure mode where an agent reports a check it planned but never executed — the audit's DXF/`sdf` rows list this pattern as the reason the two skills scored above their `gcode`/`bambu-labs` siblings, which have no equivalent line and lost 10 points each for it.

### R34 — Include test command

`AGENTS.md`'s Checks section lists the exact test entry point plus scoped variants, so an agent never has to guess how to verify a change:

> Real quote from `AGENTS.md:128-133`:
>
> ```
> Run the smallest path-targeted check that covers the change. Use broad wrappers
> when touching shared surfaces or before handoff:
>
> - Code tests: `scripts/test/test.sh`
> ```

Below this line, `AGENTS.md` also lists `test-js.sh`, `test-docs.sh`, `test-python.sh`, and `test-global.sh` as narrower alternatives — giving the agent a path-scoped choice instead of one blanket command that's slow for small changes.

### R35 — Include architecture overview

`AGENTS.md`'s Repo Map is a one-line-per-directory index that tells an agent where a given kind of change belongs before it starts searching:

> Real quote from `AGENTS.md:40-56`:
>
> ```
> - `skills/`: agent skills and their references/scripts.
> - `plugins/`: versioned agent plugin packages that bundle repo skills.
> - `models/`: sample and durable CAD/robot-description fixtures.
> - `viewer/`: editable CAD Viewer source app.
> - `packages/cadjs`: shared JS CAD/render/runtime code, UI-framework agnostic.
> ```

Each entry states the directory's *role* ("UI-framework agnostic", "dependency-free... vendored into generated... runtimes") rather than just its name, which is what lets the later Repo Rules section say "shared helpers belong in `packages/`" without re-explaining the layout.

### R36 — `@` imports must resolve

`CLAUDE.md` is a one-line import of the canonical `AGENTS.md`, and the import target exists at repo root:

> Real quote from `CLAUDE.md:1`:
>
> ```
> @AGENTS.md
> ```

This is the exact multi-tool pattern NLPM's own conventions recommend (one canonical memory file, thin per-tool importers) — verified live rather than asserted, since `AGENTS.md` is a real 188-line file at the path the import names, not a stub or a dangling reference.

## Worth adopting

Pattern: provenance declaration for dual-distributed skills. Evidence: `skills/cad-viewer/SKILL.md:8-10`, repeated verbatim (with the skill's own repo link) at the top of every one of the 11 `SKILL.md` files:
```
Provenance: maintained in [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad).
Use the installed local skill files as the runtime source of truth; the
repository link is only for provenance and release review.
```
Why it would be a useful rule: this repo ships each skill through two channels — the source tree (`skills/`) and a generated plugin bundle (`plugins/cad/skills/`, byte-identical per the audit's cross-component check) — and a skill with no provenance note leaves an agent unable to tell which copy is the one to edit versus the one to treat as read-only build output. A rule like "**Declare provenance when a skill is distributed through more than one path.** State which copy is the source of truth and which is generated. Without it, agents edit the generated copy and the fix is silently overwritten on the next bundle." would generalize this beyond CAD tooling to any plugin repo that vendors or bundles its own skills.
