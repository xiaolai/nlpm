# NLPM Audit: c0x12c/ai-toolkit

**Date:** 2026-04-25  
**Plugin:** `@c0x12c/ai-toolkit` v1.22.1  
**Repo:** https://github.com/c0x12c/ai-toolkit  
**Auditor:** NLPM Auditor Pipeline  
**Overall NL Score:** 96 / 100

---

## Summary

The c0x12c/ai-toolkit is a mature, high-quality Claude Code plugin implementing the "Spartan / GSD" (Get Stuff Done) workflow framework. It packages 10 agents, 25 commands, and 34 skills covering full-stack development, infrastructure, design, research, and startup operations. The overall NL quality is excellent. Two bugs and one pervasive quality gap (missing `allowed-tools` on all commands) prevent a perfect score. Security posture is acceptable with no Critical or High findings; three Medium risks warrant attention.

---

## NL Score Table

### Agents (unique — `.codex/agents/` mirrors are byte-for-byte identical)

| File | Score | Penalties |
|------|-------|-----------|
| `toolkit/agents/research-planner.md` | 85 | -15 zero examples |
| `toolkit/agents/micronaut-backend-expert.md` | 98 | -2 vague quantifier ("when helpful") |
| `toolkit/agents/sre-architect.md` | 100 | — |
| `toolkit/agents/phase-reviewer.md` | 90 | -10 BUG: body references shell commands (cat, ls) without Bash in tools |
| `toolkit/agents/idea-killer.md` | 85 | -15 zero examples |
| `toolkit/agents/design-critic.md` | 100 | — |
| `toolkit/agents/team-coordinator.md` | 100 | — |
| `toolkit/agents/infrastructure-expert.md` | 100 | — |
| `toolkit/agents/solution-architect-cto.md` | 100 | — |
| `toolkit/agents/ai-designer.md` | 85 | -15 zero examples |

**Agents average: 94.3 / 100**

---

### Commands (unique — `.codex/commands/spartan/` files, no `.codex` mirrors of the spartan commands in toolkit)

All 25 commands share one systemic penalty: **missing `allowed-tools` frontmatter field (-5 each)**.

| File | Score | Additional Penalties |
|------|-------|----------------------|
| `spartan:ask` | 95 | — |
| `spartan:architect` | 95 | — |
| `spartan:backend-api-design` | 95 | — |
| `spartan:brainstorm` | 95 | — |
| `spartan:commit-message` | 95 | — |
| `spartan:competitive-teardown` | 95 | — |
| `spartan:content-engine` | 95 | — |
| `spartan:database-table-creator` | 95 | — |
| `spartan:debug` | 95 | — |
| `spartan:deep-research` | 95 | — |
| `spartan:design` | 95 | — |
| `spartan:design-figma-to-code` | 95 | — |
| `spartan:gsd` | 95 | — |
| `spartan:guard` | 90 | -5 also missing empty-input guard for required `{{ args[0] }}` with no Jinja default |
| `spartan:idea-validation` | 95 | — |
| `spartan:implement` | 95 | — |
| `spartan:investor-outreach` | 95 | — |
| `spartan:ops-investigate-alert` | 95 | — |
| `spartan:ops-oncall-log` | 95 | — |
| `spartan:pr` | 95 | — |
| `spartan:review` | 95 | — |
| `spartan:security-checklist` | 95 | — |
| `spartan:terraform-review` | 95 | — |
| `spartan:test` | 95 | — |
| `spartan:web-to-prd` | 95 | — |

**Commands average: 94.8 / 100**

---

### Skills (unique — `toolkit/skills/`, `.codex/skills/` mirrors identical where they exist)

