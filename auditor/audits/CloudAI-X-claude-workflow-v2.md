# NLPM Audit: CloudAI-X/claude-workflow-v2
**Date**: 2026-04-12  |  **Artifacts**: 50  |  **Strategy**: batched
**NL Score**: 93/100
**Security**: CLEAR
**Bugs**: 6  |  **Quality Issues**: 20  |  **Security Findings**: 9

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/parallel-review.md | command | 82 | BUG: Task tool used, not declared in allowed-tools; no empty-input handling |
| commands/parallel-analyze.md | command | 82 | BUG: Task tool used, not declared in allowed-tools; no empty-input handling |
| commands/quick-fix.md | command | 88 | No explicit empty-input handling for $ARGUMENTS |
| commands/lint-fix.md | command | 88 | Missing output format template |
| commands/summarize-changes.md | command | 88 | No explicit empty-input handling for $ARGUMENTS |
| skills/convex-backend/SKILL.md | skill | 88 | BUG: References non-existent AGENTS.md |
| skills/vercel-react-best-practices/SKILL.md | skill | 88 | BUG: References non-existent AGENTS.md |
| commands/add-tests.md | command | 90 | Missing output format template |
| commands/commit.md | command | 90 | Minimal output format (no structured template) |
| commands/sync-branch.md | command | 90 | No explicit empty-input fallback for $ARGUMENTS |
| skills/designing-apis/SKILL.md | skill | 90 | BUG: References non-existent OPENAPI-TEMPLATE.md |
| commands/review.md | command | 92 | Missing allowed-tools declaration; "thorough" vague |
| commands/save-session-learnings.md | command | 92 | Vague "significant" used 3x (-6 pts) |
| commands/commit-push-pr.md | command | 92 | Minimal output format (no structured template) |
| CLAUDE.md | docs | 92 | Documents "1 hook file"; hooks.json registers 14 scripts |
| hooks/hooks.json | config | 92 | More hooks than CLAUDE.md implies; discrepancy with docs |
| commands/mentor.md | command | 93 | Missing allowed-tools declaration |
| commands/run-tests.md | command | 93 | Missing allowed-tools declaration |
| commands/verify-changes.md | command | 93 | BUG: Task tool used, not declared in allowed-tools |
| commands/code-simplifier.md | command | 93 | Missing allowed-tools declaration |
| commands/lint-check.md | command | 93 | Missing allowed-tools declaration |
| commands/rapid.md | command | 93 | Missing allowed-tools declaration |
| commands/security-scan.md | command | 93 | Missing allowed-tools declaration |
| commands/architect.md | command | 93 | Missing allowed-tools declaration |
| commands/validate-build.md | command | 93 | Missing allowed-tools declaration |
| agents/test-architect.md | agent | 94 | "comprehensive" vague (-2); "appropriate data structures" (-2) |
| agents/orchestrator.md | agent | 94 | "appropriate subagents" (-2); "relevant file paths" (-2) |
| agents/security-auditor.md | agent | 95 | Clean; minor phrasing |
| skills/managing-git/SKILL.md | skill | 95 | Clean |
| skills/devops-infrastructure/SKILL.md | skill | 95 | Clean |
| skills/analyzing-projects/SKILL.md | skill | 95 | Clean |
| skills/optimizing-performance/SKILL.md | skill | 95 | Clean |
| agents/debugger.md | agent | 96 | "strategic logging" mildly vague (-2) |
| agents/refactorer.md | agent | 96 | "apply as appropriate" (-2) |
| skills/designing-tests/SKILL.md | skill | 96 | Clean |
| skills/parallel-execution/SKILL.md | skill | 96 | Clean |
| agents/code-reviewer.md | agent | 97 | Clean |
| agents/docs-writer.md | agent | 97 | Clean |
| commands/plan.md | command | 97 | "significant update" vague (-2) |
| commands/tutorial.md | command | 97 | Clean |
| commands/bootstrap-repo.md | command | 97 | Clean; Task correctly declared |
| commands/metrics.md | command | 97 | Clean |
| skills/error-handling/SKILL.md | skill | 97 | Clean; exemplary anti-pattern coverage |
| skills/web-design-guidelines/SKILL.md | skill | 97 | Clean |
| skills/designing-architecture/SKILL.md | skill | 97 | Clean |
| skills/security-patterns/SKILL.md | skill | 97 | Clean |
| skills/database-design/SKILL.md | skill | 97 | Clean |
| .claude-plugin/plugin.json | config | 97 | Clean |
| commands/refactor-guided.md | command | 98 | Clean; best-in-class command |
| commands/dependency-upgrade.md | command | 98 | Clean; best-in-class command |

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 6 |
| Low | 3 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| hooks/hooks.json (registration) | 1 |
| Python hook scripts | 9 (protect-files.py, security-check.py, pre-commit-check.py, validate-environment.py, validate-prompt.py, format-on-edit.py, typescript-check.py, verify-on-complete.py, track-metrics.py, suggest-doc-updates.py — 10 actual) |
| Shell hook scripts | 4 (branch-protection.sh, log-commands.sh, notify-complete.sh, notify-input.sh) |
| MCP configs | none found |
| package.json / requirements.txt | none found |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | hooks/log-commands.sh | 3 | Unvalidated env var for file path | `CLAUDE_PROJECT_DIR` used without validation to construct log file path and `mkdir -p` target; a manipulated env var could redirect logs to arbitrary paths |
| 2 | Medium | hooks/track-metrics.py | 78–84 | File write using env var path | `CLAUDE_PROJECT_DIR` env var used to determine metrics file path; `os.makedirs()` + file open in append mode creates files at env-controlled location |
| 3 | Medium | hooks/format-on-edit.py | 48–52 | file_path passed to subprocess | `file_path` from `tool_input` passed directly as argument to formatter subprocess (`npx prettier --write <file_path>`). No shell=True, but path is caller-influenced |
| 4 | Medium | hooks/verify-on-complete.py | 57–82 | Executes auto-discovered package.json scripts | Reads `package.json` scripts.test and scripts.lint keys, then executes them via subprocess. If `package.json` is malicious, arbitrary commands run at session Stop |
| 5 | Medium | hooks/typescript-check.py | 46–52 | Executes project-local `npx tsc` | Runs `npx tsc` in the project directory, which resolves TypeScript from local `node_modules`. A malicious local package could be executed |
| 6 | Medium | hooks/validate-environment.py | 36–45 | Environment variable access for file checks | Reads `CLAUDE_PROJECT_DIR` and `CLAUDE_PROJECT_DIR/package.json` to check node_modules presence; low-risk but worth noting |
| 7 | Low | hooks/format-on-edit.py | 17–31 | Unpinned formatter invocations | `npx prettier`, `black`, `gofmt`, `rustfmt` run without version pinning; formatter behavior could change across environments |
| 8 | Low | hooks/typescript-check.py | 46 | Unpinned `npx tsc` | TypeScript compiler invoked via npx without a pinned version |
| 9 | Low | hooks/log-commands.sh | 2–3 | Verbose hook trigger (all Bash) | Hook fires on every Bash tool call and writes a log file; creates `.claude/` directory as a side effect on first run |

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/parallel-review.md | Uses `Task` tool (implicit, via run_in_background subagent spawning) but `allowed-tools` field is absent — `Task` is never declared | Command cannot spawn parallel subagents as designed; registration may block or silently fail |
| 2 | commands/parallel-analyze.md | Same as above: uses `Task` for 4 parallel perspective agents but `allowed-tools` is absent | Same: parallel analysis will fail silently |
| 3 | commands/verify-changes.md | Uses `Task` (5 verification + 3 adversarial subagents) but `allowed-tools` is absent | Verification subagents cannot be spawned; core feature broken |
| 4 | skills/convex-backend/SKILL.md | Line 119: `see: AGENTS.md` — no AGENTS.md exists in the skill directory or plugin root | Developers following the cross-reference find a dead link; full Convex ruleset is inaccessible via the skill |
| 5 | skills/vercel-react-best-practices/SKILL.md | Line 111: `see: AGENTS.md` — same broken reference | 45 Vercel/React rules described in the summary are unreachable; skill is effectively truncated |
| 6 | skills/designing-apis/SKILL.md | Line 198: `[OPENAPI-TEMPLATE.md](OPENAPI-TEMPLATE.md)` — file does not exist | OpenAPI spec template referenced in the API Design Validation section is a dead link |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | hooks/log-commands.sh | `CLAUDE_PROJECT_DIR` used without validation for log path and `mkdir -p` | Validate that the resolved path stays within a known safe prefix (e.g., check it starts with `$HOME` or `$(pwd)`) before creating directories |
| 2 | hooks/track-metrics.py | `CLAUDE_PROJECT_DIR` used for `os.makedirs()` + file write without path validation | Apply `os.path.realpath()` and assert the resolved path is under `os.getcwd()` or `$HOME` before writing |
| 3 | hooks/verify-on-complete.py | Executes discovered `package.json` script values directly | Restrict to an allowlist of known safe test runners (e.g., `npm test`, `pytest`, `go test ./...`); do not execute arbitrary script values |
| 4 | hooks/format-on-edit.py | Formatter invocations use `npx` without version constraint | Pin formatters via project devDependencies and use `./node_modules/.bin/prettier` instead of `npx`; fallback gracefully when not installed |
| 5 | hooks/typescript-check.py | `npx tsc` resolves from project node_modules without integrity check | Same fix as #4: use local `./node_modules/.bin/tsc` if available, skip otherwise |
| 6 | hooks/log-commands.sh | Broad trigger on all Bash calls creates noisy log with no rotation | Add log rotation (e.g., limit file size to 1MB) and consider narrowing the Bash matcher to git commands only |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/mentor.md | Missing `allowed-tools` in frontmatter; no tool restrictions declared | -5 |
| 2 | commands/run-tests.md | Missing `allowed-tools` in frontmatter | -5 |
| 3 | commands/code-simplifier.md | Missing `allowed-tools` in frontmatter (uses Bash implicitly via git) | -5 |
| 4 | commands/review.md | Missing `allowed-tools` in frontmatter | -5 |
| 5 | commands/lint-check.md | Missing `allowed-tools` in frontmatter | -5 |
| 6 | commands/rapid.md | Missing `allowed-tools` in frontmatter | -5 |
| 7 | commands/security-scan.md | Missing `allowed-tools` in frontmatter | -5 |
| 8 | commands/architect.md | Missing `allowed-tools` in frontmatter | -5 |
| 9 | commands/validate-build.md | Missing `allowed-tools` in frontmatter | -5 |
| 10 | commands/quick-fix.md | No explicit empty-input handling for `$ARGUMENTS`; if blank, task silently proceeds with no target | -10 |
| 11 | commands/sync-branch.md | `argument-hint` notes `(default: rebase)` but command body has no `if no argument` branch | -10 |
| 12 | commands/summarize-changes.md | `$ARGUMENTS` scope used with no explicit fallback to `today` in the command body | -10 |
| 13 | commands/lint-fix.md | No output format template; "Report what was fixed" is the only output guidance | -10 |
| 14 | commands/add-tests.md | No structured output format section (passes for NL but reduces consistency) | -10 |
| 15 | commands/commit.md | No output format template; commit result format not specified | -10 |
| 16 | commands/save-session-learnings.md | "significant" used 3× as gating criterion without definition; creates ambiguity about what triggers a save | -6 |
| 17 | agents/test-architect.md | "comprehensive tests" in task description; "appropriate data structures" in review checklist — both vague | -4 |
| 18 | agents/orchestrator.md | "appropriate subagents" and "relevant file paths" in communication guidelines — mildly vague | -4 |
| 19 | CLAUDE.md | States "Hooks: 1 files" (referring to hooks.json) but fails to document the 14 underlying scripts, their purposes, or event types | informational |
| 20 | hooks/hooks.json | Registers 6 event categories and 14 scripts vs CLAUDE.md implying a single hook; discoverability gap for new contributors | informational |

