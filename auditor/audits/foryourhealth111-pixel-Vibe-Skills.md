# Audit: foryourhealth111-pixel/Vibe-Skills

**Date**: 2026-04-19  
**Auditor**: NLPM Auditor (automated)  
**Repo**: foryourhealth111-pixel/Vibe-Skills  
**Pre-scan risk level**: HIGH (698 script files, 2 high-pattern matches detected)

---

## NL Score Summary

Artifacts scored: 72 (4 agent templates, 3 opencode agents, 7 commands, 58 skills)

| Artifact | Type | Score | Top Penalties |
|---|---|---|---|
| `agents/templates/debugger.md` | agent | 30 | -25 name, -25 description, -15 no examples, -5 no model |
| `agents/templates/security-reviewer.md` | agent | 30 | -25 name, -25 description, -15 no examples, -5 no model |
| `agents/templates/reviewer.md` | agent | 30 | -25 name, -25 description, -15 no examples, -5 no model |
| `agents/templates/planner.md` | agent | 30 | -25 name, -25 description, -15 no examples, -5 no model |
| `config/opencode/agents/vibe-implement.md` | agent | 55 | -25 name, -15 no examples, -5 no model |
| `config/opencode/agents/vibe-plan.md` | agent | 55 | -25 name, -15 no examples, -5 no model |
| `config/opencode/agents/vibe-review.md` | agent | 55 | -25 name, -15 no examples, -5 no model |
| `config/opencode/commands/vibe-implement.md` | command | 60 | -25 name, -5 no allowed-tools, -10 no empty-input handling |
| `config/opencode/commands/vibe.md` | command | 60 | -25 name, -5 no allowed-tools, -10 no empty-input handling |
| `config/opencode/commands/vibe-review.md` | command | 60 | -25 name, -5 no allowed-tools, -10 no empty-input handling |
| `commands/vibe-what-do-i-want.md` | command | 50 | -25 name, -5 no allowed-tools, -10 multi-step/no numbered steps, -10 no empty-input handling |
| `commands/vibe-implement.md` | command | 60 | -25 name, -5 no allowed-tools, -10 no empty-input handling |
| `commands/vibe.md` | command | 60 | -25 name, -5 no allowed-tools, -10 no empty-input handling |
| `commands/vibe-review.md` | command | 60 | -25 name, -5 no allowed-tools, -10 no empty-input handling |
| `bundled/skills/code-reviewer/SKILL.md` | skill | 65 | -20 vague (automated, best practices, deep, recommendations, fixes) |
| `bundled/skills/mathematical-logic-expert/SKILL.md` | skill | 58 | -12 vague, -10 marked legacy/low-confidence, -10 no verified examples |
| `bundled/skills/aios-ux-design-expert/SKILL.md` | skill | 58 | -25 no examples, -7 vague, -10 defers to external files at unknown paths |
| `bundled/skills/aios-devops/SKILL.md` | skill | 58 | -25 no examples, -7 vague, -10 defers to external files at unknown paths |
| `bundled/skills/deepagent-memory-fold/SKILL.md` | skill | 68 | -10 no examples, -12 hardcoded Windows absolute paths |
| `bundled/skills/cancel-ralph/SKILL.md` | skill | 70 | -15 minimal content, -5 PS1-only scope |
| `bundled/skills/ralph-loop/SKILL.md` | skill | 72 | -15 minimal content, -5 PS1-only scope |
| `bundled/skills/aios-squad-creator/SKILL.md` | skill | 72 | -15 very brief, -8 external dependency references |
| `bundled/skills/yeet/SKILL.md` | skill | 72 | -15 no examples, -8 git add -A unexplained |
| `bundled/skills/windows-hook-debugging/SKILL.md` | skill | 73 | -15 short, -12 vague confidence level wording |
| `bundled/skills/vibe-what-do-i-want/SKILL.md` | skill | 65 | -25 no examples, -10 unclear execution boundary |
| `bundled/skills/report-generator/SKILL.md` | skill | 75 | -15 primarily Chinese language, -10 mixed-locale output contract |
| `bundled/skills/video-studio/SKILL.md` | skill | 75 | -10 primarily Chinese, -5 backend detection vague, -10 Windows absolute paths |
| `bundled/skills/data-exploration-visualization/SKILL.md` | skill | 83 | -7 primarily Chinese description, -10 mixed output locale |
| `bundled/skills/submission-checklist/SKILL.md` | skill | 83 | -7 primarily Chinese, -10 mixed output locale |
| `bundled/skills/latex-submission-pipeline/SKILL.md` | skill | 83 | -7 primarily Chinese, -10 mixed output locale |
| `bundled/skills/error-resolver/SKILL.md` | skill | 78 | -12 capitalized name (`Error Resolver` vs kebab-case convention) |
| `bundled/skills/excel-analysis/SKILL.md` | skill | 78 | -12 capitalized name (`Excel Analysis` vs kebab-case convention) |
| `bundled/skills/digital-brain/agents/AGENTS.md` | skill | 78 | -12 no model, -10 dispatch-only with few examples |
| `bundled/skills/evals-context/SKILL.md` | skill | 82 | -8 vague disambiguation terms |
| `bundled/skills/scientific-brainstorming/SKILL.md` | skill | 82 | -8 no allowed-tools, conversational style |
| `bundled/skills/omero-integration/SKILL.md` | skill | 83 | -7 vague integration language |
| `bundled/skills/document-skills/SKILL.md` | skill | 82 | -8 dispatcher pattern, -10 no examples |
| `bundled/skills/context-hunter/SKILL.md` | skill | 80 | -10 checklist format, no code examples |
| `bundled/skills/node-zombie-guardian/SKILL.md` | skill | 80 | -10 limited examples, -10 PowerShell-only scope |
| `bundled/skills/figma/SKILL.md` | skill | 83 | -7 vague "required flow" terminology |
| `bundled/skills/comprehensive-research-agent/SKILL.md` | skill | 82 | -8 self-referential "Score Expectations" section, -10 vague confidence claims |
| `bundled/skills/theme-factory/SKILL.md` | skill | 85 | -5 vague design terms, -10 no allowed-tools |
| `bundled/skills/context-fundamentals/SKILL.md` | skill | 87 | -3 vague, -10 no allowed-tools |
| `bundled/skills/pptx-posters/SKILL.md` | skill | 85 | -5 vague, -10 space-separated allowed-tools format |
| `bundled/skills/tiledbvcf/SKILL.md` | skill | 83 | -7 vague, -10 no allowed-tools |
| `bundled/skills/pathml/SKILL.md` | skill | 85 | -5 vague, -10 no allowed-tools |
| `bundled/skills/latchbio-integration/SKILL.md` | skill | 87 | -3 vague, -10 no allowed-tools |
| `bundled/skills/imagegen/SKILL.md` | skill | 87 | -3 vague, -10 no allowed-tools |
| `bundled/skills/plotly/SKILL.md` | skill | 87 | -3 vague, -10 no allowed-tools |
| `bundled/skills/pytorch-lightning/SKILL.md` | skill | 87 | -3 vague, -10 no allowed-tools |
| `bundled/skills/vaex/SKILL.md` | skill | 87 | -3 vague, -10 no allowed-tools |
| `bundled/skills/get-available-resources/SKILL.md` | skill | 83 | -7 description unusually long, -10 no allowed-tools |
| `bundled/skills/datacommons-client/SKILL.md` | skill | 87 | -3 vague, -10 no allowed-tools |
| `bundled/skills/pyzotero/SKILL.md` | skill | 87 | -3 vague, allowed-tools ✓ |
| `bundled/skills/speckit-plan/SKILL.md` | skill | 88 | -2 minor vague, -10 no allowed-tools |
| `bundled/skills/paper-2-web/SKILL.md` | skill | 87 | -3 vague, allowed-tools ✓ |
| `bundled/skills/document-skills/docx/SKILL.md` | skill | 82 | -8 short, -10 no allowed-tools |
| `bundled/skills/document-skills/pdf/SKILL.md` | skill | 83 | -7 vague terms, -10 no allowed-tools |
| `bundled/skills/document-skills/pptx/SKILL.md` | skill | 88 | -2 minor vague, -10 no allowed-tools |
| `bundled/skills/labarchive-integration/SKILL.md` | skill | 85 | -5 vague terms, -10 no allowed-tools |
| `bundled/skills/data-normalization-tool/SKILL.md` | skill | 85 | allowed-tools ✓, -5 vague |
| `bundled/skills/evaluating-machine-learning-models/SKILL.md` | skill | 85 | allowed-tools ✓, -5 vague |
| `bundled/skills/creating-data-visualizations/SKILL.md` | skill | 87 | allowed-tools ✓, -3 vague |
| `bundled/skills/performance-testing/SKILL.md` | skill | 83 | -7 vague, -10 no allowed-tools |
| `bundled/skills/aios-ux-design-expert/SKILL.md` | skill | 58 | (already listed above) |
| `bundled/skills/rowan/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/sympy/SKILL.md` | skill | 92 | -8 no allowed-tools |
| `bundled/skills/metabolomics-workbench-database/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/pdb-database/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/opentargets-database/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/clinvar-database/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/gwas-database/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/pubchem-database/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/clinicaltrials-database/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/ml-data-leakage-guard/SKILL.md` | skill | 92 | -8 no allowed-tools |
| `bundled/skills/timesfm-forecasting/SKILL.md` | skill | 92 | allowed-tools ✓, quality checklist excellent |
| `bundled/skills/speckit-analyze/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/speckit-specify/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/speckit-implement/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/polars/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/dask/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/deepchem/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/neurokit2/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/hypogenic/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/data-quality-frameworks/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/protocolsio-integration/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/clinpgx-database/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/etetoolkit/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/openai-docs/SKILL.md` | skill | 85 | -5 vague, -10 no allowed-tools |
| `bundled/skills/edgartools/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/esm/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/fred-economic-data/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/alphafold-database/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/diffdock/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/matlab/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/pysam/SKILL.md` | skill | 87 | -3 vague, -10 no allowed-tools |
| `bundled/skills/data-artist/SKILL.md` | skill | 85 | -5 vague, -10 no allowed-tools |
| `bundled/skills/digital-brain/SKILL.md` | skill | 87 | -3 vague, -10 no allowed-tools |
| `bundled/skills/security-best-practices/SKILL.md` | skill | 85 | -5 vague, -10 no allowed-tools |
| `bundled/skills/node-zombie-guardian/SKILL.md` | skill | 80 | (already listed) |
| `bundled/skills/context-hunter/SKILL.md` | skill | 80 | (already listed) |
| `bundled/skills/fluidsim/SKILL.md` | skill | 80 | -10 no allowed-tools, -2 `uv uv pip install` typo bug |
| `bundled/skills/pytorch-lightning/SKILL.md` | skill | 87 | -3 vague, -10 no allowed-tools |
| `bundled/skills/etetoolkit/SKILL.md` | skill | 90 | -10 no allowed-tools |
| `bundled/skills/paper-2-web/SKILL.md` | skill | 87 | (see above) |
| `bundled/skills/scientific-brainstorming/SKILL.md` | skill | 82 | (see above) |
| `bundled/skills/unsloth/SKILL.md` | skill | 87 | -3 vague, -10 no allowed-tools |

