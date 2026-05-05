# NLPM Audit: wasp-lang/open-saas
**Date**: 2026-05-05  |  **Artifacts**: 3  |  **Strategy**: single
**NL Score**: 87/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 7  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| template/app/.agents/skills/guided-tour/SKILL.md | Skill | 84 | Missing output format; vague qualifiers (clearly, concisely, comfortable) |
| template/app/.agents/skills/add-wasp-skills/SKILL.md | Skill | 88 | Missing output format; vague phrasing "Walk the user through" |
| template/app/.agents/skills/getting-started/SKILL.md | Skill | 88 | Missing output format; vague phrasing "walk them through" |

**Scoring notes:**
- All three skills have required frontmatter (name, description) ✅
- All three are `user_invocable: true` and have numbered steps ✅
- Model declaration and example-block penalties do not apply to SKILL.md files (agent-only penalties)
- Output format specification is absent from all three skills (no declared response structure or completion signal)

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 4 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts | 3 (opensaas-sh/blog/public/scripts/reo.js, opensaas-sh/blog/public/scripts/posthog.js, opensaas-sh/blog/scripts/generate-llm-files.mjs) |
| MCP configs | 0 |
| Package manifests | 5 (package.json, template/app/package.json, template/e2e-tests/package.json, template/blog/package.json, opensaas-sh/blog/package.json) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Low | opensaas-sh/blog/public/scripts/posthog.js | 2 | hardcoded-api-key | PostHog project API key hardcoded in public client JS. Client-side analytics keys are intentionally public; flagged for completeness. |
| 2 | Low | opensaas-sh/blog/public/scripts/reo.js | 4 | hardcoded-api-key | Reo analytics clientID hardcoded in public client JS. Same pattern as PostHog — expected for client-side analytics. |
| 3 | Low | template/app/package.json | null | unpinned-semver | Production dependencies use `^` semver ranges (stripe, AWS SDK, openai, react). Supply-chain risk if a breaking or malicious patch is released. |
| 4 | Low | template/e2e-tests/package.json | 14 | shell-kill-pid | npm script uses `kill -9 $PID` where PID is grep-derived from `ps` output. Dev utility only; controlled input, low actual risk. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No bugs found | — |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | template/app/package.json | Unpinned semver for production deps (stripe, openai, @aws-sdk/*) | Pin exact versions for security-critical packages; use lockfile integrity checks in CI |
| 2 | template/e2e-tests/package.json | kill -9 on grep-derived PID in npm script | Store PID in a file when starting stripe listener; read from file to kill |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | template/app/.agents/skills/add-wasp-skills/SKILL.md | Missing output format: no declaration of how installation guidance should be presented to the user | -10 |
| 2 | template/app/.agents/skills/add-wasp-skills/SKILL.md | Vague directive: "Walk the user through" does not specify format, depth, or confirmation style | -2 |
| 3 | template/app/.agents/skills/getting-started/SKILL.md | Missing output format: no specification of response structure or completion signal | -10 |
| 4 | template/app/.agents/skills/getting-started/SKILL.md | Vague directive: "walk them through the steps" (Step 4) does not specify presentation format | -2 |
| 5 | template/app/.agents/skills/guided-tour/SKILL.md | Missing output format: no specification of section presentation format or tour completion signal | -10 |
| 6 | template/app/.agents/skills/guided-tour/SKILL.md | Vague qualifiers: "clearly and concisely" (Step 3, item 1) are unmeasurable directives | -4 |
| 7 | template/app/.agents/skills/guided-tour/SKILL.md | Vague qualifier: "Keep the pace comfortable" is unmeasurable; no heuristic given | -2 |

## Cross-Component
All three skills are internally consistent:
- `getting-started` and `guided-tour` both fetch from the same docs index (`https://docs.opensaas.sh/llms.txt`) — consistent live-doc strategy.
- `add-wasp-skills` fetches from a different upstream (wasp-agent-plugins repo) — appropriate separation.
- No broken intra-skill references. No orphaned components.
- Terminology is consistent across skills: "Wasp", "Open SaaS", "guide", "documentation map" all used coherently.
- All three are `user_invocable: true` — consistent registration.
- Live URL dependencies (all three skills fetch from external URLs at runtime) mean they degrade gracefully if the docs URLs move, but there is no fallback specified in any skill. This is a minor robustness gap, not a bug.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

No bugs were found. No critical or high security findings. The two Low security fixes (pinning production deps, safer PID handling) are straightforward and PR-ready. Quality improvements (output format declarations, eliminating vague directives in guided-tour) would raise all three skills above 90.
