# NLPM Audit: SuperClaude-Org/SuperClaude_Framework
**Date**: 2026-04-26  |  **Artifacts**: 100  |  **Strategy**: progressive
**NL Score**: 84/100
**Security**: BLOCKED
**Bugs**: 6  |  **Quality Issues**: 42  |  **Security Findings**: 6

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| src/superclaude/agents/README.md | agent-readme | 50 | No frontmatter (name/description missing) |
| docs/agents/pm-agent-guide.md | agent-guide | 50 | No frontmatter (name/description missing) |
| src/superclaude/commands/business-panel.md | command | 50 | YAML config embedded in code block, not actual frontmatter |
| plugins/superclaude/commands/business-panel.md | command | 50 | YAML config embedded in code block, not actual frontmatter |
| src/superclaude/commands/README.md | cmd-readme | 50 | No frontmatter (name/description missing) |
| src/superclaude/agents/business-panel-experts.md | agent | 70 | No model, no examples, no output format section |
| plugins/superclaude/agents/business-panel-experts.md | agent | 70 | No model, no examples, no output format section |
| src/superclaude/commands/agent.md | command | 70 | Broken frontmatter (missing opening ---) |
| plugins/superclaude/commands/agent.md | command | 70 | Broken frontmatter (missing opening ---) |
| src/superclaude/commands/recommend.md | command | 75 | No allowed-tools, no numbered steps, no empty input handling |
| plugins/superclaude/commands/recommend.md | command | 75 | No allowed-tools, no numbered steps, no empty input handling |
| src/superclaude/agents/technical-writer.md | agent | 78 | No model, no examples, vague "appropriate" |
| src/superclaude/agents/refactoring-expert.md | agent | 78 | No model, no examples, vague "appropriate" |
| src/superclaude/agents/learning-guide.md | agent | 78 | No model, no examples, vague "appropriate" |
| plugins/superclaude/agents/technical-writer.md | agent | 78 | No model, no examples, vague "appropriate" |
| plugins/superclaude/agents/refactoring-expert.md | agent | 78 | No model, no examples, vague "appropriate" |
| plugins/superclaude/agents/learning-guide.md | agent | 78 | No model, no examples, vague "appropriate" |
| src/superclaude/agents/quality-engineer.md | agent | 80 | No model, no examples |
| src/superclaude/agents/system-architect.md | agent | 80 | No model, no examples |
| src/superclaude/agents/socratic-mentor.md | agent | 80 | No model, 1 example, no output format section |
| src/superclaude/agents/root-cause-analyst.md | agent | 80 | No model, no examples |
| src/superclaude/agents/backend-architect.md | agent | 80 | No model, no examples |
| src/superclaude/agents/requirements-analyst.md | agent | 80 | No model, no examples |
| src/superclaude/agents/performance-engineer.md | agent | 80 | No model, no examples |
| src/superclaude/agents/security-engineer.md | agent | 80 | No model, no examples |
| src/superclaude/agents/devops-architect.md | agent | 80 | No model, no examples |
| src/superclaude/agents/frontend-architect.md | agent | 80 | No model, no examples |
| src/superclaude/agents/python-expert.md | agent | 80 | No model, no examples |
| plugins/superclaude/agents/quality-engineer.md | agent | 80 | No model, no examples |
| plugins/superclaude/agents/system-architect.md | agent | 80 | No model, no examples |
| plugins/superclaude/agents/socratic-mentor.md | agent | 80 | No model, 1 example, no output format section |
| plugins/superclaude/agents/root-cause-analyst.md | agent | 80 | No model, no examples |
| plugins/superclaude/agents/backend-architect.md | agent | 80 | No model, no examples |
| plugins/superclaude/agents/requirements-analyst.md | agent | 80 | No model, no examples |
| plugins/superclaude/agents/performance-engineer.md | agent | 80 | No model, no examples |
| plugins/superclaude/agents/security-engineer.md | agent | 80 | No model, no examples |
| plugins/superclaude/agents/devops-architect.md | agent | 80 | No model, no examples |
| plugins/superclaude/agents/frontend-architect.md | agent | 80 | No model, no examples |
| plugins/superclaude/agents/python-expert.md | agent | 80 | No model, no examples |
| src/superclaude/commands/help.md | command | 95 | No allowed-tools |
| src/superclaude/commands/save.md | command | 83 | No allowed-tools, no empty input handling, vague "appropriate" |
| plugins/superclaude/commands/save.md | command | 83 | No allowed-tools, no empty input handling, vague "appropriate" |
| src/superclaude/commands/troubleshoot.md | command | 83 | No allowed-tools, no empty input handling, vague "appropriate" |
| plugins/superclaude/commands/troubleshoot.md | command | 83 | No allowed-tools, no empty input handling, vague "appropriate" |
| src/superclaude/commands/improve.md | command | 83 | No allowed-tools, no empty input handling, vague "appropriate" |
| plugins/superclaude/commands/improve.md | command | 83 | No allowed-tools, no empty input handling, vague "appropriate" |
| src/superclaude/commands/spec-panel.md | command | 83 | No allowed-tools, no empty input handling, vague "appropriate" |
| src/superclaude/commands/select-tool.md | command | 85 | No allowed-tools, no empty input handling |
| src/superclaude/commands/spawn.md | command | 85 | No allowed-tools, no empty input handling |
| src/superclaude/commands/research.md | command | 85 | No allowed-tools, no empty input handling |
| src/superclaude/commands/document.md | command | 85 | No allowed-tools, no empty input handling |
| src/superclaude/commands/implement.md | command | 85 | No allowed-tools, no empty input handling |
| src/superclaude/commands/task.md | command | 85 | No allowed-tools, no empty input handling |
| src/superclaude/commands/brainstorm.md | command | 85 | No allowed-tools, no empty input handling |
| src/superclaude/commands/estimate.md | command | 85 | No allowed-tools, no empty input handling |
| src/superclaude/commands/workflow.md | command | 85 | No allowed-tools, no empty input handling |
| src/superclaude/commands/design.md | command | 85 | No allowed-tools, no empty input handling |
| src/superclaude/commands/explain.md | command | 85 | No allowed-tools, no empty input handling |
| src/superclaude/commands/git.md | command | 85 | No allowed-tools, no empty input handling |
| plugins/superclaude/commands/select-tool.md | command | 85 | No allowed-tools, no empty input handling |
| plugins/superclaude/commands/spawn.md | command | 85 | No allowed-tools, no empty input handling |
| plugins/superclaude/commands/research.md | command | 85 | No allowed-tools, no empty input handling |
| plugins/superclaude/commands/document.md | command | 85 | No allowed-tools, no empty input handling |
| plugins/superclaude/commands/implement.md | command | 85 | No allowed-tools, no empty input handling |
| plugins/superclaude/commands/task.md | command | 85 | No allowed-tools, no empty input handling |
| plugins/superclaude/commands/brainstorm.md | command | 85 | No allowed-tools, no empty input handling |
| plugins/superclaude/commands/estimate.md | command | 85 | No allowed-tools, no empty input handling |
| plugins/superclaude/commands/workflow.md | command | 85 | No allowed-tools, no empty input handling |
| plugins/superclaude/commands/design.md | command | 85 | No allowed-tools, no empty input handling |
| plugins/superclaude/commands/explain.md | command | 85 | No allowed-tools, no empty input handling |
| src/superclaude/agents/self-review.md | agent | 90 | No model, 1 example |
| src/superclaude/agents/deep-research.md | agent | 90 | No model, 1 example |
| src/superclaude/agents/repo-index.md | agent | 90 | No model, 1 example |
| src/superclaude/agents/deep-research-agent.md | agent | 90 | No model, 1 workflow example |
| plugins/superclaude/agents/self-review.md | agent | 90 | No model, 1 example |
| plugins/superclaude/agents/deep-research.md | agent | 90 | No model, 1 example |
| plugins/superclaude/agents/repo-index.md | agent | 90 | No model, 1 example |
| plugins/superclaude/agents/deep-research-agent.md | agent | 90 | No model, 1 workflow example |
| src/superclaude/commands/index-repo.md | command | 95 | No allowed-tools |
| src/superclaude/commands/pm.md | command | 95 | No allowed-tools |
| src/superclaude/commands/index.md | command | 95 | No allowed-tools |
| src/superclaude/commands/reflect.md | command | 95 | No allowed-tools |
| src/superclaude/commands/analyze.md | command | 95 | No allowed-tools |
| src/superclaude/commands/sc.md | command | 95 | No allowed-tools, stale version (4.1.7 vs 4.3.0) |
| src/superclaude/commands/build.md | command | 95 | No allowed-tools |
| src/superclaude/commands/test.md | command | 95 | No allowed-tools |
| src/superclaude/commands/cleanup.md | command | 95 | No allowed-tools |
| src/superclaude/commands/load.md | command | 95 | No allowed-tools |
| plugins/superclaude/commands/index-repo.md | command | 95 | No allowed-tools |
| plugins/superclaude/commands/pm.md | command | 95 | No allowed-tools |
| plugins/superclaude/commands/index.md | command | 95 | No allowed-tools |
| plugins/superclaude/commands/reflect.md | command | 95 | No allowed-tools |
| plugins/superclaude/commands/analyze.md | command | 95 | No allowed-tools |
| plugins/superclaude/commands/sc.md | command | 95 | No allowed-tools, stale version |
| plugins/superclaude/commands/build.md | command | 95 | No allowed-tools |
| plugins/superclaude/commands/test.md | command | 95 | No allowed-tools |
| plugins/superclaude/commands/cleanup.md | command | 95 | No allowed-tools |
| plugins/superclaude/commands/load.md | command | 95 | No allowed-tools |
| plugins/superclaude/commands/help.md | command | 95 | No allowed-tools |
| src/superclaude/agents/pm-agent.md | agent | 95 | No model |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 1 |
| Medium | 2 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | src/superclaude/hooks/hooks.json, plugins/superclaude/hooks/hooks.json |
| Scripts | scripts/analyze_workflow_metrics.py, scripts/publish.sh, scripts/sync_from_framework.py, scripts/build_superclaude_plugin.py, scripts/uninstall_legacy.sh, scripts/ab_test_workflows.py, scripts/cleanup.sh |
| MCP configs | plugins/superclaude/.mcp.json |
| Package manifests | package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | package.json | 7 | SEC-postinstall-script | `postinstall` script runs `node ./bin/install.js` automatically at `npm install` time; the bin/ directory does not exist in the repo, so this fails silently on install but the pattern enables arbitrary code execution in any published version |
| 2 | High | src/superclaude/hooks/hooks.json | 7 | SEC-missing-hook-script | SessionStart hook executes `./scripts/session-init.sh` on every session start; this script does not exist in the repository — any file dropped at that path would silently execute without user awareness |
| 3 | Medium | plugins/superclaude/hooks/hooks.json | 7 | SEC-missing-hook-script | SessionStart hook executes `${CLAUDE_PLUGIN_ROOT}/scripts/session-init.sh`; script does not exist; env-var-based path adds injection surface |
| 4 | Medium | plugins/superclaude/.mcp.json | 4,9 | SEC-unpinned-semver | Both MCP servers use `npx -y` with `@latest` or implicit latest version; downloaded and executed at startup without version pinning or integrity check |
| 5 | Low | scripts/sync_from_framework.py | 177,272,673,689 | SEC-subprocess | Multiple `subprocess.run()` calls with git commands; list-form invocation (no shell=True) so not directly exploitable, but note the framework URL is passed as a CLI argument which could be user-supplied |
| 6 | Low | package.json | 8 | SEC-postinstall-script | `update` script runs `node ./bin/update.js`; same missing-file issue as postinstall; lower severity since it is not auto-executed at install time |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | src/superclaude/commands/agent.md | Frontmatter is missing its opening `---` delimiter; the file starts with bare `name: sc:agent` on line 1, so Claude Code cannot parse it as valid frontmatter | Command fails to register; agent.md is effectively invisible to the plugin system |
| 2 | plugins/superclaude/commands/agent.md | Same broken frontmatter as src counterpart (missing opening ---) | Same registration failure |
| 3 | src/superclaude/hooks/hooks.json | References `./scripts/session-init.sh` which does not exist in the repository | SessionStart hook errors on every session; hook system may silently fail |
| 4 | plugins/superclaude/hooks/hooks.json | References `session-init.sh` which does not exist | Same hook-failure impact as above |
| 5 | src/superclaude/commands/business-panel.md | YAML frontmatter block is inside a fenced code block in the document body (not real frontmatter); the file has no actual YAML front matter so `name` and `description` are not registered | Command may not be discoverable via standard plugin tooling |
| 6 | plugins/superclaude/commands/business-panel.md | Same missing-frontmatter issue as src counterpart | Same registration impact |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | plugins/superclaude/hooks/hooks.json | SessionStart hook path via env variable is fragile and references a non-existent script | Create `scripts/session-init.sh` with a safe no-op body, or remove the hook until the script exists |
| 2 | plugins/superclaude/.mcp.json | `npx -y @upstash/context7-mcp@latest` — unpinned version auto-downloaded at startup | Pin to a specific release (e.g., `@upstash/context7-mcp@1.0.0`) and verify the package hash |
| 3 | plugins/superclaude/.mcp.json | `npx -y @modelcontextprotocol/server-sequential-thinking` — same unpinned pattern | Pin to a verified release version |
| 4 | scripts/sync_from_framework.py | --framework-repo URL argument is passed to subprocess git clone; a caller-controlled URL enables SSRF or local-path traversal | Validate the URL against an allowlist or restrict to https://github.com/* before passing to git |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | All 40 agent files (src/ + plugins/) | No `model` field declared in frontmatter; Claude Code cannot optimise model selection | -5 each |
| 2 | 13 src/ agents + 13 plugins/ agents (quality-engineer, system-architect, root-cause-analyst, backend-architect, requirements-analyst, performance-engineer, security-engineer, devops-architect, frontend-architect, python-expert, business-panel-experts, refactoring-expert, learning-guide) | Zero example blocks; user cannot see expected agent behaviour | -15 each |
| 3 | 4 src/ agents + 4 plugins/ agents (self-review, deep-research, repo-index, deep-research-agent) | Only one example block | -5 each |
| 4 | All 58 command files (src/ + plugins/) | No `allowed-tools` field in frontmatter; Claude Code uses `mcp-servers` instead, which is non-standard for the allowed-tools convention | -5 each |
| 5 | 15 commands (troubleshoot, select-tool, spawn, research, document, implement, task, brainstorm, estimate, workflow, design, explain, git, save, improve) × 2 copies | No empty-input handling documented; `[required-arg]` commands give no fallback or guidance when invoked bare | -10 each |
| 6 | src/superclaude/agents/business-panel-experts.md + plugins/ copy | No output format section; the persona spec describes expert frameworks but not what the agent actually produces | -10 each |
| 7 | src/superclaude/agents/socratic-mentor.md + plugins/ copy | No explicit output format section; rich YAML knowledge but unclear what the agent emits per turn | -10 each |
| 8 | technical-writer.md, refactoring-expert.md, learning-guide.md (src/ + plugins/) | Vague quantifier "appropriate" each | -2 each |
| 9 | save.md, troubleshoot.md, improve.md, spec-panel.md (src/ + plugins/) | Vague quantifier "appropriate" each | -2 each |
| 10 | src/superclaude/commands/sc.md + plugins/ copy | Version string shows v4.1.7 / Python 0.4.0 but repo is at v4.3.0; will confuse users who read the help command | informational |
| 11 | src/superclaude/agents/README.md | Lists only 3 agents but directory contains 21 files | informational |

