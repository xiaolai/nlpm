---
name: conventions-claude
description: "Use when scoring or writing Claude Code artifacts — covers .claude/ paths, plugin.json schema, command + agent + skill frontmatter, CLAUDE.md, hook events, hooks.json format, settings.json, LSP, monitors, memory file conventions, and the Claude Code built-in tool catalog. Refreshed 2026-06-07 against docs map dated 2026-06-05 (Claude Code ≥ v2.1.16x)."
version: 0.2.0
---

# Claude Code Conventions

Tool-specific overlay for Claude Code plugin artifacts. Loaded by the scorer and checker when an artifact is classified as **Tier 2-Claude** (per `agents/scorer.md` step 3). The universal floor lives in `nlpm:conventions`; this overlay adds Claude-Code-specific schemas on top.

**Primary authoritative sources:**
- <https://code.claude.com/docs/en/claude_code_docs_map.md>
- <https://code.claude.com/docs/en/skills.md>
- <https://code.claude.com/docs/en/hooks.md>
- <https://code.claude.com/docs/en/plugins.md>
- <https://code.claude.com/docs/en/plugins-reference.md>
- <https://code.claude.com/docs/en/sub-agents.md>
- <https://code.claude.com/docs/en/settings.md>
- <https://code.claude.com/docs/en/memory.md>
- <https://code.claude.com/docs/en/slash-commands.md>
- <https://code.claude.com/docs/en/tools-reference.md> — **authoritative built-in tool catalog** (see §16)
- <https://code.claude.com/docs/en/plugin-marketplaces.md>

---

## 1. `.claude-plugin/plugin.json`

The plugin manifest.

**Required fields:**
- `name` — string, kebab-case, unique identifier

The manifest is **fully optional** — artifacts auto-discover from conventional paths, and only `name` is required when present. Unrecognized top-level fields are ignored with a warning (error only under `claude plugin validate --strict`).

**Optional fields:**
- `version` — semver string (e.g. `"0.1.0"`). If omitted, commit SHA is used (every commit = new version). For stable releases, set explicit semver.
- `description` — one-line summary
- `displayName` — human-readable name shown in installer UI (v2.1.143+)
- `author` — object: `{ "name": "...", "email": "...", "url": "..." }`
- `homepage` — URL string
- `repository` — URL string or object
- `license` — SPDX identifier
- `keywords` — string array for discovery
- `$schema` — URL to the manifest JSON Schema (editor validation)
- `defaultEnabled` — boolean; whether the plugin is enabled on install (v2.1.154+)
- `userConfig` — object; per-key prompts shown to the user at enable time; values exposed as `${user_config.<key>}` substitutions
- `channels` — array; message-injection channel bindings
- `dependencies` — array of other plugins this one requires (supports semver constraints)

