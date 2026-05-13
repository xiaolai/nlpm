---
slug: uppinote20-claude-dashboard
repo: uppinote20/claude-dashboard
audited: 2026-05-13
commit_sha: 1281b7d66dbcd88e9891574706ce2edb29b00c26
score: 99
exemplifies:
  - R14
  - R15
  - R16
  - R18
  - R35
  - R38
---

# Exemplar: uppinote20/claude-dashboard

**Score**: 99/100  |  **Date**: 2026-05-13  |  **Commit**: `1281b7d66dbcd88e9891574706ce2edb29b00c26`

A four-command Claude Code plugin for status-line configuration and AI-CLI usage tracking; notable for its command frontmatter precision and a CLAUDE.md that is almost entirely instructive rather than descriptive.

## Per-rule evidence

### R14 — Steps must be numbered

Every command in the repo wraps its work in explicitly numbered task steps. `update.md` is the tightest example — three numbered steps, each with a copy-paste shell block, no prose between them.

> From `commands/update.md`:
>
> ```
> ## Task
>
> 1. Find the latest version in the plugin cache:
> ```bash
> ls -d ~/.claude/plugins/cache/claude-dashboard/claude-dashboard/*/ 2>/dev/null | grep -E '/[0-9]+\.[0-9]+\.[0-9]+/$' | sort -V | tail -1
> ```
>
> 2. Update settings.json with the latest version path:
> ...
>
> 3. Show the user what was updated:
>    - Previous version (if changed)
>    - New version path
>    - Remind them to restart Claude Code for changes to take effect
> ```

The sequence is unambiguous — no "then" connectives, no bullet-over-bullet prose that Claude might reorder.

### R15 — Handle empty input

`setup.md` splits the entire task body into two labeled paths based on whether `$ARGUMENTS` is blank, making the default behavior explicit rather than inferred.

> From `commands/setup.md:83-131`:
>
> ```
> **If no arguments provided (interactive mode):**
>
> Use AskUserQuestion to ask the user. Batch independent questions into a
> single AskUserQuestion call (max 4 per call) to minimize back-and-forth.
>
> **Turn 1** — Ask all 4 questions in a single AskUserQuestion call:
> ...
>
> **If arguments provided (direct mode):**
>
> Use the provided arguments directly.
> ```

The two paths are labeled with bold headings, not buried in conditionals. Claude cannot miss the branch point, and the default behavior (interactive) is described first and in full.

### R16 — Define output format

Both `update.md` and `setup-alias.md` supply exact output templates, including conditional variants. `setup-alias.md` covers three separate cases — already-installed, newly-installed, and Windows — each with a literal output block.

> From `commands/setup-alias.md:103-130`:
>
> ```
> **If already exists:**
> ```
> ✓ check-ai is already configured in [config file].
>
> Usage:
>   check-ai          # Pretty output
>   check-ai --json   # JSON output for scripting
> ```
>
> **If newly added:**
> ```
> ✓ Added check-ai to [config file].
>
> To activate now, run:
>   source ~/.zshrc   (or restart your terminal)
> ...
> ```
>
> **For Windows:**
> ```
> ✓ Added check-ai to PowerShell profile.
> ...
> ```
> ```

Three output paths, three templates — no "show the results" ambiguity.

### R18 — `argument-hint` when command takes input

`setup.md` uses `argument-hint` to encode four positional args and a custom-mode variant in a single line, showing the optional-bracket convention and the `|` separator for the custom sub-path.

> From `commands/setup.md:3`:
>
> ```
> argument-hint: "[displayMode] [language] [plan] | custom \"widgets\""
> ```

All four arguments are bracketed (optional), and the `| custom "widgets"` suffix signals the alternative invocation without requiring a prose paragraph. The `/help` display gives a user enough to self-serve without opening the full command file.

### R35 — Include architecture overview

`CLAUDE.md` carries a 36-row widget reference table (Widget ID → Data Source → Description) plus a `DISPLAY_PRESETS` TypeScript block showing which widgets appear on each line per display mode. Together they constitute a complete component map.

> From `CLAUDE.md:128-191` (excerpt):
>
> ```
> | Widget ID | Data Source | Description |
> |-----------|-------------|-------------|
> | `model`   | stdin + settings | Model name with emoji, effort level for Opus/Sonnet (X/H/M/L), fast mode for Opus (↯) |
> | `context` | stdin | Progress bar, %, tokens |
> ...
> | `peakHours` | system clock | Peak hours indicator with countdown (weekdays 5-11 AM PT) |
> | `tagStatus` | git | Distance (commits ahead) from matched git tags. Supports multiple glob patterns via `tagPatterns` config (default `["v*"]`). Hidden when no pattern matches. |
>
> const DISPLAY_PRESETS = {
>   compact: [
>     ['model', 'context', 'cost', 'rateLimit5h', 'rateLimit7d', 'rateLimit7dSonnet', 'zaiUsage'],
>   ],
>   normal: [
>     ['model', 'context', 'cost', 'rateLimit5h', 'rateLimit7d', 'rateLimit7dSonnet', 'zaiUsage'],
>     ['projectInfo', 'sessionId', 'sessionDuration', 'burnRate', 'todoProgress'],
>   ],
>   ...
> ```

The table is a lookup index — Claude knows exactly which data source a widget consumes before writing any code. The `DISPLAY_PRESETS` block makes the default layouts machine-readable, not just described in prose.

### R38 — More instructive than descriptive

The bulk of `CLAUDE.md` is step-by-step task instructions, not feature descriptions. The "Common Tasks" section runs four numbered task lists (adding a widget, adding a locale, modifying display modes, updating the API client), each scoped to exactly the files that change.

> From `CLAUDE.md:298-310`:
>
> ```
> ### Adding a new widget
>
> 1. Create `scripts/widgets/{widget-name}.ts`
> 2. Implement `Widget` interface with `getData()` and `render()`
> 3. Add widget ID to `WidgetId` type in `types.ts`
> 4. Register widget in `scripts/widgets/index.ts`
> 5. Add translations to `locales/*.json` if needed
> 6. Update `DISPLAY_PRESETS` if adding to default modes
> 7. Rebuild and test
> ```

Seven steps, seven files touched, zero ambiguity about the order. A new contributor (or Claude) can follow this without reading the source code first.

## Worth adopting

**Pattern: Batch interactive prompts up front with an explicit max.** Evidence: `commands/setup.md:87` — "Batch independent questions into a single AskUserQuestion call (max 4 per call) to minimize back-and-forth." Why it would be a useful rule: interactive commands that ask one question per turn multiply round-trips unnecessarily; a rule like "batch up to 4 independent questions per AskUserQuestion call" would eliminate this pattern across all commands.

**Pattern: Embed ASCII previews in AskUserQuestion option descriptions.** Evidence: `commands/setup.md:91-113` — each display-mode option carries a multi-line `markdown:` block showing the actual rendered status line. Why it would be a useful rule: for commands where the user is choosing a visual layout, showing the output before they commit eliminates "what does this look like?" follow-up turns.
