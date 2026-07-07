---
slug: gamedev-skills-awesome-gamedev-agent-skills
repo: gamedev-skills/awesome-gamedev-agent-skills
audited: 2026-07-07
commit_sha: 9d0fa9612225d51d9a89f0a0c6f0fe15d85e3ee0
score: 99
exemplifies:
  - R04
  - R05
  - R06
  - R07
  - R08
---

# Exemplar: gamedev-skills/awesome-gamedev-agent-skills

**Score**: 99/100  |  **Date**: 2026-07-07  |  **Commit**: `9d0fa9612225d51d9a89f0a0c6f0fe15d85e3ee0`

A 67-file game-development skills collection (one router + 66 engine/discipline/genre/workflow
skills) covering Godot, Unity, Unreal, Bevy, and five web/other engines; scored 99/100 with zero
bugs and zero security findings.

## Per-rule evidence

### R04 — Description is a trigger, not a summary

`router/SKILL.md` packs the full dispatch surface — every engine it detects and every task
category it routes — into the frontmatter `description`, so Claude can pick the router without
reading its body.

> Real quote from `router/SKILL.md:3-11`:
>
> ```
> description: >
>   Routes any game-development request to the right specialized skill(s): it detects the engine
>   (Godot, Unity, Unreal, Bevy, Phaser, PixiJS, three.js, LÖVE, pygame, Roblox) and the task, then
>   reads the chosen skill before acting. Use to make a game or to decide which skill applies — for
>   players, levels, enemies, shaders, UI/UX, cameras, game feel, physics, input, audio, saving,
>   multiplayer, AI, dialogue, procedural generation, or performance, for genres (platformer,
>   roguelike, RPG, FPS, tower-defense, card game, visual novel, survival-crafting, puzzle), and for
>   shipping (game jam, Steam, itch). Start here
>   when unsure which gamedev skill to use.
> ```

This isn't "helpful game dev skill" — it names 10 engines, 13 disciplines, 9 genres, and 4
workflow keywords, each a phrase a real user query would contain, plus the explicit trigger
"Start here when unsure which gamedev skill to use."

### R05 — Under 500 lines

Every one of the 67 files is well under the 500-line cap the repo's own validator enforces at
`scripts/validate-skills.py:29` (`MAX_LINES = 500`). `router/SKILL.md` — the single skill with the
largest surface to describe (10 engines × 3 task categories) — is 212 lines; `godot-gdscript/
SKILL.md` is 136 lines.

> From `scripts/validate-skills.py:113-116`:
>
> ```
>     # line count
>     line_count = len(text.splitlines())
>     if line_count >= MAX_LINES:
>         errors.append(f"file is {line_count} lines (must be < {MAX_LINES})")
> ```

The cap isn't just followed, it's mechanically enforced on every commit — the repo doesn't rely
on authors remembering the rule.

### R06 — Code examples must be runnable

`skills/godot/godot-gdscript/SKILL.md` shows four complete, pasteable GDScript snippets — not
pseudocode — each demonstrating one real API surface (typed export/onready, 4.x signal
`Callable` syntax, `await`, typed arrays).

> Real quote from `skills/godot/godot-gdscript/SKILL.md:68-87`:
>
> ```gdscript
> extends Node
>
> signal health_changed(current: int, maximum: int)   # typed signal params
>
> var health := 100
>
> func take_damage(amount: int) -> void:
>     health = max(health - amount, 0)
>     health_changed.emit(health, 100)     # 4.x: emit as a method on the signal
>
> func _ready() -> void:
>     # 4.x: connect with a Callable, not a string method name.
>     health_changed.connect(_on_health_changed)
>
> func _on_health_changed(current: int, maximum: int) -> void:
>     print("HP: %d/%d" % [current, maximum])
> ```

The inline comments call out the exact thing that trips up a model trained on older material —
`emit_signal("x")` vs. `x.emit(...)`, string-based `connect` vs. `Callable` — instead of showing
generic signal syntax with no version anchor.

### R07 — Scope note when related skills exist

Both the router and the leaf skills state explicitly when *not* to use them, pointing at the
sibling skill that should be read instead.

> Real quote from `skills/godot/godot-gdscript/SKILL.md:28-30`:
>
> ```
> **When *not* to use:** scene/node structure and instancing questions →
> `godot-nodes-scenes`; signal *architecture*/decoupling patterns →
> `godot-signals-groups`; using C# instead of GDScript → `godot-csharp`.
> ```

> Real quote from `router/SKILL.md:34-36`:
>
> ```
> **When *not* to use:** once the right skill is loaded and the task is squarely inside it, work
> from that skill — don't re-run the router every turn. Re-route only when the task **pivots** to a
> new engine or concern (router step 6).
> ```

Three named alternatives with a one-clause reason each — a model deciding between
`godot-gdscript`, `godot-nodes-scenes`, and `godot-signals-groups` doesn't have to guess from
three overlapping descriptions.

### R08 — Patterns over theory

`router/SKILL.md` teaches routing as a lookup table keyed on concrete trigger phrases, not an
abstract description of "how a router works."

> Real quote from `router/SKILL.md:109-123` (Disciplines table, excerpted):
>
> ```
> | Concept (`says:`) | Discipline skill | Pairs with (engine API) |
> |-------------------|------------------|-------------------------|
> | enemy AI, behavior tree, pathfinding, steering | `game-ai` | `unity-navmesh` / `unreal-behavior-trees` / Godot nav |
> | procedural, noise, seed, dungeon generator | `procedural-gen` | engine tilemap/grid skill |
> | shader, fragment, dissolve/outline | `shader-programming` | `godot-shaders` / engine material |
> | screen shake, hit-stop, juice, squash & stretch, "make it punchy" | `game-feel` | engine animation/tween + `camera-systems` (shake) |
> ```

Instead of explaining what a discipline skill *is*, the table maps the literal words a user would
type ("make it punchy", "dungeon generator") straight to the skill and engine API to pair it
with — the situation-to-action mapping R08 asks for, not a taxonomy lecture.

## Worth adopting

Pattern: progressive-disclosure router with an announce step. Evidence: `router/SKILL.md:148-161`
— the router specifies three read tiers (preloaded frontmatter only → chosen skill body → `references/`
on demand) and requires narrating the choice: *"Detected Godot (`project.godot`). Loading
`godot-2d-movement` for the controller and `platformer` for jump feel..."* Why it would be a useful
rule: R05 caps a single file's length, but a 67-skill collection still risks context bloat if an
orchestrating skill bulk-loads sibling bodies before knowing which one is needed; a router that
states its own read-order (frontmatter → body → reference) and echoes the decision back extends
the token-discipline principle from one file to an entire skill tree, and gives the user a visible
checkpoint to catch a wrong route before it burns context on the wrong skill.
