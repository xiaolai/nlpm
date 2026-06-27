# NLPM Audit: buildatscale-tv/claude-code-plugins
**Date**: 2026-06-27  |  **Artifacts**: 7  |  **Strategy**: single
**NL Score**: 92/100
**Security**: BLOCKED
**Bugs**: 1  |  **Quality Issues**: 13  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| plugins/buildatscale/commands/pr.md | command | 73 | Multi-step without numbered steps; `git branch` called but not in allowed-tools |
| plugins/buildatscale/commands/commit.md | command | 86 | No empty input handling (no-changes case unhandled) |
| plugins/nano-banana/skills/generate/SKILL.md | skill | 91 | Missing allowed-tools declaration despite directing shell command execution |
| plugins/promo-video/skills/promo-video/SKILL.md | skill | 95 | Unused `pip:*` declared; vague "couple" |
| plugins/buildatscale/commands/ceo.md | command | 96 | Vague "suitable", "if needed" |
| plugins/nano-banana/CLAUDE.md | memory | 100 | No penalties found |
| plugins/promo-video/CLAUDE.md | memory | 100 | No penalties found |

**Weighted average**: (73 + 86 + 91 + 95 + 96 + 100 + 100) / 7 = **92/100**

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 1 |
| Medium | 1 |
| Low | 1 |

Note: Pre-scan reported 2 Critical and 1 High pattern matches. One Critical match (bash-guard.sh lines 44, 68, 74) is a **confirmed false positive** — the script contains these patterns as grep regex strings for detection/blocking purposes, not for execution. The true findings below reflect only verified execution-surface risks.

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | plugins/buildatscale/hooks/bash-guard.sh, hooks/git-block-force-push.sh, hooks/file-write-cleanup.sh, hooks/file-guard.sh (4 files) |
| Scripts | plugins/buildatscale/scripts/statusline.sh, plugins/nano-banana/skills/generate/scripts/image.py, plugins/promo-video/skills/promo-video/scripts/generate_voiceover.py (3 files) |
| MCP configs | None |
| Package manifests | None found |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | plugins/buildatscale/hooks/file-guard.sh | 13 | eval-with-variables | `eval "$(echo "$input" \| jq -r '@sh "tool_name=... file_path=..."')"` — eval with jq-processed external input. jq's `@sh` operator mitigates the risk substantially, but `eval` on any external data is a dangerous pattern; a jq version with a `@sh` escaping bug would allow command injection via a crafted `file_path` value in the hook JSON. |
| 2 | High | plugins/buildatscale/hooks/file-write-cleanup.sh | 11 | file-write-outside-repo | `echo "$(date): Hook triggered with input: $input" >> /tmp/claude-hook-debug.log` — writes the full PostToolUse hook JSON payload to a world-readable /tmp path. The payload includes `tool_input` (file_path, and for Write hooks, the full file content), which can expose code and credentials to any process on the same machine. Debug artifact left in production. |
| 3 | Medium | plugins/buildatscale/scripts/statusline.sh | 218 | path-traversal | `git -C "$CURRENT_DIR" rev-parse --show-toplevel` — `CURRENT_DIR` is drawn from `jq -r '.workspace.current_dir'` on Claude Code's status-line JSON (line 103). If the JSON payload were tampered with (e.g., via a path injection), the unquoted-expansion path could escape the intended directory context. Risk is low in practice because the source is Claude Code's own output, but the value is not sanitized. |
| 4 | Low | plugins/nano-banana/skills/generate/scripts/image.py | 3–7 | unpinned-semver | PEP 723 inline script metadata declares `google-genai` and `pillow` without version pins; `uv run` will resolve the latest available version at execution time, making the script vulnerable to supply-chain changes in those packages. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | plugins/buildatscale/commands/pr.md | `git branch --show-current` is called directly at line 11 and via subshell on lines 20 and 27, but `Bash(git branch)` is absent from the `allowed-tools` frontmatter list | Claude Code will block these calls in strict permission mode; the command will fail at the first `git branch` invocation |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | plugins/buildatscale/hooks/file-write-cleanup.sh | Debug log to world-readable /tmp path (line 11) may expose file content from hook payloads | Remove the `echo "$(date): Hook triggered..."` debug line entirely; if logging is needed, write to a project-local path (e.g., `.claude/hook-debug.log`) and add that path to `.gitignore` |
| 2 | plugins/nano-banana/skills/generate/scripts/image.py | Unpinned `google-genai` and `pillow` dependencies in PEP 723 header | Pin to tested versions, e.g. `google-genai>=1.16,<2` and `pillow>=11,<12` |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | plugins/buildatscale/commands/pr.md | Multi-step command (check status → check diff → verify branch → push → create PR) lacks numbered steps | -10 |
| 2 | plugins/buildatscale/commands/pr.md | No empty input handling: no guard for "zero commits ahead of base branch"; command would push an empty branch and open a PR with no changes | -10 |
| 3 | plugins/buildatscale/commands/pr.md | `Bash(git checkout)` declared in allowed-tools but never called in the command body | -3 |
| 4 | plugins/buildatscale/commands/pr.md | Vague "appropriate title and description" — no specification of title format or required body sections | -2 |
| 5 | plugins/buildatscale/commands/pr.md | Vague "if the changes warrant testing steps" — unspecified criterion for when a test plan is included | -2 |
| 6 | plugins/buildatscale/commands/commit.md | No empty input handling: if working tree is clean, command proceeds through all steps and may attempt an empty commit | -10 |
| 7 | plugins/buildatscale/commands/commit.md | Vague "appropriate commit messages" and "Stage the appropriate files" (×2 occurrences) | -4 |
| 8 | plugins/buildatscale/commands/ceo.md | Vague "suitable for a CEO or executive audience" | -2 |
| 9 | plugins/buildatscale/commands/ceo.md | Vague "if needed to understand the context" | -2 |
| 10 | plugins/nano-banana/skills/generate/SKILL.md | Missing `allowed-tools` frontmatter; skill directs execution of `echo`, `grep`, and `uv run` (Bash) without declaring them | -5 |
| 11 | plugins/nano-banana/skills/generate/SKILL.md | Vague "for any purpose" and "for ANY image generation request" in description (×2) | -4 |
| 12 | plugins/promo-video/skills/promo-video/SKILL.md | `Bash(pip:*)` declared in allowed-tools but no `pip` invocation appears in SKILL.md body | -3 |
| 13 | plugins/promo-video/skills/promo-video/SKILL.md | Vague "a couple quick setup questions" — "couple" is an unspecified quantity | -2 |

