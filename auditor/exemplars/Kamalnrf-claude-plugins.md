---
slug: Kamalnrf-claude-plugins
repo: Kamalnrf/claude-plugins
audited: 2026-06-20
commit_sha: 992902339ff12aea44ad2e59d01e4c72d26571fa
score: 98
exemplifies:
  - R04
  - R06
  - R08
  - R02
---

# Exemplar: Kamalnrf/claude-plugins

**Score**: 98/100  |  **Date**: 2026-06-20  |  **Commit**: `992902339ff12aea44ad2e59d01e4c72d26571fa`

A skills-discovery meta-skill paired with a Bun-runtime project memory. The skill's `description` field encodes a 5-condition trigger algorithm, and the body pairs every instruction with a runnable command.

## Per-rule evidence

### R04 — Description as trigger

The `description` field in `skills-discovery/SKILL.md` opens with the use-case, then immediately encodes trigger logic as explicit conditions rather than relying on the agent to infer when to fire.

> Real quote from `skills/skills-discovery/SKILL.md:3`:
>
> ```
> description: Search for and install Agent Skills that give you specialized capabilities.
> Before starting work, ask might a skill exist that handles this better than my base
> knowledge? If the task involves specific technologies, frameworks, file formats, or
> expert domains. Search proactively, even if the user doesn't mention skills. Skills
> encode best practices, tools, and techniques you wouldn't otherwise have. Also use
> when users explicitly ask to find, install, or manage skills.
> ```

Five distinct firing conditions in one paragraph: (1) before starting non-trivial work, (2) specific technologies/frameworks/file formats, (3) expert domains, (4) proactively even without user mention, (5) explicit user request. Each condition is stated positively and independently, so any single one is sufficient to trigger the skill. Compare to a typical description like "Helps find skills" — that describes capability without specifying when to invoke it.

### R06 — Runnable examples

The skill provides three classes of runnable content: the search API call with all parameters, the install command with every flag variation, and a complete end-to-end dialogue example showing the full agent interaction pattern.

> Real quote from `skills/skills-discovery/SKILL.md:32-61`:
>
> ```bash
> curl "https://claude-plugins.dev/api/skills?q=QUERY&limit=20&offset=0"
> ```
>
> ```json
> {
>   "skills": [
>     {
>       "id": "...",
>       "name": "skill-name",
>       "namespace": "@owner/repo/skill-name",
>       "sourceUrl": "https://github.com/...",
>       "description": "...",
>       "author": "...",
>       "installs": 123,
>       "stars": 45
>     }
>   ],
>   "total": 100,
>   "limit": 10,
>   "offset": 0
> }
> ```

The response schema is included alongside the request so the agent knows which fields to extract when presenting results. The install section (lines 98–114) shows `--client` and `--local` flag variations in separate commands rather than combining all flags in a single example — each variant is runnable in isolation. The full dialogue at lines 145–163 shows agent output format, not just API syntax.

### R08 — Patterns over theory

The "Search strategies" section at lines 64–73 delivers four concrete construction patterns instead of generic advice.

> Real quote from `skills/skills-discovery/SKILL.md:66-73`:
>
> ```
> The registry indexes skill names, descriptions, and tags. Construct queries that match
> how skill authors describe their work.
>
> **Query construction:**
>
> - Use 1-3 specific terms (too broad = noise, too narrow = misses)
> - Prefer widely-used terminology over project-specific jargon
> - Technology + task often outperforms either alone
> - If results are poor, broaden or try synonyms
> ```

"Technology + task often outperforms either alone" is a construction rule: `django rest` beats `django` or `api` in isolation. The parenthetical on the first bullet — `(too broad = noise, too narrow = misses)` — names the failure mode for each edge, giving the agent enough context to self-correct without returning to the skill for help.

### R02 — Tokens earn their keep

The `CLAUDE.md` project memory is 107 lines with zero explanatory prose. Every section is a substitution table: the preferred command on the left, the deprecated alternatives on the right.

> Real quote from `CLAUDE.md:2-9`:
>
> ```
> Default to using Bun instead of Node.js.
>
> - Use `bun <file>` instead of `node <file>` or `ts-node <file>`
> - Use `bun test` instead of `jest` or `vitest`
> - Use `bun build <file.html|file.ts|file.css>` instead of `webpack` or `esbuild`
> - Use `bun install` instead of `npm install` or `yarn install` or `pnpm install`
> - Use `bun run <script>` instead of `npm run <script>` or `yarn run <script>` or `pnpm run <script>`
> - Bun automatically loads .env, so don't use dotenv.
> ```

Six substitutions in six bullets, each containing both the target command and the deprecated alternatives it replaces. The Testing and APIs sections follow the same format: no background on why Bun was chosen, no caveats, just the replacement command. The file scores 100/100 with zero vague quantifiers.

## Worth adopting

**Pattern: Decision algorithm in the description field.** Evidence: `skills/skills-discovery/SKILL.md:3`. The description encodes a 5-step "do I have it / might one exist" firing algorithm directly in the `description` frontmatter rather than only in the body. Agents scan descriptions to decide which skills to load — a description that encodes the firing conditions directly eliminates the body-read round-trip for the skip case. Why it would be a useful rule: the trigger lives where the loader reads it, not inside content the loader never reads when skipping.

**Pattern: Substitution-pair bullet format for project memory.** Evidence: `CLAUDE.md:4-9`. Bun substitutions use `` Use `A` instead of `B` `` on every bullet rather than separate "use" and "don't use" lists. The pair format keeps the constraint and its concrete alternative co-located. Why it would be a useful rule: substitution-pair bullets are more actionable than standalone prohibitions because they answer "what not to do" and "what to do instead" in the same line, removing the need for the agent to cross-reference two sections.
