# NLPM Audit: vstorm-co/pydantic-deepagents
**Date**: 2026-04-06  |  **Artifacts**: 31  |  **Strategy**: batched
**NL Score**: 93/100
**Security**: BLOCKED
**Bugs**: 2  |  **Quality Issues**: 25  |  **Security Findings**: 6

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| apps/cli/skills/verification-strategy/SKILL.md | skill | 88 | Missing output format; vague "reasonable" (-12) |
| pydantic_deep/bundled_skills/verification-strategy/SKILL.md | skill | 88 | Identical to cli counterpart; same issues (-12) |
| apps/cli/skills/build-and-compile/SKILL.md | skill | 90 | Missing output format section (-10) |
| apps/cli/skills/refactor/SKILL.md | skill | 90 | Missing output format section (-10) |
| apps/cli/skills/performant-code/SKILL.md | skill | 90 | Missing output format section (-10) |
| apps/cli/skills/data-formats/SKILL.md | skill | 90 | Missing output format section (-10) |
| apps/cli/skills/systematic-debugging/SKILL.md | skill | 90 | Missing output format section (-10) |
| apps/cli/skills/git-workflow/SKILL.md | skill | 90 | Missing output format section (-10) |
| apps/cli/skills/environment-discovery/SKILL.md | skill | 90 | Missing output format section (-10) |
| apps/deepresearch/skills/diagram-design/SKILL.md | skill | 90 | Missing output format section (-10) |
| pydantic_deep/bundled_skills/build-and-compile/SKILL.md | skill | 90 | Duplicate of cli/build-and-compile; missing output format (-10) |
| pydantic_deep/bundled_skills/refactor/SKILL.md | skill | 90 | Duplicate of cli/refactor; missing output format (-10) |
| pydantic_deep/bundled_skills/performant-code/SKILL.md | skill | 90 | Duplicate of cli/performant-code; missing output format (-10) |
| pydantic_deep/bundled_skills/data-formats/SKILL.md | skill | 90 | Duplicate of cli/data-formats; missing output format (-10) |
| pydantic_deep/bundled_skills/systematic-debugging/SKILL.md | skill | 90 | Duplicate of cli/systematic-debugging; missing output format (-10) |
| pydantic_deep/bundled_skills/git-workflow/SKILL.md | skill | 90 | Duplicate of cli/git-workflow; missing output format (-10) |
| pydantic_deep/bundled_skills/environment-discovery/SKILL.md | skill | 90 | Duplicate of cli/environment-discovery; missing output format (-10) |
| examples/full_app/skills/code-review/SKILL.md | skill | 92 | Broken ref to `example_review.md`; vague: clear, proper x3 (-8) |
| examples/skills/code-review/SKILL.md | skill | 92 | Identical to full_app version; broken ref, vague quantifiers (-8) |
| apps/deepresearch/skills/research-methodology/SKILL.md | skill | 93 | Weak output format coverage; vague "comprehensively" (-7) |
| examples/full_app/skills/data-analysis/SKILL.md | skill | 94 | Vague: appropriate, clearly, relevant (-6) |
| CLAUDE.md | context | 95 | Vague "sensible defaults" (-2); otherwise precise and comprehensive |
| examples/full_app/skills/test-generator/SKILL.md | skill | 98 | Vague "when possible" (-2) |
| examples/skills/test-generator/SKILL.md | skill | 98 | Identical to full_app version; vague "when possible" (-2) |
| apps/deepresearch/skills/report-writing/SKILL.md | skill | 98 | Vague "clear" in style guidance (-2) |
| apps/cli/skills/code-review/SKILL.md | skill | 100 | Clean — precise output format, no vague language |
| apps/cli/skills/test-writer/SKILL.md | skill | 100 | Clean — naming convention serves as output format |
| apps/cli/skills/skill-creator/SKILL.md | skill | 100 | Clean — embedded template defines output format |
| pydantic_deep/bundled_skills/code-review/SKILL.md | skill | 100 | Identical to cli/code-review; clean |
| pydantic_deep/bundled_skills/test-writer/SKILL.md | skill | 100 | Identical to cli/test-writer; clean |
| pydantic_deep/bundled_skills/skill-creator/SKILL.md | skill | 100 | Identical to cli/skill-creator; clean |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 2 |
| High | 0 |
| Medium | 3 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Shell scripts | `install.sh` |
| Python source (subprocess calls) | `apps/harbor/agent.py`, `apps/cli/commands.py`, `apps/cli/local_context.py`, `apps/cli/update.py`, `apps/cli/app.py`, `apps/deepresearch/src/deepresearch/config.py` |
| Embedded shell template | `apps/harbor/agent.py` (Docker container init script string) |
| Package manifest | `pyproject.toml` |
| MCP configs | None found |
| Hooks | None found |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | CRITICAL | `install.sh` | 38 | curl-pipe-to-sh | `curl -LsSf https://astral.sh/uv/install.sh \| sh` — downloads and immediately executes a remote shell script with no integrity check (no `--sha256` or signature verification). Susceptible to supply-chain compromise or MitM if HTTPS is stripped. |
| 2 | CRITICAL | `apps/harbor/agent.py` | 320 | curl-pipe-to-sh | Same `curl ... \| sh` pattern embedded inside a Docker container init template string. The template is injected into every spawned harbor container at runtime, propagating the risk to all cloud agent instances. |
| 3 | MEDIUM | `install.sh` | 63 | PATH modification | `export PATH="$HOME/.local/bin:$PATH"` prepends a user-writable directory to PATH, potentially shadowing system binaries if an attacker controls that directory. |
| 4 | MEDIUM | `apps/harbor/agent.py` | 321, 330 | PATH modification | Two `export PATH=...` statements in the container init template prepend both `$HOME/.local/bin` and the venv bin dir; same shadowing risk as finding #3, scoped to Docker containers. |
| 5 | MEDIUM | `apps/harbor/agent.py` | 333 | runtime install from external git ref | `uv pip install "pydantic-deep[cli] @ git+{_GIT_REPO}@{git_ref}"` — if `git_ref` is attacker-influenced, this enables installing an arbitrary commit or branch. The variable should be validated against an allowlist (e.g., semver tag regex) before insertion. |
| 6 | LOW | `pyproject.toml` | 42–50 | unpinned upper bounds | All runtime dependencies use `>=` minimum-only constraints (e.g., `pydantic-ai-slim[web-fetch]>=1.77.0`). The `uv.lock` lockfile mitigates this for reproducible installs, but users who install without the lockfile (`pip install pydantic-deep`) get unconstrained versions. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `examples/full_app/skills/code-review/SKILL.md` | Line 67 references `example_review.md` ("See `example_review.md` for a sample code review output") but no such file exists in the directory | Broken link confuses users; skill appears incomplete when loaded in an agent context |
| 2 | `examples/skills/code-review/SKILL.md` | Identical broken reference to `example_review.md` | Same impact as bug #1; affects the standalone examples/ variant of the skill |

