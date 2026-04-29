# NLPM Audit: safishamsi/graphify

**Date**: 2026-04-29  |  **Artifacts**: 13  |  **Strategy**: single
**NL Score**: 58/100
**Security**: REVIEW
**Bugs**: 3  |  **Quality Issues**: 6  |  **Security Findings**: 4

graphify is a 37k-star Python CLI distributed as a multi-tool AI coding assistant skill (Claude Code, Codex, OpenCode, Cursor, Aider, OpenClaw, Factory Droid, Trae, GitHub Copilot CLI, Kiro, VSCode, Windows). It builds knowledge graphs from arbitrary code/doc/media folders. This audit was triggered manually after the discovery probe missed the repo's NL artifacts due to non-canonical paths (`graphify/skill*.md` and `AGENTS.md` rather than the canonical `skills/<name>/SKILL.md`). The discovery-probe gap is filed separately as a v0.7.18 fix.

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| AGENTS.md | claude-md | 72 | No `<example>` blocks; "graphify update" instruction is stale relative to skill.md |
| graphify/skill-windows.md | skill | 61 | Best variant — full PowerShell port with Windows-specific troubleshooting |
| graphify/skill.md | skill | 58 | Non-canonical path; no examples; interpreter-cache path drift bug |
| graphify/skill-codex.md | skill | 57 | Differentiated B2 (spawn_agent API) but stale on later features |
| graphify/skill-droid.md | skill | 57 | Differentiated B2 (Task tool) but stale |
| graphify/skill-copilot.md | skill | 57 | No justified divergence — functionally identical to skill.md |
| graphify/skill-kiro.md | skill | 57 | Identical to skill-copilot.md (one of these is redundant) |
| graphify/skill-aider.md | skill | 56 | Stale variant + interpreter-cache path drift bug |
| graphify/skill-claw.md | skill | 56 | Stale variant + path drift bug |
| graphify/skill-opencode.md | skill | 56 | Near-duplicate of skill-claw |
| graphify/skill-trae.md | skill | 56 | Reproducible Python SyntaxError at line 829 (--cluster-only block) |
| graphify/skill-vscode.md | skill | 52 | Most-degraded — strips ~70% of features incl. broken merge step |

**Weighted average**: 58/100

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 3 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks (Python) | graphify/hooks.py |
| Scripts (Python) | graphify/__main__.py, detect.py, ingest.py, security.py |
| MCP configs | none |
| Package manifest | pyproject.toml (no lockfile) |
| Bash in commands | graphify/skill.md (documentation, capped at Low) |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | graphify/__main__.py | 922 | SEC-allowlist-bypass | `_clone_repo` GitHub URL regex matches `github.com.evil.com/x/y`; allowlist is too loose — should be `url.startswith("https://github.com/")` |
| 2 | Medium | graphify/__main__.py | 948 | SEC-path-traversal | `--out` / `--dir` accept arbitrary writable paths (e.g. `/etc`, `~/.ssh`) with no containment check (same in ingest.py:1356) |
| 3 | Medium | graphify/security.py | 52 | SEC-ssrf-blocklist-narrow | SSRF blocklist for cloud metadata is narrower than the IP check it supplements; missing `metadata.aws.internal` aliases — defense-in-depth gap, not a bypass |
| 4 | Low | pyproject.toml | 13 | SEC-unpinned-deps | All 20+ dependencies unpinned, no lockfile committed |
| 5 | Low | graphify/skill.md | 111 | SEC-runtime-install | Skill instructs the agent to run `pip install graphifyy` at runtime if import fails — capped at Low (documentation), but the package name `graphifyy` (double-y) differs from the GitHub repo name `graphify` and is squatting-prone |
| 6 | Low | graphify/hooks.py | 64 | SEC-shell-exec-context | Git hook executes `$GRAPHIFY_PYTHON -c "..."` with allowlist filter and env-var (not shell interpolation) — Low risk, mitigations in place |

