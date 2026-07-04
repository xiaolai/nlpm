# NLPM Audit: zubair-trabzada/ai-marketing-claude
**Date**: 2026-04-06  |  **Artifacts**: 20  |  **Strategy**: single
**NL Score**: 53/100
**Security**: BLOCKED
**Bugs**: 21  |  **Quality Issues**: 45  |  **Security Findings**: 5

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/market-strategy.md | agent | 26 | Missing frontmatter (no `name`/`description`) — agent cannot be dispatched by name |
| agents/market-content.md | agent | 28 | Missing frontmatter — agent cannot be dispatched by name |
| agents/market-conversion.md | agent | 28 | Missing frontmatter — agent cannot be dispatched by name |
| agents/market-competitive.md | agent | 30 | Missing frontmatter — agent cannot be dispatched by name |
| agents/market-technical.md | agent | 30 | Missing frontmatter — agent cannot be dispatched by name |
| skills/market-seo/SKILL.md | skill | 44 | Missing frontmatter + 8 vague-quantifier instances |
| skills/market-landing/SKILL.md | skill | 50 | Missing frontmatter + 5 vague-quantifier instances |
| skills/market-copy/SKILL.md | skill | 56 | Missing frontmatter + no empty-input handling |
| skills/market-funnel/SKILL.md | skill | 56 | Missing frontmatter + no empty-input handling |
| skills/market-ads/SKILL.md | skill | 58 | Missing frontmatter + no empty-input handling |
| skills/market-brand/SKILL.md | skill | 60 | Missing frontmatter + no empty-input handling |
| skills/market-competitors/SKILL.md | skill | 60 | Missing frontmatter + broken script CLI usage example |
| skills/market-emails/SKILL.md | skill | 60 | Missing frontmatter + 5 vague-quantifier instances |
| skills/market-proposal/SKILL.md | skill | 60 | Missing frontmatter + 5 vague-quantifier instances |
| skills/market-launch/SKILL.md | skill | 66 | Missing frontmatter (`description`) |
| skills/market-social/SKILL.md | skill | 66 | Missing frontmatter (`description`) |
| skills/market-report/SKILL.md | skill | 68 | Missing frontmatter + broken sibling-output filename references |
| skills/market-audit/SKILL.md | skill | 70 | Missing frontmatter (`description`) |
| skills/market-report-pdf/SKILL.md | skill | 70 | Missing frontmatter + broken sibling-output filename references |
| market/SKILL.md | skill (orchestrator) | 73 | Missing frontmatter (`description`) |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 3 |
| Medium | 0 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none found |
| Scripts (Python) | scripts/analyze_page.py, scripts/competitor_scanner.py, scripts/generate_pdf_report.py, scripts/social_calendar.py |
| Scripts (shell) | install.sh, uninstall.sh |
| MCP configs | none found |
| Package manifests | requirements.txt (no package.json / npm present) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | README.md | 40 | curl piped to shell | One-command install instructs `curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/ai-marketing-claude/main/install.sh \| bash` — executes remote code with no integrity check (no checksum/signature pinning). Common installer pattern, but still an uncontrolled-execution surface per the rubric's literal CRITICAL criteria. |
| 2 | High | scripts/analyze_page.py | 306-308 | TLS certificate verification disabled | `fetch_page()` builds an SSL context with `check_hostname = False` and `verify_mode = ssl.CERT_NONE`, disabling certificate validation for all outbound HTTPS fetches (CWE-295). Enables MITM tampering of fetched marketing pages. |
| 3 | High | scripts/analyze_page.py | 342-344 | TLS certificate verification disabled | `fetch_sitemap()` repeats the same `CERT_NONE` / `check_hostname = False` pattern for the sitemap.xml fetch. |
| 4 | High | scripts/competitor_scanner.py | 177-179 | TLS certificate verification disabled | `fetch_page()` disables certificate verification identically to analyze_page.py, applied to every competitor URL scanned (including user- and LLM-supplied URLs). |
| 5 | Low | requirements.txt | 4 | Unpinned dependency version | `reportlab>=4.0` uses a floor-only version constraint with no upper bound — future major-version releases install unvetted. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | agents/market-strategy.md | No YAML frontmatter at all (file opens directly with `# Market Strategy Subagent`) | No `name:` field — Claude Code's Agent/Task dispatch has no identifier to invoke this subagent by. Breaks the "5 parallel subagents" mechanism `/market audit` depends on. |
| 2 | agents/market-content.md | No YAML frontmatter | Same as above — subagent cannot be dispatched by name. |
| 3 | agents/market-conversion.md | No YAML frontmatter | Same as above. |
| 4 | agents/market-competitive.md | No YAML frontmatter | Same as above. |
| 5 | agents/market-technical.md | No YAML frontmatter | Same as above. |
| 6 | market/SKILL.md | No YAML frontmatter (missing required `description:`) | Claude Code's native skill-discovery cannot auto-trigger this skill from natural-language requests; only works if the user already knows to type `/market ...`. |
| 7 | skills/market-ads/SKILL.md | No YAML frontmatter (missing `description:`) | Skill cannot be auto-discovered/triggered outside the orchestrator's explicit text-based routing. |
| 8 | skills/market-audit/SKILL.md | No YAML frontmatter (missing `description:`) | Same discovery gap; also the flagship command's own file is unregistered. |
| 9 | skills/market-brand/SKILL.md | No YAML frontmatter (missing `description:`) | Same discovery gap. |
| 10 | skills/market-competitors/SKILL.md | No YAML frontmatter (missing `description:`) | Same discovery gap. |
| 11 | skills/market-copy/SKILL.md | No YAML frontmatter (missing `description:`) | Same discovery gap. |
| 12 | skills/market-emails/SKILL.md | No YAML frontmatter (missing `description:`) | Same discovery gap. |
| 13 | skills/market-funnel/SKILL.md | No YAML frontmatter (missing `description:`) | Same discovery gap. |
| 14 | skills/market-landing/SKILL.md | No YAML frontmatter (missing `description:`) | Same discovery gap. |
| 15 | skills/market-launch/SKILL.md | No YAML frontmatter (missing `description:`) | Same discovery gap. |
| 16 | skills/market-proposal/SKILL.md | No YAML frontmatter (missing `description:`) | Same discovery gap. |
| 17 | skills/market-report-pdf/SKILL.md | No YAML frontmatter (missing `description:`) | Same discovery gap. |
| 18 | skills/market-report/SKILL.md | No YAML frontmatter (missing `description:`) | Same discovery gap. |
| 19 | skills/market-seo/SKILL.md | No YAML frontmatter (missing `description:`) | Same discovery gap. |
| 20 | skills/market-social/SKILL.md | No YAML frontmatter (missing `description:`) | Same discovery gap. |
| 21 | skills/market-competitors/SKILL.md | Line 55 documents `python scripts/competitor_scanner.py --url [competitor-url] --output json`, but `scripts/competitor_scanner.py`'s `main()` (lines 262-277) takes positional URL arguments only — it never parses `--url` or `--output` flags. Running the documented command treats `--url`, `--output`, and `json` as literal URLs and fails to collect the intended data. | Following the skill's own documented usage produces broken/garbage output instead of a competitor scan. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | requirements.txt | `reportlab>=4.0` is unpinned above the floor | Pin to a tested range, e.g. `reportlab>=4.0,<5.0`, or an exact version with a documented upgrade process. |

