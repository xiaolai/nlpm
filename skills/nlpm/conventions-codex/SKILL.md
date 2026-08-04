---
name: conventions-codex
description: "Use when scoring or writing Codex CLI artifacts — covers .codex/config.toml schema, .codex-plugin/plugin.json, .agents/skills/ layout, Codex hook events, AGENTS.md hierarchy, marketplace.json, and the agents/openai.yaml sidecar. Refreshed 2026-08-02 against Codex 0.146.0 (2026-07-29); §3/§4 field-type + policy-enum corrections 2026-08-04."
version: 0.3.1
---

# Codex CLI Conventions

Tool-specific overlay for OpenAI Codex CLI artifacts. Loaded by the scorer and checker when an artifact is classified as **Tier 2-Codex** (per `agents/scorer.md` step 3). The universal floor lives in `nlpm:conventions`; this overlay adds Codex-specific schemas on top.

**Primary authoritative sources:**
- <https://learn.chatgpt.com/docs> (the `developers.openai.com/codex/*` tree now 308-redirects here)
- <https://learn.chatgpt.com/docs/build-skills>
- <https://learn.chatgpt.com/docs/agent-configuration/agents-md>
- <https://learn.chatgpt.com/docs/agent-configuration/subagents>
- <https://learn.chatgpt.com/docs/config-file/config-reference>
- <https://learn.chatgpt.com/docs/hooks>
- <https://learn.chatgpt.com/docs/skills-and-plugins>
- <https://learn.chatgpt.com/docs/changelog>
- <https://github.com/openai/codex> (authoritative for `CLA.md`, `contributing.md`, and machine-readable spec samples like `plugin-json-spec.md`)

---

## 1. File system layout

Codex separates the **cross-tool surface** (`.agents/`) from the **Codex-private surface** (`.codex/`). The Claude Code mental model of "everything under one tool directory" does not transfer.

| Artifact | Project scope | User scope |
|---|---|---|
| Skills | `.agents/skills/<name>/SKILL.md` (CWD→repo-root scan) | `~/.agents/skills/`, admin `/etc/codex/skills/` |
| Plugin manifest | `<plugin-root>/.codex-plugin/plugin.json` | — |
| Marketplace | `.agents/plugins/marketplace.json` (+ legacy `.claude-plugin/marketplace.json`) | `~/.agents/plugins/marketplace.json` |
| AGENTS.md | Git root → CWD; per dir `AGENTS.override.md` → `AGENTS.md` → fallback (one file/dir; closer overrides earlier) | `~/.codex/AGENTS.override.md`, `~/.codex/AGENTS.md` |
| Config | `.codex/config.toml` (trust-gated) | `~/.codex/config.toml` |
| Hooks | `.codex/hooks.json` OR inline `[hooks]` in `config.toml` | `~/.codex/hooks.json` |
| Slash commands / prompts | — (not project-shareable) | `~/.codex/prompts/<name>.md` |
| MCP servers | `[mcp_servers.<id>]` table inside `config.toml` | same |
| Skill sidecar (Codex-specific) | `<skill>/agents/openai.yaml` next to `SKILL.md` | — |

**Trust gate:** Project hooks load only when `.codex/` is trusted. Trust is enforced via `/hooks` and `allow_managed_hooks_only` in `requirements.toml`.

---

## 2. SKILL.md (Tier 1, open spec — `name`, `description` required only)

Codex reads SKILL.md from `.agents/skills/`, **not** `.codex/skills/` (reconfirmed 2026-08-02 against `build-skills`: *"Codex reads skills from `.agents/skills` directories, not `.codex/skills`"*; it scans `.agents/skills` from CWD up to the repo root, plus `~/.agents/skills` and `/etc/codex/skills`). Skills placed under `.codex/skills/` — a common mistake in repos ported from Claude Code's `.claude/skills/` habit — are **not discovered** by Codex; flag them. The required frontmatter is the agentskills.io baseline — `name` and `description` — same as every other tool.

**Codex-specific extras live in a SIDECAR `agents/openai.yaml`**, not in SKILL.md frontmatter. Treat the sidecar as additive metadata, not a deviation from the open spec.

**Sidecar fields:**
```yaml
# <skill>/agents/openai.yaml
interface:
  display_name: "My Skill"
  short_description: "One-line summary"      # added 2026-06
  default_prompt: "Use this skill when..."
  icon_small: "icon-16.png"
  icon_large: "icon-512.png"                 # added 2026-06
  brand_color: "#FF6B00"
policy:
  allow_implicit_invocation: true            # default true; set false to disable auto-selection
dependencies:
  tools:
    - type: "bash"
      value: "jq"
      description: "JSON processor"
      transport: "stdio"
```