**NOT plugin.json fields (common mistake):**
- `agent` — this is a **settings.json** default key (a plugin's bundled `settings.json` supports only `agent` and `subagentStatusLine`), not a manifest field.
- `category` — belongs to a **marketplace.json** plugin entry, not the manifest.

**Artifact path fields (all optional, string or string[]):**
- `commands` — path(s) to command markdown files
- `agents` — path(s) to agent markdown files
- `skills` — path(s) to skill directories
- `hooks` — path to hooks.json
- `mcpServers` — path(s) to MCP server config
- `lspServers` — path(s) to LSP server config (stable in 2026; schema in §12)
- `outputStyles` — path(s) to output style definitions
- `experimental.themes` — path(s) to theme definitions (was top-level `themes`; now nested under `experimental`)
- `experimental.monitors` — path(s) to monitor config (was top-level `monitors`; schema in §13). Top-level still works but `claude plugin validate` warns; a future release will require the `experimental.*` form.

**Example:**
```json
{
  "name": "my-plugin",
  "version": "0.2.1",
  "description": "Does useful things",
  "author": { "name": "dev" },
  "license": "MIT",
  "keywords": ["tools", "productivity"],
  "commands": "commands/",
  "agents": "agents/",
  "skills": "skills/"
}
```

---

## 2. Commands and Skills — merged surfaces (v2.1.x change)

**Critical:** as of Claude Code v2.1.x, commands and skills are the **same architecture**. Both surfaces support the same frontmatter and execution semantics. The recommended canonical path is:

```
.claude/skills/<name>/SKILL.md     # preferred for new development
.claude/commands/<name>.md         # still works; equivalent behavior
```

Existing `.claude/commands/` files continue to function. New code should prefer the skill layout because it allows companion files (`scripts/`, `references/`, `examples/`) in the same directory.

**Authoritative reference:** <https://code.claude.com/docs/en/slash-commands>

### 2.1 Frontmatter (shared between commands and skills)

**Required:**
- `description` — string; explains what it does and when to invoke. Combined with `when_to_use:` if present.

**Optional (universal):**
- `name` — string; per official docs, **explicitly optional**. When omitted, filename or enclosing directory is used. Pre-v0.7.15 nlpm incorrectly flagged missing `name:` as a bug; corrected after Jeffallan/claude-skills#184 maintainer feedback.
- `argument-hint` — string; placeholder shown in UI (e.g., `"[path]"`)
- `arguments` — space-separated or YAML list of named arguments for `$name` substitution (e.g., `"issue branch"`)
- `allowed-tools` — string array OR space-separated string; pre-approved tools (no per-use prompt). Format: `"Read Grep Bash(git *)"` or `["Read", "Grep"]`.
- `disallowed-tools` — string array OR space-separated string; tools removed from the pool while the skill is active.
- `model` — `haiku` / `sonnet` / `opus` / a full model ID / **`inherit`** (keep the active model); overrides session model for one turn.
- `effort` — `low` / `medium` / `high` / `xhigh` / `max`; overrides session effort.
- `user-invocable` — boolean; `false` hides from menu (only Claude invokes).
- `disable-model-invocation` — boolean; `true` means only the user invokes (manual `/skill-name` only).

**Optional (v2.1.x additions — NEW since pre-2026 conventions):**
- `when_to_use` — string; additional trigger hints (appends to description)
- `context` — `"fork"` runs in a forked subagent (isolates from main history)
- `agent` — which subagent type (built-in: `Explore`, `Plan`, `general-purpose`)
- `hooks` — `{...}` skill-scoped hooks (same shape as settings.json hooks)
- `paths` — glob patterns; auto-load only for matching files (e.g., `"src/**/*.ts,lib/**/*.ts"`)
- `shell` — `bash` (default) or `powershell` for `!`cmd`` blocks

### 2.2 Body conventions

- Write imperative instructions directed at Claude (not the user)
- Use numbered steps for multi-phase workflows
- Reference shared partials by relative path: `commands/shared/name.md`
- Define expected output format explicitly in the body

### 2.3 Dynamic context injection

- `` !`git diff HEAD` `` — runs command before Claude sees the skill; replaces line with output.
- ` ```! ` fenced blocks — multi-line commands.
- Disabled if `"disableSkillShellExecution": true` in settings.

### 2.4 String substitutions (valid in command/skill bodies)

`$ARGUMENTS`, `$ARGUMENTS[N]`, `$N` (positional), `$name` (named argument), `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PLUGIN_ROOT}`. Do NOT flag these as undefined variables.

---

## 3. Shared Partials

Reusable shared partials located in `commands/shared/`.

**Rules:**
- MUST include `user-invocable: false` in frontmatter — prevents appearing as top-level commands
- MUST have a `description` stating their purpose as a partial
- Referenced by full relative path from the consuming command file
- Can contain any mix of instructions, templates, or decision logic

---

## 4. Agent Frontmatter

Agents live in `.claude/agents/<name>.md`.

**The system prompt is the markdown body** of the file (in `--agents` JSON form it is the `prompt` key). There is **no `system-prompt` frontmatter key** — flagging or recommending one is a bug (corrected 2026-06-07 against `sub-agents.md`).

**Documented fields:**
- `name` — string; identifier for invocation
- `description` — string; critical for reliable triggering — should contain 3+ specific phrases describing when to use this agent
- `tools` — tools the agent body uses; two valid formats:
  - JSON array: `tools: ["Read", "Glob"]`
  - Comma-separated string: `tools: Read, Glob, Grep`
- `disallowedTools` — tools removed from the inherited pool (this is the correct key — there is **no** `tool-restrictions: {allow, deny}` key; the old nlpm name was wrong)
- `model` — `haiku` / `sonnet` / `opus` / a full ID (e.g. `claude-opus-4-8`) / `inherit`; **defaults to `inherit`**
- `skills` — preload skill content into this agent's context at startup. Two valid formats:
  - JSON array: `skills: ["nlpm:conventions"]`
  - YAML list: `skills:\n  - nlpm:conventions`

**Convention / additional fields:**
- `effort` — `low` / `medium` / `high` / `xhigh` / `max`
- `color` — one of `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan`; visual label. **`magenta` is NOT valid** (old nlpm list had it; the current valid set adds `purple`, `orange`, `pink`).
- `permissionMode` — `default` / `acceptEdits` / `auto` / `dontAsk` / `bypassPermissions` / `plan`
- `isolation` — only valid value `"worktree"` (runs the agent in a git worktree)
- `memory` — `user` / `project` / `local`
- `maxTurns` — integer turn cap
- `background` — boolean; run asynchronously
- `initialPrompt` — string; seeds the agent's first turn
- `mcpServers`, `hooks` — agent-scoped overrides

**Plugin-shipped agents are restricted:** `hooks`, `mcpServers`, and `permissionMode` are **ignored** for agents distributed inside a plugin (security). Score plugin agents accordingly.

**Best practice: include `<example>` blocks in description.** Two or more `<example>` blocks with diverse scenarios is the minimum for reliable triggering.

---

## 5. Skills — Claude Code path conventions

Universal SKILL.md spec lives in `nlpm:conventions` (open spec at agentskills.io). Claude Code uses these path conventions:

- Single plugin skill: `skills/<name>/SKILL.md`
- Multi-skill plugin: `skills/<plugin>/<name>/SKILL.md`
- Project-scoped: `.claude/skills/<name>/SKILL.md`
- User-scoped: `~/.claude/skills/<name>/SKILL.md`

**Skill discovery paths now support parent-directory and monorepo nested scanning** (v2.1.x). Skills from `./parent/.claude/skills/` and `./packages/frontend/.claude/skills/` auto-load. Skills from `--add-dir` paths also load from `.claude/skills/` within added directories.

**Supporting files:** Same directory as `SKILL.md` — `scripts/`, `references/`, `examples/`, etc. Reference them from `SKILL.md` so Claude knows when to load them.

**Skill preloading in agents (v2.1.x):** Declare `skills: [name1, name2]` in agent frontmatter to inject full skill content at startup (vs. Claude auto-loading on demand).

---

## 6. Rules

Rules live in `.claude/rules/<name>.md`.

**Frontmatter:**
- `description` — string (required)
- `paths` — string array (optional); glob patterns scoping which files this rule applies to

**Body format:**
- Lead with a **bold imperative**: `**Always do X.**` or `**Use Y instead of Z.**`
- Follow immediately with rationale
- Be specific and testable
- State what to DO, not only what to avoid (Pink Elephant effect)

**Budget:** Under 500 lines total per rules file.

**Naming convention for ordered sets:** `NN-kebab-name.md` (e.g. `01-formatting.md`).

---

## 7. Hook Events (Claude Code)

Hook events are **case-sensitive**. Using wrong case silently ignores the hook.

**Confirmed against 2026-06-07 docs refresh (`hooks.md`):**

| Event | Trigger | Context fields |
|---|---|---|
| `SessionStart` | Session begin | `source` (startup/resume/clear/compact), `model` |
| `SessionEnd` | Session end | (trigger only) |
| `UserPromptSubmit` | User submits a prompt | `prompt` text |
| `PreToolUse` | Before any tool call | `tool_name`, `tool_input` |
| `PostToolUse` | After tool call | `tool_name`, `tool_input`, `tool_output` |
| `PermissionRequest` | When Claude requests permission | `tool_name`, `tool_input`, `permission_mode` |
| `Stop` | Once per turn | `reason` (can set `decision: block` to prevent stopping) |
| `StopFailure` | Once per turn — Claude failed to complete | `reason` |
| `FileChanged` | Per file change | `filename`, `watcher_path` |

**Now confirmed real (were "uncertain" in v0.1.0 — resolved 2026-06-07):**
`SubagentStop`, `PreCompact`, `Notification`, `PostToolUseFailure`, `InstructionsLoaded`, `TaskCompleted` (exact spelling — not `TaskComplete`). These are valid events; do NOT flag them as unknown.

**Additional current events (add to the known-event allow-list):**
`Setup`, `SubagentStart`, `UserPromptExpansion`, `PermissionDenied`, `PostToolBatch`, `MessageDisplay`, `TaskCreated`, `TeammateIdle`, `ConfigChange`, `CwdChanged`, `WorktreeCreate`, `WorktreeRemove`, `PostCompact`, `Elicitation`, `ElicitationResult`. Any string matching a documented event name is valid regardless of whether it post-dates this doc — when in doubt, verify against `code.claude.com/docs/en/hooks.md` rather than penalizing.

**Hook types** (canonical, all lowercase in JSON):
- `command` — shell script (stdin/stdout)
- `http` — HTTP POST endpoint
- `mcp_tool` — MCP server tool invocation
- `prompt` — LLM evaluation
- `agent` — subagent verification

A `command` hook may add `"shell": "powershell"` to run that hook in PowerShell instead of the default shell.

**Matcher patterns:** string (exact), pipe-separated list (`Bash|Edit`), or regex (non-alphanumeric chars).

**MCP tool naming:** `mcp__<server>__<tool>` (e.g., `mcp__memory__write.*`). Hook matchers use this format.

**Exit codes (command hooks):**
- `0` — success (stdout to debug log; for `UserPromptSubmit`, `UserPromptExpansion`, and `SessionStart`, stdout is injected as context)
- `2` — blocking error (action denied, stderr fed to Claude) — **only on blockable events**. Non-blockable events ignore exit 2: `PostToolUse`, `PostToolUseFailure`, `Notification`, `SessionStart`, `SessionEnd`, `InstructionsLoaded`, `StopFailure`, `MessageDisplay`.
- `1, 3+` — non-blocking error (logged in debug only)

---

## 8. `hooks.json` Format

Located at `.claude/hooks.json` or `<plugin>/hooks/hooks.json`.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/pre-write-check.sh"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are now in strict TDD mode."
          }
        ]
      }
    ]
  }
}
```

