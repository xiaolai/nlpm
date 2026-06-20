# NLPM Audit: eze-is/web-access
**Date**: 2026-06-20  |  **Artifacts**: 2  |  **Strategy**: single
**NL Score**: 95/100
**Security**: BLOCKED
**Bugs**: 1  |  **Quality Issues**: 5  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| SKILL.md | Skill | 92/100 | Four vague quantifiers (合适, 合理, 有必要, 大量) at -2 each |
| .claude-plugin/plugin.json | Plugin manifest | 98/100 | "intelligent" vague marketing term in description (-2) |

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
| Scripts | scripts/check-deps.mjs, scripts/cdp-proxy.mjs, scripts/find-url.mjs, scripts/browser-discovery.mjs, scripts/match-site.mjs |
| Hooks | None |
| MCP configs | None |
| Package manifests | None |

Note: the pre-scan reported "Scripts: 0 files" — five `.mjs` files were found under `scripts/` during the detailed pass.

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | scripts/cdp-proxy.mjs | 569 | SEC-path-traversal | `fs.writeFileSync(q.file, ...)` uses the raw `?file=` query parameter with no path validation; any local caller can write arbitrary data to any filesystem path accessible by the Node.js process |
| 2 | Medium | scripts/cdp-proxy.mjs | 418 | SEC-new-function-eval | `/eval` endpoint passes raw POST body directly to Chrome's `Runtime.evaluate`; no authentication on the localhost proxy means any local process can execute arbitrary JavaScript in the user's browser |
| 3 | Low | scripts/find-url.mjs | 140 | SEC-sql-injection-risk | SQL conditions are built with string interpolation; only single-quote escaping is applied (`replace(/'/g, "''")`); other SQL metacharacters are unmitigated (risk is limited because `execFileSync` prevents shell injection and the target is a local SQLite copy) |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .claude-plugin/plugin.json | `"version": "2.5.2"` does not match `SKILL.md` metadata `version: "2.5.3"` | Consumers that parse `plugin.json` as the authoritative version (upgrade checks, marketplace display) will show a stale release number |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/find-url.mjs | SQL conditions built with basic single-quote escaping only | Use a parameterised approach or at minimum escape all SQLite metacharacters; alternatively, pass user keywords as bound parameters via a Node.js SQLite binding rather than constructing raw SQL |

Note: Finding #1 (HIGH — path traversal in `/screenshot` endpoint) and Finding #2 (MEDIUM — unrestricted `Runtime.evaluate` API) require **private disclosure to the maintainer**, not public PRs. No fix PRs of any kind should be opened while BLOCKED status is in effect.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | SKILL.md | Vague quantifier "合适" (suitable/appropriate) in "请积极在任务合适时组合使用" (line 68) — does not specify what makes a task "suitable" for Jina | -2 |
| 2 | SKILL.md | Vague quantifier "合理" (reasonable) in "鼓励合理分治给子 Agent 并行执行" (line 199) — the split-or-not decision table on the same page is good, but the prose framing remains vague | -2 |
| 3 | SKILL.md | Vague quantifier "有必要" (when necessary) in "如果发现了有必要记录经验的新站点或新模式" (line 240) — criteria for what merits recording are unstated | -2 |
| 4 | SKILL.md | Vague quantifier "大量" (large amount) in "页面中存在大量已加载但未展示的内容" (line 169) — imprecise; could be "many elements not yet in the viewport" | -2 |
| 5 | .claude-plugin/plugin.json | "intelligent" in description (line 3) is marketing language without an operational definition | -2 |

## Cross-Component
**Version drift**: `plugin.json` declares `"version": "2.5.2"` (line 8); `SKILL.md` frontmatter declares `version: "2.5.3"` (line 10). These must stay in sync. The SKILL.md value appears to be the authoritative source (it carries the v2.5.3 migration notice in its own body), so `plugin.json` is the one lagging.

**Skill resolution**: `"skills": ["./"]` in `plugin.json` correctly resolves to `SKILL.md` at the plugin root — no structural issue.

**Reference paths**: `SKILL.md` cites `references/cdp-api.md`, `references/site-patterns/{domain}.md`, and `references/migration-2.5.3.md`. These files were not in scope for this audit but must exist at runtime for the skill to function correctly. A follow-up check is recommended.

## Recommendation
BLOCKED — do not submit PRs. File a private security report with the maintainer for Finding #1 (HIGH: unvalidated `?file=` path traversal in the `/screenshot` endpoint of `scripts/cdp-proxy.mjs`). Finding #2 (MEDIUM: unauthenticated `Runtime.evaluate` proxy) should be included in the same disclosure. Once the maintainer has acknowledged or resolved the HIGH finding, the following PRs become eligible: the version-bump bug fix in `plugin.json` and the SQL-escaping improvement in `find-url.mjs`.
