# NLPM Audit: AgriciDaniel/claude-blog
**Date**: 2026-04-06  |  **Artifacts**: 28  |  **Strategy**: batched
**NL Score**: 92/100
**Security**: BLOCKED
**Bugs**: 1  |  **Quality Issues**: 15  |  **Security Findings**: 4

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/blog-researcher.md | Agent | 72 | No model declared, no examples, vague quantifiers ("suitable", "appropriate") |
| agents/blog-writer.md | Agent | 76 | No model declared, no examples, vague quantifiers |
| agents/blog-reviewer.md | Agent | 77 | No model declared, no examples, Bash tool declared but unused |
| agents/blog-seo.md | Agent | 80 | No model declared, no examples |
| skills/blog-write/SKILL.md | Skill | 88 | Vague quantifiers ("appropriate", "relevant", "suitable") totaling −12 pts |
| CLAUDE.md | Doc | 88 | Not an NL artifact; contains curl-pipe-sh install command (security) |
| skills/blog-strategy/SKILL.md | Skill | 92 | Vague quantifiers ("appropriate", "relevant", "authentic") −8 pts |
| skills/blog-brief/SKILL.md | Skill | 93 | Vague quantifiers ("appropriate", "relevant") −4 pts |
| skills/blog/SKILL.md | Skill | 93 | Vague quantifiers ("appropriate") −4 pts |
| skills/blog-rewrite/SKILL.md | Skill | 94 | Vague quantifiers ("appropriate", "relevant") −6 pts |
| skills/blog-cannibalization/SKILL.md | Skill | 95 | Minor vague terms |
| skills/blog-calendar/SKILL.md | Skill | 95 | Minor vague terms |
| .claude-plugin/plugin.json | Manifest | 95 | No NL structure (manifest only) |
| skills/blog-factcheck/SKILL.md | Skill | 96 | Minimal vague |
| skills/blog-notebooklm/SKILL.md | Skill | 96 | Minimal |
| skills/blog-image/SKILL.md | Skill | 96 | Minimal |
| skills/blog-taxonomy/SKILL.md | Skill | 96 | Minimal |
| skills/blog-audio/SKILL.md | Skill | 96 | Minimal |
| skills/blog-google/SKILL.md | Skill | 96 | Minimal |
| skills/blog-outline/SKILL.md | Skill | 96 | Minimal |
| skills/blog-repurpose/SKILL.md | Skill | 96 | Minimal |
| skills/blog-persona/SKILL.md | Skill | 97 | Nearly clean |
| skills/blog-chart/SKILL.md | Skill | 97 | Nearly clean |
| skills/blog-geo/SKILL.md | Skill | 97 | Nearly clean |
| skills/blog-schema/SKILL.md | Skill | 97 | Nearly clean |
| skills/blog-seo-check/SKILL.md | Skill | 97 | Nearly clean |
| skills/blog-audit/SKILL.md | Skill | 97 | Nearly clean |
| skills/blog-analyze/SKILL.md | Skill | 98 | Nearly clean |

