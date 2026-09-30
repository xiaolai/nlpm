# NLPM Scoring — Antigravity / Gemini Tables

Penalty tables for Antigravity and Gemini-lineage (Tier 2-Antigravity) artifacts. Part of the `nlpm:scoring` rubric: the formula, the shared tables (including the universal Hooks checks), the score bands and the false-positive list are in `../SKILL.md`. These rows carry the same weight as the rows there, and each table states its own advisory status.

---

### Hooks (Antigravity / Gemini lineage — Tier 2-Antigravity only) — ADVISORY

Authoritative event list: `nlpm:conventions-antigravity` §5. **All Antigravity-specific hook scoring is advisory-only** (confidence:low) until the Antigravity 2.0 spec stabilizes — see `analysis/multi-tool-design-2026-05.md` decision #3.

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R27 | Event names valid (Gemini lineage) | Uses unrecognized event name — confirmed events: `SessionStart`, `BeforeAgent`, `BeforeModel`, `BeforeToolSelection`, `BeforeTool`, `AfterTool`, `AfterModel`, `AfterAgent`, `SessionEnd`, `Notification`, `PreCompress` | -10 (advisory) |
| R27 | Case correct (Gemini lineage) | Event name has wrong case | -5 (advisory) |

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
