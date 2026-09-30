---
slug: michaelshimeles-skills
repo: michaelshimeles/skills
audited: 2026-09-30
commit_sha: 4b72f46b045e6fef52e6a98d4c162dd309826aed
score: 95
exemplifies:
  - R04
  - R05
  - R06
  - R07
  - R08
---

# Exemplar: michaelshimeles/skills

**Score**: 95/100  |  **Date**: 2026-09-30  |  **Commit**: `4b72f46b045e6fef52e6a98d4c162dd309826aed`

A collection of 7 single-purpose Claude Code skills (worktrees, PR screenshots, Greptile loops, prose cleanup, service-layer refactoring, recorded test evidence). Descriptions carry quoted trigger phrases, every SKILL.md stays under 500 lines, and the largest skills push API detail into `references/`.

## Per-rule evidence

### R04 — Description as trigger

`before-and-after` lists five literal user phrases and the accepted input forms in one frontmatter line, so the skill can be matched on real queries.

> Real quote from `before-and-after/SKILL.md:3`:
>
> ```
> description: Captures before/after screenshots of web pages or elements for visual comparison. Use when user says "take before and after", "screenshot comparison", "visual diff", "PR screenshots", "compare old and new", or needs to document UI changes. Accepts two URLs (file://, http://, https://) or two image paths.
> ```

It gives 5 quoted trigger phrases plus an input contract, instead of a summary of what the skill is.

`code-structure` triggers on situations rather than phrases, which also satisfies the rule:

> Real quote from `code-structure/SKILL.md:3`:
>
> ```
> description: Use when multiple workflows duplicate the same operational logic, when deciding what belongs in actions vs shared services, or when refactoring repeated operational blocks across domain flows. Use when adding new features that share mechanics with existing ones.
> ```

Each "when" clause names a concrete moment (duplicated logic, an actions-vs-services decision, a refactor of repeated blocks), so it matches a task in progress.

### R05 — Body length

All 7 SKILL.md files are under 500 lines. The two largest, `greploop` (455) and `greploop-apps` (463), keep bulky API material out of the body and link to it.

> Real quote from `greploop-apps/SKILL.md:343`:
>
> ```
> **GitHub** — fetch unresolved review threads and resolve all that have been addressed (see [GraphQL reference](references/graphql-queries.md)):
> ```

> Real quote from `greploop-apps/SKILL.md:375`:
>
> ```
> **GitLab** — fetch unresolved discussions and resolve each one (see [GitLab API reference](references/gitlab-api.md)):
> ```

The GraphQL and GitLab query details live in `references/*.md`, which is how a 3-platform workflow stays at 463 lines.

### R06 — Runnable examples

`code-structure` shows a Good pattern in real TypeScript, plus a two-caller example where the same mechanic serves different business rules.

> Real quote from `code-structure/SKILL.md:93-107`:
>
> ```ts
> // emailService.ts — shared mechanics
> export async function sendWelcomeEmail(params: { to: string; name: string }) {
>   const html = `<h1>Welcome ${params.name}</h1>`;
>   await emailProvider.send(params.to, "Welcome", html);
> }
>
> // userSignup.ts — orchestration (owns WHEN to send)
> if (user.marketingOptIn) {
>   await sendWelcomeEmail({ to: user.email, name: user.name });
> }
>
> // adminInvite.ts — orchestration (different business rule, same mechanic)
> await sendWelcomeEmail({ to: invitee.email, name: invitee.name });
> ```

`new-feature` does the same for shell, with a verification line whose expected output is stated:

> Real quote from `new-feature/SKILL.md:50-53`:
>
> ```bash
> cd <worktrees-dir>/<task-name>
> git branch --show-current   # must print your new branch, not main
> ```

The inline comment says what a correct result looks like, so the agent can check it.

### R07 — Scope note when related skills exist

`greploop` and `greploop-apps` overlap almost completely. The second one opens its description by naming the sibling and the single difference.

> Real quote from `greploop-apps/SKILL.md:3-8`:
>
> ```
> description: >
>   Iteratively improves a PR (GitHub), MR (GitLab), or shelved changelist (Perforce) until Greptile
>   gives it a 5/5 confidence score with zero unresolved comments. Identical to greploop, but triggers
>   reviews by tagging @greptile-apps, which bypasses Greptile's file-count limit on huge PRs that the
>   plain @greptile mention refuses to review. Use when the user wants to fully optimize a large
>   PR/MR/CL against Greptile's code review standards.
> ```

The disambiguator is "large PR" versus the plain `@greptile` mention, so the choice between the two skills is stated in the description where matching happens.

`code-structure` adds a negative scope line as well:

> Real quote from `code-structure/SKILL.md:21`:
>
> ```
> **Don't use when:** Logic is truly domain-specific and used by only one caller.
> ```

### R08 — Patterns over theory

`code-structure` turns its principles into a Do/Don't table keyed to situations.

> Real quote from `code-structure/SKILL.md:41-47`:
>
> ```
> | Design Principle | Do | Don't |
> |---|---|---|
> | API shape | Composable capability blocks | One giant "do everything" method |
> | Inputs/outputs | Explicit params, structured returns | Hidden global state, reaching into DB |
> | Migration | Extract one block, replace one caller, verify, then migrate rest | Refactor everything at once |
> | Domain logic | Keep auth, policy, error classification in actions | Let service mutate domain state directly |
> | Extraction trigger | Logic repeated across 2+ callers | Logic used once (over-abstraction) |
> ```

`new-feature` branches on the harness the agent is running in, which is a situational rule rather than a principle:

> Real quote from `new-feature/SKILL.md:14-17`:
>
> ```
> - **Claude Code**: the harness creates and manages worktrees itself (under
>   `.claude/worktrees/<name>`). **Skip steps 3–4 below** (no manual
>   `git worktree add` / `remove`), and keep the harness-assigned branch name.
>   Steps 1–2 and 5 still apply.
> ```

It names the exact steps to skip and the exact steps that still apply.

## Worth adopting

Pattern: Harness-delta block before the steps. Evidence: `new-feature/SKILL.md:12-20`. Why it would be a useful rule: a skill that runs under several harnesses should list, before step 1, which steps each harness skips, so the agent does not repeat work the harness already did.
