---
name: conventions
description: "Universal NL programming conventions — SKILL.md open spec (agentskills.io), AGENTS.md as canonical universal memory file, vague-quantifier list, prompt engineering layers, naming conventions, the override system. Tool-specific schemas live in nlpm:conventions-claude / nlpm:conventions-codex / nlpm:conventions-antigravity."
version: 0.2.1
---

# Universal NL Programming Conventions

The cross-tool floor for all artifact schemas. Use this skill when scoring or writing any NL programming artifact regardless of which tool (Claude Code / Codex CLI / Antigravity) it targets.

**Tool-specific overlays** load on top of this universal floor:
- `nlpm:conventions-claude` — Claude Code artifacts (`.claude/`, `plugin.json`, etc.)
- `nlpm:conventions-codex` — Codex CLI artifacts (`.codex/`, `.agents/`, `AGENTS.md`)
- `nlpm:conventions-antigravity` — Antigravity (and legacy Gemini CLI) artifacts (`.gemini/`, `.agent/`)

The scorer loads the matching overlay per tier classification — see `agents/scorer.md` step 3.

**Design rationale:** `analysis/multi-tool-design-2026-05.md`.

---

## 1. SKILL.md — Cross-Tool Open Standard

SKILL.md is the **Agent Skills open spec**, stewarded by the Agentic AI Foundation under the Linux Foundation. Anthropic published the spec on 2025-12-18; OpenAI, Microsoft, Google adopted within 48 hours. By 2026-03, 32+ tools read the same SKILL.md format (Claude Code, Codex, Gemini CLI / Antigravity, Cursor, Kiro, Continue, etc.).

**Authoritative reference:** <https://agentskills.io/specification>

**Required frontmatter (per the open spec):**
- `name` — string; 1-64 chars, lowercase + hyphens only, **MUST match parent directory name** (no leading/trailing/consecutive hyphens).
- `description` — string; 1-1024 chars; should describe what the skill does AND when to use it.

**Optional frontmatter (per the open spec):**
- `license` — license name or reference to a bundled file.
- `compatibility` — environment requirements, max 500 chars (e.g., "Designed for Claude Code", "Requires Python 3.14+ and uv").
- `metadata` — arbitrary key-value mapping (`author`, `version`, etc. go here, NOT as top-level fields).
- `allowed-tools` — space-separated tool list (experimental in spec; tool-specific in practice — e.g., `Bash(git:*) Read`).

**Tool-specific extensions to SKILL.md frontmatter** live in the per-tool overlay skills. The scorer applies the universal spec rules to ALL SKILL.md files. Tool-specific overlay rules apply ONLY to files at the matching tool's canonical paths.

**Skill paths (canonical, per tool):**

| Tool | Path |
|---|---|
| Open-spec (cross-tool) | `.agents/skills/<name>/SKILL.md` |
| Claude Code | `.claude/skills/<name>/SKILL.md` |
| Codex CLI | `.agents/skills/<name>/SKILL.md` |
| Antigravity | `<workspace>/.agent/skills/<name>/SKILL.md` (singular) AND `.agents/skills/<name>/SKILL.md` (cross-tool alias) |
| Gemini CLI (legacy) | `.gemini/skills/<name>/SKILL.md` |
| Continue, Cursor, Kiro | `.<tool>/skills/<name>/SKILL.md` |

**Body rules (recommendations, not spec requirements):**
- Keep under 500 lines — exceeding creates context bloat (spec recommends under 5000 tokens for the body, with overflow in `references/`).
- Reference material — imperatives belong in commands/agents.
- Include a scope note: what this skill covers and what it does NOT cover.
- Cross-reference related skills with their `plugin:skill` identifiers.

The spec explicitly says "no format restrictions" on the body — do NOT penalize SKILL.md files for missing `## Output` or other section conventions. Those are tool-specific style preferences, not spec violations.

**Supporting directories (per the spec):**
- `scripts/` — executable code (Python, Bash, JavaScript)
- `references/` — additional docs loaded on demand
- `assets/` — templates, images, data files

**Progressive disclosure:**
1. Metadata (~100 tokens): name + description loaded at startup for ALL skills.
2. Instructions (<5000 tokens): full SKILL.md body loaded when activated.
3. Resources: scripts/references/assets loaded only when needed.

---

## 2. AGENTS.md — Canonical Universal Memory File

