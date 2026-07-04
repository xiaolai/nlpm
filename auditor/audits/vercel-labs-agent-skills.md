# NLPM Audit: vercel-labs/agent-skills
**Date**: 2026-04-06  |  **Artifacts**: 9  |  **Strategy**: single
**NL Score**: 99/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 1  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/vercel-cli-with-tokens/SKILL.md | skill | 90 | Missing explicit output/response-format section (-10) |
| skills/composition-patterns/SKILL.md | skill | 100 | None — clean |
| skills/deploy-to-vercel/SKILL.md | skill | 100 | None — clean |
| skills/react-best-practices/SKILL.md | skill | 100 | None — clean (70/70 rule files indexed) |
| skills/react-native-skills/SKILL.md | skill | 100 | 3 rule files exist on disk but aren't listed in Quick Reference (cross-component, not scored) |
| skills/react-view-transitions/SKILL.md | skill | 100 | None — clean |
| skills/vercel-optimize/SKILL.md | skill | 100 | None — clean |
| skills/web-design-guidelines/SKILL.md | skill | 100 | Fetches rules from unpinned `main` ref each run (see Security) |
| skills/writing-guidelines/SKILL.md | skill | 100 | Fetches rules from unpinned `main` ref each run (see Security) |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 4 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none found |
| Scripts (shell, no-auth deploy fallback) | `skills/deploy-to-vercel/resources/deploy.sh`, `skills/deploy-to-vercel/resources/deploy-codex.sh` |
| Scripts (Node, vercel-optimize pipeline) | 15 files under `skills/vercel-optimize/scripts/`, ~50 files under `skills/vercel-optimize/lib/**` (spot-checked; all shell-outs use `execFile` with an argument array, never `shell: true` or string interpolation into a shell) |
| MCP configs | none found |
| Package manifests | `packages/react-best-practices-build/package.json` (build tooling, no `postinstall`), `packages/vercel-optimize-tests/package.json` (test runner, no `postinstall`) |
| Marketplace manifest | `skills.sh.json` |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | skills/deploy-to-vercel/resources/deploy.sh | 239 | network call (curl POST) | Packages the project directory into a tarball and uploads it via `curl -F file=@$TARBALL` to `https://claude-skills-deploy.vercel.com/api/deploy`. This is the script's documented purpose (no-auth deploy fallback); the packaging step already excludes `node_modules`, `.git`, `.env`, and `.env.*` (line 201-206) before upload, so no obvious secret-exfiltration path. Flagged for inventory completeness, not as a defect. |
| 2 | Medium | skills/deploy-to-vercel/resources/deploy-codex.sh | 239 | network call (curl POST) | Identical pattern targeting `https://codex-deploy-skills.vercel.sh/api/deploy`. Same mitigations apply (`.env`/`.git`/`node_modules` excluded from the tarball). |
| 3 | Medium | skills/web-design-guidelines/SKILL.md | 26 | unpinned remote fetch | Instructs the agent to `WebFetch` `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` "before each review" and treat the fetched content as the source of rules **and** output-format instructions. The ref is the mutable `main` branch, not a pinned commit or tag — a compromised or edited upstream file would silently change what the agent does and reports on every invocation, with no local record of what changed. |
| 4 | Medium | skills/writing-guidelines/SKILL.md | 26 | unpinned remote fetch | Same pattern: fetches `https://raw.githubusercontent.com/vercel-labs/writing-guidelines/main/command.md` on `main`, unpinned, treated as authoritative rules + output format. |

No Critical or High patterns found: no `eval`/`new Function` on variable input, no shell-piped-to-`sh`, no `shell: true` or `os.system`/raw `subprocess`, no reverse shells, no base64-decode-and-exec, no credential exfiltration, no `postinstall` scripts. All Node-based CLI invocations in `skills/vercel-optimize/lib/vercel.mjs` and `lib/verify-claim.mjs` use `execFile`/`execFileP` with argument arrays (never a shell), and the file explicitly documents this choice in a comment (`lib/vercel.mjs:1`). `skills/vercel-cli-with-tokens/SKILL.md` explicitly instructs agents never to pass tokens as CLI flags or embed them in echoed commands.

## Bugs (PR-worthy)
No NL bugs found — all 9 SKILL.md files have complete required frontmatter (`name`, `description`), and every relative file reference checked (rule files, `references/*.md`, `resources/*.sh`, `lib/*.mjs`, `scripts/*.mjs`) resolves to a file that exists on disk.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | skills/web-design-guidelines/SKILL.md | Fetches instructions from mutable `main` ref | Pin the fetch URL to a specific commit SHA or release tag of `vercel-labs/web-interface-guidelines`, and bump it deliberately when the upstream guidelines change. |
| 2 | skills/writing-guidelines/SKILL.md | Fetches instructions from mutable `main` ref | Same fix: pin `vercel-labs/writing-guidelines`'s fetch URL to a commit SHA or release tag instead of `main`. |

The two `deploy.sh` / `deploy-codex.sh` network calls (Security Findings #1–#2) are not included here — the network call *is* the deploy skill's core function, and the tarball already excludes secrets before upload. There is no code change to recommend beyond what's already in place.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/vercel-cli-with-tokens/SKILL.md | No explicit section telling the agent what to show the user after a deploy/env/domain operation, unlike its sibling `deploy-to-vercel/SKILL.md`, which has a dedicated `## Output` section | -10 |

## Cross-Component
- **Orphaned rule files** — `skills/react-native-skills/SKILL.md`'s Quick Reference table lists 33 rules, but `skills/react-native-skills/rules/` contains 36 non-template files. Three rules are undocumented and effectively undiscoverable to an agent that only reads the SKILL.md quick reference: `design-system-compound-components.md`, `scroll-position-no-state.md`, `state-ground-truth.md`. (`react-best-practices/SKILL.md` claims "70 rules" and the `rules/` directory has exactly 70 non-template files — no drift there; `composition-patterns/SKILL.md` lists 8 rules against 8 files on disk — also exact.)
- **Marketplace listing gap** — `skills.sh.json` groups 8 skills into "React" / "Vercel" / "Design" categories but omits `writing-guidelines`, even though it is a complete, valid skill directory (has its own `SKILL.md`, matches the same author/version conventions as `web-design-guidelines`, its closest sibling). It won't surface to `npx skills add` marketplace browsing.
- No broken relative links, no terminology drift in the `deploy-to-vercel` / `vercel-cli-with-tokens` shared vocabulary (both consistently use "preview deployment", "linked project", `.vercel/project.json` / `.vercel/repo.json`), and no contradictions found between sibling skills.

## Recommendation
CLEAR — submit PRs for the cross-component gaps (add the 3 missing rules to `react-native-skills/SKILL.md`'s Quick Reference; add `writing-guidelines` to `skills.sh.json`), the quality fix (add an Output section to `vercel-cli-with-tokens/SKILL.md`), and the two medium security fixes (pin the `web-design-guidelines` / `writing-guidelines` remote fetch URLs to a commit SHA instead of `main`). No Critical/High security issues found; no private disclosure needed.
