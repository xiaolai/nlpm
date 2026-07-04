# NLPM Audit: prompt-security/clawsec
**Date**: 2026-04-06  |  **Artifacts**: 17  |  **Strategy**: single
**NL Score**: 99/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 4  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/claw-release/SKILL.md | skill | 90 | "Existing Skills" table lists only 5 of 16 skills in the repo (stale) |
| skills/clawsec-scanner/SKILL.md | skill | 94 | Vague quantifier "comprehensive/Comprehensive" used 3x |
| skills/clawsec-feed/SKILL.md | skill | 98 | Vague quantifier "relevant" |
| skills/clawsec-suite/SKILL.md | skill | 98 | Vague quantifier "relevant" |
| skills/openclaw-audit-watchdog/SKILL.md | skill | 98 | Vague quantifier "robust" |
| CLAUDE.md | memory | 100 | None |
| skills/clawsec-clawhub-checker/SKILL.md | skill | 100 | None |
| skills/clawsec-nanoclaw/SKILL.md | skill | 100 | None |
| skills/clawtributor/SKILL.md | skill | 100 | None |
| skills/hermes-attestation-guardian/SKILL.md | skill | 100 | None |
| skills/hermes-traffic-guardian/SKILL.md | skill | 100 | None |
| skills/nanoclaw-traffic-guardian/SKILL.md | skill | 100 | None |
| skills/openclaw-traffic-guardian/SKILL.md | skill | 100 | None |
| skills/picoclaw-security-guardian/SKILL.md | skill | 100 | None |
| skills/picoclaw-self-pen-testing/SKILL.md | skill | 100 | None |
| skills/picoclaw-traffic-guardian/SKILL.md | skill | 100 | None |
| skills/soul-guardian/SKILL.md | skill | 100 | None |

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
| Hooks (repo root `hooks/**`) | 0 (none at repo root; per-skill hook packages live under `skills/*/hooks/`, e.g. `skills/clawsec-suite/hooks/clawsec-advisory-guardian/`, `skills/clawsec-scanner/hooks/clawsec-scanner-hook/`) |
| Scripts (`scripts/**/*.{sh,py,js}`) | 20 (`backfill-exploitability.sh`, `feed-utils.sh`, `populate-local-feed.sh`, `populate-local-skills.sh`, `populate-local-wiki.sh`, `prepare-to-push.sh`, `release-skill.sh`, `validate-release-links.sh`, `ci/enrich_exploitability.sh`, `ci/install_clawhub_cli.sh`, `ci/verify_signing_key_consistency.sh`, `ci/guard_clawhub_slug_owner.sh`, `ci/verify_skill_release_import_closure.py`, `ci/test_verify_skill_release_import_closure.py`, `i18n/bootstrap_language_from_en.py`, `i18n/fill_missing_translations_argos.py`, `i18n/test_fill_missing_translations_argos.py`, `i18n/qa_check.py`, `i18n/test_qa_check.py`, `i18n/link_check.py`); an additional 20+ `.mjs` scripts also live under `scripts/` and were spot-checked (subprocess calls all use `spawnSync`/`execFile` with array arguments, no `shell: true`) |
| MCP configs (`.mcp.json`) | 0 (none found at repo root) |
| Package manifests | `package.json` (no `postinstall`/`preinstall` lifecycle scripts; standard `dev`/`build`/`i18n` scripts only) |
| `requirements.txt` | 0 (none found; Python deps documented via `uv pip install ruff bandit` in CLAUDE.md, no lockfile-managed runtime deps) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | Low | skills/clawsec-suite/SKILL.md | 222 | SEC-signature-bypass-flag | `CLAWSEC_ALLOW_UNSIGNED_FEED=1` disables advisory-feed signature verification; documented as opt-in, temporary-migration-only, fail-closed by default |
| 2 | Low | skills/hermes-attestation-guardian/SKILL.md | 224 | SEC-signature-bypass-flag | `HERMES_ADVISORY_ALLOW_UNSIGNED_FEED=1` disables advisory-feed signature verification; documented as "UNSAFE emergency bypass only" |
| 3 | Low | skills/picoclaw-security-guardian/SKILL.md | 167 | SEC-signature-bypass-flag | `--allow-unsigned-checksums` degrades supply-chain verification to integrity-only (no provenance); documented as short/offline-triage-only |
| 4 | Low | package.json | 22-40 | SEC-unpinned-semver | Frontend/dev dependencies pinned with caret (`^`) ranges rather than exact versions, allowing minor/patch drift on fresh installs |

