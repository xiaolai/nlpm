# NLPM Audit: ComposioHQ/awesome-claude-plugins
**Date**: 2026-04-06  |  **Artifacts**: 88  |  **Strategy**: progressive
**NL Score**: 88/100
**Security**: CLEAR
**Bugs**: 11  |  **Quality Issues**: 34  |  **Security Findings**: 5

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| documentation-generator/commands/documentation-generator.md | command | 61 | No allowed-tools, no steps, no output format, no input handling |
| commit/commands/commit.md | command | 65 | No allowed-tools, no steps, no output format |
| create-pr/commands/create-pr.md | command | 65 | No allowed-tools, no steps, no output format |
| bug-fix/commands/bug-fix.md | command | 65 | No allowed-tools, minimal body |
| debugger/agents/debugger.md | agent | 70 | No model, no examples, no output format |
| ship/commands/ship-deployment.md | command | 70 | No frontmatter (reference doc without registration) |
| ship/commands/ship-ci-review-loop.md | command | 70 | No frontmatter (reference doc without registration) |
| ship/commands/ship-error-handling.md | command | 70 | No frontmatter (reference doc without registration) |
| audit-project/commands/audit-project-agents.md | command | 70 | No frontmatter (reference doc without registration) |
| audit-project/commands/audit-project-github.md | command | 70 | No frontmatter (reference doc without registration) |
| agent-sdk-dev/agents/agent-sdk-verifier-ts.md | agent | 73 | No examples, no tools declared, vague language |
| agent-sdk-dev/agents/agent-sdk-verifier-py.md | agent | 73 | No examples, no tools declared, vague language |
| perf/agents/perf-theory-gatherer.md | agent | 75 | No examples, no output format in agent body |
| perf/agents/perf-code-paths.md | agent | 75 | No examples, minimal body (delegates to skill) |
| pr-review/commands/pr-review.md | command | 75 | No allowed-tools, no output format, no input handling |
| test-writer-fixer/agents/test-writer-fixer.md | agent | 82 | No tools field, no model |
| perf/agents/perf-orchestrator.md | agent | 83 | No examples |
| perf/agents/perf-theory-tester.md | agent | 85 | No examples |
| perf/agents/perf-analyzer.md | agent | 85 | No examples |
| perf/agents/perf-investigation-logger.md | agent | 85 | No examples |
| frontend-developer/agents/frontend-developer.md | agent | 85 | No model declared |
| backend-architect/agents/backend-architect.md | agent | 85 | No model declared |
| senior-frontend/skills/senior-frontend/SKILL.md | skill | 86 | No output format, vague terms |
| frontend-design/skills/frontend-design/SKILL.md | skill | 86 | No output format, vague terms |
| code-review/commands/code-review.md | command | 86 | No empty input handling, vague terms |
| agent-sdk-dev/commands/new-sdk-app.md | command | 87 | No allowed-tools, vague language |
| skill-bus/skills/add-sub/SKILL.md | skill | 90 | No output format (pure delegation) |
| skill-bus/skills/help/SKILL.md | skill | 90 | No output format (pure delegation) |
| skill-bus/skills/remove-sub/SKILL.md | skill | 90 | No output format (pure delegation) |
| skill-bus/hooks/hooks.json | hook | 90 | No description field |
| artifacts-builder/.claude-plugin/plugin.json | plugin | 90 | Missing version |
| changelog-generator/.claude-plugin/plugin.json | plugin | 90 | Missing version |
| mcp-builder/.claude-plugin/plugin.json | plugin | 90 | Missing version |
| theme-factory/.claude-plugin/plugin.json | plugin | 90 | Missing version |
| senior-frontend/.claude-plugin/plugin.json | plugin | 90 | Missing version |
| connect-apps/.claude-plugin/plugin.json | plugin | 90 | Missing version |
| frontend-design/.claude-plugin/plugin.json | plugin | 90 | Missing version |
| developer-growth-analysis/.claude-plugin/plugin.json | plugin | 90 | Missing version |
| canvas-design/.claude-plugin/plugin.json | plugin | 90 | Missing version |
| skill-bus/commands/report.md | command | 91 | No allowed-tools, minor vague terms |
| skill-bus/commands/onboard.md | command | 91 | No allowed-tools, minor vague terms |
| skill-bus/commands/add-sub.md | command | 91 | No allowed-tools, minor vague terms |
| ship/commands/ship.md | command | 92 | Minor vague terms |
| mcp-builder/skills/mcp-builder/SKILL.md | skill | 92 | Vague terms (comprehensive, well-designed) |
| audit-project/commands/audit-project.md | command | 94 | Minor vague terms |
| skill-bus/commands/pause-subs.md | command | 95 | No allowed-tools |
| skill-bus/commands/remove-sub.md | command | 95 | No allowed-tools |
| skill-bus/commands/list-subs.md | command | 95 | No allowed-tools |
| skill-bus/commands/help.md | command | 95 | No allowed-tools |
| skill-bus/commands/unpause-subs.md | command | 95 | No allowed-tools |
| skill-bus/commands/complete.md | command | 95 | No allowed-tools |
| skill-bus/commands/edit-insert.md | command | 95 | No allowed-tools |
| security-guidance/hooks/hooks.json | hook | 95 | — |
| code-review/.claude-plugin/plugin.json | plugin | 95 | — |
| pr-review/.claude-plugin/plugin.json | plugin | 95 | — |
| security-guidance/.claude-plugin/plugin.json | plugin | 95 | — |
| debugger/.claude-plugin/plugin.json | plugin | 95 | — |
| commit/.claude-plugin/plugin.json | plugin | 95 | — |
| frontend-developer/.claude-plugin/plugin.json | plugin | 95 | — |
| backend-architect/.claude-plugin/plugin.json | plugin | 95 | — |
| documentation-generator/.claude-plugin/plugin.json | plugin | 95 | — |
| create-pr/.claude-plugin/plugin.json | plugin | 95 | — |
| test-writer-fixer/.claude-plugin/plugin.json | plugin | 95 | — |
| agent-sdk-dev/.claude-plugin/plugin.json | plugin | 95 | — |
| bug-fix/.claude-plugin/plugin.json | plugin | 95 | — |
| artifacts-builder/skills/artifacts-builder/SKILL.md | skill | 96 | Minor vague terms |
| theme-factory/skills/theme-factory/SKILL.md | skill | 96 | Minor vague terms |
| canvas-design/skills/canvas-design/SKILL.md | skill | 96 | Minor vague terms |
| perf/commands/perf.md | command | 96 | Minor vague terms |
| developer-growth-analysis/skills/developer-growth-analysis/SKILL.md | skill | 98 | Minor vague terms |
| ship/.claude-plugin/plugin.json | plugin | 98 | — |
| perf/.claude-plugin/plugin.json | plugin | 98 | — |
| audit-project/.claude-plugin/plugin.json | plugin | 98 | — |
| skill-bus/.claude-plugin/plugin.json | plugin | 98 | — |
| changelog-generator/skills/changelog-generator/SKILL.md | skill | 100 | — |
| perf/skills/code-paths/SKILL.md | skill | 100 | — |
| perf/skills/investigation-logger/SKILL.md | skill | 100 | — |
| perf/skills/analyzer/SKILL.md | skill | 100 | — |
| perf/skills/theory/SKILL.md | skill | 100 | — |
| perf/skills/profile/SKILL.md | skill | 100 | — |
| perf/skills/theory-tester/SKILL.md | skill | 100 | — |
| perf/skills/benchmark/SKILL.md | skill | 100 | — |
| perf/skills/baseline/SKILL.md | skill | 100 | — |
| skill-bus/skills/pause-subs/SKILL.md | skill | 100 | — |
| skill-bus/skills/list-subs/SKILL.md | skill | 100 | — |
| skill-bus/skills/unpause-subs/SKILL.md | skill | 100 | — |
| skill-bus/skills/reflecting-on-sessions/SKILL.md | skill | 100 | — |
| connect-apps/commands/setup.md | command | 100 | — |

