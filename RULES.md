# The 50 Rules of Natural Language Programming

The normative reference lives in the rules skill: `skills/nlpm/rules/SKILL.md`

Run `/nlpm:score` to enforce these rules. Run `/nlpm:fix` to auto-repair fixable ones. See [EXAMPLES.md](EXAMPLES.md) for before/after walkthroughs.

## Quick Reference

| Section | Rules | Summary |
|---------|-------|---------|
| Universal | R01-R03 | No vague quantifiers, every line earns tokens, positive framing |
| Skills | R04-R08 | Trigger descriptions, 500-line limit, runnable examples, scope notes |
| Agents | R09-R13 | Example blocks, model tier, least-privilege tools, output format |
| Commands | R14-R18 | Numbered steps, empty input, output format, error paths |
| Shared Partials | R19-R20 | user-invocable: false, purpose description |
| Rules | R21-R26 | Bold imperative + rationale, enforceable, budget, scoping |
| Hooks | R27-R32 | Case-sensitive events, script existence, fail-open, block vs advise |
| Memory file | R33-R39 | Build/test commands, architecture, no stale refs (CLAUDE.md / AGENTS.md / GEMINI.md) |
| Prompts | R40-R42 | Five layers, exact output format, injection resistance |
| Orchestration | R43-R47 | Parallel/sequential, QC gates, cost gates, retry limits |
| Plugins | R48-R50 | Name required, memory file vs README, four-place version bump |
