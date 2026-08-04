---
name: spec-sync
description: "Sync nlpm's convention overlays with the latest official Claude Code / Codex / Antigravity specs — research upstream docs, diff, apply corrections, propagate, check"
argument-hint: "[claude|codex|antigravity|all]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

## User Input

```text
$ARGUMENTS
```

## Workflow

A pipeline that keeps nlpm's tool overlays current with the upstream specs they document. The web research fans out to `spec-researcher` agents (one per tool, in parallel); the high-judgment editing stays here in the reviewable main thread.

This command **never commits, pushes, or touches the marketplace.** It edits overlay skills and reports the remaining release steps.

### Step 1: Parse target

| Input | Overlays to sync |
|-------|------------------|
| (empty) or `all` | all three |
| `claude` | `skills/nlpm/conventions-claude/SKILL.md` |
| `codex` | `skills/nlpm/conventions-codex/SKILL.md` |
| `antigravity` | `skills/nlpm/conventions-antigravity/SKILL.md` |

Resolve today's date with `date +%Y-%m-%d` (passed to the agents and used for the "Refreshed" note). Confirm each selected overlay file exists; if one is missing, report "Overlay not found: {path}" and continue with the rest.

### Step 2: Research (parallel)

Dispatch one `spec-researcher` agent **per selected overlay, all in a single message** so they run concurrently. Pass each agent:

- the **tool** name (`claude` / `codex` / `antigravity`)
- the **overlay path** and its full current content
- **today's date**

Each agent fetches the overlay's declared authoritative sources (plus the docs index and, for Codex, GitHub releases), diffs them, and returns a structured gap report tagged `[FIX | REMOVE | ADD | CONFIRM | RESOLVED]` with a confidence section.

Collect every report. If an agent returns nothing, note "Research failed for {tool} — re-run /nlpm:spec-sync {tool}" and continue.

### Step 3: Present the diagnosis

Show the consolidated gap report, grouped by tool, **corrections first** (`FIX` / `REMOVE` / `RESOLVED`), then additive (`ADD`), then a confidence summary. This is the human-reviewable diff before any file changes.

### Step 4: Apply corrections

For each overlay, edit the SKILL.md to absorb its report:

- **Apply** every `FIX`, `REMOVE`, `RESOLVED+` (uncertainty resolved — the thing exists), and `RESOLVED-` (uncertainty resolved — the thing is *confirmed removed/absent* against a first-party source) finding, plus every `ADD` the agent rated structural (high-confidence).
- **Defer, do not guess:** skip anything in the agent's confidence notes — `verify-tag` (a version/date specific that needs pinning) and `not-found` (a claim the agent could *not* confirm against any source). Note the distinction from `RESOLVED-`: a `RESOLVED-` is a *confirmed* absence and gets applied; a bare `not-found` is *unconfirmed* and gets deferred. List deferred items in the final report rather than writing an unverified fact into the overlay.
- When correcting a fact, leave a brief inline note of what the old value was and the refresh date (matches the existing overlay style, e.g. "`magenta` is NOT valid (old list had it; corrected {date})") — this keeps the overlay self-documenting and prevents a future pass from regressing it.
- Refresh the overlay frontmatter: bump `version:` (**patch** if corrections-only, **minor** if additive sections were added) and update the "Refreshed {date}" clause in `description:`.

**Antigravity caveat:** that overlay is advisory-only against an unsettled spec. Apply only changes the agent confirmed against a first-party source; when sources disagree or the spec is still settling, report the finding instead of editing.

### Step 5: Propagate for self-consistency

A correction to an overlay can invalidate nlpm's *own* artifacts (e.g. an agent using a now-removed color or tool name). For each `FIX`/`REMOVE` that changed an enum value, field name, or tool name, grep the rest of the repo for the old value with a **fixed-string** search — old values like `[profiles.*]`, `Task(...)`, or `color: magenta` contain regex metacharacters and would misbehave under `grep -E`:

```
grep -rnF -- "<old-value>" agents/ commands/ skills/ hooks/ scripts/
```

Exclude the overlay's intentional corrective text from the hits. For each real hit in a working artifact, fix it to a valid current value (or flag it if the right replacement needs a human call). Report these as "self-consistency fixes" — this is the step that catches nlpm contradicting its own refreshed spec.

### Step 6: Check

1. Run `python3 bin/nlpm-check <repo-root>` — must report clean.
2. For each removed/renamed term, grep to confirm no stale occurrence survives outside intentional corrective notes.
3. If `bin/nlpm-check` is unavailable, say so and fall back to the grep checks only.

Report any failure with the exact output; do not claim success on a failed check.

### Step 7: Report

```markdown
NLPM Spec-Sync Report — {date}

Overlays synced: {list}

Per overlay:
  conventions-{tool}  v{old} → v{new}
    Corrections applied: {N}   (FIX {a}, REMOVE {b}, RESOLVED {c})
    Additive applied:    {N}
    Deferred:            {N}   (verify-tag / not-found — listed below)

Self-consistency fixes:
  {file}:{line} — {old} → {new}        (or "none")

Verification:
  nlpm-check: {clean | FAILED — output}
  stale-term grep: {clean | hits listed}

Deferred (need a human / verbatim source before adopting):
  [{tool}] {finding} — {why deferred}

Remaining release steps (NOT done by this command):
  - Bump plugin.json + marketplace.json versions
  - Run /nlpm:score, /nlpm:check, /nlpm:test
  - Commit and push, then update the central marketplace
```

**Error handling:**
- No overlays drifted → "All overlays already current. Nothing to apply."
- Overlay file not writable → skip that overlay with a warning; still report its diagnosis.
- A `spec-researcher` returns a malformed report → present what it returned and skip auto-apply for that tool (report-only).