**Score breakdown by type** (NL artifacts only, 61 files):
- Agents (12): avg 80/100
- Commands (26): avg 84/100
- Skills (23): avg 97/100

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 2 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks (Python) | security-guidance/hooks/security_reminder_hook.py |
| Hooks (Bash) | skill-bus/hooks/dispatch.sh, pre-skill.sh, post-skill.sh, prompt-monitor.sh |
| MCP configs | None found |
| Package manifests | None found in repo root |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | security-guidance/hooks/security_reminder_hook.py | 14 | File write to /tmp | Debug log written to world-writable `/tmp/security-warnings-log.txt`. Any local user can read session-scoped warning history, potentially revealing file paths being edited. |
| 2 | Medium | connect-apps/commands/setup.md | 23 | API key in code string | API key is interpolated into a Python one-liner as `api_key='API_KEY_HERE'`. If the key contains a single-quote character, Python parsing fails. Unlikely in practice for Composio API keys but worth guarding with a proper subprocess arg. |
| 3 | Medium | skill-bus/hooks/prompt-monitor.sh | entire file | Broad hook — all prompts | The UserPromptSubmit hook fires on every user message. Even with a fast-path exit (~2ms), it processes all user input. This is inherent to the feature but broadens the attack surface if the Python dispatcher is ever compromised. |
| 4 | Low | skill-bus/hooks/dispatch.sh | 16 | CWD from JSON via grep/sed | CWD is extracted from hook JSON via `grep -o '...' | sed`. Malformed or crafted CWD values in the JSON could cause unexpected path behavior, though Python dispatcher performs its own validation. |
| 5 | Low | ship/commands/ship.md | ~350 | User-controlled strategy arg | `--strategy` value from `$ARGUMENTS` is interpolated directly into `gh pr merge $PR_NUMBER --$STRATEGY`. A crafted strategy like `squash --admin` could inject extra gh flags. In practice only Claude parses this arg, but the pattern is fragile. |

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | ship/commands/ship-deployment.md | No YAML frontmatter — file has no `description` or `allowed-tools` | Claude Code cannot register or describe this command; referenced sub-doc pattern works but breaks standalone invocation |
| 2 | ship/commands/ship-ci-review-loop.md | No YAML frontmatter — file starts with XML-like `<ci-review-loop>` tag | Same registration failure as ship-deployment.md |
| 3 | ship/commands/ship-error-handling.md | No YAML frontmatter | Same registration failure |
| 4 | audit-project/commands/audit-project-agents.md | No YAML frontmatter — starts with `# Phase 2: Multi-Agent Review - Reference` | Same registration failure |
| 5 | audit-project/commands/audit-project-github.md | No YAML frontmatter | Same registration failure |
| 6 | test-writer-fixer/agents/test-writer-fixer.md | No `tools` field in agent frontmatter (has `color: cyan` but no tools) | Agent has no declared tool budget; behavior is undefined across Claude Code versions |
| 7 | pr-review/commands/pr-review.md | No `allowed-tools` — command has no tool access declared | Cannot read git data or make API calls needed for a PR review |
| 8 | commit/commands/commit.md | No `allowed-tools` — needs at least `Bash(git:*)` to commit | Command body references git operations but declares no tool access |
| 9 | create-pr/commands/create-pr.md | No `allowed-tools` — needs Bash (git, gh, biome) | Cannot execute any of its described workflow steps |
| 10 | documentation-generator/commands/documentation-generator.md | No `allowed-tools` — needs at least `Read` and `Glob` | Cannot read source files to generate documentation |
| 11 | bug-fix/commands/bug-fix.md | No `allowed-tools` — needs Bash (git, gh) | Cannot create GitHub issue, checkout branch, commit, or push |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | security-guidance/hooks/security_reminder_hook.py | Debug log writes to world-writable `/tmp/security-warnings-log.txt` | Change `DEBUG_LOG_FILE` to write under `~/.claude/` (already used for state files), or disable the log by default and gate behind `SECURITY_REMINDER_DEBUG=1` env var |
| 2 | connect-apps/commands/setup.md | API key interpolated into Python one-liner string literal | Use `subprocess.run(['python3', '-c', code], env={**os.environ, 'COMPOSIO_KEY': key})` and read key from env var inside the Python snippet, or pass key as CLI argument to a dedicated helper script |
| 3 | ship/commands/ship.md | `--strategy` value used directly as `--$STRATEGY` flag | Validate STRATEGY against allowlist `["squash", "merge", "rebase"]` before use; reject anything else with a clear error |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | debugger/agents/debugger.md | No model declaration | -5 |
| 2 | debugger/agents/debugger.md | Zero example blocks | -15 |
| 3 | debugger/agents/debugger.md | No output format defined | -10 |
| 4 | perf/agents/perf-orchestrator.md | Zero example blocks | -15 |
| 5 | perf/agents/perf-orchestrator.md | Vague term: "meaningful improvement" | -2 |
| 6 | perf/agents/perf-theory-tester.md | Zero example blocks | -15 |
| 7 | perf/agents/perf-theory-gatherer.md | Zero example blocks | -15 |
| 8 | perf/agents/perf-theory-gatherer.md | No output format in agent body (delegates entirely to skill) | -10 |
| 9 | perf/agents/perf-analyzer.md | Zero example blocks | -15 |
| 10 | perf/agents/perf-code-paths.md | Zero example blocks | -15 |
| 11 | perf/agents/perf-code-paths.md | No output format in agent body | -10 |
| 12 | perf/agents/perf-investigation-logger.md | Zero example blocks | -15 |
| 13 | frontend-developer/agents/frontend-developer.md | No model declared | -5 |
| 14 | frontend-developer/agents/frontend-developer.md | No output format in agent body | -10 |
| 15 | backend-architect/agents/backend-architect.md | No model declared | -5 |
| 16 | backend-architect/agents/backend-architect.md | No output format in agent body | -10 |
| 17 | test-writer-fixer/agents/test-writer-fixer.md | No model declared | -5 |
| 18 | test-writer-fixer/agents/test-writer-fixer.md | No output format in agent body | -10 |
| 19 | agent-sdk-dev/agents/agent-sdk-verifier-ts.md | Zero example blocks | -15 |
| 20 | agent-sdk-dev/agents/agent-sdk-verifier-ts.md | No tools field declared | quality |
| 21 | agent-sdk-dev/agents/agent-sdk-verifier-ts.md | Vague terms: "reasonably current", "appropriate", "properly", "well-structured" | -8 |
| 22 | agent-sdk-dev/agents/agent-sdk-verifier-py.md | Zero example blocks | -15 |
| 23 | agent-sdk-dev/agents/agent-sdk-verifier-py.md | No tools field declared | quality |
| 24 | agent-sdk-dev/agents/agent-sdk-verifier-py.md | Vague terms: "reasonably current", "appropriate", "properly" | -8 |
| 25 | code-review/commands/code-review.md | No empty input handling (no recent changes case not addressed) | -10 |
| 26 | code-review/commands/code-review.md | Vague terms: "comprehensive", "appropriate" | -4 |
| 27 | pr-review/commands/pr-review.md | No output format | -10 |
| 28 | pr-review/commands/pr-review.md | No empty input handling | -10 |
| 29 | commit/commands/commit.md | No numbered execution steps (body is description only) | -10 |
| 30 | commit/commands/commit.md | No output format | -10 |
| 31 | commit/commands/commit.md | No empty input handling | -10 |
| 32 | create-pr/commands/create-pr.md | No numbered steps, no output format, no input handling | -30 |
| 33 | documentation-generator/commands/documentation-generator.md | No numbered steps, no output format, no input handling | -30 |
| 34 | bug-fix/commands/bug-fix.md | No output format, no input handling, minimal body | -25 |

