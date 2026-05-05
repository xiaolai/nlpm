# NLPM Audit: wasp-lang/open-saas
**Date**: 2026-05-05  |  **Artifacts**: 3  |  **Strategy**: single
**NL Score**: 92/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 5  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| template/app/.agents/skills/add-wasp-skills/SKILL.md | skill | 90 | R04: description is a summary, not 3+ trigger phrases |
| template/app/.agents/skills/guided-tour/SKILL.md | skill | 90 | R04: description has 2 action phrases; R07: no scope note |
| template/app/.agents/skills/getting-started/SKILL.md | skill | 95 | R07: no scope note linking to related skills |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 3 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts | tools/dope.sh, opensaas-sh/tools/diff.sh, opensaas-sh/tools/patch.sh, template-test/tools/diff.sh, template-test/tools/patch.sh, opensaas-sh/blog/public/scripts/reo.js, opensaas-sh/blog/public/scripts/posthog.js |
| MCP configs | 0 |
| Package manifests | package.json, template/e2e-tests/package.json, template/blog/package.json, template/app/package.json, opensaas-sh/blog/package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | opensaas-sh/blog/public/scripts/reo.js | 9 | SEC-cdn-script-inject | Third-party script dynamically created and loaded from `https://static.reo.dev/<clientID>/reo.js`; if reo.dev CDN is compromised, arbitrary JS executes on the blog |
| 2 | Low | opensaas-sh/blog/public/scripts/posthog.js | 2 | SEC-hardcoded-api-key | PostHog project key hardcoded in client-side script (intentionally public by PostHog's design; false positive — noting for completeness) |
| 3 | Low | package.json | 11 | SEC-unpinned-semver | Multiple devDependencies use `^` semver ranges, allowing minor/patch drift on `npm install` |
| 4 | Low | template-test/tools/diff.sh | 20 | SEC-runtime-network | `wasp new -t saas base-app` downloads a project template from Wasp's servers at script runtime |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No bugs found | — |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | opensaas-sh/blog/public/scripts/reo.js | Third-party CDN script loaded dynamically from reo.dev | Add Subresource Integrity (SRI) hash or pin to a specific versioned CDN URL; document the vendor in a dependency manifest |
| 2 | package.json | Unpinned `^` semver ranges in devDependencies | Pin exact versions (`"eslint": "9.39.4"`) or adopt lockfile-only installs (`npm ci`) in CI to prevent drift |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | template/app/.agents/skills/add-wasp-skills/SKILL.md | R04: description is a one-phrase summary ("Install Wasp agent skills…that add Wasp knowledge…"). Should list 3+ specific user-query trigger phrases, e.g. "Use when adding Wasp plugins, installing agent skills, or setting up Wasp-specific AI tooling." | -5 |
| 2 | template/app/.agents/skills/add-wasp-skills/SKILL.md | R07: no scope note. Two closely-related skills (getting-started, guided-tour) exist but are not referenced. When all three are loaded, Claude has no guidance on which to invoke for overlapping queries. | -5 |
| 3 | template/app/.agents/skills/getting-started/SKILL.md | R07: no scope note linking to guided-tour (next step after onboarding) or add-wasp-skills (optional companion for AI tooling setup). | -5 |
| 4 | template/app/.agents/skills/guided-tour/SKILL.md | R04: description has 2 action phrases ("Take a guided tour", "walks you through…project structure, features, and customization checklist"). R04 requires 3+. | -5 |
| 5 | template/app/.agents/skills/guided-tour/SKILL.md | R07: no scope note linking to getting-started (prerequisite) or add-wasp-skills. | -5 |

## Cross-Component
All three skills are peer artifacts in `template/app/.agents/skills/` and are thematically sequential (onboarding → tour → plugins). None reference the others, so skill selection is ambiguous when all three are active. The CLAUDE.md in `template/app/` correctly points to `https://docs.opensaas.sh/llms.txt` — consistent with the doc-fetch steps in getting-started and guided-tour. The `add-wasp-skills` external reference (`wasp-lang/wasp-agent-plugins` on GitHub) is structurally sound; cannot verify live availability but the URL pattern is consistent. No orphaned or broken internal references found.

## Recommendation
CLEAR — no PR-worthy NL bugs. Open a security issue for the reo.js CDN injection risk (Medium). Quality findings are informational and can be addressed in a follow-up NL improvement PR: add R07 scope notes linking the three sibling skills to each other, and expand the descriptions for add-wasp-skills and guided-tour to meet R04's 3+ trigger-phrase threshold.
