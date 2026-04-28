# Audit: jnuyens/gsd-plugin

**Repo:** https://github.com/jnuyens/gsd-plugin  
**Audited at:** 2026-04-28  
**Auditor:** NLPM automated audit pipeline  
**Plugin version:** 2.38.8  
**Artifacts scored:** 115 (33 agents + 82 skills)  
**Threshold:** 70 (configurable)

---

## NL Score Summary

### Agents (33 files)

| File | Score | Key Deductions |
|------|-------|----------------|
| agents/gsd-advisor-researcher.md | 76 | no model (−5), zero examples (−15), vague: "focused" "genuine" (−4) |
| agents/gsd-ai-researcher.md | 86 | no model (−5), one example (−5), vague: "brief" "relevant" (−4) |
| agents/gsd-assumptions-analyzer.md | 78 | no model (−5), zero examples (−15), vague: "relevant" (−2) |
| agents/gsd-code-fixer.md | 86 | no model (−5), one example (−5), vague: "intelligently" "clean" (−4) |
| agents/gsd-code-reviewer.md | 86 | no model (−5), one example (−5), vague: "relevant" "appropriate" (−4) |
| agents/gsd-codebase-mapper.md | 91 | no model (−5), template examples ✓, vague: "key" "relevant" (−4) |
| agents/gsd-debug-session-manager.md | 93 | no model (−5), dispatch table ✓, vague: "compact" (−2) |
| agents/gsd-debugger.md | 93 | no model (−5), many examples ✓, vague: "relevant" (−2) |
| agents/gsd-doc-classifier.md | 90 | no model (−5), one example (−5) |
| agents/gsd-doc-synthesizer.md | 93 | no model (−5), multiple examples ✓, vague: "transparent" (−2) |
| agents/gsd-doc-verifier.md | 90 | no model (−5), one example (−5) |
| agents/gsd-doc-writer.md | 91 | no model (−5), template examples ✓, vague: "accurate" "appropriate" (−4) |
| agents/gsd-domain-researcher.md | 88 | no model (−5), one example (−5), vague: "targeted" (−2) |
| agents/gsd-eval-auditor.md | 80 | no model (−5), zero examples (−15) |
| agents/gsd-eval-planner.md | 88 | no model (−5), one example (−5), vague: "appropriate" (−2) |
| agents/gsd-executor.md | 93 | no model (−5), many examples ✓, vague: "relevant" (−2) |
| agents/gsd-framework-selector.md | 90 | no model (−5), one example (−5) |
| agents/gsd-integration-checker.md | 86 | no model (−5), one example (−5), vague: "properly" "relevant" (−4) |
| agents/gsd-intel-updater.md | 86 | no model (−5), one example (−5), vague: "key files" "important" (−4) |
| agents/gsd-nyquist-auditor.md | 95 | no model (−5) |
| agents/gsd-pattern-mapper.md | 86 | no model (−5), one example (−5), vague: "closest" "relevant" (−4) |
| agents/gsd-phase-researcher.md | 88 | no model (−5), one example (−5), vague: "relevant" (−2) |
| agents/gsd-plan-checker.md | 89 | no model (−5), one example (−5), vague: "appropriate" "reasonable" "minor" (−6) |
| agents/gsd-planner.md | 89 | no model (−5), multiple examples ✓, vague: "relevant" "appropriate" "reasonable" (−6) |
| agents/gsd-project-researcher.md | 93 | no model (−5), format examples ✓, vague: "appropriate" (−2) |
| agents/gsd-research-synthesizer.md | 86 | no model (−5), one example (−5), vague: "key points" "brief" (−4) |
| agents/gsd-roadmapper.md | 95 | no model (−5) |
| agents/gsd-security-auditor.md | 95 | no model (−5) |
| agents/gsd-ui-auditor.md | 86 | no model (−5), one example (−5), vague: "relevant" "appropriate" (−4) |
| agents/gsd-ui-checker.md | 93 | no model (−5), multiple examples ✓, vague: "brief note" (−2) |
| agents/gsd-ui-researcher.md | 88 | no model (−5), one example (−5), vague: "sensible" (−2) |
| agents/gsd-user-profiler.md | 88 | no model (−5), one example (−5), vague: "representative" (−2) |
| agents/gsd-verifier.md | 91 | no model (−5), many examples ✓, vague: "relevant" "appropriate" (−4) |

