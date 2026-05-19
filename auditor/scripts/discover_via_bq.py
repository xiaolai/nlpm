#!/usr/bin/env python3
"""BigQuery velocity harvest — parallel signal source for auditor-discover.

Queries Google's `githubarchive.day.20*` public dataset for repos with
recent star / fork / release activity that match a Claude-Code-relevant
keyword set. Returns a ranked candidate list to stdout as JSONL, one
record per line, in the same shape `auditor-discover.yml` expects from
its existing `gh search repos` step.

Why this exists
---------------
`gh search repos` finds repos that *already cleared* the popularity
threshold the query specifies. BigQuery's `githubarchive` event log
shows what is *currently spiking* — repos crossing the threshold for
the first time, or with unusual recent fork / release activity. The two
signals are complementary; both feed the same artifact-probe gate
downstream.

Source
------
Ported with adaptations from `claudepot-office/bots/alan@repo-scout/
repo_scout/bigquery.py`. Adapted differences:
  - keyword prefilter narrowed to Claude-Code-relevant terms
  - return shape matches NLPM's existing gh-search JSON contract
    (fullName, stargazersCount, updatedAt, description, isArchived)
    so the workflow's later steps don't need to special-case BQ rows
  - --dry-run flag emits the cost estimate alone for cost gating

Cost
----
Partition pruning via `_TABLE_SUFFIX BETWEEN '<lo>' AND '<hi>'` keeps
scan bytes inside the 1 TB/month BigQuery free tier at default
parameters (recent=1d, baseline=7d, pool=200). Run with --dry-run to
confirm before any real query.

Auth
----
Uses Application Default Credentials. In GitHub Actions the
`google-github-actions/auth` action populates ADC from the
GCP_SA_KEY secret; locally, run `gcloud auth application-default login`
once. The script does not handle credentials directly.

Usage
-----
    python3 discover_via_bq.py --project <gcp-project-id> [options]

    --project           GCP project with BigQuery API enabled (required)
    --archive-dataset   default: githubarchive.day
    --recent-days       default: 1
    --baseline-days     default: 7
    --pool-size         default: 200
    --min-stars-24h     default: 5 (BQ-side minimum)
    --dry-run           print cost estimate, do not run query

Output
------
JSONL on stdout. Each line is a JSON object shaped like:

    {
      "fullName": "owner/name",
      "stargazersCount": 0,         # not known from BQ; left at 0 — the
                                    # gh-search merge fills this in if
                                    # the same repo also surfaces there
      "stars_24h": 42,              # velocity signal, BQ-specific
      "stars_7d_avg": 3.5,
      "forks_24h": 5,
      "releases_24h": 1,
      "unique_actors": 38,
      "last_event_at": "2026-05-19T11:23:45Z",
      "description": "",            # filled later by REST enrichment
      "updatedAt": "2026-05-19T...", # set from last_event_at as a proxy
      "isArchived": false,           # not known from BQ; defaults false
      "discovery_source": "bq"       # marker for the merge step
    }

The downstream "Filter against registry + case studies" and "Probe
repos for NL artifacts" steps in auditor-discover.yml are unchanged —
they consume this same shape regardless of source.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, date, datetime, timedelta


# Keywords used in the BQ prefilter regex on repo.name. The list is
# intentionally narrower than the GH-search query set — coarse over-
# match here costs scan bytes. Final filtering happens in the artifact
# probe downstream, so we can afford to miss the edge cases.
#
# Compared to alan's list this drops the general AI terms (gpt, rag,
# diffusion, transformer) that are mostly noise for the Claude Code
# plugin niche, and adds the plugin/skill/agent-related ones that
# actually correlate with NLPM-relevant repos.
_PREFILTER_KEYWORDS = [
    # Claude Code primary terms
    "claude", "claude-code", "claudecode",
    # Plugin / skill / agent layout markers
    "plugin", "skill", "skills", "agent", "agents",
    "subagent", "subagents",
    # MCP ecosystem
    "mcp", "mcp-server", "claude-mcp",
    # Cross-vendor agent terms that often house Claude artifacts
    "cline", "aider", "codex", "anthropic",
]


def _build_prefilter_regex() -> str:
    """Compile the keyword list into a single boundary-aware regex.

    Each keyword is escaped and bracketed by `(?:^|/|\\b|-)` and
    `(?:\\b|-|$)` so `agent` matches `foo/agent-tools` and `claude/agent`
    but not `tangential`. The leading `(?i)` makes it case-insensitive.
    """
    parts = [re.escape(k) for k in _PREFILTER_KEYWORDS]
    return r"(?i)(?:^|/|\b|-)(?:" + "|".join(parts) + r")(?:\b|-|$)"


def _partition_dates(end_date: date, *, recent_days: int, baseline_days: int) -> tuple[list[date], list[date]]:
    """Return (recent_dates, baseline_dates) sorted oldest → newest.

    `recent` = the last `recent_days` ending at `end_date`.
    `baseline` = the `baseline_days` immediately before that window.
    """
    recent = [end_date - timedelta(days=i) for i in range(recent_days)]
    recent.reverse()
    baseline_start = recent_days
    baseline = [
        end_date - timedelta(days=baseline_start + i)
        for i in range(baseline_days)
    ]
    baseline.reverse()
    return recent, baseline


def _format_table_suffix_range(dates: list[date]) -> tuple[str, str]:
    """Return (lo, hi) suffix bounds for `_TABLE_SUFFIX BETWEEN ...`.

    The wildcard pattern is `<dataset>.20*` (not `.*`) because
    `githubarchive.day` contains view tables like `yesterday` and
    `today` that can't be queried through a bare-`*` wildcard. With
    `20*` consuming the leading `20`, the `_TABLE_SUFFIX` is YYMMDD,
    not YYYYMMDD.
    """
    return dates[0].strftime("%y%m%d"), dates[-1].strftime("%y%m%d")


def build_query(
    *,
    archive_dataset: str,
    end_date: date,
    recent_days: int,
    baseline_days: int,
    candidate_pool_size: int,
    min_stars_24h: int,
) -> str:
    """Compose the SQL.

    Two partition ranges are scanned in one UNION ALL query:
      - recent: last `recent_days` (today + …)
      - baseline: the `baseline_days` BEFORE that, used to compute
        stars_7d_avg as a denominator for the burst-factor signal.

    Both UNION arms carry the same prefilter regex so partition pruning
    works on both halves.
    """
    recent_dates, baseline_dates = _partition_dates(
        end_date, recent_days=recent_days, baseline_days=baseline_days,
    )
    recent_lo, recent_hi = _format_table_suffix_range(recent_dates)
    base_lo, base_hi = _format_table_suffix_range(baseline_dates)
    prefilter = _build_prefilter_regex()
    return f"""
