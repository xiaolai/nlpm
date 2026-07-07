# NLPM Audit: dongbeixiaohuo/writing-agent
**Date**: 2026-04-06  |  **Artifacts**: 72  |  **Strategy**: progressive
**NL Score**: 82/100
**Security**: BLOCKED
**Bugs**: 3  |  **Quality Issues**: 51  |  **Security Findings**: 5

## Notes on repo structure

This repo ships every agent/skill/hook in **three mirrored locations**:
`.claude/` (dev), `claude-runtime/` (documented as the sync source-of-truth —
see `scripts/sync_claude_runtime.py` / `check_claude_runtime_sync.py`), and
`plugins/writing-agent/` (the distributable plugin). `diff -rq` confirms all
20 agents and 3 skills are byte-identical across the three copies; only
`hooks/hooks.json` legitimately differs (the plugin copy adds a
`SessionStart` bootstrap hook and uses `${CLAUDE_PLUGIN_ROOT}`-relative
paths). Because of this, every NL finding below is real in triplicate (one
occurrence per copy — 60 agent-path rows + 9 skill-path rows in the score
table), but is reported **once**, anchored at the `claude-runtime/` copy
(the documented sync source), to keep the tables actionable. Fixing the
`claude-runtime/` copy and running `python scripts/sync_claude_runtime.py`
propagates the fix to the other two automatically.

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/agents/writing-executor.md | agent | 74 | No `<example>` blocks (-15); `model` not declared (-5) |
| claude-runtime/agents/writing-executor.md | agent | 74 | No `<example>` blocks (-15); `model` not declared (-5) |
| plugins/writing-agent/agents/writing-executor.md | agent | 74 | No `<example>` blocks (-15); `model` not declared (-5) |
| .claude/agents/humanizer.md | agent | 77 | No `<example>` blocks (-15); `model` not declared (-5) |
| claude-runtime/agents/humanizer.md | agent | 77 | No `<example>` blocks (-15); `model` not declared (-5) |
| plugins/writing-agent/agents/humanizer.md | agent | 77 | No `<example>` blocks (-15); `model` not declared (-5) |
| .claude/agents/article-illustrator.md | agent | 79 | No `<example>` blocks (-15); `GenerateImage` tool unused (-3) |
| claude-runtime/agents/article-illustrator.md | agent | 79 | No `<example>` blocks (-15); `GenerateImage` tool unused (-3) |
| plugins/writing-agent/agents/article-illustrator.md | agent | 79 | No `<example>` blocks (-15); `GenerateImage` tool unused (-3) |
| .claude/agents/writing-clarifier.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| claude-runtime/agents/writing-clarifier.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| plugins/writing-agent/agents/writing-clarifier.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| .claude/agents/outline-architect.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| claude-runtime/agents/outline-architect.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| plugins/writing-agent/agents/outline-architect.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| .claude/agents/fact-checker.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| claude-runtime/agents/fact-checker.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| plugins/writing-agent/agents/fact-checker.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| .claude/agents/topic-generator.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| claude-runtime/agents/topic-generator.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| plugins/writing-agent/agents/topic-generator.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| .claude/agents/editor-review.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| claude-runtime/agents/editor-review.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| plugins/writing-agent/agents/editor-review.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| .claude/agents/research-expert.md | agent | 79 | No `<example>` blocks (-15); `WebFetch` unused (-3) |
| claude-runtime/agents/research-expert.md | agent | 79 | No `<example>` blocks (-15); `WebFetch` unused (-3) |
| plugins/writing-agent/agents/research-expert.md | agent | 79 | No `<example>` blocks (-15); `WebFetch` unused (-3) |
| .claude/agents/topic-research.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| claude-runtime/agents/topic-research.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| plugins/writing-agent/agents/topic-research.md | agent | 79 | No `<example>` blocks (-15); `Grep` unused (-3) |
| .claude/agents/wechat-reader-test.md | agent | 82 | No `<example>` blocks (-15) |
| claude-runtime/agents/wechat-reader-test.md | agent | 82 | No `<example>` blocks (-15) |
| plugins/writing-agent/agents/wechat-reader-test.md | agent | 82 | No `<example>` blocks (-15) |
| .claude/agents/edit-diff-learner.md | agent | 82 | No `<example>` blocks (-15) |
| claude-runtime/agents/edit-diff-learner.md | agent | 82 | No `<example>` blocks (-15) |
| plugins/writing-agent/agents/edit-diff-learner.md | agent | 82 | No `<example>` blocks (-15) |
| .claude/agents/opening-tournament.md | agent | 82 | No `<example>` blocks (-15) |
| claude-runtime/agents/opening-tournament.md | agent | 82 | No `<example>` blocks (-15) |
| plugins/writing-agent/agents/opening-tournament.md | agent | 82 | No `<example>` blocks (-15) |
| .claude/agents/pre-publish-review.md | agent | 82 | No `<example>` blocks (-15) |
| claude-runtime/agents/pre-publish-review.md | agent | 82 | No `<example>` blocks (-15) |
| plugins/writing-agent/agents/pre-publish-review.md | agent | 82 | No `<example>` blocks (-15) |
| .claude/agents/title-designer.md | agent | 82 | No `<example>` blocks (-15) |
| claude-runtime/agents/title-designer.md | agent | 82 | No `<example>` blocks (-15) |
| plugins/writing-agent/agents/title-designer.md | agent | 82 | No `<example>` blocks (-15) |
| .claude/agents/position-engine.md | agent | 82 | No `<example>` blocks (-15) |
| claude-runtime/agents/position-engine.md | agent | 82 | No `<example>` blocks (-15) |
| plugins/writing-agent/agents/position-engine.md | agent | 82 | No `<example>` blocks (-15) |
| .claude/agents/memory-loader.md | agent | 82 | No `<example>` blocks (-15) |
| claude-runtime/agents/memory-loader.md | agent | 82 | No `<example>` blocks (-15) |
| plugins/writing-agent/agents/memory-loader.md | agent | 82 | No `<example>` blocks (-15) |
| .claude/agents/concretizer.md | agent | 82 | No `<example>` blocks (-15) |
| claude-runtime/agents/concretizer.md | agent | 82 | No `<example>` blocks (-15) |
| plugins/writing-agent/agents/concretizer.md | agent | 82 | No `<example>` blocks (-15) |
| .claude/agents/empathy-designer.md | agent | 82 | No `<example>` blocks (-15) |
| claude-runtime/agents/empathy-designer.md | agent | 82 | No `<example>` blocks (-15) |
| plugins/writing-agent/agents/empathy-designer.md | agent | 82 | No `<example>` blocks (-15) |
| .claude/agents/html-exporter.md | agent | 82 | No `<example>` blocks (-15) |
| claude-runtime/agents/html-exporter.md | agent | 82 | No `<example>` blocks (-15) |
| plugins/writing-agent/agents/html-exporter.md | agent | 82 | No `<example>` blocks (-15) |
| .claude/skills/工作流导演/SKILL.md | skill | 85 | `name: workflow-producer` ≠ parent dir `工作流导演` (-15) |
| claude-runtime/skills/工作流导演/SKILL.md | skill | 85 | `name: workflow-producer` ≠ parent dir `工作流导演` (-15) |
| plugins/writing-agent/skills/工作流导演/SKILL.md | skill | 85 | `name: workflow-producer` ≠ parent dir `工作流导演` (-15) |
| .claude/skills/风格建模/SKILL.md | skill | 85 | `name: style-modeler` ≠ parent dir `风格建模` (-15) |
| claude-runtime/skills/风格建模/SKILL.md | skill | 85 | `name: style-modeler` ≠ parent dir `风格建模` (-15) |
| plugins/writing-agent/skills/风格建模/SKILL.md | skill | 85 | `name: style-modeler` ≠ parent dir `风格建模` (-15) |
| .claude/skills/公众号文章获取/SKILL.md | skill | 85 | `name: web-article-extractor` ≠ parent dir `公众号文章获取` (-15) |
| claude-runtime/skills/公众号文章获取/SKILL.md | skill | 85 | `name: web-article-extractor` ≠ parent dir `公众号文章获取` (-15) |
| plugins/writing-agent/skills/公众号文章获取/SKILL.md | skill | 85 | `name: web-article-extractor` ≠ parent dir `公众号文章获取` (-15) |
| claude-runtime/hooks/hooks.json | hooks | 100 | None |
| plugins/writing-agent/hooks/hooks.json | hooks | 100 | None |
| plugins/writing-agent/.claude-plugin/plugin.json | plugin.json | 100 | None |

