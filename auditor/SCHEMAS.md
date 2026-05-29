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
| `auditor/audits/<slug>.re-audit.md` | no (rewritten per re-audit) | `auditor-case-study.yml` | Post-merge re-scoring report at target HEAD |
| `auditor/audits/<slug>.re-audit.findings.jsonl` | no (rewritten per re-audit) | `auditor-case-study.yml` | Re-audit findings sidecar, diffed against the original — NOT appended to global `findings.jsonl` |
| `auditor/audits/<slug>.re-audit.diff.md` | no (rewritten per re-audit) | `auditor-case-study.yml` | Per-finding verification table — source material for the case-study writer's "Re-Audit" section |
| `auditor/feedback/log.json` | no (rebuilt) | daily report | Rolling summary, derived from the three append-only logs |
| `auditor/registry/repos.json` | no (mutated in place) | multiple workflows | Tracking database for repos and PRs |
| `auditor/vocab-advisories.jsonl` | yes | `auditor-vocab-drift.yml` | One record per vocabulary drift cluster. Advisory only — never reaches the contribute step. |
| `auditor/audits/<slug>.vocab-drift.md` | no (rewritten per scan) | `auditor-vocab-drift.yml` | Human-readable drift advisory report |
| `auditor/audits/<slug>.vocab-drift.jsonl` | no (rewritten per scan) | `auditor-vocab-drift.yml` | Per-scan advisory sidecar, source for global `vocab-advisories.jsonl` |

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
  "confidence": "high",
  "evidence": "new Function() runs against a regex-extracted string; reproducer raises if input is malformed",
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
| `confidence` | enum | yes | One of `high`, `medium`, `low`. **Only `high` findings reach the contribute step**; `medium` / `low` stay in audit data for our own learning. `high` requires the scorer to have reproduced the breakage during the scoring pass — ran the snippet and saw the error, followed the link and got 404, etc. Default is `medium`. Strict definitions in `auditor/prompts/score-artifacts.md` §sidecar. |
| `evidence` | string | yes | One-line concrete observation when `confidence: high` (e.g., `NameError: name 'model_id' is not defined`, `link returns 404`). Empty string `""` for `medium` / `low`. |
| `penalty` | int \| null | yes | Negative integer for `nl_quality` findings; `null` otherwise |
| `pattern` | string | yes | Short machine-friendly id (e.g., `new-Function-eval`, `missing-frontmatter`) |
| `description` | string | yes | One-line human summary, no newlines |
| `false_positive` | bool | yes | `true` if the auditor itself decided the finding is invalid; default `false` |
| `suggested_fix` | string | yes | One-line fix hint, empty string if none |
| `fp_reason` | string | when `false_positive: true` | One-line explanation of why the finding is invalid in this context |
| `rule_gap` | string | when `false_positive: true` | One-line hint at what the rule should account for to avoid this misfire |

#### Backward compatibility

Findings emitted before the `confidence` / `evidence` fields were introduced
(2026-04-28) will not have these keys. Consumers MUST treat missing
`confidence` as `medium` (default-conservative), so legacy findings cannot
unintentionally ship as PRs through the contribute filter.

### `rule_id` namespace conventions

- `R01`–`R51`: NL rules from `skills/nlpm/rules/` (R51 is opt-in; auditor never enables it on external repos)
- `SEC-<pattern-slug>`: security patterns (e.g., `SEC-curl-pipe-sh`, `SEC-new-function-eval`, `SEC-shell-true`, `SEC-postinstall-script`)
- `BUG-<kind>`: NL artifact bugs (e.g., `BUG-missing-frontmatter`, `BUG-broken-reference`, `BUG-undeclared-tool`, `BUG-invalid-semver`)
- `CC-<kind>`: cross-component issues (e.g., `CC-stale-count`, `CC-broken-relative-path`, `CC-terminology-drift`, `CC-orphan-component`)
- `VOCAB-<disposition>`: vocab-drift advisories from `auditor-vocab-drift.yml` (e.g., `VOCAB-drift`, `VOCAB-cooccurrence-drift`, `VOCAB-ambiguous`). These IDs only appear in `vocab-advisories.jsonl`, never in `findings.jsonl`.
- `UNCLASSIFIED`: used sparingly, surfaces as a rule-gap signal in reports

New IDs may be introduced without a schema change, but should be documented in the rules skill when they recur.

### `fingerprint` computation

