# NLPM Audit: wesammustafa/Claude-Code-Everything-You-Need-to-Know
**Date**: 2026-04-06  |  **Artifacts**: 12  |  **Strategy**: single
**NL Score**: 71/100
**Security**: CLEAR
**Bugs**: 8  |  **Quality Issues**: 23  |  **Security Findings**: 15

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/commands/review.md | command | 44 | Missing frontmatter; no empty-input handling; no unified output format |
| .claude/commands/pr.md | command | 50 | Missing frontmatter; steps not numbered; no output format |
| .claude/commands/ux.md | command | 60 | Missing frontmatter; no steps/argument handling/output format — persona text, not a runnable command |
| .claude/agents/coder-reviewer.md | agent | 66 | Final third of body is a verbatim design-reviewer template that contradicts the declared code-review role |
| .claude/commands/tdd.md | command | 66 | Missing frontmatter |
| .claude/commands/test.md | command | 68 | Missing frontmatter; reads as a reference checklist, not a command |
| .claude/commands/five.md | command | 70 | Missing frontmatter |
| .claude/agents/ux-designer.md | agent | 71 | File truncates mid-sentence; zero example blocks |
| .claude/agents/frontend-engineer.md | agent | 81 | Zero example blocks in description |
| .claude/commands/todo.md | command | 90 | No `argument-hint`; no `allowed-tools` |
| .claude/agents/project-manager.md | agent | 95 | One inline example only, no `<example>` block |
| .claude/agents/tech-lead-architect.md | agent | 95 | One inline example only, no `<example>` block |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 4 |
| Low | 11 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks (Claude Code) | `.claude/hooks/notification.py`, `.claude/hooks/subagent_stop.py`, `.claude/hooks/post_tool_use.py`, `.claude/hooks/stop.py` |
| Hook utilities | `.claude/hooks/utils/llm/anth.py`, `.claude/hooks/utils/llm/oai.py`, `.claude/hooks/utils/tts/elevenlabs_tts.py`, `.claude/hooks/utils/tts/openai_tts.py`, `.claude/hooks/utils/tts/pyttsx3_tts.py` |
| Hook wiring | `.claude/settings.json` (registers `PostToolUse`, `Notification`, `Stop`, `SubagentStop` → the four hook scripts above) |
| MCP configs | none found (`.mcp.json` absent) |
| Package manifests | none found (`package.json`, `requirements.txt` absent — dependencies are declared inline via PEP 723 `uv run --script` blocks) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | .claude/hooks/utils/llm/anth.py | 36 | network call | Calls the Anthropic Messages API using `ANTHROPIC_API_KEY` from the environment to generate a completion message — expected functionality, key stays local and goes only to Anthropic's own endpoint |
| 2 | Medium | .claude/hooks/utils/llm/oai.py | 36 | network call | Calls the OpenAI Chat Completions API using `OPENAI_API_KEY` — same expected pattern as #1 |
| 3 | Medium | .claude/hooks/utils/tts/elevenlabs_tts.py | 65 | network call | Calls the ElevenLabs TTS API using `ELEVENLABS_API_KEY` to synthesize and play audio |
| 4 | Medium | .claude/hooks/utils/tts/openai_tts.py | 68 | network call | Streams audio from the OpenAI TTS endpoint using `OPENAI_API_KEY` |
| 5 | Low | .claude/hooks/notification.py | 71 | hardcoded path | Hardcoded absolute path `/Users/wesam/.local/bin/uv` (leaks the author's local username; breaks on any other machine) instead of the bare `uv` used by every other hook script |
| 6 | Low | .claude/hooks/notification.py | 5 | unpinned dependency | `python-dotenv` declared with no version constraint in the PEP 723 metadata block |
| 7 | Low | .claude/hooks/subagent_stop.py | 5 | unpinned dependency | `python-dotenv` unpinned |
| 8 | Low | .claude/hooks/stop.py | 5 | unpinned dependency | `python-dotenv` unpinned |
| 9 | Low | .claude/hooks/utils/llm/anth.py | 6 | unpinned dependency | `anthropic` unpinned |
| 10 | Low | .claude/hooks/utils/llm/oai.py | 6 | unpinned dependency | `openai` unpinned |
| 11 | Low | .claude/hooks/utils/tts/elevenlabs_tts.py | 6 | unpinned dependency | `elevenlabs` unpinned |
| 12 | Low | .claude/hooks/utils/tts/openai_tts.py | 7 | unpinned dependency | `openai[voice_helpers]` unpinned |
| 13 | Low | .claude/hooks/utils/tts/pyttsx3_tts.py | 5 | unpinned dependency | `pyttsx3` unpinned |
| 14 | Low | .claude/hooks/subagent_stop.py | 116-136 | unvalidated file path | `transcript_path` is taken from the hook's JSON stdin payload and opened/read without confirming it stays within an expected directory; low risk in practice since the value is set by Claude Code itself, not by free-form user text |
| 15 | Low | .claude/hooks/stop.py | 178-198 | unvalidated file path | Same pattern as #14 |

No Critical or High findings — no `eval`/`exec` on untrusted input, no `curl \| sh`, no `shell=True`, no `os.system`, no credential exfiltration to third-party endpoints, and every `subprocess.run` call uses list-argument form with fixed script paths.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .claude/agents/ux-designer.md | File truncates mid-sentence at line 403 (`"Remember: You are the user advocate"`, no trailing punctuation, no more content) | The agent's closing directive is incomplete — a model reading it trails off without the intended closing guidance |
| 2 | .claude/agents/coder-reviewer.md | Lines 289-328 (Feedback Delivery Framework / Report Structure / Technical Requirements) are a near-verbatim copy of `specialized-agents/system-prompts/design-reviewer.md` — they require the Playwright MCP toolset and a "Design Review Summary" output, contradicting the agent's declared code-quality-review purpose (maintainability, performance, test coverage) | Invoking `coder-reviewer` produces a mismatched deliverable (visual/design review template + screenshot requirement) instead of the promised code-quality report |
| 3 | .claude/commands/five.md | Missing YAML frontmatter (no `description`) | No machine-readable description for command discovery/registration tooling |
| 4 | .claude/commands/pr.md | Missing YAML frontmatter (no `description`) | Same as #3 |
| 5 | .claude/commands/review.md | Missing YAML frontmatter (no `description`) | Same as #3 |
| 6 | .claude/commands/tdd.md | Missing YAML frontmatter (no `description`) | Same as #3 |
| 7 | .claude/commands/test.md | Missing YAML frontmatter (no `description`) | Same as #3 |
| 8 | .claude/commands/ux.md | Missing YAML frontmatter (no `description`); body has no Usage/argument pattern, no numbered steps, and no output format | `/ux` has nothing that tells Claude what to *do* when invoked — it only injects a persona description, unlike every other command in the set |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | .claude/hooks/notification.py:71 | Hardcoded absolute path `/Users/wesam/.local/bin/uv` | Replace with `"uv"` (bare command, resolved via `PATH`), matching `subagent_stop.py`/`stop.py` |
| 2 | .claude/hooks/utils/llm/anth.py, oai.py, elevenlabs_tts.py, openai_tts.py, notification.py, subagent_stop.py, stop.py, pyttsx3_tts.py | Unpinned dependencies in PEP 723 `# dependencies = [...]` blocks | Add version bounds, e.g. `"anthropic>=0.40,<1.0"`, `"openai>=1.50,<2.0"`, `"python-dotenv>=1.0,<2.0"` |
| 3 | .claude/hooks/subagent_stop.py, stop.py | `transcript_path` from hook JSON input read without path containment check | Resolve the path and verify it stays under the expected transcript directory before opening |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/agents/coder-reviewer.md | One inline "For example:" clause only — no structured `<example>` block | -5 |
| 2 | .claude/agents/coder-reviewer.md | 7 vague-quantifier hits (`security-relevant` ×7) | -14 |
| 3 | .claude/agents/frontend-engineer.md | Zero examples in description | -15 |
| 4 | .claude/agents/frontend-engineer.md | 2 vague-quantifier hits ("appropriate", "properly") | -4 |
| 5 | .claude/agents/project-manager.md | One inline example only, no `<example>` block | -5 |
| 6 | .claude/agents/tech-lead-architect.md | One inline example only, no `<example>` block | -5 |
| 7 | .claude/agents/ux-designer.md | Zero examples in description | -15 |
| 8 | .claude/agents/ux-designer.md | 2 vague-quantifier hits ("various", "as needed") | -4 |
| 9 | .claude/commands/five.md | No `allowed-tools` declared | -5 |
| 10 | .claude/commands/pr.md | No `allowed-tools` declared | -5 |
| 11 | .claude/commands/pr.md | Six-stage workflow written as unordered bullets, not numbered steps | -10 |
| 12 | .claude/commands/pr.md | No explicit commit-message/PR-body output format defined | -10 |
| 13 | .claude/commands/review.md | No `allowed-tools` declared | -5 |
| 14 | .claude/commands/review.md | No handling for a missing/empty `$ARGUMENTS` (PR link/number) | -10 |
| 15 | .claude/commands/review.md | No unified output format for posting the combined 6-task review to GitHub | -10 |
| 16 | .claude/commands/review.md | 3 vague-quantifier hits ("sufficient", "properly", "relevant") | -6 |
| 17 | .claude/commands/tdd.md | No `allowed-tools` declared | -5 |
| 18 | .claude/commands/tdd.md | 2 vague-quantifier hits ("relevant", "relevent" [sic]) | -4 |
| 19 | .claude/commands/test.md | No `allowed-tools` declared | -5 |
| 20 | .claude/commands/test.md | 1 vague-quantifier hit ("correctly") | -2 |
| 21 | .claude/commands/todo.md | No `argument-hint` despite taking positional arguments | -5 |
| 22 | .claude/commands/todo.md | No `allowed-tools` declared | -5 |
| 23 | .claude/commands/ux.md | No output format, no numbered steps, no argument handling (persona-only body) | -10 |

## Cross-Component
- `coder-reviewer.md`, `frontend-engineer.md`, and `ux-designer.md` each describe a numbered position in a sequential pipeline (e.g. "SEVENTH specialist", "THIRD specialist", "SIXTH phase") and name collaborators — Security Reviewer, Backend Engineer, Database Engineer, Business Analyst — that do **not** exist as `.claude/agents/*.md` files. Those roles only exist as prose docs under `specialized-agents/system-prompts/` and are not registered as invocable Claude Code subagents, so the implemented agent pipeline (5 agents) is incomplete relative to what the agents themselves describe. This may be an intentional scope limit (the missing roles are documented elsewhere) rather than a defect — flagged at medium confidence.
- `.claude/commands/ux.md` and `.claude/agents/ux-designer.md` both cover UX/design responsibilities with different vocabulary ("UX Engineer" vs. "User Experience Designer & UI Specialist") and different structures (full agent spec vs. bare persona doc) — likely redundant, overlapping artifacts worth consolidating. Flagged at low confidence since this could be an intentional split between subagent delegation and manual persona injection.

## Recommendation
**CLEAR** — submit PRs for all 8 bugs and the 3 medium/low security fixes listed above. No Critical or High security findings were found, so no private disclosure is needed; all security items are minor hardening (path portability, dependency pinning, defensive path handling) rather than exploitable vulnerabilities.