WITH events AS (
  SELECT
    'recent' AS bucket,
    repo.name AS repo_name,
    type,
    created_at,
    actor.login AS actor_login
  FROM `{archive_dataset}.20*`
  WHERE _TABLE_SUFFIX BETWEEN '{recent_lo}' AND '{recent_hi}'
    AND type IN ('WatchEvent', 'ForkEvent', 'ReleaseEvent')
    AND repo.name IS NOT NULL
    AND REGEXP_CONTAINS(repo.name, r'{prefilter}')
  UNION ALL
  SELECT
    'baseline' AS bucket,
    repo.name AS repo_name,
    type,
    created_at,
    actor.login AS actor_login
  FROM `{archive_dataset}.20*`
  WHERE _TABLE_SUFFIX BETWEEN '{base_lo}' AND '{base_hi}'
    AND type = 'WatchEvent'
    AND repo.name IS NOT NULL
    AND REGEXP_CONTAINS(repo.name, r'{prefilter}')
),
agg AS (
  SELECT
    repo_name,
    COUNTIF(bucket = 'recent' AND type = 'WatchEvent')   AS stars_24h,
    COUNTIF(bucket = 'recent' AND type = 'ForkEvent')    AS forks_24h,
    COUNTIF(bucket = 'recent' AND type = 'ReleaseEvent') AS releases_24h,
    COUNTIF(bucket = 'baseline')                         AS stars_baseline_total,
    MAX(created_at) AS last_event_at,
    COUNT(DISTINCT actor_login) AS unique_actors
  FROM events
  GROUP BY repo_name
)
SELECT
  repo_name,
  stars_24h,
  forks_24h,
  releases_24h,
  stars_baseline_total,
  last_event_at,
  unique_actors
