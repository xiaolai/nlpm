# NLPM Audit: a5c-ai/babysitter
**Date**: 2026-04-20  |  **Artifacts**: 4189  |  **Strategy**: progressive
**NL Score**: 70/100
**Security**: REVIEW
**Bugs**: 1  |  **Quality Issues**: 17  |  **Security Findings**: 14

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| pilot-shell/spec-guard/README.md | agent-doc | 20 | No AGENT.md companion; missing frontmatter (name, description); no examples; no output format |
| ruflo/coder/README.md | agent-doc | 60 | Stub content (4 lines); no frontmatter; no examples; no output format |
| ruflo/adaptive-queen/README.md | agent-doc | 60 | Stub content (4 lines); no frontmatter; no examples; no output format |
| ruflo/reviewer/README.md | agent-doc | 60 | Stub content (4 lines); no frontmatter; no examples; no output format |
| ruflo/strategic-queen/README.md | agent-doc | 60 | Stub content (4 lines); no frontmatter; no examples; no output format |
| ruflo/optimizer/README.md | agent-doc | 60 | Stub content (4 lines); no frontmatter; no examples; no output format |
| ruflo/security-auditor/README.md | agent-doc | 60 | Stub content (4 lines); no frontmatter; no examples; no output format |
| ruflo/tactical-queen/README.md | agent-doc | 60 | Stub content (4 lines); no frontmatter; no examples; no output format |
| quantum/multi-platform-engineer/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("support", "coordinate") |
| quantum/quantum-optimization-engineer/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("post-processing", "analyze") |
| quantum/quantum-chemist/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("accuracy validation", "chemical insights") |
| quantum/quantum-test-engineer/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("test coverage analysis") |
| quantum/qec-specialist/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("validate error correction performance") |
| quantum/quantum-circuit-architect/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("balance fidelity and depth tradeoffs") |
| quantum/hamiltonian-simulator/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("analyze time evolution") |
| quantum/hardware-integrator/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("validate execution", "document configurations") |
| quantum/qnn-trainer/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("optimize training convergence") |
| quantum/quantum-sdk-developer/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("create tutorials and examples") |
| quantum/hybrid-system-architect/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("handle errors gracefully") |
| quantum/algorithm-benchmarker/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("assess quantum advantage claims") |
| quantum/variational-algorithm-specialist/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("avoid barren plateaus") |
| quantum/pqc-analyst/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("design migration strategies") |
| quantum/qrng-engineer/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("validate randomness quality") |
| quantum/quantum-finance-analyst/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("validate against classical methods") |
| quantum/noise-characterizer/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("assess hardware quality") |
| quantum/quantum-documentation-specialist/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("support developer onboarding") |
| quantum/qml-engineer/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("compare with classical baselines") |
| quantum/error-mitigation-engineer/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("balance overhead vs accuracy") |
| biomed/cybersecurity-specialist/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("implement security controls") |
| biomed/tissue-engineer/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("optimize", "characterize") |
| biomed/materials-specialist/AGENT.md | agent-def | 66 | No model; no output format; no examples; vague ("trade-off analysis", "application suitability") |
| civil/shop-drawing-reviewer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/structural-load-analyst/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/permit-coordinator/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/foundation-engineer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/water-distribution-engineer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/construction-scheduler/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/structural-peer-reviewer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/hydrology-analyst/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/bridge-engineer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/pavement-engineer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/specifications-writer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/reinforced-concrete-designer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/building-code-analyst/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/stormwater-management-specialist/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/seismic-design-specialist/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/bim-coordinator/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/environmental-compliance-specialist/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/slope-stability-analyst/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/cost-estimator/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/hydraulic-engineer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/structural-steel-designer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| civil/traffic-engineer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/human-factors-engineer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/biocompatibility-evaluator/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/software-vv-specialist/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/software-lifecycle-manager/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/clinical-study-manager/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/medical-imaging-engineer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/clinical-evidence-specialist/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/regulatory-submission-strategist/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/sterilization-engineer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/gait-biomechanist/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/manufacturing-engineer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/biomechanical-analyst/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/orthopedic-test-engineer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/packaging-engineer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/design-control-manager/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/post-market-surveillance-manager/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/vv-test-engineer/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/aiml-device-specialist/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| biomed/risk-manager/AGENT.md | agent-def | 70 | No model; no output format; no examples |
| ruflo/adaptive-queen/AGENT.md | agent-def | 71 | No output format section; no examples; vague ("dynamically", "appropriate memory scope") |
| mech/test-validation-specialist/AGENT.md | agent-def | 72 | No model; no examples; vague ("root cause analysis", "anomaly recognition", "lessons learned") |
| ruflo/strategic-queen/AGENT.md | agent-def | 73 | No output format; no examples; vague ("maintain vision") |
| ruflo/tactical-queen/AGENT.md | agent-def | 73 | No output format; no examples; vague ("properly") |
| mech/systems-engineering-specialist/AGENT.md | agent-def | 74 | No model; no examples; vague ("facilitate trade studies", "identify risks", "maturity assessment") |
| pilot-shell/plan-reviewer/README.md | agent-doc | 75 | No examples; no output format |
| pilot-shell/file-checker/README.md | agent-doc | 75 | No examples; no output format |
| pilot-shell/tdd-enforcer/README.md | agent-doc | 75 | No examples; no output format |
| pilot-shell/memory-curator/README.md | agent-doc | 75 | No examples; no output format |
| pilot-shell/unified-reviewer/README.md | agent-doc | 75 | No examples; no output format |
| pilot-shell/context-monitor/README.md | agent-doc | 75 | No examples; no output format |
| pilot-shell/plan-reviewer/AGENT.md | agent-def | 76 | No model; no examples; minor vague ("appropriate") |
| mech/pressure-equipment-specialist/AGENT.md | agent-def | 76 | No model; no examples; vague ("assess material requirements", "resolve code questions") |
| .claude/code-reviewer.md | agent-root | 80 | No model; no examples |
| .claude/sdk-api-documenter.md | agent-root | 80 | No model; no examples |
| pilot-shell/file-checker/AGENT.md | agent-def | 80 | No model; no examples |
| pilot-shell/tdd-enforcer/AGENT.md | agent-def | 80 | No model; no examples |
| pilot-shell/memory-curator/AGENT.md | agent-def | 80 | No model; no examples |
| pilot-shell/unified-reviewer/AGENT.md | agent-def | 80 | No model; no examples |
| pilot-shell/context-monitor/AGENT.md | agent-def | 80 | No model; no examples |
| ruflo/optimizer/AGENT.md | agent-def | 81 | No examples; minor vague ("tune", "improve") |
| ruflo/architect/AGENT.md | agent-def | 83 | No examples; minor vague ("complex") |
| ruflo/coder/AGENT.md | agent-def | 85 | No examples |
| ruflo/reviewer/AGENT.md | agent-def | 85 | No examples |
| ruflo/security-auditor/AGENT.md | agent-def | 85 | No examples |
| elec/test-measurement-expert/AGENT.md | agent-def | 90 | No model; one-example partial (reference tables only) |
| elec/reliability-engineer/AGENT.md | agent-def | 90 | No model; one-example partial (reference tables only) |
| elec/hardware-validation-engineer/AGENT.md | agent-def | 90 | No model; one-example partial (debug workflow diagram) |

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 4 |
| Medium | 8 |
| Low | 2 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hook scripts (shell) | `plugins/babysitter/hooks/babysitter-session-start-hook.sh`, `babysitter-stop-hook.sh`, `babysitter-pre-tool-use-hook.sh`, `babysitter-user-prompt-submit-hook.sh` |
| Hook configs (JSON) | `plugins/babysitter/hooks/hooks.json`, `plugins/babysitter-codex/hooks.json`, `plugins/babysitter-cursor/hooks.json` (+4 others) |
| Shell scripts | `scripts/rollback-release.sh`, `scripts/eval-compression.sh` |
| Package manifest | `package.json` (root workspace, no postinstall) |
| MCP configs | None found |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | `plugins/babysitter/hooks/babysitter-session-start-hook.sh` | 41 | PATH modification | `export PATH="$HOME/.local/bin:$PATH"` inside `install_sdk()` function; adds user-local dir to PATH, enabling PATH hijacking if `~/.local/bin` is writable by unprivileged processes |
| 2 | High | `plugins/babysitter/hooks/babysitter-stop-hook.sh` | 11 | PATH modification | `export PATH="$HOME/.local/bin:$PATH"` during stop hook execution; same hijacking vector as #1 |
| 3 | High | `plugins/babysitter/hooks/babysitter-pre-tool-use-hook.sh` | 10 | PATH modification | `export PATH="$HOME/.local/bin:$PATH"` during pre-tool-use hook; runs before every Bash tool call |
| 4 | High | `plugins/babysitter/hooks/babysitter-user-prompt-submit-hook.sh` | 10 | PATH modification | `export PATH="$HOME/.local/bin:$PATH"` during user prompt submission; high-frequency execution surface |
| 5 | Medium | `plugins/babysitter/hooks/babysitter-session-start-hook.sh` | 35 | Runtime package install | `npm i -g "@a5c-ai/babysitter-sdk@${target_version}"` installs external npm package at session start; version pinned via `versions.json` but fetched from network |
| 6 | Medium | `plugins/babysitter/hooks/babysitter-session-start-hook.sh` | 40 | Runtime package install | `npm i -g ... --prefix "$HOME/.local"` user-local fallback install; same supply-chain concern |
| 7 | Medium | `plugins/babysitter/hooks/babysitter-session-start-hook.sh` | 73 | Runtime package install (npx -y) | `npx -y "@a5c-ai/babysitter-sdk@${SDK_VERSION}"` last-resort auto-install without confirmation |
| 8 | Medium | `plugins/babysitter/hooks/babysitter-stop-hook.sh` | 16 | Runtime package install (npx -y) | `npx -y "@a5c-ai/babysitter-sdk@${SDK_VERSION}"` in stop hook; can install during any Claude stop event |
| 9 | Medium | `plugins/babysitter/hooks/babysitter-pre-tool-use-hook.sh` | 14 | Runtime package install (npx -y) | `npx -y "@a5c-ai/babysitter-sdk@${SDK_VERSION}"` in pre-tool-use hook; fires before every Bash tool call |
| 10 | Medium | `plugins/babysitter/hooks/babysitter-user-prompt-submit-hook.sh` | 14 | Runtime package install (npx -y) | `npx -y "@a5c-ai/babysitter-sdk@${SDK_VERSION}"` fires on every user prompt |
| 11 | Medium | `scripts/eval-compression.sh` | 170 | Heredoc with variable interpolation | `node --input-type=module <<NODESCRIPT ... '${OUT_FILE}' ... '${COMPRESSION_MJS}' ...` — variables (`OUT_FILE`, `COMPRESSION_MJS`) from env/filesystem are interpolated into executable Node.js code; malformed paths with shell metacharacters could break script integrity |
| 12 | Medium | `scripts/eval-compression.sh` | 176 | Variable interpolation in heredoc code | File paths from `find` scan of `~/.claude/projects/` are interpolated via `jq` into the inline Node.js heredoc; paths with special characters could affect script behavior |
| 13 | Low | `scripts/eval-compression.sh` | 84 | Sensitive data access | Script reads `~/.claude/projects/` (Claude Code session logs containing conversation history); appropriate for its stated purpose but worth noting in security review |
| 14 | Low | `scripts/rollback-release.sh` | 35 | User input in git push | `git push origin ":refs/tags/$TAG"` uses caller-supplied `$TAG` argument; value is quoted but a tag like `HEAD` or a refspec with `/` could have unintended effects |

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `library/methodologies/pilot-shell/agents/spec-guard/README.md` | Missing companion `AGENT.md` — the spec-guard agent has only a README with no YAML frontmatter (`name`, `description`); cannot be registered or invoked as a Claude Code agent | spec-guard agent is undiscoverable and unregisterable; it exists as documentation only with no executable definition |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `plugins/babysitter/hooks/babysitter-session-start-hook.sh` | `npm i -g` and `npx -y` fetch from npm registry at runtime without integrity verification | Pin `npm install` with `--prefer-offline` after a one-time verified download; add `npm pack` checksum in `versions.json` alongside `sdkVersion`; or ship the SDK as a bundled artifact within the plugin |
| 2 | `plugins/babysitter/hooks/babysitter-stop-hook.sh` | `npx -y` auto-install on every stop event | Same as #1; additionally consider moving SDK resolution to session-start only and caching the result |
| 3 | `plugins/babysitter/hooks/babysitter-pre-tool-use-hook.sh` | `npx -y` auto-install fires before every Bash tool call | Same as #1; pre-tool-use is a high-frequency path — unresolved CLI should exit 0 rather than auto-install |
| 4 | `plugins/babysitter/hooks/babysitter-user-prompt-submit-hook.sh` | `npx -y` auto-install on every user prompt | Same as #1 |
| 5 | `scripts/eval-compression.sh` | Variable interpolation into inline Node.js heredoc | Replace heredoc approach with a dedicated `.mjs` script file and pass variables as `--env` flags or CLI args; avoid building executable code strings from filesystem-derived values |
| 6 | `scripts/rollback-release.sh` | User-supplied `$TAG` in `git push` | Add input validation: `[[ "$TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "Invalid tag format"; exit 1; }` |

