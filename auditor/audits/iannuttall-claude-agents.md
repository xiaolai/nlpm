# NLPM Audit: iannuttall/claude-agents
**Date**: 2026-04-06  |  **Artifacts**: 7  |  **Strategy**: single
**NL Score**: 88/100
**Security**: CLEAR
**Bugs**: 4  |  **Quality Issues**: 17  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/vibe-coding-coach.md | agent | 80 | Missing output format (R12); no tools declared (R11) |
| agents/security-auditor.md | agent | 82 | Three unused tools: Edit, MultiEdit, NotebookEdit (R11) |
| agents/content-writer.md | agent | 90 | No tools declared (R11); missing model (R10) |
| agents/frontend-designer.md | agent | 90 | No tools declared (R11); missing model (R10) |
| agents/prd-writer.md | agent | 90 | Missing model (R10); unused Task + vague "relevant" |
| agents/project-task-planner.md | agent | 90 | Missing model (R10); unused NotebookEdit + vague "relevant" |
| agents/code-refactorer.md | agent | 95 | Missing model declaration (R10) |

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
| Scripts | none |
| MCP configs | none |
| Package manifests | none |

### Security Findings
No security findings.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | agents/content-writer.md | No `tools` field in frontmatter; body instructs the agent to write Markdown files ("Save as Markdown in specified folder") and perform web research, but no tools are declared | Agent cannot write output files or research topics as designed |
| 2 | agents/frontend-designer.md | No `tools` field in frontmatter; body instructs the agent to generate `frontend-design-spec.md` and use web search for best practices, but no tools are declared | Agent cannot write the design spec it promises to deliver |
| 3 | agents/vibe-coding-coach.md | No `tools` field in frontmatter; body describes building complete working applications and writing code iteratively, but no tools are declared at all | Agent cannot create or modify any files |
| 4 | agents/prd-writer.md | `Task` declared in tools but body explicitly states "You are not responsible or allowed to create tasks or actions" — a direct contradiction; no workflow step exercises Task | Misleading declaration; creates false expectation that the agent orchestrates sub-agents |

## Security Fixes (PR-worthy, Medium/Low only)
No security fixes needed.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/code-refactorer.md | R10: no model declared in frontmatter | -5 |
| 2 | agents/content-writer.md | R10: no model declared in frontmatter | -5 |
| 3 | agents/frontend-designer.md | R10: no model declared in frontmatter | -5 |
| 4 | agents/prd-writer.md | R10: no model declared in frontmatter | -5 |
| 5 | agents/prd-writer.md | R11: `Task` declared but unused — body prohibits task creation | -3 |
| 6 | agents/prd-writer.md | R01: vague quantifier "relevant" (line 38: "relevant subheadings") | -2 |
| 7 | agents/project-task-planner.md | R10: no model declared in frontmatter | -5 |
| 8 | agents/project-task-planner.md | R11: `NotebookEdit` declared but unused — agent writes Markdown task lists, not notebooks | -3 |
| 9 | agents/project-task-planner.md | R01: vague quantifier "relevant" (line 96: "relevant technical details") | -2 |
| 10 | agents/security-auditor.md | R10: no model declared in frontmatter | -5 |
| 11 | agents/security-auditor.md | R11: `Edit` declared but unused — body describes reporting remediation steps as checklist items, not implementing fixes | -3 |
| 12 | agents/security-auditor.md | R11: `MultiEdit` declared but unused — same reasoning as Edit | -3 |
| 13 | agents/security-auditor.md | R11: `NotebookEdit` declared but unused — agent only writes security-report.md | -3 |
| 14 | agents/security-auditor.md | R01: vague quantifier "relevant" (line 25: "relevant security standards or best practices") | -2 |
| 15 | agents/security-auditor.md | R01: vague quantifier "appropriate" (line 26: "suggest an appropriate location first") | -2 |
| 16 | agents/security-auditor.md | Informational: `Read`, `Grep`, `LS` absent from tools; codebase review is the core task but `Bash` must substitute — functional but less ergonomic | 0 |
| 17 | agents/vibe-coding-coach.md | R10: no model declared in frontmatter | -5 |
| 18 | agents/vibe-coding-coach.md | R12: no output format defined — body describes a 5-step development process but never specifies what files are produced, in what format, or where they are written | -10 |

## Cross-Component
README.md lists all 7 agents by name and every `name:` frontmatter field matches exactly. No broken file references, no count mismatches. The agents do not cross-reference each other, so there are no inter-agent dependency issues.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

Priority order for PRs:
1. **Bug #3** (vibe-coding-coach missing tools) — agent is completely non-functional without a tools declaration; suggest `tools: Edit, Write, Bash, Read, Grep, LS, WebSearch` at minimum
2. **Bug #1** (content-writer missing tools) — agent cannot write files or search the web; suggest `tools: Write, WebSearch, WebFetch`
3. **Bug #2** (frontend-designer missing tools) — agent cannot write its primary output; suggest `tools: Write, WebSearch, WebFetch, Read`
4. **Bug #4** (prd-writer contradictory Task tool) — remove `Task` from the tools list
5. **Quality** — add `model: claude-sonnet-4-5` to all 7 agents (universal fix, one PR)
6. **Quality** — remove `Edit`, `MultiEdit`, `NotebookEdit` from security-auditor; add `Read`, `Grep`, `LS`
7. **Quality** — remove `NotebookEdit` from project-task-planner
8. **Quality** — add an explicit output format section to vibe-coding-coach describing what files are written and where
