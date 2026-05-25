---
slug: viticci-shortcuts-playground-plugin
repo: viticci/shortcuts-playground-plugin
audited: 2026-05-25
commit_sha: 14550f1c722aecbdaae158465666dc3d9da771bb
score: 91
exemplifies:
  - R04
  - R05
  - R07
  - R08
  - R13
  - R30
  - R31
---

# Exemplar: viticci/shortcuts-playground-plugin

**Score**: 91/100  |  **Date**: 2026-05-25  |  **Commit**: `14550f1c722aecbdaae158465666dc3d9da771bb`

A two-agent Claude Code plugin for authoring Apple Shortcuts plists, notable for description triggers that precisely delimit scope, a 57-rule key-rules section that buries all theory in concrete imperatives, and fail-open hook engineering that never blocks unrelated writes.

## Per-rule evidence

### R04 — Description as trigger

The SKILL.md packs seven distinct trigger phrases into a single description field, each matching a different way a user might ask for Shortcuts help. The agent descriptions do the same and also state their negative boundary — something most agents omit.

> `claude/skills/shortcuts-playground/SKILL.md:3-5`:
>
> ```
> description: Build, validate, sign, archive, and REMIX macOS/iOS Shortcuts by creating plist
>   files. Use when asked to create, modify, or remix shortcuts; automate workflows; build
>   .shortcut files; or generate Shortcuts plists. Covers WF actions, AppIntents, third-party
>   actions, variable references, and control flow using bundled ToolKit v63 metadata with
>   optional local ToolKit expansion.
> ```

> `claude/agents/shortcut-remixer.md:2-4`:
>
> ```
> description: Specialized agent that remixes an existing `.xml` Shortcuts plist by applying a
>   natural-language diff. Invoke when the user supplies BOTH a path to an existing unsigned XML
>   file AND a description of changes to apply. NOT for from-scratch builds — if there's no
>   source XML, decline and suggest /shortcuts-playground:build instead.
> ```

The remixer description does triple duty: triggers on "remix + path", excludes "from-scratch builds" explicitly, and names the redirect target. A description that says what NOT to invoke it for cuts misfires more effectively than one that only says what to invoke it for.

### R05 — Under 500 lines

The `SKILL.md` itself is 444 lines — under the 500-line cap — despite covering a sprawling domain. Everything that would bloat it is split into 18 scoped sub-files, each linked by name from a "Detailed Reference Files" table. The agent is told to load only the sub-files its task actually requires.

> `claude/skills/shortcuts-playground/SKILL.md:182-201`:
>
> ```
> ## Detailed Reference Files
>
> For complete documentation, see:
> - [PLIST_FORMAT.md](PLIST_FORMAT.md) - Complete plist structure
> - [ICONS_AND_COLORS.md](ICONS_AND_COLORS.md) - Icon glyph + color selection
> - [ACTIONS.md](ACTIONS.md) - WF*Action identifiers and parameters
> - [APPINTENTS.md](APPINTENTS.md) - AppIntent actions (ToolKit + backups)
> - [PARAMETER_TYPES.md](PARAMETER_TYPES.md) - All parameter value types
> - [HEALTHKIT.md](HEALTHKIT.md) - iOS/iPadOS Health actions
> ...
> ```

> `claude/agents/shortcut-builder.md:53-54`:
>
> ```
> 2. **Read SKILL.md + relevant reference files.** Start with `SKILL.md` and `BEST_PRACTICES.md`.
>    Load `ACTIONS.md`, `APPINTENTS.md`, `THIRD_PARTY_ACTIONS.md`, `VARIABLES.md`,
>    `CONTROL_FLOW.md`, `FILTERS.md`, `PARAMETER_TYPES.md`, and `EXAMPLES.md` only when the
>    task requires them. Don't bulk-load everything upfront.
> ```

The sub-file split succeeds because each sub-file has a single clear scope (`HEALTHKIT.md` = Health actions, `DATE_TIME.md` = date formatting). Without that constraint, splitting a monolith just moves the bloat.