## Quality Issues (informational)

| # | File(s) | Issue | Penalty |
|---|---------|-------|---------|
| 1 | All 100 files | No example blocks — zero files include a concrete example invocation showing agent input → output | -15 per file |
| 2 | Civil engineering (22 files), Biomedical engineering (22 files), Quantum computing (20 files) | No output format section — 64 agent definitions lack any output format specification, leaving consumers to infer expected response structure | -10 per file |
| 3 | Civil engineering (22), Biomedical engineering (22), Quantum computing (20), Mechanical engineering (3), `.claude/agents` (2), pilot-shell AGENT.mds (6) | No `model` field in frontmatter — 91 files do not declare a preferred model; defaults to harness default which may not match agent complexity | -5 per file |
| 4 | Quantum computing (20 files) | Pervasive vague language — every quantum agent uses unmeasurable verbs: "support", "analyze", "optimize", "validate", "coordinate" without concrete acceptance criteria or deliverable specs | -4 per file |
| 5 | `biomed/cybersecurity-specialist`, `biomed/tissue-engineer`, `biomed/materials-specialist` | Moderate vague language in biomedical agents — "implement security controls", "optimize", "trade-off analysis" lack specificity compared to other biomedical agents | -4 per file |
| 6 | Mechanical engineering (3 files) | Minor vague language — "assess material requirements", "facilitate trade studies", "root cause analysis" without methodologies | -4 to -8 per file |
| 7 | Ruflo README stubs (7 files): `coder`, `adaptive-queen`, `reviewer`, `strategic-queen`, `optimizer`, `security-auditor`, `tactical-queen` | README stubs are 3–4 lines (title + one-sentence description + attribution) — no persona, expertise, collaboration, or usage sections; provide near-zero documentation value | -40 per file |
| 8 | `pilot-shell/spec-guard/README.md` | Standalone README with no companion AGENT.md — the only artifact for this agent lacks YAML frontmatter (`name`, `description`, `model`) required for Claude Code registration | -80 total |
| 9 | `ruflo/adaptive-queen/AGENT.md`, `ruflo/strategic-queen/AGENT.md`, `ruflo/tactical-queen/AGENT.md` | No output format section — queen agents define prompt templates but omit explicit output format; the three queens are the most complex agents in the ruflo swarm | -10 per file |
| 10 | All pilot-shell AGENT.mds (6 files) | No model declaration — complex agents (plan-reviewer, unified-reviewer) have no model hint; they use sophisticated multi-criteria reasoning that benefits from Sonnet/Opus | -5 per file |
| 11 | `.claude/agents/code-reviewer.md`, `.claude/agents/sdk-api-documenter.md` | No model declaration on root project agents; these serve as primary review/documentation agents for a TypeScript monorepo | -5 per file |
| 12 | Electrical engineering (3 files) | No `model` field — the EE agents have good output format + reference tables but omit model, which matters for complex measurement uncertainty and FMEA analysis | -5 per file |
| 13 | Quantum computing (20 files) | Role categorization overlap — "Application Development Agent" is assigned to 3 distinct agents (quantum-optimization-engineer, quantum-sdk-developer, quantum-finance-analyst); "Error Management Agent" to 3 others; reduces disambiguation | informational |
| 14 | Biomedical engineering (22 files) | Cross-reference IDs (e.g., "Works with AG-004") not validated — references point to numeric IDs that cannot be resolved from directory structure alone; a registry mapping IDs to paths is absent | informational |
| 15 | Pilot-shell READMEs (6 files) | No output format or examples — supplementary README docs are well-structured but don't document what agents produce, making them incomplete as standalone references | -10 per file |
| 16 | All AGENT.md files in `library/` | No `tools` or `allowed-tools` declared — library agents don't specify which Claude Code tools they may invoke; this makes capability scoping impossible | informational |
| 17 | Quantum computing (20 files) | `phase: 6` metadata is unexplained — no documentation of what phases mean or how they map to the development lifecycle | informational |