**Weighted mean (estimates):**
- Agent templates: ~30/100 (4 artifacts)
- OpenCode agents: ~55/100 (3 artifacts)
- Commands: ~58/100 (7 artifacts)
- Skills: ~85/100 (58 artifacts)
- **Overall portfolio mean: ~79/100**

---

## Security Scan

| File | Severity | Pattern | Finding |
|---|---|---|---|
| `bundled/skills/autonomous-builder/assets/auto-continue.sh` | **HIGH** | `--dangerously-skip-permissions` in unattended loop | Shell script runs `claude --dangerously-skip-permissions` in an infinite restart loop (max 10 iterations). Bypasses all permission prompts. Comment explicitly warns this is unsafe outside trusted environments. |
| `scripts/setup/persist-codex-openai-env.ps1` | **HIGH** | Credential persistence | Writes `VCO_INTENT_ADVICE_API_KEY` directly into Codex `settings.json`. API key flows from parameter or env var into persistent config on disk. |
| `scripts/setup/sync-codex-settings-to-user-env.ps1` | **HIGH** | Credential exfiltration surface | Syncs API keys (`VCO_INTENT_ADVICE_API_KEY`, `VCO_VECTOR_DIFF_API_KEY`) from settings.json to Windows User-scope environment variables (registry). |
| `bundled/skills/denario/references/llm_configuration.md` | MEDIUM | `curl https://sdk.cloud.google.com | bash` in docs | Documentation reference instructs users to pipe curl to bash. In a skill reference file; not executed by agent, but may be copied by users without review. |
| `bundled/skills/unsloth/references/llms-txt.md` | MEDIUM | `curl -fsSL https://ollama.com/install.sh | sh` (×10) | Same pattern repeated ~10 times throughout a large reference file. Content is mirrored from upstream vendor docs (Ollama install). |
| `bundled/skills/alphafold-database/references/api_reference.md` | MEDIUM | `curl https://sdk.cloud.google.com | bash` in docs | Same Google Cloud SDK install pattern as denario skill. |
| `scripts/setup/install-local-vm-host.sh` | LOW | `sudo apt-get` | Setup script requires passwordless sudo to install QEMU/KVM packages. Scoped to VM host setup; not invoked automatically. |
| `bundled/skills/digital-brain/package.json` | LOW | npm scripts without `postinstall` | Scripts exist (`setup`, `weekly-review`, etc.) but no postinstall hook; no auto-execution risk. |

