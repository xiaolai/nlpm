# NLPM Audit: huggingface/skills
**Date**: 2026-04-06  |  **Artifacts**: 21  |  **Strategy**: batched
**NL Score**: 96/100
**Security**: REVIEW
**Bugs**: 4  |  **Quality Issues**: 13  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/huggingface-vision-trainer/SKILL.md | SKILL.md | 76 | Stale references to nonexistent skill `hugging-face-jobs` / `hugging-face-model-trainer` (R37 ×2) |
| skills/huggingface-community-evals/SKILL.md | SKILL.md | 88 | Stale reference to nonexistent skill `hugging-face-jobs` (R37) |
| skills/transformers-js/SKILL.md | SKILL.md | 90 | Vague quantifiers (×5) |
| skills/huggingface-llm-trainer/SKILL.md | SKILL.md | 92 | Vague quantifiers (×4) |
| skills/huggingface-lora-space-builder/SKILL.md | SKILL.md | 92 | Vague quantifiers (×4) |
| skills/huggingface-paper-publisher/SKILL.md | SKILL.md | 94 | Vague quantifiers (×3) |
| skills/huggingface-zerogpu/SKILL.md | SKILL.md | 94 | Vague quantifiers (×3) |
| skills/huggingface-best/SKILL.md | SKILL.md | 94 | Vague quantifiers (×3) |
| skills/huggingface-tool-builder/SKILL.md | SKILL.md | 96 | Vague quantifiers (×2) |
| skills/trl-training/SKILL.md | SKILL.md | 96 | Vague quantifiers (×2) |
| skills/huggingface-gradio/SKILL.md | SKILL.md | 98 | Vague quantifiers (×1) |
| skills/huggingface-trackio/SKILL.md | SKILL.md | 98 | Vague quantifiers (×1) |
| skills/hf-cli/SKILL.md | SKILL.md | 98 | Vague quantifiers (×1) |
| skills/huggingface-local-models/SKILL.md | SKILL.md | 100 | None |
| skills/huggingface-papers/SKILL.md | SKILL.md | 100 | None |
| skills/hf-mem/SKILL.md | SKILL.md | 100 | None |
| skills/huggingface-datasets/SKILL.md | SKILL.md | 100 | None |
| skills/train-sentence-transformers/SKILL.md | SKILL.md | 100 | None |
| skills/huggingface-spaces/SKILL.md | SKILL.md | 100 | None |
| hf-mcp/skills/hf-mcp/SKILL.md | SKILL.md | 100 | None |
| .claude-plugin/plugin.json | plugin manifest | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts (top-level `scripts/`) | 9 (`.py` ×6, `.sh` ×1, `.md` ×2 docs, not executable) |
| Scripts (per-skill `scripts/` + `references/*.sh`) | 38 (`.py` training/eval/inspection scripts, `.sh` reference examples) |
| MCP configs | 1 (`.mcp.json` — single `http` server, `huggingface.co/mcp?login`) |
| Package manifests | 0 (`package.json` / `requirements.txt` — none present) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | Medium | skills/hf-cli/SKILL.md | 6 | curl-pipe-sh | Install instruction pipes `curl -LsSf https://hf.co/cli/install.sh` directly into `bash -s`; first-party `hf.co` domain, official CLI installer, not auto-executed by any hook |
| 2 | Medium | skills/hf-cli/SKILL.md | 225 | curl-pipe-sh | Install instruction pipes `curl -fsSL https://raw.githubusercontent.com/huggingface/hf-mount/main/install.sh` into `sh`; first-party `huggingface` GitHub org, same pattern as #1 |
| 3 | Low | skills/train-sentence-transformers/references/hf_jobs_execution.md | 9 | curl-pipe-sh | Duplicate reference to the same `hf.co/cli/install.sh \| bash -s` one-liner from finding #1 |

No credential exfiltration, reverse shells, `eval`/`exec` misuse, `shell=True` subprocess calls, or `os.system` calls were found in any of the 47 script files. All `subprocess.run()` calls in the per-skill scripts (`inspect_eval_uv.py`, `lighteval_vllm_uv.py`, `inspect_vllm_uv.py`, `convert_to_gguf.py`) use list-form argv with no `shell=True`, built from local argparse values — no injection path found. `.mcp.json` registers a single scoped `http` MCP server against the first-party `huggingface.co` domain — not a broad-permissions grant.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | skills/huggingface-vision-trainer/SKILL.md | Lines 24–25, 246, 363 reference a skill named `hugging-face-jobs` and a skill named `hugging-face-model-trainer` — neither exists anywhere in the repo (verified: no `skills/*jobs*` or `skills/*model-trainer*` directory; the actual HF-Jobs/TRL-training skill is `huggingface-llm-trainer`) | Agent hand-off instructions for "how do secrets work / hardware / tokens" and for language-model training point to a dead end; the agent cannot locate the named skill |
| 2 | skills/huggingface-vision-trainer/references/hub_saving.md | Line 257 references the same nonexistent `hugging-face-jobs` skill | Same dead-end hand-off for the token usage guide |
| 3 | skills/huggingface-community-evals/SKILL.md | Lines 24, 53, 67, 147, 182, 192 all reference a skill named `hugging-face-jobs`, which does not exist in the repo | Every "hand off to remote/Jobs execution" instruction in this skill is a dead end |
| 4 | skills/huggingface-community-evals/examples/USAGE_EXAMPLES.md | Lines 20, 101 reference the same nonexistent `hugging-face-jobs` skill | Same dead-end hand-off reproduced in the examples file |

