---
slug: leowux-pony
repo: leowux/pony
audited: 2026-05-13
commit_sha: 50d7ec3f4fee26fe7a7f75ee10443cd5baa28428
score: 91
exemplifies:
  - R10
  - R11
  - R12
  - R13
  - R33
  - R34
  - R35
  - R47
---

# Exemplar: leowux/pony

**Score**: 91/100  |  **Date**: 2026-05-13  |  **Commit**: `50d7ec3f4fee26fe7a7f75ee10443cd5baa28428`

Four-agent task-management Claude Code plugin (planner/explorer/executor/verifier) demonstrating textbook model-tier selection, tool least-privilege, concrete output schemas, and a 100/100 CLAUDE.md.

## Per-rule evidence

### R10 — Model must match task complexity

Four agents, two tiers: `explorer` is assigned `claude-haiku-4-5` for mechanical search; `planner`, `executor`, and `verifier` each use `claude-sonnet-4-6` for reasoning work. The split is explicit in frontmatter, not left to defaults.

> `agents/explorer.md:1-6`:
>
> ```
> ---
> name: explorer
> description: Codebase search specialist for finding files and code patterns
> model: claude-haiku-4-5
> disallowedTools: Write, Edit
> ---
> ```

> `agents/planner.md:1-5`:
>
> ```
> ---
> name: planner
> description: Strategic planning agent for task decomposition and work plan creation
> model: claude-sonnet-4-6
> ---
> ```

What lifts this above mere compliance: the body's `<Why_This_Matters>` in explorer.md reads "Search agents that return incomplete results force the caller to re-search, wasting time and tokens" — the haiku choice is motivated by throughput and cost, which is exactly the trade-off R10 is about.

### R11 — Tools follow least-privilege

Explorer is read-only by design. `disallowedTools` in the frontmatter makes the restriction machine-enforceable; the matching Constraints block reinforces it in the body so the rule survives if someone edits the frontmatter.

> `agents/explorer.md:5-6` (frontmatter):
>
> ```
> disallowedTools: Write, Edit
> ```

> `agents/explorer.md:28-31` (Constraints):
>
> ```
> - Read-only: you cannot create, modify, or delete files.
> - Never use relative paths.
> - Never store results in files; return them as message text.
> - Focus on the codebase, not external documentation.
> ```

Double enforcement — declaration in frontmatter AND explicit constraint in the body — means the restriction holds even if a future editor paraphrases away the Constraints block.

### R12 — Output format defined in body

Every agent specifies a response template. Verifier's schema is the most concrete: three tables with fixed enum values covering verdict, evidence, and acceptance criteria status.

> `agents/verifier.md:49-74`:
>
> ```
> <Output_Format>
>   ## Verification Report
>
>   ### Verdict
>   **Status**: PASS | FAIL | INCOMPLETE
>   **Confidence**: high | medium | low
>   **Blockers**: [count — 0 means PASS]
>
>   ### Evidence
>   | Check | Result | Command | Output |
>   |-------|--------|---------|--------|
>   | Tests | pass/fail | `pnpm test` | X passed, Y failed |
>   | Types | pass/fail | `pnpm typecheck` | N errors |
>   | Format | pass/fail | `pnpm fmt --check` | exit code |
>   | Lint | pass/fail | `pnpm lint` | N issues |
>   | Build | pass/fail | `pnpm build` | exit code |
>
>   ### Acceptance Criteria
>   | # | Criterion | Status | Evidence |
>   |---|-----------|--------|----------|
>   | 1 | [criterion text] | VERIFIED / PARTIAL / MISSING | [specific evidence] |
>
>   ### Recommendation
>   APPROVE | REQUEST_CHANGES | NEEDS_MORE_EVIDENCE
>   [One sentence justification]
> </Output_Format>
> ```

The `PASS | FAIL | INCOMPLETE` and `VERIFIED / PARTIAL / MISSING` enums eliminate free-form hedging. Claude cannot output "looks mostly done" as a verdict because the schema's enum list doesn't include it.

### R13 — System prompt structure: mission → steps → boundaries → format

Planner follows all four layers with named XML tags: `<Role>` (mission), `<Investigation_Protocol>` (numbered steps), `<Constraints>` (what not to do), `<Output_Format>` (response template). The XML sectioning makes the structure readable without requiring the reader to infer where one layer ends and the next begins.

