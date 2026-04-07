# NLPM Audit: deanpeters/Product-Manager-Skills
**Date**: 2026-04-07  |  **Artifacts**: 55  |  **Strategy**: batched
**NL Score**: 89/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 19  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| CLAUDE.md | doc | 50 | No NL frontmatter (name/description absent) |
| commands/README.md | doc | 50 | No command frontmatter (name/description absent) |
| commands/discover.md | command | 85 | Missing allowed-tools; no empty-input handling |
| commands/leadership-transition.md | command | 85 | Missing allowed-tools; no empty-input handling |
| commands/plan-roadmap.md | command | 85 | Missing allowed-tools; no empty-input handling |
| commands/prioritize.md | command | 85 | Missing allowed-tools; no empty-input handling |
| commands/strategy.md | command | 85 | Missing allowed-tools; no empty-input handling |
| commands/write-prd.md | command | 85 | Missing allowed-tools; no empty-input handling |
| skills/company-research/SKILL.md | component | 90 | No best_for/scenarios metadata |
| skills/eol-message/SKILL.md | component | 90 | No best_for/scenarios metadata |
| skills/epic-hypothesis/SKILL.md | component | 90 | No best_for/scenarios metadata |
| skills/jobs-to-be-done/SKILL.md | component | 90 | Placeholder Substack reference in refs section |
| skills/opportunity-solution-tree/SKILL.md | interactive | 90 | No best_for/scenarios metadata |
| skills/pestel-analysis/SKILL.md | component | 90 | No best_for/scenarios metadata |
| skills/press-release/SKILL.md | component | 90 | Placeholder Substack reference in refs section |
| skills/problem-statement/SKILL.md | component | 90 | Placeholder Substack reference in refs section |
| skills/product-strategy-session/SKILL.md | workflow | 90 | No best_for/scenarios metadata |
| skills/recommendation-canvas/SKILL.md | component | 90 | No best_for/scenarios metadata |
| skills/tam-sam-som-calculator/SKILL.md | interactive | 90 | No best_for/scenarios metadata |
| skills/user-story-mapping/SKILL.md | component | 90 | No best_for/scenarios metadata |
| skills/user-story-splitting/SKILL.md | component | 90 | No best_for/scenarios metadata |
| skills/ai-shaped-readiness-advisor/SKILL.md | interactive | 91 | File too large (>10K tokens) for single-pass read |
| skills/altitude-horizon-framework/SKILL.md | component | 91 | None significant |
| skills/business-health-diagnostic/SKILL.md | interactive | 91 | None significant |
| skills/context-engineering-advisor/SKILL.md | interactive | 91 | None significant |
| skills/customer-journey-map/SKILL.md | component | 91 | None significant |
| skills/customer-journey-mapping-workshop/SKILL.md | interactive | 91 | None significant |
| skills/director-readiness-advisor/SKILL.md | interactive | 91 | None significant |
| skills/discovery-interview-prep/SKILL.md | interactive | 91 | None significant |
| skills/discovery-process/SKILL.md | workflow | 91 | None significant |
| skills/epic-breakdown-advisor/SKILL.md | interactive | 91 | None significant |
| skills/feature-investment-advisor/SKILL.md | interactive | 91 | None significant |
| skills/finance-based-pricing-advisor/SKILL.md | interactive | 91 | None significant |
| skills/finance-metrics-quickref/SKILL.md | component | 91 | None significant |
| skills/lean-ux-canvas/SKILL.md | interactive | 91 | None significant |
| skills/pol-probe-advisor/SKILL.md | interactive | 91 | None significant |
| skills/pol-probe/SKILL.md | component | 91 | None significant |
| skills/positioning-workshop/SKILL.md | interactive | 91 | None significant |
| skills/prioritization-advisor/SKILL.md | interactive | 91 | None significant |
| skills/problem-framing-canvas/SKILL.md | interactive | 91 | None significant |
| skills/product-sense-interview-answer/SKILL.md | component | 91 | None significant |
| skills/roadmap-planning/SKILL.md | workflow | 91 | None significant |
| skills/saas-economics-efficiency-metrics/SKILL.md | component | 91 | None significant |
| skills/saas-revenue-growth-metrics/SKILL.md | component | 91 | None significant |
| skills/skill-authoring-workflow/SKILL.md | workflow | 91 | None significant |
| skills/user-story/SKILL.md | component | 91 | None significant |
| skills/vp-cpo-readiness-advisor/SKILL.md | interactive | 91 | None significant |
| skills/workshop-facilitation/SKILL.md | interactive | 91 | None significant |
| skills/acquisition-channel-advisor/SKILL.md | interactive | 93 | None significant |
| skills/proto-persona/SKILL.md | component | 93 | None significant |
| skills/storyboard/SKILL.md | component | 93 | None significant |
| skills/prd-development/SKILL.md | workflow | 94 | None significant |
| skills/positioning-statement/SKILL.md | component | 94 | None significant |
| skills/user-story-mapping-workshop/SKILL.md | interactive | 94 | None significant |
| skills/executive-onboarding-playbook/SKILL.md | workflow | 95 | None significant |

