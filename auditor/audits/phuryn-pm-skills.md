# NLPM Audit: phuryn/pm-skills
**Date**: 2026-04-06  |  **Artifacts**: 100 (42 commands + 58 skills; scope per audit task — see Cross-Component)  |  **Strategy**: progressive
**NL Score**: 92/100
**Security**: CLEAR
**Bugs**: 38  |  **Quality Issues**: 134  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| pm-toolkit/commands/review-resume.md | command | 76 | No handling for empty/missing input |
| pm-data-analytics/commands/write-query.md | command | 78 | Missing allowed-tools despite reading uploaded schema files |
| pm-market-research/commands/competitive-analysis.md | command | 78 | No explicit handling for empty/missing input |
| pm-execution/commands/test-scenarios.md | command | 78 | No handling for empty/missing input |
| pm-toolkit/commands/proofread.md | command | 80 | No handling for empty/missing input |
| pm-data-analytics/commands/analyze-cohorts.md | command | 80 | Missing allowed-tools despite Python/pandas + file-save use |
| pm-go-to-market/commands/plan-launch.md | command | 80 | Missing allowed-tools despite file-save + PRD/deck upload use |
| pm-go-to-market/commands/growth-strategy.md | command | 80 | Missing allowed-tools despite file-save + metrics upload use |
| pm-go-to-market/commands/battlecard.md | command | 80 | Missing allowed-tools despite web-research + file-save use |
| pm-product-strategy/skills/startup-canvas/SKILL.md | skill | 80 | Description has only 2 trigger phrases (borderline generic) |
| pm-execution/commands/pre-mortem.md | command | 80 | No handling for empty/missing plan input |
| pm-execution/commands/transform-roadmap.md | command | 80 | No handling for empty/missing roadmap input |
| pm-data-analytics/commands/analyze-test.md | command | 83 | Missing allowed-tools despite Python/scipy + CSV upload use |
| pm-ai-shipping/commands/document-app.md | command | 83 | No structured output template defined |
| pm-market-research/commands/analyze-feedback.md | command | 85 | No explicit handling for empty/missing input |
| pm-execution/commands/red-team-prd.md | command | 85 | No handling for empty/missing plan input |
| pm-toolkit/skills/review-resume/SKILL.md | skill | 87 | Repeated unqualified use of "relevant" |
| pm-toolkit/commands/draft-nda.md | command | 88 | Missing allowed-tools despite file-save instruction |
| pm-toolkit/skills/draft-nda/SKILL.md | skill | 88 | No worked example of actual NDA clause language |
| pm-product-strategy/commands/business-model.md | command | 88 | Missing allowed-tools despite file-save instruction |
| pm-product-strategy/commands/strategy.md | command | 88 | Missing allowed-tools despite file-save instruction |
| pm-execution/commands/write-stories.md | command | 88 | Missing allowed-tools despite file-save instruction |
| pm-marketing-growth/commands/market-product.md | command | 90 | Missing allowed-tools despite file-save instruction |
| pm-marketing-growth/commands/north-star.md | command | 90 | Missing allowed-tools despite file-save instruction |
| pm-toolkit/commands/privacy-policy.md | command | 90 | Missing allowed-tools despite file-save instruction |
| pm-marketing-growth/skills/product-name/SKILL.md | skill | 90 | No concrete example of a generated name |
| pm-market-research/skills/market-sizing/SKILL.md | skill | 90 | No concrete worked example |
| pm-product-strategy/commands/market-scan.md | command | 90 | Missing allowed-tools despite web-research instruction |
| pm-product-strategy/commands/value-proposition.md | command | 90 | Missing allowed-tools despite file-save instruction |
| pm-execution/commands/stakeholder-map.md | command | 90 | Missing allowed-tools despite file-save instruction |
| pm-execution/commands/generate-data.md | command | 90 | Missing allowed-tools despite script-execution + file-save use |
| pm-execution/commands/sprint.md | command | 90 | Missing allowed-tools despite file-save instruction |
| pm-product-discovery/commands/triage-requests.md | command | 90 | Missing allowed-tools frontmatter |
| pm-product-discovery/commands/brainstorm.md | command | 90 | Missing allowed-tools frontmatter |
| pm-product-discovery/commands/discover.md | command | 90 | Missing allowed-tools frontmatter |
| pm-toolkit/commands/tailor-resume.md | command | 91 | Missing allowed-tools despite file-upload handling |
| pm-marketing-growth/skills/marketing-ideas/SKILL.md | skill | 92 | No concrete example of a generated idea |
| pm-go-to-market/skills/gtm-motions/SKILL.md | skill | 92 | Complex 7-motion-type framework, no worked examples |
| pm-go-to-market/skills/beachhead-segment/SKILL.md | skill | 92 | Complex 4-criteria framework, no worked example |
| pm-go-to-market/skills/ideal-customer-profile/SKILL.md | skill | 92 | Complex JTBD/ICP framework, no worked example |
| pm-go-to-market/skills/gtm-strategy/SKILL.md | skill | 92 | GTM framework explained with no worked example |
| pm-market-research/skills/market-segments/SKILL.md | skill | 92 | No concrete worked example |
| pm-market-research/skills/competitor-analysis/SKILL.md | skill | 92 | No concrete worked example |
| pm-market-research/skills/sentiment-analysis/SKILL.md | skill | 92 | No concrete worked example |
| pm-market-research/skills/user-personas/SKILL.md | skill | 92 | No concrete worked example |
| pm-market-research/skills/user-segmentation/SKILL.md | skill | 92 | No concrete worked example |
| pm-ai-shipping/skills/shipping-artifacts/SKILL.md | skill | 92 | Description length in 500-800 char penalty band (585 chars) |
| pm-product-strategy/commands/pricing.md | command | 93 | Missing allowed-tools despite web-research + file-save use |
| pm-execution/skills/create-prd/SKILL.md | skill | 93 | No worked example of a filled PRD |
| pm-execution/skills/wwas/SKILL.md | skill | 93 | Missing scope note vs. user-stories/job-stories |
| pm-market-research/commands/research-users.md | command | 95 | Missing allowed-tools despite clear tool use |
| pm-ai-shipping/commands/derive-tests.md | command | 95 | Missing allowed-tools despite clear tool use |
| pm-ai-shipping/commands/ship-check.md | command | 95 | Missing allowed-tools despite clear tool use |
| pm-ai-shipping/commands/performance-audit-static.md | command | 95 | No error-path handling for missing prerequisite input |
| pm-execution/commands/write-prd.md | command | 95 | Missing allowed-tools despite file-save instruction |
| pm-execution/commands/meeting-notes.md | command | 95 | Missing allowed-tools despite file-save instruction |
| pm-execution/skills/user-stories/SKILL.md | skill | 95 | Missing scope note vs. job-stories/wwas |
| pm-execution/skills/test-scenarios/SKILL.md | skill | 95 | Missing scope note vs. user-stories/job-stories/wwas |
| pm-execution/skills/job-stories/SKILL.md | skill | 95 | Missing scope note vs. user-stories/wwas |
| pm-execution/skills/sprint-plan/SKILL.md | skill | 95 | Missing scope note vs. retro |
| pm-execution/skills/pre-mortem/SKILL.md | skill | 95 | Missing scope note vs. strategy-red-team |
| pm-execution/skills/strategy-red-team/SKILL.md | skill | 95 | No worked example of the red-team methodology |
| pm-product-discovery/commands/setup-metrics.md | command | 95 | Missing allowed-tools frontmatter |
| pm-product-discovery/commands/interview.md | command | 95 | Missing allowed-tools frontmatter |
| pm-product-discovery/skills/analyze-feature-requests/SKILL.md | skill | 95 | Opportunity Score formula, no worked example |
| pm-product-discovery/skills/prioritize-assumptions/SKILL.md | skill | 95 | ICE/Risk formula, no worked numeric example |
| pm-product-discovery/skills/opportunity-solution-tree/SKILL.md | skill | 95 | No single end-to-end worked example |
| pm-product-discovery/skills/prioritize-features/SKILL.md | skill | 95 | Opportunity/ICE/RICE formulas, no worked example |
| pm-data-analytics/skills/cohort-analysis/SKILL.md | skill | 95 | No scope note vs. sibling skills |
| pm-marketing-growth/skills/positioning-ideas/SKILL.md | skill | 97 | Missing scope note |
| pm-marketing-growth/skills/north-star-metric/SKILL.md | skill | 97 | Missing scope note |
| pm-marketing-growth/skills/value-prop-statements/SKILL.md | skill | 97 | Missing scope note |
| pm-toolkit/skills/grammar-check/SKILL.md | skill | 97 | Missing scope note |
| pm-toolkit/skills/privacy-policy/SKILL.md | skill | 97 | Missing scope note |
| pm-data-analytics/skills/sql-queries/SKILL.md | skill | 97 | No scope note vs. sibling skills |
| pm-data-analytics/skills/ab-test-analysis/SKILL.md | skill | 97 | No scope note vs. sibling skills |
| pm-go-to-market/skills/competitive-battlecard/SKILL.md | skill | 97 | No scope note vs. sibling skills |
| pm-go-to-market/skills/growth-loops/SKILL.md | skill | 97 | No scope note vs. gtm-motions |
| pm-market-research/skills/customer-journey-map/SKILL.md | skill | 97 | Missing scope note vs. sibling skills |
| pm-product-strategy/skills/monetization-strategy/SKILL.md | skill | 97 | No scope note vs. sibling pricing-strategy skill |
| pm-execution/skills/retro/SKILL.md | skill | 97 | Missing scope note vs. sprint-plan |
| pm-product-discovery/skills/brainstorm-ideas-existing/SKILL.md | skill | 97 | No scope note vs. brainstorm-ideas-new |
| pm-product-discovery/skills/brainstorm-experiments-new/SKILL.md | skill | 97 | No scope note vs. brainstorm-experiments-existing |
| pm-product-discovery/skills/identify-assumptions-existing/SKILL.md | skill | 97 | No scope note vs. identify-assumptions-new |
| pm-product-discovery/skills/identify-assumptions-new/SKILL.md | skill | 97 | No scope note vs. identify-assumptions-existing |
| pm-product-discovery/skills/brainstorm-experiments-existing/SKILL.md | skill | 97 | No scope note vs. brainstorm-experiments-new |
| pm-product-discovery/skills/brainstorm-ideas-new/SKILL.md | skill | 97 | No scope note vs. brainstorm-ideas-existing |
| pm-execution/skills/brainstorm-okrs/SKILL.md | skill | 98 | Vague quantifier "some" |
| pm-execution/skills/summarize-meeting/SKILL.md | skill | 98 | Vague quantifier "as needed" |
| pm-execution/skills/dummy-dataset/SKILL.md | skill | 98 | Vague quantifier "business-appropriate" |
| pm-execution/skills/stakeholder-map/SKILL.md | skill | 98 | Vague quantifier "relevant" |
| pm-ai-shipping/commands/security-audit-static.md | command | 100 | None |
| pm-ai-shipping/skills/intended-vs-implemented/SKILL.md | skill | 100 | None |
| pm-execution/commands/plan-okrs.md | command | 100 | None |
| pm-execution/skills/outcome-roadmap/SKILL.md | skill | 100 | None |
| pm-execution/skills/prioritization-frameworks/SKILL.md | skill | 100 | None |
| pm-execution/skills/release-notes/SKILL.md | skill | 100 | None |
| pm-product-discovery/skills/summarize-interview/SKILL.md | skill | 100 | None |
| pm-product-discovery/skills/interview-script/SKILL.md | skill | 100 | None |
| pm-product-discovery/skills/metrics-dashboard/SKILL.md | skill | 100 | None |

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
| Hooks | none |
| Scripts | `validate_plugins.py`, `tests/test_validator.py`, `tests/test_consistency.py` |
| MCP configs | none |
| Package manifests | none (`package.json`, `requirements.txt` not present) |

