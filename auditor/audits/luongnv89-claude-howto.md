# NLPM Audit: luongnv89/claude-howto
**Date**: 2026-04-19  |  **Artifacts**: 117  |  **Strategy**: progressive
**NL Score**: 77/100
**Security**: REVIEW
**Bugs**: 4  |  **Quality Issues**: 275  |  **Security Findings**: 7

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| vi/07-plugins/documentation/agents/api-documenter.md | agent | 68 | No model, no examples, no output format, vague "comprehensive" |
| vi/07-plugins/documentation/agents/example-generator.md | agent | 68 | No model, no examples, no output format, vague "practical" |
| zh/07-plugins/documentation/agents/api-documenter.md | agent | 68 | No model, no examples, no output format, vague "comprehensive" |
| zh/07-plugins/documentation/agents/example-generator.md | agent | 68 | No model, no examples, no output format, vague "practical" |
| 07-plugins/documentation/agents/api-documenter.md | agent | 68 | No model, no examples, no output format, vague "comprehensive" |
| 07-plugins/documentation/agents/example-generator.md | agent | 68 | No model, no examples, no output format, vague "practical" |
| uk/07-plugins/documentation/agents/api-documenter.md | agent | 68 | No model, no examples, no output format, vague "comprehensive" |
| uk/07-plugins/documentation/agents/example-generator.md | agent | 68 | No model, no examples, no output format, vague "practical" |
| vi/07-plugins/pr-review/agents/security-reviewer.md | agent | 70 | No model, no examples, no output format |
| vi/07-plugins/pr-review/agents/test-checker.md | agent | 70 | No model, no examples, no output format |
| vi/07-plugins/pr-review/agents/performance-analyzer.md | agent | 70 | No model, no examples, no output format |
| vi/07-plugins/devops-automation/agents/alert-analyzer.md | agent | 70 | No model, no examples, no output format |
| vi/07-plugins/devops-automation/agents/deployment-specialist.md | agent | 70 | No model, no examples, no output format |
| vi/07-plugins/devops-automation/agents/incident-commander.md | agent | 70 | No model, no examples, no output format |
| vi/07-plugins/documentation/agents/code-commentator.md | agent | 70 | No model, no examples, no output format |
| zh/07-plugins/pr-review/agents/security-reviewer.md | agent | 70 | No model, no examples, no output format |
| zh/07-plugins/pr-review/agents/test-checker.md | agent | 70 | No model, no examples, no output format |
| zh/07-plugins/pr-review/agents/performance-analyzer.md | agent | 70 | No model, no examples, no output format |
| zh/07-plugins/devops-automation/agents/alert-analyzer.md | agent | 70 | No model, no examples, no output format |
| zh/07-plugins/devops-automation/agents/deployment-specialist.md | agent | 70 | No model, no examples, no output format |
| zh/07-plugins/devops-automation/agents/incident-commander.md | agent | 70 | No model, no examples, no output format |
| zh/07-plugins/documentation/agents/code-commentator.md | agent | 70 | No model, no examples, no output format |
| 07-plugins/pr-review/agents/security-reviewer.md | agent | 70 | No model, no examples, no output format |
| 07-plugins/pr-review/agents/test-checker.md | agent | 70 | No model, no examples, no output format |
| 07-plugins/pr-review/agents/performance-analyzer.md | agent | 70 | No model, no examples, no output format |
| 07-plugins/devops-automation/agents/alert-analyzer.md | agent | 70 | No model, no examples, no output format |
| 07-plugins/devops-automation/agents/deployment-specialist.md | agent | 70 | No model, no examples, no output format |
| 07-plugins/devops-automation/agents/incident-commander.md | agent | 70 | No model, no examples, no output format |
| 07-plugins/documentation/agents/code-commentator.md | agent | 70 | No model, no examples, no output format |
| uk/07-plugins/pr-review/agents/security-reviewer.md | agent | 70 | No model, no examples, no output format |
| uk/07-plugins/pr-review/agents/test-checker.md | agent | 70 | No model, no examples, no output format |
| uk/07-plugins/pr-review/agents/performance-analyzer.md | agent | 70 | No model, no examples, no output format |
| uk/07-plugins/devops-automation/agents/alert-analyzer.md | agent | 70 | No model, no examples, no output format |
| uk/07-plugins/devops-automation/agents/deployment-specialist.md | agent | 70 | No model, no examples, no output format |
| uk/07-plugins/devops-automation/agents/incident-commander.md | agent | 70 | No model, no examples, no output format |
| uk/07-plugins/documentation/agents/code-commentator.md | agent | 70 | No model, no examples, no output format |
| vi/07-plugins/pr-review/commands/review-pr.md | command | 73 | No allowed-tools, no empty-input handling, no output format, vague "comprehensive" |
| zh/07-plugins/pr-review/commands/review-pr.md | command | 73 | No allowed-tools, no empty-input handling, no output format, vague "comprehensive" |
| 07-plugins/pr-review/commands/review-pr.md | command | 73 | No allowed-tools, no empty-input handling, no output format, vague "comprehensive" |
| uk/07-plugins/pr-review/commands/review-pr.md | command | 73 | No allowed-tools, no empty-input handling, no output format, vague "comprehensive" |
| vi/07-plugins/pr-review/commands/check-tests.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| vi/07-plugins/pr-review/commands/check-security.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| vi/07-plugins/devops-automation/commands/rollback.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| vi/07-plugins/devops-automation/commands/incident.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| vi/07-plugins/devops-automation/commands/status.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| vi/07-plugins/devops-automation/commands/deploy.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| vi/07-plugins/documentation/commands/validate-docs.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| vi/07-plugins/documentation/commands/generate-api-docs.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| vi/07-plugins/documentation/commands/generate-readme.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| vi/07-plugins/documentation/commands/sync-docs.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| zh/07-plugins/pr-review/commands/check-tests.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| zh/07-plugins/pr-review/commands/check-security.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| zh/07-plugins/devops-automation/commands/rollback.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| zh/07-plugins/devops-automation/commands/incident.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| zh/07-plugins/devops-automation/commands/status.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| zh/07-plugins/devops-automation/commands/deploy.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| zh/07-plugins/documentation/commands/validate-docs.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| zh/07-plugins/documentation/commands/generate-api-docs.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| zh/07-plugins/documentation/commands/generate-readme.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| zh/07-plugins/documentation/commands/sync-docs.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| 07-plugins/pr-review/commands/check-tests.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| 07-plugins/pr-review/commands/check-security.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| 07-plugins/devops-automation/commands/rollback.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| 07-plugins/devops-automation/commands/incident.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| 07-plugins/devops-automation/commands/status.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| 07-plugins/devops-automation/commands/deploy.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| 07-plugins/documentation/commands/validate-docs.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| 07-plugins/documentation/commands/generate-api-docs.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| 07-plugins/documentation/commands/generate-readme.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| 07-plugins/documentation/commands/sync-docs.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| uk/07-plugins/pr-review/commands/check-tests.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| uk/07-plugins/pr-review/commands/check-security.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| uk/07-plugins/devops-automation/commands/rollback.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| uk/07-plugins/devops-automation/commands/incident.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| uk/07-plugins/devops-automation/commands/status.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| uk/07-plugins/devops-automation/commands/deploy.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| uk/07-plugins/documentation/commands/validate-docs.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| uk/07-plugins/documentation/commands/generate-api-docs.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| uk/07-plugins/documentation/commands/generate-readme.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| uk/07-plugins/documentation/commands/sync-docs.md | command | 75 | No allowed-tools, no empty-input handling, no output format |
| vi/03-skills/brand-voice/SKILL.md | skill | 85 | No model, no declared output format |
| 03-skills/brand-voice/SKILL.md | skill | 85 | No model, no declared output format |
| zh/03-skills/brand-voice/SKILL.md | skill | 85 | No model, no declared output format |
| .claude/skills/self-assessment/SKILL.md | skill | 95 | No model declared |
| .claude/skills/lesson-quiz/SKILL.md | skill | 95 | No model declared |
| vi/03-skills/code-review/SKILL.md | skill | 95 | No model declared |
| vi/03-skills/refactor/SKILL.md | skill | 95 | No model declared |
| vi/03-skills/claude-md/SKILL.md | skill | 95 | No model declared |
| vi/03-skills/blog-draft/SKILL.md | skill | 95 | No model declared |
| 03-skills/code-review/SKILL.md | skill | 95 | No model declared |
| 03-skills/refactor/SKILL.md | skill | 95 | No model declared |
| 03-skills/claude-md/SKILL.md | skill | 95 | No model declared |
| 03-skills/doc-generator/SKILL.md | skill | 95 | No model declared |
| 03-skills/blog-draft/SKILL.md | skill | 95 | No model declared |
| zh/03-skills/code-review/SKILL.md | skill | 95 | No model declared |
| zh/03-skills/refactor/SKILL.md | skill | 95 | No model declared |
| zh/03-skills/claude-md/SKILL.md | skill | 95 | No model declared |
| zh/03-skills/doc-generator/SKILL.md | skill | 95 | No model declared |
| zh/03-skills/blog-draft/SKILL.md | skill | 95 | No model declared |
| uk/03-skills/code-review/SKILL.md | skill | 95 | No model declared |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 4 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts | 5 (scripts/build_epub.py, scripts/check_links.py, scripts/check_mermaid.py, scripts/check_cross_references.py, scripts/sync_translations.py) |
| MCP configs | 0 |
| Package manifests | 2 (scripts/requirements.txt, scripts/requirements-dev.txt) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | MEDIUM | scripts/build_epub.py | 291–309 | subprocess with user-controlled binary path | `subprocess.run(cmd, ...)` where `cmd[0]` is `config.mmdc_path`, set via `--mmdc-path` CLI arg. Not `shell=True`, so no shell injection, but caller controls the executed binary. nosec B603 annotation present. Acceptable for a local dev tool; flag if ever used in a CI service context. |
| 2 | MEDIUM | scripts/check_links.py | 70 | Network calls with markdown-sourced URLs | `urllib.request.urlopen()` fetches arbitrary URLs extracted from markdown files. In a server-side context this is an SSRF vector; in a local pre-commit hook the risk is low but URLs could redirect to internal endpoints. nosec B310 annotation present. |
| 3 | MEDIUM | scripts/check_mermaid.py | 56 | subprocess with environment-influenced args | `subprocess.run(["mmdc", "-i", tmp_path, "-o", out_path, *extra_args])` where `extra_args` comes from `os.environ.get("MERMAID_PUPPETEER_NO_SANDBOX")`. The env flag controls `--no-sandbox` passed to Chrome/Puppeteer. nosec B603 B607 annotations present. |
| 4 | LOW | scripts/check_mermaid.py | 30 | Environment variable access | `os.environ.get("MERMAID_PUPPETEER_NO_SANDBOX")` used to disable Chrome sandbox for mmdc. An attacker who can set env vars in CI could force sandbox-off rendering. |
| 5 | LOW | scripts/requirements.txt | 1–7 | Unpinned dependency versions | All 6 packages (ebooklib, markdown, beautifulsoup4, httpx, pillow, tenacity) are fully unpinned. A compromised upstream release could silently introduce malicious code on `pip install`. |
| 6 | LOW | scripts/requirements-dev.txt | 4–11 | Partially unpinned dev dependencies | `pytest>=7.0`, `ruff>=0.8.0`, `bandit>=1.7.7`, `mypy>=1.8.0` specify minimums but not upper bounds, allowing unexpected major-version upgrades. |
| 7 | LOW | scripts/check_cross_references.py | 91 | File path traversal (theoretical) | `(file_path.parent / link_path).resolve()` resolves relative markdown links without constraining them to the repo root. A crafted `../../etc/passwd` link in a markdown file would resolve but not be read; it only checks `.exists()`. Low practical risk. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | vi/07-plugins/pr-review/agents/security-reviewer.md | `tools` declares `diff` — not a valid Claude Code tool name (use `bash` to invoke diff) | Agent registration may silently ignore unknown tool, resulting in no diff capability |
| 2 | zh/07-plugins/pr-review/agents/security-reviewer.md | Same as #1 | Same |
| 3 | 07-plugins/pr-review/agents/security-reviewer.md | Same as #1 | Same |
| 4 | uk/07-plugins/pr-review/agents/security-reviewer.md | Same as #1 | Same |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/requirements.txt | All 6 packages fully unpinned | Pin to known-good versions: `ebooklib==0.18`, `markdown==3.7`, `beautifulsoup4==4.12.3`, `httpx==0.28.1`, `pillow==11.1.0`, `tenacity==9.0.0` |
| 2 | scripts/requirements-dev.txt | Dev packages have floor-only bounds | Add upper bounds or use `pip-tools`/`uv lock` to generate a lockfile |
| 3 | scripts/check_links.py | `urlopen` with unvalidated markdown URLs | Add a URL allowlist or restrict to `https://` only; consider `--no-network` flag to skip in air-gapped environments |
| 4 | scripts/check_cross_references.py | `resolve()` without repo-root bound check | Wrap with: `if not resolved.is_relative_to(Path().resolve()): continue` |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | All 36 agents (vi/zh/07-plugins/uk × 9 types) | No `model` field in frontmatter | -5 each (−180 total) |
| 2 | All 36 agents | Zero example blocks | -15 each (−540 total) |
| 3 | All 36 agents | No output format section | -10 each (−360 total) |
| 4 | All 44 commands | No `allowed-tools` field in frontmatter | -5 each (−220 total) |
| 5 | All 44 commands | No empty-input handling | -10 each (−440 total) |
| 6 | All 44 commands | No output format section | -10 each (−440 total) |
| 7 | All 20 skills | No `model` field in frontmatter | -5 each (−100 total) |
| 8 | vi/03-skills/brand-voice/SKILL.md, 03-skills/brand-voice/SKILL.md, zh/03-skills/brand-voice/SKILL.md | No explicit output format section (reference skill describes vocabulary and tone but not when/how output is applied) | -10 each (−30 total) |
| 9 | api-documenter agents ×4 locales | Vague quantifier "comprehensive" in body | -2 each (−8 total) |
| 10 | example-generator agents ×4 locales | Vague quantifier "practical" in body | -2 each (−8 total) |
| 11 | review-pr commands ×4 locales | Vague quantifier "comprehensive" in description | -2 each (−8 total) |
| 12 | All 36 agents | Very thin body (4–5 bullet points only) — no behavioral instructions, no dispatch logic, no error handling | Informational: agents are stubs, not production-quality |
| 13 | All 44 commands | Commands do not dispatch to the named agents (review-pr does not invoke security-reviewer, etc.) | Informational: cross-component wiring is absent |
| 14 | deployment-specialist and incident-commander agents (×4 locales) | Declare `write` tool but have no write-path behavior described; write access on analysis agents is over-privileged | Informational |