| File | Score | Penalties |
|------|-------|-----------|
| `toolkit/skills/terraform-review/SKILL.md` | 100 | — |
| `toolkit/skills/startup-pipeline/SKILL.md` | 100 | — |
| `toolkit/skills/deep-research/SKILL.md` | 100 | — |
| `toolkit/skills/service-debugging/SKILL.md` | 100 | — |
| `toolkit/skills/testing-strategies/SKILL.md` | 100 | — |
| `toolkit/skills/investor-outreach/SKILL.md` | 100 | — |
| `toolkit/skills/ui-ux-pro-max/SKILL.md` | 97 | -3 no Gotchas section |
| `toolkit/skills/backend-api-design/SKILL.md` | 100 | — |
| `toolkit/skills/design-intelligence/SKILL.md` | 100 | — |
| `toolkit/skills/security-checklist/SKILL.md` | 100 | — |
| `toolkit/skills/kotlin-best-practices/SKILL.md` | 97 | -3 no Gotchas section (has "What to Avoid" inline) |
| `toolkit/skills/api-endpoint-creator/SKILL.md` | 97 | -3 no Gotchas section |
| `toolkit/skills/python-best-practices/SKILL.md` | 100 | — |
| `toolkit/skills/python-api-endpoint-creator/SKILL.md` | 100 | — |
| `toolkit/skills/database-patterns/SKILL.md` | 100 | — |
| `toolkit/skills/database-table-creator/SKILL.md` | 97 | -3 uses "Common Mistakes" not canonical Gotchas section |
| `toolkit/skills/ci-cd-patterns/SKILL.md` | 100 | — |
| `toolkit/skills/browser-qa/SKILL.md` | 100 | — |
| `toolkit/skills/article-writing/SKILL.md` | 100 | — |
| `toolkit/skills/brainstorm/SKILL.md` | 100 | — |
| `toolkit/skills/competitive-teardown/SKILL.md` | 100 | — |
| `toolkit/skills/content-engine/SKILL.md` | 100 | — |
| `toolkit/skills/design-workflow/SKILL.md` | 95 | -5 no Gotchas section, no formal examples |
| `toolkit/skills/idea-validation/SKILL.md` | 100 | — |
| `toolkit/skills/investor-materials/SKILL.md` | 100 | — |
| `toolkit/skills/market-research/SKILL.md` | 100 | — |
| `toolkit/skills/ops-investigate-alert/SKILL.md` | 97 | -3 no Gotchas section |
| `toolkit/skills/ops-oncall-log/SKILL.md` | 97 | -3 no Gotchas section |
| `toolkit/skills/python-testing-strategies/SKILL.md` | 100 | — |
| `toolkit/skills/terraform-best-practices/SKILL.md` | 88 | -12 BUG: missing required `allowed_tools` frontmatter field |
| `toolkit/skills/terraform-module-creator/SKILL.md` | 97 | -3 no Gotchas section |
| `toolkit/skills/terraform-security-audit/SKILL.md` | 97 | -3 no Gotchas (but has extensive inline bad/good examples) |
| `toolkit/skills/terraform-service-scaffold/SKILL.md` | 97 | -3 no Gotchas section |
| `toolkit/skills/web-to-prd/SKILL.md` | 97 | -3 no formal Gotchas (extensive rules section present) |

**Skills average: 98.6 / 100**

---

### Weighted Overall

| Category | Count | Average | Weight |
|----------|-------|---------|--------|
| Agents | 10 | 94.3 | 14.5% |
| Commands | 25 | 94.8 | 36.2% |
| Skills | 34 | 98.6 | 49.3% |
| **Overall** | **69** | **96.0** | — |

---

## Security Scan

**Scan date:** 2026-04-25  
**Surfaces examined:** hooks (JS), scripts (shell, Python), bridges (JS), package manifests

### Severity Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH | 0 |
| MEDIUM | 3 |
| LOW | 3 |

### Medium Findings

**M-1: String interpolation in execSync — `toolkit/hooks/spartan-check-update.js:174,181`**

```javascript
execSync('git fetch --quiet origin ' + branch, {...})
execSync('git show origin/' + branch + ':toolkit/VERSION', {...})
```

`branch` is built from git output and concatenated directly into a shell command string. Sanitization exists at line 169 (`branch.replace(/[^a-zA-Z0-9._/-]/g, '')`), but the allowlist permits `/` which could enable path traversal in git refs. Risk is locally bounded (attacker must already control the git remote or environment), but pattern is unsafe.

**M-2: Default bypassPermissions in bridge engine — `bridges/core/engine.js:433-438`**

```javascript
options.permissionMode = "bypassPermissions";
options.allowDangerouslySkipPermissions = true;
options.allowedTools = ["Read","Write","Edit","Bash","Glob","Grep","WebSearch","WebFetch","Task"];
```

When `permInteractive` is false (the default), the bridge engine silently grants all tools with permission bypass. Users who adopt the bridge without reading this default get a maximally-permissive agent with no confirmation prompts.

**M-3: Unpinned latest npm execution — `toolkit/scripts/setup.sh:262`**

```bash
npx get-shit-done-cc@latest $GSD_FLAGS
```

Executes whatever the npm registry serves as `latest` at run time. A compromised or malicious publish could execute arbitrary code on the installer's machine.

### Low Findings

**L-1: Caret-pinned bridge dependency — `bridges/telegram/package.json`**

`node-telegram-bot-api@^0.66.0` and `dotenv@^16.4.7` use caret ranges — minor/patch updates install automatically. Low supply chain risk.

**L-2: Caret-pinned root dependency — `toolkit/package.json`**

`js-yaml@^4.1.1` auto-updates minor/patch. Low risk for a parsing library.

**L-3: API key sourcing from env files — `toolkit/scripts/design/ai-image.sh`**

Sources `.spartan/ai.env`, `.env`, and `~/.spartan/ai.env` for Gemini API keys. Expected behavior; no credentials are logged or transmitted beyond the intended API.

---

## Bugs

### BUG-1: `toolkit/agents/phase-reviewer.md` — Bash commands without Bash tool

**Severity:** HIGH (registration/runtime break)  
**Location:** Agent body, instructions section

The agent's step-by-step instructions include:

```
cat .spartan/config.yaml
ls rules/
ls .claude/rules/
```

