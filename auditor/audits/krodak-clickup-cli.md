# NLPM Audit: krodak/clickup-cli
**Date**: 2026-04-06  |  **Artifacts**: 4  |  **Strategy**: single
**NL Score**: 95/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 3  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `.claude-plugin/plugin.json` | Plugin manifest | 90/100 | No `entries`/`skills` listing; automation cannot enumerate provided surfaces |
| `.agents/skills/testing-clickup-cli/SKILL.md` | Skill | 95/100 | "edge cases" in step guidance is marginally vague |
| `.agents/skills/releasing-clickup-cli/SKILL.md` | Skill | 97/100 | None significant |
| `skills/clickup-cli/SKILL.md` | Skill | 97/100 | None significant |

**Weighted average**: (90 + 95 + 97 + 97) / 4 = **95/100**

### Per-file notes

**`.agents/skills/releasing-clickup-cli/SKILL.md`** — 97/100
All frontmatter present. Nine numbered steps, concrete bash examples at every step, no vague language. Minor non-standard `metadata.internal: true` field does not affect scoring. The pre-release checklist and "common mistakes" section are genuinely useful. One point of interest: step 9 copies the skill to `~/.config/opencode/skills/clickup/SKILL.md` (OpenCode path), which is correct for multi-tool distribution and not a defect.

**`.agents/skills/testing-clickup-cli/SKILL.md`** — 95/100
Frontmatter complete, `metadata.internal: true` present. Well-organized: suite overview table, exact run commands, E2E workspace fixture inventory, unit test patterns with working TypeScript examples. The phrase "happy path, error cases, edge cases" in the new-unit-test steps is standard testing vocabulary rather than genuinely vague; 2-point deduction applied conservatively.

**`.claude-plugin/plugin.json`** — 90/100
Valid JSON, all standard manifest fields present (`name`, `description`, `version`, `author`, `homepage`, `repository`, `license`). No `entries`, `commands`, or `skills` array to enumerate what the plugin exposes. Claude's plugin loader likely discovers skills by filesystem convention, so this is not a registration blocker — but it prevents automation tooling from enumerating surfaces without a filesystem scan. 10-point quality deduction.

**`skills/clickup-cli/SKILL.md`** — 97/100
Frontmatter complete. Stands out as an exemplary reference skill: `Output Modes` section explicitly documents TTY vs. piped behavior, `Global Flags` and `Flags & Conventions` tables are thorough, `Agent Workflow Examples` section groups concrete multi-command flows by task type, and a `DELETE SAFETY` block at the end reinforces irreversible operation handling. No vague quantifiers found.

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
| Hooks | None |
| Scripts (sh/py/js) | None |
| MCP configs | None |
| Package manifests | `package.json` |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Low | `package.json` | 48 | SEC-unpinned-semver | Production dep `@inquirer/prompts: "^8.3.0"` uses caret range; minor-version updates are auto-applied on fresh installs |
| 2 | Low | `package.json` | 49 | SEC-unpinned-semver | Production dep `chalk: "^5.6.2"` uses caret range |
| 3 | Low | `package.json` | 50 | SEC-unpinned-semver | Production dep `commander: "^14.0.3"` uses caret range |

All three production dependencies use `^` (caret) ranges. `devDependencies` are similarly unpinned but carry lower risk as they are never shipped to end-users. No `postinstall` or `preinstall` scripts are present; the only lifecycle hook is `prepublishOnly` which runs the standard typecheck → lint → test → build chain and is not exploitable.

## Bugs (PR-worthy)
No bugs found. All NL artifacts have complete required frontmatter; no broken internal references; no undeclared tool usage.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `package.json` | Production deps use `^` semver ranges, allowing unexpected minor-version updates on install | Pin to exact versions (remove `^`) or use `npm shrinkwrap` / lock-file-only distribution |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `.claude-plugin/plugin.json` | No `entries`, `commands`, or `skills` array; automation cannot enumerate plugin surfaces without a filesystem scan | -10 |
| 2 | `skills/clickup-cli/SKILL.md` | Skill `name` field is `clickup` while the package/repo name is `clickup-cli`; may cause confusion for users loading the skill by name | informational (0) |
| 3 | `.agents/skills/testing-clickup-cli/SKILL.md` | Step 3 in "New unit test" section says "Test happy path, error cases, edge cases" — "edge cases" is marginally vague without examples of what counts as an edge case for this codebase | -2 |

## Cross-Component
**Version sync** — ✅ `.claude-plugin/plugin.json` version `1.25.2` matches `skills/clickup-cli/SKILL.md` version header `1.25.2` and `package.json` version `1.25.2`. The sync script described in `releasing-clickup-cli/SKILL.md` (step 3) enforces this automatically.

**Path references** — ✅ `releasing-clickup-cli/SKILL.md` references `.claude-plugin/plugin.json`, `skills/clickup-cli/SKILL.md`, `docs/commands.md`, and `scripts/sync-command-docs.ts`. All paths are plausible and consistent with the repo layout.

**Name drift** — The `skills/clickup-cli/SKILL.md` frontmatter uses `name: clickup` while the package, plugin manifest, and directory all use `clickup-cli`. This is a minor terminology inconsistency. It is likely intentional (agent loads the skill under the short name `clickup`) but warrants a code comment or documentation note.

**Internal flag** — Both `.agents/skills/` files carry `metadata.internal: true`. This field is non-standard in known Claude plugin schemas. If the Claude plugin loader ignores unknown metadata, this is harmless; if it gates loading, it could silently suppress the skills. Not a confirmed bug, but worth verifying against the platform schema.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

No Critical or High security findings. Zero NL bugs. The three LOW security findings (unpinned semver on production deps) are suitable for a public fix PR: pin `@inquirer/prompts`, `chalk`, and `commander` to exact versions in `package.json`. The quality issues are informational and do not require a PR unless the maintainer agrees with the `plugin.json` entries proposal.
