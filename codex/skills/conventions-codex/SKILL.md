---
name: conventions-codex
description: Use when scoring or writing Codex CLI artifacts — covers .codex/config.toml schema, .codex-plugin/plugin.json, .agents/skills/ layout, Codex hook events, AGENTS.md hierarchy, marketplace.json, and the agents/openai.yaml sidecar. Refreshed 2026-06-07 against Codex 0.137.0 (2026-06-04).
version: 0.2.0
---

# Codex CLI Conventions

Tool-specific overlay for OpenAI Codex CLI artifacts. Loaded by the scorer and checker when an artifact is classified as **Tier 2-Codex** (per `agents/scorer.md` step 3). The universal floor lives in `nlpm:conventions`; this overlay adds Codex-specific schemas on top.

**Primary authoritative sources:**
- <https://developers.openai.com/codex>
- <https://developers.openai.com/codex/skills>
- <https://developers.openai.com/codex/guides/agents-md>
- <https://developers.openai.com/codex/config-reference>
- <https://developers.openai.com/codex/hooks>
- <https://developers.openai.com/codex/plugins>
- <https://github.com/openai/codex>

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

Codex reads SKILL.md from `.agents/skills/`, not `.codex/skills/`. The required frontmatter is the agentskills.io baseline — `name` and `description` — same as every other tool.

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
  "skills": ["./skills/foo"],
  "mcpServers": ["./mcp/bar.toml"],
  "apps": ["./apps/baz.app.json"],
  "hooks": ["./hooks.json"],
  "interface": {
    "displayName": "My Plugin",
    "longDescription": "Detailed description for installer UI"
  }
}
```

**Required fields:** `name` (kebab-case), `version` (semver), `description`.
**Optional component paths** (all relative `./` paths only): `skills`, `mcpServers`, `apps`, `hooks`.
**Optional identity fields (added 2026-06):** `author` (`{name, email, url}`), `homepage`, `repository`, `license`, `keywords`.
**Optional UI block** `interface`:
- `displayName`, `shortDescription`, `longDescription`, `developerName`, `category`, `capabilities`
- `defaultPrompt` — an **array** of starter prompts (not a single string)
- `websiteURL`, `privacyPolicyURL`, `termsOfServiceURL`
- `brandColor`, `composerIcon`, `logo`, `screenshots`

---

## 4. `.agents/plugins/marketplace.json` (marketplace manifest)

Three marketplace tiers exist in Codex:

- **Official Curated** — OpenAI-managed; self-serve publishing "coming soon" as of May 2026.
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
        "installation": "auto",
        "authentication": "none"
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

---

## 5. `.codex/config.toml`

TOML — NOT JSON. Top-level sections nlpm cares about:

- `[features]` — feature flags. **Breaking change ~2026-04 (CLI 0.129+):** `[features].codex_hooks` was renamed to `[features].hooks` (boolean; enables hooks from `hooks.json` or inline `[hooks]`). Old key is a deprecated alias and emits a warning. Flag config files that still use `codex_hooks`.
- `[mcp_servers.<id>]` — MCP server registrations. Fields: `command`, `args`, `cwd`, `url`, `enabled`, `enabled_tools`, `disabled_tools`, `env`, `startup_timeout_sec`, `tool_timeout_sec` (per-tool, default 60s — added 2026-06).
- `[hooks.<event>]` — inline hook registrations (alternative to `.codex/hooks.json`).
- `[agents.<name>]` — subagent definitions (Codex multi-agent feature). Keys: `config_file`, `description`, `nickname_candidates`.
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

**Absent in Codex (but present in Claude):** `Notification`, `SessionEnd`, `FileChanged`, `StopFailure`.

**Hook I/O contract:** Same JSON-on-stdin / JSON-on-stdout shape as Claude. Stdin: `session_id`, `cwd`, `hook_event_name`, `tool_name`, `tool_input`, etc. Stdout fields: `continue`, `stopReason`, `systemMessage`, `hookSpecificOutput`. Exit codes: `0` + JSON = success with directives; `0` + plain text = added as context; `2` = block (reason to **stderr**); other = warning.

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

Latest stable as of 2026-06-07: **0.137.0** (pre-releases through `0.138.0-alpha.6`).

Repos relying on the removed built-in MCPs will silently regress under 0.131+. nlpm should flag MCP configs that name MCPs no longer shipped natively. Configs using `[profiles.*]` tables are stale under 0.134+.

---

## 10. Scope and uncertainty

This skill covers Codex CLI conventions. It does NOT cover:
- Universal SKILL.md spec → `nlpm:conventions`
- Penalty tables → `nlpm:scoring`
- Cross-artifact check → invoked by `agents/checker.md`

**Resolved in the 2026-06-07 refresh:**
- `child_agents_md` feature flag — **not found** in any current doc (config-reference, config-advanced, agents-md). Treat as removed/never-shipped; do not score against it.
- AGENTS.md merge boundary — resolved (§7): pure positional override, one file per directory, walk stops at CWD.

**Still open (verify before scoring with confidence):**
- `.app.json` schema for the plugin `apps` field — the field is documented (points to a relative `.app.json` at plugin root for app/connector mappings) but the **full schema is still unpublished**.
- OpenAI's contributor / CLA policy for PRs into `openai/codex`-ecosystem repos — no official doc located; research needed before the auditor pipeline (PR-C/PR-D) scales Codex contributions.
