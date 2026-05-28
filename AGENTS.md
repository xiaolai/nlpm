# Project Instructions

> nlpm

# nlpm

Natural-Language Programming Manager — multi-tool (Claude Code, Codex CLI, Antigravity) NL artifact scoring, checking, fixing, and testing. Delivered as a Claude Code plugin; the scoring rubric covers all three ecosystems via tier-aware overlays (see `analysis/multi-tool-design-2026-05.md`).

## Architecture

Commands orchestrate agents. Agents use skills as reference knowledge.
Each command does one thing -- no flags (except `--changed` on score).

## Commands

- commands/ls.md -- `/nlpm:ls` -- discover NL artifacts (dispatches scanner)
- commands/score.md -- `/nlpm:score` -- 100-point quality scoring (dispatches scorer + vague-scanner in parallel)
- commands/check.md -- `/nlpm:check` -- cross-component consistency (dispatches checker)
- commands/fix.md -- `/nlpm:fix` -- auto-fix mechanical issues (dispatches scorer)
- commands/trend.md -- `/nlpm:trend` -- track score history over time (dispatches scorer + vague-scanner)
- commands/test.md -- `/nlpm:test` -- run NL-TDD specs (dispatches tester)
- commands/init.md -- `/nlpm:init` -- configure project
- commands/security-scan.md -- `/nlpm:security-scan` -- scan plugin for security risks in executable artifacts
- commands/vocab-init.md -- `/nlpm:vocab-init` -- bootstrap a vocabulary skill for any project (runs extractor, seeds canonical noun/verb tables, writes R51 opt-in stub). Adopter-facing entry point for vocabulary discipline.
- commands/vocab-drift.md -- `/nlpm:vocab-drift` -- registry-free vocabulary drift scan (dispatches vocab-drift-scanner). Advisory only; no penalty. Use before/alongside R51.
- commands/report.md -- `/nlpm:report` -- self-contained HTML report (per-file scores, trend, cross-component graph, vocabulary noun-verb map via AntV G6, drift candidates, findings). Output: `.claude/nlpm-reports/index.html`. file://-openable, no server.
- commands/shared/discover.md -- artifact discovery patterns (not user-invocable)
- commands/shared/classify.md -- artifact type classification (not user-invocable)
- commands/shared/append-history.md -- snapshot persistence to .claude/nlpm-history.json with scope marker (not user-invocable). Used by /nlpm:init, /nlpm:score, /nlpm:trend so trend data accumulates without manual upkeep.

## Agents

- agents/scanner.md -- haiku, mechanical file discovery
- agents/scorer.md -- sonnet, 100-point quality scoring (skills: scoring, conventions, conventions-claude, conventions-codex, conventions-antigravity, vocabulary)
- agents/checker.md -- sonnet, cross-component consistency (skills: conventions, conventions-claude, conventions-codex, conventions-antigravity, vocabulary)
- agents/vague-scanner.md -- haiku, mechanical vague-word counting (no skills)
- agents/tester.md -- sonnet, evaluates artifacts against test specs (skills: testing, conventions, scoring)
- agents/security-scanner.md -- sonnet, security risk detection in executable artifacts (skills: security)
- agents/vocab-drift-scanner.md -- sonnet, judgment-based clustering of likely-synonymous nouns/verbs across a corpus; no registry required (skills: vocabulary, conventions). Output is advisory only.

## Skills

