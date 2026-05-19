---
name: report
description: "Render a self-contained HTML report — per-file scores, score trend, cross-component graph, vocabulary noun-verb map, drift candidates, and findings — into .claude/nlpm-reports/. Opens directly via file://. No server, no build, no network."
argument-hint: "[path]"
allowed-tools: Read, Write, Glob, Grep, Bash, Task
---

## User Input

```text
$ARGUMENTS
```

## Workflow

### Step 1: Resolve target

| Input | Behavior |
|-------|----------|
| (empty) | Target = current working directory |
| absolute path | Target = that path |
| relative path | Target = `<cwd>/<path>` |

If the target does not exist or is not a directory → "Target path not found: {path}". Stop.

Set `out_dir = <target>/.claude/nlpm-reports/`.

### Step 2: Read config

Read `<target>/.claude/nlpm.local.md` if it exists. Extract:

- `score_threshold` (default 70)
- `strictness` (default "standard")
- `rule_overrides.R51.enabled` (default false)
- `rule_overrides.R51.vocabulary_skill` (default empty)

These feed the report header and gate which panels are rendered.

### Step 3: Read history

Read `<target>/.claude/nlpm-history.json` if it exists. Each snapshot has `timestamp` and `average_score`. Keep all snapshots for the trend panel; the most recent one is the headline.

If the file is missing or has zero snapshots → emit the report with the trend panel showing "no history" rather than aborting.

### Step 4: Score artifacts (fresh)

Discover artifacts via `commands/shared/discover.md` against the target. Then dispatch the `nlpm:scorer` and `nlpm:vague-scanner` agents in parallel (same pattern as `/nlpm:score`). Collect per-file scores and findings.

If the corpus has more than 50 artifacts, batch into groups of 25 per dispatch.

### Step 5: Cross-component check (fresh)

Dispatch the `nlpm:checker` agent against the target. Capture:

- Reference graph (artifacts and their references; mark broken ones)
- Orphans
- Contradictions
- Terminology drift (the checker's existing finding type)
- R51 vocabulary drift findings if R51 is enabled

### Step 6: Vocabulary data (read registry if present)

If the config from Step 2 declares a `vocabulary_skill` path, read `<target>/<vocabulary_skill>/registry.yaml`. Extract:

- `scopes` (list of declared scopes)
- `verbs` per scope: canonical name, deprecated synonyms, output, judgment flag
- `nouns` (artifact_class, output_class, role_nouns, etc.)
- `cross_scope_homonyms.verbs`
- `deferred_pending_warrant` and `rejected_by_higher_principle`

Build verb→noun edges by walking each verb's `output` field — if the output references a noun by id, emit a `produces` edge. If the output is freeform text, skip the edge (don't fabricate).

If no `vocabulary_skill` is configured, look for `<target>/skills/*/vocabulary/registry.yaml` and use the first match. If none found, omit the vocabulary panel.

### Step 7: Vocab drift (fresh, if applicable)

If a vocabulary skill is configured **and** the corpus has at least 5 NL artifacts, dispatch the `nlpm:vocab-drift-scanner` agent (registry-free; reads existing `cross_scope_homonyms` to suppress false positives). Capture the JSONL records.

If fewer than 5 artifacts, skip vocab drift; the panel will render "corpus too small for drift analysis."

### Step 8: Assemble data blob

Build a single JSON object with this shape (omit any panel's data when absent):

```json
{
  "project": "<plugin-name-from-plugin.json-or-dir-basename>",
  "generated_at": "<ISO 8601 UTC>",
  "score_threshold": 70,
  "r51_enabled": false,
  "summary": {
    "total_files": 22,
    "average_score": 95,
    "pass_count": 22,
    "fail_count": 0
  },
  "files": [{"path": "...", "type": "...", "score": 95, "findings": [...]}],
  "history": [{"timestamp": "...", "average_score": 92}],
  "cross_component": {
    "nodes": [{"id": "...", "label": "...", "type": "artifact|manifest", "broken": false}],
    "edges": [{"source": "...", "target": "...", "broken": false}]
  },
  "vocabulary": {
    "scopes": [{"id": "internal", "label": "Internal"}],
    "verbs": [{"id": "score", "scope": "internal", "deprecated": ["analyze"], "judgment": false, "output": "number+penalty"}],
    "nouns": [{"id": "artifact", "class": "artifact_class", "definition": "..."}],
    "edges": [{"source": "score", "target": "finding", "type": "produces"}],
    "cross_scope_homonyms": ["scan", "test", "discover"],
    "deferred": [{"verb": "triage", "scope": "internal", "needed_warrant": "user warrant"}]
  },
  "vocab_drift": {
    "candidates": [{"terms": ["scanner", "analyzer"], "confidence": "high", "disposition": "drift", "suggested_canonical": "scanner", "files_affected": 3, "evidence": "..."}]
  },
  "findings": [{"rule": "R09", "severity": "low", "file": "agents/x.md", "line": 12, "message": "..."}]
}
```

Write this to `/tmp/nlpm-report-data.json`.

### Step 9: Render

Invoke the renderer via Bash:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/bin/nlpm-report \
  --data /tmp/nlpm-report-data.json \
  --project <plugin-name> \
  --out <target>/.claude/nlpm-reports/
```

If `CLAUDE_PLUGIN_ROOT` is unset, fall back to `~/.claude/plugins/cache/xiaolai/nlpm/*/bin/nlpm-report` (use `Glob`).

### Step 10: Report

```
NLPM HTML Report

  Project: {name}
  Score:   {avg}/100 ({pass}/{total} files pass, threshold {threshold})
  Trend:   {N} snapshots
  Vocab:   {V} verbs, {N} nouns, {D} drift candidates
  Findings: {F} total, {high} high-severity

  Report:  {target}/.claude/nlpm-reports/index.html
  Archive: {target}/.claude/nlpm-reports/<timestamp>.html

  Open with: open '{target}/.claude/nlpm-reports/index.html'
```

## Error Handling

| Condition | Response |
|-----------|----------|
| Target path doesn't exist | "Target path not found: {path}" |
| No NL artifacts in target | "No NL artifacts found at {path}; nothing to report." |
| `bin/nlpm-report` not findable | "Could not locate nlpm-report binary. Set CLAUDE_PLUGIN_ROOT or install NLPM at user scope." |
| Scorer agent fails on a batch | Report the failure inline in the HTML's findings section; do not abort the entire report |
| `.claude/nlpm-history.json` is corrupt JSON | Render trend panel as "history file corrupted at {path}"; continue with the rest of the report |

## Notes

- The report is fully self-contained — the renderer copies G6 (vendored at `templates/report/vendor/g6.min.js`) and the report assets into the output directory. No network access at view time.
- Timestamped archives accumulate under `.claude/nlpm-reports/<timestamp>.html`. The `index.html` always points to the most recent render.
- For the auditor pipeline's cross-repo aggregate dashboard, see `/nlpm:report --dashboard` (TODO) or the workflow `.github/workflows/auditor-render-dashboard.yml`.
