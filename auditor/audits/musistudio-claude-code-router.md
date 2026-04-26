# NLPM Audit: musistudio/claude-code-router
**Date**: 2026-04-26  |  **Artifacts**: 15  |  **Strategy**: single
**NL Score**: 79/100
**Security**: CLEAR
**Bugs**: 5  |  **Quality Issues**: 4  |  **Security Findings**: 5

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `docs/i18n/zh-CN/docusaurus-plugin-content-docs.backup.20260101_205603/cli/commands/preset.md` | cli-ref-zh | 65 | Router format bug: `openai:gpt-4` should be `openai,gpt-4` |
| `docs/docs/cli/commands/other.md` | cli-reference | 70 | Missing output format for all five commands |
| `docs/i18n/zh-CN/docusaurus-plugin-content-docs/current/cli/commands/other.md` | cli-ref-zh | 70 | Missing output format for all five commands |
| `docs/i18n/zh-CN/docusaurus-plugin-content-docs/current/cli/commands/start.md` | cli-ref-zh | 72 | Default port (3456) contradicts EN docs (8080) |
| `docs/i18n/zh-CN/docusaurus-plugin-content-docs/current/cli/commands/status.md` | cli-ref-zh | 72 | Default port (3456) contradicts EN docs (8080) |
| `docs/i18n/zh-CN/docusaurus-plugin-content-docs/current/cli/commands/statusline.md` | cli-ref-zh | 80 | Locale link missing `/zh` prefix |
| `docs/docs/cli/commands/model.md` | cli-reference | 82 | No explicit description in frontmatter |
| `docs/i18n/zh-CN/docusaurus-plugin-content-docs.backup.20260101_205603/cli/commands/statusline.md` | cli-ref-zh | 82 | Locale link missing `/zh` prefix |
| `docs/i18n/zh-CN/docusaurus-plugin-content-docs/current/cli/commands/model.md` | cli-ref-zh | 82 | No description in frontmatter |
| `docs/i18n/zh-CN/docusaurus-plugin-content-docs/current/cli/commands/preset.md` | cli-ref-zh | 82 | No description in frontmatter |
| `docs/docs/cli/commands/status.md` | cli-reference | 83 | No description in frontmatter |
| `docs/docs/cli/commands/start.md` | cli-reference | 84 | No description in frontmatter |
| `docs/docs/cli/commands/preset.md` | cli-reference | 85 | No description in frontmatter |
| `docs/docs/cli/commands/statusline.md` | cli-reference | 87 | No description in frontmatter |
| `CLAUDE.md` | project-guidance | 88 | "typically lightweight models" is vague |

**Weighted average: 79/100**

