# NLPM Audit: 0xNyk/council-of-high-intelligence
**Date**: 2026-04-06  |  **Artifacts**: 21  |  **Strategy**: batched
**NL Score**: 71/100
**Security**: REVIEW
**Bugs**: 15  |  **Quality Issues**: 19  |  **Security Findings**: 4

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/council-sun-tzu.md | agent | 63 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) + vague quantifiers "appropriate"/"correctly" (-4) |
| agents/council-karpathy.md | agent | 65 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) + vague quantifier "sufficient" (-2) |
| agents/council-ada.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-feynman.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-torvalds.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-meadows.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-lao-tzu.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-socrates.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-musashi.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-munger.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-sutskever.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-aristotle.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-watts.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-aurelius.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-kahneman.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-taleb.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-machiavelli.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| agents/council-rams.md | agent | 67 | Zero `<example>` blocks (-15) + 6 unused declared tools (-18) |
| SKILL.md | skill/command | 85 | Missing `allowed-tools` frontmatter (-5) + no empty-input handling for `/council` with no problem statement (-10) |
| CLAUDE.md | memory | 100 | None |
| .claude-plugin/plugin.json | manifest | 100 | None |

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 1 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks | none found |
| Scripts | `install.sh`, `scripts/convert-agents-opencode.py`, `scripts/detect-providers.sh`, `scripts/gen-star-history.py`, `scripts/council-simulation-checklist.sh` |
| MCP configs | none found |
| Package manifests | none found (no `package.json` / `requirements.txt`) |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | SKILL.md | 314 | `codex exec -c auto_approve=true` | codex_exec dispatch runs with `auto_approve=true` and no read-only/sandbox restriction, unlike the explicit `--mode ask` read-only restriction applied to the cursor_cli seat (SKILL.md:348) a few paragraphs later. A council member is supposed to "only reason," but nothing in this invocation stops the dispatched Codex agent from writing files or running shell commands if it chooses to. |
| 2 | Medium | SKILL.md | 327 | `gemini -m {model} -p ...` (no sandbox flag) | gemini_cli dispatch has no read-only/no-tool-use flag equivalent to cursor_cli's `--mode ask`, so a dispatched Gemini council member is not tooling-restricted to analysis-only the way the cursor_cli seat explicitly is. |
| 3 | Medium | scripts/detect-providers.sh | 102 | `curl -sf ... -H @<(...)` to NVIDIA NIM endpoint | Legitimate reachability check against the NIM catalog endpoint. Recorded for completeness — the credential is passed via process substitution specifically to avoid appearing in `ps` output, which is the correct pattern. No fix needed. |
| 4 | Low | scripts/convert-agents-opencode.py | 22 | `pip3 install --user pyyaml` | The install hint has no version pin, so a future breaking PyYAML release could silently change parsing behavior for anyone following the error message. |

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | agents/council-aristotle.md:14 | `profiles:` declares `exploration-orthogonal`, but SKILL.md:163's canonical 12-member roster for that profile (Socrates, Feynman, Sun Tzu, Machiavelli, Ada, Lao Tzu, Aurelius, Torvalds, Karpathy, Sutskever, Kahneman, Meadows) does not include Aristotle | A user running `--profile exploration-orthogonal` will not get Aristotle per SKILL.md's own selection logic, contradicting what Aristotle's own frontmatter advertises |
| 2 | agents/council-machiavelli.md:11 | `polarity_pairs: ["ada"]` omits `sutskever`, even though council-sutskever.md:11 declares `["karpathy", "machiavelli"]` and SKILL.md:147 documents "Sutskever vs Machiavelli" as a Duo Polarity Pair | The auto-routing hard constraint in SKILL.md STEP 1 Path B rule 1 ("Check the `council.polarity_pairs` field in each member's frontmatter") can silently fail to separate Sutskever and Machiavelli onto different providers when both are on a panel (e.g. `--full` mode) if the check isn't made bidirectional |
| 3 | agents/council-meadows.md:5 | `color: teal` is not in the documented 8-value Claude Code enum (red, blue, green, yellow, purple, orange, pink, cyan) | Color badge may fail to render or silently fall back in the Claude Code UI |
| 4 | agents/council-lao-tzu.md:5 | `color: indigo` — same invalid-enum issue | Same as above |
| 5 | agents/council-socrates.md:5 | `color: white` — same invalid-enum issue | Same as above |
| 6 | agents/council-musashi.md:5 | `color: crimson` — same invalid-enum issue | Same as above |
| 7 | agents/council-munger.md:5 | `color: gold` — same invalid-enum issue | Same as above |
| 8 | agents/council-sutskever.md:5 | `color: ice-blue` — same invalid-enum issue | Same as above |
| 9 | agents/council-aristotle.md:5 | `color: amber` — same invalid-enum issue | Same as above |
| 10 | agents/council-aurelius.md:5 | `color: silver` — same invalid-enum issue | Same as above |
| 11 | agents/council-kahneman.md:5 | `color: coral` — same invalid-enum issue | Same as above |
| 12 | agents/council-taleb.md:5 | `color: black` — same invalid-enum issue | Same as above |
| 13 | agents/council-machiavelli.md:5 | `color: dark-green` — same invalid-enum issue | Same as above |
| 14 | agents/council-rams.md:5 | `color: white-smoke` — same invalid-enum issue | Same as above |
| 15 | SKILL.md | No explicit handling for `/council` invoked with no problem statement | STEP 0's Auto-Triad Selection assumes a problem statement to match against triad keywords; an empty invocation has no documented fallback |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | SKILL.md:314 | codex_exec dispatch has no read-only restriction | Restrict the codex_exec invocation to a non-mutating/read-only mode (or drop `auto_approve=true`) so a "reasoning-only" council member can't silently take write actions, mirroring the `--mode ask` restriction already used for cursor_cli |
| 2 | SKILL.md:327 | gemini_cli dispatch has no read-only restriction | Add an explicit read-only/no-tool-use flag to the gemini invocation, mirroring cursor_cli's `--mode ask` pattern |
| 3 | scripts/convert-agents-opencode.py:22 | Unpinned PyYAML install hint | Pin the suggested install command, e.g. `pip3 install --user "pyyaml>=6.0,<7"` |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/council-ada.md | Zero `<example>` blocks (R09); 6 declared tools never referenced in body — Read, Grep, Glob, Bash, WebSearch, WebFetch (R11) | -33 |
| 2 | agents/council-feynman.md | Same as above | -33 |
| 3 | agents/council-torvalds.md | Same as above | -33 |
| 4 | agents/council-meadows.md | Same as above | -33 |
| 5 | agents/council-lao-tzu.md | Same as above | -33 |
| 6 | agents/council-socrates.md | Same as above | -33 |
| 7 | agents/council-musashi.md | Same as above | -33 |
| 8 | agents/council-karpathy.md | Same as above, plus vague quantifier "sufficient" (R01, line 33) | -35 |
| 9 | agents/council-sun-tzu.md | Same as above, plus vague quantifiers "appropriate" (line 29) and "correctly" (line 36) (R01) | -37 |
| 10 | agents/council-munger.md | Zero `<example>` blocks (R09); 6 unused declared tools (R11) | -33 |
| 11 | agents/council-sutskever.md | Same as above | -33 |
| 12 | agents/council-aristotle.md | Same as above | -33 |
| 13 | agents/council-watts.md | Same as above | -33 |
| 14 | agents/council-aurelius.md | Same as above | -33 |
| 15 | agents/council-kahneman.md | Same as above | -33 |
| 16 | agents/council-taleb.md | Same as above | -33 |
| 17 | agents/council-machiavelli.md | Same as above | -33 |
| 18 | agents/council-rams.md | Same as above | -33 |
| 19 | SKILL.md | Missing `allowed-tools` frontmatter field despite the body instructing extensive Bash usage | -5 |

