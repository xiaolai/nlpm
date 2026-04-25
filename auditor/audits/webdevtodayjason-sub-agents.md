# NLPM Audit: webdevtodayjason/sub-agents
**Date**: 2026-04-06  |  **Artifacts**: 40  |  **Strategy**: batched
**NL Score**: 78/100
**Security**: REVIEW
**Bugs**: 4  |  **Quality Issues**: 26  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| CLAUDE.md | config | 48 | No frontmatter (name, description) |
| agents/devops-engineer/agent.md | agent | 64 | Zero usage examples; no output format section |
| commands/debug.md | command | 65 | Missing name; no empty-input handling for $ARGUMENTS |
| commands/document.md | command | 65 | Missing name; no empty-input handling for $ARGUMENTS |
| commands/refactor.md | command | 65 | Missing name; no empty-input handling for $ARGUMENTS |
| commands/api-docs.md | command | 70 | Missing name; missing allowed-tools |
| commands/api.md | command | 70 | Missing name; missing allowed-tools |
| commands/content.md | command | 70 | Missing name; missing allowed-tools |
| commands/deploy.md | command | 70 | Missing name; missing allowed-tools |
| commands/devops.md | command | 70 | Missing name; missing allowed-tools |
| commands/frontend.md | command | 70 | Missing name; missing allowed-tools |
| commands/marketing.md | command | 70 | Missing name; missing allowed-tools |
| commands/plan.md | command | 70 | Missing name; missing allowed-tools |
| commands/product.md | command | 70 | Missing name; missing allowed-tools |
| commands/requirements.md | command | 70 | Missing name; missing allowed-tools |
| commands/shadcn.md | command | 70 | Missing name; missing allowed-tools |
| commands/tdd.md | command | 70 | Missing name; missing allowed-tools |
| commands/test-first.md | command | 70 | Missing name; missing allowed-tools |
| commands/ui.md | command | 70 | Missing name; missing allowed-tools |
| commands/review.md | command | 75 | Missing name field |
| commands/security-scan.md | command | 75 | Missing name field |
| commands/test.md | command | 75 | Missing name field |
| agents/shadcn-ui-builder/agent.md | agent | 79 | No Bash tool; broken MCP reference; unused NotebookRead |
| agents/frontend-developer/agent.md | agent | 81 | No explicit output format; no model declared |
| agents/tdd-specialist/agent.md | agent | 83 | No explicit output format; no model declared |
| agents/api-developer/agent.md | agent | 87 | No model; 4 vague quantifiers (robust, scalable, comprehensive, clean) |
| agents/doc-writer/agent.md | agent | 89 | No model; 3 vague quantifiers |
| agents/project-planner/agent.md | agent | 89 | No model; 3 vague quantifiers |
| agents/api-documenter/agent.md | agent | 91 | No model declared |
| agents/code-reviewer/agent.md | agent | 91 | No model declared |
| agents/product-manager/agent.md | agent | 91 | No model declared |
| agents/test-runner/agent.md | agent | 91 | No model declared |
| agents/marketing-writer/agent.md | agent | 93 | No model declared |
| agents/refactor/agent.md | agent | 93 | No model declared |
| agents/security-scanner/agent.md | agent | 93 | No model declared |
| commands/context-forge/continue-implementation.md | command | 93 | No allowed-tools; vague "appropriate agent" |
| commands/context-forge/implementation-status.md | command | 95 | No allowed-tools |
| commands/context-forge/prime-context.md | command | 95 | No allowed-tools |
| commands/context-forge/prp-execute.md | command | 95 | No allowed-tools |
| agents/debugger/agent.md | agent | 95 | No model declared |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 0 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts (JS) | 26 (src/commands/*.js, src/utils/*.js, src/memory/index.js, test/*.js, examples/*.js) |
| MCP configs | 0 |
| Package manifests | 2 (package.json, dashboard/package.json) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | src/commands/dashboard.js | 60 | SEC-shell-true | `spawn('npm', ['run', 'dashboard:start'], { shell: true })` — shell: true is unnecessary since all arguments are hardcoded; enables shell injection if future edits interpolate user input into the command |
| 2 | Low | package.json | 71 | SEC-unpinned-semver | Eight production dependencies use `^` semver ranges (e.g., `chalk: ^5.3.0`); a minor-version compromise could inject malicious code |
| 3 | Low | dashboard/package.json | 12 | SEC-unpinned-semver | All dashboard dependencies use `^` semver ranges; `next: 14.1.0` is pinned but radix-ui and others are not |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/* (all 20 files) | Missing `name` field in frontmatter | Without an explicit `name`, Claude Code command registration relies on filename convention only; breaks discoverability in any registry that reads frontmatter |
| 2 | commands/api-docs, api, content, deploy, devops, frontend, marketing, plan, product, requirements, shadcn, tdd, test-first, ui (14 files) | Missing `allowed-tools` on agent-dispatch commands | Commands that omit `allowed-tools` give Claude no guidance on which tools are permitted; other commands in the repo use `allowed-tools: Task` as the correct pattern |
| 3 | agents/shadcn-ui-builder/agent.md | No `Bash` tool declared, yet body requires running ShadCN installation commands | Agent instructs "Install the required ShadCN components using the appropriate installation commands" with no way to execute shell commands |
| 4 | agents/shadcn-ui-builder/agent.md | "ALWAYS use the MCP server during planning" — no `.mcp.json` exists and no MCP tool is in the tools list | Reference to MCP server is unresolvable; agent planning phase will silently fail to access described resources |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | src/commands/dashboard.js | `spawn()` uses `shell: true` unnecessarily (line 60) | Replace with `shell: false` (the default); since command and args are already separated into `['npm', ['run', 'dashboard:start']]`, shell is not needed |
| 2 | package.json | Eight production deps use `^` semver | Pin exact versions or switch to `~` patch-only ranges; run `npm shrinkwrap` or commit a lockfile |
| 3 | dashboard/package.json | Dashboard deps use `^` semver | Pin exact versions; lockfile (package-lock.json) committed alongside the dashboard would mitigate most risk |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | All 15 agents | No `model` field declared in frontmatter | -5 each (systemic) |
| 2 | agents/devops-engineer/agent.md | No agent-interaction examples block — file contains CI/CD code templates but no input→output demo of the agent responding to a user | -15 |
| 3 | agents/devops-engineer/agent.md | No output format section — reader cannot predict the agent's response structure | -10 |
| 4 | agents/frontend-developer/agent.md | No explicit `## Output Format` section; code snippets present but no structured response template | -10 |
| 5 | agents/tdd-specialist/agent.md | No explicit `## Output Format` section | -10 |
| 6 | agents/shadcn-ui-builder/agent.md | Only one example workflow (login page); needs at least two to avoid -5 penalty | -5 |
| 7 | agents/shadcn-ui-builder/agent.md | `NotebookRead` tool declared but agent has no notebook-reading logic; likely cargo-culted from a template | -3 |
| 8 | commands/refactor.md | No empty-input handling: body uses `$ARGUMENTS` with no fallback if user runs `/refactor` bare | -10 |
| 9 | commands/document.md | No empty-input handling for `$ARGUMENTS` | -10 |
| 10 | commands/debug.md | No empty-input handling for `$ARGUMENTS` | -10 |
| 11 | agents/devops-engineer/agent.md | Vague quantifiers: "robust" (l.7), "scalable" (l.7), "proper" (l.403 "Implement proper RBAC") | -6 |
| 12 | agents/project-planner/agent.md | Vague quantifiers: "comprehensive" (l.8), "optimal" (l.64 "optimal agent assignments"), "realistic" (l.154 "realistic time estimates") | -6 |
| 13 | agents/api-developer/agent.md | Vague quantifiers: "robust" (desc), "scalable" (desc), "comprehensive" (l.218 "comprehensive tests"), "clean" (l.302 "clean, secure APIs") | -8 |
| 14 | agents/shadcn-ui-builder/agent.md | Vague quantifiers: "appropriate" ×3 (ll.21,29,65), "comprehensive" (l.25 "comprehensive ui-implementation.md") | -8 |
| 15 | agents/doc-writer/agent.md | Vague quantifiers: "comprehensive" (desc), "user-friendly" (desc), "appropriate" (l.247 "appropriate documentation type") | -6 |
| 16 | agents/code-reviewer/agent.md | Vague quantifiers: "Adequate" (l.67 "Adequate test coverage"), "appropriate" (l.38 "Appropriate abstraction levels") | -4 |
| 17 | agents/api-documenter/agent.md | Vague quantifiers: "comprehensive" (desc), "developer-friendly" (desc) | -4 |
| 18 | agents/product-manager/agent.md | Vague quantifiers: "actionable" (l.14 "clear, actionable user stories"), "realistic" (l.154 "Provide realistic time estimates") | -4 |
| 19 | agents/frontend-developer/agent.md | Vague quantifiers: "modern" (desc), "performant" (desc) | -4 |
| 20 | agents/test-runner/agent.md | Vague quantifiers: "comprehensive" (l.4 desc), "maintainable" (l.149 "maintainable and clear") | -4 |
| 21 | agents/security-scanner/agent.md | Vague quantifier: "comprehensive" (l.11 "comprehensive security audit") | -2 |
| 22 | agents/marketing-writer/agent.md | Vague quantifier: "compelling" (desc, "compelling technical marketing materials") | -2 |
| 23 | agents/refactor/agent.md | Vague quantifier: "Appropriate" (l.38 "Appropriate abstraction levels") | -2 |
| 24 | agents/tdd-specialist/agent.md | Vague quantifier: "comprehensive" (desc, "comprehensive test suites") | -2 |
| 25 | commands/context-forge/continue-implementation.md | Vague quantifier: "appropriate" (l.45 "appropriate agent based on task type") | -2 |
| 26 | CLAUDE.md | Vague quantifier: "related" (l.34 "Launch ALL related agents simultaneously"); also no frontmatter | -2 |

## Cross-Component
**Memory API mismatch**: Every agent and the context-forge commands reference a JavaScript memory API (`memory.set()`, `memory.get()`, `memory.isContextForgeProject()`, `memory.getAvailablePRPs()`, `memory.updatePRPState()`, etc.) as if it is a live runtime feature of Claude Code. The actual source (`src/commands/run.js`) implements this as an in-process, in-memory store (`src/memory/index.js`) with no cross-agent sharing — the "shared memory" advertised in the NL artifacts is a CLI-side simulation, not a Claude Code SDK capability. Agents running inside Claude Code will not have access to this memory store. This creates a systemic documentation-to-implementation gap across 12+ files.

**Duplicate command targets**: `commands/devops.md` and `commands/deploy.md` both dispatch to the `devops-engineer` agent with nearly identical single-sentence bodies. No functional distinction is documented between `/devops` and `/deploy`, making one effectively redundant. Similarly, `commands/marketing.md` and `commands/content.md` both dispatch to `marketing-writer` with different one-liners but no clear rule for when to use each.

**Shadcn MCP reference is unresolvable**: `agents/shadcn-ui-builder/agent.md` (line 22) instructs the agent to "ALWAYS use the MCP server during planning." No `.mcp.json` file exists anywhere in the repository, Bash is not a declared tool, and no MCP tool appears in the agent's tools list. This planning instruction is unexecutable as written, causing silent failure every time the agent enters its planning phase.

## Recommendation
REVIEW — Submit NL fix PRs for all Bugs and Security Fixes. File a GitHub issue flagging the `shell: true` finding (`src/commands/dashboard.js:60`) before merging other changes. The High security pattern is low-exploitability in the current hardcoded form, but removing `shell: true` is a one-line fix that eliminates future injection risk.

**Priority fix order**:
1. Add `name` field to all 20 commands (prevents registration ambiguity)
2. Add `allowed-tools: Task` to the 14 agent-dispatch commands
3. Remove `shell: true` from `dashboard.js` line 60
4. Fix shadcn-ui-builder: add Bash to tools OR replace shell-based install instructions with Task-based delegation; remove MCP reference or add `.mcp.json`
5. Add `model` declaration to all 15 agents
6. Add output format sections to devops-engineer, frontend-developer, tdd-specialist
7. Add usage examples to devops-engineer
8. Add empty-input fallback to refactor, document, debug commands
