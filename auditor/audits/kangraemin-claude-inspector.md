# NLPM Audit: kangraemin/claude-inspector
**Date**: 2026-04-19  |  **Artifacts**: 7  |  **Strategy**: single
**NL Score**: 76/100
**Security**: REVIEW
**Bugs**: 3  |  **Quality Issues**: 9  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/agents/proxy-analyzer.md | agent | 43 | Missing `name` frontmatter + no examples + no output format |
| .claude/agents/ui-debugger.md | agent | 45 | Missing `name` frontmatter + no examples + no output format |
| .claude/agents/reviewer.md | agent | 55 | Missing `name` frontmatter + no examples |
| CLAUDE.md | project-config | 88 | Minimal but content is clear and specific |
| .claude/skills/e2e/SKILL.md | skill | 100 | No issues |
| .claude/skills/build/SKILL.md | skill | 100 | No issues |
| .claude/skills/deploy/SKILL.md | skill | 100 | No issues |

**Weighted average**: (43 + 45 + 55 + 88 + 100 + 100 + 100) / 7 = **76**

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
| Hooks | 0 |
| Scripts | 1 — `scripts/notarize.js` |
| MCP configs | 0 |
| Package manifests | 1 — `package.json` |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | scripts/notarize.js | 25 | credential in CLI arg | `APPLE_APP_SPECIFIC_PASSWORD` passed as `--password` flag to `xcrun notarytool`; value is visible in `ps` output to all local users during the build. Fix: use `notarytool` keychain profiles (`--keychain-profile`) instead of explicit `--password`. |
| 2 | Medium | package.json | 32 | external data exfiltration | `analytics.js` is bundled into the distributed app alongside `@sentry/electron`; Sentry captures and transmits runtime errors and potentially user-identifying device data to `sentry.io` servers. Intentional but end-users are not explicitly informed via README/privacy policy. |
| 3 | Low | scripts/notarize.js | 20, 25 | subprocess with string interpolation | `execSync` uses template literals interpolating `appPath` and `zipPath` (sourced from electron-builder's trusted build context, so actual risk is low; log for completeness). |
| 4 | Low | package.json | 59–65 | unpinned dependencies | All 6 dependencies (`@sentry/electron`, `dotenv`, `electron-updater`, `@playwright/test`, `electron`, `electron-builder`) use `^` semver ranges; a compromised patch release could propagate automatically. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .claude/agents/proxy-analyzer.md | Missing `name` field in frontmatter | Agent cannot be registered by Claude Code — the `name` key is required for agent lookup |
| 2 | .claude/agents/reviewer.md | Missing `name` field in frontmatter | Agent cannot be registered by Claude Code |
| 3 | .claude/agents/ui-debugger.md | Missing `name` field in frontmatter | Agent cannot be registered by Claude Code |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/notarize.js | APPLE_APP_SPECIFIC_PASSWORD visible in process list (Medium) | Replace `--apple-id … --password … --team-id …` with `--keychain-profile <profile>` using `notarytool store-credentials` pre-configured in the build environment |
| 2 | package.json | Sentry bundled without user disclosure (Medium) | Add a README/privacy notice disclosing that error telemetry is collected via Sentry; or gate Sentry initialization behind explicit opt-in |
| 3 | package.json | Unpinned `^` semver ranges (Low) | Lock critical runtime deps (`@sentry/electron`, `electron-updater`) to exact versions or use `package-lock.json` with `npm ci` in CI |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/agents/proxy-analyzer.md | No `model` declaration | -5 |
| 2 | .claude/agents/proxy-analyzer.md | Zero example blocks | -15 |
| 3 | .claude/agents/proxy-analyzer.md | No output format section | -10 |
| 4 | .claude/agents/proxy-analyzer.md | Vague quantifier: "합리적" (reasonable) in evidence-strength table | -2 |
| 5 | .claude/agents/reviewer.md | No `model` declaration | -5 |
| 6 | .claude/agents/reviewer.md | Zero example blocks (요약 포맷 defines output shape but shows no invocation example) | -15 |
| 7 | .claude/agents/ui-debugger.md | No `model` declaration | -5 |
| 8 | .claude/agents/ui-debugger.md | Zero example blocks | -15 |
| 9 | .claude/agents/ui-debugger.md | No output format section (수정 원칙 describes behavior but not result shape) | -10 |

## Cross-Component
- **Broken external reference**: `reviewer.md` line 17 reads `~/.claude/rules/review-rules.md`. This is a user-level file outside the repo. It will silently 404 on any fresh clone — the reviewer agent's priority rules become unavailable. Recommend either committing `review-rules.md` into the repo at a relative path, or documenting the manual setup step in README.
- **Internal references are consistent**: all three agents reference `public/index.html` and `main.js` (project source files); `CLAUDE.md` references `proxyDetailView` structure that ui-debugger also cites — these are in sync.
- **Skill → package.json consistency**: `build`, `deploy`, and `e2e` skills invoke npm scripts (`dist:mac`, `test:unit`, `test:e2e`, `predist`) that all exist in `package.json` — no drift detected.
- **notarize.js registered correctly**: `package.json` `afterSign` hook points to `scripts/notarize.js` which exists ✅.
- **analytics.js referenced but not audited**: `package.json` bundles `analytics.js` in the `files` array, but this file was not in the NL artifact list. If it contains Claude-specific prompt logic it should be included in future audits.

## Recommendation
REVIEW — submit NL fix PRs for the three missing `name` frontmatter bugs (high-confidence, zero-risk), flag the `review-rules.md` orphaned reference, and open a disclosure/opt-in issue for the Sentry telemetry finding. The credential-in-CLI-arg finding warrants a separate issue on the notarize script. No Critical or High security findings; contribution is safe to proceed after NL fixes.
