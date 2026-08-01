---
name: score
description: "Score NL programming artifacts — 100-point quality score per file"
argument-hint: "[path]"
allowed-tools: Read, Write, Glob, Grep, Bash, Task
---

## User Input

```text
$ARGUMENTS
```

## Workflow

### Step 1: Load Config

Read `.claude/nlpm.local.md` if it exists. Extract `score_threshold` (default: 70).

### Step 2: Parse Arguments

| Input | Behavior |
|-------|----------|
| (empty) | Score all Category A+B artifacts in cwd |
| directory path | Score all artifacts under that directory |
| file path | Score that single file |
| --changed | Score only files changed since last commit (uses `git diff --name-only HEAD`) |

If `--changed` is present: run `git diff --name-only HEAD` to get changed files, then filter through `commands/shared/classify.md` to keep only NL artifacts. Skip the full discovery step.

### Step 3: Discover Artifacts

If path is a directory: use `commands/shared/discover.md` to find all NL artifacts.
If path is a file: use `commands/shared/classify.md` to determine its type.

If no artifacts found → "No NL programming artifacts found."

### Step 4: Score Artifacts

Dispatch two agents in parallel for each batch of up to 5 artifacts:

1. **`nlpm:scorer`** -- scores each artifact on the 100-point rubric (penalties, structure, heuristics)
2. **`nlpm:vague-scanner`** -- counts vague quantifier words mechanically (fast, haiku)

The scorer incorporates the vague-scanner's word counts into its penalty calculation. If the vague-scanner reports counts that differ from the scorer's own detection, use the vague-scanner's counts (deterministic grep is more reliable than heuristic detection for word counting).

Pass to both agents:
- The artifact contents (read each file)
- The artifact types (from classify.md)
- Any rule overrides from the config (if `rule_overrides` is present in `.claude/nlpm.local.md`)

Collect results: per-artifact score + finding list.

### Step 5: Report

```markdown
NLPM Score Report

File                              Type      Score   Findings
───────────────────────────────────────────────────────────
{for each file}

Overall: {avg_score}/100 — {EXCELLENT|GOOD|ADEQUATE|WEAK|REWRITE}    [threshold: {score_threshold}]
  High: {N} | Medium: {N} | Low: {N}
  Below threshold: {N} files

Top findings:
  1. [{SEVERITY}] {file}:{line} — {finding} ({penalty})
  2. ...

Score guide: 90+ Excellent | 80-89 Good | 70-79 Adequate | 60-69 Weak | <60 Rewrite
```

**Error handling:**
- File unreadable → skip with warning: "Skipped {path}: unreadable"
- Malformed YAML frontmatter → score penalty -25, continue scoring on body
- Empty file → score 0, finding: "Empty file"

### Step 6: Append Snapshot to History

Persist this scoring run so `/nlpm:trend` has data to compare against. Follow `commands/shared/append-history.md` with:

- `files`: the per-file scores from Step 4 (one entry per scored artifact, with score + type)
- `files_scored`: the count
- `scope`: derived from Step 2's parsed arguments —
  - empty arguments → `"full"`
  - directory path → `"path:<directory>/"` (trailing slash)
  - single file path → `"path:<file>"`
  - `--changed` → `"changed"`

The partial handles file creation, deduplication of trivial repeats, and atomic write. Silent failure on write (e.g., read-only project) is acceptable — the score report the user just saw is the primary output; persistence is best-effort telemetry.

If Step 4 scored zero artifacts (no NL artifacts found), skip this step.
