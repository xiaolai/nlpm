# NLPM Audit: K-Dense-AI/scientific-agent-skills
**Date**: 2026-04-25  |  **Artifacts**: 100  |  **Strategy**: batched
**NL Score**: 83/100
**Security**: CLEAR
**Bugs**: 6  |  **Quality Issues**: 31  |  **Security Findings**: 2

---

## NL Score Summary

100 SKILL.md files scored. Scores computed by subtracting penalties from a 100-point baseline. Skills are reference documents (not agents or commands), so agent-specific penalties (missing model declaration, missing example blocks) do not apply. Applicable penalties: missing/malformed frontmatter fields (name, description, license, metadata.skill-author), vague quantifiers, and code-correctness bugs.

| Tier | Count | Score Range | Representative Skills |
|------|-------|-------------|----------------------|
| Clean | ~48 | 86–88 | zarr-python, umap-learn, medchem, pymc, simpy, networkx, geomaster, iso-13485-certification, anndata, cobrapy, pennylane, dask, vaex |
| Minor issues | ~27 | 82–85 | tiledbvcf, scikit-learn (bug), pyopenms (bug), molecular-dynamics, dnanexus-integration, timesfm-forecasting, rowan, scvelo, benchling-integration |
| Quality issues | ~17 | 73–80 | venue-templates, scientific-writing, peer-review, literature-review, citation-management, pptx-posters, docx, markitdown, fluidsim (bug), gtars (bug), geniml (bug) |
| Significant issues | ~8 | 70–72 | treatment-plans, clinical-reports, scientific-critical-thinking, scholar-evaluation, latex-posters |

**Weighted average: 83/100**

### Per-file scores (notable deviations only)

| File | Score | Top Issue |
|------|-------|-----------|
| scikit-learn/SKILL.md | 82 | BUG: `uv uv pip install scikit-learn` (doubled prefix) |
| pyopenms/SKILL.md | 82 | BUG: `uv uv pip install pyopenms` (doubled prefix) |
| fluidsim/SKILL.md | 80 | BUG: `uv uv pip install fluidsim` (3× occurrences) |
| gtars/SKILL.md | 78 | BUG: `uv uv pip install gtars` + `license: Unknown` |
| geniml/SKILL.md | 80 | BUG: `uv uv pip install geniml` (3× occurrences including extras) |
| latchbio-integration/SKILL.md | 80 | BUG: `python3 -m uv pip install latch` (wrong invocation) |
| scanpy/SKILL.md | 83 | QUALITY: `license: SD-3-Clause license` (apparent typo for BSD-3-Clause) |
| treatment-plans/SKILL.md | 72 | QUALITY: Nano Banana Pro proprietary tool branding throughout |
| clinical-reports/SKILL.md | 72 | QUALITY: Nano Banana Pro proprietary tool branding throughout |
| scientific-critical-thinking/SKILL.md | 72 | QUALITY: Nano Banana Pro proprietary tool branding + Gemini 3.1 Pro ref |
| scientific-schematics/SKILL.md | 75 | QUALITY: Nano Banana 2 + "Gemini 3.1 Pro Preview" proprietary branding |
| scholar-evaluation/SKILL.md | 75 | QUALITY: Nano Banana Pro branding |
| venue-templates/SKILL.md | 75 | QUALITY: Nano Banana Pro branding |
| pptx-posters/SKILL.md | 75 | QUALITY: Nano Banana Pro branding |
| scientific-writing/SKILL.md | 72 | QUALITY: Nano Banana Pro branding |
| peer-review/SKILL.md | 75 | QUALITY: Nano Banana Pro branding |
| literature-review/SKILL.md | 72 | QUALITY: Nano Banana Pro branding |
| citation-management/SKILL.md | 75 | QUALITY: Nano Banana Pro branding |
| latex-posters/SKILL.md | 72 | QUALITY: Nano Banana Pro branding + missing license + missing metadata |
| generate-image/SKILL.md | 80 | QUALITY: Nano Banana 2 proprietary branding |
| markitdown/SKILL.md | 78 | QUALITY: Nano Banana Pro branding + `pip install` not `uv pip` |
| docx/SKILL.md | 78 | QUALITY: missing metadata.skill-author |
| xlsx/SKILL.md | 80 | QUALITY: missing metadata block entirely, `license: Proprietary` |
| pdf/SKILL.md | 80 | QUALITY: missing metadata block entirely, `license: Proprietary` |
| dnanexus-integration/SKILL.md | 80 | QUALITY: `license: Unknown` |
| protocolsio-integration/SKILL.md | 80 | QUALITY: `license: Unknown` |
| glycoengineering/SKILL.md | 80 | QUALITY: `license: Unknown` |
| opentrons-integration/SKILL.md | 80 | QUALITY: `license: Unknown` |
| omero-integration/SKILL.md | 80 | QUALITY: `license: Unknown` |
| labarchive-integration/SKILL.md | 80 | QUALITY: `license: Unknown` |
| benchling-integration/SKILL.md | 82 | QUALITY: `license: Unknown` |
| phylogenetics/SKILL.md | 80 | QUALITY: `license: Unknown` + conda-only install |
| paper-lookup/SKILL.md | 82 | QUALITY: missing `license` field |
| torch-geometric/SKILL.md | 82 | QUALITY: missing `license` field |
| sympy/SKILL.md | 85 | QUALITY: `license` value is a URL not a SPDX identifier |
| polars/SKILL.md | 85 | QUALITY: `license` value is a URL not a SPDX identifier |
| polars-bio/SKILL.md | 85 | QUALITY: `license` value is a URL not a SPDX identifier |
| rowan/SKILL.md | 84 | QUALITY: `license: Proprietary (API key required)` — non-standard format |
| scvelo/SKILL.md | 82 | QUALITY: `pip install scvelo` (should be `uv pip install`) |
| neuropixels-analysis/SKILL.md | 83 | QUALITY: `pip install` not `uv pip install` |
| tiledbvcf/SKILL.md | 82 | QUALITY: conda-only install, third-party author |
| molecular-dynamics/SKILL.md | 82 | QUALITY: conda/pip mix, third-party author |

