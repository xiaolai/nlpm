---
slug: coreyhaines31-marketingskills
repo: coreyhaines31/marketingskills
audited: 2026-05-13
commit_sha: 906c2fb28e471c5b1d149d4159ec5ddb40b7c364
score: 96
exemplifies:
  - R01
  - R04
  - R06
  - R07
  - R08
---

# Exemplar: coreyhaines31/marketingskills

**Score**: 96/100  |  **Date**: 2026-05-13  |  **Commit**: `906c2fb`

A 35-skill marketing collection (ad creative, SEO, CRO, email, research) that treats every description as a trigger list, scopes every skill with "for X, see Y" boundaries, and enforces cross-skill context sharing via a dedicated context-anchor skill checked at the top of every body.

## Per-rule evidence

### R04 — Description as trigger

R04 requires 3+ specific action phrases matching real user queries. Every skill in this collection packs 8–15 trigger phrases covering both explicit task names ("RSA headlines," "SEO audit") and informal user phrasing ("write me some ads," "I don't know what to write").

> From `skills/ad-creative/SKILL.md:3`:
>
> ```
> When the user wants to generate, iterate, or scale ad creative — headlines, descriptions,
> primary text, or full ad variations — for any paid advertising platform. Also use when
> the user mentions 'ad copy variations,' 'ad creative,' 'generate headlines,' 'RSA headlines,'
> 'bulk ad copy,' 'ad iterations,' 'creative testing,' 'ad performance optimization,'
> 'write me some ads,' 'Facebook ad copy,' 'Google ad headlines,' 'LinkedIn ad text,'
> or 'I need more ad variations.' Use this whenever someone needs to produce ad copy at
> scale or iterate on existing ads. For campaign strategy and targeting, see paid-ads.
> For landing page copy, see copywriting.
> ```

What makes this exemplary rather than adequate: it pairs platform-specific terms with intent-phrasing so the trigger matches both precise and imprecise user language. The "Use this whenever someone needs to…" catch-all closes the gap between the enumerated phrases and any formulation the user didn't think to list.

---

### R07 — Scope note when related skills exist

R07 requires "Covers X. For Y, see [[other-skill]]." when sibling skills exist — otherwise the model can't choose between overlapping options. This collection puts scope boundaries in both the description (trigger-time routing) and a `## Related Skills` section (mid-task handoffs).

> From `skills/copywriting/SKILL.md:3` (description field):
>
> ```
> ...Use this whenever someone is working on website text that needs to persuade or convert.
> For email copy, see email-sequence. For popup copy, see popup-cro.
> For editing existing copy, see copy-editing.
> ```

> From `skills/seo-audit/SKILL.md:3` (description field):
>
> ```
> ...For building pages at scale to target keywords, see programmatic-seo.
> For adding structured data, see schema-markup.
> For AI search optimization, see ai-seo.
> ```

The scope note appears twice in every skill: in the description (stops the wrong skill from loading) and in the `## Related Skills` table at the bottom (enables a handoff after the current skill has run). Double placement means routing works whether the user invokes the skill by name or arrives mid-task.

---

### R06 — Code examples must be runnable

R06 requires real syntax, not pseudocode. `ad-creative` ships annotated output blocks with literal character counts and a bash workflow using actual CLI tools from the repo's `tools/clis/` directory.

> From `skills/ad-creative/SKILL.md:253–265`:
>
> ```
> ## Angle: [Pain Point — Manual Reporting]
>
> ### Headlines (30 char max)
> 1. "Stop Building Reports by Hand" (29)
> 2. "Automate Your Weekly Reports" (28)
> 3. "Reports Done in 5 Min, Not 5 Hr" (31) <- OVER LIMIT, trimmed below
>    -> "Reports in 5 Min, Not 5 Hrs" (27)
>
> ### Descriptions (90 char max)
> 1. "Marketing teams save 10+ hours/week with automated reporting. Start free." (73)
> 2. "Connect your data sources once. Get automated reports forever. No code required." (80)
> ```

> From `skills/ad-creative/SKILL.md:344–352`:
>
> ```bash
> # 1. Pull recent ad performance
> node tools/clis/google-ads.js reports get --type ad_performance --date-range last_30_days
>
> # 2. Analyze output (identify top/bottom performers)
> # 3. Feed winning patterns into this skill
> # 4. Generate new variations
> # 5. Upload to platform
> ```

The output example is demonstrably executable: character counts are correct, the over-limit flag is shown inline with its trim, and the bash command references a real file in `tools/clis/` that ships with the repo. A model following this example can produce output the platform will accept without guessing at limits.

---

### R08 — Patterns over theory

R08 requires teaching what to do in specific situations, not abstract concepts. The most striking R08 evidence is a cross-collection operational pattern: every skill body opens with an identical "Check for product marketing context first" block before any task-specific instructions.

> From `skills/ad-creative/SKILL.md:14–15` (identical in all 35 skills):
>
> ```
> **Check for product marketing context first:**
> If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md`
> in older setups), read it before asking questions. Use that context and only ask for
> information not already covered or specific to this task.
> ```

Rather than "gather context about the user's product" (theory), each skill gives the model a concrete file path to check (pattern), with a fallback path for legacy setups and an explicit decision rule ("only ask for information not already covered"). The audit confirmed 100% adoption across all 35 skills.

---

### R01 — No vague quantifiers without criteria

R01 penalizes words like "appropriate," "sufficient," or "adequate" without measurable criteria. `seo-audit` replaces vague performance guidance with pass/fail thresholds, and `copywriting` demonstrates the contrast inline as a teaching example.

> From `skills/seo-audit/SKILL.md:112–115`:
>
> ```
> **Core Web Vitals**
> - LCP (Largest Contentful Paint): < 2.5s
> - INP (Interaction to Next Paint): < 200ms
> - CLS (Cumulative Layout Shift): < 0.1
> ```

> From `skills/copywriting/SKILL.md:49–51`:
>
> ```
> **Specificity Over Vagueness**
> - Vague: "Save time on your workflow"
> - Specific: "Cut your weekly reporting from 4 hours to 15 minutes"
> ```

The Core Web Vitals section is the clearest compliance example: Google's pass/fail thresholds are stated directly so the model can produce a verdict rather than an impression. The copywriting contrast example teaches R01 compliance inside the domain content itself — a form of self-documenting specificity.

---

## Worth adopting

**Pattern: Shared context anchor.** Evidence: `skills/product-marketing-context/SKILL.md` is a dedicated skill whose output (`.agents/product-marketing-context.md`) is consumed by all 35 sibling skills. Every skill checks that path before gathering input. Why it would be a useful rule: a collections-level pattern that designates one skill as the context provider eliminates redundant setup questions across sessions without requiring a custom hook. Candidate rule: "**Designate a context-anchor skill in multi-skill collections.** One skill writes shared project state to a predictable path (e.g., `.agents/<context>.md`). All sibling skills read that path before gathering context. Without it, the model repeats the same setup questions on every invocation, and context gathered in one skill session is invisible to the next."