## Cross-Component

**Broken References:**
- `pilot-shell/spec-guard/README.md` references `pilot-shell-feature.js` for spec completion enforcement, but no `AGENT.md` exists to make spec-guard invocable. The orchestration process expects an agent that cannot be registered.

**Orphaned Components:**
- The 7 ruflo README stubs serve only as attribution notes. The actual agent definitions (`AGENT.md`) exist, but the READMEs provide no additional context beyond a one-line description. They can be merged into the AGENT.mds or expanded.

**Structural Inconsistencies:**
- Pilot-shell agents follow a pattern of README.md + AGENT.md pairs; ruflo follows the same pattern except `architect` has only an AGENT.md (no README). This is the inverse problem from spec-guard.
- Electrical engineering agents use a `backlog-id` field (AG-009, AG-013, AG-014) while biomedical agents use `agent-id` with BME-AG-XXX format and civil engineering uses CIV-AG-XXX. No unified agent ID scheme across specializations.
- Civil engineering agents define `Collaboration` sections that reference other civil engineering agents by display name ("Works with Structural Load Analyst"), while biomedical agents use numeric IDs ("Works with AG-004"). Cross-specialization collaboration would be ambiguous.
- The `.claude/settings.json` is empty `{}`, meaning the project's PostToolUse lint hook documented in `CLAUDE.md` is not actually configured — the CLAUDE.md documentation describes a hook that is not present in settings.

