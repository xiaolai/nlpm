# NLPM Audit: zhsama/claude-sub-agent
**Date**: 2026-04-25  |  **Artifacts**: 14  |  **Strategy**: single
**NL Score**: 72/100
**Security**: CLEAR
**Bugs**: 2  |  **Quality Issues**: 27  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/agent-workflow.md | command | 55 | Missing `name` frontmatter (-25); no empty-input guard (-10) |
| agents/frontend/senior-frontend-architect.md | agent | 58 | No model (-5); no usage examples (-15); no output format (-10) |
| agents/spec-agents/spec-developer.md | agent | 58 | No model (-5); no usage examples (-15); no output format (-10) |
| agents/spec-agents/spec-planner.md | agent | 66 | No model (-5); no usage examples (-15); heavy vague load (-14) |
| agents/backend/senior-backend-architect.md | agent | 70 | No model (-5); no usage examples (-15) |
| agents/spec-agents/spec-architect.md | agent | 70 | No model (-5); no usage examples (-15) |
| agents/spec-agents/spec-analyst.md | agent | 72 | No model (-5); no usage examples (-15) |
| agents/spec-agents/spec-orchestrator.md | agent | 72 | No model (-5); no usage examples (-15) |
| agents/utility/refactor-agent.md | agent | 74 | No model (-5); no output format (-10); NotebookEdit unused (-3) |
| agents/spec-agents/spec-validator.md | agent | 78 | No model (-5); one example only (-5); vague load (-12) |
| agents/ui-ux/ui-ux-master.md | agent | 80 | No model (-5); no tools declared |
| agents/spec-agents/spec-tester.md | agent | 85 | No model (-5); vague quantifiers (-10) |
| agents/spec-agents/spec-reviewer.md | agent | 85 | No model (-5); vague quantifiers (-10) |
| CLAUDE.md | project-context | 85 | Vague quantifiers (-8); cross-component inconsistencies |

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
| Package manifests (package.json, requirements.txt) | None found |

### Security Findings
No security findings.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/agent-workflow.md | Missing `name` field in frontmatter; only `description` and `allowed-tools` are present | Slash command cannot be invoked by name; registration is incomplete |
| 2 | CLAUDE.md (line 111) + agents/utility/refactor-agent.md | CLAUDE.md lists the utility agent as `refactor-agent` but the agent's frontmatter declares `name: code-refactorer-agent`; the names are mismatched | Users following CLAUDE.md instructions will reference a non-existent agent name |

