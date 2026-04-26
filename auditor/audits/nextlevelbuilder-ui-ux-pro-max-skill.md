# NLPM Audit: nextlevelbuilder/ui-ux-pro-max-skill
**Date**: 2026-04-26  |  **Artifacts**: 9  |  **Strategy**: single
**NL Score**: 85/100
**Security**: CLEAR
**Bugs**: 2  |  **Quality Issues**: 7  |  **Security Findings**: 6

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/skills/slides/SKILL.md | skill | 78 | Stale template artifact `<args>$ARGUMENTS</args>` at line 14; thin content |
| .claude/skills/design/SKILL.md | skill | 82 | References 6+ external skills not bundled in this plugin |
| .claude/skills/brand/SKILL.md | skill | 83 | Pure routing with no workflow guidance; missing output format |
| .claude/skills/ui-ux-pro-max/SKILL.md | skill | 86 | Missing `ckm:` prefix; stale "React Native only" claim |
| .claude/skills/design-system/SKILL.md | skill | 87 | Well-structured; minor external script dependency assumptions |
| .claude/skills/ui-styling/SKILL.md | skill | 87 | Strong content; vague quality descriptors ("museum-quality") |
| .claude/skills/banner-design/SKILL.md | skill | 88 | References 4 external skills not in this plugin |
| CLAUDE.md | project guide | 88 | Good technical reference; paths assume specific install structure |
| .claude-plugin/plugin.json | manifest | 90 | Count mismatch vs SKILL.md (67 styles/15 stacks stated vs 50+/10 documented) |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 3 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Python scripts | 18 (across .claude/skills/ and src/, cli/assets/) |
| JavaScript/CJS scripts | 7 (brand, design-system CJS utilities) |
| TypeScript CLI | 8 (cli/src/**/*.ts) |
| MCP configs | 0 |
| Package manifests | cli/package.json, .claude/skills/ui-styling/scripts/requirements.txt |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | .claude/skills/brand/scripts/sync-brand-to-tokens.cjs | 253 | execSync-template-string | `execSync` called with a backtick template string containing path variables. All three variables are hardcoded constants so there is no current injection risk, but the pattern is fragile — any future variable substitution with user input would create shell injection. |
| 2 | Medium | .claude/skills/ui-styling/scripts/shadcn_add.py | 101 | unpinned-runtime-install | `subprocess.run(["npx", "shadcn@latest", "add"] + components)` uses `@latest` without a version pin, so each run silently downloads whatever version is current on npm. List-form subprocess prevents shell injection, but the package itself is unverified at runtime. |
| 3 | Medium | cli/src/utils/github.ts | 72 | network-download-install | `downloadRelease()` fetches a ZIP from GitHub releases and writes it to disk; `init.ts` then extracts and copies the contents into the user's project. No checksum verification is performed — a compromised release asset would be silently installed. |
| 4 | Low | .claude/skills/design-system/scripts/fetch-background.py | 142 | external-url-hardcoded | 20 hardcoded Pexels image URLs are embedded in `CURATED_IMAGES`. At runtime the script references these URLs directly; no integrity checking or caching. The URLs are from a reputable CDN, but changes to the CDN paths would silently break the feature. |
| 5 | Low | cli/package.json | 36 | SEC-unpinned-semver | All four runtime dependencies (`commander ^12.1.0`, `chalk ^5.3.0`, `ora ^8.1.1`, `prompts ^2.4.2`) use caret ranges, allowing minor/patch-level updates without a lockfile pin. Supply chain drift is possible over time. |
| 6 | Low | .claude/skills/ui-styling/scripts/requirements.txt | 4 | SEC-unpinned-semver | Dev dependencies use `>=` floor constraints with no upper bound (`pytest>=8.0.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.12.0`). Any future breaking major version would be silently pulled in. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .claude/skills/slides/SKILL.md | Line 14 contains raw template variable `<args>$ARGUMENTS</args>` that was never substituted — likely a copy-paste artifact from a template generator. Renders as literal XML-like text in the skill body. | Claude Code will include this tag as part of the skill content, potentially confusing the LLM or downstream parsers. |
| 2 | .claude-plugin/plugin.json | Description claims "67 styles, 15 stacks" but the primary SKILL.md self-reports "50+ styles, 10 stacks". The listed stacks total 12, not 15. | Misleading marketplace description; users expect 67 styles and 15 stacks but the documented database is smaller. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | .claude/skills/brand/scripts/sync-brand-to-tokens.cjs | `execSync` with template string at line 253 | Replace with `execFileSync('node', [generateScript, '--config', DESIGN_TOKENS_JSON, '-o', DESIGN_TOKENS_CSS])` to eliminate the shell-expansion surface. |
| 2 | .claude/skills/ui-styling/scripts/shadcn_add.py | `npx shadcn@latest` without version pin | Pin to a specific version: `npx shadcn@2.x.y` or read the pinned version from `package.json`. |
| 3 | cli/src/utils/github.ts | Downloaded ZIP is not checksum-verified | Add SHA-256 verification: fetch the release's expected checksum from the GitHub API (`release.assets` metadata) and verify the downloaded buffer before writing to disk. |
| 4 | cli/package.json | All runtime deps use caret ranges | Pin to exact versions in `package.json` or enforce via `package-lock.json` / `bun.lockb`. |
| 5 | .claude/skills/ui-styling/scripts/requirements.txt | Dev deps use unbounded `>=` | Change to exact pins (`pytest==8.x.y`) or add an upper bound (`pytest>=8.0,<9`). |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/skills/ui-ux-pro-max/SKILL.md | `name: ui-ux-pro-max` lacks the `ckm:` namespace prefix used by every other skill in this plugin (`ckm:banner-design`, `ckm:brand`, etc.). Causes inconsistent skill registration. | -5 |
| 2 | .claude/skills/ui-ux-pro-max/SKILL.md | Step 1 (line ~359) states "**Stack**: React Native (this project's only tech stack)" — a project-specific note that was left in a generic, published skill. The skill itself documents 10 stacks. | -4 |
| 3 | .claude/skills/design/SKILL.md | References six external skills not bundled in this plugin: `frontend-design`, `ai-artist`, `ai-multimodal`, `chrome-devtools`, `project-management`, `assets-organizing`. No fallback instructions if they are absent. | -5 |
| 4 | .claude/skills/brand/SKILL.md | Provides no workflow guidance — only a scripts table and a routing snippet. Missing output format, no examples of what the extracted brand context looks like. | -7 |
| 5 | .claude/skills/slides/SKILL.md | Thin content beyond routing: no examples of slide output, no direct workflow steps, no output format description. The entire value is deferred to `references/create.md` which is not in the plugin manifest. | -8 |
| 6 | .claude/skills/banner-design/SKILL.md | References model IDs `gemini-2.5-flash-image` and `gemini-3-pro-image-preview` in workflow code blocks. The latter (`gemini-3-pro`) is not a publicly confirmed model ID as of the audit date; may cause silent generation failures. | -3 |
| 7 | .claude/skills/design/SKILL.md | Banner and CIP workflow sections duplicate content already covered in the dedicated `banner-design` skill. If either file is updated independently the two will drift. | -4 |

