# NLPM Audit: Enderfga/claw-orchestrator
**Date**: 2026-04-06  |  **Artifacts**: 3  |  **Strategy**: single
**NL Score**: 95/100
**Security**: BLOCKED
**Bugs**: 1  |  **Quality Issues**: 4  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/SKILL.md | skill-reference | 92/100 | Tool count "65 tools" conflicts with CLAUDE.md "63 canonical tools" |
| skills/ultraapp/SKILL.md | skill-persona | 96/100 | Vague quantifiers: "briefly", "(when relevant)" in behavioral contract |
| CLAUDE.md | project-memory | 97/100 | Undocumented `<personal-or-internal-string>` placeholder in release checklist |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 1 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Scripts | scripts/postbuild.mjs, scripts/test-integration.ts, scripts/test-ultraapp-integration.ts |
| Package manifest | package.json |
| Hooks | none |
| MCP configs | none |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | CLAUDE.md | 113 | security-disclosure-obfuscation | Documents a policy requiring developers to "Frame as a bland refactor" when patching previously hard-coded secrets, and to omit words like "security", "hard-coded", or "sanitize" from commit messages, CHANGELOG, release title, and release body. This actively prevents users of the npm package from identifying security-relevant releases and making informed upgrade decisions — a supply chain transparency anti-pattern. |
| 2 | Medium | package.json | 28 | rm-rf-in-lifecycle-script | Build script `"build": "rm -rf dist && tsc && node scripts/postbuild.mjs"` executes `rm -rf` as part of the npm lifecycle. Scoped to `dist/` in practice, but any symlink or directory confusion at `dist` would cause unintended deletion. Also executed via `prepublishOnly` on every `npm publish`. |
| 3 | Low | package.json | 93 | unpinned-semver | All four runtime dependencies (`@modelcontextprotocol/sdk`, `commander`, `diff`, `re2`) and all dev dependencies use `^` semver ranges. Published package consumers receive unpredictable versions on fresh installs; a malicious or broken minor release in any dependency could silently break or compromise downstream installs. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | skills/SKILL.md vs CLAUDE.md | Tool count discrepancy: CLAUDE.md line 14 states "63 canonical tools"; skills/SKILL.md line 46 states "65 tools". One document is stale after a recent tool addition. | Misleads integrators about the plugin surface area; breaks automated tooling that parses counts from skill descriptions. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | package.json | `rm -rf dist` in npm build and prepublishOnly scripts is an unrestricted shell deletion command | Replace with a cross-platform Node.js cleanup step (e.g. `node -e "fs.rmSync('dist',{recursive:true,force:true})"`) or add an explicit path guard (`rm -rf ./dist`) to make the relative scope unambiguous. |
| 2 | package.json | Unpinned semver ranges on all runtime deps | Pin runtime dependencies to exact versions (`1.29.0` instead of `^1.29.0`) in `package.json`; use lockfile in CI. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | CLAUDE.md | Release checklist (lines 103–104, 111) contains `<personal-or-internal-string>` placeholders with no explanation of what string to substitute or that substitution is required. Developers following the checklist verbatim will run no-op grep commands. | -3 |
| 2 | skills/SKILL.md | `metadata:` frontmatter block uses JSON flow syntax (`{ "openclaw": { ... } }`) inside a YAML document. Valid YAML but non-standard; several YAML parsers with strict-mode fail on embedded flow-JSON at the top level, and the multiline structure breaks some frontmatter linters. | -3 |
| 3 | skills/ultraapp/SKILL.md | Behavioral contract item 5 uses two vague quantifiers: "briefly explain" (line 17) and "(when relevant)" (line 17). "Briefly" gives no length guidance; "when relevant" leaves inclusion criteria to the agent's judgment. | -4 |
| 4 | skills/ultraapp/SKILL.md | Skill is filed as a reference document (`skills/ultraapp/SKILL.md`) but is written as an agent persona with imperative behavioral contracts, tool invocation syntax, and an interview completion protocol. The artifact type (skill-reference vs agent definition) does not match the content's structural role. | informational |

## Cross-Component
- **Tool count drift**: `CLAUDE.md:14` registers "63 canonical tools"; `skills/SKILL.md:46` advertises "65 tools". The skill description is the user-facing surface; the CLAUDE.md comment is the developer authority. One is stale. Confidence: medium (exact count requires running `src/index.ts`; both numbers are plausible given the timeline between file updates and the `codex_goal_*`/`claude_goal_*` wildcard entries in the tools table).
- **Unverified reference links**: `skills/SKILL.md` contains three relative Markdown links — `[references/council.md](references/council.md)`, `[references/autoloop.md](references/autoloop.md)`, and `[references/tools.md](references/tools.md)` — that resolve relative to the `skills/` directory. These files are not in the artifact set provided for this audit. If they are absent from the shipped npm package (`files` array in `package.json` includes `skills/` broadly, so they would ship if they exist on disk), the links are live broken references for anyone reading the skill in their editor.
- **CLI version in CLAUDE.md vs SKILL.md option tables**: `skills/SKILL.md` documents `CLI 2.1.111` and `CLI 2.1.121` option blocks while `CLAUDE.md` references Claude CLI tested version `2.1.178`. The option table headers are frozen at older version numbers even though the code has been updated; this creates a maintenance gap for contributors scanning the skill for version compatibility.

## Recommendation
BLOCKED — do not submit PRs. File private security report.

The HIGH security finding (finding #1) documents a deliberate policy in `CLAUDE.md` that instructs developers to conceal the security nature of vulnerability-patching releases from downstream users of the published npm package. This is a supply chain transparency anti-pattern that requires private disclosure to the maintainer before any NL fix PRs are opened. Once the maintainer has acknowledged or corrected the policy, the one confirmed NL bug (tool count discrepancy) and the two Medium/Low security fixes are suitable for public PRs.
