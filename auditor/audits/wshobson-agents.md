---
repo: wshobson/agents
stars: 33000
audited: 2026-04-17
nl_score: 76
security: PASS
recommendation: contribute
---

# Audit: wshobson/agents

**Repo:** https://github.com/wshobson/agents  
**Stars:** ~33K  
**Audited:** 2026-04-17  
**Artifacts:** 64 agents, 36 commands (100 total)  
**Overall NL Score:** 76/100 — Agent avg: 82/100 · Command avg: 65/100

---

## NL Score Summary

### Agents

| Artifact | Score | Top Penalties |
|---|---|---|
| conductor/agents/conductor-validator | 93 | — |
| agent-teams/agents/team-debugger | 93 | — |
| agent-teams/agents/team-reviewer | 92 | — |
| agent-teams/agents/team-implementer | 91 | — |
| database-design/agents/database-architect | 90 | — |
| dotnet-contribution/agents/dotnet-architect | 90 | — |
| reverse-engineering/agents/malware-analyst | 90 | — |
| reverse-engineering/agents/firmware-analyst | 90 | — |
| reverse-engineering/agents/reverse-engineer | 90 | — |
| c4-architecture/agents/c4-context | 89 | — |
| c4-architecture/agents/c4-container | 89 | — |
| c4-architecture/agents/c4-component | 89 | — |
| c4-architecture/agents/c4-code | 88 | — |
| comprehensive-review/agents/security-auditor | 88 | — |
| comprehensive-review/agents/code-reviewer | 88 | — |
| security-scanning/agents/security-auditor | 88 | DUPLICATE of comprehensive-review/security-auditor |
| code-documentation/agents/code-reviewer | 88 | DUPLICATE of comprehensive-review/code-reviewer |
| comprehensive-review/agents/architect-review | 87 | — |
| ui-design/agents/accessibility-expert | 87 | — |
| ui-design/agents/ui-designer | 87 | — |
| jvm-languages/agents/java-pro | 87 | — |
| python-development/agents/python-pro | 87 | — |
| python-development/agents/fastapi-pro | 87 | — |
| python-development/agents/django-pro | 87 | — |
| game-development/agents/unity-developer | 87 | — |
| llm-application-dev/agents/prompt-engineer | 86 | — |
| performance-testing-review/agents/test-automator | 86 | — |
| llm-application-dev/agents/ai-engineer | 84 | no output format (-10), no empty input handling (-5) |
| agent-teams/agents/team-lead | 84 | no example tasks section (-10) |
| distributed-debugging/agents/devops-troubleshooter | 84 | — |
| llm-application-dev/agents/vector-database-engineer | 83 | — |
| deployment-validation/agents/cloud-architect | 83 | no output format (-10) |
| seo-analysis-monitoring/agents/seo-content-refresher | 83 | — |
| seo-analysis-monitoring/agents/seo-cannibalization-detector | 82 | — |
| seo-analysis-monitoring/agents/seo-authority-builder | 82 | — |
| startup-business-analyst/agents/startup-analyst | 82 | — |
| data-validation-suite/agents/backend-security-coder | 85 | — |
| frontend-mobile-development/agents/frontend-developer | 85 | — |
| frontend-mobile-development/agents/mobile-developer | 85 | — |
| customer-sales-automation/agents/customer-support | 85 | — |
| arm-cortex-microcontrollers/agents/arm-cortex-expert | 85 | — |
| performance-testing-review/agents/performance-engineer | 85 | — |
| observability-monitoring/agents/database-optimizer | 85 | — |
| observability-monitoring/agents/observability-engineer | 85 | — |
| observability-monitoring/agents/performance-engineer | 85 | DUPLICATE of performance-testing-review/performance-engineer |
| observability-monitoring/agents/network-engineer | 85 | — |
| database-design/agents/sql-pro | 85 | — |
| ui-design/agents/design-system-architect | 85 | — |
| debugging-toolkit/agents/dx-optimizer | 79 | no examples (-15) |
| debugging-toolkit/agents/debugger | 77 | no examples (-15) |
| code-documentation/agents/tutorial-engineer | 77 | no examples (-15) |
| code-documentation/agents/docs-architect | 76 | no examples (-15) |
| game-development/agents/minecraft-bukkit-pro | 75 | no examples section (-15) |
| customer-sales-automation/agents/sales-automator | 74 | no examples (-15) |
| functional-programming/agents/elixir-pro | 73 | no examples (-15) |
| functional-programming/agents/haskell-pro | 73 | no examples (-15) |
| jvm-languages/agents/csharp-pro | 73 | no examples (-15) |
| jvm-languages/agents/scala-pro | 73 | no examples (-15) |
| dependency-management/agents/legacy-modernizer | 73 | no examples (-15) |
| distributed-debugging/agents/error-detective | 72 | no examples (-15), very sparse content |
| meigen-ai-design/agents/image-generator | 58 | missing `name` field (-25) |
| meigen-ai-design/agents/gallery-researcher | 53 | missing `name` field (-25) |
| meigen-ai-design/agents/prompt-crafter | 50 | missing `name` field (-25), no examples (-15) |
| security-scanning/agents/threat-modeling-expert | 50 | NO YAML frontmatter at all (-50) |

