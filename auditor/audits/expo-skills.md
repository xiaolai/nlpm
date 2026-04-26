# NLPM Audit: expo/skills
**Date**: 2026-04-26  |  **Artifacts**: 15  |  **Strategy**: single
**NL Score**: 92/100
**Security**: CLEAR
**Bugs**: 2  |  **Quality Issues**: 9  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| CLAUDE.md | project-doc | 80 | Outdated repo structure docs; describes split plugins that don't exist |
| plugins/expo/skills/expo-ui-swift-ui/SKILL.md | skill | 80 | Import path mismatch (`@expo-ui/swift-ui` vs `@expo/ui/swift-ui`); name not kebab-case |
| plugins/expo/skills/expo-deployment/SKILL.md | skill | 85 | Inconsistent reference paths: top section uses `references/`, body uses `reference/` |
| plugins/expo/skills/expo-ui-jetpack-compose/SKILL.md | skill | 88 | Name field not kebab-case ("Expo UI Jetpack Compose"); SDK 55–only scope undisclosed in description |
| plugins/expo/skills/expo-cicd-workflows/SKILL.md | skill | 91 | `{baseDir}` placeholder in commands not documented; unclear if auto-substituted |
| plugins/expo/skills/building-native-ui/SKILL.md | skill | 92 | Four vague quantifiers: "almost always" ×2, "Whenever possible", "frequently" |
| plugins/expo/skills/upgrading-expo/SKILL.md | skill | 93 | Clean; minor formatting nits |
| plugins/expo/.claude-plugin/plugin.json | manifest | 95 | Well-formed; no issues |
| plugins/expo/skills/expo-dev-client/SKILL.md | skill | 95 | Clean |
| plugins/expo/skills/expo-tailwind-setup/SKILL.md | skill | 95 | Clean |
| plugins/expo/skills/use-dom/SKILL.md | skill | 95 | Clean |
| plugins/expo/skills/expo-api-routes/SKILL.md | skill | 96 | Vague instruction words: "focused", "gracefully" |
| plugins/expo/skills/native-data-fetching/SKILL.md | skill | 96 | Vague decision-tree labels: "Complex", "Simpler" |
| plugins/expo/skills/expo-module/SKILL.md | skill | 97 | Excellent |
| plugins/expo/skills/eas-update-insights/SKILL.md | skill | 98 | Excellent; model skill for the collection |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 3 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | None |
| Scripts | `plugins/expo/skills/expo-cicd-workflows/scripts/fetch.js`, `plugins/expo/skills/expo-cicd-workflows/scripts/validate.js` |
| MCP configs | None |
| Package manifests | `plugins/expo/skills/expo-cicd-workflows/scripts/package.json` |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | plugins/expo/skills/expo-cicd-workflows/scripts/fetch.js | 96–107 | Unvalidated URL arg passed to fetch | Script accepts any URL via `process.argv[2]` and makes an HTTP request without domain or scheme validation; SSRF if invoked with attacker-controlled input outside skill context |
| 2 | Low | plugins/expo/skills/expo-cicd-workflows/scripts/package.json | 7 | SEC-unpinned-semver | `ajv@^8.17.1` — caret range allows minor/patch upgrades without lock-file pinning |
| 3 | Low | plugins/expo/skills/expo-cicd-workflows/scripts/package.json | 8 | SEC-unpinned-semver | `ajv-formats@^3.0.1` — caret range |
| 4 | Low | plugins/expo/skills/expo-cicd-workflows/scripts/package.json | 9 | SEC-unpinned-semver | `js-yaml@^4.1.0` — caret range |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | plugins/expo/skills/expo-ui-swift-ui/SKILL.md | Import path in code example uses `@expo-ui/swift-ui` (line 27) but frontmatter description and install command say `@expo/ui/swift-ui` — these are different packages | Developers copying the example import will get a module-not-found error |
| 2 | plugins/expo/skills/expo-deployment/SKILL.md | Top-level References section uses `./references/` (plural, lines 18–22) but all five in-body `See …` links use `./reference/` (singular, lines 126, 127, 130, 133, 165) | Half the references point to a non-existent directory; Claude can't read them |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | plugins/expo/skills/expo-cicd-workflows/scripts/fetch.js | URL arg is not validated before use in `fetch()` | Add an allowlist of permitted URL prefixes (e.g., `https://api.expo.dev/`, `https://raw.githubusercontent.com/expo/`) and reject others |
| 2 | plugins/expo/skills/expo-cicd-workflows/scripts/package.json | Three dependencies use caret semver ranges | Pin exact versions (`"ajv": "8.17.1"`) or add a lockfile commit policy |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | plugins/expo/skills/expo-ui-jetpack-compose/SKILL.md | `name` field is "Expo UI Jetpack Compose" — must be lowercase kebab-case per plugin conventions ("expo-ui-jetpack-compose") | −5 |
| 2 | plugins/expo/skills/expo-ui-swift-ui/SKILL.md | `name` field is "Expo UI SwiftUI" — must be lowercase kebab-case ("expo-ui-swift-ui") | −5 |
| 3 | plugins/expo/skills/expo-cicd-workflows/SKILL.md | Commands reference `{baseDir}` (lines 19, 82, 84) with no explanation of whether Claude Code auto-substitutes this or the agent must resolve it manually | −5 |
| 4 | plugins/expo/skills/building-native-ui/SKILL.md | Vague instruction "its first child should almost always be a ScrollView" (line 103) | −2 |
| 5 | plugins/expo/skills/building-native-ui/SKILL.md | Vague instruction "it should almost always be the first component" (line 104) | −2 |
| 6 | plugins/expo/skills/building-native-ui/SKILL.md | Vague instruction "Whenever possible, include a `<Link.Preview>`" (line 161) | −2 |
| 7 | plugins/expo/skills/building-native-ui/SKILL.md | Vague instruction "Use link previews frequently" (line 229) | −2 |
| 8 | plugins/expo/skills/expo-api-routes/SKILL.md | Vague rule "Keep API routes focused" (line 366) — no criterion for what "focused" means | −2 |
| 9 | plugins/expo/skills/expo-api-routes/SKILL.md | Vague rule "Handle errors gracefully" (line 364) — no specification | −2 |

## Cross-Component
**CLAUDE.md repo structure is stale.** The "Repository Structure" section (lines 7–25) and installation examples (lines 228–234) describe three separate plugin directories — `expo-app-design/`, `upgrading-expo/`, and `expo-cicd-workflows/` — which do not exist at the top level. All skills are actually consolidated under `plugins/expo/` as a single plugin. The install commands referencing `expo-app-design` and `expo-cicd-workflows` as standalone plugin names will fail against the actual marketplace configuration.

No orphaned skills or missing agent references found. All skill `references/` paths listed in frontmatter sections appear internally consistent within each file (the `expo-deployment` inconsistency is already captured as Bug #2).

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

Priority order:
1. **Bug #1** (expo-ui-swift-ui import path) — breaks developer workflow immediately; one-line fix.
2. **Bug #2** (expo-deployment reference paths) — renders half the reference links dead.
3. **Security fix #1** (fetch.js URL validation) — low practical risk but straightforward to harden.
4. **Security fix #2** (package.json pin versions) — supply-chain hygiene.
5. **Quality #1–2** (kebab-case names) — convention alignment.
6. **Cross-component** (CLAUDE.md structure) — update to reflect actual layout.
