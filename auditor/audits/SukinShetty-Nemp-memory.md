# NLPM Audit: SukinShetty/Nemp-memory
**Date**: 2026-04-06  |  **Artifacts**: 29  |  **Strategy**: batched
**NL Score**: 92/100
**Security**: CLEAR
**Bugs**: 4  |  **Quality Issues**: 30  |  **Security Findings**: 2

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/suggest.md | command | 75 | Vague quantifiers (>10 instances, capped -20) + no allowed-tools (-5) |
| commands/context.md | command | 81 | Vague quantifiers (7 instances, -14) + no allowed-tools (-5) |
| CLAUDE.md | data | 85 | Stale file count (cross-component) |
| commands/export.md | command | 89 | No allowed-tools (-5) + vague terms (-6) |
| commands/sync.md | command | 89 | No allowed-tools (-5) + vague terms (-6) |
| SKILL.md | skill | 90 | Empty body — no skill content beyond frontmatter (-10) |
| .claude-plugin/hooks/hooks.json | hook-config | 90 | Broad trigger scope on Edit|Write|Bash |
| commands/recall.md | command | 91 | No allowed-tools (-5) + vague terms (-4) |
| commands/save.md | command | 91 | No allowed-tools (-5) + vague terms (-4) |
| commands/init.md | command | 91 | No allowed-tools (-5) + vague terms (-4) |
| commands/nemp-pro-export.md | command | 93 | No allowed-tools (-5) + minor vague terms (-2) |
| skills/nemp-memory/SKILL.md | skill | 93 | Backslash-escaped markdown throughout file body (-7) |
| commands/activate.md | command | 95 | No allowed-tools (-5) |
| commands/log.md | command | 95 | No allowed-tools (-5) |
| commands/recall-global.md | command | 95 | No allowed-tools (-5) |
| commands/health.md | command | 95 | No allowed-tools (-5) |
| commands/foresight.md | command | 95 | No allowed-tools (-5) |
| commands/import.md | command | 95 | No allowed-tools (-5) |
| commands/auto-sync.md | command | 95 | No allowed-tools (-5) |
| commands/forget.md | command | 95 | No allowed-tools (-5) |
| commands/activity.md | command | 95 | No allowed-tools (-5) |
| commands/save-global.md | command | 95 | No allowed-tools (-5) |
| commands/decay.md | command | 95 | No allowed-tools (-5) |
| commands/cortex.md | command | 95 | No allowed-tools (-5) |
| commands/list.md | command | 95 | No allowed-tools (-5) |
| commands/list-global.md | command | 95 | No allowed-tools (-5) |
| commands/auto-export.md | command | 95 | No allowed-tools (-5) |
| commands/auto-capture.md | command | 95 | No allowed-tools (-5) |
| .claude-plugin/plugin.json | manifest | 95 | Version drift vs marketplace.json (cross-component) |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | `.claude-plugin/hooks/hooks.json`, `.claude-plugin/hooks/post-tool.md` |
| Scripts | none |
| MCP configs | none |
| Package manifests | none |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Low | .claude-plugin/hooks/hooks.json | 4 | broad-hook-trigger | Hook matcher `Edit\|Write\|Bash` fires on every single tool invocation. Internal guards exist (checks config before acting) but the hook overhead runs unconditionally for all file edits and shell commands. |
| 2 | Low | .claude-plugin/hooks/post-tool.md | 49-57 | activity-logging-bash | When auto-capture is enabled, all significant Bash command details are logged to `.nemp-pro/activity.log`. Log content is local-only, but no sanitization is applied to exclude commands that may contain sensitive values in arguments. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/export.md | "Nemp Pro" section at bottom lists `/nemp:export --codex`, `/nemp:export --cursor`, `/nemp:export --windsurf`, `/nemp:export --all` — the correct commands are `/nemp-pro:export --*`. | Users who activate Pro and follow documentation in `/nemp:export` are directed to non-existent command flags; Pro features appear broken. |
| 2 | commands/activate.md | Step 4 confirmation output lists `/nemp:export --codex / --cursor / --windsurf / --all` instead of the correct `/nemp-pro:export --*` syntax. | Newly activated Pro users immediately see wrong command syntax in their first success message. |
| 3 | .claude-plugin/marketplace.json | `plugins[0].version` is `"0.1.0"` but `.claude-plugin/plugin.json` declares `"0.3.0"`. | Marketplace registry shows a version two minor versions behind the actual published plugin; may prevent marketplace indexing from picking up latest release. |
| 4 | CLAUDE.md | `structure` memory value says `"commands/ (20 .md files)"` but the repo contains 24 command .md files. | Stale documentation; contributors and tools inspecting CLAUDE.md will have an inaccurate picture of the plugin's command surface. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | .claude-plugin/hooks/hooks.json | Hook matcher `Edit\|Write\|Bash` runs on every tool call regardless of config. Since auto-capture and auto-sync only trigger on `Write` events (specifically writes to `.nemp/memories.json`), the `Edit` and `Bash` triggers cause unnecessary overhead when both features are disabled. | Change matcher to `Write` only, or add a fast-path early-exit check using a lightweight config probe before any JSON parsing. |
| 2 | .claude-plugin/hooks/post-tool.md | Activity log captures `"details": "<brief-description>"` from Bash commands without sanitizing for sensitive-looking tokens or keys in arguments (e.g. `npm install --auth-token=...`). | Filter out or redact arguments matching patterns like `--token`, `--key`, `--password`, `--secret` before appending to the activity log. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/suggest.md | No `allowed-tools` declared in frontmatter (systemic across all commands) | -5 |
| 2 | commands/save.md | No `allowed-tools` declared | -5 |
| 3 | commands/foresight.md | No `allowed-tools` declared | -5 |
| 4 | commands/recall.md | No `allowed-tools` declared | -5 |
| 5 | commands/nemp-pro-export.md | No `allowed-tools` declared | -5 |
| 6 | commands/activate.md | No `allowed-tools` declared | -5 |
| 7 | commands/init.md | No `allowed-tools` declared | -5 |
| 8 | commands/log.md | No `allowed-tools` declared | -5 |
| 9 | commands/recall-global.md | No `allowed-tools` declared | -5 |
| 10 | commands/health.md | No `allowed-tools` declared | -5 |
| 11 | commands/export.md | No `allowed-tools` declared | -5 |
| 12 | commands/import.md | No `allowed-tools` declared | -5 |
| 13 | commands/auto-sync.md | No `allowed-tools` declared | -5 |
| 14 | commands/forget.md | No `allowed-tools` declared | -5 |
| 15 | commands/activity.md | No `allowed-tools` declared | -5 |
| 16 | commands/save-global.md | No `allowed-tools` declared | -5 |
| 17 | commands/decay.md | No `allowed-tools` declared | -5 |
| 18 | commands/cortex.md | No `allowed-tools` declared | -5 |
| 19 | commands/context.md | No `allowed-tools` declared | -5 |
| 20 | commands/list.md | No `allowed-tools` declared | -5 |
| 21 | commands/sync.md | No `allowed-tools` declared | -5 |
| 22 | commands/list-global.md | No `allowed-tools` declared | -5 |
| 23 | commands/auto-export.md | No `allowed-tools` declared | -5 |
| 24 | commands/auto-capture.md | No `allowed-tools` declared | -5 |
| 25 | commands/suggest.md | Excessive vague quantifiers: "intelligent", "smart", "actionable", "useful", "beautiful", "meaningful", "valuable", "significant", "relevant" — >10 distinct instances | -20 (capped) |
| 26 | commands/context.md | Vague quantifiers: "intelligent", "smart", "beautiful", "relevant" — 7 instances | -14 |
| 27 | skills/nemp-memory/SKILL.md | Entire body uses backslash-escaped markdown (`\#`, `\*\*`, `\_`) which renders as literal backslashes in most parsers instead of formatted headings and emphasis | -7 |
| 28 | SKILL.md | Root SKILL.md has valid frontmatter but an empty body — no skill reference content beyond the 5-line frontmatter block | -10 |
| 29 | commands/forget.md | Duplicate step numbering: two separate "### 7." headings appear in sequence (steps 1–6, then 7, 8, then another 7) | -2 |
| 30 | commands/sync.md | Minor vague terms: "clean, professional", "relevant" | -6 |