## Security Fixes (PR-worthy, Medium/Low only)
**BLOCKED** — Critical findings (#1 and #2) must be privately disclosed and resolved before any PRs are submitted. Do not open public issues or PRs referencing these findings until the maintainer has acknowledged the report.

Once the critical findings are cleared, the following Medium/Low fixes are suitable for public PRs:

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `install.sh` | PATH prepend to user-writable directory (finding #3) | Move `export PATH=...` after the uv install check; document the risk in install docs |
| 2 | `apps/harbor/agent.py` | Unsanitized `git_ref` passed to `uv pip install` (finding #5) | Validate `git_ref` against `^v?\d+\.\d+\.\d+$` or an explicit allowlist before string interpolation |
| 3 | `pyproject.toml` | Uncapped dependency ranges (finding #6) | Add upper bounds (e.g., `>=1.77.0,<2.0`) for major dependencies, or document that `uv.lock` must be used for reproducible installs |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `apps/cli/skills/verification-strategy/SKILL.md` | No output format section; "reasonable" is a vague quantifier | -12 |
| 2 | `pydantic_deep/bundled_skills/verification-strategy/SKILL.md` | Exact duplicate of cli counterpart; inherits same issues | -12 |
| 3 | `apps/cli/skills/build-and-compile/SKILL.md` | No output format section describing how the agent should present build results | -10 |
| 4 | `apps/cli/skills/refactor/SKILL.md` | No output format section; agents have no guidance on how to summarise refactoring changes | -10 |
| 5 | `apps/cli/skills/performant-code/SKILL.md` | No output format section; agents have no guidance on how to report performance findings | -10 |
| 6 | `apps/cli/skills/data-formats/SKILL.md` | No output format section | -10 |
| 7 | `apps/cli/skills/systematic-debugging/SKILL.md` | No output format section; a structured "debug report" format would help consumers | -10 |
| 8 | `apps/cli/skills/git-workflow/SKILL.md` | No output format section | -10 |
| 9 | `apps/cli/skills/environment-discovery/SKILL.md` | No output format section | -10 |
| 10 | `apps/deepresearch/skills/diagram-design/SKILL.md` | No output format section; also missing `version` and `tags` frontmatter fields | -10 |
| 11–17 | `pydantic_deep/bundled_skills/{build-and-compile,refactor,performant-code,data-formats,systematic-debugging,git-workflow,environment-discovery}/SKILL.md` | Exact duplicates of corresponding cli skills; all 7 inherit the missing output format issue | -10 each |
| 18 | `examples/full_app/skills/code-review/SKILL.md` | Four vague quantifiers: "clear" responsibilities, "proper" use of type hints, "proper" exception handling, "properly" cleaned up | -8 |
| 19 | `examples/skills/code-review/SKILL.md` | Identical content to full_app version; same four vague quantifiers | -8 |
| 20 | `examples/full_app/skills/data-analysis/SKILL.md` | Vague: "when appropriate" (visualizations), "clearly" (summarise findings), "relevant" (statistics) | -6 |
| 21 | `apps/deepresearch/skills/research-methodology/SKILL.md` | Weak output format coverage (note-taking template present but no agent response format); vague "comprehensively"; missing `version` and `tags` | -7 |
| 22 | `apps/deepresearch/skills/report-writing/SKILL.md` | Vague "clear, direct language" in style guidance; missing `version` and `tags` frontmatter | -2 |
| 23 | `examples/full_app/skills/test-generator/SKILL.md` | Vague "when possible" in best practices | -2 |
| 24 | `examples/skills/test-generator/SKILL.md` | Identical to full_app version; vague "when possible" | -2 |
| 25 | `CLAUDE.md` | "sensible defaults" in `create_default_deps()` description is mildly vague | -2 |

## Cross-Component

**Duplicate skill trees** — `apps/cli/skills/` and `pydantic_deep/bundled_skills/` are byte-for-byte identical across all 11 shared files. Any fix to one set must be manually replicated to the other. Consider symlinks, a build step that copies them, or a single canonical path with a reference in the other location. This duplication also means the missing output format issues (#3–9 and #11–17 above) represent only 9 unique fixes needed, not 16.

**Inconsistent frontmatter across skill groups** — The `apps/cli/` and `pydantic_deep/bundled_skills/` files all include `version: "1.0.0"` and `tags: [...]`. The three `apps/deepresearch/` skills omit both fields. `diagram-design` also omits `auto_load`, while `research-methodology` and `report-writing` include it. A shared frontmatter schema would prevent drift.

**Example skills lag behind production skills** — `examples/full_app/skills/code-review/` and `examples/skills/code-review/` use a lower-quality version of the code-review skill (references a missing file, more vague language) compared to `apps/cli/skills/code-review/SKILL.md`. Users reading the examples directory get an inferior mental model of the skill format.

**No commands or agents present** — All 30 NL artifacts are skills (plus one CLAUDE.md). No command or agent definitions were found in the repo root or app directories. The repo ships skills as a library component but delegates orchestration to consumers.

## Recommendation

**BLOCKED** — do not submit PRs. File a private security report.

Two critical `curl | sh` patterns were found: one in the documented installer (`install.sh`) and one embedded in the harbor Docker container init template (`apps/harbor/agent.py`). These must be addressed via private disclosure before any public PR activity.

Suggested private report contents:
- Finding #1: `install.sh:38` — propose replacing `curl | sh` with a checksum-verified download or a `uv` bootstrap that pins a known-good release hash.
- Finding #2: `apps/harbor/agent.py:320` — propose the same fix applied to the container init template, plus input validation for `git_ref` (finding #5).

Once the security gate is cleared, submit separate PRs for:
1. Bug fixes: add `example_review.md` (or remove the broken reference) in both `examples/` code-review skills.
2. DRY: consolidate `apps/cli/skills/` and `pydantic_deep/bundled_skills/` to a single canonical source.
3. Output format: add an `## Output Format` section to the 9 cli/bundled skills that lack one.
4. Frontmatter consistency: add `version` and `tags` to the three `apps/deepresearch/` skills.
