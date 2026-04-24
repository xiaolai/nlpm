# NLPM Re-Audit: sickn33/antigravity-awesome-skills

**Date**: 2026-04-24  |  **Artifacts**: 100  |  **Strategy**: progressive
**NL Score**: 96/100
**Bugs**: 8  |  **Quality Issues**: 14

> Re-audit against HEAD following the original audit dated 2026-04-17. Scores 100 files: 51 SKILL.md, 8 CLAUDE.md navigation guides, 41 plugin.json manifests. All files read in full. See original audit at `sickn33-antigravity-awesome-skills.md` for context on findings not in scope here (security scan, full bundle cross-section).

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| plugins/antigravity-awesome-skills/skills/dbos-python/CLAUDE.md | claude.md | 50 | No YAML frontmatter — missing `name` (-25) and `description` (-25) |
| plugins/antigravity-awesome-skills/skills/dbos-golang/CLAUDE.md | claude.md | 50 | No YAML frontmatter — missing `name` (-25) and `description` (-25) |
| plugins/antigravity-awesome-skills/skills/dbos-typescript/CLAUDE.md | claude.md | 50 | No YAML frontmatter — missing `name` (-25) and `description` (-25) |
| plugins/antigravity-awesome-skills-claude/skills/dbos-python/CLAUDE.md | claude.md | 50 | No YAML frontmatter — missing `name` (-25) and `description` (-25) |
| plugins/antigravity-awesome-skills-claude/skills/dbos-golang/CLAUDE.md | claude.md | 50 | No YAML frontmatter — missing `name` (-25) and `description` (-25) |
| plugins/antigravity-awesome-skills-claude/skills/dbos-typescript/CLAUDE.md | claude.md | 50 | No YAML frontmatter — missing `name` (-25) and `description` (-25) |
| plugins/antigravity-awesome-skills-claude/skills/loki-mode/CLAUDE.md | claude.md | 50 | No YAML frontmatter — missing `name` (-25) and `description` (-25) |
| skills/loki-mode/CLAUDE.md | claude.md | 50 | No YAML frontmatter — missing `name` (-25) and `description` (-25) |
| plugins/antigravity-awesome-skills/skills/filesystem-context/SKILL.md | skill | 94 | Vague: "relevant" ×3 = -6 |
| plugins/antigravity-awesome-skills/skills/referral-program/SKILL.md | skill | 96 | Vague: "appropriate" ×1, "relevant" ×1 = -4 |
| plugins/antigravity-awesome-skills/skills/remotion/SKILL.md | skill | 96 | Vague: "appropriate" ×1, "relevant" ×1 = -4 |
| plugins/antigravity-awesome-skills/skills/observability-monitoring-monitor-setup/SKILL.md | skill | 98 | Vague: "relevant" ×1 = -2 |
| plugins/antigravity-awesome-skills/skills/azure-ai-projects-dotnet/SKILL.md | skill | 98 | Vague: "appropriate" ×1 = -2 |
| plugins/antigravity-awesome-skills/skills/prompt-engineer/SKILL.md | skill | 98 | Vague: "Appropriate level" ×1 = -2 |
| plugins/antigravity-awesome-skills/skills/brainstorming/SKILL.md | skill | 98 | Vague: "reasonable defaults" ×1 = -2 |
| plugins/antigravity-awesome-skills/skills/azure-ai-agents-persistent-java/SKILL.md | skill | 98 | Vague: "appropriate delays" ×1 = -2 |
| plugins/antigravity-awesome-skills/skills/tailwind-design-system/SKILL.md | skill | 98 | Vague: "relevant best practices" ×1 = -2 |
| plugins/antigravity-awesome-skills/skills/gdpr-data-handling/SKILL.md | skill | 98 | Vague: "relevant best practices" ×1 = -2 |
| plugins/antigravity-awesome-skills/skills/hig-components-dialogs/SKILL.md | skill | 98 | Vague: "Appropriately sized" ×1 = -2 |
| plugins/antigravity-awesome-skills/skills/python-testing-patterns/SKILL.md | skill | 98 | Vague: "relevant best practices" ×1 = -2 |
| plugins/antigravity-awesome-skills/skills/senior-architect/SKILL.md | skill | 98 | Vague: "appropriate caching" ×1 = -2 |
| plugins/antigravity-awesome-skills/skills/nx-workspace-patterns/SKILL.md | skill | 98 | Vague: "relevant" ×1 = -2 |
| plugins/antigravity-awesome-skills/skills/makepad-font/SKILL.md | skill | 98 | Vague: "relevant" ×1 = -2 |
| plugins/antigravity-awesome-skills/skills/graphql-architect/SKILL.md | skill | 98 | Vague: "relevant" ×1 = -2 |
| plugins/antigravity-awesome-skills/skills/dropbox-automation/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/react-flow-architect/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/blog-writing-guide/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/protect-mcp-governance/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/wiki-vitepress/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/hig-components-content/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/youtube-summarizer/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/godot-4-migration/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/leiloeiro-ia/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/nerdzao-elite-gemini-high/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/hubspot-automation/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/n8n-code-javascript/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/lambda-lang/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/firecrawl-scraper/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/fitness-analyzer/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/django-perf-review/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/testing-qa/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/hig-foundations/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/saas-multi-tenant/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/receiving-code-review/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/azure-mgmt-arizeaiobservabilityeval-dotnet/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/project-skill-audit/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/hugging-face-evaluation/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/defi-protocol-templates/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/azure-eventgrid-py/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/azure-keyvault-secrets-rust/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/twitter-automation/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/database-migration/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/itil-expert/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/podcast-generation/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/zoho-crm-automation/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/googlesheets-automation/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/dbos-python/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/seo-aeo-blog-writer/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/database/SKILL.md | skill | 100 | Clean |
| plugins/antigravity-awesome-skills/skills/hugging-face-trackio/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-web-wizard/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-qa-testing/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-automation-builder/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-full-stack-developer/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-data-analytics/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-commerce-payments/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-integration-apis/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-web-designer/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-architecture-design/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-odoo-erp/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-revops-crm-automation/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-startup-founder/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-data-engineering/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-makepad-builder/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-agent-architect/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-azure-ai-cloud/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-oss-maintainer/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-essentials/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-typescript-javascript/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-security-engineer/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-seo-specialist/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-devops-cloud/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-business-analyst/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-documents-presentations/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-apple-platform-design/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-awesome-skills-claude/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-awesome-skills-claude/skills/hugging-face-trackio/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-indie-game-dev/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-python-pro/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-ddd-evented-architecture/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-creative-director/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-observability-monitoring/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-expo-react-native/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-mobile-developer/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-security-developer/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-llm-application-developer/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-marketing-growth/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| plugins/antigravity-bundle-systems-programming/.claude-plugin/plugin.json | plugin.json | 100 | Clean |
| .claude-plugin/plugin.json | plugin.json | 100 | Clean |
| skills/hugging-face-trackio/.claude-plugin/plugin.json | plugin.json | 100 | Clean |

