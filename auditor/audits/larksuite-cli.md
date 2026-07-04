# NLPM Audit: larksuite/cli
**Date**: 2026-04-06  |  **Artifacts**: 35  |  **Strategy**: batched
**NL Score**: 96/100
**Security**: REVIEW
**Bugs**: 3  |  **Quality Issues**: 1  |  **Security Findings**: 4

## NL Score Summary

35 SKILL.md files were scored: 27 production `lark-*` skills, `lark-shared` (cross-cutting reference skill), `lark-skill-maker` (meta-skill for authoring new skills), `cli-e2e-testcase-writer` (test-authoring skill under `tests/cli_e2e/`), one Go-test fixture (`internal/qualitygate/skillscan/testdata/skills/lark-demo`), and six intentional pass/fail fixtures under `scripts/skill-format-check/tests/` that exist to unit-test the repo's own `skill-format-check` linter.

The production skill corpus is exceptionally disciplined: every file carries valid `name`/`description` frontmatter with `name` matching its parent directory, and a full-corpus grep for the R01 vague-quantifier list (`appropriate`, `relevant`, `as needed`, `sufficient`, `adequate`, `reasonable`, `properly`, `correctly`, `some`, `several`, `various`) returned only two hits in one file. The three sub-100 rows below are the linter's own deliberately-malformed negative fixtures, not real defects — see Bugs section.

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| scripts/skill-format-check/tests/bad-skill/SKILL.md | skill (test fixture) | 50 | Missing `name` + `description` (intentional negative fixture) |
| scripts/skill-format-check/tests/bad-skill-no-frontmatter/SKILL.md | skill (test fixture) | 50 | No frontmatter block at all (intentional negative fixture) |
| scripts/skill-format-check/tests/bad-skill-unclosed-frontmatter/SKILL.md | skill (test fixture) | 50 | Unclosed frontmatter (`---`) makes `name`/`description` unparseable (intentional negative fixture) |
| skills/lark-event/SKILL.md | skill | 96 | 2x R01 vague quantifier ("some") |
| scripts/skill-format-check/tests/good-skill/SKILL.md | skill (test fixture) | 100 | — |
| scripts/skill-format-check/tests/good-skill-complex/SKILL.md | skill (test fixture) | 100 | — |
| scripts/skill-format-check/tests/good-skill-minimal/SKILL.md | skill (test fixture) | 100 | — |
| internal/qualitygate/skillscan/testdata/skills/lark-demo/SKILL.md | skill (Go test fixture) | 100 | — |
| skills/lark-whiteboard/SKILL.md | skill | 100 | — |
| skills/lark-wiki/SKILL.md | skill | 100 | — |
| skills/lark-calendar/SKILL.md | skill | 100 | — |
| skills/lark-okr/SKILL.md | skill | 100 | — |
| skills/lark-vc/SKILL.md | skill | 100 | — |
| skills/lark-im/SKILL.md | skill | 100 | — |
| skills/lark-sheets/SKILL.md | skill | 100 | — |
| skills/lark-markdown/SKILL.md | skill | 100 | — |
| skills/lark-approval/SKILL.md | skill | 100 | — |
| skills/lark-workflow-meeting-summary/SKILL.md | skill | 100 | — |
| skills/lark-slides/SKILL.md | skill | 100 | — |
| skills/lark-note/SKILL.md | skill | 100 | — |
| skills/lark-drive/SKILL.md | skill | 100 | — |
| skills/lark-openapi-explorer/SKILL.md | skill | 100 | — |
| skills/lark-task/SKILL.md | skill | 100 | — |
| skills/lark-vc-agent/SKILL.md | skill | 100 | — |
| skills/lark-workflow-standup-report/SKILL.md | skill | 100 | — |
| skills/lark-attendance/SKILL.md | skill | 100 | — |
| skills/lark-apps/SKILL.md | skill | 100 | — |
| skills/lark-contact/SKILL.md | skill | 100 | — |
| skills/lark-mail/SKILL.md | skill | 100 | — |
| skills/lark-doc/SKILL.md | skill | 100 | — |
| skills/lark-base/SKILL.md | skill | 100 | — |
| skills/lark-minutes/SKILL.md | skill | 100 | — |
| skills/lark-skill-maker/SKILL.md | skill | 100 | — |
| skills/lark-shared/SKILL.md | skill | 100 | — |
| tests/cli_e2e/cli-e2e-testcase-writer/SKILL.md | skill | 100 | — |

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 2 |
| Low | 1 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks | 0 files |
| Scripts (`.sh`/`.py`/`.js`, excluding README/JSON/SKILL.md fixtures under `scripts/`) | 27 files: 17 `.js` (`scripts/install.js`, `scripts/install-wizard.js`, `scripts/run.js`, `scripts/pr-labels/index.js`, `scripts/issue-labels/index.js`, `scripts/semantic-review-publish.js`, `scripts/semantic-review-verify-artifact.js`, `scripts/pr-quality-summary.js`, `scripts/ci-quality-summary-publish.js`, plus 8 `*.test.js`), 9 `.sh` (`scripts/build-pkg-pr-new.sh`, `scripts/tag-release.sh`, `scripts/check-skill-wire-vocab.sh`, `scripts/check-doc-tokens.sh`, `scripts/resolve-changed-from.sh`, plus 4 `*.test.sh` / workflow-contract tests), 1 `.py` (`scripts/fetch_meta.py`) |
| MCP configs (`.mcp.json`) | 0 files |
| Package manifests | `package.json` (npm, declares `postinstall`), `go.mod`/`go.sum` (out of the requested glob scope, not scanned) |
| `requirements.txt` | not present |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | package.json | 9 | SEC-postinstall-script | `"postinstall": "node scripts/install.js"` runs on every `npm install`. It downloads a prebuilt binary over HTTPS from a 3-host allowlist (`github.com`, `objects.githubusercontent.com`, `registry.npmmirror.com`), verifies it against a bundled `checksums.txt` SHA-256, and only then `chmod`s and installs it (see `scripts/install.js:99-104` allowlist check, `:288-311` checksum verification). This is the standard "npm ships a native/Go binary" pattern (same shape as esbuild/sharp) and is well-mitigated, but it is still a network-fetch-and-execute step that runs unattended and matches the rubric's blanket HIGH classification for postinstall scripts. |
| 2 | Medium | scripts/install-wizard.js | 254, 283-287 | SEC-runtime-package-install | The interactive `lark-cli install` wizard shells out to `npm install -g @larksuite/cli` (line 254) and `npx -y skills add <repo>` (lines 283-287) at runtime to self-update and fetch the AI-skills bundle from `open.feishu.cn` (with a GitHub fallback). Invoked only via explicit user-run `install` subcommand, uses `execFileSync`/`execFile` (array-arg, no shell string interpolation), and prompts for user confirmation before authorizing further scopes. |
| 3 | Medium | scripts/fetch_meta.py | 44-54 | SEC-network-call | `fetch_remote()` makes an unauthenticated `urllib.request.urlopen` GET to `https://open.feishu.cn/...` or `https://open.larksuite.com/...` (brand-selectable) to refresh `internal/registry/meta_data.json` at build time. HTTPS-only, hardcoded host map (`API_HOSTS`), 10s timeout, no credentials sent. Build-time developer tooling, not part of the shipped CLI's runtime path. |
| 4 | Low | package.json | 37 | SEC-unpinned-semver | `"@clack/prompts": "^1.2.0"` uses a caret range rather than an exact pin. Mitigated in practice by the committed `package-lock.json`, which pins the resolved version for reproducible installs; the caret range only affects fresh `npm update` runs. |

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | scripts/skill-format-check/tests/bad-skill/SKILL.md | Frontmatter has `version`/`metadata` but no `name` or `description` | None — this is the checker's own "must-fail" fixture (paired with `good-skill/SKILL.md`) used by `scripts/skill-format-check/index.js` and `test.sh` to prove the linter rejects malformed frontmatter. Not a real artifact; no PR warranted. |
| 2 | scripts/skill-format-check/tests/bad-skill-no-frontmatter/SKILL.md | No YAML frontmatter block at all | Same as above — intentional negative fixture, no PR warranted. |
| 3 | scripts/skill-format-check/tests/bad-skill-unclosed-frontmatter/SKILL.md | Frontmatter opens with `---` but has no closing `---`, so `name`/`description` are not parseable as frontmatter by a standard parser | Same as above — intentional negative fixture specifically for the "unclosed frontmatter" failure mode, no PR warranted. |

