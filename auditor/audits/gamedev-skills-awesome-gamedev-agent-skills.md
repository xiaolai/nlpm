# NLPM Audit: gamedev-skills/awesome-gamedev-agent-skills
**Date**: 2026-04-06  |  **Artifacts**: 67  |  **Strategy**: progressive
**NL Score**: 99/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 18  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/other-engines/bevy-ecs/SKILL.md | skill | 94 | Vague-quantifier overuse ("etc." x3) |
| router/SKILL.md | skill | 96 | Vague-quantifier usage ("relevant" x2) |
| skills/unreal/unreal-cpp-gameplay/SKILL.md | skill | 96 | Vague-quantifier overuse ("etc." x2) |
| skills/unreal/unreal-niagara/SKILL.md | skill | 96 | Vague-quantifier overuse ("etc."/"correctly") |
| skills/disciplines/game-ui-ux/SKILL.md | skill | 96 | Vague quantifiers ("correctly", "etc.") |
| skills/web-engines/threejs-materials-lighting/SKILL.md | skill | 98 | Vague quantifier ("etc.") |
| skills/unity/unity-csharp-scripting/SKILL.md | skill | 98 | Vague quantifier ("correctly") |
| skills/unity/unity-physics/SKILL.md | skill | 98 | Vague quantifier ("correctly") |
| skills/other-engines/roblox-luau/SKILL.md | skill | 98 | Vague quantifier ("appropriate") |
| skills/unreal/unreal-enhanced-input/SKILL.md | skill | 98 | Vague quantifier ("correctly") |
| skills/disciplines/audio-design/SKILL.md | skill | 98 | Vague quantifier ("several") |
| skills/disciplines/procedural-gen/SKILL.md | skill | 98 | Vague quantifier ("several") |
| skills/disciplines/camera-systems/SKILL.md | skill | 98 | Vague quantifier ("correctly") |
| skills/genres/puzzle/SKILL.md | skill | 98 | Vague quantifier ("etc.") |
| skills/genres/fps-shooter/SKILL.md | skill | 98 | Vague quantifier ("relevant") |
| skills/workflows/itch-publish/SKILL.md | skill | 98 | Vague quantifier ("correctly") |
| skills/workflows/game-jam/SKILL.md | skill | 98 | Vague quantifier ("etc.") |
| skills/workflows/prototype-fast/SKILL.md | skill | 98 | Vague quantifier ("properly") |
| skills/web-engines/phaser-arcade-physics/SKILL.md | skill | 100 | None |
| skills/web-engines/threejs-gltf-loading/SKILL.md | skill | 100 | None |
| skills/web-engines/threejs-scene-setup/SKILL.md | skill | 100 | None |
| skills/web-engines/phaser-core/SKILL.md | skill | 100 | None |
| skills/web-engines/pixijs-rendering/SKILL.md | skill | 100 | None |
| skills/unity/unity-navmesh/SKILL.md | skill | 100 | None |
| skills/unity/unity-tilemap-2d/SKILL.md | skill | 100 | None |
| skills/unity/unity-build-pipeline/SKILL.md | skill | 100 | None |
| skills/unity/unity-scriptableobjects/SKILL.md | skill | 100 | None |
| skills/unity/unity-animation/SKILL.md | skill | 100 | None |
| skills/unity/unity-input-system/SKILL.md | skill | 100 | None |
| skills/other-engines/pygame-core/SKILL.md | skill | 100 | None |
| skills/other-engines/roblox-datastores/SKILL.md | skill | 100 | None |
| skills/other-engines/love2d-core/SKILL.md | skill | 100 | None |
| skills/unreal/unreal-behavior-trees/SKILL.md | skill | 100 | None |
| skills/unreal/unreal-blueprints/SKILL.md | skill | 100 | None |
| skills/unreal/unreal-packaging/SKILL.md | skill | 100 | None |
| skills/disciplines/dialogue-systems/SKILL.md | skill | 100 | None |
| skills/disciplines/level-design/SKILL.md | skill | 100 | None |
| skills/disciplines/shader-programming/SKILL.md | skill | 100 | None |
| skills/disciplines/physics-tuning/SKILL.md | skill | 100 | None |
| skills/disciplines/game-ai/SKILL.md | skill | 100 | None |
| skills/disciplines/performance-optimization/SKILL.md | skill | 100 | None |
| skills/disciplines/game-feel/SKILL.md | skill | 100 | None |
| skills/disciplines/input-systems/SKILL.md | skill | 100 | None |
| skills/disciplines/save-systems/SKILL.md | skill | 100 | None |
| skills/genres/visual-novel/SKILL.md | skill | 100 | None |
| skills/genres/card-game/SKILL.md | skill | 100 | None |
| skills/genres/platformer/SKILL.md | skill | 100 | None |
| skills/genres/tower-defense/SKILL.md | skill | 100 | None |
| skills/genres/rpg/SKILL.md | skill | 100 | None |
| skills/genres/roguelike/SKILL.md | skill | 100 | None |
| skills/genres/survival-crafting/SKILL.md | skill | 100 | None |
| skills/workflows/steam-publish/SKILL.md | skill | 100 | None |
| skills/godot/godot-ui-control/SKILL.md | skill | 100 | None |
| skills/godot/godot-gdscript/SKILL.md | skill | 100 | None |
| skills/godot/godot-resources/SKILL.md | skill | 100 | None |
| skills/godot/godot-multiplayer/SKILL.md | skill | 100 | None |
| skills/godot/godot-audio/SKILL.md | skill | 100 | None |
| skills/godot/godot-2d-movement/SKILL.md | skill | 100 | None |
| skills/godot/godot-export/SKILL.md | skill | 100 | None |
| skills/godot/godot-tilemap/SKILL.md | skill | 100 | None |
| skills/godot/godot-shaders/SKILL.md | skill | 100 | None |
| skills/godot/godot-physics/SKILL.md | skill | 100 | None |
| skills/godot/godot-animation/SKILL.md | skill | 100 | None |
| skills/godot/godot-nodes-scenes/SKILL.md | skill | 100 | None |
| skills/godot/godot-signals-groups/SKILL.md | skill | 100 | None |
| skills/godot/godot-3d-essentials/SKILL.md | skill | 100 | None |
| skills/godot/godot-csharp/SKILL.md | skill | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none found |
| Scripts | scripts/validate-skills.py (1 file) |
| MCP configs | none found |
| Package manifests (package.json / requirements.txt) | none found |

