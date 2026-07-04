---
slug: realrossmanngroup-no_ai_slop_writing_rules
repo: realrossmanngroup/no_ai_slop_writing_rules
audited: 2026-07-04
commit_sha: 35e32ae45878148a6bd898572a9d15c96711affe
score: 98
exemplifies:
  - R04
  - R05
  - R08
  - R38
  - R35
  - R37
  - R01
---

# Exemplar: realrossmanngroup/no_ai_slop_writing_rules

**Score**: 98/100  |  **Date**: 2026-07-04  |  **Commit**: `35e32ae45878148a6bd898572a9d15c96711affe`

A two-skill package (`no-ai-slop`, `rossmann-voice`) plus a `CLAUDE.md` entrypoint that teaches an agent to write prose without AI tells; notable for grounding every stylistic claim in a measured corpus statistic instead of an assertion, and for a self-check pass the agent runs before returning any text.

## Per-rule evidence

### R04 — Description as trigger

`rossmann-voice`'s description packs the specific traits an agent needs to match against a request, rather than a generic summary of the skill's topic.

> Real quote from `skills/rossmann-voice/SKILL.md:3`:
>
> ```
> description: "Louis Rossmann's writing voice for general prose: testable-number density, high sentence-length variance, claim-then-proof structure, contractions, contempt shown through precision. Consult when writing in his voice."
> ```

Five distinct, checkable traits are named before the trigger clause. An agent scanning descriptions for "which skill handles imitating a specific writer's style" matches on the traits, not on the word "voice" alone.

### R05 — Body length

Both `SKILL.md` files stay well clear of the 500-line ceiling despite carrying dense reference content: `skills/no-ai-slop/SKILL.md` runs 106 lines, `skills/rossmann-voice/SKILL.md` runs 173 lines. The banned-words catalog that would bloat either file is split out to `skills/no-ai-slop/references/ai-writing-detection.md` instead of inlined.

> Real quote from `CLAUDE.md:78` (pointing at the split-out reference rather than inlining it):
>
> ```
> The full categorized lists of banned verbs, adjectives, nouns, intensifiers, opening and transition and concluding phrases, heading anti-patterns, academic tells, hedging markers, and structural and statistical patterns live in `.claude/skills/no-ai-slop/references/ai-writing-detection.md`.
> ```

The split keeps both `SKILL.md` files scannable in one read while the exhaustive word list — which has no per-item action beyond "don't use this" — lives where it's loaded on demand.

### R08 — Patterns over theory

`no-ai-slop/SKILL.md` teaches every one of its nine highlighted rules as a paired WRONG/RIGHT worked example instead of an abstract description of the flaw.

> Real quote from `skills/no-ai-slop/SKILL.md:17-22`:
>
> ```
> ## Rule 4: No intensifiers
>
> "Significantly", "dramatically", "extremely" and their kin are placeholders for evidence. Replace the word with the number it was standing in for.
>
> - WRONG: "The pricing was significantly higher than the cost of the part."
> - RIGHT: "They charged $1,200 for a repair that needed a $5 chip."
> ```

The fix generalizes beyond this one sentence: "replace the vague claim with a specific, checkable fact" is stated once at the top of the file (`skills/no-ai-slop/SKILL.md:8`) and every subsequent rule is an instance of that one pattern, not a new abstraction to learn.

### R38 — More instructive than descriptive

`CLAUDE.md` is a numbered list of 24 imperative, non-negotiable rules, not a narrative description of what the project is for.

> Real quote from `CLAUDE.md:26-30`:
>
> ```
> These are non-negotiable. Violating any of them makes the output unusable.
>
> 1. **No emdashes.** The character is banned. Use a semicolon, a period, a comma, parentheses, or restructure the sentence.
>
> 2. **No unsourced statistics.** Every number must be real and attributable. If you cannot point to where it comes from, do not write it. A made-up figure is worse than no figure.
> ```

