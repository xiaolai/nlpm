# NLPM Audit: volcengine/OpenViking
**Date**: 2026-04-06  |  **Artifacts**: 44  |  **Strategy**: batched
**NL Score**: 97.4/100
**Security**: BLOCKED
**Bugs**: 4  |  **Quality Issues**: 14  |  **Security Findings**: 19

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| examples/claude-code-memory-plugin/commands/ov.md | command | 70 | Missing allowed-tools, zero examples, no output-format section |
| benchmark/tau2/train/experience_loader_template/SKILL.md | skill | 79 | Zero worked examples |
| bot/workspace/skills/skill-creator/SKILL.md | skill | 86 | Vague quantifiers ("as needed" x5, "appropriate", "relevant") |
| examples/openclaw-plugin/skills/openviking-context-database/SKILL.md | skill | 88 | Vague quantifiers ("relevant" x4, "usually", "correctly") |
| examples/openclaw-plugin/skills/install-openviking-memory/SKILL.md | skill | 90 | Vague quantifiers ("relevant" x3, "effectively", "correctly") |
| examples/skills/ov-add-paper/SKILL.md | skill | 92 | Unused declared tools (Glob, Grep) |
| examples/skills/ov-resources/SKILL.md | skill | 94 | Vague quantifiers ("correctly", "appropriate", "relevant") |
| examples/skills/ov-server-operate/SKILL.md | skill | 96 | Vague quantifiers ("as needed", "sufficient") |
| examples/skills/ov-skills/SKILL.md | skill | 96 | Vague quantifiers ("correctly", "appropriate") |
| examples/skills/ov_dream/SKILL.md | skill | 96 | Vague quantifiers ("relevant", "correctly") |
| docs/images/agents/zh/mcp.md | doc | 100 | None |
| docs/images/agents/en/mcp.md | doc | 100 | None |
| docs/images/agents/zh/hermes.md | doc | 100 | None |
| docs/images/agents/en/hermes.md | doc | 100 | None |
| docs/images/agents/zh/api.md | doc | 100 | None |
| docs/images/agents/en/api.md | doc | 100 | None |
| docs/images/agents/zh/agent-cli.md | doc | 100 | None (see Cross-Component) |
| docs/images/agents/en/agent-cli.md | doc | 100 | None |
| docs/images/agents/zh/sdk.md | doc | 100 | None |
| docs/images/agents/en/sdk.md | doc | 100 | None |
| docs/images/agents/zh/codex.md | doc | 100 | None |
| docs/images/agents/en/codex.md | doc | 100 | None |
| docs/images/agents/zh/cursor.md | doc | 100 | Broken markdown escaping — see Bugs |
| docs/images/agents/en/cursor.md | doc | 100 | None |
| docs/images/agents/zh/claude-code.md | doc | 100 | None |
| docs/images/agents/en/claude-code.md | doc | 100 | None |
| docs/images/agents/zh/cli.md | doc | 100 | None (see Cross-Component) |
| docs/images/agents/en/cli.md | doc | 100 | None |
| docs/images/agents/zh/openclaw.md | doc | 100 | None |
| docs/images/agents/en/openclaw.md | doc | 100 | None |
| docs/images/agents/zh/opencode.md | doc | 100 | None |
| docs/images/agents/en/opencode.md | doc | 100 | None |
| docs/images/agents/zh/trae.md | doc | 100 | Broken markdown escaping — see Bugs |
| docs/images/agents/en/trae.md | doc | 100 | None |
| bot/workspace/skills/github/SKILL.md | skill | 100 | None |
| bot/workspace/skills/summarize/SKILL.md | skill | 100 | None |
| bot/workspace/skills/tmux/SKILL.md | skill | 100 | None |
| bot/workspace/skills/github-proxy/SKILL.md | skill | 100 | None |
| bot/workspace/skills/cron/SKILL.md | skill | 100 | None |
| bot/workspace/skills/opencode/SKILL.md | skill | 100 | Broken script reference — see Bugs |
| bot/workspace/skills/weather/SKILL.md | skill | 100 | None |
| examples/claude-code-memory-plugin/hooks/hooks.json | config | 100 | None |
| examples/codex-memory-plugin/hooks/hooks.json | config | 100 | Broad "*" matcher — see Cross-Component/Security |
| examples/claude-code-memory-plugin/.claude-plugin/plugin.json | config | 100 | None |

