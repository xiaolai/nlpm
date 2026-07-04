# NLPM Audit: lst97/claude-code-sub-agents
**Date**: 2026-04-06  |  **Artifacts**: 38  |  **Strategy**: batched
**NL Score**: 70/100
**Security**: CLEAR
**Bugs**: 4  |  **Quality Issues**: 38  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/development/ux-designer.md | agent | 47 | 12 unused declared tools, incl. playwright never mentioned in body |
| agents/development/backend-architect.md | agent | 59 | Zero examples + 8 unused declared tools |
| agents/development/ui-designer.md | agent | 59 | Zero examples + 8 unused declared tools |
| agents/infrastructure/incident-responder.md | agent | 61 | Missing output format section + zero examples |
| agents/data-ai/ai-engineer.md | agent | 64 | Missing output format section + unused MultiEdit |
| agents/development/python-pro.md | agent | 64 | Zero examples (3 vague quantifiers) |
| agents/infrastructure/devops-incident-responder.md | agent | 65 | Zero examples; duplicate `Bash` in tools list |
| agents/data-ai/prompt-engineer.md | agent | 66 | Missing output format section |
| agents/security/security-auditor.md | agent | 67 | Write/Edit declared on a functionally read-only auditor role |
| agents/quality-testing/debugger.md | agent | 68 | Zero examples + 5 unused declared tools |
| agents/specialization/documentation-expert.md | agent | 68 | Zero worked examples |
| agents/development/frontend-developer.md | agent | 68 | Zero examples + duplicate tool entry |
| agents/development/legacy-modernizer.md | agent | 68 | Zero invocation examples |
| agents/data-ai/data-scientist.md | agent | 69 | Missing output format section |
| agents/infrastructure/performance-engineer.md | agent | 69 | Zero examples; duplicate `Bash` in tools list |
| agents/quality-testing/qa-expert.md | agent | 69 | Zero examples |
| agents/quality-testing/test-automator.md | agent | 69 | Zero examples |
| CLAUDE.md | memory | 70 | No build/run or test commands; generic non-repo-specific content |
| agents/specialization/api-documenter.md | agent | 70 | Zero worked examples |
| agents/business/product-manager.md | agent | 70 | Zero worked examples |
| agents/development/typescript-pro.md | agent | 71 | Zero examples (cleanest tool list in the batch) |
| agents/infrastructure/deployment-engineer.md | agent | 71 | Zero examples |
| agents/data-ai/ml-engineer.md | agent | 73 | Missing output format section |
| agents/agent-organizer.md | agent | 73 | Write/Edit declared despite explicit read-only self-description |
| agents/development/nextjs-pro.md | agent | 74 | Zero example blocks (4 vague quantifiers) |
| agents/development/full-stack-developer.md | agent | 75 | Zero example blocks |
| agents/development/mobile-developer.md | agent | 75 | Zero example blocks |
| agents/data-ai/postgres-pro.md | agent | 75 | Vague quantifiers (5 occurrences, highest in corpus) |
| agents/infrastructure/cloud-architect.md | agent | 75 | Zero examples |
| agents/development/react-pro.md | agent | 76 | Zero example blocks |
| agents/quality-testing/architect-review.md | agent | 77 | 4 unused declared tools (LS, WebFetch, WebSearch, Task) |
| agents/quality-testing/code-reviewer.md | agent | 77 | 4 unused declared tools (Bash, WebFetch, WebSearch, Task) |
| agents/development/electorn-pro.md | agent | 78 | Zero example blocks |
| agents/data-ai/database-optimizer.md | agent | 78 | Zero worked examples |
| agents/data-ai/data-engineer.md | agent | 78 | Unused MultiEdit tool |
| agents/development/golang-pro.md | agent | 80 | Zero example blocks |
| agents/development/dx-optimizer.md | agent | 80 | Zero example blocks |
| agents/data-ai/graphql-architect.md | agent | 80 | Unused MultiEdit tool |

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
| Hooks | 0 — no `hooks/` directory present |
| Scripts | 0 — no `scripts/**/*.{sh,py,js}` files present |
| MCP configs | 0 — no `.mcp.json` present |
| Package manifests | 0 — no `package.json` or `requirements.txt` present |
| Commands | 0 — repo has no `commands/*.md` (agents-only collection) |