## Security Fixes (PR-worthy, Medium/Low only)
No security fixes needed.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/backend/senior-backend-architect.md | No `model` field declared in frontmatter | -5 |
| 2 | agents/backend/senior-backend-architect.md | No usage/invocation example blocks showing how to invoke the agent | -15 |
| 3 | agents/frontend/senior-frontend-architect.md | No `model` field declared in frontmatter | -5 |
| 4 | agents/frontend/senior-frontend-architect.md | No usage/invocation example blocks | -15 |
| 5 | agents/frontend/senior-frontend-architect.md | No explicit output format section; agent produces no defined deliverable schema | -10 |
| 6 | agents/spec-agents/spec-analyst.md | No `model` field declared in frontmatter | -5 |
| 7 | agents/spec-agents/spec-analyst.md | No usage/invocation example blocks | -15 |
| 8 | agents/spec-agents/spec-architect.md | No `model` field declared in frontmatter | -5 |
| 9 | agents/spec-agents/spec-architect.md | No usage/invocation example blocks | -15 |
| 10 | agents/spec-agents/spec-developer.md | No `model` field declared in frontmatter | -5 |
| 11 | agents/spec-agents/spec-developer.md | No usage/invocation example blocks | -15 |
| 12 | agents/spec-agents/spec-developer.md | No explicit output format section | -10 |
| 13 | agents/spec-agents/spec-orchestrator.md | No `model` field declared in frontmatter | -5 |
| 14 | agents/spec-agents/spec-orchestrator.md | No usage/invocation example blocks | -15 |
| 15 | agents/spec-agents/spec-planner.md | No `model` field declared in frontmatter | -5 |
| 16 | agents/spec-agents/spec-planner.md | No usage/invocation example blocks | -15 |
| 17 | agents/spec-agents/spec-planner.md | High vague-quantifier density: "comprehensive" ×3, "detailed" ×2, "actionable", "clear" — total -14, near cap | -14 |
| 18 | agents/spec-agents/spec-reviewer.md | No `model` field declared in frontmatter | -5 |
| 19 | agents/spec-agents/spec-reviewer.md | Vague quantifiers: "appropriate" ×2, "proper", "comprehensive", "significant" | -10 |
| 20 | agents/spec-agents/spec-tester.md | No `model` field declared in frontmatter | -5 |
| 21 | agents/spec-agents/spec-tester.md | Vague quantifiers: "comprehensive" ×3, "appropriate", "rigorous" | -10 |
| 22 | agents/spec-agents/spec-validator.md | No `model` field declared in frontmatter | -5 |
| 23 | agents/spec-agents/spec-validator.md | Only one substantive example (the validation report template); no invocation example | -5 |
| 24 | agents/spec-agents/spec-validator.md | Vague quantifiers: "comprehensive" ×2, "appropriate", "thorough" ×2, "actionable" | -12 |
| 25 | agents/ui-ux/ui-ux-master.md | No `model` field declared in frontmatter | -5 |
| 26 | agents/ui-ux/ui-ux-master.md | No `tools` field declared; agent cannot read files or write output documents in production | -0 (quality concern) |
| 27 | agents/utility/refactor-agent.md | No `model` field declared in frontmatter | -5 |
| 28 | agents/utility/refactor-agent.md | No explicit output format section; agent describes analysis process but not deliverable schema | -10 |
| 29 | agents/utility/refactor-agent.md | `NotebookEdit` declared in tools but agent never references notebooks in its workflow | -3 |
| 30 | commands/agent-workflow.md | No empty `$ARGUMENTS` handling; if invoked without arguments the chain starts with no feature description | -10 |

## Cross-Component
**Quality gate threshold inconsistency**: Three artifacts define the Gate 2 threshold differently.
- `CLAUDE.md` line 43: "Gate 2: Development Quality (80% threshold)"
- `agents/spec-agents/spec-orchestrator.md` line 107: Gate 2 threshold is 85%
- `commands/agent-workflow.md`: a single quality gate at ≥95% (no Gate 2 concept at all)

The agent-workflow command does not implement the three-gate model described in CLAUDE.md and spec-orchestrator; it uses one consolidated 95% threshold applied after spec-validator.

**CLAUDE.md documents unimplemented CLI flags**: CLAUDE.md (lines 158–163) documents `--quality=75-95`, `--skip-agent=spec-analyst`, `--phase=planning|development|validation`, and `--language=zh|en` as supported options for `/agent-workflow`. None of these flags are parsed or handled in `commands/agent-workflow.md`. The command accepts only a raw `$ARGUMENTS` string.

**Broken copy instruction**: CLAUDE.md (line 55) shows `cp agents/* .claude/agents/` but the agents are organized in subdirectories (`backend/`, `frontend/`, `spec-agents/`, `ui-ux/`, `utility/`). The glob `agents/*` will copy subdirectory names, not their contents; the correct command is `cp -r agents/* .claude/agents/`.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

Priority fix order:
1. Add `name: agent-workflow` to `commands/agent-workflow.md` frontmatter (Bug #1 — breaks registration)
2. Align `CLAUDE.md` agent reference to `code-refactorer-agent` or rename the frontmatter field in `refactor-agent.md` (Bug #2 — breaks discoverability)
3. Add `model` declarations to all 13 agents (Quality — affects model selection)
4. Add invocation `<example>` blocks to agents missing them (Quality — discoverability)
5. Resolve quality-gate threshold contradiction across CLAUDE.md, spec-orchestrator, agent-workflow (Cross-component — user confusion)
6. Add empty-arguments guard to agent-workflow command (Quality — UX)
