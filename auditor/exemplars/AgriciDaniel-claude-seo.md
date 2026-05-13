---
slug: AgriciDaniel-claude-seo
repo: AgriciDaniel/claude-seo
audited: 2026-05-13
commit_sha: HEAD
score: 94
exemplifies:
  - R04
  - R05
  - R07
  - R08
  - R12
  - R13
  - R30
---

# Exemplar: AgriciDaniel/claude-seo

**Score**: 94/100  |  **Date**: 2026-05-13  |  **Commit**: `HEAD`

A 25-skill, 18-agent SEO plugin where every skill file scored 100/100, demonstrating that a large skills collection can hold the line on description quality, body length, and scope discipline simultaneously.

## Per-rule evidence

### R04 — Description as trigger

The orchestrator skill packs two distinct trigger strategies into a single description: an enumerated sub-task list and an explicit "Triggers on:" suffix with 13 named keywords. This eliminates the ambiguity of "what does this skill cover?" before the body is ever read.

> Real quote from `skills/seo/SKILL.md:3-3`:
>
> ```
> description: "Comprehensive SEO analysis for any website or business type. Full site audits, single-page analysis, technical SEO (crawlability, indexability, Core Web Vitals with INP), schema markup, content quality (E-E-A-T), image optimization, sitemap analysis, and GEO for AI Overviews/ChatGPT/Perplexity. Industry detection for SaaS, e-commerce, local, publishers, agencies. Triggers on: SEO, audit, schema, Core Web Vitals, sitemap, E-E-A-T, AI Overviews, GEO, technical SEO, content quality, page speed, structured data."
> ```

The sub-skill descriptions follow the same pattern and add explicit "Use when user says…" phrases:

> Real quote from `skills/seo-audit/SKILL.md:3-3`:
>
> ```
> description: "Full website SEO audit with parallel subagent delegation. Crawls up to 500 pages, detects business type, delegates to up to 15 specialists (8 always + 7 conditional), generates health score. Use when user says audit, full SEO check, analyze my site, or website health check."
> ```

The description closes with four exact user-phrasing matches — not paraphrases, not categories — making it usable as a string-matching fallback if semantic routing fails.

---

### R05 — Body length

All 25 skill files scored 100, and the CLAUDE.md encodes the 500-line rule as a hard development constraint rather than an informal guideline, making it enforceable during code review.

> Real quote from `CLAUDE.md:157`:
>
> ```
> - Keep SKILL.md files under 500 lines / 5000 tokens
> - Reference files should be focused and under 200 lines
> ```

The pattern that makes this tractable at scale: detail that doesn't belong in the skill body is pushed into `references/` files loaded on-demand (see R07). The seo-technical skill covers 9 audit categories, a CWV threshold table, and an AI crawler management table while staying well under the limit by deferring hreflang specifics to the hreflang sub-skill and keeping each category's checklist to bullet points rather than prose.

---

### R07 — Scope note when related skills exist

The agent definition for `seo-technical` shows the minimal correct form of a cross-skill scope note: one sentence, explicit skill name, actionable condition.

> Real quote from `agents/seo-technical.md:28`:
>
> ```
> ## Cross-Skill Delegation
>
> - For detailed hreflang validation, defer to the `seo-hreflang` sub-skill.
> ```

The orchestrator takes this further with a `references/` system that declares which files exist and when to load them, preventing the skill from bloating its own body with material needed only for specific sub-commands:

> Real quote from `skills/seo/SKILL.md:142-148`:
>
> ```
> ## Reference Files
>
> Load these on-demand as needed (do NOT load all at startup):
> - `references/cwv-thresholds.md`: Current Core Web Vitals thresholds and measurement details
> - `references/schema-types.md`: All supported schema types with deprecation status
> - `references/eeat-framework.md`: E-E-A-T evaluation criteria (Sept 2025 QRG update)
> - `references/quality-gates.md`: Content length minimums, uniqueness thresholds
> - `references/local-seo-signals.md`: Local ranking factors, review benchmarks, citation tiers, GBP status
> - `references/local-schema-types.md`: LocalBusiness subtypes, industry-specific schema and citation sources
> ```