## Cross-Component

**References verified:**
- `perf-orchestrator` → all 7 delegated agents/skills exist in the plugin ✓
- `ship.md` → ship-deployment.md, ship-ci-review-loop.md, ship-error-handling.md all exist ✓
- `audit-project.md` → audit-project-agents.md, audit-project-github.md both exist ✓
- `new-sdk-app.md` → agent-sdk-verifier-ts, agent-sdk-verifier-py agents both exist ✓
- `skill-bus` commands ↔ skills are mirror-paired correctly ✓

**Orphaned patterns:**
- `ship.md` references `Task({subagent_type: "next-task:ci-fixer", ...})` — the `ci-fixer` subagent type is not present in this plugin collection. It appears to be an external dependency from the `awesome-slash` ecosystem. Commands invoking it will silently fail if the environment lacks that agent.
- `perf-orchestrator` references `perf:perf-profiler`, `perf:perf-benchmarker`, `perf:perf-baseline-manager` skills — these correspond to skills named `perf-profiler`, `perf-benchmarker`, `perf-baseline-manager` in the `perf/skills/` directory (as `profile/SKILL.md`, `benchmark/SKILL.md`, `baseline/SKILL.md`). The skill names in frontmatter are `perf-profiler`, `perf-benchmarker`, `perf-baseline-manager` which match. ✓
- `perf` and `ship` plugins reference Node.js lib modules (`lib/perf/investigation-state.js`, `lib/ship/workflow-state.js`, `@awesome-slash/lib/cross-platform`) as `require()` calls. These runtime dependencies are not visible in the plugin markdown files and must be installed separately. If missing, all code-block phases in `perf.md` and `ship.md` would fail at runtime.

