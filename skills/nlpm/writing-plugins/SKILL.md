---
name: writing-plugins
description: "How to design and build plugins -- architecture decisions, artifact selection, file structure, manifest configuration, marketplace publishing. Primarily Claude Code (.claude-plugin/plugin.json); the same architecture maps to Codex CLI (.codex-plugin/plugin.json) and Antigravity extensions. Use when planning, creating, or reviewing a plugin."
version: 0.2.0
---

# Writing Plugins

> Scope: covers plugin design and architecture. The examples use the **Claude Code** layout (`.claude-plugin/plugin.json` + auto-discovered `commands/`, `agents/`, `skills/`, `hooks/`). The same artifact-selection and architecture reasoning maps to the other tools — only the manifest path and packaging differ:
> - **Codex CLI**: `.codex-plugin/plugin.json` manifest + `.agents/plugins/marketplace.json`; skills live at `.agents/skills/`. See [[nlpm:conventions-codex]].
> - **Antigravity**: `gemini-extension.json` (becoming "Antigravity plugins"); skills at `.agent/skills/`. See [[nlpm:conventions-antigravity]].
> - **Cross-tool skills**: a `SKILL.md` collection with no plugin wrapper installs into any tool via `npx skills add`. See [[writing-skills]].
>
> For individual artifact authoring, see [[writing-skills]], [[writing-agents]], [[writing-hooks]], [[writing-rules]].

## 1. Plugin = Commands + Agents + Skills + Hooks

A plugin is a collection of NL artifacts that work together. Before writing anything, decide which artifacts you need.

### Component Selection Guide

| User need | Component | Example |
|-----------|-----------|---------|
| User runs a slash command | Command | `/nlpm:score path/to/file.md` |
| AI works autonomously on a task | Agent | Security scanner dispatched by a command |
| Domain knowledge for agents/Claude | Skill | SKILL.md with patterns and decision tables |
| Something must happen automatically on events | Hook | Lint-on-save, block force push |
| External service integration | MCP server (`.mcp.json`) | GitHub API, Slack notifications |

### Minimum Viable Plugin

The smallest useful plugin has **one artifact**:

```
my-plugin/
  .claude-plugin/
    plugin.json
  commands/
    do-thing.md
```

Don't add agents, skills, or hooks until you need them. Each artifact adds maintenance burden.

## 2. Architecture Patterns

### Pattern: Single Command (simplest)

Command does everything itself. No agents, no orchestration.

```
Command receives input --> processes --> outputs result
```

**Use when**: task is simple, deterministic, single-step.
**Example**: `loc-guardian /scan` -- counts lines, checks limits, reports.

**File structure**:
```
my-plugin/
  .claude-plugin/plugin.json
  commands/do-thing.md
```

### Pattern: Command + Agent

Command parses input and dispatches one agent for heavy work.

```
Command parses input --> dispatches agent --> formats output
```

**Use when**: task requires AI judgment but has a clear entry point.
**Example**: `/nlpm:score` dispatches a scorer agent.

**File structure**:
```
my-plugin/
  .claude-plugin/plugin.json
  commands/analyze.md
  agents/analyzer.md
```

### Pattern: Command + Multiple Agents (parallel)

Command dispatches 2–6 agents in parallel, synthesizes results.

```
Command --> agent-1 (security)
        --> agent-2 (performance)    --> synthesize --> output
        --> agent-3 (architecture)
```

**Use when**: multiple independent analyses of the same input.
**Example**: grill dispatches 6 review agents in parallel.

**File structure**:
```
my-plugin/
  .claude-plugin/plugin.json
  commands/review.md
  agents/
    security-agent.md
    performance-agent.md
    architecture-agent.md
```

### Pattern: Command + Agent Pipeline (sequential)

Each agent feeds into the next. Stages have different model requirements.

```
Command --> parse (haiku) --> analyze (sonnet) --> QC (sonnet) --> output
```

**Use when**: multi-phase processing where each phase depends on the previous.
**Example**: reading-assistant's 4-phase pipeline.

**File structure**:
```
my-plugin/
  .claude-plugin/plugin.json
  commands/process.md
  agents/
    parser.md       # haiku
    analyzer.md     # sonnet
    qc-agent.md     # sonnet
```

### Pattern: Hooks Only (no commands)

Plugin enforces policy silently via hooks. No user-facing commands.

```
Event fires --> hook checks --> allow/deny/advise
```

**Use when**: enforcement should be automatic, not user-initiated.
**Example**: tdd-guardian's pre-commit quality gate.

