---
slug: alizarion-openclaw-claude-code-plugin
repo: alizarion/openclaw-claude-code-plugin
audited: 2026-06-27
commit_sha: 7a524f6309b7213cc106b8ec7ff308af9287ada4
score: 92
exemplifies:
  - R04
  - R05
  - R06
  - R07
  - R08
---

# Exemplar: alizarion/openclaw-claude-code-plugin

**Score**: 92/100  |  **Date**: 2026-06-27  |  **Commit**: `7a524f6309b7213cc106b8ec7ff308af9287ada4`

A single-skill plugin for orchestrating multiple Claude Code sessions from inside OpenClaw; notable for dense runnable examples across three cost tiers, a nine-row anti-patterns table with mechanism-level consequences, and a decision tree that collapses agent judgment into two exhaustive lists.

## Per-rule evidence

### R04 — Description as trigger

The description enumerates six distinct operational topics rather than restating the skill title:

> From `skills/claude-code-orchestration/SKILL.md:3`:
>
> ```
> description: Skill for orchestrating Claude Code sessions from OpenClaw. Covers launching,
> monitoring, multi-turn interaction, lifecycle management, notifications, and parallel work patterns.
> ```

Each of the six topics ("launching," "monitoring," "multi-turn interaction," "lifecycle management," "notifications," "parallel work patterns") is a plausible user query phrase. The parenthetical `from OpenClaw` constrains the scope so Claude does not fire this skill when the orchestration context is a different platform. Six triggers in 35 words.

### R05 — Body length

The SKILL.md covers eight sections in 299 lines — 201 below the ceiling. The entire tool API reference is compressed into a single 11-row table with no surrounding prose:

> From `skills/claude-code-orchestration/SKILL.md:287-299`:
>
> ```
> ## 8. Quick tool reference
>
> | Tool | Usage | Key parameters |
> |---|---|---|
> | `claude_launch` | Launch a session | `prompt`, `name`, `workdir`, `multi_turn`, `max_budget_usd` |
> | `claude_sessions` | List sessions | `status` (all/running/completed/failed) |
> | `claude_output` | Read the output | `session`, `full`, `lines` |
> | `claude_fg` | Foreground + live stream | `session` |
> | `claude_bg` | Switch back to background | `session` |
> | `claude_kill` | Kill a session | `session` |
> | `claude_respond` | Send a follow-up | `session`, `message`, `interrupt` |
> | `claude_stats` | Usage metrics | none |
> ```

Trading trailing prose for a reference table at the end is what keeps eight sections under 300 lines.

### R06 — Code examples must be runnable

All launch examples use real parameter names in real call syntax. The three examples span three cost tiers and explicitly model when to reach for `model: "opus"`:

> From `skills/claude-code-orchestration/SKILL.md:38-66`:
>
> ```
> # Simple task
> claude_launch(
>   prompt: "Fix the null pointer in src/auth.ts line 42",
>   name: "fix-null-auth",
>   workdir: "/home/user/projects/myapp",
>   multi_turn: true,
>   max_budget_usd: 2
> )
>
> # Full feature
> claude_launch(
>   prompt: "Implement dark mode toggle in the settings page. Use the existing theme context
>   in src/context/theme.tsx. Add a toggle switch component and persist the preference in localStorage.",
>   name: "add-dark-mode",
>   workdir: "/home/user/projects/myapp",
>   multi_turn: true,
>   max_budget_usd: 5
> )
>
> # Major refactoring
> claude_launch(
>   prompt: "Refactor the database layer to use the repository pattern. Migrate all direct
>   Prisma calls in src/services/ to use repositories in src/repositories/.",
>   name: "refactor-db-repositories",
>   workdir: "/home/user/projects/myapp",
>   multi_turn: true,
>   max_budget_usd: 10,
>   model: "opus"
> )
> ```

The prompts are specific enough to execute — none say "do the refactoring task." The `model: "opus"` override appears only in the highest-budget example, making the model-selection heuristic implicit in the examples rather than stated as a rule.

### R07 — Scope note when related skills exist

Section 5 routes the channel-setup question out of the skill at exactly the point where a reader would start asking about it:

> From `skills/claude-code-orchestration/SKILL.md:204-206`:
>
> ```
> Notifications are routed automatically based on the session's `workdir` using the `agentChannels`
> plugin config. Each workspace directory maps to a specific channel (e.g., `telegram:seo-bot:123456789`).
> See [Agent Channels](../../docs/AGENT_CHANNELS.md) for setup.
> ```

The cross-reference is placed mid-section rather than at the top, so it fires only after the reader has the routing concept in hand. The audit confirmed the target resolves: `docs/AGENT_CHANNELS.md` ✓ — no R36 breakage.

### R08 — Patterns over theory

Section 7 is a nine-row anti-pattern table with three columns: what goes wrong, the mechanism behind it, and the fix:

> From `skills/claude-code-orchestration/SKILL.md:272-284`:
>
> ```
> | Anti-pattern | Consequence | Fix |
> |---|---|---|
> | Passing `channel` explicitly | Bypasses automatic routing, notifications may go to wrong bot | Let `agentChannels` handle routing automatically |
> | Forgetting `multi_turn: true` | Unable to send follow-ups with `claude_respond` | Enable `multi_turn` except for explicit one-shots |
> | Not checking the result of a completed session | The user doesn't know what happened | Always read `claude_output` and summarize |
> | Launching too many sessions in parallel | `maxSessions` limit reached, sessions rejected, diluted attention | Respect the limit, prioritize, sequence if necessary |
> | Using the agent's `workdir` instead of the project's | Claude Code works in the wrong directory | Always point to the target project directory |
> | Not naming sessions | Hard to identify them in `claude_sessions` | Always use `name` in kebab-case |
> | Auto-responding to critical questions | Decisions made without the user's approval | When in doubt, forward to the user |
> | Ignoring wake events | Sessions stuck waiting indefinitely | Handle each wake event promptly |
> | Not adjusting the budget | Waste (too high) or interruption (too low) | Calibrate `max_budget_usd` based on complexity |
> ```

The Consequence column names the mechanism (`maxSessions limit reached`, `Claude Code works in the wrong directory`), not just the symptom. Claude can match its current situation against a mechanism rather than a vague label.

## Worth adopting

Pattern: Two-column exhaustive decision gate for binary agent judgment. Evidence: `skills/claude-code-orchestration/SKILL.md:147-161` (the "When to auto-respond vs forward to the user" section lists 4 auto-respond cases and 6 forward-to-user cases under explicit headers). Why it would be a useful rule: when a skill must teach a binary routing decision, exhaustive enumeration under labeled headers is faster for a model to match against than principle-based prose, and leaves no gray zone for judgment drift.

Pattern: Numbered pre-flight checklist with inline consequences. Evidence: `skills/claude-code-orchestration/SKILL.md:234-239` (the "Launch checklist" sub-section — five items, each ending with `->` and the consequence of compliance, e.g., `` `agentChannels` is configured for this workdir -> notifications arrive ``). Why it would be a useful rule: pairing each checklist item with its consequence makes the list enforceable — Claude can verify each item and understand why skipping it matters, rather than treating the checklist as advisory.
