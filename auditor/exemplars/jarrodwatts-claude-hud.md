---
slug: jarrodwatts-claude-hud
repo: jarrodwatts/claude-hud
audited: 2026-05-13
commit_sha: b53c3f0b208fd14df6407f9d830c565c0b43d520
score: 92
exemplifies:
  - R08
  - R14
  - R16
  - R17
  - R33
  - R35
  - R49
---

# Exemplar: jarrodwatts/claude-hud

**Score**: 92/100  |  **Date**: 2026-05-13  |  **Commit**: `b53c3f0b208fd14df6407f9d830c565c0b43d520`

A two-command Claude Code plugin (setup + configure) for a real-time statusline HUD; notable for exhaustive error-path coverage across three OS/shell combinations and a configure command that never asks Claude to infer output format.

## Per-rule evidence

### R08 — Patterns over theory

`configure.md` teaches via direct option→config-key tables across every configurable dimension. No explanatory paragraphs about how layout configuration "conceptually works" — each user-facing choice maps to an exact JSON key with a concrete rendered example.

> `commands/configure.md` (Layout Mapping section):
>
> ```
> | Option | Config |
> |--------|--------|
> | Expanded | `lineLayout: "expanded", showSeparators: false` |
> | Compact | `lineLayout: "compact", showSeparators: false` |
> | Compact + Separators | `lineLayout: "compact", showSeparators: true` |
> ```
>
> ```
> | Element | Config Key |
> |---------|------------|
> | Tools activity | `display.showTools` |
> | Agents status | `display.showAgents` |
> | Todo progress | `display.showTodos` |
> | Project name | `display.showProject` |
> | Git status | `gitStatus.enabled` |
> ```

The file contains 8 mapping tables total. No theory, no abstraction — every option resolves to a config key or a rendered example string.

### R14 — Steps must be numbered

`setup.md` splits the install workflow into 6 explicitly named phases (Step 0 through Step 5), each with a single declared scope. Step 0 even includes a parenthetical execution hint (`Run First`) because the ghost-install check must precede path detection.

> `commands/setup.md` (section headers):
>
> ```
> ## Step 0: Detect Ghost Installation (Run First)
> ## Step 1: Detect Platform, Shell, and Runtime
> ## Step 2: Test Command
> ## Step 3: Apply Configuration
> ## Step 4: Optional Features
> ## Step 5: Verify & Finish
> ```

Each heading is a re-entry point — Claude can resume at "Step 3: Apply Configuration" after a restart prompt without re-parsing earlier steps. Unnumbered prose phases collapse on interruption.

### R16 — Define output format

`configure.md` does not say "show the user what the HUD will look like." It embeds the rendered template verbatim — actual block-character art for both layout variants — in the Before Writing section. Claude cannot hallucinate the format because it is literal text in the instruction.

> `commands/configure.md` (Before Writing — Show preview):
>
> ```
> **Preview of HUD (Expanded layout):**
> ```
> [Opus | Pro] │ my-project git:(main*)
> Context ████░░░░░ 45% │ Usage ██░░░░░░░░ 25% (1h 30m / 5h)
> ◐ Edit: file.ts | ✓ Read ×3
> ▸ Fix auth bug (2/5)
> ```
>
> **Preview of HUD (Compact layout):**
> ```
> [Opus | Pro] ████░░░░░ 45% | my-project git:(main*) | 5h: 25% | ⏱️ 5m
> ◐ Edit: file.ts | ✓ Read ×3
> ▸ Fix auth bug (2/5)
> ```
> ```

Both variants are required because the same instruction must produce identical previews across sessions and models. Without both, a Haiku invocation and a Sonnet invocation generate different-looking previews.

### R17 — Specify error paths

Step 5's "If no" branch gives 5 numbered debug steps, each scoped to a specific failure mode with the exact symptom string and a concrete fix command. No generic "something went wrong" fallback exists.

