# NLPM Audit: antfu/skills
**Date**: 2026-04-06  |  **Artifacts**: 17  |  **Strategy**: single
**NL Score**: 93/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 30  |  **Security Findings**: 5

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/vueuse-functions/SKILL.md | skill | 77 | -10 no inline examples (R06), -8 vague quantifiers (R01), -5 body 400–500 lines (R05) |
| skills/vue-best-practices/SKILL.md | skill | 85 | -10 vague quantifiers across 5 instances (R01), -5 no inline examples (R06) |
| skills/turborepo/SKILL.md | skill | 86 | -10 body >500 lines (R05), -4 vague quantifiers (R01) |
| skills/web-design-guidelines/SKILL.md | skill | 92 | -5 no inline code examples (R06), -3 no scope note for related skills (R07) |
| skills/pinia/SKILL.md | skill | 93 | -5 no inline examples (R06), -2 vague quantifier (R01) |
| skills/unocss/SKILL.md | skill | 93 | -5 no inline examples (R06), -2 vague quantifier (R01) |
| skills/nuxt/SKILL.md | skill | 95 | -5 no inline examples (R06) |
| skills/pnpm/SKILL.md | skill | 95 | -5 no inline examples (R06) |
| skills/tsdown/SKILL.md | skill | 95 | -5 body 400–500 lines (R05) |
| skills/vitepress/SKILL.md | skill | 95 | -5 no inline examples (R06) |
| skills/vitest/SKILL.md | skill | 95 | -5 no inline examples (R06) |
| skills/vue-router-best-practices/SKILL.md | skill | 95 | -5 no inline examples (R06) |
| skills/vue-testing-best-practices/SKILL.md | skill | 95 | -5 no inline examples (R06) |
| skills/antfu/SKILL.md | skill | 96 | -4 vague quantifiers (R01) |
| skills/slidev/SKILL.md | skill | 100 | — |
| skills/vite/SKILL.md | skill | 100 | — |
| skills/vue/SKILL.md | skill | 100 | — |

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 2 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Scripts | `scripts/cli.ts` |
| Package manifest | `package.json` |
| Hooks | none |
| MCP configs | none |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | scripts/cli.ts | 13 | shell-exec | `execSync` wrapper runs git submodule commands; inputs come from `meta.ts` config and `.gitmodules` parsing, not direct user input, but shell execution surface exists |
| 2 | Medium | scripts/cli.ts | 52 | recursive-delete | `rmSync({ recursive: true })` removes submodule directories derived from `.gitmodules` parsing; a crafted `.gitmodules` entry could influence deletion targets |
| 3 | Medium | skills/web-design-guidelines/SKILL.md | 28 | external-url-fetch | Skill instructs agents to `WebFetch` guideline rules from `raw.githubusercontent.com` at runtime; upstream repo compromise could inject instructions into agent behavior |
| 4 | Low | package.json | 8 | postinstall-script | `prepare` lifecycle script runs `simple-git-hooks` and `git submodule update` on `pnpm install`; standard dev practice for a `private: true` repo but executes code on install |
| 5 | Low | package.json | 10–18 | unpinned-semver | All seven `devDependencies` use `^` semver ranges; minor-version supply-chain drift possible |

## Bugs (PR-worthy)