**Weighted average**: (1603×3 agent-scores + 85×9 + 100×3) / 72 = 5874/72 = **81.6 → 82/100**.

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 0 |
| Medium | 4 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 2 (`claude-runtime/hooks/hooks.json`, `plugins/writing-agent/hooks/hooks.json`; `.claude/settings.json` embeds an equivalent inline `hooks` block, not separately scored) |
| Scripts | 59 (10 in `scripts/` ×3 mirrored copies + `tests/*.py` ×4 + 2 Python in `skills/风格建模/scripts/` ×3 copies + 6 JS/vendor in `skills/公众号文章获取/scripts/` ×3 copies + 1 `writing-agent-app/eslint.config.js`; two additional `.ts` scripts — `scripts/generate_image.ts`, `scripts/export_markdown_to_html.ts` — exist alongside but outside the `.{sh,py,js}` glob) |
| MCP configs | 0 (no `.mcp.json` in repo; `公众号文章获取` skill documents an optional `chrome-devtools` MCP server the *user* must add — not shipped) |
| Package manifests | 2 (`package.json`, `writing-agent-app/package.json`; neither has `postinstall`/`preinstall` scripts) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | `.claude/skills/公众号文章获取/scripts/readability_loader.js` | 15–17, 28–30 | eval with variable input, attacker-influenceable path | `SKILL_PATH` defaults to a fixed string but is overridable via `globalThis.__WEB_ARTICLE_EXTRACTOR_PATH__` (line 15-17); that path is joined with a filename and read via `fs.readFileSync` (line 28-29), then passed straight to `eval()` (line 30). Any code path in the same JS execution context that can set `globalThis.__WEB_ARTICLE_EXTRACTOR_PATH__` before this IIFE runs controls what file gets read and `eval`'d — an arbitrary-file-read-into-eval primitive, not just a static self-eval of a first-party file. Mitigating context: today nothing in this repo actually sets that global, so it is currently dead/unreachable, and the file it reads by default is the first-party `readability_extractor.js` sitting next to it. |
| 2 | Medium | `.claude/skills/公众号文章获取/scripts/readability_loader.js` | 74–75 | Remote script load + execution | CDN fallback path dynamically injects `<script src="https://cdn.jsdelivr.net/npm/@mozilla/readability@0.6.0/...">` into the page and executes it. Version is pinned (mitigates left-pad-style breakage) but there is no Subresource Integrity (SRI) hash, so a compromised CDN edge/package could serve altered code that runs in the browsing context. |
| 3 | Medium | `.claude/skills/公众号文章获取/scripts/markdown_converter.js` | 19, 34 | Remote script load + execution | Same CDN-script-injection pattern for `turndown@7.1.3` and `@mozilla/readability@0.5.0` from `cdn.jsdelivr.net`, no SRI hash. A local, already-vendored `Readability.js` exists in the same directory (`scripts/Readability.js`) and is not reused here, so this network dependency looks avoidable. |
| 4 | Medium | `scripts/generate_image.ts` | 38, 57, 80–85 | Network calls + env var API key | Sends the user's writing prompt to an external image-generation endpoint (Google Gemini or an OpenAI-compatible host, `API_BASE`/`GEMINI_API_KEY` from env). This is the tool's documented, intended feature (image generation), not a covert exfiltration channel — flagged per the rubric's "network calls + env var access" pattern for completeness, not as a defect. |
| 5 | Medium | `.claude/skills/公众号文章获取/scripts/save_with_images.js` | 20–52 | Network calls | Downloads every `<img>` URL found in scraped page content via raw `http.get`/`https.get` to local disk. Standard for a "save article with images" feature; flagged because the target host is fully attacker-influenceable (whatever URLs happen to be on the extracted page) — worth a timeout/size cap review, but not itself a bug (a 30s timeout is already present). |