**Agent average: 88.7 / 100**  
**Below threshold (<70): 0**  
**Universal finding: 0 / 33 agents declare a `model` field**

---

### Skills (82 files)

| File | Score | Notes |
|------|-------|-------|
| skills/add-backlog/SKILL.md | 100 | Full process, output template, code examples |
| skills/add-phase/SKILL.md | 85 | One example, no output format |
| skills/add-tests/SKILL.md | 100 | Input examples, output described |
| skills/add-todo/SKILL.md | 85 | One example (numbered list), no output format |
| skills/ai-integration-phase/SKILL.md | 85 | One example (flow description), no output format |
| skills/analyze-dependencies/SKILL.md | 85 | Zero examples |
| skills/audit-fix/SKILL.md | 95 | Flags documented, one example (dry-run) |
| skills/audit-milestone/SKILL.md | 85 | Zero examples |
| skills/audit-uat/SKILL.md | 75 | Zero examples, no process section |
| skills/autonomous/SKILL.md | 95 | Flags documented, one example |
| skills/check-todos/SKILL.md | 85 | One example, no output format |
| skills/cleanup/SKILL.md | 75 | Zero examples, thin |
| skills/code-review-fix/SKILL.md | 95 | Output described, flags documented |
| skills/code-review/SKILL.md | 95 | Output described, flags documented |
| skills/complete-milestone/SKILL.md | 100 | 8 steps, multiple examples, output format |
| skills/debug/SKILL.md | 100 | Multiple subcommands, format examples, security notes |
| skills/discuss-phase/SKILL.md | 93 | Flags documented, output described; vague: "intelligent" (−2); one example (−5) |
| skills/do/SKILL.md | 75 | Zero examples, no output format |
| skills/docs-update/SKILL.md | 85 | Flags documented, zero standalone examples |
| skills/eval-review/SKILL.md | 75 | Zero examples, no output format |
| skills/execute-phase/SKILL.md | 95 | Flags documented, output format section |
| skills/explore/SKILL.md | 85 | One example (usage), no output format |
| skills/extract_learnings/SKILL.md | 75 | Zero examples, no output format |
| skills/fast/SKILL.md | 75 | Zero examples, no output format |
| skills/forensics/SKILL.md | 85 | Success criteria, zero concrete examples |
| skills/from-gsd2/SKILL.md | 100 | 4 steps, code examples, notes |
| skills/graphify/SKILL.md | 100 | Multiple subcommands, detailed steps, code examples |
| skills/health/SKILL.md | 75 | Zero examples, no output format |
| skills/help/SKILL.md | 85 | Zero examples |
| skills/import/SKILL.md | 75 | Zero examples, no output format |
| skills/inbox/SKILL.md | 95 | Flow described, flags documented, one example |
| skills/ingest-docs/SKILL.md | 95 | Two modes described, precedence rules |
| skills/insert-phase/SKILL.md | 75 | Zero examples, no output format |
| skills/intel/SKILL.md | 100 | Multiple subcommands, code examples, anti-patterns |
| skills/join-discord/SKILL.md | 100 | Clear output with actual invite link |
| skills/list-phase-assumptions/SKILL.md | 95 | 4 steps, output described, success criteria |
| skills/list-workspaces/SKILL.md | 85 | Zero examples |
| skills/manager/SKILL.md | 95 | Creates/Updates section, one example |
| skills/map-codebase/SKILL.md | 95 | 7 steps, success criteria, output described |
| skills/milestone-summary/SKILL.md | 95 | Success criteria, output described |
| skills/new-milestone/SKILL.md | 95 | Creates/Updates section, flow described |
| skills/new-project/SKILL.md | 95 | Creates section, flag documented |
| skills/new-workspace/SKILL.md | 95 | Flags documented, use cases, creates section |
| skills/next/SKILL.md | 90 | Behavior well-described, no output format |
| skills/note/SKILL.md | 95 | Three subcommands, constraints stated |
| skills/pause-work/SKILL.md | 95 | Output described, numbered list |
| skills/plan-milestone-gaps/SKILL.md | 90 | One example, output partially described |
| skills/plan-phase/SKILL.md | 95 | Flags documented, output format section |
| skills/plant-seed/SKILL.md | 85 | Output paths stated, zero standalone examples |
| skills/pr-branch/SKILL.md | 85 | Good objective, zero examples |
| skills/profile-user/SKILL.md | 95 | 10-step process, flags documented |
| skills/progress/SKILL.md | 85 | Zero examples |
| skills/quick/SKILL.md | 100 | Multiple subcommands, format examples, security notes |
| skills/reapply-patches/SKILL.md | 100 | 7 steps, three-way merge logic, Hunk Verification Table |
| skills/remove-phase/SKILL.md | 85 | Output described, zero examples |
| skills/remove-workspace/SKILL.md | 85 | Zero examples |
| skills/research-phase/SKILL.md | 100 | 6 steps, agent spawn template, success criteria |
| skills/resume-at/SKILL.md | 100 | 5 steps, output_format, rules, notes |
| skills/resume-work/SKILL.md | 95 | 6 steps, rules, one example |
| skills/review-backlog/SKILL.md | 100 | 7 steps, code examples, report format |
| skills/review/SKILL.md | 95 | Flow described, flags documented |
| skills/scan/SKILL.md | 85 | Zero examples |
| skills/secure-phase/SKILL.md | 90 | Three states documented, output described |
| skills/session-report/SKILL.md | 85 | Zero examples |
| skills/set-profile/SKILL.md | 90 | Has `model: haiku` (only skill with model), thin process |
| skills/settings/SKILL.md | 95 | 6-step process, flags described |
| skills/ship/SKILL.md | 95 | Output format section, flow described |
| skills/sketch-wrap-up/SKILL.md | 95 | Output paths described, one example |
| skills/sketch/SKILL.md | 95 | Two modes, flags documented |
| skills/spec-phase/SKILL.md | 95 | 6-step how-it-works, flags, success criteria |
| skills/spike-wrap-up/SKILL.md | 95 | Output paths described |
| skills/spike/SKILL.md | 95 | Two modes, flags documented |
| skills/stats/SKILL.md | 85 | Zero examples |
| skills/thread/SKILL.md | 100 | Five modes, code examples, security notes |
| skills/ui-phase/SKILL.md | 95 | Flow described, output described |
| skills/ui-review/SKILL.md | 95 | Output described |
| skills/ultraplan-phase/SKILL.md | 85 | Beta flag, zero examples |
| skills/undo/SKILL.md | 95 | Three modes described |
| skills/update/SKILL.md | 95 | 8-step process, numbered list |
| skills/validate-phase/SKILL.md | 95 | Three states, output described |
| skills/verify-work/SKILL.md | 95 | Output described, output format section |
| skills/workstreams/SKILL.md | 100 | Subcommand table, code examples |