Of the file's 78 lines, the "Purpose" and "Voice" sections (12 lines) are the only descriptive content; the remaining majority is either a directive rule or a worked instruction — well under R38's 60% description ceiling.

### R35 — Architecture overview

`AGENTS.md` opens with the exact directory shape a contributor or agent needs before touching the package, as a fenced tree rather than prose.

> Real quote from `AGENTS.md:9-16`:
>
> ```
> skills/
> ├── no-ai-slop/
> │   ├── SKILL.md
> │   └── references/
> └── rossmann-voice/
>     └── SKILL.md
> ```

It also states the one invariant that matters for that layout in the very next line — "The `.claude/skills/` directory is kept for Claude Code project-local use. Keep the skill content synchronized when changing either published skill" — which is the fact a mirrored-directory layout needs and a plain file listing would not convey.

### R37 — No stale references

Every path `CLAUDE.md` and `AGENTS.md` point at resolves to a real file, and the two skill mirrors (`skills/` and `.claude/skills/`) are kept byte-identical rather than one going stale.

> Real quote from `CLAUDE.md:15-16`:
>
> ```
> - `.claude/skills/no-ai-slop/SKILL.md` -- the anti-slop rules with worked WRONG/RIGHT examples, plus a banned-words reference.
> - `.claude/skills/rossmann-voice/SKILL.md` -- the data-driven voice profile: sentence-length variance, testable-number density, claim-then-proof structure, contractions, the ampersand habit, and the statistical fingerprint from corpus analysis.
> ```

Both files exist at those exact paths, and `skills/no-ai-slop/SKILL.md` / `.claude/skills/no-ai-slop/SKILL.md` are identical on disk, confirmed by the audit's cross-component check. A reference that names a path is only as good as the file staying there; this repo keeps both copies in lockstep rather than letting the published and Claude Code-local trees drift apart.

### R01 — No vague quantifiers without criteria

This repo's own subject is banning vague language, and its rule text practices what it prohibits: `CLAUDE.md` bans exactly the words R01 penalizes ("some," "various," "many," "significantly") in the artifact author's *output*, and does not use them in its own body to describe that ban.

> Real quote from `skills/rossmann-voice/SKILL.md:112-116` (the vocabulary substitution table it imposes on generated prose):
>
> ```
> | many issues / various problems | state the count or name the specific issues |
> ```

The rule about vague quantifiers is itself stated with a quantifier: "32.0 dollar amounts per 10k words," "83.6% contraction rate," "106 lines," not "a good amount of numbers" or "frequent contractions." The self-referential consistency — a style guide against vagueness that is not vague about its own claims — is the strongest kind of evidence for R01 because the artifact had every opportunity to violate its own rule while describing it, and didn't.

## Worth adopting

Pattern: corpus-grounded style claims. Evidence: `skills/rossmann-voice/SKILL.md:16` ("Dollar amounts appear at 32.0 per 10,000 words and legal or technical terms at 18.4 per 10,000 words") and the "Statistical Fingerprint" table at `skills/rossmann-voice/SKILL.md:158-172`. Why it would be a useful rule: a voice or style skill that asserts a trait ("use short sentences," "sound formal") without a measured baseline gives the agent no way to check whether its output actually matches; a skill that states the measured distribution (mean, percentile, rate per word count) gives the agent a checkable target instead of a vibe.

Pattern: pre-return self-check checklist anchored to the skill's own rule numbers. Evidence: `skills/no-ai-slop/SKILL.md:92-105` ("Self-check before returning text," a 10-step numbered pass, each step citing the rule it enforces, e.g. "Check every number: is it real and attributable? If not, cut it (Rule 2)"). Why it would be a useful rule: skills that state constraints but never tell the agent to verify its own output against them rely on the constraints being followed on the first pass; a closing checklist that maps each check back to a specific rule number turns "try not to violate these" into a mechanical last step before the agent hands back text.
