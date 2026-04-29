# NLPM Audit: google-labs-code/stitch-skills
**Date**: 2026-04-06  |  **Artifacts**: 8  |  **Strategy**: single
**NL Score**: 96/100
**Security**: CLEAR
**Bugs**: 1  |  **Quality Issues**: 11  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/stitch-design/SKILL.md | Skill | 88 | No output format declared; skill acts as a router without describing what it produces |
| skills/react-components/SKILL.md | Skill | 94 | No formal Output Format section; `web_fetch` in allowed-tools is not referenced in skill body |
| skills/shadcn-ui/SKILL.md | Skill | 94 | No formal Output Format section; `web_fetch` in allowed-tools is not referenced in skill body |
| skills/remotion/SKILL.md | Skill | 96 | "appropriate" vague quantifier appears twice (timing and font sizes) |
| skills/design-md/SKILL.md | Skill | 97 | "Overview" and "The Goal" sections contain near-identical content |
| skills/enhance-prompt/SKILL.md | Skill | 98 | "appropriate" vague quantifier in assessment table |
| skills/stitch-loop/SKILL.md | Skill | 98 | "if appropriate" vague quantifier for navigation decision |
| skills/taste-design/SKILL.md | Skill | 99 | No significant issues |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 (none found) |
| Scripts | 4: skills/react-components/scripts/fetch-stitch.sh, skills/react-components/scripts/validate.js, skills/remotion/scripts/download-stitch-asset.sh, skills/shadcn-ui/scripts/verify-setup.sh |
| MCP configs | 0 (no .mcp.json) |
| Package manifests | 1: skills/react-components/package.json (includes package-lock.json) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | skills/react-components/scripts/fetch-stitch.sh | 23 | SEC-network-call | curl downloads from any URL provided by caller; no allowlist or scheme validation |
| 2 | Medium | skills/remotion/scripts/download-stitch-asset.sh | 25 | SEC-network-call | curl downloads from any URL provided by caller; mkdir -p creates directories along the output path |
| 3 | Low | skills/remotion/scripts/download-stitch-asset.sh | 18 | SEC-path-traversal | OUTPUT_PATH is not validated; a caller-supplied path like `../../etc/file` would create or overwrite files outside the repo |
| 4 | Low | skills/react-components/package.json | 11 | SEC-unpinned-semver | @swc/core pinned to semver range `^1.3.100` rather than an exact version; lock file present partially mitigates this |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | skills/remotion/SKILL.md | Line 193 references `examples/walkthrough/` directory which does not exist; examples are directly in `examples/` (WalkthroughComposition.tsx, screens.json) | Agent cannot find reference resources; broken discovery path |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/remotion/scripts/download-stitch-asset.sh | No output path validation; directory traversal possible if path escapes repo root | Validate that OUTPUT_PATH resolves within the current working directory before calling curl and mkdir |
| 2 | skills/react-components/package.json | @swc/core uses semver range `^1.3.100` | Pin to exact version (e.g., `"1.3.100"`) now that a lock file exists; the lock file already pins transitively but the manifest range allows drift on fresh installs without the lock |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/design-md/SKILL.md | "Overview" (lines 17–27) and "The Goal" (lines 26–27) sections contain near-identical sentences about DESIGN.md purpose | -3 |
| 2 | skills/enhance-prompt/SKILL.md | "Add appropriate descriptors" in the platform assessment table (line 44) is a vague quantifier | -2 |
| 3 | skills/react-components/SKILL.md | No formal Output Format section; outputs (mockData.ts, component files, App.tsx) are implied by execution steps but never collected into a dedicated section | -3 |
| 4 | skills/react-components/SKILL.md | `web_fetch` declared in allowed-tools but not referenced anywhere in the skill body; download is handled entirely by `scripts/fetch-stitch.sh` via Bash | -3 |
| 5 | skills/remotion/SKILL.md | "appropriate display duration" (Step 3, Adjust timing) — vague quantifier | -2 |
| 6 | skills/remotion/SKILL.md | "appropriate font sizes" (Best Practices, Readable text) — vague quantifier | -2 |
| 7 | skills/shadcn-ui/SKILL.md | No formal Output Format section; the skill's output (component files via CLI) is implied rather than declared | -3 |
| 8 | skills/shadcn-ui/SKILL.md | `web_fetch` declared in allowed-tools but not referenced in skill body; all network interaction goes through shadcn MCP tools or Bash | -3 |
| 9 | skills/stitch-design/SKILL.md | No output format declared; skill is a router to workflow files and never describes what it itself produces | -10 |
| 10 | skills/stitch-design/SKILL.md | "Intelligently route user requests" (line 16) — "intelligently" is a vague qualifier | -2 |
| 11 | skills/stitch-design/SKILL.md | Typo "Prefere" (line 82) should be "Prefer" | -0 (informational) |
| 12 | skills/stitch-loop/SKILL.md | "Add the new page to the global navigation if appropriate" (line 106) — "appropriate" is a vague quantifier | -2 |

## Cross-Component
**Inconsistent Stitch tool naming across skills.** Three skills (`stitch-loop`, `design-md`, `react-components`) declare the Stitch MCP tools as `stitch*:*` (glob pattern); two skills (`stitch-design`, `taste-design`) declare them as the literal string `StitchMCP`. If the MCP server registers its tools under a prefix like `mcp_stitch_` or `stitch_`, then `StitchMCP` will never match and those two skills will operate without any Stitch tools accessible. The glob `stitch*:*` used by the majority is the safer convention and should be adopted consistently. This is a potential functional gap, not just a style inconsistency.

**Broken sub-directory reference in remotion.** The skill references `examples/walkthrough/` but the two example files (`WalkthroughComposition.tsx`, `screens.json`) live directly in `examples/`. No nested `walkthrough/` subdirectory exists. This is captured in Bugs #1 above.

**Design overlap between design-md and stitch-design.** Both skills can synthesize a `DESIGN.md` file (design-md's primary purpose; stitch-design's `generate-design-md` workflow). No contradiction — stitch-design is a superset — but new users may not discover the overlap. Low risk; informational only.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

Priority order:
1. **Bug PR**: Fix broken `examples/walkthrough/` reference in `skills/remotion/SKILL.md` → correct to `examples/`.
2. **Security PR (Low)**: Add output-path validation to `skills/remotion/scripts/download-stitch-asset.sh`.
3. **Security PR (Low)**: Pin `@swc/core` to an exact version in `skills/react-components/package.json`.
4. **Quality PR**: Align Stitch tool naming — replace `StitchMCP` with `stitch*:*` in `skills/stitch-design/SKILL.md` and `skills/taste-design/SKILL.md`.
5. **Quality PR**: Add an Output Format section to `skills/stitch-design/SKILL.md`; remove unused `web_fetch` from allowed-tools in `skills/react-components/SKILL.md` and `skills/shadcn-ui/SKILL.md`.
