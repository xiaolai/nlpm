# NLPM Audit: codeaholicguy/ai-devkit
**Date**: 2026-04-06  |  **Artifacts**: 71  |  **Strategy**: progressive
**NL Score**: 96/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 62  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .cursor/commands/technical-writer-review.md | command | 85 | No empty input handling (-10), no allowed-tools (-5) |
| .claude/commands/capture-knowledge.md | command | 95 | Missing allowed-tools |
| .claude/commands/check-implementation.md | command | 95 | Missing allowed-tools |
| .claude/commands/code-review.md | command | 95 | Missing allowed-tools |
| .claude/commands/debug.md | command | 95 | Missing allowed-tools |
| .claude/commands/execute-plan.md | command | 95 | Missing allowed-tools |
| .claude/commands/new-requirement.md | command | 95 | Missing allowed-tools |
| .claude/commands/remember.md | command | 95 | Missing allowed-tools |
| .claude/commands/review-design.md | command | 95 | Missing allowed-tools |
| .claude/commands/review-requirements.md | command | 95 | Missing allowed-tools |
| .claude/commands/simplify-implementation.md | command | 95 | Missing allowed-tools |
| .claude/commands/update-planning.md | command | 95 | Missing allowed-tools |
| .claude/commands/writing-test.md | command | 95 | Missing allowed-tools |
| packages/cli/templates/commands/capture-knowledge.md | command | 95 | Missing allowed-tools |
| packages/cli/templates/commands/check-implementation.md | command | 95 | Missing allowed-tools |
| packages/cli/templates/commands/code-review.md | command | 95 | Missing allowed-tools |
| packages/cli/templates/commands/debug.md | command | 95 | Missing allowed-tools |
| packages/cli/templates/commands/execute-plan.md | command | 95 | Missing allowed-tools |
| packages/cli/templates/commands/new-requirement.md | command | 95 | Missing allowed-tools |
| packages/cli/templates/commands/remember.md | command | 95 | Missing allowed-tools |
| packages/cli/templates/commands/review-design.md | command | 95 | Missing allowed-tools |
| packages/cli/templates/commands/review-requirements.md | command | 95 | Missing allowed-tools |
| packages/cli/templates/commands/simplify-implementation.md | command | 95 | Missing allowed-tools |
| packages/cli/templates/commands/update-planning.md | command | 95 | Missing allowed-tools |
| packages/cli/templates/commands/writing-test.md | command | 95 | Missing allowed-tools |
| .codex/commands/capture-knowledge.md | command | 95 | Missing allowed-tools |
| .codex/commands/check-implementation.md | command | 95 | Missing allowed-tools |
| .codex/commands/code-review.md | command | 95 | Missing allowed-tools |
| .codex/commands/debug.md | command | 95 | Missing allowed-tools |
| .codex/commands/execute-plan.md | command | 95 | Missing allowed-tools |
| .codex/commands/new-requirement.md | command | 95 | Missing allowed-tools |
| .codex/commands/remember.md | command | 95 | Missing allowed-tools |
| .codex/commands/review-design.md | command | 95 | Missing allowed-tools |
| .codex/commands/review-requirements.md | command | 95 | Missing allowed-tools |
| .codex/commands/simplify-implementation.md | command | 95 | Missing allowed-tools |
| .codex/commands/update-planning.md | command | 95 | Missing allowed-tools |
| .codex/commands/writing-test.md | command | 95 | Missing allowed-tools |
| .cursor/commands/capture-knowledge.md | command | 95 | Missing allowed-tools |
| .cursor/commands/check-implementation.md | command | 95 | Missing allowed-tools |
| .cursor/commands/code-review.md | command | 95 | Missing allowed-tools |
| .cursor/commands/debug.md | command | 95 | Missing allowed-tools |
| .cursor/commands/execute-plan.md | command | 95 | Missing allowed-tools |
| .cursor/commands/new-requirement.md | command | 95 | Missing allowed-tools |
| .cursor/commands/remember.md | command | 95 | Missing allowed-tools |
| .cursor/commands/review-design.md | command | 95 | Missing allowed-tools |
| .cursor/commands/review-requirements.md | command | 95 | Missing allowed-tools |
| .cursor/commands/simplify-implementation.md | command | 95 | Missing allowed-tools |
| .cursor/commands/update-planning.md | command | 95 | Missing allowed-tools |
| .cursor/commands/writing-test.md | command | 95 | Missing allowed-tools |
| commands/capture-knowledge.md | command | 95 | Missing allowed-tools |
| commands/check-implementation.md | command | 95 | Missing allowed-tools |
| commands/code-review.md | command | 95 | Missing allowed-tools |
| commands/debug.md | command | 95 | Missing allowed-tools |
| commands/execute-plan.md | command | 95 | Missing allowed-tools |
| commands/new-requirement.md | command | 95 | Missing allowed-tools |
| commands/remember.md | command | 95 | Missing allowed-tools |
| commands/review-design.md | command | 95 | Missing allowed-tools |
| commands/review-requirements.md | command | 95 | Missing allowed-tools |
| commands/simplify-implementation.md | command | 95 | Missing allowed-tools |
| commands/update-planning.md | command | 95 | Missing allowed-tools |
| commands/writing-test.md | command | 95 | Missing allowed-tools |
| skills/agent-orchestration/SKILL.md | skill | 100 | None |
| skills/capture-knowledge/SKILL.md | skill | 100 | None |
| skills/debug/SKILL.md | skill | 100 | None |
| skills/dev-lifecycle/SKILL.md | skill | 100 | None |
| skills/memory/SKILL.md | skill | 100 | None |
| skills/simplify-implementation/SKILL.md | skill | 100 | None |
| skills/tdd/SKILL.md | skill | 100 | None |
| skills/technical-writer/SKILL.md | skill | 100 | None |
| skills/verify/SKILL.md | skill | 100 | None |
| .claude-plugin/plugin.json | manifest | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 4 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Shell scripts | skills/dev-lifecycle/scripts/check-status.sh |
| TypeScript scripts | packages/memory/scripts/benchmark.ts |
| Jest configs | e2e/jest.config.js, packages/*/jest.config.js (×4) |
| Package manifests | package.json (root), packages/cli/package.json, packages/memory/package.json, packages/agent-manager/package.json, packages/channel-connector/package.json, web/package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Low | skills/dev-lifecycle/scripts/check-status.sh | 7–22 | unvalidated-path-component | `FEATURE="$1"` is interpolated directly into file paths (`feature-${FEATURE}.md`). No sanitization prevents path traversal (e.g., `../../etc/passwd`). Used with `[[ -f … ]]` and `grep`, so no code execution — risk is accidental access to unintended files. |
| 2 | Low | package.json | 8 | prepare-lifecycle-hook | `"prepare": "husky"` runs automatically on `npm install`, installing git hooks without explicit user consent on first checkout. Standard pattern but installs executable hooks. |
| 3 | Low | package.json | 31–33 | unpinned-dependency-ranges | devDependencies use `^` ranges (`@nx/js ^22.4.0`, `husky ^9.1.7`, `nx ^22.4.0`). npm can silently upgrade to incompatible minor versions. |
| 4 | Low | packages/cli/package.json | 29–43 | unpinned-dependency-ranges | Runtime dependencies use `^` ranges (chalk, commander, fs-extra, yaml, zod, etc.). Supply chain risk if any package is compromised at a minor/patch version. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No NL registration bugs found | — |

No command files have missing `description` frontmatter, no broken cross-references were detected (all skill `references/` files and scripts exist in the repo), and no tools are called outside of declared `allowed-tools` (because no command file declares `allowed-tools` at all — consistently absent, handled as a quality issue below).

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/dev-lifecycle/scripts/check-status.sh | Unvalidated FEATURE path component | Add `[[ "$FEATURE" =~ ^[a-zA-Z0-9_-]+$ ]] \|\| { echo "Invalid feature name"; exit 1; }` after line 8 |
| 2 | package.json | `prepare` hook installs husky silently | Document in README that `npm install` installs git hooks; no code change required, documentation only |
| 3 | package.json | Unpinned devDependency ranges | Pin to exact versions or use `npm shrinkwrap` / lock-file verification in CI |
| 4 | packages/cli/package.json | Unpinned runtime dependency ranges | Pin runtime deps to exact versions; particularly `commander`, `zod`, `yaml` which have public APIs agents depend on |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | All 61 command files (5 groups × 12 + technical-writer-review) | Missing `allowed-tools` declaration in frontmatter | -5 per file |
| 2 | .cursor/commands/technical-writer-review.md | No empty input handling — command begins with review criteria and assumes a document is already in scope; does not ask which document to review when invoked with no argument | -10 |
| 3 | .claude/commands/code-review.md, .codex/commands/code-review.md | Missing "Holistic Codebase Review" step present in commands/code-review.md and .cursor/commands/code-review.md — the richer variant was not back-propagated to .claude and .codex installs | Informational |
| 4 | .claude/commands/new-requirement.md, .codex/commands/new-requirement.md | Step ordering differs from template/cursor/commands variants: these versions put Capture before Memory search, while other variants put Memory search first (reducing redundant questions) | Informational |

## Cross-Component
**Variant drift across tool targets** — The repo ships the same 12 commands in five locations (`.claude/commands/`, `packages/cli/templates/commands/`, `.codex/commands/`, `.cursor/commands/`, and `commands/`). Over time, the variants have diverged:

- `code-review.md`: The `commands/` and `.cursor/commands/` versions include a "Holistic Codebase Review" step (breadth-first grep/glob across the codebase) that the `.claude/commands/` and `.codex/commands/` versions lack. The richer version should be canonical.
- `new-requirement.md`: Step ordering is inconsistent — `.cursor/commands/` and `commands/` versions run Memory search as Step 1 before gathering requirements (better: avoids asking for context the AI already has). `.claude/` and `.codex/` versions gather requirements first.
- `packages/cli/templates/commands/` uses `{{docsDir}}` placeholders correctly; the installed variants use hardcoded `docs/ai/` paths. This is intentional (template vs instantiated) and not a defect.

**Skills ↔ commands cross-reference** — `skills/dev-lifecycle/SKILL.md` references all 9 phase commands via `references/*.md` files inside the skill directory. All references resolve correctly. The `scripts/check-status.sh` referenced on line 51 also exists. No broken links.

**plugin.json version** — `.claude-plugin/plugin.json` declares version `0.24.0`, which matches `package.json` and `packages/cli/package.json`. Version is consistent across manifests. ✓

## Recommendation
CLEAR — submit PRs for quality improvements. No security blockers. Suggested PRs:

1. **Add `allowed-tools` to all command files** — Declare the tools each command actually uses (Read, Bash, Write, etc.). Affects all 61 command files across 5 locations. High impact for discoverability and permission scoping.
2. **Fix `technical-writer-review.md` empty input handling** — Add an opening step: "If no document path is provided, ask: which file(s) or directory should I review?" This brings it in line with the other 12 command patterns.
3. **Propagate the holistic `code-review.md`** — Copy the fuller version (with Holistic Codebase Review step) from `commands/code-review.md` to `.claude/commands/code-review.md` and `.codex/commands/code-review.md`.
4. **Sanitize FEATURE arg in check-status.sh** (security fix #1 above) — One-line guard, low effort.
