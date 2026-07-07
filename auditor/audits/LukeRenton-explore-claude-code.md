# NLPM Audit: LukeRenton/explore-claude-code
**Date**: 2026-04-06  |  **Artifacts**: 27  |  **Strategy**: batched
**NL Score**: 89/100
**Security**: REVIEW
**Bugs**: 4  |  **Quality Issues**: 37  |  **Security Findings**: 1

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/agents/engineers/orchestrator-engineer.md | agent | 65 | Vague quantifiers capped at -20 (11 hits, mostly from copy-pasted generic memory-system boilerplate) |
| .claude/agents/engineers/engineering-frontend-developer.md | agent | 75 | Zero `<example>` blocks in description |
| .claude/agents/engineers/engineering-code-reviewer.md | agent | 75 | Zero `<example>` blocks in description |
| .claude/agents/engineers/engineering-backend-developer.md | agent | 75 | Zero `<example>` blocks in description |
| .claude/agents/engineers/engineering-software-architect.md | agent | 75 | Zero `<example>` blocks in description |
| site/content/.claude/plugins/my-plugin/.claude-plugin/plugin.json | plugin.json | 75 | File is not valid JSON (uses `//` comments) |
| .claude/skills/build-skill/SKILL.md | skill | 82 | No worked examples; 4 vague quantifiers |
| .claude/agents/core-planner.md | agent | 83 | Zero `<example>` blocks in description |
| .claude/agents/content-writing/content-writer.md | agent | 83 | Zero `<example>` blocks in description |
| site/content/.claude/commands/review-pr.md | command | 83 | No empty-input / error-path handling |
| .claude/skills/build-agent/SKILL.md | skill | 84 | No worked examples; 3 vague quantifiers |
| site/content/.claude/commands/my-command/my-command.md | command | 85 | No empty-input / error-path handling |
| site/content/.claude/commands/write-tests.md | command | 85 | No empty-input / error-path handling |
| .claude/skills/core-brainstorm/SKILL.md | skill | 88 | No worked examples |
| .claude/skills/frontend-design/SKILL.md | skill | 90 | No worked examples |
| CLAUDE.md | memory | 95 | No prerequisites/setup section |
| site/content/.claude/skills/my-skill/SKILL.md | skill (scaffold) | 98 | 1 vague quantifier |
| site/content/built-in/commands/BUILT-IN-COMMANDS.md | doc | 98 | 1 vague quantifier |
| site/content/.claude/agents/my-agent/my-agent.md | agent (scaffold) | 100 | none |
| site/content/.claude/agents/AGENTS.md | doc | 100 | none |
| site/content/built-in/commands/init/init.md | doc | 100 | none |
| site/content/built-in/commands/diff/diff.md | doc | 100 | none |
| site/content/built-in/commands/btw/btw.md | doc | 100 | none |
| site/content/built-in/commands/rewind/rewind.md | doc | 100 | none |
| site/content/built-in/commands/compact/compact.md | doc | 100 | none |
| site/content/.claude/commands/COMMANDS.md | doc | 100 | none |
| site/content/CLAUDE.md | doc | 100 | none (see Cross-Component: this file also functions as a real, auto-loaded CLAUDE.md) |

