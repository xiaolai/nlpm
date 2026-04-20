# NLPM Audit: aaron-he-zhu/seo-geo-claude-skills
**Date**: 2026-04-20  |  **Artifacts**: 38  |  **Strategy**: full
**NL Score**: 91/100
**Security**: CLEAR
**Bugs**: 3  |  **Quality Issues**: 21  |  **Security Findings**: 2

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/contract-lint.md | command | 80 | BUG: calls shasum + hash comparison without declaring `allowed-tools: ["Bash", "Grep", "Read"]`; checks are non-functional |
| commands/wiki-lint.md | command | 82 | Missing `allowed-tools`; 7-check table has no numbered sequential steps |
| commands/optimize-meta.md | command | 83 | Missing `allowed-tools`; no `argument-hint` field |
| commands/audit-domain.md | command | 88 | Missing `allowed-tools`; dispatches to WebFetch-using auditor without capability declaration |
| commands/p2-review.md | command | 88 | Missing `allowed-tools: ["Read"]`; reads deferred item files without tool declaration |
| commands/keyword-research.md | command | 85 | Missing `allowed-tools`; vague quantifiers: "comprehensive", "relevant" |
| commands/report.md | command | 85 | Missing `allowed-tools`; vague "appropriate reporting period" |
| commands/setup-alert.md | command | 85 | Missing `allowed-tools`; vague "appropriate thresholds" |
| commands/write-content.md | command | 85 | Missing `allowed-tools`; vague "comprehensive" |
| commands/geo-drift-check.md | command | 91 | Experimental label lacks version floor; vague "notable drift" threshold |
| commands/audit-page.md | command | 93 | Minor vague quantifiers: "thorough", "comprehensive" |
| commands/check-technical.md | command | 93 | Minor vague quantifiers: "appropriate" |
| commands/generate-schema.md | command | 93 | Minor vague quantifiers: "relevant" |
| commands/sync-versions.md | command | 93 | Minor: no argument-hint |
| commands/validate-library.md | command | 96 | None significant — best-in-class command |
| research/content-gap-analysis/SKILL.md | skill | 93 | Vague: "comprehensive", "significant", "appropriate" |
| research/competitor-analysis/SKILL.md | skill | 93 | Vague: "comprehensive", "innovative", "appropriate" |
| research/serp-analysis/SKILL.md | skill | 93 | Vague: "thorough", "comprehensive" |
| build/geo-content-optimizer/SKILL.md | skill | 93 | Vague: "comprehensive", "appropriate", "relevant" |
| build/meta-tags-optimizer/SKILL.md | skill | 92 | Vague: "appropriate", "relevant", "effective" |
| build/schema-markup-generator/SKILL.md | skill | 93 | Vague: "appropriate", "relevant" |
| monitor/rank-tracker/SKILL.md | skill | 93 | Vague: "significant", "appropriate" |
| monitor/backlink-analyzer/SKILL.md | skill | 93 | Vague: "significant", "comprehensive" |
| monitor/performance-reporter/SKILL.md | skill | 93 | Vague: "comprehensive", "appropriate" |
| monitor/alert-manager/SKILL.md | skill | 93 | Vague: "appropriate", "relevant" |
| optimize/internal-linking-optimizer/SKILL.md | skill | 93 | Vague: "comprehensive", "appropriate" |
| optimize/content-refresher/SKILL.md | skill | 93 | Vague: "comprehensive", "thorough" |
| cross-cutting/entity-optimizer/SKILL.md | skill | 93 | Vague: "relevant", "appropriate" |
| cross-cutting/memory-management/SKILL.md | skill | 93 | Vague: "relevant", "appropriate" |
| research/keyword-research/SKILL.md | skill | 95 | Vague: "appropriate", "relevant" (mitigated by explicit quality bar with numbers) |
| build/seo-content-writer/SKILL.md | skill | 95 | Vague: "comprehensive" (mitigated by banned-vocab list) |
| optimize/on-page-seo-auditor/SKILL.md | skill | 95 | Vague: "thorough" (mitigated by 11-step workflow) |
| optimize/technical-seo-checker/SKILL.md | skill | 95 | Vague: "appropriate" (mitigated by LLM-crawler handling specificity) |
| cross-cutting/content-quality-auditor/SKILL.md | skill | 95 | None significant — auditor-class with inline runbook |
| cross-cutting/domain-authority-auditor/SKILL.md | skill | 95 | None significant — auditor-class with inline runbook |
| CLAUDE.md | doc | 88 | Vague: "comprehensive", "appropriate"; some contribution rules reference external scripts now removed |
| hooks/hooks.json | hook | 87 | "Complete silence" instruction in Artifact Gate hook may suppress useful advisory output on edge cases |
| .claude-plugin/plugin.json | json | 90 | Well-formed; version 9.0.1 in manifest vs 9.0.0 in all SKILL.md files — minor drift |

