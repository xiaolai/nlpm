---
slug: plugin87-ux-ui-agent-skills
repo: plugin87/ux-ui-agent-skills
audited: 2026-10-01
commit_sha: f2e2f7fcc5cb9d99bbd8ec5e0d75cebb98e21e7e
score: 98
exemplifies:
  - R04
  - R07
  - R14
  - R16
  - R22
  - R24
  - R35
---

# Exemplar: plugin87/ux-ui-agent-skills

**Score**: 98/100  |  **Date**: 2026-10-01  |  **Commit**: `f2e2f7fcc5cb9d99bbd8ec5e0d75cebb98e21e7e`

A design-system plugin with 19 skills, 5 commands, 1 agent and 7 path-split rule files. Its skills name a runnable script for each check, so a reviewer can verify compliance by running the gate.

## Per-rule evidence

### R04 — Description as trigger

The `a11y-audit` description states the deliverable first, then lists four concrete user intents after "Use when". The intents are phrased as things a user would say: accessibility check, contrast verification, keyboard/screen-reader review, POUR conformance.

> Real quote from `.claude/skills/a11y-audit/SKILL.md:3`:
>
> ```
> description: Audit a UI or design against WCAG 2.2 AA/AAA and ARIA patterns, returning criterion-referenced findings with severity and specific fixes. Use when the user wants an accessibility check, contrast verification, keyboard/screen-reader review, or wants to confirm a component meets POUR.
> ```

The summary clause and the trigger clause are separate sentences, so the trigger list is not diluted by a feature overview.

### R07 — Scope note when related skills exist

`design-component` and `design-code` overlap (both produce components). The description of `design-component` ends with a redirect that tells Claude which of the two to pick for framework output.

> Real quote from `.claude/skills/design-component/SKILL.md` (frontmatter `description`):
>
> ```
> Use when the user wants to design or document a component (button, input, tabs, toast, combobox, date picker, modal, etc.) at the spec level before or alongside code. For generating framework code, use design-code.
> ```

The redirect names the sibling skill by its exact `name`, and it sits in the `description`, which is the field Claude reads when choosing between skills.

### R14 — Steps must be numbered

Both `a11y-audit` and `design-qa` put the procedure under `## Steps` as a numbered list. Each step names the file or script it uses and the order matters (fast gates before slow ones).

> Real quote from `.claude/skills/design-qa/SKILL.md:11-16`:
>
> ```
> ## Steps
> 1. Read `workflows/design-qa.md` (the QA pyramid: token/lint gates → automated a11y → visual regression → manual a11y).
> 2. Wire the **fast gates** first (every commit/PR): `python3 scripts/validate_tokens.py`, `python3 scripts/validate_contrast.py` (batch WCAG over the token pairs), and `python3 scripts/lint_hardcodes.py <src>` (no raw hex/px/timing in component code). The repo's `.github/workflows/ci.yml` runs these.
> 3. Add **automated a11y** (axe-core / Pa11y) over each component's states (error/loading/disabled/expanded/selected), zero serious/critical to merge.
> ```

Each step carries a literal command line, so the step can be executed without interpretation.

### R16 — Define output format

`a11y-audit` closes with an `## Output` section giving the exact columns of the findings table. `design-qa` closes with a `## Verification (definition of done)` section of checkable statements.

> Real quote from `.claude/skills/a11y-audit/SKILL.md:18-19`:
>
> ```
> ## Output
> A findings table: WCAG criterion (e.g. 1.4.3) · severity (P0/P1/P2) · what fails · specific fix. Confirm passes explicitly. Accessibility may never be traded for aesthetics.
> ```

The four columns are named and ordered, and "Confirm passes explicitly" prevents a findings-only report from being read as a silent pass.

> Real quote from `.claude/skills/design-qa/SKILL.md:19`:
>
> ```
> - An unreviewed PR cannot introduce an unresolved token alias, a contrast failure, a raw hex/px, or an axe violation — a gate blocks each.
> ```