**Scoring notes:**
- `site/content/**` files are a self-referential "teaching website" corpus: most are documentation *about* Claude Code artifact types, not functioning artifacts themselves (e.g. `init.md`, `diff.md`, `btw.md`, `rewind.md`, `compact.md`, `AGENTS.md`, `COMMANDS.md`, `BUILT-IN-COMMANDS.md` describe built-in features and have no frontmatter by design). These were scored as documentation, not against the Agent/Command/Skill rubrics.
- Three files (`my-agent.md`, `my-command.md`'s explanatory half, `my-skill/SKILL.md`) are explicit "starter/scaffolding" templates whose bodies literally say "this is a starter file." Their placeholder/generic description text was not penalized under R04-style genericness rules, since genericness is the intended teaching device, not a defect.
- `.claude/agents/**` and `.claude/skills/**` (repo root) are this project's own *real* operating agents/skills (its actual `.claude/` config) and were scored at full rigor.

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 0 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks | None found (0 files registered at repo root) |
| Scripts | site/content/.claude/hooks/my-hook/my-hook.sh; site/content/.claude/skills/my-skill/scripts/helper.sh; site/js/app.js; site/js/content-loader.js; site/js/file-explorer.js; site/js/icons.js; site/js/progress.js; site/js/terminal.js |
| MCP configs | site/content/.mcp.json |
| Package manifests | None found (no package.json / requirements.txt in the repo) |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | Medium | .claude/settings.json | 3 | `permissions.defaultMode: bypassPermissions` | This is the repo's real, committed (non-`.local`) project settings file, not a documentation sample. Setting `defaultMode` to `bypassPermissions` disables all tool-use confirmation prompts for every Claude Code session run against this project, removing the human safety net for Bash/Write/Edit/etc. |

The two shipped shell scripts (`my-hook/my-hook.sh`, `my-skill/scripts/helper.sh`) and the six `site/js/*.js` files were reviewed line by line: no `eval`, no `curl|sh`, no `subprocess`/`os.system`, no `shell=True`, no credential exfiltration, no postinstall hooks. `my-hook.sh` is itself a defensive example (blocks `rm -rf` and `git push --force`). `site/content/.mcp.json` uses safe `${env:VAR}` expansion syntax with no hardcoded secrets. `site/js` network calls are same-origin `fetch()` of the site's own bundled `manifest.json`/content files, not external endpoints.

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .claude/agents/engineers/orchestrator-engineer.md | Hardcoded personal Windows path (`C:\Users\luker\Documents\Teaching Claude Code\.claude\agent-memory\orchestrator-engineer\`) is given as the agent's persistent-memory directory, inside a file whose own memory-system text says it is "shared with your team via version control" | Memory reads/writes target a path that only exists on the original author's machine; every other contributor (and any non-Windows machine) silently gets a broken or no-op memory system |
| 2 | site/content/.claude/plugins/my-plugin/.claude-plugin/plugin.json | File uses `//` line comments, which are not part of the JSON grammar; any standard JSON parser (`JSON.parse`, Python `json.load`) fails on line 2 | Anyone copying this "scaffolding" example verbatim as a real `.claude-plugin/plugin.json` gets a parse error and the plugin fails to register |
| 3 | site/content/.claude/plugins/my-marketplace/.claude-plugin/marketplace.json | Same `//` comment issue; not valid JSON | Same failure mode as #2 — a marketplace catalogue copied as-is fails to load |
| 4 | site/content/.mcp.json | Same `//` comment issue; not valid JSON | Same failure mode as #2 — a project `.mcp.json` copied as-is fails to parse, so no MCP servers load |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | .claude/settings.json | `permissions.defaultMode: bypassPermissions` in the shared, committed settings file disables permission prompts for every contributor | Move `bypassPermissions` to a personal `.claude/settings.local.json` (gitignored), or replace the blanket bypass with the same scoped `allow`/`deny` pattern already used in `site/content/.claude/settings.json`'s teaching example |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/agents/core-planner.md | Zero `<example>` blocks (R09) | -15 |
| 2 | .claude/agents/core-planner.md | Vague quantifier "Relevant" ×1 (R01) | -2 |
| 3 | .claude/agents/content-writing/content-writer.md | Zero `<example>` blocks (R09) | -15 |
| 4 | .claude/agents/content-writing/content-writer.md | Vague quantifier "properly" ×1 (R01) | -2 |
| 5 | .claude/agents/engineers/engineering-frontend-developer.md | Zero `<example>` blocks (R09) | -15 |
| 6 | .claude/agents/engineers/engineering-frontend-developer.md | `model` not declared (R10) | -5 |
| 7 | .claude/agents/engineers/engineering-frontend-developer.md | `tools` not declared (R11) | -5 |
| 8 | .claude/agents/engineers/engineering-code-reviewer.md | Zero `<example>` blocks (R09) | -15 |
| 9 | .claude/agents/engineers/engineering-code-reviewer.md | `model` not declared (R10) | -5 |
| 10 | .claude/agents/engineers/engineering-code-reviewer.md | `tools` not declared (R11) | -5 |
| 11 | .claude/agents/engineers/engineering-backend-developer.md | Zero `<example>` blocks (R09) | -15 |
| 12 | .claude/agents/engineers/engineering-backend-developer.md | `model` not declared (R10) | -5 |
| 13 | .claude/agents/engineers/engineering-backend-developer.md | `tools` not declared (R11) | -5 |
| 14 | .claude/agents/engineers/engineering-software-architect.md | Zero `<example>` blocks (R09) | -15 |
| 15 | .claude/agents/engineers/engineering-software-architect.md | `model` not declared (R10) | -5 |
| 16 | .claude/agents/engineers/engineering-software-architect.md | `tools` not declared (R11) | -5 |
| 17 | .claude/agents/engineers/orchestrator-engineer.md | `tools` not declared (R11) | -5 |
| 18 | .claude/agents/engineers/orchestrator-engineer.md | No output-format spec in body (R12) | -10 |
| 19 | .claude/agents/engineers/orchestrator-engineer.md | Vague quantifiers ×11, capped (R01) | -20 |
| 20 | site/content/built-in/commands/BUILT-IN-COMMANDS.md | Vague quantifier "Some" ×1 (R01) | -2 |
| 21 | site/content/.claude/commands/my-command/my-command.md | No empty/missing-input handling (R15) | -10 |
| 22 | site/content/.claude/commands/my-command/my-command.md | No error-path handling (R17) | -5 |
| 23 | site/content/.claude/commands/review-pr.md | No empty/missing-input handling (R15) | -10 |
| 24 | site/content/.claude/commands/review-pr.md | No error-path handling (R17) | -5 |
| 25 | site/content/.claude/commands/review-pr.md | Vague quantifier "appropriate" ×1 (R01) | -2 |
| 26 | site/content/.claude/commands/write-tests.md | No empty/missing-input handling (R15) | -10 |
| 27 | site/content/.claude/commands/write-tests.md | No error-path handling (R17) | -5 |
| 28 | .claude/skills/frontend-design/SKILL.md | No worked examples in a technical skill (R06) | -10 |
| 29 | .claude/skills/build-skill/SKILL.md | No worked examples (R06) | -10 |
| 30 | .claude/skills/build-skill/SKILL.md | Vague quantifiers ×4 (R01) | -8 |
| 31 | .claude/skills/build-agent/SKILL.md | No worked examples (R06) | -10 |
| 32 | .claude/skills/build-agent/SKILL.md | Vague quantifiers ×3 (R01) | -6 |
| 33 | .claude/skills/core-brainstorm/SKILL.md | No worked examples (R06) | -10 |
| 34 | .claude/skills/core-brainstorm/SKILL.md | Vague quantifier ×1 (R01) | -2 |
| 35 | site/content/.claude/skills/my-skill/SKILL.md | Vague quantifier "relevant" ×1 (R01) | -2 |
| 36 | CLAUDE.md | No prerequisites/setup section | -5 |
| 37 | CLAUDE.md | (informational) No test-command section, but waived — the project has no test suite/framework to document (static HTML/CSS/JS, no package.json) | 0 |

## Cross-Component

- **`site/content/CLAUDE.md` doubles as a real, auto-loaded `CLAUDE.md`.** Claude Code discovers and loads `CLAUDE.md` files from subdirectories on demand (this exact behavior is what the file itself documents). Because this teaching article is literally named and placed as `site/content/CLAUDE.md`, any Claude Code session working inside `site/content/` will have this generic "what is CLAUDE.md" documentation auto-injected as if it were real project guidance for that subtree, rather than actual conventions for the `site/content/` directory. Likely an accepted trade-off of the site's self-referential design (every article is named after the real artifact it documents), but worth a maintainer note.
- **Naming drift in `.claude/agents/engineers/`.** Four sibling files use the `engineering-*` prefix (`engineering-frontend-developer.md`, `engineering-backend-developer.md`, `engineering-code-reviewer.md`, `engineering-software-architect.md`) while the fifth, `orchestrator-engineer.md`, uses a `*-engineer` suffix instead. Cosmetic, but breaks the directory's otherwise-consistent naming convention.
- No broken cross-references found: `orchestrator-engineer.md`'s specialist-agent table (`Frontend Developer`, `Backend Architect`, `Software Architect`, `Code Reviewer`, `content-writer`) matches the `name:` frontmatter of all five referenced agent files exactly.
- All file paths referenced in the root `CLAUDE.md` (`app.js`, `file-explorer.js`, `content-loader.js`, `terminal.js`, `progress.js`, `variables.css`, `layout.css`, `components.css`, `syntax.css`, `terminal.css`, `void.css`) exist on disk under `site/js/` and `site/css/`. No stale references.

## Recommendation

**REVIEW** — submit NL fix PRs for the 4 bugs (especially the hardcoded personal path in `orchestrator-engineer.md`, which is a real cross-contributor breakage, and the three invalid-JSON scaffolding files), and flag the Medium security finding (`bypassPermissions` in the committed `.claude/settings.json`) in the accompanying issue rather than a silent PR, since it is a deliberate-looking configuration choice the maintainer may want to keep for their own workflow.