## Cross-Component

**No plugin.json found.** Neither plugin (buildatscale nor nano-banana nor promo-video) ships a `plugin.json` manifest. Without a manifest, Claude Code cannot register commands or skills via `claude plugin install`; users must manually configure the artifacts. This also means command allowed-tools cannot be verified against a registry entry. Recommend adding `plugin.json` to each plugin root.

**External skill dependency (promo-video).** `plugins/promo-video/skills/promo-video/SKILL.md` requires the `remotion-best-practices` skill (`npx skills add remotion-dev/skills`), documented in `CLAUDE.md`. This dependency is not bundled and not verified at install time. If the external skill is unavailable or the install command changes, Phase 3 instructions will reference an unloaded skill.

**Internal references resolve.** All intra-repo references in `promo-video/SKILL.md` (`metallic-swoosh.md`, `voiceover.md`, `promo-patterns.md`, `scripts/generate_voiceover.py`) were verified to exist on disk. The `nano-banana` skill's reference to `skills/generate/scripts/image.py` also resolves.

**bash-guard.sh false positive.** The pre-scan flagged two Critical pattern matches in `plugins/buildatscale/hooks/bash-guard.sh` (curl-pipe-sh at line 44, eval pattern at line 74). Both are detection regex strings inside `grep -qE` tests — the script actively *blocks* these patterns rather than executing them. Downstream tooling should treat bash-guard.sh findings as false positives.

## Recommendation

**BLOCKED — do not submit PRs. File private security reports.**

- **SEC-1 (Critical):** `eval` in `file-guard.sh:13` — report privately to maintainer. The `@sh` escape mitigates the immediate risk but the pattern should be replaced with a safer variable-assignment approach (e.g., two separate `jq -r` invocations into distinct variables without `eval`).
- **SEC-2 (High):** `/tmp` debug log in `file-write-cleanup.sh:11` — report privately. Remove the debug line before any public release.
- **BUG-1 (PR-worthy after security is resolved):** `git branch` missing from `pr.md` allowed-tools.
- **SEC-3 / SEC-4 (Medium/Low — safe to PR):** statusline.sh path sanitization and image.py unpinned deps can be raised as public issues or PRs once the Critical/High path is clear.
