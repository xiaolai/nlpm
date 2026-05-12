# NLPM Audit: lackeyjb/playwright-skill
**Date**: 2026-05-12  |  **Artifacts**: 2  |  **Strategy**: single
**NL Score**: 98/100
**Security**: CLEAR
**Bugs**: 1  |  **Quality Issues**: 1  |  **Security Findings**: 1

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `skills/playwright-skill/SKILL.md` | Skill | 97/100 | "comprehensive" — borderline R01 vague quantifier |
| `.claude-plugin/plugin.json` | Plugin Manifest | 100/100 | None |

### Scoring Notes

**`skills/playwright-skill/SKILL.md` — 97/100**

The skill is exceptionally well-written. Valid frontmatter with name and description. Description follows R04 (trigger, not summary): enumerates specific use-cases with user-query phrasing. CRITICAL WORKFLOW uses numbered steps per R14 spirit. Six code-example patterns plus two interaction examples in "Example Usage" satisfy R06 and the spirit of R09 for skills. Line count is 454 — under the R05 500-line ceiling. Concrete, imperative instructions dominate; minimal padding.

Deductions applied:
- "comprehensive Playwright API documentation" (line 373): borderline R01. "Comprehensive" is not in the R01 enumerated list but is functionally vague — it tells Claude nothing actionable about what the reference contains. **−2**
- "Clean test scripts" (description, line 3): "clean" is subjective with no measurable criteria. **−1**

**`.claude-plugin/plugin.json` — 100/100**

Valid manifest with all required fields: `name`, `version`, `description`, `author`, `license`, `repository`, `keywords`. No NL-specific penalties applicable to JSON manifests. The `"model-invoked"` keyword is correct for a skill consumed at inference time.

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts | 0 |
| MCP configs | 0 |
| Package manifests | `skills/playwright-skill/package.json` |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Low | `skills/playwright-skill/package.json` | 20 | SEC-unpinned-semver | `"playwright": "^1.57.0"` — caret allows automatic minor-version updates; a supply-chain compromise in any minor playwright release would silently propagate. |

**Notes on inline execution pattern:** The SKILL.md instructs Claude to pass LLM-generated JavaScript as an inline argument to `node run.js "..."`. Because the code string is composed by the model, not interpolated from unsanitized user shell input, this is not a shell injection vector. No additional finding raised.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `.claude-plugin/marketplace.json` | `metadata.version` is `"1.0.0"` but `plugins[0].version` and `plugin.json` version are both `"4.1.0"` | Registry lookups that rely on the outer metadata version field will see a stale version, potentially causing install or update failures |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `skills/playwright-skill/package.json` | `"playwright": "^1.57.0"` allows automatic minor updates | Pin to an exact version: `"playwright": "1.57.0"` and update intentionally; or use a lock-file-only strategy with `npm ci` in setup docs |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `skills/playwright-skill/SKILL.md` | "comprehensive Playwright API documentation" (line 373) and "clean test scripts" (description, line 3) — subjective adjectives with no measurable criteria (R01 spirit) | −3 |

## Cross-Component
**Version drift in marketplace.json:** The outer `metadata.version` field is `"1.0.0"` while `plugins[0].version` and `plugin.json` both declare `"4.1.0"`. The metadata block carries a plugin-scoped description ("Playwright browser automation skill for Claude Code"), suggesting `metadata.version` was intended to track the plugin version and was not bumped when the plugin advanced from v1 to v4.

**Skill registration:** `plugin.json` does not include a `skills` array explicitly declaring `skills/playwright-skill/SKILL.md`. If the Claude Code plugin installer relies on explicit declaration rather than convention-based discovery, the skill may install without being registered. No evidence of actual breakage found — the `"model-invoked"` keyword suggests the author expects auto-discovery — but this is worth confirming against the plugin system's discovery contract.

**No broken references found:** `API_REFERENCE.md` is referenced from SKILL.md line 373. The file exists at `skills/playwright-skill/API_REFERENCE.md` per the plugin's repo structure (not audited here but consistent with the relative path used). No other cross-references to verify.

**`marketplace.json` email format:** `owner.email` is `"github@lackeyjb"` — this is not a valid RFC 5321 email address. Informational only; unlikely to affect plugin installation.

## Recommendation
CLEAR — submit PRs for the marketplace.json version-sync bug and the semver pin. The skill itself is high quality and requires no functional changes.
