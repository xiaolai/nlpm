# NLPM Audit: NicholasSpisak/claude-code-subagents
**Date**: 2026-04-06  |  **Artifacts**: 79  |  **Strategy**: progressive
**NL Score**: 77/100
**Security**: CLEAR
**Bugs**: 19  |  **Quality Issues**: 289  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/marketing/reddit-community-builder.md | Agent | 3 | Missing frontmatter + 6 vague "relevant" |
| agents/marketing/twitter-engager.md | Agent | 11 | Missing frontmatter (no name/description) |
| agents/marketing/content-creator.md | Agent | 13 | Missing frontmatter (no name/description) |
| agents/marketing/growth-hacker.md | Agent | 15 | Missing frontmatter (no name/description) |
| agents/marketing/instagram-curator.md | Agent | 15 | Missing frontmatter (no name/description) |
| agents/core/code-refactoring-expert.md | Agent | 69 | Zero example blocks |
| agents/marketing/tiktok-strategist.md | Agent | 69 | 4 declared tools unused in body |
| agents/core/performance-optimizer.md | Agent | 73 | Zero example blocks |
| agents/core/qa-test-engineer.md | Agent | 73 | Zero example blocks |
| agents/design/whimsy-injector.md | Agent | 72 | No output format specified |
| agents/operations/infrastructure-maintainer.md | Agent | 74 | No output format specified |
| agents/ai-automation-specialists/ml-engineer-aa.md | Agent | 75 | Missing model/tools fields |
| agents/ai-automation-specialists/integration-specialist-aa.md | Agent | 75 | Missing model/tools fields |
| agents/ai-automation-specialists/ai-workflow-designer-aa.md | Agent | 75 | Missing model/tools fields |
| agents/ai-automation-specialists/workflow-analyst-aa.md | Agent | 75 | Missing model/tools fields |
| agents/ai-automation-specialists/automation-architect-aa.md | Agent | 75 | Missing model/tools fields |
| agents/growth-revenue-operations/retention-specialist-gr.md | Agent | 75 | Missing model/tools fields |
| agents/growth-revenue-operations/customer-acquisition-gr.md | Agent | 75 | Missing model/tools fields |
| agents/growth-revenue-operations/operations-optimizer-gr.md | Agent | 75 | Missing model/tools fields |
| agents/growth-revenue-operations/partnership-strategist-gr.md | Agent | 75 | Missing model/tools fields |
| agents/growth-revenue-operations/sales-engineer-gr.md | Agent | 75 | Missing model/tools fields |
| agents/growth-revenue-operations/revenue-analyst-gr.md | Agent | 75 | Missing model/tools fields |
| agents/finance-strategy/compliance-officer-fs.md | Agent | 75 | No output format specified |
| agents/finance-strategy/investment-analyst-fs.md | Agent | 75 | No output format specified |
| agents/finance-strategy/business-strategist-fs.md | Agent | 75 | No output format specified |
| agents/finance-strategy/cost-optimizer-fs.md | Agent | 75 | No output format specified |
| agents/finance-strategy/pricing-strategist-fs.md | Agent | 75 | No output format specified |
| CLAUDE.md | Memory | 75 | Stale references (nonexistent logs/, outdated agent count) |
| agents/core/backend-reliability-engineer.md | Agent | 76 | No output format specified |
| agents/ai-automation-specialists/prompt-engineer-aa.md | Agent | 76 | Missing model/tools + vague words |
| agents/core/product-manager-orchestrator.md | Agent | 78 | No output format specified |
| agents/operations/support-responder.md | Agent | 78 | Vague quantifiers x4 |
| agents/marketing/app-store-optimizer.md | Agent | 78 | 5 declared tools unused in body |
| agents/account-team-agents/customer-support-at.md | Agent | 78 | No output format specified |
| agents/finance-strategy/financial-analyst-fs.md | Agent | 78 | No output format specified |
| agents/market-research-agents/competitive-intelligence-mx.md | Agent | 78 | No output format + malformed frontmatter |
| agents/specialized-agents/ui-ux-analyst.md | Agent | 80 | No output format specified |
| agents/core/senior-software-engineer.md | Agent | 80 | No output format specified |
| agents/product/trend-researcher.md | Agent | 80 | 5 declared tools unused in body |
| agents/product/feedback-synthesizer.md | Agent | 80 | 5 declared tools unused in body |
| agents/account-team-agents/managed-services-engineer.md | Agent | 80 | No output format specified |
| agents/account-team-agents/customer-success-manager.md | Agent | 80 | No output format specified |
| agents/growth-revenue-operations/growth-hacker-gr.md | Agent | 80 | Missing model/tools fields |
| commands/workflow.md | Command | 81 | No empty-input handling; undeclared MCP tools |
| agents/testing/test-results-analyzer.md | Agent | 82 | MultiEdit declared on a read-only analysis role |
| agents/core/gpt-5.md | Agent | 83 | No output format; undeclared bash tool usage |
| agents/product/sprint-prioritizer.md | Agent | 83 | 4 declared tools unused in body |
| agents/design/visual-storyteller.md | Agent | 84 | model not declared |
| agents/design/ux-researcher.md | Agent | 84 | model not declared |
| agents/finance-strategy/risk-assessor-fs.md | Agent | 85 | Only one example block |
| agents/market-research-agents/reddit-intelligence-mx.md | Agent | 86 | model+tools undeclared; malformed frontmatter |
| agents/project-management/studio-producer.md | Agent | 86 | 3 unused declared tools |
| agents/project-management/project-shipper.md | Agent | 86 | 3 unused declared tools |
| agents/core/technical-mentor-guide.md | Agent | 86 | Missing tools + model |
| agents/account-team-agents/account-executive-revenue.md | Agent | 86 | Missing model + tools fields |
| agents/design/ui-designer.md | Agent | 87 | model not declared |
| agents/design/brand-guardian.md | Agent | 87 | model not declared |
| agents/operations/legal-compliance-checker.md | Agent | 87 | model not declared |
| agents/testing/api-tester.md | Agent | 87 | model not declared |
| agents/market-research-agents/experience-analyzer-mx.md | Agent | 88 | model+tools undeclared; malformed frontmatter |
| agents/core/security-threat-analyst.md | Agent | 88 | model/tools not declared |
| agents/specialized-agents/product-requirements-generator.md | Agent | 88 | Missing tools and model fields |
| agents/project-management/experiment-tracker.md | Agent | 89 | Vague quantifiers x3 |
| agents/operations/analytics-reporter.md | Agent | 89 | model not declared |
| agents/operations/finance-tracker.md | Agent | 89 | model not declared |
| agents/testing/performance-benchmarker.md | Agent | 89 | model not declared |
| agents/specialized-agents/content-marketer-writer.md | Agent | 90 | Undeclared tool usage; duplicate agent name |
| agents/specialized-agents/market-research-analyst.md | Agent | 90 | Undeclared tool usage |
| agents/core/content-marketer-writer.md | Agent | 90 | Undeclared tool usage; duplicate agent name |
| agents/core/frontend-ux-specialist.md | Agent | 90 | Missing tools + model |
| agents/core/code-analyzer-debugger.md | Agent | 90 | Missing tools + model |
| agents/core/prd-writer.md | Agent | 90 | Missing tools + model |
| agents/core/systems-architect.md | Agent | 90 | Undeclared tool usage |
| agents/core/deep-research-specialist.md | Agent | 90 | Missing tools + model |
| agents/account-team-agents/product-engineer-at.md | Agent | 90 | Missing model + tools fields |
| agents/market-research-agents/business-model-analyzer-mx.md | Agent | 90 | model+tools undeclared; malformed frontmatter |
| agents/market-research-agents/tam-market-sizing-mx.md | Agent | 90 | model+tools undeclared; malformed frontmatter |
| agents/testing/tool-evaluator.md | Agent | 93 | model not declared |
| agents/testing/workflow-optimizer.md | Agent | 95 | model not declared |

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
| Hooks (`hooks/**`) | None found |
| Scripts (`scripts/**/*.{sh,py,js}`) | None found |
| MCP configs (`.mcp.json`) | None found |
| package.json | None found |
| requirements.txt | None found |

