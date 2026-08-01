---
name: check
description: "Check cross-artifact consistency — reference integrity, orphans, contradictions"
argument-hint: "[path]"
allowed-tools: Read, Glob, Grep, Task
---

## User Input

```text
$ARGUMENTS
```

## Workflow

### Step 1: Discover ALL Artifacts

Parse `$ARGUMENTS` for path (default: cwd). Use `commands/shared/discover.md` to find all Category A+B artifacts. Read every file.

If no artifacts found → "No NL programming artifacts found."

If fewer than 2 artifacts → "Cross-artifact check requires multiple artifacts. Use /nlpm:score for individual files."

### Step 2: Run the Cross-Artifact Check

Dispatch the `nlpm:checker` agent with ALL artifacts and the instruction to perform cross-artifact checks:

1. **Reference integrity**
   - Commands reference shared partials by path (`commands/shared/name.md`) → verify file exists
   - Agents reference skills in frontmatter (`skills: [plugin:skill]`) → verify skill SKILL.md exists
   - Hooks reference scripts (`${CLAUDE_PLUGIN_ROOT}/scripts/name.sh`) → verify script exists
   - Any `Follow commands/shared/...` or `See commands/shared/...` in body → verify path

2. **Orphaned artifacts**
   - Shared partials not referenced by any command → orphan
   - Skills not referenced by any agent → orphan
   - Scripts not referenced by any hook → orphan

3. **Behavioral contradictions**
   - Command says "always do X" but referenced partial says "never do X"
   - Two agents claim the same responsibility domain
   - Rules contradict each other or contradict CLAUDE.md

4. **Terminology drift**
   - Same concept called different names across artifacts
   - Inconsistent naming (kebab vs camelCase vs snake_case)

### Step 3: Report

```markdown
NLPM Cross-Artifact Check

Artifacts checked: {N}

Reference Integrity:
  {N} references checked, {N} broken
  {list broken references}

Orphaned Artifacts:
  {N} orphans found
  {list orphans}

Contradictions:
  {N} found
  {list contradictions with both sides}

Terminology:
  {N} inconsistencies
  {list}

Verdict: {CLEAN | {N} findings}
```

**Error handling:**
- Unreadable files → skip with warning, note in report
- Path doesn't exist → "Directory not found: {path}"
