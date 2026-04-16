# NLPM Audit: zebbern/claude-code-guide
**Date**: 2026-04-16  |  **Artifacts**: 137  |  **Strategy**: progressive
**NL Score**: 86/100
**Security**: CLEAR
**Bugs**: 2  |  **Quality Issues**: 52  |  **Security Findings**: 0

## NL Score Summary

Scoring method: all agents start at 100, subtract -5 (missing `model:` field, universal across this repo), then subtract -2 per line containing a vague quantifier from the set {appropriate, relevant, comprehensive, robust, ensure, various, suitable, necessary, proper, effective, efficient, seamlessly, optimal, leverage, utilize}, capped at -20. Skills start at 100 and subtract only vague-quantifier penalties (no model required). Guide files (CLAUDE.md) scored on content quality; frontmatter not required for this file type.

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/README.md | agent-readme | 23 | Missing name + description frontmatter; no examples |
| agents/risk-manager.md | agent | 75 | Missing model; 10 vague-word lines (cap hit) |
| agents/qa-expert.md | agent | 75 | Missing model; 10 vague-word lines (cap hit) |
| agents/dotnet-core-expert.md | agent | 75 | Missing model; 11 vague-word lines (cap hit) |
| agents/rails-expert.md | agent | 75 | Missing model; 12 vague-word lines (cap hit) |
| agents/django-developer.md | agent | 75 | Missing model; 11 vague-word lines (cap hit) |
| agents/agent-organizer.md | agent | 75 | Missing model; 12 vague-word lines (cap hit) |
| agents/laravel-specialist.md | agent | 75 | Missing model; 11 vague-word lines (cap hit) |
| agents/data-engineer.md | agent | 75 | Missing model; 10 vague-word lines (cap hit) |
| agents/search-specialist.md | agent | 75 | Missing model; 12 vague-word lines (cap hit) |
| agents/multi-agent-coordinator.md | agent | 75 | Missing model; 11 vague-word lines (cap hit) |
| agents/slack-expert.md | agent | 75 | Missing model; 10 vague-word lines (cap hit) |
| skills/top-web-vulnerabilities/SKILL.md | skill | 80 | 17 vague-word lines (cap hit) |
| agents/workflow-orchestrator.md | agent | 77 | Missing model; 9 vague-word lines |
| agents/performance-engineer.md | agent | 77 | Missing model; 9 vague-word lines |
| agents/research-analyst.md | agent | 77 | Missing model; 9 vague-word lines |
| agents/dotnet-framework-4.8-expert.md | agent | 77 | Missing model; 9 vague-word lines |
| agents/technical-writer.md | agent | 79 | Missing model; 8 vague-word lines |
| agents/angular-architect.md | agent | 79 | Missing model; 8 vague-word lines |
| agents/data-researcher.md | agent | 79 | Missing model; 8 vague-word lines |
| agents/incident-responder.md | agent | 79 | Missing model; 8 vague-word lines |
| agents/iot-engineer.md | agent | 79 | Missing model; 8 vague-word lines |
| agents/test-automator.md | agent | 79 | Missing model; 8 vague-word lines |
| agents/database-optimizer.md | agent | 81 | Missing model; 7 vague-word lines |
| agents/embedded-systems.md | agent | 81 | Missing model; 7 vague-word lines |
| agents/security-auditor.md | agent | 81 | Missing model; 7 vague-word lines |
| agents/prompt-engineer.md | agent | 81 | Missing model; 7 vague-word lines |
| agents/ai-engineer.md | agent | 81 | Missing model; 7 vague-word lines |
| agents/nextjs-developer.md | agent | 81 | Missing model; 7 vague-word lines |
| agents/fullstack-developer.md | agent | 81 | Missing model; 7 vague-word lines |
| agents/context-manager.md | agent | 81 | Missing model; 7 vague-word lines |
| agents/llm-architect.md | agent | 81 | Missing model; 7 vague-word lines |
| agents/mlops-engineer.md | agent | 81 | Missing model; 7 vague-word lines |
| agents/kubernetes-specialist.md | agent | 83 | Missing model; 6 vague-word lines |
| agents/dependency-manager.md | agent | 83 | Missing model; 6 vague-word lines |
| agents/flutter-expert.md | agent | 83 | Missing model; 6 vague-word lines |
| agents/blockchain-developer.md | agent | 83 | Missing model; 6 vague-word lines |
| agents/api-documenter.md | agent | 83 | Missing model; 6 vague-word lines |
| agents/build-engineer.md | agent | 83 | Missing model; 6 vague-word lines |
| agents/performance-monitor.md | agent | 83 | Missing model; 6 vague-word lines |
| agents/trend-analyst.md | agent | 83 | Missing model; 6 vague-word lines |
| agents/react-specialist.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/backend-developer.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/devops-engineer.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/quant-analyst.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/knowledge-synthesizer.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/kotlin-specialist.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/devops-incident-responder.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/frontend-developer.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/mcp-developer.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/tooling-engineer.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/rust-engineer.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/golang-pro.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/ml-engineer.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/terraform-engineer.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/api-designer.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/payment-integration.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/postgres-pro.md | agent | 85 | Missing model; 5 vague-word lines |
| agents/nlp-engineer.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/debugger.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/python-pro.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/java-architect.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/machine-learning-engineer.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/cloud-architect.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/documentation-engineer.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/deployment-engineer.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/game-developer.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/ui-designer.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/error-coordinator.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/network-engineer.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/task-distributor.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/git-workflow-manager.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/wordpress-master.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/refactoring-specialist.md | agent | 87 | Missing model; 4 vague-word lines |
| agents/architect-reviewer.md | agent | 87 | Missing model; 4 vague-word lines |
| skills/burp-suite-testing/SKILL.md | skill | 88 | 6 vague-word lines |
| agents/php-pro.md | agent | 89 | Missing model; 3 vague-word lines |
| agents/cli-developer.md | agent | 89 | Missing model; 3 vague-word lines |
| agents/error-detective.md | agent | 89 | Missing model; 3 vague-word lines |
| agents/accessibility-tester.md | agent | 89 | Missing model; 3 vague-word lines |
| agents/seo-specialist.md | agent | 89 | Missing model; 3 vague-word lines |
| agents/security-engineer.md | agent | 89 | Missing model; 3 vague-word lines |
| agents/javascript-pro.md | agent | 89 | Missing model; 3 vague-word lines |
| agents/data-scientist.md | agent | 89 | Missing model; 3 vague-word lines |
| agents/dx-optimizer.md | agent | 89 | Missing model; 3 vague-word lines |
| agents/fintech-engineer.md | agent | 89 | Missing model; 3 vague-word lines |
| agents/data-analyst.md | agent | 89 | Missing model; 3 vague-word lines |
| skills/metasploit-framework/SKILL.md | skill | 90 | 5 vague-word lines |
| agents/microservices-architect.md | agent | 91 | Missing model; 2 vague-word lines |
| agents/csharp-developer.md | agent | 91 | Missing model; 2 vague-word lines |
| agents/graphql-architect.md | agent | 91 | Missing model; 2 vague-word lines |
| agents/database-administrator.md | agent | 91 | Missing model; 2 vague-word lines |
| agents/project-manager.md | agent | 91 | Missing model; 2 vague-word lines |
| agents/legacy-modernizer.md | agent | 91 | Missing model; 2 vague-word lines |
| agents/ux-researcher.md | agent | 91 | Missing model; 2 vague-word lines |
| agents/websocket-engineer.md | agent | 91 | Missing model; 2 vague-word lines |
| agents/elixir-expert.md | agent | 91 | Missing model; 2 vague-word lines |
| agents/powershell-5.1-expert.md | agent | 91 | Missing model; 2 vague-word lines |
| agents/code-reviewer.md | agent | 91 | Missing model; 2 vague-word lines |
| skills/html-injection-testing/SKILL.md | skill | 92 | 4 vague-word lines |
| skills/ssh-penetration-testing/SKILL.md | skill | 92 | 4 vague-word lines |
| agents/agent-installer.md | agent | 93 | Missing model; 1 vague-word line |
| agents/sales-engineer.md | agent | 93 | Missing model; 1 vague-word line |
| agents/mobile-app-developer.md | agent | 93 | Missing model; 1 vague-word line |
| agents/it-ops-orchestrator.md | agent | 93 | Missing model; 1 vague-word line |
| agents/platform-engineer.md | agent | 93 | Missing model; 1 vague-word line |
| agents/cpp-pro.md | agent | 93 | Missing model; 1 vague-word line |
| skills/cloud-penetration-testing/SKILL.md | skill | 94 | 3 vague-word lines |
| skills/linux-privilege-escalation/SKILL.md | skill | 94 | 3 vague-word lines |
| skills/red-team-tools/SKILL.md | skill | 94 | 3 vague-word lines |
| skills/scanning-tools/SKILL.md | skill | 94 | 3 vague-word lines |
| skills/wordpress-penetration-testing/SKILL.md | skill | 94 | 3 vague-word lines |
| skills/pentest-checklist/SKILL.md | skill | 94 | 3 vague-word lines |
| skills/ethical-hacking-methodology/SKILL.md | skill | 94 | 3 vague-word lines |
| skills/wireshark-analysis/SKILL.md | skill | 94 | 3 vague-word lines |
| skills/windows-privilege-escalation/SKILL.md | skill | 94 | 3 vague-word lines |
| guides/CLAUDE.md by zebbern/CLAUDE.md | guide | 94 | No YAML frontmatter (expected for guide type); 3 vague-word lines |
| guides/CLAUDE.md by Sabrina/CLAUDE.md | guide | 94 | No YAML frontmatter (expected for guide type); 3 vague-word lines |
| agents/powershell-ui-architect.md | agent | 95 | Missing model only (0 vague words) |
| agents/m365-admin.md | agent | 95 | Missing model only (0 vague words) |
| agents/powershell-7-expert.md | agent | 95 | Missing model only (0 vague words) |
| agents/powershell-module-architect.md | agent | 95 | Missing model only (0 vague words) |
| skills/xss-html-injection/SKILL.md | skill | 96 | 2 vague-word lines |
| skills/idor-testing/SKILL.md | skill | 96 | 2 vague-word lines |
| skills/broken-authentication/SKILL.md | skill | 96 | 2 vague-word lines |
| skills/privilege-escalation-methods/SKILL.md | skill | 96 | 2 vague-word lines |
| skills/sql-injection-testing/SKILL.md | skill | 96 | 2 vague-word lines |
| skills/network-101/SKILL.md | skill | 96 | 2 vague-word lines |
| skills/pentest-commands/SKILL.md | skill | 96 | 2 vague-word lines |
| skills/file-path-traversal/SKILL.md | skill | 96 | 2 vague-word lines |
| skills/smtp-penetration-testing/SKILL.md | skill | 96 | 2 vague-word lines |
| skills/aws-penetration-testing/SKILL.md | skill | 98 | 1 vague-word line |
| skills/sqlmap-database-pentesting/SKILL.md | skill | 98 | 1 vague-word line |
| skills/api-fuzzing-bug-bounty/SKILL.md | skill | 98 | 1 vague-word line |
| skills/active-directory-attacks/SKILL.md | skill | 98 | 1 vague-word line |
| skills/shodan-reconnaissance/SKILL.md | skill | 98 | 1 vague-word line |
| skills/linux-shell-scripting/SKILL.md | skill | 98 | 1 vague-word line |

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
| Hooks | None found |
| Scripts (.sh/.py/.js) | None found |
| MCP configs (.mcp.json) | None found |
| Package manifests (package.json) | None found |
| Python requirements (requirements.txt) | None found |

