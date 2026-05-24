# NLPM Audit: Yuan1z0825/nature-skills
**Date**: 2026-05-24  |  **Artifacts**: 10  |  **Strategy**: single
**NL Score**: 93/100
**Security**: REVIEW
**Bugs**: 1  |  **Quality Issues**: 12  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/nature-academic-search/SKILL.md | skill | 86 | Missing output format (−10); vague "broad"/"results may vary" (−4) |
| skills/nature-figure/SKILL.md | skill | 86 | Missing output format (−10); vague "high-impact"/"similar venues" (−4) |
| .claude-plugin/plugin.json | manifest | 90 | Stale description — 4 shipped skills absent from description text |
| skills/nature-citation/SKILL.md | skill | 92 | Vague "roughly"/"about"/"usually"/"useful" (−8) |
| skills/nature-writing/SKILL.md | skill | 92 | Vague "ambitious"/"concise"/"material"/"compact" (−8) |
| skills/nature-paper2ppt/SKILL.md | skill | 94 | Vague "usually"/"useful"/"concise" (−6) |
| skills/nature-data/SKILL.md | skill | 96 | Vague "reasonable"/"suitable" (−4) |
| skills/nature-reader/SKILL.md | skill | 96 | Vague "relevant"/"clearly" (−4) |
| skills/nature-response/SKILL.md | skill | 96 | Vague "concise"/"long" (−4) |
| skills/nature-polishing/SKILL.md | skill | 98 | Vague "clearly" (−2) |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 1 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Shell scripts | skills/nature-academic-search/install.sh |
| Python scripts | skills/nature-academic-search/scripts/format-converter.py, scripts/preflight.py, scripts/converters.py; skills/nature-academic-search/mcp-server/academic_search_server.py, mcp-server/sources/crossref.py, mcp-server/sources/pubmed.py, mcp-server/sources/arxiv.py, mcp-server/utils/config.py; skills/nature-citation/scripts/nature_citation.py; skills/nature-figure/assets/figures4papers/** (28 plotting scripts) |
| Package manifests | skills/nature-academic-search/mcp-server/requirements.txt |
| MCP configs | None |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | skills/nature-academic-search/install.sh | 58 | Shell-variable injection into Python code | PUBMED_EMAIL ($1 arg) is interpolated unquoted into a `python3 -c "..."` heredoc; a crafted email such as `'); import os; os.system('...')#` executes arbitrary Python code. Medium confidence: requires malicious argument, but is exploitable in any automated pipeline. |
| 2 | Medium | skills/nature-academic-search/install.sh | 21 | Runtime package install without pinning | `pip install mcp requests toml lxml` installs unpinned latest versions globally; no hash verification. Supply-chain drift or malicious yanked-and-replaced version could be installed silently. |
| 3 | Low | skills/nature-academic-search/mcp-server/requirements.txt | 1–4 | Unpinned semver dependencies | All four deps use `>=` floor only (`mcp>=1.0.0`, `requests>=2.28.0`, `toml>=0.10.2`, `lxml>=4.9.0`); no upper cap or hash pinning. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .claude-plugin/plugin.json | Description text names only 5 of 9 shipped skills; nature-academic-search, nature-reader, nature-response, and nature-writing are absent. The description also states these categories are "Future releases" when several (peer-review responses → nature-response, methods writing → nature-writing) are already present on disk. | Misleads adopters about plugin scope; manifests incorrectly as a citation/figure-only plugin. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/nature-academic-search/install.sh | Runtime `pip install` with no version pinning or hash verification | Replace with `pip install -r requirements.txt` (pinned), or add `--require-hashes` and a locked requirements file |
| 2 | skills/nature-academic-search/mcp-server/requirements.txt | All deps use `>=` floor only | Pin to exact versions (`mcp==1.9.4`, etc.) and add hashes via `pip-compile --generate-hashes` |

*The High finding (install.sh line 58 injection) requires private disclosure, not a public PR. Do not open a public issue for it.*

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/nature-academic-search/SKILL.md | No "Output format" or "Report results" section; skill describes which MCP tools to use but not what Claude should return to the user | −10 |
| 2 | skills/nature-figure/SKILL.md | No "Output format" section defining what Claude returns after figure generation (script, file paths, description, QA result) | −10 |
| 3 | skills/nature-academic-search/SKILL.md | Vague quantifiers: "Broad academic search" (table), "results may vary" (Limitations) | −4 |
| 4 | skills/nature-citation/SKILL.md | Vague quantifiers: "roughly 3000 characters", "about 700 characters", "about 10 segments", "A useful answer is usually 3–8 candidates" | −8 |
| 5 | skills/nature-figure/SKILL.md | Vague quantifiers: "high-impact journals" (description), "similar venues" (When to load) | −4 |
| 6 | skills/nature-paper2ppt/SKILL.md | Vague quantifiers: "usually select 4–8 figure/table assets", "Speaker notes should be useful but concise" | −6 |
| 7 | skills/nature-data/SKILL.md | Vague quantifiers: "reasonable request", "suitable community repository" | −4 |
| 8 | skills/nature-reader/SKILL.md | Vague quantifiers: "near the relevant discussion", "clearly lawful open-access content" | −4 |
| 9 | skills/nature-response/SKILL.md | Vague quantifiers: "concise, evidence-linked replies", "long defensive explanations" | −4 |
| 10 | skills/nature-polishing/SKILL.md | Vague quantifier: "clearly Chinese-influenced English" | −2 |
| 11 | skills/nature-writing/SKILL.md | Vague quantifiers: "ambitious but bounded claims", "concise notes", "material issues", "compact bullets" | −8 |
| 12 | skills/nature-reader/SKILL.md | references/ directory contains grounding-rules.md and output-spec.md that are never referenced in SKILL.md; orphaned files create maintenance confusion | informational |

## Cross-Component
**plugin.json description vs. disk state:** The description text enumerates five skills (nature-figure, nature-polishing, nature-citation, nature-data, nature-paper2ppt) and lists peer-review responses and methods writing as "Future releases planned." However, nature-response (peer-review responses) and nature-writing (methods writing) are already present under `skills/`. Additionally nature-academic-search and nature-reader are fully shipped but completely absent from the description. The `keywords` array (`["nature","academic","science","figure","writing","citation","publication"]`) does not mention "reader", "response", or "academic-search", compounding the omission.

**nature-reader external skill cross-references:** SKILL.md instructs agents to "load the `pdf` skill first for extraction and OCR guidance" and to use `web-artifacts-builder` or `frontend-design` as preview layers. None of these skills are included in this plugin. The references are soft (advisory), so no hard breakage, but adopters who rely on those skills will need to install them separately. No mention of this dependency appears in install instructions.

**No broken file references detected:** All `[link](references/file.md)` targets in every SKILL.md were verified to exist on disk. Workflow files wf1–wf5, all reference directories, and the examples/index.md for nature-writing are all present.

## Recommendation
REVIEW — The NL quality is strong (93/100) and all internal file references resolve correctly. One High-severity security finding (PUBMED_EMAIL injection in install.sh) requires private disclosure before any PR activity; do not open a public issue. Once privately disclosed:

- Submit a PR fixing the plugin.json description (Bug #1) — low-risk, high adopter value.
- Submit a PR adding output format sections to nature-academic-search and nature-figure (Quality #1–2) — clear improvement.
- Submit a PR pinning requirements.txt and fixing the install.sh pip invocation (Security Fixes #1–2, Medium/Low only).
- The High injection finding must be filed as a private security report to the repo maintainer.
