# NLPM Audit: shareAI-lab/learn-claude-code
**Date**: 2026-04-06  |  **Artifacts**: 4  |  **Strategy**: single
**NL Score**: 88/100
**Security**: BLOCKED
**Bugs**: 0  |  **Quality Issues**: 13  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/mcp-builder/SKILL.md | skill | 84 | Missing output format (-10); vague: meaningful, sensitive, safe (-6) |
| skills/pdf/SKILL.md | skill | 84 | Missing output format (-10); vague: preferred, recommended, various (-6) |
| skills/agent-builder/SKILL.md | skill | 88 | Missing output format (-10); vague: relevant (-2) |
| skills/code-review/SKILL.md | skill | 94 | Vague quantifiers: thorough, comprehensive, Meaningful (-6) |

**Scoring detail**

| File | R16 output format | R01 vague (×-2) | Total deductions | Score |
|------|------------------|-----------------|-----------------|-------|
| skills/agent-builder/SKILL.md | -10 | -2 (1 term) | -12 | 88 |
| skills/code-review/SKILL.md | — (has format) | -6 (3 terms) | -6 | 94 |
| skills/mcp-builder/SKILL.md | -10 | -6 (3 terms) | -16 | 84 |
| skills/pdf/SKILL.md | -10 | -6 (3 terms) | -16 | 84 |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 |
| Medium | 1 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Scripts (agents/) | agents/s01_agent_loop.py, s02_tool_use.py, s03_todo_write.py, s04_subagent.py, s05_skill_loading.py, s06_context_compact.py, s07_task_system.py, s08_background_tasks.py, s09_agent_teams.py, s10_team_protocols.py, s11_autonomous_agents.py, s12_worktree_task_isolation.py, s_full.py |
| Scripts (references) | skills/agent-builder/references/minimal-agent.py, skills/agent-builder/references/tool-templates.py |
| Scripts (scaffold) | skills/agent-builder/scripts/init_agent.py |
| Tests | tests/test_agents_smoke.py, tests/test_s_full_background.py |
| Package manifests | requirements.txt, web/package.json |
| Hooks | none |
| MCP configs | none |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | agents/s01_agent_loop.py | 70 | SEC-shell-true | `subprocess.run(command, shell=True)` passes LLM-generated command strings directly to the shell. Pattern is architectural and present in all 13 agent files (s01–s12, s_full) and 2 reference scripts. |
| 2 | High | agents/s01_agent_loop.py | 66 | SEC-shell-true | Blocklist-only mitigation (`["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]`) is trivially bypassed: `rm -rf / ` (trailing space), `sudo sh`, `rm -rf /*`, bypassed `> /dev/sda` variants, etc. Provides false sense of security. |
| 3 | Medium | requirements.txt | null | SEC-unpinned-semver | All three dependencies use `>=` pinning (`anthropic>=0.25.0`, `python-dotenv>=1.0.0`, `pyyaml>=6.0`) allowing unlimited major-version upgrades on each fresh `pip install`. |
| 4 | Low | web/package.json | null | SEC-unpinned-semver | All npm dependencies use caret (`^`) ranges. While standard for Node.js development, minor-version updates can introduce regressions in production builds. |

## Bugs (PR-worthy)
No bugs found. All four skill files have required `name` and `description` frontmatter. All references cited in `skills/agent-builder/SKILL.md` exist on disk.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | requirements.txt | `>=` pinning allows unbounded version upgrades | Pin to exact versions (`==`) or add upper bounds, e.g. `anthropic>=0.25.0,<2.0.0` |
| 2 | web/package.json | All deps use `^` semver ranges | For a deployed web app, pin to exact versions in production; leave ranges only in dev tooling |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/agent-builder/SKILL.md | Missing output format — no response template or structure guidance (R16) | -10 |
| 2 | skills/agent-builder/SKILL.md | "Load it when relevant" — "relevant" is undefined criteria (R01, line 45) | -2 |
| 3 | skills/code-review/SKILL.md | "Perform thorough code reviews" — "thorough" undefined (R01, line 3) | -2 |
| 4 | skills/code-review/SKILL.md | "conducting comprehensive code reviews" — "comprehensive" undefined (R01, line 8) | -2 |
| 5 | skills/code-review/SKILL.md | "Meaningful, specific checks" — "Meaningful" undefined (R01, line 69) | -2 |
| 6 | skills/mcp-builder/SKILL.md | Missing output format — no response template or structure guidance (R16) | -10 |
| 7 | skills/mcp-builder/SKILL.md | "Return meaningful error messages" — "meaningful" undefined (R01, line 210) | -2 |
| 8 | skills/mcp-builder/SKILL.md | "Never expose sensitive operations without auth" — "sensitive" undefined (R01, line 212) | -2 |
| 9 | skills/mcp-builder/SKILL.md | "Tools should be safe to retry" — "safe" undefined (R01, line 213) | -2 |
| 10 | skills/pdf/SKILL.md | Missing output format — no response template or structure guidance (R16) | -10 |
| 11 | skills/pdf/SKILL.md | "Quick text extraction (preferred)" — "preferred" without criteria (R01, line 12) | -2 |
| 12 | skills/pdf/SKILL.md | "From Markdown (recommended)" — "recommended" without criteria (R01, line 43) | -2 |
| 13 | skills/pdf/SKILL.md | "PDFs may contain various character encodings" — "various" is a vague placeholder (R01, line 110) | -2 |

## Cross-Component
All references declared in `skills/agent-builder/SKILL.md` resolve correctly: `references/agent-philosophy.md`, `references/minimal-agent.py`, `references/tool-templates.py`, `references/subagent-pattern.py`, and `scripts/init_agent.py` all exist on disk. No orphaned components. Terminology is consistent across all four skills ("MCP", "Claude", "agent"). No cross-skill contradictions detected.

## Recommendation
BLOCKED — do not submit PRs. File private security report.

Two HIGH security findings are present: `subprocess.run(command, shell=True)` is used as the primary bash-tool implementation across all 13 agent demonstration files, and the accompanying blocklist mitigation is trivially bypassed. While this design is intentional for an educational "build coding agents" repository, the false-security blocklist represents a real risk for anyone who copies these templates into production systems. The codebase should document the trust boundary explicitly (these agents are for local, trusted use only) and either remove the blocklist entirely (honest about the capability) or replace it with a proper allowlist or sandboxing mechanism.

Once the security posture is documented or remediated, the 13 quality issues are addressable as normal PRs. The most impactful are the three missing output-format sections (-10 each on agent-builder, mcp-builder, pdf); adding a brief response-structure template to each would bring all four skills above 90.