All three Python scripts are stdlib-only (`json`, `os`, `re`, `sys`, `pathlib`, `unittest`). No `eval`/`exec`, no `subprocess`/`os.system`, no `shell=True`, no network calls (`curl`/`wget`/`requests`/`fetch`), no credential handling, no dynamic code loading, no file writes outside the repo tree (`validate_plugins.py` only reads; the two test modules only read via `Path.read_text`/`json.load`). `validate_plugins.py`'s only "risk-adjacent" behavior is ANSI color-code printing to stdout — cosmetic, not a security concern. No `.mcp.json`, no hooks, no `package.json` postinstall scripts.

Commands (`*/commands/*.md`) were also checked for the "Bash + unsanitized user arguments" pattern: none of the 42 commands declare or instruct raw shell execution of `$ARGUMENTS`; the two commands that do declare `allowed-tools` (`security-audit-static.md`, `performance-audit-static.md`) scope their `Bash` grants to read-only git subcommands (`Bash(git log:*)`, `Bash(git diff:*)`, `Bash(git show:*)`) and a path-scoped `Write(reports/**)` — least-privilege, no injection surface.

### Security Findings
No security findings.

## Bugs (PR-worthy)

Systemic pattern: **38 of 42 commands (90%)** instruct the model to use a specific tool (`Write` to save output, `Read` to ingest uploaded files, `Bash` to execute a script, `WebSearch`/`WebFetch` for research, `Task` to fan out subagents) but declare no `allowed-tools` frontmatter field at all. Only 2 commands in the repo (`pm-ai-shipping/commands/security-audit-static.md`, `pm-ai-shipping/commands/performance-audit-static.md`) declare `allowed-tools`, and both scope it tightly. This is deterministic and reproducible (`grep -L allowed-tools` cross-referenced against explicit tool-use instructions in the body) — every row below is a mechanical one-line frontmatter fix.

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | pm-marketing-growth/commands/market-product.md | Instructs "Save as markdown" (Write) with no allowed-tools declared | Command runs with unrestricted, undeclared tool access instead of least-privilege |
| 2 | pm-marketing-growth/commands/north-star.md | Instructs "Save as markdown" (Write) with no allowed-tools declared | Same |
| 3 | pm-toolkit/commands/privacy-policy.md | Instructs "Save as markdown. Offer DOCX export." with no allowed-tools declared | Same |
| 4 | pm-toolkit/commands/proofread.md | Instructs accepting uploaded DOCX/PDF (Read) with no allowed-tools declared | Same |
| 5 | pm-toolkit/commands/tailor-resume.md | Instructs reading uploaded resume/JD + URL fetch (Read, WebFetch) with no allowed-tools declared | Same |
| 6 | pm-toolkit/commands/review-resume.md | Instructs "Accept... uploaded PDF, or DOCX file" (Read) with no allowed-tools declared | Same |
| 7 | pm-toolkit/commands/draft-nda.md | Instructs "Save as markdown. Offer to export as DOCX" with no allowed-tools declared | Same |
| 8 | pm-data-analytics/commands/analyze-cohorts.md | Instructs Python/pandas processing + markdown/CSV save with no allowed-tools declared | Same |
| 9 | pm-data-analytics/commands/write-query.md | Instructs reading uploaded schema files with no allowed-tools declared | Same |
| 10 | pm-data-analytics/commands/analyze-test.md | Instructs Python/scipy.stats + CSV/screenshot read with no allowed-tools declared | Same |
| 11 | pm-go-to-market/commands/plan-launch.md | Instructs "Save as markdown" + PRD/deck upload with no allowed-tools declared | Same |
| 12 | pm-go-to-market/commands/growth-strategy.md | Instructs "Save as markdown" + metrics upload with no allowed-tools declared | Same |
| 13 | pm-go-to-market/commands/battlecard.md | Instructs web research + "Save as markdown" with no allowed-tools declared | Same |
| 14 | pm-market-research/commands/competitive-analysis.md | Instructs web research + "Save as markdown" with no allowed-tools declared | Same |
| 15 | pm-market-research/commands/analyze-feedback.md | Instructs reading uploaded CSV/Excel + saving CSV/markdown with no allowed-tools declared | Same |
| 16 | pm-market-research/commands/research-users.md | Instructs reading uploaded research files + "Save as markdown" with no allowed-tools declared | Same |
| 17 | pm-ai-shipping/commands/derive-tests.md | Instructs writing `documentation/tests.md` + timestamped report with no allowed-tools declared | Same |
| 18 | pm-ai-shipping/commands/document-app.md | Instructs producing files under `documentation/` and fanning out subagents (Write, Task) with no allowed-tools declared | Same |
| 19 | pm-ai-shipping/commands/ship-check.md | Instructs creating/refreshing CLAUDE.md/AGENTS.md + parallel subagents (Write, Task) with no allowed-tools declared | Same |
| 20 | pm-product-strategy/commands/business-model.md | Instructs "Save as markdown" with no allowed-tools declared | Same |
| 21 | pm-product-strategy/commands/pricing.md | Instructs web research + "Save as markdown" with no allowed-tools declared | Same |
| 22 | pm-product-strategy/commands/market-scan.md | Instructs "Use web research to ground the analysis" with no allowed-tools declared | Same |
| 23 | pm-product-strategy/commands/value-proposition.md | Instructs "Save as markdown" with no allowed-tools declared | Same |
| 24 | pm-product-strategy/commands/strategy.md | Instructs "Save as markdown" with no allowed-tools declared | Same |
| 25 | pm-execution/commands/write-prd.md | Instructs "Save the PRD as a markdown file" with no allowed-tools declared | Same |
| 26 | pm-execution/commands/stakeholder-map.md | Instructs "Save as markdown" with no allowed-tools declared | Same |
| 27 | pm-execution/commands/pre-mortem.md | Instructs "Save as markdown" with no allowed-tools declared | Same |
| 28 | pm-execution/commands/generate-data.md | Instructs executing a generator script + saving output (Bash, Write) with no allowed-tools declared | Same |
| 29 | pm-execution/commands/meeting-notes.md | Instructs "Save as markdown" with no allowed-tools declared | Same |
| 30 | pm-execution/commands/transform-roadmap.md | Instructs "Save as a markdown file" with no allowed-tools declared | Same |
| 31 | pm-execution/commands/test-scenarios.md | Instructs "Save as markdown" with no allowed-tools declared | Same |
| 32 | pm-execution/commands/sprint.md | Instructs "Save as markdown and offer to format for different channels" with no allowed-tools declared | Same |
| 33 | pm-execution/commands/write-stories.md | Instructs "Save as markdown" with no allowed-tools declared | Same |
| 34 | pm-product-discovery/commands/setup-metrics.md | Instructs "Save as a markdown file" with no allowed-tools declared | Same |
| 35 | pm-product-discovery/commands/triage-requests.md | Instructs reading uploaded files + saving markdown/CSV output with no allowed-tools declared | Same |
| 36 | pm-product-discovery/commands/brainstorm.md | Instructs "Accept context from uploaded files" (Read) with no allowed-tools declared | Same |
| 37 | pm-product-discovery/commands/interview.md | Instructs "Save the summary as a markdown file" with no allowed-tools declared | Same |
| 38 | pm-product-discovery/commands/discover.md | Instructs reading uploaded research + "Save the plan as a markdown file" with no allowed-tools declared | Same |

