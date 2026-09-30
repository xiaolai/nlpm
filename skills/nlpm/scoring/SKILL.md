---
name: scoring
description: "Use when scoring NL artifact quality, applying penalties, or calibrating lint judgment — contains the 100-point rubric with penalty tables per artifact type; tables for Codex, Antigravity, memory-file and workflow-program artifacts live in `references/` (indexed under Penalty Tables). Four worked calibration examples (Excellent Agent / Rewrite Agent / Excellent Rule / Weak Rule) live in `references/calibration-examples.md`, loaded on demand when anchoring borderline cases."
version: 0.4.0
user-invocable: false
---

# NLPM Quality Scoring Rubric

100-point quality scale for all NL programming artifacts. Apply penalties deterministically. Use calibration examples to anchor judgment on borderline cases.

---

## Scoring Formula

```
base_score = 100
adjustments = sum of all applicable penalties (all penalties are negative)
final_score = max(0, min(100, base_score + adjustments))
```

Penalties stack. The floor is 0; the ceiling is 100. No bonuses — the default assumption is that an artifact is well-formed, and quality is measured by what is missing or wrong.

---

## Penalty Tables

The tables in this file cover every artifact type a Claude Code project contains. Tables for the remaining artifact types live in `references/`, one file per group. When the artifact you are scoring is listed below, Read that file and apply its tables as if they appeared here — they carry the same weight, and a finding cited to one of their rows is a rubric finding.

| Artifact being scored | Read |
|---|---|
| Codex hook events; `.codex-plugin/plugin.json`; `.agents/plugins/marketplace.json`; `agents/openai.yaml`; `.codex/config.toml` | [`references/codex.md`](references/codex.md) |
| Antigravity / Gemini-lineage hook events; `gemini-extension.json`; `.gemini/commands/*.toml` | [`references/antigravity.md`](references/antigravity.md) |
| Memory files (`~/.claude/projects/*/memory/*.md`); agent workflow programs (project-root `program.md`-style files) | [`references/memory-and-workflow.md`](references/memory-and-workflow.md) |

The universal Hooks checks below apply to Codex and Antigravity hook configs too.

### Skills

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| -- | `name` present | Missing | -25 |
| -- | `name` matches parent directory | Frontmatter `name:` value does not equal parent directory name (per `nlpm:conventions` §5 — open spec MUST) | -15 |
| R04 | `description` present | Missing | -25 |
| R04 | Trigger quality | Description is generic (≤1 specific phrase) | -15 |
| R04 | Description length | Description 500–800 chars | -5 |
| R04 | Description length | Description >800 chars | -10 |
| R05 | Body length | 400–500 lines | -5 |
| R05 | Body length | >500 lines | -10 |
| R06 | Code examples | Complex concepts with no examples | -5 |
| R06 | Code examples | No examples at all in a technical skill | -10 |
| R06 | `<example>` blocks | Zero `<example>` blocks on a user-invocable skill (`user-invocable` absent or `true`) | -10 |
| R07 | Scope note | No scope note / cross-references | -3 |

> **Scope-note discipline:** R07 means "scope note when related skills exist."
> Do NOT apply R07 to missing example blocks — that is the new R06 row above
> (penalty -10, not -15). The 2026-05-13 lijigang/ljg-skills audit applied
> R07 + −15 fourteen times for missing example blocks; both labels were
> wrong (R07 is not example-related, and -15 is the agents penalty, not
> the skills penalty). The validator at `auditor/scripts/validate-rule-ids.py`
> catches this kind of drift in CI.

> **`<example>`-block counting discipline** (added 2026-08-01, origin:
> xiaolai/cc-suite v1.3.1 remediation): an `<example>` block counts only when
> it sits outside fenced code blocks — in the body or in a frontmatter
> description block scalar. Tags inside a fenced template (` ```markdown … ``` `)
> are illustrative content, and prose that names the string `` `<example>` ``
> is a mention, not a block. A 2026-07-31 scoring pass credited a skill with
> example blocks that existed only inside a fenced template, hiding a real R06
> violation across 13 files. Verify by reading the file, not by grepping for
> the tag.

