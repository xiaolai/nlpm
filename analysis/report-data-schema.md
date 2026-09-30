# NLPM Report Data Schemas

Single source of truth for the shape of data that both report renderers consume.

- **Local pipeline** (`/nlpm:report` / `bin/nlpm-report`): emits self-contained HTML using `templates/report/single.html` + vendored G6.
- **Online pipeline** (nlpm.com): VitePress pages mount Vue components that import G6 via ESM and render the same data.

Both pipelines read the same JSON shape. Today, the data is built by these scripts:

| Pipeline | Builder | Output |
|----------|---------|--------|
| Local | `bin/nlpm-report` (Claude Code dispatches scorer/checker/etc. via the slash command) | `<target>/.claude/nlpm-reports/data/<timestamp>.json` |
| Auditor → per-repo | `auditor/scripts/render-repo-report.py` | `auditor/reports/<slug>.json` (sidecar to `<slug>.html`) |
| Auditor → dashboard | `auditor/scripts/render-dashboard.py` | `auditor/reports/dashboard.json` (sidecar to `dashboard.html`) |

The HTML/Markdown renderers are *consumers* of these JSON files. New visualization pipelines (e.g. the upcoming Vue components for nlpm.com) read the same JSON, so adding a new view never duplicates the metric definitions.

---

## `RepoReportData` (per-repo)

Used by `/nlpm:report` locally and by `auditor/reports/<slug>.html` + the upcoming `/reports/<slug>` VitePress page.

```jsonc
{
  "project": "Q00/ouroboros",                  // string  — repo slug or local plugin name
  "generated_at": "2026-05-19T07:30:00Z",      // ISO 8601 UTC
  "score_threshold": 70,                        // int     — pass threshold for this run
  "r51_enabled": false,                          // bool    — vocab discipline opt-in (local only)
  "summary": {
    "total_files": 46,                          // int
    "average_score": 69,                        // number | null — overall score (null for auditor sidecars where per-file scoring isn't tracked)
    "pass_count": 0,                            // int
    "fail_count": 0                             // int
  },
  "files": [
    {
      "path": "agents/foo.md",                  // string  — relative to repo root
      "type": "agent",                          // enum    — see Artifact types in /reference/
      "score": 85,                              // number | null
      "findings": [
        {
          "rule": "R09",                        // string  — rule id; see /reference/rules
          "severity": "low",                    // enum    — "high" | "medium" | "low"
          "line": 12,                           // int | null
          "message": "agent description names no situation it is not for"
        }
      ]
    }
  ],
  "history": [
    {
      "timestamp": "2026-05-15T10:00:00Z",      // ISO 8601 UTC
      "average_score": 64,                       // number
      "kind": "initial_audit"                    // optional — "initial_audit" | "re_audit" | "local_snapshot"
    }
  ],
  "cross_component": {
    "nodes": [
      {
        "id": "agents/foo.md",                  // string  — unique per node
        "label": "foo.md",                      // string
        "type": "agent",                        // string  — artifact type
        "broken": false                         // bool    — true if this node is the target of a broken reference
      }
    ],
    "edges": [
      {
        "source": "commands/foo.md",
        "target": "agents/foo.md",
        "broken": false
      }
    ]
  },
  "vocabulary": null,                            // object | null — only populated when the target ships a vocabulary skill; shape below in VocabularyData
  "vocab_drift": {
    "candidates": [
      {
        "terms": ["scanner", "analyzer"],        // string[] — sorted alphabetically
        "confidence": "high",                    // enum    — "high" | "medium" | "low"
        "disposition": "drift",                  // enum    — "drift" | "likely_drift" | "co_occurrence_drift" | "ambiguous"
        "suggested_canonical": "scanner",        // string
        "files_affected": 3,                     // int
        "evidence": "both appear as role-nouns"  // string
      }
    ]
  },
  "findings": [
    {
      "rule": "R09",                             // string
      "severity": "low",                         // enum
      "confidence": "medium",                    // enum — auditor-only; absent for local
      "file": "agents/foo.md",
      "line": 12,
      "message": "agent description names no situation it is not for"
    }
  ],
  "repo_meta": null                              // object | null — auditor-side metadata; null for local runs. Shape below.
}
```

