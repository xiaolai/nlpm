---
name: writing-hooks
description: "How to write Claude Code hooks — creating command, prompt, and agent hooks, selecting events, writing matcher patterns, configuring blocking vs advisory behavior, and setting up portable paths. Use when creating hooks for quality gates, pre-commit checks, automated linting, policy enforcement, or hook configuration."
version: 0.1.0
---

# Writing Hooks

> Scope: covers hooks.json authoring and hook script design. For plugin architecture, see [[writing-plugins]]. For rules (which are simpler but static), see [[writing-rules]].

## 1. Three Hook Types

| Type | What it does | When to use | Complexity |
|------|-------------|-------------|------------|
| `command` | Runs a shell script, reads JSON from stdin | Deterministic checks: file existence, JSON validation, regex matching | Medium |
| `prompt` | Injects text into Claude's context | Advisory: reminders, context injection, style guidance | Low |
| `agent` | Spawns a verification agent | Complex verification: code quality, semantic analysis, multi-file checks | High |

### Type Selection Flowchart

```
Is the check deterministic (regex, file exists, JSON schema)?
  YES --> command hook (shell script)
  NO  --> Does it need AI judgment?
    YES --> agent hook
    NO  --> prompt hook (context injection)
```

### Command Hook Example

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/check-loc.sh",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```

Hook script receives JSON on stdin with tool name and parameters. It outputs JSON to stdout.

### Prompt Hook Example

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Remember: this project uses Result<T, E> for error handling. Never use try/catch directly."
          }
        ]
      }
    ]
  }
}
```

### Agent Hook Example

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "agent",
            "agent": "Verify the written file follows project conventions. Check: import order, export style, naming conventions. Report any violations."
          }
        ]
      }
    ]
  }
}
```

## 2. Blocking vs Advisory

### Blocking (PreToolUse with deny)

The hook prevents the tool from executing. Use for hard quality gates.

**Script output for blocking**:
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "deny",
    "permissionDecisionReason": "File exceeds 300 LOC limit (current: 342). Extract logic before writing."
  }
}
```

**When to block**:
- Tests must pass before committing
- File exceeds size limit
- Required field missing from config
- Dangerous operation detected (force push, drop table)

### Advisory (PostToolUse with message)

The hook adds a message to Claude's context after the action completes. Use for suggestions and reminders.

**Script output for advisory**:
```json
{
  "hookSpecificOutput": {
    "message": "The file you just edited has no tests. Consider adding tests in __tests__/."
  }
}
```

**When to advise**:
- Suggest related actions (run tests, update docs)
- Remind about conventions
- Surface contextual information
- Warn about potential issues without blocking

### Decision Matrix

| Situation | Block or Advise? | Rationale |
|-----------|-----------------|-----------|
| Test failure on commit | Block | Broken tests should never be committed |
| File over LOC limit | Block | Enforce hard limit |
| Missing JSDoc on export | Advise | Nice to have, not a hard requirement |
| No tests for new file | Advise | Reminder, not a gate |
| Force push to main | Block | Destructive, irreversible |
| Large file creation (>500 lines) | Advise | Might be intentional (generated code) |

**Rule of thumb**: block only what you would reject in a code review. Advise on everything else.

## 3. Event Selection Guide

| Event | When it fires | Common use cases |
|-------|--------------|-----------------|
| `PreToolUse` | Before a tool executes | Block dangerous operations, validate inputs, check preconditions |
| `PostToolUse` | After a tool succeeds | Trigger follow-up actions, lint changed files, update state |
| `PostToolUseFailure` | After a tool fails | Error recovery, suggest alternatives, log failures |
| `UserPromptSubmit` | When user sends a message | Context injection, session setup, mode activation |
| `Stop` | When Claude stops responding | Cleanup, summary generation, state persistence |
| `SessionStart` | Session begins | Environment validation, context loading, config checks |

### Event Selection by Goal

| Goal | Event | Hook type |
|------|-------|-----------|
| Prevent bad writes | `PreToolUse` + matcher `Write\|Edit` | command |
| Lint after edit | `PostToolUse` + matcher `Write\|Edit` | command |
| Inject project context | `UserPromptSubmit` | prompt |
| Validate environment on start | `SessionStart` | command |
| Save session summary on exit | `Stop` | agent |
| Recover from failed bash commands | `PostToolUseFailure` + matcher `Bash` | prompt |

## 4. Matcher Patterns

The `matcher` field uses regex to match tool names. It applies only to `PreToolUse`, `PostToolUse`, and `PostToolUseFailure` events.

| Pattern | Matches | Use case |
|---------|---------|----------|
| `"Bash"` | Bash tool only | Guard shell commands |
| `"Write\|Edit"` | Write or Edit | Guard file modifications |
| `"Write"` | Write only | Guard new file creation |
| `"Edit"` | Edit only | Guard file edits (not creation) |
| `"Read"` | Read tool | Track what files Claude reads |
| `"mcp__.*"` | All MCP tool calls | Guard external integrations |
| `"mcp__github__.*"` | GitHub MCP tools | Guard GitHub operations |
| `"Task"` | Task tool (agent dispatch) | Monitor agent dispatching |
| `".*"` | Everything | Use carefully -- fires on every tool call |

### Matcher Testing

Before deploying, verify your matcher with test cases:

| Matcher | Should match | Should NOT match |
|---------|-------------|-----------------|
| `"Write\|Edit"` | Write, Edit | Bash, Read, WriteFile |
| `"Bash"` | Bash | BashScript, mcp__bash |
| `"mcp__github__.*"` | mcp__github__create_pr | mcp__slack__send |

## 5. Portable Paths

Always use `${CLAUDE_PLUGIN_ROOT}` for script paths in hooks.json. This variable resolves to the plugin's installation directory at runtime.

### Correct

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/check-loc.sh"
}
```