## Security Fixes (PR-worthy, Medium/Low only)
No Medium/Low security findings — nothing to fix.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | pm-marketing-growth/commands/market-product.md | No error-path handling for missing/ambiguous product context (R17) | -5 |
| 2 | pm-marketing-growth/commands/north-star.md | No error-path handling for missing/ambiguous metrics data (R17) | -5 |
| 3 | pm-toolkit/commands/privacy-policy.md | No error-path handling for missing/ambiguous data-handling context (R17) | -5 |
| 4 | pm-toolkit/commands/proofread.md | No handling for empty/missing input — no text provided (R15) | -10 |
| 5 | pm-toolkit/commands/proofread.md | No error-path handling for unreadable/corrupted documents (R17) | -5 |
| 6 | pm-toolkit/commands/tailor-resume.md | Two unqualified uses of "relevant" (R01) | -4 |
| 7 | pm-toolkit/commands/review-resume.md | No handling for empty/missing input — no resume provided (R15) | -10 |
| 8 | pm-toolkit/commands/review-resume.md | No error-path handling for unreadable/corrupted resume files (R17) | -5 |
| 9 | pm-toolkit/commands/review-resume.md | Two unqualified uses of "relevant" (R01) | -4 |
| 10 | pm-toolkit/commands/draft-nda.md | No error-path handling for missing/ambiguous party/jurisdiction details (R17) | -5 |
| 11 | pm-toolkit/commands/draft-nda.md | Vague quantifier "jurisdiction-appropriate" in description (R01) | -2 |
| 12 | pm-marketing-growth/skills/positioning-ideas/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 13 | pm-marketing-growth/skills/north-star-metric/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 14 | pm-marketing-growth/skills/marketing-ideas/SKILL.md | No worked example of a generated idea (R06) | -5 |
| 15 | pm-marketing-growth/skills/marketing-ideas/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 16 | pm-marketing-growth/skills/value-prop-statements/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 17 | pm-marketing-growth/skills/product-name/SKILL.md | No worked example of a generated name (R06) | -5 |
| 18 | pm-marketing-growth/skills/product-name/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 19 | pm-marketing-growth/skills/product-name/SKILL.md | Unqualified "relevant" (R01) | -2 |
| 20 | pm-toolkit/skills/grammar-check/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 21 | pm-toolkit/skills/privacy-policy/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 22 | pm-toolkit/skills/review-resume/SKILL.md | Five unqualified uses of "relevant" (R01) | -10 |
| 23 | pm-toolkit/skills/review-resume/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 24 | pm-toolkit/skills/draft-nda/SKILL.md | No worked example of NDA clause language (R06) | -5 |
| 25 | pm-toolkit/skills/draft-nda/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 26 | pm-toolkit/skills/draft-nda/SKILL.md | Vague quantifiers "relevant", "some" (R01) | -4 |
| 27 | pm-data-analytics/commands/analyze-cohorts.md | No empty-input handling for zero data + zero description (R15) | -10 |
| 28 | pm-data-analytics/commands/analyze-cohorts.md | No error-path handling for malformed/unreadable data (R17) | -5 |
| 29 | pm-data-analytics/commands/write-query.md | No empty-input handling (R15) | -10 |
| 30 | pm-data-analytics/commands/write-query.md | No error-path handling for malformed schema uploads (R17) | -5 |
| 31 | pm-data-analytics/commands/write-query.md | Vague quantifier "reasonable" (R01) | -2 |
| 32 | pm-data-analytics/commands/analyze-test.md | No empty-input handling (R15) | -10 |
| 33 | pm-data-analytics/commands/analyze-test.md | Vague quantifier "sufficient" (R01) | -2 |
| 34 | pm-go-to-market/commands/plan-launch.md | No empty-input handling (R15) | -10 |
| 35 | pm-go-to-market/commands/plan-launch.md | No error-path handling for unreadable PRD/deck uploads (R17) | -5 |
| 36 | pm-go-to-market/commands/growth-strategy.md | No empty-input handling (R15) | -10 |
| 37 | pm-go-to-market/commands/growth-strategy.md | No error-path handling for bad metrics data (R17) | -5 |
| 38 | pm-go-to-market/commands/battlecard.md | No empty-input handling (R15) | -10 |
| 39 | pm-go-to-market/commands/battlecard.md | No error-path handling for missing competitor materials (R17) | -5 |
| 40 | pm-data-analytics/skills/sql-queries/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 41 | pm-data-analytics/skills/ab-test-analysis/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 42 | pm-data-analytics/skills/cohort-analysis/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 43 | pm-data-analytics/skills/cohort-analysis/SKILL.md | Vague quantifier "Sufficient" as a heading (R01) | -2 |
| 44 | pm-go-to-market/skills/gtm-motions/SKILL.md | Complex 7-motion-type framework with no worked examples (R06) | -5 |
| 45 | pm-go-to-market/skills/gtm-motions/SKILL.md | Missing scope note vs. growth-loops (R07) | -3 |
| 46 | pm-go-to-market/skills/competitive-battlecard/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 47 | pm-go-to-market/skills/beachhead-segment/SKILL.md | No worked example (R06) | -5 |
| 48 | pm-go-to-market/skills/beachhead-segment/SKILL.md | Missing scope note vs. ideal-customer-profile (R07) | -3 |
| 49 | pm-go-to-market/skills/ideal-customer-profile/SKILL.md | No worked example (R06) | -5 |
| 50 | pm-go-to-market/skills/ideal-customer-profile/SKILL.md | Missing scope note vs. beachhead-segment (R07) | -3 |
| 51 | pm-go-to-market/skills/growth-loops/SKILL.md | Missing scope note vs. gtm-motions (R07) | -3 |
| 52 | pm-go-to-market/skills/gtm-strategy/SKILL.md | No worked example (R06) | -5 |
| 53 | pm-go-to-market/skills/gtm-strategy/SKILL.md | Missing scope note (umbrella skill for 5 siblings) (R07) | -3 |
| 54 | pm-market-research/commands/competitive-analysis.md | No empty-input handling (R15) | -10 |
| 55 | pm-market-research/commands/competitive-analysis.md | No error-path handling for missing competitor data (R17) | -5 |
| 56 | pm-market-research/commands/competitive-analysis.md | Vague quantifier "relevant" (R01) | -2 |
| 57 | pm-market-research/commands/analyze-feedback.md | No empty-input handling (R15) | -10 |
| 58 | pm-ai-shipping/commands/document-app.md | No output format/template defined, unlike sibling commands (R16) | -10 |
| 59 | pm-ai-shipping/commands/document-app.md | Vague quantifier "relevant" ("permission-relevant journeys") (R01) | -2 |
| 60 | pm-ai-shipping/commands/performance-audit-static.md | No error-path handling for missing prerequisite input (R17) | -5 |
| 61 | pm-market-research/skills/market-segments/SKILL.md | No worked example (R06) | -5 |
| 62 | pm-market-research/skills/market-segments/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 63 | pm-market-research/skills/competitor-analysis/SKILL.md | No worked example (R06) | -5 |
| 64 | pm-market-research/skills/competitor-analysis/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 65 | pm-market-research/skills/market-sizing/SKILL.md | No worked TAM/SAM/SOM example (R06) | -5 |
| 66 | pm-market-research/skills/market-sizing/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 67 | pm-market-research/skills/market-sizing/SKILL.md | Vague quantifier "relevant" (R01) | -2 |
| 68 | pm-market-research/skills/customer-journey-map/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 69 | pm-market-research/skills/sentiment-analysis/SKILL.md | No worked example (R06) | -5 |
| 70 | pm-market-research/skills/sentiment-analysis/SKILL.md | Missing scope note vs. user-personas/user-segmentation overlap (R07) | -3 |
| 71 | pm-market-research/skills/user-personas/SKILL.md | No worked example (R06) | -5 |
| 72 | pm-market-research/skills/user-personas/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 73 | pm-market-research/skills/user-segmentation/SKILL.md | No worked example (R06) | -5 |
| 74 | pm-market-research/skills/user-segmentation/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 75 | pm-ai-shipping/skills/shipping-artifacts/SKILL.md | Description is 585 chars, in the 500-800 penalty band (R04) | -5 |
| 76 | pm-ai-shipping/skills/shipping-artifacts/SKILL.md | No reciprocal scope note to intended-vs-implemented (R07) | -3 |
| 77 | pm-product-strategy/commands/business-model.md | No error-path handling for incomplete/ambiguous input (R17) | -5 |
| 78 | pm-product-strategy/commands/business-model.md | Vague quantifier "relevant" (R01) | -2 |
| 79 | pm-product-strategy/commands/pricing.md | Vague quantifier "relevant" (R01) | -2 |
| 80 | pm-product-strategy/commands/market-scan.md | No error-path handling for missing/unreliable market data (R17) | -5 |
| 81 | pm-product-strategy/commands/value-proposition.md | No error-path handling for incomplete product context (R17) | -5 |
| 82 | pm-product-strategy/commands/strategy.md | No error-path handling for missing/contradictory strategy inputs (R17) | -5 |
| 83 | pm-product-strategy/commands/strategy.md | Vague quantifier "some" (R01) | -2 |
| 84 | pm-product-strategy/skills/monetization-strategy/SKILL.md | No scope note vs. sibling pricing-strategy skill (R07) | -3 |
| 85 | pm-product-strategy/skills/startup-canvas/SKILL.md | Description gives only 2 trigger phrases, not 3+ (R04) | -15 |
| 86 | pm-product-strategy/skills/startup-canvas/SKILL.md | No worked example of a completed canvas (R06) | -5 |
| 87 | pm-execution/commands/pre-mortem.md | No empty-input handling — no plan/PRD example (R15) | -10 |
| 88 | pm-execution/commands/pre-mortem.md | No error-path handling for thin plan detail (R17) | -5 |
| 89 | pm-execution/commands/generate-data.md | No error-path handling for ambiguous schema requests (R17) | -5 |
| 90 | pm-execution/commands/red-team-prd.md | No empty-input handling (R15) | -10 |
| 91 | pm-execution/commands/red-team-prd.md | No error-path handling for a plan too thin to red-team (R17) | -5 |
| 92 | pm-execution/commands/transform-roadmap.md | No empty-input handling (R15) | -10 |
| 93 | pm-execution/commands/transform-roadmap.md | No error-path handling for unparseable roadmap uploads (R17) | -5 |
| 94 | pm-execution/commands/test-scenarios.md | No empty-input handling (R15) | -10 |
| 95 | pm-execution/commands/test-scenarios.md | No error-path handling for ambiguous acceptance criteria (R17) | -5 |
| 96 | pm-execution/commands/test-scenarios.md | Vague quantifier "correctly" (R01) | -2 |
| 97 | pm-execution/commands/sprint.md | No error-path handling across the three modes (R17) | -5 |
| 98 | pm-execution/commands/write-stories.md | No error-path handling for missing feature input (R17) | -5 |
| 99 | pm-execution/commands/write-stories.md | Vague quantifier "relevant" (R01) | -2 |
| 100 | pm-execution/commands/stakeholder-map.md | No error-path handling for sparse stakeholder info (R17) | -5 |
| 101 | pm-execution/skills/user-stories/SKILL.md | Missing scope note vs. job-stories/wwas (R07) | -3 |
| 102 | pm-execution/skills/user-stories/SKILL.md | Vague quantifier "correctly" (R01) | -2 |
| 103 | pm-execution/skills/retro/SKILL.md | Missing scope note vs. sprint-plan (R07) | -3 |
| 104 | pm-execution/skills/test-scenarios/SKILL.md | Missing scope note vs. sibling skills (R07) | -3 |
| 105 | pm-execution/skills/test-scenarios/SKILL.md | Vague quantifier "correctly" (R01) | -2 |
| 106 | pm-execution/skills/create-prd/SKILL.md | No worked example of a filled PRD (R06) | -5 |
| 107 | pm-execution/skills/create-prd/SKILL.md | Vague quantifier "relevant" (R01) | -2 |
| 108 | pm-execution/skills/wwas/SKILL.md | Missing scope note vs. user-stories/job-stories (R07) | -3 |
| 109 | pm-execution/skills/wwas/SKILL.md | Vague quantifier "correctly" (R01) | -2 |
| 110 | pm-execution/skills/wwas/SKILL.md | Vague quantifier "appropriately" (R01) | -2 |
| 111 | pm-execution/skills/job-stories/SKILL.md | Missing scope note vs. user-stories/wwas (R07) | -3 |
| 112 | pm-execution/skills/job-stories/SKILL.md | Vague quantifier "properly" (R01) | -2 |
| 113 | pm-execution/skills/brainstorm-okrs/SKILL.md | Vague quantifier "some" (R01) | -2 |
| 114 | pm-execution/skills/summarize-meeting/SKILL.md | Vague quantifier "as needed" (R01) | -2 |
| 115 | pm-execution/skills/sprint-plan/SKILL.md | Missing scope note vs. retro (R07) | -3 |
| 116 | pm-execution/skills/sprint-plan/SKILL.md | Vague quantifier "appropriately" (R01) | -2 |
| 117 | pm-execution/skills/dummy-dataset/SKILL.md | Vague quantifier "business-appropriate" (R01) | -2 |
| 118 | pm-execution/skills/stakeholder-map/SKILL.md | Vague quantifier "relevant" (R01) | -2 |
| 119 | pm-execution/skills/pre-mortem/SKILL.md | Missing scope note vs. strategy-red-team (R07) | -3 |
| 120 | pm-execution/skills/pre-mortem/SKILL.md | Vague quantifier "relevant" (R01) | -2 |
| 121 | pm-execution/skills/strategy-red-team/SKILL.md | No worked example of the red-team methodology (R06) | -5 |
| 122 | pm-product-discovery/commands/triage-requests.md | No error-path handling for malformed uploads (R17) | -5 |
| 123 | pm-product-discovery/commands/brainstorm.md | No error-path handling for unreadable uploaded context (R17) | -5 |
| 124 | pm-product-discovery/commands/discover.md | No error-path handling for bad uploaded research (R17) | -5 |
| 125 | pm-product-discovery/skills/analyze-feature-requests/SKILL.md | Opportunity Score formula given with no worked example (R06) | -5 |
| 126 | pm-product-discovery/skills/brainstorm-ideas-existing/SKILL.md | No scope note vs. brainstorm-ideas-new (R07) | -3 |
| 127 | pm-product-discovery/skills/prioritize-assumptions/SKILL.md | ICE/RICE/Risk formulas given with no worked example (R06) | -5 |
| 128 | pm-product-discovery/skills/brainstorm-experiments-new/SKILL.md | No scope note vs. brainstorm-experiments-existing (R07) | -3 |
| 129 | pm-product-discovery/skills/opportunity-solution-tree/SKILL.md | No single end-to-end worked OST example (R06) | -5 |
| 130 | pm-product-discovery/skills/identify-assumptions-existing/SKILL.md | No scope note vs. identify-assumptions-new (R07) | -3 |
| 131 | pm-product-discovery/skills/prioritize-features/SKILL.md | Opportunity/ICE/RICE formulas given with no worked example (R06) | -5 |
| 132 | pm-product-discovery/skills/identify-assumptions-new/SKILL.md | No scope note vs. identify-assumptions-existing (R07) | -3 |
| 133 | pm-product-discovery/skills/brainstorm-experiments-existing/SKILL.md | No scope note vs. brainstorm-experiments-new (R07) | -3 |
| 134 | pm-product-discovery/skills/brainstorm-ideas-new/SKILL.md | No scope note vs. brainstorm-ideas-existing (R07) | -3 |