**File structure**:
```
my-plugin/
  .claude-plugin/plugin.json
  hooks/hooks.json
  scripts/check.sh
```

### Pattern Selection Matrix

| Question | Yes --> | No --> |
|----------|---------|--------|
| Does the user explicitly trigger it? | Needs a command | Hooks only |
| Does it require AI judgment? | Needs agents | Command-only or hooks |
| Are there independent sub-analyses? | Parallel agents | Sequential or single agent |
| Does each step depend on the previous? | Sequential pipeline | Parallel or single |
| Should it run automatically on events? | Add hooks | Commands only |
| Does Claude need domain knowledge? | Add skills | No skills needed |

## 3. The plugin.json Manifest

### Required Fields

Only `name` is strictly required:

```json
{
  "name": "my-plugin"
}
```

### Recommended Fields

Ship with these for discoverability and marketplace listing:

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "What this plugin does in one sentence",
  "author": { "name": "your-name" },
  "license": "MIT",
  "keywords": ["relevant", "search", "terms"],
  "category": "developer-tools"
}
```

### Field Reference

| Field | Purpose | Example |
|-------|---------|---------|
| `name` | Unique identifier, used in slash commands | `"nlpm"` |
| `version` | Semver, used by marketplace and update checks | `"0.1.0"` |
| `description` | One-line summary for marketplace listing | `"NL programming quality tools"` |
| `author.name` | Creator attribution | `"xiaolai"` |
| `license` | Open source license | `"MIT"` |
| `keywords` | Search terms for marketplace discovery | `["linter", "quality"]` |
| `category` | Marketplace category | `"developer-tools"` |

## 4. File Structure

### Full Plugin Layout

```
my-plugin/
  .claude-plugin/
    plugin.json              # manifest (required)
    marketplace.json         # for marketplace publishing
  commands/                  # auto-discovered by Claude Code
    do-thing.md              # user-invocable: /plugin:do-thing
    advanced-thing.md
    shared/                  # non-invocable partials
      common-logic.md        # user-invocable: false
      format-output.md
  agents/                    # auto-discovered
    worker.md
    reviewer.md
  skills/                    # auto-discovered
    my-plugin/
      domain-knowledge/
        SKILL.md
      advanced-topic/
        SKILL.md
        references/
          deep-dive.md
  hooks/
    hooks.json               # hook definitions
  scripts/                   # hook scripts, utilities
    check.sh
    validate.sh
  CLAUDE.md                  # architecture guide (for Claude)
  README.md                  # user documentation (for humans)
  LICENSE
```

### Directory Conventions

| Directory | Auto-discovered? | What goes here |
|-----------|-----------------|----------------|
| `.claude-plugin/` | Yes (manifest) | Plugin metadata |
| `commands/` | Yes | Slash command definitions |
| `commands/shared/` | Yes (but not invocable) | Shared command logic |
| `agents/` | Yes | Agent definitions |
| `skills/` | Yes | Domain knowledge |
| `hooks/` | Yes (`hooks.json`) | Event hooks |
| `scripts/` | No | Shell scripts, utilities |

### Naming Conventions

| Component | File naming | Example |
|-----------|------------|---------|
| Commands | kebab-case, descriptive verb | `scan-files.md`, `generate-report.md` |
| Agents | kebab-case, role-noun | `security-reviewer.md`, `parser.md` |
| Skills | kebab-case directory, always `SKILL.md` | `skills/my-plugin/react-patterns/SKILL.md` |
| Hook scripts | kebab-case, descriptive | `check-loc.sh`, `validate-config.sh` |

## 5. Versioning

### Semver Rules

| Change type | Bump | Example |
|------------|------|---------|
| Bug fixes, typo corrections, penalty adjustments | Patch: 0.1.0 -> 0.1.1 | Fix scoring formula |
| New commands, new agents, new features | Minor: 0.1.0 -> 0.2.0 | Add `/plugin:export` command |
| Breaking changes (renamed commands, removed features) | Major: 0.1.0 -> 1.0.0 | Rename `/scan` to `/analyze` |

### Four-Place Update

When bumping version, update in **four** places:

| Location | File | Field |
|----------|------|-------|
| 1. Plugin manifest | `.claude-plugin/plugin.json` | `version` |
| 2. Plugin marketplace | `.claude-plugin/marketplace.json` | `version` in the plugin's entry |
| 3. Central marketplace manifest | `~/.claude/plugins/marketplaces/xiaolai/.claude-plugin/marketplace.json` | `version` |
| 4. Central marketplace README | `~/.claude/plugins/marketplaces/xiaolai/README.md` | Version in the table |

**Order**: push plugin repo first, then update central marketplace. The marketplace points to the repo -- if the repo isn't updated yet, users pull stale code.

## 6. CLAUDE.md for Plugins

Your plugin's CLAUDE.md is for **Claude** (the AI), not the user. It tells Claude how the plugin's artifacts relate to each other.

### What to Include

```markdown
# my-plugin

