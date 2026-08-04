---
name: init
description: "Prepare NLPM for this project — detect artifacts, set strictness, capture baseline trend snapshot"
allowed-tools: Read, Write, Glob, Bash, AskUserQuestion, Task
---

## Workflow

### Step 1: Check Existing Config

Read `.claude/nlpm.local.md`. If exists, show current settings and ask: "Reconfigure? (yes/no)". If no → stop.

### Step 2: Scan

Run artifact discovery (same as /nlpm:ls) to show what's in the project.

### Step 3: Ask Strictness

```
AskUserQuestion:
  question: "What strictness level?"
  header: "Strictness"
  options:
    - label: "Relaxed"
      description: "Threshold 60 — only flag seriously broken artifacts"
    - label: "Standard (Recommended)"
      description: "Threshold 70 — flag artifacts that need improvement"
    - label: "Strict"
      description: "Threshold 80 — flag anything below good quality"
```

### Step 4: Write Config

Create `.claude/` directory if needed. Write `.claude/nlpm.local.md`:

```markdown
---
# NLPM Configuration
strictness: {chosen}
score_threshold: {60|70|80}
---

# NLPM Settings

When scoring NL artifacts in this project, use **{strictness}** strictness.
Flag artifacts scoring below **{threshold}/100** for improvement.
```

### Step 5: Update .gitignore

Append the following to `.gitignore` (skip lines already present):

```
# nlpm generated artifacts
.claude/nlpm-history.json
```

### Step 6: Capture Baseline Snapshot

Score every NL artifact discovered in Step 2 so `/nlpm:trend` has a starting point.

1. Dispatch `nlpm:scorer` and `nlpm:vague-scanner` in parallel over the discovered artifacts (same dispatch pattern as `/nlpm:score`). The vague-scanner's counts override the scorer's heuristic detection.
2. Persist the result by following `commands/shared/append-history.md` with `scope: "full"` and `files_scored` equal to the artifact count.

If Step 2 found zero artifacts, skip this step — there is nothing to score and the partial declines to write empty snapshots.

### Step 7: Confirm

```
NLPM is ready for this project.
  Strictness: {standard}
  Threshold: {70}/100
  Artifacts found: {N}
  Baseline score: {overall}/100   (snapshot saved to .claude/nlpm-history.json)
  Config: .claude/nlpm.local.md

Run /nlpm:score to re-score later, or /nlpm:trend to compare against this baseline.
```

If Step 6 was skipped (zero artifacts), omit the "Baseline score" line and replace the final sentence with "No artifacts found yet — re-run /nlpm:init after adding artifacts to the project."

**Error handling:**
- No artifacts found → still create config, skip Step 6, note "No artifacts found yet"
- `.claude/` directory doesn't exist → create it
- Step 6 scorer dispatch fails → log a one-line warning, write config + .gitignore but no history, exit successfully (init's primary job is config)
