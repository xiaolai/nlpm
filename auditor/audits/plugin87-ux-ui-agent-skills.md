# NLPM Audit: plugin87/ux-ui-agent-skills
**Date**: 2026-04-06  |  **Artifacts**: 29  |  **Strategy**: batched
**NL Score**: 98/100
**Security**: REVIEW
**Bugs**: 0  |  **Quality Issues**: 11  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/agents/design-critic.md | agent | 85 | No example blocks (-15) |
| templates/product-design/.claude/commands/gate.md | command | 85 | Multi-step checks without numbered steps (-10); no allowed-tools (-5) |
| .claude/commands/critique.md | command | 95 | No allowed-tools |
| .claude/commands/ship.md | command | 95 | No allowed-tools |
| .claude/commands/grill-me.md | command | 95 | No allowed-tools |
| .claude/commands/gate.md | command | 95 | No allowed-tools |
| .claude/commands/scaffold-project.md | command | 95 | No allowed-tools |
| .claude/skills/design-tokens/SKILL.md | skill | 98 | Vague quantifier "relevant" (line 13) |
| .claude/skills/governance/SKILL.md | skill | 98 | Vague quantifier "relevant" (line 16) |
| CLAUDE.md | project doc | 98 | Vague quantifier "relevant" |
| .claude/skills/design-doctrine/SKILL.md | skill | 100 | None found |
| .claude/skills/figma-integration/SKILL.md | skill | 100 | None found |
| .claude/skills/prototype/SKILL.md | skill | 100 | None found |
| .claude/skills/data-dashboard/SKILL.md | skill | 100 | None found |
| .claude/skills/token-build/SKILL.md | skill | 100 | None found |
| .claude/skills/a11y-audit/SKILL.md | skill | 100 | None found |
| .claude/skills/design-review/SKILL.md | skill | 100 | None found |
| .claude/skills/design-qa/SKILL.md | skill | 100 | None found |
| .claude/skills/design-code/SKILL.md | skill | 100 | None found |
| .claude/skills/migrate-design-system/SKILL.md | skill | 100 | None found |
| .claude/skills/redesign/SKILL.md | skill | 100 | None found |
| .claude/skills/image-to-code/SKILL.md | skill | 100 | None found |
| .claude/skills/ux-writing/SKILL.md | skill | 100 | None found |
| .claude/skills/design-component/SKILL.md | skill | 100 | None found |
| .claude/skills/apply-aesthetic/SKILL.md | skill | 100 | None found |
| .claude/skills/brandkit/SKILL.md | skill | 100 | None found |
| .claude/skills/performance/SKILL.md | skill | 100 | None found |
| templates/product-design/CLAUDE.md | project doc | 100 | None found |
| .claude-plugin/plugin.json | manifest | 100 | None found |

Note: the 17 skills at 100 were checked for frontmatter and vague-language grep hits; their bodies were not read line by line.

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
| Hooks | none |
| Scripts (Python) | scripts/*.py (13 files), tests/unit/python_units.py |
| Scripts (Node) | bin/cli.js, scripts/*.mjs, examples/component-states/icons.js, evals/out/blind-2026-08-25/*/*.js |
| MCP configs | templates/product-design/.mcp.json |
| Package manifests | package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | templates/product-design/.mcp.json | 6 | npx -y unpinned package | `figma-developer-mcp` is fetched and run via `npx -y` with no version pin, and receives FIGMA_API_KEY. |
| 2 | Medium | templates/product-design/.mcp.json | 13 | npx -y unpinned package | `@notionhq/notion-mcp-server` is fetched and run via `npx -y` with no version pin, and receives NOTION_API_KEY. |
| 3 | Low | bin/cli.js | 177 | child_process.spawn | Spawns an OS opener with a local path; `shell: true` only on win32; no user-controlled input. |
| 4 | Low | package.json | 57 | unpinned-semver | devDependency `playwright` uses `^1.40.0`. |

No critical or high patterns found: no shell=True, os.system, eval, curl piped to shell, sudo, postinstall scripts, or hooks. Secrets in `.mcp.json` use `${VAR}` expansion, not literals.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| - | - | No NL bugs found. plugin.json commands, agents and skills paths all resolve on disk; all 19 skills have name and description. | - |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | templates/product-design/.mcp.json | Unpinned npx packages carrying API keys | Pin versions, e.g. `figma-developer-mcp@<version>` |
| 2 | package.json | Caret range on playwright | Optional: pin exact or rely on a lockfile |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/agents/design-critic.md | No example blocks in description | -15 |
| 2 | .claude/commands/critique.md | No allowed-tools | -5 |
| 3 | .claude/commands/ship.md | No allowed-tools | -5 |
| 4 | .claude/commands/grill-me.md | No allowed-tools | -5 |
| 5 | .claude/commands/gate.md | No allowed-tools | -5 |
| 6 | .claude/commands/scaffold-project.md | No allowed-tools | -5 |
| 7 | templates/product-design/.claude/commands/gate.md | No allowed-tools | -5 |
| 8 | templates/product-design/.claude/commands/gate.md | Multi-step checks under headings, not numbered steps | -10 |
| 9 | .claude/skills/design-tokens/SKILL.md | Vague quantifier "relevant" | -2 |
| 10 | .claude/skills/governance/SKILL.md | Vague quantifier "relevant" | -2 |
| 11 | CLAUDE.md | Vague quantifier "relevant" | -2 |

## Cross-Component
- Every script referenced by the commands and the critic agent exists under `scripts/`.
- `design-critic` is referenced by `/critique` and registered in plugin.json. No orphan agent.
- plugin.json lists all 5 commands in `.claude/commands/` and the skills directory. The template `gate.md` ships as a template and is intentionally not registered.
- Counts are consistent: 19 skill directories, and package.json says "19 runnable skills".
- Skills use a non-standard `invocation:` frontmatter key (model/user). It is informational only, not a registration bug.

## Recommendation
REVIEW — no NL bugs found and no Critical/High security findings. Medium findings are unpinned `npx -y` MCP servers in the shipped template. Flag them in an issue, and submit a pin-versions PR if desired.