No High-severity findings. No credential exfiltration, no `curl \| sh`, no `os.system`/`subprocess(shell=True)`, no hardcoded secrets found anywhere in the 59 scripts or 2 hooks.json files.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `claude-runtime/skills/工作流导演/SKILL.md` | Frontmatter `name: workflow-producer` does not match parent directory `工作流导演` | Violates the open Agent Skills spec ("`name` ... MUST match parent directory name", `nlpm:conventions` §5); mirrored identically in `.claude/skills/工作流导演/SKILL.md` and `plugins/writing-agent/skills/工作流导演/SKILL.md` |
| 2 | `claude-runtime/skills/风格建模/SKILL.md` | Frontmatter `name: style-modeler` does not match parent directory `风格建模` | Same spec violation; mirrored in `.claude/skills/风格建模/SKILL.md` and `plugins/writing-agent/skills/风格建模/SKILL.md` |
| 3 | `claude-runtime/skills/公众号文章获取/SKILL.md` | Frontmatter `name: web-article-extractor` does not match parent directory `公众号文章获取` | Same spec violation; mirrored in `.claude/skills/公众号文章获取/SKILL.md` and `plugins/writing-agent/skills/公众号文章获取/SKILL.md` |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `.claude/skills/公众号文章获取/scripts/readability_loader.js` | CDN script injection without SRI (lines 74–75) | Add `integrity`/`crossorigin` attributes to the injected `<script>` tag, or prefer the local embedded extractor (`readability_extractor.js`) that already ships in the same directory and drop the CDN fallback entirely |
| 2 | `.claude/skills/公众号文章获取/scripts/markdown_converter.js` | CDN script injection without SRI (lines 19, 34) | Same fix: add SRI hashes, or replace with the vendored `scripts/Readability.js` + a bundled Turndown copy so no runtime network fetch is needed |
| 3 | `scripts/generate_image.ts` | API key read from env with no explicit redaction in error/log paths (line 57) | Low-risk as written (key is never printed), but consider wrapping the `catch` block's `console.error("❌ 生成失败:", error)` (line 131) to strip any header/body echoes if the upstream API ever includes the key in error payloads |
| 4 | `.claude/skills/公众号文章获取/scripts/save_with_images.js` | Unbounded image download from URLs found in arbitrary scraped pages | Add a max-file-size cap alongside the existing 30s timeout, and restrict `protocol` to `http/https` only (already implicit, but make it explicit) to avoid surprises if `image.src` is ever a `file://` or other scheme |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `claude-runtime/agents/wechat-reader-test.md` | Zero `<example>` blocks (R09) | -15 |
| 2 | `claude-runtime/agents/wechat-reader-test.md` | `Glob` declared in `tools:` but never referenced in body | -3 |
| 3 | `claude-runtime/agents/article-illustrator.md` | Zero `<example>` blocks (R09) | -15 |
| 4 | `claude-runtime/agents/article-illustrator.md` | `Glob` declared but unused | -3 |
| 5 | `claude-runtime/agents/article-illustrator.md` | `GenerateImage` declared in `tools:` but body invokes image generation via `Bash` (`npx tsx scripts/generate_image.ts`), not the declared tool | -3 |
| 6 | `claude-runtime/agents/writing-clarifier.md` | Zero `<example>` blocks (R09) | -15 |
| 7 | `claude-runtime/agents/writing-clarifier.md` | `Glob` declared but unused | -3 |
| 8 | `claude-runtime/agents/writing-clarifier.md` | `Grep` declared but unused | -3 |
| 9 | `claude-runtime/agents/outline-architect.md` | Zero `<example>` blocks (R09) | -15 |
| 10 | `claude-runtime/agents/outline-architect.md` | `Glob` declared but unused | -3 |
| 11 | `claude-runtime/agents/outline-architect.md` | `Grep` declared but unused | -3 |
| 12 | `claude-runtime/agents/edit-diff-learner.md` | Zero `<example>` blocks (R09) | -15 |
| 13 | `claude-runtime/agents/edit-diff-learner.md` | `Glob` declared but unused | -3 |
| 14 | `claude-runtime/agents/writing-executor.md` | Zero `<example>` blocks (R09) | -15 |
| 15 | `claude-runtime/agents/writing-executor.md` | `Glob` declared but unused | -3 |
| 16 | `claude-runtime/agents/writing-executor.md` | `Grep` declared but unused | -3 |
| 17 | `claude-runtime/agents/writing-executor.md` | `model` not declared in frontmatter (R10). Changelog v1.3.0 states this was a deliberate removal ("移除 model 钉死（改为继承会话模型）") — flagged per rubric regardless of intent | -5 |
| 18 | `claude-runtime/agents/opening-tournament.md` | Zero `<example>` blocks (R09) | -15 |
| 19 | `claude-runtime/agents/opening-tournament.md` | `Glob` declared but unused | -3 |
| 20 | `claude-runtime/agents/fact-checker.md` | Zero `<example>` blocks (R09) | -15 |
| 21 | `claude-runtime/agents/fact-checker.md` | `Glob` declared but unused | -3 |
| 22 | `claude-runtime/agents/fact-checker.md` | `Grep` declared but unused (WebSearch/WebFetch both are used) | -3 |
| 23 | `claude-runtime/agents/topic-generator.md` | Zero `<example>` blocks (R09) | -15 |
| 24 | `claude-runtime/agents/topic-generator.md` | `Glob` declared but unused | -3 |
| 25 | `claude-runtime/agents/topic-generator.md` | `Grep` declared but unused | -3 |
| 26 | `claude-runtime/agents/pre-publish-review.md` | Zero `<example>` blocks (R09) | -15 |
| 27 | `claude-runtime/agents/pre-publish-review.md` | `Glob` declared but unused | -3 |
| 28 | `claude-runtime/agents/humanizer.md` | Zero `<example>` blocks (R09) | -15 |
| 29 | `claude-runtime/agents/humanizer.md` | `Glob` declared but unused | -3 |
| 30 | `claude-runtime/agents/humanizer.md` | `model` not declared in frontmatter (R10); changelog v1.3.0 states this is deliberate ("移除 model 钉死（灵魂注入改为继承会话模型）") | -5 |
| 31 | `claude-runtime/agents/title-designer.md` | Zero `<example>` blocks (R09) | -15 |
| 32 | `claude-runtime/agents/title-designer.md` | `Glob` declared but unused | -3 |
| 33 | `claude-runtime/agents/editor-review.md` | Zero `<example>` blocks (R09) | -15 |
| 34 | `claude-runtime/agents/editor-review.md` | `Glob` declared but unused | -3 |
| 35 | `claude-runtime/agents/editor-review.md` | `Grep` declared but unused | -3 |
| 36 | `claude-runtime/agents/research-expert.md` | Zero `<example>` blocks (R09) | -15 |
| 37 | `claude-runtime/agents/research-expert.md` | `Glob` declared but unused | -3 |
| 38 | `claude-runtime/agents/research-expert.md` | `WebFetch` declared but unused (WebSearch is used) | -3 |
| 39 | `claude-runtime/agents/position-engine.md` | Zero `<example>` blocks (R09) | -15 |
| 40 | `claude-runtime/agents/position-engine.md` | `Glob` declared but unused | -3 |
| 41 | `claude-runtime/agents/memory-loader.md` | Zero `<example>` blocks (R09) | -15 |
| 42 | `claude-runtime/agents/memory-loader.md` | `Glob` declared but unused | -3 |
| 43 | `claude-runtime/agents/concretizer.md` | Zero `<example>` blocks (R09) | -15 |
| 44 | `claude-runtime/agents/concretizer.md` | `Glob` declared but unused | -3 |
| 45 | `claude-runtime/agents/topic-research.md` | Zero `<example>` blocks (R09) | -15 |
| 46 | `claude-runtime/agents/topic-research.md` | `Glob` declared but unused | -3 |
| 47 | `claude-runtime/agents/topic-research.md` | `Grep` declared but unused (WebSearch is used) | -3 |
| 48 | `claude-runtime/agents/empathy-designer.md` | Zero `<example>` blocks (R09) | -15 |
| 49 | `claude-runtime/agents/empathy-designer.md` | `Glob` declared but unused | -3 |
| 50 | `claude-runtime/agents/html-exporter.md` | Zero `<example>` blocks (R09) | -15 |
| 51 | `claude-runtime/agents/html-exporter.md` | `Glob` declared but unused | -3 |