**Score calculation:** 2×50 + 6×85 + 13×90 + 27×91 + 3×93 + 3×94 + 1×95 = 4893 / 55 = **89/100**

---

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts (sh) | 13 |
| Scripts (py) | 3 |
| MCP configs | 0 |
| Package manifests (package.json, requirements.txt) | 0 |

Scripts found: `scripts/adapters/ADAPTER_TEMPLATE.sh`, `scripts/adapters/claude-code.sh`, `scripts/adapters/manual.sh`, `scripts/add-a-skill.sh`, `scripts/build-a-skill.sh`, `scripts/find-a-command.sh`, `scripts/find-a-skill.sh`, `scripts/package-claude-skills.sh`, `scripts/run-pm.sh`, `scripts/test-a-skill.sh`, `scripts/test-library.sh`, `scripts/zip-a-skill.sh`, `scripts/check-command-metadata.py`, `scripts/check-skill-metadata.py`, `scripts/check-skill-triggers.py`, `scripts/generate-catalog.py`

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | scripts/run-pm.sh | ~119 | Network call via external CLI | `claude "$prompt"` executes the Claude Code CLI with user-supplied input (`$INPUT` from argv[3]). No shell injection risk (no `eval`), but content flows to an AI API without sanitization. Local dev tool; low operational risk. |
| 2 | Medium | scripts/run-pm.sh | ~128 | Network call via external CLI | `codex "$prompt"` executes the OpenAI Codex CLI with the same user-supplied prompt. Same pattern as finding #1. |
| 3 | Medium | scripts/add-a-skill.sh | ~120 | Dynamic file sourcing | `source "$adapter"` dynamically sources shell scripts resolved from `$ADAPTERS_DIR/*.sh`. If the adapters directory is writable by untrusted parties, a malicious `.sh` file dropped there would execute in the script's context. In practice this is a local developer tool; risk is minimal. |

---

## Bugs (PR-worthy)
No bugs found. All 6 command files have the required `name` and `description` frontmatter fields. All 47 skill files have the required `name`, `description`, `intent`, and `type` fields. No broken skill or command cross-references were detected. No tools are called outside of declared permissions.

---

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/run-pm.sh | User CLI input passed directly to `claude` and `codex` binaries with no length or content validation | Add input length guard (e.g., max 2000 chars) and strip shell metacharacters before passing to CLI. Document that this script is for local development only. |
| 2 | scripts/add-a-skill.sh | Dynamic `source` of files from `$ADAPTERS_DIR` | Validate sourced files against a whitelist of known adapter names before sourcing; add a comment warning that adapters directory must not be world-writable. |

