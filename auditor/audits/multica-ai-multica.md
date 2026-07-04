# NLPM Audit: multica-ai/multica
**Date**: 2026-04-06  |  **Artifacts**: 11  |  **Strategy**: single
**NL Score**: 98/100
**Security**: BLOCKED
**Bugs**: 2  |  **Quality Issues**: 1  |  **Security Findings**: 8

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .agents/skills/web-design-guidelines/SKILL.md | Skill | 85 | `argument-hint` nested under a custom `metadata:` block instead of top-level frontmatter — Claude Code won't read it as the `/help` hint |
| server/internal/service/builtin_skills/multica-working-on-issues/SKILL.md | Skill | 97 | `allowed-tools` uses comma-separated tool patterns, not the documented space-separated scalar format |
| CLAUDE.md | Memory | 100 | — |
| apps/mobile/CLAUDE.md | Memory | 100 | — |
| server/internal/service/builtin_skills/multica-autopilots/SKILL.md | Skill | 100 | — |
| server/internal/service/builtin_skills/multica-creating-agents/SKILL.md | Skill | 100 | — |
| server/internal/service/builtin_skills/multica-mentioning/SKILL.md | Skill | 100 | — |
| server/internal/service/builtin_skills/multica-projects-and-resources/SKILL.md | Skill | 100 | — |
| server/internal/service/builtin_skills/multica-runtimes-and-repos/SKILL.md | Skill | 100 | — |
| server/internal/service/builtin_skills/multica-skill-importing/SKILL.md | Skill | 100 | — |
| server/internal/service/builtin_skills/multica-squads/SKILL.md | Skill | 100 | — |

Weighted average (11 files): **98/100**.

This is an unusually strong artifact set: every `SKILL.md` in `builtin_skills/` carries complete `name`/`description` frontmatter, zero vague quantifiers found in any of the 11 files, and each of the 8 `references/*-source-map.md` sidecars they cite was confirmed to exist on disk. Spot-checked source claims (the `MentionRe` regex, the reserved-slugs generator round-trip, all `apps/mobile/CLAUDE.md` file references) all resolved to real, matching code on the current tree.

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 4 |
| Medium | 2 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 files |
| Scripts (shell) | `scripts/check.sh`, `scripts/dev.sh`, `scripts/ensure-postgres.sh`, `scripts/init-worktree-env.sh`, `scripts/install.sh`, `scripts/install.test.sh`, `scripts/local-env.sh`, `scripts/selfhost-config.test.sh`, `docker/entrypoint.sh` |
| Scripts (PowerShell) | `scripts/install.ps1` |
| Scripts (Node) | `scripts/generate-reserved-slugs.mjs`, `scripts/screenshot-pr-cards.mjs` |
| MCP configs | none (`.mcp.json` not present) |
| Package manifests | `package.json` (root); `apps/desktop/package.json` (`postinstall: electron-builder install-app-deps`); `apps/web/package.json`, `apps/docs/package.json` (`postinstall: fumadocs-mdx`) |
| Python deps | none (`requirements.txt` not present — Go + TS project) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | Critical | scripts/install.sh | 5, 8, 430, 468 | SEC-curl-pipe-sh | Documented/advertised self-install invocation `curl -fsSL https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.sh \| bash`, mirrored as the PowerShell equivalent `irm ... \| iex` at `scripts/install.ps1:4,7`. This is the standard installer idiom used by rustup/Homebrew/Deno and is served from the project's own `raw.githubusercontent.com` path over HTTPS (not attacker-controlled), but it matches the CRITICAL pattern definition literally — pipe-to-shell of remote content with no local review step. |
| 2 | High | scripts/install.sh | 157-162 | SEC-missing-integrity-check | `install_cli_binary` downloads the release `.tar.gz` via `curl -fsSL ... -o` and extracts/installs it with **no checksum or signature verification** — contrast with the sibling `install.ps1:263-294`, which SHA256-verifies the same release asset against `checksums.txt` before installing. Deterministic gap: diffing the two installers for the same release artifact shows one path is unverified. |
| 3 | High | scripts/install.sh | 169-170 | SEC-sudo-usage | `install_cli_binary` falls back to `sudo mv "$tmp_dir/multica" "$bin_dir/multica"` when `/usr/local/bin` is not writable. Scoped to a single `mv` of a file already downloaded in the same function (not parameterized by external input), but sudo escalation in a piped installer is a real trust-boundary widening. |
| 4 | High | scripts/install.sh | 178-179, 187-195 | SEC-path-modification | `install_cli_binary` exports `PATH` for the current shell and `add_to_path()` appends an `export PATH=...` line to `~/.bashrc` / `~/.zshrc` when the target bin dir isn't already on `PATH`. |
| 5 | High | apps/desktop/package.json, apps/web/package.json, apps/docs/package.json | 33, 13, 12 | SEC-postinstall-script | `postinstall` scripts present: `electron-builder install-app-deps` (desktop), `fumadocs-mdx` (web, docs). Both are well-known, actively maintained framework tools invoked with no extra arguments or network calls beyond their normal build responsibilities — recorded per pattern match; reviewed content is benign. |
| 6 | Medium | .agents/skills/web-design-guidelines/SKILL.md | 26 | SEC-unpinned-remote-source | Skill fetches `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` (mutable `main`, no commit pin) via WebFetch, and the skill's own text says "the fetched content contains all the rules **and output format instructions**" — i.e. remote, third-party content drives this skill's behavior at run time with no local pin or review step. Not classic R42 injection (not user-controlled), but a supply-chain / mutable-ref risk. |
| 7 | Medium | scripts/check.sh, scripts/dev.sh, scripts/install.sh | 60/108/118 (check.sh), 391 (install.sh) | SEC-network-call | Multiple scripts make outbound network calls (`curl` health-checks against `localhost`, `curl` against `github.com`/`raw.githubusercontent.com`, `docker compose ... pull`). All observed calls are either localhost-scoped health checks or fetches from the project's own GitHub org — recorded for inventory; no exfiltration or unexpected destination found. |
| 8 | Low | package.json | 27 | SEC-unpinned-semver | `"ui:add": "cd packages/ui && npx shadcn@latest add"` pulls `shadcn@latest` unpinned at invocation time, unlike every other dependency in this file (which uses `^`-ranges, `catalog:`, or lockfile-pinned versions). |