### Security Findings

No security findings. The repo contains no executable artifacts — no hooks, no shell scripts, no MCP server configs, and no package manifests with postinstall scripts. The pentesting skill files contain offensive security reference knowledge (exploitation techniques, red team tools, active directory attacks) but these are documentation-only and not executable code surfaces. They are appropriate reference material in a security practitioner context.

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | agents/README.md | Missing `name:` frontmatter field | NLPM scanner treats `.md` files in `agents/` as agent definitions; absence of `name` causes registration failure |
| 2 | agents/README.md | Missing `description:` frontmatter field | Same — the README is a human-facing index, not an agent, but its location in the agents directory makes it vulnerable to scanner misclassification |

## Security Fixes (PR-worthy, Medium/Low only)

No security findings to remediate.

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | ALL 105 named agent files | Missing `model:` field in YAML frontmatter (e.g. `model: claude-sonnet-4-5`) | -5 each |
| 2 | agents/search-specialist.md | 12 vague-quantifier lines (highest density in repo) | -20 (cap) |
| 3 | agents/rails-expert.md | 12 vague-quantifier lines | -20 (cap) |
| 4 | agents/agent-organizer.md | 12 vague-quantifier lines | -20 (cap) |
| 5 | agents/multi-agent-coordinator.md | 11 vague-quantifier lines | -20 (cap) |
| 6 | agents/laravel-specialist.md | 11 vague-quantifier lines | -20 (cap) |
| 7 | agents/dotnet-core-expert.md | 11 vague-quantifier lines | -20 (cap) |
| 8 | agents/django-developer.md | 11 vague-quantifier lines | -20 (cap) |
| 9 | agents/risk-manager.md | 10 vague-quantifier lines | -20 (cap) |
| 10 | agents/qa-expert.md | 10 vague-quantifier lines | -20 (cap) |
| 11 | agents/slack-expert.md | 10 vague-quantifier lines | -20 (cap) |
| 12 | agents/data-engineer.md | 10 vague-quantifier lines | -20 (cap) |
| 13 | agents/workflow-orchestrator.md | 9 vague-quantifier lines | -18 |
| 14 | agents/research-analyst.md | 9 vague-quantifier lines | -18 |
| 15 | agents/performance-engineer.md | 9 vague-quantifier lines | -18 |
| 16 | agents/dotnet-framework-4.8-expert.md | 9 vague-quantifier lines | -18 |
| 17 | agents/technical-writer.md | 8 vague-quantifier lines | -16 |
| 18 | agents/angular-architect.md | 8 vague-quantifier lines | -16 |
| 19 | agents/incident-responder.md | 8 vague-quantifier lines | -16 |
| 20 | agents/data-researcher.md | 8 vague-quantifier lines | -16 |
| 21 | agents/test-automator.md | 8 vague-quantifier lines | -16 |
| 22 | agents/iot-engineer.md | 8 vague-quantifier lines | -16 |
| 23 | agents/context-manager.md | 7 vague-quantifier lines | -14 |
| 24 | agents/database-optimizer.md | 7 vague-quantifier lines | -14 |
| 25 | agents/embedded-systems.md | 7 vague-quantifier lines | -14 |
| 26 | agents/security-auditor.md | 7 vague-quantifier lines | -14 |
| 27 | agents/ai-engineer.md | 7 vague-quantifier lines | -14 |
| 28 | agents/prompt-engineer.md | 7 vague-quantifier lines | -14 |
| 29 | agents/nextjs-developer.md | 7 vague-quantifier lines | -14 |
| 30 | agents/llm-architect.md | 7 vague-quantifier lines | -14 |
| 31 | agents/mlops-engineer.md | 7 vague-quantifier lines | -14 |
| 32 | agents/fullstack-developer.md | 7 vague-quantifier lines | -14 |
| 33 | agents/kubernetes-specialist.md | 6 vague-quantifier lines | -12 |
| 34 | agents/dependency-manager.md | 6 vague-quantifier lines | -12 |
| 35 | agents/flutter-expert.md | 6 vague-quantifier lines | -12 |
| 36 | agents/blockchain-developer.md | 6 vague-quantifier lines | -12 |
| 37 | agents/api-documenter.md | 6 vague-quantifier lines | -12 |
| 38 | agents/build-engineer.md | 6 vague-quantifier lines | -12 |
| 39 | agents/performance-monitor.md | 6 vague-quantifier lines | -12 |
| 40 | agents/trend-analyst.md | 6 vague-quantifier lines | -12 |
| 41 | skills/top-web-vulnerabilities/SKILL.md | 17 vague-quantifier lines (highest in repo including skills) | -20 (cap) |
| 42 | skills/burp-suite-testing/SKILL.md | 6 vague-quantifier lines | -12 |
| 43 | skills/ssh-penetration-testing/SKILL.md | 4 vague-quantifier lines | -8 |
| 44 | skills/html-injection-testing/SKILL.md | 4 vague-quantifier lines | -8 |
| 45 | skills/metasploit-framework/SKILL.md | 5 vague-quantifier lines | -10 |
| 46 | agents/README.md | No agent frontmatter at all — no examples, no output format | -50 frontmatter + -15 examples |
| 47 | (all agents) | Common checklist pattern uses "ensure X is Y" phrasing throughout checklist items | systemic |
| 48 | agents/search-specialist.md | "ensure", "comprehensive", "relevant", "effective", "various" all appear densely | -20 |
| 49 | agents/rails-expert.md | "properly", "effectively", "thoroughly" cluster in checklist items | -20 |
| 50 | agents/agent-organizer.md | "optimal", "efficient", "effectively", "thoroughly" cluster | -20 |
| 51 | guides/CLAUDE.md by zebbern/CLAUDE.md | No YAML frontmatter (expected for guide type, not a bug) | informational |
| 52 | guides/CLAUDE.md by Sabrina/CLAUDE.md | No YAML frontmatter (expected for guide type, not a bug) | informational |