No real bugs (missing required fields, dangling cross-skill references, or undeclared-tool usage) were found in any of the 29 production/authored skills. Sibling-skill links (e.g. `../lark-doc/SKILL.md`, `../lark-shared/SKILL.md`, `../lark-vc/SKILL.md`) all resolve to directories that exist in `skills/`. Deep links into individual `references/*.md` files were out of scope for this pass (only the 35 listed `SKILL.md` files were read) and were not verified.

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/fetch_meta.py | Network call to external API has no explicit egress allowlist enforcement (relies solely on the hardcoded `API_HOSTS` dict) | No fix required — the host set is already a closed, hardcoded map with no user-controlled input reaching the URL beyond the `--brand` enum choice. Optional hardening: mirror `scripts/install.js`'s explicit `assertAllowedHost()` pattern for defense-in-depth consistency across the two Python/Node download paths. |
| 2 | package.json | `@clack/prompts` pinned with `^` instead of exact version | No fix required — `package-lock.json` already pins the resolved version for reproducible installs. Optional: switch to an exact version string if the team wants `package.json` itself (not just the lockfile) to be the source of truth. |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/lark-event/SKILL.md | R01 vague quantifier "some" used twice ("some also have `format`"; a second generic "some" reference) | -4 |

## Cross-Component