**Structure rules:**
- Top-level key: `"hooks"`
- Second-level keys: event names (case-sensitive)
- Each event maps to an array of matcher objects: `{ "matcher": "<regex>", "hooks": [...] }`
- Each hook object: `{ "type": "command"|"http"|"mcp_tool"|"prompt"|"agent", "<type-field>": "..." }`
- Field name matches the type: `"command"` for type `command`, `"prompt"` for type `prompt`, etc.

---

## 9. `.mcp.json`

Claude Code reads MCP server registrations from a **standalone JSON file** at the repo root (NOT embedded in `settings.json` like Gemini, NOT inside `config.toml` like Codex).

```json
{
  "mcpServers": {
    "my-server": {
      "type": "stdio",
      "command": "node",
      "args": ["./server.js"]
    }
  }
}
```

Plugin scope: `<plugin>/.claude-plugin/.mcp.json` or `<plugin>/.mcp.json` (path per `plugin.json`).

---

## 10. CLAUDE.md (memory file)

Project-scoped: `CLAUDE.md` at repo root, plus optional `.claude/memory/*.md`. User-scoped: `~/.claude/CLAUDE.md`.

**Recommended pattern for multi-tool projects** (per `analysis/multi-tool-design-2026-05.md` decision #5): use a one-line `CLAUDE.md` that imports `AGENTS.md`:

```markdown
@AGENTS.md
```

This makes AGENTS.md the canonical universal memory file. AGENTS.md is what Codex reads natively; Gemini/Antigravity can be configured to read it via `context.fileName` array. This is how nlpm itself works.

**Body conventions** when content lives in CLAUDE.md directly:
- Build/run instructions
- Test commands
- Architecture overview (what lives where)
- Prerequisites section
- Valid `@`-imports must reference existing files

---

## 11. `.claude/settings.json` and `.claude/settings.local.json`

| Field | Purpose |
|---|---|
| `permissions` | Permission policy (allow/deny rules, modes); incl. `permissions.additionalDirectories` |
| `hooks` | Hook event registrations (alternative to `hooks/hooks.json` for project-scoped hooks) |
| `model` | Default model selection |
| `disableSkillShellExecution` | If `true`, disables `!`...`` and ` ```! ` dynamic blocks in skills |
| `env` | Environment variables injected into the session |
| `statusLine` | Custom status line command/config |
| `agent` | Default agent (also the only default-settings key, besides `subagentStatusLine`, a plugin may set) |
| `effortLevel` | Default effort |
| `language`, `outputStyle` | Locale / output style defaults |
| `enabledPlugins` | Plugins enabled for the project |
| `claudeMd`, `claudeMdExcludes` | Extra memory file globs / exclusions |
| `autoMemoryEnabled`, `autoMemoryDirectory` | Auto-memory toggle + location (see §15) |
| `sandbox.enabled` | Sandbox execution toggle |
| `extraKnownMarketplaces`, `strictKnownMarketplaces` | Marketplace trust config |

> `theme` is **not** a documented `settings.json` field — do not flag its absence or treat it as valid here (removed from this list 2026-06-07). The above is representative, not exhaustive; treat unrecognized-but-plausible keys as advisory, not errors.

**Rule:** `.local.json` is gitignored (per-user); the non-local file is shared. NEVER set `bypassPermissions: true` in the shared file.

---

## 12. LSP Servers (`.lsp.json`)

**Stable in 2026** (was experimental in 2025). `.lsp.json` file, or a `lspServers` object in `plugin.json`. Required fields `command` + `extensionToLanguage`. **Full per-server schema → [reference.md](reference.md#lsp-servers).**

---

## 13. Monitors (`monitors/monitors.json`)

**Stable in 2026** (was experimental in 2025). Plugin background watchers; requires v2.1.105+; inline via `experimental.monitors` (§1). Per-entry required `name` + `command` + `description`. **Full schema → [reference.md](reference.md#monitors).**

---

## 14. Reference Syntax

**Commands referencing shared partials:**
```
<!-- Include: commands/shared/discover.md -->
```
Or by instruction: "Follow the steps in commands/shared/discover.md"

**Agents referencing skills in frontmatter:**
```yaml
skills: ["nlpm:conventions", "nlpm:conventions-claude"]
```

**Hooks referencing scripts:**
```json
"command": "${CLAUDE_PLUGIN_ROOT}/scripts/check.sh"
```

**Always use `${CLAUDE_PLUGIN_ROOT}` for intra-plugin file references.** Hardcoded absolute paths break portability.

**Cross-plugin skill references** use the same `plugin:skill` format. The plugin must be installed for the reference to resolve.

---

## 15. Memory File Conventions (`~/.claude/projects/<slug>/memory/`)

Claude Code writes per-project persistent memory at `~/.claude/projects/<project-slug>/memory/` ("Auto memory", v2.1.59+). Toggled by `autoMemoryEnabled`; location overridable via `autoMemoryDirectory` (§11). At session start the first ~200 lines / 25 KB of `MEMORY.md` plus topic files are loaded into context.

**Index file:** `MEMORY.md` (no frontmatter; one-line-per-entry index).

**Individual memory files** MUST include YAML frontmatter:

```yaml
---
name: "short identifier"
description: "one-line summary"
type: user | feedback | project | reference
---
```

**`type` values:**

| Value | Meaning |
|---|---|
| `user` | Preferences, habits, or facts about the user |
| `feedback` | Corrections or lessons from past sessions |
| `project` | Project-specific facts, decisions, or context |
| `reference` | External reference material copied into memory |

**Rules:**
- Every memory file must appear in `MEMORY.md` (orphans are flagged).
- `MEMORY.md` itself is the index; not scored as a memory file.
- Memory files should not reference removed files or functions.

---

## 16. Claude Code Tool Catalog

Tool names valid in `tools:`, `allowed-tools:`, `disallowed-tools:`. **Never flag a well-formed tool name as "unknown" or "undocumented"** — the catalog grows and any string matching `Pascal`-name or `mcp__<server>__<tool>` patterns is valid. Key renames: `Task` → **`Agent`** (alias kept); `MultiEdit`, `BashOutput`, `KillBash` **removed**; `TodoWrite` default-off (→ `Task*` family); `SlashCommand` folded into `Skill`.

**Full catalog — built-in tools, renames/removals, MCP naming → [reference.md](reference.md#tool-catalog).** Authoritative source: `code.claude.com/docs/en/tools-reference.md`.

---

## 17. Plugin distribution

**Marketplace manifest:** `.claude-plugin/marketplace.json` at the marketplace repo root. Schema:

```json
{
  "name": "marketplace-name",
  "plugins": [
    {
      "name": "plugin-name",
      "source": {
        "source": "github",
        "repo": "owner/repo"
      },
      "description": "...",
      "version": "1.0.0",
      "author": { "name": "..." },
      "repository": "https://github.com/owner/repo",
      "license": "MIT",
      "category": "developer-tools"
    }
  ]
}
```

**Plugin from URL (v2.1.x):** `--plugin-url` and `--plugin-dir` flags accept `.zip` archives.

**Namespacing:** Skills are namespaced (`/my-plugin:hello`). Commands and agents use short names. Prevents conflicts between plugins.

---

## 18. Scope and uncertainty

This skill covers Claude Code conventions. It does NOT cover:
- Universal SKILL.md spec → `nlpm:conventions`
- Penalty tables → `nlpm:scoring`

**Resolved in the 2026-06-07 refresh (no longer uncertain):**
- The six previously-uncertain hook events are confirmed real (§7).
- LSP server schema (`.lsp.json`) — now documented (§12).
- Monitor schema (`monitors/monitors.json`) — now documented (§13).

**Still approximate (verify before citing a specific tag):**
- Exact version-gate tags (e.g. v2.1.142 for `TodoWrite` default-off, v2.1.154 for `defaultEnabled`) came from a summarizing fetch; the *change* is confirmed, the precise version is approximate.
- `userConfig` / `channels` / `dependencies` plugin.json field shapes are listed but not field-by-field enumerated here.
- `plugin-marketplaces.md` full field schema not yet folded into §17.