## Cross-Component

- The Sutskever/Machiavelli polarity-pair asymmetry and the Aristotle profile-roster mismatch (both listed under Bugs above) are the two genuine cross-file contradictions found between `agents/*.md` frontmatter and `SKILL.md`'s own tables.
- All 18 agent files referenced by name in SKILL.md's "18 Council Members" table, the triad tables, and the profile member lists resolve to an actual `agents/council-*.md` file — no orphaned or missing member references.
- `plugin.json` (1.2.0), `marketplace.json` (1.2.0), and `CHANGELOG.md`'s latest entry (`[1.2.0] - 2026-07-04`) are in sync — no version drift.
- `skills/council/SKILL.md` is a symlink to `../../SKILL.md` and resolves correctly — the marketplace plugin-install path for the skill is intact (verified by resolving the symlink directly; not a bug, despite the top-level `SKILL.md` living outside the conventional `skills/<name>/SKILL.md` directory structure on its own).
- `CLAUDE.md` documents project architecture directly rather than importing an `AGENTS.md` (no `AGENTS.md` exists in this repo). This is an informational deviation from nlpm's own "AGENTS.md as canonical memory" convention, not a scored penalty under the rubric applied here.

## Recommendation

**REVIEW** — submit PRs for the 15 NL bugs (the Aristotle/exploration-orthogonal roster mismatch, the Machiavelli/Sutskever polarity asymmetry, the 12 invalid `color` enum values, and the SKILL.md empty-input gap) and for the Low-severity PyYAML pin. Flag the two Medium security findings (codex_exec/gemini_cli lacking a read-only restriction) in the audit issue for maintainer awareness rather than opening security PRs directly, since they concern an architectural trust boundary (how much autonomy a "reasoning-only" council member actually has) that the maintainer should weigh in on before a fix is prescribed.