## Security Fixes (PR-worthy, Medium/Low only)
No Medium/Low security fixes are recommended. All three curl-pipe-sh findings are standard first-party CLI installer one-liners (`hf.co` and the `huggingface` GitHub org) documented as manual install steps, not auto-executed automation — the same pattern used by `rustup`, `uv`, and most modern CLI tools. Rewriting them would not reduce real risk and would diverge from upstream Hugging Face documentation conventions.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/transformers-js/SKILL.md | R01 vague quantifiers ×5 ("suitable", "some", "typically", "several" ×2) | -10 |
| 2 | skills/huggingface-llm-trainer/SKILL.md | R01 vague quantifiers ×4 | -8 |
| 3 | skills/huggingface-lora-space-builder/SKILL.md | R01 vague quantifiers ×4 | -8 |
| 4 | skills/huggingface-paper-publisher/SKILL.md | R01 vague quantifiers ×3 | -6 |
| 5 | skills/huggingface-zerogpu/SKILL.md | R01 vague quantifiers ×3 | -6 |
| 6 | skills/huggingface-best/SKILL.md | R01 vague quantifiers ×3 | -6 |
| 7 | skills/huggingface-tool-builder/SKILL.md | R01 vague quantifiers ×2 | -4 |
| 8 | skills/trl-training/SKILL.md | R01 vague quantifiers ×2 | -4 |
| 9 | skills/huggingface-gradio/SKILL.md | R01 vague quantifier ×1 | -2 |
| 10 | skills/huggingface-trackio/SKILL.md | R01 vague quantifier ×1 | -2 |
| 11 | skills/hf-cli/SKILL.md | R01 vague quantifier ×1 | -2 |
| 12 | skills/huggingface-vision-trainer/SKILL.md | R01 vague quantifiers ×2 (in addition to the R37 stale references above) | -4 |
| 13 | skills/huggingface-community-evals/SKILL.md | R01 vague quantifier ×1 (in addition to the R37 stale reference above) | -2 |

## Cross-Component
1. **Stale skill references** (see Bugs #1–4): four files across two skills point to a skill named `hugging-face-jobs` (and one to `hugging-face-model-trainer`) that doesn't exist under `skills/`. The likely intended target is `huggingface-llm-trainer`, which is the repo's actual TRL/HF-Jobs training skill and matches the described scope ("General HF Jobs infrastructure... TRL-based language model training (SFT, DPO, GRPO)").
2. **`.claude-plugin/marketplace.json` contradicts `skills/huggingface-community-evals/SKILL.md`'s own stated scope.** `marketplace.json` line 39 (propagated into `README.md`'s auto-generated table by `scripts/generate_agents.py`, which sources descriptions from `marketplace.json` over SKILL.md frontmatter) describes the skill as "Add and manage evaluation results in Hugging Face model cards... importing scores from Artificial Analysis API." The SKILL.md itself explicitly states: "It does **not** cover:... model-card or `model-index` edits... Artificial Analysis imports... PR creation or community-evals automation." These are direct opposites of the same skill's scope.
3. **`.claude-plugin/marketplace.json` references a nonexistent tool.** Line 75 describes `huggingface-datasets` as covering "SQL via parquetlens." A repo-wide search for `parquetlens` finds it only in `marketplace.json` and the generated `README.md` table — never in `skills/huggingface-datasets/SKILL.md`, which instead documents `hf datasets sql` (DuckDB via the `hf` CLI).
4. **`.claude-plugin/marketplace.json` understates `huggingface-vision-trainer`'s scope.** Line 99 describes only object detection and image classification; the actual SKILL.md dedicates roughly a third of its content to SAM/SAM2 segmentation training (dataset requirements, script, hardware guidance), which is omitted entirely from the marketplace/README description.
5. No orphaned skill directories were found — all 19 `skills/*/SKILL.md` plus `hf-mcp/skills/hf-mcp/SKILL.md` are represented in `marketplace.json`'s plugin list (per `scripts/generate_agents.py`'s own `validate_marketplace()` check, which this audit spot-verified for the affected skills).
6. All `scripts/`, `references/`, and template-file paths referenced from the 20 SKILL.md files' own bodies resolve to real files on disk — the stale-reference problem here is specifically cross-skill name references (pointing at *other skills*), not missing local files.

## Recommendation
REVIEW — submit NL fix PRs for the four stale `hugging-face-jobs` / `hugging-face-model-trainer` references (Bugs #1–4) and the three marketplace.json/README description drifts (Cross-Component #2–4); flag the curl-pipe-sh security findings in the tracking issue as informational only (no action recommended, see Security Fixes).