**Skill average: 90.9 / 100**  
**Below threshold (<70): 0**

---

### Overall

| Metric | Value |
|--------|-------|
| Total artifacts | 115 |
| Overall average | 90.3 |
| Below threshold (70) | 0 |
| Agents average | 88.7 |
| Skills average | 90.9 |
| Highest score | 100 (multiple agents/skills) |
| Lowest score | 75 (9 thin-delegation skills) |
| Artifacts below 80 | 12 (3 agents + 9 skills) |

---

## Security Scan

**Pre-scan summary:** 1 hook file (hooks.json), 0 standalone scripts, 1 MCP config, 1 package.json, 0 requirements.txt  
**Verdict: CLEAR — no CRITICAL or HIGH patterns**

### hooks/hooks.json

Four hook event handlers — SessionStart, PreToolUse (Edit|Write), PostToolUse (Bash|Edit|Write|MultiEdit|NotebookEdit|Read|Grep|Glob|WebFetch|WebSearch), PreCompact — each running an identical inline Node.js one-liner.

**Pattern analysis of the hook command:**

The inline Node.js code performs version-aware fallback resolution for `gsd-tools.cjs`:
1. Checks `$CLAUDE_PLUGIN_ROOT/bin/gsd-tools.cjs` (canonical plugin install)
2. Falls back to scanning `~/.claude/plugins/cache/gsd-plugin/gsd/` for the highest semver version
3. Calls `require(resolved_path)` to load the CJS module

