# NLPM Audit: leowux/pony
**Date**: 2026-04-06  |  **Artifacts**: 10  |  **Strategy**: single
**NL Score**: 91/100
**Security**: CLEAR
**Bugs**: 1  |  **Quality Issues**: 15  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/task.md | command | 75 | No output format, no empty-input handling, no allowed-tools |
| commands/run.md | command | 83 | No output format, no allowed-tools, "appropriate" vague |
| commands/hud.md | command | 85 | No output format, no allowed-tools |
| commands/init.md | command | 85 | No output format, no allowed-tools |
| agents/explorer.md | agent | 93 | No concrete invocation examples, "relevant" vague quantifier |
| agents/executor.md | agent | 95 | No concrete invocation examples |
| agents/planner.md | agent | 95 | No concrete invocation examples |
| agents/verifier.md | agent | 95 | No concrete invocation examples |
| CLAUDE.md | docs | 100 | None |
| .claude-plugin/plugin.json | manifest | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 3 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | None found |
| Scripts | None found |
| MCP configs | None found |
| Package manifests | package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Low | package.json | 54 | SEC-unpinned-semver | `vite-plus: "latest"` — floating `latest` tag allows any future version to be installed automatically, including breaking or malicious updates |
| 2 | Low | package.json | 43–46 | SEC-unpinned-semver | Production dependencies `chalk ^5.3.0`, `commander ^12.0.0`, `zod ^3.22.0` use semver ranges; minor/patch updates install automatically |
| 3 | Low | package.json | 60–62 | SEC-unpinned-semver | `publishConfig.registry` points to internal Alipay registry (`registry.antgroup-inc.cn`); external consumers cannot install via standard npm and may have no visibility into published versions |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/run.md | Uses `Agent` tool in the Implementation section but `Agent` is not declared in `allowed-tools` frontmatter | Claude Code may deny the Agent call at runtime if tool allowances are enforced; the default pipeline (planner → executor → verifier) cannot execute |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | package.json | `vite-plus: "latest"` is a floating version tag | Pin to an exact version (e.g. `"0.1.15"`) or at minimum a semver range (`"^0.1.15"`) |
| 2 | package.json | `chalk`, `commander`, `zod` use `^` ranges | Consider pinning to exact versions in a lockfile-verified workflow; already mitigated if `pnpm-lock.yaml` is committed |
| 3 | package.json | Private Alipay registry in `publishConfig` makes the package invisible to external npm consumers | If the package is intended to be public (GitHub repo is public), publish to the public npm registry |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/executor.md | Missing concrete invocation examples — `<Output_Format>` is a template, not an input→output demonstration | -5 |
| 2 | agents/explorer.md | Missing concrete invocation examples | -5 |
| 3 | agents/explorer.md | Vague quantifier "relevant" in Success Criteria ("ALL relevant matches found") | -2 |
| 4 | agents/planner.md | Missing concrete invocation examples | -5 |
| 5 | agents/verifier.md | Missing concrete invocation examples | -5 |
| 6 | commands/hud.md | No `allowed-tools` declared; Claude would need Bash to invoke `pony hud *` commands | -5 |
| 7 | commands/hud.md | No output format specified for Claude's response after running HUD commands | -10 |
| 8 | commands/init.md | No `allowed-tools` declared; Bash is needed to run `pony init` | -5 |
| 9 | commands/init.md | No output format specified | -10 |
| 10 | commands/run.md | No `allowed-tools` declared (Agent tool is used but undeclared — see Bugs) | -5 |
| 11 | commands/run.md | No output format specified for the orchestration loop | -10 |
| 12 | commands/run.md | Vague quantifier "appropriate" in Workflow step 5 ("Use Agent tool with appropriate subagent_type") | -2 |
| 13 | commands/task.md | No `allowed-tools` declared; Bash needed for `pony *` CLI commands | -5 |
| 14 | commands/task.md | No output format specified | -10 |
| 15 | commands/task.md | No empty-input handling — argument-hint requires `<add\|list\|get\|update\|delete\|next>` but the command body does not specify what Claude should do when invoked with no arguments | -10 |

## Cross-Component
- **Agent coverage**: All four agents referenced by `commands/run.md` (`pony:planner`, `pony:explorer`, `pony:executor`, `pony:verifier`) have corresponding agent files. References are consistent.
- **Undeclared tool — executor.md**: `<Tool_Usage>` lists `TaskCreate/TaskUpdate/TaskList` as tools, but these are not declared in `plugin.json` and do not match any standard Claude Code built-in tool names. If these are pony-plugin-specific tools exposed via the Claude Code tool API, their registration is absent from the plugin manifest. If they are intended to be Claude's internal `TodoWrite`/`TodoRead` tools, the naming is incorrect and will silently fail.
- **Repository URL mismatch**: `plugin.json` lists `"url": "git@code.alipay.com:wuwenbang.wwb/pony.git"` (Alipay internal Git) while `package.json` lists `"repository": "git@github.com:leowux/pony.git"` (public GitHub). These are different repositories; plugin.json should be updated to point to the canonical public repository.
- **CLAUDE.md references hooks/hooks.json** in its restrictions table, but no `hooks/` directory or `hooks.json` file exists in the repository. The documentation is correct (it says not to add `"hooks"` to plugin.json), but the existence reference may confuse contributors.

## Recommendation
CLEAR — submit PRs for the one bug (run.md missing `allowed-tools: [Agent]`) and the three Low security fixes. The agent suite is well-structured with good model selection and role separation; the main gap is the absence of concrete example blocks and output format declarations in command files.
