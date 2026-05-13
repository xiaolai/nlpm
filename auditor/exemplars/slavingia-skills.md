---
slug: slavingia-skills
repo: slavingia/skills
audited: 2026-05-13
commit_sha: eb9f57fba03ddb0382ed3bfe6654d3d7df128c70
score: 97
exemplifies:
  - R01
  - R04
  - R05
  - R07
  - R08
---

# Exemplar: slavingia/skills

**Score**: 97/100  |  **Date**: 2026-05-13  |  **Commit**: `eb9f57fba03ddb0382ed3bfe6654d3d7df128c70`

A 10-skill business-advisor collection built around a single book's framework, scoring 97 through tight trigger descriptions, sub-100-line files, explicit workflow cross-references, and pattern-first structure throughout.

## Per-rule evidence

### R04 — Description as trigger

Every skill in the collection packs multiple distinct action phrases into its `description` field, matching real user queries rather than summarizing content. The phrases cover different entry-point situations so Claude routes correctly regardless of how the user phrases the question.

> From `skills/find-community/SKILL.md:3`:
>
> ```
> description: Help identify and evaluate communities to build a minimalist business around. Use when someone is looking for a business idea, trying to find their community, or wondering where to start as an entrepreneur.
> ```

> From `skills/minimalist-review/SKILL.md:3-4`:
>
> ```
> description: Review any business decision, plan, or strategy through the minimalist entrepreneur lens. Use when someone wants a gut-check on a business decision, wants to simplify their approach, or needs to decide between options.
> argument-hint: describe your decision or situation
> ```

> From `skills/processize/SKILL.md:3`:
>
> ```
> description: Turn a product idea into a manual-first process you can start delivering today. Use when you have an idea and want to figure out how to deliver value by hand before writing any code.
> ```

Each description covers 2–3 distinct user states ("looking for a business idea", "trying to find their community", "wondering where to start") rather than collapsing them into one vague phrase. The `minimalist-review` skill also adds `argument-hint`, giving the user an input prompt in `/help` listings.

### R05 — Body length

All 10 SKILL.md files stay well under the 500-line ceiling: the longest (`processize`) is 91 lines; the median is around 75 lines. No skill needed splitting. This matters because each of these files is loaded into context whenever its trigger fires — bloated skills tax every interaction.

> From `skills/first-customers/SKILL.md` (80 lines total) — the full file runs from the frontmatter to the Output section at line 80 with no padding sections, repeated preambles, or appendices:
>
> ```
> ## Output
>
> Help the user create:
> 1. A list of 10 friends/family to pitch this week
> 2. A list of 10 community members to reach out to
> 3. A cold outreach template (personalized, not copy-paste)
> 4. Their initial pricing strategy
> 5. A weekly sales goal and tracking method
> ```

The Output section is the last thing in every skill — no trailing notes or appendices. The discipline of "Output is the last section, then stop" keeps every file bounded.

### R07 — Scope note when related skills exist

The collection covers a linear entrepreneur workflow. Skills that depend on prior steps surface the dependency explicitly with a cross-reference rather than silently assuming the user is at the right stage.

> From `skills/processize/SKILL.md:33-34`:
>
> ```
> If you can't name 10 specific people who have this problem right now?
> If you can't name 10 people, you don't know your community well enough yet. Go back to `/find-community`.
> ```

This is a runtime decision branch: if the user fails the "10 people" check, the skill redirects rather than proceeding on weak footing. The cross-reference is embedded in a conditional ("if you can't…"), which is more useful than a generic "see also" link — it fires only when the redirect is warranted.

### R08 — Patterns over theory

The skills teach what to do in specific situations, not the abstract philosophy behind each principle. Pattern structures include numbered stages, decision tables, and named checklists.

**Three-stage pattern (mvp/SKILL.md:14–29):**

> From `skills/mvp/SKILL.md:14-29`:
>
> ```
> ## The Three Stages
>
> ### Stage 1: Manual (Do it yourself)
> - Solve the problem by hand for each customer
> - You are the product. You are customer service, fulfillment, and engineering
> - Write down every step you take — this becomes your process
> - Example: Before Gumroad automated payouts, Sahil collected PayPal emails and sent payments manually, one by one
>
> ### Stage 2: Processized (Systematize the manual work)
> - Document your process on a piece of paper so anyone could do it
> - If you go on vacation, someone else can take over
> ...
>
> ### Stage 3: Productized (Automate the process)
> - Now automate each task so customers can use your product without you
> - This is when you actually build software or a product
> - Only build what you've already proven works manually
> ```

**Decision table (minimalist-review/SKILL.md:55–65):**

> From `skills/minimalist-review/SKILL.md:55-65`:
>
> ```
> ## Decision Framework
>
> For any decision, evaluate:
>
> | Question | Answer |
> |----------|--------|
> | Does this serve my community/customers? | |
> | Is this the simplest approach? | |
> | Does this improve profitability? | |
> | Is this reversible if it doesn't work? | |
> | Am I spending time or money? | |
> | Have customers asked for this? | |
> | Does this align with my values? | |
> | Will I still want this in a year? | |
> ```

The decision table gives Claude a literal structure to fill in for the user — pattern, not concept. The three-stage model gives a concrete sequencing rule: manual first, then processized, then productized.

### R01 — No vague quantifiers without criteria

Where the skills use numbers, they are grounded in specific evidence. The `first-customers` skill is particularly strong here.

> From `skills/first-customers/SKILL.md:60-62`:
>
> ```
> - **Manual sales = 99% of early growth.** Word of mouth = 99% of later growth.
> - You need far fewer customers than you think. Slack's IPO: 575 customers = 40% of revenue.
> - If your product costs $10/month, you need 200 customers for $2,000/month. At one customer per business day, that's less than a year.
> ```

Each claim is tied to a concrete number or a named real-world example (Slack's IPO). The audit flagged three vague-quantifier violations in the collection (pricing: "typical", "feels natural"; marketing-plan: "Be authentic") — all in skills that score 96, not 98. The 98-scoring skills avoid this pattern entirely.

## Worth adopting

**Pattern: Workflow back-links as stage gates.** Rather than listing skills in sequence in a README, `processize/SKILL.md` embeds the back-link at the decision point where it matters: "If you can't name 10 people … Go back to `/find-community`." This turns cross-references into runtime gates rather than static documentation. Evidence: `skills/processize/SKILL.md:34`. Why it would be a useful rule: R07 says "scope note when related skills exist" but doesn't distinguish a static "see also" from a conditional redirect — the conditional form is strictly more useful and should be the taught pattern.

**Pattern: Cross-cutting advisor skill.** The collection includes one skill (`minimalist-review`) explicitly designed to be applied at any stage, operating as a lens over any decision rather than a step in a sequence. Its description names this role: "Review any business decision, plan, or strategy." Evidence: `skills/minimalist-review/SKILL.md:3`. Why it would be a useful rule: skill collections with a linear workflow benefit from one transverse skill that provides the framework's core judgment — without it, users must remember which stage-specific skill to invoke for a general gut-check question.
