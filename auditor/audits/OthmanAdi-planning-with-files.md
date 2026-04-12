# NLPM Audit: OthmanAdi/planning-with-files
**Date**: 2026-04-06  |  **Artifacts**: 25  |  **Strategy**: batched
**NL Score**: 91/100
**Security**: REVIEW
**Bugs**: 6  |  **Quality Issues**: 14  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .pi/skills/planning-with-files/SKILL.md | Skill | 82 | Missing allowed-tools, no hooks, PowerShell syntax bug |
| .mastracode/skills/planning-with-files/SKILL.md | Skill | 85 | Duplicate `version` key in YAML metadata, no examples section |
| .gemini/skills/planning-with-files/SKILL.md | Skill | 85 | Missing allowed-tools (hooks externalized), no examples section |
| .codebuddy/skills/planning-with-files/SKILL.md | Skill | 85 | Duplicate `version` key in YAML metadata, no examples section |
| .codex/skills/planning-with-files/SKILL.md | Skill | 85 | Duplicate `version` key in YAML metadata, no examples section |
| .opencode/skills/planning-with-files/SKILL.md | Skill | 85 | Duplicate `version` key in YAML metadata, no examples section |
| .continue/skills/planning-with-files/SKILL.md | Skill | 85 | Missing allowed-tools (Continue format), no examples section |
| .cursor/skills/planning-with-files/SKILL.md | Skill | 85 | Duplicate `version` key in YAML metadata, no examples section |
| commands/status.md | Command | 90 | Missing allowed-tools declaration |
| .github/hooks/planning-with-files.json | Hook Config | 90 | No NL-specific issues; purely structural |
| .factory/skills/planning-with-files/SKILL.md | Skill | 92 | No examples section |
| .kiro/skills/planning-with-files/SKILL.md | Skill | 92 | Version drift from canonical (2.32.0-kiro vs 2.33.0), no examples section |
| .claude-plugin/plugin.json | Manifest | 92 | No NL-specific issues; metadata only |
| commands/plan.md | Command | 95 | Missing allowed-tools declaration |
| commands/plan-ar.md | Command | 95 | Missing allowed-tools declaration |
| commands/plan-de.md | Command | 95 | Missing allowed-tools declaration |
| commands/plan-zh.md | Command | 95 | Missing allowed-tools declaration |
| commands/plan-es.md | Command | 95 | Missing allowed-tools declaration |
| commands/start.md | Command | 95 | Missing allowed-tools declaration |
| skills/planning-with-files/SKILL.md | Skill | 95 | No dedicated examples section (inline examples present) |
| skills/planning-with-files-es/SKILL.md | Skill | 95 | No dedicated examples section |
| skills/planning-with-files-de/SKILL.md | Skill | 95 | No dedicated examples section |
| skills/planning-with-files-zht/SKILL.md | Skill | 95 | No dedicated examples section |
| skills/planning-with-files-ar/SKILL.md | Skill | 95 | No dedicated examples section |
| skills/planning-with-files-zh/SKILL.md | Skill | 95 | No dedicated examples section |

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
| Hooks (in-SKILL.md frontmatter) | 14 SKILL.md files containing hook definitions with shell commands |
| Hook scripts (.github/hooks/scripts/) | 5 files: session-start.sh, pre-tool-use.sh, post-tool-use.sh, agent-stop.sh, error-occurred.sh |
| Hook scripts (.cursor/hooks/) | 4 files: pre-tool-use.sh, post-tool-use.sh, stop.sh, user-prompt-submit.sh |
| Hook scripts (.gemini/hooks/) | 5 files: session-start.sh, before-tool.sh, after-tool.sh, before-model.sh, session-end.sh |
| Helper scripts (scripts/) | 5 files: session-catchup.py, sync-ide-folders.py, check-complete.sh, init-session.sh, check-continue.sh |
| IDE skill scripts (*/scripts/) | ~30 files: check-complete.sh, init-session.sh, session-catchup.py copies per IDE |
| Bootstrap scripts | .kiro/skills/planning-with-files/assets/scripts/bootstrap.sh |
| Example scripts | examples/boxlite/quickstart.py |
| MCP configs | None |
| Package manifests | None (no package.json or requirements.txt) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | skills/planning-with-files/SKILL.md (and 13 IDE/localized variants) | 15 | Unconditional context injection | PreToolUse hook runs `cat task_plan.md 2>/dev/null \| head -30` before every tool call, injecting file content into model context on each turn. task_plan.md may contain web/search results. The skill documents this as a known risk in its Security Boundary section but the amplification is real: every tool call re-injects potentially adversarial content. Mitigated by documented guidance to write external content only to findings.md. |
| 2 | Medium | .github/hooks/scripts/session-start.sh | 18–26 | Unsanitized catchup output injection | Session-start hook runs `session-catchup.py`, captures its full output (which may include arbitrary user messages and web content from previous sessions), and injects it verbatim as `additionalContext` into the model context without sanitization. Prior session content could contain adversarial instructions. |
| 3 | Low | skills/planning-with-files/SKILL.md (and 11 localized/IDE variants) | 24 | Env-var derived script path | Stop hook constructs script path via `${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/planning-with-files}/scripts`. If CLAUDE_PLUGIN_ROOT is overridden (e.g., via .env injection), the hook executes scripts from an attacker-controlled path. CLAUDE_PLUGIN_ROOT is set by the Claude Code runtime in normal use, so real-world risk is low. |
| 4 | Low | .github/hooks/scripts/session-start.sh, pre-tool-use.sh, error-occurred.sh | 19, 25, 17 | Runtime Python path resolution | Python interpreter resolved at runtime via `command -v python3 \|\| command -v python`. Malicious PATH modification would redirect execution. Risk is low since PATH manipulation requires prior compromise, but the pattern is worth hardening with an explicit interpreter path or env validation. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .mastracode/skills/planning-with-files/SKILL.md | Duplicate `version: "2.33.0"` key in `metadata:` block (lines 28 and 30) | Strict YAML parsers raise an error or silently drop one value; may break tooling that reads SKILL.md frontmatter |
| 2 | .codebuddy/skills/planning-with-files/SKILL.md | Duplicate `version: "2.33.0"` key in `metadata:` block (lines 28 and 30) | Same as above |
| 3 | .codex/skills/planning-with-files/SKILL.md | Duplicate `version: "2.33.0"` key in `metadata:` block (lines 28 and 30) | Same as above |
| 4 | .opencode/skills/planning-with-files/SKILL.md | Duplicate `version: "2.33.0"` key in `metadata:` block (lines 27 and 29) | Same as above |
| 5 | .cursor/skills/planning-with-files/SKILL.md | Duplicate `version: "2.33.0"` key in `metadata:` block (lines 27 and 29) | Same as above |
| 6 | .pi/skills/planning-with-files/SKILL.md | PowerShell path string missing `$` prefix (line 23): `python scripts\session-catchup.py" (Get-Location)` — the opening quote is absent, making the command syntactically invalid | Windows users running session-catchup via PowerShell get a syntax error; script silently fails |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | .github/hooks/scripts/session-start.sh | Session catchup output injected verbatim into model context (Finding #2) | Truncate or summarize catchup output; add a size cap (e.g., `head -100`) before JSON-encoding; add a prefix note that content is from previous sessions |
| 2 | .github/hooks/scripts/session-start.sh, pre-tool-use.sh, error-occurred.sh | Python interpreter resolved from user PATH (Finding #4) | Use `/usr/bin/env python3` with an existence check, or validate `$PYTHON` points to a known location before invoking |
| 3 | .pi/skills/planning-with-files/SKILL.md | PowerShell syntax error in session-catchup invocation (line 23) | Fix to: `python "$env:USERPROFILE\.pi\skills\planning-with-files\scripts\session-catchup.py" (Get-Location)` |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/plan.md | Missing `allowed-tools` declaration in frontmatter | -5 |
| 2 | commands/plan-ar.md | Missing `allowed-tools` declaration in frontmatter | -5 |
| 3 | commands/plan-de.md | Missing `allowed-tools` declaration in frontmatter | -5 |
| 4 | commands/plan-zh.md | Missing `allowed-tools` declaration in frontmatter | -5 |
| 5 | commands/plan-es.md | Missing `allowed-tools` declaration in frontmatter | -5 |
| 6 | commands/start.md | Missing `allowed-tools` declaration in frontmatter | -5 |
| 7 | commands/status.md | Missing `allowed-tools` declaration in frontmatter | -5 |
| 8 | .gemini/skills/planning-with-files/SKILL.md | Missing `allowed-tools` in frontmatter (hooks are in .gemini/settings.json, but allowed-tools should still be declared for NL tooling) | -5 |
| 9 | .pi/skills/planning-with-files/SKILL.md | Missing `allowed-tools` and no `hooks` section; Pi's hook support is unclear but the omission is inconsistent with all other IDE variants | -5 |
| 10 | .continue/skills/planning-with-files/SKILL.md | Missing `allowed-tools` in frontmatter (Continue uses a different hook format, but allowed-tools helps NL tooling) | -5 |
| 11 | All 25 NL artifacts | No dedicated `## Examples` section; skills/commands show usage patterns only via decision matrices and anti-pattern tables, not input/output examples | -5 each (capped) |
| 12 | .kiro/skills/planning-with-files/SKILL.md | Version 2.32.0-kiro vs canonical 2.33.0 — one minor version behind; may cause confusion for users comparing versions | informational |
| 13 | skills/planning-with-files/SKILL.md | Security Boundary section warns about prompt injection but does not suggest input validation or content length limits on task_plan.md | informational |
| 14 | .factory/skills/planning-with-files/SKILL.md | References `references.md` and `examples.md` flat (not in `references/` subdir); these files exist per IDE but the reference style differs from most other IDEs | informational |

## Cross-Component
**References check:**
- `commands/plan.md` → `planning-with-files:planning-with-files` skill ✓ (skill exists at `skills/planning-with-files/SKILL.md`)
- `commands/plan-ar.md` → `planning-with-files-ar:planning-with-files-ar` skill ✓
- `commands/plan-de.md` → `planning-with-files-de:planning-with-files-de` skill ✓
- `commands/plan-zh.md` → `planning-with-files-zh:planning-with-files-zh` skill ✓
- `commands/plan-es.md` → `planning-with-files-es:planning-with-files-es` skill ✓
- `commands/start.md` → `planning-with-files:planning-with-files` skill ✓
- `commands/status.md` → reads `task_plan.md` directly (no skill reference, correct)

**Version consistency:**
- `.claude-plugin/plugin.json` version 2.33.0 matches canonical `skills/planning-with-files/SKILL.md` metadata ✓
- `.kiro/skills/SKILL.md` version 2.32.0-kiro — one minor version behind canonical ⚠
- All other IDE SKILL.md files: version 2.33.0 ✓ (when parsed correctly despite duplicate key bug)

**Orphaned components:** None detected. All commands reference resolvable skills. All hook scripts are referenced from their respective hook JSON/YAML configurations.

**Contradiction:** The `.pi/skills/SKILL.md` frontmatter declares `name: pi-planning-with-files` while all other IDE variants use `name: planning-with-files`. This inconsistency means the skill name differs from the invocation slug used by other tools.

**Architecture note:** The `scripts/sync-ide-folders.py` tool provides a formal mechanism to propagate canonical content to IDE-specific folders. The duplicate `version` key bugs in five SKILL.md files suggest either the sync script skipped those files or a manual edit introduced the duplication without regenerating from canonical.

## Recommendation

REVIEW — submit PRs for all 6 NL bugs (duplicate version keys, Pi PowerShell syntax). Flag Medium security findings (PreToolUse injection amplification, session-start catchup injection) in a GitHub issue for the maintainer to document or mitigate. The Low findings (PATH-resolved Python, env-var script paths) can be included as security fix PRs since they are Medium/Low severity.

The plugin is well-architected: excellent skill content quality, thorough multilingual coverage (6 languages), cross-IDE support for 11+ tools, and the canonical sync tool prevents drift. The Security Boundary section's self-documentation of the prompt injection risk is commendable. The main systemic issue is the duplicate YAML key introduced by the sync process, affecting 5 IDE SKILL.md files.
