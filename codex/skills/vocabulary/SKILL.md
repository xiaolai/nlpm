---
name: vocabulary
description: Use when writing, reviewing, or naming any NLPM artifact (command, agent, skill, rule, workflow) — pick the canonical noun or verb from this registry rather than coining a synonym. Loaded by the scorer and checker agents to detect vocabulary drift across artifacts.
metadata:
  version: 0.1.0
---

# NLPM Domain Vocabulary

> The canonical noun-and-verb set NLPM uses to name what it does. Every artifact name, command name, agent name, rule wording, and prose description should draw from this registry. Synonyms are flagged by `/nlpm:check` and penalized by `/nlpm:score`.
>
> **Sister skill:** `nlpm:conventions` holds upstream Claude Code framework terms (hook events, frontmatter fields, manifest keys). This skill holds NLPM-internal domain language. If a term is from Anthropic's docs, it belongs in `conventions`. If it is from NLPM's own corpus, it belongs here.

---

## How this registry is built

Every term listed below has **literary warrant** — it appears in at least one NLPM artifact today, captured by `analysis/scripts/extract-vocabulary.py`. Re-run that script after adding or renaming artifacts; the freshest output lives at `analysis/vocabulary-extract/summary.md`. New terms enter the registry only after one of the four warrant types from `analysis/vocabulary-design-principles.md` (P6) is satisfied — literary warrant alone is the entry bar for terms already in use; new coinages need user, structural, or domain warrant.

---

## Two scopes (P1)

NLPM has two declared scopes. A homonym across them is a **boundary**, not a collision.

| Scope | Lives in | What it operates on |
|-------|----------|---------------------|
| **internal** | `commands/`, `agents/`, `skills/`, `bin/`, `scripts/`, project CLAUDE.md | NLPM's own behavior — scoring, checking, fixing, testing, listing, trending NL artifacts in the current project. |
| **auditor** | `.github/workflows/auditor-*.yml`, `auditor/` | The self-evolution pipeline that audits external repos, opens contribution PRs, tracks outcomes, refines rules. |

A verb that appears in both scopes (`scan`, `test`, `discover`) carries the same identity criterion in both — these are sanctioned homonyms. A verb that appears in only one scope (`audit`, `contribute`, `track` in auditor; `score`, `check`, `fix`, `ls`, `trend`, `init` in internal) is scope-bound; using it in the other scope requires either renaming or declaring a second scope-specific definition.

---

## Verbs

### Internal scope (NLPM commands)

| Canonical verb | Output | Judgment? | Examples in corpus |
|----------------|--------|-----------|--------------------|
| `score` | number + penalty list | no (deterministic) | `commands/score.md`, `agents/scorer.md` |
| `check` | consistency violation list | no (deterministic) | `commands/check.md`, `agents/checker.md` |
| `test` | pass/fail against named specs | no (deterministic) | `commands/test.md`, `agents/tester.md` |
| `scan` | pattern-match findings against a signature database | no (deterministic) | `commands/security-scan.md`, `agents/vague-scanner.md`, `agents/security-scanner.md` |
| `fix` | mutated artifact | no (mechanical) | `commands/fix.md` |
| `ls` | inventory of artifacts | no | `commands/ls.md`, `agents/scanner.md` |
| `trend` | history report | no | `commands/trend.md` |
| `init` | config file | no | `commands/init.md` |

**Deprecated synonyms (do not use in internal scope):**
- `lint`, `validate` → use `check` (structural) or `score` (quality)
- `find`, `search`, `list` → use `ls`
- `analyze` → use `score` (if quantitative) or pick a more specific verb
- `audit` → not in internal scope; live in auditor scope only

### Auditor scope (`.github/workflows/auditor-*.yml`, `auditor/scripts/`)

