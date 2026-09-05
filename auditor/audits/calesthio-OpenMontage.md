# NLPM Audit: calesthio/OpenMontage
**Date**: 2026-04-06  |  **Artifacts**: 152  |  **Strategy**: progressive
**NL Score**: 95/100
**Security**: REVIEW
**Bugs**: 21  |  **Quality Issues**: 15  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .agents/skills/motion-graphics/agents/director.md | agent | 55/100 | No frontmatter/model/examples; broken ref to `references/shot-plan-ir.md` |
| .agents/skills/motion-graphics/agents/builder.md | agent | 55/100 | No frontmatter/model/examples; broken refs `catalog-map.md`, `references/builder-contract.md` |
| .agents/skills/motion-graphics/agents/finalize.md | agent | 55/100 | No frontmatter, no declared model, zero example blocks |
| .agents/skills/ltx2/SKILL.md | skill | 55/100 | Documents nonexistent `tools/ltx2.py` CLI; real tool is `tools/video/ltx_video_modal.py` |
| .agents/skills/manimgl-best-practices/SKILL.md | skill | 65/100 | 5 broken example file links (L51-55) |
| .agents/skills/website-to-video/SKILL.md | skill | 68/100 | Broken relative refs to hyperframes techniques/html-in-canvas docs (L144-145) |
| .claude/skills/video_toolkit/SKILL.md | skill | 70/100 | Directory name `video_toolkit` mismatches frontmatter `name: video-toolkit` |
| .agents/skills/d3-viz/SKILL.md | skill | 78/100 | Template refs `.js`, real files are `.jsx` (L814-815) |
| .agents/skills/remotion/SKILL.md | skill | 80/100 | Broken ref to nonexistent `remotion-official` skill |
| .agents/skills/acestep/SKILL.md | skill | 80/100 | Wrong tool path `tools/music_gen.py` + nonexistent `tools/sfx.py` |
| .agents/skills/video-toolkit/SKILL.md | skill | 85/100 | Duplicate `#### 4e.` heading; `MODAL_DEWATERMARK_ENDPOINT_URL` env var has no matching deploy step |
| .claude/commands/animated-drawing.md | command | 85/100 | Missing `allowed-tools`; no empty-input handling |
| .claude/commands/ink-art.md | command | 85/100 | Missing `allowed-tools`; no empty-input handling |
| .claude/skills/ai-video-gen/SKILL.md | skill | 87/100 | Stale vs `.agents/skills/ai-video-gen/SKILL.md` — missing Kling Official gateway (supplementary finding, see note below) |
| .agents/skills/remotion-best-practices/SKILL.md | skill | 90/100 | Broken ref `rules/sound-effects.md` (real file: `sfx.md`) |
| .agents/skills/beautiful-mermaid/SKILL.md | skill | 90/100 | Requires nonexistent `agent-browser` skill (L12) |
| .agents/skills/synthetic-screen-recording/SKILL.md | skill | 90/100 | Broken ref to nonexistent `projects/openmontage-showcase/build_composition.py` (L182) |
| .agents/skills/vercel-react-best-practices/SKILL.md | skill | 90/100 | Claims "65 rules" — 68 rule files exist (L12) |
| .claude/skills/vercel-react-best-practices/SKILL.md | skill | 90/100 | Claims "65 rules" — 68 rule files exist (L12) |
| .agents/skills/ffmpeg/SKILL.md | skill | 90/100 | Self-ref path assumes `.claude/` tree while file lives under `.agents/` (L432) |
| .claude/skills/ffmpeg/SKILL.md | skill | 90/100 | Self-ref path assumes `.claude/` tree (L432) |
| .agents/skills/video-understand/SKILL.md | skill | 90/100 | Script paths missing `.agents/`/`.claude/` tree prefix (L22-43) |
| .claude/skills/video-understand/SKILL.md | skill | 90/100 | Script paths missing tree prefix (L22-43) |
| .cursor/commands/animated-drawing.md | command | 90/100 | No YAML frontmatter (non-Claude-Code format; may be intentional for Cursor) |
| .cursor/commands/backlot.md | command | 90/100 | No YAML frontmatter (may be intentional for Cursor) |
| .cursor/commands/ink-art.md | command | 90/100 | No YAML frontmatter (may be intentional for Cursor) |
| .claude/commands/backlot.md | command | 95/100 | Missing `allowed-tools`; unsanitized `$ARGUMENTS` in bash block — see Security |
| .agents/skills/motion-graphics/SKILL.md | skill | 95/100 | Broken ref `motion-graphics-genre.md` (L172) |
| .agents/skills/flux-best-practices/SKILL.md | skill | 96/100 | Vague "optimal"/"Comprehensive" |
| .agents/skills/visual-style/SKILL.md | skill | 96/100 | Vague "appropriate" x2 (L41, L50) |
| .claude/skills/visual-style/SKILL.md | skill | 96/100 | Vague "appropriate" x2 (L41, L50) |
| .agents/skills/ai-video-gen/SKILL.md | skill | 97/100 | `allowed-tools: mcp__heygen__*` declared, never invoked in body |
| .agents/skills/video-translate/SKILL.md | skill | 97/100 | `allowed-tools: mcp__heygen__*` declared, never invoked in body |
| .agents/skills/faceswap/SKILL.md | skill | 97/100 | `allowed-tools: mcp__heygen__*` declared, never invoked in body |
| .agents/skills/agents/references/agent-configuration.md | reference | 98/100 | Vague "relevant" (L279) |
| .claude/skills/agents/references/agent-configuration.md | reference | 98/100 | Vague "relevant" (L279) |
| .agents/skills/agents/references/client-tools.md | reference | 98/100 | Vague "reasonable" (L463) |
| .claude/skills/agents/references/client-tools.md | reference | 98/100 | Vague "reasonable" (L463) |
| .agents/skills/remotion-to-hyperframes/SKILL.md | skill | 98/100 | Vague "relevant" (L95) |
| .agents/skills/comfyui/SKILL.md | skill | 98/100 | Vague "usually" (L27) |
| .agents/skills/seedance-2-0/SKILL.md | skill | 98/100 | Vague "optimal" (L161) |
| CLAUDE.md | memory | 100/100 | none |
| .agents/skills/agents/SKILL.md | skill | 100/100 | none |
| .claude/skills/agents/SKILL.md | skill | 100/100 | none |
| .agents/skills/agents/references/outbound-calls.md | reference | 100/100 | none |
| .claude/skills/agents/references/outbound-calls.md | reference | 100/100 | none |
| .agents/skills/agents/references/widget-embedding.md | reference | 100/100 | none |
| .claude/skills/agents/references/widget-embedding.md | reference | 100/100 | none |
| .agents/skills/agents/references/installation.md | reference | 100/100 | none |
| .claude/skills/agents/references/installation.md | reference | 100/100 | none |
| .agents/skills/manimce-best-practices/SKILL.md | skill | 100/100 | none |
| .agents/skills/manim-composer/SKILL.md | skill | 100/100 | none |
| .agents/skills/gsap-core/SKILL.md | skill | 100/100 | none |
| .agents/skills/gsap-utils/SKILL.md | skill | 100/100 | none |
| .agents/skills/gsap-timeline/SKILL.md | skill | 100/100 | none |
| .agents/skills/gsap-react/SKILL.md | skill | 100/100 | none |
| .agents/skills/gsap-scrolltrigger/SKILL.md | skill | 100/100 | none |
| .agents/skills/threejs-materials/SKILL.md | skill | 100/100 | none |
| .agents/skills/threejs-postprocessing/SKILL.md | skill | 100/100 | none |
| .agents/skills/threejs-interaction/SKILL.md | skill | 100/100 | none |
| .agents/skills/threejs-lighting/SKILL.md | skill | 100/100 | none |
| .agents/skills/threejs-shaders/SKILL.md | skill | 100/100 | none |
| .agents/skills/threejs-fundamentals/SKILL.md | skill | 100/100 | none |
| .agents/skills/threejs-loaders/SKILL.md | skill | 100/100 | none |
| .agents/skills/threejs-animation/SKILL.md | skill | 100/100 | none |
| .claude/skills/threejs-animation/SKILL.md | skill | 100/100 | none |
| .agents/skills/threejs-geometry/SKILL.md | skill | 100/100 | none |
| .claude/skills/threejs-geometry/SKILL.md | skill | 100/100 | none |
| .agents/skills/threejs-textures/SKILL.md | skill | 100/100 | none |
| .claude/skills/threejs-textures/SKILL.md | skill | 100/100 | none |
| .agents/skills/hyperframes/SKILL.md | skill | 100/100 | none |
| .agents/skills/hyperframes-registry/SKILL.md | skill | 100/100 | none |
| .agents/skills/hyperframes-cli/SKILL.md | skill | 100/100 | none |
| .agents/skills/hyperframes-creative/SKILL.md | skill | 100/100 | none |
| .agents/skills/elevenlabs/SKILL.md | skill | 100/100 | none |
| .agents/skills/doubao-tts/SKILL.md | skill | 100/100 | none |
| .agents/skills/text-to-speech/SKILL.md | skill | 100/100 | none |
| .agents/skills/speech-to-text/SKILL.md | skill | 100/100 | none |
| .agents/skills/azure-speech-to-text/SKILL.md | skill | 100/100 | none |
| .claude/skills/azure-speech-to-text/SKILL.md | skill | 100/100 | none |
| .agents/skills/music/SKILL.md | skill | 100/100 | none |
| .claude/skills/music/SKILL.md | skill | 100/100 | none |
| .agents/skills/music-to-video/SKILL.md | skill | 100/100 | none |
| .agents/skills/dashscope/SKILL.md | skill | 100/100 | none |
| .agents/skills/sound-effects/SKILL.md | skill | 100/100 | none |
| .claude/skills/sound-effects/SKILL.md | skill | 100/100 | none |
| .agents/skills/video-download/SKILL.md | skill | 100/100 | none |
| .agents/skills/video-edit/SKILL.md | skill | 100/100 | none |
| .agents/skills/create-video/SKILL.md | skill | 100/100 | none |
| .agents/skills/grok-media/SKILL.md | skill | 100/100 | none |
| .agents/skills/gemini-omni/SKILL.md | skill | 100/100 | none |
| .agents/skills/bfl-api/SKILL.md | skill | 100/100 | none |
| .agents/skills/character-rigging/SKILL.md | skill | 100/100 | none |
| .agents/skills/character-animation-qa/SKILL.md | skill | 100/100 | none |
| .agents/skills/svg-character-animation/SKILL.md | skill | 100/100 | none |
| .agents/skills/pose-library-design/SKILL.md | skill | 100/100 | none |
| .agents/skills/playwright-recording/SKILL.md | skill | 100/100 | none |
| .claude/skills/playwright-recording/SKILL.md | skill | 100/100 | none |
| .agents/skills/lottie-bodymovin/SKILL.md | skill | 100/100 | none |
| .agents/skills/framer-motion/SKILL.md | skill | 100/100 | none |
| .agents/skills/web-design-guidelines/SKILL.md | skill | 100/100 | none |
| .agents/skills/tailwind-design-system/SKILL.md | skill | 100/100 | none |
| .agents/skills/heygen/SKILL.md | skill | 100/100 | none |
| .claude/skills/heygen/SKILL.md | skill | 100/100 | none |
| .agents/skills/setup-api-key/SKILL.md | skill | 100/100 | none |
| .claude/skills/setup-api-key/SKILL.md | skill | 100/100 | none |
| .agents/skills/vercel-composition-patterns/SKILL.md | skill | 100/100 | none |
| .claude/skills/vercel-composition-patterns/SKILL.md | skill | 100/100 | none |
| .agents/skills/avatar-video/SKILL.md | skill | 100/100 | none |

