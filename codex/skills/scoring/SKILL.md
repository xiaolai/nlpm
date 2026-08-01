---
name: scoring
description: Use when scoring NL artifact quality, applying penalties, or calibrating lint judgment — contains the 100-point rubric with penalty tables per artifact type and 4 worked calibration examples.
version: 0.3.0
---

# NLPM Quality Scoring Rubric

100-point quality scale for all NL programming artifacts. Apply penalties deterministically. Use calibration examples to anchor judgment on borderline cases.

---

## Scoring Formula

```
base_score = 100
adjustments = sum of all applicable penalties (all penalties are negative)
final_score = max(0, min(100, base_score + adjustments))
```

Penalties stack. The floor is 0; the ceiling is 100. No bonuses — the default assumption is that an artifact is well-formed, and quality is measured by what is missing or wrong.

---

## Penalty Tables

### Skills

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| -- | `name` present | Missing | -25 |
| -- | `name` matches parent directory | Frontmatter `name:` value does not equal parent directory name (per `nlpm:conventions` §5 — open spec MUST) | -15 |
| R04 | `description` present | Missing | -25 |
| R04 | Trigger quality | Description is generic (≤1 specific phrase) | -15 |
| R04 | Description length | Description 500–800 chars | -5 |
| R04 | Description length | Description >800 chars | -10 |
| R05 | Body length | 400–500 lines | -5 |
| R05 | Body length | >500 lines | -10 |
| R06 | Code examples | Complex concepts with no examples | -5 |
| R06 | Code examples | No examples at all in a technical skill | -10 |
| R06 | `<example>` blocks | Zero `<example>` blocks on a `user_invocable: true` skill | -10 |
| R07 | Scope note | No scope note / cross-references | -3 |

> **Scope-note discipline:** R07 means "scope note when related skills exist."
> Do NOT apply R07 to missing example blocks — that is the new R06 row above
> (penalty -10, not -15). The 2026-05-13 lijigang/ljg-skills audit applied
> R07 + −15 fourteen times for missing example blocks; both labels were
> wrong (R07 is not example-related, and -15 is the agents penalty, not
> the skills penalty). The validator at `auditor/scripts/validate-rule-ids.py`
> catches this kind of drift in CI.

> **`name` matches parent directory** (added 2026-05-25, audit:
> google/skills): the open Agent Skills spec at agentskills.io makes this
> a MUST. Mismatch is deterministic, high-confidence, and reproducible by
> single-line diff (frontmatter `name:` vs `basename($(dirname FILE))`).
> Mark such findings `confidence: high` per the manifest-vs-disk-diff
> principle in `agents/scorer.md` step 6. Note: this penalty did not
> exist before 2026-05-25 — re-scoring past audits will yield slightly
> lower scores for any corpus containing this defect, but no contribute
> outcomes are retroactively affected since no PRs were ever opened
> against a name-mismatch finding under the prior rubric.

---

### Agents

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R09 | `description` present | Missing | -25 |
| R09 | `<example>` blocks | Exactly 1 example | -5 |
| R09 | `<example>` blocks | Zero examples | -15 |
| R10 | `model` declared | Not declared | -5 |
| R10 | `model` appropriate | Wrong tier for task (e.g. opus for parsing) | -5 |
| R11 | `tools` declared | Not declared | -5 |
| R11 | Unused tools | Each tool declared but not used in body | -3 each |
| R12 | Output format | No output format spec in body | -10 |
| R11 | Write on read-only | Audit/review/scan agent declares Write or Edit | -10 |

---

### Commands

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| -- | `description` present | Missing | -25 |
| R18 | `argument-hint` present | Command takes input but no hint | -5 |
| R14 | Steps numbered | Multi-step body with no numbered steps | -10 |
| R15 | Empty input handling | No handling for empty/missing input | -10 |
| R16 | Output format | No output format defined | -10 |
| R17 | Error paths | No error handling for missing files or bad data | -5 |

---

