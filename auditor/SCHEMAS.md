# Auditor Data Schemas

The auditor pipeline emits structured, append-only logs so NLPM can learn from history. This document is the single source of truth for every log format the workflows produce.

## Files

| Path | Append-only | Written by | Purpose |
|------|-------------|------------|---------|
| `auditor/findings.jsonl` | yes | `auditor-audit.yml` | One record per audit finding (bug, quality, security, cross-component) |
| `auditor/disagreements.jsonl` | yes | `auditor-track.yml`, `auditor-suppressions.yml`, `auditor-audit.yml` | Evidence that a finding was wrong, contested, or unwelcome |
| `auditor/logs/events.jsonl` | yes | all workflows via `log-event.sh` | Workflow lifecycle events plus aggregated outcome events |
| `auditor/audits/<slug>.md` | no (rewritten per audit) | `auditor-audit.yml` | Human-readable audit report |
| `auditor/audits/<slug>.findings.jsonl` | no (rewritten per audit) | `auditor-audit.yml` | Per-audit findings sidecar, source for global `findings.jsonl` |
| `auditor/feedback/log.json` | no (rebuilt) | daily report | Rolling summary, derived from the three append-only logs |
| `auditor/registry/repos.json` | no (mutated in place) | multiple workflows | Tracking database for repos and PRs |

Append-only means: new records are only added. Fixing a record means appending a superseding event (e.g., `finding_amended`), never editing the original.

## `findings.jsonl` — one record per finding

Every audit appends one line per finding to `auditor/findings.jsonl`. The audit first writes a per-audit sidecar (`auditor/audits/<slug>.findings.jsonl`) with the bare finding fields; a post-step enriches each line with workflow metadata and appends to the global log.

### Record schema

```json
{
  "event": "finding",
  "timestamp": "2026-04-17T12:00:00Z",
  "audit_run_id": "24564889725",
  "repo": "owner/name",
  "commit_sha": "abc123def456...",
  "fingerprint": "sha256:a3f9c2b1...",
  "category": "security",
  "rule_id": "SEC-new-function-eval",
  "file": "scripts/build.js",
  "line": 122,
  "severity": "high",
  "penalty": null,
  "pattern": "new-Function(dynamic-string)",
  "description": "Regex-extracts ANTIPATTERNS array, evaluates via new Function().",
  "false_positive": false,
  "suggested_fix": "Replace with ESM import (ANTIPATTERNS already exported)"
}
```

### Field reference

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `event` | string | yes | Always `"finding"` for this log |
| `timestamp` | ISO 8601 UTC | yes | Set by post-step, not by Claude |
| `audit_run_id` | string | yes | `GITHUB_RUN_ID` or `"local"` |
| `repo` | string | yes | `owner/name` |
| `commit_sha` | string | yes | Full SHA of target repo's HEAD at audit time; `"unknown"` if clone didn't include `.git` |
| `fingerprint` | string | yes | `sha256:<hex>` of `repo + file + rule_id + pattern + line` |
| `category` | enum | yes | One of `nl_quality`, `security`, `bug`, `cross_component` |
| `rule_id` | string | yes | See rule_id conventions below; use `"UNCLASSIFIED"` only when no rule applies |
| `file` | string | yes | Path relative to target repo root |
| `line` | int \| null | yes | `null` for file-level or cross-component findings |
| `severity` | enum | yes | One of `critical`, `high`, `medium`, `low`, `info` |
| `penalty` | int \| null | yes | Negative integer for `nl_quality` findings; `null` otherwise |
| `pattern` | string | yes | Short machine-friendly id (e.g., `new-Function-eval`, `missing-frontmatter`) |
| `description` | string | yes | One-line human summary, no newlines |
| `false_positive` | bool | yes | `true` if the auditor itself decided the finding is invalid; default `false` |
| `suggested_fix` | string | yes | One-line fix hint, empty string if none |
| `fp_reason` | string | when `false_positive: true` | One-line explanation of why the finding is invalid in this context |
| `rule_gap` | string | when `false_positive: true` | One-line hint at what the rule should account for to avoid this misfire |

### `rule_id` namespace conventions

- `R01`–`R50`: NL rules from `skills/nlpm/rules/`
- `SEC-<pattern-slug>`: security patterns (e.g., `SEC-curl-pipe-sh`, `SEC-new-function-eval`, `SEC-shell-true`, `SEC-postinstall-script`)
- `BUG-<kind>`: NL artifact bugs (e.g., `BUG-missing-frontmatter`, `BUG-broken-reference`, `BUG-undeclared-tool`, `BUG-invalid-semver`)
- `CC-<kind>`: cross-component issues (e.g., `CC-stale-count`, `CC-broken-relative-path`, `CC-terminology-drift`, `CC-orphan-component`)
- `UNCLASSIFIED`: used sparingly, surfaces as a rule-gap signal in reports

New IDs may be introduced without a schema change, but should be documented in the rules skill when they recur.

