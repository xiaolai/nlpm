# Auditor (self-evolution pipeline)

Reference for the `auditor/` pipeline, moved out of `AGENTS.md` so the memory file stays instruction-first. The binding rules for working on the pipeline are in `AGENTS.md` § Auditor rules; this file is the narrative, the workflow and data inventories, and the evidence behind the gates. Record contracts: `auditor/SCHEMAS.md`.

The `auditor/` subdirectory contains a GitHub Actions pipeline that discovers, audits, and contributes to NL programming plugin/skill repos across GitHub — then feeds learnings back into NLPM's rules. **Current scope**: discovery and contribution target Claude Code plugin/skill repos (matches the broadest published corpus). The scoring rubric itself is multi-tool (Tier 2-Claude / Tier 2-Codex / Tier 2-Antigravity per `analysis/multi-tool-design-2026-05.md`); Codex CLI and Antigravity discovery + contribution is a planned PR-D follow-up.

## Workflows (.github/workflows/auditor-*.yml)

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| auditor-discover | Weekly cron / manual | Discover repos with 500+ stars and 5+ NL artifacts via `gh search repos` (popularity signal). Vendor-default filter (`auditor/scripts/vendor_default_filter.py`) drops anthropics/* and CLA-gated orgs before the artifact probe. Velocity signal (rising-but-not-yet-popular repos) is planned to arrive as inbound GitHub issues posted by `claudepot-office/bots/alan@repo-scout` — keeps the BQ scan + GCP credentials in one place rather than mirrored here. Also searches for **agent workflow program** repos (project-root `program.md` driving an autonomous loop, karpathy/autoresearch-style) via the `"program.md" autonomous in:description` query; the probe matches `^program\.md$` as an artifact path. These repos typically have a single artifact (program.md), below the default `MIN_ARTIFACTS=5` floor — manual runs with `min_artifacts: 1` are the path to audit them today (per-repo-type floor policy is a follow-up). |
| auditor-batch-processor | Every 6h cron / manual | Pick next batch, promote audits to contribution. v0.8.23: phase1 now skips promotion when every high-confidence finding sits on a "low-landing-rate" rule (`hits ≥ 20`, `contributed ≥ 5`, `merged/contributed < 0.15`, state not noisy/disputed). Calls `auditor/scripts/rule-health.py` once per run to compute the suppression set; fail-soft if it fails. Opt out via `NLPM_DISABLE_LOW_LANDING_SUPPRESSION=1`. The 2026-05-20 query found `BUG-broken-reference` + `BUG-missing-frontmatter` in this state — high verify_rate but zero direct merges; suppression catches them without touching the rulebook (refinement is the path for noisy/disputed rules; this is the orthogonal path for rules whose findings reproduce — high verify_rate — but rarely merge). **Phase 4 (housekeeping)** closes each open `audit-complete` "Audit candidate" issue once its repo reaches a terminal registry status (`contributed`/`tracked`/`complete`/`policy_denied`/`orphaned`, or `audited` after `NLPM_AUDITED_CLOSE_GRACE_DAYS`, default 3d). Never closes `discovered`/`none` backlog or any issue with an action-pending label (`audit-ready`/`contribute-approved`/`case-study-ready`/`security-blocked`); closing too early would make the pipeline skip contribution, so the grace window lets phase1 promote a fresh audit first. Decision logic is the pure `_terminal_close_note` predicate (unit-tested in `tests/test_batch_close.py`). Fixes the accumulation of hundreds of never-closed terminal issues. |
| auditor-audit | Issue labeled `audit-ready` | Security scan + NL score; emits findings.jsonl + disagreements.jsonl |
| auditor-contribute | Issue labeled `contribute-approved` | Reads target's CONTRIBUTING.md / PR template / CoC, forks, opens PRs for verified bugs only (max 3 first-contact, 5 thereafter); stamps each PR body with `nlpm-metadata` block; **never** opens an umbrella/summary issue on the target; backstop step verifies post-hoc. **Duplicate-detection gate** (in the `Prepare findings` step): drops any finding whose `file` is already modified by an OPEN PR on the target (precise signal — open PR's changed-files list contains the path; fail-open on gh error; capped at 100 open PRs). Added 2026-05-26 after ChromeDevTools/chrome-devtools-mcp#2122 was closed by a maintainer as a duplicate of an existing open PR for the same fix. If the gate drops all findings, `skip_contribute` fires and no PR is opened. |
| auditor-track | Every 4h cron | PR state, emits finding_outcome + pr_comments_snapshot on transitions |
| auditor-case-study | Issue labeled `case-study-ready` | Re-audit target at HEAD (diff vs. original findings, emit finding_verified + finding_introduced), write article, self-review, polish, cover image |
| auditor-exemplar | Issue labeled `case-study-clean` | Write a teaching artifact from a high-scoring audit (score ≥ 90, security != BLOCKED). Output is `auditor/exemplars/<slug>.md` cited by `skills/nlpm/rules/` as a positive real-world reference. Auto-labeled by `batch-process.py phase0`. Also regenerates `auditor/exemplars/README.md` (the gallery). |
| auditor-cite-exemplars | Weekly cron / manual | **Human-gated**: walks `auditor/exemplars/*.md`, proposes `> Real-world example:` line edits in `skills/nlpm/rules/SKILL.md` (one per rule with ≥1 exemplar), opens a PR labeled `exemplar-citation-proposal` for review. Deterministic — no LLM. |
| auditor-daily-report | Daily cron | Pipeline state + per-rule health (healthy/noisy/dormant/disputed) |
| auditor-classify | Daily cron / manual | Haiku classifies `pr_comments_snapshot` → `maintainer_rejected` |
| auditor-suppressions | Weekly cron / manual | Scan public repos for NLPM rule-override configs |
| auditor-vocab-drift | Issue labeled `audit-ready` / manual | Registry-free vocabulary drift advisory for external repos. Runs in parallel with `auditor-audit`. Output is advisory only — never produces PRs, never gates contribute. Sidecar at `auditor/audits/<slug>.vocab-drift.{md,jsonl}`; global log at `auditor/vocab-advisories.jsonl`. |
| auditor-render-dashboard | Daily cron / manual | Renders `auditor/reports/dashboard.html` — cross-repo HTML aggregate showing repo table, rule distribution, cross-repo vocab-drift network (AntV G6), and activity timeline. Self-contained, file://-openable. Driven by `auditor/scripts/render-dashboard.py`. |
| auditor-repo-report | Manual dispatch only | Backfill renderer for per-repo HTML reports. Takes a `--repo` input (`owner/name` or `all`) and writes `auditor/reports/<slug>.html` using `render-repo-report.py`. The same render runs automatically at the tail of `auditor-audit` and `auditor-vocab-drift`; this workflow re-renders without re-auditing. |
| auditor-refine-rules | Weekly cron / manual | **Human-gated**: open PR with proposed rule edits (reviewer: xiaolai) |
| auditor-docs-diff | Weekly cron (Tue 06:00 UTC) / manual | Hashes the Claude Code doc URLs cited by NLPM rules (`auditor/docs-citations.json` → `auditor/docs-hashes.json`) and opens an issue listing the rule files that cite any doc whose content changed. Surfaces drift only; never edits a rule. |
| auditor-rule-review | Quarterly cron (1st of Jan/Apr/Jul/Oct) / manual | Opens an issue with a rule-review checklist (missing citations, stale `last_verified` dates, new Claude Code features, aged premises). Fixes nothing; the maintainer works the checklist. |
| auditor-integration-test | Manual dispatch only | Exercises the auditor scripts at a chosen level (`unit` / `smoke` / `full`); read-only except the `full` job. |
| auditor-unstick-bot-prs | Every 30 min cron / manual | **Janitor** for the no-direct-push flow. Every auditor workflow now commits through `auditor/scripts/commit-via-pr.sh` (one auto-merging `auditor-bot` PR per commit); two bot PRs touching the same append-only file (events.jsonl, repos.json, findings.jsonl) conflict at merge and the second stalls. `commit-via-pr.sh`'s own reconcile loop clears conflicts that surface while its opening job is still running; this janitor clears the rest — a sibling that merges after that job exited. Deterministic (no LLM): rebases each `DIRTY` bot PR onto main with `resolve-merge-conflicts.sh` (the same per-file resolver the pre-migration direct pushes used), force-pushes, and re-asserts auto-merge; closes a PR whose commit already reached main via a sibling. Auto-merge is disabled on this repo, so it also merges `CLEAN` bot PRs younger than `UNSTICK_MERGE_MAX_AGE_HOURS` (default 48) and warns about older ones, whose state snapshot may be superseded. Driven by `auditor/scripts/unstick-bot-prs.sh`. Without it, shared-log collisions pile up exactly as the pre-migration `track:` PRs did. |
| pre-release-quality-gate | PR with `.claude-plugin/plugin.json` or `.codex-plugin/plugin.json` change / manual | **Release gate**: runs `bin/nlpm-check` on the whole repo (deterministic floor) + the LLM-judged scorer on the NL artifacts the PR changes (every NL artifact on a manual run) + the vocab-drift scanner. Asserts every changed NL artifact scores at least 95/100 against nlpm's own rubric (95, not 100, because the LLM scorer varies between runs; `bin/nlpm-check` is the exact floor) AND zero enforced vocabulary drift (deterministic `registry-drift-check.py`; the LLM drift clustering is advisory). Blocks the release PR from merging if either fails. Outputs per-file scores to a workflow artifact (`pre-release-gate-<pr#>`) for inspection. Add to branch protection's required checks to make the gate truly blocking. |

## Data (auditor/)

| Path | Append-only | Purpose |
|------|-------------|---------|
| auditor/registry/repos.json | no | Tracking database |
| auditor/feedback/log.json | no | Rolling summary, derived from the three append-only logs |
| auditor/audits/<slug>.md | no | Per-repo human-readable scoring report |
| auditor/audits/<slug>.findings.jsonl | no | Per-audit findings sidecar, source for the global log |
| auditor/audits/<slug>.re-audit.md | no | Post-merge re-scoring report at target HEAD |
| auditor/audits/<slug>.re-audit.findings.jsonl | no | Re-audit findings sidecar (NOT appended to global log) |
| auditor/audits/<slug>.re-audit.diff.md | no | Per-finding verification table feeding the case-study writer |
| auditor/audits/<slug>.vocab-drift.md | no | Per-scan vocabulary drift advisory (human-readable) |
| auditor/audits/<slug>.vocab-drift.jsonl | no | Per-scan advisory sidecar; source for the global advisory log |
| auditor/vocab-advisories.jsonl | yes | One record per drift cluster; advisory only, never PR-eligible |
| auditor/reports/dashboard.html | no (rewritten daily) | Cross-repo HTML dashboard rendered by `auditor-render-dashboard.yml`. Self-contained, file://-openable. |
| auditor/reports/&lt;slug&gt;.html | no (rewritten per audit) | Per-repo HTML report; rendered at the tail of `auditor-audit` and `auditor-vocab-drift`. Drilled into from the dashboard's repo table. |
| auditor/exemplars/<slug>.md | no | Teaching artifact from a high-scoring audit; `exemplifies:` frontmatter join key consumed by `rule-health.py` |
| auditor/exemplars/README.md | no | Auto-generated gallery: by-score, by-rule, by-repo views. Regenerated by `build-exemplar-gallery.py` after every exemplar write. |
| auditor/findings.jsonl | yes | One record per finding, joined by fingerprint |
| auditor/disagreements.jsonl | yes | self_false_positive, pr_comments_snapshot, maintainer_rejected, downstream_suppression |
| auditor/logs/events.jsonl | yes | Lifecycle events + finding_outcome + finding_verified + finding_introduced + findings_aggregated |
| auditor/prompts/score-artifacts.md | no | Shared rubric-and-sidecar scoring prompt used by audit (first pass) and case-study (re-audit) |
| auditor/reports/ | no | Daily reports |

See `auditor/SCHEMAS.md` for the full record contracts.

## The Loop

```
discover → security scan → audit → contribute → track outcomes
                                                       │
                              re-audit at HEAD ←───────┤
                              (emit finding_verified,
                               finding_introduced,
                               feed case-study writer)
                                                       │
                          classify PR dissent ←────────┤
                                                       │
                    daily report / rule-health query ←─┤
                                                       │
                    refine rules (human-gated PR) ←────┘
                                 │
                                 └→ audit better
```

Everything before `refine rules` is automated observation. Only
`auditor-refine-rules` mutates NLPM's own rulebook, and it does so by
opening a PR for human review — never by merging.

The re-audit closes the loop between *intent* (a PR merged) and *effect*
(the scorer's target is actually gone from the code). `finding_verified`
is higher-signal than `finding_outcome` for per-rule precision — a PR
can merge without fully removing the finding, and a maintainer can fix
a finding in a commit outside any PR we opened. `rule-health.py` weights
the verified signal above the merged signal whenever at least three
findings have been verified for the rule.

## Security Gate

The audit workflow includes a security scan BEFORE the NL quality audit:
1. Detects executable surfaces (hooks, scripts, MCP configs, dependencies)
2. Pattern-matches against Critical/High risk signatures (eval, curl-pipe-sh, credential exfil, etc.)
3. If Critical patterns found: labels issue `security-blocked`, skips contribution
4. The contribute workflow refuses to run if `security-blocked` label is present
5. Manual review required to clear the security gate

## Policy Gates (contribute workflow)

After security, the contribute workflow runs three org/repo-level policy
gates. All preserve the audit data and only skip PR creation.

| Gate | Trigger | Status set | Label | Recovery |
|------|---------|------------|-------|----------|
| no-external-PRs | Owner in `DENY_OWNERS` (currently `anthropics`) | `policy_denied` | `policy-no-external-prs` | Manual override only — permanent. |
| CLA-required (signature missing) | Owner in `CLA_REQUIRED_OWNERS` (Google's orgs: `google`, `google-gemini`, `googleworkspace`, `google-labs-code`, `googleapis`, `googlecloudplatform`) **and** `vars.GOOGLE_CLA_SIGNED != 'true'` | `policy_cla_required` | `policy-cla-required` | Sign the individual CLA at <https://cla.developers.google.com/about>, set repo variable `GOOGLE_CLA_SIGNED=true`, set `CONTRIBUTE_AUTHOR_EMAIL` and `CONTRIBUTE_AUTHOR_NAME` to the CLA-signed identity, re-add `contribute-approved` on the audit issue. |
| CLA-required (author identity missing) | Owner in `CLA_REQUIRED_OWNERS` **and** `GOOGLE_CLA_SIGNED == 'true'` **but** `CONTRIBUTE_AUTHOR_EMAIL` or `CONTRIBUTE_AUTHOR_NAME` is empty | `policy_cla_required` | `policy-cla-required` | Set both repo variables to the CLA-signed human identity, re-add `contribute-approved`. |
| pushback-gated | Repo has any prior `maintainer_rejected` event, **or** any `pr_comments_snapshot` event with `pr_state: closed_unmerged`, in `auditor/logs/events.jsonl` | `pushback_gated` | `policy-pushback-gated` | Append a `gate_override` counter-event to `auditor/logs/events.jsonl` with the same `pr` value and a justification — only when the maintainer has explicitly invited a follow-up. |

Why three separate trigger rows: a signed CLA is required, and it does
not by itself clear the gate. `claude-code-action`'s default commit identity is `claude[bot]
<claude[bot]@users.noreply.github.com>`, which is not covered by any CLA.
Even with `GOOGLE_CLA_SIGNED=true`, commits authored by the bot leave
`cla/google` on FAILURE — confirmed by `googleworkspace/cli` #757–#760
(bot-authored, all stuck) and `google-gemini/gemini-skills` #36–#38
(authored by `lixiaolai@gmail.com` because the human ran the contribute
step locally rather than via CI). The author-identity gate prevents
future CI runs from re-creating the first failure mode.

`anthropics/*` rejected 3/3 of our PRs as a policy matter (no external
PRs at all). Google orgs accept external PRs but only when the commit
author has signed the CLA — confirmed across both stranded sets.
Without these gates, the pipeline opens PRs that sit indefinitely and
inflate "in flight" counts for rule-health.

The `Configure commit author identity` workflow step (after the policy
gates, before `Contribute with Claude Code`) sets `git config --global
user.email` and `user.name` from the two `CONTRIBUTE_AUTHOR_*` vars
when both are present. The contribute prompt then re-applies the same
identity inside the target fork's working directory before any commit,
so claude-code-action's bot identity is overridden in both places.

The track workflow detects the `cla_blocked` PR state by inspecting
`statusCheckRollup` for a check whose name matches `^cla(/|$)/i` with
conclusion `FAILURE`. CLA-blocked PRs:
- emit `pr_state: cla_blocked` on every transition (one of the
  `finding_outcome` enum values, see `auditor/SCHEMAS.md`)
- are excluded from `stale_90d` emission (the contributor, not the
  maintainer, is the blocker)
- prevent promotion from `contributed` to `tracked` until the CLA
  gate clears

## Shared scripts (auditor/scripts/)

| Script | Purpose |
|--------|---------|
| log-event.sh | Append lifecycle events to events.jsonl |
| compute-fingerprint.sh | SCHEMAS §fingerprint formula, shared by audit + contribute + re-audit |
| diff-findings.py | Diff a re-audit's sidecar against the original, emit finding_verified / finding_introduced events and the case-study diff report; `--self-test` cross-checks Python fingerprint vs. the shell helper |
| guard-protected-paths.sh | Block stray edits to skills/, agents/ from automation commits |
| resolve-merge-conflicts.sh | Auto-resolve conflicts on append-only log pushes: 3-way merge for the registry, line-union for the append-only logs, regenerate-from-disk for the exemplar gallery, this commit's version for everything else. Rebase-aware: during a rebase git's `--ours`/`:2` is upstream and `--theirs`/`:3` is the commit being landed, so the script maps stages by operation (before 2026-09-30 it assumed the merge mapping and silently kept upstream's side). Shared by the direct-push retry helper (`git-push-with-retry.sh`) AND the PR-flow reconcile paths (`commit-via-pr.sh`, `unstick-bot-prs.sh`). |
| commit-via-pr.sh | Commit the staged tree via one auto-merging `auditor-bot` PR instead of pushing to main. The sole write path for every auditor workflow (nothing pushes to main directly). Commits as the bot on a branch unique to the call (`auditor/bot/<workflow>/<run_id>-<sha>`, so a job may call it more than once), opens the PR, enables auto-merge or — where the repo disallows it — merges directly, then watches briefly: on a shared-file conflict it rebases onto latest main via `resolve-merge-conflicts.sh`, force-pushes, and merges again (closing the PR if the rebase finds its commit already upstream); otherwise it retries the direct merge each tick. Fail-soft: a timeout leaves the PR for `unstick-bot-prs.sh`. |
| unstick-bot-prs.sh | Janitor for `auditor-unstick-bot-prs.yml`: reconciles any open `auditor-bot` PR left `DIRTY` after its opening job exited — same rebase+resolve+force-push as `commit-via-pr.sh`'s in-run loop, for conflicts that surface asynchronously. |
| atomic-registry-write.sh | Validate-then-rename for `auditor/registry/repos.json` writes — rejects malformed JSON before it can hit disk; sole writer used by every workflow that mutates the registry |
| parse-suppressions.py | Extract rule_overrides from NLPM config frontmatter |
| parse-pr-metadata.py | Extract `nlpm-metadata` block from a PR body on stdin |
| rule-health.py | Run SCHEMAS §Learning query, write feedback-summary.json (consumes finding_verified for precision) |
| compute-vocab-fingerprint.sh | SCHEMAS §vocab fingerprint formula; sole writer used by `auditor-vocab-drift.yml` |
| render-dashboard.py | Aggregate cross-repo HTML dashboard renderer. Reads `findings.jsonl` + `vocab-advisories.jsonl` + `logs/events.jsonl` + `registry/repos.json`; emits `auditor/reports/dashboard.html` using `templates/report/` and vendored G6. |
| render-repo-report.py | Per-repo HTML report renderer. Takes `--repo owner/name`, filters the global logs to one repo, and emits `auditor/reports/<slug>.html` using the same template as `/nlpm:report`. Runs at the tail of `auditor-audit` and `auditor-vocab-drift`; standalone backfill via `auditor-repo-report.yml`. Dashboard rows link to these via relative anchor. |
| vendor_default_filter.py | JSONL filter on stdin → stdout. Drops candidates whose owner is on the `DENY_OWNERS` list (no-external-PRs policy, e.g. `anthropics`) or `CLA_REQUIRED_OWNERS` list (Google orgs requiring CLA-signed commits). Saves API + LLM cost vs. discovering and then failing at the contribute policy gates. Used by `auditor-discover.yml` between gh-search and the artifact-probe step. |

The framework-reference doc builder lives in `bin/nlpm-build-docs` and is
invoked as a side effect by all three renderers (`bin/nlpm-report`,
`render-dashboard.py`, `render-repo-report.py`). It reads
`skills/nlpm/{rules,vocabulary,scoring,conventions}/SKILL.md`,
`analysis/vocabulary-design-principles.md`, and
`agents/vocab-drift-scanner.md`, then emits a single anchored HTML guide
at `<out>/docs/index.html`. Reports cross-link into it (`./docs/index.html#R06`,
`./docs/index.html#P1`, `./docs/index.html#severity-levels`, etc.).
Markdown→HTML conversion uses a stdlib-only subset converter (~150 lines).

## Model pinning

One workflow pins a specific Claude model ID; the rest use the
claude-code-action default (currently Sonnet 4.6).

| Workflow | Model | Why pinned |
|----------|-------|------------|
| auditor-classify | `claude-haiku-4-5-20251001` | Bounded-enum classification is Haiku's sweet spot and ~10× cheaper than Sonnet for the same task |

When Anthropic retires the pinned model, update the ID and note the
migration in the commit message. All other workflows pick up model
upgrades automatically.