> **Scoring note**: These files are Docusaurus documentation pages, not NL skill/agent/command specs. The `name`/`description` YAML frontmatter rule is a false positive for this artifact type (Docusaurus uses `title`/`sidebar_position`). Scores reflect actual content quality: accuracy, completeness, output format coverage, and cross-language consistency.

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 4 |
| Low | 1 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts | 6 (`scripts/build.js`, `scripts/build-cli.js`, `scripts/build-core.js`, `scripts/build-server.js`, `scripts/build-shared.js`, `scripts/release.sh`) |
| MCP configs | 0 |
| Package manifests | 1 (`package.json`) |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | `scripts/release.sh` | 65 | `npm-publish-external` | Publishes `@musistudio/llms` to public npm registry; no provenance attestation or OTP enforcement — compromised CI credentials enable malicious release |
| 2 | Medium | `scripts/release.sh` | 124 | `npm-publish-external` | Publishes `@CCR/cli` to public npm registry under same conditions as finding #1 |
| 3 | Medium | `scripts/release.sh` | 159 | `docker-push-external` | Pushes Docker image to Docker Hub without content signing; compromised CI credentials enable image replacement |
| 4 | Medium | `scripts/release.sh` | 162 | `docker-push-external` | Pushes `latest` tag to Docker Hub — `latest` is widely consumed; unsigned push is higher-impact than versioned push |
| 5 | Low | `package.json` | 36 | `SEC-unpinned-semver` | All four devDependencies use `^` semver ranges; minor/patch bumps in `esbuild`, `typescript`, or `@types/node` can silently alter build output |

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `docs/i18n/zh-CN/docusaurus-plugin-content-docs/current/cli/commands/start.md` | Default port documented as **3456** but EN version says **8080**; one value is wrong | Users starting server with EN docs get wrong port expectation |
| 2 | `docs/i18n/zh-CN/docusaurus-plugin-content-docs/current/cli/commands/status.md` | Status example output shows port **3456**; EN example shows **8080** | Contradictory reference for the same tool option |
| 3 | `docs/i18n/zh-CN/docusaurus-plugin-content-docs.backup.20260101_205603/cli/commands/preset.md` | Router example at line 151 uses `"openai:gpt-4"` (colon) instead of `"openai,gpt-4"` (comma) | Readers copy-pasting the example get an invalid router config |
| 4 | `docs/i18n/zh-CN/docusaurus-plugin-content-docs.backup.20260101_205603/cli/commands/statusline.md` | Related command link `/docs/cli/commands/status` missing `/zh` locale prefix (line 401) | Link navigates to English page for zh-CN users |
| 5 | `docs/i18n/zh-CN/docusaurus-plugin-content-docs/current/cli/commands/statusline.md` | Related command link `/docs/cli/commands/status` missing locale prefix (line 400) | Same broken locale link as backup version; not fixed in current |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `scripts/release.sh` | npm publish (lines 65, 124) has no provenance or CI-gate | Add `--provenance` flag; add `if [ -z "$CI" ]; then echo "Must run in CI"; exit 1; fi` guard |
| 2 | `scripts/release.sh` | Docker push (lines 159, 162) uses unverified credentials without content signing | Enable Docker Content Trust (`export DOCKER_CONTENT_TRUST=1`) before push; gate push to CI |
| 3 | `package.json` | devDependencies use `^` ranges (line 36–39) | Pin to exact versions (`"esbuild": "0.25.1"`) and rely on lockfile for reproducible builds |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `docs/docs/cli/commands/other.md` | `ccr stop`, `ccr restart`, `ccr code`, `ccr ui`, `ccr activate` have no output format examples | -10 |
| 2 | `docs/i18n/zh-CN/docusaurus-plugin-content-docs/current/cli/commands/other.md` | zh-CN translation inherits same missing output coverage | -10 |
| 3 | `CLAUDE.md` | Line 50: "background: Background tasks (typically lightweight models)" — "typically" is vague; no model tier or example given | -2 |
| 4 | `docs/i18n/zh-CN/docusaurus-plugin-content-docs.backup.20260101_205603/cli/commands/preset.md` | Manifest example uses `"api_base_url": "https://api.openai.com/v1"` (bare) while EN and zh-CN current use `/v1/chat/completions` | -2 |

## Cross-Component

**Port default inconsistency (EN ↔ zh-CN):** `docs/docs/cli/commands/start.md` documents default port 8080; `docs/i18n/zh-CN/.../start.md` documents 3456. The same conflict appears in both `start.md` and `status.md`. Root cause is likely a default change that was only propagated to the zh-CN docs. Action: audit `packages/cli/src/` for the actual default and update the incorrect doc set.

**Backup directory in tracked repo:** `docs/i18n/zh-CN/docusaurus-plugin-content-docs.backup.20260101_205603/` contains two files that have already diverged from the current versions (wrong Router separator, wrong `api_base_url`, missing locale links). Backup directories in a tracked repo are a maintenance hazard: they are never updated, accumulate drift, and confuse automated scanners. Recommend removing this directory or adding it to `.gitignore`.

**zh-CN current `model.md` has extra section absent from EN:** The zh-CN version includes an "Interactive Features" section (lines 107–123) describing the full interactive model-management workflow, which is absent from the EN version. This is positive content that should be back-ported to EN.

**`statusline.md` locale link not fixed in current version:** Bug #4 (backup locale link) was not fixed when the file was promoted to current. Both versions share the identical broken link, suggesting the backup was copied without correction.

## Recommendation

CLEAR — submit PRs for all bugs and medium/low security fixes.

Priority order:
1. **Bug #3** (Router format): Highest user impact — broken config causes silent routing failure.
2. **Bugs #1 & #2** (port mismatch): Misleads users on first run; easy one-line fix once the authoritative default is confirmed.
3. **Bugs #4 & #5** (locale links): Low friction, high UX polish for zh-CN users.
4. **Security fixes #1 & #2** (provenance/CI gate): Adds supply-chain hygiene at low cost.
5. **Security fix #3** (pin devDeps): Standard lockfile hygiene.
6. **Quality #1 & #2** (other.md output format): Informational; improves completeness of reference.