No bugs found. All 17 artifacts have valid `name` and `description` frontmatter. No broken tool declarations or unresolvable internal references detected.

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/cli.ts | `rmSync` takes path derived from `.gitmodules` without path validation | Add `path.resolve` + assert path is under `root` before deletion |
| 2 | skills/web-design-guidelines/SKILL.md | External runtime fetch for instructions; no fallback if URL unreachable | Add inline fallback summary of key rules so skill functions offline |
| 3 | package.json | Seven deps with `^` ranges | Pin exact versions in a private dev tool where reproducibility matters |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/antfu/SKILL.md | "whenever possible" — vague quantifier (R01) | -2 |
| 2 | skills/antfu/SKILL.md | "complex inline types" — "complex" is unmeasured (R01) | -2 |
| 3 | skills/nuxt/SKILL.md | No inline code examples for a complex framework skill (R06) | -5 |
| 4 | skills/pinia/SKILL.md | No inline code examples (R06) | -5 |
| 5 | skills/pinia/SKILL.md | "complex logic, composables, and watchers" — "complex" vague (R01) | -2 |
| 6 | skills/pnpm/SKILL.md | No inline code examples (R06) | -5 |
| 7 | skills/tsdown/SKILL.md | Body is 405 lines (400–500 range) (R05) | -5 |
| 8 | skills/turborepo/SKILL.md | Body is 912 lines (>500 range) (R05) | -10 |
| 9 | skills/turborepo/SKILL.md | "truly cannot exist in packages" — "truly" vague (R01) | -2 |
| 10 | skills/turborepo/SKILL.md | "Overly Broad globalDependencies" — "overly" unmeasured (R01) | -2 |
| 11 | skills/unocss/SKILL.md | No inline code examples (R06) | -5 |
| 12 | skills/unocss/SKILL.md | "If the project setup is unclear" — "unclear" vague (R01) | -2 |
| 13 | skills/vitepress/SKILL.md | No inline code examples (R06) | -5 |
| 14 | skills/vitest/SKILL.md | No inline code examples (R06) | -5 |
| 15 | skills/vue-best-practices/SKILL.md | No inline code examples for a code-heavy Vue workflow skill (R06) | -5 |
| 16 | skills/vue-best-practices/SKILL.md | "for any non-trivial feature" — "non-trivial" vague (R01) | -2 |
| 17 | skills/vue-best-practices/SKILL.md | "brief component map" — "brief" unmeasured (R01) | -2 |
| 18 | skills/vue-best-practices/SKILL.md | "substantial presentational markup" — "substantial" vague (R01) | -2 |
| 19 | skills/vue-best-practices/SKILL.md | "keep entry/root and route view components thin" — "thin" unmeasured (R01) | -2 |
| 20 | skills/vue-best-practices/SKILL.md | "very small throwaway demos" — "very small" vague (R01) | -2 |
| 21 | skills/vue-router-best-practices/SKILL.md | No inline code examples (R06) | -5 |
| 22 | skills/vue-testing-best-practices/SKILL.md | No inline code examples (R06) | -5 |
| 23 | skills/vueuse-functions/SKILL.md | Body is 420 lines (400–500 range) (R05) | -5 |
| 24 | skills/vueuse-functions/SKILL.md | No code examples at all across 420 lines of function catalog (R06) | -10 |
| 25 | skills/vueuse-functions/SKILL.md | Description: "where appropriate" — "appropriate" vague (R01) | -2 |
| 26 | skills/vueuse-functions/SKILL.md | "Map requirements to the most suitable VueUse function" — "suitable" vague (R01) | -2 |
| 27 | skills/vueuse-functions/SKILL.md | "Map requirements to the most appropriate VueUse function" — "appropriate" vague (R01) | -2 |
| 28 | skills/vueuse-functions/SKILL.md | "ask to install only if truly needed" — "truly" vague (R01) | -2 |
| 29 | skills/web-design-guidelines/SKILL.md | No inline code examples (R06) | -5 |
| 30 | skills/web-design-guidelines/SKILL.md | No scope note referencing related skills (R07) | -3 |

## Cross-Component

**Reference directory naming convention divergence**: `vue-router-best-practices` and `vue-testing-best-practices` (sourced from `vuejs-ai` upstream) use `reference/` (singular) as their sub-reference directory, while all antfu-generated skills use `references/` (plural). Both conventions are internally self-consistent and references resolve correctly, but the inconsistency is visible to any contributor adding cross-skill links. No broken references detected.

**Body-length drift in turborepo**: At 912 lines, `turborepo/SKILL.md` is the only skill that substantially exceeds the R05 500-line budget. The content is high-quality (decision trees, anti-patterns, worked examples), but R05 suggests splitting into scoped sub-skills with cross-references to keep context overhead manageable.

**Metadata field presence inconsistency**: `slidev/SKILL.md` and `tsdown/SKILL.md` omit the `metadata:` block (`author`, `version`) present in all other antfu-ecosystem skills. Not a registration bug, but breaks the convention established by every other skill in the collection.

## Recommendation

CLEAR — submit PRs for all bugs and medium/low security fixes.

No critical or high security findings. Zero registration-breaking bugs. The most actionable improvements are:

1. **Security**: Validate deletion path in `scripts/cli.ts` before `rmSync` (prevents path-escape if `.gitmodules` is tampered with).
2. **Quality — highest-value**: `turborepo/SKILL.md` at 912 lines should be split; `vueuse-functions/SKILL.md` needs at least one usage pattern example per function category to earn its 420-line weight.
3. **Quality — low-effort**: Replace 10 vague quantifiers across `vue-best-practices` and `vueuse-functions` with measurable criteria (size limits, specific thresholds, named patterns).
