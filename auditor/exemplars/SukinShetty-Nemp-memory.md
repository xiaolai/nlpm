---
slug: SukinShetty-Nemp-memory
repo: SukinShetty/Nemp-memory
audited: 2026-05-13
commit_sha: 5f3e48af5129d00fb28c7e8b27e03aeb3b89ed28
score: 92
exemplifies:
  - R04
  - R08
  - R14
  - R15
  - R16
  - R17
  - R18
  - R30
---

# Exemplar: SukinShetty/Nemp-memory

**Score**: 92/100  |  **Date**: 2026-05-13  |  **Commit**: `5f3e48af5129d00fb28c7e8b27e03aeb3b89ed28`

A 24-command Claude Code plugin for persistent local memory (zero-cloud, plain JSON), notable for trigger-phrase-dense skill descriptions, fully templated output formats in every command, and rigorous empty-input handling throughout.

## Per-rule evidence

### R04 — Description as trigger

The `nemp-memory` skill packs five distinct invocation scenarios into its description, each phrased as a user action rather than a feature summary. A model reading this description knows exactly when to auto-load the skill without being told explicitly.

> Real quote from `skills/nemp-memory/SKILL.md:4-6`:
>
> ```
> description: Persistent local memory for AI agents. Use when starting a new session,
> when the user mentions remembering something, when you need project context,
> when making architecture decisions, or when working with other agents on the same project.
> ```

Five action phrases ("starting a new session", "user mentions remembering something", "need project context", "making architecture decisions", "working with other agents") each match a distinct query shape. Most skill descriptions stop at one.

---

### R08 — Patterns over theory

Rather than explaining the abstract concept of fuzzy recall, the skill body enumerates concrete keyword expansion mappings: the exact synonyms the model should use when a query term doesn't match a stored key. This is a lookup table, not a prose explanation.

> Real quote from `skills/nemp-memory/SKILL.md:61-76`:
>
> ```
> Search `.nemp/memories.json` with keyword expansion:
> - auth -> authentication, login, session, jwt, token, oauth
> - database -> db, postgres, mysql, sqlite, mongo, prisma, drizzle
> - styling -> css, tailwind, sass, scss, styled-components, shadcn
> - testing -> test, jest, vitest, cypress, playwright, e2e
> - deploy -> deployment, docker, vercel, netlify, aws, ci, cd
> ```

Five expansion families, each listing 5–8 technology-specific terms. A model reading "find the auth config" can expand to 6 candidate keys without guessing.

---

### R14 — Steps must be numbered

`commands/health.md` runs ten numbered steps (Steps 1–10), each with named sub-checks (3a–3f, 4a–4d). The numbering is structural, not decorative: Step 10 references sub-check results from Steps 2–9 to compute a final score, and Step 8 is a hard STOP gate if Step 1 fails.

> Real quote from `commands/health.md:22-37`:
>
> ```
> ### Step 1: Check .nemp/ Directory Exists
>
> ```bash
> [ -d ".nemp" ] && echo "NEMP_DIR_EXISTS" || echo "NEMP_DIR_MISSING"
> ```
>
> If `.nemp/` doesn't exist:
> ```
> ❌ CRITICAL: No .nemp/ directory found.
>
> Run /nemp:init to initialize Nemp Memory.
> ```
> **Stop here** — no further checks possible.
> ```

Ten-step command with sub-steps numbered in letter suffixes (3a, 3b, … 3f). Numbered prose elsewhere ("check the data and report issues") is ambiguous; numbered sub-steps here let a reviewer confirm which check maps to which score deduction in Step 10's table.

---

### R15 — Handle empty input

`commands/activate.md` guards against a blank `$ARGUMENTS` as Step 1 — before any validation or file I/O — with an exact usage string and a "Stop." sentinel. The sentinel is the key detail: it signals that execution halts, not that the model should produce an error and continue.

> Real quote from `commands/activate.md:18-29`:
>
> ```
> Extract the license key from the argument. If no argument is provided, show:
>
> ```
> Usage: /nemp:activate <license-key>
>
> License keys look like: NEMP-PRO-XXXX-XXXX
> Get yours at nemp.dev/pro
> ```
>
> Stop.
> ```

