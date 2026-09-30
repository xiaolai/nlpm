# nlpm component inventory

Per-component reference moved out of `AGENTS.md` so the memory file stays instruction-first. The architecture summary and the rules for changing components are in `AGENTS.md` § Architecture; this file lists every command, agent, skill, hook and author-surface file with its role.

## Commands

- commands/ls.md -- `/nlpm:ls` -- discover NL artifacts (dispatches scanner)
- commands/score.md -- `/nlpm:score` -- 100-point quality scoring (dispatches scorer + vague-scanner in parallel)
- commands/check.md -- `/nlpm:check` -- cross-artifact consistency (dispatches checker)
- commands/fix.md -- `/nlpm:fix` -- auto-fix mechanical findings (dispatches scorer)
- commands/trend.md -- `/nlpm:trend` -- track score history over time (dispatches scorer + vague-scanner)
- commands/test.md -- `/nlpm:test` -- run NL-TDD specs (dispatches tester)
- commands/init.md -- `/nlpm:init` -- init project
- commands/security-scan.md -- `/nlpm:security-scan` -- scan plugin for security risks in executable artifacts
- commands/vocab-init.md -- `/nlpm:vocab-init` -- init a vocabulary skill for any project (runs extractor, seeds canonical noun/verb tables, writes R51 opt-in stub). Adopter-facing entry point for vocabulary discipline.
- commands/vocab-drift.md -- `/nlpm:vocab-drift` -- registry-free vocabulary drift scan (dispatches vocab-drift-scanner). Advisory only; no penalty. Use before/alongside R51.
- commands/report.md -- `/nlpm:report` -- self-contained HTML report (per-file scores, trend, cross-artifact graph, vocabulary noun-verb map via AntV G6, drift candidates, findings). Output: `.claude/nlpm-reports/index.html`. file://-openable, no server.
- commands/spec-sync.md -- `/nlpm:spec-sync` -- sync the tool overlays (conventions-claude/codex/antigravity) with upstream official specs (dispatches spec-researcher per tool in parallel; applies corrections, propagates for self-consistency, verifies via bin/nlpm-check). Never commits/pushes.
- commands/shared/discover.md -- artifact discovery patterns (not user-invocable)
- commands/shared/classify.md -- artifact type classification (not user-invocable)
- commands/shared/append-history.md -- snapshot persistence to .claude/nlpm-history.json with scope marker (not user-invocable). Used by /nlpm:init, /nlpm:score, /nlpm:trend so trend data accumulates without manual upkeep.

## Agents

- agents/scanner.md -- haiku, mechanical artifact discovery
- agents/scorer.md -- sonnet, 100-point quality scoring (skills: scoring, conventions, conventions-claude, conventions-codex, conventions-antigravity, vocabulary)
- agents/checker.md -- sonnet, cross-artifact consistency (skills: conventions, conventions-claude, conventions-codex, conventions-antigravity, vocabulary)
- agents/vague-scanner.md -- haiku, mechanical vague-word counting (no skills)
- agents/tester.md -- sonnet, evaluates artifacts against test specs (skills: testing, conventions, scoring)
- agents/security-scanner.md -- sonnet, security risk detection in executable artifacts (skills: security)
- agents/vocab-drift-scanner.md -- sonnet, judgment-based clustering of likely-synonymous nouns/verbs across a corpus; no registry required (skills: vocabulary, conventions). Output is advisory only.
- agents/spec-researcher.md -- sonnet, research-and-diff one tool's current official docs against an overlay; returns a tagged gap report (FIX/REMOVE/ADD/CONFIRM/RESOLVED) with a confidence guard. Read-only on web and repo; never edits (tools: Read, Glob, Grep, WebFetch, WebSearch).

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