```
payload     = repo + "|" + file + "|" + rule_id + "|" + pattern + "|" + line + "\n"
fingerprint = "sha256:" + sha256(payload)
```

The trailing `\n` is part of the contract: `auditor/scripts/compute-fingerprint.sh` pipes `jq` output through `shasum -a 256`, and `jq`'s default mode appends a newline that `shasum` folds into the digest. Python or other language reimplementations (e.g., `auditor/scripts/diff-findings.py`) MUST include the same trailing newline — omitting it silently produces a different digest. A self-test in `diff-findings.py --self-test` cross-checks Python's output against the shell helper on every run.

The fingerprint is deliberately stable across re-audits of the same file (same repo, same rule, same pattern, same line). It is the join key that connects findings to PR outcomes and to disagreements.

If the line shifts but the finding is otherwise identical, the fingerprint changes. This is intentional: line-shift fingerprint churn is tolerable, and false-matches across moved code is worse. When a line-shift match matters — e.g., the post-merge re-audit — the consumer falls back to a "loose key" of `(repo, file, rule_id, pattern)` and distinguishes `persists_identically` from `persists_line_shifted` in its output. See `finding_verified` below.

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

Emitted by `auditor-classify.yml` when it consumes a `pr_comments_snapshot` and determines the comments indicate genuine dissent. Classification is done by a Haiku call over the comment thread; results are cached by `comments_hash` so unchanged threads don't re-classify.

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

## `vocab-advisories.jsonl` — one record per vocab drift cluster

Vocab advisories live in a dedicated log, not in `findings.jsonl`. They are **advisory only** — the contribute workflow never reads this file, so vocab clusters never become PRs. The judgment of whether a cluster is real drift or a legitimate semantic distinction belongs to the target's maintainers, not to the auditor.

### Record schema

```json
{
  "event": "vocab_advisory",
  "timestamp": "2026-05-19T12:00:00Z",
  "audit_run_id": "24564889725",
  "repo": "owner/name",
  "commit_sha": "abc123def456...",
  "fingerprint": "sha256:c36de2e5...",
  "disposition": "drift",
  "confidence": "high",
  "terms": ["analyzer", "scanner"],
  "term_freq": {"scanner": 12, "analyzer": 3},
  "term_files": {
    "scanner": ["agents/scanner.md", "docs/intro.md"],
    "analyzer": ["docs/intro.md", "skills/foo/SKILL.md"]
  },
  "files_affected": 3,
  "suggested_canonical": "scanner",
  "evidence": "both terms appear in role-noun position with overlapping neighbor words",
  "rule_id": "VOCAB-drift"
}
```

### Field reference

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `event` | string | yes | Always `"vocab_advisory"` |
| `timestamp` | ISO 8601 UTC | yes | Set by post-step, not by Claude |
| `audit_run_id` | string | yes | `GITHUB_RUN_ID` or `"local"` |
| `repo` | string | yes | `owner/name` |
| `commit_sha` | string | yes | Full SHA at scan time; `"unknown"` if clone failed |
| `fingerprint` | string | yes | `sha256:<hex>` of `repo + "VOCAB" + sorted_terms_csv + disposition` |
| `disposition` | enum | yes | `drift`, `likely_drift`, `co_occurrence_drift`, or `ambiguous` |
| `confidence` | enum | yes | `high`, `medium`, or `low` — scanner's confidence in the cluster judgment |
| `terms` | string[] | yes | Alphabetically sorted; length ≥ 2 |
| `term_freq` | object | yes | One int count per term |
| `term_files` | object | yes | Max 5 paths per term |
| `files_affected` | int | yes | Distinct files in the union of `term_files` |
| `suggested_canonical` | string | yes | Must be one of `terms` |
| `evidence` | string | yes | One-line summary of why these cluster |
| `rule_id` | string | yes | `VOCAB-drift` / `VOCAB-cooccurrence-drift` / `VOCAB-ambiguous` |

### `fingerprint` computation

```
payload     = repo + "|VOCAB|" + sorted(terms).join(",") + "|" + disposition + "\n"
fingerprint = "sha256:" + sha256(payload)
```

Same `\n` contract as the main fingerprint formula — `compute-vocab-fingerprint.sh` pipes `jq` output through `shasum`. Python reimplementations MUST include the trailing newline.

The fingerprint is stable across re-runs as long as the cluster's term set is unchanged. Changing the cluster (adding or removing a term) changes the fingerprint, which is the correct behavior — a different cluster is a different advisory.

