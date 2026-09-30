# Claude Code Conventions — Extended Reference

Detailed schemas split out of `SKILL.md` to keep the overlay body under the 400-line R05 threshold. Loaded on demand by the scorer/checker when an artifact involves hooks.json, settings, auto-memory files, LSP servers, monitors, or a tool-name validity question. The overlay's §1, §8, §9, §11, §12, §13, §15, and §16 each point here.

---

## LSP Servers

`.lsp.json` (file form) or a `lspServers` object in `plugin.json` (inline form). **Stable in 2026** (was experimental in 2025). Schema documented in `plugins-reference.md`.

**Per-server fields:**
- `command` — **required**; LSP server executable
- `extensionToLanguage` — **required**; map of file extension → language id (e.g. `{ ".rs": "rust" }`)
- `args` — string array
- `transport` — `"stdio"` (default) or `"socket"`
- `env` — environment variables
- `initializationOptions` — passed at LSP `initialize`
- `settings` — server-specific settings
- `workspaceFolder` — workspace root override
- `startupTimeout` — milliseconds
- `maxRestarts` — restart cap

Supports `${CLAUDE_PLUGIN_ROOT}` substitution in paths.

---

## Monitors

`monitors/monitors.json` (default) or inline via `experimental.monitors` in `plugin.json`. **Experimental**: it moved under `experimental.monitors` and its schema may change between releases (see SKILL.md §13). Plugin-level background watchers (logs, files, status). Requires Claude Code v2.1.105+.

**Format:** JSON array; per-entry fields:
- `name` — **required**; identifier
- `command` — **required**; shell command to run
- `description` — **required**; what it watches
- `when` — `"always"` (default) or `"on-skill-invoke:<skill-name>"`

Substitutions supported: `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${CLAUDE_PROJECT_DIR}`, `${user_config.*}`.

---

## Tool Catalog

Tool names valid in `tools:`, `allowed-tools:`, and `disallowed-tools:`. Do NOT flag any as "undocumented" or "unknown". Authoritative source: `code.claude.com/docs/en/tools-reference.md`.

**Renames / removals (corrected 2026-06-07):**
- `Task` → **`Agent`** (renamed v2.1.x; `Task(...)` still works as an alias — both are valid).
- `MultiEdit` — **removed** (use `Edit` with `replace_all`). Still tolerable as a legacy name, but no longer the default.
- `BashOutput`, `KillBash` — **removed** (background tasks now managed via the `Task*` family and `Read` on the output file).
- `TodoWrite` — disabled by default (v2.1.14x), superseded by `TaskCreate`/`TaskGet`/`TaskList`/`TaskUpdate`. Still a valid name.
- `SlashCommand` — folded into `Skill` (commands invoked via the `Skill` tool); not in the current catalog table.

**Built-in tools (current):**
- File I/O: `Read`, `Write`, `Edit`, `NotebookEdit`
- Discovery: `Glob`, `Grep`
- Execution: `Bash`, `PowerShell`
- Agent / multi-agent: `Agent`, `SendMessage`, `TeamCreate`, `TeamDelete`, `Workflow`
- Tasks: `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate`, `TaskStop`
- Planning / worktrees: `EnterPlanMode`, `ExitPlanMode`, `EnterWorktree`, `ExitWorktree`
- Scheduling: `ScheduleWakeup`, `CronCreate`, `CronDelete`, `CronList`
- Web: `WebFetch`, `WebSearch`
- User interaction: `AskUserQuestion`, `PushNotification`
- Skill / tool discovery: `Skill`, `ToolSearch`
- Dev surfaces: `Monitor`, `LSP`
- MCP plumbing: `ListMcpResourcesTool`, `ReadMcpResourceTool`, `WaitForMcpServers`
- Remote: `RemoteTrigger`

**MCP tools:** `mcp__<server-name>__<tool-name>` (e.g., `mcp__mermaider__validate_syntax`).

Tool names are case-sensitive. Any string matching the patterns above is a valid tool reference regardless of whether this document pre-dates the tool's introduction — the catalog grows; never penalize an unrecognized-but-well-formed tool name.

