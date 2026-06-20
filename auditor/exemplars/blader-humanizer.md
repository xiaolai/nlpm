---
slug: blader-humanizer
repo: blader/humanizer
audited: 2026-06-20
commit_sha: 9600f2b7241cb4eed6ad803abee5ea01d67fe8e4
score: 98
exemplifies:
  - R01
  - R04
  - R06
  - R08
---

# Exemplar: blader/humanizer

**Score**: 98/100  |  **Date**: 2026-06-20  |  **Commit**: `9600f2b7241cb4eed6ad803abee5ea01d67fe8e4`

A single-file Claude Code / OpenCode skill for removing AI writing patterns; notable for anchoring every instruction in a named, quoted-evidence pattern rather than abstract editorial theory.

## Per-rule evidence

### R04 — Description as trigger

The frontmatter `description` field packs 10 specific pattern names into 4 lines, each matching a real user query ("em dash overuse", "rule of three", "passive voice"). A user typing "remove AI writing patterns" or "fix promotional language" gets an exact keyword hit.

> Real quote from `SKILL.md:4-10` (YAML frontmatter):
>
> ```yaml
> description: |
>   Remove signs of AI-generated writing from text. Use when editing or reviewing
>   text to make it sound more natural and human-written. Based on Wikipedia's
>   comprehensive "Signs of AI writing" guide. Detects and fixes patterns including:
>   inflated symbolism, promotional language, superficial -ing analyses, vague
>   attributions, em dash overuse, rule of three, AI vocabulary words, passive
>   voice, negative parallelisms, and filler phrases.
> ```

What makes this good rather than mediocre: the description names 10 distinct detectable phenomena in 4 lines, all of which appear verbatim as section headings in the body. The description is a surface-level index of the body, making it a reliable trigger rather than a marketing tagline.

### R06 — Runnable examples

Every one of the 33 patterns has a self-contained Before/After pair showing real prose (not pseudocode). The "Full Example" at lines 571-614 extends this to a four-stage walkthrough: original AI-sounding text → draft rewrite → self-critique → final rewrite. The self-critique stage is itself quoted evidence of the process working.

> Real quote from `SKILL.md:588-613` (the four-stage example, abbreviated to key stages):
>
> ```
> **Draft rewrite:**
> > AI coding assistants speed up some tasks. In a 2024 study by Google, developers
> > using Codex completed simple functions 55% faster than a control group...
>
> **What makes the below so obviously AI generated?**
> - The rhythm is still a bit too tidy (clean contrasts, evenly paced paragraphs).
> - The named people and study citations can read like plausible-but-made-up placeholders...
> - The closer leans a touch slogan-y ("If you do not have tests...")
>
> **Now make it not obviously AI generated.**
> > AI coding assistants can make you faster at the boring parts. Not everything.
> > Definitely not architecture.
> ```

This beats the minimum R06 bar (two examples) by a significant margin: 33 pattern-specific pairs plus one full end-to-end example that shows the agent interrogating its own intermediate output. The self-critique step demonstrates the agent following its own three-pass process, not just showing an idealized final result.

### R08 — Patterns over theory

The body has 33 named, numbered patterns (CONTENT, LANGUAGE, STYLE, COMMUNICATION, FILLER sections), each structured as: **Words to watch** → **Problem** (one sentence) → **Before** → **After**. There is no abstract "AI writing is bad because" preamble; the skill goes straight into evidence-backed specifics.

> Real quote from `SKILL.md:90-101` (Pattern 1, representative):
>
> ```
> ### 1. Undue Emphasis on Significance, Legacy, and Broader Trends
>
> **Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/
> crucial/pivotal/key role/moment, underscores/highlights its importance/significance,
> reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the,
> setting the stage for, marking/shaping the, represents/marks a shift, key turning
> point, evolving landscape, focal point, indelible mark, deeply rooted
>
> **Problem:** LLM writing puffs up importance by adding statements about how arbitrary
> aspects represent or contribute to a broader topic.
>
> **Before:**
> > The Statistical Institute of Catalonia was officially established in 1989,
> > marking a pivotal moment in the evolution of regional statistics in Spain...
>
> **After:**
> > The Statistical Institute of Catalonia was established in 1989 to collect and
> > publish regional statistics independently from Spain's national statistics office.
> ```

Each pattern is a self-contained decision rule: given input matching the "words to watch" list, apply the transformation shown. No pattern asks the agent to make an abstract judgment about "quality" without operationalizing it. Compare to a weaker approach that would say "avoid inflated language" without naming the trigger words.

### R01 — No vague quantifiers without criteria

Throughout 621 lines, vague quantifiers almost never appear in instructional prose. Where the skill says "enough", it immediately operationalizes: "the final rewrite contains no em dashes (—) or en dashes (–)" is a hard constraint, not a suggestion. The audit caught a single instance at line 79 ("Let some mess in"), docking 2 points.

> Real quote from `SKILL.md:261-262` (Pattern 14):
>
> ```
> **Rule:** The final rewrite contains no em dashes (—) or en dashes (–). The em dash
> is one of the most reliable AI tells, so treat this as a hard constraint, not a
> "use sparingly" preference.
> ```

> Real quote from `SKILL.md:275`:
>
> ```
> Before returning the final rewrite, scan it for `—` and `–`. Any hit means the
> draft isn't done.
> ```

What separates this from a mediocre example: the em-dash rule explicitly closes the loophole of "use sparingly" by naming it and rejecting it, then provides a verifiable exit condition (scan for the characters; any hit = not done). The agent cannot rationalize an exception.

## Worth adopting

**Pattern: False-positive guardrail section.** Evidence: `SKILL.md:523-555`, "DETECTION GUIDANCE / What NOT to flag". Why it would be a useful rule: Any pattern-detection skill that lists things to detect should also list what not to flag — real-world patterns that superficially resemble the targets. The section prevents the agent from over-editing legitimate human prose. Candidate rule: "**Include a false-positive list in any detection skill.** For every class of patterns the skill hunts, enumerate at least 3 surface-similar patterns that are not violations. Without this, the agent applies its checklist too broadly and corrupts human-written content that happens to resemble AI tells."