**Findings:**

| Severity | Pattern | Location | Notes |
|----------|---------|----------|-------|
| MEDIUM | PostToolUse fires on Read/Grep/Glob | hooks.json:PostToolUse | Matcher includes read-only tools; the hook executes on every file read and every grep, adding 3s timeout overhead to each. This can noticeably slow Claude's performance during heavy file-scanning phases. |
| LOW | Inline minified JS in hook commands | hooks.json (all hooks) | The Node.js one-liner is 700+ chars of compact code. Functionally correct and the intent is clear on expansion, but reduces auditability. A reference to an external script file would be more reviewable. |
| LOW | Dynamic `require()` with runtime path resolution | hooks.json (all hooks) | Loads CJS module from a semver-sorted version directory in the plugin cache. The path is bounded to `~/.claude/plugins/cache/gsd-plugin/gsd/`, not arbitrary user input. Low actual risk, but any compromise of the plugin cache would gain hook execution. |
| INFO | PreToolUse (Edit|Write) hook blocks file writes | hooks.json:PreToolUse | Edit/Write calls block until the 3000ms hook completes or times out. Intended for workflow enforcement gate. |

### package.json

- No `postinstall` or lifecycle scripts ✓
- devDependencies: `ajv@^8.18.0`, `ajv-formats@^3.0.1` (schema validation only) ✓
- No network fetch scripts ✓

### .mcp.json

- `{"mcpServers": {}}` — empty config, no MCP servers configured ✓

---

## Bugs

No BUGS found. All 115 artifacts pass frontmatter registration requirements:
- All have `name` and `description` fields ✓
- No tools used in agent bodies that are not in their `tools:` frontmatter declarations (based on reviewed content) ✓
- `@${CLAUDE_PLUGIN_ROOT}` cross-references in agent/skill bodies are a valid plugin runtime pattern, not broken references ✓

---

## Security Fixes

**Priority 1 (MEDIUM) — Narrow the PostToolUse hook matcher**

`hooks.json` PostToolUse fires on `Bash|Edit|Write|MultiEdit|NotebookEdit|Read|Grep|Glob|WebFetch|WebSearch`. The read-only tools (Read, Grep, Glob) do not modify state, so firing the GSD state-tracking hook on every read call adds latency without benefit.

**Suggested fix:** Narrow the PostToolUse matcher to state-changing tools only:
```json
"matcher": "Bash|Edit|Write|MultiEdit|NotebookEdit"
```
This eliminates hook overhead on the majority of Claude's tool calls during file-scanning intensive operations (plan creation, code review, research).

**Priority 2 (LOW) — Move inline hook JS to an external script**

Replace the inline 700-char Node.js one-liner in all four hooks with a call to an external script:
```json
"command": "node $CLAUDE_PLUGIN_ROOT/bin/hook-runner.cjs <event>"
```
This makes the hook code reviewable in a single place and reduces hooks.json to a clean configuration file.

---

## Quality Issues

### Q-01: No model tier declared (affects all 33 agents)

