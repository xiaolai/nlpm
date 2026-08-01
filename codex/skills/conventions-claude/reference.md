# Claude Code Conventions — Extended Reference

Detailed schemas split out of `SKILL.md` to keep the overlay under the 500-line cap (R05). Loaded on demand by the scorer/checker when an artifact involves LSP servers, monitors, or a tool-name validity question. The overlay's §12, §13, and §16 each point here.

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

`monitors/monitors.json` (default) or inline via `experimental.monitors` in `plugin.json`. **Stable in 2026** (was experimental in 2025). Plugin-level background watchers (logs, files, status). Requires Claude Code v2.1.105+.

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
- **Additional current events:** `Setup`, `SubagentStart`, `UserPromptExpansion`, `PermissionDenied`, `PostToolBatch`, `MessageDisplay`, `TaskCreated`, `TeammateIdle`, `ConfigChange`, `CwdChanged`, `WorktreeCreate`, `WorktreeRemove`, `PostCompact`, `Elicitation`, `ElicitationResult`.

---

## Plugin Distribution (marketplace.json)

`.claude-plugin/marketplace.json` at the marketplace repo root. **Required top-level:** `name`, `owner` (maintainer-info object), `plugins`. **Optional top-level:** `$schema`, `description`, `version`, `metadata.pluginRoot`, `allowCrossMarketplaceDependenciesOn`, `renames`.

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

**`source` types:** `relative path`, `github`, `url`, `git-subdir`, `npm`.

**`renames`** (v2.1.193+): an append-only map (`{oldName: newName | null}`) letting a marketplace rename or remove a plugin without breaking existing installs.