## Cross-Component
1. **Stale agent README**: `src/superclaude/agents/README.md` claims only three agents exist (deep-research, repo-index, self-review) and says nothing about the other 18 agent files in the same directory. The list is severely stale and will mislead contributors.

2. **sync_from_framework.py prefix not applied**: The sync script is supposed to add `sc-` prefix to agent names when syncing to `plugins/` (`name: quality-engineer` → `name: sc-quality-engineer`). The current `plugins/superclaude/agents/` files have the same unprefixed names as `src/`. The transform is either not being run or the plugins/ files are being manually maintained, breaking the intended namespace isolation.

3. **session-init.sh missing across both hook locations**: Both `src/superclaude/hooks/hooks.json` and `plugins/superclaude/hooks/hooks.json` reference a `session-init.sh` script that does not exist anywhere in the repository. The hooks are effectively broken for all users.

4. **Version mismatch**: `src/superclaude/commands/sc.md` and `plugins/superclaude/commands/sc.md` display `SuperClaude v4.1.7` (Python 0.4.0) but `package.json` and `CLAUDE.md` both state v4.3.0. The command-level help is two minor versions behind.

5. **Duplicate orchestration protocol**: Both `pm.md` (command) and `pm-agent.md` (agent) define detailed Serena MCP session-start protocols using overlapping memory keys (`pm_context`, `last_session`, `next_actions`). No canonical owner is specified; concurrent use could cause write conflicts in Serena memory.

## Recommendation
BLOCKED — do not submit PRs. File private security report.

The `package.json` postinstall hook (`node ./bin/install.js`) constitutes a Critical supply-chain risk: it runs automatically at `npm install` time and the referenced `bin/` directory does not exist in the current repository state — any version that ships a `bin/install.js` would execute arbitrary Node.js code on every user machine without confirmation. Additionally, both hooks.json files reference a `session-init.sh` that does not exist, meaning any file dropped at that path by a future commit would execute silently at every Claude Code session start.

Address the Critical finding privately before submitting any NL-quality PRs. The Medium-severity MCP pinning fixes (SEC findings 3–4) can be bundled into the same security PR once the Critical is resolved.