This repository contains only Markdown agent definitions, one command file, one CLAUDE.md, a README/PRD, and a static image asset. There is no executable surface of any kind (no hooks, no scripts, no MCP server config, no package manifest, no dependency lockfiles). `commands/workflow.md` declares `Bash(*)` in `allowed-tools` but the command itself is a natural-language orchestration prompt, not a script — its only notable issue is referencing MCP tool names (`--seq`, `--serena`, `--c7`) that aren't declared anywhere, which is captured as an NL bug below, not a security finding.

### Security Findings
No security findings.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | agents/marketing/growth-hacker.md | Entire file has no YAML frontmatter — no `name`/`description` fields at all | Agent will not register in Claude Code's subagent list |
| 2 | agents/marketing/twitter-engager.md | Entire file has no YAML frontmatter | Agent will not register |
| 3 | agents/marketing/content-creator.md | Entire file has no YAML frontmatter | Agent will not register |
| 4 | agents/marketing/instagram-curator.md | Entire file has no YAML frontmatter | Agent will not register |
| 5 | agents/marketing/reddit-community-builder.md | Entire file has no YAML frontmatter | Agent will not register |
| 6 | agents/specialized-agents/content-marketer-writer.md | Body says "Use all available tools including web search and MCP servers for thorough research" (line 15) but no `tools` field is declared in frontmatter | Undeclared-tool usage; agent's own instructions assume capabilities it was never granted |
| 7 | agents/core/content-marketer-writer.md | Same undeclared-tool-usage pattern, identical line 15 wording | Same as above |
| 8 | agents/specialized-agents/market-research-analyst.md | Body instructs "Conduct systematic web searches using multiple query strategies" (line 12) and "Use varied search terms" (line 33) with no `tools` field declared | Undeclared-tool usage |
| 9 | agents/core/systems-architect.md | Body says "Research proven patterns (using web search if needed)" (line 113) with no `tools` field declared | Undeclared-tool usage |
| 10 | agents/core/deep-research-specialist.md | Body describes multi-source research collection with no `tools` field declared | Undeclared-tool usage (medium confidence — less explicit than #8/#9) |
| 11 | agents/core/gpt-5.md | Body includes a literal bash invocation example (`cursor-agent -p "..."`) with no `tools` field declared anywhere in frontmatter | Undeclared-tool usage |
| 12 | agents/market-research-agents/experience-analyzer-mx.md | Frontmatter block contains a bare, non-`key: value` sentence ("This agent is launched every time the user append MX to the request...") between `description:` and `color:` | Malformed YAML frontmatter likely to fail strict parsing |
| 13 | agents/market-research-agents/competitive-intelligence-mx.md | Same malformed-frontmatter sentence | Same |
| 14 | agents/market-research-agents/reddit-intelligence-mx.md | Same malformed-frontmatter sentence | Same |
| 15 | agents/market-research-agents/business-model-analyzer-mx.md | Same malformed-frontmatter sentence | Same |
| 16 | agents/market-research-agents/tam-market-sizing-mx.md | Same malformed-frontmatter sentence | Same |
| 17 | commands/workflow.md | References MCP tools (Sequential Thinking `--seq`, Serena `--serena`, context7 `--c7`) throughout the body (lines 27-53, 355-384) that are never declared in `allowed-tools` (line 2 only lists `Bash(*), Task, web_search, web_fetch, google_drive_search, google_drive_fetch, repl, artifacts`) | Command instructs behavior for tools it may never actually have access to |
| 18 | CLAUDE.md | Line 13 references a `logs/` directory ("Claude Code session logs and tool usage tracking") that does not exist anywhere in the repository | Stale reference — misleads anyone using CLAUDE.md as ground truth |
| 19 | CLAUDE.md | Architecture section (lines 12, 19-29) describes only 9 flat agents; the repo actually has 77 agent files across 13 category subdirectories, and never mentions `commands/`, `PRD.md`, `README.md`, or `assets/` | Severely outdated architecture overview |

## Security Fixes (PR-worthy, Medium/Low only)
No security findings — nothing to fix.

## Quality Issues (informational)
| # | File(s) | Issue | Penalty |
|---|------|-------|---------|
| 1 | 76 of 77 agent files (all except agents/core/gpt-5.md) | `model` field not declared in frontmatter | -5 each |
| 2 | 54 of 77 agent files | `tools` field not declared in frontmatter | -5 each |
| 3 | 36 of 77 agent files | No output format / deliverable structure specified anywhere in body | -10 each |
| 4 | 17 files (5× finance-strategy, 1× risk-assessor-fs, 5× ai-automation-specialists, 6× growth-revenue-operations) | Exactly one `<example>` block in description | -5 each |
| 5 | 8 files (3× agents/core/{code-refactoring-expert,performance-optimizer,qa-test-engineer}, 5× agents/marketing/{growth-hacker,twitter-engager,content-creator,instagram-curator,reddit-community-builder}) | Zero `<example>` blocks | -15 each |
| 6 | ~20 files with a declared `tools:` list (project-management, design, operations, marketing, product, testing) | Declared tools never referenced/exercised anywhere in body (~59 individual tool instances) | -3 each |
| 7 | 33 files across all categories | Vague quantifiers ("appropriate", "relevant", "properly", "various", etc.) used without measurable criteria | -2 each, capped -20/file |
| 8 | agents/testing/test-results-analyzer.md | `MultiEdit` (an Edit-family tool) declared on an agent whose entire role is read-only analysis/reporting | -10 |
| 9 | commands/workflow.md | No `argument-hint`; no explicit handling for the empty/no-argument case | -5, -10 |
| 10 | CLAUDE.md | No test-run instructions; >60% descriptive rather than instructive; no prerequisites/setup section | -5, -5, -5 |

*(289 total individual quality-issue instances across 79 files; grouped above by pattern for readability. Per-file breakdowns were computed by the scoring passes and are reflected in each file's score above.)*

## Cross-Component
- **Duplicate agent name collision**: `agents/core/content-marketer-writer.md` and `agents/specialized-agents/content-marketer-writer.md` both declare `name: content-marketer-writer` in frontmatter. Two independently-authored agents share one registration name — whichever loads second will collide with or shadow the other. Verified directly (both files' frontmatter read side-by-side).
- **Manifest-vs-disk diff**: `README.md`'s "🏗️ Core Technical Excellence (14 agents)" section (lines 37-52) lists exactly 14 agents, but `agents/core/` contains 15 files on disk — `agents/core/gpt-5.md` is not mentioned anywhere in that section. Deterministic, high-confidence (bullet count vs. `ls` count).
- **Systemic template gap**: 76 of 77 agent files never declare a `model:` tier — this reads as a repo-wide authoring convention/gap rather than 76 independent oversights, and would be best fixed with one template update plus a bulk edit rather than 76 separate PRs.
- **Systemic template duplication**: the `finance-strategy/`, `ai-automation-specialists/`, and `growth-revenue-operations/` directories (20 files total) share a near-identical boilerplate structure (frontmatter shape, single `<example>` block, "DELIVERABLE STANDARDS" bullet section, no `tools`/`model`/output-format) — consistent with being generated from one shared template rather than authored independently per agent.
- **Systemic template anomaly**: the 5 `market-research-agents/*-mx.md` files share an identical malformed frontmatter line (see Bugs #12-16) — also a single-template defect, not 5 independent bugs.
- No orphaned agent/command files were found relative to README's category listing (all 77 agent files map onto one of the 13 documented categories), aside from the `gpt-5.md` omission noted above.

## Recommendation
**CLEAR — submit PRs for all bugs and medium/low security fixes.** There are no security findings of any severity (no execution surface exists in this repository at all), so nothing is security-blocked. Prioritize the 5 missing-frontmatter agents in `agents/marketing/` (bugs #1-5) — these likely fail to register at all and are the highest-impact, lowest-risk fixes — followed by the duplicate-name collision and the 5 malformed `*-mx.md` frontmatter files. The systemic `model`/`tools`/output-format gaps are better addressed as a small number of template-level PRs (one per affected directory) rather than dozens of near-identical single-file PRs.