Note: `.claude/skills/ai-video-gen/SKILL.md` was not in the originally supplied file manifest but was scored and included above because it is the direct sibling of `.agents/skills/ai-video-gen/SKILL.md` (item in the manifest) and diffing the two surfaced a genuine content-drift bug (see Cross-Component). Excluding it, the manifest-only average is effectively unchanged (weighted average across all 99 unique scored artifacts ≈ 94.6, rounded to 95).

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 1 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 (only `.git/hooks`, not plugin-owned) |
| Scripts (.sh/.py/.js) | 483 |
| MCP configs (.mcp.json) | 0 |
| package.json manifests | 4 (`remotion-composer/package.json` + 3 under `.agents/skills/remotion-to-hyperframes/assets/test-corpus/*/remotion-src/package.json`, no `postinstall` scripts in any) |
| requirements*.txt | 3 (`requirements.txt`, `requirements-dev.txt`, `requirements-gpu.txt`) |
| Claude Code slash commands with Bash-executable bodies | 3 (`.claude/commands/{animated-drawing,backlot,ink-art}.md`) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | High | .claude/commands/backlot.md | 9 | Unsanitized argument interpolation into shell command | Command body is a fenced ```bash block containing `python -m backlot open $ARGUMENTS` with no quoting or sanitization; a `project-id` argument containing shell metacharacters would be interpreted by the shell. No `allowed-tools` restriction gates Bash use either. |
| 2 | Medium | .agents/skills/remotion-to-hyperframes/assets/test-corpus/run.sh | 130 | Runtime package install | `npm install --silent --no-progress` runs automatically inside a test/smoke script on first run, with no explicit user confirmation gate. |
| 3 | Low | requirements.txt | 1-16 | Unpinned dependency versions | All Python deps use `>=` lower-bound-only constraints (e.g. `pyyaml>=6.0`); no lockfile present for the root Python environment, so resolved versions can drift between installs. |
| 4 | Low | remotion-composer/package.json | 2-14 | Unpinned dependency versions | `dependencies` use caret ranges (e.g. `"remotion": "^4.0.484"`); risk is mitigated by the committed `remotion-composer/package-lock.json`, but the manifest itself is not exact-pinned. |

No Critical patterns found: no curl-pipe-to-shell, no `eval()`/`exec()` on dynamic input, no `os.system()`, no `subprocess(..., shell=True)`, no reverse shells, no base64-decode-then-execute, no credential exfiltration to third-party endpoints. The `x-key`/`X-Api-Key` header usage in `bfl-api` and `avatar-video`/`heygen` skills sends API keys only to each provider's own documented API host — standard auth, not exfiltration. `sudo apt install ffmpeg` strings across several `tools/*.py` files are user-facing install instructions printed to stdout, never executed by the script itself.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .agents/skills/motion-graphics/agents/director.md | Broken relative ref `references/shot-plan-ir.md`; resolves under `agents/` (file's own dir), real file is one directory up at `motion-graphics/references/shot-plan-ir.md` | Agent following its own doc link gets a file-not-found instead of the shot-plan schema |
| 2 | .agents/skills/motion-graphics/agents/builder.md | Broken relative refs `catalog-map.md` (L12) and `references/builder-contract.md` (L24); both need a `../` prefix | Same class of failure — build-contract rules become unreachable |
| 3 | .agents/skills/motion-graphics/agents/director.md, builder.md, finalize.md | Missing YAML frontmatter (name/description), no declared model, zero example blocks | Breaks Claude Code agent-registration discovery; no model-tier calibration |
| 4 | .agents/skills/motion-graphics/SKILL.md | Broken ref to `motion-graphics-genre.md` §5-7 (L172); file does not exist anywhere in the repo | Registration guidance points nowhere |
| 5 | .agents/skills/manimgl-best-practices/SKILL.md | "Complete, tested example files" section (L51-55) links to `examples/basic_animations.py`, `math_visualization.py`, `graph_plotting.py`, `3d_visualization.py`, `updater_patterns.py` — none exist; real examples dir has differently-named files (e.g. `mlp_neurons_flow.py`) | Every linked example is a dead link |
| 6 | .agents/skills/remotion/SKILL.md | References `.claude/skills/remotion-official/` (L3, L8) as the source of "core Remotion knowledge" — directory does not exist anywhere in the repo | Core-knowledge pointer is entirely dangling |
| 7 | .agents/skills/remotion-best-practices/SKILL.md | Links to `./rules/sound-effects.md` (L26); actual file is `./rules/sfx.md` | Sound-effects guidance unreachable via the documented link |
| 8 | .agents/skills/acestep/SKILL.md | All Quick Reference commands (L15-91) invoke `python tools/music_gen.py`; real script is `tools/audio/music_gen.py`. Also references `tools/sfx.py` (L262), which does not exist anywhere in the repo | Every copy-pasted example command fails with file-not-found |
| 9 | .agents/skills/ltx2/SKILL.md | Entire Quick Reference/Setup documents a `tools/ltx2.py` CLI and `docker/modal-ltx2/app.py` deploy path; neither exists. Real tools are `tools/video/ltx_video_modal.py` / `ltx_video_local.py`, invoked via `tools.tool_registry` (per the working pattern in `seedance-2-0/SKILL.md`) | Skill is unusable as literally written |
| 10 | .agents/skills/website-to-video/SKILL.md | Broken relative refs `../hyperframes/references/techniques.md` and `../hyperframes/references/html-in-canvas-patterns.md` (L144-145); real files live at `.agents/skills/hyperframes-animation/techniques.md` and `.../hyperframes-animation/adapters/html-in-canvas-patterns.md` (different skill name, no `references/` subdir) | Two of the five workflow-technique links are dangling |
| 11 | .agents/skills/synthetic-screen-recording/SKILL.md | References `projects/openmontage-showcase/build_composition.py` (L182) as "the reference implementation"; no `projects/` directory exists anywhere in the repo | Cited reference implementation is unreachable |
| 12 | .agents/skills/d3-viz/SKILL.md | "Templates" section (L814-815) references `chart-template.js` / `interactive-template.js`; actual files are `.jsx` (`assets/chart-template.jsx`, `assets/interactive-template.jsx`) | Both starter-template links are dead |
| 13 | .agents/skills/beautiful-mermaid/SKILL.md | Requires an `agent-browser` skill for PNG capture (L12, L92-110); no such skill exists anywhere in the repo | PNG-capture step (Step 4) cannot be completed as documented |
| 14 | .agents/skills/vercel-react-best-practices/SKILL.md + .claude twin | Description (L12) claims "Contains 65 rules across 8 categories"; `rules/` actually contains 68 `.md` files | Stale count misleads consumers about rubric coverage |
| 15 | .claude/skills/video_toolkit/SKILL.md | Directory name `video_toolkit` (underscore) does not match its own frontmatter `name: video-toolkit` / `metadata.openclaw.skillKey: video-toolkit` (hyphen) — the `.agents/` sibling correctly uses `video-toolkit` for both | Claude Code resolves skills by directory name; this mismatch risks the skill failing to register/load correctly under its declared name |
| 16 | .agents/skills/video-toolkit/SKILL.md (+ .claude/video_toolkit twin) | Duplicate `#### 4e.` step heading used twice — "Talking Head Narrator" (L298) and "Image Editing" (L330); also deploys `docker/modal-propainter/app.py` (L70) but documents env var `MODAL_DEWATERMARK_ENDPOINT_URL` (L87) with no matching `MODAL_PROPAINTER_ENDPOINT_URL` or dedicated dewatermark deploy step | Step numbering is ambiguous; env var wiring for the propainter/dewatermark tool is inconsistent |
| 17 | .claude/skills/ai-video-gen/SKILL.md | Stale relative to `.agents/skills/ai-video-gen/SKILL.md`: missing the "Kling Official" direct-API gateway/provider and `KLING_API_KEY` documented in the sibling copy | Claude Code users of this skill are told there are only two provider gateways when a third (working) one exists |
| 18 | .agents/skills/video-understand/SKILL.md (+ .claude twin) | All "Commands" examples use path `skills/video-understand/scripts/understand_video.py`, omitting the `.agents/`/`.claude/` tree prefix | None of the copy-paste commands resolve when run from repo root |
| 19 | .agents/skills/ffmpeg/SKILL.md | "Improve this skill" flow (L432) hardcodes `.claude/skills/ffmpeg/SKILL.md`; this exact file lives under `.agents/skills/ffmpeg/` in this tree | Instruction is wrong when the skill is read from the `.agents/` copy |
| 20 | .agents/skills/video-translate/SKILL.md, .agents/skills/faceswap/SKILL.md | Both declare `allowed-tools: mcp__heygen__*` (L5) but never reference any `mcp__heygen__*` tool in the body (grep count = 1, the frontmatter line itself) | Declared tool permission is dead weight; contrast with `create-video/SKILL.md` and `avatar-video/SKILL.md`, which document the MCP tools explicitly |
| 21 | .agents/skills/ai-video-gen/SKILL.md (+ .claude twin) | Same unused-tool pattern: `allowed-tools: mcp__heygen__*` declared, never invoked in body | Same as #20 |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | .agents/skills/remotion-to-hyperframes/assets/test-corpus/run.sh | Auto-runs `npm install` on first invocation with no confirmation | Gate behind an explicit `--install` flag or check for a lockfile-satisfied `node_modules` before installing silently |
| 2 | requirements.txt | Unpinned `>=` version floors, no lockfile | Adopt a lockfile (`pip-compile`/`uv lock`) or pin exact versions for reproducible installs |

Note: the High-severity `backlot.md` finding and its `.cursor/` counterpart are **not** included here per instructions — Critical/High findings require private disclosure, not public PRs.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .agents/skills/agents/references/agent-configuration.md (+ .claude twin) | Vague quantifier "relevant" (L279) | -2 |
| 2 | .agents/skills/agents/references/client-tools.md (+ .claude twin) | Vague quantifier "reasonable" (L463) | -2 |
| 3 | .agents/skills/remotion-to-hyperframes/SKILL.md | Vague quantifier "relevant" (L95) | -2 |
| 4 | .agents/skills/seedance-2-0/SKILL.md | Vague quantifier "optimal" (L161) | -2 |
| 5 | .agents/skills/flux-best-practices/SKILL.md | Vague quantifiers "optimal" (L12), "Comprehensive" (L3) | -4 |
| 6 | .agents/skills/comfyui/SKILL.md | Vague quantifier "usually" (L27) | -2 |
| 7 | .agents/skills/visual-style/SKILL.md (+ .claude twin) | Vague quantifier "appropriate" x2 (L41, L50) | -4 |
| 8 | .agents/skills/website-to-video/SKILL.md | Vague quantifier "as needed" (L59) | -2 |
| 9 | .agents/skills/d3-viz/SKILL.md | Vague quantifier "as needed" (L818) | -2 |
| 10 | .claude/commands/animated-drawing.md | Missing `allowed-tools` frontmatter field | -5 |
| 11 | .claude/commands/backlot.md | Missing `allowed-tools` frontmatter field | -5 |
| 12 | .claude/commands/ink-art.md | Missing `allowed-tools` frontmatter field | -5 |
| 13 | .claude/commands/animated-drawing.md | No empty-input handling described for `$ARGUMENTS` | -10 |
| 14 | .claude/commands/ink-art.md | No empty-input handling described for `$ARGUMENTS` | -10 |
| 15 | .cursor/commands/{animated-drawing,backlot,ink-art}.md | No YAML frontmatter at all — low confidence this is a defect rather than intentional Cursor-format convention (Cursor is outside NLPM's tracked tier overlays) | informational only, no penalty applied |

## Cross-Component
- **`.claude/skills/ai-video-gen/SKILL.md` vs `.agents/skills/ai-video-gen/SKILL.md`**: the two copies are supposed to be identical mirrors (confirmed identical for every other shared skill name between the two trees — `agents`, `heygen`, `music`, `vercel-react-best-practices`, `threejs-animation`, etc.) but this pair has drifted: the `.claude` copy is missing the "Kling Official" direct-API gateway that the `.agents` copy documents. This is the only content-diverging pair found among ~48 shared skill names.
- **`video_toolkit` (.claude/) vs `video-toolkit` (.agents/)**: same skill, dual-published under inconsistent directory-naming conventions (underscore vs. hyphen). Content is otherwise byte-identical. The `.claude/` copy's directory name doesn't match its own declared `name:`/`skillKey:` field (see Bug #15); the `.agents/` copy's directory name matches correctly.
- **`.claude/skills/` is a partial mirror of `.agents/skills/`**: only ~48 of the ~85 skills under `.agents/skills/` are mirrored into `.claude/skills/`. Skills present only in `.agents/skills/` (not orphaned, just not dual-published) include the `gsap-*` family, `hyperframes-*` variants, `character-rigging`, `comfyui`, `kling-official`, `lyria`, `media-use`, and others. This appears to be intentional scoping rather than a bug (no references broken by the asymmetry were found), but is worth confirming with the maintainer.
- **`AGENT_GUIDE.md` reference from `CLAUDE.md`**: confirmed to resolve correctly (46KB file exists at repo root); not a broken reference.
- No stale artifact counts found elsewhere in cross-referencing `AGENTS.md`/`CODEX.md`/`COPILOT.md`/`CURSOR.md` beyond the `vercel-react-best-practices` "65 rules" mismatch (Bug #14).

## Recommendation
**REVIEW** — submit NL bug-fix PRs for the 21 items above (broken references, frontmatter/naming mismatches, unused-tool declarations), and flag the Medium/Low security findings (auto-`npm install` in a test fixture, unpinned Python dependencies) in the same or a follow-up PR. The one High-severity finding (`.claude/commands/backlot.md` — unsanitized `$ARGUMENTS` interpolated directly into a shell command) requires private disclosure to the maintainer rather than a public PR; do not include it in any public issue or PR description.