> `commands/setup.md` (Step 5 — If no):
>
> ```
> **If no**: Debug systematically:
>
> 1. **Restart Claude Code** (most common cause on macOS):
>     - The statusLine config requires a restart to take effect
>
> 4. **Common issues to check**:
>
>    **"command not found" or empty output**:
>    - Runtime path might be wrong: `ls -la {RUNTIME_PATH}`
>    - On macOS with mise/nvm/asdf: the absolute path may have changed after a runtime update
>
>    **"No such file or directory" for plugin**:
>    - Plugin might not be installed: `ls "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/*/claude-hud/`
>
>    **Windows shell mismatch (for example, "bash not recognized")**:
>    - Command format does not match `Platform:` + `Shell:`
> ```

Each error string is quoted verbatim so Claude can pattern-match actual shell output without guessing. The ordering (restart first, inspect config second, test command third) reflects triage priority — the most common cause is listed first.

### R33 — Include build/run command

`CLAUDE.md` opens its Build Commands section with three commands covering the full development cycle, including a sample stdin payload to exercise the main data path without a live Claude Code session.

> `CLAUDE.md:11-16`:
>
> ```
> ```bash
> npm ci               # Install dependencies
> npm run build        # Build TypeScript to dist/
>
> # Test with sample stdin data
> echo '{"model":{"display_name":"Opus"},"context_window":{"current_usage":{"input_tokens":45000},"context_window_size":200000}}' | node dist/index.js
> ```
> ```

The inline test command is a concrete detail: a Claude agent modifying `src/` can validate rendering output immediately without a running Claude Code instance. A bare `npm run build` would leave the data path untested.

### R35 — Include architecture overview

`CLAUDE.md` leads with an ASCII data-flow diagram and follows it with a structured breakdown of the three data sources (native stdin JSON, transcript JSONL, config files) and an annotated directory tree. The three-source model is the key non-obvious fact about the runtime — none of it is derivable from the file names alone.

> `CLAUDE.md:23-27`:
>
> ```
> ### Data Flow
>
> ```
> Claude Code → stdin JSON → parse → render lines → stdout → Claude Code displays
>            ↘ transcript_path → parse JSONL → tools/agents/todos
> ```
> ```

> `CLAUDE.md:62-83`:
>
> ```
> src/
> ├── index.ts           # Entry point
> ├── stdin.ts           # Parse Claude's JSON input
> ├── transcript.ts      # Parse transcript JSONL
> ├── config-reader.ts   # Read MCP/rules configs
> ├── config.ts          # Load/validate user config
> ├── git.ts             # Git status (branch, dirty, ahead/behind)
> ├── types.ts           # TypeScript interfaces
> └── render/
>     ├── index.ts       # Main render coordinator
>     ├── session-line.ts   # Compact mode: single line with all info
>     ├── tools-line.ts     # Tool activity (opt-in)
>     ...
> ```

Per-file annotations mean a Claude agent can locate the right module without tracing imports from `index.ts`.

### R49 — CLAUDE.md for Claude, README for humans

The split is clean and non-overlapping. `CLAUDE.md` contains context thresholds, data-source semantics, and a Key Insight about the 300ms invocation cadence. `README.md` opens with install instructions and a screenshot — neither bleeds into the other's audience.

> `README.md:1-14`:
>
> ```
> # Claude HUD
>
> A Claude Code plugin that shows what's happening — context usage, active tools,
> running agents, and todo progress. Always visible below your input.
>
> ## Install
>
> Inside a Claude Code instance, run the following commands:
> ```

> `CLAUDE.md:99-105`:
>
> ```
> ### Context Thresholds
>
> | Threshold | Color | Action |
> |-----------|-------|--------|
> | <70% | Green | Normal |
> | 70-85% | Yellow | Warning |
> | >85% | Red | Show token breakdown |
> ```

The threshold table is pure agent guidance — it shapes rendering decisions that a Claude agent fixing a display bug needs. The README never mentions it; the CLAUDE.md never mentions the screenshot.

## Worth adopting

Pattern: **Platform-branch decision table at the top of a multi-OS command.** Evidence: `commands/setup.md:104-108`. A four-row table maps `Platform × Shell → Command Format` before any branching logic, so Claude reads the decision matrix once and executes the correct branch without re-evaluating OS conditions at each step. Why it would be a useful rule: multi-platform commands that embed detection in prose force the model to re-parse branch conditions mid-step; a leading decision table eliminates that re-evaluation and cuts branching errors on Windows/bash vs. Windows/PowerShell splits.