**Correction (2026-06-07):** `dependencies.tools` is an **array of tool objects** (`type`, `value`, `description`, `transport`), **not** a bare string list. The v0.1.0 `- bash` / `- jq` form was wrong.

Duplicate-name skills across scopes are NOT merged — both appear in selectors, repo-level wins for local workflows.

---

## 3. `.codex-plugin/plugin.json` (plugin manifest)

```json
{
  "name": "my-codex-plugin",
  "version": "1.0.0",
  "description": "Short summary",
  "skills": "./skills/",
  "mcpServers": "./mcp/servers.json",
  "apps": "./apps/",
  "hooks": "./hooks.json",
  "interface": {
    "displayName": "My Plugin",
    "longDescription": "Detailed description for installer UI"
  }
}
```

**Required field:** `name` (kebab-case) — and only when a `plugin.json` is present at all. **All other top-level fields are optional**, including `version`, `description`, `author`, and `interface` (corrected 2026-08-02 against the vendor's `plugin-json-spec.md`; the earlier "version + description required" claim was wrong).
**Optional artifact paths — each a single relative-path STRING, not an array** (corrected 2026-08-04 against the vendor `plugin-json-spec.md`): `skills` (string), `hooks` (string), `apps` (string), `mcpServers` (string **or** object). A bare directory string like `"skills": "./skills/"` is the documented sample form; these paths *supplement* Codex's default discovery, they do not replace it. Do NOT flag a scalar-string `skills`/`hooks`/`apps`/`mcpServers` as wrong — the array form the v0.3.0 overlay showed was incorrect.
**Optional identity fields (added 2026-06):** `author` (`{name, email, url}`), `homepage`, `repository`, `license`, `keywords`.
**Optional UI block** `interface`:
- `displayName`, `shortDescription`, `longDescription`, `developerName`, `category`, `capabilities`
- `defaultPrompt` — an **array** of starter prompts (not a single string). **At most 3 entries** (extras ignored); **each capped at 128 characters** (longer entries truncated).
- `websiteURL`, `privacyPolicyURL`, `termsOfServiceURL`
- `brandColor`, `composerIcon`, `logo`, `logoDark` (dark-mode logo variant), `screenshots` (PNG files stored under `./assets/`, paths relative to plugin root)

---

## 4. `.agents/plugins/marketplace.json` (marketplace manifest)

Three marketplace tiers exist in Codex:

- **Official Curated** — OpenAI-managed. Workspace plugin publishing and additional marketplaces (Amazon Bedrock, Claude Code interop) shipped in 0.146.0 (2026-07-29); the exact self-serve mechanics are still settling — verify before asserting.
- **Repository** — `<repo-root>/.agents/plugins/marketplace.json` aggregates plugins shipped from that repo.
- **Personal** — `~/.agents/plugins/marketplace.json`.

Schema:

```json
{
  "name": "xiaolai",
  "interface": {
    "displayName": "xiaolai Marketplace"
  },
  "plugins": [
    {
      "name": "nlpm",
      "source": {
        "source": "github",
        "repo": "xiaolai/nlpm"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_USE"
      },
      "category": "developer-tools",
      "interface": {
        "displayName": "nlpm"
      }
    }
  ]
}
```

Per-plugin `source` types: `"github"`, `"git"`, `"local"`.

**`policy` values are UPPERCASE enums** (corrected 2026-08-04 against nlpm's own shipping `.agents/plugins/marketplace.json` and observed real plugins): `installation` e.g. `"AVAILABLE"`; `authentication` e.g. `"ON_USE"` or `"ON_INSTALL"`. The lowercase `"auto"`/`"none"` the v0.3.0 overlay showed was wrong — do NOT flag `AVAILABLE`/`ON_USE`/`ON_INSTALL` as invalid.

---

## 5. `.codex/config.toml`

TOML — NOT JSON. Top-level sections nlpm cares about:

- `[features]` — feature flags. **Breaking change ~2026-04 (CLI 0.129+):** `[features].codex_hooks` was renamed to `[features].hooks` (boolean; enables hooks from `hooks.json` or inline `[hooks]`). Old key is a deprecated alias and emits a warning. Flag config files that still use `codex_hooks`.
- `[mcp_servers.<id>]` — MCP server registrations. Fields: `command`, `args`, `cwd`, `url`, `enabled`, `enabled_tools`, `disabled_tools`, `env`, `startup_timeout_sec`, `tool_timeout_sec` (per-tool, default 60s — added 2026-06).
- `[hooks.<event>]` — inline hook registrations (alternative to `.codex/hooks.json`).
- `[agents]` — **global** subagent settings ONLY: `enabled`, `max_concurrent_threads_per_session`, `default_subagent_model`, `default_subagent_reasoning_effort`, `interrupt_message`. Individual subagents are **not** `[agents.<name>]` tables — they are standalone TOML files at `.codex/agents/*.toml` (project) or `~/.codex/agents/*.toml` (personal), one file per agent, with required `name` + `description` + `developer_instructions` and optional `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config` (corrected 2026-08-02 — the old `[agents.<name>]` / `config_file` / `nickname_candidates` schema is gone).
- `[permissions.*]` — permission policy.
- `project_doc_max_bytes`, `project_doc_fallback_filenames` — AGENTS.md controls (see §7).
- Optional model-catalog JSON path loaded at startup, overridable per profile.

**REMOVED — `[profiles.*]` table syntax is gone as of 0.134.0 (2026-05-26).** Profiles now live in dedicated per-profile files `~/.codex/<name>.config.toml`, selected with `--profile <name>`. A config still using `[profiles.foo]` tables is stale — flag it.

**No `.mcp.json` at repo root.** Codex does NOT read Claude's `.mcp.json` — MCP servers live inside `config.toml`. A bridge from `.mcp.json` → `.codex/config.toml` is a common port pattern (see `cc-suite:bridge-mcp` skill).

---

## 6. Hook events (Codex CLI)

Codex hooks mostly mirror Claude Code's event names — easier than the Antigravity divergence.

| Event | In Claude? | In Antigravity? | Notes |
|---|---|---|---|
| `SessionStart` | yes | yes | — |
| `UserPromptSubmit` | yes | — | — |
| `PreToolUse` | yes | — (different model) | — |
| `PostToolUse` | yes | — | — |
| `PermissionRequest` | yes | — | — |
| `PreCompact` | yes | — (uses `PreCompress`) | — |
| `PostCompact` | yes | — | Claude added `PostCompact` in its 2026-06 hook set (see conventions-claude §7) |
| `SubagentStart` | yes | — | In Claude too (2026-06 hook set); Codex added it 2026-05-21 in 0.133.0 |
| `SubagentStop` | yes | — | — |
| `Stop` | yes | — | — |
| `SessionEnd` | yes | — | Real Codex event (confirmed 2026-08-02): fires on archive/delete of a still-open conversation, normal Codex close, or after ~30-min idle with no connected client; 1s default timeout (max 3s); advisory-only (output does not steer Codex) |

**Absent in Codex (but present in Claude):** `Notification`, `FileChanged`, `StopFailure`.

**Hook I/O contract:** Same JSON-on-stdin / JSON-on-stdout shape as Claude. Stdin: `session_id`, `cwd`, `hook_event_name`, `tool_name`, `tool_input`, etc. Stdout fields: `continue`, `stopReason`, `systemMessage`, `suppressOutput`, `hookSpecificOutput`. Exit codes: `0` + JSON = success with directives; `0` + plain text = added as context; `2` = block (reason to **stderr**); other = warning.

**Caveats (added 2026-06):**
- `SubagentStart` / `SubagentStop` hook inputs now carry subagent identity, including `permission_mode` (0.134.0).
- For `SubagentStart`, `continue: false` does **not** stop the subagent.
- **Async command hooks are parsed but not yet supported** — a config declaring one is accepted but the async behavior is a no-op.

---

## 7. AGENTS.md (Codex's canonical memory file)

Codex reads `AGENTS.md` before every turn. Files are **concatenated root-down**, joined by blank lines; files closer to CWD override earlier ones by position (there is no separate global/project boundary marker — it is pure positional override). Within each directory the search order is `AGENTS.override.md` → `AGENTS.md` → fallback filenames, and **at most one file per directory** is taken; the walk stops at CWD. Global layer: `~/.codex/AGENTS.override.md` → `~/.codex/AGENTS.md`.

**Default cap:** 32 KiB per file (`project_doc_max_bytes` in config.toml).
**Fallback filenames:** Configurable via `project_doc_fallback_filenames` — this is the official hook for AGENTS.md / CLAUDE.md / GEMINI.md interop (set the array to include all three to make Codex read whichever exists).

**Body conventions** (not enforced, but common):
- `## Working agreements` — high-level decisions
- `## Repository expectations` — invariants
- `@file.md` imports are NOT supported (unlike Gemini's GEMINI.md hierarchy) — use file concatenation instead.

The nlpm pattern of `CLAUDE.md` → one line `@AGENTS.md` does NOT work for Codex (no @-import). Codex authors should put content directly in AGENTS.md and configure Claude Code's CLAUDE.md to import it instead.

---

## 8. Slash commands / prompts

Codex's slash-command / prompt format lives at `~/.codex/prompts/<name>.md` (project form `.codex/prompts/`). The "deprecated in favor of skills" framing is **not confirmed in current docs** (2026-06-07) — prompts are still documented. nlpm should NOT penalize their presence, and should treat any migration recommendation as advisory/soft rather than asserting deprecation.

Placeholders if scoring legacy prompts: `$1..$9`, `$ARGUMENTS`, `$FILE`, `$TICKET_ID`, `$$`.

---

## 9. Recent breaking / material changes (last 6 months)

| Date | Version | Change |
|---|---|---|
| 2026-03-26 | — | Plugin marketplace **launched**. New artifact class. |
| ~2026-04 | 0.129.0 | `[features].codex_hooks` renamed to `[features].hooks` (deprecation warning) |
| 2026-05-18 | 0.131.0 | Plugin hooks enabled by default; legacy shell tools + built-in MCPs removed; `codex doctor` added |
| 2026-05-21 | 0.133.0 | Goals enabled by default; `SubagentStart` event observable by hooks |
| 2026-05-26 | 0.134.0 | **`[profiles.*]` table syntax dropped** → per-profile files `~/.codex/<name>.config.toml` (`--profile`); MCP OAuth for HTTP servers + per-server env; read-only MCP tools run concurrently (`readOnlyHint`); subagent identity in hook inputs |
| 2026-05-28 | 0.135.0 | `/permissions` understands named permission profiles; expanded `codex doctor` diagnostics; `CODEX_NON_INTERACTIVE=1` |
| 2026-06-01 | 0.136.0 | Session archive (`/archive`, `codex archive`/`unarchive`); `CODEX_API_KEY` remote-exec registration; 4 security fixes |
| 2026-06-04 | 0.137.0 | `codex plugin list --json`; Multi-agent v2 per-thread runtime persistence; plugin skill manifest validation improvements; cloud-managed config bundles |
| 2026-07-21 | 0.145.0 | Paginated thread history (experimental); `/import` migrates Cursor + Claude Code settings/MCP/plugins/sessions/commands/memories; experimental Amazon Bedrock auth; audio I/O; multi-agent V2 stabilized (opt-in) |
| 2026-07-29 | 0.146.0 | Session naming/pinning + thread switching; **Agent Plugins manifests + workspace plugin publishing + additional marketplaces (Amazon Bedrock, Claude Code)**; paginated thread forks; discovery of executor-provided skills (a non-filesystem skill source §1 doesn't cover) |

Latest stable as of 2026-08-02: **0.146.0** (2026-07-29); pre-releases through ~`0.147.0-alpha` (verify the exact tag before quoting). Versions **0.138.0–0.144.x** are omitted here — only non-first-party aggregators carried them this refresh; add rows once a first-party changelog source is read.

Repos relying on the removed built-in MCPs will silently regress under 0.131+. nlpm should flag MCP configs that name MCPs no longer shipped natively. Configs using `[profiles.*]` tables are stale under 0.134+.

---

## 10. Scope and uncertainty

This skill covers Codex CLI conventions. It does NOT cover:
- Universal SKILL.md spec → `nlpm:conventions`
- Penalty tables → `nlpm:scoring`
- Cross-artifact check → invoked by `agents/checker.md`

**Resolved in the 2026-08-02 refresh:**
- `plugin.json` required fields — only `name` is required; `version`/`description`/`author`/`interface` are optional (§3).
- Subagent config mechanism — standalone `.codex/agents/*.toml` files, not `[agents.<name>]` tables (§5).
- `SessionEnd` is a real Codex hook event (§6).
- `.agents/skills/` (not `.codex/skills/`) reconfirmed as the sole filesystem skill-discovery path (§2).
- Contributor / CLA policy for `openai/codex` **itself**: external contributions are **by invitation only** — unsolicited PRs are closed without review; invited contributors sign a lightweight bot-verified CLA via a PR comment. This governs the `openai/codex` repo only, NOT third-party repos that merely target Codex as a tool (the auditor's actual PR targets). If PR-D ever contributes to `openai/codex` directly it needs an invite-only DENY-style gate, not the Google URL-CLA flow.

**Resolved in the 2026-06-07 refresh:**
- `child_agents_md` feature flag — **not found** in any current doc. Treat as removed/never-shipped; do not score against it.
- AGENTS.md merge boundary — resolved (§7): pure positional override, one file per directory, walk stops at CWD.

**Still open (verify before scoring with confidence):**
- `.app.json` schema for the plugin `apps` field — documented but the **full schema is still unpublished**.
- Sidecar `agents/openai.yaml` `dependencies.tools[].url` field — seen once in `build-skills`, not cleanly re-confirmed; do not hard-flag its presence or absence yet.
- Codex versions 0.138.0–0.144.x — first-party changelog rows still pending (§9).