| Canonical verb | Output | Judgment? | Examples in corpus |
|----------------|--------|-----------|--------------------|
| `discover` | candidate-repo list | no | `auditor-discover.yml` |
| `audit` | composite quality + security report | **yes** | `auditor-audit.yml` |
| `contribute` | PR(s) to target repo | no | `auditor-contribute.yml` |
| `track` | outcome events appended to `events.jsonl` | no | `auditor-track.yml` |
| `classify` | categorical label on a PR comment | no (model-deterministic) | `auditor-classify.yml` |
| `refine` | rule-edit PR (human-gated) | no (LLM-generated, human-merged) | `auditor-refine-rules.yml` |
| `cite` | citation-edit PR (human-gated) | no | `auditor-cite-exemplars.yml`, `propose-rule-citations.py` |
| `diff` | finding-by-finding comparison | no | `diff-findings.py`, `auditor-docs-diff.yml` |
| `report` | rolled-up summary at a cadence | no | `auditor-daily-report.yml`, `generate-daily-report.py` |
| `review` | rule-review issue body (human reads, decides) | **yes** (human) | `auditor-rule-review.yml`, `generate-rule-review-body.py` |
| `propose` | a draft for human approval | no | `propose-rule-citations.py` |
| `validate` | yes/no on a structural rule | no | `validate-feedback.sh`, `validate-rule-ids.py` |

> **Sibling-granularity note (P1):** `report` is broader than its peers (`classify`, `refine`, `cite`, `diff`). The auditor's noun-named workflow convention absorbs this — workflows that produce reports are noun-named after the output (`auditor-daily-report`, `auditor-rule-review`), and the verb `report` is the generic act behind that family. Documented inconsistency, not a P1 violation; flagged here so future additions don't replicate the pattern without intent.

**Cross-scope homonyms (same meaning in both scopes):**
- `scan` — pattern-match against a signature database (used by `security-scan` command and `scan-suppressions.py`)
- `test` — pass/fail against named specs (used by `/nlpm:test` and `auditor-integration-test.yml`)
- `discover` — produce a candidate list (`/nlpm:ls` description text and `auditor-discover.yml`)

### Verbs proposed but not entered

Per the precedence order in `analysis/vocabulary-design-principles.md` (P6 last; warrant is an entry check, not a veto), proposed terms split into two lists.

**Deferred (P2–P5 satisfied; awaiting warrant):**

| Proposed verb | Closure gap or judgment named | Warrant needed |
|---------------|------------------------------|----------------|
| `triage` | Finding-disposition (P4 closure: `finding` has no consumer verb) | User warrant — practitioner reaches for the term unprompted |
| `review` (internal scope) | Human-in-the-loop reading, sanctioned cross-scope homonym with auditor `review` | User warrant — practitioner names a review act in internal artifacts |
| `rationalize` | Vocabulary curation (P5: act of picking canonical from extracted frequencies has no name) | User warrant — practitioner names the curation act |

Deferred terms are documented but not yet canonical. R51 does **not** flag them as deprecated — they are nameless gaps, not synonyms.

**Rejected by higher principle (no entry possible regardless of warrant):**

| Proposed verb | Blocking principle | Reason |
|---------------|--------------------|--------|
| `audit` (internal scope) | P1 | Merge test fails — `score`+`check` already cover internal-scope evaluation |
| `lint` (internal scope) | P1 | Synonym of `check`; same identity criterion |
| `validate` (internal scope) | P1 | Collapses to `check` in internal scope (canonical in auditor scope) |
| `analyze` (internal scope) | P1 | Synonym of `score`; quantitative evaluation |

---

## Nouns

### Artifact-class nouns (rigid; survive state changes)

