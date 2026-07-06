---
slug: Graphify-Labs-graphify
repo: Graphify-Labs/graphify
audited: 2026-07-06
commit_sha: 31211a0e7c512d63972b4f0438877d3777ae0e85
score: 99
exemplifies:
  - R01
  - R05
  - R04
  - R07
  - R08
  - R06
---

# Exemplar: Graphify-Labs/graphify

**Score**: 99/100  |  **Date**: 2026-07-06  |  **Commit**: `31211a0e7c512d63972b4f0438877d3777ae0e85`

A Claude Code skill (with 13 generated platform siblings) that turns a folder
into a knowledge graph; its 8 conditionally-loaded reference files split a
674-line dispatcher into scoped chunks that are only read when their trigger
condition is true, and its extraction prompt turns a fuzzy "confidence" field
into a discrete, quotable rubric.

## Per-rule evidence

### R01 — No vague quantifiers without criteria

`extraction-spec.md` could have told the extraction subagent to assign a
"reasonable confidence score" to inferred edges. Instead it enumerates exactly
five allowed values, each anchored to a concrete evidentiary description, and
explicitly forbids the midpoint value that models default to when given a
continuous range.

> Real quote from `graphify/skills/agents/references/extraction-spec.md:49-58`:
>
> ```
> - INFERRED edges: pick exactly ONE value from this set — never 0.5:
>     0.95  direct structural evidence (shared data structure, named cross-file reference).
>     0.85  strong inference (clear functional alignment, no direct symbol link).
>     0.75  reasonable inference (shared problem domain + similar shape, requires interpretation).
>     0.65  weak inference (thematically related, no shape evidence).
>     0.55  speculative but plausible (surface-level co-occurrence only).
>   Models follow discrete rubrics better than continuous ranges; the bimodal
>   distribution observed in production (>50% at 0.5, >40% at 0.85+) shows the
>   range guidance is being collapsed to a binary. If no value above fits, mark
>   the edge AMBIGUOUS rather than picking 0.4 or below.
> ```

