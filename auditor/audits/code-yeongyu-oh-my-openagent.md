# NLPM Audit: code-yeongyu/oh-my-openagent
**Date**: 2026-04-06  |  **Artifacts**: 12  |  **Strategy**: single
**NL Score**: 74/100
**Security**: REVIEW
**Bugs**: 6  |  **Quality Issues**: 7  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| src/agents/AGENTS.md | DOC | 50 | Missing frontmatter: no name or description |
| src/agents/hephaestus/AGENTS.md | DOC | 50 | Missing frontmatter: no name or description |
| src/agents/prometheus/AGENTS.md | DOC | 50 | Missing frontmatter: no name or description |
| src/agents/sisyphus/AGENTS.md | DOC | 50 | Missing frontmatter: no name or description |
| src/hooks/atlas/tsconfig.json | CONFIG | 50 | Not an NL artifact; no frontmatter possible |
| src/features/builtin-skills/dev-browser/SKILL.md | SKILL | 80 | Missing output format; 2 broken cross-references |
| .opencode/skills/github-triage/SKILL.md | SKILL | 90 | Minor: duplicate `---` separator at line 80–83 |
| .opencode/skills/work-with-pr/SKILL.md | SKILL | 90 | No penalizable issues found |
| src/features/builtin-skills/agent-browser/SKILL.md | SKILL | 90 | Missing output format declaration |
| src/features/builtin-skills/frontend-ui-ux/SKILL.md | SKILL | 90 | Missing output format declaration |
| .opencode/skills/pre-publish-review/SKILL.md | SKILL | 94 | Vague quantifiers: "significant" ×2, "minor" ×1 |
| src/features/builtin-skills/git-master/SKILL.md | SKILL | 98 | Vague quantifier: "suitable" ×1 |

**Weighted average**: (50×5 + 80 + 90×5 + 94 + 98) / 12 = **74/100**

---

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
| Hooks (shell) | 0 |
| Scripts (JS/TS, in `script/`) | 7 (TypeScript, developer tooling only) |
| Postinstall script | `postinstall.mjs` (shipped in npm package, runs on `npm install`) |
| MCP configs | 0 |
| Package manifest | `package.json` |

Note: `src/hooks/` contains TypeScript source files (compiled at build time), not shell hook scripts. They are not execution surfaces at the npm install level.

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH | postinstall.mjs | 52 | Subprocess in postinstall | `execSync("opencode --version", {...})` runs a child process inside a postinstall script that executes automatically on `npm install`. Command is hardcoded and benign, but the structural pattern (arbitrary code execution on install) is a supply-chain risk. |
| 2 | MEDIUM | package.json | 96–100 | trustedDependencies with author-owned package | `@code-yeongyu/comment-checker` is the repository author's own package listed in `trustedDependencies`, which bypasses npm/bun install-script prompts. Any compromise of that package propagates to all consumers silently. |
| 3 | MEDIUM | package.json | 72 | Telemetry dependency | `posthog-node ^5.29.2` is a telemetry/analytics library. Its presence means analytics calls may originate from installed environments without explicit user opt-in documentation. |
| 4 | LOW | package.json | 57–80 | Unpinned dependency versions | All production dependencies use semver caret ranges (`^`). Minor/patch updates (including transitive) are applied silently on reinstall, expanding the supply-chain attack surface over time. |

---

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | src/agents/AGENTS.md | Missing YAML frontmatter (`name`, `description`) | File cannot be registered or discovered by NL tooling; breaks skill/agent indexing |
| 2 | src/agents/hephaestus/AGENTS.md | Missing YAML frontmatter (`name`, `description`) | Same as above |
| 3 | src/agents/prometheus/AGENTS.md | Missing YAML frontmatter (`name`, `description`) | Same as above |
| 4 | src/agents/sisyphus/AGENTS.md | Missing YAML frontmatter (`name`, `description`) | Same as above |
| 5 | src/features/builtin-skills/dev-browser/SKILL.md | Broken reference: `references/installation.md` does not exist in the skill directory | Users directed to non-existent setup docs; Windows support instructions unavailable |
| 6 | src/features/builtin-skills/dev-browser/SKILL.md | Broken reference: `references/scraping.md` does not exist in the skill directory | Users directed to non-existent scraping guide; advanced workflow docs unavailable |