---

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/prioritize.md | Missing `allowed-tools` field — no tool access restriction when command runs | -5 |
| 2 | commands/write-prd.md | Missing `allowed-tools` field | -5 |
| 3 | commands/strategy.md | Missing `allowed-tools` field | -5 |
| 4 | commands/leadership-transition.md | Missing `allowed-tools` field | -5 |
| 5 | commands/plan-roadmap.md | Missing `allowed-tools` field | -5 |
| 6 | commands/discover.md | Missing `allowed-tools` field | -5 |
| 7 | commands/prioritize.md | No empty-input handling — behavior undefined when invoked with no argument | -10 |
| 8 | commands/write-prd.md | No empty-input handling | -10 |
| 9 | commands/strategy.md | No empty-input handling | -10 |
| 10 | commands/leadership-transition.md | No empty-input handling | -10 |
| 11 | commands/plan-roadmap.md | No empty-input handling | -10 |
| 12 | commands/discover.md | No empty-input handling | -10 |
| 13 | commands/README.md | No command frontmatter (name, description absent); unfindable by automation that parses commands/ | -50 |
| 14 | CLAUDE.md | No NL artifact frontmatter; treated as unstructured documentation by NLPM tooling | -50 |
| 15 | skills/jobs-to-be-done/SKILL.md | Placeholder reference text: "Link to relevant Dean Peters' Substack articles if applicable" — dead link | -2 |
| 16 | skills/problem-statement/SKILL.md | Same placeholder reference | -2 |
| 17 | skills/positioning-statement/SKILL.md | Same placeholder reference | -2 |
| 18 | skills/storyboard/SKILL.md | Same placeholder reference | -2 |
| 19 | skills/ai-shaped-readiness-advisor/SKILL.md | File exceeds 10K tokens; cannot be loaded in a single context read by scanning tools | informational |

---

## Cross-Component
**References:** All `uses:` entries in the 6 commands resolve to existing `skills/*/SKILL.md` files. All inter-skill references in `## References` sections (e.g., `skills/proto-persona/SKILL.md`, `../workshop-facilitation/SKILL.md`) resolve correctly.

**CLAUDE.md planned skills:** Three skills listed as "Remaining (Planned)" in CLAUDE.md — `ai-product-evals`, `ai-observability-framework`, `ai-maintenance-planning` — do not exist yet. This is expected (planned work), not a broken reference.

**commands/README.md vs commands/*.md:** The README lists `discover`, `strategy`, `write-prd`, `plan-roadmap`, `prioritize`, `leadership-transition` as the v1 command set, which matches the 6 command files present. No orphaned commands.

**workshop-facilitation as dependency:** Several interactive skills (`user-story-mapping-workshop`, `prd-development`, `acquisition-channel-advisor`, `pol-probe-advisor`, `director-readiness-advisor`) reference `../workshop-facilitation/SKILL.md` as the canonical facilitation protocol. That file exists and is well-defined — the pattern is consistent and healthy.

**Scoring tools vs. repo philosophy:** The CLAUDE.md explicitly notes (v0.75 update) that "external scoring tools optimizing for the wrong rubric" are a known risk. The `allowed-tools` and empty-input-handling deductions above represent standard NLPM rubric penalties, not defects in the skills themselves. The pedagogic content (Why This Works, Anti-Patterns, Common Pitfalls) that this repo deliberately protects has not been penalized.

---

## Recommendation

Security is **CLEAR** — no Critical or High findings. All scripts are local developer tools with no destructive patterns, no credential exfiltration, and no eval-with-variables. The three Medium findings are informational; the suggested fixes are low-effort hardening for a public-facing tool.

NL quality is strong at **89/100**, well above the default 70 threshold. The skill library is exceptionally well-structured — full frontmatter across all 47 skills, comprehensive Examples and Common Pitfalls sections, detailed pedagogic content, and clean cross-references. The primary scoring drag comes from the 6 commands lacking `allowed-tools` and empty-input handling, and the two documentation files (CLAUDE.md, commands/README.md) that are not in command/skill format.

**CLEAR — submit PRs for the medium/low security hardening fixes. No NL bugs require PRs. Quality improvements (allowed-tools, empty-input handling on commands) are optional enhancements worth noting to the maintainer.**
