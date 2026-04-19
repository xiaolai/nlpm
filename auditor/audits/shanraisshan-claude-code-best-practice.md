# NLPM Audit: shanraisshan/claude-code-best-practice
**Date**: 2026-04-19  |  **Artifacts**: 44  |  **Strategy**: batched
**NL Score**: 88/100
**Security**: CLEAR
**Bugs**: 3  |  **Quality Issues**: 17  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `.claude/agents/time-agent.md` | agent | 57 | 8 unused tools declared; Write/Edit on time-display-only agent |
| `.claude/agents/workflows/best-practice/workflow-concepts-agent.md` | agent | 68 | Read-only agent with Write/Edit; no examples; vague quantifiers |
| `agent-teams/.claude/commands/time-orchestrator.md` | command | 70 | Missing `description` frontmatter (breaks slash command discovery) |
| `.claude/agents/development-workflows-research-agent.md` | agent | 72 | Read-only agent declares Write/Edit; no examples; NotebookEdit unused |
| `.claude/agents/weather-agent.md` | agent | 72 | Read-only intent but Write/Edit declared; no examples; NotebookEdit unused |
| `.claude/agents/workflows/best-practice/workflow-claude-subagents-agent.md` | agent | 72 | Read-only agent with Write/Edit; no examples; NotebookEdit unused |
| `.claude/agents/workflows/best-practice/workflow-claude-skills-agent.md` | agent | 72 | Read-only agent with Write/Edit; no examples; NotebookEdit unused |
| `.claude/agents/workflows/best-practice/workflow-claude-settings-agent.md` | agent | 72 | Read-only agent with Write/Edit; no examples; NotebookEdit unused |
| `.claude/agents/workflows/best-practice/workflow-claude-commands-agent.md` | agent | 72 | Read-only agent with Write/Edit; no examples; NotebookEdit unused |
| `development-workflows/rpi/.claude/agents/technical-cto-advisor.md` | agent | 77 | No examples; vague quantifiers ("appropriate", "relevant") |
| `development-workflows/rpi/.claude/agents/constitutional-validator.md` | agent | 81 | No examples; vague quantifiers |
| `development-workflows/rpi/.claude/agents/documentation-analyst-writer.md` | agent | 81 | No examples; vague quantifiers ("appropriate") |
| `.claude/agents/presentation-vibe-coding.md` | agent | 82 | No examples; NotebookEdit unused |
| `.claude/agents/presentation-learning-journey.md` | agent | 82 | No examples; NotebookEdit unused |
| `.claude/agents/workflows/development-workflows-research-agent.md` | agent | 85 | No examples |
| `development-workflows/rpi/.claude/agents/ux-designer.md` | agent | 85 | No examples |
| `development-workflows/rpi/.claude/agents/product-manager.md` | agent | 85 | No examples |
| `development-workflows/rpi/.claude/agents/senior-software-engineer.md` | agent | 85 | No examples |
| `development-workflows/rpi/.claude/agents/code-reviewer.md` | agent | 85 | No examples |
| `agent-teams/.claude/agents/time-agent.md` | agent | 85 | No examples |
| `development-workflows/rpi/.claude/commands/rpi/plan.md` | command | 89 | No allowed-tools; vague quantifiers |
| `development-workflows/rpi/.claude/commands/rpi/research.md` | command | 91 | No allowed-tools; vague quantifiers |
| `development-workflows/rpi/.claude/commands/rpi/implement.md` | command | 91 | No allowed-tools; vague quantifiers |
| `development-workflows/rpi/.claude/agents/requirement-parser.md` | agent | 94 | Vague quantifiers ("relevant", "appropriate") |
| `.claude/commands/time-command.md` | command | 95 | No allowed-tools declared |
| `.claude/commands/workflows/development-workflows.md` | command | 95 | No allowed-tools declared |
| `.claude/commands/workflows/best-practice/workflow-claude-settings.md` | command | 95 | No allowed-tools declared |
| `.claude/commands/workflows/best-practice/workflow-claude-skills.md` | command | 95 | No allowed-tools declared |
| `.claude/commands/workflows/best-practice/workflow-claude-commands.md` | command | 95 | No allowed-tools declared |
| `.claude/commands/workflows/best-practice/workflow-claude-subagents.md` | command | 95 | No allowed-tools declared |
| `.claude/commands/workflows/best-practice/workflow-concepts.md` | command | 95 | No allowed-tools declared |
| `.claude/commands/weather-orchestrator.md` | command | 95 | No allowed-tools declared |
| `CLAUDE.md` | config | 95 | Minor: verbose, no structural issues |
| `.claude/skills/weather-svg-creator/SKILL.md` | skill | 100 | — |
| `.claude/skills/time-skill/SKILL.md` | skill | 100 | — |
| `.claude/skills/agent-browser/SKILL.md` | skill | 100 | — |
| `.claude/skills/presentation/vibe-to-agentic-framework/SKILL.md` | skill | 100 | — |
| `.claude/skills/presentation/presentation-styling/SKILL.md` | skill | 100 | — |
| `.claude/skills/presentation/presentation-structure/SKILL.md` | skill | 100 | — |
| `.claude/skills/weather-fetcher/SKILL.md` | skill | 100 | — |
| `agent-teams/.claude/skills/time-svg-creator/SKILL.md` | skill | 100 | — |
| `agent-teams/.claude/skills/time-fetcher/SKILL.md` | skill | 100 | — |
| `.claude/hooks/config/hooks-config.json` | config | 100 | — |
| `.codex/hooks/config/hooks-config.json` | config | 100 | — |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hook scripts | `.claude/hooks/scripts/hooks.py` |
| MCP config | `.mcp.json` |
| Hook configs | `.claude/hooks/config/hooks-config.json`, `.codex/hooks/config/hooks-config.json` |
| Package manifests | None found (`package.json`, `requirements.txt` absent) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | `.mcp.json` | 4,8,12 | `npx -y` auto-install | Three MCP servers use `npx -y` which auto-installs packages without version pinning; any of the three npm packages could be compromised or updated to a malicious version without notice |
| 2 | Medium | `.claude/hooks/scripts/hooks.py` | 185–190 | `subprocess.Popen` | Launches audio player binary with a file path derived from hook event data; path is sanitized (no `..` or `/` in sound_name), but the audio player binary itself is resolved from PATH at runtime |
| 3 | Low | `.mcp.json` | 12 | Unpinned dependency | `deepwiki-mcp` is a lesser-known npm package with no version pin; supply-chain risk if the package is abandoned or hijacked |
| 4 | Low | `.claude/hooks/scripts/hooks.py` | 325–348 | File write with hook data | Logs full hook event data (including `tool_input`, which may contain file contents or command arguments) to `.claude/hooks/logs/hooks-log.jsonl`; log file is not in `.gitignore` by default |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `agent-teams/.claude/commands/time-orchestrator.md` | Missing `description` frontmatter field (only `model: haiku` present) | Command will not appear in `/` slash-command menu; not user-discoverable |
| 2 | `.claude/agents/development-workflows-research-agent.md` AND `.claude/agents/workflows/development-workflows-research-agent.md` | Both files declare `name: development-workflows-research-agent`; name collision across scope boundaries | When both scopes are active, Claude Code may load the wrong agent variant; the root agent incorrectly includes `Write`, `Edit`, `Agent`, `NotebookEdit`, `mcp__*` that the workflow variant wisely omits |
| 3 | `.claude/agents/time-agent.md` (root) AND `agent-teams/.claude/agents/time-agent.md` | Both declare `name: time-agent` with different implementations (PKT/UTC+5 vs Dubai GST/UTC+4) | Whichever scope is active, the wrong time-agent may be invoked; the root variant also bloats allowedTools with 10+ unnecessary tools |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `.mcp.json` | `npx -y @playwright/mcp` — no version pin | Change to `npx -y @playwright/mcp@0.0.29` (or current stable); repeat for all three servers |
| 2 | `.mcp.json` | `npx -y deepwiki-mcp` — unknown package, no pin | Audit package provenance; pin to a specific version; consider replacing with a more established alternative if available |
| 3 | `.claude/hooks/scripts/hooks.py` | `subprocess.Popen` resolves audio player from PATH | Acceptable risk given current sanitization; optionally hardcode known safe paths (e.g., `/usr/bin/afplay`) instead of relying on PATH resolution |
| 4 | `.claude/hooks/scripts/hooks.py` | Hook log may persist sensitive tool input data | Add `hooks-log.jsonl` to `.gitignore`; consider scrubbing `tool_input` from log entries before writing |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | All 20 agents | Zero usage examples across every agent in the repo — systematic gap | −15 each |
| 2 | `.claude/agents/development-workflows-research-agent.md` | Body explicitly says "read-only research, Do NOT modify any local files" but `allowedTools` includes `Write`, `Edit`, `Agent`, `NotebookEdit`, `mcp__*` | −10 (Write/Edit on read-only) + −3 (NotebookEdit unused) |
| 3 | `.claude/agents/weather-agent.md` | Body says "not to write files or create outputs" but `allowedTools` includes `Write`, `Edit`, `NotebookEdit` | −10 + −3 |
| 4 | `.claude/agents/time-agent.md` (root) | Single-purpose time agent (runs one bash date command) declares 10+ tools: `Write`, `Edit`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `Agent`, `NotebookEdit`, `mcp__*` — nearly all unused | −10 (Write/Edit) + −18 (6 clearly unused: Glob, Grep, WebFetch, WebSearch, Agent, NotebookEdit) |
| 5 | Five `workflows/best-practice/*-agent.md` files | All five workflow research agents declare `Write` and `Edit` in `allowedTools` despite each stating "This is a read-only research workflow. Do NOT modify any files." | −10 each |
| 6 | `.claude/agents/presentation-vibe-coding.md`, `.claude/agents/presentation-learning-journey.md` | `NotebookEdit` in allowedTools is not used by HTML-presentation-editing agents | −3 each |
| 7 | `agent-teams/.claude/commands/time-orchestrator.md` | No `description` means no allowed-tools either | −5 (no allowed-tools, subsumed by Bug #1) |
| 8 | All 8 standalone commands | No `allowed-tools` frontmatter declared | −5 each |
| 9 | `development-workflows/rpi/.claude/commands/rpi/plan.md` | Vague quantifiers: "appropriate" (×2), "relevant" (×1) | −6 |
| 10 | `development-workflows/rpi/.claude/commands/rpi/research.md` | Vague quantifiers: "appropriate" (×1), "relevant" (×2) | −6 |
| 11 | `development-workflows/rpi/.claude/commands/rpi/implement.md` | Vague quantifiers: "appropriate" (×2) | −4 |
| 12 | `development-workflows/rpi/.claude/agents/requirement-parser.md` | Vague quantifiers: "relevant" (×2), "appropriate" (×1) | −6 |
| 13 | `development-workflows/rpi/.claude/agents/technical-cto-advisor.md` | Vague quantifiers: "appropriate" (×3), "relevant" (×1) | −8 |
| 14 | `development-workflows/rpi/.claude/agents/constitutional-validator.md` | Vague quantifiers: "appropriate" (×2), "relevant" (×1) | −6 |
| 15 | `development-workflows/rpi/.claude/agents/documentation-analyst-writer.md` | Vague quantifiers: "appropriate" (×2) | −4 |
| 16 | `development-workflows/rpi/.claude/agents/*.md` (all 8 RPI agents) | No `allowedTools` in frontmatter; tools available only described in body prose | Informational (no scoring rule for agents) |
| 17 | Repo-wide agents | Inconsistent frontmatter format: root-scope agents use `allowedTools: [list]` YAML sequence; `agent-teams/time-agent.md` uses `tools: Bash` string — both are accepted by Claude Code but diverges from the schema documented in `CLAUDE.md` which specifies `tools` as comma-separated | Informational |

## Cross-Component
**Name collisions (Bugs #2 and #3):**
- Two files share `name: development-workflows-research-agent`: the root (`.claude/agents/`) and workflows (`.claude/agents/workflows/`) variants. The root variant has a superset of tools that contradicts its read-only body. The workflows variant is the correctly-scoped implementation. Recommended fix: rename the root to `development-workflows-research-agent-root` or remove it if the workflows copy supersedes it.
- Two files share `name: time-agent`: root (PKT, UTC+5) vs agent-teams (Dubai GST, UTC+4). These serve different commands (`/time-command` vs `agent-teams/time-orchestrator`) but the name collision will cause the wrong agent to fire in mixed-scope sessions. Rename the root to `time-agent-pkt` and update `time-command.md` accordingly.

**Workflow command ↔ agent reference integrity:**
All workflow commands correctly reference agent names via `subagent_type` that exist in the repo:
- `workflow-claude-settings.md` → `workflow-claude-settings-agent` ✓
- `workflow-claude-skills.md` → `workflow-claude-skills-agent` ✓
- `workflow-claude-subagents.md` → `workflow-claude-subagents-agent` ✓
- `workflow-claude-commands.md` → `workflow-claude-commands-agent` ✓
- `workflow-concepts.md` → `workflow-concepts-agent` ✓
- `development-workflows.md` → `development-workflows-research-agent` ✓ (but see Bug #2)
- `weather-orchestrator.md` → `weather-agent` ✓
- `agent-teams/time-orchestrator.md` → `time-agent` ✓ (but see Bug #3)

**Skill reference integrity:**
- `weather-svg-creator/SKILL.md` references `reference.md` and `examples.md` (relative links); these files are not in the artifact list — verify they exist at `.claude/skills/weather-svg-creator/reference.md`
- `agent-browser/SKILL.md` references `references/` and `templates/` subdirectories — verify these exist

**RPI workflow integrity:**
The three RPI commands (research → plan → implement) form a sequential pipeline. Cross-references look correct: `plan.md` checks for `RESEARCH.md`, `implement.md` checks for `PLAN.md`. Agent names referenced in the commands (`requirement-parser`, `product-manager`, `senior-software-engineer`, `ux-designer`, `technical-cto-advisor`, `documentation-analyst-writer`, `code-reviewer`, `constitutional-validator`) all have matching agent files in `development-workflows/rpi/.claude/agents/` ✓.

**`documentation-analyst-writer` conflict:** `implement.md` uses `documentation-analyst-writer` as `subagent_type="documentation-analyst-writer"` (treating it as a built-in agent). However `documentation-analyst-writer.md` is also defined as a custom agent in the RPI agents directory. This dual-declaration is intentional (the custom file extends the built-in) but worth noting.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

**Priority order:**
1. **Bug #1** (missing `description` in `time-orchestrator.md`) — one-line fix, command is non-functional without it
2. **Bug #2 & #3** (name collisions) — rename one agent in each collision pair and update the referencing command
3. **Security Fix #4** (add `hooks-log.jsonl` to `.gitignore`) — prevents accidental leakage of tool input data
4. **Security Fix #1 & #2** (pin MCP package versions) — reduces supply-chain risk
5. **Quality: remove Write/Edit from read-only agents** — five `workflows/best-practice/*-agent.md` files plus root `development-workflows-research-agent.md` all state they are read-only but expose mutation tools
6. **Quality: trim root `time-agent.md` allowedTools** — 8 unnecessary tools declared on a one-command agent
7. **Quality: add examples to agents** — all 20 agents have zero usage examples; adding one per agent would each gain +10 points and bring the overall score above 90
