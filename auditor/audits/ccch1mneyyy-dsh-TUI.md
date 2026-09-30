# NLPM Audit: ccch1mneyyy/dsh-TUI
**Date**: 2026-04-06  |  **Artifacts**: 9  |  **Strategy**: single
**NL Score**: 95/100
**Security**: REVIEW
**Bugs**: 0  |  **Quality Issues**: 3  |  **Security Findings**: 5

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .agents/skills/review/SKILL.md | skill | 90 | ~90-line body, 700+ char description; output format delegated to references/report-contract.md |
| .agents/skills/pr/SKILL.md | skill | 95 | Hard-coded PR-number examples (#919, #1110) |
| guide/dsh-tui-guide/SKILL.md | skill | 95 | No explicit output format (answer-with-citation only) |
| .agents/skills/audit/SKILL.md | skill | 96 | Empty-scope input handling implicit |
| .agents/skills/bug/SKILL.md | skill | 96 | None significant |
| .agents/skills/pr-comments/SKILL.md | skill | 96 | None significant |
| .agents/skills/practice/SKILL.md | skill | 96 | None significant |
| .agents/skills/release-notes/SKILL.md | skill | 96 | None significant |
| .agents/skills/vuln-check/SKILL.md | skill | 96 | None significant |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 5 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none |
| Scripts | scripts/** (400+ .mjs/.cjs/.tsx/.ts/.mts helpers, scripts/build.sh), .agents/skills/review/scripts/*.mjs |
| MCP configs | none |
| Package manifests | package.json (`prepare` script) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | medium | package.json | 122 | prepare script | `prepare` runs local guard then compile; the guard is local and benign, runs on git installs |
| 2 | medium | scripts/run-verify-build.mjs | 132 | spawnSync shell:true | Runs package.json script strings (repo-controlled, not user input) through a shell |
| 3 | medium | scripts/make-standalone-bundle.mjs | 186 | runtime package install | `pnpm install --lockfile-only` at build time |
| 4 | medium | scripts/make-standalone-bundle.mjs | 203 | runtime package install | `pnpm install --frozen-lockfile` at build time (lockfile pinned) |
| 5 | medium | scripts/verify-settings-compat.mjs | 141 | new Function | Evaluates generated registration JS in a verify script; input is build output, not external (also line 165 and scripts/verify-cordis-approval.mjs:44) |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
No bugs found. All frontmatter valid; referenced reference/script files exist.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/run-verify-build.mjs | shell:true on fixed strings | Low value; optionally document why the shell is required (npm script strings) |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .agents/skills/review/SKILL.md | Very long description and body; output format lives only in a reference file | -10 |
| 2 | .agents/skills/pr/SKILL.md | Issue/PR numbers (#919, #1110) baked into instructions will go stale | -5 |
| 3 | guide/dsh-tui-guide/SKILL.md | No explicit output format section | -5 |

## Cross-Component
- review SKILL references references/*.md and scripts/*.mjs; all present.
- pr SKILL references docs/contributing.md and .github/PULL_REQUEST_TEMPLATE.md; both present.
- Guide SKILL lists 8 topics; 16 files on disk match.
- No broken references or orphans found.

## Recommendation
REVIEW — only medium security findings, all in developer/build scripts with repo-controlled inputs; no NL bugs to PR. No Critical/High findings.