### R22 — Must be enforceable

The CLAUDE.md verification protocol turns "be accurate" into a rule that can be checked from the transcript: any quoted number must trace to a gate's output. The `.claude/rules/accessibility.md` P0 list does the same with thresholds instead of adjectives.

> Real quote from `CLAUDE.md` (Verification Protocol, item 1):
>
> ```
> 1. **Never state a number you did not measure.** Any contrast ratio, "WCAG pass", "100%", or "all states OK" must come from actually running a gate and reporting its real output — never from reasoning or memory. If you haven't run it, say "not verified yet."
> ```

> Real quote from `.claude/rules/accessibility.md:13-18`:
>
> ```
> 1. Keyboard navigable — Tab reaches it, Enter/Space activates it
> 2. Focus visible — Focus ring meets 3:1 contrast
> 3. Screen reader — Announces name, role, state
> 4. Color contrast — 4.5:1 text, 3:1 UI
> 5. Target size — ≥ 24×24px
> 6. No color-only — Information not conveyed by color alone
> ```

A reviewer can check the first rule by looking for a gate invocation before any ratio appears, and each P0 line has a numeric or observable pass condition.

### R24 — Don't duplicate tooling

Where a script already checks a rule, the rule text points at the script and does not restate the check. The "Single-Theme Consistency" section lists the enforcer next to each constraint.

> Real quote from `.claude/rules/tokens-and-color.md` (Single-Theme Consistency, items 2-3):
>
> ```
> 2. **No off-theme values** — zero hardcoded hex/px/timing in component/page code. Enforced by `scripts/lint_hardcodes.py` (the one allowed exception: adapter theme-config that maps our tokens *into* a 3rd-party API, e.g. MUI/Mantine).
> 3. **Real WCAG, on the source** — the token theme itself passes WCAG 2.2 in **both** light and dark before any page ships. Enforced by `scripts/validate_contrast.py` (required text/action pairs fail the build; tertiary/decorative are advisory).
> ```

Each rule names its enforcing script, states its one exception, and says which pairs fail the build and which are advisory.

### R35 — Include architecture overview

CLAUDE.md ends with a "File Reference Map" that gives the purpose of every top-level directory, and a "Request Router" table that maps each request type to a skill and the files to load.

> Real quote from `CLAUDE.md` (Request Router):
>
> ```
> | Request | Skill | Load |
> |---------|-------|------|
> | Generate/extend/validate tokens, palettes, theming | `design-tokens` | `tokens/*.json`, "Token System"; `scripts/validate_tokens.py` |
> | Design or build a screen / component | `design-component` | `components/*`, `accessibility/aria-patterns.md`, `tokens/*`; `scripts/scaffold_component.py` |
> | Accessibility / WCAG / contrast check | `a11y-audit` | `accessibility/*`; `scripts/contrast.py` |
> ```

The map pairs each intent with the skill and the exact files to read, so Claude loads `accessibility/*` for an audit and skips `frameworks/*`.

## Worth adopting

Pattern: Always-on core plus on-demand rule files, with a test that the split holds. Evidence: `CLAUDE.md` (Rules table: "`CLAUDE.md` stays short because it loads on every turn. Read the rule file when the task enters its territory") and the `scripts/validate_instruction_surface.py` entry in the File Reference Map ("the emoji ban and gate protocol stay always-on in CLAUDE.md; every .claude/rules file is routed; brief stays short"). Why it would be a useful rule: R25 covers path-scoping, but nothing requires a check that every on-demand rule file is routed from CLAUDE.md and that the always-on invariants have not drifted out of it.

Pattern: Treat a gate that cannot run as failing. Evidence: `CLAUDE.md` Verification Protocol item 8 ("A render gate with no browser prints SKIPPED and exits 0. That is not a pass... set `DS_REQUIRE_BROWSER=1`"). Why it would be a useful rule: an instruction that tells Claude to run a verification step should say what a skipped or unavailable run means, or Claude will report a skip as a pass.
