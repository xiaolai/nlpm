# NLPM Audit: fivetaku/gptaku_plugins
**Date**: 2026-04-06  |  **Artifacts**: 4  |  **Strategy**: single
**NL Score**: 96/100
**Security**: BLOCKED
**Bugs**: 0  |  **Quality Issues**: 3  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| plugins/insane-crawl/commands/insane-crawl.md | command | 90 | No empty-input handling; `$ARGUMENTS` passed unquoted to shell |
| CLAUDE.md | project instructions | 96 | Hardcoded absolute path `/Users/chulrolee/...` |
| plugins/insane-crawl/.claude-plugin/plugin.json | manifest | 100 | None |
| plugins/insane-crawl/skills/insane-crawl/SKILL.md | skill | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 3 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none |
| Scripts (plugin engine) | plugins/insane-crawl/skills/insane-crawl/engine/*.py (13 modules) plus tests/ |
| Scripts (repo tooling) | scripts/plugin-release.sh, shared/update-hook/migrate-to-setup.sh, tools/*.py, docs/landing/*.py, site/assets/site.js |
| MCP configs | none |
| Package manifests | none found |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | plugins/insane-crawl/commands/insane-crawl.md | 15 | Bash + unsanitized `$ARGUMENTS` | User arguments are interpolated unquoted into `python3 -m engine $ARGUMENTS` with Bash allowed, so shell metacharacters can inject commands. |
| 2 | Medium | plugins/insane-crawl/skills/insane-crawl/engine/discovery.py | 43 | subprocess.run + env override | Runs an endpoint-miner script located via `INSANE_SEARCH_ENDPOINT_MINER` / `INSANE_SEARCH_SKILL_ROOT` env vars (lines 90-92); list-form args, no shell=True. |
| 3 | Medium | plugins/insane-crawl/skills/insane-crawl/engine/fetcher.py | 79-116 | env access, sys.path insert, dynamic import | Loads a module from an env-controlled path via importlib and sets `INSANE_ALLOW_PRIVATE=1`. |
| 4 | Medium | plugins/insane-crawl/skills/insane-crawl/engine/browser_capture.py | 82 | subprocess.run + env override | Launches a browser worker with a Python interpreter taken from `INSANE_CRAWL_CLOAK_PYTHON` (line 103). |

The engine's network fetching is the crawler's stated purpose and is not counted separately.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
No NL bugs found.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | plugins/insane-crawl/skills/insane-crawl/engine/fetcher.py | Env-controlled module path is imported | Validate that the override path is inside the plugin or the known insane-search install before importing it. |
| 2 | plugins/insane-crawl/skills/insane-crawl/engine/browser_capture.py | Interpreter path taken from env | Check that the override exists and is executable, and log it visibly. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | plugins/insane-crawl/commands/insane-crawl.md | No handling for empty `$ARGUMENTS` (R-empty-input) | -10 |
| 2 | CLAUDE.md | Hardcoded user-specific absolute path in Step 3 | -2 |
| 3 | CLAUDE.md | Long operational checklist with no explicit output format | -2 |

## Cross-Component
- The command and SKILL.md agree on the CLI entrypoint (`python3 -m engine`, run from `skills/insane-crawl`), and the `engine/` module exists.
- SKILL.md documents `crawl`, `status`, `resume`, `results`, `page`, `events` and `cancel`. The command's argument-hint also lists `fetch` and `discover`, which SKILL.md does not document for `fetch`. This is low-confidence drift.
- `discover` depends on the separate `insane-search` plugin, which plugin.json does not declare.

## Recommendation
BLOCKED — do not submit PRs. File private security report. (One High finding: unsanitized `$ARGUMENTS` passed to Bash. Medium items may be raised publicly once that is resolved.)
