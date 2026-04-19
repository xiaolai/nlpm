# NLPM Audit: rohitg00/pro-workflow
**Date**: 2026-04-06  |  **Artifacts**: 60  |  **Strategy**: batched
**NL Score**: 90/100
**Security**: BLOCKED
**Bugs**: 13  |  **Quality Issues**: 29  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| templates/split-claude-md/CLAUDE.md | template | 75 | Placeholder-only content, no real project guidance |
| commands/learn.md | command | 70 | Missing description frontmatter |
| commands/learn-rule.md | command | 70 | Missing description frontmatter |
| commands/commit.md | command | 70 | Missing description frontmatter |
| commands/search.md | command | 70 | Missing description frontmatter |
| commands/insights.md | command | 70 | Missing description frontmatter |
| commands/wrap-up.md | command | 70 | Missing description frontmatter |
| commands/handoff.md | command | 70 | Missing description frontmatter |
| commands/deslop.md | command | 70 | Missing description frontmatter |
| commands/context-optimizer.md | command | 70 | Missing description frontmatter |
| commands/parallel.md | command | 70 | Missing description frontmatter |
| commands/list.md | command | 70 | Missing description frontmatter |
| commands/replay.md | command | 70 | Missing description frontmatter |
| .claude-plugin/plugin.json | config | 80 | cost-analyst and permission-analyst agents not registered |
| commands/develop.md | command | 85 | No empty-input handling for $ARGUMENTS |
| hooks/hooks.json | config | 90 | Well-formed; 26 hook events wired correctly |
| agents/scout.md | agent | 95 | Model not declared |
| agents/cost-analyst.md | agent | 95 | Model not declared |
| agents/reviewer.md | agent | 95 | Model not declared |
| agents/planner.md | agent | 95 | Model not declared |
| agents/context-engineer.md | agent | 95 | Model not declared |
| agents/permission-analyst.md | agent | 95 | Model not declared |
| commands/mcp-audit.md | command | 95 | Missing allowed-tools |
| commands/sprint-status.md | command | 95 | Missing allowed-tools |
| commands/compact-guard.md | command | 95 | Missing allowed-tools |
| commands/safe-mode.md | command | 95 | Missing allowed-tools |
| commands/doctor.md | command | 95 | Missing allowed-tools |
| commands/auto-setup.md | command | 95 | Missing allowed-tools |
| commands/permission-tuner.md | command | 95 | Missing allowed-tools |
| commands/cost-tracker.md | command | 95 | Missing allowed-tools |
| skills/pro-workflow/SKILL.md | skill | 96 | Long reference document; no quality defects |
| skills/context-optimizer/SKILL.md | skill | 97 | Minor: no explicit output format section header |
| skills/replay-learnings/SKILL.md | skill | 97 | Minor: trigger section could be more specific |
| skills/orchestrate/SKILL.md | skill | 97 | Minor: no explicit output format |
| skills/thoroughness-scoring/SKILL.md | skill | 97 | Minor: "appropriate" used once |
| skills/token-efficiency/SKILL.md | skill | 97 | Clean; attribution note informational only |
| skills/cost-tracker/SKILL.md | skill | 97 | Minor: output section thin |
| skills/context-engineering/SKILL.md | skill | 97 | Minor: budget figures marked as estimates |
| skills/llm-gate/SKILL.md | skill | 97 | Minor: no output format section |
| skills/agent-teams/SKILL.md | skill | 97 | Minor: no output format section |
| skills/insights/SKILL.md | skill | 97 | Minor: data sources relying on file patterns |
| skills/file-watcher/SKILL.md | skill | 97 | Minor: watchPaths integration notes incomplete |
| skills/auto-setup/SKILL.md | skill | 97 | Minor: no output format section |
| skills/safe-mode/SKILL.md | skill | 97 | Minor: hook frontmatter fields non-standard |
| agents/debugger.md | agent | 98 | Clean; model declared (opus); multiple examples |
| skills/bug-capture/SKILL.md | skill | 98 | Excellent; domain-language focus well specified |
| skills/deslop/SKILL.md | skill | 98 | Clean; guardrails well defined |
| skills/learn-rule/SKILL.md | skill | 98 | Clean; guardrails and output defined |
| skills/session-handoff/SKILL.md | skill | 98 | Clean; resume command pattern valuable |
| skills/smart-commit/SKILL.md | skill | 98 | Clean; review suppressions list excellent |
| skills/batch-orchestration/SKILL.md | skill | 98 | Clean; phase decomposition well specified |
| skills/module-map/SKILL.md | skill | 98 | Clean; 15-second read constraint enforced |
| skills/permission-tuner/SKILL.md | skill | 98 | Clean; risk tiers well defined |
| skills/parallel-worktrees/SKILL.md | skill | 98 | Clean; guardrails explicit |
| skills/compact-guard/SKILL.md | skill | 98 | Clean; POST_COMPACT constants cited |
| skills/sprint-status/SKILL.md | skill | 98 | Clean; all four status states defined |
| skills/plan-interrogate/SKILL.md | skill | 98 | Clean; single-question constraint enforced |
| skills/wrap-up/SKILL.md | skill | 98 | Clean; all checklist steps specified |
| skills/mcp-audit/SKILL.md | skill | 98 | Clean; thresholds quantified |
| agents/orchestrator.md | agent | 100 | Clean; model, skills, memory, phases all declared |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 0 |
| Medium | 2 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks config | hooks/hooks.json (26 hook events, 35 script references) |
| Scripts | scripts/*.js (35 Node.js hook scripts) |
| MCP configs | None found |
| Package manifest | package.json (better-sqlite3 dependency) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | CRITICAL | commands/doctor.md | 37 | AWS Access Key pattern (AKIA...) | `AKIAIOSFODNN7EXAMPLE` embedded in hook sanity-check test command. Pattern matches `/AKIA[0-9A-Z]{16}/`. Contextually a false positive — it is the canonical AWS documentation test key used to verify secret-scan.js blocks it. The key is not a real credential and is not sent anywhere. secret-scan.js ALLOWLIST would catch it (`/example/i`). However, automated scanners flag as CRITICAL per pattern match. |
| 2 | MEDIUM | commands/learn.md | 207 | User input in shell SQLite command | Learning content (`<rule>`, `<mistake>`, `<correction>`) interpolated into sqlite3 INSERT shell command. Manual escaping instruction present ("escape single quotes by doubling them") but not enforced programmatically. SQLite is local; no network exposure. |
| 3 | MEDIUM | commands/replay.md | 27 | User input in SQLite FTS5 MATCH | User task keywords interpolated directly into `WHERE learnings_fts MATCH '<keywords>'` in a sqlite3 shell command. FTS5 special characters (`"`, `*`, `^`, `(`) in keywords could cause query errors or unexpected behavior. |
| 4 | LOW | package.json | 46 | Unpinned dependency versions | `better-sqlite3: "^12.6.2"`, `@types/node: "^25.2.2"`, `typescript: "^6.0.2"` use caret ranges. A breaking update in better-sqlite3 could break the learnings database silently. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/learn.md | Missing `description` frontmatter | Command not shown in `/help` menu; plugin marketplace listing incomplete |
| 2 | commands/learn-rule.md | Missing `description` frontmatter | Command not shown in `/help` menu |
| 3 | commands/commit.md | Missing `description` frontmatter | Command not shown in `/help` menu |
| 4 | commands/search.md | Missing `description` frontmatter | Command not shown in `/help` menu |
| 5 | commands/insights.md | Missing `description` frontmatter | Command not shown in `/help` menu |
| 6 | commands/wrap-up.md | Missing `description` frontmatter | Command not shown in `/help` menu |
| 7 | commands/handoff.md | Missing `description` frontmatter | Command not shown in `/help` menu |
| 8 | commands/deslop.md | Missing `description` frontmatter | Command not shown in `/help` menu |
| 9 | commands/context-optimizer.md | Missing `description` frontmatter | Command not shown in `/help` menu |
| 10 | commands/parallel.md | Missing `description` frontmatter | Command not shown in `/help` menu |
| 11 | commands/list.md | Missing `description` frontmatter | Command not shown in `/help` menu |
| 12 | commands/replay.md | Missing `description` frontmatter | Command not shown in `/help` menu |
| 13 | .claude-plugin/plugin.json | `agents/cost-analyst.md` and `agents/permission-analyst.md` not in `agents` array | Both agents are present as files but unregistered; users cannot invoke them via the plugin |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | commands/learn.md | User values interpolated into sqlite3 shell command with advisory-only escaping | Replace the inline `sqlite3` shell command with the Node.js `store` API alternative already documented on lines 214–216; the Node API uses parameterized inserts |
| 2 | commands/replay.md | User keywords in SQLite FTS5 MATCH without sanitization | Sanitize keywords before the query: strip FTS5 special characters (`"*^():-`) or wrap each term in double-quotes (`"term"`) to treat them as phrase queries |
| 3 | package.json | Unpinned better-sqlite3 dependency | Pin to exact version: `"better-sqlite3": "12.6.2"` to prevent unexpected breaking changes in the learnings database layer |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/scout.md | Model not declared in frontmatter | -5 |
| 2 | agents/cost-analyst.md | Model not declared in frontmatter | -5 |
| 3 | agents/reviewer.md | Model not declared in frontmatter | -5 |
| 4 | agents/planner.md | Model not declared in frontmatter | -5 |
| 5 | agents/context-engineer.md | Model not declared in frontmatter | -5 |
| 6 | agents/permission-analyst.md | Model not declared in frontmatter | -5 |
| 7 | commands/* (all 21) | All commands missing `allowed-tools` field | -5 each |
| 8 | commands/develop.md | No empty-input handling for `$ARGUMENTS`; command fails silently if invoked without a feature description | -10 |
| 9 | templates/split-claude-md/CLAUDE.md | Template-only content with `[Project Name]` and `[Brief description]` placeholders; provides no real guidance in its installed state | -25 |
| 10 | skills/pro-workflow/SKILL.md | Longest skill at 562 lines; could be split into focused sub-skills to reduce load overhead | informational |
| 11 | skills/safe-mode/SKILL.md | `hooks` in frontmatter uses non-standard schema fields (Claude Code hook frontmatter is not a recognized plugin feature) | informational |

## Cross-Component
**Agent registration gap**: `plugin.json` registers 6 agents but 8 agent files exist. `cost-analyst.md` and `permission-analyst.md` are present in `agents/` but absent from the `agents` array in `.claude-plugin/plugin.json`. Users installing via the plugin marketplace will not have these two agents available. The corresponding commands (`/cost-tracker` and `/permission-tuner`) reference skill content from these agents but will work independently; only direct agent invocation is broken.

**Command–skill symmetry**: Strong. Most commands (`/commit`, `/wrap-up`, `/replay`, `/handoff`, `/insights`, `/deslop`) have corresponding skill counterparts with matching output formats. The `commands/develop.md` orchestration command correctly delegates to `agents/orchestrator.md`, which preloads `skills/pro-workflow/SKILL.md`.

**Hook–script coverage**: All 35 scripts referenced in `hooks/hooks.json` follow the naming pattern `scripts/<name>.js`. No broken references detected.

**Orphaned skill**: `skills/orchestrate/SKILL.md` documents the `/develop` command pattern but there is no corresponding `/orchestrate` command. This is intentional (it's a reference skill), but the mismatch between skill name and command name (`orchestrate` vs `develop`) could confuse users discovering the skill independently.

**Version inconsistency**: `package.json` reports version `3.2.0` but `.claude-plugin/plugin.json` reports version `3.1.0`. These should be kept in sync for marketplace display.

## Recommendation

**BLOCKED — do not submit PRs. File private security report.**

Finding #1 (commands/doctor.md:37) matches the CRITICAL AWS Access Key pattern. Although contextually a false positive — it is the well-known `AKIAIOSFODNN7EXAMPLE` test key used in the hook sanity-check section to verify that `secret-scan.js` correctly blocks hardcoded credentials — the audit security gate requires BLOCKED status for any CRITICAL pattern match.

**Recommended path to CLEAR**:
1. File a private security report noting the false-positive CRITICAL finding and its context (test-only command, non-executable key value).
2. Replace `AKIAIOSFODNN7EXAMPLE` in `commands/doctor.md:37` with a clearly non-matching placeholder such as `AKIAXXXXXXXXXXXXXXXX` or a redacted form, which still tests the detection logic without triggering the AKIA pattern.
3. Once the critical finding is resolved, this repo qualifies for CLEAR status with a strong NL score of 90/100. The 13 frontmatter bugs (missing `description` on 12 commands + 2 unregistered agents) are all mechanical fixes suitable for a single PR.
