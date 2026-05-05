# NLPM Audit: hellowind777/hello2cc
**Date**: 2026-04-06  |  **Artifacts**: 3  |  **Strategy**: single
**NL Score**: 84/100
**Security**: REVIEW
**Bugs**: 0  |  **Quality Issues**: 3  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/native.md | agent | 61 | Zero example blocks; no output format section |
| hooks/hooks.json | hook config | 95 | All references valid; no scoring penalties |
| .claude-plugin/plugin.json | plugin manifest | 95 | Comprehensive userConfig; clean structure |

**Weighted average**: (61 + 95 + 95) / 3 = 84/100

### Score Breakdown — agents/native.md
- Start: 100
- Zero example blocks: −15
- Missing output format section: −10
- Vague quantifiers × 7 ("genuinely unclear", "genuinely independent", "尽量" × 5): −14
- **Final: 61**

### Score Breakdown — hooks/hooks.json
- Start: 100
- All 11 event types well-formed; all 5 referenced scripts exist; timeouts set: no deductions
- **Final: 95**

### Score Breakdown — .claude-plugin/plugin.json
- Start: 100
- All required fields present; 10 userConfig entries with full title + description; license, keywords, outputStyles all valid
- **Final: 95**

---

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 2 |
| Low | 1 |

> The single High finding is marked false-positive (see findings table). Effective highest severity is Medium. Overall posture: REVIEW.

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | hooks/hooks.json — 11 event types, 5 distinct scripts |
| Scripts (hook-invoked) | scripts/orchestrator.mjs, scripts/subagent-context.mjs, scripts/subagent-stop.mjs, scripts/teammate-idle.mjs, scripts/task-lifecycle.mjs |
| Scripts (dev utility) | scripts/ccstatusline-bridge.mjs, scripts/generate-release-notes.mjs, scripts/lib/* |
| MCP configs | None |
| Package manifests | package.json (no postinstall script) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH *(fp)* | scripts/ccstatusline-bridge.mjs | 52 | SEC-shell-true | `spawn(command, {shell:true})` where `command` derives from `process.argv.slice(2)` or `HELLO2CC_CCSTATUSLINE_COMMAND` env var. **False positive**: `shell:true` is intentional — this bridge script is designed to execute a user-configured downstream command (e.g., `npx -y ccstatusline@latest`) and is not invoked by any hook in hooks.json; the command source is the developer, not untrusted hook input. |
| 2 | MEDIUM | scripts/generate-release-notes.mjs | 80 | UNCLASSIFIED | `fetch()` to `api.github.com` at runtime; reads `GH_TOKEN` / `GITHUB_TOKEN` env vars and sends them as Authorization header to GitHub. Dev-only utility, not in hook surface. |
| 3 | MEDIUM | scripts/lib/hook-io.mjs | 18 | UNCLASSIFIED | `HELLO2CC_DEBUG_ROUTE_PATH` env var controls the destination path of `writeFileSync`; if set to an attacker-controlled value, could write debug payload outside the repo. Enabled only when the env var is non-empty. |
| 4 | LOW | scripts/ccstatusline-bridge.mjs | 47 | SEC-unpinned-semver | Default downstream command is `npx -y ccstatusline@latest`; `@latest` is unpinned and will silently pull future versions on each invocation. |

---

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No NL bugs found. All required frontmatter fields present; all hook script references resolve. | — |

---

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/ccstatusline-bridge.mjs | Unpinned `npx -y ccstatusline@latest` (LOW) | Pin to a specific version: `npx ccstatusline@<version>` and update on each release. |
| 2 | scripts/generate-release-notes.mjs | Runtime `fetch()` to GitHub API with token env var (MEDIUM) | Document the network dependency in README; add a `--no-network` flag that skips acknowledgement resolution when the token is absent. |
| 3 | scripts/lib/hook-io.mjs | `HELLO2CC_DEBUG_ROUTE_PATH` allows arbitrary write path (MEDIUM) | Validate the resolved path is within a known safe directory (e.g., `os.tmpdir()` or the plugin data root) before calling `writeFileSync`. |

---

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/native.md | Zero example blocks — no `## Example` sections illustrating correct vs. incorrect agent behavior | −15 |
| 2 | agents/native.md | No output format section — agent gives no guidance on expected response structure or length constraints | −10 |
| 3 | agents/native.md | Vague quantifiers: "genuinely unclear" (×1, line 33), "genuinely independent" (×1, line 36), "尽量" (×5, lines 27–46) | −14 |

---

## Cross-Component
- **plugin.json → outputStyles**: `"./output-styles"` resolves to `output-styles/` directory, which exists. ✓
- **hooks.json → scripts**: All five referenced scripts (`orchestrator.mjs`, `subagent-context.mjs`, `subagent-stop.mjs`, `teammate-idle.mjs`, `task-lifecycle.mjs`) exist under `scripts/`. ✓
- **No commands layer**: The plugin ships only one agent (`native.md`) and no command `.md` files; no command↔agent cross-reference to validate.
- **ccstatusline-bridge.mjs not in hooks.json**: The bridge script appears to be a user-invoked utility for piping to a downstream statusline renderer; its absence from hook declarations is consistent with its optional nature.
- No orphaned components or terminology drift detected.

---

## Recommendation
REVIEW — submit NL fix PRs for `agents/native.md` (examples + output format), flag MEDIUM security findings in a tracking issue. The single HIGH pattern match (shell:true in ccstatusline-bridge.mjs) is determined to be a false positive given the bridge script's intentional design and its absence from the hook invocation graph.
