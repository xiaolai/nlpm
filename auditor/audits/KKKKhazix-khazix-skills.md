# NLPM Audit: KKKKhazix/khazix-skills
**Date**: 2026-04-06  |  **Artifacts**: 18  |  **Strategy**: single
**NL Score**: 96/100
**Security**: BLOCKED
**Bugs**: 0  |  **Quality Issues**: 9  |  **Security Findings**: 12

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| neat-freak/evals/fixtures/eval-1-routine-dev-sync/workspace/taskflow/CLAUDE.md | Memory (eval fixture) | 90 | No test command; no prerequisites section |
| neat-freak/evals/fixtures/eval-2-memory-conflict/workspace/notesapp/CLAUDE.md | Memory (eval fixture) | 90 | No test command; no prerequisites section |
| neat-freak/evals/fixtures/eval-4-cross-project/workspace/auth-center/CLAUDE.md | Memory (eval fixture) | 90 | No test command; no prerequisites section |
| neat-freak/evals/fixtures/eval-4-cross-project/workspace/skills-hub/CLAUDE.md | Memory (eval fixture) | 90 | No test command; no prerequisites section |
| neat-freak/evals/fixtures/eval-5-governance/workspace/pdf-tools/CLAUDE.md | Memory (eval fixture) | 90 | No test command; no architecture/prerequisites section |
| neat-freak/evals/fixtures/eval-6-scope-boundary/workspace/current-app/CLAUDE.md | Memory (eval fixture) | 90 | No test command; deliberately minimal (scope-boundary fixture) |
| hv-analysis/SKILL.md | Skill | 95 | Description ~515 chars, in the R04 500–800 char band |
| khazix-writer/SKILL.md | Skill | 95 | Body ~409 lines, in the R05 400–500 line band |
| neat-freak/SKILL.md | Skill | 95 | Description near the R04 800-char threshold |
| aihot/SKILL.md | Skill | 100 | None — clean |
| storage-analyzer/SKILL.md | Skill | 100 | None — clean |
| neat-freak/evals/fixtures/eval-1-routine-dev-sync/workspace/CLAUDE.md | Rules (workspace root, eval fixture) | 100 | None — appropriately scoped |
| neat-freak/evals/fixtures/eval-2-memory-conflict/workspace/CLAUDE.md | Rules (workspace root, eval fixture) | 100 | None — appropriately scoped |
| neat-freak/evals/fixtures/eval-3-cold-start/workspace/CLAUDE.md | Rules (workspace root, eval fixture) | 100 | None — appropriately scoped |
| neat-freak/evals/fixtures/eval-4-cross-project/workspace/CLAUDE.md | Rules (workspace root, eval fixture) | 100 | None — appropriately scoped |
| neat-freak/evals/fixtures/eval-5-governance/workspace/CLAUDE.md | Rules (workspace root, eval fixture) | 100 | None — appropriately scoped |
| neat-freak/evals/fixtures/eval-6-scope-boundary/workspace/CLAUDE.md | Rules (workspace root, eval fixture) | 100 | None — appropriately scoped |
| neat-freak/evals/fixtures/eval-7-release-terminal/project/CLAUDE.md | Rules (release gate, eval fixture) | 100 | None — appropriately scoped |

