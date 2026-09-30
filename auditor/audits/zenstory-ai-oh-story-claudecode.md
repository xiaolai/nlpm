# NLPM Audit: zenstory-ai/oh-story-claudecode
**Date**: 2026-04-06  |  **Artifacts**: 58  |  **Strategy**: batched
**NL Score**: 89/100
**Security**: REVIEW
**Bugs**: 0  |  **Quality Issues**: 7  |  **Security Findings**: 6

> Method note: scores come from a structural scan of frontmatter (name/description/model/tools), example blocks and quantifier grep across all 58 artifacts, plus full reads of a sample of agents and AGENTS.md. Per-file scores are estimates; none is backed by a full line-by-line read of every file.

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/story-setup/references/opencode/agents/{character-designer,chapter-extractor,consistency-checker,story-architect,story-explorer,narrative-writer,story-researcher}.md (7 files) | agent (OpenCode) | 80 | No example blocks (-15); no model declared (-5) |
| skills/story-setup/references/templates/agents/{chapter-extractor,consistency-checker,story-explorer,story-architect,character-designer}.md (5 files) | agent | 85 | No example blocks (-15) |
| skills/story-setup/references/templates/agents/{narrative-writer,story-researcher}.md (2 files) | agent | 95 | Only one example; description names no "not for" situation (-5) |
| skills/story-setup/references/opencode/commands/*.md (13 files) | command (OpenCode) | 90 | No allowed-tools (-5), no visible empty-input handling (-5) |
| skills/story-setup/references/zcode/commands/*.md (13 files) | command (ZCode) | 90 | No allowed-tools (-5), no visible empty-input handling (-5) |
| skills/*/SKILL.md (13 files) | skill | 95 | No allowed-tools declared; very long descriptions (story-short-analyze, story-long-analyze) |
| skills/story-setup/references/{antigravity,codex,zcode}/hooks/hooks.json (3 files) | config | 100 | Not an NL artifact; scored in Security |
| CLAUDE.md | config | 100 | Imports AGENTS.md only |
| .claude-plugin/plugin.json | manifest | 95 | No skills array (relies on auto-discovery) |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 6 |
| Low | 0 |

The pre-scan flagged 2 Critical pattern matches. Triage found the matching lines are `eval` and `shell=True` in repo-owned test scripts. They run fixed strings read from this repo's own hooks.json or docs, with no network or user input. They are recorded as false positives and kept out of the Critical count.

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | skills/story-setup/references/antigravity/hooks/hooks.json, skills/story-setup/references/codex/hooks/hooks.json, skills/story-setup/references/zcode/hooks/hooks.json |
| Hook scripts | skills/story-setup/references/templates/hooks/story_hook_core.js, skills/story-setup/references/opencode/story_hook_core.js (use child_process.spawnSync) |
| Scripts | scripts/ (158 files: test-*, check-*, bench/*, sync-opencode.py) |
| MCP configs | none |
| Package manifests | package.json, package-lock.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | medium | scripts/test-charcount-portable.sh | 68 | eval with variable (false positive) | `eval "$COUNT_BLOCK"` in a test; the command block is extracted from repo docs. |
| 2 | medium | scripts/test-codex-hooks.sh | 357 | eval with variable (false positive) | `eval "$launcher_cmd"`, where the command comes from the repo's own codex hooks.json. |
| 3 | medium | scripts/test-codex-hooks.sh | 395 | subprocess shell=True (false positive) | Python test runs the hooks.json command with a fixed payload. |
| 4 | medium | scripts/test-codex-hooks.sh | 413 | eval with variable (false positive) | Same pattern as #2. |
| 5 | medium | skills/story-setup/references/codex/hooks/hooks.json | 12 | powershell -ExecutionPolicy Bypass | `commandWindows` hooks bypass the execution policy and walk up parent directories to find `.codex/hooks/run-story-hook.cmd`. A launcher planted in a parent directory would run. |
| 6 | medium | skills/story-setup/UPGRADING.md | 69 | curl piped to bash (documentation) | Docs suggest `curl -fsSL https://opencode.ai/v2/install \| bash` as an upgrade option. It is not executed by the plugin. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
No bugs found. plugin.json has no `skills` array, and all 13 skill directories carry SKILL.md with name and description.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/story-setup/references/*/hooks/hooks.json | Parent-directory launcher walk plus ExecutionPolicy Bypass | Stop the walk at the git root or the project dir, and drop `-ExecutionPolicy Bypass` if a signed or in-repo launcher is possible. |
| 2 | skills/story-setup/UPGRADING.md | curl-pipe-bash install suggestion | Point to the official docs or a checksum-verified download. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/story-setup/references/templates/agents/ (5 of 7 agents) | No example blocks | -15 each |
| 2 | skills/story-setup/references/opencode/agents/*.md (7 files) | No example blocks | -15 each |
| 3 | skills/story-setup/references/opencode/agents/*.md (7 files) | No `model` declared | -5 each |
| 4 | skills/story-setup/references/{opencode,zcode}/commands/*.md (26 files) | No allowed-tools | -5 each |
| 5 | skills/story-setup/references/templates/agents/{narrative-writer,story-researcher}.md | Description names no situation the agent is not for | -5 each |
| 6 | skills/story-short-analyze/SKILL.md, skills/story-long-analyze/SKILL.md | Very long descriptions (trigger lists) | -2 each |
| 7 | skills/*/SKILL.md | No allowed-tools declared | -2 each |

## Cross-Component
- plugin.json says "13 Skills" and 13 skill directories exist, so the count is consistent.
- The OpenCode agents have no `name` field. OpenCode derives the name from the filename, so this is not a bug there.
- The OpenCode and ZCode commands are generated from the skills (sync-opencode.py), so they drift only if regeneration is skipped.
- CLAUDE.md is `@AGENTS.md`, which is consistent.

## Recommendation
REVIEW — submit NL fix PRs, flag security findings in issue. The Critical pattern matches are false positives (test scripts run repo-controlled strings). The remaining Medium items are hook launcher hardening and a docs suggestion.
