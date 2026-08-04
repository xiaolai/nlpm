---
description: "Discover NL programming artifact files in a directory by category (A: plugin, B: project config, F: memory). Used by /nlpm:ls, /nlpm:score, /nlpm:check, and /nlpm:trend."
user-invocable: false
---

# Discover NL Programming Artifacts

**Purpose:** Discover NL programming artifacts by path pattern.

**Input:** directory path, category filter (A, B, or both)
**Output:** classified file list with line counts

## Category A — Plugin Artifacts

Patterns to search (relative to target directory):

| Pattern | Notes |
|---------|-------|
| `.claude-plugin/plugin.json` | Plugin manifest |
| `.claude-plugin/marketplace.json` | Marketplace entry |
| `commands/**/*.md` | Exclude `commands/shared/` — those are shared partials |
| `commands/shared/**/*.md` | Shared partials |
| `agents/**/*.md` | Agent definitions |
| `skills/**/SKILL.md` | Skill definitions |
| `hooks/**/*.json` | Hook configs |
| `.mcp.json` | MCP config |
| `.lsp.json` | LSP config |
| `settings.json` | Root-level settings |

## Category B — Project Config

| Pattern | Notes |
|---------|-------|
| `CLAUDE.md` | Root project instructions |
| `.claude/CLAUDE.md` | Claude config directory instructions |
| `**/CLAUDE.md` | Subdirectory CLAUDE.md files (monorepo packages) |
| `.claude/rules/**/*.md` | Rule files |
| `.claude/settings.json` | Claude settings — also check for inline `hooks` key |
| `.claude/settings.local.json` | Local Claude settings — also check for inline `hooks` key |
| `.claude/**/*.local.md` | Local plugin config files |
| `.claude/commands/**/*.md` | User-level custom commands |

## Category F — Memory Files

| Pattern | Notes |
|---------|-------|
| `~/.claude/projects/*/memory/*.md` | Project memory files |
| `~/.claude/projects/*/memory/MEMORY.md` | Memory index |

## Skip Directories

Always skip these directories during traversal:

- `node_modules/`
- `.git/`
- `target/`
- `dist/`
- `build/`
- `vendor/`
- `__pycache__/`
- `.next/`
- `.venv/`

## Instructions

1. Receive: `directory` (absolute path), `category` ("A", "B", "F", or "both")
2. Use Glob to discover files matching each pattern within the directory
3. Filter out any results that fall inside skip directories
4. For each found file, use Read to count lines
5. Return a structured list with entries: `{ path, category, pattern_matched, line_count }`
6. For Category B settings files (`.claude/settings.json`, `.claude/settings.local.json`): after discovering the file, flag whether it contains a top-level `hooks` key — if so, note `inline_hooks: true` on the entry so the scanner knows to treat it as a hook source as well

## Notes

- For `commands/**/*.md` results, exclude any file whose path contains `/commands/shared/` (those match the shared partials pattern instead)
- `.gitkeep` files are not artifacts — ignore them
- If a file matches multiple patterns, use the first matching pattern in the order listed above (Category A first, then B, then F)
- `**/CLAUDE.md` in Category B will also match the root `CLAUDE.md` — deduplicate: if a file was already matched by the root `CLAUDE.md` pattern, do not add it again
- Category F patterns expand `~` to the user's home directory before globbing
