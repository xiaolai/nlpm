# NLPM Audit: kwakseongjae/oh-my-design
**Date**: 2026-04-06  |  **Artifacts**: 84  |  **Strategy**: progressive
**NL Score**: 86/100
**Security**: REVIEW
**Bugs**: 27  |  **Quality Issues**: 72  |  **Security Findings**: 5

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/omd-orchestrator.md | agent | 51 | Zero `<example>` blocks (-15) + 8 unused declared tools (-24) + broken ref `data/research/2026-05-18-agent-landscape.md` (dir doesn't exist) |
| .claude/agents/omd-orchestrator.md | agent | 51 | Same as canonical copy |
| .claude/agents/omd-master.md | agent | 64 | Deployed copy calls retired CLI commands `omd context --internal` / `omd init prepare --ref` (only `install-skills` exists) + zero examples (-15) + 7 unused tools (-21) |
| agents/omd-ux-writer.md | agent | 63 | Zero examples (-15) + 4 unused tools (-12) + Write/Edit declared on an explicitly advisory/read-only role (-10) |
| agents/omd-ux-engineer.md | agent | 63 | Zero examples (-15) + 4 unused tools (-12) + Write/Edit declared on an explicitly advisory/read-only role (-10) |
| agents/omd-asset-curator.md | agent | 67 | Zero examples (-15) + 6 unused declared tools (-18) |
| web/CLAUDE.md | memory | 70 | Missing build/run command (-10) + missing test command (-10) + missing architecture overview (-10) |
| agents/omd-kr-writer.md | agent | 73 | Zero examples (-15) + 4 unused tools (-12) + broken ref `data/research/2026-05-18-kr-style-presets.md` |
| .claude/agents/omd-kr-writer.md | agent | 73 | Same as canonical copy |
| .codex/skills/omd-remember/SKILL.md | skill | 76 | Entire "실행" section is `omd remember "<note>"` — command doesn't exist in shipped CLI (only `install-skills`) |
| agents/omd-locale-adapter.md | agent | 76 | Zero examples (-15) + 3 unused tools (-9) |
| .claude/agents/omd-locale-adapter.md | agent | 76 | Same as canonical copy |
| agents/omd-designer-review.md | agent | 76 | Zero examples (-15) + 3 unused tools (-9) + Write called in body but not declared in tools |
| .claude/agents/omd-designer-review.md | agent | 76 | Same as canonical copy |
| agents/omd-master.md | agent | 76 | Zero examples (-15) + 3 unused tools (-9) |
| agents/omd-codex-image.md | agent | 76 | Zero examples (-15) + 3 unused tools (-9) |
| .claude/agents/omd-codex-image.md | agent | 76 | Same as canonical copy |
| agents/omd-ui-junior.md | agent | 76 | Zero examples (-15) + 3 unused declared tools (-9) |
| .claude/agents/omd-ui-junior.md | agent | 76 | Same as canonical copy |
| agents/omd-final-qa.md | agent | 76 | Zero examples (-15) + 3 unused tools (-9) + Write called in body but not declared in tools |
| .claude/agents/omd-final-qa.md | agent | 76 | Same as canonical copy |
| .codex/skills/omd-harness/SKILL.md | skill | 77 | Bootstrap step runs `omd harness "<task>" --internal` — nonexistent CLI invocation |
| .codex/skills/omd-init/SKILL.md | skill | 78 | Phases 2/4 call `omd init recommend`/`omd init prepare --ref` — neither exists in shipped CLI |
| .agents/skills/omd-design/SKILL.md | skill | 85 | Hardcodes author's personal machine path `cd /Users/kwakseongjae/Desktop/projects/oh-my-design` |
| .claude/skills/omd-lab-02-design-harness/SKILL.md | skill | 85 | References `playbooks/v1.md` as an existing baseline — no `playbooks/` dir exists |
| .claude/skills/omd-kr-writer/SKILL.md | skill | 85 | Broken ref `data/research/2026-05-18-kr-style-presets.md` — dir doesn't exist |
| .claude/skills/omd-orchestrator/SKILL.md | skill | 85 | Broken ref `data/research/2026-05-18-agent-landscape.md` — dir doesn't exist |
| agents/AGENT.md | doc (compact context card) | 85 | Broken refs: `research/harness-design/{06-omd-integration-design,07-poc-spec,docs-todo}.md` — no `research/` dir exists anywhere in the repo |
| skills/omd-lab-02-design-harness/SKILL.md | skill | 81 | References nonexistent CLI `omd harness --lab v2` / `omd lab compare` |
| .codex/skills/omd-lab-02-design-harness/SKILL.md | skill | 81 | Same nonexistent CLI surface as above |
| .codex/skills/omd-sync/SKILL.md | skill | 80 | Entire skill built on `omd sync`/`--force`/`--check` — none exist in shipped CLI |
| .codex/skills/omd-learn/SKILL.md | skill | 80 | Entire skill built on `omd learn`/`--mark-applied`/`--mark-rejected` — none exist |
| .codex/skills/omd-apply/SKILL.md | skill | 85 | Self-report phase calls `omd remember "..." --context "..."` — nonexistent command |
| skills/omd-harness/SKILL.md | skill | 89 | 4 vague quantifiers (-8) + 727 lines (R05 length note) |
| skills/omd-kr-writer/SKILL.md | skill | 90 | 5 vague quantifiers (-10) |
| skills/claude-design/SKILL.md | skill | 90 | 5 vague quantifiers (-10) |
| skills/omd-apply/SKILL.md | skill | 90 | Dispatch table's "omd-add-reference" alternate target is a dev-repo-only skill (`.claude/skills/omd-add-reference`) never installed by `install-skills` for npm end users (-8) + 1 vague quantifier |
| .agents/skills/omd-add-reference/SKILL.md | skill | 90 | Two unreconciled SYNC procedures described for the same step (manual vs. registry-driven) |
| .claude/skills/omd-add-reference/SKILL.md | skill | 90 | Same SYNC-procedure duplication as `.agents` copy |
| skills/omd-reference-capture/SKILL.md | skill | 91 | 3 vague quantifiers (-6) + 723 lines (R05 length note) |
| .claude/skills/omd-codex-image/SKILL.md | skill | 92 | Cross-references sibling skill `omd-reference-capture`, which only exists under `skills/`, not under `.claude/skills/` where this file lives |
| .claude/skills/omd-final-qa/SKILL.md | skill | 92 | Frontmatter says "8-item rubric", body header says "(9 items)"; only 8 are ever listed |
| skills/omd-final-qa/SKILL.md | skill | 96 | 2 vague quantifiers (-4) |
| skills/omd-init/SKILL.md | skill | 98 | 1 vague quantifier (-2) |
| skills/omd-learn/SKILL.md | skill | 98 | 1 vague quantifier (-2) |
| skills/omd-orchestrator/SKILL.md | skill | 98 | 1 vague quantifier (-2) |
| skills/omd-asset-fetch/SKILL.md | skill | 98 | 1 vague quantifier (-2) |
| skills/omd-designer-review/SKILL.md | skill | 98 | 1 vague quantifier (-2) |
| .agents/skills/google-analytics/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| agents/omd-persona-tester.md | agent | 82 | Zero examples (-15) + WebFetch unused (-3) + `mcp__playwright__*` called in body but not declared in tools |
| .claude/agents/omd-persona-tester.md | agent | 82 | Same as canonical copy |
| agents/omd-microcopy.md | agent | 82 | Zero examples (-15) + Edit unused (-3) |
| .claude/agents/omd-microcopy.md | agent | 82 | Same as canonical copy |
| agents/omd-critic.md | agent | 79 | Zero examples (-15) + 2 unused tools (-6) |
| .claude/agents/omd-critic.md | agent | 79 | Deployed copy is missing the "Anti-platitude audit" and "Anti-engineering-pivot audit" sections present in the canonical copy (verified: both section headers exist only in `agents/omd-critic.md` lines 126/138, absent from `.claude/agents/omd-critic.md`) |
| agents/omd-a11y-auditor.md | agent | 79 | Zero examples (-15) + 2 unused tools (-6) |
| .claude/agents/omd-a11y-auditor.md | agent | 79 | Same as canonical copy |
| agents/omd-ux-researcher.md | agent | 79 | Zero examples (-15) + 2 unused tools (-6) |
| .claude/agents/omd-ux-researcher.md | agent | 79 | Same as canonical copy |
| .claude/agents/omd-asset-curator.md | agent | 79 | Deployed copy is a completely different, stale implementation (English/Pinterest-brief workflow, missing Edit+Agent tools) vs. canonical (Korean/SVG-first/OMD-STACK workflow) — verified via diff of frontmatter + body |
| .agents/skills/omd-token-backfill/SKILL.md | skill | 100 | none found |
| skills/omd-remember/SKILL.md | skill | 100 | none found |
| skills/omd-codex-image/SKILL.md | skill | 100 | none found |
| skills/omd-experiment-gallery/SKILL.md | skill | 100 | none found |
| skills/omd-taste/SKILL.md | skill | 100 | none found |
| skills/omd-locale-adapter/SKILL.md | skill | 100 | none found |
| skills/omd-sync/SKILL.md | skill | 100 | none found |
| skills/omd-feel/SKILL.md | skill | 100 | none found |
| .claude/skills/omd/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-init/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-learn/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-release-hygiene/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-lab-01-designmd-impact/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-remember/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-migrate/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-token-backfill/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-harness/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-locale-adapter/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-batch-launch/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-sync/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-feel/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-apply/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-component-harvest/SKILL.md | skill | 100 | none found |
| .claude/skills/omd-designer-review/SKILL.md | skill | 100 | none found |

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 2 |

Note on the pre-scan's "High pattern matches: 1": this corresponds to `scripts/postinstall.cjs` being registered as an npm `postinstall` lifecycle script — categorically HIGH-risk by pattern class. On full read, its content only prints a colorized console message and is explicitly gated to skip under `CI`, `NODE_ENV=production`, or nested/sub-dependency installs; it performs no network calls, no file writes, and no package installs. It is not counted as a finding below.

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Scripts | `scripts/check-release-hygiene.sh`, `skills/claude-design/scripts/gather_references.py`, `skills/claude-design/scripts/clickable_link.sh`, `skills/claude-design/scripts/collect_source.py`, `skills/claude-design/scripts/analyze_codebase.py`, `.agents/skills/google-analytics/scripts/ga_client.py`, `.agents/skills/google-analytics/scripts/analyze.py` |
| Hooks (wired into `.claude/settings.json`, outside the strict pre-scan glob but a live execution surface) | `.claude/hooks/post-edit-watch.cjs` (PostToolUse), `.claude/hooks/session-state-loader.cjs` (SessionStart), `.claude/hooks/skill-activation.cjs` (UserPromptSubmit), `.claude/hooks/session-end-foldin.cjs` (Stop), `.claude/hooks/lib/preferences-parser.cjs`, `.claude/hooks/lib/preferences-writer.cjs` |
| Node lifecycle/build scripts | `scripts/postinstall.cjs` (npm `postinstall`), `scripts/context.cjs`, `scripts/ctx-prime.cjs`, `scripts/gen-llms-full.cjs` (npm `prepublishOnly` chain) |
| MCP configs | `.mcp.json` (1 server: `playwright`, stdio, `npx @playwright/mcp@latest`) |
| Package manifests | `package.json` (no `requirements.txt` present) |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | .mcp.json | 3-10 | broad-mcp-permissions | The `playwright` MCP server is declared with empty `env` and no scoping flags (no allowed-origins/headless/sandbox restriction) — full browser automation (navigate, click, read page content, screenshot) is available with no restriction on destination sites. |
| 2 | Medium | .agents/skills/google-analytics/scripts/ga_client.py | 50, 57-58 | credential-env-read | Reads `GOOGLE_ANALYTICS_PROPERTY_ID` and `GOOGLE_APPLICATION_CREDENTIALS` (a path to a service-account JSON key) from the environment to construct the official `BetaAnalyticsDataClient`; no export/exfiltration of the secret value observed — local use only. |
| 3 | Medium | .agents/skills/google-analytics/scripts/ga_client.py | 144 | network-call | `self.client.run_report(request)` makes an outbound HTTPS call via Google's official `google-analytics-data` SDK to the GA4 Data API — legitimate use, flagged per the network-call category for completeness. |
| 4 | Low | .mcp.json | 7 | unpinned-latest-tag | `npx @playwright/mcp@latest` has no version pin; `npx` fetches/executes whatever is currently published under `latest` at MCP-server startup. |
| 5 | Low | package.json | 77-85 | unpinned-semver | All `dependencies`/`devDependencies` use caret ranges (`@clack/prompts ^0.9.1`, `commander ^13.1.0`, `picocolors ^1.1.1`, `@types/node ^22.13.10`, `tsup ^8.4.0`, `typescript ^5.8.2`, `vitest ^3.1.1`) rather than exact pins. |

No `shell=True`/`shell: true`, `os.system`/`exec()`, `sudo`, PATH mutation, curl-pipe-to-shell, eval-on-variable, or unsanitized argument interpolation into shell commands were found anywhere in scope. `skills/claude-design/scripts/analyze_codebase.py`'s `subprocess.run(["git", "-C", root] + args, ...)` uses list-form argv with no shell and internally constructed args — not exploitable, not flagged. No `commands/*.md` directory exists in this repo, so the argument-interpolation check does not apply.

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | agents/omd-orchestrator.md | Boot step requires reading `data/research/2026-05-18-agent-landscape.md`; no `data/research/` directory exists anywhere in the repo (verified) | Boot sequence fails before the routing decision tree can be applied |
| 2 | .claude/agents/omd-orchestrator.md | Same broken reference as canonical copy | Same as above — this is the copy Claude Code actually loads |
| 3 | .claude/skills/omd-orchestrator/SKILL.md | Same `data/research/2026-05-18-agent-landscape.md` broken reference, in the skill-side copy | Cited orchestrator-pattern justification is unavailable to anyone reading the skill |
| 4 | agents/omd-kr-writer.md | Boot step requires reading `data/research/2026-05-18-kr-style-presets.md` for 11 of 12 writing presets; directory doesn't exist (verified) | Every invocation hits a Read failure before any preset other than the inlined default can be applied |
| 5 | .claude/agents/omd-kr-writer.md | Same broken reference as canonical copy | Same as above — this is the copy Claude Code actually loads |
| 6 | .claude/skills/omd-kr-writer/SKILL.md | Same `data/research/2026-05-18-kr-style-presets.md` broken reference, in the skill-side copy | Cited 9-field spec + verbatim examples are unavailable for 11 of 12 presets |
| 7 | agents/AGENT.md | "Where to look when stuck" points to `research/harness-design/06-omd-integration-design.md`, `07-poc-spec.md`, and `docs-todo.md` — no `research/` directory exists anywhere in the repo (verified) | Anyone or any agent following this pointer hits three consecutive dead links |
| 8 | agents/omd-final-qa.md | Body instructs writing to `<work_dir>/.reviews/final-qa-round-<N>.md`, but frontmatter `tools:` is `Read, Glob, Grep, Bash` — Write is not declared | The QA report cannot be persisted, breaking the 2-round revision cap the orchestrator depends on |
| 9 | .claude/agents/omd-final-qa.md | Same undeclared-Write bug as canonical copy | Same as above — this is the copy Claude Code actually loads |
| 10 | agents/omd-designer-review.md | Body instructs writing to `<work_dir>/.reviews/designer-review-round-<N>.md`, but `tools:` is `Read, Glob, Grep, Bash` — Write not declared | Brand-consistency review reports can fail to save, breaking PASS/REVISION/BLOCK round-tracking |
| 11 | .claude/agents/omd-designer-review.md | Same undeclared-Write bug as canonical copy | Same as above — this is the copy Claude Code actually loads |
| 12 | agents/omd-persona-tester.md | Body calls `mcp__playwright__browser_navigate`/`browser_snapshot`/`browser_click`; none are declared in `tools:` (`Read, Bash, WebFetch, Write`) | The higher-fidelity Playwright walkthrough path can't invoke these MCP tools; agent is forced into a less-reliable text-simulation fallback |
| 13 | .claude/agents/omd-persona-tester.md | Same undeclared `mcp__playwright__*` tools bug | Same as above — this is the copy Claude Code actually loads |
| 14 | .claude/agents/omd-master.md | Calls retired CLI commands `omd context --internal` and `omd init prepare --ref <id> ... --json` (verified against `bin/oh-my-design.ts`: only `install-skills` is registered) | The deployed conversational orchestrator's Phase 5 (`DESIGN.md.patch` generation) invokes commands that don't exist and will fail at runtime |
| 15 | .claude/agents/omd-critic.md | Missing the "Anti-platitude audit" and "Anti-engineering-pivot audit" sections present in canonical `agents/omd-critic.md` (verified: headers exist only at canonical lines 126/138) | The deployed critic won't flag platitudes ("완벽", "Looks great!") or forbidden engineering-pivot proposals (localStorage, Next.js migration, backend/API) — a guardrail documented in source but absent from what actually runs |
| 16 | .claude/agents/omd-asset-curator.md | Deployed copy is an entirely different, stale implementation vs. canonical (verified: description/tools/body diverge completely — English Pinterest-brief workflow with `Read, Write, WebSearch, WebFetch, Bash, Glob` vs. canonical Korean SVG-first/OMD-STACK workflow with `Read, Write, Edit, WebSearch, WebFetch, Bash, Glob, Grep, Agent`) | Real Claude Code sessions get the old stock-photo/Pinterest-first asset behavior instead of the current SVG-first design the rest of the repo documents |
| 17 | .codex/skills/omd-init/SKILL.md | Phases 2/4 call `omd init recommend "<description>" --json` and `omd init prepare --ref <id> ... --json`; shipped CLI (`bin/oh-my-design.ts`) registers only `install-skills` (verified) | Any Codex-channel user hits command-not-found at Phase 2; the entire DESIGN.md bootstrap flow fails |
| 18 | .codex/skills/omd-learn/SKILL.md | Entire skill built on `omd learn`, `omd learn --mark-applied`, `omd learn --mark-rejected`; none exist in the CLI | Preference fold-in is non-functional on Codex |
| 19 | .codex/skills/omd-remember/SKILL.md | Sole action is `omd remember "<note>" [--scope] [--context] [--agent]`; command doesn't exist | Preference logging never happens on Codex; every "remember this" request silently no-ops |
| 20 | .codex/skills/omd-harness/SKILL.md | Bootstrap step runs `omd harness "<task>" --internal`, described as a hidden helper returning JSON; command doesn't exist | The harness can never bootstrap a run directory on Codex, blocking the entire design-pipeline entry point |
| 21 | .codex/skills/omd-sync/SKILL.md | Entire skill is `omd sync`/`--force`/`--check`; none exist | Shim files (CLAUDE.md/AGENTS.md/.cursor rule) can never be created or drift-checked via this skill on Codex |
| 22 | .codex/skills/omd-apply/SKILL.md | Self-report phase calls `omd remember "..." --context "..."`; nonexistent command | Corrections a user makes during UI work are silently never logged |
| 23 | skills/omd-lab-02-design-harness/SKILL.md | References `omd harness "<task>" --lab v2` and `omd lab compare --task <slug> --versions v1,v2`; neither subcommand/flag exists in the shipped CLI | The lab's entire comparison workflow cannot run |
| 24 | .codex/skills/omd-lab-02-design-harness/SKILL.md | Same nonexistent `--lab`/`lab compare` CLI surface as the `skills/` copy | Same as above, on the Codex channel |
| 25 | skills/omd-apply/SKILL.md | Dispatch table offers "omd-init (또는 omd-add-reference)" as an alternate handler; `omd-add-reference` exists only as `.claude/skills/omd-add-reference` / `.agents/skills/omd-add-reference` (dev-repo-only — confirmed absent from the npm `files` manifest and from `install-skills`' source directory, which reads only from the package's `skills/` folder) | An end user who installed via `npm`/`npx` and reaches this dispatch branch has no matching subagent/skill installed — the reference is accurate for repo maintainers but broken for the CLI's actual distributed audience |
| 26 | .agents/skills/omd-design/SKILL.md | Step 2 hardcodes `cd /Users/kwakseongjae/Desktop/projects/oh-my-design` — the original author's personal machine path | Any user other than the author hits a nonexistent directory and the DESIGN.md generation step fails outright |
| 27 | .claude/skills/omd-lab-02-design-harness/SKILL.md | Describes `playbooks/v1.md` as the current active baseline; no `playbooks/` directory exists under this skill folder (only `SKILL.md` is present) | An agent invoking this skill to compare against the "v1 baseline" has no baseline file to read or diff against |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | .mcp.json | `playwright` MCP server has no scoping/permission restrictions | Add `--headless`/allowed-origin restrictions or document why unrestricted browsing is required for the design-reference workflow |
| 2 | .mcp.json | `npx @playwright/mcp@latest` is unpinned | Pin to an exact published version (e.g. `@playwright/mcp@0.x.y`) to avoid silently picking up breaking changes on every invocation |
| 3 | package.json | All dependencies use caret (`^`) ranges | Consider exact pins or a committed lockfile policy note for a CLI that's installed via `npx`/global install, where an unreviewed transitive bump ships straight to users |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/omd-ui-junior.md | Zero `<example>` blocks | -15 |
| 2 | agents/omd-ui-junior.md | 3 unused declared tools (Edit, Glob, Bash) | -9 |
| 3 | .claude/agents/omd-ui-junior.md | Zero `<example>` blocks | -15 |
| 4 | .claude/agents/omd-ui-junior.md | 3 unused declared tools (Edit, Glob, Bash) | -9 |
| 5 | agents/omd-final-qa.md | Zero `<example>` blocks | -15 |
| 6 | agents/omd-final-qa.md | 3 unused declared tools (Glob, Grep, Bash) | -9 |
| 7 | .claude/agents/omd-final-qa.md | Zero `<example>` blocks + 3 unused tools | -24 |
| 8 | agents/omd-persona-tester.md | Zero `<example>` blocks | -15 |
| 9 | agents/omd-persona-tester.md | WebFetch declared but unused (Bash/curl used instead) | -3 |
| 10 | .claude/agents/omd-persona-tester.md | Zero `<example>` blocks + WebFetch unused | -18 |
| 11 | agents/omd-kr-writer.md | Zero `<example>` blocks | -15 |
| 12 | agents/omd-kr-writer.md | 4 unused declared tools (Edit, Glob, Grep, Bash) | -12 |
| 13 | .claude/agents/omd-kr-writer.md | Zero `<example>` blocks + 4 unused tools | -27 |
| 14 | agents/omd-ux-writer.md | Zero `<example>` blocks | -15 |
| 15 | agents/omd-ux-writer.md | 4 unused declared tools (Edit, WebFetch, Grep, Glob) | -12 |
| 16 | agents/omd-ux-writer.md | Write+Edit declared on an explicitly advisory role ("생성이 아니라 평가", "최종본으로 emit 금지") | -10 |
| 17 | agents/omd-ux-researcher.md | Zero `<example>` blocks | -15 |
| 18 | agents/omd-ux-researcher.md | 2 unused declared tools (Bash, Grep) | -6 |
| 19 | .claude/agents/omd-ux-researcher.md | Zero `<example>` blocks + 2 unused tools | -21 |
| 20 | agents/AGENT.md | No output-format section; not written as a subagent registration file (no `name`/`description` frontmatter expected — see note below) | 0 (see note) |
| 21 | agents/omd-orchestrator.md | Zero `<example>` blocks | -15 |
| 22 | agents/omd-orchestrator.md | No output-format section | -10 |
| 23 | agents/omd-orchestrator.md | 8 unused declared tools (Write, Edit, Bash, Glob, Grep, TaskCreate, TaskUpdate, TaskList — only Read+Agent used) | -24 |
| 24 | .claude/agents/omd-orchestrator.md | Same 3 issues as canonical copy | -49 |
| 25 | agents/omd-asset-curator.md | Zero `<example>` blocks | -15 |
| 26 | agents/omd-asset-curator.md | 6 unused declared tools (Edit, WebSearch, Bash, Glob, Grep, Agent) | -18 |
| 27 | agents/omd-asset-curator.md | Description promises a "(c) 3D subagent routing" branch; body's Step 3 only implements A/B/C=chart branches, no 3D/Agent path exists | informational |
| 28 | .claude/agents/omd-asset-curator.md | Zero `<example>` blocks + 2 unused tools (Bash, Glob) | -21 |
| 29 | agents/omd-microcopy.md | Zero `<example>` blocks | -15 |
| 30 | agents/omd-microcopy.md | Edit declared but unused | -3 |
| 31 | .claude/agents/omd-microcopy.md | Zero `<example>` blocks + Edit unused | -18 |
| 32 | agents/omd-locale-adapter.md | Zero `<example>` blocks | -15 |
| 33 | agents/omd-locale-adapter.md | 3 unused declared tools (Edit, Glob, Grep) | -9 |
| 34 | .claude/agents/omd-locale-adapter.md | Zero `<example>` blocks + 3 unused tools | -24 |
| 35 | agents/omd-critic.md | Zero `<example>` blocks | -15 |
| 36 | agents/omd-critic.md | 2 unused declared tools (Glob, Grep) | -6 |
| 37 | .claude/agents/omd-critic.md | Zero `<example>` blocks + 2 unused tools | -21 |
| 38 | agents/omd-a11y-auditor.md | Zero `<example>` blocks | -15 |
| 39 | agents/omd-a11y-auditor.md | 2 unused declared tools (Glob, WebFetch — URL check uses Bash/curl instead) | -6 |
| 40 | .claude/agents/omd-a11y-auditor.md | Zero `<example>` blocks + 2 unused tools | -21 |
| 41 | agents/omd-ux-engineer.md | Zero `<example>` blocks | -15 |
| 42 | agents/omd-ux-engineer.md | 4 unused declared tools (Edit, Grep, Glob, Bash) | -12 |
| 43 | agents/omd-ux-engineer.md | Write+Edit declared on an explicitly advisory role ("새 component를 최종본으로 emit 금지") | -10 |
| 44 | agents/omd-designer-review.md | Zero `<example>` blocks | -15 |
| 45 | agents/omd-designer-review.md | 3 unused declared tools (Glob, Grep, Bash) | -9 |
| 46 | .claude/agents/omd-designer-review.md | Same 2 issues as canonical copy | -24 |
| 47 | agents/omd-master.md | Zero `<example>` blocks | -15 |
| 48 | agents/omd-master.md | 3 unused declared tools (TaskCreate, TaskUpdate, TaskList) | -9 |
| 49 | .claude/agents/omd-master.md | Zero `<example>` blocks + 7 unused tools (Edit, Glob, Grep, TaskCreate, TaskUpdate, TaskList, WebFetch) | -36 |
| 50 | agents/omd-codex-image.md | Zero `<example>` blocks | -15 |
| 51 | agents/omd-codex-image.md | 3 unused declared tools (Glob, Grep, Bash) | -9 |
| 52 | .claude/agents/omd-codex-image.md | Same 2 issues as canonical copy | -24 |
| 53 | skills/omd-harness/SKILL.md | 4 vague quantifiers | -8 |
| 54 | skills/omd-harness/SKILL.md | 727 lines (R05 length note — advisory, no PR needed) | 0 |
| 55 | skills/omd-kr-writer/SKILL.md | 5 vague quantifiers | -10 |
| 56 | skills/claude-design/SKILL.md | 5 vague quantifiers | -10 |
| 57 | skills/omd-apply/SKILL.md | 1 vague quantifier | -2 |
| 58 | .agents/skills/omd-add-reference/SKILL.md | Two unreconciled SYNC procedures (manual "SYNC 모드" vs. later registry-driven "Phase 5 — SYNC") describing different mechanisms for the same step | -10 |
| 59 | .claude/skills/omd-add-reference/SKILL.md | Same SYNC-procedure duplication as `.agents` copy | -10 |
| 60 | .claude/skills/omd-codex-image/SKILL.md | Cross-references sibling skill `omd-reference-capture`, which exists only under `skills/`, not under `.claude/skills/` (this file's own loadable directory) | -8 |
| 61 | .claude/skills/omd-final-qa/SKILL.md | Frontmatter says "8-item rubric"; body header claims "(9 items, 모두 closed checklist)"; only 8 items are ever listed, and a footnote admits a spelling-check item is explicitly not automated | -8 |
| 62 | skills/omd-final-qa/SKILL.md | 2 vague quantifiers | -4 |
| 63 | skills/omd-init/SKILL.md | 1 vague quantifier | -2 |
| 64 | skills/omd-learn/SKILL.md | 1 vague quantifier | -2 |
| 65 | skills/omd-orchestrator/SKILL.md | 1 vague quantifier | -2 |
| 66 | skills/omd-asset-fetch/SKILL.md | 1 vague quantifier | -2 |
| 67 | skills/omd-designer-review/SKILL.md | 1 vague quantifier | -2 |
| 68 | .agents/skills/google-analytics/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 69 | .codex/skills/omd-harness/SKILL.md | Hardcodes `.claude/data/reference-fingerprints.json` instead of its own channel's `.codex/data/reference-fingerprints.json` (which exists and is correct) | informational, cross-component |
| 70 | web/CLAUDE.md | Missing build/run command | -10 |
| 71 | web/CLAUDE.md | Missing test command | -10 |
| 72 | web/CLAUDE.md | Missing architecture overview (file is a one-line `@AGENTS.md` import; target `web/AGENTS.md` only directs the reader to `node_modules/next/dist/docs/`, unverifiable without a full install) | -10 |

## Cross-Component

- **Systemic broken reference to `data/research/`**: six files across two channels (`agents/omd-kr-writer.md`, `.claude/agents/omd-kr-writer.md`, `.claude/skills/omd-kr-writer/SKILL.md`, `agents/omd-orchestrator.md`, `.claude/agents/omd-orchestrator.md`, `.claude/skills/omd-orchestrator/SKILL.md`) cite specific files under a `data/research/` directory that does not exist anywhere in the repo (`data/` contains only `issues/`, `architecture-proposals/`, `reference-audits/`, verified). This reads as a directory that was planned or existed at authoring time and was later removed or never committed, with every consumer left pointing at it.
- **Canonical-vs-deployed drift**: `agents/AGENT.md` documents `agents/` as the canonical source that "generates" `.claude/agents/` (and `.codex/agents/`), but 3 of the 14 paired files have silently drifted: `omd-asset-curator` (deployed copy is a wholly different, older Pinterest-brief design), `omd-critic` (deployed copy is missing two mandatory audit sections), and `omd-master` (deployed copy is ~240 lines shorter and calls retired CLI commands). Since `.claude/agents/*.md` is what Claude Code actually loads at runtime, these are the versions in effect for real users — not the more complete canonical sources the rest of the repo's docs assume are active.
- **CLI/skill contract drift by channel**: the shipped CLI (`bin/oh-my-design.ts`) registers exactly one subcommand, `install-skills`, and its own `--description` states "no other CLI commands." The `skills/` (Claude Code) tree was migrated off CLI calls accordingly, but the entire `.codex/skills/` tree (7/7 files) plus `skills/omd-lab-02-design-harness/SKILL.md` still instruct the agent to shell out to `omd init`, `omd learn`, `omd remember`, `omd sync`, and `omd harness --lab` subcommands that no longer exist — a full channel (Codex CLI) is left non-functional relative to the Claude Code channel it was ported from.
- **Dev-only component referenced from a shipped skill**: `omd-add-reference` genuinely exists (`.claude/skills/omd-add-reference/SKILL.md`, `.agents/skills/omd-add-reference/SKILL.md`) but only in the dev repo — `install-skills` sources exclusively from the package's `skills/` directory (verified in `src/cli/install-skills.ts`), and `omd-add-reference` is absent from both `skills/` and the npm `files` manifest in `package.json`. `skills/omd-reference-capture/SKILL.md` correctly documents this dev-repo-only scoping. However `skills/omd-apply/SKILL.md` — itself one of the shipped, installable skills — still lists `omd-add-reference` as a live dispatch target, which is unreachable for anyone who installed via `npm`/`npx` rather than working in this source checkout.

## Recommendation

**REVIEW** — submit NL bug-fix PRs for the 28 items above (the `data/research/` broken references, the CLI/skill drift in `.codex/skills/`, the undeclared-tool/MCP-tool bugs, and the canonical-vs-deployed agent drift are all concrete, PR-worthy fixes), and separately flag the 3 Medium/Low security findings (unscoped MCP permissions, unpinned Playwright MCP version, unpinned npm dependency ranges) in an issue rather than a PR, since they are hardening suggestions rather than exploitable vulnerabilities. No Critical/High security findings were confirmed — the pre-scan's single High hit resolved to a benign, explicitly-gated `postinstall` script on manual review.