### Shared Partials

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R19 | `user-invocable: false` | Missing or set to true | -25 |
| R20 | Purpose clear | Description doesn't state it's a partial | -10 |

---

### Rules

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R21 | `description` present | Missing frontmatter description | -10 |
| R21 | Format: bold imperative | No bold imperative opening | -5 |
| R21 | Format: rationale | No rationale following the imperative | -10 |
| R22 | Enforceability | Rule is not specific/testable | -10 |
| R23 | Budget | Rule file over 500 lines | -15 |
| R26 | Conflicts with other rules | Direct contradiction with another rule in same set | -20 |
| R24 | Duplicates tooling | Re-states what eslint/ruff/clippy already catches | -10 |

---

### Hooks — universal checks (apply to all tools)

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| -- | Valid syntax | Hook config file fails to parse (JSON or TOML per tool) | -25 |
| R29 | Scripts exist | Referenced script file does not exist | -20 |
| -- | Command safety | Hook command contains dangerous patterns (`rm -rf`, `git push --force`, `DROP TABLE`) | -15 |
| -- | Matcher regex valid | Matcher pattern doesn't compile as valid regex | -10 |
| -- | Timeout reasonable | Hook specifies timeout > 30s (likely hangs) | -5 |

### Hooks (Claude Code — Tier 2-Claude only)

