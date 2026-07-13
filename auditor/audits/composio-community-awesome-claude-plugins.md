# NLPM Audit: composio-community/awesome-claude-plugins
**Date**: 2026-04-06  |  **Artifacts**: 88  |  **Strategy**: progressive
**NL Score**: 89/100
**Security**: BLOCKED
**Bugs**: 20  |  **Quality Issues**: 105  |  **Security Findings**: 13

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| bug-fix/commands/bug-fix.md | command | 55 | Uses literal $ARG instead of $ARGUMENTS; no steps, no output format, no error handling |
| agent-sdk-dev/agents/agent-sdk-verifier-py.md | agent | 60 | Zero examples, tools not declared, heavy vague language (capped -20) |
| agent-sdk-dev/agents/agent-sdk-verifier-ts.md | agent | 60 | Zero examples, tools not declared, heavy vague language (capped -20) |
| create-pr/commands/create-pr.md | command | 68 | No numbered steps, no output format, no allowed-tools |
| audit-project/commands/audit-project-agents.md | command | 68 | Missing frontmatter entirely; references nonexistent 'review' agent |
| audit-project/commands/audit-project-github.md | command | 70 | Missing frontmatter entirely; no allowed-tools |
| ship/commands/ship-error-handling.md | command | 70 | Missing frontmatter; references nonexistent next-task:ci-fixer plugin |
| ship/commands/ship-ci-review-loop.md | command | 70 | Missing frontmatter; references nonexistent next-task:ci-fixer plugin |
| ship/commands/ship-deployment.md | command | 70 | Missing frontmatter entirely |
| commit/commands/commit.md | command | 73 | No allowed-tools, no empty-input/error handling |
| documentation-generator/commands/documentation-generator.md | command | 75 | No empty-input handling, no output format, no error handling |
| pr-review/commands/pr-review.md | command | 75 | No empty-input handling, no output format, no error handling |
| frontend-developer/agents/frontend-developer.md | agent | 75 | No model declared, no output format, unused tools |
| perf/agents/perf-theory-gatherer.md | agent | 75 | Zero examples, no output format; references nonexistent docs/perf-requirements.md |
| perf/agents/perf-code-paths.md | agent | 75 | Zero examples, no output format |
| backend-architect/agents/backend-architect.md | agent | 76 | No model declared, no output format, vague language |
| test-writer-fixer/agents/test-writer-fixer.md | agent | 78 | No model, no tools declared, vague language |
| debugger/agents/debugger.md | agent | 80 | Zero examples, no model declared |
| perf/skills/theory/SKILL.md | skill | 80 | name mismatch (perf-theory-gatherer vs theory dir); references missing docs/perf-requirements.md |
| code-review/commands/code-review.md | command | 81 | No output-format template, no error handling |
| perf/skills/investigation-logger/SKILL.md | skill | 82 | name mismatch (perf-investigation-logger vs investigation-logger dir) |
| perf/skills/benchmark/SKILL.md | skill | 82 | name mismatch (perf-benchmarker vs benchmark dir) |
| perf/skills/analyzer/SKILL.md | skill | 82 | name mismatch (perf-analyzer vs analyzer dir) |
| perf/skills/profile/SKILL.md | skill | 82 | name mismatch (perf-profiler vs profile dir) |
| perf/skills/baseline/SKILL.md | skill | 82 | name mismatch (perf-baseline-manager vs baseline dir) |
| perf/agents/perf-analyzer.md | agent | 82 | Zero examples; unused Write tool |
| skill-bus/commands/help.md | command | 85 | No argument-hint, no allowed-tools, no SB_CLI-missing handling |
| perf/agents/perf-theory-tester.md | agent | 85 | Zero examples |
| perf/agents/perf-investigation-logger.md | agent | 85 | Zero examples |
| perf/agents/perf-orchestrator.md | agent | 85 | Zero examples; grep used in body but not declared in tools |
| skill-bus/commands/onboard.md | command | 87 | No allowed-tools; repeated vague 'relevant' |
| agent-sdk-dev/commands/new-sdk-app.md | command | 87 | No allowed-tools; vague language |
| skill-bus/skills/help/SKILL.md | skill | 87 | Zero examples, no scope note |
| skill-bus/skills/list-subs/SKILL.md | skill | 87 | Zero examples, no scope note |
| skill-bus/skills/remove-sub/SKILL.md | skill | 87 | Zero examples, no scope note |
| skill-bus/skills/unpause-subs/SKILL.md | skill | 87 | Zero examples, no scope note |
| skill-bus/skills/add-sub/SKILL.md | skill | 87 | Zero examples, no scope note |
| skill-bus/commands/unpause-subs.md | command | 88 | Missing 'nothing paused' case; no allowed-tools |
| skill-bus/commands/list-subs.md | command | 90 | No allowed-tools; unquoted argument interpolation (security) |
| skill-bus/skills/pause-subs/SKILL.md | skill | 90 | Zero examples |
| mcp-builder/skills/mcp-builder/SKILL.md | skill | 90 | No code examples for complex schema concepts |
| frontend-design/skills/frontend-design/SKILL.md | skill | 90 | No code examples for complex concepts |
| developer-growth-analysis/skills/developer-growth-analysis/SKILL.md | skill | 92 | Repeated vague 'relevant'/'several' |
| skill-bus/commands/pause-subs.md | command | 93 | No allowed-tools |
| perf/skills/code-paths/SKILL.md | skill | 93 | No scope note; vague 'relevant' |
| skill-bus/commands/remove-sub.md | command | 95 | No allowed-tools |
| skill-bus/commands/edit-insert.md | command | 95 | No allowed-tools |
| skill-bus/commands/report.md | command | 95 | No allowed-tools; unquoted argument interpolation (security) |
| skill-bus/commands/add-sub.md | command | 95 | No allowed-tools |
| skill-bus/commands/complete.md | command | 95 | No argument-hint |
| perf/skills/theory-tester/SKILL.md | skill | 97 | No scope note |
| canvas-design/skills/canvas-design/SKILL.md | skill | 98 | One vague quantifier ('some') |
| theme-factory/skills/theme-factory/SKILL.md | skill | 98 | One vague quantifier; references unbacked theme spec data |
| agent-sdk-dev/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| artifacts-builder/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| artifacts-builder/skills/artifacts-builder/SKILL.md | skill | 100 | References missing scripts/init-artifact.sh, scripts/bundle-artifact.sh |
| audit-project/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| audit-project/commands/audit-project.md | command | 100 | References nonexistent 'review' agent; unsanitized ${ARGUMENTS} in bash (security) |
| backend-architect/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| bug-fix/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| canvas-design/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| changelog-generator/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| changelog-generator/skills/changelog-generator/SKILL.md | skill | 100 | None |
| code-review/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| commit/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| connect-apps/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| connect-apps/commands/setup.md | command | 100 | None |
| create-pr/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| debugger/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| developer-growth-analysis/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| documentation-generator/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| frontend-design/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| frontend-developer/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| mcp-builder/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| perf/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| perf/commands/perf.md | command | 100 | References missing docs/; unsanitized $ARGUMENTS spliced into JS (security) |
| pr-review/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| security-guidance/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| security-guidance/hooks/hooks.json | hooks | 100 | None |
| senior-frontend/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| senior-frontend/skills/senior-frontend/SKILL.md | skill | 100 | None |
| ship/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| ship/commands/ship.md | command | 100 | References nonexistent 'review'/'next-task' agents; unsanitized $ARGUMENTS into JS (security) |
| skill-bus/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| skill-bus/hooks/hooks.json | hooks | 100 | None |
| skill-bus/skills/reflecting-on-sessions/SKILL.md | skill | 100 | None |
| test-writer-fixer/.claude-plugin/plugin.json | plugin-manifest | 100 | None |
| theme-factory/.claude-plugin/plugin.json | plugin-manifest | 100 | None |

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 5 |
| Medium | 5 |
| Low | 3 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks configs | skill-bus/hooks/hooks.json, security-guidance/hooks/hooks.json |
| Hook scripts | skill-bus/hooks/post-skill.sh, skill-bus/hooks/dispatch.sh, skill-bus/hooks/pre-skill.sh, skill-bus/hooks/prompt-monitor.sh, security-guidance/hooks/security_reminder_hook.py |
| Library scripts (JS) | 96 files under perf/lib/** — **byte-identical** duplicates also present at audit-project/lib/** and ship/lib/** (confirmed via `diff -rq`, zero differences); scanned once as canonical copy |
| Library scripts (Python) | skill-bus/lib/dispatcher.py, skill-bus/lib/cli.py, skill-bus/lib/telemetry.py |
| MCP configs | none found (no `.mcp.json` anywhere in the repo) |
| Package manifests | none found (no `package.json` or `requirements.txt` anywhere in the repo) |
| Commands with embedded shell/JS argument interpolation | perf/commands/perf.md, ship/commands/ship.md, audit-project/commands/audit-project.md, skill-bus/commands/list-subs.md, skill-bus/commands/report.md |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | skill-bus/commands/list-subs.md | 28 | unsanitized-arg-into-shell | `python3 "$SB_CLI" simulate <skill-name> --cwd "$PWD" --timing <pre\|post\|complete>` substitutes user-supplied values directly into the shell command line with no quoting |
| 2 | High | skill-bus/commands/report.md | 33 | unsanitized-arg-into-shell | `python3 "$SB_CLI" simulate [skill] --cwd "$PWD"` substitutes a suggestion-derived value directly into the shell command with no quotes |
| 3 | High | perf/commands/perf.md | 59 | arg-into-js-string-literal | `const args = argumentParser.parseArguments('$ARGUMENTS');` splices the raw `$ARGUMENTS` placeholder into a JS string literal executed via `node`, with no escaping |
| 4 | High | audit-project/commands/audit-project.md | 59 | arg-into-bash-conditional | `RESUME_MODE=$([ "${ARGUMENTS}" != "${ARGUMENTS%--resume*}" ] && echo true \|\| echo false)` interpolates raw `${ARGUMENTS}` into a bash test expression with no quoting |
| 5 | High | ship/commands/ship.md | 81 | arg-into-js-string-literal | `const args = '$ARGUMENTS'.split(' ');` splices the raw `$ARGUMENTS` placeholder into a JS string literal executed via `node`, with no escaping |
| 6 | Medium | perf/lib/perf/benchmark-runner.js | 74 | execSync-arbitrary-command | `runBenchmark(command, options)` passes a caller-supplied string straight to `execSync` (shell-invoking); legitimate benchmark-runner design, but no allowlist/validation on `command`. Identical code also at audit-project/lib and ship/lib |
| 7 | Medium | perf/lib/perf/profiling-runner.js | 35 | execSync-arbitrary-command | `runProfiling` builds a command via `profiler.buildCommand()` and runs it with `execSync`; same shell-invocation pattern. Identical code also at audit-project/lib and ship/lib |
| 8 | Medium | skill-bus/lib/dispatcher.py | 281 | config-driven-file-read | `fileExists`/`fileContains` condition types accept absolute or `~`-expanded paths from `skill-bus.json` and read their contents for pattern matching; a locally-authored config could point this at sensitive files |
| 9 | Medium | security-guidance/hooks/security_reminder_hook.py | 14 | hardcoded-tmp-path-write | `DEBUG_LOG_FILE = "/tmp/security-warnings-log.txt"` is a hardcoded absolute path outside the repo/project directory that the hook appends debug messages to |
| 10 | Medium | perf/lib/perf/benchmark-runner.js | 60 | env-passthrough | `runBenchmark` spreads the full `process.env` plus caller-supplied env into the child process before `execSync`, forwarding any secrets present in the parent environment |
| 11 | Low | perf/lib/platform/detect-platform.js | 234 | shell-exec-fixed-string | `detectBranchStrategy`/`detectMainBranch` use `exec`/`execAsync` (shell-invoking) with fixed literal git commands, no interpolated input |
| 12 | Low | perf/lib/cross-platform/index.js | 48 | env-var-read | Reads non-secret configuration env vars (`AI_STATE_DIR`, `PLUGIN_ROOT`, `PERF_EXPERIMENT`, etc.); pattern repeats across several perf/lib files |
| 13 | Low | security-guidance/hooks/security_reminder_hook.py | 131 | state-file-in-home-dir | Session state written under `~/.claude/security_warnings_state_<id>.json` rather than the project directory; standard convention for this plugin family |

No critical findings. No curl/wget-pipe-to-shell, no `eval()` on untrusted input, no reverse-shell patterns, no base64-decode-then-exec chains, no credential exfiltration, and no evidence of a backdoor anywhere in the scanned surface.

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | bug-fix/commands/bug-fix.md | Uses literal `$ARG` (line 8) instead of `$ARGUMENTS` | User's bug description is never substituted into the prompt; every invocation runs with no real input |
| 2 | audit-project/commands/audit-project-agents.md | Missing frontmatter entirely (no name/description) | Command may not register/discover correctly |
| 3 | audit-project/commands/audit-project-agents.md | References nonexistent `orchestrate-review` skill and `subagent_type: "review"` agent | Review-dispatch phase cannot resolve an agent/skill |
| 4 | audit-project/commands/audit-project-github.md | Missing frontmatter entirely | Command may not register/discover correctly |
| 5 | audit-project/commands/audit-project.md | Inherits the broken `subagent_type: "review"` dependency via Phase 2 | Top-level orchestrator surfaces the same dispatch failure |
| 6 | ship/commands/ship.md | References `subagent_type: "review"` and `"next-task:ci-fixer"` — neither exists in this repo or marketplace.json's 25 listed plugins | Review and CI-auto-fix phases cannot dispatch |
| 7 | ship/commands/ship-error-handling.md | Missing frontmatter entirely | File is not registered as an invocable command |
| 8 | ship/commands/ship-error-handling.md | References nonexistent `next-task:ci-fixer` plugin | CI-fixer delegation step cannot resolve an agent |
| 9 | ship/commands/ship-ci-review-loop.md | Missing frontmatter entirely | File is not registered as an invocable command |
| 10 | ship/commands/ship-ci-review-loop.md | References nonexistent `next-task:ci-fixer` plugin | CI review loop's auto-fix step cannot resolve an agent |
| 11 | ship/commands/ship-deployment.md | Missing frontmatter entirely | File is not registered as an invocable command |
| 12 | perf/commands/perf.md (+13 other perf agents/skills) | References `docs/perf-requirements.md` as the canonical contract; no `docs/` directory exists anywhere under perf/ | Every phase of the perf workflow instructs Claude to read a file that doesn't exist — first-step failure across nearly the whole plugin |
| 13 | perf/skills/investigation-logger/SKILL.md | frontmatter `name: perf-investigation-logger` ≠ parent dir `investigation-logger` | Skills that resolve by name==directory match may fail to load |
| 14 | perf/skills/benchmark/SKILL.md | frontmatter `name: perf-benchmarker` ≠ parent dir `benchmark` | Same as above |
| 15 | perf/skills/analyzer/SKILL.md | frontmatter `name: perf-analyzer` ≠ parent dir `analyzer` | Same as above |
| 16 | perf/skills/profile/SKILL.md | frontmatter `name: perf-profiler` ≠ parent dir `profile` | Same as above |
| 17 | perf/skills/baseline/SKILL.md | frontmatter `name: perf-baseline-manager` ≠ parent dir `baseline` | Same as above |
| 18 | perf/skills/theory/SKILL.md | frontmatter `name: perf-theory-gatherer` ≠ parent dir `theory` | Same as above |
| 19 | artifacts-builder/skills/artifacts-builder/SKILL.md | References `scripts/init-artifact.sh`/`scripts/bundle-artifact.sh`; no `scripts/` dir exists (plugin has only SKILL.md + plugin.json) | Following the skill's own instructions fails on its two core operations |
| 20 | perf/agents/perf-orchestrator.md | Instructs identifying hotspots "via repo-map or grep" but neither `Grep` nor `Bash(grep:*)` is declared in tools | Agent is instructed to use a capability it isn't granted |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | perf/lib/perf/benchmark-runner.js | `execSync(command, ...)` runs a caller-supplied string via shell, with full env passthrough | Consider `execFileSync` with an argv array, or an explicit env allowlist; apply identically to audit-project/lib and ship/lib (byte-identical files) |
| 2 | perf/lib/perf/profiling-runner.js | `execSync` runs a built command string via shell | Consider `execFileSync` with an argv array; apply identically to audit-project/lib and ship/lib |
| 3 | skill-bus/lib/dispatcher.py | `fileExists`/`fileContains` conditions can read arbitrary absolute/`~` paths from a local config | Restrict path resolution to the project directory, or document the trust assumption explicitly |
| 4 | security-guidance/hooks/security_reminder_hook.py | Hardcoded `/tmp/security-warnings-log.txt` debug log outside the plugin's own state directory | Write to `~/.claude/...` alongside the hook's other state files |
| 5 | perf/lib/perf/benchmark-runner.js | Full `process.env` passthrough to the benchmarked child process | Pass only an explicit allowlist of environment variables |
| 6 | perf/lib/platform/detect-platform.js | `exec`/`execAsync` used for fixed git commands instead of `execFile` | Switch to `execFile` with an argv array for consistency with the rest of the codebase |
| 7 | perf/lib/cross-platform/index.js | Reads several env vars for platform/state detection (documented for visibility) | No action needed |
| 8 | security-guidance/hooks/security_reminder_hook.py | Session state file lives in `~/.claude/` (documented for visibility) | No action needed |

## Quality Issues (informational)

105 rule-level findings across 53 files — full detail (rule id, exact penalty, per-file breakdown) is in the JSONL sidecar (`category: "nl_quality"`). Summary by dominant theme:

| Theme | Rule(s) | Files affected | Typical penalty |
|-------|---------|-----------------|------------------|
| Zero `<example>` blocks on agents | R09 | 9 agents (agent-sdk-verifier-py/ts, perf-theory-gatherer, perf-code-paths, perf-analyzer, perf-theory-tester, perf-investigation-logger, perf-orchestrator, debugger) | -15 each |
| Zero `<example>` blocks on user-invocable skills | R06 | 6 skill-bus skills (help, list-subs, remove-sub, unpause-subs, add-sub, pause-subs) | -10 each |
| No code examples for complex technical concepts | R06 | mcp-builder, frontend-design | -10 each |
| Missing `model` in agent frontmatter | R10 | frontend-developer, backend-architect, test-writer-fixer, debugger | -5 each |
| No output format defined | R12 / R16 | frontend-developer, backend-architect, perf-theory-gatherer, perf-code-paths (agents); create-pr, documentation-generator, pr-review, code-review (commands) | -10 each |
| Missing `allowed-tools` on commands that clearly invoke Bash | UNCLASSIFIED (no matching rule number in skills/nlpm/rules) | 19 commands across skill-bus, bug-fix, create-pr, commit, audit-project-github, new-sdk-app, ship-error-handling, ship-ci-review-loop, ship-deployment | -5 each |
| No numbered steps / empty-input / error-path handling | R14, R15, R16, R17 | bug-fix, create-pr, commit, documentation-generator, pr-review, code-review, skill-bus/help, skill-bus/list-subs, skill-bus/unpause-subs | -5 to -10 each |
| Missing `argument-hint` on input-taking commands | R18 | bug-fix, commit, skill-bus/help, skill-bus/complete | -5 each |
| No scope note / cross-references to sibling skills | R07 | 8 perf skills, skill-bus/help | -3 each |
| Vague quantifiers without measurable criteria | R01 | 21 files, capped at -20/file where dense (agent-sdk-verifier-py/ts) | -2 per occurrence |
| Unused tools declared in agent frontmatter | R11 | frontend-developer (Grep, Glob), backend-architect (Grep), perf-analyzer (Write) | -3 each |
| Tools not declared at all | R11 | agent-sdk-verifier-py/ts, test-writer-fixer | -5 each |

## Cross-Component

- **`docs/perf-requirements.md` gap**: 14 in-scope perf artifacts (perf.md, 8 SKILL.md files, 5 agent files) — plus perf/README.md and 2 perf/hooks/*.md files outside the scored 88 — all cite `docs/perf-requirements.md` (and two also cite `docs/perf-research-methodology.md`) as the "canonical contract." No `docs/` directory exists anywhere under `perf/`. This is the single highest-impact defect in the corpus: it affects nearly every artifact in one plugin.
- **Dangling `subagent_type` references across two plugins**: `audit-project` and `ship` both dispatch `Task({subagent_type: "review", ...})`, and `ship` additionally dispatches `"next-task:ci-fixer"`. Neither agent/plugin exists anywhere in this repo, and `marketplace.json` lists exactly 25 plugins — `next-task` is not among them, confirming this isn't a lookup miss but a genuine absence.
- **Perf skill name/directory mismatches**: 6 of 8 `perf/skills/*/SKILL.md` files have a frontmatter `name:` that doesn't match their parent directory (only `code-paths` and `theory-tester` are consistent). This is a repo-wide pattern within one plugin, not isolated typos.
- **Duplicate library trees**: `perf/lib/`, `audit-project/lib/`, and `ship/lib/` are byte-identical 96-file trees (`diff -rq` produced zero output for both pairwise comparisons). Not a functional bug, but a maintenance liability — a fix applied to one copy (e.g. the `execSync` hardening suggested above) needs to be applied three times unless the shared code is extracted into a common package.
- No broken `commands/shared/*.md` partial references were found (this marketplace doesn't use that partial pattern). No contradictions were found between sibling CLAUDE.md-equivalent files (none of the 25 plugins ship a root CLAUDE.md/AGENTS.md of their own).

## Recommendation

**BLOCKED — do not submit PRs for the 5 High-severity security findings. File a private security report for the unsanitized `$ARGUMENTS`/argument interpolation patterns in perf.md, ship.md, audit-project.md, list-subs.md, and report.md before any of those files are touched.**

Once the security gate clears (or in parallel, since these are independent code paths), the following are safe to act on immediately:
- All 20 NL bugs above, especially the `docs/perf-requirements.md` gap (highest blast radius) and the two missing-frontmatter clusters in `audit-project`/`ship`.
- The 8 Medium/Low security fixes (none require private disclosure).
- The 105 quality issues, prioritized by the "missing allowed-tools" and "zero examples" themes, which account for the bulk of the score deductions.
