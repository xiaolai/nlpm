# NLPM Audit: glitternetwork/pinme
**Date**: 2026-05-04  |  **Artifacts**: 6  |  **Strategy**: single
**NL Score**: 93/100
**Security**: BLOCKED
**Bugs**: 0  |  **Quality Issues**: 14  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/pinme-share/SKILL.md | skill | 86/100 | 7 vague quantifiers (R01): "relevant", "clean", "restrained", "sensible", "short", "unrelated", "valuable" |
| skills/pinme/SKILL.md | skill | 92/100 | 4 vague quantifiers (R01): "simple", "some", "clear", "truly needed"; no scope notes for related skills (R07) |
| CLAUDE.md | claude.md | 95/100 | Strong project context; no significant issues |
| skills/pinme-auth/SKILL.md | skill | 95/100 | No issues; bilingual body (Chinese + English) is stylistic, not penalized |
| skills/pinme-email/SKILL.md | skill | 95/100 | No issues |
| skills/pinme-llm/SKILL.md | skill | 95/100 | Example uses `openai/gpt-5.2`; potentially stale model ID (informational) |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 1 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts | build.js, rollup.config.js, .prettierrc.js, example/supabase/eslint.config.js |
| MCP configs | 0 |
| Package manifests | package.json, example/supabase/package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | build.js | 5–7 | SEC-env-var-bulk-injection | `for (const key in process.env)` injects ALL environment variables as esbuild compile-time defines. During `npm publish` (auto-triggered via `prepublishOnly`), any CI secrets present in the build environment (e.g. NPM_TOKEN, AWS credentials) will be baked into the distributed `dist/index.js` binary on npm. |
| 2 | Medium | build.js | 9–10 | SEC-secret-key-injection | `process.env.SECRET_KEY` is explicitly injected into the published bundle. If this value is set at publish time (e.g. a signing or encryption key read from `.env`), it ships publicly in the npm package. The variable name strongly implies it is sensitive. |
| 3 | Low | example/supabase/package.json | 1 | SEC-unpinned-semver | All dependencies in the supabase example use caret ranges (`^`), permitting unexpected minor/patch upgrades on fresh installs. Lower risk as this is example code, but introduces reproducibility concerns. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No NL bugs found. All skill files have valid frontmatter. | — |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | build.js | SEC-secret-key-injection (Medium): `SECRET_KEY` explicitly baked into published binary | Move `SECRET_KEY` and other sensitive values out of esbuild `define`; inject only public config constants; load secrets at runtime via env vars instead |
| 2 | example/supabase/package.json | SEC-unpinned-semver (Low): caret ranges allow uncontrolled upgrades in example code | Pin exact versions or document that this is example code intentionally using floating ranges |

> **Note**: Finding #1 (High — bulk env var injection via `for (const key in process.env)`) requires **private disclosure**, not a public PR. See Recommendation.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/pinme-share/SKILL.md | R01: "relevant PinMe integration skill" — "relevant" is a vague quantifier | -2 |
| 2 | skills/pinme-share/SKILL.md | R01: "clean, responsive HTML/CSS" — "clean" is a vague adjective | -2 |
| 3 | skills/pinme-share/SKILL.md | R01: "keep the design restrained and readable" — "restrained" is vague | -2 |
| 4 | skills/pinme-share/SKILL.md | R01: "sensible mobile spacing" — "sensible" is vague | -2 |
| 5 | skills/pinme-share/SKILL.md | R01: "keep the response short" — "short" is vague; specify a token or sentence limit | -2 |
| 6 | skills/pinme-share/SKILL.md | R01: "unrelated logs" — "unrelated" is vague; list the exclusion criteria explicitly | -2 |
| 7 | skills/pinme-share/SKILL.md | R01: "unless interaction is valuable" — "valuable" is vague; specify when JS is warranted | -2 |
| 8 | skills/pinme/SKILL.md | R01: "simple manual routing" — "simple" is vague | -2 |
| 9 | skills/pinme/SKILL.md | R01: "some `fs` capabilities" — "some" is vague | -2 |
| 10 | skills/pinme/SKILL.md | R01: "if there is a clear need" — "clear" is vague; define the condition explicitly | -2 |
| 11 | skills/pinme/SKILL.md | R01: "only splitting when isolation is truly needed" — "truly needed" is vague | -2 |
| 12 | skills/pinme/SKILL.md | R07: No scope notes for related skills; email/auth/LLM/share docs are duplicated inline rather than delegating to `[[pinme-email]]`, `[[pinme-auth]]`, `[[pinme-llm]]`, `[[pinme-share]]` | informational |
| 13 | skills/pinme-share/SKILL.md | R07: Cross-reference "any relevant PinMe integration skill" is vague; use explicit `[[pinme]]`, `[[pinme-auth]]` etc. | informational |
| 14 | skills/pinme-llm/SKILL.md | Data quality: example code uses `openai/gpt-5.2` as a model ID in the web search example (line ~95); this model may not exist and could confuse users | informational |

## Cross-Component
- **Consistent API base URL**: All skills use `https://pinme.cloud` as the default base URL. No contradictions found.
- **Email duplication**: `skills/pinme/SKILL.md` includes a full "Email API Reference" section (with `handleSendEmail` code) that closely mirrors `skills/pinme-email/SKILL.md`. This creates two sources of truth for the same API. If the email endpoint changes, both files must be updated. The `pinme` skill should scope-note to `[[pinme-email]]` and omit the duplicate inline code.
- **Auth omission in main skill**: `skills/pinme/SKILL.md` documents the full-stack project structure but does not mention `pinme-auth` for authentication integration. Users scaffolding an auth-enabled project via the `pinme` skill may miss the dedicated auth skill entirely.
- **CLAUDE.md accuracy**: CLAUDE.md correctly identifies `rollup.config.js` as "legacy, unused" and directs to `build.js`. The file still exists in the repo but the note prevents confusion. No stale references found (R37 satisfied).
- **No broken skill references**: All skill names match their `name` frontmatter. Cross-references in `pinme-share` are informal prose, not `[[slug]]` links, so they cannot be mechanically verified but point to real skills.

## Recommendation
BLOCKED — do not submit PRs. File private security report.

**Why**: Finding #1 (HIGH — `build.js` lines 5–7) injects all build-time environment variables into the publicly distributed npm binary. Combined with `prepublishOnly` auto-triggering the build on `npm publish`, any CI secret present during publish (npm token, cloud credentials, etc.) is silently baked into the package. This is a supply-chain-level credential exfiltration risk that requires private disclosure to the maintainer before any public PR activity.

**After the security issue is resolved**:
- Submit NL fix PRs for quality issues #1–11 (vague quantifiers in `pinme-share` and `pinme` skills)
- Submit security fix PR for finding #2 (Medium: explicit `SECRET_KEY` injection)
- Submit security fix PR for finding #3 (Low: unpinned semver in example)
- File informational notes for quality issues #12–14 (R07 scope notes, model ID staleness)