## Cross-Component

**Internal references**: Agent files frequently cross-reference other agents by name (e.g. `microservices-architect.md` references `backend-developer`, `devops-engineer`, `security-auditor`, `performance-engineer`, `database-optimizer`, `api-designer`, `fullstack-developer`, `graphql-architect`). Spot-checked all referenced agent names — all exist in the `agents/` directory. No broken cross-references found.

**agent-installer.md**: References external repo `VoltAgent/awesome-claude-code-subagents` via GitHub API URLs. This is a runtime external dependency, not a broken reference. URLs are hardcoded (`api.github.com/repos/VoltAgent/awesome-claude-code-subagents`). If that repo moves or is renamed, the installer silently fails. Low risk; informational.

**README.md placement**: The `agents/README.md` file sits in a directory that NLPM's scanner treats as an agent source. Any tool doing recursive `.md` discovery will pick it up as a candidate agent definition and fail to register it (missing frontmatter). Should either be moved outside `agents/` or given a frontmatter block with `name` and `description` that signals it's an index file.

**Skill coverage vs. agent surface**: Security-focused skills (29 SKILL.md files covering pentesting, exploitation, red-teaming) have no corresponding security-specialist agents in the collection that reference them. The `security-auditor.md` and `security-engineer.md` agents exist but don't explicitly reference any of the 29 security skills. Minor gap — agents work with loaded skills implicitly, not by name reference.