### Security Findings
No security findings.

`scripts/validate-skills.py` is a pure-stdlib Python validator (uses only `re`, `sys`, `pathlib`). It only reads files under the repo and prints results to stdout — no network calls, no `subprocess`/`os.system`, no `eval`/`exec`, no credential access, no writes outside the repo, no `sudo`, no PATH modification. The repo ships no hooks, no `.mcp.json`, no `package.json`/`requirements.txt` (no dependency or postinstall surface at all). Execution surface is minimal and clean.

## Bugs (PR-worthy)
No bugs found. Every one of the 67 SKILL.md files (66 skills + router) has valid, well-formed YAML frontmatter with non-empty `name` and `description`; every `name` exactly matches its containing folder (the repo's own convention, enforced by `scripts/validate-skills.py`); every `references/*.md` link resolves to a real file; every file is well under the 500-line cap. `marketplace.json`'s `gamedev` plugin lists exactly 67 skill paths (`./router` + 66 `./skills/**`) which matches the 67 SKILL.md files on disk one-for-one — no manifest/disk drift.

## Security Fixes (PR-worthy, Medium/Low only)
No security fixes to propose — scan came back clean at every severity level.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/other-engines/bevy-ecs/SKILL.md | R01: vague quantifier "etc." x3 (lines 43, 97, 135) | -6 |
| 2 | router/SKILL.md | R01: vague quantifier "relevant" x2 (lines 157, 187) | -4 |
| 3 | skills/unreal/unreal-cpp-gameplay/SKILL.md | R01: vague quantifier "etc." x2 (lines 41, 136) | -4 |
| 4 | skills/unreal/unreal-niagara/SKILL.md | R01: vague quantifiers "etc." (line 41) and "correctly" (line 51) | -4 |
| 5 | skills/disciplines/game-ui-ux/SKILL.md | R01: vague quantifiers "correctly" (line 28) and "etc." (line 54) | -4 |
| 6 | skills/web-engines/threejs-materials-lighting/SKILL.md | R01: vague quantifier "etc." (line 29) | -2 |
| 7 | skills/unity/unity-csharp-scripting/SKILL.md | R01: vague quantifier "correctly" (line 89) | -2 |
| 8 | skills/unity/unity-physics/SKILL.md | R01: vague quantifier "correctly" (line 118) | -2 |
| 9 | skills/other-engines/roblox-luau/SKILL.md | R01: vague quantifier "appropriate" (line 183) | -2 |
| 10 | skills/unreal/unreal-enhanced-input/SKILL.md | R01: vague quantifier "correctly" (line 112) | -2 |
| 11 | skills/disciplines/audio-design/SKILL.md | R01: vague quantifier "several" (line 100) | -2 |
| 12 | skills/disciplines/procedural-gen/SKILL.md | R01: vague quantifier "several" (line 73) | -2 |
| 13 | skills/disciplines/camera-systems/SKILL.md | R01: vague quantifier "correctly" (line 81) | -2 |
| 14 | skills/genres/puzzle/SKILL.md | R01: vague quantifier "etc." (design-knobs table) | -2 |
| 15 | skills/genres/fps-shooter/SKILL.md | R01: vague quantifier "relevant" ("...from the relevant genre") | -2 |
| 16 | skills/workflows/itch-publish/SKILL.md | R01: vague quantifier "correctly" ("...auto-tagged correctly") | -2 |
| 17 | skills/workflows/game-jam/SKILL.md | R01: vague quantifier "etc." ("...phaser-core, etc.") | -2 |
| 18 | skills/workflows/prototype-fast/SKILL.md | R01: vague quantifier "properly" ("...rebuilt properly") | -2 |

Two additional non-penalized observations, noted for completeness:
- `skills/godot/godot-csharp/SKILL.md` pitfalls section makes a specific version-pinned claim ("Android export on 4.5 needs .NET 9") that is worth spot-checking against current Godot release notes as the toolchain evolves, but is not verifiably wrong today.
- `skills/unreal/unreal-niagara/SKILL.md` and `skills/unreal/unreal-packaging/SKILL.md` cite only an external docs URL in their References section rather than a local `references/*.md` deep-dive (unlike most sibling skills). This is a stylistic asymmetry, not a broken link — both are valid, intentional choices for topics with less local detail to add.

## Cross-Component
- `marketplace.json`'s `gamedev` plugin skill list (67 entries: `./router` + 66 `./skills/**` paths) matches the 67 `SKILL.md` files found on disk exactly — no stale-count drift, no orphaned components, no manifest entries pointing at missing skills.
- Every `name:` frontmatter field matches its containing folder name across all 67 files, consistent with the convention enforced by `scripts/validate-skills.py`.
- No contradictions found between sibling skills (e.g. version numbers cited for Unity 6, Unreal 5.4+, Godot 4.x, three.js r147+/r155/r165+/r184, PixiJS v8, Phaser 3.90, LÖVE 11.x, pygame-ce, Bevy 0.16 are consistent across the skills that reference the same engine/library).
- No terminology drift detected between skills that reference each other by name (e.g. `game-jam` and `prototype-fast` cross-reference each other and the engine skills by exact skill-folder name, not a paraphrase).

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

There are no bugs and no security findings to act on. The only outstanding items are 18 minor R01 vague-quantifier nits (each a single-word swap, e.g. "correctly" → a measurable criterion), which are low-value, low-risk PR candidates if the maintainer wants to push this repo from 99/100 to 100/100. This is one of the cleanest audited repos to date: 100% valid frontmatter, 100% resolving references, 100% manifest/disk consistency, and a minimal, harmless execution surface (one stdlib-only validator script, no hooks, no MCP, no dependencies).