The "Stop." on its own line after the output block is a clean halt contract. Many commands say "show an error and proceed" when they mean "halt" — this one doesn't leave that ambiguous.

---

### R16 — Define output format

`commands/health.md` Step 11 gives a literal output template, not a prose description of what to show. The template includes score notation (`73/80`), the emoji band indicator, per-check tick/warning/error prefixes, a summary section, and a quick-fix block with actual command examples.

> Real quote from `commands/health.md:194-215`:
>
> ```
> ```
> Nemp Memory Health Check
>
>   Score: 73/80 🟢 HEALTHY
>
>   ✅ memories.json — 23 memories, all valid
>   ✅ CLAUDE.md — in sync (last sync: 2 min ago)
>   ⚠️ 2 memories exceed 200 char limit
>   ❌ Key "auth-flow" has empty value
>   ✅ Access log — 47 entries, no gaps
>   ✅ Config — autoSync enabled
>   ✅ Global — 4 global memories
>
>   Issues found: 2
>     ⚠️ auth-strategy: value is 247 chars (compress with /nemp:save)
>     ❌ auth-flow: empty value (delete with /nemp:forget auth-flow)
>
>   Quick fix:
>     /nemp:save auth-strategy "<shorter version>"
>     /nemp:forget auth-flow
> ```
> ```

The template includes a "Quick fix:" block with the exact commands to repair each reported issue. Most health-check outputs stop at "here are the problems" — this one tells the user the next command to run.

---

### R17 — Specify error paths

Every command in this plugin has an `## Error Handling` section listing specific failure modes, not a generic fallback. `commands/save.md` lists four distinct error paths, each with a defined response.

> Real quote from `commands/save.md:264-268`:
>
> ```
> ## Error Handling
> - If key is missing: Ask user to provide a key
> - If value is missing: Ask user to provide a value
> - If write fails: Report the error and suggest checking permissions
> - If auto-sync fails: Report briefly but don't fail the save operation
> ```

The last entry is the meaningful one: "don't fail the save operation" means a CLAUDE.md sync failure is non-fatal. Without this distinction, a model treating all errors identically would abort the entire save when CLAUDE.md is read-only.

---

### R18 — `argument-hint` when command takes input

Every command that accepts arguments declares `argument-hint` in its frontmatter. Commands with no arguments (like `/nemp:decay`, which is a Pro gate stub) omit it.

> Real quote from `commands/forget.md:1-4`:
>
> ```
> ---
> description: "Delete a memory by key"
> argument-hint: "<key> [--force]"
> ---
> ```

The `[--force]` bracket notation in the hint signals an optional flag, which is richer than the bare `<key>` a simpler implementation would show. The `/help` display for this command exposes the flag without requiring users to read the full instruction body.

---

### R30 — `${CLAUDE_PLUGIN_ROOT}` for paths

The hook config uses `${CLAUDE_PLUGIN_ROOT}` rather than a relative or absolute path for the hook body reference, making the plugin portable across install locations.

> Real quote from `.claude-plugin/hooks/hooks.json:7-10`:
>
> ```json
> {
>   "type": "command",
>   "command": "${CLAUDE_PLUGIN_ROOT}/hooks/post-tool.md"
> }
> ```

Single occurrence, but it's the only path reference in the hooks config. Repos that hardcode `./hooks/post-tool.md` break when the plugin installs into a non-default path.

---

## Worth adopting

**Pattern: `Stop.` as an explicit halt sentinel in command steps.** Evidence: `commands/activate.md:28`, `commands/health.md:37`. Used consistently after early-exit error outputs to signal that no further steps execute — not just "show a message" but "terminate this invocation." Why it would be a useful rule: the current R15 specifies *what* to output for empty input but not *how to signal halting behavior* to the model; "Stop." on its own line is a mechanical cue that prevents models from continuing into later steps after an error path.

**Pattern: Scored output with named bands.** Evidence: `commands/health.md:170-191`. The health check emits a numeric score with a named severity band (HEALTHY / NEEDS ATTENTION / DEGRADED / CRITICAL) mapped to explicit ranges. Why it would be a useful rule: commands that produce diagnostic output (score, lint, check) benefit from named bands because they give the user a decision boundary, not just a number; without bands, users must interpret raw numbers each time.
