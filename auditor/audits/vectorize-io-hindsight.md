# NLPM Audit: vectorize-io/hindsight
**Date**: 2026-04-06  |  **Artifacts**: 10  |  **Strategy**: single
**NL Score**: 94/100
**Security**: BLOCKED
**Bugs**: 1  |  **Quality Issues**: 8  |  **Security Findings**: 6

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| hindsight-integrations/codex/hooks/hooks.json | Hook Config | 88 | Unresolved template placeholder `__SCRIPTS_DIR__`; missing SessionEnd hook and `async: true` on Stop |
| .claude/skills/code-review/SKILL.md | Skill | 90 | Five vague quantifiers: "non-trivial" ×3, "significantly changed", "meaningful" (−10) |
| CLAUDE.md | Project Context | 90 | Dense, well-structured; minimal vague phrasing |
| skills/hindsight-architect/SKILL.md | Skill | 94 | Vague: "appropriate" ×3 (−6) |
| skills/hindsight-docs/SKILL.md | Skill | 95 | References `references/` docs tree; clean otherwise |
| hindsight-integrations/claude-code/.claude-plugin/plugin.json | Plugin Manifest | 95 | Clean |
| hindsight-integrations/claude-code/hooks/hooks.json | Hook Config | 95 | Clean |
| skills/hindsight-cloud/SKILL.md | Skill | 98 | Vague: "non-trivial" ×1 (−2) |
| skills/hindsight-local/SKILL.md | Skill | 98 | Vague: "non-trivial" ×1 (−2) |
| skills/hindsight-self-hosted/SKILL.md | Skill | 98 | Vague: "non-trivial" ×1 (−2) |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 2 |
| High | 2 |
| Medium | 2 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks (claude-code) | hindsight-integrations/claude-code/hooks/hooks.json |
| Hooks (codex) | hindsight-integrations/codex/hooks/hooks.json |
| Hook scripts (claude-code) | scripts/recall.py, retain.py, session_start.py, session_end.py + lib/*.py |
| Hook scripts (codex) | scripts/recall.py, retain.py, session_start.py + lib/*.py |
| Package manifest | package.json |
| MCP configs | None |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | skills/hindsight-cloud/SKILL.md | 24 | SEC-curl-pipe-sh | Skill instructs Claude to run `curl -fsSL https://hindsight.vectorize.io/get-cli \| bash` when setting up the CLI. Claude executes this on the user's machine, downloading and running arbitrary code from a remote server without integrity verification. |
| 2 | Critical | skills/hindsight-self-hosted/SKILL.md | 24 | SEC-curl-pipe-sh | Same curl-pipe-bash install pattern as finding #1; executed by Claude on user's machine during self-hosted CLI setup. |
| 3 | High | hindsight-integrations/claude-code/scripts/lib/daemon.py | 297 | SEC-shell-true | `subprocess.Popen(..., shell=True)` used to chain profile-create and daemon-start commands. Arguments are safely pre-escaped via `shlex.join()`, which significantly mitigates injection risk, but the shell=True pattern remains a concern if config values ever bypass shlex quoting. |
| 4 | High | hindsight-integrations/codex/scripts/lib/daemon.py | 269 | SEC-shell-true | Identical `subprocess.Popen(..., shell=True)` pattern as finding #3 in the codex integration's daemon pre-start function. Same shlex.join() mitigation applies. |
| 5 | Medium | package.json | 12 | SEC-postinstall-script | `"prepare": "./scripts/setup-hooks.sh"` runs automatically on `npm install`. The script only configures git hooks (`core.hooksPath`) and is low-risk in content, but any auto-executed install script is a medium-severity supply-chain surface. |
| 6 | Medium | hindsight-integrations/claude-code/scripts/retain.py | 147 | SEC-network-call | Hook script POSTs full conversation transcripts to the configured Hindsight API endpoint (cloud or local) on every Stop event. This is intentional functionality, but consumers should be aware that conversation content leaves the local machine to the configured `hindsightApiUrl`. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | hindsight-integrations/codex/hooks/hooks.json | Uses `__SCRIPTS_DIR__` as a path prefix — a template placeholder, not a resolved runtime variable. Unlike the claude-code plugin which uses the standard `${CLAUDE_PLUGIN_ROOT}` runtime variable, this placeholder must be substituted at install time. If deployed without substitution, all codex hooks silently fail. | All codex hooks (SessionStart, UserPromptSubmit, Stop) would invoke non-existent paths, disabling recall and retain. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/hindsight-cloud/SKILL.md | curl-pipe-bash install instruction (Critical — do NOT PR; file private report) | Replace with `pip install hindsight-cli` or `brew install hindsight` once packages are published; or verify download integrity with a checksum before executing. |
| 2 | skills/hindsight-self-hosted/SKILL.md | Same as above (Critical — private report only) | Same mitigation as #1. |
| 3 | package.json | `prepare` script auto-runs `setup-hooks.sh` on `npm install` | Document the prepare script's behavior in package.json or move git-hook setup to an explicit post-clone step in CONTRIBUTING.md to reduce surprise execution. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/skills/code-review/SKILL.md | "significantly changed" (line 130) — vague threshold | −2 |
| 2 | .claude/skills/code-review/SKILL.md | "non-trivial" ×3 (lines 135, 148, 167) — vague qualifier used in review criteria | −6 |
| 3 | .claude/skills/code-review/SKILL.md | "meaningful" (line 156, "meaningful test files") — vague standard | −2 |
| 4 | skills/hindsight-architect/SKILL.md | "appropriate" ×3 (lines ~675, ~718, ~834) — vague routing; prefer "use naming convention X" or "store ID in application database" | −6 |
| 5 | skills/hindsight-cloud/SKILL.md | "non-trivial" (line 133, "non-trivial task") — vague trigger; prefer listing example task types | −2 |
| 6 | skills/hindsight-local/SKILL.md | "non-trivial" (line 100) — same vague trigger as above | −2 |
| 7 | skills/hindsight-self-hosted/SKILL.md | "non-trivial" (line 141) — same vague trigger | −2 |
| 8 | hindsight-integrations/codex/hooks/hooks.json | Stop hook lacks `async: true` and uses 30s timeout vs claude-code's 15s async; missing SessionEnd hook means no guaranteed final retain on session close | −5 |

## Cross-Component
- **hindsight-docs/SKILL.md ↔ references/ directory**: The docs skill references `references/best-practices.md`, `references/developer/api/`, `references/sdks/`, and `references/cookbook/` as the documentation source. These directories exist in the repo at `skills/hindsight-docs/references/` and are marked "Auto-generated from `hindsight-docs/docs/`." The skill implicitly depends on the `generate-docs-skill.sh` script being run to keep references current; stale docs reduce skill accuracy. No missing files detected in this audit pass.
- **codex vs claude-code hook inconsistency**: The claude-code plugin uses `${CLAUDE_PLUGIN_ROOT}` (runtime-resolved env var) while the codex integration uses `__SCRIPTS_DIR__` (install-time template placeholder). The installation mechanism for codex is not documented in the hooks.json itself, creating an asymmetry that risks misconfiguration.
- **CLAUDE.md ↔ code-review/SKILL.md**: CLAUDE.md (line 174) references `.claude/skills/code-review/SKILL.md` by path and instructs Claude to read it before writing code. The skill exists and is well-formed — no broken reference. Consistent.

## Recommendation

BLOCKED — do not submit PRs. File private security report.

Two critical findings (curl-pipe-bash in `skills/hindsight-cloud/SKILL.md` and `skills/hindsight-self-hosted/SKILL.md`) and two high findings (shell=True in both daemon.py files) require private disclosure before any public contribution activity. The curl-pipe-bash pattern is particularly significant because it is embedded in skills that Claude actively loads and executes — when a user asks Claude to set up the Hindsight CLI, Claude will run `curl | bash` on their machine.

After the security findings are resolved:
- **Bug PR**: Fix the `__SCRIPTS_DIR__` placeholder in `hindsight-integrations/codex/hooks/hooks.json` (or document the substitution mechanism), add SessionEnd hook, add `async: true` to Stop hook.
- **Quality PRs**: Replace vague quantifiers ("non-trivial", "significantly changed", "meaningful", "appropriate") with concrete examples or specific thresholds across code-review/SKILL.md, hindsight-architect/SKILL.md, hindsight-cloud/SKILL.md, hindsight-local/SKILL.md, and hindsight-self-hosted/SKILL.md.
