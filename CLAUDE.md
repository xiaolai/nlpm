# nlpm

Natural-Language Programming Manager for Claude Code.

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
- commands/shared/discover.md -- artifact discovery patterns (not user-invocable)
- commands/shared/classify.md -- artifact type classification (not user-invocable)

## Agents

- agents/scanner.md -- haiku, mechanical file discovery
- agents/scorer.md -- sonnet, 100-point quality scoring (skills: scoring, conventions)
- agents/checker.md -- sonnet, cross-component consistency (skills: conventions)
- agents/vague-scanner.md -- haiku, mechanical vague-word counting (no skills)
- agents/tester.md -- sonnet, evaluates artifacts against test specs (skills: testing, conventions, scoring)
- agents/security-scanner.md -- sonnet, security risk detection in executable artifacts (skills: security)

## Skills

### Core (loaded by agents)
- skills/nlpm/conventions/ -- Claude Code schemas, hook events, naming patterns
- skills/nlpm/patterns/ -- NL programming patterns + anti-patterns (cross-referenced to rules)
- skills/nlpm/scoring/ -- penalty tables with rule number cross-references
- skills/nlpm/rules/ -- the 50 Rules of Natural Language Programming (R01-R50) -- single source of truth
- skills/nlpm/testing/ -- NL-TDD spec format, test patterns
- skills/nlpm/security/ -- security pattern database for executable artifact scanning

### Writing Reference (loaded on demand)
- skills/nlpm/writing-skills/ -- how to write SKILL.md files
- skills/nlpm/writing-agents/ -- how to write agent definitions
- skills/nlpm/writing-rules/ -- how to write .claude/rules/ files
- skills/nlpm/writing-prompts/ -- universal prompt engineering guide
- skills/nlpm/writing-hooks/ -- how to write Claude Code hooks
- skills/nlpm/writing-plugins/ -- how to design and build plugins
- skills/nlpm/orchestration/ -- multi-agent workflow patterns

## Hooks

- hooks/hooks.json -- PostToolUse command hook on Write|Edit
- scripts/check-artifact.sh -- classifies written file, emits advisory only for NL artifacts

## Self-Tests

- .nlpm-test/ -- spec files for all 5 agents (dogfooding NL-TDD)

## Build & Run

No build step. Pure markdown plugin. Install with:
```
claude plugin install nlpm@xiaolai --scope project
```

Test by running `/nlpm:ls` on any project with NL artifacts.
Run `/nlpm:test` to verify agent specs pass.

## Prerequisites

None. No Python, Node.js, or compiled dependencies.

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

The `auditor/` subdirectory contains a GitHub Actions pipeline that discovers, audits, and contributes to Claude Code plugin/skill repos across GitHub — then feeds learnings back into NLPM's rules.

### Workflows (.github/workflows/auditor-*.yml)

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| auditor-discover | Weekly cron / manual | Find repos with 500+ stars and 5+ NL artifacts |
| auditor-batch-processor | Every 6h cron / manual | Pick next batch, promote audits to contribution |
| auditor-audit | Issue labeled `audit-ready` | Security scan + NL score; emits findings.jsonl + disagreements.jsonl |
| auditor-contribute | Issue labeled `contribute-approved` | Fork, PR for verified bugs; stamps PR body with `nlpm-metadata` block |
| auditor-track | Every 4h cron | PR state, emits finding_outcome + pr_comments_snapshot on transitions |
| auditor-case-study | Issue labeled `case-study-ready` | Write article, self-review, polish, cover image |
| auditor-daily-report | Daily cron | Pipeline state + per-rule health (healthy/noisy/dormant/disputed) |
| auditor-classify | Daily cron / manual | Haiku classifies `pr_comments_snapshot` → `maintainer_rejected` |
| auditor-suppressions | Weekly cron / manual | Scan public repos for NLPM rule-override configs |
| auditor-refine-rules | Weekly cron / manual | **Human-gated**: open PR with proposed rule edits (reviewer: xiaolai) |

### Data (auditor/)

| Path | Append-only | Purpose |
|------|-------------|---------|
| auditor/registry/repos.json | no | Tracking database |
| auditor/feedback/log.json | no | Rolling summary, derived from the three append-only logs |
| auditor/audits/<slug>.md | no | Per-repo human-readable scoring report |
| auditor/audits/<slug>.findings.jsonl | no | Per-audit findings sidecar, source for the global log |
| auditor/findings.jsonl | yes | One record per finding, joined by fingerprint |
| auditor/disagreements.jsonl | yes | self_false_positive, pr_comments_snapshot, maintainer_rejected, downstream_suppression |
| auditor/logs/events.jsonl | yes | Lifecycle events + finding_outcome + findings_aggregated |
| auditor/reports/ | no | Daily reports |

See `auditor/SCHEMAS.md` for the full record contracts.

### The Loop

```
discover → security scan → audit → contribute → track outcomes
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

### Security Gate

The audit workflow includes a security scan BEFORE the NL quality audit:
1. Detects executable surfaces (hooks, scripts, MCP configs, dependencies)
2. Pattern-matches against Critical/High risk signatures (eval, curl-pipe-sh, credential exfil, etc.)
3. If Critical patterns found: labels issue `security-blocked`, skips contribution
4. The contribute workflow refuses to run if `security-blocked` label is present
5. Manual review required to clear the security gate

### Shared scripts (auditor/scripts/)

| Script | Purpose |
|--------|---------|
| log-event.sh | Append lifecycle events to events.jsonl |
| compute-fingerprint.sh | SCHEMAS §fingerprint formula, shared by audit + contribute |
| guard-protected-paths.sh | Block stray edits to skills/, agents/ from automation commits |
| resolve-merge-conflicts.sh | Auto-resolve conflicts on append-only log pushes |
| parse-suppressions.py | Extract rule_overrides from NLPM config frontmatter |
| parse-pr-metadata.py | Extract `nlpm-metadata` block from a PR body on stdin |
| rule-health.py | Run SCHEMAS §Learning query, write feedback-summary.json |

### Model pinning

One workflow pins a specific Claude model ID; the rest use the
claude-code-action default (currently Sonnet 4.6).

| Workflow | Model | Why pinned |
|----------|-------|------------|
| auditor-classify | `claude-haiku-4-5-20251001` | Bounded-enum classification is Haiku's sweet spot and ~10× cheaper than Sonnet for the same task |

When Anthropic retires the pinned model, update the ID and note the
migration in the commit message. All other workflows pick up model
upgrades automatically.
