---
# NLPM Configuration — self-applied
strictness: strict
score_threshold: 90
rule_overrides:
  R51:
    enabled: true
    vocabulary_skill: skills/nlpm/vocabulary/
  R05:
    suppress: true
    paths:
      - skills/nlpm/conventions-claude/SKILL.md
      - skills/nlpm/conventions-codex/SKILL.md
      - skills/nlpm/conventions-antigravity/SKILL.md
      - skills/nlpm/scoring/SKILL.md
      - skills/nlpm/rules/SKILL.md
    reason: "nlpm's inherently-large canonical reference documents — the per-tool convention overlays (conventions-*), the penalty rubric (scoring), and the 50-rules catalog (rules). Each is a dense reference whose overflow is already extracted to sibling references/ files (calibration-examples, tool-manifest tables) or is auto-generated payload (the exemplar-citation blocks auditor-cite-exemplars.yml writes into rules); the R05 line budget targets ordinary artifacts, not the reference corpus. Scoped by path — the universal conventions floor and all general artifacts remain subject to R05."
---

# NLPM Settings

When linting NL artifacts in this project, use **strict** strictness. Flag artifacts scoring below **90/100** for improvement — NLPM dogfoods its own quality bar.

## R51 opt-in

NLPM uses its own vocabulary registry to detect drift across its artifacts. The registry lives at `skills/nlpm/vocabulary/registry.yaml`; SKILL.md in that directory is the human-readable counterpart.

R51 is **off by default** for projects that install NLPM. Other projects opt in by:

1. Creating a vocabulary skill at `skills/<plugin>/vocabulary/` with a `registry.yaml` listing canonical/deprecated term pairs.
2. Adding the `R51` block above to their own `.claude/nlpm.local.md` with the path pointing at their registry.

See `analysis/vocabulary-design-principles.md` for the six principles R51 operationalizes.

## R05 waiver (canonical reference skills)

R05 (body length) is **suppressed for nlpm's inherently-large canonical reference documents**: the three per-tool overlays (`conventions-claude`, `conventions-codex`, `conventions-antigravity`), the penalty rubric (`scoring`), and the 50-rules catalog (`rules`). Each documents a whole surface (a tool's artifact schema, the full penalty table, or all 50 rules) and is a dense reference, not an ordinary artifact. Overflow is already extracted into sibling `references/` files where it makes sense (`scoring` → `calibration-examples.md`; the overlays → `reference.md` for LSP/monitors/tool-catalog/marketplace schemas), and `rules`'s length is dominated by the auto-generated exemplar-citation blocks `auditor-cite-exemplars.yml` writes inline.

The waiver is **scoped by path** — it does not touch the universal `conventions` floor or any general artifact, which stay fully subject to R05 so genuinely bloated files are still caught. See `analysis/spec-sync-2026-08.md` for the decision record.
