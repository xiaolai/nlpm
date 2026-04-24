# Re-Audit: sickn33/antigravity-awesome-skills

**Date**: 2026-04-24  |  **Before**: `unknown` (82/100)  |  **After**: `3ade322` (96/100)

## Summary

| Outcome | Count |
|---------|------:|
| fixed — our PR merged | 6 |
| fixed — upstream, not via our PR | 31 |
| newly introduced (regressions) | 24 |

## Original findings — verification

| # | File | Line | Rule | Pattern | Outcome | PR |
|---|------|------|------|---------|---------|----|
| 1 | `antigravity-awesome-skills/skills/prompt-engineer/SKILL.md` | — | BUG-missing-steps | `missing-step-ordering` | fixed — our PR merged | #534 |
| 2 | `antigravity-awesome-skills/skills/youtube-summarizer/SKILL.md` | — | BUG-malformed-markdown | `malformed-markdown` | fixed — our PR merged | #535 |
| 3 | `antigravity-bundle-seo-specialist/skills/schema-markup/SKILL.md` | 9 | BUG-invalid-frontmatter | `malformed-frontmatter` | fixed — our PR merged | #536 |
| 4 | `antigravity-bundle-seo-specialist/skills/seo-fundamentals/SKILL.md` | 9 | BUG-invalid-frontmatter | `malformed-frontmatter` | fixed — our PR merged | #536 |
| 5 | `antigravity-awesome-skills/skills/blog-writing-guide/SKILL.md` | — | BUG-missing-frontmatter | `missing-date-added` | fixed — our PR merged | #537 |
| 6 | `antigravity-awesome-skills/skills/docx-official/SKILL.md` | — | BUG-unclassified | `references-docx-js-md-and-ooxml-md-that` | fixed — upstream, not via our PR |  |
| 7 | `antigravity-awesome-skills-claude/skills/active-directory-attacks/SKILL.md` | — | SEC-credential-exfil | `credential-exfil` | fixed — upstream, not via our PR |  |
| 8 | `antigravity-awesome-skills/skills/active-directory-attacks/SKILL.md` | — | CC-duplication | `duplicate-file` | fixed — upstream, not via our PR |  |
| 9 | `active-directory-attacks/SKILL.md` | — | SEC-unknown | `no-security-allowlist-annotation-for-dcs` | fixed — upstream, not via our PR |  |
| 10 | `ethical-hacking-methodology/SKILL.md` | — | SEC-unknown | `risk-unknown-despite-containing-backdoor` | fixed — our PR merged | #538 |
| 11 | `environment-setup-guide/SKILL.md` | — | SEC-unknown | `nodesource-curl-pipe-bash-without-annota` | fixed — upstream, not via our PR |  |
| 12 | `gitops-workflow/SKILL.md` | — | SEC-unknown | `flux-cd-curl-pipe-bash-without-annotatio` | fixed — upstream, not via our PR |  |
| 13 | `gdpr-data-handling/SKILL.md` | — | UNCLASSIFIED | `body-is-only-open-implementation-playboo` | fixed — upstream, not via our PR |  |
| 14 | `tavily-web/SKILL.md` | — | R09 | `no-examples` | fixed — upstream, not via our PR |  |
| 15 | `tailwind-design-system/SKILL.md` | — | UNCLASSIFIED | `delegates-entirely-to-implementation-pla` | fixed — upstream, not via our PR |  |
| 16 | `nextjs-app-router-patterns/SKILL.md` | — | UNCLASSIFIED | `delegates-entirely-to-implementation-pla` | fixed — upstream, not via our PR |  |
| 17 | `git-pushing/SKILL.md` | — | R09 | `no-examples` | fixed — upstream, not via our PR |  |
| 18 | `cloud-penetration-testing/SKILL.md` | — | UNCLASSIFIED | `no-output-format-section` | fixed — upstream, not via our PR |  |
| 19 | `linux-privilege-escalation/SKILL.md` | — | UNCLASSIFIED | `no-output-format-section` | fixed — upstream, not via our PR |  |
| 20 | `observability-monitoring-monitor-setup/SKILL.md` | — | UNCLASSIFIED | `vague-relevant-best-practices-appropriat` | fixed — upstream, not via our PR |  |
| 21 | `dropbox-automation/SKILL.md` | — | R09 | `no-examples` | fixed — upstream, not via our PR |  |
| 22 | `one-drive-automation/SKILL.md` | — | R09 | `no-examples` | fixed — upstream, not via our PR |  |
| 23 | `azure-ai-projects-dotnet/SKILL.md` | — | UNCLASSIFIED | `no-output-format-section` | fixed — upstream, not via our PR |  |
| 24 | `skill-router/SKILL.md` | — | UNCLASSIFIED | `only-1-example-partial-credit` | fixed — upstream, not via our PR |  |
| 25 | `seo-content-writer through seo-content-auditor (5 files)` | — | UNCLASSIFIED | `no-output-format-in-any-of-the-5-seo-ski` | fixed — upstream, not via our PR |  |
| 26 | `bash-linux/SKILL.md` | — | R09 | `no-examples` | fixed — upstream, not via our PR |  |
| 27 | `lint-and-validate/SKILL.md` | — | R09 | `no-examples` | fixed — upstream, not via our PR |  |
| 28 | `agent-orchestrator/SKILL.md` | — | UNCLASSIFIED | `workflow-requires-3-external-python-scri` | fixed — upstream, not via our PR |  |
| 29 | `top-web-vulnerabilities/SKILL.md` | — | UNCLASSIFIED | `risk-unknown-should-be-risk-offensive-or` | fixed — upstream, not via our PR |  |
| 30 | `security-auditor/SKILL.md` | — | UNCLASSIFIED | `risk-unknown-inconsistent-with-rest-of-s` | fixed — upstream, not via our PR |  |
| 31 | `typescript-expert/SKILL.md` | — | UNCLASSIFIED | `no-output-format-section-despite-compreh` | fixed — upstream, not via our PR |  |
| 32 | `docker-expert/SKILL.md` | — | UNCLASSIFIED | `no-output-format-section` | fixed — upstream, not via our PR |  |
| 33 | `kubernetes-architect/SKILL.md` | — | UNCLASSIFIED | `no-output-format-section` | fixed — upstream, not via our PR |  |
| 34 | `terraform-specialist/SKILL.md` | — | UNCLASSIFIED | `no-output-format-section` | fixed — upstream, not via our PR |  |
| 35 | `react-best-practices/SKILL.md` | — | UNCLASSIFIED | `all-detail-deferred-to-external-rules-md` | fixed — upstream, not via our PR |  |
| 36 | `nodejs-best-practices/SKILL.md` | — | UNCLASSIFIED | `learn-to-think-meta-instruction-in-body` | fixed — upstream, not via our PR |  |
| 37 | `Multiple skills across all bundles` | — | UNCLASSIFIED | `vague-terms-relevant-appropriate-best-pr` | fixed — upstream, not via our PR |  |