The entire tracked tree (`git ls-files`, 55 files) consists of markdown documentation/agent-definitions, images (`_images/*.png`, `*.gif`), `LICENSE`, and `.gitignore`. There is no executable surface of any kind in this repository — nothing to sandbox-escape, nothing that runs on checkout, nothing a hook or CI step would invoke.

### Security Findings
No security findings.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | agents/data-ai/postgres-pro.md | Frontmatter `name: postgresql-pglite-pro` (line 2) does not match the filename or the `postgres-pro` label used by README.md (line 75, 425) | Claude Code resolves sub-agents by the frontmatter `name` field, not the filename — a user following the README's "postgres-pro" reference cannot invoke this agent under that name; it is only reachable as `postgresql-pglite-pro`, an undocumented name |
| 2 | agents/infrastructure/devops-incident-responder.md | `Bash` is listed twice in the `tools:` frontmatter (line 4) | Cosmetic/manifest-hygiene defect from a copy-paste error; no functional breakage, but signals the tools list wasn't reviewed after editing |
| 3 | agents/infrastructure/performance-engineer.md | `Bash` is listed twice in the `tools:` frontmatter (line 4) | Same defect pattern as #2 |
| 4 | agents/development/frontend-developer.md | `mcp__magic__21st_magic_component_builder` is listed twice in the `tools:` frontmatter (line 4) | Same defect pattern as #2/#3 |

