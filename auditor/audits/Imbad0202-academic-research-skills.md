# NLPM Audit: Imbad0202/academic-research-skills
**Date**: 2026-04-12  |  **Artifacts**: 40  |  **Strategy**: full read
**NL Score**: 20/100
**Security**: CLEAR
**Bugs**: 3  |  **Quality Issues**: 73  |  **Security Findings**: 0

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| academic-pipeline/agents/integrity_verification_agent.md | agent | 10 | Missing frontmatter (name, description), no examples, no model, vague cap (≥10 vague terms) |
| academic-pipeline/agents/pipeline_orchestrator_agent.md | agent | 10 | Missing frontmatter (name, description), no examples, no model, vague cap (≥10 vague terms) |
| deep-research/agents/synthesis_agent.md | agent | 10 | Missing frontmatter (name, description), no examples, no model, vague cap (≥10 vague terms) |
| deep-research/agents/ethics_review_agent.md | agent | 10 | Missing frontmatter (name, description), no examples, no model, vague cap (≥10 vague terms) |
| deep-research/agents/report_compiler_agent.md | agent | 10 | Missing frontmatter (name, description), no examples, no model, vague cap (≥10 vague terms) |
| deep-research/agents/socratic_mentor_agent.md | agent | 10 | Missing frontmatter (name, description), no examples, no model, vague cap (≥10 vague terms) |
| academic-paper/agents/formatter_agent.md | agent | 10 | Missing frontmatter (name, description), no examples, no model, vague cap (≥10 vague terms) |
| academic-paper/agents/peer_reviewer_agent.md | agent | 10 | Missing frontmatter (name, description), no examples, no model, vague cap (≥10 vague terms) |
| academic-paper/agents/citation_compliance_agent.md | agent | 10 | Missing frontmatter (name, description), no examples, no model, vague cap (≥10 vague terms) |
| academic-paper/agents/draft_writer_agent.md | agent | 10 | Missing frontmatter (name, description), no examples, no model, vague cap (≥10 vague terms) |
| academic-paper/agents/socratic_mentor_agent.md | agent | 10 | Missing frontmatter (name, description), no examples, no model, vague cap (≥10 vague terms) |
| academic-paper-reviewer/agents/editorial_synthesizer_agent.md | agent | 10 | Missing frontmatter (name, description), no examples, no model, vague cap (≥10 vague terms) |
| deep-research/agents/editor_in_chief_agent.md | agent | 14 | Missing frontmatter (name, description), no examples, no model, 8 vague terms |
| deep-research/agents/devils_advocate_agent.md | agent | 14 | Missing frontmatter (name, description), no examples, no model, 8 vague terms |
| academic-paper/agents/visualization_agent.md | agent | 14 | Missing frontmatter (name, description), no examples, no model, 8 vague terms |
| academic-paper/agents/structure_architect_agent.md | agent | 14 | Missing frontmatter (name, description), no examples, no model, 8 vague terms |
| academic-paper/agents/literature_strategist_agent.md | agent | 14 | Missing frontmatter (name, description), no examples, no model, 8 vague terms |
| academic-paper/agents/argument_builder_agent.md | agent | 14 | Missing frontmatter (name, description), no examples, no model, 8 vague terms |
| academic-paper/agents/intake_agent.md | agent | 14 | Missing frontmatter (name, description), no examples, no model, 8 vague terms |
| academic-paper-reviewer/agents/devils_advocate_reviewer_agent.md | agent | 14 | Missing frontmatter (name, description), no examples, no model, 8 vague terms |
| academic-paper-reviewer/agents/methodology_reviewer_agent.md | agent | 14 | Missing frontmatter (name, description), no examples, no model, 8 vague terms |
| academic-paper-reviewer/agents/domain_reviewer_agent.md | agent | 14 | Missing frontmatter (name, description), no examples, no model, 8 vague terms |
| academic-paper-reviewer/agents/perspective_reviewer_agent.md | agent | 14 | Missing frontmatter (name, description), no examples, no model, 8 vague terms |
| deep-research/agents/source_verification_agent.md | agent | 16 | Missing frontmatter (name, description), no examples, no model, 7 vague terms |
| deep-research/agents/bibliography_agent.md | agent | 16 | Missing frontmatter (name, description), no examples, no model, 7 vague terms |
| academic-paper-reviewer/agents/eic_agent.md | agent | 16 | Missing frontmatter (name, description), no examples, no model, 7 vague terms |
| academic-paper-reviewer/agents/field_analyst_agent.md | agent | 16 | Missing frontmatter (name, description), no examples, no model, 7 vague terms |
| academic-pipeline/agents/state_tracker_agent.md | agent | 18 | Missing frontmatter (name, description), no examples, no model, 6 vague terms |
| deep-research/agents/research_architect_agent.md | agent | 18 | Missing frontmatter (name, description), no examples, no model, 6 vague terms |
| deep-research/agents/monitoring_agent.md | agent | 18 | Missing frontmatter (name, description), no examples, no model, 6 vague terms |
| deep-research/agents/meta_analysis_agent.md | agent | 18 | Missing frontmatter (name, description), no examples, no model, 6 vague terms |
| academic-paper/agents/revision_coach_agent.md | agent | 18 | Missing frontmatter (name, description), no examples, no model, 6 vague terms |
| deep-research/agents/risk_of_bias_agent.md | agent | 20 | Missing frontmatter (name, description), no examples, no model, 5 vague terms |
| deep-research/agents/research_question_agent.md | agent | 20 | Missing frontmatter (name, description), no examples, no model, 5 vague terms |
| academic-paper/agents/abstract_bilingual_agent.md | agent | 22 | Missing frontmatter (name, description), no examples, no model, 4 vague terms |
| .claude/CLAUDE.md | doc | 45 | No frontmatter, no examples, no model, vague terms in routing section |
| academic-paper-reviewer/SKILL.md | skill | 65 | Version mismatch (frontmatter 1.8 vs body 1.7), no model, no allowed-tools, vague cap |
| academic-paper/SKILL.md | skill | 70 | No model declared, no allowed-tools, vague cap (≥10 vague terms) |
| academic-pipeline/SKILL.md | skill | 70 | No model declared, no allowed-tools, vague cap (≥10 vague terms) |
| deep-research/SKILL.md | skill | 70 | No model declared, no allowed-tools, vague cap (≥10 vague terms) |

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks JSON | none found |
| Scripts (.sh, .py, .js) | none found |
| MCP configs (.mcp.json) | none found |
| Package manifests (package.json, requirements.txt) | none found |

