# NLPM Audit: JuliusBrussee/cavekit
**Date**: 2026-04-06  |  **Artifacts**: 9  |  **Strategy**: single
**NL Score**: 97/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 8  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/check.md | command | 93 | Missing allowed-tools; vague "relevant" |
| commands/build.md | command | 95 | Missing allowed-tools |
| commands/spec.md | command | 95 | Missing allowed-tools |
| skills/backprop/SKILL.md | skill | 96 | Vague "sometimes", "usually" |
| skills/check/SKILL.md | skill | 98 | Vague "relevant" |
| .claude-plugin/plugin.json | manifest | 100 | None |
| skills/build/SKILL.md | skill | 100 | None |
| skills/caveman/SKILL.md | skill | 100 | None |
| skills/spec/SKILL.md | skill | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | None |
| Scripts | None |
| MCP configs | None |
| Package manifests | None |

### Security Findings
No security findings.

## Bugs (PR-worthy)
No bugs found. All required frontmatter fields present. FORMAT.md referenced by commands/spec.md, commands/build.md, and skills/spec/SKILL.md exists at repo root. No broken cross-references.

## Security Fixes (PR-worthy, Medium/Low only)
No security fixes required.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/build.md | Missing `allowed-tools` in frontmatter — Bash and Write/Edit tools used but undeclared | -5 |
| 2 | commands/check.md | Missing `allowed-tools` in frontmatter — Read and Grep tools used but undeclared | -5 |
| 3 | commands/check.md | Vague quantifier "relevant" in CHECK §V step 2: "Grep / read relevant files" | -2 |
| 4 | commands/spec.md | Missing `allowed-tools` in frontmatter — Read and Write tools used but undeclared | -5 |
| 5 | skills/backprop/SKILL.md | Vague quantifier "sometimes" in ANALYZE section (step 2) | -2 |
| 6 | skills/backprop/SKILL.md | Vague quantifier "usually" in OUTPUT SHAPE section: "§V entry (usually)" | -2 |
| 7 | skills/check/SKILL.md | Vague quantifier "relevant" in CHECK §V step 2: "Grep / read relevant files" | -2 |
| 8 | commands/check.md | Empty-argument handling implicit (default = §V) rather than explicit; minor clarity gap | 0 (informational) |

## Cross-Component
- **commands/ ↔ skills/ alignment**: Strong. Each command (build, check, spec) maps cleanly to a same-named skill plus the shared caveman skill. The backprop skill is cross-referenced correctly from both commands/build.md and skills/build/SKILL.md.
- **FORMAT.md dependency**: Three artifacts (commands/spec.md, commands/build.md, skills/spec/SKILL.md) reference `FORMAT.md` at repo root. File confirmed present — no broken reference.
- **commands/build.md vs skills/build/SKILL.md**: Command uses `/spec bug: <cause>` slash-command syntax; skill correctly says "invoke spec skill with `bug: <cause>`". Consistent intent, different invocation surface — acceptable given command vs skill context.
- **Vague "relevant files" duplication**: Both commands/check.md and skills/check/SKILL.md contain the same vague phrase "Grep / read relevant files". Fixing one should propagate to both.
- No orphaned components. No contradictions found.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

No bugs or security issues require remediation. The three quality items worth addressing are:
1. Add `allowed-tools` frontmatter to all three commands (build, check, spec) to make tool dependencies explicit.
2. Replace "relevant files" with a more specific phrase in commands/check.md and skills/check/SKILL.md (e.g., "files cited in §V invariants").
3. Replace "sometimes" and "usually" in skills/backprop/SKILL.md with deterministic phrasing (e.g., "if §I shape mismatch" and "§V entry added unless purely mechanical typo — see WHEN NOT TO ADD §V").
