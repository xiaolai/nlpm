---
description: "Shared partial: classify a file path to its NL artifact type — command, agent, skill, rule, hook-config, manifest, etc. Used by /nlpm:score, /nlpm:fix, /nlpm:test, and /nlpm:check."
user-invocable: false
disable-model-invocation: true
---

# Classify NL Artifact Type

**Purpose:** Classify a file's artifact type from its path.

**Input:** file path (absolute or relative)
**Output:** artifact type string

## Classification Rules

Checked in order — **first match wins**:

| # | Condition | Type |
|---|-----------|------|
| 1 | Path matches `commands/shared/**/*.md` | `shared-partial` |
| 2 | Path matches `.claude/commands/**/*.md` | `user-command` |
| 3 | Path matches `commands/**/*.md` | `command` |
| 4 | Path matches `agents/**/*.md` | `agent` |
| 5 | Filename is `SKILL.md` | `skill` |
| 6 | Path matches `.claude/rules/**/*.md` | `rule` |
| 7 | Path matches `hooks/**/*.json` | `hook-config` |
| 8 | Filename is `plugin.json` AND parent directory is `.claude-plugin` | `manifest` |
| 9 | Filename is `marketplace.json` AND parent directory is `.claude-plugin` | `marketplace` |
| 10 | Filename is `.mcp.json` | `mcp-config` |
| 11 | Filename is `.lsp.json` | `lsp-config` |
| 12 | Path contains `/memory/` AND filename ends in `.md` | `memory` |
| 13 | Filename is `CLAUDE.md` AND path is NOT at the repo root | `claude-md` |
| 14 | Filename is `CLAUDE.md` | `claude-md` |
| 15 | Path matches `.claude/**/*.local.md` | `plugin-config` |
| 16 | Path matches `.claude/settings*.json` | `settings` |
| 17 | (fallback) | `document` |

## Notes

- Classification is path-based only — no content analysis required
- Path matching uses simple substring/suffix checks, not regex
- For rules 8 and 9, check that the immediate parent directory name is `.claude-plugin`
- Rule 15 applies to files like `.claude/nlpm.local.md`
- Rule 16 applies to `.claude/settings.json` and `.claude/settings.local.json`; settings files are now fully scored (not just discovered) — see `nlpm:scoring` for the settings penalty table
- Rule 12 matches memory files from `~/.claude/projects/*/memory/` — the `/memory/` path segment is the key discriminator
- Rules 13 and 14 both produce `claude-md`; rule 13 exists to document that subdirectory CLAUDE.md files (monorepo packages) receive the same type as the root one