No executable artifacts present. The repository consists entirely of Markdown documentation files. Security scan is CLEAR with no surface to assess.

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | All 35 agent `.md` files across deep-research/agents/, academic-paper/agents/, academic-paper-reviewer/agents/, academic-pipeline/agents/ | Missing `name:` field in YAML frontmatter — no frontmatter block present at all | Agents cannot be registered by name in the plugin registry; the SKILL.md orchestrators dispatch them by filename but Claude Code agent resolution depends on the `name` field in frontmatter for proper tracking and deduplication |
| 2 | All 35 agent `.md` files (same set as Bug #1) | Missing `description:` field in YAML frontmatter | Without a description, agents cannot be discovered, indexed, or surfaced to users through the registry; the orchestrator has no machine-readable summary to present |
| 3 | academic-paper-reviewer/SKILL.md | Version mismatch: YAML frontmatter declares `version: "1.8"` but the Version Info table in the body reads "1.7" | Consumers relying on version negotiation (e.g., a pipeline checking compatibility) will see inconsistent values depending on which field they parse; changelog is unreliable |

## Security Fixes (PR-worthy, Medium/Low only)

*No security findings. Nothing to fix.*

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | deep-research/agents/research_question_agent.md | No model declared | -5 |
| 2 | deep-research/agents/socratic_mentor_agent.md | No model declared | -5 |
| 3 | deep-research/agents/research_architect_agent.md | No model declared | -5 |
| 4 | deep-research/agents/bibliography_agent.md | No model declared | -5 |
| 5 | deep-research/agents/source_verification_agent.md | No model declared | -5 |
| 6 | deep-research/agents/risk_of_bias_agent.md | No model declared | -5 |
| 7 | deep-research/agents/meta_analysis_agent.md | No model declared | -5 |
| 8 | deep-research/agents/synthesis_agent.md | No model declared | -5 |
| 9 | deep-research/agents/devils_advocate_agent.md | No model declared | -5 |
| 10 | deep-research/agents/ethics_review_agent.md | No model declared | -5 |
| 11 | deep-research/agents/editor_in_chief_agent.md | No model declared | -5 |
| 12 | deep-research/agents/report_compiler_agent.md | No model declared | -5 |
| 13 | deep-research/agents/monitoring_agent.md | No model declared | -5 |
| 14 | academic-paper/agents/intake_agent.md | No model declared | -5 |
| 15 | academic-paper/agents/structure_architect_agent.md | No model declared | -5 |
| 16 | academic-paper/agents/literature_strategist_agent.md | No model declared | -5 |
| 17 | academic-paper/agents/argument_builder_agent.md | No model declared | -5 |
| 18 | academic-paper/agents/visualization_agent.md | No model declared | -5 |
| 19 | academic-paper/agents/draft_writer_agent.md | No model declared | -5 |
| 20 | academic-paper/agents/abstract_bilingual_agent.md | No model declared | -5 |
| 21 | academic-paper/agents/citation_compliance_agent.md | No model declared | -5 |
| 22 | academic-paper/agents/peer_reviewer_agent.md | No model declared | -5 |
| 23 | academic-paper/agents/revision_coach_agent.md | No model declared | -5 |
| 24 | academic-paper/agents/socratic_mentor_agent.md | No model declared | -5 |
| 25 | academic-paper/agents/formatter_agent.md | No model declared | -5 |
| 26 | academic-paper-reviewer/agents/field_analyst_agent.md | No model declared | -5 |
| 27 | academic-paper-reviewer/agents/eic_agent.md | No model declared | -5 |
| 28 | academic-paper-reviewer/agents/domain_reviewer_agent.md | No model declared | -5 |
| 29 | academic-paper-reviewer/agents/methodology_reviewer_agent.md | No model declared | -5 |
| 30 | academic-paper-reviewer/agents/perspective_reviewer_agent.md | No model declared | -5 |
| 31 | academic-paper-reviewer/agents/devils_advocate_reviewer_agent.md | No model declared | -5 |
| 32 | academic-paper-reviewer/agents/editorial_synthesizer_agent.md | No model declared | -5 |
| 33 | academic-pipeline/agents/pipeline_orchestrator_agent.md | No model declared | -5 |
| 34 | academic-pipeline/agents/state_tracker_agent.md | No model declared | -5 |
| 35 | academic-pipeline/agents/integrity_verification_agent.md | No model declared | -5 |
| 36 | deep-research/agents/research_question_agent.md | Zero examples | -15 |
| 37 | deep-research/agents/socratic_mentor_agent.md | Zero examples | -15 |
| 38 | deep-research/agents/research_architect_agent.md | Zero examples | -15 |
| 39 | deep-research/agents/bibliography_agent.md | Zero examples | -15 |
| 40 | deep-research/agents/source_verification_agent.md | Zero examples | -15 |
| 41 | deep-research/agents/risk_of_bias_agent.md | Zero examples | -15 |
| 42 | deep-research/agents/meta_analysis_agent.md | Zero examples | -15 |
| 43 | deep-research/agents/synthesis_agent.md | Zero examples | -15 |
| 44 | deep-research/agents/devils_advocate_agent.md | Zero examples | -15 |
| 45 | deep-research/agents/ethics_review_agent.md | Zero examples | -15 |
| 46 | deep-research/agents/editor_in_chief_agent.md | Zero examples | -15 |
| 47 | deep-research/agents/report_compiler_agent.md | Zero examples | -15 |
| 48 | deep-research/agents/monitoring_agent.md | Zero examples | -15 |
| 49 | academic-paper/agents/intake_agent.md | Zero examples | -15 |
| 50 | academic-paper/agents/structure_architect_agent.md | Zero examples | -15 |
| 51 | academic-paper/agents/literature_strategist_agent.md | Zero examples | -15 |
| 52 | academic-paper/agents/argument_builder_agent.md | Zero examples | -15 |
| 53 | academic-paper/agents/visualization_agent.md | Zero examples | -15 |
| 54 | academic-paper/agents/draft_writer_agent.md | Zero examples | -15 |
| 55 | academic-paper/agents/abstract_bilingual_agent.md | Zero examples | -15 |
| 56 | academic-paper/agents/citation_compliance_agent.md | Zero examples | -15 |
| 57 | academic-paper/agents/peer_reviewer_agent.md | Zero examples | -15 |
| 58 | academic-paper/agents/revision_coach_agent.md | Zero examples | -15 |
| 59 | academic-paper/agents/socratic_mentor_agent.md | Zero examples | -15 |
| 60 | academic-paper/agents/formatter_agent.md | Zero examples | -15 |
| 61 | academic-paper-reviewer/agents/field_analyst_agent.md | Zero examples | -15 |
| 62 | academic-paper-reviewer/agents/eic_agent.md | Zero examples | -15 |
| 63 | academic-paper-reviewer/agents/domain_reviewer_agent.md | Zero examples | -15 |
| 64 | academic-paper-reviewer/agents/methodology_reviewer_agent.md | Zero examples | -15 |
| 65 | academic-paper-reviewer/agents/perspective_reviewer_agent.md | Zero examples | -15 |
| 66 | academic-paper-reviewer/agents/devils_advocate_reviewer_agent.md | Zero examples | -15 |
| 67 | academic-paper-reviewer/agents/editorial_synthesizer_agent.md | Zero examples | -15 |
| 68 | academic-pipeline/agents/pipeline_orchestrator_agent.md | Zero examples | -15 |
| 69 | academic-pipeline/agents/state_tracker_agent.md | Zero examples | -15 |
| 70 | academic-pipeline/agents/integrity_verification_agent.md | Zero examples | -15 |
| 71 | deep-research/SKILL.md | No allowed-tools declared | -5 |
| 72 | academic-paper/SKILL.md | No allowed-tools declared | -5 |
| 73 | academic-paper-reviewer/SKILL.md | No allowed-tools declared | -5 |

*Vague-word penalties (-2 per occurrence, capped at -20) applied to all 35 agent files and all 4 SKILL.md files. The 12 agents scoring 10/100 hit the vague cap (≥10 vague terms each); terms include "appropriate," "comprehensive," "thorough," "relevant," "effectively," "various," "sufficient," "adequate," "timely," "robust." Agents scoring 14–22 show progressively fewer vague terms (8 down to 4 per file).*

## Cross-Component

**Systemic frontmatter gap (all 35 agents):** Every agent `.md` file in the repository — across all four sub-packages (`deep-research`, `academic-paper`, `academic-paper-reviewer`, `academic-pipeline`) — is missing YAML frontmatter entirely. The SKILL.md orchestrators reference them by filename path, which works at runtime, but the Claude Code registry cannot surface or track agents without `name:` and `description:` fields. This is a single structural decision (likely "agents are implementation details, not registry entries") that has uniformly propagated across the entire codebase. A single PR template adding frontmatter to all 35 agent files would fix Bugs #1 and #2 simultaneously.

**SKILL.md version mismatch (academic-paper-reviewer):** The `academic-paper-reviewer/SKILL.md` frontmatter declares `version: "1.8"` while the embedded Version Info table reads "1.7". The CLAUDE.md routing document (suite overview) also lists it as "v1.8". This means the body changelog is one version behind. The fix is a one-line edit to the body table.

**Ironic omission (integrity_verification_agent):** The most comprehensive agent in the suite — a 479-line verification agent whose entire purpose is detecting fabricated, hallucinated, and inconsistent references — has the same score (10/100) as the shortest agents. It enforces rigorous documentation standards on research output but is itself entirely undocumented at the registration level.

**Model routing ambiguity:** None of the 35 agents declare a model, and none declare `model: inherit`. The SKILL.md files specify which agents to invoke but do not propagate model selection downward. When a user invokes `deep-research` with `claude-opus-4-6` and the SKILL.md spawns subagents, those subagents will default to whatever model the runtime selects — potentially `claude-haiku-4-5` for cost reasons — rather than the heavyweight model appropriate for tasks like meta-analysis or integrity verification. Adding `model: claude-sonnet-4-6` (or `model: inherit` for agents that should inherit the orchestrator's model) would make this behavior explicit and predictable.

**Agent count in CLAUDE.md vs SKILL.md:** CLAUDE.md describes `deep-research` as a "13-agent research team" and `academic-paper` as a "12-agent paper writing" pipeline. Counting the agent files: `deep-research/agents/` has 13 files, `academic-paper/agents/` has 12 files — counts are accurate. No orphaned agents detected.

## Recommendation

**CLEAR — submit PRs for all bugs and quality issues.**

No security gate issues. The repository contains no executable surfaces. The quality problems are entirely structural and addressable through documentation additions.

Recommended PR sequence:

1. **Bug fix PR — frontmatter (all 35 agents):** Add YAML frontmatter blocks to all 35 agent files. Template per agent:
   ```yaml
   ---
   name: <package>:<agent-slug>
   description: <one-line description of the agent's role and trigger condition>
   ---
   ```
   This single PR resolves Bugs #1 and #2 and is the highest-leverage change in the repository.

2. **Bug fix PR — version mismatch:** In `academic-paper-reviewer/SKILL.md`, change the Version Info table body entry from "1.7" to "1.8" to match the frontmatter.

3. **Quality PR — model declarations (all 35 agents):** Add `model: claude-sonnet-4-6` to compute-intensive agents (meta-analysis, integrity-verification, synthesis, pipeline-orchestrator) and `model: inherit` to utility agents (state-tracker, monitoring, formatting). This prevents silent model downgrade when subagents are spawned.

4. **Quality PR — examples (all 35 agents):** Add at least two concrete examples per agent showing input → output. Given the domain (academic research), good examples would show a real research question going through each agent's processing — they exist naturally in the SKILL.md example files and can be adapted.

5. **Quality PR — allowed-tools (all 4 SKILL.md files):** Declare `allowed-tools` in each SKILL.md to constrain what tools the skill may invoke, reducing blast radius and making tool usage auditable.