Note: the Critical (README.md curl\|bash) and High (disabled TLS verification, ×3) findings above are **not** included here — per policy they require private disclosure rather than a public PR.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/market-competitive.md | Zero `<example>` blocks (R09 requires ≥2) | -15 |
| 2 | agents/market-competitive.md | Model tier not declared (R10) | -5 |
| 3 | agents/market-content.md | Zero `<example>` blocks (R09) | -15 |
| 4 | agents/market-content.md | Model tier not declared (R10) | -5 |
| 5 | agents/market-content.md | 1 vague-quantifier instance ("appropriate") (R01) | -2 |
| 6 | agents/market-conversion.md | Zero `<example>` blocks (R09) | -15 |
| 7 | agents/market-conversion.md | Model tier not declared (R10) | -5 |
| 8 | agents/market-conversion.md | 1 vague-quantifier instance ("appropriate") (R01) | -2 |
| 9 | agents/market-strategy.md | Zero `<example>` blocks (R09) | -15 |
| 10 | agents/market-strategy.md | Model tier not declared (R10) | -5 |
| 11 | agents/market-strategy.md | 2 vague-quantifier instances (R01) | -4 |
| 12 | agents/market-technical.md | Zero `<example>` blocks (R09) | -15 |
| 13 | agents/market-technical.md | Model tier not declared (R10) | -5 |
| 14 | market/SKILL.md | 1 vague-quantifier instance (R01) | -2 |
| 15 | skills/market-ads/SKILL.md | No `allowed-tools` declared though the skill drives WebFetch/Bash-invoked scripts (R11) | -5 |
| 16 | skills/market-ads/SKILL.md | No empty-input handling documented for a missing `<url>` (R15) | -10 |
| 17 | skills/market-ads/SKILL.md | 1 vague-quantifier instance (R01) | -2 |
| 18 | skills/market-audit/SKILL.md | No `allowed-tools` declared (R11) | -5 |
| 19 | skills/market-brand/SKILL.md | No `allowed-tools` declared (R11) | -5 |
| 20 | skills/market-brand/SKILL.md | No empty-input handling documented (R15) | -10 |
| 21 | skills/market-competitors/SKILL.md | No `allowed-tools` declared (R11) | -5 |
| 22 | skills/market-competitors/SKILL.md | No empty-input handling documented (R15) | -10 |
| 23 | skills/market-copy/SKILL.md | No `allowed-tools` declared (R11) | -5 |
| 24 | skills/market-copy/SKILL.md | No empty-input handling documented (R15) | -10 |
| 25 | skills/market-copy/SKILL.md | 2 vague-quantifier instances (R01) | -4 |
| 26 | skills/market-emails/SKILL.md | No `allowed-tools` declared (R11) | -5 |
| 27 | skills/market-emails/SKILL.md | 5 vague-quantifier instances (R01) | -10 |
| 28 | skills/market-funnel/SKILL.md | No `allowed-tools` declared (R11) | -5 |
| 29 | skills/market-funnel/SKILL.md | No empty-input handling documented (R15) | -10 |
| 30 | skills/market-funnel/SKILL.md | 2 vague-quantifier instances (R01) | -4 |
| 31 | skills/market-landing/SKILL.md | No `allowed-tools` declared (R11) | -5 |
| 32 | skills/market-landing/SKILL.md | No empty-input handling documented (R15) | -10 |
| 33 | skills/market-landing/SKILL.md | 5 vague-quantifier instances (R01) | -10 |
| 34 | skills/market-launch/SKILL.md | No `allowed-tools` declared (R11) | -5 |
| 35 | skills/market-launch/SKILL.md | 2 vague-quantifier instances (R01) | -4 |
| 36 | skills/market-proposal/SKILL.md | No `allowed-tools` declared (R11) | -5 |
| 37 | skills/market-proposal/SKILL.md | 5 vague-quantifier instances (R01) | -10 |
| 38 | skills/market-report-pdf/SKILL.md | No `allowed-tools` declared (R11) | -5 |
| 39 | skills/market-report/SKILL.md | No `allowed-tools` declared (R11) | -5 |
| 40 | skills/market-report/SKILL.md | 1 vague-quantifier instance (R01) | -2 |
| 41 | skills/market-seo/SKILL.md | No `allowed-tools` declared (R11) | -5 |
| 42 | skills/market-seo/SKILL.md | No empty-input handling documented (R15) | -10 |
| 43 | skills/market-seo/SKILL.md | 8 vague-quantifier instances (R01) | -16 |
| 44 | skills/market-social/SKILL.md | No `allowed-tools` declared (R11) | -5 |
| 45 | skills/market-social/SKILL.md | 2 vague-quantifier instances (R01) | -4 |

