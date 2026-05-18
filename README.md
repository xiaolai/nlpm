# nlpm

[![Validated by NLPM](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/xiaolai/nlpm-for-claude/main/nlpm-badge.json)](https://github.com/xiaolai/nlpm-for-claude/blob/main/nlpm-badge.json)

Natural-Language Programming Manager -- discover, score, check, and fix NL artifacts with Claude-native intelligence.

Part of the [xiaolai Claude plugin marketplace](https://github.com/xiaolai/claude-plugin-marketplace).

NLPM is the only validator in the Claude Code plugin ecosystem that systematically checks **manifest-vs-disk consistency** — the bug class where a SKILL.md exists on disk but is silently missing from `plugin.json` (and therefore invisible after `claude plugin install`). Verified across 8+ tools including Anthropic's official `plugin-validator` and the Linux Foundation's `skills-ref`. See [`analysis/ecosystem-gap.md`](analysis/ecosystem-gap.md) for the research.

## What it does

NLPM treats natural language artifacts as **programs that can be linted**. Just as ESLint scores JavaScript and ruff scores Python, NLPM scores the markdown files that drive AI behavior: skills, agents, commands, rules, hooks, prompts, CLAUDE.md, and memory files.

Eight commands, each doing one thing:

| Command | What it does |
|---------|-------------|
| `/nlpm:ls` | Discover and inventory all NL artifacts in a repo |
| `/nlpm:score` | Score artifact quality (100-point scale) |
| `/nlpm:check` | Cross-component consistency checks |
| `/nlpm:fix` | Auto-fix fixable issues |
| `/nlpm:trend` | Track quality score trends over time |
| `/nlpm:test` | Run NL artifact tests against spec files (TDD) |
| `/nlpm:init` | Initialize NLPM for a project |
| `/nlpm:security-scan` | Scan plugins for security risks in executable artifacts |

Claude-native slash commands (no API keys, no Codex, no external models) plus a standalone Python 3.11+ validator for pre-commit hooks and CI.

## Installation

```bash
# Project scope (recommended)
claude plugin install nlpm@xiaolai --scope project

# Global (all projects)
claude plugin install nlpm@xiaolai --scope user
```

> **Install fails with "Plugin not found in marketplace 'xiaolai'"?** Your local marketplace clone is stale. Run `claude plugin marketplace update xiaolai` and retry — `plugin install` does not auto-refresh.

## Quick Start

In Claude Code:

```
/nlpm:ls                    # see what NL artifacts you have
/nlpm:score                 # score them all
/nlpm:score agents/         # score just agents
/nlpm:score --changed       # score only git-changed files
/nlpm:check                 # check cross-component consistency
/nlpm:fix                   # auto-fix what's fixable
/nlpm:trend                 # track score history over time
/nlpm:test                  # run NL-TDD specs
```

From CI or a pre-commit hook (no Claude Code required):

```bash
curl -fsSL -o /usr/local/bin/nlpm-check \
  https://raw.githubusercontent.com/xiaolai/nlpm-for-claude/main/bin/nlpm-check
chmod +x /usr/local/bin/nlpm-check
nlpm-check .               # exit 1 on high-confidence findings
```

## For plugin/skill authors — standalone validator

If you author a plugin and want NLPM in your **pre-commit hook, CI, or pre-publish gate**, use the standalone binary at [`bin/nlpm-check`](bin/nlpm-check). It's a single Python 3.11+ file with no external dependencies. It runs the deterministic subset of `/nlpm:check` — including the manifest-vs-disk consistency check that no other validator (Anthropic's official `plugin-validator`, Linux Foundation's `skills-ref`, third-party tools) currently covers.

```bash
# One-line install
curl -fsSL -o /usr/local/bin/nlpm-check \
  https://raw.githubusercontent.com/xiaolai/nlpm-for-claude/main/bin/nlpm-check
chmod +x /usr/local/bin/nlpm-check

# Run in your plugin repo
nlpm-check .
```

Templates ship in [`templates/`](templates/):
- `pre-commit-nlpm.sh` — drop-in git pre-commit hook
- `workflows/nlpm-check.yml` — drop-in GitHub Actions workflow

See [`docs/for-authors.md`](docs/for-authors.md) for the full author guide. See [`analysis/ecosystem-gap.md`](analysis/ecosystem-gap.md) for the research on why this check exists and which other validators do (and don't) cover it.

## Scoring System

Scores start at 100 and go down. Every issue has a fixed penalty. The score is deterministic: same artifact, same penalties, same number.

| Score | Band | Meaning |
|-------|------|---------|
| 90-100 | Excellent | Production-ready |
| 80-89 | Good | Minor gaps |
| 70-79 | Adequate | Meets threshold, should improve |
| 60-69 | Weak | Below threshold |
| <60 | Rewrite | Fundamental problems |

Default pass threshold: 70. Configure in `.claude/nlpm.local.md`.

See `skills/nlpm/scoring/SKILL.md` for the full penalty tables. See `skills/nlpm/rules/SKILL.md` for the 50 Rules of Natural Language Programming.

## What it scores

13 artifact types across 3 categories:

| Category | Artifacts |
|----------|-----------|
| A: Plugin | commands, shared partials, agents, skills, hooks, plugin.json, .mcp.json |
| B: Project | CLAUDE.md, .claude/rules/, settings files |
| F: Memory | ~/.claude/projects/*/memory/*.md |

## NL-TDD

Write test specs BEFORE writing artifacts:

```
1. Write spec:    .nlpm-test/my-agent.spec.md
2. /nlpm:test     -> RED (artifact doesn't exist)
3. Write artifact: agents/my-agent.md
4. /nlpm:test     -> check trigger accuracy, output format, score
5. /nlpm:score    -> verify quality score
6. Iterate        -> fix until GREEN
```

See `skills/nlpm/testing/SKILL.md` for the full spec format.

## Configuration

Create `.claude/nlpm.local.md` (or run `/nlpm:init`):

```yaml
---
strictness: standard
score_threshold: 70
rule_overrides:
  R09: { min_examples: 1 }      # require only 1 example block
  R05: { threshold: 600 }       # allow skills up to 600 lines
  R23: { budget: 800 }          # increase rules budget
---
```

| Level | Threshold | Effect |
|-------|-----------|--------|
| Relaxed | 60 | Only flag seriously broken artifacts |
| Standard | 70 | Flag artifacts that need improvement |
| Strict | 80 | Flag anything below good quality |

## Continuous Enforcement

NLPM ships a `PostToolUse` hook that fires when you write or edit files. A shell script (`scripts/check-artifact.sh`) classifies the file -- if it's an NL artifact, Claude reminds you to run `/nlpm:score`. Non-NL files produce no output.

This is advisory -- it does not block writes. For blocking enforcement, use a `PreToolUse` hook (see tdd-guardian for an example).

## Architecture

```
commands/           User-facing commands (8 + 2 shared partials)
  ls.md             Discover artifacts -> dispatches scanner
  score.md          Score quality -> dispatches scorer + vague-scanner in parallel
  check.md          Cross-component checks -> dispatches checker
  fix.md            Auto-fix issues -> dispatches scorer
  trend.md          Track score history -> dispatches scorer + vague-scanner
  test.md           Run NL-TDD specs -> dispatches tester
  init.md           Configure project
  security-scan.md  Scan plugins for security risks -> dispatches security-scanner
  shared/
    discover.md     Artifact path patterns (not user-invocable)
    classify.md     Type classification rules (not user-invocable)

agents/             Dispatched by commands (6 agents)
  scanner.md        haiku -- fast artifact discovery
  scorer.md         sonnet -- 100-point quality scoring
  checker.md        sonnet -- cross-component consistency
  vague-scanner.md  haiku -- mechanical vague-word counting
  tester.md         sonnet -- evaluates artifacts against test specs
  security-scanner.md sonnet -- security risk detection in executable artifacts

skills/nlpm/        Knowledge base (13 skills)

  Core (loaded by agents):
  conventions/      Claude Code schemas, hook events, naming patterns
  patterns/         NL programming best practices + anti-patterns
  scoring/          Penalty tables with rule number cross-references
  rules/            The 50 Rules of Natural Language Programming (R01-R50)
  testing/          NL-TDD spec format, test patterns
  security/         Security pattern database for executable artifact scanning

  Writing Reference (loaded on demand):
  writing-skills/   How to write SKILL.md files
  writing-agents/   How to write agent definitions
  writing-rules/    How to write .claude/rules/ files
  writing-prompts/  Universal prompt engineering guide
  writing-hooks/    How to write Claude Code hooks
  writing-plugins/  How to design and build plugins
  orchestration/    Multi-agent workflow patterns

hooks/
  hooks.json        PostToolUse advisory (command type + check-artifact.sh)

scripts/
  check-artifact.sh NL artifact classifier for the PostToolUse hook

.nlpm-test/         Self-test specs (dogfooding NL-TDD)

bin/                Standalone author surface (v0.8.0+)
  nlpm-check        Pure-Python validator for pre-commit / CI / pre-publish

tests/              Python unittest suite for bin/nlpm-check
  test_nlpm_check.py

templates/          Drop-in author templates
  pre-commit-nlpm.sh             git pre-commit hook
  workflows/nlpm-check.yml       GitHub Actions workflow

docs/
  for-authors.md    Full guide for plugin/skill authors

analysis/
  ecosystem-gap.md                  Why this validator exists (stable ref)
  scope-expansion-2026-05.md        Author-surface plan
  2026-05-11-why-obvious-bugs-persist.md   Original research snapshot

auditor/            Self-evolution pipeline (GitHub Actions + data)
  audits/           Per-repo audit reports and findings sidecars
  findings.jsonl    Append-only audit findings (joined by fingerprint)
  logs/events.jsonl Lifecycle events + outcome signals
  registry/         Repo tracking database
  scripts/          Shared GHA helpers
  prompts/          Shared rubric prompts
  reports/          Daily pipeline reports
```

## Tips

- **Score early, score often.** Run `/nlpm:score` after writing any new artifact.
- **Use `--changed` for speed.** `score --changed` only scores git-modified files.
- **Use `/nlpm:trend` before releases.** Catches regressions that individual scoring misses.
- **Do not chase 100.** 85+ is excellent. The last 5-10 points are diminishing returns.
- **R01 is the most common penalty.** "appropriate", "relevant", "as needed" each cost -2. Replace with measurable criteria.
- **Auto-fix handles the mechanical stuff.** Focus your energy on descriptions, examples, and scope notes.
- **Pre-commit + slash commands together.** Run `nlpm-check` in your pre-commit hook for the deterministic checks; let `/nlpm:score` handle the judgment calls inside Claude Code.

## Troubleshooting

**"Score seems too low"** -- Check which penalties hit. Scoring is deterministic. Vague quantifiers stack up fast.

**"Writing skill didn't load"** -- Use keywords from the skill's description: "write an agent definition", "create a new agent".

**"Check found orphans that aren't really orphans"** -- Writing skills are on-demand (loaded by Claude, not referenced by agents). This is expected.

**"Trend shows no history"** -- Run `/nlpm:score` first to create the baseline snapshot.

## Case Studies

25+ case studies in [`case-studies/`](case-studies/) from the auditor pipeline. A few representative ones:

- [The frontmatter tax: 19 silent registration failures in a 33,000-star plugin collection](case-studies/2026-04-24-wshobson-agents.md) — `wshobson/agents`, 100 artifacts sampled of 509, 5 PRs batched and agentically merged in 13 seconds. (Companion [learnings debrief](case-studies/2026-04-18-wshobson-agents-learnings.md).)
- [Four bytes of quoting, approved by two OpenAI engineers](case-studies/2026-04-07-openai-codex-plugin-cc.md) — `openai/codex-plugin-cc`, 93/100 Gold tier, two shell-injection fixes merged by OpenAI contributors in 39 hours.
- [Auditing kubesphere/kubesphere](case-studies/2026-05-07-kubesphere-kubesphere.md) — 16k-star repo, 18 findings including duplicate sections and broken YAML, surfaced by manifest-vs-disk and cross-component checks the other validators don't run.
- [When the Linter Met Its Match](case-studies/2026-04-06-how-we-helped-gsd.md) — `gsd-build/get-shit-done`, 80 files scored, 5 PRs accepted, plus the false-positive that improved NLPM itself.

## Effectiveness

As of 2026-05-18 the auditor pipeline has filed 278 PRs across 49 distinct repos, with a 71% acceptance rate (97 merged + 20 applied-separately, 48 rejected, 113 still open). The following data points are the highest-signal:

- **`google-gemini/gemini-skills`** and **`googleworkspace/cli`** — both Google orgs that originally CLA-blocked the pipeline — ended up accepting work: 2 merged and 4 applied-separately respectively, once the CLA gate was satisfied.
- **`openai/codex-plugin-cc`** has 2 merges — first-party OpenAI org acceptance.
- **`kubesphere/kubesphere`** (24k+ stars) accepted 5 PRs — the highest-profile downstream.
- 8 repos (`zubair-trabzada/geo-seo-claude`, `wshobson/agents`, `sickn33/antigravity-awesome-skills`, `kubesphere/kubesphere`, `jeremylongshore/claude-code-plugins-plus-skills`, `Jeffallan/claude-skills`, `hesreallyhim/awesome-claude-code`, `caliber-ai-org/ai-setup`) each hit the per-repo PR cap of 5 — more PRs could ship if the cap were raised.
- 2 repos have crossed into **rule-adoption** (maintainer credited NLPM in CHANGELOG or systemically backfilled siblings): [`jeremylongshore/claude-code-plugins-plus-skills`](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/blob/main/CHANGELOG.md) and [`sickn33/antigravity-awesome-skills`](https://github.com/sickn33/antigravity-awesome-skills/blob/main/CHANGELOG.md).

## Auditor — Self-Evolution Pipeline

The `auditor/` directory contains a GitHub Actions pipeline that systematically discovers, audits, and contributes to Claude Code repos across GitHub. Learnings feed back into NLPM's rules.

```
discover (weekly) → audit → contribute PRs → track merges → write case study
                                                    ↓
                                           feedback/log.json
                                                    ↓
                                         update NLPM rules → audit better
```

13 workflows in [`.github/workflows/auditor-*.yml`](.github/workflows/): discover, batch-processor, audit, contribute, track, case-study, classify, daily-report, suppressions, refine-rules, docs-diff, rule-review, integration-test. Human-in-the-loop via issue labels at the audit, contribute, and rule-refinement decision points.

See [auditor/README.md](auditor/README.md) for the full pipeline documentation and [auditor/SCHEMAS.md](auditor/SCHEMAS.md) for the data contracts.

## Prerequisites

- **Slash commands (`/nlpm:*`)**: none. Pure markdown — no Python, no Node.js.
- **Standalone `bin/nlpm-check`**: Python 3.11+ (stdlib only; no pip install).
- **Auditor workflows**: `CLAUDE_CODE_OAUTH_TOKEN`, `PAT_TOKEN`, and `OPENAI_API_KEY` GitHub repo secrets.

## License

ISC
