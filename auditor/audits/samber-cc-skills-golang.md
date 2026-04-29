# NLPM Audit: samber/cc-skills-golang
**Date**: 2026-04-29  |  **Artifacts**: 40  |  **Strategy**: batched
**NL Score**: 87/100
**Security**: CLEAR
**Bugs**: 3  |  **Quality Issues**: 6  |  **Security Findings**: 0

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/golang-graphql/SKILL.md | skill | 45 | -55 empty skill body — placeholder text only; no persona, guidance, examples, modes, or best practices |
| skills/golang-stay-updated/SKILL.md | skill | 77 | -10 no inline code examples (R06), -5 no persona (R03), -5 resource-list-only body (R06), -3 vague trigger description (R04) |
| skills/golang-popular-libraries/SKILL.md | skill | 82 | -8 thin body with minimal standalone guidance (R06), -5 vague description triggers (R04), -5 no modes section (R10) |
| skills/golang-uber-dig/SKILL.md | skill | 82 | -18 broken cross-reference to non-existent `golang-google-wire` skill |
| skills/golang-uber-fx/SKILL.md | skill | 83 | -17 broken cross-reference to non-existent `golang-google-wire` skill |
| skills/golang-benchmark/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-cli/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-code-style/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-concurrency/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-context/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-continuous-integration/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-data-structures/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-database/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-dependency-injection/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-dependency-management/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-design-patterns/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-documentation/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-error-handling/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-grpc/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-lint/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-modernize/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-naming/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-observability/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-project-layout/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-safety/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-samber-do/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-samber-hot/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-samber-lo/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-samber-mo/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-samber-oops/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-samber-ro/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-samber-slog/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-stretchr-testify/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-structs-interfaces/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-testing/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, examples, cross-references |
| skills/golang-troubleshooting/SKILL.md | skill | 89 | minor vague quantifiers (R01); otherwise well-formed with persona, modes, ultrathink directive, examples |
| .claude-plugin/plugin.json | config | 90 | plugin manifest — no skill frontmatter or trigger description by design |
| CLAUDE.md | config | 90 | developer guide — no skill frontmatter or trigger description by design |
| skills/golang-performance/SKILL.md | skill | 91 | minor vague quantifiers (R01); excellent structure with ultrathink, modes, decision tree |
| skills/golang-security/SKILL.md | skill | 91 | minor vague quantifiers (R01); excellent structure with ultrathink, parallel audit agents, decision tree |

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
| Scripts | none |
| Package manifest | none |
| Hooks | none |
| MCP configs | none |

CLEAR — no executable surfaces found. The repository is pure markdown with no hooks, shell scripts, package manifests, or MCP server configurations. No patterns were evaluated because no surfaces exist to evaluate them against.

## Bugs (PR-worthy)

| # | File | Issue | Confidence | Evidence |
|---|------|-------|------------|----------|
| 1 | skills/golang-graphql/SKILL.md | Skill body contains only the placeholder text `(Content will be added in a future iteration)` — no instructions, no code examples, no guidance. The skill has valid frontmatter (`user-invocable: false`, version `0.0.2`) but provides zero instructional value and will never productively load. | high | Body lines 1–7 read only the placeholder string; no headings, code, or instructional text present |
| 2 | skills/golang-uber-dig/SKILL.md | Cross-References section links to `` `samber/cc-skills-golang@golang-google-wire` `` but no `skills/golang-google-wire/` directory exists in the repository. Agents following this reference will silently receive no content. | high | `ls skills/golang-google-wire` returns no match; skill name appears in Cross-References section of uber-dig but has no corresponding directory |
| 3 | skills/golang-uber-fx/SKILL.md | Same broken cross-reference to `` `samber/cc-skills-golang@golang-google-wire` `` as uber-dig — likely a copy-paste from the same Cross-References template. | high | `ls skills/golang-google-wire` returns no match; same dangling reference appears in uber-fx Cross-References section |

## Security Fixes (PR-worthy, Medium/Low only)