---

## Bugs

### BUG-01: `fluidsim/SKILL.md` — doubled `uv` command

**File**: `bundled/skills/fluidsim/SKILL.md`, lines 26–32  
**Type**: Documentation bug / broken instruction  
The install instructions use `uv uv pip install fluidsim` (duplicated `uv`). A user following this instruction verbatim will get a command-not-found error.

```
# Actual text:
uv uv pip install fluidsim
uv uv pip install "fluidsim[fft]"
uv uv pip install "fluidsim[fft,mpi]"
```

**Fix**: Remove duplicated `uv`:
```bash
uv pip install fluidsim
uv pip install "fluidsim[fft]"
uv pip install "fluidsim[fft,mpi]"
```

---

### BUG-02: All agent templates missing required frontmatter

**Files**: `agents/templates/debugger.md`, `agents/templates/security-reviewer.md`, `agents/templates/reviewer.md`, `agents/templates/planner.md`  
**Type**: Structural defect — templates will not load correctly  
All four agent template files have zero YAML frontmatter. The files begin with a markdown heading (`# Debugger Agent Template`) with no `---` block. Without `name` and `description`, Claude Code cannot register these agents, and any agent that references them by name will fail silently.

---

### BUG-03: All opencode agents missing `name` field

**Files**: `config/opencode/agents/vibe-implement.md`, `config/opencode/agents/vibe-plan.md`, `config/opencode/agents/vibe-review.md`  
**Type**: Missing required field  
All three opencode agents have `description` and `mode: primary` but no `name` field. The `name` field is required for agent registration and invocation.

