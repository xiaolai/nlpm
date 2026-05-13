---
slug: backnotprop-plannotator
repo: backnotprop/plannotator
audited: 2026-05-13
commit_sha: ef3172e33924d0eb3721573f9283bc6fb50a2603
score: 93
exemplifies:
  - R04
  - R06
  - R07
  - R08
---

# Exemplar: backnotprop/plannotator

**Score**: 93/100  |  **Date**: 2026-05-13  |  **Commit**: `ef3172e33924d0eb3721573f9283bc6fb50a2603`

A plan-review and code-annotation plugin for Claude Code that ships five SKILL.md files, all scoring 100. The skills demonstrate trigger-dense descriptions, embedded runnable commands, tight scope delimitation, and full sub-agent dispatch templates.

## Per-rule evidence

### R04 — Description as trigger

The rule requires 3+ specific action phrases matching real user queries. All four `.agents/skills/` files and the compound skill satisfy this. The release skill packs natural-language synonyms alongside structural triggers, covering the realistic spread of how users phrase the same request.

> Real quote from `.agents/skills/release/SKILL.md:3-4`:
>
> ```
> description: Prepare and execute a Plannotator release — draft release notes with full contributor credit, bump versions across all package files, build in dependency order, and kick off the tag-driven release pipeline. Use this skill whenever the user mentions preparing a release, bumping versions, writing release notes, tagging a release, or publishing. Also trigger when the user says things like "let's ship", "prep a release", "what's changed since last release", or "time to cut a new version".
> ```

Four distinct trigger clusters in one description: structural verbs ("draft release notes", "bump versions"), event terms ("tagging a release", "publishing"), colloquial phrases ("let's ship", "prep a release"), and question forms ("what's changed since last release"). A description that covers only the formal name of the operation misses the majority of real invocations.

The pierre-guard skill shows the same pattern applied to a safety-gate context:

> Real quote from `.agents/skills/pierre-guard/SKILL.md:3-4`:
>
> ```
> description: Guard against breaking the @pierre/diffs integration in Plannotator's code review UI. Use this skill whenever modifying DiffViewer.tsx, upgrading the @pierre/diffs package, changing unsafeCSS injection, adding new props to FileDiff, or touching shadow DOM selectors or CSS variables that cross into Pierre's shadow boundary. Also trigger when someone asks "will this break the diff viewer", "is this safe to change", or when reviewing PRs that touch the review-editor package.
> ```

The "Also trigger when someone asks" clause registers question-form queries as first-class triggers — the file/path triggers alone would miss a user asking a safety question in natural language.

---

### R06 — Code examples must be runnable

The review-renovate skill embeds the exact CLI invocation an agent would run to verify a GitHub Actions SHA — no pseudocode, no placeholders needing lookup.

> Real quote from `.agents/skills/review-renovate/SKILL.md:36-38`:
>
> ```
> ### 3. Verify pinned SHAs against upstream tags
>
> For every action being updated, verify **both old and new** SHAs match the claimed version tags:
>
> ```
> gh api repos/{owner}/{repo}/git/ref/tags/{version} --jq '.object.sha'
> ```
>
> Compare each result against the SHA in the workflow file. If any SHA does not match, **stop and report a supply chain integrity failure**. Do not approve the PR.
> ```

The command includes the `jq` filter that extracts the field directly — the agent doesn't need to figure out the response structure. The instruction that follows turns the command's output into a binary gate ("does not match → stop") rather than leaving interpretation open.

The release skill's contributor-research section applies the same concreteness to GitHub API calls:

> Real quote from `.agents/skills/release/SKILL.md:36-43`:
>
> ```bash
> # Get issue details including author
> gh issue view <number> --json author,title,body
>
> # Get issue comments to find participants
> gh api repos/backnotprop/plannotator/issues/<number>/comments --jq '.[].user.login'
>
> # Get PR review comments
> gh api repos/backnotprop/plannotator/pulls/<number>/comments --jq '.[].user.login'
> ```

The owner/repo is hardcoded, not a generic placeholder — these commands run without substitution.