**Impact:** −5 per agent × 33 = 165 penalty points across the agent corpus  
**Pattern:** No `model:` field in any agent frontmatter  
**Severity:** LOW per instance; HIGH aggregate impact on cost predictability

Every agent in the plugin uses the default model (currently Sonnet 4.6 via the skill orchestrator). Agents vary significantly in complexity — `gsd-debugger` (1453 lines, iterative scientific method) should run on Opus; `gsd-doc-classifier` (90 lines, enum classification) is ideal for Haiku.

**Affected files:** All 33 agent `.md` files  
**Suggested fix:** Add `model: opus|sonnet|haiku` to each agent's frontmatter based on task complexity. Example: `gsd-doc-classifier` → `model: haiku`, `gsd-debugger` → `model: sonnet`, `gsd-planner` → `model: sonnet`.

The only exception: `skills/set-profile/SKILL.md` does declare `model: haiku` — demonstrating the pattern works.

---

### Q-02: Zero example blocks in three agents

**Impact:** −15 per agent  
**Pattern:** No concrete input/output examples anywhere in the agent body

| Agent | Score impact | Context |
|-------|-------------|---------|
| agents/gsd-advisor-researcher.md | −15 | Returns 5-column comparison table but no table example shown |
| agents/gsd-assumptions-analyzer.md | −15 | Three calibration tiers described but no sample output |
| agents/gsd-eval-auditor.md | −15 | Scores eval dimensions but no graded example |

**Suggested fix:** Add at least one concrete `<structured_returns>` or example block showing what the agent produces. For `gsd-advisor-researcher`, a sample row of the comparison table would suffice.

---

### Q-03: Vague quantifiers degrade instruction precision (20+ agents)

**Impact:** −2 per occurrence, cap −20  
**Pattern:** Words like "appropriate", "relevant", "intelligent", "reasonable", "properly", "key" used as qualifiers without measurable criteria

Common offenders:
- "appropriate" — in gsd-plan-checker (−2), gsd-code-reviewer (−2), gsd-doc-writer (−2), gsd-ui-researcher (−2)
- "relevant" — in gsd-integration-checker (−2), gsd-ai-researcher (−2), gsd-debugger (−2)
- "intelligently" — in gsd-code-fixer (−2)
- "properly" — in gsd-integration-checker (−2)

**Suggested fix:** Replace vague qualifiers with measurable criteria. Instead of "apply appropriate error handling", write "add error handling for network failures, null inputs, and 4xx/5xx status codes".

---

### Q-04: Nine thin-delegation skills score 75/100

**Impact:** −15 (zero examples) + −10 (no output format) per skill  
**Pattern:** Skills that consist only of an objective + `@workflow` reference, with no concrete process steps, examples, or output description

| Skill | Missing |
|-------|---------|
| skills/audit-uat/SKILL.md | Examples, process steps |
| skills/cleanup/SKILL.md | Examples, output format |
| skills/do/SKILL.md | Examples, output format |
| skills/eval-review/SKILL.md | Examples, output format |
| skills/extract_learnings/SKILL.md | Examples, output format |
| skills/fast/SKILL.md | Examples, output format |
| skills/health/SKILL.md | Examples, output format |
| skills/import/SKILL.md | Examples, output format |
| skills/insert-phase/SKILL.md | Examples, output format |

**Suggested fix:** For each skill, add: (1) an `<output_format>` section naming the artifact produced (file path, format), and (2) a brief usage example showing a concrete invocation. Thin delegation is acceptable — the example does not need to replicate the workflow's full logic.

---

### Q-05: gsd-advisor-researcher scores lowest overall (76/100)

This agent combines three separate quality deductions:
- No model (−5)
- Zero examples (−15)
- Vague: "focused" "genuine" (−4)

The agent returns a 5-column comparison table but provides no sample row, no output format spec, and no model guidance. It is also the only agent with "genuine" as a qualifier ("avoid generic advice, provide genuine recommendations") — a word that cannot be operationalized.