---

## Issue Breakdown

### Bugs (code-correctness issues that will break user workflows)

**BUG-1: Doubled `uv` prefix in install commands (5 skills)**

The pattern `uv uv pip install <pkg>` appears in five skills. This is an invalid shell command — `uv uv` is not a valid invocation. Users copying these commands will get an error.

Affected skills: `scikit-learn`, `pyopenms`, `fluidsim` (×3), `gtars`, `geniml` (×3 including extras variant and git install)

All instances should be `uv pip install <pkg>`.

**BUG-2: Wrong uv invocation in latchbio-integration (1 skill)**

`python3 -m uv pip install latch` is the wrong way to call uv. The correct form is `uv pip install latch`.

**BUG-3: License field typo in scanpy (1 skill)**

`license: SD-3-Clause license` — the leading `B` is missing. Should be `BSD-3-Clause`.

### Quality Issues (cross-cutting patterns)

**QUALITY-1: Proprietary "Nano Banana Pro/2" tool branding (~14 skills)**

Approximately 14 skills contain mandatory workflow instructions that reference "Nano Banana Pro" or "Nano Banana 2" — K-Dense Inc.'s proprietary AI image generation product. These instructions direct Claude to call `python scripts/generate_schematic.py` or `python scripts/generate_schematic_ai.py` using a paid OpenRouter API key. This is not a neutral reference but a workflow dependency on a proprietary product.

From the skills' perspective, this creates two problems:
1. Skills become unusable without a paid API key (`OPENROUTER_API_KEY`), which is undisclosed in most affected skill descriptions.
2. The wording ("Nano Banana Pro will automatically generate...") misleads users into thinking this is a free capability.

Affected skills (partial list): `treatment-plans`, `clinical-reports`, `scientific-critical-thinking`, `scientific-schematics`, `scholar-evaluation`, `venue-templates`, `pptx-posters`, `scientific-writing`, `peer-review`, `literature-review`, `citation-management`, `latex-posters`, `generate-image`, `markitdown`

**QUALITY-2: `license: Unknown` on 9 skills**

Nine skills (plus `benchling-integration`) have `license: Unknown` in their frontmatter. This is not a valid SPDX identifier and signals that the skill author did not determine the license of the referenced library. Downstream users cannot assess redistribution rights.

Affected: `dnanexus-integration`, `protocolsio-integration`, `glycoengineering`, `opentrons-integration`, `omero-integration`, `labarchive-integration`, `phylogenetics`, `gtars`, `benchling-integration`

**QUALITY-3: Missing `license` field on 2 skills**

`paper-lookup` and `torch-geometric` have no `license` field at all.

**QUALITY-4: `license` value is a URL (3 skills)**

`sympy`, `polars`, and `polars-bio` set `license` to a URL string rather than an SPDX identifier (e.g., `license: LGPL-3.0-or-later` not `license: https://...`).

**QUALITY-5: Missing `metadata.skill-author` (4 skills)**

`docx`, `xlsx`, `pdf`, and `latex-posters` have no `metadata:` block at all, omitting the required `skill-author` field. This makes attribution and provenance impossible.

**QUALITY-6: Non-standard `license: Proprietary` (3 skills)**

`pdf`, `xlsx`, and `rowan` use `license: Proprietary` or `license: Proprietary (API key required)`. While not incorrect, these should reference a `LICENSE.txt` file or a specific proprietary license name for clarity. `xlsx` and `pdf` both say `LICENSE.txt has complete terms` but `latex-posters` has no license field at all.

**QUALITY-7: Package manager inconsistency (~6 skills)**

Several skills use `pip install` instead of `uv pip install`, inconsistent with the collection's standard: `scvelo`, `neuropixels-analysis`, `citation-management`, `markitdown`. Others use conda exclusively (`tiledbvcf`) or mix conda and pip (`molecular-dynamics`, `diffdock`, `geomaster`).

