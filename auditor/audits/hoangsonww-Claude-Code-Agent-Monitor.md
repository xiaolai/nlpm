# NLPM Audit: hoangsonww/Claude-Code-Agent-Monitor
**Date**: 2026-04-06  |  **Artifacts**: 126  |  **Strategy**: progressive
**NL Score**: 72/100
**Security**: REVIEW
**Bugs**: 56  |  **Quality Issues**: 158  |  **Security Findings**: 6

100 NL artifacts were scored directly (17 agents, 30 commands, 53 skills). Two systemic, repo-wide patterns dominate the result: **every one of the 53 `SKILL.md` files omits the required `name` frontmatter field** (open SKILL.md spec, -25 each), and **every one of the 30 commands omits `allowed-tools`** despite invoking `Bash`/`curl` in their bodies (-5 each). Both are single mechanical fixes applied repo-wide, not 83 independent design problems.

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| plugins/ccam-devtools/skills/health-check/SKILL.md | skill | 56 | Missing required frontmatter field: name (-25) |
| plugins/ccam-dashboard/skills/live-watch/SKILL.md | skill | 58 | Missing required frontmatter field: name (-25) |
| plugins/ccam-dashboard/skills/endpoint-probe/SKILL.md | skill | 58 | Missing required frontmatter field: name (-25) |
| plugins/ccam-devtools/skills/data-export/SKILL.md | skill | 58 | Missing required frontmatter field: name (-25) |
| plugins/ccam-cost-guard/skills/daily-budget-check/SKILL.md | skill | 58 | Missing required frontmatter field: name (-25) |
| plugins/ccam-analytics/skills/productivity-score/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-analytics/skills/usage-trends/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-analytics/skills/cost-breakdown/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-analytics/skills/model-mix/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-analytics/skills/session-report/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-analytics/skills/cache-efficiency/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-dashboard/skills/quick-stats/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-dashboard/skills/dashboard-status/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-devtools/skills/hook-diagnostics/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-devtools/skills/transcript-grep/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-devtools/skills/event-trace/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-devtools/skills/session-debug/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-insights/skills/anomaly-alert/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-insights/skills/session-compare/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-insights/skills/pattern-detect/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-insights/skills/regression-watch/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-insights/skills/benchmark/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-insights/skills/optimization-suggest/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-quality/skills/hook-failure-audit/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-quality/skills/api-error-report/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-quality/skills/error-scan/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-quality/skills/slo-check/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-quality/skills/regression-alert/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-productivity/skills/time-of-day/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-productivity/skills/weekly-report/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-productivity/skills/sprint-summary/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-productivity/skills/monthly-review/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-productivity/skills/daily-standup/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-productivity/skills/workflow-optimizer/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-workflows/skills/concurrency-report/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-workflows/skills/fleet-runs/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-workflows/skills/delegation-audit/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-workflows/skills/dag-map/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-workflows/skills/error-propagation/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-config/skills/mcp-audit/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-config/skills/memory-review/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-config/skills/skill-inventory/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-config/skills/hook-inventory/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-config/skills/config-audit/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-sessions/skills/session-timeline/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-sessions/skills/session-cleanup/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-sessions/skills/cwd-rollup/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-sessions/skills/transcript-replay/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-sessions/skills/session-search/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-cost-guard/skills/budget-set/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-cost-guard/skills/spend-forecast/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-cost-guard/skills/cost-alert/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-cost-guard/skills/model-savings/SKILL.md | skill | 60 | Missing required frontmatter field: name (-25) |
| plugins/ccam-productivity/agents/productivity-coach.md | agent | 66 | No `<example>` blocks (-15) + missing Output Standards section (-10) + 3 unused declared tools (-9) |
| plugins/ccam-dashboard/agents/dashboard-operator.md | agent | 67 | Broken reference to non-existent scripts/self-update-restart.js |
| .claude/agents/frontend-reviewer.md | agent | 73 | No `<example>` blocks (-15) + all 4 declared tools unused in body (-12) |
| .claude/agents/backend-reviewer.md | agent | 73 | No `<example>` blocks (-15) + all 4 declared tools unused in body (-12) |
| .claude/agents/mcp-reviewer.md | agent | 73 | No `<example>` blocks (-15) + all 4 declared tools unused in body (-12) |
| plugins/ccam-insights/agents/insights-advisor.md | agent | 76 | No `<example>` blocks (-15) + Bash/Read/Grep all unused (-9) |
| plugins/ccam-analytics/agents/analytics-advisor.md | agent | 77 | No `<example>` blocks (-15) |
| plugins/ccam-devtools/agents/issue-triager.md | agent | 77 | No `<example>` blocks (-15) |
| plugins/ccam-analytics/agents/token-economist.md | agent | 79 | No `<example>` blocks (-15) |
| plugins/ccam-devtools/agents/db-inspector.md | agent | 79 | No `<example>` blocks (-15) |
| plugins/ccam-insights/agents/trend-forecaster.md | agent | 79 | No `<example>` blocks (-15) |
| plugins/ccam-quality/agents/reliability-engineer.md | agent | 79 | No `<example>` blocks (-15) |
| plugins/ccam-productivity/agents/focus-analyst.md | agent | 79 | No `<example>` blocks (-15) |
| plugins/ccam-workflows/agents/orchestration-analyst.md | agent | 79 | No `<example>` blocks (-15) |
| plugins/ccam-config/agents/config-auditor.md | agent | 79 | No `<example>` blocks (-15) |
| plugins/ccam-sessions/agents/session-investigator.md | agent | 79 | No `<example>` blocks (-15) |
| plugins/ccam-cost-guard/agents/budget-sentinel.md | agent | 79 | No `<example>` blocks (-15) |
| plugins/ccam-dashboard/commands/open-dashboard.md | command | 83 | Multi-step body without numbered steps (-10) |
| plugins/ccam-devtools/commands/tail-events.md | command | 85 | Multi-step body without numbered steps (-10) |
| plugins/ccam-workflows/commands/dag.md | command | 85 | Unsanitized $ARGUMENTS spliced unquoted into curl (command-injection risk) |
| plugins/ccam-workflows/commands/workflow.md | command | 85 | Unsanitized $ARGUMENTS spliced unquoted into curl (command-injection risk) |
| plugins/ccam-config/commands/audit-config.md | command | 85 | Multi-step body without numbered steps (-10) |
| plugins/ccam-sessions/commands/recent.md | command | 85 | Multi-step body without numbered steps (-10) |
| plugins/ccam-insights/commands/insights.md | command | 93 | Missing allowed-tools (-5) + vague quantifier "decision-relevant" (-2) |
| plugins/ccam-analytics/commands/burn-rate.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-analytics/commands/top-spenders.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-analytics/commands/cost-today.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-dashboard/commands/ping.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-dashboard/commands/status.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-devtools/commands/export.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-devtools/commands/doctor.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-insights/commands/compare.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-insights/commands/anomalies.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-quality/commands/errors.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-quality/commands/health.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-quality/commands/slo.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-productivity/commands/whats-next.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-productivity/commands/focus-report.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-productivity/commands/standup.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-workflows/commands/runs.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-config/commands/inventory.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-config/commands/memory.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-sessions/commands/replay.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-sessions/commands/find-session.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-cost-guard/commands/overspend.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-cost-guard/commands/forecast.md | command | 95 | Missing allowed-tools declaration (-5) |
| plugins/ccam-cost-guard/commands/budget.md | command | 95 | Missing allowed-tools declaration (-5) |

