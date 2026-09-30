---
slug: phuryn-pm-skills
repo: phuryn/pm-skills
audited: 2026-09-30
commit_sha: 18468a95b427e70e258b51389796367c6f684e7d
score: 92
exemplifies:
  - R01
  - R04
  - R05
  - R06
  - R07
  - R15
  - R16
---

# Exemplar: phuryn/pm-skills

**Score**: 92/100  |  **Date**: 2026-09-30  |  **Commit**: `18468a95b427e70e258b51389796367c6f684e7d`

A 9-plugin product-management collection (42 commands, 68 skills) whose best artifacts pair trigger-rich descriptions with concrete transformation examples and fixed output templates; 9 of the 100 audited files scored 100.

## Per-rule evidence

### R04 — Description as trigger

`release-notes` names the artifact it produces, then lists four user-phrased triggers after "Use when". Each trigger matches something a user would actually type.

> Real quote from `pm-execution/skills/release-notes/SKILL.md:3`:
>
> ```
> description: "Generate user-facing release notes from tickets, PRDs, or changelogs. Creates clear, engaging summaries organized by category (new features, improvements, fixes). Use when writing release notes, creating changelogs, announcing product updates, or summarizing what shipped."
> ```

The trigger list is action phrases ("writing release notes", "announcing product updates") rather than a restatement of the skill's summary.

### R05 — Body length

Skills are short. The three 100-scoring skills audited here run 42, 63 and 53 lines, against the 500-line limit, and each holds one task.

> Real quote from `pm-ai-shipping/skills/intended-vs-implemented/SKILL.md:18-20`:
>
> ```
> ## Method
>
> 1. **Establish intent.** Read the `documentation/*.md` set as the source of truth for what *should* be true: who may access what, which boundaries are trusted, which data is public. Treat the docs as claims to verify, not as proof.
> ```

A five-step method, a "What counts" list and a "Notes" list fit in 42 lines because each step states the action and the evidence required, with no background theory.

### R06 — Concrete examples

`release-notes` shows before/after pairs in the exact register it wants, instead of describing the register.

> Real quote from `pm-execution/skills/release-notes/SKILL.md:36-41`:
>
> ```
>    **Example transformations**:
>    - Technical: "Implemented Redis caching layer for dashboard API endpoints"
>    - User-facing: "Dashboards now load up to 3× faster, so you spend less time waiting and more time analyzing."
>
>    - Technical: "Fixed race condition in concurrent checkout flow"
>    - User-facing: "Fixed an issue where some orders could fail during high-traffic periods."
> ```

Two pairs with different change types (performance, bug fix) let the model infer the pattern. The skills the audit flagged for R06 (for example `gtm-motions`, `create-prd`) lack exactly this.

### R07 — Scope note when related skills exist

`intended-vs-implemented` states its dependency on `shipping-artifacts` and its boundary with the audit commands that overlap it.

> Real quote from `pm-ai-shipping/skills/intended-vs-implemented/SKILL.md:12` and `:40`:
>
> ```
> It is the differentiator: it only works when intent has been written down first (see the **shipping-artifacts** skill), and that's exactly why commodity tools can't replicate it.
> ...
> - This method feeds the security and performance audits; it does not replace their sink-level analysis — it adds the intent axis they lack.
> ```

It says what the skill covers, which sibling to read first and what it does not replace. The audit found the reverse pointer missing in `shipping-artifacts`, so this is a one-directional example.

### R15 — Handle empty input

`/security-audit-static` defines the blank-argument case with a default scope and a prioritised target list.

> Real quote from `pm-ai-shipping/commands/security-audit-static.md:27`:
>
> ```
> Audit **$ARGUMENTS**. If empty, audit the whole repository, prioritizing request handlers, auth, data access, background jobs, and anything that renders, fetches, executes, logs, or stores user-controlled data.
> ```

The default is a behavior, not an error message. Its `argument-hint` (`"<repo path or area; defaults to the whole repository>"`, line 3) repeats it in frontmatter.

### R16 — Define output format

`summarize-interview` gives a literal template with a placeholder per field, and one filled example for the least obvious field.

> Real quote from `pm-product-discovery/skills/summarize-interview/SKILL.md:26-43`:
>
> ```
> **Date**: [Date and time of the interview]
> **Participants**: [Full names and roles]
> **Background**: [Background information about the customer]
>
> **Current Solution**: [What solution they currently use]
> ...
> **Action Items**:
> - [Date, Owner, Action — e.g., "2025-01-15, Paweł Huryn, Follow up with customer about pricing"]
> ```

It also defines the missing-data rule in the step above ("Use "-" if information is unavailable"), so the template keeps its shape on sparse transcripts.

### R01 — No vague quantifiers

Where the audit-static command needs a threshold, it gives numbers.

> Real quote from `pm-ai-shipping/commands/security-audit-static.md:29`:
>
> ```
> When the scope exceeds roughly 30 files or 5,000 lines, fan out with parallel subagents — one per module/feature cluster, each running the mapping and inspection (steps 1–3) on its slice and reading that slice in full.
> ```

"Roughly" softens the bound, but the trigger is still 30 files or 5,000 lines, and the subagent return shape follows as a named-field record. Most R01 hits elsewhere in the repo are single words ("relevant", "correctly") in otherwise specific prose.

## Worth adopting

Pattern: Untrusted-input declaration in audit artifacts. Evidence: `pm-ai-shipping/commands/security-audit-static.md:13` and `pm-ai-shipping/skills/intended-vs-implemented/SKILL.md:42`. Why it would be a useful rule: a command or skill that reads third-party code or docs should say to treat that content as data and to report steering attempts as findings, which closes the prompt-injection path for the artifact class.

Pattern: Least-privilege `allowed-tools` with path-scoped writes. Evidence: `pm-ai-shipping/commands/security-audit-static.md:4` (`Bash(git log:*), Bash(git diff:*), Bash(git show:*), Write(reports/**)`). Why it would be a useful rule: a command that writes output should scope `Write` to one directory and `Bash` to read-only subcommands; the repo's other 38 commands omit the field.
