# NLPM Audit: mxyhi/ok-skills
**Date**: 2026-04-06  |  **Artifacts**: 40  |  **Strategy**: batched
**NL Score**: 92/100
**Security**: BLOCKED
**Bugs**: 2  |  **Quality Issues**: 47  |  **Security Findings**: 20

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| imagegen-frontend-web/SKILL.md | skill | 65 | 10 vague quantifiers (capped -20); body 987 lines (>500) |
| autoresearch/SKILL.md | skill | 70 | References `scripts/orchestrate.sh`, which does not exist |
| teach/SKILL.md | skill | 77 | Generic description restates the skill name, no concrete trigger |
| minimax-docx/SKILL.md | skill | 78 | 7 vague quantifiers ("relevant" ×6, "as needed") |
| gpt-taste/SKILL.md | skill | 80 | Generic description, no concrete "use when" trigger |
| find-docs/SKILL.md | skill | 81 | Description >800 chars (878) |
| huashu-design/SKILL.md | skill | 85 | References nonexistent companion skill `huashu-gpt-image` |
| improve-codebase-architecture/SKILL.md | skill | 85 | Description gives no concrete trigger phrases |
| grill-with-docs/SKILL.md | skill | 85 | Description gives no concrete trigger phrases |
| get-api-docs/SKILL.md | skill | 86 | Description >800 chars (856) |
| minimax-pdf/SKILL.md | skill | 87 | Description >800 chars (~856) |
| kimi-webbridge/SKILL.md | skill | 88 | Description 500–800 chars; no cross-ref to overlapping agent-browser |
| agent-browser/SKILL.md | skill | 90 | Description >800 chars (925) |
| tdd/SKILL.md | skill | 90 | No code examples in body (delegated to referenced files) |
| opencli/opencli-browser/SKILL.md | skill | 91 | Body 439 lines (400–500 band) |
| opencli/opencli-browser-sitemap/SKILL.md | skill | 93 | 2 vague quantifiers ("relevant" ×2) |
| codebase-design/SKILL.md | skill | 93 | Vague quantifiers + no cross-ref to domain-modeling |
| minimax-xlsx/SKILL.md | skill | 95 | Description 500–800 chars (630) |
| prototype/SKILL.md | skill | 96 | 2 vague quantifiers ("several", "relevant") |
| x-twitter-scraper/SKILL.md | skill | 96 | 2 vague quantifiers ("relevant" ×2) |
| ai-elements/SKILL.md | skill | 96 | 2 vague quantifiers ("correctly" ×2) |
| find-skills/SKILL.md | skill | 96 | 2 vague quantifiers ("relevant" ×2) |
| grilling/SKILL.md | skill | 97 | No cross-ref to related planning/prototype skills |
| domain-modeling/SKILL.md | skill | 97 | No cross-ref to related codebase-design |
| pptx-generator/SKILL.md | skill | 97 | No cross-ref to overlapping huashu-design |
| planning-with-files/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| opencli/opencli-sitemap-author/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| opencli/opencli-usage/SKILL.md | skill | 98 | 1 vague quantifier ("Some") |
| systematic-debugging/SKILL.md | skill | 98 | 1 vague quantifier ("appropriate") |
| migrate-to-shoehorn/SKILL.md | skill | 98 | 1 vague quantifier ("some") |
| diagnosing-bugs/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| browser-trace/SKILL.md | skill | 100 | None found |
| karpathy-guidelines/SKILL.md | skill | 100 | None found |
| opencli/opencli-autofix/SKILL.md | skill | 100 | None found |
| opencli/opencli-adapter-author/SKILL.md | skill | 100 | None found |
| better-icons/SKILL.md | skill | 100 | None found |
| caveman/SKILL.md | skill | 100 | None found |
| handoff/SKILL.md | skill | 100 | None found |
| exa-search/SKILL.md | skill | 100 | None found |
| opencli/smart-search/SKILL.md | skill | 100 | None found |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 9 |
| Medium | 9 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts | 39 (`.sh`/`.py`/`.js` under `*/scripts/`) |
| MCP configs | 0 (no `.mcp.json`) |
| Package manifests | 2 (`browser-trace/package.json`, `huashu-design/package.json`) |

