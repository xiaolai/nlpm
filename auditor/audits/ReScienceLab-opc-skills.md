# NLPM Audit: ReScienceLab/opc-skills
**Date**: 2026-04-20  |  **Artifacts**: 23  |  **Strategy**: batched
**NL Score**: 92/100
**Security**: BLOCKED
**Bugs**: 1  |  **Quality Issues**: 10  |  **Security Findings**: 7

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| template/SKILL.md | SKILL | 85 | All fields are unfilled template placeholders; name: "skill-name" would break registration |
| skills/twitter/SKILL.md | SKILL | 90 | No output format shown; CLI output shape undocumented |
| skills/producthunt/SKILL.md | SKILL | 90 | No output format shown; no sample GraphQL response |
| skills/reddit/SKILL.md | SKILL | 90 | No output format shown; no sample JSON response |
| .agents/skills/seo-geo/SKILL.md | SKILL | 92 | Near-duplicate of skills/seo-geo/SKILL.md; only diff is triggers in frontmatter |
| skills/seo-geo/SKILL.md | SKILL | 92 | "Comprehensive" vague qualifier (-2); otherwise excellent |
| .factory/skills/add-new-opc-skill/SKILL.md | SKILL | 93 | "appropriate position" vague (-2) |
| skills/banner-creator/SKILL.md | SKILL | 93 | Minor: nanobanana dependency only named in prose, not frontmatter |
| skills/domain-hunter/SKILL.md | SKILL | 93 | "most reliable" vague (-2); otherwise well-structured |
| skills/archive/SKILL.md | SKILL | 95 | No inline example archive entry; references external template |
| skills/logo-creator/SKILL.md | SKILL | 95 | Well-structured; minor placeholder paths |
| skills/nanobanana/SKILL.md | SKILL | 96 | "good quality", "good prompts" vague (-4) |
| skills/requesthunt/SKILL.md | SKILL | 97 | Excellent structure and safety guidance; CRITICAL security pattern in install docs |
| skills/archive/hooks/hooks.json | Config | 100 | Valid hook configuration |
| skills/twitter/.claude-plugin/plugin.json | Config | 100 | Valid plugin manifest |
| skills/seo-geo/.claude-plugin/plugin.json | Config | 100 | Valid plugin manifest |
| skills/banner-creator/.claude-plugin/plugin.json | Config | 100 | Valid plugin manifest |
| skills/domain-hunter/.claude-plugin/plugin.json | Config | 100 | Valid plugin manifest |
| skills/nanobanana/.claude-plugin/plugin.json | Config | 100 | Valid plugin manifest |
| skills/requesthunt/.claude-plugin/plugin.json | Config | 100 | Valid plugin manifest |
| skills/logo-creator/.claude-plugin/plugin.json | Config | 100 | Valid plugin manifest |
| skills/producthunt/.claude-plugin/plugin.json | Config | 100 | Valid plugin manifest |
| skills/reddit/.claude-plugin/plugin.json | Config | 100 | Valid plugin manifest |

