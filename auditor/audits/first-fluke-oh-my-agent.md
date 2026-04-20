# NLPM Audit: first-fluke/oh-my-agent
**Date**: 2026-04-20  |  **Artifacts**: 41  |  **Strategy**: batched
**NL Score**: 86/100
**Security**: BLOCKED
**Bugs**: 2  |  **Quality Issues**: 18  |  **Security Findings**: 10

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .agents/skills/oma-coordination/SKILL.md | skill | 80 | Missing output format specification |
| cli/CLAUDE.md | doc | 80 | Auto-managed OMA block only; minimal standalone content |
| .agents/agents/architecture-reviewer.md | agent | 80 | No model declared; no examples |
| .agents/agents/backend-engineer.md | agent | 80 | No model declared; no examples |
| .agents/agents/db-engineer.md | agent | 80 | No model declared; no examples |
| .agents/agents/debug-investigator.md | agent | 80 | No model declared; no examples |
| .agents/agents/frontend-engineer.md | agent | 80 | No model declared; no examples |
| .agents/agents/mobile-engineer.md | agent | 80 | No model declared; no examples |
| .agents/agents/pm-planner.md | agent | 80 | No model declared; no examples |
| .agents/agents/qa-reviewer.md | agent | 80 | No model declared; no examples |
| .agents/agents/tf-infra-engineer.md | agent | 80 | No model declared; no examples |
| .agents/skills/oma-mobile/SKILL.md | skill | 82 | Minimal body; heavy reliance on unlisted resource files |
| hooks/hooks.json | config | 85 | No inline documentation on hook purpose |
| CLAUDE.md | doc | 85 | Good structure; Project Rules table references unlisted rule files |
| .agents/skills/oma-debug/SKILL.md | skill | 85 | Brief body; substantive content deferred to resource files |
| .agents/hooks/variants/gemini.json | config | 87 | Timeout values in ms (5000) differ from other variants (seconds: 5) |
| .agents/skills/oma-architecture/SKILL.md | skill | 87 | "lightest sufficient methodology" — vague qualifier |
| .agents/skills/oma-frontend/SKILL.md | skill | 87 | Core rules section brief; detail deferred to resource files |
| .agents/skills/oma-pm/SKILL.md | skill | 87 | No inline task examples; references external examples.md |
| .agents/hooks/variants/codex.json | config | 88 | No statusLine entry (Claude-only feature, acceptable) |
| .agents/hooks/variants/cursor.json | config | 88 | Missing Stop/persistent-mode event |
| .agents/hooks/variants/qwen.json | config | 88 | No statusLine entry |
| .agents/skills/oma-brainstorm/SKILL.md | skill | 88 | Execution protocol deferred to vendor injection; no fallback shown |
| .agents/skills/oma-design/SKILL.md | skill | 88 | "appropriate for the target audience" — vague qualifier |
| .agents/skills/oma-qa/SKILL.md | skill | 88 | "When relevant, map findings to ISO…" — vague trigger |
| .claude-plugin/plugin.json | config | 88 | `skills`/`agents` paths point to .claude/ not .agents/; depends on install |
| cli/commands/migrations/README.md | doc | 88 | Good technical docs; no frontmatter |
| .agents/hooks/core/triggers.json | config | 90 | Comprehensive; no issues |
| .agents/hooks/variants/claude.json | config | 90 | Well-structured; complete |
| .agents/skills/oma-backend/SKILL.md | skill | 90 | Detailed and well-structured |
| .agents/skills/oma-dev-workflow/SKILL.md | skill | 90 | Very detailed with code examples |
| .agents/skills/oma-orchestrator/SKILL.md | skill | 90 | Typo: "oh-my-ag agent:spawn" (line 23) |
| .agents/skills/oma-pdf/SKILL.md | skill | 90 | Good examples and output formats |
| .agents/skills/oma-recap/SKILL.md | skill | 90 | Detailed output format spec |
| .agents/skills/oma-search/SKILL.md | skill | 90 | Invocation examples included |
| .agents/skills/oma-tf-infra/SKILL.md | skill | 90 | Very detailed; multi-cloud mapping table |
| .agents/hooks/variants/hook-variant.schema.json | config | 92 | Well-documented JSON Schema |
| .agents/skills/oma-db/SKILL.md | skill | 92 | "oh-my-agent agent:spawn" inconsistency vs "oma agent:spawn" |
| .agents/skills/oma-hwp/SKILL.md | skill | 92 | Excellent examples; security note on kordoc |
| .agents/skills/oma-scm/SKILL.md | skill | 92 | Rich commit workflow with concrete examples |
| .agents/skills/oma-translator/SKILL.md | skill | 95 | Exemplary detail; 7-stage workflow; no issues found |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 2 |
| High | 1 |
| Medium | 4 |
| Low | 3 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks (hooks.json) | hooks/hooks.json |
| Scripts (.sh) | .agents/hooks/core/filter-test-output.sh, .agents/skills/oma-orchestrator/scripts/parallel-run.sh, .agents/skills/oma-orchestrator/scripts/spawn-agent.sh, .agents/skills/oma-orchestrator/scripts/verify.sh, benchmarks/collect.sh, benchmarks/run.sh, benchmarks/scoring/auto-score.sh, benchmarks/scoring/visual-score.sh, cli/install.sh, docs/demo/demo-combined.sh, docs/demo/demo-v2.sh |
| MCP configs | None found |
| Package manifests | package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | CRITICAL | cli/install.sh | 85 | curl-pipe-to-bash | `download_to_stdout https://bun.sh/install \| bash` — downloads and executes the bun installer directly from the internet with no checksum or signature verification |
| 2 | CRITICAL | cli/install.sh | 106 | curl-pipe-to-sh | `download_to_stdout https://astral.sh/uv/install.sh \| sh` — downloads and executes the uv installer directly from the internet with no integrity check |
| 3 | HIGH | benchmarks/run.sh | 356–363 | third-party install.sh execution | Clones `affaan-m/everything-claude-code` then runs its `install.sh --profile full` without any integrity verification; a compromised upstream would execute arbitrary code |
| 4 | MEDIUM | benchmarks/run.sh | 289 | unpinned runtime package | `bunx oh-my-agent@latest install` — resolves the latest version at runtime; no version pin or checksum check |
| 5 | MEDIUM | benchmarks/run.sh | 313–317 | unverified third-party clone | `git clone https://github.com/Yeachan-Heo/oh-my-claudecode` — cloned repo is loaded via `--plugin-dir` and executed; no tag, commit hash, or signature pinned |
| 6 | MEDIUM | benchmarks/run.sh | 394–398 | unverified third-party clone | `git clone https://github.com/obra/superpowers` — same pattern; cloned repo executed as a Claude Code plugin without integrity verification |
| 7 | MEDIUM | benchmarks/scoring/auto-score.sh | 134 | bash -c with constructed path | `bash -c "cd $(printf '%q' "$PROJECT_DIR") && npm install && npm run build"` — uses `bash -c` with a shell-constructed argument; `printf '%q'` mitigates injection but the pattern is fragile and unnecessary |
| 8 | LOW | cli/install.sh | 142 | unpinned package invocation | `exec bunx oh-my-agent@latest < /dev/tty` — @latest resolves at runtime without pinning; a breaking or malicious update would affect all installs |
| 9 | LOW | hooks/hooks.json | 3–12 | verbose hook trigger | `UserPromptSubmit` hook fires on every user prompt; if the hook script has a bug or is replaced, it could inadvertently process all user input |
| 10 | LOW | package.json | 12 | prepare script | `"prepare": "husky"` runs automatically on `npm install`; any contributor running install will execute this hook setup silently |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .agents/skills/oma-orchestrator/SKILL.md:23 | Truncated command name: `oh-my-ag agent:spawn` — missing "ent"; should be `oma agent:spawn` or `oh-my-agent agent:spawn` | Agents following this skill will invoke a non-existent CLI command and silently fail fallback dispatch |
| 2 | .agents/skills/oma-db/SKILL.md:78 | Inconsistent CLI reference: `oh-my-agent agent:spawn` while every other skill uses `oma agent:spawn` | Creates confusion about the correct CLI entrypoint; could cause failures in environments where only `oma` is in PATH |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | benchmarks/run.sh:289 | `bunx oh-my-agent@latest install` — unpinned | Pin to a specific version: `bunx oh-my-agent@5.13.0 install` and update on intentional upgrades |
| 2 | benchmarks/run.sh:313–317 | `git clone https://github.com/Yeachan-Heo/oh-my-claudecode` without ref | Clone a pinned tag: `git clone --depth 1 --branch vX.Y.Z ...` or verify commit hash post-clone |
| 3 | benchmarks/run.sh:394–398 | `git clone https://github.com/obra/superpowers` without ref | Same: pin to a tag or commit hash |
| 4 | benchmarks/scoring/auto-score.sh:134 | `bash -c "cd $(printf '%q' ...) && ..."` pattern | Replace with subshell: `(cd "$PROJECT_DIR" && npm install && npm run build)` |
| 5 | cli/install.sh:142 | `bunx oh-my-agent@latest` — unpinned | Document the intentional @latest choice or pin to a minimum version |
| 6 | hooks/hooks.json | No comment explaining hook purpose or what data it accesses | Add an inline doc field or README entry describing what keyword-detector.ts and persistent-mode.ts do with prompt content |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | All 9 agent files | No `model` field in frontmatter — Claude Code cannot route to correct tier | -5 each |
| 2 | All 9 agent files | Zero inline examples — users cannot infer output format from agent definition alone | -15 each |
| 3 | .agents/agents/mobile-engineer.md | Charter Preflight block missing LOW/MEDIUM/HIGH procedure descriptions (present in other agents) | -3 |
| 4 | .agents/agents/frontend-engineer.md | Charter Preflight block missing LOW/MEDIUM/HIGH procedure descriptions | -3 |
| 5 | .agents/skills/oma-coordination/SKILL.md | No output format section — skill doesn't declare what it produces | -10 |
| 6 | .agents/skills/oma-mobile/SKILL.md | Minimal prose; all substantive content deferred to unlisted resource files | -8 |
| 7 | .agents/skills/oma-architecture/SKILL.md | "Use the lightest sufficient methodology" — "sufficient" is vague; no measurable criteria | -2 |
| 8 | .agents/skills/oma-design/SKILL.md | "fonts appropriate for the target audience" — "appropriate" is a vague quantifier | -2 |
| 9 | .agents/skills/oma-qa/SKILL.md | "When relevant, map findings to ISO/IEC 25010" — "relevant" is vague; no trigger condition | -2 |
| 10 | .agents/hooks/variants/gemini.json | Timeout values are in milliseconds (5000) while all other variants use seconds (5) — likely correct for Gemini's API but undocumented | informational |
| 11 | .claude-plugin/plugin.json | `"skills": "./.claude/skills/"` and `"agents": "./.claude/agents/"` — paths point to .claude/ installation target, not the source .agents/ directory; works post-install but confusing during development | informational |
| 12 | cli/CLAUDE.md | Entire content is within OMA:START/END managed block; manually adding project-specific instructions below the block is not documented | informational |
| 13 | .agents/skills/oma-orchestrator/SKILL.md | "oh-my-ag agent:spawn" typo (see Bugs #1) | -10 |
| 14 | .agents/skills/oma-db/SKILL.md | Inconsistent CLI reference (see Bugs #2) | -3 |
| 15 | .agents/skills/oma-brainstorm/SKILL.md | Execution protocol section says "injected automatically by `oma agent:spawn`" — no fallback behaviour documented for direct invocation | -3 |
| 16 | All 20 skill files | Core workflow content deferred to `resources/execution-protocol.md` — quality of skill depends on unlisted files not included in this audit | informational |
| 17 | .agents/agents/qa-reviewer.md | `qa-reviewer` has an excellent inline `## Output Format` section — other agents should follow this pattern | informational (positive exemplar) |
| 18 | .agents/skills/oma-translator/SKILL.md | Exemplary: 7-stage workflow, mechanical verification gate, figurative-language mapping — this is the standard all skills should target | informational (positive exemplar) |

## Cross-Component
**Broken references**
- `oma-orchestrator/SKILL.md:23`: `oh-my-ag agent:spawn` — truncated command; should be `oma agent:spawn`. No other component defines this CLI alias.
- `oma-db/SKILL.md:78`: uses `oh-my-agent agent:spawn`; all other 18 skill files use `oma agent:spawn`. Inconsistency could confuse consumers inheriting from this skill.

**Orphaned / unverifiable references**
- All skill files reference `resources/execution-protocol.md`, `resources/examples.md`, `resources/checklist.md`, etc. None of these resource files were included in the audit scope. Their quality is unknown and the skills are partially opaque without them.
- `CLAUDE.md` Project Rules table references `.agents/rules/*.md` files (debug.md, quality.md, i18n-guide.md, etc.) — not included in audit scope.

**Contradictions**
- `cli/CLAUDE.md` and root `CLAUDE.md` share identical OMA architecture sections (expected — auto-managed). No contradiction.
- Hook variant files consistently reference `.agents/hooks/core/` scripts (`keyword-detector.ts`, `skill-injector.ts`, `persistent-mode.ts`, `test-filter.ts`, `hud.ts`) — not listed in audit scope, so existence is unverified. The `filter-test-output.sh` found in `.agents/hooks/core/` corresponds to `test-filter.ts` in the variants, suggesting a TypeScript wrapper exists.
- `hooks/hooks.json` (root) only includes `UserPromptSubmit` + `Stop` hooks; variants also include `PreToolUse`. This is intentional: the root hooks.json is the plugin's deployed configuration for Claude Code, while variants are the source definitions for `oma install`.

**Timeout units inconsistency**
- `gemini.json` uses 5000 (ms), all other variants use 5 (seconds). If the variants are processed by a single code path that doesn't account for unit differences per vendor, Gemini hooks would timeout 1000× faster than intended. This warrants verification in the hook runner.

## Recommendation
BLOCKED — do not submit PRs. File a private security report for findings #1 and #2 (curl-pipe-to-shell in cli/install.sh) and finding #3 (unverified third-party install.sh execution in benchmarks/run.sh). These are the patterns that triggered the Critical pre-scan flag.

Once the Critical/High security findings are resolved through private disclosure and patched releases, the following work items are ready:
- **NL fix PRs**: Bugs #1 (oma-orchestrator typo) and #2 (oma-db CLI inconsistency) are safe to submit as public PRs.
- **Medium/Low security fixes**: Items 1–6 in the Security Fixes table can be submitted as a separate public PR after Critical/High are patched.
- The 9 agent files would benefit significantly from adding a `model` field and at least one inline example — a high-leverage quality improvement across the whole plugin.
