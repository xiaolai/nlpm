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
    reason: "Per-tool convention overlays are inherently large reference documents; overflow detail is extracted to reference.md rather than deleted. Scoped to the conventions-* tool overlays only — the universal conventions floor and all general artifacts remain subject to R05."
---

# NLPM Settings

When linting NL artifacts in this project, use **strict** strictness. Flag artifacts scoring below **90/100** for improvement — NLPM dogfoods its own quality bar.

## R51 opt-in

NLPM uses its own vocabulary registry to detect drift across its artifacts. The registry lives at `skills/nlpm/vocabulary/registry.yaml`; SKILL.md in that directory is the human-readable counterpart.

R51 is **off by default** for projects that install NLPM. Other projects opt in by:

1. Creating a vocabulary skill at `skills/<plugin>/vocabulary/` with a `registry.yaml` listing canonical/deprecated term pairs.
2. Adding the `R51` block above to their own `.claude/nlpm.local.md` with the path pointing at their registry.

See `analysis/vocabulary-design-principles.md` for the six principles R51 operationalizes.

## R05 waiver (tool overlays only)

R05 (body length) is **suppressed for the `conventions-*` per-tool overlays** (`conventions-claude`, `conventions-codex`, `conventions-antigravity`). These files document an entire tool's artifact surface and are inherently large reference documents; overflow detail is extracted into a sibling `reference.md` (the pattern the overlays already use for LSP/monitors/tool-catalog/marketplace schemas) rather than deleted. `conventions-claude` in particular sits in the 400–500 line band by design.

The waiver is **scoped by path** — it does not touch the universal `conventions` floor or any general artifact, which stay fully subject to R05 so genuinely bloated files are still caught. See `analysis/spec-sync-2026-08.md` for the decision record.
