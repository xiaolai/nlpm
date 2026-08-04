---
name: vocab-drift
description: "Find vocabulary drift in a corpus without a declared registry — judgment-based clustering of likely-synonymous nouns and verbs. Advisory only, no penalty. Use for early-stage projects or as a periodic health check before/alongside R51."
argument-hint: "[path]"
allowed-tools: Read, Glob, Grep, Task
---

## User Input

```text
$ARGUMENTS
```

## Workflow

### Step 1: Parse target

| Input | Behavior |
|-------|----------|
| (empty) | Target = current working directory |
| absolute path | Target = that path |
| relative path | Target = `<cwd>/<path>` |

If the target does not exist or is not a directory → "Target path not found: {path}". Stop.

### Step 2: Discover artifacts

Use `commands/shared/discover.md` against the target path to collect all NL artifacts. Filter to Category A (plugin) and Category B (project config) — these are where vocabulary lives. Skip Category F (memory files) — they are user-specific and not part of the project's published surface.

If the discovery returns fewer than 5 artifacts → "Target has minimal NL surface ({N} artifacts). Vocabulary drift analysis is uninformative on small corpora; re-run when the corpus grows past 5 artifacts." Stop.

### Step 3: Dispatch the scanner

Invoke the `nlpm:vocab-drift-scanner` agent via the Task tool.

Pass the agent:

- The full list of artifact paths from Step 2
- The contents of every artifact (read with `Read` before dispatching)
- The path to `skills/*/vocabulary/registry.yaml` if one exists in the target (use `Glob` to find it). The scanner reads `cross_scope_homonyms.verbs` from this file to suppress false positives on already-declared homonyms.

If the artifact set is large (>30 files), batch into groups of ≤20 artifacts per scanner invocation. The agent's clustering algorithm scales linearly in the number of unique terms, not files, so batches can run in parallel via separate Task dispatches.

### Step 4: Merge results (if batched)

If multiple batches ran, merge findings:

- Two findings with overlapping term sets (≥1 shared term in the cluster) → merge into one finding. Sum occurrence counts; combine file lists; take the higher confidence.
- Re-rank the merged set by the criteria in the scanner's Step 5.
- Cap final output at 20 findings.

### Step 5: Report

Print the scanner's output verbatim. Then append a single line:

```
Run /nlpm:vocab-init to create a vocabulary skill, or edit your existing registry.yaml to incorporate the high-confidence pairs.
```

## Error Handling

| Condition | Response |
|-----------|----------|
| Target path doesn't exist | "Target path not found: {path}" |
| Fewer than 5 artifacts | Premature-message from Step 2 |
| Scanner agent fails on a batch | Continue with successful batches; note the failed batch's artifact count in the report header |
| All scanner batches fail | "Vocabulary drift scan failed across all batches. Re-run with a smaller scope or check the scanner agent's error output." |

## Notes

This command is **registry-free**. It works on projects that have never adopted R51 and produces advisory output only. To convert advisory findings into enforced penalties, the adopter must:

1. Run `/nlpm:vocab-init` to create a vocabulary skill (or edit an existing one)
2. Add the high-confidence drift pairs to `registry.yaml` as canonical+deprecated entries
3. Opt in to R51 via `.claude/nlpm.local.md`

See `docs/for-authors.md` for the full adoption flow.
