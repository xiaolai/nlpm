---
slug: huggingface-skills
repo: huggingface/skills
audited: 2026-07-05
commit_sha: 4948baec814c92edd91024b76d8c2ffa6df4eb70
score: 96
exemplifies:
  - R04
  - R05
  - R06
  - R07
  - R08
---

# Exemplar: huggingface/skills

**Score**: 96/100  |  **Date**: 2026-07-05  |  **Commit**: `4948baec814c92edd91024b76d8c2ffa6df4eb70`

A 19-skill collection covering Hugging Face Hub workflows (CLI, Spaces, dataset viewer, training, papers); each `SKILL.md` stays short by pushing depth into per-skill `references/*.md` files linked from a trailing index table.

## Per-rule evidence

### R04 — Description is a trigger, not a summary

`hf-cli`'s frontmatter packs both positive and negative trigger conditions plus an explicit override for the case where the user doesn't name the tool.

> Real quote from `skills/hf-cli/SKILL.md:3`:
>
> ```
> description: "Hugging Face Hub CLI (`hf`) for downloading, uploading, and managing models, datasets, spaces, buckets, repos, papers, jobs, and more on the Hugging Face Hub. Use when: handling authentication; managing local cache; managing Hugging Face Buckets; running or scheduling jobs on Hugging Face infrastructure; managing Hugging Face repos; discussions and pull requests; browsing models, datasets and spaces; reading, searching, or browsing academic papers; managing collections; querying datasets; configuring spaces; setting up webhooks; or deploying and managing HF Inference Endpoints. Make sure to use this skill whenever the user mentions 'hf', 'huggingface', 'Hugging Face', 'huggingface-cli', or 'hugging face cli', or wants to do anything related to the Hugging Face ecosystem and to AI and ML in general. Also use for cloud storage needs like training checkpoints, data pipelines, or agent traces. Use even if the user doesn't explicitly ask for a CLI command. Replaces the deprecated `huggingface-cli`."
> ```

This isn't a one-line summary — it enumerates 14 distinct trigger scenarios plus a fallback ("even if the user doesn't explicitly ask") and a migration note (`huggingface-cli` → `hf`), so the router can match on symptom ("PicklingError") as well as on tool name.

### R05 — Under 500 lines

Three of the audited SKILL.md files stay well under the 500-line ceiling by delegating depth to `references/`, rather than inlining everything:

| File | Lines |
|---|---|
| `skills/huggingface-spaces/SKILL.md` | 230 |
| `skills/huggingface-local-models/SKILL.md` | 113 |
| `skills/huggingface-datasets/SKILL.md` | 107 |

> Real quote from `skills/huggingface-spaces/SKILL.md:219-230` (the file's closing section):
>
> ```
> ## Reference index
>
> | When to read | File |
> |---|---|
> | **How ZeroGPU works** + correct patterns (decorator, sizing, pickle, generators, real-time, AoTI) | [`references/zerogpu.md`](references/zerogpu.md) |
> | **Iterate + debug**: logs, rung ladder, smoke testing (and dev mode + SSH as a last resort) | [`references/debugging.md`](references/debugging.md) |
> | **Error-string lookup** — the single place for all error symptoms (Spaces, ZeroGPU, Gradio, deps) | [`references/known-errors.md`](references/known-errors.md) |
> ```

The split isn't arbitrary — each reference file is named for the failure mode it resolves (`known-errors.md`, `debugging.md`, `zerogpu.md`), so the agent can jump straight to the right file instead of re-reading the whole skill.

### R06 — Code examples must be runnable

`huggingface-spaces` gives a complete, pasteable ZeroGPU app rather than a pseudocode sketch:

> Real quote from `skills/huggingface-spaces/SKILL.md:119-132`:
>
> ```python
> import spaces           # MUST come before torch / diffusers / transformers
> import torch
> import gradio as gr
> from diffusers import DiffusionPipeline
>
> pipe = DiffusionPipeline.from_pretrained("<repo>", torch_dtype=torch.bfloat16).to("cuda")
>
> @spaces.GPU(duration=60)
> def generate(prompt):
>     return pipe(prompt).images[0]
>
> gr.Interface(fn=generate, inputs=gr.Text(), outputs=gr.Image()).launch()
> ```

Every import and decorator here is real, versioned API (`spaces.GPU`, `diffusers.DiffusionPipeline`) — copy-paste runs, it doesn't need translation from placeholder names first.

### R07 — Scope note when related skills exist

Two independent skills point to the same companion skill by its real, correct name (unlike the `hugging-face-jobs` dead-end reference flagged elsewhere in this same audit — see the audit report's Bugs #1–4 for the failure mode this rule prevents):

> Real quote from `skills/huggingface-spaces/SKILL.md:18`:
>
> ```
> The `hf-cli` skill teaches an agent every `hf` command and is the recommended companion to this one. Install it with `hf skills add hf-cli` (add `--claude --global` to install for Claude Code as well, user-level).
> ```

> Real quote from `skills/huggingface-datasets/SKILL.md:56`:
>
> ```
> For CLI-based parquet URL discovery or SQL, use the `hf-cli` skill with `hf datasets parquet` and `hf datasets sql`.
> ```

Both references resolve — `skills/hf-cli/SKILL.md` exists in the repo — which is exactly what separates a working scope note from the stale `hugging-face-jobs` references the audit flagged as bugs in `huggingface-vision-trainer` and `huggingface-community-evals`.

### R08 — Patterns over theory

`huggingface-spaces` opens with a numbered situational checklist instead of explaining what a Space "is" in the abstract first:

> Real quote from `skills/huggingface-spaces/SKILL.md:10-18`:
>
> ```
> ## 0. Getting ready
>
> Before anything else:
>
> 1. Check the `hf` CLI is installed: `which hf`. If not, `pip install -U huggingface_hub`.
> 2. Check the user is logged in: `hf auth whoami`. If not, ask them to run `! hf auth login` in this session — they'll need a write-scoped token from https://huggingface.co/settings/tokens.
> 3. Note `whoami`'s `canPay` and `isPro` flags — they gate hardware choices below.
> ```

Each numbered step is an action with a concrete command and a branch ("If not, ..."), not a description of what authentication is — the agent has enough to execute the step without further reasoning.

## Worth adopting

Pattern: Load-triggered reference index. Evidence: `skills/huggingface-spaces/SKILL.md:219-230` (quoted under R05). Why it would be a useful rule: when a skill splits into scoped reference files (per R05), a closing table mapping situation → file lets the agent pick the right reference on the first read instead of opening several candidates to find the relevant one — the current rules cover *that* splitting should happen (R05) but not how the split files should be indexed for retrieval.