---

### R07 — Scope note when related skills exist

The pierre-guard skill delimits its scope to a single source file and a single import surface, eliminating ambiguity about where the skill's constraints apply.

> Real quote from `.agents/skills/pierre-guard/SKILL.md:25-26`:
>
> ```
> These are the only three imports. `DiffViewer.tsx` is the only file that touches Pierre.
> ```

Without this sentence, an agent reviewing a PR might waste time cross-checking other components against Pierre's API. The phrase "the only file" ends that search immediately.

The release skill applies the same pattern to version management, naming an exact list of files that are in scope and explicitly excluding one that is not:

> Real quote from `.agents/skills/release/SKILL.md:120-135`:
>
> ```
> Bump the version string in these **7 files** (and only these — other package.json files use stub versions):
>
> | File | Field |
> |------|-------|
> | `package.json` (root) | `"version"` |
> | `apps/opencode-plugin/package.json` | `"version"` |
> ...
>
> Do not bump the VS Code extension (`apps/vscode-extension/package.json`) — it has independent versioning.
> ```

"7 files (and only these)" is a hard constraint, not a guideline. The explicit exclusion of `vscode-extension/package.json` prevents the most likely mistake (bumping all `package.json` files) without requiring the agent to infer why from the project structure.

---

### R08 — Patterns over theory

The update-deps skill teaches dependency auditing by embedding the complete sub-agent prompt that the orchestrator passes to each per-package Haiku agent, including the JSON output schema the orchestrator expects back.

> Real quote from `.agents/skills/update-deps/SKILL.md:40-97`:
>
> ```
> ### Sub-agent prompt template
>
> For each outdated package, spawn a Sonnet agent with this task:
>
> ```
> You are auditing the npm package "{package}" for a version bump from {current} to {target}.
>
> Run these checks and report back with a JSON object:
>
> 1. **Maintainer verification**: Check if maintainers changed between versions.
>    npm view {package}@{current} maintainers --json
>    npm view {package}@{target} maintainers --json
>    Compare the two lists. Flag any additions or removals.
> ...
> Report your findings as JSON:
>
> {{
>   "package": "{package}",
>   ...
>   "verdict": "safe" | "review" | "defer",
>   "verdict_reason": "<one sentence explanation>"
> }}
>
> Verdict guidelines:
> - "safe": Same maintainers, no new runtime deps, changes match what changelog describes, no suspicious patterns
> - "review": Minor concerns (e.g., new maintainer who is clearly from the same org, small new dep from known publisher)
> - "defer": Maintainer changes from unknown accounts, new runtime deps with unclear purpose...
> ```
> ```

A skill that says "check maintainers, check age, check provenance" is abstract instruction. This skill shows the exact prompt the sub-agent receives, the exact JSON fields it must emit, and the exact decision criteria for each verdict value. An orchestrating agent reading this can copy the template directly without inference.

The pierre-guard skill applies the same approach to a verification checklist — each item is a concrete imperative with a grep command or test step, not a category name:

> Real quote from `.agents/skills/pierre-guard/SKILL.md:105-108`:
>
> ```
> ### Shadow DOM Selectors
> - [ ] Grep the upstream source for each `data-*` attribute we target in `unsafeCSS`
> - [ ] If upgrading the package version, diff the old and new CSS/HTML output for renamed attributes
> - [ ] Test both `split` and `unified` views — selectors are layout-dependent
> ```

---

## Worth adopting

**Pattern: Embedded dispatch template.** Evidence: `.agents/skills/update-deps/SKILL.md:39-97`. A skill that orchestrates sub-agents includes a complete, ready-to-send prompt template inside a fenced block, with `{placeholder}` tokens for the per-invocation variables. The orchestrating agent reads the template, substitutes the variables, and passes the result to a sub-agent — no prompt engineering required at runtime. Why it would be a useful rule: when an orchestration skill leaves the sub-agent prompt to be inferred, different runs produce structurally inconsistent outputs; embedding the template makes the output schema a contract, not a suggestion.
