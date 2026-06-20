# NLPM Audit: zscole/adversarial-spec
**Date**: 2026-04-06  |  **Artifacts**: 2  |  **Strategy**: single
**NL Score**: 84/100
**Security**: BLOCKED
**Bugs**: 1  |  **Quality Issues**: 5  |  **Security Findings**: 5

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/adversarial-spec/SKILL.md | skill | 77 | Zero examples (−15) |
| .claude-plugin/plugin.json | plugin-manifest | 90 | Missing skills array declaration |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 3 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Scripts (Python) | skills/adversarial-spec/scripts/debate.py, models.py, providers.py, telegram_bot.py, session.py, prompts.py, mutmut_config.py, __init__.py, tests/__init__.py, tests/test_models.py, tests/test_model_calls.py, tests/test_cli.py, tests/test_prompts.py, tests/test_session.py, tests/test_providers.py, tests/test_telegram_bot.py |
| Package manifests | requirements.txt |
| Hooks | (none) |
| MCP configs | (none) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH | skills/adversarial-spec/SKILL.md | 364 | SEC-shell-injection | MODEL_LIST from AskUserQuestion is substituted directly into a Bash command template without quoting; a malicious "Other" model name entry (e.g. `gpt-4o; rm -rf ~`) could inject shell commands |
| 2 | MEDIUM | skills/adversarial-spec/scripts/telegram_bot.py | 63 | SEC-network-exfil | Full spec content is sent to api.telegram.org on every debate round via `api_call`; no content filtering, no explicit user confirmation before enabling —telegram; if TELEGRAM_BOT_TOKEN is exposed, spec data leaks |
| 3 | MEDIUM | skills/adversarial-spec/scripts/models.py | 330 | SEC-subprocess-cli | `subprocess.run` passes user-provided model name as a positional arg to the external `codex` binary; no validation of model-name format (could include flag-injection sequences) |
| 4 | MEDIUM | skills/adversarial-spec/scripts/providers.py | 101 | SEC-path-write | Config data written to `~/.claude/adversarial-spec/config.json` and profile data to `~/.config/adversarial-spec/` — both outside the repo and undocumented in the SKILL.md |
| 5 | LOW | requirements.txt | 1 | SEC-unpinned-semver | `litellm==1.80.13` is exact-pinned to a specific version that may miss security patches; range-pin with an upper bound is safer |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .claude-plugin/plugin.json | No `skills` array — the plugin's sole artifact (`skills/adversarial-spec/SKILL.md`) is undeclared in the manifest, breaking auto-discovery and install verification | Skill may silently not install on `claude plugin install` |

## Security Fixes (PR-worthy, Medium/Low only)
*Note: PRs are blocked pending resolution of the HIGH finding above. The items below are documented for post-resolution action only.*

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/adversarial-spec/scripts/telegram_bot.py | Spec content transmitted to Telegram without explicit user consent step | Document data-sharing behavior in SKILL.md; require the user to acknowledge before enabling `--telegram` |
| 2 | skills/adversarial-spec/scripts/models.py | Model name passed unsanitized to subprocess | Validate model name matches `^[\w./:@-]+$` before constructing the `cmd` list |
| 3 | skills/adversarial-spec/scripts/providers.py | Config/profile write locations not documented | Add a "Configuration Storage" section to SKILL.md listing `~/.claude/adversarial-spec/config.json` and `~/.config/adversarial-spec/profiles/` |
| 4 | requirements.txt | Exact-pinned litellm may miss security patches | Change to `litellm>=1.80.13,<2.0.0` and run test suite to validate |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/adversarial-spec/SKILL.md | Zero example blocks — no worked invocation or expected-output sample | −15 |
| 2 | skills/adversarial-spec/SKILL.md | Vague quantifier "comprehensive" (×2, lines ~200 and ~263): replace with "covers all 8 interview topic categories" / "all sections populated with ≥2 paragraphs" | −4 |
| 3 | skills/adversarial-spec/SKILL.md | Vague quantifier "thorough" (line ~200): replace with "covers all 8 interview topic categories" | −2 |
| 4 | skills/adversarial-spec/SKILL.md | Vague quantifier "suitable" (line ~839): replace with the specific import format (e.g., "JSON compatible with Jira/Linear import") | −2 |
| 5 | .claude-plugin/plugin.json | Missing `skills` declaration reduces score — manifest cannot assert what the plugin provides | −10 |

## Cross-Component
- **Undeclared skill**: `plugin.json` contains no `skills` array, so `skills/adversarial-spec/SKILL.md` is the plugin's sole NL artifact but is structurally invisible to the manifest. Tooling that relies on explicit declarations for install verification or scoring cannot locate the skill through the manifest.
- **Script references are valid**: The SKILL.md references `debate.py` and `telegram_bot.py` via `$(find ~/.claude -name debate.py -path '*adversarial-spec*' ...)`. These scripts exist at `skills/adversarial-spec/scripts/` in the repo, so the structural references are intact post-install.
- **No orphaned agents or commands**: The plugin has exactly one skill that implements the full workflow. All declared allowed-tools (Bash, Read, Write, AskUserQuestion) have observable call sites in the SKILL.md steps.
- **No contradictions between SKILL.md and scripts**: The SKILL.md's Step descriptions accurately reflect what `debate.py` implements (critique, providers, send-final, diff, export-tasks, sessions, profiles, bedrock subcommands).

## Recommendation
BLOCKED — do not submit PRs. File a private security report with the repo author covering finding #1 (HIGH: unquoted shell variable interpolation in SKILL.md command templates allows command injection via AskUserQuestion "Other" input). Once that is resolved, Bug #1 (plugin.json missing skills array) is eligible for a PR.