Note on the 13 `neat-freak/evals/fixtures/**/CLAUDE.md` files: these are synthetic
test data authored to exercise the `neat-freak` governance-closeout skill's eval
harness (`evals/evals.json`, `evals/validate.py`), not production documentation
shipped to end users. Workspace-root fixtures (rules-only, no runnable code) are
scored without the project-level build/test/architecture rows, since those rows
don't apply to a workspace-root conventions file. Project-level fixtures are
scored against the full CLAUDE.md rubric; gaps there are minor and often
intentional (e.g. `eval-6-scope-boundary`'s `current-app/CLAUDE.md` is
deliberately terse to test that `neat-freak` doesn't wander into sibling
`Legacy_App/`).

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 2 |
| High | 7 |
| Medium | 1 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts (shipped, part of a skill) | 5 — `hv-analysis/scripts/md_to_pdf.py`, `neat-freak/scripts/audit-inventory.sh`, `storage-analyzer/scripts/scan.py`, `storage-analyzer/scripts/server.py`, `storage-analyzer/scripts/build_report.py` |
| Scripts (eval fixtures, never executed by the plugin) | 8 — synthetic files under `neat-freak/evals/fixtures/**` (`server.js`, `server_old.js`, `main.py`, `supabase.js`, `setup.sh`, `Link_Shortener/src/server.js`, `pdf-tools/src/app.py`) + `neat-freak/evals/validate.py` (the eval harness's own structural test, not a runtime script) |
| MCP configs | 0 |
| Package manifests (`package.json` / `requirements.txt`) | 0 — none anywhere in the repo |
| Install scripts referenced from docs | `README.md:129`, `README.en.md:129` (`curl \| bash`), `aihot/README.md:29,32,35,38,41,44,50` (`bash <(curl ...)`) — `install.sh` itself is hosted at `aihot.virxact.com` and is **not present in this repo**, so its contents could not be audited |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | README.md | 129 | curl-pipe-to-shell | `curl -fsSL https://aihot.virxact.com/aihot-skill/install.sh \| bash` — remote script piped directly into `bash` with no local review step shown at this point in the doc; the script's contents live outside this repo and cannot be verified from source control. |
| 2 | Critical | README.en.md | 129 | curl-pipe-to-shell | English mirror of finding #1, identical command. |
| 3 | High | aihot/README.md | 29 | curl-pipe-to-shell (process substitution) | `bash <(curl -fsSL .../install.sh) --target claude` — functionally equivalent to `curl \| bash` (downloads and executes without persisting a reviewable file first). |
| 4 | High | aihot/README.md | 32 | curl-pipe-to-shell (process substitution) | Same pattern, `--target codex`. |
| 5 | High | aihot/README.md | 35 | curl-pipe-to-shell (process substitution) | Same pattern, `--target gemini`. |
| 6 | High | aihot/README.md | 38 | curl-pipe-to-shell (process substitution) | Same pattern, `--target copilot`. |
| 7 | High | aihot/README.md | 41 | curl-pipe-to-shell (process substitution) | Same pattern, `--target opencode`. |
| 8 | High | aihot/README.md | 44 | curl-pipe-to-shell (process substitution) | Same pattern, `--target agents`. |
| 9 | High | aihot/README.md | 50 | curl-pipe-to-shell (process substitution) | Same pattern, custom `--dir` variant. |
| 10 | Medium | hv-analysis/scripts/md_to_pdf.py | 229 | unescaped-html-interpolation | `title`, `meta_line`, and `author` are f-string-interpolated straight into the cover-page HTML (lines 229–233) with no `html.escape()`. `meta_line` is extracted from the researched Markdown's own metadata line, which can carry content pulled from web research — a stray `<`/`&` there would corrupt the page; WeasyPrint does not execute `<script>`, so this is a rendering/robustness risk rather than code execution. |
| 11 | Low | hv-analysis/SKILL.md | 22 | unpinned-semver | `pip install weasyprint markdown --break-system-packages` has no version pins (repeated at line 212); a future breaking release of either package silently changes report output. |
| 12 | Low | storage-analyzer/assets/report_template.html | 156 | unescaped-script-json | `const DATA = __REPORT_DATA__;` embeds `json.dumps()` output raw inside a `<script>` tag without escaping `</script>` sequences. Exploiting it requires a scanned file/directory name on the user's own disk to contain a script-breakout string — i.e. a local attacker who already has filesystem write access — so real-world impact is low, but it's the standard "JSON-in-script-tag" footgun and a one-line fix. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No high-confidence NL bugs found. | — |

See **Cross-Component** below for one low-confidence, not-PR-worthy dangling reference.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | hv-analysis/scripts/md_to_pdf.py | `title`/`author`/`meta_line` interpolated unescaped into HTML (line 229–233) | Wrap each with `html.escape()` before interpolation, or use `markupsafe.escape`. |
| 2 | hv-analysis/SKILL.md | Unpinned `pip install weasyprint markdown` (lines 22, 212) | Pin to tested major versions, e.g. `pip install "weasyprint>=62,<63" "markdown>=3.7,<4" --break-system-packages`. |
| 3 | storage-analyzer/assets/report_template.html | Unescaped JSON embedded in `<script>` (line 156) | In `server.py`/`build_report.py`, emit `json.dumps(data).replace('<', '<')` (or use a JSON-in-HTML-safe serializer) before the template substitution. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | hv-analysis/SKILL.md | Description ≈515 chars — R04 500–800 char band | -5 |
| 2 | khazix-writer/SKILL.md | Body ≈409 lines — R05 400–500 line band | -5 |
| 3 | neat-freak/SKILL.md | Description ≈800 chars — at/near the R04 800-char threshold (exact count sensitive to YAML fold whitespace; treated as within the 500–800 band) | -5 |
| 4 | neat-freak/evals/fixtures/eval-1-routine-dev-sync/workspace/taskflow/CLAUDE.md | No test command (R34); no Prerequisites section | -10 |
| 5 | neat-freak/evals/fixtures/eval-2-memory-conflict/workspace/notesapp/CLAUDE.md | No test command (R34); no Prerequisites section | -10 |
| 6 | neat-freak/evals/fixtures/eval-4-cross-project/workspace/auth-center/CLAUDE.md | No test command (R34); no Prerequisites section (env-var table partially substitutes) | -10 |
| 7 | neat-freak/evals/fixtures/eval-4-cross-project/workspace/skills-hub/CLAUDE.md | No test command (R34); no Prerequisites section | -10 |
| 8 | neat-freak/evals/fixtures/eval-5-governance/workspace/pdf-tools/CLAUDE.md | No test command (R34); no architecture/Prerequisites section | -10 |
| 9 | neat-freak/evals/fixtures/eval-6-scope-boundary/workspace/current-app/CLAUDE.md | No test command (R34); no Prerequisites section (deliberately minimal per eval design) | -10 |

## Cross-Component
- `hv-analysis/SKILL.md:8` and `khazix-writer/SKILL.md:4` both tell the agent not to use that skill for "纯标题摘要生成" and to use **wechat-title** instead, but no `wechat-title/` directory exists in this repo, and it is not among the 5 skills the README's own "Skills-5" badge and table advertise. Most likely an unpublished sibling skill from the author's private toolkit rather than a build defect — low confidence, not PR-worthy as written (a maintainer conversation would resolve it faster than a patch), but worth flagging so a reader isn't left searching for a skill that isn't there.
- No other orphaned components, broken relative paths, or stale counts found. Every `references/`, `scripts/`, and `assets/` path cited across the 5 SKILL.md files resolves to a real file on disk, and the README's "Skills-5" badge matches the 5 published skill directories exactly.
- All 5 `SKILL.md` frontmatter `name:` values match their parent directory name (open-spec MUST) — no penalty triggered.

## Recommendation

**BLOCKED — do not submit PRs. File a private security report / raise the install pattern directly with the maintainer instead of a public issue or PR.**

The blocking finding is narrow and specific: `README.md:129` and `README.en.md:129` pipe a remote script straight into `bash`, and `aihot/README.md` offers six process-substitution variants of the same pattern. `install.sh` itself is hosted off-repo and could not be reviewed as part of this audit, which is exactly the risk the curl-pipe-to-shell pattern represents (the script can change server-side with no corresponding commit history).

Context worth weighing before escalating this as urgent: the maintainer shows real security awareness elsewhere — `aihot/README.md` explicitly recommends an agent-mediated "review before writing" installation path as the *primary* method, states "不要使用 sudo" twice, links directly to the hosted `SKILL.md`/`install.sh` source for review, and `aihot/SKILL.md`'s own "安全边界" section is unusually rigorous (anonymous GET only, treats all API content as untrusted data, never requests credentials). Curl-pipe-to-shell installers are also a widely-used, openly-debated convention across the Agent Skills ecosystem, not a hidden or obfuscated mechanism here. None of that changes the severity classification under this rubric, but it does mean the fix is a documentation/design conversation (e.g. promote the "download, inspect, then run" path to the only path, or vendor `install.sh` into this repo so it's diffable) rather than a mechanical one-line patch — which is also why it doesn't fit the PR-worthy Security Fixes table above.

Once the install-script disclosure is resolved, the two Medium/Low security fixes and the nine quality-band items in this report are independently safe to submit as ordinary PRs — they don't depend on the install-pattern conversation.