> **`name` matches parent directory** (added 2026-05-25, audit:
> google/skills): the open Agent Skills spec at agentskills.io makes this
> a MUST. Mismatch is deterministic, high-confidence, and reproducible by
> single-line diff (frontmatter `name:` vs `basename($(dirname FILE))`).
> Mark such findings `confidence: high` per the manifest-vs-disk-diff
> principle in `agents/scorer.md` step 6. Note: this penalty did not
> exist before 2026-05-25 — re-scoring past audits will yield slightly
> lower scores for any corpus containing this defect, but no contribute
> outcomes are retroactively affected since no PRs were ever opened
> against a name-mismatch finding under the prior rubric.

---

### Agents

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R09 | `description` present | Missing | -25 |
| R09 | `<example>` blocks | Zero `<example>` blocks in the description | -15 |
| R09 | Exclusion clause | Description names no situation the agent is not for (a "Not for …"/"Do not use …" sentence, or an example where the assistant declines or routes elsewhere) | -5 |
| R09 | Description length | Description value over 1,200 characters, examples included | -5 |
| R10 | `model` declared | Not declared | -5 |
| R10 | `model` appropriate | Wrong tier for task (e.g. opus for parsing) | -5 |
| R11 | `tools` declared | Not declared | -5 |
| R11 | Unused tools | Each tool declared but not used in body | -3 each |
| R12 | Output format | No output format spec in body | -10 |
| R11 | Write on read-only | Audit/review/scan agent declares Write or Edit | -10 |

> **R09 example budget** (changed in 1.4.0): one `<example>` block is full
> credit. An agent's `description` sits in the Agent tool's text on every turn
> and is the only thing Claude sees when choosing an agent, so examples stay in
> the description — moving them into the body hides them from routing. One
> well-chosen example plus an explicit exclusion ("Not for …") carries the
> routing signal at a fraction of the tokens; extra examples are allowed but
> cost always-on context, which is why R09 deducts 5 points when the
> description exceeds 1,200 characters.

> **`min_examples` override** (`R09: { min_examples: N }` in the project's
> `nlpm.local.md`, see `nlpm:conventions` §6): with N greater than 1, a
> description that has at least one but fewer than N `<example>` blocks costs
> -5 per missing block, capped at -15 so that a partial set never costs more
> than none; zero blocks stays -15. The exclusion-clause and length rows are
> unchanged. Without the override, N is 1 and the rows above apply as written.

---

### Commands

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| -- | `description` present | Missing | -25 |
| R18 | `argument-hint` present | Command takes input but no hint | -5 |
| R14 | Steps numbered | Multi-step body with no numbered steps | -10 |
| R15 | Empty input handling | No handling for empty/missing input | -10 |
| R16 | Output format | No output format defined | -10 |
| R17 | Error paths | No error handling for missing files or bad data | -5 |

---

### Shared Partials

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R19 | `user-invocable: false` | Missing or set to true | -25 |
| R20 | Purpose clear | Description doesn't state it's a partial | -10 |

---

### Rules

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R21 | `description` present | Missing frontmatter description | -10 |
| R21 | Format: bold imperative | No bold imperative opening | -5 |
| R21 | Format: rationale | No rationale following the imperative | -10 |
| R22 | Enforceability | Rule is not specific/testable | -10 |
| R23 | Budget | Rule file over 500 lines | -15 |
| R26 | Conflicts with other rules | Direct contradiction with another rule in same set | -20 |
| R24 | Duplicates tooling | Re-states what eslint/ruff/clippy already catches | -10 |

---

### Hooks — universal checks (apply to all tools)

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| -- | Valid syntax | Hook config file fails to parse (JSON or TOML per tool) | -25 |
| R29 | Scripts exist | Referenced script file does not exist | -20 |
| -- | Command safety | Hook command contains dangerous patterns (`rm -rf`, `git push --force`, `DROP TABLE`) | -15 |
| -- | Matcher regex valid | Matcher pattern doesn't compile as valid regex | -10 |
| -- | Timeout reasonable | Hook specifies timeout > 30s (likely hangs) | -5 |