## Findings introduced since audit

These findings appear in the re-audit but were not in the original audit. They may be true regressions (new commits introduced them) or artifacts of scoring drift.

| # | File | Line | Rule | Pattern | Description |
|---|------|------|------|---------|-------------|
| 1 | `plugins/antigravity-awesome-skills/skills/dbos-python/CLAUDE.md` | — | BUG-missing-frontmatter | `missing-frontmatter-name-description` | CLAUDE.md has no YAML frontmatter block — missing required `name` (-25) and `description` (-25) fields |
| 2 | `plugins/antigravity-awesome-skills/skills/dbos-golang/CLAUDE.md` | — | BUG-missing-frontmatter | `missing-frontmatter-name-description` | CLAUDE.md has no YAML frontmatter block — missing required `name` (-25) and `description` (-25) fields |
| 3 | `plugins/antigravity-awesome-skills/skills/dbos-typescript/CLAUDE.md` | — | BUG-missing-frontmatter | `missing-frontmatter-name-description` | CLAUDE.md has no YAML frontmatter block — missing required `name` (-25) and `description` (-25) fields |
| 4 | `plugins/antigravity-awesome-skills-claude/skills/dbos-python/CLAUDE.md` | — | BUG-missing-frontmatter | `missing-frontmatter-name-description` | CLAUDE.md has no YAML frontmatter block — duplicate of antigravity-awesome-skills version; missing `name` and `description` |
| 5 | `plugins/antigravity-awesome-skills-claude/skills/dbos-golang/CLAUDE.md` | — | BUG-missing-frontmatter | `missing-frontmatter-name-description` | CLAUDE.md has no YAML frontmatter block — duplicate of antigravity-awesome-skills version; missing `name` and `description` |
| 6 | `plugins/antigravity-awesome-skills-claude/skills/dbos-typescript/CLAUDE.md` | — | BUG-missing-frontmatter | `missing-frontmatter-name-description` | CLAUDE.md has no YAML frontmatter block — duplicate of antigravity-awesome-skills version; missing `name` and `description` |
| 7 | `plugins/antigravity-awesome-skills-claude/skills/loki-mode/CLAUDE.md` | — | BUG-missing-frontmatter | `missing-frontmatter-name-description` | CLAUDE.md navigation guide for Loki Mode has no YAML frontmatter — missing `name` and `description` |
| 8 | `skills/loki-mode/CLAUDE.md` | — | BUG-missing-frontmatter | `missing-frontmatter-name-description` | Root-level CLAUDE.md navigation guide for Loki Mode has no YAML frontmatter — missing `name` and `description` |
| 9 | `plugins/antigravity-awesome-skills/skills/filesystem-context/SKILL.md` | — | R02 | `vague-quantifier-relevant` | Vague quantifier "relevant" appears 3 times in skill body |
| 10 | `plugins/antigravity-awesome-skills/skills/referral-program/SKILL.md` | — | R02 | `vague-quantifier-appropriate-relevant` | Vague quantifiers "appropriate" (×1) and "relevant" (×1) in skill body |
| 11 | `plugins/antigravity-awesome-skills/skills/remotion/SKILL.md` | — | R02 | `vague-quantifier-appropriate-relevant` | Vague quantifiers "appropriate" (×1) and "relevant" (×1) in skill body |
| 12 | `plugins/antigravity-awesome-skills/skills/observability-monitoring-monitor-setup/SKILL.md` | — | R02 | `vague-quantifier-relevant` | Vague quantifier "relevant" (×1) in skill body |
| 13 | `plugins/antigravity-awesome-skills/skills/azure-ai-projects-dotnet/SKILL.md` | — | R02 | `vague-quantifier-appropriate` | Vague quantifier "appropriate" (×1) in skill body |
| 14 | `plugins/antigravity-awesome-skills/skills/prompt-engineer/SKILL.md` | — | R02 | `vague-quantifier-appropriate` | Vague quantifier "Appropriate level" (×1) in skill body |
| 15 | `plugins/antigravity-awesome-skills/skills/brainstorming/SKILL.md` | — | R02 | `vague-quantifier-reasonable` | Vague quantifier "reasonable defaults" (×1) in skill body |
| 16 | `plugins/antigravity-awesome-skills/skills/azure-ai-agents-persistent-java/SKILL.md` | — | R02 | `vague-quantifier-appropriate` | Vague quantifier "appropriate delays" (×1) in skill body |
| 17 | `plugins/antigravity-awesome-skills/skills/tailwind-design-system/SKILL.md` | — | R02 | `vague-quantifier-relevant` | Vague quantifier "relevant best practices" (×1) in skill body |
| 18 | `plugins/antigravity-awesome-skills/skills/gdpr-data-handling/SKILL.md` | — | R02 | `vague-quantifier-relevant` | Vague quantifier "relevant best practices" (×1) in skill body |
| 19 | `plugins/antigravity-awesome-skills/skills/hig-components-dialogs/SKILL.md` | — | R02 | `vague-quantifier-appropriate` | Vague quantifier "Appropriately sized" (×1) in skill body |
| 20 | `plugins/antigravity-awesome-skills/skills/python-testing-patterns/SKILL.md` | — | R02 | `vague-quantifier-relevant` | Vague quantifier "relevant best practices" (×1) in skill body |
| 21 | `plugins/antigravity-awesome-skills/skills/senior-architect/SKILL.md` | — | R02 | `vague-quantifier-appropriate` | Vague quantifier "appropriate caching" (×1) in skill body |
| 22 | `plugins/antigravity-awesome-skills/skills/nx-workspace-patterns/SKILL.md` | — | R02 | `vague-quantifier-relevant` | Vague quantifier "relevant" (×1) in skill body |
| 23 | `plugins/antigravity-awesome-skills-claude/skills/dbos-python/CLAUDE.md` | — | CC-duplication | `duplicate-claude-md-missing-frontmatter` | All 6 DBOS CLAUDE.md files (dbos-python, dbos-golang, dbos-typescript in both collections) share the same frontmatter gap; fix should be applied to all 6 files simultaneously |
| 24 | `plugins/antigravity-awesome-skills-claude/skills/loki-mode/CLAUDE.md` | — | CC-duplication | `duplicate-loki-mode-claude-md` | Loki Mode CLAUDE.md appears in two locations: plugins/antigravity-awesome-skills-claude/skills/loki-mode/ and skills/loki-mode/; both lack frontmatter and should be fixed together |