## Cross-Component
**Missing agent dispatch**: The `review-pr.md` command lists 5 steps (security analysis, test coverage, docs, quality, performance) but does not dispatch to `security-reviewer`, `test-checker`, or `performance-analyzer` subagents. Commands and agents are defined in the same plugin but are not wired together. Every command in every locale has this gap.

**Over-privileged agents**: `deployment-specialist` and `incident-commander` declare `write` and `bash` tools. `incident-commander` is described as a coordination agent ("status updates", "team coordination") but `write` is only needed for creating incident records. `bash` is potentially dangerous in incident response context — should be scoped or removed.

**Locale consistency**: The vi, zh, and uk translations are faithful copies of the English (07-plugins) originals. All issues in the English version are reproduced identically across all three translated versions. No locale-specific divergence detected.

**`diff` tool reference**: All four `security-reviewer.md` files declare `tools: read, grep, diff`. `diff` is not a Claude Code tool — it would need to be invoked via `bash`. This is a broken tool reference (Bug #1–4 above).

**Skills cross-reference integrity**: The `refactor` skill (all locales) references `references/code-smells.md` and `references/refactoring-catalog.md` at relative paths. These are tutorial reference files within the repo structure; the paths are internally consistent.

## Recommendation
REVIEW — submit NL fix PRs for Bugs #1–4 (replace `diff` with `bash` in security-reviewer frontmatter across all locales) and submit the Medium/Low security fixes in a separate PR. Flag security findings #1–3 in a GitHub issue for maintainer awareness. The broad quality gap (all agents lack model declaration, examples, and output format; all commands lack allowed-tools and empty-input handling) is a systemic gap across the entire plugin suite — these are tutorial stubs designed to illustrate plugin structure rather than production-ready artifacts, but a single bulk PR addressing model declarations and allowed-tools would raise the NL score from 77 to approximately 88.