| Canonical noun | What it is | Examples |
|----------------|------------|----------|
| `artifact` | any NL programming file Claude Code consumes | umbrella term |
| `command` | `commands/*.md`, invoked via `/<plugin>:<command>` | `commands/score.md` |
| `agent` | `agents/*.md`, invoked via Task tool with `subagent_type` | `agents/scorer.md` |
| `skill` | `skills/<plugin>/<name>/SKILL.md`, auto-loaded by description match | `skills/nlpm/rules/SKILL.md` |
| `rule` | a numbered item (R01–R50) inside the rules skill | inside `skills/nlpm/rules/SKILL.md` |
| `hook` | shell script wired via `hooks.json` | `hooks/hooks.json` |
| `manifest` | `plugin.json` or `marketplace.json` | `.claude-plugin/plugin.json` |
| `frontmatter` | YAML block delimited by `---` at the top of a Markdown file | every command, agent, skill |

**Sanctioned homonyms** (distinct senses, not drift — the drift scanner should
not cluster these against the canonical nouns above):

| Term | Sanctioned sense | Where |
|------|------------------|-------|
| `component` | a structural part of the *scored project's* codebase — code modules, directories, services; may not be NL artifacts at all | R35/R49 rule text ("component map"), `skills/nlpm/scoring/SKILL.md` R35 row |
| `issue` | a GitHub issue — the platform object the auditor opens, tracks, and closes | auditor scope: workflows, `auditor-rule-review.yml`, AGENTS.md auditor pipeline prose |

Everywhere else, `component` naming plugin pieces (command/agent/skill/hook)
and `issue` naming a detected problem are drift: the canonical nouns are
`artifact` and `finding`.

### Implementation-role nouns (P2/P3 — agent names ride alongside command verbs)

| Role-noun | Paired verb | File |
|-----------|-------------|------|
| `scanner` | `ls` | `agents/scanner.md` |
| `scorer` | `score` | `agents/scorer.md` |
| `checker` | `check` | `agents/checker.md` |
| `tester` | `test` | `agents/tester.md` |
| `vague-scanner` | `score` (sub-step) | `agents/vague-scanner.md` |
| `security-scanner` | `scan` | `agents/security-scanner.md` |

These are **not top-level verbs in their own right** (P3). They are role-names for sub-step agents. Treat them as nouns naming the worker, not as operations on artifacts.

### Output-class nouns (produced by verbs)

| Noun | Produced by | Notes |
|------|-------------|-------|
| `score` | `score` verb | number 0–100 + penalty breakdown |
| `finding` | `score`, `check`, `scan` | one problem detected; carries a fingerprint in auditor scope |
| `violation` | `check` | a finding specifically from cross-reference checking |
| `penalty` | `score` | the points subtracted by a single finding |
| `snapshot` | `score`, `trend` | a point-in-time record appended to `.claude/nlpm-history.json` |
| `inventory` | `ls` | the list of artifacts discovered in a path |
| `report` | `audit`, `report`, `trend` | a roll-up document |
| `spec` | `test` | a `.nlpm-test/*.spec.md` file defining expected behavior |

### Auditor-scope nouns (only meaningful inside `auditor/`)

| Noun | What it is | File evidence |
|------|------------|---------------|
| `case-study` | post-merge article comparing original audit to HEAD | `auditor/audits/<slug>.re-audit.md` |
| `exemplar` | teaching artifact from a high-scoring audit | `auditor/exemplars/<slug>.md` |
| `fingerprint` | content-hash identity of a finding across re-runs | `compute-fingerprint.sh` |
| `event` | one append-only record in `events.jsonl` | `auditor/logs/events.jsonl` |
| `disagreement` | self/maintainer dispute over a finding | `auditor/disagreements.jsonl` |
| `registry` | the tracked-repo database | `auditor/registry/repos.json` |
| `disposition` | a finding's lifecycle status | enum values inside `events.jsonl` |
| `policy gate` | a pre-PR check (no-external-PRs, CLA, pushback) | `auditor-contribute.yml` |

---

## The bright-line table (P1, P5)

When the evaluation cluster overlaps in practice, use this table to disambiguate:

