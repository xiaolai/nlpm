# NLPM Audit: astral-sh/claude-code-plugins
**Date**: 2026-04-06  |  **Artifacts**: 4  |  **Strategy**: single
**NL Score**: 97/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 4  |  **Security Findings**: 1

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| plugins/astral/skills/uv/SKILL.md | skill | 95 | Vague "clearly needed" (line 84); redundant double "only" (line 71) |
| plugins/astral/.claude-plugin/plugin.json | plugin manifest | 97 | @latest unpinned in lspServers (LOW security) |
| plugins/astral/skills/ruff/SKILL.md | skill | 97 | Borderline vague "quick" (line 34) |
| plugins/astral/skills/ty/SKILL.md | skill | 97 | Borderline vague "quick" (line 26) |

**Weighted average**: (95 + 97 + 97 + 97) / 4 = **96.5 → 97/100**

All three SKILL.md files carry well-formed YAML frontmatter (`name`, `description`), rich code-block examples covering the full command surface, and clear "When to use / When not to use" sections. The plugin.json manifest is minimal but complete; skill auto-discovery via the `skills/` directory tree makes an explicit `skills` array unnecessary in Claude Code.

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | None |
| Shell scripts | None |
| Python scripts | None |
| MCP configs (.mcp.json) | None |
| Package manifests (package.json / requirements.txt) | None |
| Plugin manifest | plugins/astral/.claude-plugin/plugin.json |
| Marketplace manifest | .claude-plugin/marketplace.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Low | plugins/astral/.claude-plugin/plugin.json | 27 | SEC-unpinned-semver | lspServers command argument `ty@latest` resolves to whatever is newest on PyPI at LSP-server startup time; a breaking or compromised release would auto-deploy to all plugin users |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No bugs found | — |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | plugins/astral/.claude-plugin/plugin.json | lspServers `ty@latest` unpinned | Pin to a specific released version, e.g. `ty==0.0.0-alpha.6`, and update alongside release notes |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | plugins/astral/skills/uv/SKILL.md | Line 84: "unless clearly needed" — "clearly" is a vague condition; should specify concrete signals (e.g. "unless a requirements.txt exists and no uv.lock is present") | −2 |
| 2 | plugins/astral/skills/uv/SKILL.md | Line 71: "Only use `uv tool install` only when…" — double "only" is a copy-editing redundancy | −1 (informational) |
| 3 | plugins/astral/skills/ruff/SKILL.md | Line 34: "quick one-off checks" — "quick" is borderline vague; acceptable colloquial usage but could be "ad-hoc checks outside a project" | −1 (low confidence) |
| 4 | plugins/astral/skills/ty/SKILL.md | Line 26: same "quick one-off checks" pattern as ruff | −1 (low confidence) |

## Cross-Component
- **marketplace.json → plugin**: `./plugins/astral` source path resolves correctly on disk. ✓
- **plugin.json ↔ ty SKILL.md**: plugin.json registers the `ty` LSP server; ty SKILL.md accurately states "This plugin automatically configures the ty language server." Consistent. ✓
- **plugin.json ↔ ruff / uv SKILL.md**: Neither ruff nor uv claims LSP configuration, matching the absence of their entries in `lspServers`. ✓
- **Skill auto-discovery**: `skills/ruff/SKILL.md`, `skills/ty/SKILL.md`, `skills/uv/SKILL.md` all reside under `plugins/astral/skills/` — Claude Code's auto-discovery path — so no explicit `skills` array is required in `plugin.json`. ✓
- **No orphaned components, stale counts, or broken relative paths detected.**

## Recommendation
CLEAR — submit a PR to pin the `ty` LSP server version in `plugin.json` (LOW security finding). The three SKILL.md files are high-quality references; the quality issues above are informational and do not warrant separate PRs.
