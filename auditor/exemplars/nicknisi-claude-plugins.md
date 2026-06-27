---
slug: nicknisi-claude-plugins
repo: nicknisi/claude-plugins
audited: 2026-06-27
commit_sha: 4cb7c053d6c48fb0fd0e45fd1ae4348214f61ad1
score: 90
exemplifies:
  - R04
  - R05
  - R08
  - R09
  - R12
  - R14
  - R30
---

# Exemplar: nicknisi/claude-plugins

**Score**: 90/100  |  **Date**: 2026-06-27  |  **Commit**: `4cb7c053d6c48fb0fd0e45fd1ae4348214f61ad1`

A multi-plugin Claude Code marketplace (8 plugins, 60 artifacts) notable for descriptions written as query-trigger lists, commands with tight output contracts, and an agent that includes a negative-trigger example to prevent mis-dispatch.

## Per-rule evidence

### R04 — Description as trigger

`prototype`'s description enumerates 7 distinct intent phrases and explicitly covers the case where none of the canonical words appear.

> Real quote from `plugins/essentials/skills/prototype/SKILL.md:3-13`:
>
> ```
> description: >-
>   Build a throwaway prototype to answer a design question before committing to
>   real implementation. Generates either a runnable terminal app (for state
>   machines, data models, business logic) or several radically different UI
>   variations on one route (for visual/layout decisions). Use when the user wants
>   to prototype, spike, POC, sanity-check a data model, mock up a UI, explore
>   design options, or says "prototype this", "spike this out", "let me play with
>   it", "try a few designs", "sketch this in code", "I want to try something
>   before building it for real", "quick and dirty version", or "validate this
>   approach" — even if they don't use the word "prototype."
> ```

The phrase "even if they don't use the word 'prototype'" is what separates this from an adequate description: it explicitly defends against miss-triggering on idiomatic requests ("spike this out", "quick and dirty version") that share intent but share no keyword with the skill name.

### R05 — Body length

`de-slopify` delivers its complete instruction set in 15 body lines. There is no orientation paragraph, no closing summary, no "this skill helps you" sentence.

> Real quote from `plugins/essentials/skills/de-slopify/SKILL.md:7-21`:
>
> ```
> The branch to diff against is $1. If no branch was provided, default to `main`.
>
> Check the diff against the branch, and remove all AI generated slop introduced in this branch.
>
> This includes:
>
> - Extra comments that a human wouldn't add or is inconsistent with the rest of the file (useful doc comments are good to keep)
> - Extra defensive checks or try/catch blocks that are abnormal for that area of the codebase (especially if called by trusted / validated codepaths)
> - Casts to any to get around type issues
> - Any other style that is inconsistent with the file
>
> Report at the end with only a 1-3 sentence summary of what you changed
> ```

Every sentence changes Claude's behavior: the first sets the diff target and default, the list enumerates exactly four slop classes (with carve-outs), and the last line caps the output format. Nothing is decorative.

### R08 — Patterns over theory

Rather than defining what a prototype is, the `prototype` skill gives a binary dispatch test expressed as observable user behavior.

> Real quote from `plugins/essentials/skills/prototype/SKILL.md:22-29`:
>
> ```
> The litmus test: **if the user could answer the question by looking at a screen, it's UI.
> If they'd need to push buttons and watch state change, it's logic.**
>
> - **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). Build a tiny
>   interactive app that pushes the state machine through cases that are hard to reason
>   about on paper.
> - **"What should this look like?"** → [UI.md](UI.md). Generate several radically
>   different UI variations on a single route, switchable via a URL search param and a
>   floating bottom bar.
> ```

The test is two observable conditions, each mapping directly to a sub-skill. A model cannot misapply a rule that says "push buttons and watch state change" the way it can misapply a rule that says "interactive."

### R09 — Example blocks are mandatory

`security-auditor` includes 3 `<example>` blocks. The third shows a non-trigger, explicitly handling the nearest-neighbor false-positive (generic code review).

> Real quote from `plugins/essentials/agents/security-auditor.md:24-31`:
>
> ```
>   <example>
>   Context: User asks for general code review.
>   user: "Can you review this PR for code quality?"
>   assistant: "I'll handle the code quality review directly. The security-auditor is
>   reserved for explicit security audits."
>   <commentary>
>   NOT a trigger. The description explicitly says "Do not auto-invoke for general code
>   review." Generic review requests use a different path.
>   </commentary>
>   </example>
> ```

Without a negative example, two positive examples covering "security audit" and "IDOR/auth bypass" leave the dispatch boundary ambiguous for any "review" request. The third example closes that gap by demonstrating the refusal explicitly.

### R12 — Output format defined in body

Phase 6 of `security-auditor` enumerates 7 mandatory fields per finding and caps total report length.

> Real quote from `plugins/essentials/agents/security-auditor.md:163-177`:
>
> ```
> ## Phase 6 — Output
>
> Report only confirmed high or critical issues and possible attacks. Do not propose
> detailed fixes. Do not create files; include all analysis and findings directly in
> the response.
>
> Each finding must include:
>
> - a high-level description of the vulnerability
> - its exact extent (e.g., "these four endpoints are affected") and impact
> - why the issue matters in the threat model and what new capability the attacker
>   gains that they did not have before
> - an exploit flow specifying all necessary steps and data an attacker must pass in
> - any endpoints the attacker calls
> - any relevant permissions needed to access the passed-in data or call endpoints
> - thoroughly commented code snippets
>
> Use casual, natural language when describing the issue and its impacts. Keep the
> entire report to roughly one page.
> ```

The bullet "what new capability the attacker gains that they did not have before" functions as a severity gate embedded in the output spec: a finding that can't answer that question doesn't belong in the report.

### R14 — Steps must be numbered

`capture.md` breaks its workflow into 6 numbered steps. Step 6 co-locates the output format with the reporting step rather than placing it in a separate section.

> Real quote from `plugins/sidequest/commands/capture.md:96-107`:
>
> ```
> ### 6. Report back
>
> Four lines, nothing more:
>
> ```
> Parked: <seed>
> File: <absolute path to markdown>
> OmniFocus: "<seed>" in "Side Quests" #<repo name>
> <obsidian:// URL>
> ```
>
> Do not dump the handoff contents into the response — the point of parking is to get
> back to the main thread.
> ```

"Four lines, nothing more" is a stronger constraint than a template alone: it names the count and forbids expansion, so the model cannot rationalize adding a summary "to be helpful." The prohibition ("Do not dump the handoff contents") co-locates the most likely error with the step that would cause it.

### R30 — Use `${CLAUDE_PLUGIN_ROOT}` for paths

`hooks.json` references the awareness script via the plugin-root variable, not a hardcoded absolute path.

> Real quote from `plugins/tmux/hooks/hooks.json:7-12`:
>
> ```json
>     "SessionStart": [
>       {
>         "matcher": "*",
>         "hooks": [
>           {
>             "type": "command",
>             "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/tmux-awareness.sh",
>             "timeout": 10
>           }
> ```

The hook also sets `"timeout": 10`, limiting blast radius if the tmux probe stalls. This defensive default is not mandated by any rule but prevents hook latency from degrading every session start.

## Worth adopting

Pattern: **Negative trigger example**. Evidence: `plugins/essentials/agents/security-auditor.md:24-31` (the third `<example>` block labeled `NOT a trigger`). Why it would be a useful rule: agents with names adjacent to common verbs ("review", "check", "scan") accumulate false dispatches from requests that share surface words but differ in intent; a negative example trains the dispatch boundary with the same `<example>` mechanism already required by R09, requiring no new infrastructure.