**Model declaration gap**: No agent in this repository declares a `model:` field. This means Claude Code will use the project default for all agents. For the 100+ specialized agents, some (e.g. `llm-architect`, `multi-agent-coordinator`, `security-auditor`) would benefit from explicitly targeting a more capable model tier.

## Recommendation

**CLEAR — submit PRs for all bugs.**

Security posture is clean: zero executable surfaces, zero critical or high findings. The two bugs (agents/README.md missing frontmatter) are minor but PR-worthy since they can cause scanner misclassification.

**Suggested PR 1 — Fix README.md registration conflict:**
Add a frontmatter block to `agents/README.md` or move it to a non-scanned location. Simplest fix:
```yaml
---
name: specialized-domains-index
description: Index of specialized domain subagents. Not an agent — documentation only.
---
```

**Suggested PR 2 — Add model declarations (batch):**
Add `model: claude-sonnet-4-5` (or appropriate tier) to all 105 agent frontmatter blocks. This is a mechanical find-and-replace in each YAML header.

**Suggested PR 3 — Reduce vague language in high-density files:**
Target the 12 files where the vague-word cap was hit: search-specialist, rails-expert, agent-organizer, multi-agent-coordinator, laravel-specialist, dotnet-core-expert, django-developer, risk-manager, qa-expert, slack-expert, data-engineer, workflow-orchestrator. Replace "ensure X is Y" checklist phrasing with measurable criteria.