Scripts concentrate in six skills: `planning-with-files` (6), `minimax-xlsx` (10), `minimax-pdf` (9), `minimax-docx` (4), `huashu-design` (9), `diagnosing-bugs` (1). No `hooks/` directory, `.mcp.json`, or `requirements.txt` exists anywhere in the repo. No `commands/*.md` directory exists, so the Bash-tool/user-argument injection check does not apply.

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | huashu-design/scripts/render-narration.sh | 79 | SEC-shell-injection | `$TIMELINE` (raw `--timeline=` CLI arg) is spliced unescaped into a single-quoted JS string inside `node -e "..."`; a path containing `'` or `` ` `` breaks out of the string and injects arbitrary JS executed by `node`. |
| 2 | High | huashu-design/scripts/render-narration.sh | 80 | SEC-shell-injection | Same unescaped `$TIMELINE` interpolation pattern, second `node -e` invocation reading `voiceover` path. |
| 3 | High | huashu-design/scripts/render-narration.sh | 89 | SEC-shell-injection | `$TOTAL_DURATION` (output of the line-79 `node -e`, itself reachable via the same injection chain) is re-interpolated unescaped into a further `node -e` arithmetic expression. |
| 4 | High | minimax-docx/scripts/setup.sh | 109, 111, 136, 139 | SEC-download-execute | Downloads Microsoft's `dotnet-install.sh` from `https://dot.net/v1/dotnet-install.sh` to `/tmp` via `wget`/`curl`, then `chmod +x` and executes it directly — no checksum or signature verification of the fetched script. |
| 5 | High | minimax-docx/scripts/setup.sh | 112, 113, 140, 141 | SEC-path-modification | Prepends `$HOME/.dotnet` to `PATH` for the current shell and permanently appends the same export line to `~/.bashrc`, mutating the user's shell startup config outside the repo. |
| 6 | High | minimax-docx/scripts/setup.sh | 107, 108, 117, 120, 123 | SEC-sudo-usage | Runs `sudo apt-get`/`dnf`/`pacman`/`zypper install` unprompted in every package-manager branch of the setup dispatch. |
| 7 | High | minimax-xlsx/scripts/xlsx_add_column.py | 94 | SEC-path-traversal | `find_ws_path()` builds `os.path.join(work_dir, "xl", rel.get("Target"))` from `workbook.xml.rels` `Target` (attacker-controlled xlsx content) with no `../` sanitization, then opens/overwrites that path — zip-slip on a crafted `.xlsx`. |
| 8 | High | minimax-xlsx/scripts/xlsx_insert_row.py | 88 | SEC-path-traversal | Identical unsanitized `rel.get("Target")` → `os.path.join` → parse/overwrite pattern as finding #7. |
| 9 | High | minimax-xlsx/scripts/style_audit.py | 467 | SEC-path-traversal | `_load_from_dir()` builds `os.path.join(unpacked_dir, "xl", rel_path)` from the same unsanitized rels `Target`; substring/`startswith` checks do not block `../` segments, allowing arbitrary file read into the audit report. |
| 10 | Medium | huashu-design/scripts/fetch_images.py | 29, 64 | SEC-network-call | Two outbound HTTP(S) calls via `urllib.request.urlopen()` to `commons.wikimedia.org` for image assets. |
| 11 | Medium | huashu-design/scripts/html2pptx.js | 1097 | SEC-env-read | Reads `process.env.TMPDIR` to configure a Playwright temp directory. |
| 12 | Medium | minimax-docx/scripts/setup.sh | 109, 136 | SEC-network-call | `wget`/`curl` fetch of the dotnet installer script from `dot.net` (network leg of finding #4). |
| 13 | Medium | minimax-pdf/scripts/fill_inspect.py, fill_write.py, merge.py, reformat_parse.py, render_body.py | 27, 36, 21, 42, 44 | SEC-runtime-pip-install | Each script's `ensure_deps()` runs `pip install` for `pypdf`/`reportlab` at runtime if the import is missing. |
| 14 | Medium | minimax-pdf/scripts/make.sh | 109 | SEC-runtime-pip-install | `cmd_fix` installs `reportlab`, `pypdf`, `matplotlib` via `pip --break-system-packages` at runtime. |
| 15 | Medium | minimax-pdf/scripts/make.sh, render_cover.js | 117, 62 | SEC-network-call | Runs `npm install -g playwright` then `npx playwright install chromium`, downloading a Chromium binary from the network at runtime. |
| 16 | Medium | minimax-pdf/scripts/render_cover.js | 62 | SEC-shell-true | `spawnSync("npx", [...], { shell: true })` — args are static literals (not attacker-controlled) so exploitability is low, but the construct is a bad pattern. |
| 17 | Medium | minimax-pdf/scripts/cover.py, palette.py | 23, 996, 1097, 1378, 229 | SEC-network-call | Embeds Google Fonts `@import url()` plus an unsanitized `--cover-image` URL into generated HTML, both fetched by a headless browser at render time (SSRF-adjacent if a malicious/internal URL is supplied as `cover_image`). |
| 18 | Medium | planning-with-files/scripts/resolve-plan-dir.sh, check-complete.sh, init-session.sh, session-catchup.py | 109, 35, 183, 93, 128, 153, 189 | SEC-env-read | Reads `PLAN_ID`, `PLANNING_DISABLED` (bypasses the completion gate entirely when `1`), `PWF_GATE_CAP`, `PYTHON_BIN`, `CODEX_THREAD_ID`, `CODEX_SESSIONS_DIR`, `XDG_DATA_HOME`/`OPENCODE_DATA_DIR` from the environment for config/session discovery. |
| 19 | Low | minimax-docx/scripts/setup.sh | 410 | SEC-file-write-outside-repo | Verification test document written to `/tmp/minimax-docx-setup-test-$$.docx`, a predictable filename guarded only by the shell PID. |
| 20 | Low | planning-with-files/scripts/set-active-plan.sh | 35 | SEC-path-traversal | `PLAN_DIR="${PLAN_ROOT}/${PLAN_ID}"` built straight from the first CLI arg with no slug validation, unlike `resolve-plan-dir.sh`'s `slug_is_valid` + containment guard. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | autoresearch/SKILL.md | Skill instructs the model to call `scripts/orchestrate.sh` (classify/next-hop/units/plateau/screen-cmd subcommands), but no `scripts/` directory exists anywhere under `autoresearch/`. | Any agent following the skill's instructions will fail immediately with a file-not-found error; the skill's primary orchestration mechanism is non-functional as written. |
| 2 | huashu-design/SKILL.md | Skill routes to a companion tool/skill named `huashu-gpt-image` (lines 241, 275, 282) for an AI-image-generation fallback, but no such directory or file exists in the repo. | An agent following the documented fallback path will fail to locate the referenced skill, breaking the image-generation fallback flow. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | huashu-design/scripts/html2pptx.js:1097 | Reads `TMPDIR` from environment with no validation | Low risk as-is; document the expected value or fall back safely if unset/invalid. |
| 2 | minimax-pdf/scripts/cover.py, palette.py:23,996,1097,1378,229 | Unsanitized `--cover-image` URL fetched by a headless browser at render time | Restrict `cover_image` to `http(s)`/local-file schemes and reject link-local/metadata IP ranges (e.g. `169.254.169.254`) before passing it to the renderer. |
| 3 | minimax-pdf/scripts/render_cover.js:62 | `spawnSync(..., { shell: true })` with static args | Drop `shell: true` — the args array does not need shell interpretation. |
| 4 | minimax-docx/scripts/setup.sh:410 | Predictable `/tmp` filename (`$$`-based) for the verification test doc | Use `mktemp` instead of a PID-suffixed literal path. |
| 5 | planning-with-files/scripts/set-active-plan.sh:35 | `PLAN_ID` joined into a path with no slug validation | Reuse `resolve-plan-dir.sh`'s `slug_is_valid` + containment check before constructing `PLAN_DIR`. |
| 6 | planning-with-files/scripts/check-complete.sh:35 | `PLANNING_DISABLED=1` env var silently bypasses the entire completion gate | Document this as an intentional escape hatch, or require an explicit flag/log line so a bypassed gate is visible in output. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | planning-with-files/SKILL.md | Vague quantifier "relevant" (×1) | -2 |
| 2 | prototype/SKILL.md | Vague quantifiers "several", "relevant" (×2) | -4 |
| 3 | x-twitter-scraper/SKILL.md | Vague quantifier "relevant" (×2) | -4 |
| 4 | minimax-xlsx/SKILL.md | Description 630 chars (500–800 band) | -5 |
| 5 | teach/SKILL.md | Generic description, restates skill name only | -15 |
| 6 | teach/SKILL.md | Vague quantifiers "several"×2, "relevant"/"highly-relevant"×2 | -8 |
| 7 | get-api-docs/SKILL.md | Description 856 chars (>800) | -10 |
| 8 | get-api-docs/SKILL.md | Vague quantifiers "some", "relevant" | -4 |
| 9 | grilling/SKILL.md | No cross-ref to related planning-with-files/prototype skills | -3 |
| 10 | opencli/opencli-sitemap-author/SKILL.md | Vague quantifier "relevant" (×1) | -2 |
| 11 | opencli/opencli-browser/SKILL.md | Body 439 lines (400–500 band) | -5 |
| 12 | opencli/opencli-browser/SKILL.md | Vague quantifiers "some", "relevant" | -4 |
| 13 | opencli/opencli-browser-sitemap/SKILL.md | Vague quantifier "relevant" (×2) | -4 |
| 14 | opencli/opencli-browser-sitemap/SKILL.md | No cross-ref back to opencli-browser (one-directional handoff) | -3 |
| 15 | opencli/opencli-usage/SKILL.md | Vague quantifier "Some" (×1) | -2 |
| 16 | agent-browser/SKILL.md | Description 925 chars (>800) | -10 |
| 17 | domain-modeling/SKILL.md | No cross-ref to related codebase-design skill | -3 |
| 18 | codebase-design/SKILL.md | Vague quantifiers "correctly", "several" | -4 |
| 19 | codebase-design/SKILL.md | No cross-ref to related domain-modeling skill | -3 |
| 20 | kimi-webbridge/SKILL.md | Description 535 chars (500–800 band) | -5 |
| 21 | kimi-webbridge/SKILL.md | Vague quantifiers "several", "some" | -4 |
| 22 | kimi-webbridge/SKILL.md | No cross-ref to overlapping agent-browser skill | -3 |
| 23 | systematic-debugging/SKILL.md | Vague quantifier "appropriate" (×1) | -2 |
| 24 | find-skills/SKILL.md | Vague quantifier "relevant" (×2) | -4 |
| 25 | tdd/SKILL.md | No code/example blocks in body (delegated to referenced files) | -10 |
| 26 | autoresearch/SKILL.md | Generic description, no concrete invocation trigger | -15 |
| 27 | autoresearch/SKILL.md | Complex orchestration concepts with no worked example | -5 |
| 28 | pptx-generator/SKILL.md | No cross-ref to overlapping huashu-design skill | -3 |
| 29 | find-docs/SKILL.md | Description 878 chars (>800) | -10 |
| 30 | find-docs/SKILL.md | Vague quantifier "relevant" (×3) | -6 |
| 31 | find-docs/SKILL.md | No cross-ref to near-identical get-api-docs skill | -3 |
| 32 | migrate-to-shoehorn/SKILL.md | Vague quantifier "some" (×1) | -2 |
| 33 | gpt-taste/SKILL.md | Generic description, no concrete invocation trigger | -15 |
| 34 | gpt-taste/SKILL.md | Technical GSAP directives with essentially no code examples | -5 |
| 35 | diagnosing-bugs/SKILL.md | Vague quantifier "relevant" (×1) | -2 |
| 36 | minimax-pdf/SKILL.md | Description ~856 chars (>800) | -10 |
| 37 | minimax-pdf/SKILL.md | No cross-ref to sibling minimax-docx/minimax-xlsx skills | -3 |
| 38 | imagegen-frontend-web/SKILL.md | Vague quantifiers, 10 occurrences (capped) | -20 |
| 39 | imagegen-frontend-web/SKILL.md | Body 987 lines (>500) | -10 |
| 40 | imagegen-frontend-web/SKILL.md | Description ~663 chars (500–800 band) | -5 |
| 41 | minimax-docx/SKILL.md | Vague quantifiers "relevant"×6, "as needed"×1 | -14 |
| 42 | minimax-docx/SKILL.md | Description ~645 chars (500–800 band) | -5 |
| 43 | minimax-docx/SKILL.md | No cross-ref to sibling minimax-pdf/minimax-xlsx skills | -3 |
| 44 | huashu-design/SKILL.md | Body 499 lines (400–500 band) | -5 |
| 45 | improve-codebase-architecture/SKILL.md | Generic description, no concrete trigger phrases | -15 |
| 46 | ai-elements/SKILL.md | Vague quantifier "correctly" (×2) | -4 |
| 47 | grill-with-docs/SKILL.md | Generic description, no concrete trigger phrases | -15 |

## Cross-Component
- **Broken references** (also listed as Bugs): `autoresearch/SKILL.md` → `scripts/orchestrate.sh` (missing); `huashu-design/SKILL.md` → `huashu-gpt-image` (missing skill).
- **Unlinked sibling overlap** — several skill pairs cover near-identical or tightly-adjacent ground with no cross-reference in either direction, which risks an agent picking the wrong one or duplicating work:
  - `find-docs/SKILL.md` and `get-api-docs/SKILL.md` — both are "look up third-party API/library docs" skills.
  - `kimi-webbridge/SKILL.md` and `agent-browser/SKILL.md` — both are browser-automation skills; `agent-browser/SKILL.md` even says "prefer agent-browser over any built-in browser automation" but `kimi-webbridge` doesn't reference it.
  - `domain-modeling/SKILL.md` and `codebase-design/SKILL.md` — both are software-design-vocabulary skills.
  - `pptx-generator/SKILL.md` and `huashu-design/SKILL.md` — both target slide-deck generation (huashu-design explicitly lists "PPT/幻灯片" as a trigger).
  - `minimax-pdf/SKILL.md`, `minimax-docx/SKILL.md`, `minimax-xlsx/SKILL.md` — three sibling document-generation skills under the same author, none cross-referencing the others.
  - `opencli/opencli-browser/SKILL.md` → `opencli/opencli-browser-sitemap/SKILL.md` is a one-directional handoff (the former points to the latter; the latter never points back).
- No stale artifact counts, plugin-manifest/disk mismatches, or terminology-drift clusters were observed beyond the above.

## Recommendation
BLOCKED — do not submit PRs. File private security report.

High-severity findings — the `node -e` shell-injection chain in `huashu-design/scripts/render-narration.sh`, the unsigned download-then-execute installer pattern in `minimax-docx/scripts/setup.sh`, and the zip-slip-style path traversal in the three `minimax-xlsx` scripts — require private disclosure to the maintainer before any public PR activity. Once those are resolved (or the maintainer clears them), the two NL bugs (`autoresearch/SKILL.md`, `huashu-design/SKILL.md` broken references) and the Medium/Low security fixes listed above are safe to submit as follow-up PRs.