**Weighted average**: 91/100 (commands: 88.0 avg; skills: 93.6 avg; infra: 88.3 avg)

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 2 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks JSON | hooks/hooks.json |
| Shell scripts | scripts/validate-skill.sh |
| MCP configs | .mcp.json |
| Package manifests | None found |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | LOW | .mcp.json | 1–60 | HTTP MCP servers — 14 external API endpoints | All 14 MCP servers use `"type": "http"`. No API keys stored in config (supplied at runtime). All domains are established SaaS providers (ahrefs.com, semrush.com, hubspot.com, etc.). No localhost or suspicious endpoints. Low risk: HTTP MCP requires auth at connection time, not execution time. No stdio servers that would spawn local processes. |
| 2 | LOW | scripts/validate-skill.sh | 13–14 | `cd "$(dirname "$0")/.."` path construction | Uses `dirname "$0"` to find repo root. If script is invoked via a symlink across filesystem boundaries, the computed repo root may be incorrect. No security impact — the script performs read-only validation only (no writes, no network calls, no `eval`, no credential access). All `$1` input is used as a file path argument to `-f` tests only, never exec'd. |

### Hooks Analysis

All 5 hook events (SessionStart, UserPromptSubmit, PostToolUse, FileChanged, Stop) use `"type": "prompt"`. No shell execution at any hook trigger point. The PostToolUse Artifact Gate hook (line 47) instructs Claude to validate auditor-class handoffs and emit "complete silence" for non-auditor files — this is a natural-language instruction, not executable code. No credential access, no network calls from hooks.

## Bugs (Must Fix)

| # | File | Severity | Description | Fix |
|---|------|----------|-------------|-----|
| 1 | commands/contract-lint.md | HIGH | Command explicitly specifies SHA-256 hash verification (comparing `source_sha256` against live `shasum` output) and uses `awk`/Grep pattern inspection, but declares no `allowed-tools`. Without `Bash` and `Grep`, the hash comparison and pattern scanning steps cannot execute. The command's core functionality is non-functional as specified. | Add `allowed-tools: ["Read", "Grep", "Bash"]` to frontmatter |
| 2 | commands/wiki-lint.md | MEDIUM | 7-check validation table lists checks to perform but provides no numbered sequential workflow steps. The command has no procedural instruction for which tool to use per check or in what order. Agents cannot reliably reproduce consistent output without step ordering. | Add a numbered workflow section beneath the check table (e.g., "Step 1: Glob all `memory/wiki/*.md` files…") |
| 3 | .claude-plugin/plugin.json | LOW | Plugin manifest declares `"version": "9.0.1"` while all 20 SKILL.md files declare `version: "9.0.0"` in their frontmatter. This creates version drift that `/seo:validate-library` check #6 is designed to catch, suggesting the sync step was skipped after a patch release. | Run `/seo:sync-versions` to propagate the manifest version to all SKILL.md files, or bump plugin.json back to 9.0.0 if the patch was not yet applied to skills |