## Cross-Component
**Count drift (plugin.json ↔ SKILL.md):** The marketplace description in `plugin.json` claims "67 styles, 15 stacks" while `ui-ux-pro-max/SKILL.md` documents "50+ styles, 10 stacks." Counting the stacks listed in `plugin.json` yields 12, not 15. The authoritative search CSV should be the source of truth; one of these needs to be reconciled.

**Naming convention drift:** All skills in the `skills` array use the `ckm:` namespace prefix (`ckm:brand`, `ckm:design-system`, etc.) except `ui-ux-pro-max/SKILL.md`, which declares `name: ui-ux-pro-max`. This will cause the skill to register under a different namespace than expected.

**Orphan external skill references:** `banner-design/SKILL.md` and `design/SKILL.md` both invoke workflows via `ai-artist`, `ai-multimodal`, `chrome-devtools`, `frontend-design`, `project-management`, and `assets-organizing` — none of which are declared in `plugin.json` or present in `.claude/skills/`. Users who install only this plugin will hit silent failures when those code paths are reached.

**Stale project-scope note in published skill:** `ui-ux-pro-max/SKILL.md` Step 1 contains "React Native (this project's only tech stack)" — this is residue from the maintainer's own project and was accidentally published. The skill is platform-agnostic; the note contradicts the rest of the file.

**Duplicate content between design/SKILL.md and banner-design/SKILL.md:** The banner workflow (steps 1–5, size reference table, top art styles, design rules) is fully reproduced in `design/SKILL.md`. Any update to one must be mirrored manually.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

Priority order:
1. **Bug fix:** Remove `<args>$ARGUMENTS</args>` from `slides/SKILL.md` line 14.
2. **Bug fix:** Reconcile `plugin.json` description counts with actual SKILL.md numbers.
3. **Security (Medium):** Replace `execSync` template string in `sync-brand-to-tokens.cjs` with `execFileSync` array form.
4. **Security (Medium):** Pin `npx shadcn@latest` to a specific version in `shadcn_add.py`.
5. **Security (Medium):** Add checksum verification to `cli/src/utils/github.ts` download flow.
6. **Quality:** Add `ckm:` prefix to `ui-ux-pro-max/SKILL.md` name field.
7. **Quality:** Remove or scope the "React Native only" note from `ui-ux-pro-max/SKILL.md` Step 1.
8. **Quality:** Add fallback instructions in `banner-design/SKILL.md` and `design/SKILL.md` for when external skills are not installed.