### Commands

| Artifact | Score | Top Penalties |
|---|---|---|
| startup-business-analyst/commands/business-case | 90 | no argument-hint (-3) |
| startup-business-analyst/commands/financial-projections | 90 | no argument-hint (-3) |
| startup-business-analyst/commands/market-opportunity | 90 | no argument-hint (-3) |
| block-no-verify/commands/block-no-verify | 87 | no allowed-tools (-5) |
| tdd-workflows/commands/tdd-red | 87 | no allowed-tools (-5) |
| tdd-workflows/commands/tdd-green | 87 | no allowed-tools (-5) |
| full-stack-orchestration/commands/full-stack-feature | 85 | no allowed-tools (-5), cross-plugin refs |
| conductor/commands/manage | 83 | no allowed-tools (-5) |
| conductor/commands/new-track | 83 | no allowed-tools (-5) |
| conductor/commands/setup | 83 | no allowed-tools (-5) |
| conductor/commands/revert | 83 | no allowed-tools (-5) |
| conductor/commands/implement | 83 | no allowed-tools (-5) |
| conductor/commands/status | 83 | no allowed-tools (-5) |
| framework-migration/commands/legacy-modernize | 83 | no allowed-tools (-5) |
| database-migrations/commands/sql-migrations | 83 | non-standard `tool_access` field, no argument-hint |
| database-migrations/commands/migration-observability | 83 | non-standard `tool_access` field, no argument-hint |
| tdd-workflows/commands/tdd-cycle | 82 | no allowed-tools (-5), cross-plugin ref (code-reviewer) |
| application-performance/commands/performance-optimization | 82 | no allowed-tools (-5), cross-plugin refs |
| llm-application-dev/commands/ai-assistant | 77 | no allowed-tools (-5), no empty input handling (-10) |
| llm-application-dev/commands/prompt-optimize | 77 | no allowed-tools (-5), no empty input handling (-10) |
| llm-application-dev/commands/langchain-agent | 77 | no allowed-tools (-5), no empty input handling (-10) |
| deployment-validation/commands/config-validate | 50 | NO YAML frontmatter (-25) |
| c4-architecture/commands/c4-architecture | 50 | NO YAML frontmatter (-25) |
| systems-programming/commands/rust-project | 50 | NO YAML frontmatter (-25) |
| framework-migration/commands/code-migrate | 50 | NO YAML frontmatter (-25) |
| framework-migration/commands/deps-upgrade | 50 | NO YAML frontmatter (-25) |
| accessibility-compliance/commands/accessibility-audit | 50 | NO YAML frontmatter (-25) |
| codebase-cleanup/commands/tech-debt | 50 | NO YAML frontmatter (-25) |
| codebase-cleanup/commands/deps-audit | 50 | NO YAML frontmatter (-25) |
| codebase-cleanup/commands/refactor-clean | 50 | NO YAML frontmatter (-25) |
| database-cloud-optimization/commands/cost-optimize | 50 | NO YAML frontmatter (-25) |
| javascript-typescript/commands/typescript-scaffold | 50 | NO YAML frontmatter (-25) |
| tdd-workflows/commands/tdd-refactor | 50 | NO YAML frontmatter (-25), ghost subagent_type ref |
| error-diagnostics/commands/error-trace | 50 | NO YAML frontmatter (-25) |
| error-diagnostics/commands/error-analysis | 50 | NO YAML frontmatter (-25) |
| error-diagnostics/commands/smart-debug | 50 | NO YAML frontmatter (-25), cross-plugin ref |

---

## Security Scan

**Result: PASS — No CRITICAL or HIGH findings.**

### Executable Surface Inventory

| Surface | Files Found |
|---|---|
| hooks/** | None |
| scripts/**/*.{sh,py,js} | None |
| .mcp.json | None |
| package.json | None |
| requirements.txt | tools/requirements.txt |
| Other executables | tools/yt-design-extractor.py |

### Findings