Weighted average across all 100 scored artifacts (17 agents, 30 commands, 53 skills; simple mean, each file equal weight): agents avg 76.1, commands avg 92.9, skills avg 59.8 → overall **72/100**.

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 3 |

The pre-scan flagged 1 Critical + 3 High coarse pattern matches. Under a detailed, context-aware manual review — including a repo-wide regex sweep for `curl\|sh`, `eval(`, `os.system`, `shell=True`, `sudo`, `base64 -d`, `/dev/tcp/`, `child_process.exec`, `new Function()` across every `.sh/.py/.js/.ts/.tsx` file outside `node_modules` — **zero** of those patterns reproduced in first-party code. The only repo-wide hit was inside a vendored, minified third-party bundle (`wiki/mermaid.min.js`), which is not first-party executable surface and is out of scope. The Critical/High pre-scan flags most likely came from coarse substring matches (e.g. `password`/`secret`-shaped identifiers in the legitimate Apple notarization flow, or `sudo`/`shell` appearing in deployment-script comments and usage text) that do not hold up as real vulnerabilities on inspection.

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks (`plugins/*/hooks/hooks.json`) | 3 (`ccam-analytics`, `ccam-productivity`, `ccam-cost-guard`) |
| MCP configs (`plugins/*/.mcp.json`) | 1 (`ccam-dashboard`) |
| Operational scripts (`scripts/`, `deployments/scripts/`, `desktop/scripts/`, `monitoring/scripts/`, `.claude/skills/*/scripts/`, `bin/`, `.husky/`) | 36 reviewed in full (of 165 total `.sh/.py/.js` files repo-wide; the remainder are application source/tests under `server/`, `mcp/src/`, `client/`, `desktop/src/`, `vscode-extension/` — not operational/install-time scripts) |
| Package manifests (`package.json`) | 6 (root, `mcp/`, `desktop/`, `vscode-extension/`, `monitoring/`, `client/`) — no `requirements.txt` in the repo |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | plugins/ccam-analytics/hooks/hooks.json | 8 | network-call | Stop/SubagentStop hooks pipe hook JSON through `jq` and POST it via `curl` to `http://localhost:4820/api/hooks/event`. Loopback-only, no external network or credential exposure, but it is an unconditional network call pattern from a hook. |
| 2 | Medium | plugins/ccam-cost-guard/hooks/hooks.json | 8 | network-call | Stop hook POSTs `{session_id, stop_reason, timestamp}` via `curl` to `http://localhost:4820/api/hooks/event`. Same loopback-only pattern as finding 1. |
| 3 | Medium | monitoring/scripts/ensure-binaries.js / monitoring/scripts/install-utils.js | ensure-binaries.js:41,56; install-utils.js:13-23 | runtime-binary-download | `npm run monitoring:setup` (also wired as `monitoring/package.json`'s `postinstall`) downloads Prometheus and Grafana release archives over HTTPS from `github.com`/`dl.grafana.com` and extracts+installs them into `monitoring/.bin/` with **no checksum or signature verification** before they are later executed as local binaries. URLs and versions are hardcoded/pinned (not user-controlled), which limits — but does not eliminate — the supply-chain exposure if either upstream host is compromised or MITM'd. |
| 4 | Low | plugins/ccam-productivity/hooks/hooks.json | 8, 20 | file-write-outside-repo | SessionStart/SessionEnd hooks append a timestamp line to `/tmp/ccam-session-timing.log`. Fixed path, non-sensitive content (a timestamp), low real-world impact. |
| 5 | Low | monitoring/scripts/paths.js | 123-124 | hardcoded-credentials | `GRAFANA_ADMIN_USER`/`GRAFANA_ADMIN_PASSWORD` are hardcoded to `admin`/`admin` and seeded into the local Grafana container via `GF_SECURITY_ADMIN_*` env vars on first start. Scoped to a local-only monitoring stack (127.0.0.1), but a well-known default-credential pattern worth flagging if the stack is ever exposed. |
| 6 | Low | scripts/postinstall.js / desktop/scripts/install.js / desktop/scripts/prebuild.js | postinstall.js:38; install.js:26; prebuild.js:36 | shell-true-reviewed | `spawnSync(..., { shell: true })` is used to launch `npm`/`npx`, but is gated to `process.platform === "win32"` with a fixed, non-interpolated argument list in every call site. Reviewed and confirmed not exploitable — no shell metacharacters reach the command. Recorded for completeness (false positive). |

### Execution Surfaces Reviewed and Cleared
`deployments/scripts/{deploy,rollback,teardown,blue-green-switch,db-backup,db-restore,health-check}.sh` (production-grade ops scripts: multi-step confirmation prompts on `production`, `set -euo pipefail`, array-based `kubectl`/`helm`/`terraform` invocations — no unquoted variable expansion into a shell string), `scripts/{hook-handler,codex-hook-handler,install-hooks,install-codex-hooks,postinstall,dev,clear-data,import-history,seed,generate-openapi-yaml}.js`, `scripts/expand-ts-module-docs.py`, `.claude/skills/file-headers/scripts/check-headers*.sh`, `.claude/skills/update-project-docs/scripts/doc-coverage.sh`, `.husky/{pre-commit,commit-msg}`, `bin/ccam.js`, `desktop/scripts/{build-icons.sh,notarize.js}`, all 6 `package.json` manifests (semver-range-pinned dependencies throughout, no `preinstall`/`postinstall` scripts beyond the reviewed items above).

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | plugins/ccam-workflows/commands/dag.md | Line 13: `curl -s http://localhost:4820/api/workflows/$ARGUMENTS` splices `$ARGUMENTS` unquoted directly into the shell command | A session id containing shell metacharacters executed via the Bash tool can break out of the intended `curl` invocation — command-injection risk when the argument is user-supplied. |
| 2 | plugins/ccam-workflows/commands/workflow.md | Line 13: identical unquoted `$ARGUMENTS` splice into `curl -s http://localhost:4820/api/workflows/$ARGUMENTS` | Same command-injection risk as #1. |
| 3 | plugins/ccam-dashboard/agents/dashboard-operator.md | Line 55 documents `node scripts/self-update-restart.js` as the self-update+restart command; no such file exists anywhere in the repo (verified) | Following the documented instruction fails with `MODULE_NOT_FOUND`; the agent will hallucinate or fail when a user asks it to self-update. |
| 4–30 | 27 files under `plugins/*/skills/**/SKILL.md` (ccam-analytics ×6, ccam-dashboard ×4, ccam-devtools ×6, ccam-insights ×6, ccam-quality ×5) | Frontmatter contains only `description:`, no `name:` field | Violates the open SKILL.md spec (`name` is required, 1-64 chars, must match the parent directory name); strict frontmatter validators will reject or fail to register the skill. Full file list in the JSONL sidecar. |
| 31–56 | 26 files under `plugins/*/skills/**/SKILL.md` (ccam-productivity ×6, ccam-workflows ×5, ccam-config ×5, ccam-sessions ×5, ccam-cost-guard ×5) | Same missing `name:` field | Same as above. Full file list in the JSONL sidecar. |

All 53 `SKILL.md` files repo-wide are missing `name:` — this is one mechanical, repo-wide fix (add `name: <directory-name>` to each frontmatter block), not 53 unrelated design issues.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | plugins/ccam-productivity/hooks/hooks.json | SessionStart/SessionEnd write to `/tmp/ccam-session-timing.log` | Route through the dashboard's own data directory (e.g. `getDataDir()` from `server/lib/claude-home.js`) instead of the shared, world-writable `/tmp`, for consistency with how the rest of the app stores state. |
| 2 | monitoring/scripts/ensure-binaries.js, monitoring/scripts/install-utils.js | Downloads and extracts Prometheus/Grafana binaries with no integrity check | Verify the downloaded archive's SHA256 against the checksum files both projects publish alongside each release (`prometheus-*.sha256`, `grafana-*.sha256`) before extraction; abort on mismatch. |
| 3 | monitoring/scripts/paths.js | Hardcoded `admin`/`admin` Grafana credentials | Generate a random password on first setup (persist it to `monitoring/.data/` alongside the other local state) and print it once, or read `GF_SECURITY_ADMIN_PASSWORD` from the environment with `admin`/`admin` only as an explicit `--insecure-default-creds`-style opt-in. |

Medium/Low findings 4 and 6 (the two loopback-only hook POSTs, and the reviewed-safe `shell:true` usage) need no code change — flagging them in the tracking issue for visibility is sufficient.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | plugins/ccam-analytics/agents/token-economist.md | No `<example>` blocks | -15 |
| 2 | plugins/ccam-analytics/agents/token-economist.md | `Read` declared in frontmatter, never used in body | -3 |
| 3 | plugins/ccam-analytics/agents/token-economist.md | `Grep` declared in frontmatter, never used in body | -3 |
| 4 | plugins/ccam-analytics/agents/analytics-advisor.md | No `<example>` blocks | -15 |
| 5 | plugins/ccam-analytics/agents/analytics-advisor.md | `Read` declared, never used | -3 |
| 6 | plugins/ccam-analytics/agents/analytics-advisor.md | `Grep` declared, never used | -3 |
| 7 | plugins/ccam-analytics/agents/analytics-advisor.md | Line 49: vague quantifier "relevant endpoints" | -2 |
| 8 | plugins/ccam-dashboard/agents/dashboard-operator.md | No `<example>` blocks | -15 |
| 9 | plugins/ccam-dashboard/agents/dashboard-operator.md | `Read` declared, never used | -3 |
| 10 | plugins/ccam-dashboard/agents/dashboard-operator.md | `Grep` declared, never used | -3 |
| 11 | plugins/ccam-dashboard/agents/dashboard-operator.md | Line 71: vague quantifier "when relevant" | -2 |
| 12 | plugins/ccam-devtools/agents/db-inspector.md | No `<example>` blocks | -15 |
| 13 | plugins/ccam-devtools/agents/db-inspector.md | `Read` declared, never used | -3 |
| 14 | plugins/ccam-devtools/agents/db-inspector.md | `Grep` declared, never used | -3 |
| 15 | plugins/ccam-devtools/agents/issue-triager.md | No `<example>` blocks | -15 |
| 16 | plugins/ccam-devtools/agents/issue-triager.md | `Read` declared, never used | -3 |
| 17 | plugins/ccam-devtools/agents/issue-triager.md | `Grep` declared, never used | -3 |
| 18 | plugins/ccam-devtools/agents/issue-triager.md | Line 70: vague quantifier "missing some events" | -2 |
| 19 | plugins/ccam-insights/agents/trend-forecaster.md | No `<example>` blocks | -15 |
| 20 | plugins/ccam-insights/agents/trend-forecaster.md | `Read` declared, never used | -3 |
| 21 | plugins/ccam-insights/agents/trend-forecaster.md | `Grep` declared, never used | -3 |
| 22 | plugins/ccam-insights/agents/insights-advisor.md | No `<example>` blocks | -15 |
| 23 | plugins/ccam-insights/agents/insights-advisor.md | `Bash` declared, never referenced (unlike sibling agents, body never names curl or a shell command) | -3 |
| 24 | plugins/ccam-insights/agents/insights-advisor.md | `Read` declared, never used | -3 |
| 25 | plugins/ccam-insights/agents/insights-advisor.md | `Grep` declared, never used | -3 |
| 26 | plugins/ccam-quality/agents/reliability-engineer.md | No `<example>` blocks | -15 |
| 27 | plugins/ccam-quality/agents/reliability-engineer.md | `Read` declared, never used | -3 |
| 28 | plugins/ccam-quality/agents/reliability-engineer.md | `Grep` declared, never used | -3 |
| 29 | plugins/ccam-productivity/agents/focus-analyst.md | No `<example>` blocks | -15 |
| 30 | plugins/ccam-productivity/agents/focus-analyst.md | `Read` declared, never used | -3 |
| 31 | plugins/ccam-productivity/agents/focus-analyst.md | `Grep` declared, never used | -3 |
| 32 | plugins/ccam-productivity/agents/productivity-coach.md | No `<example>` blocks | -15 |
| 33 | plugins/ccam-productivity/agents/productivity-coach.md | No "Output Standards" section (sibling agents all define one) | -10 |
| 34 | plugins/ccam-productivity/agents/productivity-coach.md | `Bash` declared, never referenced | -3 |
| 35 | plugins/ccam-productivity/agents/productivity-coach.md | `Read` declared, never used | -3 |
| 36 | plugins/ccam-productivity/agents/productivity-coach.md | `Grep` declared, never used | -3 |
| 37 | plugins/ccam-workflows/agents/orchestration-analyst.md | No `<example>` blocks | -15 |
| 38 | plugins/ccam-workflows/agents/orchestration-analyst.md | `Read` declared, never used | -3 |
| 39 | plugins/ccam-workflows/agents/orchestration-analyst.md | `Grep` declared, never used | -3 |
| 40 | plugins/ccam-config/agents/config-auditor.md | No `<example>` blocks | -15 |
| 41 | plugins/ccam-config/agents/config-auditor.md | `Read` declared, never used | -3 |
| 42 | plugins/ccam-config/agents/config-auditor.md | `Grep` declared, never used | -3 |
| 43 | plugins/ccam-sessions/agents/session-investigator.md | No `<example>` blocks | -15 |
| 44 | plugins/ccam-sessions/agents/session-investigator.md | `Read` declared, never used | -3 |
| 45 | plugins/ccam-sessions/agents/session-investigator.md | `Grep` declared, never used | -3 |
| 46 | plugins/ccam-cost-guard/agents/budget-sentinel.md | No `<example>` blocks | -15 |
| 47 | plugins/ccam-cost-guard/agents/budget-sentinel.md | `Read` declared, never used | -3 |
| 48 | plugins/ccam-cost-guard/agents/budget-sentinel.md | `Grep` declared, never used | -3 |
| 49 | .claude/agents/frontend-reviewer.md | No `<example>` blocks | -15 |
| 50 | .claude/agents/frontend-reviewer.md | `Read`/`Grep`/`Glob`/`Bash` all declared, none referenced explicitly in body | -12 |
| 51 | .claude/agents/backend-reviewer.md | No `<example>` blocks | -15 |
| 52 | .claude/agents/backend-reviewer.md | `Read`/`Grep`/`Glob`/`Bash` all declared, none referenced explicitly in body | -12 |
| 53 | .claude/agents/mcp-reviewer.md | No `<example>` blocks | -15 |
| 54 | .claude/agents/mcp-reviewer.md | `Read`/`Grep`/`Glob`/`Bash` all declared, none referenced explicitly in body | -12 |
| 55–84 | All 30 files under `plugins/*/commands/*.md` | Missing `allowed-tools` frontmatter despite the body invoking Bash/curl | -5 each |
| 85 | plugins/ccam-dashboard/commands/open-dashboard.md | Multi-step body (print block → detect platform → suggest open command) with no numbered list | -10 |
| 86 | plugins/ccam-dashboard/commands/open-dashboard.md | Line 6: vague quantifier "the relevant commands" | -2 |
| 87 | plugins/ccam-devtools/commands/tail-events.md | Multi-step body with no numbered list | -10 |
| 88 | plugins/ccam-insights/commands/insights.md | Line 17: vague quantifier "decision-relevant" | -2 |
| 89 | plugins/ccam-config/commands/audit-config.md | Multi-step body with no numbered list | -10 |
| 90 | plugins/ccam-sessions/commands/recent.md | Multi-step body with no numbered list | -10 |
| 91–117 | 27 files under `plugins/*/skills/**/SKILL.md` (ccam-analytics through ccam-quality) | No `<example>` blocks | -15 each |
| 118 | plugins/ccam-dashboard/skills/live-watch/SKILL.md | Line 3: vague quantifier "several times" | -2 |
| 119 | plugins/ccam-dashboard/skills/endpoint-probe/SKILL.md | Line 6: vague quantifier "correctly" | -2 |
| 120 | plugins/ccam-devtools/skills/health-check/SKILL.md | Line 5: vague quantifier "correctly" | -2 |
| 121 | plugins/ccam-devtools/skills/health-check/SKILL.md | Line 39: vague quantifier "reasonable size" | -2 |
| 122 | plugins/ccam-devtools/skills/data-export/SKILL.md | Line 10: vague quantifier "various formats" | -2 |
| 123–148 | 26 files under `plugins/*/skills/**/SKILL.md` (ccam-productivity through ccam-cost-guard) | No `<example>` blocks | -15 each |
| 149 | plugins/ccam-cost-guard/skills/daily-budget-check/SKILL.md | Line 34: vague quantifier "for some rows" | -2 |

Rows 55–84, 91–117, and 123–148 are collapsed ranges of one repeated finding type each (missing `allowed-tools` on all 30 commands; no `<example>` blocks on all 53 skills) — every individual instance is broken out by file in the JSONL sidecar (158 quality-issue lines total).

## Cross-Component
- `plugins/ccam-dashboard/.mcp.json` references `../../mcp/build/index.js`, which does not exist on disk — **not a bug**: `mcp/build/` is listed in both `.gitignore` and `mcp/.gitignore` as a TypeScript build output, generated by `npm run mcp:build`.
- `.claude-plugin/marketplace.json` lists exactly 10 plugin entries, matching the 10 directories under `plugins/`. No stale or orphaned plugin entries found.
- Skills referenced by name from command bodies (`dag-map`, `fleet-runs`, `delegation-audit`, `concurrency-report`, `error-propagation`, `model-savings`) all resolve to an existing `SKILL.md` under the matching plugin's `skills/` directory — no broken cross-references found beyond the one documented in Bugs #3.
- The missing-`name`-frontmatter pattern (53/53 skills) and missing-`allowed-tools` pattern (30/30 commands) are both total — i.e. they are not local to one plugin but apply identically across all 10 plugins, consistent with all 10 plugins having been generated from one shared template that predates both requirements.

## Recommendation
**REVIEW — submit NL fix PRs for the 56 bugs, flag the 3 Medium security findings in the tracking issue** (do not open public PRs for the Medium findings per the security-fix policy; note them for the maintainer). No Critical or High security findings survived detailed review, so contribution is not blocked. Given the size of the bug set, PR splitting guidance:
1. One PR: add `name:` frontmatter to all 53 `SKILL.md` files (single mechanical commit).
2. One PR: add `allowed-tools` frontmatter to all 30 commands (single mechanical commit).
3. One PR: quote `$ARGUMENTS` in `dag.md` and `workflow.md` (security-adjacent NL bug, small and isolated — safe for a public PR since it's a documentation/prompt fix, not the underlying execution engine).
4. One PR: fix or remove the `scripts/self-update-restart.js` reference in `dashboard-operator.md`.