No Critical or High findings. Every subprocess invocation reviewed (`spawnSync`/`execFile` in `scripts/*.mjs`, `scripts/ci/*.mjs`) passes arguments as arrays (never `shell: true`), matching the "Subprocess Execution Pattern" documented in `skills/clawsec-scanner/SKILL.md`. All install/download flows in `SKILL.md` files verify Ed25519 signatures over `checksums.json` before verifying per-file SHA-256 checksums, and reject unresolved `$HOME`-style path tokens. `scripts/ci/release-skill.sh`, `guard_clawhub_slug_owner.sh`, and related CI scripts validate skill-name/slug input against `^[a-z0-9-]+$` before using it in paths or API calls, preventing path/argument injection. No `eval`, no curl-piped-to-shell, no `sudo`, no world-writable `chmod`, and no hardcoded credentials were found in any reviewed script.

## Bugs (PR-worthy)
No bugs found. Frontmatter (`name`, `description`) is present and well-formed on all 16 SKILL.md files; `version` in every `skill.json` matches its sibling `SKILL.md` frontmatter; every relative file reference checked (`SPEC.md`, `HOOK.md`, `docs/INTEGRITY.md`, `docs/SKILL_SIGNING.md`, `reporting.md`, `wiki/exploitability-scoring.md`, `utils/validate_skill.py`, the three CLAUDE.md-referenced `.test.mjs` paths) resolves to an existing file.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | skills/clawsec-suite/SKILL.md:222,412 | `CLAWSEC_ALLOW_UNSIGNED_FEED` bypass has no expiry/self-destruct mechanism once set | Consider having the guardian hook log a persistent warning (or refuse to run unattended/cron) whenever the bypass env var is set, so a forgotten migration flag doesn't silently stay enabled |
| 2 | skills/hermes-attestation-guardian/SKILL.md:154,224 | Same unsigned-bypass pattern as #1, Hermes-specific | Same mitigation: emit a recurring high-visibility warning while `HERMES_ADVISORY_ALLOW_UNSIGNED_FEED=1` remains set, rather than relying on operator memory to unset it |
| 3 | package.json:22-40 | Caret-range dependencies can silently pull a new minor/patch version with different transitive deps on a fresh `npm install` | Consider `npm shrinkwrap`/exact pinning for security-sensitive deps, or rely on the committed `package-lock.json` (already present) and add a CI check that fails on lockfile drift |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/claw-release/SKILL.md | "Existing Skills" table (lines ~241-249) lists only 5 of the repo's 16 skills as an authoritative catalog | -10 |
| 2 | skills/clawsec-scanner/SKILL.md | Vague quantifier "comprehensive"/"Comprehensive" used 3x (lines 14, 35, 482) | -6 |
| 3 | skills/clawsec-feed/SKILL.md | Vague quantifier "relevant" (line 386) | -2 |
| 4 | skills/clawsec-suite/SKILL.md | Vague quantifier "relevant" (line 389) | -2 |
| 5 | skills/openclaw-audit-watchdog/SKILL.md | Vague quantifier "robust" (line 438) | -2 |

## Cross-Component
- **skill.json ↔ SKILL.md version consistency**: verified all 16 skills — every `skill.json` `version` field matches its sibling `SKILL.md` frontmatter `version` (CI-enforced per CLAUDE.md, and confirmed independently here).
- **`claw-release/SKILL.md` "Existing Skills" table is stale**: it lists `clawsec-feed`, `clawtributor`, `openclaw-audit-watchdog`, `soul-guardian`, and `claw-release` as the full catalog, but `skills/` contains 16 directories today (missing: `clawsec-clawhub-checker`, `clawsec-nanoclaw`, `clawsec-scanner`, `clawsec-suite`, `hermes-attestation-guardian`, `hermes-traffic-guardian`, `nanoclaw-traffic-guardian`, `openclaw-traffic-guardian`, `picoclaw-security-guardian`, `picoclaw-self-pen-testing`, `picoclaw-traffic-guardian`). This is the one orphan/stale-count finding of the audit.
- **Cross-skill trust-boundary references** (e.g. `openclaw-traffic-guardian` explicitly disclaiming overlap with `clawsec-scanner`/`openclaw-audit-watchdog`/`soul-guardian`; `*-traffic-guardian` skills each pointing to their platform-specific `*-security-guardian`/`*-attestation-guardian` sibling for posture export) are internally consistent — no contradictions found.
- **Signing-key fingerprint consistency**: all `RELEASE_PUBKEY_SHA256` references across the 16 SKILL.md files and the 3 canonical `.pem` locations resolve to the same fingerprint (enforced by `scripts/ci/verify_signing_key_consistency.sh`, spot-checked here).
- No orphaned components or broken relative links found among the checked artifacts.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes. There are no bugs and no Critical/High security findings. The one NL quality issue worth a PR is the stale "Existing Skills" table in `skills/claw-release/SKILL.md` (Quality Issue #1 / Cross-Component finding). The three documented unsigned-verification-bypass flags and the caret-range dependency pinning are Low-severity, already-labeled design tradeoffs — safe to mention in an issue for the maintainer's awareness rather than urgent fixes.
