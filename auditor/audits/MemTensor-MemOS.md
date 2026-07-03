# NLPM Audit: MemTensor/MemOS
**Date**: 2026-04-06  |  **Artifacts**: 14  |  **Strategy**: single
**NL Score**: 89/100
**Security**: BLOCKED
**Bugs**: 2  |  **Quality Issues**: 18  |  **Security Findings**: 16

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/agents/explorer.md | Agent | 75 | Zero `<example>` blocks (R09) |
| apps/openwork-memos-integration/CLAUDE.md | Memory | 75 | Stale reference to non-existent `lib/accomplish.ts` (R37) |
| .claude/agents/design-reviewer.md | Agent | 78 | Zero `<example>` blocks (R09) |
| .claude/agents/backend-dev.md | Agent | 80 | Zero `<example>` blocks (R09) |
| .claude/agents/code-reviewer.md | Agent | 80 | Zero `<example>` blocks (R09) |
| .claude/agents/integration-tester.md | Agent | 80 | Zero `<example>` blocks (R09) |
| apps/memos-local-openclaw/site/public/SKILL.md | Skill | 92 | 4 vague quantifiers (R01) |
| apps/memos-local-openclaw/skill/memos-memory-guide/SKILL.md | Skill | 92 | 4 vague quantifiers (R01) |
| apps/memos-local-openclaw/skill/browserwing-executor/SKILL.md | Skill | 96 | 2 vague quantifiers (R01) |
| apps/memos-local-openclaw/skill/browserwing-admin/SKILL.md | Skill | 98 | 1 vague quantifier (R01) |
| CLAUDE.md | Memory | 100 | Clean |
| apps/openwork-memos-integration/apps/desktop/skills/ask-user-question/SKILL.md | Skill | 100 | Clean |
| apps/openwork-memos-integration/apps/desktop/skills/dev-browser/SKILL.md | Skill | 100 | Clean |
| apps/openwork-memos-integration/apps/desktop/skills/safe-file-deletion/SKILL.md | Skill | 100 | Clean |