## Cross-Component
- **Broken sibling-output filename references (both report compilers).** `skills/market-report/SKILL.md` (Step 1 data-source list) and `skills/market-report-pdf/SKILL.md` (Step 1 primary data sources) both look for `COMPETITOR-ANALYSIS.md`, `SOCIAL-AUDIT.md`, `EMAIL-AUDIT.md`, and `AD-AUDIT.md` — but the actual sibling skills write different filenames: `skills/market-competitors/SKILL.md` → `COMPETITOR-REPORT.md`, `skills/market-social/SKILL.md` → `SOCIAL-CALENDAR.md`, `skills/market-emails/SKILL.md` → `EMAIL-SEQUENCES.md`, `skills/market-ads/SKILL.md` → `AD-CAMPAIGNS.md`. `market-report/SKILL.md` additionally lists `CONTENT-AUDIT.md`, which no skill in the suite ever produces. Net effect: even when a user has already run `/market competitors`, `/market social`, `/market emails`, and `/market ads`, neither `/market report` nor `/market report-pdf` will ever find that data, because they check for the wrong filenames. High confidence — verified by diffing each skill's own "Output Format" filename against the two report skills' data-source checklists.
- No orphaned skill/agent files were found — every skill listed in README.md's architecture diagram and install.sh's `SKILLS`/`AGENTS` arrays corresponds to an actual file on disk, and vice versa (14 sub-skills + 1 orchestrator + 5 agents, matching install.sh's "15 Skills · 5 Agents · 4 Scripts" banner).
- `scripts/social_calendar.py` exists on disk and is installed by `install.sh`, but no SKILL.md in the suite documents a CLI invocation of it (unlike `analyze_page.py`, `competitor_scanner.py`, and `generate_pdf_report.py`, which are each referenced with example commands). Not a bug — `/market social` may intentionally generate the calendar via reasoning rather than the script — but it is an unused/undocumented execution surface worth a maintainer note.

## Recommendation
**BLOCKED — do not submit PRs. File private security report.**

The disabled TLS certificate verification (3 instances, High) and the curl-piped-to-shell installer instruction (Critical) must be privately disclosed and resolved before any public contribution activity. Once cleared, the 21 NL bugs (frontmatter additions restoring agent dispatch and skill auto-discovery, the broken `competitor_scanner.py` CLI usage example, and the two cross-component filename mismatches) are all straightforward, high-confidence fixes suitable for follow-up PRs.