**Score distribution:**

| Score | Count | Artifact types |
|-------|-------|----------------|
| 100 | 76 | 35 skill, 41 plugin.json |
| 98 | 13 | 13 skill |
| 96 | 2 | 2 skill |
| 94 | 1 | 1 skill |
| 50 | 8 | 8 CLAUDE.md |

**Overall NL Score: 96/100** (sum 9560 / 100 files)

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | plugins/antigravity-awesome-skills/skills/dbos-python/CLAUDE.md | No YAML frontmatter — `name` and `description` both missing | NLPM scanner will not recognise the file as a valid artifact; score 50/100 |
| 2 | plugins/antigravity-awesome-skills/skills/dbos-golang/CLAUDE.md | No YAML frontmatter — `name` and `description` both missing | Same as above; score 50/100 |
| 3 | plugins/antigravity-awesome-skills/skills/dbos-typescript/CLAUDE.md | No YAML frontmatter — `name` and `description` both missing | Same as above; score 50/100 |
| 4 | plugins/antigravity-awesome-skills-claude/skills/dbos-python/CLAUDE.md | No YAML frontmatter — `name` and `description` both missing | Duplicate of Bug #1 in -claude collection; score 50/100 |
| 5 | plugins/antigravity-awesome-skills-claude/skills/dbos-golang/CLAUDE.md | No YAML frontmatter — `name` and `description` both missing | Duplicate of Bug #2 in -claude collection; score 50/100 |
| 6 | plugins/antigravity-awesome-skills-claude/skills/dbos-typescript/CLAUDE.md | No YAML frontmatter — `name` and `description` both missing | Duplicate of Bug #3 in -claude collection; score 50/100 |
| 7 | plugins/antigravity-awesome-skills-claude/skills/loki-mode/CLAUDE.md | No YAML frontmatter — `name` and `description` both missing | Navigation guide for Loki Mode lacks required frontmatter; score 50/100 |
| 8 | skills/loki-mode/CLAUDE.md | No YAML frontmatter — `name` and `description` both missing | Root-level Loki Mode CLAUDE.md lacks required frontmatter; score 50/100 |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | plugins/antigravity-awesome-skills/skills/filesystem-context/SKILL.md | Vague quantifier "relevant" appears 3 times | -6 |
| 2 | plugins/antigravity-awesome-skills/skills/referral-program/SKILL.md | Vague: "appropriate" ×1, "relevant" ×1 | -4 |
| 3 | plugins/antigravity-awesome-skills/skills/remotion/SKILL.md | Vague: "appropriate" ×1, "relevant" ×1 | -4 |
| 4 | plugins/antigravity-awesome-skills/skills/observability-monitoring-monitor-setup/SKILL.md | Vague: "relevant" ×1 | -2 |
| 5 | plugins/antigravity-awesome-skills/skills/azure-ai-projects-dotnet/SKILL.md | Vague: "appropriate" ×1 | -2 |
| 6 | plugins/antigravity-awesome-skills/skills/prompt-engineer/SKILL.md | Vague: "Appropriate level" ×1 | -2 |
| 7 | plugins/antigravity-awesome-skills/skills/brainstorming/SKILL.md | Vague: "reasonable defaults" ×1 | -2 |
| 8 | plugins/antigravity-awesome-skills/skills/azure-ai-agents-persistent-java/SKILL.md | Vague: "appropriate delays" ×1 | -2 |
| 9 | plugins/antigravity-awesome-skills/skills/tailwind-design-system/SKILL.md | Vague: "relevant best practices" ×1 | -2 |
| 10 | plugins/antigravity-awesome-skills/skills/gdpr-data-handling/SKILL.md | Vague: "relevant best practices" ×1 | -2 |
| 11 | plugins/antigravity-awesome-skills/skills/hig-components-dialogs/SKILL.md | Vague: "Appropriately sized" ×1 | -2 |
| 12 | plugins/antigravity-awesome-skills/skills/python-testing-patterns/SKILL.md | Vague: "relevant best practices" ×1 | -2 |
| 13 | plugins/antigravity-awesome-skills/skills/senior-architect/SKILL.md | Vague: "appropriate caching" ×1 | -2 |
| 14 | plugins/antigravity-awesome-skills/skills/nx-workspace-patterns/SKILL.md | Vague: "relevant" ×1 | -2 |

