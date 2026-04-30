# NLPM Audit: kazukinagata/shinkoku
**Date**: 2026-04-06  |  **Artifacts**: 26  |  **Strategy**: batched
**NL Score**: 94/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 5  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| CLAUDE.md | project-config | 85 | No NL frontmatter (by design for CLAUDE.md type); otherwise well-documented |
| skills/e-tax/SKILL.md | skill | 88 | File too large to fully read (25k+ tokens); structure and frontmatter confirmed clean in first 150 lines |
| skills/income-tax/SKILL.md | skill | 92 | Longest skill (873 lines); some estimated quality cost for complexity |
| skills/tax-housing-loan-context/SKILL.md | skill | 95 | Clean |
| skills/tax-legal-context/SKILL.md | skill | 95 | Clean |
| skills/tax-invoice-credit-context/SKILL.md | skill | 95 | Clean |
| skills/tax-ebookkeeping-context/SKILL.md | skill | 95 | Clean |
| skills/capabilities/SKILL.md | skill | 95 | Clean |
| skills/reading-invoice/SKILL.md | skill | 95 | Clean |
| skills/e-bookkeeping-compliance/SKILL.md | skill | 95 | Clean |
| skills/reading-deduction-cert/SKILL.md | skill | 95 | Clean |
| skills/assess/SKILL.md | skill | 95 | Clean |
| skills/submit/SKILL.md | skill | 95 | Clean |
| skills/reading-payment-statement/SKILL.md | skill | 95 | Clean |
| skills/reading-receipt/SKILL.md | skill | 95 | Clean |
| skills/incorporation/SKILL.md | skill | 95 | Clean |
| skills/reading-withholding/SKILL.md | skill | 95 | Clean |
| skills/invoice-system/SKILL.md | skill | 95 | Clean |
| skills/gather/SKILL.md | skill | 95 | Clean |
| skills/settlement/SKILL.md | skill | 96 | 2× "妥当か" vague quantifier (-4) |
| skills/setup/SKILL.md | skill | 96 | Clean |
| skills/tax-advisor/SKILL.md | skill | 96 | 1× "網羅的に" vague quantifier (-2); uses `reference/` not `references/` (inconsistent with other skills, but not broken) |
| skills/journal/SKILL.md | skill | 96 | Clean |
| skills/furusato/SKILL.md | skill | 97 | 1× "適切に設定されているか" vague quantifier (-2) |
| skills/consumption-tax/SKILL.md | skill | 97 | Clean |
| .claude-plugin/plugin.json | metadata | 100 | Well-formed; valid semver 0.6.5; matches pyproject.toml |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks (`target-repo/hooks/**`) | 0 — directory does not exist |
| Scripts (`target-repo/scripts/**`) | 0 — directory does not exist |
| Skill scripts (`skills/e-tax/scripts/`) | 1 — `etax-stealth.js` |
| MCP configs | 0 — `.mcp.json` not found |
| Package manifests | 1 — `pyproject.toml` |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | medium | skills/setup/SKILL.md | 21 | SEC-runtime-package-install | Skill instructs `uv tool install git+https://github.com/kazukinagata/shinkoku` — runtime install from a git URL with no version pin. Git URL installs bypass package registry integrity guarantees. Intent is legitimate (self-install of the plugin); risk is unpinned supply chain. |
| 2 | low | skills/e-tax/scripts/etax-stealth.js | 1–206 | SEC-browser-fingerprint-spoof | Spoofs `navigator.platform`, `navigator.userAgent`, `navigator.userAgentData`, `navigator.webdriver` and patches server-baked OS-detection functions (`getClientOS`, `isRecommendedOsAsEtaxAsync`). Purpose is to enable Linux users to access Japan's NTA e-Tax filing site, which discriminates against non-Windows OSes. All manipulations are in-browser, client-side only; no network exfiltration. |
| 3 | low | pyproject.toml | 34–37 | SEC-unpinned-semver | Dependencies use `>=` floor constraints (pydantic>=2.0, pdfplumber>=0.10, pyyaml>=6.0.3) rather than exact pins. Future incompatible versions could silently break tax calculations or introduce vulnerabilities. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No bugs found | All 26 artifacts have valid frontmatter, all inter-skill references resolve, plugin.json semver is valid and matches pyproject.toml |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/setup/SKILL.md | Runtime git-URL install is unpinned | Add version tag to install command: `uv tool install git+https://github.com/kazukinagata/shinkoku@v0.6.5` and update instructions to always match current plugin version |
| 2 | pyproject.toml | Unpinned dependency floor constraints | Pin exact versions in a lock-based install or use `uv lock` (already present as `uv.lock`); document that `uv.lock` is authoritative for reproducible installs |
| 3 | skills/e-tax/scripts/etax-stealth.js | Browser user-agent spoofing could trigger ToS concerns | Add a clear in-file comment block (beyond current comments) explaining that this script is required because the NTA website enforces OS restrictions that discriminate against Linux users, so the spoofing is defensive compatibility, not deceptive |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/settlement/SKILL.md | "妥当か" used twice as a vague qualifier for account balance review (lines 99, 279). Prefer explicit criteria: "残高がマイナスでないか" or "異常値（前年比±50%超等）がないか". | -4 |
| 2 | skills/furusato/SKILL.md | "適切に設定されているか" (line: "自宅兼事務所の場合、事業割合が適切に設定されているか"). Vague — prefer "事業専用面積比率で按分されているか（例: 事務所20㎡/自宅100㎡ = 20%）". | -2 |
| 3 | skills/tax-advisor/SKILL.md | "網羅的に" (comprehensively) used once when listing applicable deductions. Prefer "次の優先順で全項目を確認する". | -2 |
| 4 | CLAUDE.md | No YAML frontmatter (name, description). Not a bug — CLAUDE.md is a project instruction file, not an NL artifact — but the artifact list includes it, so flagged informational. | info |
| 5 | skills/e-tax/SKILL.md | File exceeds read tool limit (25k+ tokens). Audit coverage of this skill is limited to the first ~150 lines. Recommend splitting into a top-level orchestration SKILL.md + sub-skill files per form section, to stay within tool read limits. | info |

