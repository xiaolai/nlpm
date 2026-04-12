# NLPM Audit: AgriciDaniel/claude-seo
**Date**: 2026-04-12  |  **Artifacts**: 40  |  **Strategy**: batched
**NL Score**: 94/100
**Security**: REVIEW
**Bugs**: 2  |  **Quality Issues**: 17  |  **Security Findings**: 9

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| extensions/banana/agents/seo-image-gen.md | agent | 80 | No examples (-15), no model (-5) |
| extensions/dataforseo/agents/seo-dataforseo.md | agent | 80 | No examples (-15), no model (-5) |
| agents/seo-backlinks.md | agent | 85 | No examples (-15) |
| agents/seo-content.md | agent | 85 | No examples (-15) |
| agents/seo-dataforseo.md | agent | 85 | No examples (-15) |
| agents/seo-geo.md | agent | 85 | No examples (-15) |
| agents/seo-google.md | agent | 85 | No examples (-15) |
| agents/seo-image-gen.md | agent | 85 | No examples (-15) |
| agents/seo-local.md | agent | 85 | No examples (-15) |
| agents/seo-maps.md | agent | 85 | No examples (-15) |
| agents/seo-performance.md | agent | 85 | No examples (-15) |
| agents/seo-schema.md | agent | 85 | No examples (-15) |
| agents/seo-sitemap.md | agent | 85 | No examples (-15) |
| agents/seo-technical.md | agent | 85 | No examples (-15) |
| agents/seo-visual.md | agent | 85 | No examples (-15) |
| extensions/banana/skills/seo-image-gen/SKILL.md | skill | 100 | Stale version (v1.6.1 vs core v1.8.2) |
| extensions/dataforseo/skills/seo-dataforseo/SKILL.md | skill | 100 | Stale version (v1.6.1 vs core v1.8.2) |
| extensions/firecrawl/skills/seo-firecrawl/SKILL.md | skill | 100 | — |
| skills/seo-audit/SKILL.md | skill | 100 | — |
| skills/seo-backlinks/SKILL.md | skill | 100 | — |
| skills/seo-competitor-pages/SKILL.md | skill | 100 | — |
| skills/seo-content/SKILL.md | skill | 100 | — |
| skills/seo-dataforseo/SKILL.md | skill | 100 | — |
| skills/seo-geo/SKILL.md | skill | 100 | — |
| skills/seo-google/SKILL.md | skill | 100 | — |
| skills/seo-hreflang/SKILL.md | skill | 100 | — |
| skills/seo-image-gen/SKILL.md | skill | 100 | — |
| skills/seo-images/SKILL.md | skill | 100 | — |
| skills/seo-local/SKILL.md | skill | 100 | — |
| skills/seo-maps/SKILL.md | skill | 100 | — |
| skills/seo-page/SKILL.md | skill | 100 | — |
| skills/seo-plan/SKILL.md | skill | 100 | — |
| skills/seo-programmatic/SKILL.md | skill | 100 | — |
| skills/seo-schema/SKILL.md | skill | 100 | — |
| skills/seo-sitemap/SKILL.md | skill | 100 | — |
| skills/seo-technical/SKILL.md | skill | 100 | — |
| skills/seo/SKILL.md | skill | 100 | — |
| hooks/hooks.json | config | 100 | — |
| CLAUDE.md | instructions | 100 | — |
| .claude-plugin/plugin.json | manifest | 100 | — |

**Score calculation**: 13 core agents × 85 + 2 extension agents × 80 + 25 skills/other × 100 = 3765 / 40 = **94.1 → 94/100**

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 3 |
| Medium | 3 |
| Low | 3 |