## Cross-Component

**References verified:**
- All 7 agents referenced in CLAUDE.md's "Available Agents" table exist and have correct names ✓
- All skills declared in agent frontmatter (`skills:` field) exist in `skills/*/SKILL.md` ✓
- `plugin.json` name `project-starter` matches command prefix used throughout all command files ✓
- All 14 scripts listed in `hooks.json` exist in `hooks/` ✓

**Broken references:**
- `skills/convex-backend/SKILL.md` → `AGENTS.md` (does not exist in plugin or skill directory)
- `skills/vercel-react-best-practices/SKILL.md` → `AGENTS.md` (same missing file)
- `skills/designing-apis/SKILL.md` → `OPENAPI-TEMPLATE.md` (does not exist)

**Orphaned components:**
- None identified. All agents are reachable via orchestrator delegation table; all commands have a corresponding use-case in CLAUDE.md.

**Contradictions:**
- `commands/run-tests.md` (line 127–130) and `commands/lint-check.md` (line 133–137) both include "Copy to your project" installation instructions referencing a `templates/subagents/` path that does not exist in this plugin. These files appear to have been adapted from a templates library without removing the stale installation instructions.
- Similarly, `commands/verify-changes.md`, `commands/code-simplifier.md`, and `commands/validate-build.md` all contain "Copy to your project: `cp templates/subagents/…`" instructions — stale copy from template origin.

