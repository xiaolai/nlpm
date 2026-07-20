# NLPM Audit: laolaoshiren/claude-code-skills-zh
**Date**: 2026-04-06  |  **Artifacts**: 20  |  **Strategy**: single
**NL Score**: 99.1/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 9  |  **Security Findings**: 9

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/github-actions-gen/SKILL.md | skill | 94 | Vague quantifiers ("合理利用缓存"、"适当的权限"、"合理的超时时间") without operational definition (-6) |
| skills/zh-code-reviewer/SKILL.md | skill | 96 | Vague quantifiers ("是否合理使用"、"是否恰当") without operational definition (-4) |
| skills/zh-readme/SKILL.md | skill | 96 | Vague quantifiers ("尽量补上"、"尽量收敛") without operational definition (-4) |
| skills/git-workflow/SKILL.md | skill | 98 | Vague quantifier ("必要时说明原因") without explicit trigger condition (-2) |
| skills/refactor-advisor/SKILL.md | skill | 98 | Vague quantifier ("尽量小步提交") without operational definition (-2) |
| skills/api-tester/SKILL.md | skill | 100 | None |
| skills/changelog-gen/SKILL.md | skill | 100 | None |
| skills/db-migrator/SKILL.md | skill | 100 | None |
| skills/dep-auditor/SKILL.md | skill | 100 | None |
| skills/ds-mapper/SKILL.md | skill | 100 | None |
| skills/env-manager/SKILL.md | skill | 100 | None |
| skills/error-translator/SKILL.md | skill | 100 | None |
| skills/eslint-fix/SKILL.md | skill | 100 | None |
| skills/i18n-helper/SKILL.md | skill | 100 | None |
| skills/log-analyzer/SKILL.md | skill | 100 | None |
| skills/perf-profiler/SKILL.md | skill | 100 | None |
| skills/security-audit/SKILL.md | skill | 100 | None |
| skills/skill-curator/SKILL.md | skill | 100 | None |
| skills/test-generator/SKILL.md | skill | 100 | None |
| skills/zh-docgen/SKILL.md | skill | 100 | None |

All 20 artifacts have valid `name`/`description` frontmatter and a defined
output section (or, for `db-migrator`, per-framework code templates that
serve the same purpose). Several of the artifacts (`api-tester`,
`eslint-fix`, `git-workflow`, `dep-auditor`, `perf-profiler`,
`test-generator`) are notably rigorous, with explicit authorization
boundaries, evidence requirements, and "generated ≠ executed" distinctions
that go beyond the minimum rubric.

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 5 |
| Low | 4 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none |
| Scripts | scripts/package.json, scripts/post_to_juejin.py, scripts/post_to_juejin.js, scripts/sync_readme_to_site.py, scripts/test_juejin_post.js, scripts/test_sync_readme_to_site.py |
| MCP configs | none |
| Package manifests | scripts/package.json (dependency: playwright ^1.40.0) |

`scripts/` is maintainer-only tooling (Juejin auto-publish + README↔site
sync) invoked manually via `npm run post-juejin` / `python
sync_readme_to_site.py`; it is not part of the 20 shipped `SKILL.md`
artifacts and is not installed by end users who `cp -r skills/*
~/.claude/skills/`.

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | Low | scripts/package.json | 11 | SEC-unpinned-semver | `playwright` pinned with caret range `^1.40.0`, allowing automatic minor/patch upgrades in CI/local installs |
| 2 | Medium | scripts/post_to_juejin.py | 33 | SEC-network-call | `requests.post` sends the raw Juejin session Cookie (loaded from env or `~/.hermes/.../.juejin_cookie`) to `api.juejin.cn` to create a draft |
| 3 | Medium | scripts/post_to_juejin.py | 84,107 | SEC-dynamic-code-generation | Builds a Node.js script via unescaped f-string interpolation of `draft_id` (sourced from the Juejin API JSON response), writes it to a temp file, and executes it with `subprocess.run(['node', tmp_file])`; a tampered/malformed `draft_id` value could break out of the embedded string literal |
| 4 | Low | scripts/post_to_juejin.py | 102 | SEC-temp-file-write | Generated `.js` script is written to the OS temp directory (`tempfile.NamedTemporaryFile`, no explicit dir) outside the repo tree |
| 5 | Medium | scripts/post_to_juejin.js | 50 | SEC-network-call | `https.request` sends the Juejin session Cookie to `api.juejin.cn` to create a draft |
| 6 | Low | scripts/post_to_juejin.js | 9 | SEC-temp-file-write | Error/result screenshots and `juejin_result.json` are written to `os.tmpdir()`, outside the repo tree |
| 7 | Medium | scripts/test_juejin_post.js | 27 | SEC-network-call | Live-smoke script sends the Juejin session Cookie to `api.juejin.cn` and, when run with `--publish`, actually creates and publishes a real article on the maintainer's account |
| 8 | Low | scripts/test_juejin_post.js | 99 | SEC-temp-file-write | Draft/publish screenshots written to `os.tmpdir()`, outside the repo tree |
| 9 | Medium | scripts/sync_readme_to_site.py | 507 | SEC-network-call | `subprocess.run(["gh","api","graphql",...])` performs an external network call (via `gh`) to fetch GitHub star counts for every curated repo URL in README.md |

