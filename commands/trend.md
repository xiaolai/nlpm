---
name: trend
description: "Show quality score trends over time — track improvements, detect degradation"
argument-hint: "[path]"
allowed-tools: Read, Write, Glob, Task
---

## User Input

```text
$ARGUMENTS
```

## Workflow

### Step 1: Load History

Read `.claude/nlpm-history.json` from the project root.

- If it doesn't exist: this is the first run. Score everything in Step 2 and the snapshot saved in Step 4 becomes the baseline; Step 3's comparison is skipped (no prior data).
- If it exists but parses as malformed JSON: warn one line, treat as empty, continue.

### Step 2: Score Current State

Dispatch the `nlpm:scorer` and `nlpm:vague-scanner` agents in parallel to score all artifacts (or artifacts at the given path).

### Step 3: Compare Against History

Filter the loaded snapshots to **only those whose `scope` matches the current scope** — otherwise a path-bound trend would be compared against full-repo baselines and produce nonsense deltas. The scope is derived from the current invocation's arguments using the same mapping as `${CLAUDE_PLUGIN_ROOT}/commands/shared/append-history.md`.

For each artifact in the current score:
- Find its most recent entry in the filtered history
- Compute delta: current_score − historical_score
- Flag: improved (delta > 0), degraded (delta < 0), unchanged (delta == 0), new (no history)

If the filtered history is empty (first run for this scope), skip the delta computation and label every artifact `new`.

### Step 4: Save Snapshot

Persist this run by following `${CLAUDE_PLUGIN_ROOT}/commands/shared/append-history.md` with the scope determined in Step 3, the per-file scores from Step 2, and the file count. The partial handles file creation, deduplication, and atomic write.

### Step 5: Report

```markdown
NLPM Trend Report

Snapshot: 2026-03-28 (3rd snapshot, 2 previous)

File                              Score   Previous  Delta
--------------------------------------------------------------
agents/scorer.md                  95      92        +3 improved
agents/scanner.md                 90      90         0 unchanged
commands/score.md                 95      88        +7 improved
skills/nlpm/scoring/SKILL.md      85      85         0 unchanged
.claude/rules/testing.md          78      82        -4 degraded
commands/fix.md (NEW)             88      --        new

Overall: 88/100 (was 87, +1)

Degraded (needs attention):
  .claude/rules/testing.md  82 → 78 (-4)

Trend: 3 snapshots — 82 → 87 → 88 (improving)
```

### Error Handling

- No history file → first run: score all artifacts, create history file, show baseline (no comparison available)
- Path doesn't exist → error with message
- History file malformed → warn, start fresh history