| Verb | Scope | Deterministic? | Judgment? | Output | Use when |
|------|-------|----------------|-----------|--------|----------|
| `score` | internal | yes | no | number + penalty list | quantifying quality with a rubric |
| `check` | internal | yes | no | violation list | verifying cross-references and structural consistency |
| `test` | both | yes | no | pass/fail | comparing actual behavior against a named spec |
| `scan` | both | yes | no | findings against signatures | pattern-matching for a known class of problems |
| `audit` | auditor | partly | **yes** | composite report | full quality assessment that combines score + scan + judgment |
| `review` | auditor | no | **yes (human)** | comment trail | a human reads and forms an opinion |

Two verbs share a scope and an identity criterion ⇒ one must be retired or scope-split. Two verbs share an identity criterion across scopes ⇒ that is a sanctioned homonym (declare it in this table).

---

## How to extend this registry

1. **Add a term only if it has warrant.** The four warrant types come from `analysis/vocabulary-design-principles.md` P6: literary, user, structural, domain. Literary warrant is automatic via the extraction script — if the script picks the term up, it qualifies.
2. **Re-run the extraction script.** `python3 analysis/scripts/extract-vocabulary.py` writes `analysis/vocabulary-extract/summary.md`. New terms appear there.
3. **Slot the term.** Add a row to the right table above (internal verb / auditor verb / artifact-class noun / role-noun / output-class noun / auditor-scope noun).
4. **Cite the file evidence.** Every row has an "examples" or "file evidence" column. Cite at least one path.
5. **If retiring a synonym, list it under its canonical verb's "deprecated synonyms" line.** Do not silently drop terms; deprecation is itself a vocabulary act and needs to be visible.

---

## Deferred work (documented, not yet executed)

| Item | Why deferred | What unblocks it |
|------|--------------|------------------|
| Per-rule warrant tags on R01–R50 | Requires reading every rule + judging which warrant it earns its place by. User warrant data lives in `rule-health.py` outputs. | A separate `auditor-refine-rules` follow-up pass that combines rule-health data with this principle set. |
| Adding `triage` as a `/nlpm:triage` command | P4 closure gap is real but `triage` has zero literary warrant today. User warrant is the missing evidence. | A practitioner reaching for the word unprompted in actual NLPM use. |
| Resolving the agent-name-vs-command-name shadowing (`scanner`/`ls`, `scorer`/`score`) | Already documented above as a class boundary; no rename proposed. | A confirmed case of practitioner confusion. None observed today. |
| (resolved 2026-05-19) Workflow filename convention | Declared as sanctioned split. See "Auditor workflow filename convention" below. | — |

---

## Auditor workflow filename convention

`.github/workflows/auditor-*.yml` filenames follow a **two-rule split**, both sanctioned:

| Pattern | Use when | Examples |
|---------|----------|----------|
| `auditor-<verb>` | The workflow changes state (gates a transition, opens a PR, classifies, moves a finding through its lifecycle) | `auditor-audit.yml`, `auditor-contribute.yml`, `auditor-track.yml`, `auditor-classify.yml`, `auditor-refine-rules.yml`, `auditor-cite-exemplars.yml`, `auditor-discover.yml` |
| `auditor-<output-noun>` | The workflow's purpose is to produce a named artifact that downstream tooling consumes by name | `auditor-case-study.yml`, `auditor-exemplar.yml`, `auditor-daily-report.yml`, `auditor-suppressions.yml`, `auditor-docs-diff.yml`, `auditor-rule-review.yml` |

By P3, both patterns produce or gate, so both pass the top-level-verb test. The split is genuine: noun-named workflows are named after what they write, verb-named workflows after what they do.

**Outlier:** `auditor-batch-processor.yml` is named after a process role, not a verb or an output noun. Rename candidate: `auditor-promote-batch`. Deferred — git history, badge, and external references make the rename costly, and the existing name has literary warrant.

---

## Scope note

This skill loads on requests to write, review, or name NLPM artifacts. For framework-level facts (hook event names, manifest field schemas, Claude Code naming conventions), see [[conventions]]. For the 50 quality rules (R01–R50), see [[rules]]. For penalty tables, see [[scoring]].