_NL Score = weighted average of 13 SKILL.md artifacts (config files excluded from NL scoring)._

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 1 |
| Medium | 4 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | skills/archive/hooks/hooks.json, skills/archive/hooks/load-memory.py |
| Scripts (Python) | 63 .py files across skills/twitter/, skills/seo-geo/, skills/producthunt/, skills/reddit/, skills/nanobanana/, skills/banner-creator/, skills/logo-creator/ |
| MCP configs | None |
| Package manifests | website/package.json |
| Requirements files | None |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | CRITICAL | skills/requesthunt/SKILL.md | 15 | curl-pipe-sh | Documents `curl -fsSL https://requesthunt.com/cli \| sh` as the install command. Even though the note says the script verifies SHA256 of downloaded binaries, the install script itself executes unverified remote code. Promotes an unsafe install pattern to all skill users. |
| 2 | HIGH | skills/logo-creator/scripts/remove_bg.py | 29–35 | sensitive file read + credential extraction | When `REMOVE_BG_API_KEY` is absent from the environment, the script runs `subprocess.run(['grep', 'REMOVE_BG_API_KEY', os.path.expanduser('~/.zshrc')])` and extracts the key with `.split('"')[1]`. This reads a sensitive shell config file outside the project scope and parses credentials with fragile string splitting — could accidentally expose adjacent secrets if the grep output contains multiple quoted values. |
| 3 | MEDIUM | skills/logo-creator/scripts/remove_bg.py | 48–59 | subprocess network call | `subprocess.run(['curl', '-H', f'X-Api-Key: {api_key}', ...])` calls remove.bg API. The API key is interpolated into the subprocess argument list (not shell=True), which is safe, but the API key appears in the process argument list visible via `ps aux`. |
| 4 | MEDIUM | skills/archive/hooks/load-memory.py | 13–23 | content injection via hook | The SessionStart hook reads `.archive/MEMORY.md` and injects its full contents verbatim into the agent's `additionalContext` with no sanitization. If `.archive/MEMORY.md` contains adversarial instructions (e.g., from a compromised or shared repo), they execute in the agent's context at session start. |
| 5 | MEDIUM | skills/twitter/scripts/twitter_api.py, skills/seo-geo/scripts/seo_audit.py, skills/producthunt/scripts/producthunt_api.py, skills/reddit/scripts/reddit_api.py | various | network calls | Multiple scripts make outbound HTTP requests using `urllib.request` to external APIs. This is expected behavior for API-wrapper skills, but represents an attack surface for SSRF if user-supplied URLs are passed without validation. `seo_audit.py` in particular accepts a user-supplied URL at line 91–93 and fetches it with minimal validation (only checks for `http` prefix). |
| 6 | LOW | website/package.json | 3 | unpinned dependency | `"marked": "^17.0.1"` uses a caret range, allowing automatic minor/patch upgrades. Should be pinned to an exact version for reproducible builds. |
| 7 | LOW | skills/archive/hooks/hooks.json | 1 | verbose hook trigger | SessionStart hook fires on every session start, loading `.archive/MEMORY.md` each time. If the archive grows large, this adds latency to every session regardless of whether the archive is relevant. Not a security issue but a resource concern. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | template/SKILL.md | `name: skill-name` in frontmatter is an unfilled placeholder. If a user installs the template directly (e.g., via `claude plugin install`) without editing, the skill registers under the literal name "skill-name", creating a registration collision and confusing trigger behavior. | Registration collision; obscures actual skill identity in plugin registries |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/logo-creator/scripts/remove_bg.py | Reads `~/.zshrc` to extract API key when env var is absent | Remove the `subprocess.run` grep fallback entirely (lines 28–36). The correct pattern is: print a clear error message directing users to `export REMOVE_BG_API_KEY=...` and exit. Reading shell config files is fragile, OS-specific, and a security anti-pattern. |
| 2 | skills/logo-creator/scripts/remove_bg.py | API key exposed in process argument list via `subprocess.run(['curl', '-H', f'X-Api-Key: {api_key}', ...])` | Replace `subprocess.run` curl call with `urllib.request` (already used elsewhere in the codebase). This keeps the key in memory, not the process table. |
| 3 | skills/archive/hooks/load-memory.py | Injects raw file content into agent context without sanitization | Add a size guard (e.g., truncate at 8 KB) and a comment in the output noting the content is user-authored project notes, not system instructions. This reduces prompt injection blast radius without breaking the feature. |
| 4 | skills/seo-geo/scripts/seo_audit.py | User-supplied URL fetched with only `url.startswith("http")` check | Validate URL is http/https with a proper parse: `urllib.parse.urlparse(url).scheme in ('http', 'https')`. Also reject URLs resolving to private/loopback addresses to prevent SSRF. |
| 5 | website/package.json | `"marked": "^17.0.1"` unpinned | Pin to exact version: `"marked": "17.0.1"` |