The explicit "do NOT load all at startup" instruction prevents the common failure mode where a skill author adds reference files but forgets to gate their loading.

---

### R08 — Patterns over theory

The industry detection block gives Claude concrete signal patterns — URL path fragments, page-level copy, and HTML elements — rather than abstract category descriptions. Each entry is actionable without inference.

> Real quote from `skills/seo/SKILL.md:79-84`:
>
> ```
> Detect business type from homepage signals:
> - **SaaS**: pricing page, /features, /integrations, /docs, "free trial", "sign up"
> - **Local Service**: phone number, address, service area, "serving [city]", Google Maps embed --> auto-suggest `/seo local` for deeper analysis
> - **E-commerce**: /products, /collections, /cart, "add to cart", product schema
> - **Publisher**: /blog, /articles, /topics, article schema, author pages, publication dates
> - **Agency**: /case-studies, /portfolio, /industries, "our work", client logos
> ```

Each bullet names 4–5 independent signals, so the classifier degrades gracefully when a signal is absent. Contrast this with the anti-pattern: "Detect if the site is a SaaS business" — which is theory without operationalization.

---

### R12 — Output format defined in body

The `seo-technical` agent specifies its output structure in three levels: named sections, the data type per section, and the priority ordering schema within each section.

> Real quote from `agents/seo-technical.md:37-43`:
>
> ```
> ## Output Format
>
> Provide a structured report with:
> - Pass/fail status per category
> - Technical score (0-100)
> - Prioritized issues (Critical → High → Medium → Low)
> - Specific recommendations with implementation details
> ```

The audit skill amplifies this with a full report template that names every section heading and its expected content, so the assembled multi-agent report has a predictable structure across runs.

---

### R13 — System prompt structure: mission → steps → boundaries → format

`agents/seo-technical.md` follows the canonical four-part structure. The mission occupies the first sentence. Seven numbered steps define the procedure. A cross-skill delegation block sets the boundary. An output format section closes the body.

> Real quote from `agents/seo-technical.md:9-17`:
>
> ```
> You are a Technical SEO specialist. When given a URL or set of URLs:
>
> 1. Fetch the page(s) and analyze HTML source
> 2. Check robots.txt and sitemap availability
> 3. Analyze meta tags, canonical tags, and security headers
> 4. Evaluate URL structure and redirect chains
> 5. Assess mobile-friendliness from HTML/CSS analysis
> 6. Flag potential Core Web Vitals issues from source inspection
> 7. Check JavaScript rendering requirements
> ```

The mission clause — "When given a URL or set of URLs" — is a conditional trigger, not a blanket invitation, which tightens activation scope. The numbered steps prevent step-skipping under context pressure.

---

### R30 — Use `${CLAUDE_PLUGIN_ROOT}` for paths

The hook configuration uses `${CLAUDE_PLUGIN_ROOT}` for the script path rather than a relative or absolute path, making it portable across machines and install locations.

> Real quote from `hooks/hooks.json:9`:
>
> ```json
> "command": "python \"${CLAUDE_PLUGIN_ROOT}/hooks/validate-schema.py\" \"$FILE_PATH\""
> ```

This also illustrates R32 correctly: the hook fires on `PostToolUse` (advisory), not `PreToolUse` (blocking). Schema validation runs after writes complete and reports issues rather than aborting the write.

---

## Worth adopting

**Pattern: Explicit trigger suffix.** The description for `seo/SKILL.md` ends with `Triggers on: SEO, audit, schema, Core Web Vitals, sitemap, E-E-A-T, ...` — a machine-readable trigger list separate from the prose summary. Evidence: `skills/seo/SKILL.md:3`. Why it would be a useful rule: separating the human-readable purpose sentence from the match-phrase list makes it easier to audit coverage and add new triggers without restructuring the description.

**Pattern: Gated reference loading.** The `references/` directory pattern (load sub-files on-demand with explicit "do NOT load all at startup" instruction) keeps skill bodies under 500 lines even in large domains without sacrificing knowledge depth. Evidence: `skills/seo/SKILL.md:142-156`, `skills/seo-google/SKILL.md`. Why it would be a useful rule: the current R05 penalizes long bodies but does not prescribe the split strategy; naming the `references/` pattern would give authors a clear model to follow.
