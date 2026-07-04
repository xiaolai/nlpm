---
slug: vercel-labs-agent-skills
repo: vercel-labs/agent-skills
audited: 2026-07-04
commit_sha: f8a72b9603728bb92a217a879b7e62e43ad76c81
score: 99
exemplifies:
  - R04
  - R05
  - R06
  - R07
  - R08
  - R11
---

# Exemplar: vercel-labs/agent-skills

**Score**: 99/100  |  **Date**: 2026-07-04  |  **Commit**: `f8a72b9603728bb92a217a879b7e62e43ad76c81`

A 9-skill collection covering Vercel deployment, React/Next.js performance, and design-review workflows for Claude Code, Codex, and claude.ai — notable for keeping every SKILL.md well under the line cap while still shipping runnable, incorrect-vs-correct code examples via a rules/ sub-directory pattern.

## Per-rule evidence

### R04 — Description is a trigger, not a summary

Every one of the 9 `SKILL.md` frontmatter blocks packs concrete trigger phrases instead of a generic summary.

> `skills/deploy-to-vercel/SKILL.md:3`:
>
> ```
> description: Deploy applications and websites to Vercel. Use when the user requests deployment actions like "deploy my app", "deploy and give me the link", "push this live", or "create a preview deployment".
> ```

> `skills/vercel-cli-with-tokens/SKILL.md:3`:
>
> ```
> description: Deploy and manage projects on Vercel using token-based authentication. Use when working with Vercel CLI using access tokens rather than interactive login — e.g. "deploy to vercel", "set up vercel", "add environment variables to vercel".
> ```

Both descriptions quote literal user phrasing ("deploy my app", "push this live") rather than describing the skill in the abstract — this is what lets a model pick the right skill among 9 similar-sounding deploy-adjacent options.

### R05 — Under 500 lines

All 9 `SKILL.md` files stay well clear of the 500-line ceiling, with the largest at 353 lines:

```
89   skills/composition-patterns/SKILL.md
296  skills/deploy-to-vercel/SKILL.md
149  skills/react-best-practices/SKILL.md
121  skills/react-native-skills/SKILL.md
320  skills/react-view-transitions/SKILL.md
353  skills/vercel-cli-with-tokens/SKILL.md
322  skills/vercel-optimize/SKILL.md
39   skills/web-design-guidelines/SKILL.md
39   skills/writing-guidelines/SKILL.md
```

The two skills with the deepest rule catalogs (`react-best-practices` at 70 rules, `composition-patterns` at 8 rules) don't inline the rules into `SKILL.md` at all — they push detail into a `rules/` sub-directory and keep the top-level file to a category index (see R07, R08 below). That's the mechanism that keeps line count flat regardless of catalog size.

### R06 — Code examples must be runnable

Rule files under `rules/` pair a labeled-incorrect example with a labeled-correct example, both in real TSX, not pseudocode.

> `skills/composition-patterns/rules/architecture-avoid-boolean-props.md:14-46` (incorrect example, abbreviated):
>
> ```tsx
> function Composer({
>   onSubmit,
>   isThread,
>   channelId,
>   isDMThread,
>   dmId,
>   isEditing,
>   isForwarding,
> }: Props) {
>   return (
>     <form>
>       <Header />
>       <Input />
>       {isDMThread ? (
>         <AlsoSendToDMField id={dmId} />
>       ) : isThread ? (
>         <AlsoSendToChannelField id={channelId} />
>       ) : null}
>       ...
> ```
>
> followed immediately by `rules/architecture-avoid-boolean-props.md:48-97`, a full working replacement (`ChannelComposer`, `ThreadComposer`, `EditComposer`) that compiles as real components, not a sketch.

The incorrect example isn't a strawman — it's the exact shape (`isThread`, `isDMThread`, `isEditing`, `isForwarding` all on one component) that boolean-prop creep actually produces, which is what makes the contrast land.

### R07 — Scope note when related skills exist

Both multi-rule skills end their `SKILL.md` with an explicit pointer to where the full detail lives, rather than leaving the reader to guess.

> `skills/composition-patterns/SKILL.md:89` and identically `skills/react-best-practices/SKILL.md:149`:
>
> ```
> For the complete guide with all rules expanded: `AGENTS.md`
> ```

This is a scope note in the opposite direction from the usual "see other skill X" — it tells the agent that `SKILL.md` is the index and a sibling file is the expansion, so a model that needs rule detail beyond the Quick Reference table knows exactly which file to open instead of re-deriving it from the rule filename.

### R08 — Patterns over theory

`deploy-to-vercel/SKILL.md` teaches deployment as a decision tree over four concrete project states, not an explanation of how Vercel deployment works in the abstract.

> `skills/deploy-to-vercel/SKILL.md:53-104` (section headers only):
>
> ```
> ## Step 2: Choose a Deploy Method
> ### Linked (`.vercel/` exists) + has git remote → Git Push
> ### Linked (`.vercel/` exists) + no git remote → `vercel deploy`
> ### Not linked + CLI is authenticated → Link first, then deploy
> ### Not linked + CLI not authenticated → Install, auth, link, deploy
> ```

Each branch is a numbered command sequence keyed to a detectable state (git remote present/absent × CLI linked/authenticated), not a prose description of what `vercel link` or `vercel deploy` do conceptually — an agent can match its actual `git remote` / `.vercel/` findings straight to a branch and run the commands under it.

### R11 — Tools follow least-privilege

`skills/vercel-optimize/lib/vercel.mjs` documents, in the file itself, the choice not to shell out with string interpolation.

> `skills/vercel-optimize/lib/vercel.mjs:1`:
>
> ```
> // Vercel CLI helpers. All shell-outs use execFile (not exec) — no shell injection. Error detection: exit code + JSON-parse first; stderr grep only as fallback (CLI error strings aren't a stable contract).
> ```

The audit spot-checked ~65 files under `skills/vercel-optimize/{scripts,lib}/` and confirmed every shell-out uses `execFile` with an argument array rather than `shell: true` or string interpolation — the file-level comment isn't just a stated intent, it matches the actual invocation pattern used throughout the directory.

## Worth adopting

Pattern: self-documenting security choice in a comment at the top of a file that does subprocess execution. Evidence: `skills/vercel-optimize/lib/vercel.mjs:1`. Why it would be a useful rule: a one-line comment stating "shell-outs use execFile, not exec/shell:true" gives both a human reviewer and an NL security scanner an explicit, checkable claim to verify against the code below it, rather than requiring the scanner to infer intent from call-site patterns alone.