| Severity | File | Finding |
|---|---|---|
| MEDIUM | tools/yt-design-extractor.py | Makes network calls to YouTube via yt-dlp and youtube-transcript-api (intended behavior — no shell injection risk; subprocess.run uses list form throughout) |
| LOW | tools/requirements.txt | Dependencies use `>=` minimum-version pinning rather than exact pins. Allows unexpected version upgrades: `yt-dlp>=2024.0.0`, `Pillow>=10.0.0`, `pytesseract>=0.3.10`, `colorthief>=0.2.1`, `youtube-transcript-api>=0.6.0` |

**No CRITICAL patterns detected:** no curl|bash pipelines, no eval+vars, no reverse shells, no base64+exec, no credential exfiltration, no subprocess shell=True, no os.system, no sudo, no PATH modifications, no postinstall scripts, no writes outside repo.

---

## Bugs

Issues that prevent correct registration or runtime behavior.

| ID | File | Issue | Fix |
|---|---|---|---|
| B01 | meigen-ai-design/agents/prompt-crafter.md | Missing required `name` frontmatter field — agent cannot register | Add `name: prompt-crafter` to YAML frontmatter |
| B02 | meigen-ai-design/agents/gallery-researcher.md | Missing required `name` frontmatter field | Add `name: gallery-researcher` to YAML frontmatter |
| B03 | meigen-ai-design/agents/image-generator.md | Missing required `name` frontmatter field | Add `name: image-generator` to YAML frontmatter |
| B04 | security-scanning/agents/threat-modeling-expert.md | NO YAML frontmatter block at all — file starts directly with `# Threat Modeling Expert`. Agent cannot register. | Wrap top of file with `---\nname: threat-modeling-expert\ndescription: ...\nmodel: opus\n---` |
| B05 | deployment-validation/commands/config-validate.md | Missing YAML frontmatter — command cannot be discovered or invoked | Add `---\ndescription: ...\n---` block |
| B06 | c4-architecture/commands/c4-architecture.md | Missing YAML frontmatter | Add frontmatter block |
| B07 | systems-programming/commands/rust-project.md | Missing YAML frontmatter | Add frontmatter block |
| B08 | framework-migration/commands/code-migrate.md | Missing YAML frontmatter | Add frontmatter block |
| B09 | framework-migration/commands/deps-upgrade.md | Missing YAML frontmatter | Add frontmatter block |
| B10 | accessibility-compliance/commands/accessibility-audit.md | Missing YAML frontmatter | Add frontmatter block |
| B11 | codebase-cleanup/commands/tech-debt.md | Missing YAML frontmatter | Add frontmatter block |
| B12 | codebase-cleanup/commands/deps-audit.md | Missing YAML frontmatter | Add frontmatter block |
| B13 | codebase-cleanup/commands/refactor-clean.md | Missing YAML frontmatter | Add frontmatter block |
| B14 | database-cloud-optimization/commands/cost-optimize.md | Missing YAML frontmatter | Add frontmatter block |
| B15 | javascript-typescript/commands/typescript-scaffold.md | Missing YAML frontmatter | Add frontmatter block |
| B16 | tdd-workflows/commands/tdd-refactor.md | Missing YAML frontmatter AND references `subagent_type: "tdd-orchestrator"` which does not exist anywhere in the repo — will fail at runtime | Add frontmatter; replace `tdd-orchestrator` with `general-purpose` or create the missing agent |
| B17 | error-diagnostics/commands/error-trace.md | Missing YAML frontmatter | Add frontmatter block |
| B18 | error-diagnostics/commands/error-analysis.md | Missing YAML frontmatter | Add frontmatter block |
| B19 | error-diagnostics/commands/smart-debug.md | Missing YAML frontmatter | Add frontmatter block |

---

## Security Fixes

No security fixes required. All security findings are informational (MEDIUM/LOW).

---

## Quality Issues

Non-blocking improvements that raise scores from the 72–87 range.

