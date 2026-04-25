# NLPM Audit: peterkrueck/Claude-Code-Development-Kit
**Date**: 2026-04-06  |  **Artifacts**: 12  |  **Strategy**: single
**NL Score**: 82/100
**Security**: BLOCKED
**Bugs**: 4  |  **Quality Issues**: 14  |  **Security Findings**: 7

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/merge.md | command | 33 | Missing `name` and `description` frontmatter (-50 combined) |
| commands/prime.md | command | 35 | Missing `name` and `description` frontmatter (-50 combined) |
| templates/CLAUDE.md | template | 82 | 4 of 6 sections are empty stubs (commented-out examples only) |
| skills/deploy/SKILL.md | skill | 88 | All deployment commands are `[PLACEHOLDER]` — non-functional without customisation |
| skills/image-edit/SKILL.md | skill | 90 | No explicit output/report step in numbered workflow |
| skills/image-gen/SKILL.md | skill | 91 | No formal report step; vague "good enough" / "best variant" qualifiers |
| skills/second-opinion/SKILL.md | skill | 92 | Multiple vague intensifiers: "genuinely", "routine", "real consequences", "add value" |
| skills/update-docs/SKILL.md | skill | 93 | No explicit output format; vague "meaningful" |
| hooks/config/pipeline.json | config | 95 | No description or version field (data file; frontmatter penalty not applied) |
| hooks/config/sensitive-patterns.json | config | 95 | No description or version field (data file; frontmatter penalty not applied) |
| skills/bg-remove/SKILL.md | skill | 96 | Cleanup step (delete magenta composite) mentioned only in Important Rules, not in numbered workflow |
| skills/review-work/SKILL.md | skill | 96 | Minor vague words: "relevant" (L29), "substantial" (description) |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 2 |
| High | 1 |
| Medium | 2 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hook scripts | hooks/notify.sh, hooks/review-on-stop.sh, hooks/security-scan.sh, hooks/snapshot-baseline.sh |
| Installer scripts | install.sh, setup.sh |
| Hook config (data) | hooks/config/pipeline.json, hooks/config/sensitive-patterns.json |
| MCP configs | None |
| Package manifests | None |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | install.sh | 6 | SEC-curl-pipe-sh | Comment documents intended invocation as `curl -fsSL … \| bash` — classic supply-chain attack vector; compromised GitHub repo yields RCE on all installers |
| 2 | Critical | install.sh | 90–188 | SEC-curl-pipe-sh | Two-step download-and-execute: fetches a tarball from GitHub (L90) and runs the extracted `setup.sh` directly (L188) without signature or checksum verification — functionally equivalent to curl-pipe-bash |
| 3 | High | hooks/security-scan.sh | 141 | SEC-json-injection | `$file` is interpolated directly into a double-quoted `echo` string that forms a JSON object. A filename containing `"` or `\` produces malformed JSON; a crafted name could inject a `"decision":"allow"` field, silently bypassing the security block |
| 4 | Medium | hooks/security-scan.sh | 87–92 | SEC-path-traversal | `$file_path` (from JSON `attached_files[]`) is passed to `stat` and `cat` without validating that the path stays within the project root — attacker-influenced path could read arbitrary files on the host |
| 5 | Medium | hooks/review-on-stop.sh | 13 | SEC-predictable-tmpfile | State file at `/tmp/claude-stop-${SESSION_ID}.state` uses a SESSION_ID sourced from untrusted JSON input; predictable path enables TOCTOU / symlink attacks in shared `/tmp/` |
| 6 | Low | hooks/snapshot-baseline.sh | 13 | SEC-predictable-tmpfile | Same predictable `/tmp/claude-baseline-${SESSION_ID}.numstat` pattern; an attacker who can pre-create the path can poison the git-diff baseline, causing the stop hook to under-count changes |
| 7 | Low | hooks/review-on-stop.sh | 130 | SEC-printf-b-escape | `printf '%b'` interprets backslash escape sequences inside `$MSG`, which contains filenames from `git diff` output; a crafted filename containing `\n` or `\t` can corrupt the JSON reason string sent to Claude Code |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/merge.md | Missing `name` frontmatter field | NLPM cannot register or discover this command |
| 2 | commands/merge.md | Missing `description` frontmatter field | NLPM scoring and auto-classification fail |
| 3 | commands/prime.md | Missing `name` frontmatter field | NLPM cannot register or discover this command |
| 4 | commands/prime.md | Missing `description` frontmatter field | NLPM scoring and auto-classification fail |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | hooks/security-scan.sh | `$file` unquoted in JSON echo (finding #3 is High — see private disclosure; this row is the underlying pattern to fix) | Replace bare `echo "{...\"$file\"...}"` with `jq -n --arg f "$file" --arg r "Security Alert…" '{"decision":"block","reason":$r}'` |
| 2 | hooks/security-scan.sh | File path from JSON not bounds-checked before `cat`/`stat` | Resolve path with `realpath` and verify it begins with `$PROJECT_ROOT` before reading |
| 3 | hooks/review-on-stop.sh | Predictable `/tmp/` state file path | Replace manual path with `mktemp` and store the result; pass path via session state or env var |
| 4 | hooks/snapshot-baseline.sh | Same predictable `/tmp/` path | Same: use `mktemp -t claude-baseline.XXXXXXXX` and store the path |
| 5 | hooks/review-on-stop.sh:130 | `printf '%b'` interprets escape sequences from git-sourced filenames | Replace `printf '%b' "$MSG"` with `printf '%s' "$MSG"` |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/merge.md | No `allowed-tools` declaration | -5 |
| 2 | commands/merge.md | No empty-input handling (`$ARGUMENTS` used but never guarded) | -10 |
| 3 | commands/merge.md | Vague word: "relevant" in "Stage relevant files by name" | -2 |
| 4 | commands/prime.md | No `allowed-tools` declaration | -5 |
| 5 | commands/prime.md | No empty-input handling (`$ARGUMENTS` passed through without guard) | -10 |
| 6 | skills/deploy/SKILL.md | All shell commands are `[YOUR_…]` placeholders — skill is non-functional until customised | -12 |
| 7 | skills/image-edit/SKILL.md | No explicit report/output step in numbered workflow | -5 |
| 8 | skills/image-gen/SKILL.md | No formal report/output step | -5 |
| 9 | skills/image-gen/SKILL.md | Vague: "good enough" (L104), "best variant" (L102) — no objective criteria | -4 |
| 10 | skills/second-opinion/SKILL.md | Vague intensifiers without definition: "genuinely useful" (L11), "routine tasks" (L22), "real consequences" (L22), "add value" (L17) | -8 |
| 11 | skills/update-docs/SKILL.md | No explicit output/confirmation format | -5 |
| 12 | skills/update-docs/SKILL.md | Vague: "meaningful" (L65, "Only update files where the change is meaningful") | -2 |
| 13 | skills/review-work/SKILL.md | Vague: "relevant source files" (L29), "substantial implementation work" (description) | -4 |
| 14 | templates/CLAUDE.md | Sections 2 (Architecture), 4 (Standards), 5 (Testing), 6 (Security) are entirely commented-out stubs with no real rules | -18 |

## Cross-Component
All internal references resolve cleanly:

- `commands/merge.md` → `/update-docs` skill and `ExitWorktree` tool: both present ✓
- `hooks/config/pipeline.json` → `review_command: "/review-work"` and `docs_command: "/update-docs"`: both skills exist ✓
- `hooks/review-on-stop.sh` → `hooks/config/pipeline.json`: file present ✓
- `hooks/security-scan.sh` → `hooks/config/sensitive-patterns.json`: file present ✓
- `skills/image-edit/SKILL.md` → `.claude/skills/image-edit/scripts/analyze_bounds.py`: installed by `setup.sh` ✓
- `skills/image-gen/SKILL.md` → `.claude/skills/image-gen/scripts/generate.ts`: installed by `setup.sh` ✓
- `skills/second-opinion/SKILL.md` → `Bash(gemini:*)` permission rule: written to `settings.local.json` by `setup.sh` ✓
- `commands/prime.md` → `@docs/ai-context/*.md` files: template stubs installed by `setup.sh` ✓

No broken references, orphaned components, or contradictions detected.

**Minor note**: `commands/merge.md` and `commands/prime.md` lack frontmatter entirely — they would be invisible to any NLPM tool that uses frontmatter-based discovery. Other commands in the kit's target installation path (`.claude/commands/`) would be unaffected, but these source files are the canonical originals.

## Recommendation

**BLOCKED — do not submit PRs. File private security report.**

Two CRITICAL findings (curl-pipe-bash installer design, L6 and L90–188 of `install.sh`) and one HIGH finding (JSON injection in `hooks/security-scan.sh:141`) require private disclosure before public PRs are appropriate. The HIGH finding is particularly ironic: the security scanner that protects against credential leakage can itself be bypassed via a crafted filename, silently allowing a blocked tool call to proceed.

Once the Critical/High findings are privately disclosed and addressed, four NL bug PRs (missing frontmatter on both commands) and the Medium/Low security fixes listed above are straightforward and PR-ready.