Authoritative event list: `nlpm:conventions-claude` §7. Per the multi-tool design (`analysis/multi-tool-design-2026-05.md` decision #4), Claude / Codex / Antigravity hook event vocabularies are NOT 1:1 mappable — three separate tables, no translation.

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R27 | Event names valid (Claude) | Uses unrecognized event name — confirmed Claude events: `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PermissionRequest`, `Stop`, `StopFailure`, `FileChanged` | -15 |
| R27 | Case correct (Claude) | Event name has wrong case (e.g. `pretooluse`) | -10 |
| -- | Hook type valid (Claude) | Uses unrecognized `type` value — confirmed Claude types: `command`, `http`, `mcp_tool`, `prompt`, `agent` | -10 |
| -- | MCP matcher format (Claude) | Matcher targets MCP tool but doesn't use `mcp__<server>__<tool>` pattern | -5 |

### Hooks (Codex CLI — Tier 2-Codex only)

Authoritative event list: `nlpm:conventions-codex` §6.

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R27 | Event names valid (Codex) | Uses unrecognized event name — confirmed Codex events: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PermissionRequest`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`, `Stop` | -15 |
| R27 | Case correct (Codex) | Event name has wrong case | -10 |
| -- | Hooks config key (Codex) | `config.toml` uses deprecated `[features].codex_hooks` instead of `[features].hooks` (renamed ~CLI 0.129+) | -5 (advisory) |

### Hooks (Antigravity / Gemini lineage — Tier 2-Antigravity only) — ADVISORY

Authoritative event list: `nlpm:conventions-antigravity` §5. **All Antigravity-specific hook scoring is advisory-only** (confidence:low) until the Antigravity 2.0 spec stabilizes — see `analysis/multi-tool-design-2026-05.md` decision #3.

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R27 | Event names valid (Gemini lineage) | Uses unrecognized event name — confirmed events: `SessionStart`, `BeforeAgent`, `BeforeModel`, `BeforeToolSelection`, `BeforeTool`, `AfterTool`, `AfterModel`, `AfterAgent`, `SessionEnd`, `Notification`, `PreCompress` | -10 (advisory) |
| R27 | Case correct (Gemini lineage) | Event name has wrong case | -5 (advisory) |

---

### plugin.json (Claude Code — `.claude-plugin/plugin.json`)

| Check | Condition | Penalty |
|-------|-----------|---------|
| `name` present | Missing | -25 |
| `version` is semver | Present but not valid semver | -10 |
| `description` present | Missing | -5 |

---

### .codex-plugin/plugin.json (Codex CLI — Tier 2-Codex only)

Schema reference: `nlpm:conventions-codex` §3.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid JSON | File fails JSON parse | -25 |
| `name` present | Missing | -25 |
| `name` kebab-case | Mixed case or underscores | -10 |
| `version` is semver | Present but not valid semver | -10 |
| `description` present | Missing | -5 |
| Artifact paths relative | `skills`/`mcpServers`/`apps`/`hooks` paths absolute or missing `./` prefix | -5 each |

---

### .agents/plugins/marketplace.json (Codex marketplace — Tier 2-Codex)

Schema reference: `nlpm:conventions-codex` §4. Schema is largely compatible with Claude's `.claude-plugin/marketplace.json`.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid JSON | File fails JSON parse | -25 |
| `name` present | Missing | -25 |
| `plugins` array present | Missing or empty | -10 |
| Per-plugin `source` valid | `source.source` not in `github`/`git`/`local`, or required `repo`/`path` missing | -10 each |
| Per-plugin `category` present | Missing (informational, helps marketplace navigation) | -3 each |

---

### agents/openai.yaml (Codex skill sidecar — Tier 2-Codex)

Schema reference: `nlpm:conventions-codex` §2.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid YAML | File fails YAML parse | -25 |
| Sidecar is colocated | `agents/openai.yaml` not in same directory as a `SKILL.md` | -10 |
| `interface.display_name` present | Missing | -5 (informational) |

---

### gemini-extension.json (Gemini/Antigravity — Tier 2-Antigravity) — ADVISORY

Schema reference: `nlpm:conventions-antigravity` §3. **All Antigravity-specific manifest scoring is advisory-only** until the post-2026-06-18 Antigravity spec stabilizes.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid JSON | File fails JSON parse | -25 |
| `name` present | Missing | -25 |
| `version` present | Missing | -10 |
| `contextFileName` includes `AGENTS.md` | Single-tool projects use only `GEMINI.md`; multi-tool should include `AGENTS.md` | -3 (advisory; multi-tool nudge) |

---

### .gemini/commands/*.toml (Gemini slash commands — legacy/transitional, Tier 2-Antigravity)

Schema reference: `nlpm:conventions-antigravity` §4.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid TOML | File fails TOML parse | -25 |
| `prompt` field present | Missing required field | -25 |
| `description` field present | Missing (auto-generated from filename, but explicit is better) | -3 |

---

### .mcp.json (Claude Code — `.mcp.json` at repo root)

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid JSON | File fails JSON parse | -25 |
| Server `command` present | MCP server entry missing `command` field | -15 |

---

### .codex/config.toml (Codex configuration — Tier 2-Codex)

Schema reference: `nlpm:conventions-codex` §5.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid TOML | File fails TOML parse | -25 |
| Deprecated `[features].codex_hooks` | Should be `[features].hooks` (renamed ~CLI 0.129) | -5 (advisory) |
| Per-MCP `command` present | `[mcp_servers.<id>]` table missing `command` field | -15 each |

---

### .lsp.json (Claude Code LSP — Tier 2-Claude)

Schema details: `nlpm:conventions-claude` §12. Stable in 2026.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid JSON | File fails JSON parse | -25 |

---

### monitors/monitors.json (Claude Code monitors — Tier 2-Claude)

Schema details: `nlpm:conventions-claude` §13. Stable in 2026.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid JSON | File fails JSON parse | -25 |

---

### Settings Files (.claude/settings.json, .claude/settings.local.json)

| Check | Condition | Penalty |
|-------|-----------|---------|
| Valid JSON | File fails JSON parse | -25 |
| No hardcoded secrets | Contains API keys, tokens, or passwords | -25 |
| Permission mode sanity | `bypassPermissions` enabled in a shared project settings file (not .local) | -15 |
| Recognized keys | Contains unknown top-level keys not in Claude Code schema | -5 each, cap -15 |
| Hook definitions valid | `hooks` key present — check event names valid and case-correct | -10 per invalid |

---

### CLAUDE.md

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R49 | File exists | No CLAUDE.md in plugin root | -10 |
| -- | Under 200 lines | CLAUDE.md exceeds 200 lines | -5 |
| R38 | Actionable content | CLAUDE.md has no actionable guidance (just filler) | -10 |
| R33 | Build/run command | No instructions for how to build or run the project | -10 |
| R34 | Test command | No instructions for how to run tests | -5 |
| R35 | Architecture overview | No structure/component description (what lives where) | -5 |
| R36 | Valid `@` imports | Contains `@` import syntax referencing a file that doesn't exist | -10 |
| R37 | No stale file references | Mentions files or functions that no longer exist in the repo | -10 |
| R38 | Actionability ratio | >60% of content is description rather than instructions | -5 |
| -- | Prerequisites section | No section covering required tools, versions, or setup steps | -5 |
| R39 | No rule conflicts | CLAUDE.md says X while a `.claude/rules/` file says not-X | -15 |

---

### Memory Files

Applies to `.md` files located in `~/.claude/projects/*/memory/` directories.

| Rule | Check | Pass (+0) | Penalty |
|------|-------|-----------|---------|
| -- | Has YAML frontmatter | Present | -15 |
| -- | `name` in frontmatter | Present | -10 |
| -- | `description` in frontmatter | Present | -10 |
| -- | `type` in frontmatter | Present (`user`/`feedback`/`project`/`reference`) | -5 |
| -- | Content matches declared type | Yes | -10 |
| -- | Referenced in MEMORY.md index | Yes | -5 (orphaned memory) |
| R37 | Stale content | No references to removed files or functions | -10 |

---

### All Artifact Types: Vague Quantifiers

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R01 | Vague quantifier | Each occurrence of: "appropriate", "relevant", "as needed", "sufficient", "adequate", "reasonable", "properly", "correctly", "some", "several", "various" without measurable criteria | -2 each |
| R01 | Vague quantifier cap | Total vague quantifier penalty | max -20 |

---

### All Artifact Types: Vocabulary Drift (R51 — opt-in, disabled by default)

Applied only when `R51: { enabled: true, vocabulary_skill: <path> }` appears in `.claude/nlpm.local.md`. Without the opt-in, R51 contributes zero penalty regardless of artifact content. The configured `vocabulary_skill` must contain a `registry.yaml` listing canonical and deprecated terms; without it, R51 emits an advisory and contributes zero penalty.

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R51 | Deprecated synonym | Each occurrence of a term marked `deprecated:` in the project's `registry.yaml`, in the scope the artifact belongs to | -2 each |
| R51 | Drift cap | Total R51 penalty | max -10 per file |
| R51 | Missing registry | `enabled: true` but `vocabulary_skill:` not set or points to a directory with no `registry.yaml` | 0 (advisory only) |

> **Why opt-in:** vocabulary discipline is high-leverage for projects with accumulated drift but premature for projects still discovering their domain. Each project decides when it has enough literary warrant (P6) to lock terms in. See `analysis/vocabulary-design-principles.md` for the six principles R51 operationalizes.

---

### Cross-Artifact (--plugin flag)

Applied when linting an entire plugin rather than individual files.

| Check | Condition | Penalty |
|-------|-----------|---------|
| Broken partial refs | Command references `commands/shared/X.md` that doesn't exist | -20 |
| Broken skill refs | Agent references `plugin:skill` that isn't installed | -20 |
| Missing scripts | Hook references script that doesn't exist | -20 |
| Orphaned files | Agent/command/skill file not referenced by anything | -5 per file |
| Contradictions | Two rules/instructions in same plugin directly contradict each other | -15 per pair |

---

## Score Bands

| Range | Label | Meaning |
|-------|-------|---------|
| 90–100 | Excellent | Production-ready; minor or no issues |
| 80–89 | Good | Solid; one or two non-critical gaps |
| 70–79 | Adequate | Meets threshold; noticeable gaps to address |
| 60–69 | Weak | Below threshold; significant issues |
| <60 | Rewrite | Fundamental problems; recommend rewriting from scratch |

**Default pass threshold:** 70. Configurable in `.claude/nlpm.local.md`.

---

## Calibration Examples

### Example 1: Excellent Agent (95/100)

**Artifact:**
```markdown
---
name: dependency-auditor
description: |
  Audits project dependencies for security vulnerabilities, outdated packages,
  and license compliance issues. Use this agent when checking npm/pip/cargo
  dependencies, reviewing package.json or requirements.txt, or running a
  security audit before release.

  <example>
  Context: Developer preparing for production release
  user: check if any of our dependencies have known CVEs
  assistant: I'll audit your dependencies for security vulnerabilities using
  the package manifest files...
  </example>

  <example>
  Context: CI pipeline running pre-merge checks
  user: /audit-deps
  assistant: Running dependency audit. Scanning package.json and
  package-lock.json for vulnerabilities and license issues...
  </example>
model: sonnet
color: yellow
tools: ["Read", "Glob", "Bash"]
skills: ["nlpm:conventions"]
---

You are a dependency security auditor. Read all package manifests in the
project. For each dependency, check version ranges against known vulnerability
patterns. Report findings in the format below.

## Output Format
### Summary
Total dependencies: N | Vulnerable: N | Outdated: N | License issues: N

### Findings
| Package | Version | Issue | Severity |
|---------|---------|-------|----------|
```

**Score breakdown:**
- Base: 100. Passes: `description` with 3+ specific phrases, 2 `<example>` blocks, `model: sonnet` (analysis-tier), declared tools used, output format defined, read-only (no Write/Edit).
- Minor: `Bash` declared but body doesn't invoke it (one unused tool): **-3**

**Final: 97/100** — Excellent. The single unused-tool penalty costs 3 points; otherwise rubric-clean.

*(For calibration: a 95 example would have zero unused tools and a scope note. The range 90-100 is Excellent regardless of the exact number.)*

---

### Example 2: Rewrite Agent (41/100)

**Artifact:**
```markdown
---
name: code-helper
description: "Helps with code tasks in an appropriate and relevant way as needed."
model: opus
tools: ["Read", "Write", "Edit", "Bash", "Glob", "WebSearch", "WebFetch"]
---

You are a helpful coding assistant. Analyze the code and make appropriate
improvements. Handle edge cases as needed and ensure the output is relevant
to the user's requirements.
```

**Score breakdown:**
- Base: 100
- Zero `<example>` blocks: **-15**
- Description is generic (1 vague phrase, 0 specific phrases): **-15**
- `opus` declared for a routine code-help task (haiku/sonnet appropriate): **-5**
- `tools` declared but too many unused (WebSearch, WebFetch, Glob all declared without body justification): **-10** (judged as 3–4 unused, rounded)
- "appropriate" + "relevant" + "as needed" (vague quantifiers, 2 instances): **-4**
- No output format defined: **-10**

Total penalties: -59

**Final: max(0, 100 - 59) = 41/100** — Rewrite.

*(For calibration: the exact number of unused tools and vague quantifier hits can vary by reviewer. The important thing is that this artifact scores well below 60 — multiple fundamental issues.)*

---

### Example 3: Excellent Rule (92/100)

**Artifact:**
```markdown
---
description: "Always use ${CLAUDE_PLUGIN_ROOT} for intra-plugin file references in hooks and scripts"
paths: ["**/.claude/hooks.json", "**/scripts/*.sh"]
---

**Use `${CLAUDE_PLUGIN_ROOT}` for all file paths within a plugin.**

Because plugins are installed at different locations for different users and
environments, hardcoded absolute paths (e.g. `/Users/alice/.claude/plugins/...`)
break when the plugin is installed by anyone other than the original author.
Using `${CLAUDE_PLUGIN_ROOT}` ensures paths resolve correctly regardless of
install location.

Correct:
```json
"command": "${CLAUDE_PLUGIN_ROOT}/scripts/check.sh"
```

Incorrect:
```json
"command": "/Users/alice/.claude/plugins/cache/my-plugin/1.0.0/scripts/check.sh"
```
```

**Score breakdown:**
- Base: 100. Passes: `description`, bold imperative, rationale, specificity (testable via grep for `/Users/` in hooks.json), `paths` scoping, length, no linter overlap, no vague quantifiers.
- Minor: no reference to related portability rules (env vars in MCP configs, etc.): **-3** (judgment call, not a formal penalty)

**Final: 92/100** — Excellent. The remaining ~5-point gap reflects scope coverage of related portability contexts rather than any rubric violation.

---

### Example 4: Weak Rule (40/100)

**Artifact:**
```markdown
Don't write bad code. Code should be clean and well-organized. Avoid using
outdated patterns. Make sure to handle errors appropriately.
```

**Score breakdown:**
- Base: 100
- Missing frontmatter (no `description` field): **-10**
- No bold imperative opening: **-5**
- No rationale: **-10**
- Not specific or testable ("bad code", "clean", "well-organized" are unmeasurable): **-10**
- "appropriately" (vague quantifier): **-2**
- "well-organized" (vague): **-2**
- Duplicates what every linter/formatter already enforces ("clean code"): **-10**
- Rule is not enforceable by NLPM or any automated tool: **-10** (enforceability)

Total penalties: -59

**Final: max(0, 100 - 59) = 41/100** — Rewrite.

*(Calibrated near 40 as specified. The exact value depends on judgment on "well-organized" as a vague quantifier.)*

---

## Scope Note

This skill covers the NLPM scoring formula, penalty tables, score bands, and calibration examples. It does NOT cover:
- Artifact schemas and valid field values → see `nlpm:conventions` (universal) and the tool-specific overlays `nlpm:conventions-claude`, `nlpm:conventions-codex`, `nlpm:conventions-antigravity` (the latter three created in PR-B; see `analysis/multi-tool-design-2026-05.md`)
- Patterns and anti-patterns catalog → see `nlpm:patterns`
- How to run the score command → see `commands/score.md`

### Multi-tool scoring (PR-B landed 2026-05-25)

nlpm now scores artifacts across three tool ecosystems — Claude Code, Codex CLI, and Antigravity (which absorbs Gemini CLI on 2026-06-18). The tier classification in `agents/scorer.md` separates open-spec (Tier 1), Tier 1.5 open-spec corpora, and per-tool Tier 2 overlays (2-Claude / 2-Codex / 2-Antigravity).

- **Hooks** are scored per tool (Claude / Codex / Antigravity tables above). The three tools' event vocabularies are not 1:1 mappable; no universal translation layer. See `analysis/multi-tool-design-2026-05.md` decision #4.
- **Codex-specific artifacts** scored: `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `.codex/config.toml`, `agents/openai.yaml` sidecars.
- **Antigravity-specific artifacts** scored (advisory-only until spec stabilizes): `gemini-extension.json`, `.gemini/commands/*.toml`, Antigravity hook events.
- **Claude-specific additions** in 2026: `.lsp.json`, `monitors/monitors.json` (validate JSON-parse only until detailed schemas land). New SKILL.md fields documented in `nlpm:conventions-claude`.

### Known False Positive Patterns

The following findings have historically been reported by the scorer despite
having no backing in this rubric. They MUST NOT be penalized:

| Invalid finding | Why it is invalid |
|---|---|
| Missing `namespace:` on skill | Not in the skill schema; `conventions` §5 does not list it |
| Missing inline `hooks:`/`skills:` registration blocks in plugin.json | `conventions` §1 defines these as optional path strings |
| `AskUserQuestion` / `Task` / `WebFetch` flagged as undocumented tool | Built-in per `conventions` §14 |
| Agent missing `skills:` when omission is documented in CLAUDE.md | Intentional architectural choice |
| plugin.json missing `engines:` / `minClaudeVersion:` / `main:` | All optional per `conventions` §1 |
| plugin.json description shorter than sibling marketplace.json description | Desynchronization ≠ defect; only penalize if required field is absent |

When in doubt: if a finding cannot be cited to a specific row in the penalty
tables above, drop it.