**Priority fix:** Add a sample comparison table row to the body, specify `model: sonnet`, replace "genuine recommendations" with a concrete constraint (e.g., "for each option, state one concrete tradeoff the developer will encounter").

---

### Q-06: gsd-planner uses vague quantifiers at cap (−6)

At 1249 lines, `gsd-planner.md` is the largest agent in the plugin. It loses 6 points to vague quantifiers: "relevant context" (×2), "appropriate tests", "reasonable default". Despite this, it scores 89 — its extensive structured returns and multi-example body offset the deductions. The vague words are addressable without touching the overall structure.

---

## Cross-Component

### Plugin-wide @${CLAUDE_PLUGIN_ROOT} dependency

Every agent body and most skill `<execution_context>` blocks use `@${CLAUDE_PLUGIN_ROOT}/...` to cross-reference workflows, templates, and references. This is a valid plugin design pattern — the host (Claude Code) resolves the variable at invocation time.

**Implication for auditing:** These references are resolvable only when the plugin is installed via `claude plugin install`. A raw `git clone` will show unresolved template variables in all cross-references. This is expected and by design; it is not a bug.

**Cross-file consistency:** Reference targets (workflows/, templates/, references/) are not included in this audit scope (only agents/ and skills/ were scored). If any referenced workflow file is missing, the agent/skill will silently receive no supplementary context.

### Parallel research agent pattern (gsd-project-researcher → 6 files)

`gsd-project-researcher` spawns up to 6 parallel subagents (SUMMARY, STACK, FEATURES, ARCHITECTURE, PITFALLS, COMPARISON, FEASIBILITY). The output files are then consumed by `gsd-research-synthesizer`. No explicit type contracts exist between producer and consumer — `gsd-research-synthesizer` reads section headers by name. If the researcher omits a section, the synthesizer degrades silently. Consider adding mandatory section headers with explicit fallback behavior.

### Debug session continuity chain

The debug flow chains: `gsd:debug` skill → `gsd-debug-session-manager` agent → `gsd-debugger` agent. The `gsd-debug-session-manager` reads `.planning/debug/{slug}.md` state files that `gsd:debug` creates. The state file schema is documented inline in `gsd:debug/SKILL.md` but not in a shared reference. If either agent version drifts from the schema, the continuation loop will break. A shared state schema reference would improve robustness.

---

## Recommendation

**Verdict: APPROVE with quality improvements**

The gsd-plugin scores **90.3 / 100** overall — well above the 70-point threshold. No artifacts are below threshold. The plugin demonstrates high structural quality: agents have clear role definitions, rich process documentation, detailed structured returns, and security-aware patterns (input sanitization in `quick`, `thread`, security boundaries in `debug`).

The dominant quality gap is **universal: 0 / 33 agents declare a model tier**. This is the single highest-leverage fix — adding `model:` fields costs one line per file and would recover 165 penalty points across the corpus, raising the agent average from 88.7 to ~94. This also enables cost-sensitive deployments to use Haiku for lightweight classifiers and Opus for complex planners.

Secondary priority: **9 thin-delegation skills** (audit-uat, cleanup, do, eval-review, extract_learnings, fast, health, import, insert-phase) each score 75. Adding one-line output descriptions and minimal usage examples to each would bring them to ~90.

Security posture is clean. The single actionable fix is narrowing the PostToolUse hook matcher to exclude read-only tools (Read, Grep, Glob), which would eliminate unnecessary hook overhead during file-intensive operations.

**Priority fix list:**
1. Add `model:` to all 33 agents (haiku for classifiers, sonnet for planners, opus for debugger)
2. Add output format + one usage example to the 9 lowest-scoring skills
3. Add example blocks to gsd-advisor-researcher, gsd-assumptions-analyzer, gsd-eval-auditor
4. Narrow PostToolUse hook matcher to exclude Read/Grep/Glob
5. Replace vague qualifiers in gsd-advisor-researcher, gsd-plan-checker, gsd-planner