### `fingerprint` computation

```
fingerprint = "sha256:" + sha256(repo + "|" + file + "|" + rule_id + "|" + pattern + "|" + line)
```

The fingerprint is deliberately stable across re-audits of the same file (same repo, same rule, same pattern, same line). It is the join key that connects findings to PR outcomes and to disagreements.

If the line shifts but the finding is otherwise identical, the fingerprint changes. This is intentional: line-shift fingerprint churn is tolerable, and false-matches across moved code is worse.

### `false_positive` semantics

Set `true` only when the auditor, during the same audit run, validates that the rule misfired. Typical cause: a rule's precondition is violated by a file the rule doesn't know about (e.g., `SEC-unpinned-semver` firing when a `bun.lock` exists). When `false_positive: true`, the record must also carry `fp_reason` (why it's invalid) and `rule_gap` (what the rule missed). These records automatically trigger a `self_false_positive` event in `disagreements.jsonl` via the aggregation step.

Later external corrections (maintainer pushback, PR rejection) do **not** flip this field. Instead, a separate `disagreements.jsonl` event is appended, and the joining query handles the cross-reference.

## `disagreements.jsonl` — evidence the finding was wrong

Four event types share one file. Every record includes `event`, `timestamp`, and one or more of `fingerprint` / `fingerprints` / `rule_id` so the learning agent can join back to findings.

### Event: `self_false_positive`

Emitted during audit aggregation when a finding line has `false_positive: true`.

```json
{
  "event": "self_false_positive",
  "timestamp": "2026-04-10T12:00:00Z",
  "repo": "owner/name",
  "fingerprint": "sha256:c1d2e3f4...",
  "rule_id": "SEC-unpinned-semver",
  "reason": "bun.lock pins versions; rule presumed npm/yarn-only",
  "rule_gap": "rule doesn't account for alternative lockfile formats"
}
```

`rule_gap` is the learning payload — one sentence naming what the rule missed.

### Event: `pr_comments_snapshot`

Emitted by `auditor-track.yml` on the transition into `closed_unmerged` state. Captures the full comment thread at the moment of rejection — a future classifier workflow reads these snapshots and emits classified `maintainer_rejected` / `maintainer_pushback` events. Decoupling raw capture from classification means comment text is preserved even if GitHub comments are later edited or deleted.

```json
{
  "event": "pr_comments_snapshot",
  "timestamp": "2026-04-14T08:31:00Z",
  "pr": "owner/repo#123",
  "pr_state": "closed_unmerged",
  "comments_hash": "sha256:...",
  "fingerprints": ["sha256:..."],
  "rule_ids": ["R27"],
  "comments": [...]
}
```

`comments` is the raw array from `gh pr view --json comments`. `comments_hash` is `sha256` of the serialized comments array — used for dedup if the classifier re-runs.

### Event: `maintainer_rejected`

Emitted by a future classifier workflow (not yet shipped) when it consumes a `pr_comments_snapshot` and determines the comments indicate genuine dissent. Classification is done by a Haiku call over the comment thread; results are cached by `comments_hash` so unchanged threads don't re-classify.

```json
{
  "event": "maintainer_rejected",
  "timestamp": "2026-04-14T08:31:00Z",
  "pr": "owner/repo#123",
  "fingerprints": ["sha256:..."],
  "rule_ids": ["R27"],
  "dissent_type": "intentional_pattern",
  "quote": "We use eval() here because the input is a compile-time constant enum.",
  "commenter_role": "maintainer",
  "classifier_model": "haiku-4-5",
  "classifier_confidence": "high"
}
```

`dissent_type` ∈ `{intentional_pattern, out_of_scope, style_disagreement, context_missed, rule_disputed}`. Each maps to a rule-refinement action category.

`commenter_role` ∈ `{maintainer, contributor, bot, unknown}`. Only `maintainer` carries high weight.

`classifier_confidence` ∈ `{high, medium, low}`. Low-confidence events are logged but weighted less in aggregation.

### Event: `maintainer_pushback`

Same shape as `maintainer_rejected`, emitted when a PR is still open or was merged despite objections to one or more findings. This is why PR metadata carries an **array** of fingerprints: per-finding attribution inside bundled PRs matters here.

### Event: `downstream_suppression`

Emitted weekly by `auditor-suppressions.yml` (new workflow). Scans public plugin repos for committed `nlpm.md` or `.claude/nlpm.md` with rule-override blocks.

```json
{
  "event": "downstream_suppression",
  "timestamp": "2026-04-20T00:00:00Z",
  "repo": "someone/their-plugin",
  "commit_sha": "def456...",
  "rule_id": "R14",
  "suppression_type": "suppress",
  "reason_given": "Rule R14 too strict for our DSL-style agents",
  "path": ".claude/nlpm.md"
}
```

`suppression_type` ∈ `{suppress, max_penalty, threshold_adjustment, rule_override}`. `reason_given` is optional — many suppressions carry no comment.

## `events.jsonl` — outcome events added to the existing log

`events.jsonl` already holds workflow lifecycle events. Three new event types are added.

### Event: `finding_outcome`

Emitted by `auditor-track.yml` on every PR state transition.

```json
{
  "timestamp": "2026-04-14T08:31:00Z",
  "workflow": "track",
  "event": "finding_outcome",
  "run_id": "...",
  "run_number": 0,
  "data": {
    "pr": "owner/repo#123",
    "pr_state": "merged",
    "fingerprints": ["sha256:..."],
    "rule_ids": ["SEC-new-function-eval"]
  }
}
```

`pr_state` ∈ `{merged, closed_unmerged, open, stale_90d}`. The `stale_90d` state is emitted once, when an open PR crosses 90 days with no activity.

### Event: `findings_aggregated`

Emitted by `auditor-audit.yml` after appending per-audit findings to the global log.

```json
{
  "data": {
    "repo": "owner/name",
    "findings": 12,
    "invalid_lines": 0
  }
}
```

Used for pipeline health monitoring — a sustained non-zero `invalid_lines` means Claude's JSONL emission is drifting.

### Event: `finding_amended`

Reserved for future use. Emitted when a prior finding record is retroactively invalidated (e.g., the rule was later deprecated). Always references a prior `fingerprint`. No current workflow emits this; it exists in the schema so tooling can handle it when introduced.

## PR metadata block

Every PR submitted by `auditor-contribute.yml` ends with a sentinel-bounded JSON block inside an HTML comment. The block is invisible to human reviewers on GitHub and trivially parseable by `auditor-track.yml`.

### Format

```markdown
(…normal PR body explaining the fix…)

<!-- nlpm-metadata-begin
{
  "version": 1,
  "findings": [
    {"rule_id": "SEC-new-function-eval", "fingerprint": "sha256:a3f9c2b1..."},
    {"rule_id": "SEC-new-function-eval", "fingerprint": "sha256:7b4d8e9f..."}
  ]
}
nlpm-metadata-end -->
```

### Parser contract

```
regex: (?s)<!-- nlpm-metadata-begin\s*(\{.*?\})\s*nlpm-metadata-end -->
```

The captured group must parse as JSON with exactly these top-level keys:

| Key | Type | Notes |
|-----|------|-------|
| `version` | int | Current: `1`. Future versions may extend the inner schema. |
| `findings` | array | One object per finding addressed by this PR |

Each `findings[i]` object:

| Key | Type | Notes |
|-----|------|-------|
| `rule_id` | string | Denormalized for convenience; fingerprint is authoritative |
| `fingerprint` | string | `sha256:<hex>`, joins to `findings.jsonl` |

The block must be the last thing in the PR body so maintainers editing the body above it don't accidentally break the sentinel match.

### Why HTML-comment + sentinel

- **Invisible to maintainers**: the block carries no information maintainers care about and shouldn't clutter PR history.
- **Sentinel-bounded**: standard HTML comment closing can appear in prose (rare, but possible); the `nlpm-metadata-begin` / `nlpm-metadata-end` sentinels make the regex unambiguous.
- **JSON inside**: tolerates the schema evolving under `version`; no custom grammar.

## Learning query

The core query a rule-refinement agent runs:

```
findings.jsonl
  ⋈ events.jsonl (where event = finding_outcome)  on fingerprint
  ⋈ disagreements.jsonl                           on fingerprint
GROUP BY rule_id
```

Derived per-rule metrics:

| Metric | Source | Signal |
|--------|--------|--------|
| `hits / repos_audited` | findings | Reach |
| `merged / contributed` | findings ⋈ outcomes | Precision (our judgment) |
| `self_fp / hits` | disagreements:self | Precision (our known errors) |
| `maintainer_rejected / contributed` | disagreements:maintainer | Precision (external) |
| `downstream_suppression / deployments` | disagreements:downstream | Community disagreement |
| median `dissent_type` | disagreements:maintainer | How the rule fails, not just that it fails |

Rules cluster into four states on these metrics:

- **healthy** — high reach, high precision, low disagreement → keep as-is
- **noisy** — high reach, low precision → refine trigger or add exceptions
- **dormant** — zero hits across many audits → delete or re-scope
- **disputed** — high reach, high disagreement → revisit the underlying principle

## Versioning

This schema is the contract between workflows and learning tooling. Changes follow these rules:

- **Additive changes** (new optional field, new event type, new enum variant) — no version bump, document the addition here.
- **Breaking changes** (rename/remove a field, change a type) — bump `version` in the PR metadata block. For JSONL logs, write a one-shot migration script that rewrites historical records to the new shape; don't leave mixed schemas in the same file.
- **Deprecations** — mark the field as deprecated in this doc; keep emitting it for at least 30 days after downstream consumers stop reading it.

The goal: a researcher six months from now can pick up any of these logs and interpret every record without context from outside this file.
