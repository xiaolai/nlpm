# NLPM Audit: softaworks/agent-toolkit
**Date**: 2026-04-29  |  **Artifacts**: 58 unique (6 agents, 9 commands, 43 skills)  |  **Strategy**: full-read
**NL Score**: 90/100
**Security**: PASS (2 Medium)
**Bugs**: 10  |  **Quality Issues**: 5  |  **Security Findings**: 2

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/explain-pr-changes.md | command | 45 | No YAML frontmatter at all — no `---` delimiters; name, description, and allowed-tools all absent; registration will silently fail |
| commands/viral-tweet.md | command | 60 | Missing name (−25); missing allowed-tools (−5); multi-step workflow uses thematic headers instead of numbered steps (−10) |
| agents/general-purpose.md | agent | 79 | Zero invocation examples (−15); three vague quantifiers "appropriate" with no measurable criteria (−6) |
| .claude/commands/add-skill.md | command | 70 | Missing name (−25); missing allowed-tools (−5) |
| .claude/commands/sync-skills-readme.md | command | 70 | Missing name (−25); missing allowed-tools (−5) |
| commands/explain-changes-mental-model.md | command | 70 | Missing name (−25); missing allowed-tools (−5) |
| commands/sync-branch.md | command | 70 | Missing name (−25); missing allowed-tools (−5) |
| commands/sync-skills-readme.md | command | 70 | Missing name (−25); missing allowed-tools (−5) |
| commands/codex-plan.md | command | 73 | Missing name (−25); non-canonical tool name "AskUser" (should be "AskUserQuestion") (−2) |
| commands/compose-email.md | command | 75 | Missing name (−25); has allowed-tools and numbered steps |
| agents/communication-excellence-coach.md | agent | 89 | One example group (−5); three vague quantifiers (−6) |
| agents/mermaid-diagram-specialist.md | agent | 89 | Missing model: field (−5); formatted as SKILL not agent; six vague quantifiers (−6) |
| agents/ui-ux-designer.md | agent | 91 | One example group (−5); two vague quantifiers "appropriate" (−4) |
| agents/codebase-pattern-finder.md | agent | 95 | One example group (−5) |
| skills/reducing-entropy/SKILL.md | skill | 85 | No Output Format section (−10); thin example count (−5) |
| skills/agent-md-refactor/SKILL.md | skill | 93 | Before/After example but no explicit "Output Format" heading (−7) |
| skills/database-schema-designer/SKILL.md | skill | 92 | Four vague quantifiers "appropriate" (−8) |
| skills/dependency-updater/SKILL.md | skill | 92 | Four vague quantifiers (−8) |
| skills/design-system-starter/SKILL.md | skill | 92 | Four vague quantifiers (−8) |
| skills/command-creator/SKILL.md | skill | 90 | Workflow present but output format only implied; references section relies on three external files (−10) |
| skills/gepetto/SKILL.md | skill | 90 | 17-step workflow; output format spread across references; minor vague language (−10) |
| skills/marp-slide/SKILL.md | skill | 90 | Output format references external asset files; thin standalone examples (−10) |
| skills/c4-architecture/SKILL.md | skill | 94 | Three vague quantifiers "appropriate" (−6) |
| skills/difficult-workplace-conversations/SKILL.md | skill | 94 | Three vague quantifiers (−6) |
| skills/professional-communication/SKILL.md | skill | 94 | Three vague quantifiers (−6) |
| skills/backend-to-frontend-handoff-docs/SKILL.md | skill | 96 | Clean; handoff template as output format |
| skills/codex/SKILL.md | skill | 96 | Clean; numbered workflow, model table, Quick Reference |
| skills/crafting-effective-readmes/SKILL.md | skill | 96 | Clean; references template files; concise |
| skills/gemini/SKILL.md | skill | 96 | Clean; numbered workflow, Quick Reference table |
| skills/jira/SKILL.md | skill | 96 | Clean; CLI+MCP dual backend; references |
| skills/lesson-learned/SKILL.md | skill | 96 | Clean; phase-based workflow; references |
| skills/skill-judge/SKILL.md | skill | 96 | Clean; 8-dimension 120-point rubric |
| skills/commit-work/SKILL.md | skill | 95 | Clean; 8-step checklist; Conventional Commits format |
| skills/datadog-cli/SKILL.md | skill | 95 | Clean; CLI examples; incident triage workflow |
| skills/domain-name-brainstormer/SKILL.md | skill | 95 | Clean; full example output |
| skills/feedback-mastery/SKILL.md | skill | 95 | Clean; SBI framework; references |
| skills/game-changing-features/SKILL.md | skill | 95 | Clean; 5-step workflow; output template |
| skills/mui/SKILL.md | skill | 95 | Clean; many TypeScript examples; references |
| skills/plugin-forge/SKILL.md | skill | 95 | Clean; 5-step workflow; JSON manifest examples |
| skills/react-useeffect/SKILL.md | skill | 95 | Clean; decision tree; references anti-patterns |
| skills/requirements-clarity/SKILL.md | skill | 95 | Clean; 100-point clarity scoring; PRD template |
| skills/session-handoff/SKILL.md | skill | 95 | Clean; CREATE/RESUME workflows; Python script references |
| skills/writing-clearly-and-concisely/SKILL.md | skill | 95 | Clean; Strunk rules; progressive disclosure |
| skills/daily-meeting-update/SKILL.md | skill | 97 | Clean; 3-phase workflow; claude_digest.py reference |
| skills/frontend-to-backend-requirements/SKILL.md | skill | 97 | Clean; Good/Bad examples; output format template |
| skills/meme-factory/SKILL.md | skill | 97 | Clean; URL examples; template selection guide; deep-dive sections |
| skills/openapi-to-typescript/SKILL.md | skill | 97 | Clean; complete OpenAPI→TypeScript example |
| skills/perplexity/SKILL.md | skill | 97 | Clean; TypeScript MCP call examples; tool selection chain |
| skills/qa-test-planner/SKILL.md | skill | 97 | Clean; test case and bug report examples; deep-dive sections |
| skills/ship-learn-next/SKILL.md | skill | 97 | Clean; Rep structure template; saving workflow |
| skills/web-to-markdown/SKILL.md | skill | 97 | Clean; explicit activation guard; numbered workflow |
| skills/draw-io/SKILL.md | skill | 98 | Clean; 9 numbered sections; checklist; XML examples |
| skills/excalidraw/SKILL.md | skill | 98 | Clean; 4 delegation examples; concise |
| skills/humanizer/SKILL.md | skill | 98 | Clean; 24 Before/After AI pattern examples |
| skills/mermaid-diagrams/SKILL.md | skill | 98 | Clean; Class/Sequence/Flowchart/ERD quick-start examples |
| skills/naming-analyzer/SKILL.md | skill | 98 | Clean; multilanguage examples; full report format template |
| skills/react-dev/SKILL.md | skill | 98 | Clean; extensive TypeScript examples; React 19 patterns |
| agents/ascii-ui-mockup-generator.md | agent | 98 | Clean; two in-description examples; 5-step process |

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 0 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts (sh) | 5 |
| Scripts (py) | 9 |
| MCP configs | 0 |
| Package manifests | 0 |