---

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | package.json | `posthog-node` telemetry dependency lacks opt-in documentation | Add a `README` section documenting what telemetry is collected and how to disable it; consider making it opt-in via config |
| 2 | package.json | Unpinned dependency versions | Pin exact versions for production dependencies (or use a lock file with `--frozen-lockfile` in CI) to prevent silent supply-chain drift |

---

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | src/features/builtin-skills/agent-browser/SKILL.md | No declared output format — skill describes CLI commands but does not specify the format an agent should produce after using them | -10 |
| 2 | src/features/builtin-skills/dev-browser/SKILL.md | No declared output format | -10 |
| 3 | src/features/builtin-skills/frontend-ui-ux/SKILL.md | No declared output format — skill describes design principles but not the expected output structure (file list? summary? live preview?) | -10 |
| 4 | .opencode/skills/pre-publish-review/SKILL.md | Vague quantifiers: "significant findings" (×2) and "minor issues" (×1) — these thresholds are undefined and agent-dependent | -6 |
| 5 | src/features/builtin-skills/git-master/SKILL.md | Vague quantifier: "No suitable target commit exists" (Phase 4.1) — "suitable" is undefined | -2 |
| 6 | .opencode/skills/github-triage/SKILL.md | Duplicate `---` separator between Phase 1 heading and preamble (lines 80–83) — cosmetic but may confuse parsers | 0 (style) |
| 7 | src/hooks/atlas/tsconfig.json | Incorrectly included in NL artifact list — this is a TypeScript compiler config file with no NL content; cannot be scored as an NL artifact | N/A |

---

## Cross-Component

**Generated documentation files without frontmatter**: The four `AGENTS.md` files in `src/agents/`, `src/agents/hephaestus/`, `src/agents/prometheus/`, and `src/agents/sisyphus/` are auto-generated summaries (all carry `**Generated:** 2026-04-xx` headers). They serve as developer-facing documentation, not as loadable NL agent definitions. Adding YAML frontmatter with `name` and `description` would allow them to be discovered and indexed by NL tooling without changing their documentation purpose.

**Non-NL artifact in scan list**: `src/hooks/atlas/tsconfig.json` is a TypeScript compiler configuration file. It was included in the scan list but has no NL content and cannot be meaningfully scored. It should be excluded from future NL artifact scans.

**Broken cross-references in dev-browser**: `dev-browser/SKILL.md` references two relative markdown files (`references/installation.md`, `references/scraping.md`) that do not exist anywhere in the repository. These were likely planned but never written, or deleted after being referenced.

**Skill coherence (opencode vs builtin-skills)**: The `.opencode/skills/` directory contains orchestration-heavy skills (`github-triage`, `pre-publish-review`, `work-with-pr`) while `src/features/builtin-skills/` contains tool-reference skills (`agent-browser`, `dev-browser`, `git-master`, `frontend-ui-ux`). These serve different audiences and are structurally consistent within each group. No contradictions found.

**posthog-node in trustedDependencies**: `posthog-node` is NOT listed in `trustedDependencies`, so its install scripts are not automatically trusted. Only `@ast-grep/cli`, `@ast-grep/napi`, and `@code-yeongyu/comment-checker` are trusted.

---

## Recommendation

**REVIEW — submit NL fix PRs, flag security findings in issue.**

The single HIGH security finding is `postinstall.mjs` running a subprocess (`execSync("opencode --version")`) on `npm install`. The command is fully hardcoded and benign — this is standard practice for binary npm packages (esbuild, Prisma, etc.) and does not warrant private disclosure. However, it should be documented in the README and the structural risk acknowledged publicly (e.g., a `SECURITY.md` noting that postinstall runs and what it does).

**Recommended actions:**

1. **NL bugs (PR-worthy):** Add YAML frontmatter to the four `AGENTS.md` documentation files. Create the two missing reference files in `dev-browser/`. These are low-risk, high-value fixes.

2. **Security (public issue):** Open a GitHub issue documenting: (a) what `postinstall.mjs` does and why, (b) the `@code-yeongyu/comment-checker` trustedDependency risk, (c) the telemetry (`posthog-node`) usage and opt-out path. No private disclosure needed — no exploitable vulnerability was found.

3. **Medium/Low security fixes (PR-worthy):** Add telemetry documentation to README; consider pinning production dependency versions.

4. **Quality improvements (future):** Add `output:` format declarations to `agent-browser`, `dev-browser`, and `frontend-ui-ux` skills. Resolve vague quantifiers in `pre-publish-review` and `git-master`.
