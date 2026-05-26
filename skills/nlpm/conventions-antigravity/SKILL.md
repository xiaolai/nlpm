---
name: conventions-antigravity
description: "Use when scoring or writing Antigravity (or legacy Gemini CLI) artifacts — covers .gemini/ paths, .agent/ workspace skills, gemini-extension.json, GEMINI.md, TOML slash commands, Gemini-lineage hook events. Spec is unsettled (Antigravity 2.0 launched 2026-05-19); many checks are advisory until PR-B verification."
version: 0.1.0
---

# Antigravity Conventions (with Gemini CLI legacy)

Tool-specific overlay for Google Antigravity CLI artifacts, including legacy Gemini CLI paths during the transition window. Loaded by the scorer and checker when an artifact is classified as **Tier 2-Antigravity** (per `agents/scorer.md` step 3). The universal floor lives in `nlpm:conventions`.

**Status:** Antigravity 2.0 was announced at Google I/O 2026 on **2026-05-19** (six days before this file was written). The directory layout is still settling, the official Antigravity-specific spec doc is sparse, and two authoritative research passes disagreed on `.agent/` (singular) vs `.agents/` (plural) as the canonical skills path. This skill is **advisory-only** for Antigravity-specific artifacts. PR-B verification trigger conditions are recorded in `analysis/multi-tool-design-2026-05.md`.

**Transition timeline:**
- **Now → 2026-06-18:** Gemini CLI continues serving AI Pro / Ultra / Free tiers in parallel with Antigravity CLI.
- **2026-06-18:** Gemini CLI sunsets for non-enterprise. Enterprise paid licenses retained.
- **After sunset:** Antigravity CLI is the sole successor; `.gemini/` paths fade to legacy.

**Primary authoritative sources:**
- <https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/>
- <https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/>
- <https://antigravity.google/>
- <https://codelabs.developers.google.com/getting-started-with-antigravity-skills>
- <https://geminicli.com/docs/cli/skills/> (Gemini lineage; transitional)
- <https://geminicli.com/docs/hooks/reference/> (Gemini lineage; transitional)
- <https://github.com/google/skills>

---

## 1. File system layout

| Artifact | Project scope (Antigravity) | Project scope (Gemini, legacy) | User scope |
|---|---|---|---|
| Skills | `<workspace>/.agent/skills/<name>/SKILL.md` (singular — Antigravity per codelab); `.agents/skills/<name>/SKILL.md` (cross-tool alias, plural) | `.gemini/skills/<name>/SKILL.md` | `~/.gemini/antigravity/skills/` (transitional global) or `~/.gemini/skills/` (legacy) |
| Slash commands | (under-documented for Antigravity) | `.gemini/commands/<name>.toml` | `~/.gemini/commands/` |
| Hooks | (under-documented for Antigravity) | `.gemini/settings.json` → `hooks` object | `~/.gemini/settings.json` |
| MCP servers | (under-documented for Antigravity) | `mcpServers` JSON key inside `.gemini/settings.json` | same |
| Extensions / plugins | "Antigravity plugins" — `gemini-extension.json` (renamed in transition, layout TBD) | `~/.gemini/extensions/<name>/gemini-extension.json` | same |
| Memory file | `GEMINI.md` (inherited; configurable via `context.fileName` array) | `GEMINI.md` (workspace + ancestors) | `~/.gemini/GEMINI.md` |
| System config | TBD | `/etc/gemini-cli/settings.json` | — |

**Discovery precedence within a tier** (Gemini-lineage; assumed to carry over): built-in → extension → user → workspace. `.agents/skills/` beats `.gemini/skills/` (cross-tool path wins).

**Uncertainty (verify before scoring):**
- `<workspace>/.agent/skills/` (singular, from Antigravity codelab) vs `.agents/skills/` (plural, cross-tool alias from agentskills.io) — both may be true (Antigravity-specific singular path + cross-tool plural alias), or one may be a documentation error. Recommend recognizing both as valid skill paths.

---

## 2. SKILL.md (Tier 1, open spec — `name`, `description` required only)

Antigravity (and Gemini CLI) explicitly adopt the agentskills.io open standard. Required: `name`, `description`. Same as every other tool.