None. Security scan returned CLEAR with no executable surfaces.

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/golang-stay-updated/SKILL.md | Body is a curated resource/link list with no instructional content, no code examples, and no procedural guidance. A developer loading this skill gets a bibliography, not actionable direction. (R06) | -10 |
| 2 | skills/golang-stay-updated/SKILL.md | No persona — the skill has no analytical or generative frame, which is acceptable for very short procedural skills, but combined with a resource-only body, the skill lacks any triggering context for the model. (R03) | -5 |
| 3 | skills/golang-stay-updated/SKILL.md | Description lacks specific "Use when" trigger scenarios. Without concrete triggers, contextual auto-loading is unreliable. (R04) | -3 |
| 4 | skills/golang-popular-libraries/SKILL.md | Body has minimal standalone guidance — it names library categories and defers all depth to reference files. Inline content is too thin to be useful if references aren't loaded. (R06) | -8 |
| 5 | skills/golang-popular-libraries/SKILL.md | Description triggers are broad ("when choosing libraries") without specificity. Risks over-triggering on any Go session where library choice comes up incidentally. (R04) | -5 |
| 6 | skills/golang-graphql/SKILL.md | `user-invocable: false` means the skill should auto-trigger on context — but with an empty body, there is no trigger signal. The skill is effectively invisible: it won't activate automatically (no body content to match against), and it can't be invoked manually (not user-invocable). Should either be raised to `user-invocable: true` as a placeholder or the frontmatter should set `user-invocable: false` with a meaningful trigger description once the body is written. | -5 |

## Cross-Component

**Dangling `golang-google-wire` cross-references**: Both `skills/golang-uber-dig/SKILL.md` and `skills/golang-uber-fx/SKILL.md` include a Cross-References entry pointing to `` `samber/cc-skills-golang@golang-google-wire` `` for compile-time DI. No `skills/golang-google-wire/` directory exists in the repository. The identical wording in both files suggests the reference was copied from a template listing planned cross-skills and `golang-google-wire` was never created. Resolution options: (1) create `skills/golang-google-wire/` covering Google Wire — the repository already covers dig, fx, samber/do, and samber/lo, so Wire is the obvious gap; or (2) remove the dangling cross-reference from both files and link to `samber/cc-skills-golang@golang-dependency-injection` for the general comparison instead.

**Performance skill cluster boundary**: `golang-performance`, `golang-benchmark`, `golang-troubleshooting`, and `golang-observability` form a documented cluster with explicit boundary disclaimers in their descriptions. Cross-references are consistent and no content duplication was detected. The cluster design is well-executed.

**`golang-graphql` stub vs. `user-invocable: false`**: A stub skill set to `user-invocable: false` is unactivatable by any path until it has content. It should be either completed or changed to `user-invocable: true` (marking it as a manual-only placeholder) until content is written.

## Recommendation

**CONTRIBUTE** — submit PRs for the 3 bugs.

The collection is a high-quality, cohesive set of 38 Go skills. 35 of 38 skills score 89–91, with proper frontmatter, personas, modes, code examples, cross-references, and common-mistakes tables throughout. The three bugs are mechanical, self-contained fixes:

1. **Bug fix 1 — `golang-graphql` stub**: Either write the skill body (covering GraphQL client/server patterns with gqlgen and graphql-client) or, if content is not ready, convert to `user-invocable: true` and add a description that acknowledges the stub status. This is the highest-priority fix — a 45/100 scoring artifact drags the collection average by 1.6 points.

2. **Bug fix 2+3 — broken `golang-google-wire` cross-references**: Remove the dangling references from both `golang-uber-dig/SKILL.md` and `golang-uber-fx/SKILL.md`, or create `skills/golang-google-wire/` to fulfill the reference. Given that the repo already covers all other major Go DI approaches (dig, fx, samber/do, samber/lo), creating the Wire skill is the higher-value path — but removing the broken link is an acceptable minimal fix.

No security concerns. No structural or systemic issues with the NL artifact design. The plugin is safe to contribute to.