Note: the R01 vague-quantifier check (`appropriate`, `relevant`, `as needed`, etc.) produced zero hits across all 20 agents and 3 skills — the corpus is entirely Chinese-language, and the rubric's quantifier list is English-only, so this check is structurally unable to fire here. Flagging this as an observation, not a defect.

## Cross-Component
- **Broken references**: none found. `.claude/workflows/collab_v2.json` (referenced by `工作流导演`/workflow-producer) exists; every `references/*.md` path in both `风格建模` and `公众号文章获取` resolves to a real file; every `scripts/*.py`/`*.js`/`*.ts` path referenced from an agent or skill body exists on disk; `web-article-extractor` (referenced from `风格建模`'s SKILL.md as the article-extraction dependency) correctly resolves to the `公众号文章获取` skill's actual `name:` field.
- **Manifest vs. disk**: `plugins/writing-agent/.claude-plugin/plugin.json` version (`0.8.1`) matches `package.json` and the latest `CHANGELOG.md` entry — no drift.
- **Roster inconsistency** (`CC-incomplete-roster`): `claude-runtime/skills/工作流导演/SKILL.md` describes `memory-loader` as an actively-called Stage-0 subagent in its prose ("Stage 1 创建项目目录并保存 01_theme.md 后，必须立即执行 Stage 0 `memory-loader`...") and `.claude/workflows/collab_v2.json` lists it as stage `"0"` with agent `"memory-loader"` — but the "Subagent 清单" (subagent roster) table at the end of the same SKILL.md enumerates only 19 of the 20 active subagents, omitting `memory-loader` entirely. The agent file exists and is genuinely wired into the workflow; only the summary table is stale.

## Recommendation

**BLOCKED — do not submit PRs. File private security report** for finding
#1 (`readability_loader.js`'s `eval()` fed by an overridable global path).
While currently unreachable in this codebase (nothing sets
`globalThis.__WEB_ARTICLE_EXTRACTOR_PATH__` today), the primitive is real
and should be disclosed privately to the maintainer rather than fixed via
a public PR that documents the exploit path.

Once the security disclosure is acknowledged, the 3 skill-name bugs and
the 4 Medium/Low security fixes are safe to submit as public PRs — none of
them require withholding details. The 51 quality issues (all "no
`<example>` blocks" + a handful of unused-tool declarations) are
low-severity and can be bundled into the same or a follow-up PR.