---

### BUG-04: Commands missing `name` field

**Files**: All 7 command files (`commands/vibe*.md`, `config/opencode/commands/vibe*.md`)  
**Type**: Missing required field  
No command file declares a `name` field. Commands without a `name` cannot be indexed by the plugin system and may conflict when multiple plugins expose same-named entries.

---

### BUG-05: `autonomous-builder/assets/auto-continue.sh` — unguarded `--dangerously-skip-permissions`

**File**: `bundled/skills/autonomous-builder/assets/auto-continue.sh`, line 204  
**Type**: Security / behavioral regression  
The script runs Claude in an unattended restart loop with `--dangerously-skip-permissions`. This flag disables all permission prompts, meaning file writes, shell executions, and tool calls proceed without user approval. The loop runs up to 10 times before pausing. There is no check for whether the target environment is "trusted" before running.

---

## Security Fixes

### SEC-FIX-01: Remove or gate `--dangerously-skip-permissions` in `auto-continue.sh`

**Priority**: HIGH  
**File**: `bundled/skills/autonomous-builder/assets/auto-continue.sh`  

The `--dangerously-skip-permissions` flag must not be the default. Add an explicit opt-in gate:

```bash
# Before:
claude --skill autonomous-builder --project "$PROJECT_DIR" --dangerously-skip-permissions 2>&1 | tee -a "$LOG_FILE"

# After:
if [ "${ALLOW_SKIP_PERMISSIONS:-false}" = "true" ]; then
    claude --skill autonomous-builder --project "$PROJECT_DIR" --dangerously-skip-permissions 2>&1 | tee -a "$LOG_FILE"
else
    claude --skill autonomous-builder --project "$PROJECT_DIR" 2>&1 | tee -a "$LOG_FILE"
fi
```

