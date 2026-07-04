---
slug: tintinweb-pi-subagents
repo: tintinweb/pi-subagents
audited: 2026-07-04
commit_sha: 8405e556acc8ab2c0fcfa02021f871365695f776
score: 94
exemplifies:
  - R01
  - R06
  - R11
  - R33
  - R34
  - R37
  - R38
---

# Exemplar: tintinweb/pi-subagents

**Score**: 94/100  |  **Date**: 2026-07-04  |  **Commit**: `8405e556acc8ab2c0fcfa02021f871365695f776`

A [pi](https://pi.dev) extension bringing Claude Code-style sub-agents to another CLI — its `AGENTS.md`, custom-agent config format (`.pi/agents/*.md`), and 628-line `README.md` are the artifacts under review.

## Per-rule evidence

### R01 — No vague quantifiers without criteria

`AGENTS.md`'s git-safety rule doesn't say "avoid destructive git commands" — it enumerates the exact commands:

> Real quote from `AGENTS.md:44`:
>
> ```
> Never run history- or worktree-destroying commands: `git reset --hard`, `git checkout .`, `git clean -fd`, `git stash`, `git add -A`, `git add .`, `git commit --no-verify`, or any force push.
> ```

A model reading "avoid destructive git commands" has to guess which commands count; this list leaves nothing to interpret, including the non-obvious ones (`git add -A` isn't "destructive" in the usual sense, but it can stage files the user didn't intend to commit). Across the whole file only one vague-quantifier hit survives a grep for the standard list (`sufficient`, `appropriate`, etc.) — and that one hit doesn't occur; the file is clean.

### R06 — Code examples must be runnable

The custom-agent section (`README.md:177-201`) shows the actual file to create, in real YAML frontmatter plus Markdown body:

> Real quote from `README.md:180-195`:
>
> ```
> ---
> description: Security Code Reviewer
> tools: read, grep, find, bash
> model: anthropic/claude-opus-4-6
> thinking: high
> max_turns: 30
> ---
>
> You are a security auditor. Review code for vulnerabilities including:
> - Injection flaws (SQL, command, XSS)
> - Authentication and authorization issues
> - Sensitive data exposure
> - Insecure configurations
>
> Report findings with file paths, line numbers, severity, and remediation advice.
> ```

...then the actual tool call that invokes it, not a description of the calling convention:

> Real quote from `README.md:199-201`:
>
> ```
> Agent({ subagent_type: "auditor", prompt: "Review the auth module", description: "Security audit" })
> ```

Both blocks are copy-pasteable as-is: the first is a valid `.pi/agents/auditor.md` file, the second a valid tool call against it. A reader (or an LLM parsing the README to explain the feature) doesn't need to reverse-engineer syntax from prose.

### R11 — Tools follow least-privilege

The repo's own production custom agent — a security *reviewer* — is scoped to read-only tools:

> Real quote from `.pi/agents/auditor.md:1-6`:
>
> ```
> ---
> description: Security Code Reviewer
> tools: read, grep, find, bash
> model: anthropic/claude-haiku-4-5-20251001
> thinking: off
> max_turns: 10
> ---
> ```

No `write` or `edit` in the tool list — a reviewer that finds vulnerabilities has no way to alter the code it's reviewing. Worth noting this file's `model`/`thinking`/`max_turns` are deliberately cheaper than the doc's own tutorial example (`opus`/`high`/`30`), which the audit report cross-checked as intentional tuning, not drift — the least-privilege discipline extends to compute budget, not just tool access.

### R33 — Include build/run command

> Real quote from `AGENTS.md:29-33`:
>
> ```
> After code changes (not docs), run the full check suite and fix all errors and warnings:
>   npm run lint        # biome
>   npm run typecheck   # tsc --noEmit
>   npm run test        # vitest run
> ```

The comment on each line (`# biome`, `# tsc --noEmit`, `# vitest run`) tells the agent which tool actually runs under the npm script — useful when it needs to invoke that tool directly (e.g. `npx vitest run test/<file>.test.ts`, given two lines later) instead of the full suite.

### R34 — Include test command

Same block covers `npm run test`, but the file goes further and specifies the single-file iteration path and what the full suite includes:

> Real quote from `AGENTS.md:35`:
>
> ```
> `npm run test` runs the whole suite, including `*-e2e.test.ts` files. To iterate on a single file, run it directly: `npx vitest run test/<file>.test.ts`.
> ```

This preempts a specific failure mode: an agent iterating on one test file by re-running the entire suite (slow, and e2e tests in this repo need a live model — see the `PI_E2E_LIVE` note later in the same file) instead of the fast, scoped command.

### R37 — No stale references

An e2e fixture narrows tool access to one function of one extension, and the referenced extension file actually registers that function under that exact name:

> Real quote from `test/fixtures/.pi/agents/narrow-alpha-read.md:1-5`:
>
> ```
> description: "Narrows alpha to a single tool via ext:ext-alpha.mjs/alpha_read."
> extensions: "./ext-alpha.mjs, ./ext-beta.mjs"
> tools: "*, ext:ext-alpha.mjs/alpha_read"
> expect_tools_present: "read, alpha_read"
> expect_tools_absent: "alpha_write, beta_tool"
> ```
>
> And `test/fixtures/ext-alpha.mjs:12`:
>
> ```
> for (const name of ["alpha_read", "alpha_write"]) {
> ```

The fixture's `ext:ext-alpha.mjs/alpha_read` selector and its `expect_tools_present`/`expect_tools_absent` claims all resolve against the extension's real registered tool names — across all 21 e2e fixtures and their 3 referenced extension/skill files, the audit found zero broken references.

### R38 — More instructive than descriptive

`AGENTS.md` carries almost no description of what the project *is* — that's the README's job. It's wall-to-wall imperative rules for the agent working in this repo:

> Real quote from `AGENTS.md:1-8`:
>
> ```
> # Development Rules
>
> ## Conversational Style
>
> - Keep answers short and concise
> - No emojis in issues, PR comments, or code
> - No fluff or cheerful filler text (e.g., "Thanks @user" not "Thanks so much @user!")
> - Technical prose only, be direct
> ```

Every bullet in the file is an instruction ("Read files in full before...", "Never commit.", "Write the comment to a temp file and post with..."), not a fact about the codebase. A description-heavy memory file would spend tokens re-explaining what `pi-subagents` does; this one spends them entirely on how to work in it.

## Worth adopting

- **Pattern**: Explicit user-override clause in the memory file. Evidence: `AGENTS.md:99-101` — `"## User Override / If the user's instructions conflict with any rule in this document, ask for explicit confirmation before overriding. Only then execute their instructions."` Why it would be a useful rule: memory files encode standing rules, but a live user request sometimes needs to deviate from them intentionally; without a written protocol for that conflict, an agent either blindly follows the file (ignoring the user) or silently breaks the file's rules (ignoring the project) — a one-line override clause resolves the ambiguity in both directions.
- **Pattern**: Precedence table for config fields with more than one source. Evidence: `README.md:375-381` — a three-row table mapping `Caller-supplied` / `Pinned in agent frontmatter` / `Parent-inherited` to distinct out-of-scope behaviors (hard error vs. warning-and-run). Why it would be a useful rule: prose like "frontmatter is authoritative" doesn't specify what happens for the sources it *doesn't* mention; a table enumerating every source and its exact resulting behavior removes the gap prose leaves for the reader (or the LLM) to fill in by guessing.