What makes this a strong example rather than a mediocre one: the rule cites
the actual failure mode it replaced ("the bimodal distribution observed in
production") instead of asserting the discrete rubric is better on faith —
the justification is itself concrete evidence, not a vague quantifier about
"better" model behavior.

### R05 — Under 500 lines (split into scoped sub-skills)

The `agents`-platform dispatcher (`graphify/skill-agents.md`, 674 lines) does
not inline everything a run might need. It defers the seven largest or
least-common flows — GitHub/multi-repo merge, the extraction subagent prompt,
add/watch, the commit hook, query/path/explain, incremental update, and
video transcription — into 8 separate reference files, all of which are
individually under 500 lines (the largest, `query.md`, is 311). Each is
gated behind an explicit condition in the dispatcher rather than always read.

> Real quote from `graphify/skill-agents.md:656-664`:
>
> ```
> ## For /graphify add and --watch
>
> Neither is part of the default build. When the user runs `/graphify add <url>` to fetch a URL into the corpus, or passes `--watch` to auto-rebuild on file changes, see `references/add-watch.md`.
>
> ---
>
> ## For the commit hook and native AGENTS.md integration
>
> When the user asks to install the post-commit auto-rebuild hook or wire graphify into a project's AGENTS.md, see `references/hooks.md`.
> ```

What makes this strong: the split boundary tracks actual usage frequency —
`hooks.md` (33 lines) and `add-watch.md` (56 lines) are two of the smallest
files, but they're still split out because they're conditionally invoked,
not because they were long. The dispatcher stays lean on the always-loaded
default path (`/graphify <path>` with no flags) rather than the file being
split arbitrarily by size alone.

### R04 — Description is a trigger, not a summary

The root `graphify/skill-agents.md` frontmatter description names the two
concrete conditions that should make an agent reach for this skill — a
general codebase question, and specifically the case where a graph already
exists on disk — rather than describing the skill's internal mechanism.

> Real quote from `graphify/skill-agents.md:1-4`:
>
> ```
> ---
> name: graphify
> description: "Use for any question about a codebase, its architecture, file relationships, or project content — especially when graphify-out/ exists, where the question should be treated as a graphify query first. Turns any input (code, docs, papers, images, videos) into a persistent knowledge graph with god nodes, community detection, and query/path/explain tools."
> ---
> ```

What makes this strong: the description front-loads the trigger condition
("especially when `graphify-out/` exists") ahead of the feature summary,
so the disambiguation signal a routing model needs most (is there already a
graph to query, or does one need to be built?) is the first clause, not
buried after the mechanism description.

### R07 — Scope note when related skills exist

Every one of the 8 reference files opens with a one-line load condition
that states exactly which invocation makes it relevant, so the dispatcher
(and any agent reading `skill-agents.md`) knows when to open the file
versus when to skip it entirely.

> Real quote from `graphify/skills/agents/references/update.md:1-3`:
>
> ```
> # graphify reference: incremental update and cluster-only
>
> Load this only when the user passed `--update` or `--cluster-only`. A first-time full build never reads this file.
> ```

> Real quote from `graphify/skills/agents/references/extraction-spec.md:3`:
>
> ```
> Load this in Step 3 Part B when the corpus has at least one doc, paper, or image chunk. A pure-code corpus skips Part B and never reads this file.
> ```

What makes this strong: the note doesn't just say when to load the file —
it also states the negative case explicitly ("a pure-code corpus... never
reads this file"), removing any ambiguity about whether the file is a
default-path dependency.

### R08 — Patterns over theory

`query.md` doesn't explain BFS/DFS graph traversal theory; it gives a
two-row decision table that maps a question shape directly to the traversal
mode to invoke, so the model can classify a user's question without
reasoning about graph algorithms.

> Real quote from `graphify/skills/agents/references/query.md:5-10`:
>
> ```
> Two traversal modes - choose based on the question:
>
> | Mode | Flag | Best for |
> |------|------|----------|
> | BFS (default) | _(none)_ | "What is X connected to?" - broad context, nearest neighbors first |
> | DFS | `--dfs` | "How does X reach Y?" - trace a specific chain or dependency path |
> ```

What makes this strong: each row anchors the mode to an example question
phrasing, not an abstract description of the algorithm's traversal order —
the model matches the user's actual wording to a row, it doesn't have to
infer which algorithm "broad context" implies.

### R06 — Runnable examples

`add-watch.md`'s inline-Python fallback is not pseudocode describing what
the URL-ingest call should do — it's the literal command, with real
exception handling for the two error types `ingest()` actually raises,
ready to run after substituting three placeholders.

> Real quote from `graphify/skills/agents/references/add-watch.md:9-25`:
>
> ```
> $(cat graphify-out/.graphify_python) -c "
> import sys
> from graphify.ingest import ingest
> from pathlib import Path
>
> try:
>     out = ingest('URL', Path('./raw'), author='AUTHOR', contributor='CONTRIBUTOR')
>     print(f'Saved to {out}')
> except ValueError as e:
>     print(f'error: {e}', file=sys.stderr)
>     sys.exit(1)
> except RuntimeError as e:
>     print(f'error: {e}', file=sys.stderr)
>     sys.exit(1)
> "
> ```

What makes this strong: the two `except` clauses match `ingest()`'s actual
raised exception types (verified against `graphify/ingest.py` during the
audit) rather than a generic `except Exception` — so the example teaches the
real failure surface, not a placeholder that would silently swallow an
unrelated bug.

## Worth adopting

**Pattern: CI-enforced byte-diff guard for multi-platform-generated artifacts.**
Evidence: `.github/workflows/ci.yml:11-47` and `tools/skillgen/gen.py:1010`
— all 8 scored files (plus their 13 platform siblings under
`graphify/skills/{amp,claude,claw,codex,...}/references/`) are generated by
`tools/skillgen/gen.py` from a shared fragment source, and the `skillgen-check`
CI job runs `python -m tools.skillgen --check` (byte-diff against committed
output), `--audit-coverage` (every heading of the source body single-homes in
its render), and `--schema-singleton` (the `file_type` enum is byte-identical
everywhere it's repeated), failing the build on any drift.
Why it would be a useful rule: any NL artifact shipped in more than one
platform-specific copy (Claude/Codex/Antigravity overlays, or NLPM's own
tier-aware conventions files) is one hand-edit away from silent divergence;
a generator-plus-CI-diff pair turns "did the copies stay in sync" from a
manual review question into a deterministic gate — the same shape as
`bin/nlpm-check`'s own role in this project, but applied to N generated
copies of one canonical source rather than one file's rule compliance.