## Cross-Component
**Version drift**: `.claude-plugin/plugin.json` declares `version: "0.3.0"` but `.claude-plugin/marketplace.json` declares `version: "0.1.0"` — these must match for correct marketplace indexing.

**Stale command count**: `CLAUDE.md` structure value records `"commands/ (20 .md files)"` but the directory contains 24 command `.md` files (added since last `nemp:init` run that generated this entry). Running `/nemp:init` or `/nemp:export` will refresh this.

**Pro command namespace confusion**: `commands/export.md` (Nemp Pro section) and `commands/activate.md` (Step 4 confirmation) both reference Pro features using the `/nemp:export` namespace with `--codex/--cursor/--windsurf/--all` flags, but the actual Pro commands live under `/nemp-pro:export`. This contradicts `commands/nemp-pro-export.md` which correctly defines the `/nemp-pro:export` namespace. Users reading either of the two affected files will attempt unavailable command forms.

**Unrecognized frontmatter key**: `SKILL.md` (root) contains `metadata: {"openclaw": {"always": true}}`. `openclaw` is not a Claude Code skill schema field — it appears to be a cross-platform compatibility marker for another AI coding tool. Claude Code will silently ignore this key, but it may emit parser warnings in strict environments.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

Priority order:
1. Fix Pro command namespace in `commands/export.md` and `commands/activate.md` (high user-facing impact)
2. Fix `marketplace.json` version to `0.3.0`
3. Run `/nemp:export` or update `CLAUDE.md` structure count to 24
4. Add `allowed-tools` declarations to all command files (systemic quality improvement)
5. Fix backslash-escaping in `skills/nemp-memory/SKILL.md`
6. Consider narrowing hook trigger from `Edit|Write|Bash` to `Write` for efficiency
