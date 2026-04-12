# NLPM Audit: ananddtyagi/cc-marketplace
**Date**: 2026-04-06  |  **Artifacts**: 272  |  **Strategy**: progressive
**NL Score**: 73/100
**Security**: CLEAR
**Bugs**: 9  |  **Quality Issues**: 200  |  **Security Findings**: 13

---

## NL Score Summary

| Score | File | Issues |
|-------|------|--------|
| 35 | plugins/growth-hacker/agents/growth-hacker.md | No YAML frontmatter: missing name (-25), description (-25), no examples (-15) |
| 35 | plugins/reddit-community-builder/agents/reddit-community-builder.md | No YAML frontmatter: missing name (-25), description (-25), no examples (-15) |
| 35 | plugins/twitter-engager/agents/twitter-engager.md | No YAML frontmatter: missing name (-25), description (-25), no examples (-15) |
| 35 | plugins/content-creator/agents/content-creator.md | No YAML frontmatter: missing name (-25), description (-25), no examples (-15) |
| 40 | plugins/changelog-generator/agents/changelog-generator.md | No YAML frontmatter: missing name (-25), description (-25), no examples (-15) |
| 45 | plugins/2-commit-fast/commands/2-commit-fast.md | Uses `title` not `name` (-25), no description (-25), no allowed-tools (-5) |
| 45 | plugins/claude-dev-infrastructure/skills/meta-skill-router/SKILL.md | No YAML frontmatter: missing name (-25), description (-25), no examples (-15) |
| 55 | plugins/fix-issue/commands/fix-issue.md | Extremely sparse body, no name (-25), no allowed-tools (-5), no examples (-15) |
| 60 | plugins/code-review/commands/code-review.md | No name (-25), no allowed-tools (-5), no examples (-15) |
| 60 | plugins/analyze-codebase/commands/analyze-codebase.md | No name (-25), no allowed-tools (-5), no examples (-15) |
| 60 | plugins/test-file/commands/test-file.md | No name (-25), no allowed-tools (-5), no examples (-15) |
| 60 | plugins/audit/commands/audit.md | No name (-25), no allowed-tools (-5), no examples (-15) |
| 60 | plugins/debug-session/commands/debug-session.md | No name (-25), no allowed-tools (-5), no examples (-15) |
| 60 | plugins/update-claudemd/commands/update-claudemd.md | No name (-25), no allowed-tools (-5), no examples (-15) |
| 60 | plugins/optimize/commands/optimize.md | No name (-25), no allowed-tools (-5), no examples (-15) |
| 60 | plugins/generate-api-docs/commands/generate-api-docs.md | No name (-25), no allowed-tools (-5), no examples (-15) |
| 60 | plugins/fix-pr/commands/fix-pr.md | No name (-25), no description (-25) |
| 60 | plugins/analyze-issue/commands/analyze-issue.md | No name (-25), no allowed-tools (-5), sparse body |
| 60 | plugins/github-issue-fix/commands/github-issue-fix.md | No name (-25), no allowed-tools (-5), sparse body |
| 60 | plugins/pr-issue-resolve/commands/pr-issue-resolve.md | No name (-25), no allowed-tools (-5), sparse body |
| 60 | plugins/update-branch-name/commands/update-branch-name.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/commit/commands/commit.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/refractor/commands/refractor.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/claude-desktop-extension/commands/claude-desktop-extension.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/discuss/commands/discuss.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/lyra/commands/lyra.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/explore/commands/explore.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/ultrathink/commands/ultrathink.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/code-review-assistant/commands/code-review-assistant.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/double-check/commands/double-check.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/bug-detective/commands/bug-detective.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/create-worktrees/commands/create-worktrees.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/documentation-generator/commands/documentation-generator.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/create-pr/commands/create-pr.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/code-explain/commands/code-explain.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/update-claude/commands/update-claude.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/fix-github-issue/commands/fix-github-issue.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/husky/commands/husky.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/create-pull-request/commands/create-pull-request.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/plan/commands/plan.md | No name (-25), no allowed-tools (-5) |
| 60 | plugins/bug-fix/commands/bug-fix.md | No name (-25), no allowed-tools (-5) |
| 62 | plugins/code-reviewer/agents/code-reviewer.md | No model (-5), no examples (-15), tools: Read/Grep/Glob/Bash |
| 65 | plugins/debugger/agents/debugger.md | No model (-5), no examples (-15), 1 example (-5) |
| 65 | plugins/experienced-engineer/agents/documentation-writer.md | No model (-5), no examples (-15) |
| 65 | plugins/experienced-engineer/agents/devops-engineer.md | No model (-5), no examples (-15) |
| 65 | plugins/experienced-engineer/agents/database-architect.md | No model (-5), no examples (-15) |
| 65 | plugins/experienced-engineer/agents/code-quality-reviewer.md | No model (-5), no examples (-15) |
| 65 | plugins/experienced-engineer/agents/ux-ui-designer.md | No model (-5), no examples (-15) |
| 65 | plugins/experienced-engineer/agents/testing-specialist.md | No model (-5), no examples (-15) |
| 65 | plugins/experienced-engineer/agents/performance-engineer.md | No model (-5), no examples (-15) |
| 65 | plugins/experienced-engineer/agents/security-specialist.md | No model (-5), no examples (-15) |
| 65 | plugins/experienced-engineer/agents/api-architect.md | No model (-5), no examples (-15) |
| 65 | plugins/experienced-engineer/agents/tech-lead.md | No model (-5), no examples (-15) |
| 65 | plugins/data-scientist/agents/data-scientist.md | No model (-5), no examples (-15) |
| 65 | plugins/planning-prd-agent/agents/planning-prd-agent.md | model: opus, no examples (-15), no tools listed (-5+) |
| 68 | plugins/sugar/agents/quality-guardian.md | No model (-5), no examples (-15), 2 vague words (-4) |
| 68 | plugins/sugar/agents/task-planner.md | No model (-5), no examples (-15), 2 vague words (-4) |
| 70 | plugins/sugar/agents/sugar-orchestrator.md | No model (-5), no examples (-15) |
| 70 | plugins/onomastophes/agents/onomastophes.md | No model (-5), no examples (-15), tools: WebSearch/Read |
| 72 | plugins/b2b-project-shipper/agents/b2b-project-shipper.md | name mismatch (project-shipper vs b2b-project-shipper), no model (-5) |
| 72 | plugins/desktop-app-dev/agents/desktop-app-dev.md | Malformed frontmatter (all on one line), model: sonnet, 2 examples |
| 72 | plugins/unit-test-generator/agents/unit-test-generator.md | model: sonnet, no examples (-15) |
| 75 | plugins/vision-specialist/agents/vision-specialist.md | model: opus, no examples (-15) |
| 75 | plugins/code-architect/agents/code-architect.md | model: sonnet, no examples (-15) |
| 75 | plugins/project-curator/agents/project-curator.md | model: opus, no examples (-15) |
| 75 | plugins/openapi-expert/commands/openapi-expert.md | Agent-style file in commands/, no allowed-tools (-5), no name mismatch |
| 75 | plugins/kreatsaas/commands/kreatsaas.md | name, description, arguments defined, no allowed-tools (-5) |
| 75 | plugins/claude-dev-infrastructure/commands/dev-manager.md | name, description, no allowed-tools (-5) |
| 75 | plugins/claude-dev-infrastructure/commands/dev-setup.md | name, description, no allowed-tools (-5) |
| 75 | plugins/sugar/commands/sugar-review.md | name, description, no allowed-tools (-5) |
| 75 | plugins/sugar/commands/sugar-task.md | name, description, no allowed-tools (-5) |
| 75 | plugins/sugar/commands/sugar-analyze.md | name, description, no allowed-tools (-5) |
| 75 | plugins/sugar/commands/sugar-status.md | name, description, no allowed-tools (-5) |
| 75 | plugins/sugar/commands/sugar-run.md | name, description, no allowed-tools (-5) |
| 78 | plugins/devops-automator/agents/devops-automator.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/analytics-reporter/agents/analytics-reporter.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/customer-success-manager/agents/customer-success-manager.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/support-responder/agents/support-responder.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/enterprise-onboarding-specialist/agents/enterprise-onboarding-specialist.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/data-privacy-engineer/agents/data-privacy-engineer.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/experiment-tracker/agents/experiment-tracker.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/performance-benchmarker/agents/performance-benchmarker.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/infrastructure-maintainer/agents/infrastructure-maintainer.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/studio-producer/agents/studio-producer.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/workflow-optimizer/agents/workflow-optimizer.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/test-results-analyzer/agents/test-results-analyzer.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/enterprise-integrator-architect/agents/enterprise-integrator-architect.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/accessibility-expert/agents/accessibility-expert.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/ux-researcher/agents/ux-researcher.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/legal-advisor/agents/legal-advisor.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/monitoring-observability-specialist/agents/monitoring-observability-specialist.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/pricing-packaging-specialist/agents/pricing-packaging-specialist.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/brand-guardian/agents/brand-guardian.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/tiktok-strategist/agents/tiktok-strategist.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/app-store-optimizer/agents/app-store-optimizer.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/ai-ethics-governance-specialist/agents/ai-ethics-governance-specialist.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/tool-evaluator/agents/tool-evaluator.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/product-sales-specialist/agents/product-sales-specialist.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/trend-researcher/agents/trend-researcher.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/enterprise-security-reviewer/agents/enterprise-security-reviewer.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/rapid-prototyper/agents/rapid-prototyper.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/finance-tracker/agents/finance-tracker.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/database-performance-optimizer/agents/database-performance-optimizer.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/api-integration-specialist/agents/api-integration-specialist.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/whimsy-injector/agents/whimsy-injector.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/project-shipper/agents/project-shipper.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/compliance-automation-specialist/agents/compliance-automation-specialist.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/api-tester/agents/api-tester.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/legal-compliance-checker/agents/legal-compliance-checker.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/technical-sales-engineer/agents/technical-sales-engineer.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/visual-storyteller/agents/visual-storyteller.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/feedback-synthesizer/agents/feedback-synthesizer.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/test-writer-fixer/agents/test-writer-fixer.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/studio-coach/agents/studio-coach.md | 4 examples, no model (-5), 3 vague words (-6) |
| 78 | plugins/ui-designer/agents/ui-designer.md | 4 examples (magenta color), no model (-5), 3 vague words (-6) |
| 83 | plugins/prd-specialist/agents/prd-specialist.md | model: sonnet, 2 examples, minor vague words (-5) |
| 83 | plugins/codebase-documenter/agents/codebase-documenter.md | model: sonnet, 2 examples, minor vague words (-5) |
| 83 | plugins/problem-solver-specialist/agents/problem-solver-specialist.md | model: opus, 2 examples, minor vague words (-5) |
| 83 | plugins/flutter-mobile-app-dev/agents/flutter-mobile-app-dev.md | model: sonnet, 2 examples, minor vague words (-5) |
| 83 | plugins/mobile-ux-optimizer/agents/mobile-ux-optimizer.md | model: sonnet, 2 examples, minor vague words (-5) |
| 83 | plugins/ceo-quality-controller-agent/agents/ceo-quality-controller-agent.md | model: opus, tools: "*", 2 examples, minor vague words (-5) |
| 85 | plugins/deployment-engineer/agents/deployment-engineer.md | model: sonnet, 2 examples, 1 vague word (-3) |
| 85 | plugins/web-dev/agents/web-dev.md | model: sonnet, 2 examples, 1 vague word (-3) |
| 85 | plugins/claude-dev-infrastructure/skills/qa-testing/SKILL.md | name, description, detailed protocol, 1 vague word (-3) |
| 85 | plugins/claude-dev-infrastructure/skills/plugin-creator/SKILL.md | name, description, comprehensive body |
| 85 | plugins/claude-dev-infrastructure/skills/document-sync/SKILL.md | name, description, well-structured |
| 85 | plugins/claude-dev-infrastructure/skills/chief-architect/SKILL.md | name, description, orchestration patterns |
| 85 | plugins/claude-dev-infrastructure/skills/master-plan-manager/SKILL.md | name, description, planning protocols |
| 85 | plugins/claude-dev-infrastructure/skills/crisis-debugging-advisor/SKILL.md | name, description, structured debug flows |
| 87 | plugins/n8n-workflow-builder/agents/n8n-workflow-builder.md | model: sonnet, 3 examples, 1 vague word (-3) |
| 87 | plugins/python-expert/agents/python-expert.md | model: sonnet, 3 examples, 1 vague word (-3) |
| 88 | plugins/claude-dev-infrastructure/skills/safe-project-organizer/SKILL.md | name, description, triggers metadata, comprehensive safety workflow |
| 88 | plugins/claude-dev-infrastructure/skills/data-safety-auditor/SKILL.md | name, description, triggers metadata |
| 88 | plugins/claude-dev-infrastructure/skills/skill-creator-doctor/SKILL.md | name, description, well-structured protocols |
| 88 | plugins/claude-dev-infrastructure/skills/ai-truthfulness-enforcer/SKILL.md | name, description, structured enforcement rules |
| 88 | plugins/claude-dev-infrastructure/skills/skills-manager/SKILL.md | name, description, management patterns |
| 90 | plugins/math/skills/SKILL.md | name: math-tools, description, code examples with SymPy, excellent structure |
| 92 | plugins/api-contract-sync-manager/skills/api-contract-sync/SKILL.md | name, description, allowed-tools declared, structured workflow |