No reverse shells, no `eval`/`exec` on untrusted input, and no credential-exfiltration or base64-decode-and-execute patterns were found in any of the 12 scripts read.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .agents/skills/web-design-guidelines/SKILL.md:4-7 | `argument-hint: <file-or-pattern>` (plus `author`, `version`) is nested one level down inside a custom `metadata:` block instead of being a top-level frontmatter key. `skills/nlpm/conventions-claude` documents `argument-hint` as a reserved top-level field that Claude Code reads directly to populate `/help`. | Because it sits inside an arbitrary `metadata:` object rather than at the frontmatter root, Claude Code's `/help` UI will not surface the `<file-or-pattern>` argument hint for this skill — the field is present in the file but inert. Directly verifiable by comparing this file's YAML structure to the documented schema position; no live parser run needed. |
| 2 | server/internal/service/builtin_skills/multica-working-on-issues/SKILL.md:5 | `allowed-tools: Bash(multica *), Bash(git *), Bash(gh *)` separates tool patterns with commas; `skills/nlpm/conventions-claude` documents the scalar-string form as **space**-separated (`"Read Grep Bash(git *)"`). Every other `multica-*` skill in the same directory uses a single bare pattern, so this is the only file exercising multi-pattern scalar syntax, and it diverges from the documented delimiter. | If the frontmatter parser splits strictly on whitespace, the three comma-joined tokens could collapse into one malformed tool-permission string, silently under- or mis-granting `git`/`gh` Bash access for this skill. Not independently reproduced against the live parser this pass — flagged for a maintainer to confirm, not asserted as certainly broken. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | .agents/skills/web-design-guidelines/SKILL.md:26 | Guidelines fetched from a mutable `main` ref | Pin the fetch URL to a specific commit SHA (or tagged release), and re-pin deliberately when adopting upstream updates, so the skill's output-format behavior can't change silently between runs. |
| 2 | package.json:27 | `ui:add` script installs `shadcn@latest` unpinned | Pin to a specific `shadcn` version (or document that `ui:add` is an interactive dev-only command where "latest" is intentional) so the behavior is reproducible across contributor machines. |

Critical/High findings (#1-5 in the Security Findings table) are excluded here per policy — private disclosure only, not public PRs.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .agents/skills/web-design-guidelines/SKILL.md | Core behavior depends on a live network fetch of third-party content with no documented fallback if the fetch fails or returns unexpected content | -5 |

## Cross-Component
- All 8 `references/*-source-map.md` sidecars referenced by the `builtin_skills/multica-*` SKILL.md files exist on disk — no broken references.
- `CLAUDE.md` → `apps/mobile/CLAUDE.md`, `apps/docs/content/docs/developers/conventions.mdx` (+ `.zh.mdx`), `packages/views/locales/glossary.md`, and `server/internal/handler/reserved_slugs.json` all resolve to real files.
- `apps/mobile/CLAUDE.md` → `apps/mobile/docs/rnr-migration.md`, `apps/mobile/lib/inbox-display.ts`, `apps/mobile/data/realtime/issue-ws-updaters.ts`, `apps/mobile/components/inbox/swipeable-inbox-row.tsx` all resolve to real files.
- `multica-mentioning/SKILL.md`'s regex claim (`(member|agent|squad|issue|all)/([0-9a-fA-F-]+|all)`) matches the literal `MentionRe` at `server/internal/util/mention.go:16` verbatim.
- No terminology drift or orphaned components detected across the 11 artifacts — the `multica-*` skill family and both `CLAUDE.md` files consistently use the same nouns (`agent`, `squad`, `runtime`, `autopilot`, `project resource`) with matching definitions throughout.

## Recommendation
BLOCKED — do not submit PRs. File private security report covering the Critical curl-pipe-shell installer pattern and the four High findings (missing release-binary integrity check, sudo usage, PATH modification, postinstall scripts). The two NL bugs and one quality issue, plus the two Medium/Low security fixes, are recorded above for future reference once the security gate clears manual review.