## Architecture
Brief description of what the plugin does and how artifacts interact.

## Components

### Commands
| Command | Purpose |
|---------|---------|
| /plugin:scan | Discovers and inventories files |
| /plugin:fix | Auto-fixes issues found by scan |

### Agents
| Agent | Model | Role |
|-------|-------|------|
| scanner | haiku | Mechanical file discovery |
| fixer | sonnet | AI-powered fix generation |

### Conventions
- All agents output findings in severity-tagged format
- Scanner runs before fixer (sequential dependency)
- Hook scripts use fail-open pattern
```

### What NOT to Include

- Installation instructions (those go in README.md)
- User-facing documentation (README.md)
- Changelog (CHANGELOG.md or git history)
- Contributing guidelines (CONTRIBUTING.md)

## 7. Shared Partials

Extract repeated logic into `commands/shared/*.md` with `user-invocable: false`.

### Partial Frontmatter

```yaml
---
user-invocable: false
description: "Shared config loading logic"
---
```

### Good Candidates for Extraction

| Partial | Content | When to extract |
|---------|---------|----------------|
| `shared/load-config.md` | Read and validate config file | 3+ commands need config |
| `shared/discover-files.md` | Find target files by pattern | 3+ commands scan files |
| `shared/validate-prereqs.md` | Check tool availability | 2+ commands need same tools |
| `shared/format-report.md` | Report header, footer, severity format | 3+ commands output reports |

### When NOT to Extract

- Logic used by only 1 command (premature abstraction)
- Simple logic under 10 lines (duplication is fine)
- Logic that differs slightly between commands (forced generalization adds complexity)

## 8. Testing Your Plugin

### Pre-Publish Checklist

| Check | How | Pass criteria |
|-------|-----|---------------|
| Structure validation | `claude plugin validate /path/to/plugin` | No errors |
| Command: no args | Run each command with no arguments | Helpful error or usage message |
| Command: normal args | Run each command with typical input | Correct output |
| Command: edge cases | Empty files, huge files, missing files | Graceful error handling |
| Agent triggering | Try queries that should and shouldn't trigger | Correct dispatch decisions |
| Hook scripts | `chmod +x` check, run with test JSON | Valid JSON output |
| Hook fail-open | Kill script mid-execution | Action is allowed |

### Testing Agent Triggers

For each agent, test with 3 types of queries:

| Query type | Expected | Example |
|-----------|----------|---------|
| Direct match | Agent triggers | "Scan this code for security issues" |
| Adjacent topic | Agent may or may not trigger | "Is this code okay?" |
| Unrelated | Agent does NOT trigger | "What's the weather?" |

## 9. Marketplace Publishing

1. Push your plugin repo to GitHub
2. Add entry to central `marketplace.json` (name, source, description, version, author, license, keywords, category)
3. Add row to central marketplace `README.md` version table
4. Commit and push the central marketplace repo
5. Verify: `claude plugin install my-plugin@xiaolai --scope project`

**Pre-publish checks**: `claude plugin validate .`, verify no hardcoded paths (`grep -r '/Users/' commands/ agents/ hooks/`), verify all scripts executable, verify version matches in all 4 locations.

## 10. Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Commands that do too much | Hard to maintain, unreliable | Split into focused commands |
| Agents without examples | 40% trigger accuracy | Add 2-3 specific scenario examples |
| Skills over 500 lines | Context bloat, slow loading | Extract to references/ subdirectory |
| Hooks that block without explanation | Frustrating UX | Always include `permissionDecisionReason` |
| No CLAUDE.md | Claude doesn't understand plugin architecture | Add architecture overview |
| README documents internals | Users confused by implementation details | README = user guide, CLAUDE.md = internals |
| Hardcoded paths | Breaks on other machines | Use `${CLAUDE_PLUGIN_ROOT}` everywhere |
| No error handling in commands | Silent failures | Add explicit error cases |
| Version not updated in all 4 places | Marketplace shows wrong version | Use the four-place update checklist |
| Premature extraction into shared/ | Over-abstracted, harder to understand | Extract only when 3+ consumers exist |