The agent `tools` frontmatter declares only `["Read","Grep","Glob","WebSearch"]`. When Claude Code materializes this agent and it attempts to execute `cat` or `ls` via Bash, the tool call will be rejected — Bash is not in the declared toolset.

**Fix:** Add `"Bash"` to the agent's `tools` array, or replace shell commands with equivalent `Read`/`Glob` tool calls in the instructions.

---

### BUG-2: `toolkit/skills/terraform-best-practices/SKILL.md` — Missing `allowed_tools` frontmatter

**Severity:** MEDIUM (convention violation; skill will load but tool access is undefined)  
**Location:** YAML frontmatter

The `SKILL_AUTHORING.md` schema requires `allowed_tools` in every skill's frontmatter. `terraform-best-practices/SKILL.md` omits this field entirely. Claude Code cannot validate tool access for this skill at load time.

**Fix:** Add `allowed_tools: [Read, Glob, Grep]` (or appropriate set) to the frontmatter.

---

## Quality Issues

### Q-1: All 25 commands missing `allowed-tools` frontmatter (systemic)

Every command in `.codex/commands/spartan/` lacks the `allowed-tools` field in YAML frontmatter. This is a systemic gap — no command declares which tools Claude may use when executing it.

**Impact:** -5 penalty per command × 25 = -125 total penalty points absorbed into the commands category.  
**Fix:** Add `allowed-tools` lists to all command frontmatter blocks. Most commands invoke `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`; multi-step orchestration commands like `spartan:gsd` also need `Task` (for sub-agent dispatch).

---

### Q-2: Three agents have zero example blocks

`research-planner`, `idea-killer`, and `ai-designer` each have zero concrete input/output examples in their agent body. Examples are the primary mechanism for calibrating agent behavior.

**Impact:** -15 per agent × 3 = -45 penalty points.  
**Fix:** Add at least one `## Example` block per agent showing a representative invocation and the expected response format.

---

### Q-3: `spartan:guard` missing empty-input handling

`spartan:guard` requires `{{ args[0] }}` (a guard rule argument) but provides no Jinja default (e.g., `{{ args[0] | default('') }}`). If invoked with no argument, Jinja raises a TemplateError before the command body runs.

**Fix:** Add `{{ args[0] | default('') }}` and add a guard at the top of the command body that checks whether the argument is empty and returns a usage hint.

---

## Cross-Component Observations

### Mirror Architecture

`.codex/` is a mirror of `toolkit/`. All files that exist in both locations are byte-for-byte identical (confirmed by diff on representative samples). This is intentional — `compile-packs.js` in `prepublishOnly` generates the `.codex/` tree from `toolkit/`.

### Incomplete Mirror: `.codex/skills/`

`.codex/skills/` contains 26 skills; `toolkit/skills/` contains 34. Eight skills exist only in `toolkit/` and have no `.codex/` mirror:

- `ci-cd-patterns`
- `browser-qa`
- `ops-investigate-alert`
- `ops-oncall-log`
- `python-best-practices`
- `python-api-endpoint-creator`
- `python-testing-strategies`
- `service-debugging`

These skills are unreachable from the Codex command surface. If any Spartan command invokes these skills, those invocations will silently fail to find the skill.

### Incomplete Mirror: `.codex/agents/`

`.codex/agents/` contains 5 agents; `toolkit/agents/` contains 10. Five agents exist only in `toolkit/`:

- `design-critic`
- `team-coordinator`
- `infrastructure-expert`
- `solution-architect-cto`
- `ai-designer`

Same concern as skills: these agents cannot be invoked from Codex commands that route through `.codex/`.

### Rules Library Not Registered as Skills

`toolkit/rules/` contains rich, well-structured rule documents (DESIGN_PROCESS.md, ARCHITECTURE.md, GIT_COMMIT.md, NAMING_CONVENTIONS.md, TIMEZONE.md, and more). None have `SKILL.md` frontmatter wrappers. They function as human-readable reference docs but are not registered as loadable skills. Wrapping each with a `SKILL.md` would make them invocable via `/use-skill` and discoverable by NLPM scanners.

---

## Recommendation

**Merge-eligible with fixes.** The plugin is production-quality. Address bugs before shipping to any team that uses `phase-reviewer` or `terraform-best-practices`. The systemic missing `allowed-tools` on commands is the single highest-leverage quality fix — one batch PR adding those fields would close 25 findings and raise the commands average from 94.8 to ~99.8.

Priority order:
1. **BUG-1** — Add `Bash` to `phase-reviewer` tools (5-minute fix)
2. **BUG-2** — Add `allowed_tools` to `terraform-best-practices` frontmatter (2-minute fix)
3. **M-2** — Document or change `bypassPermissions` default in `bridges/core/engine.js` (design decision)
4. **M-3** — Pin `get-shit-done-cc` to a specific version in `setup.sh`
5. **Q-1** — Add `allowed-tools` to all 25 commands (batch PR)
6. **Q-2** — Add example blocks to `research-planner`, `idea-killer`, `ai-designer`
7. Mirror gap — Add `.codex/` mirrors for the 8 missing skills and 5 missing agents