## Cross-Component

**1. `$ARGUMENTS` placeholder used in 54 of 58 audited skills, directly contradicting the repo's own CLAUDE.md.** The repo's `CLAUDE.md` states as a "Key Design Rule": *"Commands use a single `$ARGUMENTS` placeholder. Skills need no placeholders (they read context from the conversation)."* A repo-wide grep (`grep -rl '\$ARGUMENTS' */skills/**/SKILL.md`) found **54 of the repo's 68 SKILL.md files** (including 42 of the 58 audited in this pass) still contain a literal `$ARGUMENTS` placeholder — most commonly an `## Input Format` section reading `Use $ARGUMENTS to pass:` or a Context line like `You are analyzing A/B test results for **$ARGUMENTS**`. Since skills are auto-triggered by topic match (not invoked with positional arguments the way commands are), `$ARGUMENTS` in a skill body is very likely to render as a literal, unresolved string rather than being substituted — a real functional defect, not just a style nit. This is a single systemic contradiction between the project's own architecture doc and the majority of its skill files; representative affected files audited in this pass: `pm-data-analytics/skills/ab-test-analysis/SKILL.md`, `pm-go-to-market/skills/gtm-motions/SKILL.md`, `pm-go-to-market/skills/competitive-battlecard/SKILL.md`, `pm-go-to-market/skills/beachhead-segment/SKILL.md`, `pm-go-to-market/skills/ideal-customer-profile/SKILL.md`, `pm-go-to-market/skills/growth-loops/SKILL.md`, `pm-go-to-market/skills/gtm-strategy/SKILL.md`, `pm-marketing-growth/skills/{marketing-ideas,north-star-metric,positioning-ideas,product-name,value-prop-statements}/SKILL.md`, `pm-market-research/skills/{competitor-analysis,customer-journey-map,market-segments,market-sizing,sentiment-analysis,user-personas,user-segmentation}/SKILL.md`, `pm-execution/skills/{brainstorm-okrs,create-prd,outcome-roadmap,pre-mortem,release-notes,retro,sprint-plan,stakeholder-map,strategy-red-team,summarize-meeting}/SKILL.md`, `pm-product-discovery/skills/{analyze-feature-requests,brainstorm-experiments-existing,brainstorm-experiments-new,brainstorm-ideas-existing,brainstorm-ideas-new,identify-assumptions-existing,identify-assumptions-new,interview-script,metrics-dashboard,opportunity-solution-tree,prioritize-assumptions,prioritize-features,summarize-interview}/SKILL.md`, `pm-product-strategy/skills/{monetization-strategy,startup-canvas}/SKILL.md` (plus the 12 out-of-scope `pm-product-strategy` skills listed below). This is not scored against the numeric rubric supplied for this audit pass (no `$ARGUMENTS`-in-skill row exists in the given penalty tables) but is flagged here as the single highest-value, most reproducible fix available in the repo — a mechanical strip of the `## Input Format` / `Use $ARGUMENTS to pass` block from each affected SKILL.md.