No `hooks/`, `.mcp.json`, `package.json`, or `requirements.txt` found. All scripts reside inside skill directories and are invoked by Claude on user request. Two build scripts (`scripts/build_plugins.py`, `scripts/bump_version.py`) use stdlib only — no subprocess, no shell=True, no network calls.

### Security Findings

| # | File | Pattern | Severity | Confidence | Notes |
|---|------|---------|----------|------------|-------|
| 1 | skills/qa-test-planner/scripts/generate_test_cases.sh:34 | eval-stdin-input | Medium | Medium | `eval "$var_name=\"$input\""` where `$input` is read from stdin — shell metacharacters in user input can trigger command execution. Script is interactive-only; risk is low in intended use but non-zero if invoked in automated pipelines. |
| 2 | skills/qa-test-planner/scripts/create_bug_report.sh:32 | eval-stdin-input | Medium | Medium | Same pattern as above in the bug-report generator. Both scripts should replace `eval` assignment with `printf -v` or `declare`. |

Medium-confidence findings: not PR-worthy under current policy (contribute step requires high confidence). Logged in sidecar for rule learning.

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/explain-pr-changes.md | **Zero YAML frontmatter** — file contains no `---` delimiters; `name:`, `description:`, and `allowed-tools:` are all absent. The file begins directly with a `#` heading. | Command cannot be registered by Claude Code; slash command will not appear; invoking it produces undefined behavior. |
| 2 | All 9 command files | **Missing `name:` field** — every command in this repository has a `description:` field but no `name:` field. Affected files: `.claude/commands/add-skill.md`, `.claude/commands/sync-skills-readme.md`, `commands/codex-plan.md`, `commands/compose-email.md`, `commands/explain-changes-mental-model.md`, `commands/explain-pr-changes.md`, `commands/sync-branch.md`, `commands/sync-skills-readme.md`, `commands/viral-tweet.md`. | Claude Code uses `name:` to register the command under a stable identifier. Without it the command may register under a derived name or fail silently. |
| 3 | agents/mermaid-diagram-specialist.md | **Missing `model:` field** — agent frontmatter declares `name`, `description`, `category`, `usage`, `input`, and `output` (SKILL-style fields) but omits `model:`. The file is structured as a skill, not an agent. | Agent will use an unspecified default model; unexpected behavior under model changes. The SKILL-style frontmatter fields will be ignored by the agent loader. |
| 4 | agents/general-purpose.md | **Zero invocation examples** — 54-line agent definition provides no `## Examples` or equivalent section; no worked invocation scenario exists. | Users cannot verify correct invocation; agent behaviour is entirely opaque from the definition. High-confidence finding — absence is machine-verifiable. |
| 5 | commands/viral-tweet.md | **Multi-step workflow without numbered steps** — the command body uses thematic section headers (`## Research`, `## Draft`, etc.) instead of a numbered sequence. | Agents following this command cannot detect step failures or resume from a partial state; the workflow is ambiguous. |
| 6 | commands/codex-plan.md | **Non-canonical tool name** — `allowed-tools` lists `AskUser`; the correct Claude Code tool name is `AskUserQuestion`. | The mis-named tool will not be granted permission; any step that calls `AskUserQuestion` will be blocked by the sandbox, silently failing user-input collection. |
| 7 | 7 command files | **Missing `allowed-tools:` field** — commands that invoke Bash, Read, Edit, or Task do not declare them. Affected: `.claude/commands/add-skill.md`, `.claude/commands/sync-skills-readme.md`, `commands/explain-changes-mental-model.md`, `commands/explain-pr-changes.md`, `commands/sync-branch.md`, `commands/sync-skills-readme.md`, `commands/viral-tweet.md`. | In restrictive permission modes Claude Code will not grant undeclared tools; commands will stall or silently skip tool calls. |