Weighted average (simple mean across 14 artifacts): **89/100**.

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 6 |
| High | 6 |
| Medium | 3 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 (no `hooks/` directory anywhere in the repo) |
| Scripts | `scripts/check_dependencies.py` (repo root); ~45 files under `evaluation/scripts/**` (eval harnesses, no execution risk found); per-app `scripts/` dirs under `apps/memos-local-openclaw/`, `apps/memos-local-plugin/`, `apps/MemOS-Cloud-OpenClaw-Plugin/` (postinstall.cjs, native-binding.cjs, generate-telemetry-credentials.cjs, sync-version.js, copy-runtime-assets.cjs, plus dev-only `.ts` scripts) |
| Installers | `apps/memos-local-openclaw/install.sh` + `install.ps1`; `apps/memos-local-plugin/install.sh` + `install.ps1` + `adapters/{openclaw,hermes}/install.*.sh`; `apps/memos-local-openclaw/tests/verify-npm-package.sh` |
| MCP configs | 0 (`.mcp.json` not present anywhere in the repo) |
| package.json manifests | 9 (`apps/MemOS-Cloud-OpenClaw-Plugin`, `apps/memos-local-openclaw`, `apps/memos-local-plugin`, `apps/openwork-memos-integration` + 3 nested, 2 desktop skill packages) — 2 declare a `postinstall` script |
| requirements.txt | `docker/requirements.txt` (128 packages, all exact-pinned) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | apps/memos-local-openclaw/site/public/SKILL.md | 500 | curl-pipe-to-shell | `curl -fsSL https://cdn.memtensor.com.cn/memos-local-openclaw/install.sh \| bash` run as an unattended fallback installer with no checksum/signature verification |
| 2 | Critical | apps/memos-local-openclaw/site/public/SKILL.md | 505 | irm-pipe-iex | `irm https://cdn.memtensor.com.cn/memos-local-openclaw/install.ps1 \| iex` — PowerShell equivalent of curl\|bash, same lack of verification |
| 3 | Critical | apps/memos-local-openclaw/site/public/SKILL.md | 1182 | curl-pipe-to-shell | Same install.sh curl\|bash pattern repeated in the "Update" section |
| 4 | Critical | apps/memos-local-openclaw/site/public/SKILL.md | 1187 | irm-pipe-iex | Same irm\|iex pattern repeated in the "Update" section |
| 5 | Critical | apps/memos-local-openclaw/install.sh | 93 | download-then-exec-as-root | Downloads NodeSource's `setup_22.x` script over HTTPS to a temp file and immediately runs it via `bash` under `sudo`/root — functionally equivalent risk to curl\|bash with a file in between |
| 6 | Critical | apps/memos-local-plugin/install.sh | 178 | download-then-exec-as-root | Same NodeSource download-then-`run_with_privilege bash` pattern |
| 7 | High | apps/memos-local-openclaw/install.sh | 44 | sudo usage | `run_with_privilege()` transparently escalates any command to `sudo "$@"` whenever not already root |
| 8 | High | apps/memos-local-plugin/install.sh | 152 | sudo usage | Same `sudo "$@"` escalation helper |
| 9 | High | apps/memos-local-openclaw/package.json | 36 | postinstall script | `"postinstall": "node scripts/postinstall.cjs"` runs unattended on every `npm install`, including transitive installs |
| 10 | High | apps/memos-local-plugin/package.json | 63 | postinstall script | Same postinstall pattern (this package's script is a documented no-op unless `MEMOS_FORCE_POSTINSTALL=1`, which lowers practical risk) |
| 11 | High | apps/memos-local-openclaw/site/public/SKILL.md | 124 | pre-authorized remote-code-execution | "Granted permissions" section pre-authorizes the agent to run `curl \| bash` / `irm \| iex` installers "without further approval," removing the human-confirmation gate that would normally sit in front of finding #1 |
| 12 | High | apps/memos-local-openclaw/skill/browserwing-admin/SKILL.md | 52 | exposed remote-debugging port | Documents launching Chrome with `--remote-debugging-address=0.0.0.0 --no-sandbox`, exposing the full DevTools Protocol (arbitrary JS execution, file access) to the entire network with no authentication |
| 13 | Medium | apps/memos-local-openclaw/skill/browserwing-admin/SKILL.md | 28 | unverified network content piped to sudo | `wget -q -O - ... \| sudo apt-key add -` imports a network-fetched signing key directly into root's trusted keyring with no shown fingerprint check; `apt-key` is also deprecated by Debian/Ubuntu |
| 14 | Medium | apps/memos-local-openclaw/site/public/SKILL.md | 697 | obfuscated command construction | Builds the strings `child_process` / `openclaw gateway restart` via `String.fromCharCode(...)` specifically to dodge shell quoting — the same technique used to evade naive static-pattern security scanning, even though the surrounding comment states the intent is cross-platform quote-escaping |
| 15 | Medium | apps/memos-local-openclaw/site/public/SKILL.md | 465 | registry override / supply-chain | Falls back to `NPM_CONFIG_REGISTRY=https://registry.npmmirror.com`, installing the plugin from a third-party mirror instead of the default npm registry with no integrity pinning mentioned |
| 16 | Low | apps/memos-local-openclaw/package.json | 51 | unpinned dependency versions | Runtime dependencies (`puppeteer`, `better-sqlite3`, `@huggingface/transformers`, etc.) use caret ranges rather than exact pins, allowing silent minor/patch drift on fresh installs |

**Context note:** findings 1–12 are all part of the documented, intentional install/update flow for a legitimate open-source memory plugin, not evidence of a backdoor. They are still scored per the strict severity taxonomy this audit uses (curl\|bash and unattended download-then-execute-as-root are defined as Critical regardless of publisher intent), because the *mechanism* — unauthenticated remote code fetched and run with elevated privilege, explicitly pre-authorized without human confirmation — is exactly the mechanism a genuinely malicious skill would use.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | apps/openwork-memos-integration/CLAUDE.md | Line 51 references `lib/accomplish.ts`; no file of that name exists anywhere under `apps/desktop/src/renderer/` | Anyone (human or agent) using CLAUDE.md as a map of the IPC wrapper layer hits a dead path |
| 2 | apps/openwork-memos-integration/CLAUDE.md | Line 107 references `apps/desktop/playwright.config.ts`; the file actually lives at `apps/desktop/e2e/playwright.config.ts` | Running the documented test-config path fails; the real E2E config is one directory deeper |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | apps/memos-local-openclaw/skill/browserwing-admin/SKILL.md:28 | `wget` output piped straight into `sudo apt-key add -` with no fingerprint check shown | Switch to `gpg --dearmor` into `/etc/apt/keyrings/` with a documented fingerprint check, per Google's current signed-by instructions (`apt-key` is deprecated) |
| 2 | apps/memos-local-openclaw/site/public/SKILL.md:697 | `String.fromCharCode(...)` obfuscation to build `child_process`/`openclaw gateway restart` | Use `execFile('openclaw', ['gateway', 'restart'])` with an argv array — sidesteps shell quoting entirely without character-code obfuscation |
| 3 | apps/memos-local-openclaw/site/public/SKILL.md:465 | Silent fallback to `registry.npmmirror.com` with no integrity note | Document that the mirror is best-effort only, and verify the installed package's integrity hash after falling back to it |
| 4 | apps/memos-local-openclaw/package.json (deps, ~line 51) | Security-sensitive deps (`puppeteer`, `better-sqlite3`) pinned with `^` ranges | Rely on the committed lockfile for reproducible installs, and consider exact pins for `puppeteer` / `better-sqlite3` specifically |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/agents/backend-dev.md | No `model:` field in frontmatter (R10) | -5 |
| 2 | .claude/agents/code-reviewer.md | No `model:` field in frontmatter (R10) | -5 |
| 3 | .claude/agents/design-reviewer.md | No `model:` field in frontmatter (R10) | -5 |
| 4 | .claude/agents/explorer.md | No `model:` field in frontmatter (R10) | -5 |
| 5 | .claude/agents/integration-tester.md | No `model:` field in frontmatter (R10) | -5 |
| 6 | .claude/agents/backend-dev.md | Zero `<example>` blocks, minimum is 2 (R09) | -15 |
| 7 | .claude/agents/code-reviewer.md | Zero `<example>` blocks (R09) | -15 |
| 8 | .claude/agents/design-reviewer.md | Zero `<example>` blocks (R09) | -15 |
| 9 | .claude/agents/explorer.md | Zero `<example>` blocks (R09) | -15 |
| 10 | .claude/agents/integration-tester.md | Zero `<example>` blocks (R09) | -15 |
| 11 | .claude/agents/design-reviewer.md:14 | Vague quantifier "appropriate extras" (R01) | -2 |
| 12 | .claude/agents/explorer.md:11 | Vague quantifier "relevant modules" (R01) | -2 |
| 13 | .claude/agents/explorer.md | `Bash` declared in `tools:` but never referenced by the body, which only describes Read/Grep/Glob-based tracing (R11) | -3 |
| 14 | apps/memos-local-openclaw/site/public/SKILL.md | 4 vague quantifiers: "relevant" (167), "typically" (460), "if needed" (1099), "usually" (1109) (R01) | -8 |
| 15 | apps/memos-local-openclaw/skill/memos-memory-guide/SKILL.md | 4 vague quantifiers: "relevant" ×4 (37, 45, 60, 174) (R01) | -8 |
| 16 | apps/memos-local-openclaw/skill/browserwing-admin/SKILL.md:353 | Vague quantifier "if needed" (R01) | -2 |
| 17 | apps/memos-local-openclaw/skill/browserwing-executor/SKILL.md | 2 vague quantifiers: "if needed" (442), "appropriate" (460) (R01) | -4 |
| 18 | apps/openwork-memos-integration/CLAUDE.md:49 | `pages/` is described as including a "Settings" page; no `Settings.tsx` exists under `pages/` — settings is implemented as `components/layout/SettingsDialog.tsx` (R37) | -5 |

## Cross-Component
- `CLAUDE.md` (root) → `.claude/agents/*.md`: the five agents listed in the root CLAUDE.md table (`explorer`, `design-reviewer`, `code-reviewer`, `backend-dev`, `integration-tester`) all exist with matching read-only/read-write tool grants — consistent.
- `CLAUDE.md` (root) → `AGENTS.md`: `AGENTS.md` exists at repo root — reference resolves.
- `CLAUDE.md` (root) → `docs/openapi.json`: not present on disk, but the Makefile's `openapi` target (`poetry run memos export_openapi --output docs/openapi.json`) generates it on demand — not a broken reference, just an artifact that doesn't ship pre-built.
- `apps/openwork-memos-integration/CLAUDE.md` → `apps/desktop/src/renderer/lib/accomplish.ts` and `apps/desktop/playwright.config.ts`: both stale (see Bugs #1–#2).
- `apps/openwork-memos-integration/CLAUDE.md` "pages/" description vs. actual renderer layout: "Settings" is a dialog component, not a page file (see Quality Issue #18) — a terminology drift rather than a hard break, but worth tightening since it's the kind of description mismatch that compounds into real broken links over time.
- `apps/memos-local-openclaw/site/public/SKILL.md` → bundled `memos-memory-guide` skill: paths (`~/.openclaw/workspace/skills/memos-memory-guide/`, `~/.openclaw/skills/memos-memory-guide/`) match what `scripts/postinstall.cjs` actually writes (`installBundledSkill()`) — consistent, no drift.
- No orphaned components found among the 14 audited artifacts: every agent/skill referenced from a memory file has a corresponding file on disk.

## Recommendation
**BLOCKED — do not submit PRs. File private security report.**

Six Critical findings (unauthenticated curl\|bash / irm\|iex installers, plus two download-then-execute-as-root install scripts) and six High findings — including a SKILL.md section that explicitly pre-authorizes autonomous execution of those same Critical patterns without human confirmation — mean this repo's install/update flow needs private disclosure and maintainer discussion before any public PR. The two NL bugs (stale references in `apps/openwork-memos-integration/CLAUDE.md`) and the four Medium/Low security fixes are safe to include as follow-up PRs once the security conversation is underway, but should not be the first contact given the security-blocked state.
