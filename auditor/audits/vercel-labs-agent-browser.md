# NLPM Audit: vercel-labs/agent-browser
**Date**: 2026-05-13  |  **Artifacts**: 7  |  **Strategy**: single
**NL Score**: 99/100
**Security**: BLOCKED
**Bugs**: 0  |  **Quality Issues**: 2  |  **Security Findings**: 6

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skill-data/dogfood/SKILL.md | skill | 97 | `Bash(npx agent-browser:*)` in allowed-tools contradicts body prohibition of npx |
| skill-data/vercel-sandbox/SKILL.md | skill | 98 | No `allowed-tools` declared; inconsistent with all five other SKILL.md files |
| skill-data/agentcore/SKILL.md | skill | 100 | — |
| skill-data/core/SKILL.md | skill | 100 | — |
| skill-data/electron/SKILL.md | skill | 100 | — |
| skill-data/slack/SKILL.md | skill | 100 | — |
| skills/agent-browser/SKILL.md | skill | 100 | — |

**Weighted average**: 695 / 7 = **99/100**

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 3 |
| Medium | 2 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts (.sh, .js) | 10 — scripts/build-all-platforms.sh, scripts/check-version-sync.js, scripts/copy-native.js, scripts/postinstall.js, scripts/sync-version.js, scripts/windows-debug/provision.sh, scripts/windows-debug/run.sh, scripts/windows-debug/start.sh, scripts/windows-debug/stop.sh, scripts/windows-debug/sync.sh |
| MCP configs | 0 |
| Package manifests | 1 — package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH | package.json | 25 | SEC-postinstall-script | `postinstall` lifecycle hook auto-runs `node scripts/postinstall.js` on every `npm install`; script downloads native binary over network and rewrites global bin entries |
| 2 | HIGH | scripts/postinstall.js | 258 | SEC-file-write-outside-repo | `symlinkSync` replaces the `agent-browser` symlink in npm global bin dir (`$npm_prefix/bin/`), a system PATH directory outside the repo |
| 3 | HIGH | scripts/postinstall.js | 301 | SEC-file-write-outside-repo | `writeFileSync` overwrites `.cmd` and `.ps1` shims in the Windows global npm prefix dir outside the package |
| 4 | MEDIUM | scripts/postinstall.js | 49 | SEC-network-download | Downloads platform-specific native binary from GitHub Releases over HTTPS; URL uses `package.json` version; no checksum verification before `chmodSync` |
| 5 | MEDIUM | scripts/postinstall.js | 27 | SEC-shell-true | `execSync('ldd --version 2>&1 \|\| true', ...)` — command string is fully hardcoded (false positive; noted for pattern awareness) |
| 6 | LOW | scripts/windows-debug/run.sh | 25 | SEC-shell-true | `$*` captured and forwarded as a PowerShell command to remote EC2 via AWS SSM; intentional developer debug tool, not a user-facing surface |

## Bugs (PR-worthy)
No NL bugs found. All seven SKILL.md files contain the required `name` and `description` frontmatter fields and carry no broken internal references.

## Security Fixes (PR-worthy, Medium/Low only)
*Blocked: do not open PRs while security status is BLOCKED. Suggestions below are for reference only.*

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/postinstall.js | Binary download has no integrity check before `chmodSync` (finding #4) | Publish SHA256 checksums alongside GitHub Releases and verify before executing |
| 2 | scripts/windows-debug/run.sh | No usage warning that all args execute as remote PowerShell (finding #6) | Add a header comment or `echo` warning naming the target instance before running |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skill-data/dogfood/SKILL.md | `allowed-tools` declares `Bash(npx agent-browser:*)` but the body (line 25) explicitly prohibits npx: "Always use `agent-browser` directly — never `npx agent-browser`." The declared tool can never be used as instructed. | −3 |
| 2 | skill-data/vercel-sandbox/SKILL.md | No `allowed-tools` field in frontmatter. All five comparable SKILL.md files (`agentcore`, `core`, `dogfood`, `electron`, `slack`) declare `Bash(agent-browser:*)`. The omission may be intentional (this skill teaches TypeScript SDK patterns, not direct CLI invocations), but it breaks the pattern and leaves tool access unrestricted. | −2 |

## Cross-Component
- **Skill cross-references** (`skills/agent-browser/SKILL.md` → five specialized skills): all five names (`electron`, `slack`, `dogfood`, `vercel-sandbox`, `agentcore`) resolve to existing `skill-data/<name>/SKILL.md` files. ✓
- **Subdirectory references** (`core`, `dogfood`, `slack`): `references/` and `templates/` subdirectories confirmed present for each skill that names them. ✓
- **CLI-served references** (`references/authentication.md`, `references/trust-boundaries.md`, etc. in `core/SKILL.md`): these are not repo files; they are served by the installed CLI via `agent-browser skills get core --full`. This is the documented design and not a broken reference. ✓
- **`{SKILL_DIR}` placeholder** in `dogfood/SKILL.md` line 47: runtime-resolved by the CLI; the target file (`skill-data/dogfood/templates/dogfood-report-template.md`) exists in the repo. ✓
- No orphaned components. No terminology drift across skill files.

## Recommendation
BLOCKED — do not submit PRs. File a private security report covering findings #1–3.

**Context**: The HIGH findings (postinstall hook, global-bin symlink replacement, Windows shim overwrite) are consistent with the standard npm pattern used by every native-binary npm package (esbuild, sharp, pnpm, etc.). No malicious code was detected; there is no credential exfiltration, eval injection, or curl-pipe-sh pattern. The recommended private disclosure is to confirm:

1. Whether SHA256 checksums are published for release binaries (and if not, to add them — see Medium finding #4).
2. Whether the maintainers want the postinstall behavior documented more prominently in the README for security-sensitive users.

Once the private security channel confirms no concerns with the binary distribution design, this repo may be re-evaluated for CLEAR status and the two Quality Issues (dogfood's npx contradiction, vercel-sandbox's missing `allowed-tools`) would each make straightforward one-line PRs.