**Contradictions:**
- `CLAUDE.md` states: "PostToolUse (Edit|Write on .ts files): Auto-runs npm run lint … Failures are suppressed." But `.claude/settings.json` contains `{}` — no hooks are configured. The documented behavior does not match the actual configuration.

## Recommendation

REVIEW — submit NL fix PRs for the spec-guard AGENT.md bug. Flag HIGH security findings (PATH modifications in all four hook scripts) in a private issue for maintainer review before merging. Medium/low security fixes (runtime npm installs, heredoc interpolation, input validation) are suitable for public PRs.

**Priority order:**
1. **Bug PR**: Add `library/methodologies/pilot-shell/agents/spec-guard/AGENT.md` with proper frontmatter (`name: spec-guard`, `description`, `model`) and output format — unblocks orchestration processes that reference this agent.
2. **Security PR (Medium)**: Replace `npx -y` auto-install pattern in all four hook scripts with a pre-verified install or offline bundle.
3. **Quality PRs**: Add `model` field to civil engineering, biomedical, and quantum computing AGENT.mds (batch PR per domain); add output format sections to civil engineering and biomedical AGENT.mds.
4. **Private issue**: PATH modification in hooks (#1–4) — review whether `export PATH=` is necessary given that session-start already handles installation; consider removing from stop/pre-tool-use/user-prompt-submit hooks.
