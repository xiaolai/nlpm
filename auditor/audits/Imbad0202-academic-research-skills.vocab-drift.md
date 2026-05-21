# NLPM Vocab Drift Advisory

Repo: Imbad0202/academic-research-skills
Artifacts scanned: 54
Drift candidates: 4 (high: 1, medium: 3, low: 0)

──────────────────────────────────────────────────────────────────

CANDIDATE 1 — confidence: high
  Disposition: drift
  Terms:
    "revision plan" — 4 occurrences across 3 files
    "revision roadmap" — 22 occurrences across 5 files
  Likely identity: the structured, prioritized output artifact that translates reviewer comments into actionable revision tasks for the author
  Evidence:
    academic-paper/agents/revision_coach_agent.md:3: "Parses reviewer comments and builds the structured revision plan for the author"
    academic-paper/agents/revision_coach_agent.md:6: "Revision Coach Agent — Reviewer Comment Parser and Revision Planner"
    academic-paper/SKILL.md:100: "Parse unstructured reviewer comments into structured Revision Roadmap; classify, map, and prioritize comments"
    academic-paper-reviewer/agents/editorial_synthesizer_agent.md:178: "### Step 5: Revision Roadmap Construction"
    commands/ars-revision-coach.md:2: "description: ARS academic-paper `revision-coach` mode — Revision Roadmap + Response Letter Skeleton"
  Suggested canonical: revision roadmap
  Action options:
    a) Update revision_coach_agent.md frontmatter description and H1 subtitle to use "Revision Roadmap" consistently
    b) Update docs/ARCHITECTURE.md and pipeline_orchestrator_agent.md to replace "revision plan" with "Revision Roadmap"
    c) If "revision plan" is intentionally a scoped sub-artifact distinct from the full Revision Roadmap, document the distinction explicitly

──────────────────────────────────────────────────────────────────

CANDIDATE 2 — confidence: medium
  Disposition: likely drift
  Terms:
    "artefact" — 4 occurrences across 2 files
    "artifact" — 68 occurrences across 5+ files
  Likely identity: an intermediate pipeline output document (e.g., the Paper Outline, Argument Blueprint, or draft) produced by one agent and consumed by the next
  Evidence:
    academic-paper/SKILL.md:189: "the writer artefact the evaluator must verify per pre_commitment_check_protocol"
    academic-paper/SKILL.md:194: "the writer Phase 4b draft (the artefact under review)"
    academic-paper/agents/peer_reviewer_agent.md:580: "the artefact under review"
    academic-paper/agents/formatter_agent.md:282: "Before emitting any final converted artifact (LaTeX / DOCX / PDF)"
    README.md:91: "from a real 10-stage pipeline run — peer review reports, integrity verification reports"
  Suggested canonical: artifact
  Action options:
    a) Normalize "artefact" → "artifact" across academic-paper/SKILL.md and peer_reviewer_agent.md (3 substitutions in SKILL.md, 1 in agent)
    b) Document the British/American spelling choice in a style guide if intentional
    c) Add an editor lint rule to catch future mixed-spelling introductions

──────────────────────────────────────────────────────────────────

CANDIDATE 3 — confidence: medium
  Disposition: likely drift
  Terms:
    "integrity check" — 7 occurrences across 5 files
    "integrity verification" — 8 occurrences across 5 files
  Likely identity: the mandatory Stage 2.5 / Stage 4.5 pipeline gate that verifies all references, citations, and data for factual accuracy
  Evidence:
    academic-paper-reviewer/SKILL.md:280: "deep-research --> academic-paper --> [integrity check] --> academic-paper-reviewer"
    .claude/CLAUDE.md:212: "→ integrity check (Stage 2.5)"
    README.md:245: "integrity verification (Stage 2.5 + 4.5) cannot be skipped"
    academic-pipeline/agents/integrity_verification_agent.md:3: "Verifies all references, citations, and data for factual accuracy before submission and after revision"
  Suggested canonical: integrity verification
  Action options:
    a) Align pipeline diagrams and cross-references in SKILL.md and CLAUDE.md to use "integrity verification" consistently
    b) Reserve "integrity check" as a shorthand alias documented alongside the canonical form
    c) If "integrity check" refers to a lighter-weight sampling pass and "integrity verification" to the full gate, document the distinction explicitly

──────────────────────────────────────────────────────────────────

CANDIDATE 4 — confidence: medium
  Disposition: co-occurrence drift
  Terms:
    "chapter plan" — 12 occurrences across 5 files
    "paper blueprint" — 2 occurrences across 1 file
  Likely identity: the structured document produced by plan mode, capturing chapter-by-chapter argument sketches and word-count allocations via Socratic dialogue
  Evidence:
    academic-paper/SKILL.md:275: "| `plan` | "guide my paper" | 1->10->3->4 | Chapter Plan + INSIGHT Collection |"
    academic-paper/SKILL.md:306: "Socratic mode that guides users through paper planning one chapter at a time. Builds a complete Paper Blueprint through structured dialogue."
    academic-paper/references/plan_mode_protocol.md:71: "Output: Chapter Plan + INSIGHT Collection"
    academic-paper/references/failure_paths.md:20: "Save completed Chapter Plan"
    MODE_REGISTRY.md:28: "| `plan` | Originality | Chapter Plan + INSIGHT collection (Socratic) |"
  Suggested canonical: chapter plan
  Action options:
    a) Update academic-paper/SKILL.md §Plan Mode description to use "Chapter Plan" instead of "Paper Blueprint"
    b) Declare canonical in a vocabulary registry and mark "Paper Blueprint" as deprecated alias
    c) If "Paper Blueprint" represents the full structured document (chapters + arguments) and "Chapter Plan" is a component, clarify the hierarchy in the plan mode protocol doc

──────────────────────────────────────────────────────────────────

Summary
  Most-drifted concept: Revision Roadmap / revision plan (HIGH confidence, most cross-file spread)
  Files with the most drift: academic-paper/SKILL.md (candidates 2, 3, 4), academic-paper-reviewer/SKILL.md (candidates 1, 3)
  Suggested next step: Bootstrap a vocabulary skill via /nlpm:vocab-init to lock in canonical terms for revision roadmap, integrity verification, artifact, and chapter plan — then use R51 drift detection to catch future regressions