## Security Fixes (PR-worthy, Medium/Low only)
No security findings — nothing to fix.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/development/ux-designer.md | Zero examples (-15); vague quantifier "relevant" L67 (-2); 12 unused declared tools incl. Edit, MultiEdit, Grep, Glob, Bash, LS, WebSearch, WebFetch, TodoWrite, Task, and both `mcp__playwright__*` tools, which are never mentioned in the body at all (-36) | -53 |
| 2 | agents/development/backend-architect.md | Zero examples (-15); vague quantifier "relevant" L43 (-2); 8 unused declared tools: Write, Edit, MultiEdit, Bash, LS, WebSearch, WebFetch, TodoWrite — role is advisory/proposal-only, never touches files or shell (-24) | -41 |
| 3 | agents/development/ui-designer.md | Zero examples (-15); vague quantifier "sufficient" L54 (-2); 8 unused declared tools: Edit, MultiEdit, Bash, LS, WebSearch, WebFetch, TodoWrite, Task (-24) | -41 |
| 4 | agents/infrastructure/incident-responder.md | Zero examples (-15); missing output-format section — only a postmortem-content list, not a response template (-10); vague quantifier "as needed" L47 (-2); 4 unused declared tools: LS, WebSearch, WebFetch, Task (-12) | -39 |
| 5 | agents/data-ai/ai-engineer.md | Zero examples (-15); missing output-format section — only a "Deliverables" list (-10); 4 vague quantifiers incl. "various" in frontmatter description (-8); unused MultiEdit (-3) | -36 |
| 6 | agents/development/python-pro.md | Zero examples (-15); 3 vague quantifiers: "relevant" L43, "appropriate" L86, "relevant" L91 (-6); 5 unused declared tools: LS, WebSearch, WebFetch, TodoWrite, Task (-15) | -36 |
| 7 | agents/infrastructure/devops-incident-responder.md | Zero examples (-15); 4 vague quantifiers: "relevant" L43, "appropriate" L57, "various" L58, "relevant" L67 (-8); 4 unused declared tools: LS, WebSearch, WebFetch, Task (-12) | -35 |
| 8 | agents/data-ai/prompt-engineer.md | Zero examples (-15); missing output-format section — only a "Deliverables" list (-10); 3 vague quantifiers: "appropriate" L39, "various" L61, "appropriate" L66 (-6); unused Bash — no shell/CLI content anywhere in body (-3) | -34 |
| 9 | agents/security/security-auditor.md | Zero examples (-15); vague quantifier "relevant" L67 (-2); unused LS, Task (-6); Write/Edit/MultiEdit declared despite an audit-only role — corroborated by agent-organizer.md's own worked example, where security-auditor's findings are handed to backend-architect for remediation rather than fixed in place (-10) | -33 |
| 10 | agents/quality-testing/debugger.md | Zero examples (-15); vague quantifier "relevant" L43 (-2); 5 unused declared tools: LS, WebSearch, WebFetch, TodoWrite, Task (-15) | -32 |
| 11 | agents/specialization/documentation-expert.md | Zero examples (-15); 4 vague quantifiers: "various" L3, "relevant" L34, "various" L35, "appropriate" L69 (-8); 3 unused declared tools: Bash, LS, Task (-9) | -32 |
| 12 | agents/development/frontend-developer.md | Zero examples (-15); vague quantifier "relevant" L45 (-2); 5 unused declared tools: LS, WebSearch, WebFetch, TodoWrite, Task (-15) | -32 |
| 13 | agents/development/legacy-modernizer.md | Zero examples (-15); vague quantifier "relevant" L43 (-2); 5 unused declared tools: LS, WebSearch, WebFetch, TodoWrite, Task (-15) | -32 |
| 14 | agents/data-ai/data-scientist.md | Zero examples (-15); missing output-format section — presentation style described but no response template (-10); 3 vague quantifiers: "relevant" L43, "appropriate" L70, "appropriate" L90 (-6) | -31 |
| 15 | agents/infrastructure/performance-engineer.md | Zero examples (-15); 2 vague quantifiers: "relevant" L44, "various" L72 (-4); 4 unused declared tools: LS, WebSearch, WebFetch, Task (-12) | -31 |
| 16 | agents/quality-testing/qa-expert.md | Zero examples (-15); 2 vague quantifiers: "various" L17, "appropriate" L87 (-4); 4 unused declared tools: LS, WebSearch, WebFetch, Task (-12) | -31 |
| 17 | agents/quality-testing/test-automator.md | Zero examples (-15); 2 vague quantifiers: "appropriate" L17, "appropriate" L55 (-4); 4 unused declared tools: LS, WebSearch, WebFetch, Task (-12) | -31 |
| 18 | CLAUDE.md | No build/run command documented anywhere (-10); no test command documented — only aspirational "pass all tests" language (-10); "Architecture" section is generic full-stack boilerplate, not a description of this repo's actual structure (a curated agent-definition library under `agents/<category>/`) (-10) | -30 |
| 19 | agents/specialization/api-documenter.md | Zero examples (-15); 5 unused declared tools: Bash, LS, WebSearch, WebFetch, Task (-15) | -30 |
| 20 | agents/business/product-manager.md | Zero examples (-15); 5 unused declared tools: Bash, LS, mcp__context7__resolve-library-id, mcp__context7__get-library-docs, mcp__sequential-thinking__sequentialthinking — file lacks the "MCP Integration" section sibling agents use to justify these (-15) | -30 |
| 21 | agents/development/typescript-pro.md | Zero examples (-15); vague quantifier "relevant" L43 (-2); 4 unused declared tools: LS, WebFetch, WebSearch, Task (-12) | -29 |
| 22 | agents/infrastructure/deployment-engineer.md | Zero examples (-15); vague quantifier "relevant" L43 (-2); 4 unused declared tools: LS, WebSearch, WebFetch, Task (-12) | -29 |
| 23 | agents/data-ai/ml-engineer.md | Zero examples (-15); missing output-format section — only an "Expected Deliverables" list (-10); vague quantifier "relevant" L43 (-2) | -27 |
| 24 | agents/agent-organizer.md | One example present, partial credit (-5); 3 vague quantifiers: "appropriate" L146, "various" L214, "appropriate" L250 (-6); unused Bash, TodoWrite (-6); Write/Edit declared despite the body explicitly stating "You DO NOT directly implement solutions or modify code" (lines 10, 246-248) (-10) | -27 |
| 25 | agents/development/nextjs-pro.md | Zero examples (-15); 4 vague quantifiers: "relevant" L43, "various" L60, "various" L73, "relevant" L109 (-8); unused Task (-3) | -26 |
| 26 | agents/development/full-stack-developer.md | Zero examples (-15); 2 vague quantifiers: "relevant" L44, "various" L87 (-4); unused Task, TodoWrite (-6) | -25 |
| 27 | agents/development/mobile-developer.md | Zero examples (-15); 2 vague quantifiers: "relevant" L43, "various" L61 (-4); unused Task, TodoWrite (-6) | -25 |
| 28 | agents/data-ai/postgres-pro.md | Zero examples (-15); 5 vague quantifiers — the most of any file: "relevant" L43, "various" L69, "appropriate" L75, "appropriate" L78, "various" L94 (-10) | -25 |
| 29 | agents/infrastructure/cloud-architect.md | Zero examples (-15); 2 vague quantifiers: "relevant" L43, "appropriate" L96 (-4); unused LS, Task (-6) | -25 |
| 30 | agents/development/react-pro.md | Zero examples (-15); 3 vague quantifiers: "relevant" L43, "appropriate" L94, "appropriate" L97 (-6); unused Task (-3) | -24 |
| 31 | agents/quality-testing/architect-review.md | One example present, partial credit (-5); 3 vague quantifiers: "appropriate" L64, "correctly" L90, "appropriate" L102 (-6); 4 unused declared tools: LS, WebFetch, WebSearch, Task (-12) | -23 |
| 32 | agents/quality-testing/code-reviewer.md | One example present, partial credit (-5); 3 vague quantifiers: "sufficient" L90, "reasonably" L97, "properly" L216 (-6); 4 unused declared tools: Bash, WebFetch, WebSearch, Task (-12) | -22 |
| 33 | agents/development/electorn-pro.md | Zero examples (-15); 2 vague quantifiers: "relevant" L43, "appropriate" L97 (-4); unused Task (-3) | -22 |
| 34 | agents/data-ai/database-optimizer.md | Zero examples (-15); 2 vague quantifiers: "relevant" L43, "relevant" L75 (-4); unused Bash — body states the agent "must not execute any queries" (-3) | -22 |
| 35 | agents/data-ai/data-engineer.md | Zero examples (-15); 2 vague quantifiers: "relevant" L43, "appropriate" L92 (-4); unused MultiEdit (-3) | -22 |
| 36 | agents/development/golang-pro.md | Zero examples (-15); vague quantifier "relevant" L43 (-2); unused Task (-3) | -20 |
| 37 | agents/development/dx-optimizer.md | Zero examples (-15); vague quantifier "relevant" L43 (-2); unused Task (-3) | -20 |
| 38 | agents/data-ai/graphql-architect.md | Zero examples (-15); vague quantifier "relevant" L43 (-2); unused MultiEdit (-3) | -20 |

