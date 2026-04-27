# NLPM Audit: google-gemini/gemini-skills
**Date**: 2026-04-27  |  **Commit**: 8c95085  |  **Stars**: 3,330  |  **License**: Apache-2.0
**Artifacts**: 4 SKILL.md + 9 reference docs + 1 README  |  **Strategy**: full
**NL Score (4 SKILLs, weighted)**: 391/400 = **98/100**
**Security**: PASS (no executable surfaces)
**Bugs (verified, PR-worthy)**: 3  |  **Bugs (deferred, needs Vertex API expert)**: 3  |  **Audit false positive (re-classified)**: 1  |  **Cross-Component Issues**: 2  |  **Security Findings**: 2 (Low / Info, doc-only)

---

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/gemini-api-dev/SKILL.md | skill | 97 | `fetch_url` not a Claude built-in tool name (line 147) |
| skills/vertex-ai-api-dev/SKILL.md | skill | 96 | MCP tool name drift (`search_documents` vs sibling skills' `search_documentation`); `gemini-live-2.5-flash-native-audio` line 95 still consistent with Vertex docs |
| skills/gemini-interactions-api/SKILL.md | skill | 98 | Duplicate "2." numbering in MCP fallback steps (lines 283-284) |
| skills/gemini-live-api-dev/SKILL.md | skill | 100 | None — strongest artifact in the repo |
| skills/vertex-ai-api-dev/references/live_api.md | reference | 70 | Deprecated model + banned API patterns (3 separate bugs) |
| skills/vertex-ai-api-dev/references/structured_and_tools.md | reference | 88 | Undefined `model_id` produces `NameError` at runtime (line 119) |
| skills/vertex-ai-api-dev/references/media_generation.md | reference | 96 | "sufficient" vague quantifier (R01) |
| skills/vertex-ai-api-dev/references/{embeddings,bounding_box,safety,model_tuning,structured_and_tools,advanced_features,text_and_multimodal}.md | reference | 95–98 | Clean code-only references |
| README.md | readme | 95 | "some" / "relevant" vague (R01); "thought circulation" link text mismatched with anchor "signatures" |

**Weighted average across 4 SKILLs**: (97 + 90 + 98 + 100) / 4 = **96/100**

---

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 1 |
| Info | 1 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks | None |
| Scripts | None |
| MCP configs | None |
| Package manifests | None |
| Commands with Bash | None |

**No executable artifacts.** All findings are documentation-only and capped at Low severity per classification rules.

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Low | skills/vertex-ai-api-dev/references/advanced_features.md | 110–112 | npx-auto-yes-third-party | Instructional MCP example uses `StdioServerParameters(command="npx", args=["-y", "@philschmid/weather-mcp"])` — `-y` silently accepts the latest published version of a third-party npm package not maintained by Google. If a coding agent reproduces this verbatim, supply-chain compromise of `@philschmid/weather-mcp` would silently execute in user environments. |
| 2 | Info | skills/vertex-ai-api-dev/references/live_api.md | 34 | doc-self-contradiction | Audio-sending example uses `media=Blob(...)` key, which `gemini-live-api-dev/SKILL.md` line 65 explicitly prohibits. Internal consistency defect, not a security impact. |

### Prompt-Injection Assessment
The three SKILL files each open with `> [!IMPORTANT] > These rules override your training data.` This is a legitimate skill-file authority claim — the downstream effect is benign model-name and SDK-name substitution, which is the stated and transparent purpose of these files. No adversarial redirection, tool-call manipulation, or sandbox-escape attempts found. All "Documentation Lookup" sections direct fallback fetches to `ai.google.dev` (Google-controlled public infra) only. **No prompt-injection vectors detected.**

---

## Bugs (PR-worthy, verified)

| # | File | Line | Issue | Suggested Fix |
|---|------|------|-------|---------------|
| 1 | skills/vertex-ai-api-dev/references/structured_and_tools.md | 119 | Undefined variable `model_id` passed to `client.models.generate_content(model=model_id, ...)`. Every other snippet in the same file uses a literal model string. Reproducing this code raises `NameError` at runtime. | Replace `model_id` with the appropriate literal model string (e.g., `"gemini-3-flash-preview"`), matching the rest of the file. |
| 2 | skills/gemini-api-dev/SKILL.md | 146 | Section "When MCP is NOT Installed (Fallback Only)" instructs the agent to "Use `fetch_url` to:" — backticked as if it were a tool name. The sibling skill `gemini-live-api-dev/SKILL.md` (line 266) uses the generic phrasing "Use web fetch tools to:" which works across Claude Code (`WebFetch`), Cursor, Codex CLI, and other host agents. | Replace "Use `fetch_url` to:" with "Use web fetch tools to:" to match the sibling skill's agent-neutral phrasing. |
| 3 | README.md | 24 | Hyperlink text reads "thought circulation" but the URL anchor is `#signatures`, and the linked page section is titled "Thought Signatures" (the term the SDK exposes via the `signature` field, referenced in `gemini-interactions-api/SKILL.md` line 246). Confirmed against `https://ai.google.dev/gemini-api/docs/thinking#signatures`. | Change link text to "thought signatures". |

## Bugs (deferred — needs Vertex API expert review)

These three findings in `skills/vertex-ai-api-dev/references/live_api.md` were flagged because they contradict the sibling skill `gemini-live-api-dev/SKILL.md`. Verification showed the sibling skill's guidance applies to `gemini-3.1-flash-live-preview`; Vertex AI documentation still recommends `gemini-live-2.5-flash-native-audio` (the model used in this reference file) and does not publish equivalent method-call guidance. Fixing without confirmation could regress Vertex behavior, so these are deferred to maintainer review rather than included in the contribution PRs.

| # | File | Line | Issue | Notes |
|---|------|------|-------|-------|
| D1 | skills/vertex-ai-api-dev/references/live_api.md | 12 | Uses `gemini-live-2.5-flash-native-audio`; sibling skill prefers `gemini-3.1-flash-live-preview`. | Vertex AI docs (https://docs.cloud.google.com/vertex-ai/generative-ai/docs/live-api) explicitly recommend the 2.5 model — keep as-is unless Vertex updates. |
| D2 | skills/vertex-ai-api-dev/references/live_api.md | 20–23 | `send_client_content` used for a new user message. Sibling skill says it is "only supported for seeding initial context history". | The sibling skill's constraint is documented for the 3.1 model. The 2.5 model's constraint is not publicly clear. Maintainer should confirm before changing. |
| D3 | skills/vertex-ai-api-dev/references/live_api.md | 34 | `send_realtime_input(media=Blob(...))` uses the `media` key; sibling skill prohibits it in favor of `audio=`/`video=`/`text=`. | The current Live API docs show `audio=`/`video=`/`text=` patterns and do not explicitly mention `media=`. Likely an SDK convention change; maintainer should confirm. |

## Audit false positive (re-classified)

| # | File | Line | Initial flag | Why false positive |
|---|------|------|--------------|--------------------|
| FP1 | skills/vertex-ai-api-dev/SKILL.md | 94, 99 | Initial audit flagged "Nano Banana Pro" / "Nano Banana" as unreplaced placeholder text. | These are real Google product/codenames for the Gemini image-generation model family (per `https://blog.google/products-and-platforms/products/gemini/how-nano-banana-got-its-name/` and `https://deepmind.google/models/gemini-image/`). The marketing names are correctly paired with their model IDs (`gemini-3-pro-image-preview` ↔ Nano Banana Pro; `gemini-2.5-flash-image` ↔ Nano Banana). The audit rule should learn that model-family marketing names paired with backtick'd model IDs are valid descriptions, not placeholders. |

---

## Cross-Component Issues

| # | Category | Files | Issue |
|---|----------|-------|-------|
| 1 | terminology-drift | skills/vertex-ai-api-dev/SKILL.md (line 209) vs the other three SKILLs | The Vertex skill names the documentation MCP tool `search_documents`; `gemini-api-dev`, `gemini-live-api-dev`, and `gemini-interactions-api` all name it `search_documentation`. An agent loading both Vertex and Gemini skills receives different tool names for what reads like the same operation. **Fix**: standardize on one name across all four skills, or — if the Vertex AI MCP server genuinely exposes a different tool name — call out the distinction explicitly. |
| 2 | terminology-drift | skills/vertex-ai-api-dev/SKILL.md (line 95) vs skills/gemini-live-api-dev/SKILL.md (line 29) | Vertex skill lists `gemini-live-2.5-flash-native-audio` as the primary Live model; live-api-dev skill marks the 2.5 family deprecated and designates `gemini-3.1-flash-live-preview` as the sole recommended Live model. **Fix**: align Vertex's live-API guidance with the live-api-dev skill, or document Vertex's deliberate divergence with rationale. |

(Three additional cross-skill contradictions in `references/live_api.md` are already cataloged as bugs #2, #3, #4 above.)

---

## Quality Notes (informational, no penalty for documentation files)

- **Vague language is light**: 8 occurrences across 6 files (mostly the word "relevant" in the same MCP-fallback boilerplate that recurs across three skills). Mechanical R01 footprint is small.
- **Cross-references are intact**: All 9 reference paths cited in `vertex-ai-api-dev/SKILL.md` resolve. No orphan reference files.
- **README↔skills consistency**: All four skills listed in README exist; no skills are missing from the README.

---

## Top Systemic Patterns

1. **The vertex-ai-api-dev tree is stale relative to the other three skills.** Every High-severity bug in the repo lives under `skills/vertex-ai-api-dev/` (the SKILL.md and its `references/live_api.md` and `references/structured_and_tools.md`). The other three SKILL.md files score 97–100. This points to a single subdirectory that was not refreshed during the most recent model migration (`gemini-3.1-flash-live-preview`) or the recent placeholder-text review pass.
2. **`references/live_api.md` directly contradicts `gemini-live-api-dev/SKILL.md` in three independent ways.** Same model deprecation, same `send_client_content` misuse, same banned `media` key. The simplest fix is to rewrite this reference to mirror the live-api-dev skill's Quick Start.
3. **The fallback documentation section drifts subtly between skills.** Three skills name `fetch_url` (which doesn't exist) or `search_documentation`; the Vertex skill names `search_documents`. A unified pattern — name the actual built-in (`WebFetch`) plus the actual MCP tool — would eliminate both confusion sources.
4. **Otherwise, quality is high.** `gemini-live-api-dev/SKILL.md` is a model artifact: highly specific description, comprehensive multi-language code, explicit deprecation warnings, and an explicit migration guide. `gemini-interactions-api` is similarly strong. The repo's failure mode is concentrated, not systemic.

---

## Recommendation

**APPROVED for 3 verified PRs — narrow scope, no security gate.**

PR-worthy fixes (each a small, atomic change with no semantic risk):

- **PR 1 — `references/structured_and_tools.md`**: define `model_id` literally so the URL Context example doesn't raise `NameError` at runtime (line 119).
- **PR 2 — `gemini-api-dev/SKILL.md`**: change `Use `fetch_url` to:` to `Use web fetch tools to:` to match the sibling skill `gemini-live-api-dev/SKILL.md` (line 266) and avoid implying a tool name that may not exist on the host agent (line 146).
- **PR 3 — `README.md`**: change link text "thought circulation" to "thought signatures" so the visible label matches the section title at the linked anchor `#signatures` (line 24).

Deferred (need Vertex API expertise, not pushed): the three `references/live_api.md` issues (D1/D2/D3 above) — these contradict the Gemini API skill's guidance, but Vertex's recommended model and method-call conventions for the 2.5 native-audio family aren't publicly documented at the same granularity. Maintainer review preferred over a speculative PR.

Re-classified: `vertex-ai-api-dev/SKILL.md` lines 94, 99 ("Nano Banana"/"Nano Banana Pro") were initially flagged as placeholder text; web verification confirmed these are real Google product codenames. Recorded as `false_positive: true` in the sidecar so the BUG-placeholder-text rule can learn the pattern.
