# NLPM Audit: Orchestra-Research/AI-Research-SKILLs
**Date**: 2026-04-12  |  **Artifacts**: 96  |  **Strategy**: progressive
**NL Score**: 89/100
**Security**: REVIEW
**Bugs**: 7  |  **Quality Issues**: 12  |  **Security Findings**: 4

## NL Score Summary

Scoring applied: -25 per missing required frontmatter field (name/description), -15 zero examples / -5 one example, -2 per vague quantifier (cap -20). All 95 SKILL.md files have both `name` and `description` frontmatter. No model declarations apply (skills, not agents). Vague-term deductions based on occurrence of "appropriate", "relevant", "suitable", "comprehensive", "foundational", "efficient" (non-technical use).

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| 03-fine-tuning/unsloth/SKILL.md | skill | 79 | Zero working examples in body (-15); placeholder text "will be added" (-6 vague) |
| 03-fine-tuning/llama-factory/SKILL.md | skill | 79 | Zero working examples in body (-15); placeholder text "will be added" (-6 vague) |
| 20-ml-paper-writing/ml-paper-writing/SKILL.md | skill | 78 | 983 lines (2× limit); est. 11 vague terms (-22, capped -20); no examples penalty N/A (has many) |
| 13-mlops/mlflow/SKILL.md | skill | 82 | 703 lines; est. 8 vague terms (-18) |
| 13-mlops/tensorboard/SKILL.md | skill | 82 | 630 lines; est. 8 vague terms (-18) |
| 16-prompt-engineering/instructor/SKILL.md | skill | 82 | 741 lines; est. 8 vague terms (-18) |
| 08-distributed-training/deepspeed/SKILL.md | skill | 82 | Very large file; est. 9 vague terms (-18) |
| 13-mlops/weights-and-biases/SKILL.md | skill | 84 | 590 lines; est. 8 vague terms (-16) |
| 16-prompt-engineering/outlines/SKILL.md | skill | 84 | 653 lines; est. 8 vague terms (-16) |
| CLAUDE.md | project-docs | 84 | Not a SKILL.md artifact; no frontmatter; est. 8 vague terms (-16) |
| 09-infrastructure/lambda-labs/SKILL.md | skill | 86 | 546 lines; est. 7 vague terms (-14) |
| 09-infrastructure/skypilot/SKILL.md | skill | 86 | 510 lines; est. 7 vague terms (-14) |
| 16-prompt-engineering/dspy/SKILL.md | skill | 86 | 591 lines; est. 7 vague terms (-14) |
| 16-prompt-engineering/guidance/SKILL.md | skill | 86 | 573 lines; est. 7 vague terms (-14) |
| 20-ml-paper-writing/presenting-conference-talks/SKILL.md | skill | 86 | Long; est. 7 vague terms (-14) |
| 18-multimodal/stable-diffusion/SKILL.md | skill | 86 | 520 lines; est. 7 vague terms (-14) |
| 18-multimodal/blip-2/SKILL.md | skill | 86 | 565 lines; est. 7 vague terms (-14) |
| 06-post-training/slime/SKILL.md | skill | 86 | 465 lines; est. 7 vague terms (-14) |
| 06-post-training/grpo-rl-training/SKILL.md | skill | 86 | 570 lines; est. 7 vague terms (-14) |
| 14-agents/a-evolve/SKILL.md | skill | 86 | 384 lines; est. 7 vague terms (-14) |
| 14-agents/llamaindex/SKILL.md | skill | 86 | 570 lines; est. 7 vague terms (-14) |
| 0-autoresearch-skill/SKILL.md | skill | 86 | Complex orchestration doc; est. 7 vague terms (-14) |
| 19-emerging-techniques/moe-training/SKILL.md | skill | 86 | 527 lines; est. 7 vague terms (-14) |
| 19-emerging-techniques/long-context/SKILL.md | skill | 86 | 535 lines; est. 7 vague terms (-14) |
| 14-agents/langchain/SKILL.md | skill | 88 | 480 lines; est. 6 vague terms (-12) |
| 14-agents/crewai/SKILL.md | skill | 88 | 499 lines; est. 6 vague terms (-12) |
| 14-agents/autogpt/SKILL.md | skill | 88 | 404 lines; est. 6 vague terms (-12) |
| 17-observability/phoenix/SKILL.md | skill | 88 | 476 lines; est. 6 vague terms (-12) |
| 11-evaluation/nemo-evaluator/SKILL.md | skill | 88 | Good; est. 6 vague terms (-12) |
| 05-data-processing/nemo-curator/SKILL.md | skill | 88 | Good; est. 6 vague terms (-12) |
| 12-inference-serving/vllm/SKILL.md | skill | 88 | 365 lines; est. 6 vague terms (-12) |
| 12-inference-serving/sglang/SKILL.md | skill | 88 | 441 lines; est. 6 vague terms (-12) |
| 13-mlops/swanlab/SKILL.md | skill | 88 | 407 lines; est. 6 vague terms (-12) |
| 03-fine-tuning/peft/SKILL.md | skill | 88 | 432 lines; est. 6 vague terms (-12) |
| 07-safety-alignment/nemo-guardrails/SKILL.md | skill | 88 | Good; est. 6 vague terms (-12) |
| 15-rag/pinecone/SKILL.md | skill | 88 | Good; est. 6 vague terms (-12) |
| 15-rag/sentence-transformers/SKILL.md | skill | 88 | Good; est. 6 vague terms (-12) |
| 15-rag/qdrant/SKILL.md | skill | 88 | Good; est. 6 vague terms (-12) |
| 19-emerging-techniques/model-merging/SKILL.md | skill | 88 | Good; est. 6 vague terms (-12) |
| 19-emerging-techniques/speculative-decoding/SKILL.md | skill | 88 | Good; est. 6 vague terms (-12) |
| 19-emerging-techniques/model-pruning/SKILL.md | skill | 88 | Good; est. 6 vague terms (-12) |
| 19-emerging-techniques/knowledge-distillation/SKILL.md | skill | 88 | Good; est. 6 vague terms (-12) |
| 06-post-training/torchforge/SKILL.md | skill | 88 | 434 lines; est. 6 vague terms (-12) |
| 06-post-training/trl-fine-tuning/SKILL.md | skill | 88 | 453 lines; est. 6 vague terms (-12) |
| 20-ml-paper-writing/academic-plotting/SKILL.md | skill | 88 | 480 lines; est. 6 vague terms (-12) |
| 18-multimodal/cosmos-policy/SKILL.md | skill | 88 | Good; est. 6 vague terms (-12) |
| 18-multimodal/segment-anything/SKILL.md | skill | 88 | Good; est. 6 vague terms (-12) |
| 18-multimodal/audiocraft/SKILL.md | skill | 88 | Good; est. 6 vague terms (-12) |
| 18-multimodal/openpi/SKILL.md | skill | 88 | Good; est. 6 vague terms (-12) |
| 18-multimodal/openvla-oft/SKILL.md | skill | 88 | 442 lines; est. 6 vague terms (-12) |
| 01-model-architecture/litgpt/SKILL.md | skill | 88 | 470 lines; est. 6 vague terms (-12) |
| 09-infrastructure/modal/SKILL.md | skill | 90 | 342 lines; est. 5 vague terms (-10) |
| 20-ml-paper-writing/systems-paper-writing/SKILL.md | skill | 90 | 271 lines; est. 5 vague terms (-10) |
| 02-tokenization/sentencepiece/SKILL.md | skill | 90 | Good; est. 5 vague terms (-10) |
| 02-tokenization/huggingface-tokenizers/SKILL.md | skill | 90 | Good; est. 5 vague terms (-10) |
| 18-multimodal/llava/SKILL.md | skill | 90 | Good; est. 5 vague terms (-10) |
| 18-multimodal/clip/SKILL.md | skill | 90 | Good; est. 5 vague terms (-10) |
| 18-multimodal/whisper/SKILL.md | skill | 90 | Good; est. 5 vague terms (-10) |
| 10-optimization/gguf/SKILL.md | skill | 90 | 428 lines; est. 5 vague terms (-10) |
| 10-optimization/hqq/SKILL.md | skill | 90 | 445 lines; est. 5 vague terms (-10) |
| 10-optimization/gptq/SKILL.md | skill | 90 | 451 lines; est. 5 vague terms (-10) |
| 06-post-training/verl/SKILL.md | skill | 90 | 391 lines; est. 5 vague terms (-10) |
| 06-post-training/miles/SKILL.md | skill | 90 | 315 lines; est. 5 vague terms (-10) |
| 01-model-architecture/torchtitan/SKILL.md | skill | 90 | 359 lines; est. 5 vague terms (-10) |
| 17-observability/langsmith/SKILL.md | skill | 90 | 423 lines; est. 5 vague terms (-10) |
| 11-evaluation/lm-evaluation-harness/SKILL.md | skill | 90 | Good; est. 5 vague terms (-10) |
| 11-evaluation/bigcode-evaluation-harness/SKILL.md | skill | 90 | Good; est. 5 vague terms (-10) |
| 04-mechanistic-interpretability/saelens/SKILL.md | skill | 90 | Good; est. 5 vague terms (-10) |
| 05-data-processing/ray-data/SKILL.md | skill | 90 | Good; est. 5 vague terms (-10) |
| 21-research-ideation/creative-thinking-for-research/SKILL.md | skill | 90 | 367 lines; est. 5 vague terms (-10) |
| 21-research-ideation/brainstorming-research-ideas/SKILL.md | skill | 90 | 385 lines; est. 5 vague terms (-10) |
| 08-distributed-training/pytorch-lightning/SKILL.md | skill | 90 | 345 lines; est. 5 vague terms (-10) |
| 08-distributed-training/megatron-core/SKILL.md | skill | 90 | 367 lines; est. 5 vague terms (-10) |
| 08-distributed-training/ray-train/SKILL.md | skill | 90 | 405 lines; est. 5 vague terms (-10) |
| 07-safety-alignment/llamaguard/SKILL.md | skill | 90 | Good; est. 5 vague terms (-10) |
| 07-safety-alignment/constitutional-ai/SKILL.md | skill | 90 | Good; est. 5 vague terms (-10) |
| 07-safety-alignment/prompt-guard/SKILL.md | skill | 90 | Good; est. 5 vague terms (-10) |
| 15-rag/chroma/SKILL.md | skill | 90 | Good; est. 5 vague terms (-10) |
| 15-rag/faiss/SKILL.md | skill | 90 | Good; est. 5 vague terms (-10) |
| 03-fine-tuning/axolotl/SKILL.md | skill | 90 | 159 lines; examples present; est. 5 vague terms (-10) |
| 10-optimization/bitsandbytes/SKILL.md | skill | 92 | 412 lines; est. 4 vague terms (-8) |
| 10-optimization/ml-training-recipes/SKILL.md | skill | 92 | 320 lines; est. 4 vague terms (-8) |
| 10-optimization/flash-attention/SKILL.md | skill | 92 | 368 lines; est. 4 vague terms (-8) |
| 10-optimization/awq/SKILL.md | skill | 92 | 311 lines; est. 4 vague terms (-8) |
| 04-mechanistic-interpretability/nnsight/SKILL.md | skill | 92 | Good; est. 4 vague terms (-8) |
| 04-mechanistic-interpretability/pyvene/SKILL.md | skill | 92 | Good; est. 4 vague terms (-8) |
| 04-mechanistic-interpretability/transformer-lens/SKILL.md | skill | 92 | Good; est. 4 vague terms (-8) |
| 08-distributed-training/accelerate/SKILL.md | skill | 92 | 333 lines; est. 4 vague terms (-8) |
| 01-model-architecture/nanogpt/SKILL.md | skill | 94 | 290 lines; est. 3 vague terms (-6) |
| 08-distributed-training/pytorch-fsdp2/SKILL.md | skill | 94 | 232 lines; est. 3 vague terms (-6) |
| 12-inference-serving/llama-cpp/SKILL.md | skill | 94 | 257 lines; est. 3 vague terms (-6) |
| 01-model-architecture/mamba/SKILL.md | skill | 96 | 260 lines; est. 2 vague terms (-4) |
| 01-model-architecture/rwkv/SKILL.md | skill | 96 | 259 lines; est. 2 vague terms (-4) |
| 06-post-training/openrlhf/SKILL.md | skill | 96 | 247 lines; est. 2 vague terms (-4) |
| 12-inference-serving/tensorrt-llm/SKILL.md | skill | 96 | 186 lines; clean; est. 2 vague terms (-4) |
| 06-post-training/simpo/SKILL.md | skill | 98 | 220 lines; minimal vague language; est. 1 term (-2) |