Note: docs/images/agents/{zh,en}/*.md are plain configuration-instruction snippets for third-party tools (MCP, Cursor, Codex, etc.), not Claude Code agent/command/skill definitions — frontmatter, example-block, model-tier, and allowed-tools penalties don't apply to this artifact family. Two files (zh/cursor.md, zh/trae.md) have a genuine rendering defect tracked as a Bug rather than a scored-rubric penalty, since "broken markdown escaping" isn't one of the ten enumerated NL penalty items.

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 7 |
| High | 2 |
| Medium | 4 |
| Low | 6 |

Methodology note: the pre-scan's raw pattern counts (10 critical, 2 high) are reconciled here. Of the 10 critical `curl`-piped-to-shell string matches, 7 are real executable code paths (listed below); the other 3 are false positives — `tests/oc2ov_test/upgrade_openviking.sh:203` and `:211` only `log(...)` the string as instructional text for a human to copy, and `examples/codex-memory-plugin/setup-helper/install.sh:9` is a code comment. The 2 high-severity matches are both genuine `subprocess(..., shell=True)` call sites.

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | examples/claude-code-memory-plugin/hooks/hooks.json, examples/codex-memory-plugin/hooks/hooks.json (2) |
| MCP configs | examples/claude-code-memory-plugin/.mcp.json, examples/codex-memory-plugin/.mcp.json (2) |
| Plugin manifest | examples/claude-code-memory-plugin/.claude-plugin/plugin.json (1) |
| Hook-invoked scripts (.mjs) | ~30 files under both plugins' scripts/ directories |
| Package manifests | docs/package.json, web-studio/package.json, bot/package.json, npm/cli/package.json (4) |
| Python requirements | tests/oc2ov_test/requirements.txt, tests/api_test/requirements.txt (2) |
| Dockerfiles (build-time exec) | Dockerfile, docker/mooncake-test/Dockerfile, bot/deploy/Dockerfile, bot/deploy/docker/Dockerfile (4; 2 contain curl-pipe-shell) |
| CI workflows | .github/workflows/api_test.yml (contains runtime curl-pipe-bash) |
| Runtime installer code | openviking_cli/utils/ollama.py (contains curl-pipe-shell) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | openviking_cli/utils/ollama.py | 146 | curl-pipe-sh | `install_ollama()` macOS fallback runs `bash -c "curl -fsSL https://ollama.com/install.sh \| sh"` via `subprocess.run` at CLI runtime, no checksum/pin verification |
| 2 | Critical | openviking_cli/utils/ollama.py | 153 | curl-pipe-sh | Same function's Linux branch, identical unpinned remote-script execution |
| 3 | Critical | bot/deploy/Dockerfile | 7 | curl-pipe-bash | `curl -fsSL https://deb.nodesource.com/setup_20.x \| bash -` during image build |
| 4 | Critical | bot/deploy/Dockerfile | 10 | curl-pipe-sh | `curl -LsSf https://astral.sh/uv/install.sh \| sh` during image build |
| 5 | Critical | bot/deploy/docker/Dockerfile | 9 | curl-pipe-bash | Duplicate NodeSource pattern in the second (mounted-volume) deployment Dockerfile |
| 6 | Critical | bot/deploy/docker/Dockerfile | 11 | curl-pipe-sh | Duplicate uv-installer pattern in the second Dockerfile |
| 7 | Critical | .github/workflows/api_test.yml | 498 | curl-pipe-bash | CI step runs `curl -fsSL http://openviking.tos-cn-beijing.volces.com/cli/install.sh \| bash` (first-party domain, CI-only, but plain HTTP and no signature check) |
| 8 | High | bot/workspace/skills/opencode/opencode_utils.py | 18 | subprocess-shell-true | `execute_cmd()` runs an arbitrary string via `subprocess.run(cmd, shell=True, ...)`; this helper backs an LLM-driven bot skill, so the string can originate from model output |
| 9 | High | examples/openclaw-plugin/tests/e2e/test-archive-expand.py | 844 | subprocess-shell-true | `shell=True` call in test harness code; test-only scope, no production trigger |
| 10 | Medium | examples/claude-code-memory-plugin/scripts/auto-capture.mjs | 408 | network-egress | Captured conversation turns (may include user-pasted secrets matched by MEMORY_TRIGGERS) are POSTed to `cfg.baseUrl`; defaults to `http://127.0.0.1:1933` but is overridable via `OPENVIKING_URL` env var |
| 11 | Medium | examples/codex-memory-plugin/scripts/auto-capture.mjs | 62 | network-egress | Same egress pattern for the Codex variant; request also attaches `Authorization`/`X-API-Key` headers built from `cfg.apiKey` |
| 12 | Medium | bot/vikingbot/sandbox/backends/srt-wrapper.mjs | 202 | child-process-exec | `exec(sandboxedCommand)` after `SandboxManager.wrapWithSandbox()` — intended purpose of this sandbox-execution backend, not raw shell injection, but worth tracking |
| 13 | Medium | bot/vikingbot/sandbox/backends/srt-wrapper.mjs | 357 | child-process-exec | Second `exec(sandboxedCommand)` call site (`executeCommandInternal`) |
| 14 | Low | npm/cli/package.json | 9 | postinstall-script | `"postinstall": "node bin/postinstall.mjs"` — reviewed `bin/postinstall.mjs`: prints version/PATH diagnostics via `execFileSync(..., ["--version"])` only, no download-and-execute |
| 15 | Low | examples/codex-memory-plugin/hooks/hooks.json | 17 | broad-hook-matcher | `"matcher": "*"` on UserPromptSubmit (also lines 29, 41 for Stop/PreCompact) fires on every event; sibling `claude-code-memory-plugin/hooks/hooks.json` uses the idiomatic empty-string `""` match-all instead |
| 16 | Low | web-studio/package.json | 44 | unpinned-latest | 6 `@tanstack/*` deps pinned to `"latest"` (lines 44, 47, 48, 81, 82, 83) instead of a resolvable version |
| 17 | Low | web-studio/package.json | 19 | unpinned-caret-range | Majority of dependencies use `^` ranges, permitting automatic minor/patch drift |
| 18 | Low | tests/oc2ov_test/requirements.txt | 1 | unpinned-semver | `requests>=2.28.0`, no upper bound |
| 19 | Low | tests/api_test/requirements.txt | 1 | unpinned-semver | All 9 listed dependencies use unbounded `>=` ranges |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | docs/images/agents/zh/cursor.md | Prose and both tables contain literal double-escaped markdown (`mcp\.json`, `ov\-mcp\-server`, `Bearer \&lt;API Key\&gt;`, `\&\#34;启用\&\#34;`) instead of clean text/entities | Renders as garbled backslashes and literal HTML-entity text to Chinese-locale readers; the fenced JSON code block itself is unaffected |
| 2 | docs/images/agents/zh/trae.md | Same double-escaping defect (`\&lt;`, `\&gt;`, `\&\#34;`, escaped hyphens/periods) throughout prose and both tables | Same rendering breakage; strongly suggests a shared, systematic bug in whatever export/translation step produced both files — worth fixing once and auditing other zh files for the same pattern |
| 3 | bot/workspace/skills/skill-creator/SKILL.md | References `scripts/init_skill.py`, `scripts/package_skill.py`, `references/workflows.md`, `references/output-patterns.md` — none exist; the skill's directory contains only SKILL.md | An agent following this skill cannot init or package any skill (both scripted steps fail file-not-found) and cannot load either linked reference doc |
| 4 | bot/workspace/skills/opencode/SKILL.md | Documents and invokes `list_messages_of_session.py`, which does not exist; only `list_sessions.py` and `opencode_utils.py` are present in the directory | The section's own example command fails file-not-found; it appears to be a copy-paste of the `list_sessions.py` invocation with the wrong filename |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | examples/claude-code-memory-plugin/scripts/auto-capture.mjs:408 | Captured session content leaves the process over HTTP with no TLS enforcement when `OPENVIKING_URL` points at a non-local, non-HTTPS endpoint | Warn (or refuse) at startup if `OPENVIKING_URL` is set to a non-localhost `http://` origin |
| 2 | examples/codex-memory-plugin/scripts/auto-capture.mjs:62 | Same as above, plus API key is attached in cleartext headers to whatever `baseUrl` resolves to | Same fix, plus redact/omit `X-API-Key` when `baseUrl` isn't localhost |
| 3 | npm/cli/package.json:9 | `postinstall` script present (reviewed benign) but its mere presence trips supply-chain scanners | Document in README/SECURITY.md that `postinstall` only prints diagnostics, to pre-empt scanner false positives |
| 4 | examples/codex-memory-plugin/hooks/hooks.json:17,29,41 | Broad `"*"` matcher instead of the empty-string match-all idiom used by the sibling plugin | Align on `""` (or scope the matcher) for consistency with `claude-code-memory-plugin` |
| 5 | web-studio/package.json:44 | 6 dependencies pinned to `"latest"` | Pin to resolved semver ranges |
| 6 | tests/api_test/requirements.txt:1 | All 9 dependencies use unbounded `>=` | Add upper bounds or a lockfile |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | examples/claude-code-memory-plugin/commands/ov.md | Missing allowed-tools declaration | -5 |
| 2 | examples/claude-code-memory-plugin/commands/ov.md | Zero example/output-sample blocks | -15 |
| 3 | examples/claude-code-memory-plugin/commands/ov.md | No output-format section describing what the status display returns | -10 |
| 4 | benchmark/tau2/train/experience_loader_template/SKILL.md | Missing example blocks — no sample query, candidate JSON, or situation snippet shown | -15 |
| 5 | benchmark/tau2/train/experience_loader_template/SKILL.md | Vague quantifiers ("relevant" x2, "usually") | -6 |
| 6 | examples/skills/ov-server-operate/SKILL.md | Vague quantifiers ("as needed", "sufficient") | -4 |
| 7 | examples/skills/ov-resources/SKILL.md | Vague quantifiers ("correctly", "appropriate", "relevant") | -6 |
| 8 | examples/skills/ov-skills/SKILL.md | Vague quantifiers ("correctly", "appropriate") | -4 |
| 9 | examples/skills/ov-add-paper/SKILL.md | Unused declared tools Glob, Grep (never referenced in body) | -6 |
| 10 | examples/skills/ov-add-paper/SKILL.md | Vague quantifier ("usually") | -2 |
| 11 | examples/skills/ov_dream/SKILL.md | Vague quantifiers ("relevant", "correctly") | -4 |
| 12 | examples/openclaw-plugin/skills/openviking-context-database/SKILL.md | Vague quantifiers ("relevant" x4, "usually", "correctly") | -12 |
| 13 | examples/openclaw-plugin/skills/install-openviking-memory/SKILL.md | Vague quantifiers ("relevant" x3, "effectively", "correctly") | -10 |
| 14 | bot/workspace/skills/skill-creator/SKILL.md | Vague quantifiers ("as needed" x5, "appropriate", "relevant") | -14 |

## Cross-Component
- All 12 zh/en documentation pairs under `docs/images/agents/` have matching step counts, code blocks, and table structures — good structural parity overall, aside from the two rendering bugs noted above.
- `docs/images/agents/zh/agent-cli.md` is slightly less explicit than its `en` counterpart about substituting the placeholder API key into the embedded prompt — a translation-completeness gap, not a scored defect.
- `docs/images/agents/zh/cli.md` says "copy the following API Key" where no key value actually follows, while `en/cli.md` (matching the pattern used by both languages of `hermes.md`/`openclaw.md`) correctly says "shown on the page" — a phrasing inconsistency worth aligning during the next translation pass.
- `examples/codex-memory-plugin/hooks/hooks.json` uses a broad `"*"` matcher on three hook events where its sibling `examples/claude-code-memory-plugin/hooks/hooks.json` uses the idiomatic empty-string `""` match-all — a convention divergence between two otherwise-parallel plugins (also tracked as a Low security finding).
- Verified all skill/command references resolve to real files, with the two exceptions already listed under Bugs: `bot/workspace/skills/skill-creator/SKILL.md` and `bot/workspace/skills/opencode/SKILL.md`. Every other cross-reference checked (docs, scripts, hooks-to-scripts, plugin.json-to-disk) resolved cleanly — `plugin.json`'s declared fields and both `hooks.json` `command` paths all point at real files.

## Recommendation
BLOCKED — do not submit PRs. File private security report.

Rationale: 7 Critical (unauthenticated `curl | shell` execution, two in a runtime code path (`openviking_cli/utils/ollama.py`) triggered by normal CLI use, not just build-time tooling) and 2 High findings (unsandboxed `subprocess(shell=True)` reachable from an LLM-driven bot skill) require private disclosure before any public PR. Once those are triaged, the 4 NL bugs and the 6 Medium/Low security fixes listed above are safe to submit as ordinary PRs; they carry no disclosure risk on their own.
