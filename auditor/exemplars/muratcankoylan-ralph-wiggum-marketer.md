---
slug: muratcankoylan-ralph-wiggum-marketer
repo: muratcankoylan/ralph-wiggum-marketer
audited: 2026-05-13
commit_sha: HEAD
score: 90
exemplifies:
  - R04
  - R05
  - R06
  - R07
  - R08
---

# Exemplar: muratcankoylan/ralph-wiggum-marketer

**Score**: 90/100  |  **Date**: 2026-05-13  |  **Commit**: `HEAD`

A Claude Code plugin with a single skill file (`skills/copywriter/SKILL.md`) that reaches 98/100 by anchoring every phase of a 7-stage content-creation workflow in concrete patterns, checklists, and comparative examples rather than abstract advice.

## Per-rule evidence

### R04 — Description as trigger

The skill's frontmatter `description` field packs 9 distinct natural-language trigger phrases covering every entry point a user is likely to type. The phrases map directly to verbs users would reach for without knowing the plugin exists.

> Real quote from `skills/copywriter/SKILL.md:3`:
>
> ```
> description: Use this skill when the user asks to "analyze my content",
> "learn my writing style", "research competitors", "find content angles",
> "improve my blog", "write like me", "embody my brand voice", or mentions
> content strategy, voice analysis, competitive research, or iterative
> content improvement.
> ```

Nine quoted phrases plus three catch-all topic clusters in 481 characters — this is what maximal trigger coverage looks like without padding.

### R05 — Body length

The skill body runs 299 lines and every line does structural work: 7 labeled phases, each with sub-sections, code blocks, checklists, or tables. There is no preamble throat-clearing and no summary that re-states what the headings already convey.

> Real quote from `skills/copywriter/SKILL.md:23-65`:
>
> ```
> ## The Quality Loop
>
> ┌─────────────────────────────────────────────────────────────────┐
> │                    RALPH QUALITY LOOP                           │
> ├─────────────────────────────────────────────────────────────────┤
> │                                                                 │
> │   ┌──────────┐                                                  │
> │   │ DISCOVER │ → Analyze your content, competitors, market      │
> │   └────┬─────┘                                                  │
> │        ▼                                                        │
> │   ┌──────────┐                                                  │
> │   │  LEARN   │ → Extract voice, style, patterns, what works     │
> │   └────┬─────┘                                                  │
> ...
> │   ┌──────────┐                                                  │
> │   │ PUBLISH  │ → Only when it meets the quality bar             │
> │   └──────────┘                                                  │
> ```

The ASCII flow diagram replaces three paragraphs of prose with a scannable decision path an agent can index at a glance. Body length is justified because it maps each phase to its own section below.

### R06 — Runnable examples

The Usage section gives three complete invocation examples, each followed by a bulleted expansion of exactly what Ralph will do — not what the command is for, but the step-by-step execution.

> Real quote from `skills/copywriter/SKILL.md:251-286`:
>
> ```
> ### Analyze My Content First
> ```
> /ralph-marketer analyze
>
> Ralph will:
> 1. Read your existing blog posts
> 2. Analyze your Twitter/LinkedIn
> 3. Extract voice patterns
> 4. Document what makes your content unique
> 5. Create a Voice DNA profile
> ```
>
> ### Write With Quality Loop
> ```
> /ralph-marketer write --quality-bar high
>
> Ralph will:
> 1. Pick a topic from your queue
> 2. Research deeply
> 3. Find unique angle
> 4. Write in your voice
> 5. Self-critique
> 6. Iterate until good
> 7. Only mark complete when quality bar met
> ```
> ```

Each example pairs the invocation with its observable side-effects. A user reading this knows what to type and what to expect without running the command first.

### R07 — Scope notes

The closing "The Promise" section is a five-item negative scope declaration — it tells the agent explicitly what output conditions must NOT be shipped, functioning as a hard stop rather than a preference.

> Real quote from `skills/copywriter/SKILL.md:290-298`:
>
> ```
> ## The Promise
>
> Ralph won't ship content that:
> - Sounds like it was written by AI
> - Takes the obvious angle
> - Lacks data or specificity
> - You wouldn't publish under your name
> - Is "fine but forgettable"
>
> If the quality bar isn't met, Ralph keeps iterating.
> ```

Negative scope framing here is intentional: each bullet is a rejection condition the agent can test against a draft, not a vague aspiration. The final line specifies the fallback behavior (iterate), closing the loop.

### R08 — Patterns over theory

Three concrete pattern structures replace abstract guidance: the Voice DNA JSON object (machine-readable style profile), the Angle Test (❌/✅ comparative pairs), and the Iteration Triggers table (problem → fix mapping).

> Real quote from `skills/copywriter/SKILL.md:102-113` (Voice DNA):
>
> ```javascript
> {
>   "tone": "confident but not arrogant",
>   "formality": "casual professional",
>   "sentence_length": "varied, avg 15 words",
>   "paragraph_style": "short, punchy, lots of white space",
>   "signature_phrases": ["here's the thing", "let me be direct"],
>   "data_usage": "leads with stats, cites sources",
>   "storytelling": "personal anecdotes to illustrate points",
>   "cta_style": "soft ask, value-first",
>   "controversial_takes": true,
>   "emoji_usage": "minimal, strategic"
> }
> ```

> Real quote from `skills/copywriter/SKILL.md:240-247` (Iteration Triggers):
>
> ```
> | Problem | Fix |
> |---------|-----|
> | Weak hook | Rewrite opening 5 ways, pick best |
> | Generic angle | Research deeper, find unique data |
> | Wrong voice | Re-read founder's content, try again |
> | Too long | Cut 30%, keep only essential |
> | No personality | Add specific anecdote or opinion |
> | Forgettable | Find the one surprising insight |
> ```

The Voice DNA JSON gives the agent a structured schema it can fill in per-client rather than an instruction to "learn their tone." The iteration table maps each failure mode to a deterministic repair action — an agent can use it as a decision tree without judgment calls.

## Worth adopting

Pattern: **Comparative angle examples (❌/✅ pairs)**. Evidence: `skills/copywriter/SKILL.md:151-163`. The Angle Test section shows two rejected titles with explanations and two accepted titles with specificity annotations, all in a single fenced block. Why it would be a useful rule: when a skill teaches judgment (not procedure), showing what the wrong output looks like alongside the right output calibrates the agent faster than a positive-only rubric, and the ❌/✅ format is scannable in < 5 seconds.
