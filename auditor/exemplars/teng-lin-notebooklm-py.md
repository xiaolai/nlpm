---
slug: teng-lin-notebooklm-py
repo: teng-lin/notebooklm-py
audited: 2026-06-21
commit_sha: 5fad7f19ce2e184ba2b11e326841c382cb228cc7
score: 99
exemplifies:
  - R04
  - R06
  - R08
  - R33
  - R34
  - R35
  - R38
---

# Exemplar: teng-lin/notebooklm-py

**Score**: 99/100  |  **Date**: 2026-06-21  |  **Commit**: `5fad7f19ce2e184ba2b11e326841c382cb228cc7`

A two-artifact repo (SKILL.md + CLAUDE.md) for an unofficial Google NotebookLM API client; notable for exhaustive runnable examples, named workflow patterns with inline error paths, and a CLAUDE.md that reads as agent instructions rather than contributor docs.

## Per-rule evidence

### R04 — Description as trigger

The SKILL.md frontmatter description packs six action phrases and two explicit trigger conditions into a single 250-character line. It names both an exact slash-command and a free-text intent signal in the same sentence, so Claude activates on direct invocation and on natural-language requests alike.

> Real quote from `SKILL.md:3`:
>
> ```
> description: Complete API for Google NotebookLM - full programmatic access including
> features not in the web UI. Create notebooks, add sources, generate all artifact types,
> download in multiple formats. Activates on explicit /notebooklm or intent like "create
> a podcast about X"
> ```

What makes this better than a mediocre description: it names the non-obvious trigger ("intent like 'create a podcast about X'"), not just the explicit command. A description that only says "Use for NotebookLM" would activate on `/notebooklm` but miss the intent path entirely.

---

### R06 — Code examples must be runnable

Every code block in SKILL.md is executable — no pseudocode. The installation section runs a real Python version probe inside a bash if-block rather than writing `# install the cookies extra if needed`:

> Real quote from `SKILL.md:18-23`:
>
> ```bash
> pip install "notebooklm-py[browser]"   # mandatory; errors must propagate
>
> # [cookies] (rookiepy) is optional and known to FAIL TO BUILD on Python 3.13+.
> if python -c "import sys; sys.exit(0 if sys.version_info < (3, 13) else 1)"; then
>     pip install "notebooklm-py[cookies]"   # errors propagate
> else
>     echo "Skipping [cookies] on Python 3.13+ (rookiepy unavailable). Use 'notebooklm login' interactively."
> fi
> ```

JSON output examples go further: every schema block shows a real response shape and a parse hint on the next line so the agent knows exactly which field to extract:

> Real quote from `SKILL.md:260-264`:
>
> ```bash
> $ notebooklm create "Research" --json
> {"notebook": {"id": "abc123de-...", "title": "Research", "created_at": null}}
> # parse with: jq -r .notebook.id
> ```

The auth-check example (line 513-516) demonstrates a common false-positive trap (`bare --json` vs `--test --json`) by showing both the wrong and right invocation inline, not in a separate troubleshooting section.

---

### R08 — Patterns over theory

The "Common Workflows" section (SKILL.md:364+) names six concrete patterns — "Research to Podcast (Interactive)", "Research to Podcast (Automated with Subagent)", "Document Analysis", "Bulk Import", etc. Each is a numbered sequence of real commands with inline error annotations at each step, not prose about how generation works.

> Real quote from `SKILL.md:366-375`:
>
> ```
> ### Research to Podcast (Interactive)
> **Time:** 5-10 minutes total
>
> 1. `notebooklm create "Research: [topic]"` — *if fails: check auth with `notebooklm login`*
> 2. `notebooklm source add` for each URL/document — *if one fails: log warning, continue with others*
> 3. Wait for sources: `notebooklm source list --json` until all status=READY — *required before generation*
> 4. `notebooklm generate audio "Focus on [specific angle]"` (confirm when asked) — *if rate limited: wait 5 min, retry once*
> 5. Note the artifact ID returned
> 6. Check `notebooklm artifact list` later for status
> 7. `notebooklm download audio ./podcast.mp3` when complete (confirm when asked)
> ```

