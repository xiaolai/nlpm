# NLPM Scoring — Codex CLI Tables

Penalty tables for Codex CLI (Tier 2-Codex) artifacts. Part of the `nlpm:scoring` rubric: the formula, the shared tables (including the universal Hooks checks), the score bands and the false-positive list are in `../SKILL.md`. These rows carry the same weight as the rows there.

---

### Hooks (Codex CLI — Tier 2-Codex only)

Authoritative event list: `nlpm:conventions-codex` §6.

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R27 | Event names valid (Codex) | Uses unrecognized event name — confirmed Codex events: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PermissionRequest`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`, `Stop` | -15 |
| R27 | Case correct (Codex) | Event name has wrong case | -10 |
| -- | Hooks config key (Codex) | `config.toml` uses deprecated `[features].codex_hooks` instead of `[features].hooks` (renamed ~CLI 0.129+) | -5 (advisory) |

---

### .codex-plugin/plugin.json (Codex CLI — Tier 2-Codex only)

Schema reference: `nlpm:conventions-codex` §3.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid JSON | File fails JSON parse | -25 |
| `name` present | Missing | -25 |
| `name` kebab-case | Mixed case or underscores | -10 |
| `version` is semver | Present but not valid semver | -10 |
| `description` present | Missing | -5 |
| Artifact paths relative | `skills`/`mcpServers`/`apps`/`hooks` paths absolute or missing `./` prefix | -5 each |

---

### .agents/plugins/marketplace.json (Codex marketplace — Tier 2-Codex)

Schema reference: `nlpm:conventions-codex` §4. Schema is largely compatible with Claude's `.claude-plugin/marketplace.json`.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid JSON | File fails JSON parse | -25 |
| `name` present | Missing | -25 |
| `plugins` array present | Missing or empty | -10 |
| Per-plugin `source` valid | `source.source` not in `github`/`git`/`local`, or required `repo`/`path` missing | -10 each |
| Per-plugin `category` present | Missing (informational, helps marketplace navigation) | -3 each |

---

### agents/openai.yaml (Codex skill sidecar — Tier 2-Codex)

Schema reference: `nlpm:conventions-codex` §2.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid YAML | File fails YAML parse | -25 |
| Sidecar is colocated | `agents/openai.yaml` not in same directory as a `SKILL.md` | -10 |
| `interface.display_name` present | Missing | -5 (informational) |

---

### .codex/config.toml (Codex configuration — Tier 2-Codex)

Schema reference: `nlpm:conventions-codex` §5.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid TOML | File fails TOML parse | -25 |
| Deprecated `[features].codex_hooks` | Should be `[features].hooks` (renamed ~CLI 0.129) | -5 (advisory) |
| Per-MCP `command` present | `[mcp_servers.<id>]` table missing `command` field | -15 each |
