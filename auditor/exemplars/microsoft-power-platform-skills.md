---
slug: microsoft-power-platform-skills
repo: microsoft/power-platform-skills
audited: 2026-09-30
commit_sha: c97753299937976aae38710c190dc64be605051f
score: 96
exemplifies:
  - R04
  - R08
  - R11
  - R30
  - R31
---

# Exemplar: microsoft/power-platform-skills

**Score**: 96/100  |  **Date**: 2026-09-30  |  **Commit**: `c97753299937976aae38710c190dc64be605051f`

A 7-plugin Power Platform marketplace (69 skills, 20 agents, 4 hook configs) whose skill descriptions pack many user phrasings, whose gotcha lists encode API quirks, and whose hook launchers fail open when their environment is missing.

## Per-rule evidence

### R04 — Description as trigger

`plugins/power-pages/skills/manage-firewall/SKILL.md` lists the concrete requests that should route to the skill (turn on WAF, block by IP or country, rate-limit login, "is my site protected against bots?"). It also names the case where the user does not use the product term ("add rate limit" without saying "firewall").

> Real quote from `plugins/power-pages/skills/manage-firewall/SKILL.md:3-13`:
>
> ```
> description: >-
>   Inspects and configures the web application firewall (WAF) in front of a
>   Power Pages production site. Lists the current state, recommends enabling
>   protection when it is off, and walks the user through adding, updating,
>   or removing custom rules — IP blocks, country blocks, path blocks, and
>   rate limits. Use when the user wants to turn on WAF, block traffic by
>   IP or country, rate-limit login or signup pages, protect pages from
>   brute-force attempts, restrict access to specific paths, review the
>   current firewall configuration, or asks "is my site protected against
>   bots / common web attacks?" — even if they say "add rate limit" or
>   "protect login page" without mentioning "firewall" or "WAF".
> ```

The description carries 6+ action phrases plus a quoted user question and an explicit "even if they don't say the keyword" clause, where a summary-only description would carry none.

A shorter description in the same repo still meets the bar:

> Real quote from `plugins/power-pages/skills/add-seo/SKILL.md:3-6`:
>
> ```
> description: >-
>   Adds SEO essentials to a Power Pages code site, including robots.txt, sitemap.xml,
>   meta tags, Open Graph tags, and favicon configuration. Use when the user wants to
>   improve search engine optimization or make their site more searchable.
> ```

It names the deliverables (robots.txt, sitemap.xml, Open Graph) and two user-intent phrasings in three lines.

### R08 — Patterns over theory

`manage-firewall` opens its body with a `## Gotchas` list. Each bullet is a situation, the API behavior, and the action to take, including exact status codes, value ranges and error codes.

> Real quote from `plugins/power-pages/skills/manage-firewall/SKILL.md:33-38`:
>
> ```
> - **Concurrent-operation guard.** `B003` means another enable/disable is in flight. Poll status until it settles, then retry.
> - **False-positive managed rule:** disable via a rule override (`EnabledState: "Disabled"` inside `RuleGroupOverrides` — managed rule fields use PascalCase).
> - **First-match-wins.** Rules evaluate in priority order. A geo-allow-then-default-deny pattern requires an explicit default-deny rule AFTER the allow.
> - **Custom rule priority range: 11–65000.** Values 1–10 are reserved for platform-managed rules.
> - **`set-rules.js` is additive / update-only.** Send only rules being created or modified. The service merges them; existing rules not in the payload are untouched.
> - **Use `delete-rules.js` to remove rules.** `set-rules.js` cannot remove. Always use `delete-rules.js --names`.
> ```

Every bullet names a trigger (`B003`, a false-positive rule, a geo-allow) and a concrete next step, with no background prose in between.

### R11 — Tools follow least-privilege

`plugins/model-apps/agents/genpage-planner.md` declares six named tools plus portable aliases, and a comment records the one tool it deliberately omits and why.

> Real quote from `plugins/model-apps/agents/genpage-planner.md:11-29`:
>
> ```
> # Two naming schemes on purpose: Claude Code names first, then the portable
> # Copilot aliases for the same capabilities. Every host ignores tool names it
> # does not recognize, so declaring both is safe and keeps this agent's file,
> # shell and todo tools even on a host that does not implement the compatible-
> # alias table. `TaskCreate`/`TaskUpdate`/`TaskList` are NOT aliases anywhere —
> # `todo` is the portable name. `agent`/`Task` is deliberately ABSENT: this
> # planner returns a discovery request and the orchestrator dispatches.
> # See references/agent-interaction-contract.md.
> tools:
>   - Read
>   - Write
>   - Bash
>   - TaskCreate
>   - TaskUpdate
>   - TaskList
> ```

The list withholds `Task` so the planner cannot spawn subagents, and the rationale sits next to the list. Note the audit found `model`/`<example>` gaps on this agent; this quote supports R11 only.

### R30 — `${CLAUDE_PLUGIN_ROOT}` for paths

`plugins/power-pages/hooks/hooks.json` resolves every hook script from the host-provided plugin root and never from `process.cwd()` or an absolute path.

> Real quote from `plugins/power-pages/hooks/hooks.json:9`:
>
> ```
> "command": "node -e \"const path=require('node:path'); const root=process.env.PLUGIN_ROOT||process.env.CLAUDE_PLUGIN_ROOT; if(!root){console.error('PLUGIN_ROOT is not set'); process.exit(0);} require(path.resolve(root,'hooks','run-skill-pretool-telemetry.js'));\"",
> ```

The same resolution appears on all three registered events (lines 9, 21, 32), so a plugin moved to any install path keeps working. It uses an env-var fallback chain (`PLUGIN_ROOT`, then `CLAUDE_PLUGIN_ROOT`) rather than the literal `${CLAUDE_PLUGIN_ROOT}` string.

### R31 — Fail-open by default

The same command exits 0 when the root is unset, so a missing environment variable cannot block the user's tool call. The repo's `CLAUDE.md` states the intent for the telemetry code these hooks call.

> Real quote from `plugins/power-pages/hooks/hooks.json:9`:
>
> ```
> if(!root){console.error('PLUGIN_ROOT is not set'); process.exit(0);}
> ```

> Real quote from `plugins/power-pages/CLAUDE.md` (Telemetry section):
>
> ```
> **Fail closed:** telemetry code must never change a script's exit code or break a skill run.
> ```

The behavior is fail-open for the user's action (exit 0, message on stderr); the source's wording "fail closed" refers to emission being suppressed. Every hook in the audited files uses `timeout: 30`, which bounds the cost of a hang.

## Worth adopting

Pattern: Declare a tool in both host naming schemes and validate that neither list is one-sided. Evidence: `plugins/model-apps/agents/genpage-planner.md:11-29`, enforced by `scripts/validate-agent-interactivity.js` per `plugins/model-apps/CLAUDE.md`. Why it would be a useful rule: an agent that names a capability in only one host's vocabulary launches without that tool on the other host, with no error.