> `agents/planner.md:7-14` (`<Role>` — mission):
>
> ```
> <Role>
>   You are Planner. Your mission is to create clear, actionable work plans through structured analysis.
>   You are responsible for decomposing complex tasks into manageable steps, identifying dependencies, and producing work plans.
>   You are not responsible for implementing code (executor), analyzing requirements gaps, or reviewing code.
>
>   When a user says "do X" or "build X", interpret it as "create a work plan for X." You never implement. You plan.
> </Role>
> ```

> `agents/planner.md:36-44` (`<Investigation_Protocol>` — numbered steps):
>
> ```
> <Investigation_Protocol>
>   1) Classify intent: Trivial (quick fix) | Refactoring | Build from Scratch | Mid-sized.
>   2) Explore codebase to understand context before planning.
>   3) Ask user ONLY about: priorities, timelines, scope decisions, risk tolerance.
>   4) Generate plan with: Context, Work Objectives, Guardrails, Task Flow, Detailed TODOs.
>   5) Display confirmation summary and wait for explicit user approval.
>   6) On approval, hand off to executor.
> </Investigation_Protocol>
> ```

The `<Role>` block names three explicit not-responsibilities alongside the three it owns. That scoping prevents the planner from drifting into implementation while planning — a common failure mode in orchestration agents.

### R33, R34, R35 — CLAUDE.md: build command, test command, architecture overview

CLAUDE.md scored 100/100. It opens with every development command in a single annotated fenced block (R33, R34), then delivers a three-level architecture breakdown: Core Modules → named source files with one-line purpose descriptions → Data Storage layout with an ASCII directory tree (R35).

> `CLAUDE.md:9-23`:
>
> ```
> ## Commands
>
> ```bash
> pnpm build      # Build library/CLI (vp pack - tsdown)
> pnpm dev        # Watch mode build
> pnpm test       # Run tests (Vitest)
> pnpm test run   # Run tests once (no watch)
> pnpm lint       # Lint code (Oxlint)
> pnpm fmt        # Format code (Oxfmt)
> pnpm check      # Combined format + lint + typecheck
> pnpm typecheck  # TypeScript type checking
> pnpm clean      # Remove dist/
> ```
>
> Run CLI locally: `node dist/cli/index.mjs <command>`
> ```

> `CLAUDE.md:25-53` (Architecture, excerpt):
>
> ```
> ## Architecture
>
> ### Core Modules
>
> - **`src/tasks/`** - Task management layer
>   - `task-file-ops.ts` - Low-level CRUD operations on JSON files
>   - `task-manager.ts` - High-level business logic with validation, status transitions, dependency checks
>
> - **`src/hud/`** - HUD rendering for Claude Code statusline
>
> ### Data Storage
>
> .pony/
> ├── tasks/
> │   ├── index.json    # nextId counter
> │   └── 1.json        # task files
> └── state/
>     └── hud-state.json
> ```

Each command annotation names the underlying tool (`# Format code (Oxfmt)`, `# Build library/CLI (vp pack - tsdown)`). The toolchain is non-standard — Oxfmt instead of Prettier, tsdown instead of tsc — so without the annotations, Claude would guess wrong.

### R47 — Max retry count on loops

Executor specifies an explicit escalation threshold — 3 failed attempts — rather than allowing an unbounded retry loop.

> `agents/executor.md:37-38`:
>
> ```
> - After 3 failed attempts on the same issue, escalate to planner with full context.
> ```

The companion `<Why_This_Matters>` at executor.md:17-20 explains: "Executors that over-engineer, broaden scope, or skip verification create more work than they save. The most common failure mode is doing too much, not too little." An agent without a retry cap responds to repeated failures by expanding scope — which is exactly the failure mode the 3-attempt escalation cap prevents.

## Worth adopting

Pattern: **`<Why_This_Matters>` rationale block in agent bodies.** Evidence: `agents/planner.md:16-19`, `agents/executor.md:17-20`, `agents/explorer.md:15-18`, `agents/verifier.md:14-16`. Every agent opens with a one-paragraph explanation of why its constraints exist — not just what the constraints are. Why it would be a useful rule: editors who encounter a constraint without a rationale remove it when it feels like unnecessary friction; the `<Why_This_Matters>` block preserves the incident history that motivated the constraint, making the rule much harder to accidentally regress away.

Pattern: **`<Final_Checklist>` pre-flight block at end of agent bodies.** Evidence: `agents/planner.md:71-75`, `agents/executor.md:91-97`, `agents/verifier.md:77-83`. Each agent ends with 4-6 yes/no self-verification questions phrased to match its success criteria. Why it would be a useful rule: a checklist forces the agent to revisit success criteria after task execution, catching omissions (e.g., "Did I run `pnpm test`?") that would otherwise only surface as bugs in the downstream stage.