**Antigravity/Gemini-specific extensions** documented to date:
- `activate_skill` tool invocation (in-agent) to load a skill on demand.
- Mandatory user-consent prompt before injection (filesystem-access grant).
- `/skills` slash command (in-agent) lists installed skills.
- `gemini skills` terminal command (list/install/uninstall) — Gemini-only; Antigravity CLI uses `npx skills add` instead.

**Install verbs:**
- Cross-tool: `npx skills add github.com/google/skills` (per `github.com/google/skills` repo page).
- Legacy Cloud Next blog wording: `npx skills install` (treat as equivalent; `add` is the canonical command).
- Gemini CLI: `gemini extensions install <github-url|path>`.

---

## 3. `gemini-extension.json` (extension manifest, becoming "Antigravity plugin")

```json
{
  "name": "my-extension",
  "version": "1.0.0",
  "mcpServers": { /* MCP server registrations */ },
  "contextFileName": "AGENTS.md",
  "excludeTools": ["WebFetch"]
}
```

Required: `name`, `version`. Notable optional: `mcpServers`, `contextFileName`, `excludeTools`. The rename to "Antigravity plugin" is announced; the manifest schema is documented to "preserve" extension semantics but Google hasn't published the full delta.

---

## 4. `.gemini/commands/<name>.toml` (slash commands — TOML)

```toml
prompt = """
Review the diff and check for {{args}}.
"""
description = "Custom code review with focus area"
```

**Required field:** `prompt`.
**Optional:** `description` (auto-generated from filename if omitted).

**Template syntax** (Gemini-specific):
- `{{args}}` — raw argument injection.
- `!{shell command}` — runs shell, args auto-escaped.
- `@{path}` — file/directory injection. Respects `.gitignore` and `.geminiignore`. Supports PNG/JPEG/PDF/audio/video.

Subdirectory layout becomes a namespace: `.gemini/commands/ns/cmd.toml` → `/ns:cmd`.

**Antigravity CLI status:** unclear whether TOML slash commands carry over. Treat as legacy-only for now; Antigravity-specific command format TBD.

---

## 5. Hook events (Gemini lineage — fundamentally different from Claude/Codex)

Gemini (and inherited Antigravity) decomposes the lifecycle into Agent/Model/Tool layers, not the tool-centric model Claude and Codex use.

| Event | Trigger |
|---|---|
| `SessionStart` | Session begin |
| `BeforeAgent` | Before each agent turn |
| `BeforeModel` | Before LLM invocation |
| `BeforeToolSelection` | Before the model decides which tool to call |
| `BeforeTool` | Before tool execution (after selection) |
| `AfterTool` | After tool execution |
| `AfterModel` | After LLM response |
| `AfterAgent` | After agent turn complete |
| `SessionEnd` | Session end |
| `Notification` | On notification |
| `PreCompress` | Before context compaction (Gemini's name for Claude's `PreCompact`) |

**No 1:1 mapping to Claude Code or Codex events.** Specifically:
- Gemini's `BeforeModel` vs `BeforeToolSelection` distinction has no Claude/Codex analog — both fall under Claude's `PreToolUse`.
- Gemini has no equivalent of Claude's `UserPromptSubmit` or `PermissionRequest`.