## Security Fixes

No security fixes required. All execution surfaces are CLEAR.

## Quality Issues (Should Fix)

| # | Files | Issue | Recommendation |
|---|-------|--------|----------------|
| 1 | commands/audit-domain.md, commands/keyword-research.md, commands/optimize-meta.md, commands/p2-review.md, commands/report.md, commands/setup-alert.md, commands/write-content.md | 7 of 15 commands missing `allowed-tools` field entirely | For dispatch-only commands, add `allowed-tools: []` (explicit empty). For commands that read files to gather context (p2-review, audit-domain), add the appropriate tool list. Follow `commands/validate-library.md` as the pattern: it fully declares `["Read", "Glob", "Grep", "Bash"]` |
| 2 | 18 of 20 SKILL.md files | Vague quantifiers: "comprehensive", "appropriate", "thorough", "significant", "relevant" appear across nearly all skills | Replace with measurable alternatives per scoring rules: "comprehensive" → "covering all 8 CORE-EEAT dimensions"; "appropriate" → the specific threshold value; "thorough" → "covering all checklist items"; "significant" → ">10% change" |
| 3 | commands/audit-domain.md, commands/optimize-meta.md, commands/wiki-lint.md, commands/p2-review.md | Missing `argument-hint` field | Add `argument-hint` matching the command's expected input format (e.g., `<domain>`, `<url>`, `[keyword]`) |
| 4 | hooks/hooks.json (Stop hook, line 81) | Stop hook auto-appends critical veto items (`T04`, `C01`, `R10`, `T03`, `T05`, `T09`) to every session-end message. If the user has not run an audit, this produces confusing output referencing framework items with no prior context. | Add a conditional: only emit veto reminders if an audit result exists in the current session context (e.g., check for `CORE-EEAT` or `CITE` in prior output) |
| 5 | commands/geo-drift-check.md | "Experimental, v9.0+" label in CLAUDE.md but the command body does not repeat this caveat or define what "drift" threshold triggers an alert | Define a numeric drift threshold in the command body (e.g., "GEO Score drop ≥5 points since last snapshot constitutes notable drift") |
| 6 | CLAUDE.md | Contribution rules reference `scripts/sync-versions.py` and `scripts/validate-descriptions.py` in the past tense ("replaces scripts/...") but these files no longer exist in the repo. Stale references may confuse contributors. | Remove the parenthetical "replaces scripts/..." notes from the Commands section, or replace with a link to the git commit that removed them |
| 7 | cross-cutting/content-quality-auditor/SKILL.md, cross-cutting/domain-authority-auditor/SKILL.md | Both auditor-class skills carry the identical `source_sha256` and `block_sha256` values in their runbook-sync markers. If the shared Auditor Runbook §1-5 source is updated, both files must be re-synced atomically. There is no automated CI check verifying the inline block matches the source. | Add a CI step (or a `/seo:contract-lint` check) that recomputes `block_sha256` from the inline content and fails if it differs from the declared value |
| 8 | All 20 SKILL.md files | `metadata.geo-relevance` values are hardcoded ("high", "medium") with no documented scoring rubric explaining what differentiates "high" from "medium" for GEO relevance | Add a one-line comment or footnote in CLAUDE.md defining the geo-relevance tiers (e.g., "high = skill directly produces AI-citation-ready content; medium = skill informs strategy that may affect GEO") |
| 9 | research/competitor-analysis/SKILL.md, optimize/internal-linking-optimizer/SKILL.md | Include a scraping legality note ("verify robots.txt, respect Crawl-delay, confirm TOS permits automated access") but do not enforce or prompt the user to confirm before proceeding | Add a mandatory user-confirmation checkpoint: "Before crawling [domain], confirm: (1) robots.txt permits access, (2) you have authorization. Proceed? [yes/no]" |
| 10 | hooks/hooks.json | The FileChanged hook (matcher: "hot-cache.md") fires on any edit to hot-cache.md and instructs Claude to "check HOT tier size, trim to 80 lines if needed". If two concurrent sessions both edit hot-cache.md, the trim logic may produce a race condition | Document in CLAUDE.md that the memory system assumes single-session usage; add a note that concurrent session writes to hot-cache.md are not supported |
| 11 | commands/report.md | "Cross-project mode" is described but the command provides no guidance on how to discover which projects exist or where to find their `memory/` directories | Add a discovery step: "Glob `../*/memory/hot-cache.md` to enumerate active projects, then prompt user to confirm scope before aggregating" |
| 12 | build/seo-content-writer/SKILL.md | Banned-vocabulary list (crucial, robust, leverage, delve, etc.) is comprehensive but has no mechanism to enforce it — the skill instructs Claude not to use these words but has no self-check step | Add a validation checkpoint at the end: "Before delivery, scan output for banned words. If any found, rewrite those sentences." |
| 13 | monitor/performance-reporter/SKILL.md | 11-step workflow integrates CORE-EEAT and CITE scores but does not specify which version of the scoring frameworks to use if the user has a custom override in `.claude/nlpm.local.md` | Add: "If the project has a `.claude/nlpm.local.md` with threshold overrides, apply those thresholds to the CORE-EEAT and CITE pass/fail gates." |
| 14 | cross-cutting/memory-management/SKILL.md | GDPR Art 17 deletion flow is documented but the skill does not specify what happens to cross-references in `memory/hot-cache.md` and `memory/decisions.md` when a subject-data record is deleted from WARM tier | Add: "On deletion, also scan hot-cache.md and decisions.md for references to the deleted entity and remove or anonymize them." |
| 15 | All research skills | The `Next Best Skill` section uses markdown links to GitHub URLs. If the repo is forked or the library is installed locally, these links break. | Replace GitHub links in `Next Best Skill` sections with relative paths (e.g., `../../build/seo-content-writer/SKILL.md`) or use skill names only (the runtime resolves them) |
| 16 | commands/p2-review.md | Tombstone rule states "tombstone review: 2026-07-10" — a hard-coded date in a command definition. If the command is not updated by that date, the review instruction becomes permanently stale | Replace the hard-coded date with a relative expression: "Tombstone review: 90 days after the v7.1.0 release date (see VERSIONS.md)" |
| 17 | commands/sync-versions.md | Step 5 says to verify all 3 cross-agent manifests match but does not specify how to verify `gemini-extension.json` and `qwen-extension.json` — they aren't in the standard plugin path | Add explicit file paths for the 3 cross-agent manifests in step 5 and a Grep verification line |
| 18 | optimize/technical-seo-checker/SKILL.md | LLM Crawler Handling section names specific bots (GPTBot, ClaudeBot, PerplexityBot) but does not note that this list changes as new AI crawlers emerge | Add: "For an up-to-date list of LLM crawlers and their user agent strings, refer to each provider's published documentation. This list reflects known crawlers as of v9.0.0." |
| 19 | build/schema-markup-generator/SKILL.md | FTC disclosure note for `aggregateRating` is present but applies only to US/FTC jurisdiction. EU users under the Digital Services Act (DSA) have additional requirements for review authenticity. | Expand the disclosure note: "US: FTC requires disclosure of material connections. EU/DSA: Ensure reviews meet authenticity requirements of Regulation (EU) 2022/2065 Art. 6." |
| 20 | All 20 SKILL.md files | `Save Results` section is identical across all 20 skills — copied verbatim. The section asks "Save these results for future sessions?" but skills that are used in pipeline mode (handoff chain) may save redundantly. | Add a condition: "If running in handoff mode (previous skill result already saved this session), skip the save prompt and reference the prior memory entry instead." |
| 21 | hooks/hooks.json | UserPromptSubmit hook (line 36) fires on every prompt submission and instructs Claude to "check if hot-cache.md should be updated." For long sessions this creates a high-frequency background instruction that may inflate context | Consider moving the hot-cache update check to the PostToolUse hook (matcher: "Write|Edit") so it only fires when files are actually written, not on every user message |

