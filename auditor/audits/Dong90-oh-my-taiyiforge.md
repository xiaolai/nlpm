# NLPM Audit: Dong90/oh-my-taiyiforge
**Date**: 2026-06-27  |  **Artifacts**: 23  |  **Strategy**: batched
**NL Score**: 95/100
**Security**: BLOCKED
**Bugs**: 0  |  **Quality Issues**: 14  |  **Security Findings**: 6

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/taiyi-test/SKILL.md | skill | 90 | Missing `## 输出` section — TEST.md path and structure not defined |
| skills/taiyi-health/SKILL.md | skill | 90 | Missing `## 输出` section — no persistent output artifact or path defined |
| skills/taiyi-requirement/SKILL.md | skill | 90 | Missing `## 输出` section — REQUIREMENT.md format not specified |
| skills/taiyi-dev/SKILL.md | skill | 90 | Missing `## 输出` section — output artifacts not formally defined |
| skills/taiyi-ultrawork/SKILL.md | skill | 90 | Missing `## 输出` section — no output format defined |
| skills/taiyi-review/SKILL.md | skill | 90 | Missing `## 输出` section — REVIEW.md structure not specified |
| skills/taiyi-integration/SKILL.md | skill | 90 | Missing `## 输出` section — CHANGELOG.md format defined only by keyword list |
| skills/taiyi-design/SKILL.md | skill | 90 | Missing `## 输出` section — DESIGN.md format not specified |
| skills/taiyi-forge/SKILL.md | skill | 90 | Missing `## 输出` section — engine skill with no document output defined |
| skills/taiyi-change/SKILL.md | skill | 90 | Missing `## 输出` section — CHANGE.md template not defined |
| skills/taiyi-diagram-render/SKILL.md | skill | 96 | Unclosed Markdown code block in step 3 (line 58) + vague "高质量" |
| skills/taiyi-intel-scan/SKILL.md | skill | 98 | Vague quantifier "相关" in instructions text |
| skills/taiyi-architect/SKILL.md | skill | 98 | Vague quantifier "显著" ("显著不同" — significantly different) |
| skills/taiyi-diagram-flow/SKILL.md | skill | 100 | — |
| skills/taiyi-ui-design/SKILL.md | skill | 100 | — |
| skills/taiyi-diagram-c4/SKILL.md | skill | 100 | — |
| skills/taiyi-task/SKILL.md | skill | 100 | — |
| skills/taiyi-diagram-pipeline/SKILL.md | skill | 100 | — |
| skills/taiyi-restyle/SKILL.md | skill | 100 | — |
| skills/taiyi-orchestrator/SKILL.md | skill | 100 | — |
| skills/taiyi-compress/SKILL.md | skill | 100 | — |
| skills/taiyi-evolve/SKILL.md | skill | 100 | — |
| skills/taiyi-diagram-arch/SKILL.md | skill | 100 | — |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 2 |
| Medium | 2 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks (registered) | 0 (hook scripts exist in scripts/ but no .claude/settings.json found at root) |
| Hook implementation scripts | ~7 (scripts/claude-keyword-hook.mjs, scripts/claude-phase-guard-hook.mjs, scripts/claude-mode-stop-hook.mjs, scripts/cursor-keyword-hook.mjs, scripts/cursor-phase-guard-hook.mjs, scripts/cursor-mode-stop-hook.mjs, scripts/codex-keyword-preflight.mjs) |
| Shell scripts | 5 (scripts/install.sh, scripts/install-skills.sh, scripts/taiyi-forge.sh, .pitfalls/scan.sh, examples/v28-all-slashes-demo/scripts/run-v28-all-slashes.sh) |
| Node/MJS scripts | 25+ (scripts/*.mjs, postinstall.mjs, .pitfalls/*.mjs, examples/**/*.mjs) |
| Python scripts | 2 (scripts/generate-architecture-svg.py, scripts/generate-architecture-poster-v023.py) |
| MCP configs | 0 |
| Package manifests | 1 (package.json with postinstall hook) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | scripts/taiyi-forge.sh | 71 | SEC-new-function-eval | `eval "$TAIYI_CLI" "$@"` — eval with variable in main execution path; TAIYI_CLI can be attacker-controlled via TAIYI_FORGE_ROOT env var or `.taiyi/forge-root` file content, enabling arbitrary command injection |
| 2 | High | scripts/taiyi-forge.sh | 53 | SEC-new-function-eval | `_out=$(eval "$TAIYI_CLI" "$@" 2>"$_err")` — same eval-with-variable pattern inside npx fallback error handler; same command injection vector |
| 3 | High | package.json | 52 | SEC-postinstall-script | `"postinstall": "node postinstall.mjs"` — automatically executes build code on `npm install`; supply chain attack surface if package registry is compromised |
| 4 | Medium | scripts/taiyi-forge.sh | 32 | SEC-network-fetch | `npx -p oh-my-taiyiforge taiyi` as CLI fallback fetches package from npm registry at runtime without version pin; subject to package substitution |
| 5 | Medium | postinstall.mjs | 10 | SEC-shell-subprocess | `spawnSync("npm", ["run", "build"])` runs full build pipeline during install without sandboxing; failure is soft-warned only, not fatal |
| 6 | Low | package.json | — | SEC-unpinned-semver | 9 production dependencies use `^` semver ranges (`@modelcontextprotocol/sdk ^1.29.0`, `handlebars ^4.7.9`, `zod ^4.4.3`, etc.); automatic minor/patch upgrades on fresh install |

