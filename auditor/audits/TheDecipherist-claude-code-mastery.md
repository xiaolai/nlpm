# NLPM Audit: TheDecipherist/claude-code-mastery
**Date**: 2026-04-06  |  **Artifacts**: 8  |  **Strategy**: single
**NL Score**: 94/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 14  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/pr.md | Command | 83/100 | No empty-input handling (empty diff / no commits on branch) |
| commands/review.md | Command | 89/100 | Vague quantifiers: "properly", "correctly", "appropriate" (3 instances) |
| commands/explain.md | Command | 91/100 | Missing `allowed-tools` frontmatter field |
| commands/test.md | Command | 93/100 | Missing `allowed-tools` frontmatter field |
| skills/security-audit/SKILL.md | Skill | 96/100 | Vague quantifiers: "comprehensive", "appropriately" |
| CLAUDE.md | Memory | 100/100 | None — repo structure diagram omits `commands/` and `docs/` (informational) |
| commands/README.md | Documentation | 100/100 | None |
| skills/commit-messages/SKILL.md | Skill | 100/100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 2 |
| High | 0 |
| Medium | 1 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | hooks/after-edit.sh, hooks/block-dangerous-commands.sh, hooks/block-secrets.py, hooks/end-of-turn.sh, hooks/notify.sh |
| Scripts (non-hook) | docs/app.js (client-side site script; counted in the pre-scan's 6-file surface total) |
| MCP configs | None found (no `.mcp.json`) |
| Package manifests | None found (no `package.json`, no `requirements.txt`) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | hooks/block-dangerous-commands.sh | 79 | curl-piped-to-shell text match | The literal substring `curl\s+.*\|\s*(ba)?sh` appears inside this hook's own `grep -qE` detection pattern — it is the string being matched *for*, never executed. This hook's purpose is to **block** curl-pipe-sh commands (exit code 2). Verified false positive: the pre-scan's naive text match fired on defensive code, not a live curl-pipe-sh execution. |
| 2 | Critical | hooks/block-dangerous-commands.sh | 87 | wget-piped-to-shell text match | Same pattern as #1, for `wget`: the `grep -qE` blocklist regex text on line 87 contains `wget\s+.*\|\s*(ba)?sh` as the string being matched against incoming Bash commands, not executed code. Verified false positive. |
| 3 | Medium | docs/app.js | 198, 215 | Network fetch | `fetchGuide()` (line 198) calls `fetch(url)` against a local relative path first, then falls back to `https://raw.githubusercontent.com/TheDecipherist/claude-code-mastery/main/GUIDE.md`; `loadGuide()` (line 215) renders the result via `marked.parse()` then sanitizes with `DOMPurify.sanitize()` before injecting into the DOM. Legitimate fallback-fetch pattern for a static GitHub Pages site, already mitigated by HTML sanitization. Flagged per the MEDIUM "network calls" criterion for completeness — no fix needed. |

## Bugs (PR-worthy)
No bugs found. No missing required frontmatter fields, no undeclared-tool calls, and no broken relative references were identified across the 8 artifacts.

## Security Fixes (PR-worthy, Medium/Low only)
No PR-worthy security fixes identified. The one Medium finding (docs/app.js network fetch) is intended fallback-fetch behavior already mitigated with DOMPurify sanitization — no actionable change to suggest.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/explain.md | Missing `allowed-tools` frontmatter field | -5 |
| 2 | commands/explain.md | Vague quantifier "clear" (line 7: "Provide a clear, thorough explanation") | -2 |
| 3 | commands/explain.md | Vague quantifier "thorough" (line 7) | -2 |
| 4 | commands/pr.md | Missing `allowed-tools` frontmatter field | -5 |
| 5 | commands/pr.md | No empty-input handling — no guard for an empty diff / branch with no commits | -10 |
| 6 | commands/pr.md | Vague quantifier "comprehensive" (line 7: "Create a comprehensive pull request description") | -2 |
| 7 | commands/review.md | Missing `allowed-tools` frontmatter field | -5 |
| 8 | commands/review.md | Vague quantifier "properly" (line 28: "Null/undefined handled properly") | -2 |
| 9 | commands/review.md | Vague quantifier "correctly" (line 29: "Async operations awaited correctly") | -2 |
| 10 | commands/review.md | Vague quantifier "appropriate" (line 43: "memoized where appropriate") | -2 |
| 11 | commands/test.md | Missing `allowed-tools` frontmatter field | -5 |
| 12 | commands/test.md | Vague quantifier "comprehensive" (line 7: "Generate comprehensive tests") | -2 |
| 13 | skills/security-audit/SKILL.md | Vague quantifier "comprehensive" (line 8: "Perform comprehensive security audits") | -2 |
| 14 | skills/security-audit/SKILL.md | Vague quantifier "appropriately" (line 110: "Sessions expire appropriately") | -2 |

## Cross-Component
- `CLAUDE.md`'s "Repository Structure" diagram (lines 17-33) lists `GUIDE.md`, `templates/`, `hooks/`, and `skills/` but omits the `commands/` directory (4 slash commands + README) and `docs/` directory (the GitHub Pages site), both of which exist in the repository. Low-confidence / informational — the omission doesn't point Claude at anything nonexistent, it just means CLAUDE.md's map of the repo is incomplete relative to current disk state. No PR recommended for this alone.
- No broken relative references found: `commands/README.md`'s command table (`/review`, `/explain`, `/test`, `/pr`) matches the four files actually present in `commands/`. `CLAUDE.md`'s hook filenames match all 5 files in `hooks/`. `docs/app.js`'s `../GUIDE.md` relative fetch path resolves correctly against the repo root.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes. In this audit there are none to submit: 0 bugs, and the sole Medium security finding requires no fix. The pre-scan's CRITICAL flag was verified during detailed review as a false positive (a curl/wget-pipe-to-shell string appearing inside `block-dangerous-commands.sh`'s own defensive blocklist regex, never executed). The 14 Quality Issues are informational only (missing `allowed-tools` declarations, absent empty-input handling on `/pr`, and vague quantifiers) and are below the PR-worthy bar for this pipeline.
