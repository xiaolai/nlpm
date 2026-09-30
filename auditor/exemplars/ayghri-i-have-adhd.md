---
slug: ayghri-i-have-adhd
repo: ayghri/i-have-adhd
audited: 2026-09-30
commit_sha: 839872f9d1cd634fed642b4589ce7226199cc15f
score: 97
exemplifies:
  - R01
  - R03
  - R04
  - R06
  - R08
---

# Exemplar: ayghri/i-have-adhd

**Score**: 97/100  |  **Date**: 2026-09-30  |  **Commit**: `839872f9d1cd634fed642b4589ce7226199cc15f`

A single output-style skill (143 lines) whose every rule is paired with a concrete Bad/Good example, and whose description packs the behavior, invocation command and off-switch into one line.

## Per-rule evidence

### R04 — Description as trigger

The description lists six concrete behaviors, then the explicit invocation (`/i-have-adhd`) and the explicit exit phrase. The skill also sets `disable-model-invocation: true`, so the description doubles as the user-facing trigger contract rather than a model-matching blurb.

> Real quote from `skills/i-have-adhd/SKILL.md:3-4`:
>
> ```
> description: 'Shape output for a reader with ADHD: lead with the next action, number multi-step work, restate state across turns, suppress tangents, give specific time estimates, make wins visible. Invoke with /i-have-adhd; stays on until "stop adhd mode".'
> disable-model-invocation: true
> ```

The description states both how to start and how to stop, so a reader of the frontmatter alone knows the skill's lifecycle.

### R08 — Concrete patterns over abstractions

Each of the ten rules follows the same shape: a one-line imperative, then a `Bad:` and a `Good:` pair. The model matches against the literal strings instead of interpreting an abstract principle.

> Real quote from `skills/i-have-adhd/SKILL.md:33-38`:
>
> ```
> ### 1. Lead with the next action
>
> The first line is something the reader can do. Not context. Not a plan. The action.
>
> Bad: "Let's think about this. Your auth flow has a few moving pieces..."
> Good: "Run `npm install jsonwebtoken`, then edit `src/auth.ts:42`."
> ```

The Good example contains a real command and a real `path:line`, not a placeholder like `<command>`.

### R06 — Runnable, real-syntax examples

Examples use real commands, file paths and error text instead of pseudocode. The numbered-list rule demonstrates the format in an actual fenced block.

> Real quote from `skills/i-have-adhd/SKILL.md:50-55`:
>
> ```
> Good:
> ```
> 1. Open `src/auth.ts`
> 2. Replace `verifyToken` (lines 42 to 58) with the snippet below
> 3. Run `npm test -- auth.spec.ts`
> ```
> ```

The error-tone rule does the same with a complete failure message (`expected 200, got 401`), so the pattern to copy is exact.

### R01 — No vague quantifiers (the skill applies it to itself, mostly)

The skill's Rule 6 bans vague estimates and gives replacement units. Rules 2 and 3 use hard bounds rather than "a few" or "short".

> Real quote from `skills/i-have-adhd/SKILL.md:82-87`:
>
> ```
> ### 6. Give specific time estimates
>
> Vague estimates fail. Ballpark in concrete units.
>
> Bad: "This will take some work."
> Good: "About 15 minutes if tests already cover this. An afternoon if not."
> ```

Numeric bounds recur: "under two minutes" (line 59), "no more than five items per group" (line 105), "the last three turns" (line 125). The audit's only deduction (-6) was for "relevant" in Rule 9, so the skill is nearly clean on this rule but not fully.

### R03 — Positive framing with a bounded negative list

Where the skill must forbid phrases, it enumerates the literal strings and then states the positive replacement in the final line.

> Real quote from `skills/i-have-adhd/SKILL.md:109-117`:
>
> ```
> ### 10. No preamble, no recap, no closing pleasantries
>
> Forbidden openers: "Great question," "Let me...", "I'll...", "Sure!", "Looking at your...", "To answer your question..."
>
> Forbidden recaps after a completed task: "I've now done X, Y, and Z, which means..."
>
> Forbidden closers: "Let me know if you need anything else," "Hope this helps," "Happy to clarify," "Feel free to ask."
>
> Start with the answer. End when the answer is done.
> ```

The prohibitions are closed lists of exact strings, and the section ends on two positive instructions, which limits the pink-elephant effect.

## Worth adopting

Pattern: Explicit rule-conflict precedence. Evidence: `skills/i-have-adhd/SKILL.md:127-128`. Why it would be a useful rule: a style skill that states which side wins when a rule collides with the task or the host harness ("the constraint wins, the shape stays") prevents the model from silently dropping either.

> ```
> 5. A rule fights the task. When a rule would delete the answer itself, the task wins; the shape stays.
> 6. A rule fights the harness. Inside an agent harness, the system prompt outranks this skill
> ```

Pattern: Persistent-mode scope statement with a literal off-switch. Evidence: `skills/i-have-adhd/SKILL.md:17-19`. Why it would be a useful rule: skills that change behavior for a whole session should name the exact phrases that end it, so persistence does not depend on the model's guess about when to stop.

> ```
> Turn them off only when the reader says "stop adhd mode" or "normal mode". Confirm in one line, then return to your default style.
> ```
