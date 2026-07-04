# NLPM Audit: greensock/gsap-skills
**Date**: 2026-04-06  |  **Artifacts**: 9  |  **Strategy**: single
**NL Score**: 97/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 6  |  **Security Findings**: 2

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/gsap-core/SKILL.md | Skill | 89 | 3 vague quantifiers ("relevant", "several", "correctly") — R01, -6 |
| skills/gsap-plugins/SKILL.md | Skill | 89 | 3 vague quantifiers ("some" x2, "as needed") — R01, -6 |
| skills/gsap-frameworks/SKILL.md | Skill | 98 | 1 vague quantifier ("some", inside a code comment) — R01, -2 |
| skills/gsap-timeline/SKILL.md | Skill | 98 | 1 vague quantifier ("several") — R01, -2 |
| .claude-plugin/plugin.json | Manifest | 100 | None — clean |
| skills/gsap-performance/SKILL.md | Skill | 100 | None — clean |
| skills/gsap-react/SKILL.md | Skill | 100 | None — clean |
| skills/gsap-scrolltrigger/SKILL.md | Skill | 100 | None — clean |
| skills/gsap-utils/SKILL.md | Skill | 100 | None — clean |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none found |
| Scripts (.sh/.py/.js) | examples/react/vite.config.js, examples/vanilla/main.js, examples/vue/vite.config.js, examples/vue/main.js |
| MCP configs | none found |
| package.json manifests | examples/react/package.json, examples/vue/package.json, examples/nuxt/package.json |
| requirements.txt | none found |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | Medium | examples/vanilla/main.js | 5-6 | SEC-cdn-script-import | Imports GSAP and ScrollTrigger from a public CDN (`cdn.jsdelivr.net`) via ES module `import` in a no-build vanilla-JS example. Version is pinned (`@3.15.0`), so this is not an unpinned-dependency issue, but ES module imports have no Subresource Integrity option, so a reader who copies this file verbatim into production would load code from a third party on every page load. |
| 2 | Low | examples/nuxt/package.json | 10 | SEC-postinstall-script | `"postinstall": "nuxt prepare"` — matches the generic postinstall-script pattern, but the command is Nuxt's own documented lifecycle step (generates local `.nuxt` type stubs); no network access, no code download, no shell/eval. Verified benign — see `false_positive` in the findings sidecar. |

## Bugs (PR-worthy)
No NL bugs found. All 8 SKILL.md files have valid frontmatter (`name`, `description`), each `name` matches its parent directory, and `.claude-plugin/plugin.json` has valid `name`/`version`/`description`. Cross-skill "Related skills" references (gsap-core ↔ gsap-timeline ↔ gsap-scrolltrigger ↔ gsap-react ↔ gsap-frameworks ↔ gsap-plugins ↔ gsap-utils ↔ gsap-performance) all resolve to skill directories that exist on disk — no broken references.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | examples/vanilla/main.js | GSAP loaded from a public CDN with no SRI option (ES module import) | Add a one-line comment clarifying this pattern is for zero-build demo purposes only, and that production apps should `npm install gsap` and bundle it rather than importing from a CDN at runtime. |

(The `examples/nuxt/package.json` postinstall finding is not included here — it was verified benign during this audit; see Security Findings table above.)

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/gsap-core/SKILL.md | Description is 500-800 chars (R04) | -5 |
| 2 | skills/gsap-core/SKILL.md | 3 vague quantifiers: "relevant" (L15), "several" (L87), "correctly" (L252) (R01) | -6 |
| 3 | skills/gsap-plugins/SKILL.md | Body is 400-500 lines — 433 lines (R05) | -5 |
| 4 | skills/gsap-plugins/SKILL.md | 3 vague quantifiers: "some" (L208), "some" (L256), "as needed" (L262) (R01) | -6 |
| 5 | skills/gsap-frameworks/SKILL.md | 1 vague quantifier: "some" (L173, inside a code comment) (R01) | -2 |
| 6 | skills/gsap-timeline/SKILL.md | 1 vague quantifier: "several" (L11) (R01) | -2 |

Note: several of the flagged R01 occurrences (e.g. "relevant" describing when GSAP docs apply, "several" as a plain descriptive count, "as needed" describing MorphSVGPlugin's own internal point-insertion algorithm) are ordinary technical prose rather than vague *instructions* lacking measurable criteria. They are reported per the mechanical R01 word-list scan but are low-severity/low-actionability; none affect correctness or agent behavior.

## Cross-Component
- All 8 skill directory names match their SKILL.md frontmatter `name:` field exactly (open-spec MUST, per `nlpm:conventions` §5).
- `.claude-plugin/plugin.json` declares `"skills": "./skills/"`, which resolves to the directory actually containing all 8 skills — no orphaned or missing entries.
- Every "Related skills" cross-reference across the 8 SKILL.md files points to a skill that exists on disk; no broken or stale references found.
- No contradictions found between skills (e.g. gsap-react and gsap-frameworks agree on scoping via `gsap.context()`/`useGSAP`; gsap-scrolltrigger and gsap-timeline agree that ScrollTrigger belongs on the top-level timeline, not child tweens).

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes. There are no NL bugs and no confirmed Critical/High security findings; the one accepted Medium finding (CDN import in the vanilla example) is a minor, optional documentation improvement, and the postinstall finding was verified benign during this audit.