The security infrastructure (`security.py`) is thoughtfully built — scheme allowlisting, redirect re-validation, DNS-rebind protection via socket patching, size caps. The Medium findings are incremental hardening, not fundamental design flaws.

## Bugs (PR-worthy)

| # | File | Issue | Confidence | Evidence | Impact |
|---|------|-------|------------|----------|--------|
| 1 | graphify/skill-trae.md | Line 829: `'output':': 0}` — stray colon in Python dict literal | high | Python parser rejects the literal as SyntaxError; `ast.parse` fails on the embedded code block | `--cluster-only` raises SyntaxError when invoked via the Trae variant of the skill |
| 2 | graphify/skill.md (and 7 variants) | Step 1 writes `graphify-out/.graphify_python`; Step 3A reads `.graphify_python` (no prefix) | high | grep confirms two conventions; `cat .graphify_python` from a clean cwd raises `No such file or directory` | First run after a fresh clone fails to find the cached interpreter path |
| 3 | graphify/skill-vscode.md | Line 154: `for chunk_json in []:` — empty placeholder loop with `# PASTE each subagent response here` comment above | high | Loop iterates over a literal empty list; the merge step silently produces a no-op graph | User running `/graphify --update` on VSCode gets a zero-node graph after merge |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | All 11 skill variants | No `<example>` blocks anywhere | -15 each |
| 2 | All variants | No `version` field in frontmatter (R03) | -5 each |
| 3 | All variants | Non-canonical skill path (R12) — note: multi-tool skill, may be intentional | -10 each |
| 4 | aider, claw, opencode, copilot, kiro | Stale: missing GitHub URL clone, `--wiki`, `--obsidian-dir`, uv detection, Node ID format spec, YouTube URL type | -5 each |
| 5 | skill-vscode.md | Most-degraded variant: 70% feature regression, no incremental update, no SVG, no wiki, no GraphML, no Neo4j | -10 |
| 6 | skill-windows.md | uv detection absent from Step 1 despite Windows being a primary uv-install target | -3 |

## Cross-Component

1. **Duplicate variants with no differentiation**: `skill-copilot.md` and `skill-kiro.md` are functionally identical to each other and to `skill.md`. Neither has a unique Step B2. One should be deleted; the other can stay if the platform has a documented agent-dispatch mechanism.

2. **Stale divergence pattern**: 5 variants (aider, claw, opencode, copilot, kiro) are missing features added to `skill.md` after the variants were forked. Either sync them or extract a shared base with tool-specific override sections.

3. **AGENTS.md is stale relative to skill.md**: The "run `graphify update .`" rule doesn't capture the AST-only optimization documented in skill.md's `--update` section.

4. **skill-vscode.md is diverged beyond maintenance**: Not a port (unlike skill-windows.md) — a partial rewrite missing most features. Either bring to parity or deprecate.

## Recommendation

**REVIEW + selective contribution.** The 3 reproducible bugs are PR-worthy. The security findings are disclosable (no Critical/High) but the maintainer should be told.

The 11-variant maintenance pattern is the deeper architectural concern — graphify is paying linear-cost-per-tool for skill ports when most could share a base. Worth flagging in the audit issue but not a PR target (too large a refactor for a drive-by contribution).

The 3 PRs the contribute step will ship:

| Bug | Target | One-line change |
|-----|--------|-----------------|
| trae syntax error | `graphify/skill-trae.md:829` | `'output':': 0}` → `'output': 0}` |
| path-prefix drift | `graphify/skill.md` (+7 sibling variants) | Unify all interpreter-cache references to `graphify-out/.graphify_python` |
| vscode empty merge | `graphify/skill-vscode.md:153-155` | Replace `for chunk_json in []:` with file-glob-based collection |

Multi-file fix #2 (path-prefix drift across 8 sibling files) is too large for a single contribute PR — recommend splitting into 8 file-scoped PRs OR fixing only the canonical `skill.md` and letting sibling-file drift surface as a follow-up. The first-contact PR cap of 3 limits the contribute step's scope; the path-prefix bug should ship as one consolidated PR targeting `skill.md` only.
