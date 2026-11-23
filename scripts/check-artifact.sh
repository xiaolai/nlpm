#!/bin/bash
# PostToolUse hook: detect NL artifact edits and remind to score.
# Fail-open (R31): if anything goes wrong, output nothing and exit 0.
set +e

input=$(cat 2>/dev/null)

# Extract file_path from JSON input. Try jq first, fall back to grep.
if command -v jq &>/dev/null; then
  file_path=$(echo "$input" | jq -r '.tool_input.file_path // .toolInput.file_path // empty' 2>/dev/null)
else
  file_path=$(echo "$input" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"file_path"[[:space:]]*:[[:space:]]*"//;s/"$//')
fi

if [ -z "$file_path" ]; then
  exit 0
fi

# Check if the file matches an NL artifact pattern.
#
# In shell case-pattern matching `*` matches `/` (unlike pathname expansion),
# so `*/commands/*.md` already matches `foo/commands/bar.md` AND
# `foo/commands/sub/bar.md` — the prior `*/commands/**/*.md` alternative
# (and the equivalents for skills/ and rules/) were unreachable. Removed.
is_artifact=false
case "$file_path" in
  */commands/*.md) is_artifact=true ;;
  */agents/*.md) is_artifact=true ;;
  */skills/*/SKILL.md) is_artifact=true ;;
  */.claude/rules/*.md) is_artifact=true ;;
  */hooks/*.json) is_artifact=true ;;
  */CLAUDE.md) is_artifact=true ;;
  */.claude-plugin/plugin.json) is_artifact=true ;;
  */.mcp.json) is_artifact=true ;;
esac

if [ "$is_artifact" = true ]; then
  basename=$(basename "$file_path")
  msg="NL artifact edited: ${basename}. /nlpm:score ${file_path} checks its quality."
  # Claude reads a PostToolUse hook's message only from stdout JSON
  # (hookSpecificOutput.additionalContext) or from stderr with exit 2.
  # stderr with exit 0 never reaches Claude:
  # https://code.claude.com/docs/en/hooks
  # JSON-escape the two characters a file path can carry that break a JSON string.
  esc=$(printf '%s' "$msg" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g')
  printf '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"%s"}}\n' "$esc"
fi

exit 0