**Weighted average**: 2586 / 28 = **92/100**

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 1 |
| Medium | 2 |
| Low | 0 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts (`.sh`, `.py`) | 35 (install.sh, uninstall.sh, scripts/analyze_blog.py, skills/blog-audio/scripts/*.py ×4, skills/blog-google/scripts/*.py ×11, skills/blog-image/scripts/*.py ×2, skills/blog-notebooklm/scripts/*.py ×9, tests/*.py ×2) |
| MCP configs | 1 (.mcp.json) |
| Package manifests | 1 (requirements.txt) |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | CLAUDE.md | 119 | SEC-curl-pipe-sh | `curl -sL https://raw.githubusercontent.com/AgriciDaniel/claude-blog/main/install.sh \| bash` is documented as the recommended standalone install method. An attacker who compromises the GitHub repository or performs MITM on the raw.githubusercontent.com URL can deliver and execute arbitrary code on the installer's machine without any signature verification. |
| 2 | High | .mcp.json | 5 | SEC-postinstall-script | `"command": "npx", "args": ["-y", "@ycse/nanobanana-mcp"]` auto-installs and executes an npm package every time the MCP server starts. The `-y` flag suppresses the confirmation prompt. A typosquatted or compromised `@ycse/nanobanana-mcp` package would silently execute in Claude Code's process context. |
| 3 | Medium | skills/blog-notebooklm/scripts/run.py | 73 | SEC-path-traversal | `script_path = skill_dir / "scripts" / script_name` where `script_name` is taken directly from `sys.argv[1]` without sanitization. Python's `pathlib` does not strip `../` sequences; a crafted argument such as `../../../../../../bin/python` resolves to an absolute path outside the scripts directory. The same pattern appears in skills/blog-audio/scripts/run.py:73 and skills/blog-google/scripts/run.py:73. |
| 4 | Medium | install.sh | 110 | SEC-unpinned-semver | `pip3 install --quiet -r requirements.txt` is called without `--require-hashes`. `requirements.txt` uses range pins (`>=0.7.3,<1.0.0`) but no hash verification. A dependency-confusion or typosquatting attack against `textstat` or `beautifulsoup4` on PyPI could substitute a malicious build at install time. |

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | skills/blog-write/SKILL.md | References `references/cta-placement.md` at lines 161 and 165, but this file is not listed in the CLAUDE.md architecture (which enumerates 13 of the stated 14 reference files). If the file is absent, the writer agent silently misses CTA placement guidance. | Writer agent receives incomplete instructions for CTA placement; posts may have arbitrary CTA positioning. |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/blog-notebooklm/scripts/run.py (and blog-audio, blog-google) | Path traversal: `script_name` from argv not sanitized before use in `Path / script_name` | Add `script_name = Path(script_name).name` (basename only, strips directories) before constructing `script_path`; reject names containing `/` or `..`. |
| 2 | install.sh | `pip3 install -r requirements.txt` without hash verification | Add `--require-hashes` to the pip call, or pin hashes in `requirements.txt` via `pip-compile --generate-hashes`. |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/blog-seo.md | No model declared in frontmatter | −5 |
| 2 | agents/blog-reviewer.md | No model declared in frontmatter | −5 |
| 3 | agents/blog-writer.md | No model declared in frontmatter | −5 |
| 4 | agents/blog-researcher.md | No model declared in frontmatter | −5 |
| 5 | agents/blog-seo.md | Zero example blocks | −15 |
| 6 | agents/blog-reviewer.md | Zero example blocks | −15 |
| 7 | agents/blog-writer.md | Zero example blocks | −15 |
| 8 | agents/blog-researcher.md | Zero example blocks | −15 |
| 9 | agents/blog-reviewer.md | `Bash` declared in `tools` but never invoked in workflow; agent only reads files and produces a scoring report | −3 |
| 10 | agents/blog-researcher.md | Vague quantifiers: "suitable" (×2), "appropriate" (×2), "relevant" (×1) — 5 instances × −2 (capped) | −8 |
| 11 | agents/blog-writer.md | Vague quantifiers: "natural" (×1), "relevant" (×1) | −4 |
| 12 | skills/blog-write/SKILL.md | Vague quantifiers: "appropriate" (×2), "relevant" (×3), "suitable" (×1) — 6 instances | −12 |
| 13 | skills/blog-strategy/SKILL.md | Vague quantifiers: "appropriate" (×1), "relevant" (×2), "authentic" (×1) — 4 instances | −8 |
| 14 | skills/blog-rewrite/SKILL.md | Vague quantifiers: "appropriate" (×1), "relevant" (×2) — 3 instances | −6 |
| 15 | skills/blog-brief/SKILL.md | Vague quantifiers: "appropriate" (×1), "relevant" (×1) — 2 instances | −4 |

## Cross-Component

**References**: All four agents reference external skill files (e.g., `blog-writer.md` is referenced from `blog-rewrite/SKILL.md` for the banned AI phrase list). This cross-agent reference is valid and consistent.

**Version consistency**: `plugin.json` and `skills/blog/SKILL.md` both report version `1.6.9`. Sub-skill versions (`blog-image` at `1.4.0`, `blog-notebooklm` at `1.0.0`) are independent component versions — acceptable.

**Artifact count**: CLAUDE.md states 22 sub-skills and 4 agents. Audit confirmed 22 skills and 4 agents — consistent.

**Missing reference file**: `skills/blog-write/SKILL.md` cites `references/cta-placement.md` in two places. CLAUDE.md lists 13 named reference files against a stated total of 14; `cta-placement.md` could be the 14th unlisted file, but its absence from the architecture summary is an inconsistency. Flagged as Bug #1 above.

**Terminology consistency**: "answer-first formatting", "citation capsule", "information gain marker", and "TL;DR box / Key Takeaways" are used consistently across `blog-write`, `blog-rewrite`, `blog-analyze`, `blog-geo`, and the four agents. No terminology drift detected.

## Recommendation

BLOCKED — do not submit PRs. File private security report.

The Critical finding (curl-pipe-sh install pattern in CLAUDE.md) and High finding (npx auto-install in .mcp.json) require private disclosure to the maintainer before any public PRs are opened. The NL quality is strong (92/100) and there is only one structural bug, but the security gate must be cleared first.

After the maintainer acknowledges the security disclosures:
- Submit Bug PR for the `cta-placement.md` broken reference.
- Submit Medium security fix PRs for path traversal sanitization and pip hash pinning.
- File quality suggestions as a single consolidated issue (not individual PRs) covering model declarations and examples for all four agents.