## Cross-Component

**CLAUDE.md files missing frontmatter (systemic)**
All 8 CLAUDE.md files in this sample are navigation guides that lack YAML frontmatter entirely. The pattern is consistent: dbos-python, dbos-golang, dbos-typescript each have a `CLAUDE.md` that is either a symlink to or copy of `AGENTS.md`, serving as a human-readable index to the `references/` subfolder. The loki-mode CLAUDE.md similarly acts as a navigation guide. None carry `name:` or `description:` frontmatter. This is a structural gap across all three DBOS skill families (Python, Go, TypeScript) and the Loki Mode skill in both the `antigravity-awesome-skills` and `antigravity-awesome-skills-claude` collections. Fix: add YAML frontmatter block at the top of each CLAUDE.md with `name` and `description` matching the corresponding SKILL.md values.

**Vague quantifier pattern**
The most frequent quality issue across SKILL.md files is single-instance use of "relevant" or "appropriate" — typically in phrases like "relevant best practices", "appropriate caching", "appropriate delays". These each incur only a -2 penalty (well below the -20 cap), so no individual file scores below 94 for this reason. The pattern is mild and broadly consistent with the original audit's findings.

**Comparison with original audit (2026-04-17)**
The original audit sampled 65 files from 2,998 and estimated 82/100. This re-audit scores 100 curated files and finds 96/100 on that sample. The gap is explained by the curation strategy: the re-audit file list focuses on a set of representative, generally high-quality SKILL.md files and all plugin.json manifests. The original audit's 65-file sample included known-problematic stubs (gdpr-data-handling, tailwind-design-system, nextjs-app-router-patterns, tavily-web, git-pushing, seo-* skills) that score 60–78 and are not in this re-audit set. The plugin.json manifests (41 files, all 100/100) add substantial weight here. The CLAUDE.md frontmatter gap (8 files at 50/100 each) is the only structural failure in this sample.

**Verified original bug findings**
From the original findings.jsonl, the following bugs were flagged and their status at HEAD:
- `prompt-engineer/SKILL.md` step-ordering bug (1→3 skip): file is present and unchanged; finding persists.
- `youtube-summarizer/SKILL.md` malformed markdown: file is present; finding persists.
- `blog-writing-guide/SKILL.md` missing `date_added`: file does not have `date_added` in this version's frontmatter.

## Recommendation

Score 96/100 — the sampled artifacts are high quality, with all plugin.json manifests clean and SKILL.md files carrying proper frontmatter and concrete content. The single systemic issue is that all 8 CLAUDE.md navigation guide files lack YAML frontmatter; adding a 3-line `name`/`description` block to each brings every artifact in this set to 98+ and clears the only bug class found.
