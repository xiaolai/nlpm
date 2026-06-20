---
slug: data-goblin-power-bi-agentic-development
repo: data-goblin/power-bi-agentic-development
audited: 2026-06-20
commit_sha: 9704f1d00f37f3d79a5d65b618571d0088ce6478
score: 95
exemplifies:
  - R04
  - R05
  - R06
  - R07
  - R08
  - R09
  - R13
  - R30
---

# Exemplar: data-goblin/power-bi-agentic-development

**Score**: 95/100  |  **Date**: 2026-06-20  |  **Commit**: `9704f1d00f37f3d79a5d65b618571d0088ce6478`

A 10-plugin Claude Code skill collection for the Power BI/Fabric ecosystem, notable for fine-grained skill scoping, literal-trigger descriptions, and a hook design where every PostToolUse fires conditionally rather than unconditionally.

## Per-rule evidence

### R04 — Description as trigger

The `pbip` skill description packs 13 specific trigger phrases into a single frontmatter field, directly quoting the user-facing language that surfaces in real queries. This is the benchmark for what "trigger, not summary" means in practice.

> `plugins/pbip/skills/pbip/SKILL.md:4`:
>
> ```
> description: Expert guidance for the Power BI Project (PBIP) file format; project
> structure, cross-cutting operations (renames, forking), and PBIX extraction/conversion.
> Automatically invoke when the user mentions PBIP, PBIX, .pbip/.pbism/.platform files,
> or asks about "PBIP project structure", "PBIP vs PBIX", "thin report vs thick report",
> "rename a table", "cascade rename", "fork a PBIP project", "convert pbix to pbip",
> "extract pbix", "what files are in a PBIP", "PBIP encoding", "definition.pbir", or
> discusses project-level file structure and post-rename verification.
> ```

What distinguishes this from a mediocre description: the triggers are quoted user query fragments, not category labels. "thin report vs thick report" and "cascade rename" fire on the exact phrasing users type; "PBIP project structure" does not.

---

### R05 — Body length

`plugins/pbip/skills/pbip/SKILL.md` is 346 lines. It covers PBIX internal format, project structure, page naming rules, resource resolution, forking, and verification — enough for a 700-line skill. It stays under 500 by routing adjacent topics immediately:

> `plugins/pbip/skills/pbip/SKILL.md:13-14`:
>
> ```
> **This skill covers project structure, not file editing.** To modify TMDL files
> (semantic model), load the `tmdl` skill. To modify PBIR JSON files (report), load
> the `pbir-format` skill -- or preferably use the `pbir` CLI with the `pbir-cli`
> skill if available.
> ```

Five sibling skills absorb what would otherwise be 400+ lines of TMDL syntax, PBIR JSON schema, CLI usage, and model quality guidance. Without these exits the skill would fail R05 and bloat every context window that loads it.

---

### R06 — Code examples must be runnable

The PBIX extraction section provides production-grade Python (with explicit Zip Slip protection) and a bash one-liner, not pseudocode. Both are copy-paste runnable.

> `plugins/pbip/skills/pbip/SKILL.md:96-116`:
>
> ```python
> import zipfile
> from pathlib import Path
>
> pbix_path = Path("MyReport.pbix")
> output_dir = Path("MyReport_extracted")
>
> with zipfile.ZipFile(pbix_path, "r") as z:
>     # Safety: validate no entries escape the target directory (Zip Slip protection)
>     resolved_output = output_dir.resolve()
>     for member in z.infolist():
>         member_path = (output_dir / member.filename).resolve()
>         if not member_path.is_relative_to(resolved_output):
>             raise ValueError(f"Zip entry escapes target: {member.filename}")
>     z.extractall(output_dir)
>
> # Detect PBIX type
> is_thick = (output_dir / "DataModel").exists()
> is_legacy = (output_dir / "Report" / "Layout").exists()
> is_modern = (output_dir / "Report" / "definition" / "report.json").exists()
> ```

The security note (`Zip Slip protection`) and the three detection flags after extraction are what make this a real example rather than a toy snippet. A model can hand this directly to a user without adaptation.

---

### R07 — Scope note when related skills exist

The `pbip` skill routes to sibling skills at the top of the body (not in an appendix) and again in a dedicated "Related Skills" section mid-file, covering both same-plugin and cross-plugin boundaries.

> `plugins/pbip/skills/pbip/SKILL.md:323-330`:
>
> ```
> ## Related Skills
>
> **Within this plugin:**
> - **`tmdl`** -- TMDL syntax, authoring, and editing rules for direct `.tmdl` file editing
> - **`pbir-format`** -- PBIR JSON format, visual.json, theme, filters, report extensions
>
> **Other plugins:**
> - **`semantic-models`** plugin -- tooling and workflows for semantic model development
> - **`pbi-desktop`** plugin -- connecting to Power BI Desktop's local Analysis Services instance
> - **`tabular-editor`** plugin -- Tabular Editor CLI, C# scripting, BPA rules
> ```

The within-plugin vs. other-plugins split tells the model how far to route — same plugin means a skill the user likely already has; cross-plugin means the user may need to install separately. That distinction is absent from most related-skill sections.

---

### R08 — Patterns over theory

Rather than explaining the PBIP format abstractly, the skill opens with a task-routing table that maps user intents directly to the specific section or skill they need.