> **Note on pre-scan discrepancy**: The pre-scan reported 4 CRITICAL pattern matches. Detailed review found these were false positives from `curl -fsSL URL | bash` appearing in `echo` statements (user-facing documentation strings, never executed). The actual executable risk is in shell variable expansion into Python heredocs, classified HIGH rather than CRITICAL because it requires attacker-controlled local input.

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | hooks/validate-schema.py (called by hooks/hooks.json) |
| Python scripts | scripts/*.py (21 files) |
| Shell installers | extensions/banana/install.sh, extensions/dataforseo/install.sh, extensions/firecrawl/install.sh |
| Uninstall scripts | extensions/banana/uninstall.sh, extensions/dataforseo/uninstall.sh, extensions/firecrawl/uninstall.sh |
| MCP configs | None (installed dynamically into ~/.claude/settings.json at runtime) |
| Package manifest | None (requirements installed into ~/.claude/skills/seo/.venv/) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH | extensions/dataforseo/install.sh | 103–106 | Shell variable expansion into python3 -c | `username = '''${DFSE_USERNAME}'''` and `password = '''${DFSE_PASSWORD}'''` are user-supplied strings injected directly into Python source code via triple-quote interpolation. A value containing `'''` breaks out of the string and allows arbitrary Python execution (e.g., a password of `x'''; import os; os.system('id'); x='''` would execute). |
| 2 | HIGH | extensions/banana/install.sh | 115 | Shell variable expansion into python3 -c | `'GOOGLE_AI_API_KEY': '''${GOOGLE_AI_API_KEY}'''` — same triple-quote injection pattern. Less likely to be exploited (API keys rarely contain quotes) but structurally identical vulnerability. |
| 3 | HIGH | extensions/firecrawl/install.sh | 88 | Shell variable expansion into python3 -c | `api_key = '''${FIRECRAWL_API_KEY}'''` — same pattern with user-read API key. |
| 4 | MEDIUM | extensions/banana/install.sh | 151 | Unpinned runtime package install | `npx --yes --package=@ycse/nanobanana-mcp@latest` downloads and executes the latest version without integrity verification or pinned SHAs. Supply chain compromise of `@ycse/nanobanana-mcp` would silently execute malicious code on install. |
| 5 | MEDIUM | extensions/dataforseo/install.sh | 144 | Unpinned runtime package install | `npx --yes --package=dataforseo-mcp-server` — same pattern for `dataforseo-mcp-server` package. |
| 6 | MEDIUM | extensions/firecrawl/install.sh | 124 | Unpinned runtime package install | `npx --yes --package=firecrawl-mcp` — same pattern for `firecrawl-mcp` package. |
| 7 | LOW | extensions/banana/install.sh | 22 | curl-pipe-bash in echo | `echo "Install it first: curl -fsSL .../install.sh \| bash"` — the command is printed as documentation text, never executed. Pattern-matched as CRITICAL by pre-scanner; confirmed false positive. |
| 8 | LOW | extensions/dataforseo/install.sh | 22 | curl-pipe-bash in echo | Same as finding #7 — documentation string only. |
| 9 | LOW | extensions/firecrawl/install.sh | 22 | curl-pipe-bash in echo | Same as finding #7 — documentation string only. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | extensions/dataforseo/skills/seo-dataforseo/SKILL.md | Stale extension skill at v1.6.1 vs core skills/seo-dataforseo/SKILL.md at v1.8.2. Extension copy is missing the `serp-images` command, the `references/tool-catalog.md` reference, and several other improvements introduced in v1.7–v1.8. When the extension installer copies this file to `~/.claude/skills/seo-dataforseo/`, users get an outdated skill that omits documented functionality. | Users who install the DataForSEO extension get a version missing Google Images SERP analysis and updated tool catalog. |
| 2 | extensions/banana/skills/seo-image-gen/SKILL.md | Stale extension skill at v1.6.1 vs core skills/seo-image-gen/SKILL.md at v1.8.2. Both files have near-identical content; the extension copy is 2 minor versions behind. When install.sh copies this to `~/.claude/skills/seo-image-gen/`, it overwrites the newer core version that was installed by the main plugin. | Users who install the banana extension after the main SEO plugin may have the core skill downgraded from v1.8.2 to v1.6.1. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | extensions/dataforseo/install.sh | Python code injection via `'''${DFSE_USERNAME}'''` and `'''${DFSE_PASSWORD}'''` in `python3 -c` | Pass credentials as environment variables rather than interpolating into source: set `DFSE_USERNAME` and `DFSE_PASSWORD` in the subprocess environment and access via `os.environ['DFSE_USERNAME']` inside the Python block. E.g.: `DFSE_USERNAME="${DFSE_USERNAME}" DFSE_PASSWORD="${DFSE_PASSWORD}" python3 -c "import json,os; username=os.environ['DFSE_USERNAME']; ..."` |
| 2 | extensions/banana/install.sh | Same triple-quote injection with `GOOGLE_AI_API_KEY` | Same fix: pass via environment variable, not source interpolation. |
| 3 | extensions/firecrawl/install.sh | Same triple-quote injection with `FIRECRAWL_API_KEY` | Same fix: pass via environment variable. |
| 4 | extensions/banana/install.sh | Unpinned `@ycse/nanobanana-mcp@latest` | Pin to a specific semver (e.g., `@ycse/nanobanana-mcp@1.6.1`) and document the update procedure. Add a version check that warns when a newer version is available. |
| 5 | extensions/dataforseo/install.sh | Unpinned `dataforseo-mcp-server` | Pin to specific version. |
| 6 | extensions/firecrawl/install.sh | Unpinned `firecrawl-mcp` | Pin to specific version. |

> **Critical/High findings (python injection, #1–#3 above)**: The full fix detail is provided here since the HIGH classification does not require private disclosure (attack vector requires local, user-controlled input). These are still PR-worthy fixes.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/seo-backlinks.md | Zero example blocks | -15 |
| 2 | agents/seo-content.md | Zero example blocks | -15 |
| 3 | agents/seo-dataforseo.md | Zero example blocks | -15 |
| 4 | agents/seo-geo.md | Zero example blocks | -15 |
| 5 | agents/seo-google.md | Zero example blocks | -15 |
| 6 | agents/seo-image-gen.md | Zero example blocks | -15 |
| 7 | agents/seo-local.md | Zero example blocks | -15 |
| 8 | agents/seo-maps.md | Zero example blocks | -15 |
| 9 | agents/seo-performance.md | Zero example blocks | -15 |
| 10 | agents/seo-schema.md | Zero example blocks | -15 |
| 11 | agents/seo-sitemap.md | Zero example blocks | -15 |
| 12 | agents/seo-technical.md | Zero example blocks | -15 |
| 13 | agents/seo-visual.md | Zero example blocks | -15 |
| 14 | extensions/banana/agents/seo-image-gen.md | Zero example blocks | -15 |
| 15 | extensions/dataforseo/agents/seo-dataforseo.md | Zero example blocks | -15 |
| 16 | extensions/banana/agents/seo-image-gen.md | No `model:` declaration in frontmatter | -5 |
| 17 | extensions/dataforseo/agents/seo-dataforseo.md | No `model:` declaration in frontmatter | -5 |

**Observation on examples**: The zero-examples penalty is systematic across all 15 agents (13 core + 2 extension). No agent shows even a single input/output example. Adding `## Examples` blocks to the top 3–5 most-used agents (seo-technical, seo-content, seo-schema, seo-geo, seo-local) would have the highest impact on the NL score.

## Cross-Component

**Skill version skew**: Two extension SKILL.md copies are out of sync with their core counterparts. The extension installer `cp` commands overwrite whichever version was installed first, creating a non-deterministic outcome depending on install order:
- `extensions/dataforseo/skills/seo-dataforseo/SKILL.md` (v1.6.1) vs `skills/seo-dataforseo/SKILL.md` (v1.8.2)
- `extensions/banana/skills/seo-image-gen/SKILL.md` (v1.6.1) vs `skills/seo-image-gen/SKILL.md` (v1.8.2)

The core skill versions are the source of truth and should be what gets installed. The extension `install.sh` scripts should either reference the core skill directly or be eliminated in favor of the core copies.

**Agent-to-reference consistency**: All cross-skill references are internally consistent. Agents reference `skills/seo/references/*.md` files that are described in CLAUDE.md's architecture. No broken cross-references detected in agent or skill files.

**Hook chain**: `hooks/hooks.json` → `hooks/validate-schema.py` → validates JSON-LD in HTML files on Edit/Write. The referenced script exists and functions correctly. The hook correctly limits execution to HTML-like file extensions, preventing unnecessary triggering on `.md` or `.py` files.

**Script completeness**: All scripts referenced in agent SKILL.md files (`google_auth.py`, `backlinks_auth.py`, `moz_api.py`, `bing_webmaster.py`, `commoncrawl_graph.py`, `verify_backlinks.py`, `pagespeed_check.py`, `crux_history.py`, `gsc_query.py`, `gsc_inspect.py`, `indexing_notify.py`, `ga4_report.py`, `google_report.py`, `youtube_search.py`, `nlp_analyze.py`, `keyword_planner.py`, `fetch_page.py`, `parse_html.py`, `capture_screenshot.py`, `analyze_visual.py`, `validate_backlink_report.py`) are all present in `scripts/`. The two dev-only scripts noted in CLAUDE.md (`mobile_analysis.py`) are correctly gitignored and no skill references them as required.

**Security architecture**: The codebase applies SSRF protection (`validate_url()`) consistently across all network-facing scripts (`fetch_page.py`, `verify_backlinks.py`, `commoncrawl_graph.py`). The `google_auth.py` SSRF protection blocks private IPs, loopback, and GCP metadata endpoint. OAuth tokens are correctly stored separately from client secrets (client_secret never written to token file). Credential paths use `~/.config/claude-seo/` (user-space, not in repo).

## Recommendation

**REVIEW — submit NL fix PRs (bugs #1 and #2), submit security fix PRs for Medium findings (#4–#6), address High security findings (#1–#3) in the same PR.**

**Priority order**:
1. **Security (High)**: Fix the triple-quote Python injection in all 3 install scripts. Use environment variable passing instead of source interpolation. Low-effort, high-impact.
2. **Bugs**: Sync extension SKILL.md copies with core versions or restructure installers to reference the canonical core files. Eliminates install-order dependency and version drift permanently.
3. **Security (Medium)**: Pin npm package versions in install scripts. Add a version-check mechanism so upgrades are deliberate.
4. **Quality**: Add `## Examples` blocks to the 5 highest-traffic agents (seo-technical, seo-content, seo-schema, seo-geo, seo-local). Each needs at minimum one input/output pair showing a real delegation scenario. This would move agent scores from 85 → 100 and push the overall NL score to ~98/100.
5. **Quality**: Add `model: sonnet` (or `model: haiku` where appropriate) to both extension agents.

The NL infrastructure (skills, hooks, CLAUDE.md, plugin.json) is excellent — well-structured, comprehensive, and internally consistent. The skill files are production-quality. The only systematic weakness is the agent example gap, which is fixable with a single focused PR.