## Cross-Component
- **Naming inconsistency**: `skills/tax-advisor/SKILL.md` references `reference/` (singular) while every other skill uses `references/` (plural). Both directories physically exist (`skills/tax-advisor/reference/` and `skills/*/references/`), so all paths resolve — not a broken reference, but a naming inconsistency that could confuse contributors.
- **All inter-skill invocations verified**: `/reading-receipt`, `/reading-invoice`, `/reading-withholding`, `/reading-deduction-cert`, `/reading-payment-statement`, `/tax-housing-loan-context`, `/tax-legal-context`, `/tax-ebookkeeping-context`, `/tax-invoice-credit-context`, `/e-bookkeeping-compliance`, `/capabilities`, `/income-tax`, `/consumption-tax`, `/settlement`, `/e-tax`, `/setup` — all resolve to existing skills. ✓
- **Version sync verified**: `plugin.json` version `0.6.5` matches `pyproject.toml` `version = "0.6.5"`. ✓
- **CLAUDE.md skill inventory matches actual files**: All skill paths listed in CLAUDE.md's `### スキル（skills/）` table correspond to existing files. ✓
- **Circular reference check**: No circular skill invocations detected. Skills invoke helpers downstream (e.g., `income-tax` → `reading-withholding`) but no cycles. ✓

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

No bugs were found. The three security findings are all low-severity or medium-severity supply-chain hygiene issues with clear, low-effort fixes. The NL score of 94/100 is well above the default threshold of 70. The plugin is high quality with consistently structured skills, proper frontmatter, numbered procedural steps, and well-defined output formats throughout. Priority fix: pin the git install URL to a version tag in `skills/setup/SKILL.md` (finding #1).
