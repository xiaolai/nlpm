# NLPM Scoring — Memory Files and Agent Workflow Programs

Penalty tables for two artifact types most projects do not contain. Part of the `nlpm:scoring` rubric: the formula, the shared tables, the score bands and the false-positive list are in `../SKILL.md`. These rows carry the same weight as the rows there.

---

### Memory Files

Applies to `.md` files located in `~/.claude/projects/*/memory/` directories.

| Rule | Check | Pass (+0) | Penalty |
|------|-------|-----------|---------|
| -- | Has YAML frontmatter | Present | -15 |
| -- | `name` in frontmatter | Present | -10 |
| -- | `description` in frontmatter | Present | -10 |
| -- | `type` in frontmatter | Present (`user`/`feedback`/`project`/`reference`) | -5 |
| -- | Content matches declared type | Yes | -10 |
| -- | Referenced in MEMORY.md index | Yes | -5 (orphaned memory) |
| R37 | Stale content | No references to removed files or functions | -10 |

---

### Agent Workflow Programs (project-root `program.md`-style files)

A new artifact type recognized 2026-05-28 (see `nlpm:conventions` §2 and `auditor/exemplars/karpathy-autoresearch.md`): a project-root Markdown file driving an autonomous agent loop, hybrid between a memory file (AGENTS.md-shaped context) and a slash command (numbered workflow with output format + error paths).

**No type-specific penalty rows.** This artifact type is scored as the UNION of:
- **Command rules R14–R17**: numbered steps for multi-phase work, empty-input handling, output format, error paths.
- **Memory file rules R33–R39**: build/run commands, architecture overview, no stale refs, instructive-not-descriptive.
- **Universal R01** (vague quantifiers) and R03 (positive framing).

Type-specific penalty rows are deferred until N ≥ 3 examples surface — the R14–R17 and R33–R39 rows, with R01 and R03, cover every section such a file has (steps, output, error paths, build/run commands, architecture), and inventing rows from N = 1 risks over-fitting (calibrated per the same discipline applied to multi-tool discovery deferrals).

**Patterns this artifact type rewards** (loaded on demand from `nlpm:patterns`):
- P10 (numeric anchoring of subjective principles)
- P11 (paired CAN/CANNOT contract)
- P12 (autonomy instruction + rationale + fallback ladder)
- P13 (vivid closing use-case)
