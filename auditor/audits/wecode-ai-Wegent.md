# NLPM Audit: wecode-ai/Wegent
**Date**: 2026-04-20  |  **Artifacts**: 12  |  **Strategy**: single
**NL Score**: 81/100
**Security**: BLOCKED
**Bugs**: 6  |  **Quality Issues**: 24  |  **Security Findings**: 8

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| backend/init_data/skills/mermaid-diagram/SKILL.md | skill | 67 | Missing `name` frontmatter (-25) |
| backend/init_data/skills/wiki_submit/SKILL.md | skill | 68 | Missing `name` frontmatter (-25) |
| backend/init_data/skills/sandbox/SKILL.md | skill | 69 | Missing `name` frontmatter (-25) |
| backend/init_data/skills/prompt-optimization/SKILL.md | skill | 71 | Missing `name` frontmatter (-25) |
| backend/init_data/skills/ui-links/SKILL.md | skill | 71 | Missing `name` frontmatter (-25) |
| backend/init_data/skills/wegent-knowledge/SKILL.md | skill | 75 | Missing `name` frontmatter (-25) |
| backend/init_data/skills/skill-creator/SKILL.md | skill | 83 | Pervasive vague quantifiers (-12) |
| backend/init_data/skills/browser/SKILL.md | skill | 91 | Vague language + missing output format section |
| backend/init_data/skills/conversation_to_prompt/SKILL.md | skill | 91 | No input→output example |
| tests/CLAUDE.md | project-instructions | 92 | Vague language (-8) |
| backend/init_data/skills/subscription-manager/SKILL.md | skill | 96 | Minor vague language (-4) |
| backend/init_data/skills/interactive-form-question/SKILL.md | skill | 98 | Minimal issues |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 1 |
| Medium | 4 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks (target-repo/hooks/) | 0 |
| Shell scripts (target-repo/scripts/) | 13 |
| Shell scripts (target-repo/scripts/hooks/) | 8 |
| MCP configs (.mcp.json) | 0 |
| Package manifests (frontend/package.json, deps/browser/relay-server/package.json, tests/package.json) | 3 |
| Requirements files (executor, executor_manager, wegent-cli, executor/code_server) | 4 |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | CRITICAL | scripts/run-e2e-local.sh | 122 | curl-pipe-sh | `curl -LsSf https://astral.sh/uv/install.sh \| sh` — bootstraps the `uv` tool manager by downloading and immediately executing an external script with no integrity check |
| 2 | HIGH | scripts/build-standalone.sh | 94 | eval with user-controlled input | `eval $BUILD_CMD` where `BUILD_CMD` is assembled from CLI args (`--tag`, `--platform`) and env vars (`IMAGE_NAME`, `IMAGE_TAG`); a malicious value like `--tag "foo; malicious_cmd"` achieves command injection |
| 3 | MEDIUM | scripts/smoke-test-workspace-recovery.sh | 44, 253 | eval with dynamic output | `eval "$(run_backend_python ...)"` and `eval "$(wait_for_new_assistant)"` — evals export statements generated from live database content; most string values use `shlex.quote()` but the pattern is inherently fragile |
| 4 | MEDIUM | scripts/run-module-tests.sh | 90 | eval pattern | `eval "$test_cmd"` — eval of a shell string constructed from hardcoded values inside the script; low actual exploit risk but violates secure-coding baseline |
| 5 | MEDIUM | scripts/fix-missing-project-id.sh | 22 | hardcoded default credential | `MYSQL_PASSWORD="${MYSQL_ROOT_PASSWORD:-123456}"` — password falls back to `123456` if the env var is unset; this default ships in a committed script |
| 6 | MEDIUM | scripts/run-e2e-local.sh | 135, 142 | hardcoded credentials | `DATABASE_URL` contains `root:123456@127.0.0.1:3306` and `SECRET_KEY="test-secret-key-for-e2e-testing"` are hardcoded; if this script is ever used against a shared environment the credentials are exposed |
| 7 | LOW | frontend/package.json | 12 | postinstall script | `"postinstall": "node scripts/download-fonts.cjs"` runs automatically on every `npm install`; downloads external font assets without pinned integrity hashes |
| 8 | LOW | executor/requirements.txt | 21–24 | unpinned dependency versions | `grpcio>=1.68.0`, `grpcio-tools>=1.68.0`, `protobuf>=5.29.5,<7.0.0`, `psutil>=5.9.0` allow unconstrained future versions; all other packages in this file are pinned |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | backend/init_data/skills/mermaid-diagram/SKILL.md | Missing required `name` frontmatter field (has `displayName` only) | Skill cannot be resolved by name in NLPM; registration may fail |
| 2 | backend/init_data/skills/prompt-optimization/SKILL.md | Missing required `name` frontmatter field | Same as above |
| 3 | backend/init_data/skills/sandbox/SKILL.md | Missing required `name` frontmatter field | Same as above |
| 4 | backend/init_data/skills/ui-links/SKILL.md | Missing required `name` frontmatter field | Same as above |
| 5 | backend/init_data/skills/wegent-knowledge/SKILL.md | Missing required `name` frontmatter field | Same as above |
| 6 | backend/init_data/skills/wiki_submit/SKILL.md | Missing required `name` frontmatter field | Same as above |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/run-module-tests.sh | `eval "$test_cmd"` on hardcoded string | Replace `eval "$test_cmd"` with direct invocation; split the string into an array: `cmd=($test_cmd); "${cmd[@]}"` |
| 2 | scripts/fix-missing-project-id.sh | Default password `123456` | Remove the default: `MYSQL_PASSWORD="${MYSQL_ROOT_PASSWORD:?MYSQL_ROOT_PASSWORD is required}"` — fail fast instead of using a known-weak default |
| 3 | scripts/run-e2e-local.sh | Hardcoded `root:123456` and `test-secret-key` | Move to a `.env.test` template with `.gitignore` entry; document required vars instead of embedding them |
| 4 | frontend/package.json | `postinstall` downloads fonts without SRI | Pin specific font file URLs and verify checksums in `download-fonts.cjs`, or bundle fonts directly |
| 5 | executor/requirements.txt | Four unpinned packages | Pin to exact versions: `grpcio==<current>`, `grpcio-tools==<current>`, `protobuf==<current>`, `psutil==<current>` |

