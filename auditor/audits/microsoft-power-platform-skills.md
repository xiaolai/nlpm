# NLPM Audit: microsoft/power-platform-skills
**Date**: 2026-04-06  |  **Artifacts**: 146  |  **Strategy**: progressive
**NL Score**: 96/100
**Security**: REVIEW
**Bugs**: 0  |  **Quality Issues**: 31  |  **Security Findings**: 9

> Scope note: 99 of the 146 artifacts were in the scoring list (20 agents, 69 skills, 7 plugin manifests, 2 hooks.json, 1 CLAUDE.md). All 20 agents were scored on frontmatter, `model`, `tools` and `<example>` presence, verified by grep across every agent file. Some agents (genpage-planner, genpage-edit-planner, genpage-page-builder, webapi-integration, code-app-architect) were also read in part. The 69 skills were only checked mechanically: `name` and `description` present, and `allowed-tools` present or absent. Their bodies were not read line by line, so their 100/100 is a floor from mechanical checks, not a full review. The weighted average is (20 agents averaging 82.25 + 79 other artifacts at 100) / 99. Security review covered hooks, MCP configs, `.mcp.json` launchers, and grep-based pattern sweeps of the non-test, non-vendor scripts. `plugins/power-automate/server/mcp.mjs` (about 48k-line minified bundle) was only pattern-swept, not read. The pre-scan reported 4 critical and 1 high pattern matches. I could not reproduce any of them as exploitable; see the Security Findings table for what they resolved to.

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| plugins/code-apps/agents/code-app-architect.md | agent | 75 | No `model`, no `tools`, no `<example>` blocks |
| plugins/mobile-apps/agents/native-app-planner.md | agent | 80 | No `model`; no `<example>` blocks |
| plugins/model-apps/agents/genpage-planner.md | agent | 80 | No `model`; no `<example>` blocks |
| plugins/model-apps/agents/genpage-edit-planner.md | agent | 80 | No `model`; no `<example>` blocks |
| plugins/model-apps/agents/genpage-customapi-builder.md | agent | 80 | No `model`; no `<example>` blocks |
| plugins/model-apps/agents/genpage-page-builder.md | agent | 80 | No `model`; no `<example>` blocks |
| plugins/model-apps/agents/genpage-connector-builder.md | agent | 80 | No `model`; no `<example>` blocks |
| plugins/model-apps/agents/genpage-entity-builder.md | agent | 80 | No `model`; no `<example>` blocks |
| plugins/canvas-apps/agents/canvas-screen-builder.md | agent | 80 | No `model`; no `<example>` blocks |
| plugins/canvas-apps/agents/canvas-app-planner.md | agent | 80 | No `model`; no `<example>` blocks |
| plugins/mobile-apps/agents/offline-profile-architect.md | agent | 85 | No `<example>` blocks |
| plugins/mobile-apps/agents/screen-planner.md | agent | 85 | No `<example>` blocks (has prose "Worked example") |
| plugins/mobile-apps/agents/screen-builder.md | agent | 85 | No `<example>` blocks |
| plugins/mobile-apps/agents/data-model-architect.md | agent | 85 | No `<example>` blocks |
| plugins/power-pages/agents/table-permissions-architect.md | agent | 85 | No `<example>` blocks (trigger phrases only in description) |
| plugins/power-pages/agents/webapi-integration.md | agent | 85 | No `<example>` blocks (trigger phrases only in description) |
| plugins/power-pages/agents/ai-webapi-settings-architect.md | agent | 85 | No `<example>` blocks |
| plugins/power-pages/agents/ai-webapi-integration.md | agent | 85 | No `<example>` blocks |
| plugins/power-pages/agents/data-model-architect.md | agent | 85 | No `<example>` blocks |
| plugins/power-pages/agents/webapi-settings-architect.md | agent | 85 | No `<example>` blocks |
| plugins/power-pages/hooks/hooks.json | hook config | 100 | Valid; three events registered (Pre/PostToolUse, UserPromptSubmit) |
| plugins/mobile-apps/hooks/hooks.json | hook config | 100 | Valid; fail-open telemetry hooks |
| plugins/power-automate/CLAUDE.md | memory | 100 | None found |
| plugins/power-apps-mobile-extension/.claude-plugin/plugin.json | manifest | 100 | Manifest not read line by line; no issue seen |
| plugins/model-apps/.claude-plugin/plugin.json | manifest | 100 | Manifest not read line by line; no issue seen |
| plugins/power-automate/.claude-plugin/plugin.json | manifest | 100 | None; name, version, description present |
| plugins/code-apps/.claude-plugin/plugin.json | manifest | 100 | Manifest not read line by line; no issue seen |
| plugins/canvas-apps/.claude-plugin/plugin.json | manifest | 100 | None; name, version, description present |
| plugins/mcp-apps/.claude-plugin/plugin.json | manifest | 100 | Manifest not read line by line; no issue seen |
| plugins/power-pages/.claude-plugin/plugin.json | manifest | 100 | None; name, version, description present |
| plugins/mobile-apps/.claude-plugin/plugin.json | manifest | 100 | None (manifest name `mobile-app` differs from directory `mobile-apps`; matches AGENTS.md usage) |
| plugins/power-apps-mobile-extension/skills/build-ios-binary/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-apps-mobile-extension/skills/audit-ppmplugin/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-apps-mobile-extension/skills/generate-native-extension/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-apps-mobile-extension/skills/test-native-extension/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-apps-mobile-extension/skills/generate-ppmplugin-manifest/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-apps-mobile-extension/skills/assemble-ppmplugin/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-apps-mobile-extension/skills/design-native-extension-feature/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-apps-mobile-extension/skills/generate-ppmplugin/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-apps-mobile-extension/skills/debug-extension/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-apps-mobile-extension/skills/build-android-binary/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-apps-mobile-extension/skills/generate-pcf-companion/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-apps-mobile-extension/skills/publish-pcf-companion/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/model-apps/skills/telemetry/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/model-apps/skills/report-issue/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/model-apps/skills/app-builder/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/model-apps/skills/genpage/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-automate/skills/create-flow/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-automate/skills/manage-desktop-flows/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-automate/skills/manage-flows/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-automate/skills/debug-flow/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-automate/skills/browse-flows/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-automate/skills/build-flow/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-automate/skills/report-issue/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-automate/skills/diagnose-flow/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-automate/skills/setup/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-automate/skills/route-environments/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/list-connections/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/add-datasource/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/add-mcscopilot/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/add-sharepoint/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/add-teams/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/add-azuredevops/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/deploy/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/report-issue/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/add-workiq/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/create-code-app/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/add-connector/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/add-office365/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/add-dataverse/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/add-onedrive/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/code-apps/skills/add-excel/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/canvas-apps/skills/configure-canvas-mcp/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/canvas-apps/skills/canvas-app/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/canvas-apps/skills/report-issue/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/canvas-apps/skills/add-data-source/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/mcp-apps/skills/generate-mcp-app-ui/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/mcp-apps/skills/generate-codeful-mcp-tool/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/mcp-apps/skills/report-issue/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/security-review/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/scan-site/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/test-site/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/setup-pipeline/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/integrate-backend/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/configure-env-variables/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/create-site/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/telemetry/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/setup-datamodel/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/integrate-webapi/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/add-ai-webapi/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/setup-auth/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/add-cloud-flow/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/add-server-logic/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/manage-headers/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/diagnose-deployment/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/deploy-site/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/migrate-webapi-selectall/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/report-issue/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/add-sample-data/SKILL.md | skill | 100 | Frontmatter-only check |
| plugins/power-pages/skills/force-link-environment/SKILL.md | skill | 100 | Frontmatter-only check |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 5 |
| Low | 4 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks (Claude format) | plugins/power-pages/hooks/hooks.json, plugins/mobile-apps/hooks/hooks.json, plugins/model-apps/hooks/hooks.json, plugins/canvas-apps/hooks/hooks.json |
| Hooks (Copilot format) | plugins/canvas-apps/hooks.json |
| Hook scripts | plugins/*/hooks/*.js (telemetry, validators), plugins/canvas-apps/hooks/inject-sync-reminder.cs (run through `dotnet run --file`) |
| MCP configs | plugins/canvas-apps/.mcp.json, plugins/mobile-apps/.mcp.json, plugins/model-apps/.mcp.json, plugins/power-automate/.mcp.json, plugins/power-pages/.mcp.json |
| MCP launchers | plugins/model-apps/scripts/launch-playwright-mcp.js, plugins/power-pages/scripts/launch-playwright-mcp.js, plugins/mcp-apps/scripts/ |
| Bundled server | plugins/power-automate/server/mcp.mjs (about 48k lines, vendored and minified; only pattern-swept) |
| Package manifests | plugins/mobile-apps/template/package.json, plugins/power-pages/skills/create-site/assets/{react,vue,angular,astro}/package.json, plugins/model-apps/scripts/_vendor-build/package.json, plugins/mcp-apps/scripts/_vendor-build/package.json |
| Repo-level scripts | scripts/install.js, scripts/validate-secure-process-execution.js |
| Lifecycle scripts | None. No `postinstall`, `preinstall` or `prepare` in any package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | plugins/model-apps/scripts/launch-playwright-mcp.js | 19 | `npx -y @playwright/mcp@latest` | The MCP server launcher fetches and runs an unpinned `@latest` package at every start. This is a runtime package install and a supply-chain exposure. The sibling power-pages launcher pins an exact version, and the repo's own secure-coding rule forbids `@latest` in MCP launchers. |
| 2 | Medium | plugins/canvas-apps/.mcp.json | 5 | `dnx <pkg> --yes` (unpinned) | The MCP server runs `Microsoft.PowerApps.CanvasAuthoring.McpServer` through `dnx --yes` with no version and auto-confirmed install. |
| 3 | Medium | plugins/power-automate/server/mcp.mjs | 17765 | `new Function(...)` | Bundled Ajv compiles generated validator source with `new Function`. I read the call site only, not the input flow. The pattern is standard Ajv code generation from schemas, not attacker-supplied strings, so I rate it medium rather than critical. Provenance of the bundle is unverified. |
| 4 | Medium | plugins/power-automate/server/mcp.mjs | 44160 | `new Function(...)` | Same as #3, second Ajv code-generation site in the same bundle. |
| 5 | Medium | plugins/power-pages/hooks/hooks.json | null | Network telemetry, default-on | UserPromptSubmit and Skill Pre/PostToolUse hooks run on every prompt or skill call and send events (per the plugin docs, including org GUID, tenant GUID and Entra object ID) to a collector. The plugin documents opt-out via `POWER_PLATFORM_SKILLS_TELEMETRY_POWER_PAGES_OPTOUT` and says the events carry no prompts, paths or URLs. I did not audit the telemetry library. Flagged as a privacy and network-call surface, not as a defect. |
| 6 | Low | plugins/mobile-apps/scripts/open-wrap-url.js | 70 | `spawnSync(..., {shell: true})` | `shell: true` is used for `command -v <cmd>`. All call sites pass fixed literals (`open`, `cmd`, `xdg-open`), so it is not injectable today, but it conflicts with the repo's own no-shell rule. |
| 7 | Low | scripts/install.js | 55 | `execSync(cmd, {shell: true})` | The installer builds shell strings by interpolating `REPO`, `MARKETPLACE_NAME` and plugin names. All are constants or come from an internal list, so I found no user-controlled input. Low risk, but `execFile` is safer. |
| 8 | Low | scripts/install.js | 398 | `curl ... \| sudo bash` (printed hint) | The string is printed as a manual install suggestion for Azure CLI and is never executed. It matches the curl-pipe-shell pattern and was likely one of the pre-scan hits. It is a false positive for execution. |
| 9 | Low | plugins/canvas-apps/hooks/hooks.json | 11 | `dotnet run --file` on every prompt | Every user prompt compiles and runs a C# file from the plugin dir (30s timeout). The path is `${CLAUDE_PLUGIN_ROOT}`-anchored, so it is not injectable. Cost and latency risk only. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
No bugs found. All 69 skills and 20 agents in scope have `name` and `description`. No plugin.json in scope declares a skills or agents array, so there is no manifest-versus-disk drift.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | plugins/model-apps/scripts/launch-playwright-mcp.js | `@playwright/mcp@latest` at line 19 | Pin to the exact version already used by `plugins/power-pages/scripts/launch-playwright-mcp.js` (`PLAYWRIGHT_MCP_VERSION`), and reuse the same launcher hardening. |
| 2 | plugins/canvas-apps/.mcp.json | Unpinned `dnx` package | Pin an explicit version, for example `Microsoft.PowerApps.CanvasAuthoring.McpServer@<version>`. |
| 3 | plugins/mobile-apps/scripts/open-wrap-url.js | `shell: true` at line 70 | Probe with `where` (Windows) or `which` (POSIX) via `spawnSync` with `shell: false`, or drop the probe and rely on the `spawn` error event. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1-20 | All 20 agents in `plugins/*/agents/` | No `<example>` blocks (R09, zero examples). The power-pages agents put trigger phrases in `description` and several mobile agents have prose worked examples, but none use `<example>` blocks. | -15 each |
| 21 | plugins/code-apps/agents/code-app-architect.md | `model` not declared (R10). | -5 |
| 22 | plugins/code-apps/agents/code-app-architect.md | `tools` not declared (R11). The agent inherits every tool although it is an advisory persona. | -5 |
| 23 | plugins/mobile-apps/agents/native-app-planner.md | `model` not declared (R10). | -5 |
| 24-29 | plugins/model-apps/agents/genpage-{planner,edit-planner,customapi-builder,page-builder,connector-builder,entity-builder}.md | `model` not declared (R10). | -5 each |
| 30-31 | plugins/canvas-apps/agents/canvas-{app-planner,screen-builder}.md | `model` not declared (R10). | -5 each |

Vague-quantifier counts were not measured because the skill bodies were not read.

## Cross-Component
| # | Finding | Detail |
|---|---------|--------|
| 1 | Stale skill count (CC-stale-count) | `plugins/mobile-apps/AGENTS.md` says "24 skills + 5 agents" but 26 `SKILL.md` files exist on disk. Its architecture block and rule 12 list 4 agents, and `offline-profile-architect` is missing from both. |
| 2 | Broken path in docs (CC-broken-relative-path) | `plugins/code-apps/AGENTS.md` tells authors to run `claude --plugin-dir /path/to/plugins/power-apps`. The directory is `plugins/code-apps`; `plugins/power-apps` does not exist. The file is also titled "Power Apps Plugin" and refers to a "power-apps plugin". |
| 3 | Undocumented skills (CC-orphan-component) | `plugins/code-apps/AGENTS.md` lists 13 skills in its table and tree. Disk has 15; `add-workiq` and `report-issue` are missing from the docs. |
| 4 | Stale hook documentation (CC-stale-count) | `plugins/power-pages/CLAUDE.md` says hooks are "a single PostToolUse hook (matcher Skill)". `hooks/hooks.json` registers three events: PreToolUse(Skill), PostToolUse(Skill) and UserPromptSubmit. |

## Recommendation
REVIEW — no Critical or High findings were confirmed. The pre-scan Critical hits resolved to a printed `curl | sudo bash` hint and Ajv `new Function` codegen in a vendored bundle. There are no NL bugs, and the Medium findings are unpinned MCP launchers plus default-on telemetry. Submit the medium and low security fix PRs (#1 and #2 are the strongest, since the repo already pins in power-pages) and the doc fixes (cross-component #1-#4). The R09 and R10 quality items are informational only. Before treating the target as fully clear, someone should review `plugins/power-automate/server/mcp.mjs` provenance and the 69 skill bodies, which this pass did not read.
