# NLPM Audit: firecrawl/firecrawl-claude-plugin
**Date**: 2026-04-06  |  **Artifacts**: 12  |  **Strategy**: single
**NL Score**: 97/100
**Security**: CLEAR
**Bugs**: 2  |  **Quality Issues**: 12  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/skill-gen.md | command | 73 | No allowed-tools, no empty-input handling, 6 vague quantifiers |
| skills/firecrawl-monitor/SKILL.md | skill | 96 | Vague: "concise" (L145), "broad" (L149) |
| skills/firecrawl-agent/SKILL.md | skill | 98 | Vague: "complex" in description |
| skills/firecrawl-cli/SKILL.md | skill | 98 | Vague: "concise" (L81); name/directory mismatch (bug) |
| .claude-plugin/plugin.json | manifest | 100 | Clean |
| skills/firecrawl-crawl/SKILL.md | skill | 100 | Clean |
| skills/firecrawl-download/SKILL.md | skill | 100 | Clean |
| skills/firecrawl-interact/SKILL.md | skill | 100 | Clean |
| skills/firecrawl-map/SKILL.md | skill | 100 | Clean |
| skills/firecrawl-parse/SKILL.md | skill | 100 | Clean |
| skills/firecrawl-scrape/SKILL.md | skill | 100 | Clean |
| skills/firecrawl-search/SKILL.md | skill | 100 | Clean |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts | 0 |
| MCP configs | 0 |
| Package manifests | 0 |

### Security Findings

No security findings.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | skills/firecrawl-cli/SKILL.md | `name: firecrawl` does not match parent directory `firecrawl-cli`; commands/skill-gen.md (the plugin's own format reference, L83) explicitly requires the name field to match the directory name exactly | Potential skill registration failure or name collision; downstream skills reference the skill as `firecrawl-cli` but the registry name would be `firecrawl` |
| 2 | skills/firecrawl-cli/SKILL.md | References `firecrawl-build` and `firecrawl-workflows` skill families (L16, L224–225) that are not listed in plugin.json's `skills` array and are not present as subdirectories in this repo | Users loading this plugin are told to use skills that are not installed with it; silent missing dependency |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| — | — | No security findings | — |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/skill-gen.md | Missing `allowed-tools` in frontmatter; command uses Write, Read, Bash, and wc but declares no tool constraints | -5 |
| 2 | commands/skill-gen.md | No empty-input handling: Step 1 proceeds directly to `firecrawl map $ARGUMENTS` with no branch for a missing or blank URL | -10 |
| 3 | commands/skill-gen.md | Vague: "production-ready" (L8) — no acceptance criteria | -2 |
| 4 | commands/skill-gen.md | Vague: "beneficial" (L8) — "include information that is beneficial" lacks a concrete signal | -2 |
| 5 | commands/skill-gen.md | Vague: "relevant pages" (L16) — a specific list follows in L22–29 but this trigger phrase underspecifies the filter criterion | -2 |
| 6 | commands/skill-gen.md | Vague: "brief" (L33) — "ask 1-2 brief questions" gives no length or scope constraint | -2 |
| 7 | commands/skill-gen.md | Vague: "primary" (L37) — "2-3 primary use cases" needs a ranking signal (most frequent? most complex? user-stated?) | -2 |
| 8 | commands/skill-gen.md | Vague: "representative sample" (L78) — no criterion for what makes a sample representative across diverse script types | -2 |
| 9 | skills/firecrawl-agent/SKILL.md | Vague: "complex" (description, L3) — "complex multi-page sites" without a concrete threshold (page count, nav depth, JS requirement) | -2 |
| 10 | skills/firecrawl-cli/SKILL.md | Vague: "concise" (L81) — "a concise 2-3 sentence monitor goal"; the sentence count is concrete but "concise" adds noise without adding meaning | -2 |
| 11 | skills/firecrawl-monitor/SKILL.md | Vague: "concise" (L145) — same pattern as above; the 2-3 sentence constraint already enforces brevity | -2 |
| 12 | skills/firecrawl-monitor/SKILL.md | Vague: "broad" (L149) — "keep the goal broad rather than guessing exclusions" is ambiguous; a concrete instruction ("omit exclusions" or "use the user's phrasing verbatim") would be actionable | -2 |

## Cross-Component

**Interval inconsistency (high confidence):** `skills/firecrawl-cli/SKILL.md` L137 states the minimum monitor schedule interval is **5 minutes**; `skills/firecrawl-monitor/SKILL.md` L120 states it is **15 minutes**. Both claim to document the same constraint. The monitor skill is more authoritative on this point. The CLI skill's value is likely stale.

**Missing skill family references:** `skills/firecrawl-cli/SKILL.md` directs users to `firecrawl-build` and `firecrawl-workflows` skill families (L16 and L224–225). These are not in `plugin.json`'s `skills` array, not present as directories in the repo, and not among the 10 registered skills. The skill text implies they are installed alongside this plugin ("already installed alongside this CLI skill when you run `firecrawl init`"), but this plugin has no mechanism to install them. Users will encounter missing-skill errors.

**Broken relative links (low confidence, advisory):** Six SKILL.md files (`firecrawl-scrape`, `firecrawl-crawl`, `firecrawl-interact`, `firecrawl-map`, `firecrawl-monitor`, `firecrawl-search`) link to the workflow escalation pattern using bare `(firecrawl-cli)` as the href (e.g., `[workflow escalation pattern](firecrawl-cli)`). As standard relative markdown, these resolve to a non-existent peer path rather than `../firecrawl-cli/SKILL.md`. In Claude Code's agent context the agent reads the text and understands the intent, so this is advisory only — but a tool that validates markdown links would report these as broken.

**All cross-references within the skills/** directory and `rules/` subdirectory (`../firecrawl-*/SKILL.md`, `rules/install.md`, `rules/security.md`) are valid and resolve to existing files.

## Recommendation

CLEAR — submit PRs for both bugs and the interval correction. Security gate passed with no findings.

Priority order:
1. **Bug #2** (missing firecrawl-build/firecrawl-workflows): update the firecrawl-cli skill body to note these are separate plugins requiring separate installation, or remove the references if the skills do not exist externally.
2. **Cross-component interval fix**: align both files to the correct minimum interval (verify against the Firecrawl API docs; firecrawl-monitor's 15-minute claim carries more context and is likely correct).
3. **Bug #1** (name/directory mismatch): rename the `name` field in `skills/firecrawl-cli/SKILL.md` to `firecrawl-cli`, or rename the directory to `firecrawl` if the intent is to register the skill under that name.
4. **Quality**: add `allowed-tools` and empty-input guard to `commands/skill-gen.md`; remove or replace the six flagged vague quantifiers.