## Recommendation

CLEAR — submit PRs for all bugs and medium/low security fixes.

The plugin is high-quality overall (93/100). All agents are well-structured with proper frontmatter, model declarations, example blocks, and output formats. The skills library is comprehensive and largely clean. The primary action items are:

1. **Highest priority** — Fix the three broken cross-references in skills (AGENTS.md × 2, OPENAPI-TEMPLATE.md × 1). These silently truncate skill content.
2. **High priority** — Add `allowed-tools: Task` (and dependent tools) to `parallel-review.md`, `parallel-analyze.md`, and `verify-changes.md`. These commands are nonfunctional without it.
3. **Medium priority** — Add `allowed-tools` declarations to the 9 commands missing them (mentor, run-tests, code-simplifier, review, lint-check, rapid, security-scan, architect, validate-build). While the commands may still execute, the absence signals missing access control.
4. **Medium priority** — Remove stale "Copy to your project: `cp templates/subagents/…`" instructions from run-tests.md, lint-check.md, verify-changes.md, code-simplifier.md, and validate-build.md. These reference a non-existent `templates/` directory.
5. **Low priority** — Apply the Medium-severity security fixes: validate env-var-derived paths in log-commands.sh and track-metrics.py, restrict verify-on-complete.py to an allowlist of test runners, and pin formatter invocations in format-on-edit.py and typescript-check.py.