Add a warning if the flag is enabled:
```bash
if [ "${ALLOW_SKIP_PERMISSIONS:-false}" = "true" ]; then
    log "⚠️ WARNING: --dangerously-skip-permissions is ENABLED. All permission prompts are bypassed."
fi
```

---

### SEC-FIX-02: Avoid committing API keys via `persist-codex-openai-env.ps1`

**Priority**: HIGH  
**File**: `scripts/setup/persist-codex-openai-env.ps1`  

The script writes an API key to `settings.json`. If `settings.json` is committed to git (even accidentally), the key is exposed. Add a `.gitignore` entry for `settings.json` and document that it should never be committed:

```powershell
# After writing settings.json, verify it is git-ignored
$gitIgnorePath = Join-Path (Split-Path $SettingsPath -Parent) '.gitignore'
if (-not (Select-String -Path $gitIgnorePath -Pattern "settings\.json" -Quiet 2>$null)) {
    Write-Warning "settings.json is not in .gitignore. API keys may be committed accidentally."
}
```

---

### SEC-FIX-03: Annotate `curl | bash` examples in reference files

**Priority**: MEDIUM  
**Files**: `bundled/skills/denario/references/llm_configuration.md`, `bundled/skills/unsloth/references/llms-txt.md`, `bundled/skills/alphafold-database/references/api_reference.md`  

Add a security note adjacent to all `curl | bash` / `curl | sh` examples:

```markdown
> **Security note**: Piping curl output directly to a shell executes remote code without inspection.
> Verify the script's contents before running. Download and inspect first:
> ```bash
> curl -fsSL https://example.com/install.sh -o install.sh
> less install.sh  # inspect before running
> bash install.sh
> ```
```

---

## Quality Issues

### Q-01: Agent templates are non-functional stubs

**Files**: `agents/templates/*.md`  
All four agent template files contain no frontmatter and cannot be used as real agents. They appear to be documentation examples rather than deployable templates, but they are in the `agents/` directory where Claude Code would try to load them. Either add proper frontmatter or move them to a `docs/` or `examples/` subdirectory.

### Q-02: `name` field systematically missing from all commands and opencode agents

**Scope**: 10 files (7 commands + 3 opencode agents)  
Every command and opencode agent omits `name`. This is the single largest quality gap across the repository. A one-line fix per file would add ~10 points to each artifact's score and raise the overall portfolio average from ~79 to ~86.

Example fix for `config/opencode/commands/vibe-implement.md`:
```yaml
---
name: vibe-implement
description: Run the governed Vibe-Skills runtime for implementation-first work after design approval.
agent: vibe-implement
---
```

### Q-03: `code-reviewer` skill has vague language throughout

**File**: `bundled/skills/code-reviewer/SKILL.md`  
Contains multiple vague quantifiers in close proximity: "Automated scaffolding", "Best practices built-in", "Deep analysis", "Recommendations", "Automated fixes". These terms do not tell the agent what specific actions to take. Replace with concrete operations (e.g., "check for unused imports", "flag functions exceeding 50 lines").

### Q-04: `mathematical-logic-expert` skill is marked legacy and low-confidence

**File**: `bundled/skills/mathematical-logic-expert/SKILL.md`  
Self-annotated as "⚠️ Legacy template awaiting research upgrade" with confidence "🔴 Low". This skill should either be upgraded or removed. A low-confidence, legacy-flagged skill in the active distribution creates expectations the artifact cannot meet.

### Q-05: `aios-ux-design-expert` and `aios-devops` skills defer entirely to external files

**Files**: `bundled/skills/aios-ux-design-expert/SKILL.md`, `bundled/skills/aios-devops/SKILL.md`  
Both skills activate by loading `.aios-core/development/agents/*.md` from the user's local filesystem. If that path does not exist, the skill silently falls back to `.codex/agents/` which may also not exist. The skill provides no standalone functionality — it is a thin wrapper with no self-contained knowledge. Add inline documentation of what the agent does so it is useful without the external dependency.