## Security Fixes (PR-worthy)

No security fixes warranted. The two Medium findings (`eval-stdin-input`) are in interactive scripts designed for human-driven terminal sessions; risk in their intended context is low. Recommend as internal refactors rather than external PRs.

## Quality Issues (informational)

| # | File(s) | Issue | Penalty |
|---|---------|-------|---------|
| 1 | skills/reducing-entropy/SKILL.md | **Missing output format** — skill describes a mindset-shift workflow but never specifies what the agent should produce (no template, no example output, no acceptance criteria). | −10 |
| 2 | agents/general-purpose.md; agents/mermaid-diagram-specialist.md; agents/communication-excellence-coach.md; agents/ui-ux-designer.md | **Vague quantifiers** — repeated use of "appropriate", "comprehensive", "effective" without measurable criteria. Worst offender: `general-purpose.md` (three occurrences, −6 pts). | −2 to −6 per file |
| 3 | agents/communication-excellence-coach.md; agents/mermaid-diagram-specialist.md; agents/ui-ux-designer.md | **Thin example count** — each file contains exactly one example group (−5 each). Multiple distinct worked examples help agents handle variations in user phrasing. | −5 per file |
| 4 | skills/agent-md-refactor/SKILL.md; skills/command-creator/SKILL.md; skills/gepetto/SKILL.md; skills/marp-slide/SKILL.md | **Implicit or delegated output format** — output format exists but is spread across referenced external files rather than summarised in SKILL.md. Increases cognitive load; agents must load references to know what "done" looks like. | −7 to −10 per file |
| 5 | commands/viral-tweet.md | **Structural inconsistency** — the only command that does not follow numbered steps. All other commands in the repo use clear step sequences; `viral-tweet.md` breaks the pattern with thematic headers. | −10 |

## Cross-Component

The repository shows a clear architectural split between high-quality skills (avg 95.1) and systematically weak commands (avg 67.0). Skills follow the progressive-disclosure pattern correctly — SKILL.md as entry point with `references/` for deep content — and are generally well-structured. Agents are intermediate (avg 90.2) with two outliers (`general-purpose.md` at 79, `mermaid-diagram-specialist.md` at 89).

The command weakness is systemic and has a single root cause: **all 9 commands are missing the `name:` field**, which accounts for the majority of the score penalty in that category. The fix is mechanical (add `name:` to each frontmatter block). Once applied, the weighted overall score would rise from 90 to approximately 93.

No broken relative path references found. The `dist/plugins/` tree contains exact copies of the source skills, agents, and commands — confirmed consistent across sampled files.

The `agents/mermaid-diagram-specialist.md` overlaps in scope with `skills/mermaid-diagrams/SKILL.md`; the agent is formatted as a skill and the skill is the more complete resource. Consider removing the agent or converting it to a proper agent definition with a distinct workflow focus.

## Recommendation

**CONTRIBUTE** — open PRs for confirmed bugs. Score above threshold (90 > 70); security gate clear.

**Immediate PR targets (high confidence, mechanical fixes):**
1. Add `name:` frontmatter to all 9 commands — one-line fix per file; zero ambiguity.
2. Add `---` frontmatter block to `commands/explain-pr-changes.md` with `name:`, `description:`, and `allowed-tools:`.
3. Fix `commands/codex-plan.md` — rename `AskUser` → `AskUserQuestion` in `allowed-tools:`.
4. Add `model:` field to `agents/mermaid-diagram-specialist.md` (e.g., `model: claude-sonnet-4-6`).

**Follow-up quality PRs (moderate effort):**
5. Add `allowed-tools:` to the 7 commands that omit it.
6. Convert `commands/viral-tweet.md` to numbered steps.
7. Add at least two invocation examples to `agents/general-purpose.md`.
8. Add an Output Format section to `skills/reducing-entropy/SKILL.md`.