### Why a separate log

`findings.jsonl` records are *things to fix*: PR-eligible bugs, quality penalties, security risks. The contribute step filters this log for `confidence: high` records and opens PRs.

`vocab-advisories.jsonl` records are *language patterns to consider*: a maintainer's call about whether two terms in their domain are synonyms or distinctions. The auditor cannot judge this — the target's vocabulary is its own. Filing PRs for vocab advisories would be presumptuous and is structurally prevented by putting them in a different log the contribute step never reads.

### Lifecycle events

`auditor-vocab-drift.yml` emits two lifecycle events to `events.jsonl`:

- `scan_skipped_premature` — when the target has fewer than 5 NL artifacts
- `advisories_aggregated` — at the end of each successful scan, with `{repo, advisories, invalid_lines}`

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

`pr_state` ∈ `{merged, closed_unmerged, open, stale_90d, cla_blocked}`. The `stale_90d` state is emitted once, when an open PR crosses 90 days with no activity. The `cla_blocked` state is emitted on every transition into a state where the PR is OPEN but a `cla/...` check is failing — typical when the contributor identity has not signed the target org's Contributor License Agreement (e.g., Google's individual CLA at https://cla.developers.google.com/about). `stale_90d` is **not** emitted for `cla_blocked` PRs: the clock is on the contributor to sign, not on the maintainer to review.

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

### Event: `finding_verified`

Emitted by `auditor-case-study.yml` after a post-merge re-audit. One record per original finding — outcome classifies the finding's fate against the re-scored target at HEAD.

```json
{
  "timestamp": "2026-04-24T10:30:00Z",
  "workflow": "case-study",
  "event": "finding_verified",
  "run_id": "...",
  "run_number": 0,
  "data": {
    "repo": "owner/name",
    "fingerprint": "sha256:...",
    "rule_id": "R09",
    "file": "agents/counter.md",
    "pattern": "no-examples",
    "outcome": "fixed_and_merged",
    "commit_sha_before": "abc123...",
    "commit_sha_after": "def456...",
    "pr_number": 42
  }
}
```

`outcome` ∈:

| Value | Meaning |
|-------|---------|
| `fixed_and_merged` | Finding absent from re-audit AND its fingerprint appeared in a merged PR — our contribution resolved it |
| `fixed_applied_separately` | Finding absent from re-audit AND its fingerprint appeared in a closed-unmerged PR whose maintainer comments indicated the fix was applied separately — our PR was not the vehicle but our finding drove the fix |
| `fixed_upstream_not_merged` | Finding absent from re-audit AND no PR we opened carried this fingerprint — maintainer found and fixed the issue independently |
| `persists_identically` | Finding present in re-audit with the same fingerprint — line + rule + pattern unchanged since audit |
| `persists_line_shifted` | Finding present in re-audit with a different line but matching `(repo, file, rule_id, pattern)` — maintainer touched surrounding lines but left the finding in place |

`pr_number` is the PR whose `nlpm-metadata` block claimed the fingerprint, or `null` for `fixed_upstream_not_merged` / `persists_*` outcomes. The emitter (`diff-findings.py`) normalizes this field to `integer | null` via `_coerce_pr_number`: registry values that leak through as strings (e.g., `"42"`), prefixed forms (`"#42"`), or malformed shapes (bool, float, non-numeric string) are coerced to int or dropped to `null`. Consumers may rely on `integer | null` without type branching.