| ID | Files | Issue | Recommended Fix |
|---|---|---|---|
| Q01 | All conductor/commands/*.md, tdd-workflows/commands/tdd-*.md, framework-migration/commands/legacy-modernize.md, application-performance/commands/*.md (17 commands) | Missing `allowed-tools` frontmatter field — loses -5 each | Add `allowed-tools: Read, Glob, Grep, Bash` (or appropriate tool set) to each command |
| Q02 | database-migrations/commands/sql-migrations.md, database-migrations/commands/migration-observability.md | Use non-standard `tool_access` field instead of `allowed-tools` — will not be parsed by NLPM | Rename field to `allowed-tools` |
| Q03 | llm-application-dev/commands/ai-assistant.md, prompt-optimize.md, langchain-agent.md | No empty input handling — commands will execute without arguments with no guidance | Add `if [ -z "$ARGUMENTS" ]` guard block or equivalent |
| Q04 | elixir-pro, haskell-pro, csharp-pro, scala-pro, legacy-modernizer, sales-automator, minecraft-bukkit-pro, docs-architect, tutorial-engineer, debugger, dx-optimizer, error-detective (12 agents) | Zero or near-zero example interactions (-15 each) | Add a `## Example Interactions` section with 5+ realistic bullet examples |
| Q05 | llm-application-dev/agents/ai-engineer.md, deployment-validation/agents/cloud-architect.md | Missing explicit output format section (-10 each) | Add `## Output Format` section describing structure of agent's response |
| Q06 | startup-business-analyst/commands/business-case.md, financial-projections.md, market-opportunity.md | Missing `argument-hint` frontmatter field | Add `argument-hint: <description>` |
| Q07 | Most agents with `model: inherit` | Correct per tier-2 convention, but agents doing code review/security work (e.g., startup-analyst, accessibility-expert, ui-designer, design-system-architect) should consider `model: opus` for Tier 1 quality | Audit model tier appropriateness per CLAUDE.md model tier table |

---

## Cross-Component Issues

### Duplicate Agents (Exact Content)

These agent files appear in multiple plugins with identical or near-identical content. Violates DRY — changes must be made in multiple places, and the secondary copy adds no value.

| Secondary (duplicate) | Primary (canonical) | Action |
|---|---|---|
| security-scanning/agents/security-auditor.md | comprehensive-review/agents/security-auditor.md | Delete secondary or make it a thin wrapper that references the primary plugin |
| code-documentation/agents/code-reviewer.md | comprehensive-review/agents/code-reviewer.md | Delete secondary |
| observability-monitoring/agents/performance-engineer.md | performance-testing-review/agents/performance-engineer.md | Delete secondary |

### Ghost Agent Reference

`tdd-workflows/commands/tdd-refactor.md` references `subagent_type: "tdd-orchestrator"` — this agent does not exist in any plugin in the repo. The command will throw a runtime error when invoked.

### Cross-Plugin Subagent References (Behavioral Rule Violation)

Several commands declare "no cross-plugin dependencies" in their own behavioral rules but then reference agents from other plugins via `subagent_type`. These references will fail if the foreign plugin is not installed.

| Command | Foreign Agent Referenced | Home Plugin |
|---|---|---|
| full-stack-orchestration/commands/full-stack-feature.md | test-automator, security-auditor, performance-engineer, deployment-engineer | various plugins |
| tdd-workflows/commands/tdd-cycle.md | code-reviewer | comprehensive-review |
| application-performance/commands/performance-optimization.md | performance-engineer, observability-engineer, frontend-developer | various plugins |
| error-diagnostics/commands/smart-debug.md | debugger | debugging-toolkit |

**Fix:** Either bundle required agents inside the plugin directory, or remove the "no cross-plugin dependencies" rule, or replace cross-plugin `subagent_type` values with `general-purpose`.

### Naming Inconsistency

- `database-migrations/commands/` uses `tool_access` (non-standard) while all other plugins use `allowed-tools`. Suggests these commands were authored against a different or draft spec.

---

## Recommendation

**Overall Assessment:** This is a high-quality, large-scale agent collection with strong agent definitions averaging 82/100. The content quality is genuinely good — clear descriptions, structured response approaches, rich capability sections. The primary weakness is the command layer, which averages only 65/100 due to 15 commands missing YAML frontmatter entirely.

**Ship-blockers (must fix before contribution PR):**

1. **Add YAML frontmatter to all 15 bare commands** (B05–B19). Every command file in the repo that currently starts with `# Title` instead of `---\ndescription:...\n---` will fail to register. This is a mechanical batch fix — add the `---` block, extract the title as `description`, and optionally add `argument-hint`.

2. **Fix the 4 agents with missing/absent frontmatter** (B01–B04). Three `meigen-ai-design` agents need `name:` added; `threat-modeling-expert` needs a complete frontmatter block created from scratch.

3. **Remove or replace the ghost `tdd-orchestrator` reference** in `tdd-workflows/commands/tdd-refactor.md` (B16). The command is currently broken at runtime.

**High-value quality improvements (post-ship):**

1. Add `## Example Interactions` sections to the 12 agents currently scoring 72–79 — this single fix is worth +15 points per file and brings them all above the 85 threshold.

2. Add `allowed-tools:` to the 17 commands missing it (+5 each) and rename `tool_access` to `allowed-tools` in the 2 database-migrations commands.

3. Delete the 3 duplicate agent files — they create a maintenance liability and inflate the artifact count without adding capability.