> `plugins/pbip/skills/pbip/SKILL.md:258-267`:
>
> ```
> | Task | Read |
> |------|------|
> | Inspect or extract a PBIX file | **Working with PBIX Files** section above |
> | Understand entry point file structure | **`references/pbip-file-types.md`** |
> | Rename a table, measure, or column | **`references/rename-cascade.md`** |
> | Fork / duplicate a PBIP project | **`references/pbip-file-types.md`** |
> | Work with Copilot tooling files | **`references/copilot-folder.md`** |
> | Edit TMDL model files | **`tmdl`** skill |
> | Edit PBIR report files | **`pbir-format`** skill |
> | Verify no broken references after rename | Grep commands below |
> ```

Eight concrete user scenarios, eight concrete resources. The model does not need to infer which section to consult — the table front-loads the routing decision before any content is read.

---

### R09 — `<example>` blocks are mandatory (minimum 2)

`pbip-validator.agent.md` has four example blocks, each with a distinct failure mode that would be missed by the others. The `<commentary>` tags explain dispatch logic, not just mechanics.

> `plugins/pbip/agents/pbip-validator.agent.md:9-43`:
>
> ```
> <example>
> Context: User has edited TMDL and PBIR files and wants to check for errors before
>          opening in PBI Desktop
> user: "Validate my PBIP project"
> assistant: "I'll use the pbip-validator agent to run validate_pbip.py and pbir validate,
>             then triage findings."
> <commentary>
> Comprehensive validation. Trigger pbip-validator; it will run the deterministic tools
> first and only fall back to manual walking for things they don't cover.
> </commentary>
> </example>
>
> <example>
> Context: User renamed a table and wants to verify no broken references remain
> user: "Check if the rename cascade is complete"
> ...
> <commentary>
> Post-rename verification is not covered by the deterministic validators. The agent
> greps for old names across TMDL, JSON, DAX, and embedded selectors.
> </commentary>
> </example>
> ```
> _(2 of 4 examples shown)_

The four examples cover: general validation, post-rename cascade, diagnostic "won't open", and single-file schema check. Together they teach the dispatch model which of these user phrases map to this agent and which fall outside it.

---

### R13 — System prompt structure: mission → steps → boundaries → format

`pbip-validator.agent.md` follows the four-section template exactly, with labeled headers for each zone.

> `plugins/pbip/agents/pbip-validator.agent.md:45-52` (mission):
>
> ```
> You are a Power BI Project (PBIP) validation agent. You diagnose structural errors,
> broken references, invalid JSON, TMDL syntax issues, and PBIR schema violations. You
> prefer deterministic validators over LLM walking whenever possible, and only fall back
> to manual inspection for classes of problems the tools do not cover.
> ```

> `plugins/pbip/agents/pbip-validator.agent.md:188-196` (boundaries):
>
> ```
> ## Fixing Rules
>
> - Fix invalid JSON syntax only when the fix is obvious (missing/trailing comma,
>   unclosed bracket). Re-validate with `jq empty` after.
> - **Never auto-generate or modify `.platform` files.** `logicalId` is Fabric identity;
>   a wrong GUID causes deployment conflicts.
> - **Never rename page/visual/bookmark folders to fix invalid-name issues.**
> - Never edit DAX expressions.
> - Never delete orphan folders automatically — warn and let the user confirm.
> ```

The boundaries section names five actions that would be plausible without the explicit stop — deleting orphans, renaming folders, modifying `.platform`. Listing prohibited actions under a "Fixing Rules" header is more enforceable than a general quality note because the model can cross-check each action against the list.

---

### R30 — Use `${CLAUDE_PLUGIN_ROOT}` for paths

All three hook scripts resolve via `${CLAUDE_PLUGIN_ROOT}`, and each hook is gated with an `if` condition so it fires only on file types within its domain.

> `plugins/pbip/hooks/hooks.json:9-22`:
>
> ```json
> {
>   "type": "command",
>   "command": "bash \"${CLAUDE_PLUGIN_ROOT}/hooks/validate-pbir.sh\"",
>   "timeout": 10,
>   "if": "Edit(**/*.Report/**)"
> },
> {
>   "type": "command",
>   "command": "bash \"${CLAUDE_PLUGIN_ROOT}/hooks/validate-tmdl.sh\"",
>   "timeout": 10,
>   "if": "Edit(**/*.tmdl)"
> },
> {
>   "type": "command",
>   "command": "bash \"${CLAUDE_PLUGIN_ROOT}/hooks/validate-report-binding.sh\"",
>   "timeout": 10,
>   "if": "Edit(**/definition.pbir)"
> }
> ```

The `if` conditions are as important as the `${CLAUDE_PLUGIN_ROOT}` usage: without them, every `Edit` anywhere in the project would trigger all three validators. The scoping — PBIR report files, any `.tmdl` file, the single `definition.pbir` entrypoint — mirrors the conceptual boundaries of the three covered domains.

---

## Worth adopting

**Pattern: Task-routing table at the top of a skill body.** Evidence: `plugins/pbip/skills/pbip/SKILL.md:258-267`. Why it would be a useful rule: when a skill covers a topic with multiple sub-tasks, a table mapping user intent → canonical resource reduces hallucination by making routing explicit before the model reads body content. Without it, the model may blend guidance from several sections for a task that has a single correct answer. Proposal: "When a skill covers 4+ distinct user tasks, open the body with a task-routing table that maps each task phrase to the section, reference file, or sibling skill that covers it."