## Cross-Component Notes

1. **Contract-lint / runbook-sync circular dependency**: `commands/contract-lint.md` is responsible for verifying that the runbook-sync SHA markers in `cross-cutting/content-quality-auditor/SKILL.md` and `cross-cutting/domain-authority-auditor/SKILL.md` are correct. But `contract-lint.md` itself is missing the `Bash` and `Grep` tools needed to run `shasum` and compare hashes (Bug #1). This means the primary integrity check for the library's most critical invariant cannot execute.

2. **validate-library / sync-versions version gate**: `commands/validate-library.md` check #6 detects version drift between `plugin.json` and `marketplace.json`. It correctly catches the root cause of Bug #3 (plugin.json at 9.0.1, skills at 9.0.0). Running `/seo:validate-library` before `/seo:sync-versions` would have surfaced this. The gate is well-designed; the process was not followed.

3. **Wiki layer / memory-management coupling**: `CLAUDE.md` documents a `memory/wiki/` wiki layer (proposal-wiki-layer-v3) that is auto-refreshed by the `memory-management` skill. However, no hook event fires on wiki reads or writes — only on `hot-cache.md` changes. If the wiki layer becomes the primary entry point for returning sessions, the FileChanged hook coverage gap means stale wiki entries are not auto-detected.

4. **Trigger overlap between skills**: `research/competitor-analysis/SKILL.md` and `research/content-gap-analysis/SKILL.md` both trigger on "what content should I create" class of queries. The `keyword-research` skill also responds to "I need content ideas". For a user asking a generic discovery question, all three skills may activate, producing redundant output. Consider adding mutual-exclusion guidance or a routing note in CLAUDE.md.

5. **scraping legality enforcement gap**: Two skills (`competitor-analysis`, `internal-linking-optimizer`) include a scraping legality note in the "Data Sources" section, but 4 other skills that recommend crawling competitor pages (`serp-analysis`, `backlink-analyzer`, `content-gap-analysis`, `technical-seo-checker`) do not. This is an inconsistent safety surface — the warning appears where the author remembered to add it, not where it is most needed.

## Recommendation

**APPROVED — conditional on 3 fixes before contribution PR.**

The library is a high-quality, production-ready SEO/GEO skills plugin. The 20 SKILL.md files are consistently well-structured with full frontmatter, multilingual triggers (7 languages), numbered workflows, handoff summaries, and the CORE-EEAT / CITE quality frameworks wired throughout. The auditor-class skills (`content-quality-auditor`, `domain-authority-auditor`) demonstrate best-in-class implementation with inline runbook sync, SHA integrity markers, and a 7-item Artifact Gate. The security posture is excellent — all hooks are prompt-type with no executable code, the single shell script is read-only with no network access, and the MCP config uses only established HTTP endpoints.

The primary weakness is in the **command layer**: 9 of 15 commands omit `allowed-tools`, and the most critical command (`contract-lint`) is functionally broken because it specifies hash-verification operations it cannot perform without `Bash` and `Grep`. Fix Bug #1 before the contribution PR; it directly undermines the library's own integrity-checking mechanism.

**Required before PR** (Bugs #1–#3): fix `contract-lint.md` tool declaration, add sequential steps to `wiki-lint.md`, and resolve the plugin.json / SKILL.md version drift.

**Recommended before PR** (Quality Issues #1, #2, #7): declare `allowed-tools` on all commands, replace the top-frequency vague quantifiers, and add CI verification for runbook-sync SHA markers.

**Contribution scope**: NL quality improvements to command layer only (Bugs #1–#3 + Quality Issues #1–#3). Do not modify SKILL.md files or the auditor-class runbook — these are high-quality and modification risk exceeds benefit.