- **Frontmatter shape drift (informational, not penalized):** `skills/lark-shared/SKILL.md` declares only `name` and `description` in frontmatter, while all 26 other `lark-*` skills additionally declare `version` and `metadata.requires.bins: ["lark-cli"]`. `version`/`metadata` are optional under the open SKILL.md spec, so this is not a rule violation, but it is a real convention gap for the one skill every other skill tells the agent to read first (`**CRITICAL — ... MUST 先用 Read 工具读取 ../lark-shared/SKILL.md**` appears in 20+ sibling skills). Low-confidence, cosmetic — worth a one-line fix for consistency but not blocking.
- **No orphaned or unreferenced skills detected:** every `skills/lark-*` directory reviewed is reachable from at least one sibling "不在本 skill 范围" (out-of-scope) cross-reference table, and `lark-shared` is referenced as a mandatory read from effectively every other skill.
- **No stale-count or manifest-vs-disk drift found** within the scope of the 35 files read (this pass did not diff `skills/` against a plugin manifest or `CODEOWNERS`, since none of the requested files is that manifest).

## Recommendation

**REVIEW** — No NL-quality PRs are warranted: the only three sub-100-scoring files are the skill-format-checker's own intentional negative-test fixtures, and the one real quality nit (2x "some" in `lark-event/SKILL.md`, -4 points) is too minor to justify a standalone PR. On the security side, the single HIGH-severity pattern match (`package.json`'s `postinstall` → `scripts/install.js`) is a well-mitigated, industry-standard binary-distribution mechanism (HTTPS-only host allowlist + SHA-256 checksum verification before execution) — flag it in the audit issue for human sign-off rather than filing a private security report, since nothing here indicates unreviewed or exploitable behavior. The two Medium findings (runtime `npm install -g` / `npx skills add` in the interactive installer, and an unauthenticated build-time metadata fetch) and the one Low finding (a caret-range dependency already pinned by the committed lockfile) are informational only; no PRs recommended for either.
