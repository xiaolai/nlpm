# NLPM Audit: tintinweb/pi-subagents
**Date**: 2026-04-06  |  **Artifacts**: 22  |  **Strategy**: batched
**NL Score**: 94/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 5  |  **Security Findings**: 1

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .pi/agents/auditor.md | agent (production, dogfooded) | 75/100 | No example/invocation block; no explicit output-format section |
| test/fixtures/.pi/agents/all-and-alpha-selected.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/beta-selected-mutes-alpha.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/disallow-alpha-write.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/exclude-beats-ext-selector.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/exclude-beta.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/extensions-disabled.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/fmt-array.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/fmt-quoted-csv.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/fmt-unquoted-csv.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/isolated-overrides-all.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/memory-readonly.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/memory-readwrite.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/minimal.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/narrow-alpha-read.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/no-selector-all-surface.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/prompt-mode-append.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/prompt-mode-replace.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/skills-preload.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/tools-narrow.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/tools-none.md | agent (e2e fixture) | 95/100 | No formatted example block |
| test/fixtures/.pi/agents/tools-omitted-ext-loaded.md | agent (e2e fixture) | 95/100 | No formatted example block |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 files |
| Scripts (`scripts/**/*.{sh,py,js}`) | 0 files |
| MCP configs (`.mcp.json`) | 0 files |
| Package manifests | `package.json` (npm, pi-extension), `package-lock.json` present |
| requirements.txt | 0 files |
| Extension source referenced by test fixtures | `test/fixtures/ext-alpha.mjs`, `test/fixtures/ext-beta.mjs`, `test/fixtures/e2e-probe-ext.mjs` (out of scope glob, inspected for cross-reference only — trivial `pi.registerTool` stubs, no dangerous patterns) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | Low | package.json | 29-31 | unpinned semver (caret ranges) | `dependencies` (`@sinclair/typebox`, `croner`, `nanoid`) and `devDependencies` use `^`-prefixed ranges rather than exact pins. Standard npm convention; fully mitigated by the committed `package-lock.json`. No postinstall/preinstall scripts, no `eval`, no `curl\|sh`, no `subprocess(shell=True)`/`os.system`, no credential exfiltration, no MCP config. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No bugs found. | All 22 artifacts registered correctly per the repo's own documented spec: `description` present everywhere, `tools`/`extensions`/`exclude_extensions`/`disallowed_tools` selectors all resolve to the behavior each fixture's `expect_tools_present`/`expect_tools_absent` annotations claim, and every referenced extension/skill file (`ext-alpha.mjs`, `ext-beta.mjs`, `probe-skill.md`) exists with matching tool names. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| — | — | None. | The single Low finding (unpinned semver) is standard, lockfile-mitigated practice — not actionable as a PR. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .pi/agents/auditor.md | Zero example/invocation blocks in the body — no sample `Agent({subagent_type: "auditor", ...})` call or sample findings output | -15 |
| 2 | .pi/agents/auditor.md | No explicit "Output Format" section specifying the structure of the security findings report | -10 |
| 3 | test/fixtures/.pi/agents/* (21 files) | No formatted `<example>`/`## Example` block; each file's prose describes an input config → expected tool-set mapping in place of a structured example, earning partial credit | -5 each |
| 4 | all 22 files | Generic rubric item "missing `name` frontmatter" does not apply to this ecosystem — **false positive, no penalty applied**. Per `README.md:166,209`, pi derives the agent type name from the filename (`.pi/agents/<name>.md`); `name` is not a frontmatter field at all, so the check cannot fire here | 0 (false positive) |
| 5 | test/fixtures/.pi/agents/* (21 files) | Generic rubric item "model not declared" — **false positive, no penalty applied**. Per `README.md:218`, `model` intentionally defaults to "inherit parent" and is documented as optional; these 21 fixtures test tool/extension scoping, not model selection, so omitting `model` is by design | 0 (false positive) |

## Cross-Component
No broken references, orphaned components, or contradictions found.

- All extension/skill files referenced by the fixtures resolve and match: `test/fixtures/ext-alpha.mjs` registers `alpha_read`/`alpha_write` (referenced by 6+ fixtures), `test/fixtures/ext-beta.mjs` registers `beta_tool`, and `test/fixtures/.pi/skills/probe-skill.md` contains the `SKILL_BODY_MARKER` that `skills-preload.md` expects.
- `.pi/agents/auditor.md` mirrors the `README.md:177-195` documented example almost verbatim (same `description`/`tools`), with a deliberately cheaper tuning (`model: claude-haiku-4-5` vs. the doc's `claude-opus-4-6`, `thinking: off` vs. `high`, `max_turns: 10` vs. `30`) — consistent dogfooding, not drift.
- Scope note: `test/fixtures/.pi/agents/*` live under `test/fixtures/`, not the project's real `.pi/agents/` — they are e2e test scaffolding for the extension's own test runner (confirmed by each file's own "e2e template" framing and by `minimal.md`'s explicit note that `expect_*` keys are "test-harness annotations and are ignored by the agent loader"). They are never discovered as real custom agent types in this repo. Applying the full production-agent quality bar to them is a scope mismatch that NLPM's rubric currently has no exception for; each fixture's score reflects that context rather than treating it as a defect.
- NLPM's tier-aware overlay system (`conventions-claude`/`conventions-codex`/`conventions-antigravity`) has no fourth overlay for the "pi" custom-agent format used by this repo, which is why two rubric checks (frontmatter `name`, `model` declaration) misfire here — see the false-positive rows above.

## Recommendation
CLEAR — no PR-worthy bugs and no actionable security fixes were found. The repo's single production custom agent (`.pi/agents/auditor.md`) is a reasonable optional-enhancement candidate for adding an example block and an output-format section, but this is a quality suggestion, not a bug — no PR is warranted from this audit. Given NL Score 94/100 and Security CLEAR, this repo is a candidate for `auditor-exemplar` treatment.
