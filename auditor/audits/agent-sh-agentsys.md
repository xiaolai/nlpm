# NLPM Audit: agent-sh/agentsys
**Date**: 2026-04-12  |  **Artifacts**: 32  |  **Strategy**: batched
**NL Score**: 91/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 19  |  **Security Findings**: 6

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .kiro/skills/sync-docs/SKILL.md | skill | 83 | Missing examples; vague qualifier |
| .kiro/skills/repo-intel/SKILL.md | skill | 85 | Missing example blocks |
| .kiro/skills/perf-code-paths/SKILL.md | skill | 85 | Missing example blocks |
| .kiro/skills/enhance-cross-file/SKILL.md | skill | 85 | Missing example blocks |
| .kiro/skills/perf-benchmarker/SKILL.md | skill | 85 | Missing example blocks |
| .kiro/skills/enhance-orchestrator/SKILL.md | skill | 85 | Missing example blocks |
| .kiro/skills/validate-delivery/SKILL.md | skill | 85 | Missing example blocks |
| .kiro/skills/perf-baseline-manager/SKILL.md | skill | 85 | Missing example blocks |
| .kiro/skills/perf-analyzer/SKILL.md | skill | 85 | Missing example blocks |
| .kiro/skills/perf-theory-gatherer/SKILL.md | skill | 85 | Missing example blocks |
| .kiro/skills/perf-theory-tester/SKILL.md | skill | 85 | Missing example blocks |
| .kiro/skills/perf-profiler/SKILL.md | skill | 85 | Missing example blocks |
| .kiro/skills/perf-investigation-logger/SKILL.md | skill | 85 | Missing example blocks |
| CLAUDE.md | project-memory | 88 | Missing WHY explanations; negative phrasing |
| .kiro/skills/web-auth/SKILL.md | skill | 90 | Hardcoded user-specific install path |
| .kiro/skills/web-browse/SKILL.md | skill | 90 | Hardcoded user-specific install path |
| .claude-plugin/plugin.json | manifest | 95 | No bugs; well-formed |
| meta/skills/maintain-cross-platform/SKILL.md | skill | 95 | Exceeds 500-line guideline (1024 lines) |
| .kiro/skills/consult/SKILL.md | skill | 96 | Near-perfect; minor vagueness |
| .kiro/skills/learn/SKILL.md | skill | 96 | Near-perfect |
| .kiro/skills/drift-analysis/SKILL.md | skill | 96 | Near-perfect |
| .kiro/skills/orchestrate-review/SKILL.md | skill | 98 | Near-perfect |
| .kiro/skills/deslop/SKILL.md | skill | 97 | None significant |
| .kiro/skills/enhance-hooks/SKILL.md | skill | 97 | None significant |
| .kiro/skills/enhance-prompts/SKILL.md | skill | 97 | None significant |
| .kiro/skills/enhance-docs/SKILL.md | skill | 97 | None significant |
| .kiro/skills/enhance-agent-prompts/SKILL.md | skill | 97 | None significant |
| .kiro/skills/enhance-skills/SKILL.md | skill | 97 | None significant |
| .kiro/skills/enhance-plugins/SKILL.md | skill | 97 | None significant |
| .kiro/skills/debate/SKILL.md | skill | 97 | None significant |
| .kiro/skills/discover-tasks/SKILL.md | skill | 97 | None significant |
| .kiro/skills/enhance-claude-memory/SKILL.md | skill | 97 | None significant |

