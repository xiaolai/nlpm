# NLPM Audit: VoltAgent/awesome-claude-code-subagents
**Date**: 2026-04-06  |  **Artifacts**: 11  |  **Strategy**: single
**NL Score**: 98/100
**Security**: BLOCKED
**Bugs**: 0  |  **Quality Issues**: 4  |  **Security Findings**: 6

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| CLAUDE.md | Memory File | 78 | No build/run command instructions (R33, -10) |
| categories/01-core-development/.claude-plugin/plugin.json | plugin.json | 100 | None — required fields present, semver valid |
| categories/02-language-specialists/.claude-plugin/plugin.json | plugin.json | 100 | None — required fields present, semver valid |
| categories/03-infrastructure/.claude-plugin/plugin.json | plugin.json | 100 | None — required fields present, semver valid |
| categories/04-quality-security/.claude-plugin/plugin.json | plugin.json | 100 | None — required fields present, semver valid |
| categories/05-data-ai/.claude-plugin/plugin.json | plugin.json | 100 | None — required fields present, semver valid |
| categories/06-developer-experience/.claude-plugin/plugin.json | plugin.json | 100 | None — required fields present, semver valid |
| categories/07-specialized-domains/.claude-plugin/plugin.json | plugin.json | 100 | None — required fields present, semver valid |
| categories/08-business-product/.claude-plugin/plugin.json | plugin.json | 100 | None — required fields present, semver valid |
| categories/09-meta-orchestration/.claude-plugin/plugin.json | plugin.json | 100 | None — required fields present, semver valid |
| categories/10-research-analysis/.claude-plugin/plugin.json | plugin.json | 100 | None — required fields present, semver valid |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 |
| Medium | 4 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | None found |
| Scripts | `install-agents.sh`, `tools/subagent-catalog/config.sh` |
| MCP configs | None found |
| Package manifests | None found (no `package.json` / `requirements.txt`) |
| Command-like NL artifacts invoking Bash with user args | `tools/subagent-catalog/search.md`, `tools/subagent-catalog/fetch.md`, `tools/subagent-catalog/invalidate.md`, `tools/subagent-catalog/list.md` |
| CI workflows | `.github/workflows/enforce-plugin-version-bump.yml` (reviewed, clean — no external input, no secrets, no dangerous patterns) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | High | tools/subagent-catalog/fetch.md | 51 | unsanitized-arg-interpolation | `grep -iF "{{NAME}}" "$SUBAGENT_CATALOG_CACHE_FILE"` — the `{{NAME}}` placeholder is filled in from user-supplied `$ARGUMENTS` and substituted directly into the shell command template with no escaping guidance; an argument containing a `"` plus shell metacharacters can break out of the quoted string when the interpreting agent builds the literal Bash call. |
| 2 | High | tools/subagent-catalog/fetch.md | 60 | unsanitized-arg-interpolation | `curl -sf "$SUBAGENT_CATALOG_REPO_URL/{{PATH}}" -o "$tmp_file"` — `{{PATH}}` is substituted unsanitized into a curl URL/shell command with no validation of its contents, enabling path traversal or shell injection if the substituted value contains shell metacharacters. |
| 3 | Medium | install-agents.sh | 55 | network-call | Unauthenticated `curl` to the GitHub API (`fetch_categories_remote`) in remote mode, response parsed with `grep`/`sed` rather than a JSON parser. |
| 4 | Medium | install-agents.sh | 85 | network-call | Unauthenticated `curl` to the GitHub API (`fetch_agents_remote`) to list agent files for a category. |
| 5 | Medium | install-agents.sh | 110 | network-call | `download_agent` fetches a remote `.md` agent definition via `curl` and writes it straight into `~/.claude/agents/` or `.claude/agents/` with no integrity/checksum verification and no pinning to a commit SHA (tracks mutable `main`). |
| 6 | Medium | tools/subagent-catalog/config.sh | 40 | network-call | `_subagent_catalog_fetch` does an unauthenticated `curl` of `README.md` from `raw.githubusercontent.com` on the mutable `main` ref, caches it locally with no signature/checksum verification. |

## Bugs (PR-worthy)
No bugs found. All 10 `plugin.json` manifests declare `name`, a valid semver `version`, and `description`; each manifest's `agents` array matches the `.md` files present on disk exactly (verified by diff, no manifest-vs-disk gaps); `.claude-plugin/marketplace.json` versions match their corresponding category `plugin.json` versions 1:1.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | install-agents.sh | Remote category/agent listing and agent download pull from the mutable `main` branch with no content verification (lines 55, 85, 110) | Pin `GITHUB_API_BASE`/`GITHUB_RAW_BASE` to a tagged release or commit SHA, and validate that downloaded content has YAML frontmatter (`^---`) before writing it into the install directory. |
| 2 | tools/subagent-catalog/config.sh | Cache fetch (line 40) pulls `README.md` from the mutable `main` ref with no integrity check | Pin `SUBAGENT_CATALOG_REPO_URL` to a tagged release/commit SHA, or at minimum verify the fetched content looks like the expected catalog format before caching it. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | CLAUDE.md | No build/run command instructions (R33) | -10 |
| 2 | CLAUDE.md | No test command instructions (R34) | -5 |
| 3 | CLAUDE.md | No prerequisites section (required tools/versions/setup) | -5 |
| 4 | CLAUDE.md | Vague quantifier "appropriate" at line 58 ("Add link in appropriate category") with no measurable criteria (R01) | -2 |

## Cross-Component
- All 10 category `plugin.json` `agents` arrays match the `.md` files present on disk exactly — no manifest-vs-disk gaps, no orphaned or missing agent references (154 total agent files across all categories, matching the `154 specialized ... subagents` count in `.claude-plugin/marketplace.json`).
- `.claude-plugin/marketplace.json` per-plugin `version` fields match each category's `plugin.json` `version` exactly — consistent with the repo's own `enforce-plugin-version-bump.yml` CI gate, which already asserts this invariant on every PR.
- `tools/subagent-catalog/*.md` (search/fetch/list/invalidate) are not referenced by any `plugin.json` — this is by design per `tools/subagent-catalog/README.md`, which documents them as a separately-installed tool (`cp -r tools/subagent-catalog ~/.claude/commands/`), not an orphaned component.
- No `@`-import syntax, no broken relative file references, and no stale file/function mentions found in CLAUDE.md.

## Recommendation
BLOCKED — do not submit PRs. File private security report for the two High-severity unsanitized-argument-interpolation findings in `tools/subagent-catalog/fetch.md` (lines 51 and 60) before any public contribution. There are no NL bugs to fix; once the High findings are privately disclosed and resolved, the two Medium security fixes (unpinned/mutable-ref fetches with no content verification) and the four informational CLAUDE.md quality issues are safe to submit as follow-up PRs.
