# NLPM Audit: Manavarya09/design-extract
**Date**: 2026-04-06  |  **Artifacts**: 11  |  **Strategy**: single
**NL Score**: 94/100
**Security**: BLOCKED
**Bugs**: 0  |  **Quality Issues**: 15  |  **Security Findings**: 16

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/extract.md | command | 83 | Multi-step post-run flow uses bullets, not numbered steps; vague "tight summary" |
| commands/remix.md | command | 85 | Multi-step post-run flow in prose, no numbered steps |
| commands/pair.md | command | 93 | Missing allowed-tools; vague "most distinctive crossover" |
| commands/battle.md | command | 95 | Missing allowed-tools |
| commands/brand.md | command | 95 | Missing allowed-tools |
| commands/grade.md | command | 95 | Missing allowed-tools |
| commands/pack.md | command | 95 | Missing allowed-tools |
| commands/theme-swap.md | command | 95 | Missing allowed-tools |
| skills/extract-design/SKILL.md | skill | 96 | Vague quantifiers: "key findings", "notable design decisions" |
| website/CLAUDE.md | context | 98 | Vague "relevant guide" in included AGENTS.md |
| .claude-plugin/plugin.json | manifest | 100 | — |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 9 |
| Medium | 1 |
| Low | 6 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts (.sh) | 1 — raycast-extension/scripts/dev-setup.sh |
| Scripts (.js, .py) | 111+ in src/, 1 in bin/ (not individually scanned) |
| MCP configs | 0 |
| Package manifests | 1 — package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH | package.json | 11 | SEC-postinstall-script | postinstall auto-runs `npx playwright install chromium --with-deps` on every `npm install`; `--with-deps` triggers OS-level system package installation (apt/brew) and may invoke sudo on Linux |
| 2 | HIGH | commands/battle.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang battle $ARGUMENTS` without quoting or sanitization; malformed or adversarial input can inject arbitrary shell commands |
| 3 | HIGH | commands/brand.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang brand $ARGUMENTS` without quoting or sanitization |
| 4 | HIGH | commands/extract.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang $ARGUMENTS` without quoting or sanitization |
| 5 | HIGH | commands/grade.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang grade $ARGUMENTS` without quoting or sanitization |
| 6 | HIGH | commands/pack.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang pack $ARGUMENTS` without quoting or sanitization |
| 7 | HIGH | commands/pair.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang pair $ARGUMENTS` without quoting or sanitization |
| 8 | HIGH | commands/remix.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang remix $ARGUMENTS` without quoting or sanitization |
| 9 | HIGH | commands/theme-swap.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang theme-swap $ARGUMENTS` without quoting or sanitization |
| 10 | MEDIUM | raycast-extension/scripts/dev-setup.sh | 43 | SEC-network-call | git clone from hardcoded external GitHub URL (`https://github.com/Manavarya09/extensions.git`) runs at developer setup time; could pull attacker-controlled code if the fork is compromised |
| 11 | LOW | package.json | 15 | SEC-unpinned-semver | `@modelcontextprotocol/sdk: ^1.29.0` — caret allows automatic minor/patch upgrades |
| 12 | LOW | package.json | 16 | SEC-unpinned-semver | `chalk: ^5.3.0` — caret allows automatic minor/patch upgrades |
| 13 | LOW | package.json | 17 | SEC-unpinned-semver | `commander: ^12.0.0` — caret allows automatic minor/patch upgrades |
| 14 | LOW | package.json | 18 | SEC-unpinned-semver | `ora: ^8.0.0` — caret allows automatic minor/patch upgrades |
| 15 | LOW | package.json | 19 | SEC-unpinned-semver | `playwright: ^1.42.0` — caret allows automatic minor/patch upgrades |
| 16 | LOW | raycast-extension/scripts/dev-setup.sh | 49 | SEC-audit-suppressed | `npm install --no-audit` suppresses npm's built-in security advisory check |

## Bugs (PR-worthy)
No NL artifact bugs found. All required frontmatter fields present; no broken cross-references.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | raycast-extension/scripts/dev-setup.sh | git clone from external fork without integrity verification (MEDIUM) | Pin to a specific commit SHA instead of a branch name: `git clone --depth=1 ... -b add-designlang-extension ... && git -C ... checkout <sha>` |
| 2 | package.json | Five caret-pinned npm dependencies (LOW) | Lock to exact versions in package.json (remove `^`) and commit package-lock.json; run `npm ci` in CI |
| 3 | raycast-extension/scripts/dev-setup.sh | `--no-audit` suppresses npm security scan (LOW) | Remove `--no-audit`; resolve any advisories that surface |

Note: Findings #1 (postinstall) and #2–9 (shell injection) are HIGH severity. Per policy, these require private disclosure and must not be filed as public PRs.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/battle.md | Missing `allowed-tools` frontmatter field | -5 |
| 2 | commands/brand.md | Missing `allowed-tools` frontmatter field | -5 |
| 3 | commands/extract.md | Missing `allowed-tools` frontmatter field | -5 |
| 4 | commands/extract.md | Multi-step post-run flow (run → read → summarize → offer follow-ups) uses bullet prose instead of numbered steps | -10 |
| 5 | commands/extract.md | "tight summary" — vague quantifier | -2 |
| 6 | commands/grade.md | Missing `allowed-tools` frontmatter field | -5 |
| 7 | commands/pack.md | Missing `allowed-tools` frontmatter field | -5 |
| 8 | commands/pair.md | Missing `allowed-tools` frontmatter field | -5 |
| 9 | commands/pair.md | "most distinctive crossover" — vague quantifier | -2 |
| 10 | commands/remix.md | Missing `allowed-tools` frontmatter field | -5 |
| 11 | commands/remix.md | Multi-step post-run flow (read index → tell user → offer --open) described in prose, no numbered steps | -10 |
| 12 | commands/theme-swap.md | Missing `allowed-tools` frontmatter field | -5 |
| 13 | skills/extract-design/SKILL.md | "key findings" — "key" is a vague quantifier | -2 |
| 14 | skills/extract-design/SKILL.md | "notable design decisions" — "notable" is a vague quantifier | -2 |
| 15 | website/CLAUDE.md | "relevant guide" in included AGENTS.md — "relevant" is a vague quantifier | -2 |

## Cross-Component
- All 8 command files reference `npx designlang <subcommand>` — the CLI package declared in `package.json` as `"designlang"` with bin `./bin/design-extract.js`. References are consistent.
- `plugin.json` declares `"commands": "./commands/"` and `"skills": "./skills/"`. Both directories exist with the expected artifacts.
- `skills/extract-design/SKILL.md` references `npx designlang <url> --screenshots` and specific output file patterns; these align with what the commands describe.
- `website/CLAUDE.md` delegates entirely to `@AGENTS.md` — a valid include, but the delegated content is a single-paragraph note; no broken reference.
- No orphaned components. No circular references. No contradictions between the plugin manifest and the command/skill set.

## Recommendation
BLOCKED — do not submit PRs. File private security report.

The eight slash commands pass `$ARGUMENTS` unquoted directly to the shell, enabling shell injection if an adversarial or malformed argument is supplied. The `postinstall` script in `package.json` runs OS-level system package installs automatically on `npm install` via `--with-deps`. Both are HIGH severity findings that require private disclosure before any public PR activity.

After the HIGH findings are resolved, one round of quality PRs would address: (a) adding `allowed-tools` to all eight commands, (b) converting the two prose post-run flows in `extract.md` and `remix.md` to numbered steps, and (c) the five vague-quantifier instances across three files.