Each step's recovery path is expressed in italics inline — not relocated to a "Troubleshooting" appendix the agent might not read in context. Timing annotations ("5-10 minutes total") give the agent a calibrated expectation before committing to a long-running operation.

---

### R33 — Include build/run command

CLAUDE.md opens its "Development Commands" section with the exact canonical install incantation and all the run paths an agent might reach for, including the e2e flag:

> Real quote from `CLAUDE.md:12-22`:
>
> ```bash
> # Canonical contributor install (respects uv.lock; full guide: docs/installation.md)
> uv sync --frozen --extra browser --extra dev --extra markdown
> source .venv/bin/activate
> uv run playwright install chromium
>
> uv run pytest                     # all tests (e2e excluded by default)
> uv run pytest --cov               # with coverage
> uv run pytest tests/e2e -m e2e    # e2e (requires auth)
> uv run notebooklm --help          # CLI
> ```

The comment "respects uv.lock" is load-bearing — it tells Claude why `uv sync --frozen` rather than a bare `pip install`, removing a likely substitution error.

---

### R34 — Include test command

The "Before Pushing" section (CLAUDE.md:27-31) names exactly the commands CI runs, so an agent knows what to verify before opening a PR — not just `pytest` but also the type-checker invocation that frequently goes missing:

> Real quote from `CLAUDE.md:27-31`:
>
> ```bash
> uv run mypy src/notebooklm --ignore-missing-imports
> uv run pytest
> ```

The prose before these lines states "CI fails otherwise" — a consequence, not a style note. An agent seeing this won't skip mypy.

---

### R35 — Include architecture overview

The Architecture section in CLAUDE.md gives the full call stack in one line and cross-references the deep-dive doc for agents that need more:

> Real quote from `CLAUDE.md:36-38`:
>
> ```
> `cli/` (Click) → `_app/` (transport-neutral business logic, reusable by MCP/HTTP adapters)
> → `client.py` + `_*.py` (client runtime) → `rpc/` (batchexecute encode/decode).
>
> See **[docs/architecture.md](docs/architecture.md)** for the layered design, call flows, ...
> ```

This is a one-read mental model: the agent knows the CLI doesn't talk to the RPC layer directly, which prevents the common mistake of reaching for `rpc/` internals when editing CLI behavior.

---

### R38 — More instructive than descriptive

CLAUDE.md's "Common Pitfalls" section (lines 42-47) is five numbered failure modes with specific causes and remedies, not a README-style capability description:

> Real quote from `CLAUDE.md:42-47`:
>
> ```
> 1. **RPC method IDs change** — re-capture network traffic and update `rpc/types.py`.
> 2. **Position-sensitive nested params** — copy the shape from an existing implementation;
>    source-id nesting varies (`[id]` / `[[id]]` / `[[[id]]]` / `[[[[id]]]]`).
> 3. **CSRF tokens expire** — call `client.refresh_auth()` or re-run `notebooklm login`.
> 4. **Rate limiting** — add delays between bulk operations.
> 5. **Concurrency** — one `NotebookLMClient` is bound to its `open()`-time event loop:
>    create one per thread, never reuse across event loops or `AuthTokens` tenants.
> ```

Pitfall 2 names the exact four nesting depths an agent must match — not "be careful with nested parameters." The PR Workflow section (lines 72-80) follows the same pattern: three numbered steps, each ending in a consequence clause that tells Claude what happens if the step is skipped.

---

## Worth adopting

**Pattern: Permission-class table for skill commands.** Evidence: `SKILL.md:122-158` — the "Autonomy Rules" section splits every command in the skill's surface into two mutually exclusive buckets ("Run automatically (no confirmation)" vs "Ask before running"), with a one-phrase rationale per command entry. This pattern is distinct from R08 (workflow sequences) because it classifies the full command surface by permission level rather than narrating a particular use-case flow. An agent reading this can determine autonomy policy for any command without scanning the whole skill. Why it would be a useful rule: skills that wrap CLIs or APIs with destructive operations need a single-read autonomy policy table; embedding the permission level in each command reference (rather than in a runtime confirmation prompt) lets the agent make the right call without asking the user for every invocation.
