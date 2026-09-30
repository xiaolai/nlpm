---
description: "Shared partial: append a scoring snapshot to .claude/nlpm-history.json. Used by /nlpm:init, /nlpm:score, and /nlpm:trend so trend data accumulates without manual upkeep."
user-invocable: false
disable-model-invocation: true
---

# Append Scoring Snapshot to History

**Purpose:** Persist a scoring result to `.claude/nlpm-history.json` so `/nlpm:trend` has data to compare against.

**Input:** the scoring result the caller just produced (per-file scores + overall average), plus a scope marker.
**Output:** updated `.claude/nlpm-history.json` with one new snapshot appended.

## File Format

`.claude/nlpm-history.json` lives at the project root.

```json
{
  "snapshots": [
    {
      "timestamp": "2026-05-19T07:00:00Z",
      "overall": 85,
      "files": {
        "agents/scorer.md": { "score": 92, "type": "agent" },
        "commands/score.md": { "score": 95, "type": "command" }
      },
      "scope": "full",
      "files_scored": 23
    }
  ]
}
```

## Scope Field

Every snapshot MUST carry a `scope` string. `/nlpm:trend` filters by scope so the overall trend line stays apples-to-apples (a partial scan should not look like an overall score regression).

| Caller | `scope` value | Meaning |
|--------|--------------|---------|
| `/nlpm:init` (baseline) | `"full"` | First-run scan of the entire project |
| `/nlpm:score` (no args) | `"full"` | Full-repo scoring pass |
| `/nlpm:score <path>` | `"path:<path>"` | Path-bound scan, e.g. `"path:agents/"` |
| `/nlpm:score <single-file>` | `"path:<file>"` | Single-file scan, e.g. `"path:agents/scorer.md"` |
| `/nlpm:score --changed` | `"changed"` | Git-changed-files scan |
| `/nlpm:trend [path]` | inherit from the caller's scope decision above | `/nlpm:trend` dispatches its own scoring pass; the scope follows the same rules as `/nlpm:score` with the same args |

## Steps

1. **Compute overall.** If the caller scored N files, `overall` is the integer-rounded arithmetic mean of their scores. If `files_scored == 0`, skip the append entirely — empty snapshots add noise.

2. **Read existing history.** Try to read `.claude/nlpm-history.json`. If it doesn't exist or doesn't parse as JSON, treat as `{"snapshots": []}` (recoverable, not an error).

3. **Build the new snapshot.**

   ```json
   {
     "timestamp": "<ISO 8601 UTC, second precision, e.g. 2026-05-19T07:00:00Z>",
     "overall": <int>,
     "files": { "<path>": { "score": <int>, "type": "<artifact-type>" }, ... },
     "scope": "<see table above>",
     "files_scored": <int>
   }
   ```

4. **Deduplicate trivial repeats.** If the most recent snapshot in `snapshots` has the same `scope` AND the same per-file scores (compare the `files` map), do NOT append — just update the existing snapshot's `timestamp`. This keeps the history clean when a developer runs `/nlpm:score` multiple times without making changes.

5. **Append.** Add the snapshot to the end of the `snapshots` array.

6. **Write atomically.** Write the JSON to `.claude/nlpm-history.json.tmp` first, then rename to the final path. Use 2-space indentation, terminate with a newline.

7. **Create parent dirs.** If `.claude/` doesn't exist, create it (this matters when `/nlpm:init` runs the very first time).

## Failure Modes

- **History file is malformed JSON.** Treat as empty (`{"snapshots": []}`) and overwrite. Do not crash the caller. Log a one-line warning: `"nlpm-history.json was malformed; rebuilding from scratch."`.
- **Project is not writable.** Skip the append silently. The score result the user just saw is what matters; failing to persist trend data should not surface as an error.
- **`.claude/nlpm-history.json` is gitignored.** That's the intended state — `/nlpm:init` adds it to `.gitignore`. Do not bypass that to commit it.

## What This Partial Does NOT Do

- Score artifacts. The caller does the scoring first; this partial only persists.
- Compare against history. That's `/nlpm:trend`'s responsibility (which reads the file this partial writes).
- Display anything to the user. The caller renders the score result; this partial runs silently.