_(Critical and High findings #1 and #2 above require private disclosure — see Recommendation.)_

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | template/SKILL.md | All body content is instructional template prose ("Brief description", "List any setup requirements", "Important note 1") with no actual skill-specific content | -15 |
| 2 | skills/twitter/SKILL.md | No output format shown; users don't know what the scripts print | -10 |
| 3 | skills/producthunt/SKILL.md | No output format shown; GraphQL response shape undocumented | -10 |
| 4 | skills/reddit/SKILL.md | No output format shown; no sample post/comment shape | -10 |
| 5 | .agents/skills/seo-geo/SKILL.md | Near-identical duplicate of skills/seo-geo/SKILL.md; the only difference is the `triggers:` list in frontmatter. Two copies create maintenance drift risk. | -8 (design) |
| 6 | skills/seo-geo/SKILL.md | "Comprehensive SEO and GEO" — "comprehensive" is a vague claim | -2 |
| 7 | .factory/skills/add-new-opc-skill/SKILL.md | "Insert in the appropriate position within the existing table" — "appropriate" is underspecified; a rule like "alphabetical by skill name" would be concrete | -2 |
| 8 | skills/domain-hunter/SKILL.md | "most reliable" used to describe WHOIS method without citation | -2 |
| 9 | skills/nanobanana/SKILL.md | "good quality" (Standard option), "good prompts" (Best Practices) — both are vague | -4 |
| 10 | skills/archive/SKILL.md | No inline example of what a completed archive entry looks like; says "see references/TEMPLATE.md" but the template is not in the scanned files | -5 |

## Cross-Component

**Duplication — seo-geo**: `skills/seo-geo/SKILL.md` and `.agents/skills/seo-geo/SKILL.md` are identical except for `triggers:` frontmatter in the `.agents/` version. The plugin.json for seo-geo only declares `"skills": ["./SKILL.md"]` pointing at the `skills/` copy; the `.agents/` copy appears orphaned. Recommend merging: add `triggers:` to `skills/seo-geo/SKILL.md` frontmatter and delete the `.agents/` copy.

**Undeclared skill dependencies**: `banner-creator/SKILL.md` and `logo-creator/SKILL.md` both depend on `nanobanana` for image generation and call `<nanobanana_skill_dir>/scripts/...`, but neither their frontmatter nor their plugin.json declares this dependency. If `nanobanana` is not installed, both skills silently fail. The `domain-hunter` skill similarly depends on `twitter` and `reddit` skills (for promo code searches) without declaration.

**Unverified internal references**: Several SKILL.md files reference local `references/*.md` files (`platform-algorithms.md`, `geo-research.md`, `schema-templates.md`, `registrars.md`, `styles.md`, `TEMPLATE.md`, etc.) that were not included in the scan manifest. These references could not be verified as existing. If any are missing, the skill documentation has broken links.

**requesthunt version mismatch**: `skills/requesthunt/.claude-plugin/plugin.json` declares `"version": "2.0.0"`, but `skills/requesthunt/SKILL.md` contains no version reference. All other skills are at `1.0.0`. The jump to 2.0.0 without a changelog entry or frontmatter version creates ambiguity about what changed.

**Archive hook path assumption**: `skills/archive/hooks/load-memory.py` resolves the project directory from `FACTORY_PROJECT_DIR` or `CLAUDE_PROJECT_DIR` env vars, falling back to `os.getcwd()`. If neither env var is set and the hook is not invoked from the project root, `.archive/MEMORY.md` will not be found — silently succeeding (exit 0) with no output. This could cause confusing "missing memory" behavior in certain environments.

## Recommendation

**BLOCKED — do not submit PRs. File private security report.**

The CRITICAL finding (curl-pipe-sh in `skills/requesthunt/SKILL.md` line 15) and HIGH finding (credential extraction from `~/.zshrc` in `skills/logo-creator/scripts/remove_bg.py`) must be addressed privately before any public contribution.

**Private disclosure path:**
1. Report the `curl -fsSL https://requesthunt.com/cli | sh` pattern to ReScienceLab maintainers via their GitHub security advisory channel. Suggest replacing with a pinned-checksum install or direct binary download with explicit SHA256 verification before execution (not after).
2. Report the `~/.zshrc` credential extraction pattern — suggest removing the fallback entirely and requiring the `REMOVE_BG_API_KEY` env var to be set explicitly.

Once those two findings are resolved, the remaining Medium/Low security fixes (items 1–5 in Security Fixes) and the NL bug (template placeholder name) are safe to submit as a single PR. The overall NL quality is high (92/100) — this is a well-maintained skill collection with only minor structural gaps.