This event is higher-signal than `finding_outcome` for per-rule precision analysis: `finding_outcome` records intent (a PR merged), while `finding_verified` records effect (the rule's target is actually gone from the code). `rule-health.py` joins both.

### Event: `finding_introduced`

Emitted alongside `finding_verified` when the post-merge re-audit surfaces findings that were NOT in the original audit. Distinguishes regressions introduced by maintainer commits from persistent findings we already knew about.

```json
{
  "timestamp": "2026-04-24T10:30:00Z",
  "workflow": "case-study",
  "event": "finding_introduced",
  "run_id": "...",
  "run_number": 0,
  "data": {
    "repo": "owner/name",
    "fingerprint": "sha256:...",
    "rule_id": "R14",
    "file": "agents/new-agent.md",
    "pattern": "missing-examples",
    "severity": "high",
    "commit_sha": "def456..."
  }
}
```

`finding_introduced` events are NOT appended to `findings.jsonl` — re-audit sidecars deliberately stay out of the global log to avoid double-counting the same rule against the same repo in per-rule reach calculations. The event carries enough fields for retrospective analysis without inflating the findings table.

### Event: `finding_amended`

Reserved for future use. Emitted when a prior finding record is retroactively invalidated (e.g., the rule was later deprecated). Always references a prior `fingerprint`. No current workflow emits this; it exists in the schema so tooling can handle it when introduced.

## Re-audit summary

`auditor/scripts/diff-findings.py` writes a summary JSON blob consumed by the case-study writer prompt and by ad-hoc reporting. Location is caller-specified (`--summary-out`); the case-study workflow writes to `/tmp/evidence/re-audit-summary.json`.

### Record schema

```json
{
  "repo": "owner/name",
  "date": "2026-04-24",
  "original_score": 74,
  "reaudit_score": 92,
  "commit_sha_before": "abc123...",
  "commit_sha_after": "def456...",
  "original_findings_count": 12,
  "reaudit_findings_count": 3,
  "original_malformed_count": 0,
  "reaudit_malformed_count": 0,
  "verified": {
    "fixed_and_merged": 8,
    "fixed_applied_separately": 1,
    "fixed_upstream_not_merged": 1,
    "persists_identically": 1,
    "persists_line_shifted": 1
  },
  "introduced_count": 1,
  "fixed_total": 10,
  "persists_total": 2
}
```

### Field reference

| Field | Type | Notes |
|-------|------|-------|
| `repo` | string | Target repo `owner/name` |
| `date` | ISO date | UTC day the re-audit ran |
| `original_score` | int \| null | `**NL Score**:` value parsed from the original audit report; `null` if absent |
| `reaudit_score` | int \| null | `**NL Score**:` value parsed from the re-audit report; `null` if absent |
| `commit_sha_before` | string | Full SHA the original audit ran against; `"unknown"` if the registry and legacy findings don't carry it |
| `commit_sha_after` | string | Full SHA of the target's default-branch HEAD at re-audit time |
| `original_findings_count` | int | Total findings in the original sidecar |
| `reaudit_findings_count` | int | Total findings in the re-audit sidecar |
| `original_malformed_count` | int | Dropped-during-parse rows in the original sidecar; non-zero means the re-audit's "fixed" tally may under-count |
| `reaudit_malformed_count` | int | Dropped-during-parse rows in the re-audit sidecar; non-zero means the "introduced" tally may under-count |
| `verified.<outcome>` | int | Count per outcome (keys match the enum in `finding_verified`) |
| `introduced_count` | int | Re-audit findings with no pairing partner in the original — may be regressions or scoring drift |
| `fixed_total` | int | Sum of all three `fixed_*` outcomes |
| `persists_total` | int | Sum of both `persists_*` outcomes |

When the writer prompt detects `skipped: true` at the top level instead of these fields, it omits the "Re-Audit" section of the article rather than fabricating one. `skipped` is a set-shape variant — only the `skipped` and `reason` keys are present — emitted by the workflow's skip step (reclone failure, zero findings, or rescore failure).

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
  ⋈ events.jsonl (where event = finding_outcome)   on fingerprint
  ⋈ events.jsonl (where event = finding_verified)  on fingerprint
  ⋈ disagreements.jsonl                            on fingerprint
GROUP BY rule_id
```

Derived per-rule metrics:

| Metric | Source | Signal |
|--------|--------|--------|
| `hits / repos_audited` | findings | Reach |
| `merged / contributed` | findings ⋈ outcomes | Precision — our judgment (a PR was merged) |
| `verified_fixed / verified_total` | findings ⋈ verified | Precision — effect (a re-audit confirmed the rule's target is gone) |
| `self_fp / hits` | disagreements:self | Precision (our known errors) |
| `maintainer_rejected / contributed` | disagreements:maintainer | Precision (external) |
| `downstream_suppression / deployments` | disagreements:downstream | Community disagreement |
| median `dissent_type` | disagreements:maintainer | How the rule fails, not just that it fails |

**`verified_fixed` vs `merged`.** `merged` tells you the maintainer accepted a PR that claimed to address the finding. `verified_fixed` tells you a re-run of the scorer against the post-merge code no longer flags it. These can diverge when:

- A PR merged that only partially addressed the finding → `merged=1`, `verified_fixed=0` (outcome `persists_identically` or `persists_line_shifted`).
- The maintainer fixed the finding in a separate commit → `merged=0`, `verified_fixed=1` (outcome `fixed_upstream_not_merged`).
- The maintainer re-introduced the defect in a later commit → `merged=1`, `verified_fixed=0` (outcome `persists_*`).

`verified_fixed` is the stricter, more load-bearing signal for rule precision. Per-rule `state` classification (healthy/noisy/disputed/dormant) in `rule-health.py` weights verified_fixed above merged when both are present.

Rules cluster into four states on these metrics:

- **healthy** — high reach, high precision, low disagreement → keep as-is
- **noisy** — high reach, low precision → refine trigger or add exceptions
- **dormant** — zero hits across many audits → delete or re-scope
- **disputed** — high reach, high disagreement → revisit the underlying principle

## Registry: `auditor/registry/repos.json`

Not a log — a mutable state file, rewritten in place by the pipeline. Documented here because its `.repos[].prs[]` array is read by `rule-health.py` and `auditor-daily-report.yml` and the shape must stay consistent.

### Top-level

```json
{
  "repos": {
    "owner/name": { /* repo record */ }
  }
}
```

### Repo record

| Field | Type | Written by | Notes |
|-------|------|------------|-------|
| `status` | enum | discover → batch → audit → contribute → track | One of `discovered`, `audited`, `contributed`, `tracked`, `complete`, `policy_denied`, `policy_cla_required`, `orphaned` |
| `audit_issue` | int | discover | Issue number in this repo, tracks the pipeline for the target |
| `stars` | int | discover | Star count at discovery time |
| `pipeline_prs` | array | contribute | PR numbers the auditor opened in the target repo |
| `prs` | array | track | Per-PR state snapshots — see below |
| `case_study_candidate` | bool | track | `true` once any PR merged or was applied separately |
| `rule_adopted` | bool | track | `true` if the maintainer's own comments indicate rule-adoption |
| `policy_no_external_prs` | bool | contribute | `true` if the owner is on the no-external-PR deny list (audit ran, contribute was skipped) |
| `policy_cla_required` | bool | contribute | `true` if the owner requires a signed CLA (e.g., Google orgs) and the contributor identity has not signed (audit ran, contribute was skipped pending CLA) |
| `terminal_reason` | enum | manual / future track | Why a repo entered the `orphaned` terminal state. Currently `prs_disabled`. |
| `retired_at` | date | manual / future track | `YYYY-MM-DD` the repo was moved to `orphaned`. |
| `retired_note` | string | manual / future track | Human-readable explanation of the retirement. |

### Status terminal states

`policy_denied` (audit data captured, no PRs opened, repo is permanent dead-end for contribute) and `policy_cla_required` (audit data captured, no PRs opened, will become eligible once `vars.GOOGLE_CLA_SIGNED=true` is set on the workflow repo and the issue is re-labeled `contribute-approved`) are both terminal-but-recoverable states for the contribute pipeline. They never advance to `tracked`/`complete` automatically because no PRs exist to track. Daily report and rule-health filter on `status` to exclude these from "in flight" counts.

`orphaned` is a terminal state for a repo where PRs **were** opened but can no longer be tracked through to an outcome because the target became unreachable — distinct from `policy_denied`/`policy_cla_required`, where no PRs were ever opened. The trigger seen in practice (2026-05-29, `iannuttall/claude-agents`): the maintainer disabled pull requests on the repository, so `gh pr view` returns *"Pull requests are disabled for this repository."* for every `pipeline_prs` entry. The track loop's `gh pr view ... || echo ""` swallows the failure and `continue`s, leaving `prs: []`; because the promotion gate at the bottom of the loop requires `jq length > 0`, the repo would otherwise sit in `contributed` forever, re-polling the dead PRs every 4 h and never reaching a case study. `orphaned` removes it from the track-poll `select(...)`. The `terminal_reason` field records the cause (`prs_disabled`; reserve room for `repo_deleted`, `repo_archived`, etc.). Like the policy states, `orphaned` is excluded from "in flight" counts and never auto-advances. The original `pipeline_prs` are preserved as the audit trail; the findings keep their last-observed `pr_state` in `events.jsonl` (no synthetic terminal `finding_outcome` is emitted, because the maintainer never adjudicated them — the door simply closed).

### PR record (`repos[owner/name].prs[i]`)

| Field | Type | Notes |
|-------|------|-------|
| `number` | int | PR number in the target repo |
| `state` | string | Raw GitHub state: `OPEN` / `CLOSED` / `MERGED` |
| `mergedAt` | ISO 8601 \| null | |
| `closedAt` | ISO 8601 \| null | |
| `title` | string | |
| `createdAt` | ISO 8601 | |
| `updatedAt` | ISO 8601 | Used for stale_90d detection |
| `outcome` | enum | Pipeline-derived: `merged`, `applied_separately`, `rejected`, `open`, `cla_blocked` |
| `fingerprints` | array | Finding fingerprints parsed from the PR body's `nlpm-metadata` block; `[]` for legacy PRs |
| `rule_ids` | array | Parallel to `fingerprints`; `[]` for legacy PRs |
| `stale_90d_emitted` | bool | Sticky flag — `true` once the `stale_90d` finding_outcome event was logged for this PR |

New PR-record fields are additive. Readers must use `.field // default` (or the equivalent) to accommodate records written before the field existed.

## `auditor/exemplars/<slug>.md` — teaching artifacts for clean audits

Written by `auditor-exemplar.yml` when an audit issue is labeled
`case-study-clean` (promoted automatically by `batch-process.py phase0`
when an audit scores ≥ `EXEMPLAR_THRESHOLD` (default 90) and security is
not `BLOCKED`). Distinct from `case-studies/<date>-<slug>.md`, which is a
narrative article about a contribute-PR outcome.

### Frontmatter contract

| Field | Required | Notes |
|-------|----------|-------|
| `slug` | yes | Same shape as `repos.json` keys (hyphen-substituted) |
| `repo` | yes | `owner/name` |
| `audited` | yes | ISO date when the audit ran |
| `commit_sha` | yes | Target HEAD at audit time (from `commit_sha_at_audit` in registry) |
| `score` | yes | Numeric audit score |
| `exemplifies` | yes | YAML list of `R##` rule IDs the body cites with concrete evidence |

`exemplifies:` is the join key. `rule-health.py load_exemplars_by_rule()`
walks `auditor/exemplars/*.md` and emits per-rule
`exemplars_count` + `exemplar_slugs[]` in `rule_metrics`. A rule with
high hits and zero exemplars is surfaced via the
`rules_high_hits_no_exemplar` field — signal that the rule is hard to
follow or compliance is rare in the wild.

Registry side-effects: the exemplar workflow sets
`repos[<slug>].exemplar_published: true` and
`repos[<slug>].exemplar_path: auditor/exemplars/<slug>.md`.

### Auto-generated gallery: `auditor/exemplars/README.md`

Built by `auditor/scripts/build-exemplar-gallery.py`. Deterministic
re-render on each `auditor-exemplar.yml` run; CI freshness check via
`--check`. Three views: by score (desc), by rule, by repo (alpha).
Never hand-edit; the workflow overwrites it.

### Citation blocks in `skills/nlpm/rules/SKILL.md`

When a rule has at least one exemplar, the
`auditor-cite-exemplars.yml` weekly workflow opens a PR adding a
3-line marker-wrapped block right before the next rule heading:

```markdown
<!-- nlpm-exemplar-citation:begin -->
> Real-world example: [slug-a](../../../auditor/exemplars/slug-a.md), [slug-b](...)
<!-- nlpm-exemplar-citation:end -->
```

The marker anchors let subsequent runs UPDATE the block in place
(idempotent — re-runs don't stack duplicates) and REMOVE it when the
exemplar list shrinks to zero. Hand-edits within the markers will be
overwritten on the next workflow run.

### Event: `exemplar_published`

Emitted by `auditor-exemplar.yml` after successful commit.

```json
{
  "event": "exemplar_published",
  "timestamp": "ISO 8601",
  "data": {
    "repo": "owner/name",
    "exemplar_path": "auditor/exemplars/owner-name.md",
    "score": 92
  }
}
```

## Versioning

This schema is the contract between workflows and learning tooling. Changes follow these rules:

- **Additive changes** (new optional field, new event type, new enum variant) — no version bump, document the addition here.
- **Breaking changes** (rename/remove a field, change a type) — bump `version` in the PR metadata block. For JSONL logs, write a one-shot migration script that rewrites historical records to the new shape; don't leave mixed schemas in the same file.
- **Deprecations** — mark the field as deprecated in this doc; keep emitting it for at least 30 days after downstream consumers stop reading it.

The goal: a researcher six months from now can pick up any of these logs and interpret every record without context from outside this file.