### Auto-loaded by agents (declared in agent frontmatter `skills:`)
- skills/nlpm/conventions/ -- Universal NL artifact conventions: SKILL.md open spec, AGENTS.md as canonical universal memory, vague-quantifier list, prompt engineering, naming, override system. Loaded by scanner, scorer, checker, tester.
- skills/nlpm/conventions-claude/ -- Claude Code overlay: .claude/* paths, plugin.json, hook events, hooks.json, CLAUDE.md, LSP, monitors, settings, tool catalog. Loaded by scorer, checker for Tier 2-Claude artifacts.
- skills/nlpm/conventions-codex/ -- Codex CLI overlay: .codex/config.toml, .codex-plugin/plugin.json, .agents/skills/ layout, AGENTS.md hierarchy, agents/openai.yaml sidecar, Codex hook events, marketplace. Loaded by scorer, checker for Tier 2-Codex artifacts.
- skills/nlpm/conventions-antigravity/ -- Antigravity + legacy Gemini CLI overlay: .gemini/* paths, .agent/ workspace skills, gemini-extension.json, GEMINI.md, TOML slash commands, Gemini-lineage hook events. Advisory-only for Antigravity-specific artifacts until spec stabilizes. Loaded by scorer, checker for Tier 2-Antigravity artifacts.
- skills/nlpm/scoring/ -- penalty tables with rule number cross-references -- loaded by scorer, tester
- skills/nlpm/testing/ -- NL-TDD spec format, test patterns -- loaded by tester
- skills/nlpm/security/ -- security pattern database for executable artifact scanning -- loaded by security-scanner

### Reference (loaded on demand by agents that need them, via cross-references in `nlpm:scoring`, `nlpm:conventions`, and skill scope notes)
- skills/nlpm/rules/ -- the 50 Rules of Natural Language Programming (R01-R50) -- single source of truth, referenced by rule number from `nlpm:scoring`
- skills/nlpm/patterns/ -- NL programming patterns + anti-patterns -- referenced by `nlpm:scoring` scope note
- skills/nlpm/vocabulary/ -- canonical noun/verb registry for NLPM's two scopes (internal vs auditor); bright-line table for the evaluation cluster (score/check/test/scan/audit/review). SKILL.md is the human-readable source; `registry.yaml` is the machine-readable sidecar for the checker/scorer. Populated from `analysis/scripts/extract-vocabulary.py` (literary warrant per P6 of `analysis/vocabulary-design-principles.md`). Drift-detection via R51 is **opt-in** — disabled by default, enabled per-project via `rule_overrides.R51.enabled: true` in `.claude/nlpm.local.md`.

### Writing Reference (loaded on demand)
- skills/nlpm/writing-skills/ -- how to write SKILL.md files
- skills/nlpm/writing-agents/ -- how to write agent definitions
- skills/nlpm/writing-rules/ -- how to write .claude/rules/ files
- skills/nlpm/writing-prompts/ -- universal prompt engineering guide
- skills/nlpm/writing-hooks/ -- how to write Claude Code hooks
- skills/nlpm/writing-plugins/ -- how to design and build plugins
- skills/nlpm/orchestration/ -- multi-agent workflow patterns

## Hooks

- hooks/hooks.json -- PostToolUse command hook on Write|Edit|MultiEdit
- scripts/check-artifact.sh -- classifies written file, emits advisory only for NL artifacts

## Standalone Author Surface (v0.8.0+)

- bin/nlpm-check -- pure-Python (stdlib only) deterministic validator; the
  subset of /nlpm:check that runs without Claude Code installed. Used in
  pre-commit hooks, CI, and pre-publish scripts.
- tests/test_nlpm_check.py -- unittest suite for the binary (run via
  `python3 -m unittest tests.test_nlpm_check`)
- templates/pre-commit-nlpm.sh -- drop-in git pre-commit hook template
- templates/workflows/nlpm-check.yml -- drop-in GitHub Actions workflow
- docs/for-authors.md -- author-facing guide
- analysis/ecosystem-gap.md -- stable research reference
- analysis/scope-expansion-2026-05.md -- the full author-surface plan

## Self-Tests

- .nlpm-test/ -- spec files for all 5 agents (dogfooding NL-TDD)
- tests/ -- Python unittest suite for bin/nlpm-check

## Build & Run

No build step. Markdown plugin + single-file Python binary. Install with:
```
claude plugin install nlpm@xiaolai --scope project
```

Test by running `/nlpm:ls` on any project with NL artifacts.
Run `/nlpm:test` to verify agent specs pass.
Run `python3 -m unittest tests.test_nlpm_check` to verify the binary.

## Prerequisites

- Slash commands (/nlpm:*) -- none. Pure markdown.
- Standalone bin/nlpm-check -- Python 3.11+ (stdlib only; no pip install).
- Auditor workflows -- CLAUDE_CODE_OAUTH_TOKEN, PAT_TOKEN, OPENAI_API_KEY secrets.

## Development

When modifying this plugin:
- Run `/nlpm:score ./` after changes to verify quality stays above 90
- Run `/nlpm:check` to verify cross-component references
- Run `/nlpm:test` to verify agent specs pass
- Bump version in plugin.json AND marketplace.json
- Push plugin repo, then update central marketplace

## Scoring

100-point scale. Start at 100, apply deterministic penalties.
Floor: 0. Ceiling: 100.
Threshold configurable via .claude/nlpm.local.md (default: 70).
Rule overrides supported (suppress, max_penalty, threshold adjustments).

## Auditor (Self-Evolution Pipeline)

The `auditor/` subdirectory contains a GitHub Actions pipeline that discovers, audits, and contributes to NL programming plugin/skill repos across GitHub — then feeds learnings back into NLPM's rules. **Current scope**: discovery and contribution target Claude Code plugin/skill repos (matches the broadest published corpus). The scoring rubric itself is multi-tool (Tier 2-Claude / Tier 2-Codex / Tier 2-Antigravity per `analysis/multi-tool-design-2026-05.md`); Codex CLI and Antigravity discovery + contribution is a planned PR-D follow-up.

### Workflows (.github/workflows/auditor-*.yml)

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| auditor-discover | Weekly cron / manual | Find repos with 500+ stars and 5+ NL artifacts via `gh search repos` (popularity signal). Vendor-default filter (`auditor/scripts/vendor_default_filter.py`) drops anthropics/* and CLA-gated orgs before the artifact probe. Velocity signal (rising-but-not-yet-popular repos) is planned to arrive as inbound GitHub issues posted by `claudepot-office/bots/alan@repo-scout` — keeps the BQ scan + GCP credentials in one place rather than mirrored here. Also searches for **agent workflow program** repos (project-root `program.md` driving an autonomous loop, karpathy/autoresearch-style) via the `"program.md" autonomous in:description` query; the probe matches `^program\.md$` as an artifact path. These repos typically have a single artifact (program.md), below the default `MIN_ARTIFACTS=5` floor — manual runs with `min_artifacts: 1` are the path to audit them today (per-repo-type floor policy is a follow-up). |
| auditor-batch-processor | Every 6h cron / manual | Pick next batch, promote audits to contribution. v0.8.23: phase1 now skips promotion when every high-confidence finding sits on a "low-landing-rate" rule (`hits ≥ 20`, `contributed ≥ 5`, `merged/contributed < 0.15`, state not noisy/disputed). Calls `auditor/scripts/rule-health.py` once per run to compute the suppression set; fail-soft if it fails. Opt out via `NLPM_DISABLE_LOW_LANDING_SUPPRESSION=1`. The 2026-05-20 query found `BUG-broken-reference` + `BUG-missing-frontmatter` in this state — high verify_rate but zero direct merges; suppression catches them without touching the rulebook (refinement is the path for noisy/disputed rules; this is the orthogonal path for rules that diagnose correctly but PR badly). |
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

### Data (auditor/)

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

### The Loop

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

### Security Gate

The audit workflow includes a security scan BEFORE the NL quality audit:
1. Detects executable surfaces (hooks, scripts, MCP configs, dependencies)
2. Pattern-matches against Critical/High risk signatures (eval, curl-pipe-sh, credential exfil, etc.)
3. If Critical patterns found: labels issue `security-blocked`, skips contribution
4. The contribute workflow refuses to run if `security-blocked` label is present
5. Manual review required to clear the security gate

### Policy Gates (contribute workflow)

After security, the contribute workflow runs three org/repo-level policy
gates. All preserve the audit data and only skip PR creation.

| Gate | Trigger | Status set | Label | Recovery |
|------|---------|------------|-------|----------|
| no-external-PRs | Owner in `DENY_OWNERS` (currently `anthropics`) | `policy_denied` | `policy-no-external-prs` | Manual override only — permanent. |
| CLA-required (signature missing) | Owner in `CLA_REQUIRED_OWNERS` (Google's various orgs: `google`, `google-gemini`, `googleworkspace`, `google-labs-code`, `googleapis`, `googlecloudplatform`) **and** `vars.GOOGLE_CLA_SIGNED != 'true'` | `policy_cla_required` | `policy-cla-required` | Sign the individual CLA at <https://cla.developers.google.com/about>, set repo variable `GOOGLE_CLA_SIGNED=true`, set `CONTRIBUTE_AUTHOR_EMAIL` and `CONTRIBUTE_AUTHOR_NAME` to the CLA-signed identity, re-add `contribute-approved` on the audit issue. |
| CLA-required (author identity missing) | Owner in `CLA_REQUIRED_OWNERS` **and** `GOOGLE_CLA_SIGNED == 'true'` **but** `CONTRIBUTE_AUTHOR_EMAIL` or `CONTRIBUTE_AUTHOR_NAME` is empty | `policy_cla_required` | `policy-cla-required` | Set both repo variables to the CLA-signed human identity, re-add `contribute-approved`. |
| pushback-gated | Repo has any prior `maintainer_rejected` event, **or** any `pr_comments_snapshot` event with `pr_state: closed_unmerged`, in `auditor/logs/events.jsonl` | `pushback_gated` | `policy-pushback-gated` | Append a `gate_override` counter-event to `auditor/logs/events.jsonl` with the same `pr` value and a justification — only when the maintainer has explicitly invited a follow-up. |

Why three separate trigger rows: a signed CLA is necessary but not
sufficient. `claude-code-action`'s default commit identity is `claude[bot]
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

### Shared scripts (auditor/scripts/)

| Script | Purpose |
|--------|---------|
| log-event.sh | Append lifecycle events to events.jsonl |
| compute-fingerprint.sh | SCHEMAS §fingerprint formula, shared by audit + contribute + re-audit |
| diff-findings.py | Diff a re-audit's sidecar against the original, emit finding_verified / finding_introduced events and the case-study diff report; `--self-test` cross-checks Python fingerprint vs. the shell helper |
| guard-protected-paths.sh | Block stray edits to skills/, agents/ from automation commits |
| resolve-merge-conflicts.sh | Auto-resolve conflicts on append-only log pushes |
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

## nlpm.com (VitePress site)

The public site lives in `site/`. Built with VitePress; deployed to the
`gh-pages` branch which GitHub Pages publishes at <https://nlpm.com>.

- `site/index.md`, `site/install.md` — landing + install pages
- `site/.vitepress/config.ts` — site config (nav, sidebar, theme, search)
- `site/reference/*.md` — auto-generated from canonical SKILL.md sources
  by `bin/nlpm-build-reference-md` (pages: rules.md, principles.md,
  vocabulary.md, scoring.md, artifact-types.md, drift.md)
- `site/build.sh` — full build pipeline: regen reference, sync auditor
  outputs (`auditor/reports/*` → `site/public/`), `pnpm install`,
  `pnpm build`. Output: `site/.vitepress/dist/` (ignored).
- Auditor outputs (dashboard.html, 209 per-repo HTMLs, legacy
  single-page `docs/index.html`, `assets/`, `vendor/g6.min.js`) ride into
  the site as static passthrough from `site/public/`. Cross-references
  from reports continue to hit `/docs/index.html#R06` — the legacy
  single-page guide is kept on the site for backward compatibility.
- `pnpm-lock.yaml` is committed; `node_modules/`, `.vitepress/cache/`,
  `.vitepress/dist/`, `public/` are gitignored.

To rebuild locally:

```bash
bash site/build.sh
```

To deploy: copy `site/.vitepress/dist/.` into the `gh-pages` worktree,
commit, push. (Automated pipeline TODO; today it's a manual step.)

### Model pinning

One workflow pins a specific Claude model ID; the rest use the
claude-code-action default (currently Sonnet 4.6).

| Workflow | Model | Why pinned |
|----------|-------|------------|
| auditor-classify | `claude-haiku-4-5-20251001` | Bounded-enum classification is Haiku's sweet spot and ~10× cheaper than Sonnet for the same task |

When Anthropic retires the pinned model, update the ID and note the
migration in the commit message. All other workflows pick up model
upgrades automatically.

## Shared Memory

**Always write new instructions, rules, and memory to `AGENTS.md` only.**

Never modify `CLAUDE.md` or `GEMINI.md` directly — they only import `AGENTS.md`.
This keeps Claude Code, Codex CLI, and Gemini CLI on the same context.

## Project Structure

- `.claude/` — Claude Code skills, agents, rules, hooks, commands
- `.agents/skills/` — symlink to `.claude/skills/` (Codex skill scan path)
- `.codex/prompts/` — Codex slash-command prompts
- `.codex/hooks.json` / `.codex/config.toml` — Codex hooks/config (optional)
- `.gemini/skills/`, `.gemini/commands/` — Gemini skills and TOML commands
- `.mcp.json` — MCP server registrations (shared by all three tools)