Per nlpm decision (`analysis/multi-tool-design-2026-05.md` §5), AGENTS.md is the canonical universal memory file across all tools nlpm supports.

**Tool-native support:**
- **Codex CLI:** reads AGENTS.md natively. Hierarchical (root→cwd; closer overrides earlier). 32 KiB cap. `~/.codex/AGENTS.override.md` for personal overlays.
- **Antigravity (and Gemini CLI):** reads `GEMINI.md` natively, but `context.fileName` setting accepts an array — set to `["AGENTS.md", "GEMINI.md"]` to make it read AGENTS.md.
- **Claude Code:** reads `CLAUDE.md` natively, supports `@file.md` import syntax. The canonical pattern is a one-line `CLAUDE.md` containing `@AGENTS.md`.

**Recommended pattern for multi-tool projects:**

```
project-root/
├── AGENTS.md           # canonical content — all instructions live here
├── CLAUDE.md           # one line: @AGENTS.md
├── GEMINI.md           # one line: @AGENTS.md  (only if Gemini-native @-import works)
└── .gemini/settings.json  # set context.fileName: ["AGENTS.md"]
```

This is exactly how nlpm itself is structured (`CLAUDE.md` → `@AGENTS.md`).

**Body conventions** (universal):
- Open with a one-line project description.
- `## Architecture` or `## Project Structure` — what lives where.
- `## Build` / `## Run` / `## Test` — verifiable commands.
- `## Prerequisites` — required tools / versions / setup.
- `## Conventions` — naming, style, patterns.