### `VocabularyData` (the `vocabulary` field)

```jsonc
{
  "scopes": [
    { "id": "internal", "label": "Internal" }
  ],
  "verbs": [
    {
      "id": "score",
      "scope": "internal",
      "deprecated": ["analyze", "grade"],
      "judgment": false,
      "output": "number + penalty list"
    }
  ],
  "nouns": [
    {
      "id": "artifact",
      "class": "artifact_class",                 // string — class group
      "definition": "any NL programming file Claude Code consumes",
      "scope": null                              // string | null
    }
  ],
  "edges": [
    { "source": "score", "target": "finding", "type": "produces" }
  ],
  "cross_scope_homonyms": ["scan", "test", "discover"],
  "deferred": [
    { "verb": "triage", "scope": "internal", "needed_warrant": "user warrant" }
  ]
}
```

### `RepoMeta` (the `repo_meta` field; auditor-only)

```jsonc
{
  "status": "audited",                           // enum — registry status
  "stars": 22474,                                 // int | null
  "security": "REVIEW",                            // enum — "CLEAR" | "REVIEW" | "BLOCKED" | null
  "audit_report_path": "auditor/audits/Q00-ouroboros.md"  // string | null — relative to nlpm root
}
```

When `repo_meta` is non-null, the header surfaces security/stars/status badges instead of the local R51 status.

---

## `DashboardData` (cross-repo aggregate)

Used by `auditor/reports/dashboard.html` and the upcoming `/dashboard` VitePress page.

```jsonc
{
  "generated_at": "2026-05-19T07:30:00Z",
  "since": null,                                  // string | null — ISO date floor if filtered
  "summary": {
    "total_repos": 211,
    "total_findings": 3132,
    "high_findings": 230,
    "total_advisories": 0,
    "high_advisories": 0,
    "repos_with_drift": 0,
    "repos_blocked": 52
  },
  "repo_rows": [
    {
      "repo": "owner/name",                      // string
      "status": "audited",                       // string
      "stars": 22474,                            // int | null
      "score": 84,                               // int | null
      "security": "CLEAR",                       // enum | null
      "total_findings": 72,
      "high_findings": 6,
      "medium_findings": 38,
      "vocab_drift_count": 0,
      "vocab_drift_high": 0
    }
  ],
  "rule_distribution": [
    {
      "rule_id": "R09",                          // string
      "total": 132,                              // int
      "repos_affected": 96                       // int
    }
  ],
  "drift_network": {
    "nodes": [
      {
        "id": "scanner",                         // string — the term itself
        "label": "scanner",
        "freq": 4,                               // int    — cluster count
        "repos": ["owner/name", "..."]           // string[]
      }
    ],
    "edges": [
      {
        "source": "scanner",
        "target": "analyzer",
        "weight": 3,                             // int    — # repos in which the pair co-clusters
        "repos": ["owner/name", "..."]
      }
    ]
  },
  "activity_timeline": [
    {
      "day": "2026-05-19",                       // string — YYYY-MM-DD
      "counts": {                                  // object<string, int> — event type → count for the day
        "audit_complete": 12,
        "prs_submitted": 4
      }
    }
  ]
}
```

---

## Versioning

The shape above is **v1**. Add a top-level `"schema_version": 1` field to outputs starting on or after the date this doc lands. Consumers should accept missing `schema_version` as v1 for backward compatibility.

When a breaking change is necessary:

1. Bump `schema_version` and document the diff here.
2. Renderers may handle multiple versions during a transition.
3. The JSON itself is the contract — the rendered HTML/Vue output is not.

---

## What's intentionally NOT in the schema

- **Rendering hints** (panel order, color choices, label rotation). The renderer owns these.
- **Per-finding rendering** (severity badges, anchor URLs to `/reference/`). Renderer-side concern, not data.
- **VitePress vs file:// distinction.** Both renderers consume the same JSON; the choice of output format lives in the renderer.

This separation is the load-bearing part: it lets a new visualization (Vue, terminal pretty-printer, slack notifier, anything) be added without redefining what "a finding" or "a drift candidate" means.
