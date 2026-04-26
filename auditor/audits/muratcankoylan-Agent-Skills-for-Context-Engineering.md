# NLPM Audit: muratcankoylan/Agent-Skills-for-Context-Engineering
**Date**: 2026-04-26  |  **Artifacts**: 26  |  **Strategy**: batched
**NL Score**: 83/100
**Security**: CLEAR
**Bugs**: 4  |  **Quality Issues**: 11  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| examples/llm-as-judge-skills/agents/index.md | agent-index | 40 | Missing frontmatter name + description (-50), no output format (-10) |
| examples/llm-as-judge-skills/agents/evaluator-agent/evaluator-agent.md | agent | 50 | Missing frontmatter name + description (-50) |
| examples/llm-as-judge-skills/agents/orchestrator-agent/orchestrator-agent.md | agent | 50 | Missing frontmatter name + description (-50) |
| examples/llm-as-judge-skills/agents/research-agent/research-agent.md | agent | 50 | Missing frontmatter name + description (-50) |
| examples/digital-brain-skill/agents/AGENTS.md | agent-doc | 70 | Model not declared (-5), zero agent I/O examples (-15), no output format (-10) |
| examples/interleaved-thinking/generated_skills/comprehensive-research-agent/SKILL.md | skill | 80 | Missing version, italic formatting bugs (`*Silent` should be `**Silent`), vague words (-4) |
| template/SKILL.md | template | 80 | Placeholder examples only (-5), vague instructional words in template body (-8) |
| SKILL.md | skill | 82 | No concrete I/O examples (-10), minor vague words (-4) |
| examples/interleaved-thinking/SKILL.md | skill | 85 | Missing output format clarity (-5), platform-specific dependency (MiniMax M2.1) (-4) |
| CLAUDE.md | project-doc | 88 | No YAML frontmatter expected for this type; well-organized |
| examples/digital-brain-skill/SKILL.md | skill | 90 | Minor vague phrases ("when needed") (-4), references external scripts in workflows |
| skills/latent-briefing/SKILL.md | skill | 90 | Sparse examples section (one scenario) (-5), otherwise excellent |
| skills/bdi-mental-states/SKILL.md | skill | 90 | Highly specialized; minor vague phrases (-4), good coverage |
| examples/book-sft-pipeline/SKILL.md | skill | 92 | Excellent; minor: references external Tinker API (-2), small style nits |
| skills/hosted-agents/SKILL.md | skill | 92 | No dedicated `## Examples` I/O section (-5); guidelines/gotchas are strong |
| skills/advanced-evaluation/SKILL.md | skill | 93 | Excellent; minor: "appropriate" appears once (-2) |
| skills/tool-design/SKILL.md | skill | 93 | Excellent; minor vague phrase in gotchas (-2) |
| skills/project-development/SKILL.md | skill | 93 | Excellent; minor: "well-suited" in task table (-2) |
| skills/evaluation/SKILL.md | skill | 93 | Excellent; minor vague phrases (-2) |
| skills/filesystem-context/SKILL.md | skill | 95 | Exemplary structure, examples, gotchas |
| skills/context-degradation/SKILL.md | skill | 95 | Exemplary; research-backed thresholds, strong gotchas |
| skills/context-fundamentals/SKILL.md | skill | 95 | Exemplary; foundational reference |
| skills/context-optimization/SKILL.md | skill | 95 | Exemplary; concrete performance targets, clear decision table |
| skills/memory-systems/SKILL.md | skill | 95 | Exemplary; benchmark comparisons, framework comparison table |
| skills/context-compression/SKILL.md | skill | 95 | Exemplary; probe-based evaluation methodology well described |
| skills/multi-agent-patterns/SKILL.md | skill | 95 | Exemplary; telephone-game pattern with code fix is high-signal |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | None (only `.git/hooks/*.sample` — not active) |
| Scripts (Python) | examples/book-sft-pipeline/scripts/pipeline_example.py, examples/interleaved-thinking/reasoning_trace_optimizer/*.py, examples/digital-brain-skill/agents/scripts/*.py (4 files), skills/*/scripts/*.py (10 files), skills/context-compression/tests/test_compression_evaluator.py |
| Scripts (Shell) | examples/digital-brain-skill/scripts/install.sh |
| Scripts (JS) | examples/llm-as-judge-skills/eslint.config.js |
| MCP configs | None found |
| Package manifests | examples/digital-brain-skill/package.json, examples/llm-as-judge-skills/package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | skills/hosted-agents/scripts/sandbox_manager.py | 186 | credential-in-url | GitHub token embedded in git clone URL string (`x-access-token:{token}@github.com/...`); token is visible in process listings and command logs |
| 2 | Low | examples/llm-as-judge-skills/package.json | 58–64 | unpinned-semver | All production dependencies use `^` caret ranges (`ai: "^4.0.0"`, `@ai-sdk/openai: "^1.0.0"`, `@ai-sdk/anthropic: "^1.0.0"`, `zod: "^3.23.0"`, `dotenv: "^16.4.0"`); major-version lock only |
| 3 | Low | examples/digital-brain-skill/scripts/install.sh | 37 | unsanitized-user-input | Custom install path read from user via `read -p` is passed directly to `mkdir -p` and `cp -r` without sanitization; a path containing shell metacharacters or `..` traversal could write files outside intended directories |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | examples/llm-as-judge-skills/agents/evaluator-agent/evaluator-agent.md | Missing YAML frontmatter: no `name` or `description` fields | Cannot be registered or discovered by Claude Code as an agent; skill-loader fails silently |
| 2 | examples/llm-as-judge-skills/agents/orchestrator-agent/orchestrator-agent.md | Missing YAML frontmatter: no `name` or `description` fields | Same as above; orchestrator cannot be auto-activated |
| 3 | examples/llm-as-judge-skills/agents/research-agent/research-agent.md | Missing YAML frontmatter: no `name` or `description` fields | Same as above; research agent cannot be auto-activated |
| 4 | examples/llm-as-judge-skills/agents/index.md | Missing YAML frontmatter: no `name` or `description` fields | Index is undiscoverable by any skill-loading toolchain that depends on frontmatter |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/hosted-agents/scripts/sandbox_manager.py | Token embedded in git clone URL string at line 186 exposes credentials in logs/process lists | Use `git config url.https://github.com/.insteadOf` or pass credentials via `GIT_ASKPASS`/env variable rather than embedding in the URL; add a code comment warning this pattern should not be used in production |
| 2 | examples/llm-as-judge-skills/package.json | All production deps use `^` caret ranges | Pin to exact versions (remove `^`) or add a lockfile audit step (`npm audit`) to CI; at minimum pin major+minor (`~4.0.0`) |
| 3 | examples/digital-brain-skill/scripts/install.sh | User-provided custom path not sanitized before use in `mkdir -p` and `cp -r` | Validate the path: reject values containing `..`, null bytes, or shell metacharacters; use `realpath` to canonicalize before use |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | examples/digital-brain-skill/agents/AGENTS.md | Model not declared anywhere in agent doc | -5 |
| 2 | examples/digital-brain-skill/agents/AGENTS.md | Zero agent I/O examples (only script invocation examples, not agent interaction examples) | -15 |
| 3 | examples/digital-brain-skill/agents/AGENTS.md | No output format specification | -10 |
| 4 | examples/llm-as-judge-skills/agents/index.md | No output format for the index (what format does a consumer expect?) | -10 |
| 5 | template/SKILL.md | Placeholder `[describe input]` / `[show expected output]` in Examples section; not a concrete example | -5 |
| 6 | SKILL.md (root) | Collection index has no concrete I/O examples; "Practical Guidance" section describes approach but shows no before/after | -10 |
| 7 | examples/interleaved-thinking/SKILL.md | Platform-specific dependency on MiniMax M2.1 model without noting this is a specific third-party dependency; limits portability | -4 |
| 8 | examples/interleaved-thinking/generated_skills/comprehensive-research-agent/SKILL.md | Formatting bug: "Patterns to Avoid" bullet items start with `*Silent Tool Failure**` (missing leading `*`), breaking bold formatting | -2 |
| 9 | skills/hosted-agents/SKILL.md | No `## Examples` section with concrete input/output pairs; practical guidance is strong but examples are missing | -5 |
| 10 | skills/latent-briefing/SKILL.md | Examples section contains only one scenario (one scenario = one example); second concrete example would improve clarity | -5 |
| 11 | examples/interleaved-thinking/generated_skills/comprehensive-research-agent/SKILL.md | Missing `version` field in frontmatter (present in most other skills in the collection) | -2 |

## Cross-Component
**Orphaned agent reference**: `examples/llm-as-judge-skills/agents/orchestrator-agent/orchestrator-agent.md` (line 37) lists `writer` as an available agent (`- writer: Generates and refines content`) and `analyst` (`- analyst: Performs data analysis`), but no `writer-agent/` or `analyst-agent/` directories exist in `examples/llm-as-judge-skills/agents/`. These are referenced but unimplemented. The `agents/index.md` also omits them from "Available Agents." This is a documentation inconsistency that could mislead users attempting to orchestrate these non-existent agents.

**CLAUDE.md claim vs. reality**: `CLAUDE.md` states "5 complete demonstration projects" (digital-brain-skill, llm-as-judge-skills, book-sft-pipeline, x-to-book-system, interleaved-thinking). This matches the repo structure; no discrepancy.

**Skill count**: Root `SKILL.md` and `CLAUDE.md` both claim 14 skills. Counting the `skills/` directories: context-fundamentals, context-degradation, context-compression, context-optimization, multi-agent-patterns, memory-systems, tool-design, filesystem-context, hosted-agents, evaluation, advanced-evaluation, project-development, bdi-mental-states, latent-briefing = 14. Count matches.

**Internal links**: Root `SKILL.md` uses bracket links to skill files (e.g., `[context-fundamentals](skills/context-fundamentals/SKILL.md)`). These are relative paths that work from the repo root but may break in Claude Code's skill loading context if the plugin root differs. The `CLAUDE.md` explicitly advises "use plain text skill names (not links) in Integration sections" but the root `SKILL.md` itself uses links — inconsistent with the project's own authoring rules.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

**Priority order**:
1. Add YAML frontmatter (`name`, `description`) to all four files in `examples/llm-as-judge-skills/agents/` — this is the highest-impact fix since without it these agents are invisible to Claude Code's skill loader.
2. Remove the credential-in-URL pattern in `sandbox_manager.py` (Medium security); the file is pseudocode but teaches an unsafe pattern.
3. Pin dependencies in `llm-as-judge-skills/package.json` (Low security).
4. Sanitize the custom path input in `install.sh` (Low security).
5. Add writer-agent and analyst-agent stubs or remove the references in orchestrator instructions (cross-component cleanup).
6. Add concrete `## Examples` sections to `hosted-agents/SKILL.md` and a second example to `latent-briefing/SKILL.md`.
7. Fix the italic formatting bug in `comprehensive-research-agent/SKILL.md`.