---

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 1 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks | 0 (none found) |
| Scripts (.py) | 5 (grpo examples + demo figures) |
| Scripts (.sh) | 0 |
| JS executables | 6 (packages/ai-research-skills/src/*.js, bin/cli.js) |
| MCP configs | 0 |
| Root package.json | 1 (no dependencies, harmless test script) |
| Package manifest | packages/ai-research-skills/package.json |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | packages/ai-research-skills/src/installer.js | 74, 187, 719, 795 | subprocess (execSync) | `execSync` with shell interpolation — URL is hardcoded constant but template-literal pattern is injectable if REPO_URL ever becomes user-controlled; `execSync` routes via `/bin/sh` on POSIX by default |
| 2 | Medium | packages/ai-research-skills/src/installer.js | 9–10 | file writes outside repo | Writes to `~/.orchestra/skills/` and `~/.orchestra/.lock.json` — modifies user home directory on every install/update |
| 3 | Medium | demos/scientific-plotting-demo/figures/gen_fig_andes_architecture_gemini.py | 19–38 | .env read + network call | Reads `.env` file and forwards `GEMINI_API_KEY` to Google Gemini API; no rate-limit or error boundary |
| 4 | Low | packages/ai-research-skills/package.json | 43–47 | unpinned dependencies | `chalk: ^5.3.0`, `inquirer: ^9.2.12`, `ora: ^8.0.1` use caret ranges — minor/patch updates apply automatically without explicit review |

---

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | CLAUDE.md | `01-model-architecture/` lists "Megatron-Core" but actual skill is `torchtitan/` — Megatron-Core lives in `08-distributed-training/` | Confuses contributors looking for torchtitan; misdirects to wrong category |
| 2 | CLAUDE.md | `13-mlops/` states 3 skills (W&B, MLflow, TensorBoard) but SwanLab (`swanlab/SKILL.md`) exists as the 4th | New contributors won't know SwanLab is maintained; skill invisible in documentation |
| 3 | CLAUDE.md | `14-agents/` states 4 skills (LangChain, LlamaIndex, CrewAI, AutoGPT) but A-Evolve (`a-evolve/SKILL.md`) exists as the 5th | A-Evolve is undocumented in CLAUDE.md; invisible to contributors |
| 4 | CLAUDE.md | `18-multimodal/` states 7 skills but cosmos-policy, openpi, and openvla-oft exist as additional 3 | 3 multimodal skills invisible in project documentation |
| 5 | CLAUDE.md | `20-ml-paper-writing/` states 1 skill but systems-paper-writing, academic-plotting, and presenting-conference-talks exist as 3 additional | 3 paper-writing skills invisible in project documentation |
| 6 | CLAUDE.md | `10-optimization/` states 6 skills but ml-training-recipes (`ml-training-recipes/SKILL.md`) exists as the 7th | ml-training-recipes skill invisible in project documentation |
| 7 | CLAUDE.md | Skill count discrepancy — "86 Skills Across 22 Categories" vs "87 skills achieved" (ROADMAP reference); actual count is ~95 SKILL.md files | Automation that reads category counts from CLAUDE.md will report wrong totals |

---

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | packages/ai-research-skills/src/installer.js:74 | `execSync` with string interpolation — safe today but fragile pattern | Replace with `spawnSync('git', ['clone', '--depth', '1', `${REPO_URL}.git`, tempDir], { stdio: 'pipe' })` to eliminate shell interpolation entirely |
| 2 | packages/ai-research-skills/src/installer.js:9 | Writes to user home outside project | Document the `~/.orchestra/` write path in README and `--help` output so users are aware of the side-effect |
| 3 | demos/scientific-plotting-demo/figures/gen_fig_andes_architecture_gemini.py:19 | Reads `.env` file with manual parser — may leak extra vars if format unexpected | Use `python-dotenv` library for `.env` parsing, or add explicit key-allowlist |
| 4 | packages/ai-research-skills/package.json:43 | Caret ranges allow automatic dependency updates | Pin exact versions (`"chalk": "5.3.0"`) or add `npm audit` to CI |

---

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | 03-fine-tuning/unsloth/SKILL.md | Auto-generated stub; body is entirely placeholder — "Quick reference patterns will be added as you use the skill." No real usage examples | -15 (zero examples) |
| 2 | 03-fine-tuning/llama-factory/SKILL.md | Auto-generated stub; identical placeholder structure to unsloth with no working code examples | -15 (zero examples) |
| 3 | 20-ml-paper-writing/ml-paper-writing/SKILL.md | 983 lines — nearly 2× the 500-line performance guideline; should be split into reference files | -20 vague cap exceeded |
| 4 | 16-prompt-engineering/instructor/SKILL.md | 741 lines — 48% over guideline | -18 (vague) |
| 5 | 13-mlops/mlflow/SKILL.md | 703 lines — 40% over guideline | -18 (vague) |
| 6 | 16-prompt-engineering/outlines/SKILL.md | 653 lines — 30% over guideline | -16 (vague) |
| 7 | 13-mlops/tensorboard/SKILL.md | 630 lines — 26% over guideline | -18 (vague) |
| 8 | 08-distributed-training/deepspeed/SKILL.md | Very large file (reported ~141 KB); far exceeds 500-line guidance | -18 (vague) |
| 9 | 13-mlops/weights-and-biases/SKILL.md | 590 lines | -16 (vague) |
| 10 | 03-fine-tuning/axolotl/SKILL.md | Auto-generated template; uses generic `view` command (non-existent tool) in guidance at line 117: "Use `view` to read specific reference files" | Informational |
| 11 | 03-fine-tuning/unsloth/SKILL.md | Same `view` command reference at line 36 | Informational |
| 12 | 03-fine-tuning/llama-factory/SKILL.md | Same `view` command reference at line 38 | Informational |

---

## Cross-Component

**CLAUDE.md accuracy**: Multiple categories in the CLAUDE.md skill inventory are stale, listing the wrong skill names or wrong counts (see Bugs section). The discrepancy between the documented skill count (86–87) and actual count (~95) suggests the CLAUDE.md was last updated before the multimodal, paper-writing, and emerging-technique expansions.

**Orphaned skills**: cosmos-policy, openpi, openvla-oft (18-multimodal), systems-paper-writing, academic-plotting, presenting-conference-talks (20-ml-paper-writing), ml-training-recipes (10-optimization), a-evolve (14-agents), and swanlab (13-mlops) are all valid, well-formed skills not reflected in CLAUDE.md's category listings. They are not orphaned from a registration standpoint — their SKILL.md files are complete — but they are invisible to contributors reading the project overview.

**Stub skills (unsloth, llama-factory, axolotl)**: Three auto-generated stubs contrast with the hand-crafted quality of the rest of the library. The stub template uses `view` as if it were a tool, but `view` is not a standard Claude Code built-in; agents will not be able to follow that instruction. The reference files they point to (`references/llms-txt.md`, `references/getting_started.md`, etc.) may provide the actual content, but the SKILL.md gateway is non-functional for in-context use without those files.

**Consistency**: All other SKILL.md files consistently use the same YAML frontmatter schema, follow progressive disclosure (SKILL.md + references/), and include when-to-use vs alternatives tables. The overall library is architecturally coherent.

---

## Recommendation

REVIEW — submit NL fix PRs for all 7 CLAUDE.md bugs (category inventory corrections). Flag the four security findings in a GitHub issue for maintainer awareness — all are Medium or Low and do not block contribution. The three stub skills (unsloth, llama-factory, axolotl) warrant content-filling PRs; the auto-generated SKILL.md bodies provide no practical guidance to agents. Over-length files (ml-paper-writing at 983 lines, deepspeed at ~141 KB) should be refactored to move deep content into reference files per the 500-line guideline.