### Wrong (breaks on other machines)

```json
{
  "command": "/Users/joker/.claude/plugins/cache/xiaolai/my-plugin/0.1.0/scripts/check-loc.sh"
}
```

### Script Location Convention

```
my-plugin/
  hooks/
    hooks.json          # hook definitions
  scripts/
    check-loc.sh        # hook scripts
    validate-config.sh
    lint-output.sh
```

### Script Requirements

Every hook script must have:

1. **Shebang line**: `#!/bin/bash` or `#!/usr/bin/env node`
2. **Executable permission**: `chmod +x scripts/*.sh`
3. **JSON output**: scripts must output valid JSON to stdout
4. **Stderr for logging**: debug output goes to stderr, not stdout (stdout is parsed as JSON)

```bash
#!/bin/bash
# Read input from stdin
input=$(cat)

# Debug logging goes to stderr
echo "Hook triggered: $(date)" >&2

# Business logic
file_path=$(echo "$input" | jq -r '.toolInput.file_path // empty')

if [ -z "$file_path" ]; then
  # Allow if we can't determine the file
  echo '{"hookSpecificOutput":{"decision":"allow"}}'
  exit 0
fi

loc=$(wc -l < "$file_path" 2>/dev/null || echo "0")

if [ "$loc" -gt 300 ]; then
  echo "{\"hookSpecificOutput\":{\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"File has $loc lines, exceeds 300 LOC limit\"}}"
else
  echo '{"hookSpecificOutput":{"decision":"allow"}}'
fi
```

## 6. Fail-Open vs Fail-Closed

What happens when your hook script crashes?

### Fail-Open (recommended default)

If the script crashes, **allow** the action. Safer for advisory hooks and non-critical checks.

```bash
#!/bin/bash
# Fail-open wrapper
set +e  # Don't exit on error

result=$(your_check_logic 2>/dev/null)
exit_code=$?

if [ $exit_code -ne 0 ]; then
  # Script failed -- allow the action (fail-open)
  echo '{"hookSpecificOutput":{"decision":"allow"}}'
  exit 0
fi

# Normal processing...
echo "$result"
```

### Fail-Closed (security-critical only)

If the script crashes, **deny** the action. Use only for critical security gates.

```bash
#!/bin/bash
# Fail-closed wrapper
set +e

result=$(your_check_logic 2>/dev/null)
exit_code=$?

if [ $exit_code -ne 0 ]; then
  # Script failed -- deny the action (fail-closed)
  echo '{"hookSpecificOutput":{"permissionDecision":"deny","permissionDecisionReason":"Safety check script failed -- blocking action as precaution"}}'
  exit 0
fi

# Normal processing...
echo "$result"
```

### When to Use Each

| Hook purpose | Fail mode | Rationale |
|-------------|-----------|-----------|
| LOC limit enforcement | Fail-open | Better to allow a large file than block all writes |
| Style reminder | Fail-open | Non-critical advisory |
| Prevent force push to main | Fail-closed | Destructive action, err on side of caution |
| Secret detection | Fail-closed | Security-critical, must not leak |
| Test runner | Fail-open | Test infra failures shouldn't block development |

## 7. Common Mistakes

| Mistake | Why it's wrong | Fix |
|---------|---------------|-----|
| Blocking on `PostToolUse` | Action already happened -- too late to block | Use `PreToolUse` for blocking |
| Wrong event case | `pretooluse` instead of `PreToolUse` -- case-sensitive | Use exact case: `PreToolUse`, `PostToolUse`, etc. |
| Script not executable | Hook fails silently | Run `chmod +x scripts/*.sh` |
| Missing shebang | Script may run with wrong interpreter | Add `#!/bin/bash` or `#!/usr/bin/env node` |
| Hardcoded paths | Breaks on other machines | Use `${CLAUDE_PLUGIN_ROOT}` |
| stdout pollution | Debug output mixed into JSON response | Use stderr for logging: `echo "debug" >&2` |
| No timeout | Slow script blocks Claude indefinitely | Set `"timeout": 10000` (10 seconds) |
| Matcher too broad (`".*"`) | Fires on every tool call, performance impact | Narrow to specific tools |
| No fail-open wrapper | Script crash = broken hook = frustrated user | Wrap in fail-open try/catch |

## 8. Quality Checklist

Before deploying hooks, verify:

- [ ] Each hook has the correct event type for its purpose
- [ ] Blocking hooks use `PreToolUse`, not `PostToolUse`
- [ ] Matchers are tested against expected and unexpected tool names
- [ ] All script paths use `${CLAUDE_PLUGIN_ROOT}`
- [ ] All scripts have shebangs and executable permissions
- [ ] All scripts output valid JSON to stdout
- [ ] Debug logging goes to stderr, not stdout
- [ ] Fail-open or fail-closed is explicitly chosen for each hook
- [ ] Timeouts are set (default: 10 seconds)
- [ ] Hooks are tested with: normal input, edge case input, missing input