FROM agg
WHERE stars_24h >= {min_stars_24h}
ORDER BY stars_24h DESC, releases_24h DESC
LIMIT {candidate_pool_size};
""".strip()


def estimate_cost(
    *,
    project: str,
    archive_dataset: str,
    end_date: date,
    recent_days: int,
    baseline_days: int,
    candidate_pool_size: int,
    min_stars_24h: int,
) -> dict:
    """Dry-run the query and report bytes-to-scan + USD estimate.

    Used as a cost gate before any real query runs. Assumes on-demand
    BigQuery pricing of USD 6.25 / TB scanned (October 2024 published
    rate; adjust the constant if Google revises it).
    """
    from google.cloud import bigquery

    sql = build_query(
        archive_dataset=archive_dataset,
        end_date=end_date,
        recent_days=recent_days,
        baseline_days=baseline_days,
        candidate_pool_size=candidate_pool_size,
        min_stars_24h=min_stars_24h,
    )
    client = bigquery.Client(project=project)
    cfg = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    job = client.query(sql, job_config=cfg)
    bytes_processed = int(job.total_bytes_processed or 0)
    return {
        "bytes": bytes_processed,
        "gb": bytes_processed / 1024**3,
        "tb": bytes_processed / 1024**4,
        "usd": (bytes_processed / 1024**4) * 6.25,
    }


def run_query(
    *,
    project: str,
    archive_dataset: str,
    end_date: date,
    recent_days: int,
    baseline_days: int,
    candidate_pool_size: int,
    min_stars_24h: int,
    timeout_seconds: int = 60,
) -> list[dict]:
    """Run the discovery query and return rows in the gh-search shape.

    Each output row carries the BQ velocity fields plus the minimal set
    of fields the existing auditor-discover.yml pipeline expects
    (fullName, stargazersCount, updatedAt, description, isArchived) so
    no special-casing is needed downstream.
    """
    from google.cloud import bigquery

    sql = build_query(
        archive_dataset=archive_dataset,
        end_date=end_date,
        recent_days=recent_days,
        baseline_days=baseline_days,
        candidate_pool_size=candidate_pool_size,
        min_stars_24h=min_stars_24h,
    )
    client = bigquery.Client(project=project)
    job = client.query(sql, timeout=timeout_seconds)
    rows = list(job.result(timeout=timeout_seconds))

    out: list[dict] = []
    for r in rows:
        repo_name = r["repo_name"]
        last_event = r["last_event_at"]
        last_event_iso = last_event.isoformat() if last_event else None
        stars_24h = int(r["stars_24h"] or 0)
        baseline_total = int(r["stars_baseline_total"] or 0)
        out.append({
            # Existing-shape fields the downstream pipeline reads
            "fullName": repo_name,
            "stargazersCount": 0,        # not known from BQ; merge with
                                         # gh-search rows fills this in
            "updatedAt": last_event_iso,
            "description": "",
            "isArchived": False,         # default; artifact-probe handles
            # BQ-specific velocity fields
            "stars_24h": stars_24h,
            "forks_24h": int(r["forks_24h"] or 0),
            "releases_24h": int(r["releases_24h"] or 0),
            "stars_baseline_total": baseline_total,
            "baseline_days": baseline_days,
            "stars_7d_avg": (baseline_total / baseline_days) if baseline_days > 0 else 0.0,
            "unique_actors": int(r["unique_actors"] or 0),
            "last_event_at": last_event_iso,
            "discovery_source": "bq",
        })
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--project", required=True,
                        help="GCP project with BigQuery API enabled")
    parser.add_argument("--archive-dataset", default="githubarchive.day",
                        help="default: githubarchive.day")
    parser.add_argument("--recent-days", type=int, default=1)
    parser.add_argument("--baseline-days", type=int, default=7)
    parser.add_argument("--pool-size", type=int, default=200)
    parser.add_argument("--min-stars-24h", type=int, default=5,
                        help="BQ-side minimum stars_24h filter")
    parser.add_argument("--timeout", type=int, default=60,
                        help="seconds to wait for the BQ job")
    parser.add_argument("--dry-run", action="store_true",
                        help="print cost estimate, do not run query")
    parser.add_argument("--end-date", default=None,
                        help="ISO date (YYYY-MM-DD). Default: today UTC.")
    parser.add_argument("--max-bytes", type=int, default=None,
                        help="abort with exit 3 if estimated scan exceeds this byte count")
    args = parser.parse_args(argv)

    if args.end_date:
        try:
            end = datetime.strptime(args.end_date, "%Y-%m-%d").date()
        except ValueError:
            print(f"error: --end-date must be YYYY-MM-DD, got {args.end_date!r}",
                  file=sys.stderr)
            return 2
    else:
        end = datetime.now(tz=UTC).date()

    common = {
        "project": args.project,
        "archive_dataset": args.archive_dataset,
        "end_date": end,
        "recent_days": args.recent_days,
        "baseline_days": args.baseline_days,
        "candidate_pool_size": args.pool_size,
        "min_stars_24h": args.min_stars_24h,
    }

    # Cost gate. Always runs first — even on a real query, we want to
    # know the bytes before paying for them. With max-bytes set, abort
    # if estimate exceeds it.
    try:
        est = estimate_cost(**common)
    except Exception as e:
        print(f"error: BQ dry-run failed: {e}", file=sys.stderr)
        return 2

    print(
        f"BQ cost estimate: {est['gb']:.2f} GB scan "
        f"(~${est['usd']:.4f} at on-demand rates)",
        file=sys.stderr,
    )
    if args.max_bytes is not None and est["bytes"] > args.max_bytes:
        print(
            f"error: estimated scan {est['bytes']} bytes exceeds "
            f"--max-bytes {args.max_bytes}; aborting",
            file=sys.stderr,
        )
        return 3

    if args.dry_run:
        print(json.dumps(est))
        return 0

    try:
        rows = run_query(**common, timeout_seconds=args.timeout)
    except Exception as e:
        print(f"error: BQ query failed: {e}", file=sys.stderr)
        return 2

    print(f"BQ harvest: {len(rows)} candidates", file=sys.stderr)
    for row in rows:
        print(json.dumps(row, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