**2. Out-of-scope artifacts.** This audit pass scored exactly the 100 files enumerated in the audit task (42/42 commands — full coverage — plus 58 of 68 SKILL.md files). `pm-product-strategy/skills/` has 12 SKILL.md files on disk; only `monetization-strategy` and `startup-canvas` were in scope for this pass. The 10 not scored — `ansoff-matrix`, `business-model`, `lean-canvas`, `pestle-analysis`, `porters-five-forces`, `pricing-strategy`, `product-strategy`, `product-vision`, `swot-analysis`, `value-proposition` — are real, non-orphaned artifacts (all five `pm-product-strategy` commands reference them, and the repo's own `tests/test_consistency.py` / `validate_plugins.py` count them). They are not orphaned or broken; they were simply outside this audit's given file list and should be picked up in a follow-up pass.

**3. No broken references found.** Every command's implicit skill/file references were checked against what agents observed while reading; no dangling cross-references, no stale counts, and no contradicting instructions were found beyond the `$ARGUMENTS` issue above. The repo ships its own consistency gate (`tests/test_consistency.py`, run in CI) that independently enforces README/marketplace/plugin.json count sync and `/plugin:command` reference validity — a strong existing safety net this audit did not need to duplicate.

## Recommendation

**CLEAR — submit PRs for all bugs and medium/low security fixes.**

Security is clean (0 findings across all three execution surfaces). The 38 missing-`allowed-tools` bugs are each a mechanical, low-risk, one-line frontmatter addition and are safe to batch into PRs. The `$ARGUMENTS`-in-skills cross-component finding (54 files) is higher-value but slightly more judgment-dependent (removing vs. rewording the Input Format section) — worth a dedicated PR grouped by plugin rather than folding into the allowed-tools fix. Quality issues (134, mostly -2/-3/-5 vague-quantifier, missing-scope-note, and missing-worked-example findings) are informational and appropriate for a follow-up low-priority PR or left for the maintainer's own backlog.
