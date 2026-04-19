# NLPM Audit: htdt/godogen
**Date**: 2026-04-19  |  **Artifacts**: 6  |  **Strategy**: single
**NL Score**: 91/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 15  |  **Security Findings**: 6

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| claude/skills/godogen/SKILL.md | skill (orchestrator) | 84 | No output format; 3 vague quantifiers |
| codex/skills/godogen/SKILL.md | skill (orchestrator) | 86 | No output format; 2 vague quantifiers |
| claude/skills/godot-api/SKILL.md | skill (lookup/fork) | 93 | Implicit but unstructured output format |
| codex/skills/godot-api/SKILL.md | skill (lookup) | 91 | Implicit output format; 2 vague quantifiers |
| claude/skills/visual-qa/SKILL.md | skill (QA/fork) | 93 | No model declared on context:fork |
| codex/skills/visual-qa/SKILL.md | skill (QA) | 98 | One vague quantifier |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 5 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Scripts (Python) | claude/skills/godogen/tools/asset_gen.py, claude/skills/godogen/tools/tripo3d.py, claude/skills/godogen/tools/rembg_matting.py, claude/skills/godogen/tools/grid_slice.py, claude/skills/godogen/tools/find_loop_frame.py, claude/skills/godot-api/tools/class_list.py, claude/skills/godot-api/tools/godot_api_converter.py, claude/skills/visual-qa/scripts/visual_qa.py + 8 identical codex/ mirrors |
| Scripts (Shell) | claude/publish.sh, claude/skills/godot-api/tools/ensure_doc_api.sh + 2 codex/ mirrors |
| Hooks | None |
| MCP configs | None |
| Package manifests | None found (no requirements.txt, package.json) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | claude/skills/godogen/tools/asset_gen.py | 158, 195, 271 | network calls | Outbound HTTP to Gemini, xAI Grok, and Tripo3D APIs via `requests` and SDK clients. Expected and documented; API keys sourced from environment. Identical in codex variant. |
| 2 | Medium | claude/skills/godogen/tools/tripo3d.py | 24–26, 37, 43 | env var + network | `os.environ.get("TRIPO3D_API_KEY")` read at call time; used in `Authorization: Bearer` header for all Tripo3D API calls (`requests.post/get`). Key never logged. Identical in codex variant. |
| 3 | Medium | claude/skills/godogen/tools/rembg_matting.py | 43–46 | subprocess | `subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"], ...)` — fixed argument list, `capture_output=True`, no `shell=True`. Runtime GPU probe only. Identical in codex variant. |
| 4 | Medium | claude/skills/visual-qa/scripts/visual_qa.py | 141–148 | network + env | `genai.Client()` reads `GEMINI_API_KEY` or `GOOGLE_API_KEY` from environment; sends images to Gemini API over HTTPS. `--model` flag accepts caller-supplied model name but is validated by the API server. Identical in codex variant. |
| 5 | Medium | claude/skills/godot-api/tools/ensure_doc_api.sh | 21–23 | network fetch | `git clone --depth 1 https://github.com/godotengine/godot.git` — clones from a hardcoded upstream GitHub URL. No user input; runs only when `doc_api/` is absent. Identical in codex variant. |
| 6 | Low | (repo-wide) | — | no pinned deps | No `requirements.txt` found. Scripts import `google-genai`, `requests`, `xai-sdk`, `rembg`, `Pillow`, `numpy`, `onnxruntime` without version pins. Supply-chain risk if a future install picks a broken or compromised version. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No bugs detected | All required frontmatter present; no broken cross-references in the six SKILL.md files |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | claude/ + codex/ skills | No pinned dependency versions | Add `requirements.txt` (or `pyproject.toml`) with pinned versions for `google-genai`, `requests`, `xai-sdk`, `rembg`, `Pillow`, `numpy`, `onnxruntime`. Lock with `pip-compile` or equivalent. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | claude/skills/godogen/SKILL.md | No output format — orchestrator defines a pipeline but no terminal response shape for callers | -10 |
| 2 | claude/skills/godogen/SKILL.md | Vague quantifier: "concise" (line 48 "concise plan summary") | -2 |
| 3 | claude/skills/godogen/SKILL.md | Vague quantifier: "small" (line 101 "small, targeted changes") | -2 |
| 4 | claude/skills/godogen/SKILL.md | Vague quantifier: "major" (line 102 "after major changes") | -2 |
| 5 | claude/skills/godot-api/SKILL.md | No structured output format template; response guidance is prose only ("return relevant methods…") | -5 |
| 6 | claude/skills/godot-api/SKILL.md | Vague quantifier: "relevant" (line 4 "return relevant methods/signals") | -2 |
| 7 | claude/skills/visual-qa/SKILL.md | `context: fork` declared but no `model` field — forked context will inherit caller's model rather than using a cost-appropriate tier | -5 |
| 8 | claude/skills/visual-qa/SKILL.md | Vague quantifier: "acceptable" (output format section "acceptable…limitations") | -2 |
| 9 | codex/skills/godogen/SKILL.md | No output format — same issue as claude variant | -10 |
| 10 | codex/skills/godogen/SKILL.md | Vague quantifier: "concise" (line 51 "concise plan summary") | -2 |
| 11 | codex/skills/godogen/SKILL.md | Vague quantifier: "major" (line 102 "after major changes") | -2 |
| 12 | codex/skills/godot-api/SKILL.md | No structured output format template | -5 |
| 13 | codex/skills/godot-api/SKILL.md | Vague quantifier: "relevant" (line 20 "return the relevant methods") | -2 |
| 14 | codex/skills/godot-api/SKILL.md | Vague quantifier: "targeted" (line 9 "Keep answers targeted to the caller's question") | -2 |
| 15 | codex/skills/visual-qa/SKILL.md | Vague quantifier: "acceptable" (output format section) | -2 |

## Cross-Component

**claude/ tree:** `godogen` references `visual-qa.md`, `task-execution.md`, `quirks.md`, and other sub-files via `${CLAUDE_SKILL_DIR}/` — runtime-resolved, consistent with publish.sh output layout. `godogen` invokes `godot-api` skill via `Skill(skill="godot-api")` — skill exists in same tree. `visual-qa` SKILL.md references `${CLAUDE_SKILL_DIR}/scripts/visual_qa.py` — file present at `claude/skills/visual-qa/scripts/visual_qa.py`. No broken references.

**codex/ tree:** `godogen` uses hardcoded `.agents/skills/godogen/...` paths (intentional — Codex runtime has no env-var equivalent of `${CLAUDE_SKILL_DIR}`). `godot-api` references `.agents/skills/godot-api/doc_api/` — bootstrapped at runtime by `ensure_doc_api.sh`. `visual-qa` references `.agents/skills/visual-qa/scripts/visual_qa.py` — present. No broken references.

**Cross-variant:** The two trees are intentionally divergent (CLAUDE.md: "Do not align the behavior across both variants unless asked"). Notable asymmetry: `claude/skills/godot-api/SKILL.md` declares `context: fork` and `model: sonnet` + `agent: Explore`; `codex/skills/godot-api/SKILL.md` omits these entirely — consistent with Codex running doc lookups inline or via a plain helper agent rather than a forked Claude context.

## Recommendation

CLEAR — submit PRs for all bugs and medium/low security fixes.

No critical or high security findings. The single actionable PR is adding a `requirements.txt` with pinned dependency versions (security finding #6). All NL quality issues are informational; highest-impact improvements are adding a terminal output format to the two `godogen` orchestrator skills and a `model:` field to `claude/skills/visual-qa/SKILL.md`.