All Cookie-bearing requests target the intended first-party endpoint
(`api.juejin.cn`) that the Cookie was issued for — no cross-domain
exfiltration observed. All publish-capable scripts (`post_to_juejin.js`,
`post_to_juejin.py`, `test_juejin_post.js`) require an explicit
`--publish` flag before touching the network or a real account, and
refuse to run without a Cookie present.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No bugs found. | — |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | scripts/package.json | `playwright` dependency uses an unpinned caret range (`^1.40.0`) | Pin to an exact version (e.g. `1.40.0`) and commit a lockfile so CI/local runs are reproducible |
| 2 | scripts/post_to_juejin.py | `draft_id` from the Juejin API response is interpolated unescaped into a generated JS string that is then executed via `node` | Validate `draft_id` matches `^\d+$` before interpolation, or pass it to the child script via `process.env`/argv instead of string interpolation |
| 3 | scripts/post_to_juejin.py, scripts/post_to_juejin.js, scripts/test_juejin_post.js | Temp scripts/screenshots/result files are written to the OS temp directory with default (unrestricted) permissions and never cleaned up on success | Write to a dedicated gitignored `.tmp/` directory under the repo (or explicitly `unlink`/`0600`-permission the files) so debug artifacts don't linger world-readable in shared temp dirs |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/github-actions-gen/SKILL.md:40 | Vague quantifier: "合理利用 cache" (no cache-key strategy specified at point of use) | -2 |
| 2 | skills/github-actions-gen/SKILL.md:89 | Vague quantifier: "设置适当的权限" (no minimal-permission set specified) | -2 |
| 3 | skills/github-actions-gen/SKILL.md:90 | Vague quantifier: "超时时间合理" (no default/range given) | -2 |
| 4 | skills/zh-code-reviewer/SKILL.md:19 | Vague quantifier: "是否合理使用" design patterns (no criteria given) | -2 |
| 5 | skills/zh-code-reviewer/SKILL.md:47 | Vague quantifier: "检查是否恰当" for Chinese identifiers/comments (no criteria given) | -2 |
| 6 | skills/zh-readme/SKILL.md:18 | Vague quantifier: "尽量补上社交证明信号" (no minimum bar given) | -2 |
| 7 | skills/zh-readme/SKILL.md:27 | Vague quantifier: "尽量收敛到 1 个正式入口" | -2 |
| 8 | skills/git-workflow/SKILL.md:58 | Vague quantifier: "必要时说明原因" in commit-message template (no trigger condition) | -2 |
| 9 | skills/refactor-advisor/SKILL.md:95 | Vague quantifier: "尽量小步提交" (no size/step definition) | -2 |

## Cross-Component
- All 20 `skills/*/SKILL.md` directories are listed and linked correctly
  in `README.md` (hero list, recommendation table, and full skills table);
  no orphaned skill directories and no dead `skills/` links found.
- `scripts/test_sync_readme_to_site.py::test_original_skill_sets_and_promo_counts_are_consistent`
  already asserts, at test time, that the on-disk `skills/*/SKILL.md` set,
  `README.md`'s original-skills section, `docs/index.html`, and
  `PROMO.md`'s counts all agree — a stronger cross-component guarantee
  than this audit's own manual pass found reason to add to.
- No contradictions found between individual `SKILL.md` frontmatter
  `description` fields and their corresponding README one-line summaries.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes. There are
no NL bugs and no Critical/High security findings; the three Security
Fixes above (unpinned `playwright` version, unescaped `draft_id`
interpolation, temp-dir artifact hygiene) are low-risk, narrowly-scoped
improvements suitable for a public PR. The nine Quality Issues (vague
quantifiers) are informational/style-level and below the PR threshold.