### Q-06: Inconsistent `name` casing: `Error Resolver`, `Excel Analysis`

**Files**: `bundled/skills/error-resolver/SKILL.md`, `bundled/skills/excel-analysis/SKILL.md`  
The `name` field uses title case (`Error Resolver`, `Excel Analysis`) while all other skills use kebab-case (`error-resolver`, `excel-analysis`). Inconsistent naming breaks predictable invocation patterns.

Fix:
```yaml
# error-resolver/SKILL.md
name: error-resolver

# excel-analysis/SKILL.md  
name: excel-analysis
```

### Q-07: `deepagent-memory-fold` embeds Windows absolute paths

**File**: `bundled/skills/deepagent-memory-fold/SKILL.md`  
The skill references `C:\Users\羽裳\.codex\_external\...` — a user-specific Windows absolute path embedded in a published skill. This path will not exist on any other machine. The skill is non-functional on Linux/macOS or for any other user.

### Q-08: `fluidsim` install command typo (`uv uv pip install`)

Already logged as BUG-01 above. Score impact: -2 points.

---

## Cross-Component Analysis

### Consistent patterns (strengths)

- **Scientific database skills are high-quality**: The genomics/bioinformatics/chemistry database skills (clinvar, gwas, opentargets, pubchem, clinicaltrials, alphafold, pdb) form a coherent, well-structured collection with excellent code examples, clear API documentation, and proper workflow organization. Most score 90/100.
- **ML/data skills are strong**: deepchem, dask, polars, vaex, timesfm all have good examples and clear "when to use" sections.
- **Speckit suite is coherent**: speckit-plan, speckit-specify, speckit-analyze, speckit-implement form a consistent 4-phase workflow with explicit handoffs. The skills cross-reference each other appropriately.

### Inconsistencies (weaknesses)

- **allowed-tools coverage gap**: Of 58 skills reviewed, only ~12 declare `allowed-tools`. The other 46 leave tool scope undefined. This inconsistency means some skills provide constraints the agent can respect while others provide none, creating unpredictable execution boundaries.

- **Language mixing**: Several skills (latex-submission-pipeline, report-generator, submission-checklist, video-studio, data-exploration-visualization) mix Chinese and English content, some primarily in Chinese. The repo appears to target English-speaking Claude Code users. Bilingual users will benefit, but English-only users may find these skills partially inaccessible.

- **AIOS suite depends on undeclared external runtime**: `aios-ux-design-expert`, `aios-devops`, and `aios-squad-creator` all depend on `.aios-core/` which is not bundled with this repo. This creates a hidden runtime dependency. The skills will not function out-of-the-box.

- **Commands lack empty-input handling**: All 7 commands fail to specify what to do when `$ARGUMENTS` is empty. This is a systematic omission across the entire command layer.

- **vibe skill proliferation without disambiguation**: There are 3 `vibe-implement` artifacts (one in `commands/`, one in `config/opencode/commands/`, one in `config/opencode/agents/`) with different schemas (Claude Code vs OpenCode format). No routing documentation explains when each is used.

---

## Recommendation

**Verdict: CONDITIONAL PASS** — The scientific skills core is production-quality; the vibe runtime layer has structural defects that should be fixed before endorsement.

**Do not contribute**: The 4 agent templates have zero frontmatter (structural defect), and the `autonomous-builder` skill's `--dangerously-skip-permissions` loop is a security concern requiring author clarification before any contribution.

**Quality fixes to propose** (if contributing):
1. Add `name` field to all 10 commands and opencode agents (~1 line each)
2. Fix `fluidsim` double-`uv` typo (1-line fix, clear correctness improvement)
3. Fix `error-resolver` and `excel-analysis` `name` casing

**Security fixes to propose** (only if author approves and `security-blocked` gate is not triggered):
1. Gate `--dangerously-skip-permissions` behind an explicit opt-in env var in `auto-continue.sh`
2. Add security notes to `curl | bash` examples in reference documentation

**Top-tier skills**: `timesfm-forecasting` (92), `ml-data-leakage-guard` (92), `sympy` (92), and the entire scientific database suite (90+) are exemplary and could be contributed as positive reference examples in NLPM rules.