---

## Hook Events (extended allow-list)

The overlay's §7 table lists the load-bearing events; the following are also valid current events — never flag any of them as "unknown". Any documented event name is valid even if it post-dates this doc; verify against `code.claude.com/docs/en/hooks.md` rather than penalizing.

- **Confirmed real (were "uncertain" pre-2026-06):** `SubagentStop`, `PreCompact`, `Notification`, `PostToolUseFailure`, `InstructionsLoaded`, `TaskCompleted` (exact spelling — not `TaskComplete`).
- **Additional current events:** `Setup`, `SubagentStart`, `UserPromptExpansion`, `PermissionDenied`, `PostToolBatch`, `MessageDisplay`, `TaskCreated`, `TeammateIdle`, `ConfigChange`, `CwdChanged`, `WorktreeCreate`, `WorktreeRemove`, `PostCompact`, `Elicitation`, `ElicitationResult`, `DirectoryAdded`, `PreModelSwitch`, `PostModelSwitch`.

---

## Plugin Distribution (marketplace.json)

`.claude-plugin/marketplace.json` at the marketplace repo root. **Required top-level:** `name`, `owner` (maintainer-info object), `plugins`. `owner` requires `name`. **Optional top-level:** `$schema`, `description`, `version`, `metadata.description`, `metadata.version`, `metadata.pluginRoot`, `forceRemoveDeletedPlugins`, `allowCrossMarketplaceDependenciesOn`, `renames`. Each plugin entry requires `name` and `source`.

```json
{
  "name": "marketplace-name",
  "owner": { "name": "maintainer" },
  "plugins": [
    {
      "name": "plugin-name",
      "source": { "source": "github", "repo": "owner/repo" },
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

**Per-plugin entry** may add `category`, `tags`, `strict`, `relevance`, `defaultEnabled` on top of the plugin-manifest fields. `strict: false` makes the marketplace entry the sole authority over that plugin's `plugin.json`.

**`source` types:** a relative-path string (starting with `./`, or a bare name under `metadata.pluginRoot`), or an object whose `source.source` is one of six types (required fields in parentheses): `github` (`repo`), `url` (`url`), `git-subdir` (`url`, `path`), `npm` (`package`), `archive` (`url`, v2.1.224+), `command` (`command`, v2.1.229+).

**`renames`** (v2.1.193+): an append-only map (`{oldName: newName | null}`) letting a marketplace rename or remove a plugin without breaking existing installs.

---

## hooks.json Format

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

**Optional hook-object fields (current — do NOT flag as malformed):** `if` (Bash-pattern, permission-scoped condition), `timeout` (seconds), `statusMessage`, `once` (v2.1+; skills/agents only), exec-form `args` (array, as an alternative to shell-form `command`), and `async` / `asyncRewake` for background command hooks.

---

## Settings Fields

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
| `claudeMd`, `claudeMdExcludes` | Extra memory file globs / exclusions. **`claudeMd` is honored only in managed/policy settings — it has no effect in user/project/local settings.** |
| `skillOverrides` | Per-skill visibility from settings (keys = skill name; values `on` / `name-only` / `user-invocable-only` / `off`); overrides the skill's own frontmatter |
| `pluginConfigs` | Stores non-sensitive plugin `userConfig` values under `pluginConfigs[<plugin-id>].options` |
| `autoMemoryEnabled`, `autoMemoryDirectory` | Auto-memory toggle + location (see §15) |
| `sandbox.enabled` | Sandbox execution toggle |
| `extraKnownMarketplaces`, `strictKnownMarketplaces` | Marketplace trust config |

> `theme` is **not** a documented `settings.json` field — do not flag its absence or treat it as valid here (removed from this list 2026-06-07). The above is representative, not exhaustive; treat unrecognized-but-plausible keys as advisory, not errors.

**Rule:** `.local.json` is gitignored (per-user); the non-local file is shared. NEVER set `bypassPermissions: true` in the shared file.

---

## Memory File Conventions

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

## plugin.json Example

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

## .mcp.json Example

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