**Naming inconsistency:**
- `audit-project-agents.md` and `audit-project-github.md` reside in `commands/` but have no frontmatter. Claude Code may enumerate them as commands yet fail to register them properly. Adding minimal frontmatter with `description` and `allowed-tools: []` (or marking them as internal) would clarify intent.

**Architecture note:**
The repo is a heterogeneous collection from multiple authors (Composio, Anthropic employees, individual contributors) assembled under one namespace. This creates intentional variation in quality and style rather than a single coherent plugin — the perf/ship/audit-project suite from `avifenesh` is significantly more rigorous than the thin utility plugins (commit, create-pr, bug-fix) from other authors.

## Recommendation

CLEAR — submit PRs for all bugs and medium/low security fixes.

**Priority order:**
1. Add minimal frontmatter to the 5 reference command files (ship-deployment.md, ship-ci-review-loop.md, ship-error-handling.md, audit-project-agents.md, audit-project-github.md) — trivial one-liner fix per file.
2. Add `allowed-tools` to the 6 commands that are entirely missing it (pr-review, commit, create-pr, documentation-generator, bug-fix, agent-sdk-dev/new-sdk-app).
3. Add `tools` field to test-writer-fixer agent and the two agent-sdk-verifier agents.
4. Fix debug log path in security_reminder_hook.py (Medium security, easy fix).
5. Add strategy allowlist validation in ship.md (Low security, two lines of bash).
6. Add model declarations to debugger, frontend-developer, backend-architect, test-writer-fixer agents.
7. Add at least one example block to each perf agent — all have zero examples despite complex workflows.