**Weighted average**: 2917 / 32 = **91/100**

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 3 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks (.md, .sh, .json) | 0 |
| Scripts (scripts/*.js) | 23 |
| MCP configs (.mcp.json) | 0 |
| Package manifests (package.json) | 1 |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | package.json | 41 | postinstall-equivalent script | `prepare` lifecycle hook runs `node bin/dev-cli.js setup-hooks` on every `npm install`, installing git hooks (pre-commit, pre-push) into the consumer's repo. The hook content is benign (runs validators, prompts for /enhance), but auto-running hooks install on third-party `npm install` is unexpected behavior. |
| 2 | Medium | .kiro/skills/web-auth/SKILL.md | 39–174 | hardcoded user filesystem path | All commands reference `/Users/avifen/.agentsys/plugins/web-ctl/scripts/web-ctl.js` - a specific developer's home directory path committed to the repo. Breaks for all other users; exposes local filesystem layout. |
| 3 | Medium | .kiro/skills/web-browse/SKILL.md | 25–516 | hardcoded user filesystem path | Same `/Users/avifen/.agentsys/...` path pattern repeated throughout the entire skill, in every CLI command example. |
| 4 | Low | package.json | 84 | unpinned dependency | `"agentsys": "^5.0.0"` - caret allows automatic minor/patch upgrades. The package depends on itself (the published version) via `agentsys`, which is unusual and version-drift-prone. |
| 5 | Low | package.json | 85 | unpinned dependency | `"js-yaml": "^4.1.1"` - unpinned; minor version float possible. |
| 6 | Low | scripts/dev-install.js | 59 | execSync with string interpolation | `execSync(\`${process.platform === 'win32' ? 'where' : 'which'} ${cmd}\`)` where `cmd` comes from a developer-controlled predefined list, not user input. Risk is low but the pattern of execSync + backtick interpolation is worth noting. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No registration-breaking bugs found. All NL artifacts have valid frontmatter with required `name` and `description` fields. | — |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | package.json | `prepare` script installs git hooks on `npm install` | Rename to a dev-only script (e.g., `setup-hooks`) invoked explicitly by contributors, not automatically during install. Document in CONTRIBUTING.md. |
| 2 | .kiro/skills/web-auth/SKILL.md | Hardcoded `/Users/avifen/.agentsys/...` path | Replace with a platform-agnostic variable. Per the repo's cross-platform skill (`maintain-cross-platform`), commands should reference `~/.agentsys/plugins/web-ctl/scripts/web-ctl.js` or use the `$AGENTSYS_DIR` convention. |
| 3 | .kiro/skills/web-browse/SKILL.md | Same hardcoded path issue | Same fix as above - replace all 40+ occurrences of `/Users/avifen/.agentsys/...` with `~/.agentsys/...` or a configurable variable. |
| 4 | package.json | Self-referential dependency `agentsys: ^5.0.0` | Investigate whether this circular dependency is intentional. If the package installs itself for CLI use, pin to an exact version or remove from runtime dependencies. |
| 5 | package.json | Unpinned `js-yaml` | Pin to exact version (`4.1.1`) or use `~4.1.1` (patch-only) for more deterministic installs. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .kiro/skills/repo-intel/SKILL.md | No example blocks - Output Expectations section is brief with no concrete before/after examples | -15 |
| 2 | .kiro/skills/perf-code-paths/SKILL.md | No example blocks showing a sample scenario → output mapping | -15 |
| 3 | .kiro/skills/enhance-cross-file/SKILL.md | No `<examples>` block; detection patterns documented but no illustrative before/after | -15 |
| 4 | .kiro/skills/perf-benchmarker/SKILL.md | No example blocks demonstrating benchmark run → output | -15 |
| 5 | .kiro/skills/enhance-orchestrator/SKILL.md | No `<examples>` block; extensive workflow documentation but no concrete illustration | -15 |
| 6 | .kiro/skills/validate-delivery/SKILL.md | No example blocks; all logic shown as pseudocode but no worked example | -15 |
| 7 | .kiro/skills/perf-baseline-manager/SKILL.md | No example blocks; very short skill with no example baseline JSON | -15 |
| 8 | .kiro/skills/perf-analyzer/SKILL.md | No example blocks; minimal content with no worked recommendation example | -15 |
| 9 | .kiro/skills/perf-theory-gatherer/SKILL.md | No example blocks; hypotheses output format shown but no example hypothesis set | -15 |
| 10 | .kiro/skills/perf-theory-tester/SKILL.md | No example blocks; experiment output shown but no worked example | -15 |
| 11 | .kiro/skills/perf-profiler/SKILL.md | No example blocks; output format shown but no profiler output example | -15 |
| 12 | .kiro/skills/perf-investigation-logger/SKILL.md | No example blocks; output template shown but no sample populated log entry | -15 |
| 13 | .kiro/skills/sync-docs/SKILL.md | Vague quantifier "appropriate" in constraints section | -2 |
| 14 | CLAUDE.md | Critical Rules lack WHY explanations - rules 1-8 state what to do but not why, reducing compliance reliability per prompt-engineering research | -5 |
| 15 | CLAUDE.md | Several rules use negative-only phrasing ("No unnecessary files", "Never bypass") without positive alternatives | -2 |
| 16 | meta/skills/maintain-cross-platform/SKILL.md | File is 1024 lines - well over the 500-line guideline. The detailed "Adding New Features" step-by-step sections and "Installer Deep Dive" would benefit from being split to a `reference.md` companion file | -5 |
| 17 | .kiro/skills/web-auth/SKILL.md | Hardcoded path will silently fail for any user other than the original developer; no fallback or detection | -10 |
| 18 | .kiro/skills/web-browse/SKILL.md | Same hardcoded path issue at scale (40+ occurrences throughout the file) | -10 |
| 19 | .kiro/skills/enhance-orchestrator/SKILL.md | References specific agent names (`plugin-enhancer`, `agent-enhancer`, etc.) inline - these are implementation details that should be stable but represent tight coupling that isn't validated by the cross-file checker | -2 |

## Cross-Component
**Broken references**: None detected. All internal relative paths (`../../scripts/detect.js`, `../../lib/...`) follow consistent conventions documented in `maintain-cross-platform/SKILL.md`.

**Orphaned components**: The `web-auth` and `web-browse` skills depend on a `web-ctl` plugin (`plugins/web-ctl/scripts/web-ctl.js`) that is not listed in the root `plugin.json` or the `maintain-cross-platform/SKILL.md` plugin manifest. These skills are either from a separate plugin (installed independently) or from a graduated plugin not tracked in this repo's manifest. The hardcoded absolute path suggests these were authored on the original developer's machine without cross-platform abstraction.

**Contradictions**: None detected. The `enhance-orchestrator/SKILL.md` correctly distinguishes itself from `enhance-agent-prompts/SKILL.md` and `enhance-prompts/SKILL.md` with a clear differentiation table.

**Version alignment**: `package.json` and `.claude-plugin/plugin.json` both declare `5.8.3` - aligned.

**perf-* skills contract**: All 8 perf skills (`perf-code-paths`, `perf-benchmarker`, `perf-baseline-manager`, `perf-analyzer`, `perf-theory-gatherer`, `perf-theory-tester`, `perf-profiler`, `perf-investigation-logger`) reference `docs/perf-requirements.md` as the "canonical contract." This file was not in the audited set but is referenced consistently across all perf skills - consistent, but represents a single point of truth that cannot be validated here.

## Recommendation
CLEAR - submit PRs for all bugs (none found) and medium/low security fixes.

Priority order for PRs:
1. **web-auth + web-browse hardcoded paths** (Medium security, high user impact - these skills are completely broken for any user who is not `avifen`). Replace `/Users/avifen/.agentsys/...` with `~/.agentsys/...` or an `$AGENTSYS_INSTALL_DIR` variable documented in the skill.
2. **package.json prepare script** (Medium security) - Move hook installation out of the postinstall lifecycle.
3. **Example blocks for perf-* and operational skills** (12 quality issues) - All 12 affected skills share the same pattern: they define output formats but provide no concrete worked examples. A single PR adding `<examples>` blocks to these skills would push the overall NL score above 93.
4. **CLAUDE.md rule improvements** - Add WHY explanations and convert negative rules to positive alternatives.
5. **maintain-cross-platform split** - Extract the "Adding New Features" and "Installer Deep Dive" sections to a `reference.md` companion file to bring the core SKILL.md under 500 lines.