### R07 — Scope note when related skills exist

Both agents carry a boundary statement in their description and reinforce it in the body. The builder's body adds "You are NOT a generalist" and names the redirect. The remixer escalation protocol specifies exact fallback language for the orchestrator to relay.

> `claude/agents/shortcut-builder.md:19-21`:
>
> ```
> You are NOT a generalist. If the user asks you something that isn't about building a Shortcut,
> politely decline and return control to the main thread.
> ```

> `claude/agents/shortcut-remixer.md:34-44`:
>
> ```
> **If you cannot confidently identify a source path, STOP immediately.** Do not read any files,
> do not grep anything, do not guess. Escalate with exactly this message (fill in the bracketed
> part):
>
> > I couldn't find an absolute file path in your remix request. Options:
> > 1. Re-run with the path prefix, e.g. `/shortcuts-playground:remix /absolute/path/to/file.xml <your idea>`
> > 2. Export the shortcut as unsigned XML ...
> > 3. Name the shortcut in your Shortcuts library ...
> >
> > Received input: `[repeat $ARGUMENTS verbatim]`
> ```

Providing the verbatim escalation message is stronger than a generic "tell the user it failed" — it gives Claude a script that requires no judgment under pressure.

### R08 — Patterns over theory

The skill's "Key Rules" section runs to 57 numbered imperatives, each one naming the specific plist key or behavior that must or must not appear. No section titled "Understanding Variable References" — instead, rule 9 says "WFURL serialization: use `WFTextTokenString` with `￼` placeholders even when the URL is entirely a variable." The Craig Loop Protocol names its anti-patterns with labels and says what happens when you do them.

> `claude/skills/shortcuts-playground/SKILL.md:257-261`:
>
> ```
> ### Anti-patterns (do NOT do these)
> - **Chatting the validator**: Running the validator repeatedly without making meaningful code
>   changes between runs. Every re-run must follow a real edit.
> - **Cosmetic fixes**: Rearranging comments or renaming variables to "try something" when the
>   error is about wiring or missing parameters.
> - **Regenerating from scratch** when only 1-2 specific actions need fixing. Targeted edits
>   preserve working wiring.
> ```

> `claude/skills/shortcuts-playground/SKILL.md:381-385`:
>
> ```
> 1. **UUIDs must be uppercase and generated via `uuidgen`, not hand-picked.** Before emitting a
>    shortcut, run a single Bash call to generate all the UUIDs you'll need:
>    ```bash
>    for i in $(seq 1 <N>); do uuidgen | tr '[:lower:]' '[:upper:]'; done
>    ```
>    ...Never use sequential placeholders like `11111111-1111-1111-1111-111111111111`...
> ```

Anti-patterns labeled with names ("Chatting the validator") are more memorable than a list of "don't do X" bullet points, because the label gives Claude something to match against when it catches itself doing the thing.

### R13 — System prompt structure: mission → steps → boundaries → format

The builder opens with a two-sentence mission, runs a 10-step numbered workflow with concrete bash commands in each step, dedicates a "What you never do" section to hard prohibitions, and closes with "When you return control" listing the exact three fields to report. The remixer mirrors this shape with 11 numbered steps.

> `claude/agents/shortcut-builder.md:12-14` (mission):
>
> ```
> You are a specialist in authoring macOS/iOS Shortcuts as signed `.shortcut` files. Every task
> you receive boils down to producing one or more valid, signed, imported-ready Shortcuts that
> implement the user's intent. You do this by:
> ```

> `claude/agents/shortcut-builder.md:80-89` (boundaries → format):
>
> ```
> 10. **Verify + report (MANDATORY).** Before declaring the build complete, you must run:
>     ```bash
>     ls -la "<OUTPUT_DIR>/<shortcut name>.shortcut"
>     ```
>     and confirm the file exists with non-zero size. ...Only once `ls` confirms the signed file,
>     report to the user:
>     - The final signed `.shortcut` absolute path (they open this in Shortcuts.app).
>     - The archive XML absolute path (for diffing later).
>     - One-line summary of what the shortcut does and any caveats.
> ```