## Cross-Component
- **Stale agent count in README.md.** README.md line 3 states "A comprehensive collection of **33** specialized AI subagents," but the repo actually contains **37** agent definition files under `agents/` (`git ls-files 'agents/**/*.md' agents/*.md` → 37; verified 2026-04-06). All 37 are otherwise correctly referenced somewhere in README.md's agent tables — no orphaned agents, and every README agent link resolves to an existing file — so this is purely a stale summary number, not a structural break.
- **Filename vs. registered-name drift (cosmetic).** Two files carry a filename that diverges from their own frontmatter `name:` field even though the divergence causes no functional break (Claude Code resolves by `name:`, not filename): `agents/development/electorn-pro.md` registers as `name: electron-pro` (correct spelling), and `agents/quality-testing/architect-review.md` registers as `name: architect-reviewer`. README.md correctly uses the registered names in both cases, so nothing is actually broken — but the filenames are a latent trap for anyone editing by hand.
- No broken relative links, `@import` references, or dead cross-references were found anywhere in the 38 scored artifacts or in README.md's ~60 agent links.
- `agents/data-ai/postgres-pro.md`'s name/filename mismatch (see Bugs #1) is the one cross-component drift with a real functional consequence, since it affects discoverability under the name README documents.

## Recommendation
**CLEAR — submit PRs for all bugs and medium/low security fixes.**

Security is fully clean: this repository has no hooks, scripts, MCP configs, or package manifests of any kind — there is no executable surface to scan for medium/low security issues, so there are no security fixes to bundle. The 4 identified bugs are all safe, mechanical, low-risk fixes (three one-token frontmatter deduplications and one frontmatter `name` correction) suitable for a single PR. The 38 quality findings are dominated by one systemic, repo-wide pattern — zero genuine `<example>` (Context → user message → assistant response) blocks across all 37 agent files — which is informational per NLPM policy and not a PR-blocking issue, though it would be the highest-leverage single improvement available to this repo's maintainers.