### Hooks (Claude Code — Tier 2-Claude only)

Authoritative event list: `nlpm:conventions-claude` §7 together with its extended allow-list in `conventions-claude/reference.md`. Per the multi-tool design (`analysis/multi-tool-design-2026-05.md` decision #4), Claude / Codex / Antigravity hook event vocabularies are NOT 1:1 mappable — three separate tables, no translation. The Codex and Antigravity tables are in `references/codex.md` and `references/antigravity.md`.

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R27 | Event names valid (Claude) | Uses an event name that is in neither the `nlpm:conventions-claude` §7 table nor its extended allow-list (`conventions-claude/reference.md`, Hook Events). Those two lists together are the confirmed set (33 events, including `SubagentStop`, `SubagentStart`, `PreCompact` and `Notification`); a name missing from both still passes if `code.claude.com/docs/en/hooks.md` documents it | -15 |
| R27 | Case correct (Claude) | Event name has wrong case (e.g. `pretooluse`) | -10 |
| -- | Hook type valid (Claude) | Uses unrecognized `type` value — confirmed Claude types: `command`, `http`, `mcp_tool`, `prompt`, `agent` | -10 |
| -- | MCP matcher format (Claude) | Matcher targets MCP tool but doesn't use `mcp__<server>__<tool>` pattern | -5 |

---

### plugin.json (Claude Code — `.claude-plugin/plugin.json`)

| Check | Condition | Penalty |
|-------|-----------|---------|
| `name` present | Missing | -25 |
| `version` is semver | Present but not valid semver | -10 |
| `description` present | Missing | -5 |

---

### .claude-plugin/marketplace.json (Claude Code — Tier 2-Claude)

Schema reference: `nlpm:conventions-claude` §17 and its `reference.md` (Plugin Distribution).

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid JSON | File fails JSON parse | -25 |
| `name` present | Missing | -25 |
| `owner.name` present | `owner` missing, or it has no `name` | -10 |
| `plugins` array present | Missing or empty | -10 |
| Per-plugin `name` and `source` | Either missing | -10 each |
| Per-plugin `source` valid | A relative path that doesn't start with `./` (bare names are valid only under `metadata.pluginRoot`), or an object whose `source.source` isn't one of the six object types in `reference.md` or that lacks that type's required field | -10 each |
| Per-plugin `version` in step | Differs from the `version` in the `plugin.json` it describes, when that file is in the same repository (`plugin.json` wins at load, so the entry is stale) | -5 each |
| Per-plugin `description` present | Missing (the `/plugin` browser shows it) | -3 each |

---

### .mcp.json (Claude Code — `.mcp.json` at repo root)

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid JSON | File fails JSON parse | -25 |
| Server `command` present | MCP server entry missing `command` field | -15 |

---

### .lsp.json (Claude Code LSP — Tier 2-Claude)

Schema details: `nlpm:conventions-claude` §12. Stable in 2026.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid JSON | File fails JSON parse | -25 |

---

### monitors/monitors.json (Claude Code monitors — Tier 2-Claude)

Schema details: `nlpm:conventions-claude` §13. Stable in 2026.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid JSON | File fails JSON parse | -25 |

---

### Settings Files (.claude/settings.json, .claude/settings.local.json)

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid JSON | File fails JSON parse | -25 |
| No hardcoded secrets | Contains API keys, tokens, or passwords | -25 |
| Permission mode sanity | `bypassPermissions` enabled in a shared project settings file (not .local) | -15 |
| Recognized keys | Contains unknown top-level keys not in Claude Code schema | -5 each, cap -15 |
| Hook definitions valid | `hooks` key present — check event names valid and case-correct | -10 per invalid |

---

### CLAUDE.md

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R49 | File exists | Neither AGENTS.md nor CLAUDE.md in plugin root | -10 |
| -- | Under 200 lines | CLAUDE.md exceeds 200 lines | -5 |
| R38 | Actionable content | CLAUDE.md has no actionable guidance (just filler) | -10 |
| R33 | Build/run command | No instructions for how to build or run the project | -10 |
| R34 | Test command | No instructions for how to run tests | -5 |
| R35 | Architecture overview | No structure/component description (what lives where) | -5 |
| R36 | Valid `@` imports | Contains `@` import syntax referencing a file that doesn't exist | -10 |
| R37 | No stale file references | Mentions files or functions that no longer exist in the repo | -10 |
| R38 | Actionability ratio | >60% of content is description rather than instructions | -5 |
| -- | Prerequisites section | No section covering required tools, versions, or setup steps | -5 |
| R39 | No rule conflicts | CLAUDE.md says X while a `.claude/rules/` file says not-X | -15 |

---

### All Artifact Types: Vague Quantifiers

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R01 | Vague quantifier | Each occurrence of: "appropriate", "relevant", "as needed", "sufficient", "adequate", "reasonable", "properly", "correctly", "some", "several", "various" without measurable criteria | -2 each |
| R01 | Vague quantifier cap | Total vague quantifier penalty | max -20 |

> **Mention-versus-use exclusion** (added 2026-08-01, origin: xiaolai/cc-suite
> audit-family false positives; design reviewed via Codex consultation): do not
> count a vague term when it is presented as a literal token AND the containing
> clause explicitly instructs the reader or a tool to detect, flag, reject,
> replace, avoid, or report that term — audit tooling must be able to name the
> words it hunts (e.g. ``Flag uses of `some`, `several`, `various` without
> concrete criteria`` is R01's own job description, not a violation). Backtick
> or quotation formatting alone does NOT qualify: a term that still modifies an
> action, criterion, or requirement is counted even when backticked —
> ``handle errors `properly` `` remains a violation.

---

### All Artifact Types: Vocabulary Drift (R51 — opt-in, disabled by default)

Applied only when `R51: { enabled: true, vocabulary_skill: <path> }` appears in `.claude/nlpm.local.md`. Without the opt-in, R51 contributes zero penalty regardless of artifact content. The configured `vocabulary_skill` must contain a `registry.yaml` listing canonical and deprecated terms; without it, R51 emits an advisory and contributes zero penalty.

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R51 | Deprecated synonym | Each occurrence of a term marked `deprecated:` in the project's `registry.yaml`, in the scope the artifact belongs to | -2 each |
| R51 | Drift cap | Total R51 penalty | max -10 per file |
| R51 | Missing registry | `enabled: true` but `vocabulary_skill:` not set or points to a directory with no `registry.yaml` | 0 (advisory only) |

> **Why opt-in:** vocabulary discipline is high-leverage for projects with accumulated drift but premature for projects still discovering their domain. Each project decides when it has enough literary warrant (P6) to lock terms in. See `analysis/vocabulary-design-principles.md` for the six principles R51 operationalizes.

> **Registry-declaration exclusion** (added 2026-08-01, origin: xiaolai/cc-suite
> vocabulary-skill self-reference; design reviewed via Codex consultation): the
> file that declares a deprecation must name the deprecated term to do so.
> Within the configured `vocabulary_skill` path, do not count a deprecated term
> where it occurs in the declaration that registers it or maps it to its
> replacement — `registry.yaml` `deprecated:` lists and the SKILL.md deprecation
> tables. The exclusion covers ONLY those declaration term fields: deprecated
> terms in surrounding prose inside the `vocabulary_skill` path are counted, and
> the path is not categorically exempt. The same mention-versus-use principle as
> R01's exclusion above, applied to R51.

---

### Cross-Artifact (--plugin flag)

Applied when linting an entire plugin rather than individual files.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Broken partial refs | Command references `commands/shared/X.md` that doesn't exist | -20 |
| Broken skill refs | Agent references `plugin:skill` that isn't installed | -20 |
| Missing scripts | Hook references script that doesn't exist | -20 |
| Orphaned files | Agent/command/skill file not referenced by anything | -5 per file |
| Contradictions | Two rules/instructions in same plugin directly contradict each other | -15 per pair |

---

## Score Bands

| Range | Label | Meaning |
|-------|-------|---------|
| 90–100 | Excellent | Production-ready; minor or no findings |
| 80–89 | Good | Solid; one or two non-critical gaps |
| 70–79 | Adequate | Meets threshold; noticeable gaps to address |
| 60–69 | Weak | Below threshold; significant findings |
| <60 | Rewrite | Fundamental problems; recommend rewriting from scratch |

**Default pass threshold:** 70. Configurable in `.claude/nlpm.local.md`.

---

## Calibration Examples

Four worked examples — *Excellent Agent (97)*, *Rewrite Agent (41)*, *Excellent Rule (92)*, *Weak Rule (41)* — live in [`references/calibration-examples.md`](references/calibration-examples.md). Load that file on demand when scoring a borderline case (around band boundaries: 88-92, 68-72, 58-62) and you need an anchored reference.

The examples are not needed for routine scoring — the penalty tables (above, plus the per-tool reference files indexed under Penalty Tables) are self-contained. They were extracted from this file 2026-05-28 to keep the rubric under R05's 500-line body budget while preserving the calibration material verbatim.

---

## Scope Note

This skill covers the NLPM scoring formula, penalty tables, score bands, and calibration examples. It does NOT cover:
- Artifact schemas and valid field values → see `nlpm:conventions` (universal) and the tool-specific overlays `nlpm:conventions-claude`, `nlpm:conventions-codex`, `nlpm:conventions-antigravity` (the latter three created in PR-B; see `analysis/multi-tool-design-2026-05.md`)
- Patterns and anti-patterns catalog → see `nlpm:patterns`
- How to run the score command → see `commands/score.md`

### Multi-tool scoring (PR-B landed 2026-05-25)

nlpm now scores artifacts across three tool ecosystems — Claude Code, Codex CLI, and Antigravity (which absorbs Gemini CLI on 2026-06-18). The tier classification in `agents/scorer.md` separates open-spec (Tier 1), Tier 1.5 open-spec corpora, and per-tool Tier 2 overlays (2-Claude / 2-Codex / 2-Antigravity).

- **Hooks** are scored per tool (the Claude table above; the Codex and Antigravity tables in `references/`). The three tools' event vocabularies are not 1:1 mappable; no universal translation layer. See `analysis/multi-tool-design-2026-05.md` decision #4.
- **Codex-specific artifacts** scored (`references/codex.md`): `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `.codex/config.toml`, `agents/openai.yaml` sidecars.
- **Antigravity-specific artifacts** scored (`references/antigravity.md`; advisory-only until spec stabilizes): `gemini-extension.json`, `.gemini/commands/*.toml`, Antigravity hook events.
- **Claude-specific additions** in 2026: `.lsp.json`, `monitors/monitors.json` (validate JSON-parse only until detailed schemas land). New SKILL.md fields documented in `nlpm:conventions-claude`.

### Known False Positive Patterns

The following findings have historically been reported by the scorer despite
having no backing in this rubric. They MUST NOT be penalized:

| Invalid finding | Why it is invalid |
|---|---|
| Missing `namespace:` on skill | Not in the skill schema; `conventions` §5 does not list it |
| Missing inline `hooks:`/`skills:` registration blocks in plugin.json | `conventions` §1 defines these as optional path strings |
| `AskUserQuestion` / `Task` / `WebFetch` flagged as undocumented tool | Built-in per `conventions-claude` §16 |
| Agent missing `skills:` when omission is documented in CLAUDE.md | Intentional architectural choice |
| plugin.json missing `engines:` / `minClaudeVersion:` / `main:` | All optional per `conventions` §1 |
| plugin.json description shorter than sibling marketplace.json description | Desynchronization ≠ defect; only penalize if required field is absent |

When in doubt: if a finding cannot be cited to a specific row in the penalty
tables above or in a reference file indexed under Penalty Tables, drop it.