Embedding the exact `ls` command (not "verify the file") inside the mandatory step means Claude cannot satisfy the step with a hallucinated path. The format section doubles as a compliance test.

### R30 — Use `${CLAUDE_PLUGIN_ROOT}` for paths

Every executable path across the hook config, the hook script, and the SKILL.md uses `${CLAUDE_PLUGIN_ROOT}` rather than an absolute path. The hook script also carries a self-healing fallback: if the env var is unset, it resolves the plugin root from its own `$0`.

> `claude/hooks/hooks.json:8-10`:
>
> ```json
> {
>   "type": "command",
>   "command": "${CLAUDE_PLUGIN_ROOT}/hooks/auto-validate.sh"
> }
> ```

> `claude/hooks/auto-validate.sh:13-17`:
>
> ```bash
> PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-}"
> if [ -z "$PLUGIN_ROOT" ]; then
>   # Fallback: resolve from this script's own location (hooks/ -> plugin root).
>   PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
> fi
> ```

The fallback is the part most implementations miss. A hook configured with `${CLAUDE_PLUGIN_ROOT}` still breaks if the env var isn't set when the hook fires. The `dirname "$0"` fallback makes the script location-independent regardless of how Claude Code resolves the variable.

### R31 — Fail-open by default

The auto-validate hook exits 0 (silent pass-through) for every early-exit condition: missing plugin root, missing validator script, Python not installed, Python version too old, file not found, wrong extension, not a Shortcuts plist. It only exits non-zero (exit 2) when the validator actually runs and explicitly fails on the file the user just wrote.

> `claude/hooks/auto-validate.sh:14-70` (key exits):
>
> ```bash
> if [ -z "$PLUGIN_ROOT" ]; then
>   PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
> fi
>
> VALIDATOR="$PLUGIN_ROOT/skills/shortcuts-playground/scripts/validate_shortcut.py"
> if [ ! -f "$VALIDATOR" ]; then
>   exit 0   # Plugin mis-packaged. Stay silent.
> fi
>
> if ! command -v "$PY" >/dev/null 2>&1; then
>   exit 0   # Python missing — stay silent.
> fi
>
> if ! "$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
>   exit 0   # Interpreter too old. Stay silent.
> fi
>
> case "$FILE_PATH" in
>   *.xml|*.shortcut) : ;;
>   *) exit 0 ;;       # Not a shortcut file. Skip.
> esac
>
> if ! /usr/bin/grep -q 'WFWorkflowActions' "$FILE_PATH" 2>/dev/null; then
>   exit 0   # Not a Shortcuts plist. Skip.
> fi
> ```

Each silent exit has an inline comment explaining why — making the fail-open choice legible to future maintainers. A hook that silently kills writes to Markdown files because Python is missing would be reported as a plugin bug immediately.

## Worth adopting

**Pattern: Bounded fix loop with named exit conditions.** Evidence: `claude/agents/shortcut-builder.md:72` and `claude/skills/shortcuts-playground/SKILL.md:248-255`. The Craig Loop Protocol specifies max iterations (5), detects same-error recurrence across 2 consecutive attempts as a signal to stop rather than retry, and names documented false-positives as a third exit condition (`ALLOW_VCARD`, `ALLOW_TOKEN_FILE`). The rules file has no equivalent for "how many retries before escalating to the user." A candidate rule: **Specify max retry count and same-error-recurrence detection in any fix loop.** When neither bound is set, a failing QC check retries until context is exhausted — the same failure R47 addresses for orchestration loops, but R47 names only the count bound, not the recurrence signal.

**Pattern: Bounded research budget declared in the agent body.** Evidence: `claude/agents/shortcut-builder.md:119-123`. The builder states "you may use up to 8 total Read/Grep/Glob calls during the research phase before you must either start authoring or escalate to the user." This prevents agents from spending their entire turn budget on reference reads. No current rule codifies a per-phase tool-call budget as an agent invariant rather than a vague recommendation.