**Tool-specific memory-file extensions** (e.g., Claude Code's `@`-import syntax, Gemini's `@{path}` injection, Codex's `project_doc_fallback_filenames`) live in the per-tool overlays.

### Agent workflow programs (recognized variant, no penalty rubric yet)

An agent workflow program is a single project-root Markdown file that drives an autonomous agent loop — imperative numbered steps with output formats and error paths, sitting between a memory file (AGENTS.md-shaped context) and a slash command (workflow with verifiable side effects). Karpathy's `program.md` in [`karpathy/autoresearch`](https://github.com/karpathy/autoresearch) is the canonical example (audited 2026-05-28 at score ~90; see [`auditor/exemplars/karpathy-autoresearch.md`](../../../auditor/exemplars/karpathy-autoresearch.md)). The README explicitly frames it as natural-language programming: "you are programming the `program.md` Markdown files that provide context to the AI agents."

nlpm recognizes the pattern but does not yet have a dedicated penalty rubric — the universal floor (R01 vague quantifiers, R03 positive framing, R09 prompt layers) + the command rules (R14–R17) + the memory-file rules (R33–R39) cover it adequately as a hybrid. A standalone rubric is deferred until N≥3 examples surface, per the same "don't build for an empty corpus" discipline applied to multi-tool discovery.

---

## 3. General Prompt Engineering

Universal patterns applicable to any NL artifact (commands, agents, skills, prompts) regardless of tool.

**Layer order** (imperative for complex prompts):
1. Role/persona — "You are a strict code reviewer..."
2. Context — project state, prior decisions, file paths, constraints
3. Task — specific action to perform
4. Constraints — what to avoid, limits, edge cases
5. Output format — exact structure of the response

**Few-shot examples:** Include 2+ concrete input→output examples for any complex judgment task. Examples dramatically improve consistency.

**Positive framing:** State what to do. "Use imperative verbs" beats "Don't use passive voice." The brain processes prohibitions poorly under inference load (Pink Elephant effect).

**Explicit output format:** Every command and agent body should define exactly what the output should look like — section names, table formats, score displays, etc.

---

## 4. Vague Quantifiers (R01)

The R01 rule penalizes unbounded quantifiers without measurable criteria. The penalty applies regardless of which tool the artifact targets.

**Penalized terms:** `appropriate`, `relevant`, `as needed`, `sufficient`, `adequate`, `reasonable`, `properly`, `correctly`, `some`, `several`, `various`.

**Carve-outs (do NOT penalize):**
- `relevant` in a markdown header (e.g., `## Relevant X`).
- `relevant to <named-scope>` constructions (semantic "pertinent to").
- Any term followed by a measurable criterion clause (e.g., "appropriate to the SLO target of 99.9% uptime").

See `nlpm:scoring` for the full vague-quantifier penalty table and cap (-2 each, -20 cap).

---

## 5. Naming Conventions (universal)

| Item | Convention | Example |
|---|---|---|
| File names | kebab-case | `tdd-guardian.md`, `pre-write-check.sh` |
| Plugin/package names | kebab-case | `nlpm`, `echo-sleuth` |
| Skill references | `plugin-name:skill-name` | `nlpm:conventions`, `tdd-guardian:rules` |
| Rule files (ordered) | `NN-kebab.md` | `01-formatting.md` |
| Environment variables | SCREAMING_SNAKE | `OPENAI_API_KEY`, `CLAUDE_PLUGIN_ROOT` |
| Plugin directory env vars | tool-specific (no universal `<TOOL>_PLUGIN_ROOT` pattern) | Claude: `CLAUDE_PLUGIN_ROOT`. Codex: `PLUGIN_ROOT` / `PLUGIN_DATA` (also mirrors `CLAUDE_PLUGIN_ROOT` for compat — there is **no** `CODEX_PLUGIN_ROOT`) |

**Portable paths:** Within a plugin, always reference files via the tool's plugin-root environment variable — `${CLAUDE_PLUGIN_ROOT}` in Claude Code, `${PLUGIN_ROOT}` in Codex (Codex additionally sets `CLAUDE_PLUGIN_ROOT` / `CLAUDE_PLUGIN_DATA` for compatibility with existing plugin hooks). Hardcoded absolute paths break portability.

Tool-specific naming details (e.g., the exact `CLAUDE_PLUGIN_ROOT` semantics) live in the per-tool overlays.

---

## 6. Rule Overrides (`.claude/nlpm.local.md` or equivalent)

The override system is universal. The configuration file path is per-tool:

| Tool | Config path |
|---|---|
| Claude Code | `.claude/nlpm.local.md` |
| Codex CLI | `.codex/nlpm.local.md` |
| Antigravity | `.gemini/nlpm.local.md` (or `.agent/nlpm.local.md` — TBD post-2026-06-18) |

Frontmatter format (identical across tools):

```yaml
---
strictness: standard
score_threshold: 70
rule_overrides:
  R01: { max_penalty: -10 }     # reduce vague quantifier cap from -20 to -10
  R05: { threshold: 600 }       # allow skills up to 600 lines instead of 500
  R09: { min_examples: 1 }      # require only 1 example block instead of 2
  R10: { suppress: true }       # disable model tier checking entirely
  R23: { budget: 800 }          # increase rules budget from 500 to 800 lines
  R51: { enabled: true, vocabulary_skill: skills/myplugin/vocabulary/ }
---
```

**Override types:**

| Type | Effect | Example |
|---|---|---|
| `suppress: true` | Disable the rule (penalty becomes 0) | `R10: { suppress: true }` |
| `enabled: true` | Activate a rule that ships disabled by default (currently only R51) | `R51: { enabled: true, vocabulary_skill: ... }` |
| `max_penalty: N` | Cap the penalty (less negative = more lenient) | `R01: { max_penalty: -10 }` |
| `threshold: N` | Adjust numeric thresholds | `R05: { threshold: 600 }` |
| `min_examples: N` | Adjust minimum example counts | `R09: { min_examples: 1 }` |
| `vocabulary_skill: <path>` | Path to project's `vocabulary` skill (R51 only) | `R51: { enabled: true, vocabulary_skill: ... }` |

Rules not listed in `rule_overrides` use their defaults from `nlpm:scoring`. Rules that ship disabled (R51) contribute zero penalty unless `enabled: true` is set explicitly.

---

## 7. Universal Tool References

**MCP tools** follow the cross-tool pattern: `mcp__<server-name>__<tool-name>`. Example: `mcp__mermaider__validate_syntax`.

Per-tool built-in tool catalogs live in the overlays:
- Claude Code built-ins → `nlpm:conventions-claude` §16
- Codex CLI built-ins → `nlpm:conventions-codex`
- Antigravity built-ins → `nlpm:conventions-antigravity`

---

## Scope Note

This skill covers the universal floor — conventions that apply regardless of which tool the artifact targets. It does NOT cover:
- Tool-specific schemas → see `nlpm:conventions-claude` / `nlpm:conventions-codex` / `nlpm:conventions-antigravity`
- Penalty tables → see `nlpm:scoring`
- Anti-patterns and best practices catalog → see `nlpm:patterns`
- General software engineering conventions outside NL programming artifacts