## Bugs (PR-worthy)
No NL bugs found. All 23 artifacts have valid `name` and `description` frontmatter.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/taiyi-forge.sh | Runtime npm fallback (`npx -p oh-my-taiyiforge taiyi`) fetches from registry without version pin | Pin to specific version: `npx -p oh-my-taiyiforge@0.42.0 taiyi` or prefer local install check before npx fallback |
| 2 | postinstall.mjs | `spawnSync("npm run build")` during install has no integrity check on build output | Add TAIYI_FORGE_SKIP_BUILD documentation prominently in README; consider checking dist/ integrity hash post-build |
| 3 | package.json | 9 production deps with `^` ranges allow silent upgrades | Pin critical deps (`@modelcontextprotocol/sdk`, `handlebars`, `zod`) to exact versions; rely on lockfile for reproducibility |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/taiyi-test/SKILL.md | Missing `## 输出` section — no output path or TEST.md template provided | -10 |
| 2 | skills/taiyi-health/SKILL.md | Missing `## 输出` section — health scan produces no named persistent artifact | -10 |
| 3 | skills/taiyi-requirement/SKILL.md | Missing `## 输出` section — REQUIREMENT.md format and path not specified | -10 |
| 4 | skills/taiyi-dev/SKILL.md | Missing `## 输出` section — dev outputs (.dev-complete, SUMMARY) have no path or format definition | -10 |
| 5 | skills/taiyi-ultrawork/SKILL.md | Missing `## 输出` section — no output format defined for the orchestration result | -10 |
| 6 | skills/taiyi-review/SKILL.md | Missing `## 输出` section — REVIEW.md structure and path not specified | -10 |
| 7 | skills/taiyi-integration/SKILL.md | Missing `## 输出` section — CHANGELOG.md format described only with section keywords, no template | -10 |
| 8 | skills/taiyi-design/SKILL.md | Missing `## 输出` section — DESIGN.md format and path not specified | -10 |
| 9 | skills/taiyi-forge/SKILL.md | Missing `## 输出` section — engine skill has no defined output artifact format | -10 |
| 10 | skills/taiyi-change/SKILL.md | Missing `## 输出` section — CHANGE.md sections described in steps but no path or template block | -10 |
| 11 | skills/taiyi-intel-scan/SKILL.md | Vague quantifier "相关" in "与本变更相关的代码现实" (line ~10); "相关" (relevant) is unquantified | -2 |
| 12 | skills/taiyi-architect/SKILL.md | Vague quantifier "显著" in "运维负担显著不同" (line ~25); "显著" (significantly) has no numeric threshold | -2 |
| 13 | skills/taiyi-diagram-render/SKILL.md | Vague qualifier "高质量" in "高质量 / 视觉审查" (line ~69) — criteria for high quality not specified | -2 |
| 14 | skills/taiyi-diagram-render/SKILL.md | Unclosed Markdown code block in step 3 (bash block opens at line 58, never closed before step 4 at line 62) — steps 4+ render inside the code block in Markdown processors | -2 |

## Cross-Component
Three unverified doc references in skills that could be broken:

1. **taiyi-diagram-render** line 48: `[`docs/diagrams/pipeline.md`](../../docs/diagrams/pipeline.md)` — renders the statement "导出说明见 [`docs/diagrams/pipeline.md`](../../docs/diagrams/pipeline.md)「导出图」节（**不再维护 RENDER.md**）". The referenced file was not verified to exist on disk. *Confidence: medium.*

2. **taiyi-forge** (references block): `docs/taiyi/canonical-commands.md` and `docs/taiyi/commands.yaml` referenced as authoritative sources for command listing. File existence not verified. *Confidence: medium.*

3. **taiyi-compress** (references block): `docs/taiyi/token-budget.yaml` and `docs/taiyi/token-compress-hooks.yaml` referenced for configuration. File existence not verified. *Confidence: medium.*

All three are medium-confidence; verification requires reading the docs/ tree. No confirmed broken references in mandatory skill-to-skill cross-references — all inter-skill invocations (diagram-pipeline → diagram-c4 → diagram-arch → diagram-render chain) are self-consistent.

## Recommendation
BLOCKED — do not submit PRs. File private security report.

The `eval "$TAIYI_CLI" "$@"` pattern in `scripts/taiyi-forge.sh` (lines 53 and 71) constitutes a Critical/High command injection surface: `TAIYI_FORGE_ROOT` env var and `.taiyi/forge-root` file are both untrusted inputs that influence the eval'd string. The `postinstall` script runs build code automatically on `npm install`. Both findings require private disclosure to the maintainer before any public PR activity.

NL quality is high (95/100 average). The 14 quality issues are concentrated in the 10 phase-skill documents that describe their output artifact in prose but omit a formal `## 输出` section with path and template. These are straightforward documentation additions. Once the security issues are resolved privately, NL fix PRs for the quality issues would be welcome.
