# NLPM Audit: NanmiCoder/cc-haha
**Date**: 2026-04-06  |  **Artifacts**: 4  |  **Strategy**: single
**NL Score**: 80/100
**Security**: CLEAR
**Bugs**: 1  |  **Quality Issues**: 5  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| src/skills/bundled/claude-api/SKILL.md | skill | 40 | File is a 2-line `stub` with no frontmatter (name, description) and no content |
| src/skills/bundled/verify/SKILL.md | skill | 90 | One-sentence body, no output format |
| src/skills/bundled/imagegen/SKILL.md | skill | 94 | Vague quantifiers ("useful", "relevant", "briefly") |
| .agents/skills/release-announcement/SKILL.md | skill | 98 | Vague quantifiers ("很短", "简短") |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

The 3 pre-scan Critical matches are the word `eval` in browser-automation test harness calls (false positives, listed below as info only).

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none |
| Scripts | 57 files under `scripts/` (TypeScript test/quality-gate tooling, `start-web-ui.sh`, `git-hooks/pre-push`), plus `.agents/skills/release-announcement/scripts/release_poster.py` |
| MCP configs | none |
| Package manifests | `site/package.json`, `adapters/package.json`, `desktop/package.json` (no postinstall scripts found) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | info (false positive) | scripts/quality-gate/desktop-smoke/deterministic.ts | 254 | `eval` | `browserStep(['eval', ...])` is an agent-browser subcommand with a generated bootstrap string, not JS eval of untrusted input |
| 2 | info (false positive) | scripts/quality-gate/desktop-smoke/team-plan.ts | 81 | `eval` | Same agent-browser `eval` subcommand with a constant expression |
| 3 | info (false positive) | scripts/quality-gate/desktop-smoke/execute.ts | 592 | `eval` | Same agent-browser `eval` subcommand with a constant bootstrap |

`release_poster.py` line 24 uses `subprocess.run` with an argument list (no `shell=True`). `pre-push` is a non-blocking echo. `start-web-ui.sh` only starts local servers.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | src/skills/bundled/claude-api/SKILL.md | Contents are `<!-- @generated stub from scan-missing-imports -->` / `stub`. No frontmatter, so no name or description. | Skill cannot register or be triggered, and it provides no guidance |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
No Medium/Low security issues.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | src/skills/bundled/claude-api/SKILL.md | No output format (stub content) | -10 |
| 2 | src/skills/bundled/verify/SKILL.md | Body is a single sentence with no steps or output format | -10 |
| 3 | src/skills/bundled/imagegen/SKILL.md | Vague quantifiers ("relevant", "useful", "briefly") | -6 |
| 4 | .agents/skills/release-announcement/SKILL.md | Vague quantifiers ("很短", "简短") | -2 |
| 5 | src/skills/bundled/claude-api/SKILL.md | Missing name and description frontmatter (counted as bug) | -50 |

## Cross-Component
- imagegen declares `allowed-tools: ImageGen, ImageEdit`. Both are referenced in the body, and the tools are host built-ins that cannot be checked in the skill directory.
- release-announcement references `references/editorial-brief.md`, `references/poster-spec.md` and `scripts/release_poster.py`. All exist on disk.
- The claude-api stub is the only skill with no content.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.
