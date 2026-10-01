---
slug: hex-claude-council
repo: hex/claude-council
audited: 2026-10-01
commit_sha: ea1dcbf42ae255b9b96141c732c1a2d396390580
score: 95
exemplifies:
  - R06
  - R09
  - R11
  - R14
  - R15
  - R18
---

# Exemplar: hex/claude-council

**Score**: 95/100  |  **Date**: 2026-10-01  |  **Commit**: `ea1dcbf42ae255b9b96141c732c1a2d396390580`

A Claude Code plugin that fans a question out to several AI providers. Its commands declare argument handling and tool allowlists explicitly, and its skills give the exact shell invocation plus the failure reason behind each rule.

## Per-rule evidence

### R06 — Runnable code examples

`skills/council-execution/SKILL.md` gives the real command with real flags, then states the flag syntax and why the `--` separator is required. The Bash timeout is stated as a concrete number with the cause of the failure it prevents.

> Real quote from `skills/council-execution/SKILL.md:10-22`:
>
> ```
> bash ${CLAUDE_PLUGIN_ROOT}/scripts/run-council.sh --providers=gemini,openai -- "Your question"
>
> This outputs the path to the saved file (e.g., `.claude/council-cache/council-1734567890.md`).
>
> **Flag syntax**: Use `=` with no spaces: `--providers=gemini,openai`
>
> **CRITICAL**: Always place `--` before the prompt to prevent prompt text containing dashes from being parsed as flags.
> ```

The command can be pasted into a shell, and the expected output path is shown next to it.

### R09 — Agent description with examples

`agents/council-advisor.md` opens its description with a trigger sentence, then supplies three `<example>` blocks. Each has Context, user turn, assistant turn and a `<commentary>` explaining why the agent fires.

> Real quote from `agents/council-advisor.md:4-13`:
>
> ```
> description: |-
>   Use this agent when the user is facing architectural decisions, design choices, or has been stuck debugging a problem after multiple failed attempts. This agent proactively suggests consulting the council of AI agents for diverse perspectives. Examples:
>
>   <example>
>   Context: User is designing authentication for their application and weighing different approaches.
>   user: "I'm trying to decide between JWT and session-based auth for this Express app. What do you think?"
>   ...
>   <commentary>
>   Architecture decisions with tradeoffs benefit from multiple expert perspectives. The council-advisor should suggest /claude-council:ask to gather diverse opinions on the approach.
>   </commentary>
>   </example>
> ```

The three examples cover architecture choice, debugging dead-end and technology choice, so each trigger class has a worked case. (The audit docked this file for description length; the examples are the reason.)

### R11 — Least-privilege tools

`commands/result.md` manages background jobs, so it allows one script entry point plus `Read`. The Bash pattern is pinned to a single script, not a bare `Bash`.

> Real quote from `commands/result.md:4`:
>
> ```
> allowed-tools: Bash(bash */scripts/run-council.sh *), Read
> ```

`council-advisor` is similarly read-only: `tools: ["Read", "Grep", "Glob"]` (`agents/council-advisor.md:34`), which matches a role that only suggests.

### R14 — Numbered steps

`skills/council-execution/SKILL.md` splits the pipeline into numbered, titled steps, each with one action.

> Real quote from `skills/council-execution/SKILL.md:8,31,53`:
>
> ```
> ## Step 1: Run Query and Save to File
> ## Step 2: Read and Display the Output VERBATIM
> ## Step 3: Complete the Synthesis Section
> ```

Each step names its tool (Bash, Read, then a prompt file), so the order cannot be inferred wrongly.

### R15 — Handle empty input

`commands/result.md` opens with an Argument Handling block that maps every input shape, including the empty one, to a branch.

> Real quote from `commands/result.md:9-13`:
>
> ```
> ## Argument Handling
>
> - `$ARGUMENTS` is empty or `list`: list jobs
> - `$ARGUMENTS` is `cancel <job-id>`: cancel that job
> - Otherwise: treat `$ARGUMENTS` as a job id and fetch its result
> ```

Three bullets cover empty, keyword and fallthrough input with no overlap.

### R18 — `argument-hint`

`commands/result.md` and `commands/advise.md` document their usage pattern in frontmatter.

> Real quote from `commands/result.md:3`:
>
> ```
> argument-hint: '[job-id] | list | cancel <job-id>'
> ```

The hint mirrors the three branches in the Argument Handling block, so `/help` and the body agree.