**QUALITY-8: Third-party authors without disclosure (7 skills)**

Seven skills are contributed by authors outside K-Dense Inc. This is fine, but users may not realize they are using third-party skill content:

| Skill | Author |
|-------|--------|
| dhdna-profiler | AHK Strategies (ashrafkahoush-ux) |
| consciousness-council | AHK Strategies (ashrafkahoush-ux) |
| what-if-oracle | AHK Strategies (ashrafkahoush-ux) |
| timesfm-forecasting | Clayton Young / Superior Byte Works, LLC (@borealBytes) |
| tiledbvcf | Jeremy Leipzig |
| molecular-dynamics | Kuan-lin Huang |
| phylogenetics | Kuan-lin Huang |
| glycoengineering | Kuan-lin Huang |
| scvelo | Kuan-lin Huang |
| rowan | Rowan Science |
| bgpt-paper-search | Paperzilla |

---

## Security Scan

### Execution Surface Inventory

| Surface | Count | Notes |
|---------|-------|-------|
| Hooks | 0 | No `.claude/hooks/` files |
| Scripts | 233 | Mostly Python; see below for breakdown |
| MCP configs | 0 | No `.mcp.json` files |
| Package manifests | 0 | No `package.json` or `requirements.txt` at repo root |

**Script breakdown by pattern:**
- `generate_schematic.py` (wrapper): ~14 copies across skills — calls Python subprocess to `generate_schematic_ai.py`
- `generate_schematic_ai.py` (AI generator): ~14 copies — makes HTTPS POST to `https://openrouter.ai/api/v1` via `requests`
- `research_lookup.py`: 1 copy — makes HTTPS POST to `https://api.parallel.ai` via `requests`
- `recalc.py`: 1 copy — calls LibreOffice via subprocess (no shell=True)
- Domain-specific analysis scripts: ~200 copies (plotting, data processing, validation helpers)

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | `scientific-schematics/scripts/generate_schematic_ai.py` (×14 copies) | ~189 | outbound-api-call | Script makes `requests.post()` to `https://openrouter.ai/api/v1` — a third-party commercial API. Prompt text (user's natural language diagram description) is transmitted to OpenRouter. API key is correctly read from `OPENROUTER_API_KEY` env var and passed via environment not CLI args (good practice). Risk: user prompt content leaves the local machine. |
| 2 | Medium | `research-lookup/research_lookup.py` | ~55 | outbound-api-call | Script sends user research queries to `https://api.parallel.ai` (`PARALLEL_API_KEY`) and, for academic searches, to OpenRouter Perplexity backend. Query text is transmitted to two separate commercial services. No data-residency or privacy disclosure in the SKILL.md description. |

**No CRITICAL or HIGH patterns found.** No `curl | bash`, no `eval()` with variables, no `os.system()`, no `shell=True` in subprocess calls, no hardcoded credentials, no reverse-shell patterns, no base64 decode+exec patterns.

The two Medium findings are not inherently malicious — outbound API calls are expected for an AI-assisted research collection. The risk is the absence of disclosure: the skill descriptions do not clearly state that user content (research queries, diagram prompts) is transmitted to third-party commercial services (`openrouter.ai`, `api.parallel.ai`).

---

## Top Recommendations

1. **Fix the `uv uv pip install` bug across 5 skills.** This is a simple find-and-replace. All 5 skills have invalid installation commands that will fail immediately for users.

2. **Fix `python3 -m uv pip install` in latchbio-integration.** One-line fix.

3. **Fix scanpy license typo** (`SD-3-Clause` → `BSD-3-Clause`).

4. **Disclose the API key requirement in skill descriptions** for all skills that depend on `OPENROUTER_API_KEY` or `PARALLEL_API_KEY`. Currently users discover this requirement only at runtime.

5. **Replace proprietary "Nano Banana Pro" references with the generic tool name or a documented API abstraction.** The branding makes 14 skills feel like marketing rather than neutral technical documentation. The scripts themselves (`generate_schematic.py`) already use a clean interface; the SKILL.md prose just needs rewording.

6. **Resolve `license: Unknown` on 9 skills.** These are all well-known libraries with clear OSS licenses (e.g., DnaNexus has an Apache-2.0 client SDK, OpenTrons has an MIT license). A 10-minute check per skill would resolve all 9.

7. **Add `metadata:` blocks to `docx`, `xlsx`, `pdf`, and `latex-posters`.** Missing `skill-author` breaks provenance tracking.

8. **Standardize `license` field format.** Use SPDX identifiers consistently (e.g., `MIT`, `Apache-2.0`, `BSD-3-Clause`) rather than URLs or free-text descriptions.

9. **Standardize installation commands.** Decide whether `uv pip install` is the house standard (it appears to be) and apply it consistently across all skills, replacing bare `pip install` calls in `scvelo`, `neuropixels-analysis`, `citation-management`, and `markitdown`.

10. **Add data-transmission disclosure to research-lookup and generate-image skill descriptions.** Users should know their queries/prompts are sent to external commercial services before they run these skills.