---

## Security Scan

**Execution Surface Inventory**

| Type | Count | Files |
|------|-------|-------|
| Hooks (hooks.json) | 3 | plugins/claude-dev-infrastructure/hooks/hooks.json, plugins/experienced-engineer/hooks/hooks.json, plugins/sugar/hooks/hooks.json |
| Shell Scripts | 12 | plugins/claude-dev-infrastructure/hooks/*.sh (×11), plugins/claude-dev-infrastructure/init/setup.sh |
| MCP Configs | 0 | — |
| Node.js Servers | 2 | plugins/sugar/mcp-server/sugar-mcp.js, plugins/claude-dev-infrastructure/dev-manager/server.js |
| CJS Modules | 1 | plugins/claude-dev-infrastructure/skills/chief-architect/index.cjs |
| Package Manifests | 2 | plugins/sugar/mcp-server/package.json, plugins/claude-dev-infrastructure/dev-manager/package.json |

**Findings Summary**

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 |
| Medium | 5 |
| Low | 6 |
| **Total** | **13** |

**Detailed Findings**

| # | File | Severity | Pattern | Description | Disposition |
|---|------|----------|---------|-------------|-------------|
| 1 | plugins/sugar/mcp-server/sugar-mcp.js | HIGH | child_process.spawn() | Spawns shell commands for clipboard/sugar CLI operations | Acceptable — uses array args, no shell:true, no user-controlled input |
| 2 | plugins/claude-dev-infrastructure/skills/chief-architect/index.cjs | HIGH | require('child_process') | Imports child_process for potential process spawning | Acceptable — static require for tool orchestration, no eval or shell:true |
| 3 | plugins/claude-dev-infrastructure/dev-manager/server.js | MEDIUM | process.env read | Reads `DEV_MANAGER_PORT` and `DEV_MANAGER_ROOT` from environment | Acceptable — standard Express.js config pattern |
| 4 | plugins/claude-dev-infrastructure/hooks/session-lock-awareness.sh | MEDIUM | find command with exec | Uses `find ... -exec` for file discovery in hooks | Acceptable — operates within project directory, no user input injection |
| 5 | plugins/claude-dev-infrastructure/hooks/task-lock-enforcer.sh | MEDIUM | Shell condition with file reads | Reads lock files and conditionally blocks tool use | Acceptable — defensive pattern, no network or elevated privileges |
| 6 | plugins/claude-dev-infrastructure/hooks/master-plan-reminder.sh | MEDIUM | File existence checks + cat | Reads master plan file and injects into context | Acceptable — static path, no interpolation of user data |
| 7 | plugins/claude-dev-infrastructure/hooks/session-lock-release.sh | MEDIUM | rm on lock file | Deletes session lock file on SessionEnd | Acceptable — scoped to specific lock file path |
| 8 | plugins/claude-dev-infrastructure/dev-manager/package.json | LOW | Caret dependency `^4.18.2` | `express: "^4.18.2"` — unpinned minor/patch versions | Low risk; recommend pinning for reproducible installs |
| 9 | plugins/sugar/mcp-server/package.json | LOW | Caret devDependencies | Multiple `^x.y.z` entries in devDependencies | Low risk in devDependencies; acceptable for local tooling |
| 10 | plugins/claude-dev-infrastructure/hooks/hooks.json | LOW | Shell script references | PreToolUse/PostToolUse hooks reference external .sh scripts | Acceptable — scripts ship in same plugin, reviewed above |
| 11 | plugins/experienced-engineer/hooks/hooks.json | LOW | PostToolUse /update-claude | Triggers `/update-claude` command on significant file changes | Acceptable — invokes slash command, not arbitrary shell |
| 12 | plugins/sugar/hooks/hooks.json | LOW | 11 hooks with throttling | Extensive hook coverage including git commit automation | Acceptable — well-structured with throttling guards |
| 13 | plugins/claude-dev-infrastructure/init/setup.sh | LOW | chmod + symlink creation | Sets permissions and creates .claude directory symlinks during setup | Acceptable — one-time setup, no network calls |

**Security Verdict**: CLEAR — no critical or genuinely high-severity patterns found. All flagged items are standard tool-development patterns with appropriate safeguards.

---

## Structural Bugs

Bugs are schema violations or mismatches that will cause Claude Code to misparse or ignore the artifact entirely.

| # | File | Bug | Fix |
|---|------|-----|-----|
| 1 | plugins/growth-hacker/agents/growth-hacker.md | No YAML frontmatter — file starts with `# Growth Hacker` markdown heading | Wrap metadata in `---` delimiters with `name`, `description`, `model`, `tools` fields |
| 2 | plugins/reddit-community-builder/agents/reddit-community-builder.md | No YAML frontmatter — file starts directly with body prose | Add YAML frontmatter block with required fields |
| 3 | plugins/twitter-engager/agents/twitter-engager.md | No YAML frontmatter — file starts directly with body prose | Add YAML frontmatter block with required fields |
| 4 | plugins/content-creator/agents/content-creator.md | No YAML frontmatter — file starts directly with body prose | Add YAML frontmatter block with required fields |
| 5 | plugins/changelog-generator/agents/changelog-generator.md | No YAML frontmatter — file begins with "You are an expert technical documentation specialist..." | Add YAML frontmatter block with required fields |
| 6 | plugins/b2b-project-shipper/agents/b2b-project-shipper.md | `name: project-shipper` does not match plugin directory `b2b-project-shipper` | Change to `name: b2b-project-shipper` |
| 7 | plugins/claude-dev-infrastructure/skills/meta-skill-router/SKILL.md | No YAML frontmatter — starts with `# Meta Skill Router` heading | Add YAML frontmatter with `name: meta-skill-router` and `description` |
| 8 | plugins/desktop-app-dev/agents/desktop-app-dev.md | Malformed frontmatter — all fields concatenated on one line instead of multi-line YAML | Reformat as proper multi-line YAML block |
| 9 | plugins/accessibility-expert/.claude-plugin/plugin.json | `description` field contains only `"Examples:"` — empty/placeholder value | Replace with meaningful plugin description |

---

## Security Fixes

No Critical or High findings require fixing. The following Medium/Low findings have actionable recommendations:

| # | File | Severity | Recommended Fix |
|---|------|----------|----------------|
| 1 | plugins/claude-dev-infrastructure/dev-manager/package.json | LOW | Pin `express` to exact version (e.g., `"express": "4.18.2"`) for reproducible installs |
| 2 | plugins/sugar/mcp-server/package.json | LOW | Consider pinning devDependencies for CI reproducibility |
| 3 | plugins/claude-dev-infrastructure/hooks/session-lock-awareness.sh | MEDIUM | Add `-- "$PROJECT_DIR"` argument quoting to prevent path injection if PROJECT_DIR contains spaces |
| 4 | plugins/claude-dev-infrastructure/init/setup.sh | LOW | Add `set -euo pipefail` header for safer shell script execution |

---

## Quality Issues (Representative Sample)

These are below-threshold quality patterns (not structural bugs) present across many artifacts.

| Pattern | Affected Count | Example File | Recommended Fix |
|---------|---------------|--------------|----------------|
| Missing `model` declaration on agents | ~70 agents | plugins/experienced-engineer/agents/tech-lead.md | Add `model: sonnet` or `model: opus` to frontmatter |
| Zero examples on agents | ~25 agents | plugins/debugger/agents/debugger.md | Add at least 2 `<example>` blocks with context/user/assistant/commentary |
| One example on agents | ~5 agents | plugins/debugger/agents/debugger.md | Add 1 more example to reach the 2-example minimum |
| Missing `name` on commands | ~38 commands | plugins/code-review/commands/code-review.md | Add `name: <slug>` to frontmatter |
| Missing `allowed-tools` on commands | ~43 commands | plugins/kreatsaas/commands/kreatsaas.md | Add `allowed-tools: <tool-list>` matching tools used in body |
| Vague quantifiers ("comprehensive", "robust", "various") | ~60 agents | plugins/ui-designer/agents/ui-designer.md | Replace with specific, measurable language |
| Agent file placed in commands/ | 1 file | plugins/openapi-expert/commands/openapi-expert.md | Move to agents/ or rewrite as proper command |
| No `allowed-tools` on skills | ~12 skills | plugins/claude-dev-infrastructure/skills/qa-testing/SKILL.md | Declare `allowed-tools` to scope tool access |
| Extremely sparse command body | ~5 commands | plugins/fix-issue/commands/fix-issue.md | Expand with context, steps, expected output |
| Wrong YAML key (`title` vs `name`) | 1 file | plugins/2-commit-fast/commands/2-commit-fast.md | Rename `title` to `name` |

---

## Cross-Component Analysis

**Consistency Issues**

- **plugins/experienced-engineer**: 10 agents share identical frontmatter structure (no model, no examples). The `tech-lead.md` agent references the other 9 agents but those agents have no `model` declaration — if orchestrated, the runtime cannot infer appropriate model tier.

- **plugins/sugar**: The 5 sugar commands (`sugar-review`, `sugar-task`, etc.) reference `sugar status` in the `hooks.json` PostToolUse hook, but `sugar-status.md` command has no `allowed-tools` declaration, creating a mismatch between hook expectation and command capability.

- **plugins/claude-dev-infrastructure**: The `dev-manager.md` command dispatches to `dev-manager/server.js` (an Express server), but neither the command nor the skill declares `allowed-tools: Bash` — developers invoking this command cannot start the server without manually granting Bash access.

- **plugins/b2b-project-shipper**: Name mismatch (`project-shipper` vs `b2b-project-shipper`) will cause issues if any other artifact or command references this agent by name.

**Positive Patterns Worth Preserving**

- `plugins/api-contract-sync-manager/skills/api-contract-sync/SKILL.md` — Best-in-class skill: proper `allowed-tools`, clear description, structured workflow. Use as template for other skills.
- `plugins/math/skills/SKILL.md` — Excellent use of code examples to specify exact tool behavior (SymPy). 
- `plugins/sugar/hooks/hooks.json` — Well-structured hook system with throttling guards. Model for other plugins.
- Agents from `plugins/n8n-workflow-builder` and `plugins/python-expert` — Correct model+examples+tools combination. Score 87.

---

## Recommendation

**CLEAR — submit PRs for all bugs and medium/low security fixes.**

Priority order:
1. **Bug fixes (9 files)**: Missing frontmatter is a hard parse failure. Submit individual PRs per plugin — each is a small, reviewable change.
2. **Model declarations (~70 agents)**: Single-line additions. Batch by contributor (Michael Galpert agents, Alysson Franklin agents) for efficient review.
3. **Command `name` fields (~38 commands)**: Affects agent dispatch routing. Many are one-line fixes.
4. **Security hardening (4 files)**: Low-risk, low-effort — dep pinning and shell script hardening.

**Do not** submit PRs for vague-word cleanup across 60+ agents in a single PR — too noisy for the repo maintainer to review. Instead, fix 3–5 agents per PR as examples, then let the community self-correct.