**I/O contract** (Gemini lineage): JSON on stdin with `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `timestamp`. JSON on stdout: `systemMessage`, `decision` (`"allow"`/`"deny"`), `reason`, `continue`, `suppressOutput`. Exit codes: `0` = ok, `2` = block (stderr = reason), other = warning.

**Antigravity CLI hook event names:** TBD — Google's transition post says "preserves hooks" without enumerating the event set. Treat the Gemini list as the current best guess.

---

## 6. GEMINI.md (memory file — sophisticated hierarchy)

`GEMINI.md` is hierarchical: `~/.gemini/GEMINI.md` → workspace + ancestor `GEMINI.md` files → JIT-discovered `GEMINI.md` on file access. All concatenated per prompt.

**Distinctive features (versus AGENTS.md and CLAUDE.md):**
- Supports `@file.md` imports via the Memory Import Processor. Verified 2026-05-26 against `geminicli.com/docs/reference/memport/`: imports nest (configurable max depth, default 5), accept any filename (not just `GEMINI.md`), and take relative or absolute paths. A `GEMINI.md` containing only `@AGENTS.md` resolves to AGENTS.md's full contents. `validateImportPath` restricts imports to allowed directories (repo-root siblings are fine).
- Filename is configurable via `context.fileName` in `settings.json`, which accepts an **array** — e.g., `context.fileName: ["AGENTS.md", "CONTEXT.md", "GEMINI.md"]`. This is the official interop hook for AGENTS.md (Codex's canonical) and CLAUDE.md (Claude Code's canonical).

**Recommended pattern for multi-tool projects (use `context.fileName`, NOT the @-import shim):**
- Set `context.fileName: ["AGENTS.md"]` in `.gemini/settings.json` — makes Gemini/Antigravity read AGENTS.md directly. nlpm decision #5: AGENTS.md is the canonical universal memory file. nlpm itself ships this exact `.gemini/settings.json`.
- **Why not rely on a `GEMINI.md` → `@AGENTS.md` shim?** It works per the import-processor docs, but every documented example uses an explicit `@./` / `@../` prefix; the bare `@AGENTS.md` form (which Claude Code accepts natively in CLAUDE.md) is a valid relative path but unconfirmed against a live Gemini run. `context.fileName` has no such ambiguity — Gemini reads the named file directly with no import resolution involved.

---

## 7. MCP integration

Gemini reads MCP servers from `mcpServers` key inside `~/.gemini/settings.json` or `.gemini/settings.json` (NOT a separate `.mcp.json` file). Standard MCP server shape: `command`, `args`, `env`. Also configurable inside `gemini-extension.json` for extension-bundled servers.

Slash commands: `/mcp list`, `/mcp auth`.

**Antigravity CLI MCP layout:** TBD.

---

## 8. Plugin marketplace

**No central JSON marketplace manifest** documented for Gemini CLI today. Discovery is via the Extensions Gallery at <https://geminicli.com/extensions/> (community/partner/Google), GitHub-stars ranked, installed via `gemini extensions install <github-url|path>`.

**Antigravity CLI marketplace** layout: TBD.

**`github.com/google/skills`** is the official Google-published skills registry. Organized under `skills/cloud/...`. Installed via `npx skills add google/skills`. Cross-tool — targets Antigravity, Gemini CLI, Codex CLI, Claude Code, Cursor, and others.

---

## 9. Recent material changes (last 6 months)

| Date | Event |
|---|---|
| 2025-11-20 | Original Antigravity public preview |
| 2026-04 (Cloud Next) | `github.com/google/skills` official registry launched; `npx skills` cross-agent installer |
| 2026-05 | Extensions Gallery launched (Dynatrace, Elastic, Figma, Harness as partners) |
| **2026-05-19 (Google I/O)** | **Antigravity 2.0 announced; Antigravity CLI GA; Gemini CLI deprecation announced** |
| 2026-06-18 (pending) | Gemini CLI stops serving AI Pro/Ultra/Free tiers |

---

## 10. Scope and uncertainty

This skill covers Antigravity CLI and legacy Gemini CLI conventions during the transition window. It does NOT cover:
- Universal SKILL.md spec → `nlpm:conventions`
- Penalty tables → `nlpm:scoring`
- Antigravity desktop IDE or Antigravity SDK (different artifact surfaces)

**Major uncertainties — defer deep audit until resolved:**

1. **Singular `.agent/` vs plural `.agents/`** — codelab uses singular for Antigravity workspace skills; agentskills.io cross-tool alias uses plural. Auditor should recognize both as valid.
2. **`npx skills` verb** — `add` per repo page, `install` per Cloud Next blog. `add` is canonical.
3. **Antigravity directory-rename spec** — Google's transition post says "not 1:1 parity" without enumerating gaps. Monitor for an official migration guide.
4. **Antigravity-specific hook events** — assumed to inherit Gemini's, but the transition post doesn't confirm.
5. **`github.com/google-antigravity/antigravity-cli`** — research surfaced this org/repo URL but the namespace differs from `google/` proper. Verify before citing as authoritative.
6. **"Antigravity plugins" manifest schema** — renamed from Gemini "extensions" but full schema delta not published.
7. **MCP support in Antigravity** — not contradicted in the transition post, but not explicitly confirmed.

PR-B verification trigger: when Google publishes a stable Antigravity directory-layout spec (or when Antigravity overtakes Gemini CLI in real-world repo count), upgrade this skill from advisory to authoritative and add Antigravity-specific penalty rows to `nlpm:scoring`.