> **Note**: Findings #1 (CRITICAL) and #2 (HIGH) require private security disclosure — do NOT include fixes in a public PR.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | mermaid-diagram/SKILL.md | "detailed error information" — vague | -2 |
| 2 | mermaid-diagram/SKILL.md | "fundamental" (error type) — vague | -2 |
| 3 | mermaid-diagram/SKILL.md | "good user experience" — vague | -2 |
| 4 | mermaid-diagram/SKILL.md | "meaningful labels" — vague | -2 |
| 5 | prompt-optimization/SKILL.md | "relevant to the user's request" — vague | -2 |
| 6 | prompt-optimization/SKILL.md | "complete, production-quality prompts" — vague | -2 |
| 7 | sandbox/SKILL.md | Description repeats "read_file/write_file" twice — copy-paste error | quality |
| 8 | sandbox/SKILL.md | "appropriate" timeouts — vague | -2 |
| 9 | sandbox/SKILL.md | "complex tasks" — vague | -2 |
| 10 | sandbox/SKILL.md | Placeholder credentials (`api_key: "xxxxx"`) in committed frontmatter — exposes config schema | quality |
| 11 | skill-creator/SKILL.md | "effective skills" (multiple occurrences) — vague | -2 |
| 12 | skill-creator/SKILL.md | "appropriate degrees of freedom" — vague | -2 |
| 13 | skill-creator/SKILL.md | "clear reason" — vague | -2 |
| 14 | skill-creator/SKILL.md | "comprehensive examples" — vague | -2 |
| 15 | skill-creator/SKILL.md | "clearly understood" — vague | -2 |
| 16 | skill-creator/SKILL.md | No formal output format section | -5 |
| 17 | subscription-manager/SKILL.md | "appropriate parameters" — vague | -2 |
| 18 | ui-links/SKILL.md | "appropriate protocol" — vague | -2 |
| 19 | browser/SKILL.md | "one comprehensive call" — vague | -2 |
| 20 | browser/SKILL.md | No explicit output format section | -5 |
| 21 | conversation_to_prompt/SKILL.md | No input→output example showing a real conversation being converted | -5 |
| 22 | wiki_submit/SKILL.md | No output format defined for tool responses | -5 |
| 23 | wiki_submit/SKILL.md | "simple command-line tool" — vague | -2 |
| 24 | tests/CLAUDE.md | "comprehensive check", "appropriate timeouts", "complex preparation" — vague (×3) | -8 |

## Cross-Component
**Inconsistent `name` vs `displayName` convention**: 6 of 11 SKILL.md files use only `displayName` in frontmatter and omit `name`. The other 2 Wegent-specific skills (`interactive-form-question`, `subscription-manager`) correctly include both. The `skill-creator` SKILL.md itself instructs authors to include `name` and `description` only — contradicting the richer schema used by Wegent's own skills (`displayName`, `version`, `author`, `tags`, `bindShells`, `mcpServers`). This creates an authoring trap for users following the bundled guide.

**Broken reference**: `tests/CLAUDE.md` line 47 references `./TEST_CASES.md`. This file was not present in the scanned tree. If absent, the cross-reference is broken.

**Credential pattern in skill frontmatter**: `sandbox/SKILL.md` embeds `api_key: "xxxxx"` / `base_url: "xxxxx"` / `model_id: "xxxxx"` as placeholder config in committed frontmatter. While not real secrets, this pattern normalizes credentials in skill files and could be mistakenly populated with real values by downstream users adapting the skill.

**`skill-creator` schema mismatch**: The `skill-creator` guide teaches a two-field frontmatter schema (`name`, `description`), but Wegent's actual skills use 8+ fields. A user following the bundled guide will produce skills incompatible with Wegent's own skill loader.

## Recommendation
**BLOCKED** — Critical and High security findings present. Do **not** submit any PRs to this repository until the following are addressed privately:

1. **CRITICAL** (`scripts/run-e2e-local.sh:122`): Replace `curl | sh` with a verified installer or pinned binary download with checksum validation. File a private security report with the maintainers.
2. **HIGH** (`scripts/build-standalone.sh:94`): Replace `eval $BUILD_CMD` with a direct `docker build` invocation using an array to avoid shell interpretation. File a private security report.

Once the Critical and High findings are resolved, the following are safe to PR publicly:
- Add `name` field to the 6 SKILL.md files missing it (6 bug fixes, straightforward)
- Medium/Low security fixes listed in the Security Fixes table above
- Quality improvements for vague language (informational, low priority)
