# NLPM Audit: mikeyobrien/ralph-orchestrator
**Date**: 2026-04-19  |  **Artifacts**: 19  |  **Strategy**: single
**NL Score**: 91/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 12  |  **Security Findings**: 6

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| crates/ralph-core/tests/fixtures/skills/complex-test-skill/SKILL.md | Skill (fixture) | 75 | Zero examples (−15), no output format (−10) |
| .claude/skills/code-assist/SKILL.md | Skill | 84 | 8 vague quantifiers: appropriate ×3, relevant ×2, necessary ×2, reasonable ×1 (−16) |
| .claude/agents/ralph-e2e-verifier.md | Agent | 86 | 7 vague quantifiers: comprehensive ×3, actionable ×2, relevant ×2 (−14) |
| skills/ralph-loop/SKILL.md | Skill | 86 | Missing output format section (−10); vague: appropriate, right (−4) |
| .claude/skills/pdd/SKILL.md | Skill | 87 | Only 1 example (−5); vague: appropriate, necessary, sufficient, relevant (−8) |
| .claude/skills/evaluate-presets/SKILL.md | Skill | 88 | Implicit/informal output format (−5); no type/version; vague: appropriate (−2) |
| .claude/skills/playwriter/SKILL.md | Skill | 88 | Missing explicit output format section (−10); no type/version; vague: appropriate (−2) |
| .claude/skills/test-driven-development/SKILL.md | Skill | 91 | No dedicated output format section (−5); vague: appropriate, relevant (−4) |
| .claude/skills/code-task-generator/SKILL.md | Skill | 92 | Vague: appropriate ×2, relevant, reasonable (−8) |
| .claude/skills/tmux-terminal/SKILL.md | Skill | 93 | No type/version; no output format section (−5) |
| .claude/skills/tui-debug-in-pane/SKILL.md | Skill | 93 | No type/version; no explicit output format (−5) |
| .claude/agents/code-assist.md | Agent | 94 | Vague: high-quality ×2, relevant, systematic (−6) |
| .claude/agents/ralph-loop-runner.md | Agent | 94 | Vague: comprehensive, appropriate, relevant (−6) |
| .claude/skills/tui-validate/SKILL.md | Skill | 94 | Vague: appropriate ×2, relevant (−6) |
| .claude/skills/release-bump/SKILL.md | Skill | 95 | No type/version; implicit output (−5) |
| .claude/skills/find-code-tasks/SKILL.md | Skill | 96 | Vague: relevant, appropriate (−4) |
| skills/ralph-hats/SKILL.md | Skill | 96 | Vague: non-trivial, current (−4) |
| .claude/skills/pr-demo/SKILL.md | Skill | 98 | Vague: appropriate (−2) |
| .claude/skills/review-pr/SKILL.md | Skill | 100 | None |

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
| Hooks | 0 (none in hooks/) |
| Shell scripts | scripts/ci-rust-gate.sh, scripts/sync-embedded-files.sh, scripts/hooks-bdd-gate.sh, scripts/test-fresh-install.sh, scripts/hooks-mutation-gate.sh, scripts/test_issue_213.sh, scripts/setup-hooks.sh |
| Python scripts | scripts/validate_llms_txt.py, scripts/update_coverage_badge.py |
| MCP configs | 0 |
| Package manifests | package.json (private workspace, no postinstall) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | scripts/sync-embedded-files.sh | 143 | network call | `curl -fsSL "$(pdd_raw_url)"` fetches external markdown content from GitHub; URL is dynamically constructed but pinned to a SHA in a local config file |
| 2 | Medium | scripts/test-fresh-install.sh | 69 | runtime package install | `npm install` resolves and executes packages from the npm registry; standard for Node projects but represents a supply-chain surface |
| 3 | Medium | scripts/ci-rust-gate.sh | 69 | network call | `rustup toolchain install stable` downloads a Rust toolchain from rustup.rs at runtime |
| 4 | Low | scripts/sync-embedded-files.sh | 72 | source local file | `source "$config_path"` executes a shell env file; path is repo-internal and hardcoded, but sourcing any file carries shell-injection potential if file content is modified |
| 5 | Low | scripts/setup-hooks.sh | 19–24 | file writes outside repo tree | Copies files into `.git/hooks/`, which is outside the main working tree; hooks become executable on every commit/push for any developer who runs this script |
| 6 | Low | scripts/hooks-bdd-gate.sh | 232 | env var write | Appends report content to `$GITHUB_STEP_SUMMARY`; safe CI variable but worth noting as an output channel to GitHub's job summary UI |

## Bugs (PR-worthy)
No bugs found. All 19 artifacts have the required `name` and `description` frontmatter fields. All cross-file references resolve:
- `skills/ralph-hats/references/{schema,commands,examples}.md` — verified present
- `skills/ralph-loop/references/{commands,diagnostics}.md` — verified present
- `code-assist` agent ↔ `.claude/skills/code-assist/SKILL.md` — matched by name
- `ralph-loop-runner` agent → `skills/ralph-loop` reference — verified present

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/sync-embedded-files.sh | `curl` fetches external URL at runtime with no checksum verification | Add `sha256sum` verification of the downloaded file against a pinned hash stored in `pdd.env` alongside the SHA ref |
| 2 | scripts/test-fresh-install.sh | `npm install` with no integrity override | Add `npm ci` instead of `npm install` (uses lockfile exactly) and/or add `--ignore-scripts` for the install step |
| 3 | scripts/setup-hooks.sh | Copies hook scripts to `.git/hooks` without validating source integrity | Document explicitly in README that this script must be run intentionally; consider adding a checksum check on the `.hooks/` source files |
| 4 | scripts/sync-embedded-files.sh | `source "$config_path"` executes shell from a config file | Replace with a safer parser (e.g., `grep`/`awk`) that extracts only the three expected variable values without executing arbitrary shell |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | crates/.../complex-test-skill/SKILL.md | Test fixture: zero examples (expected 2+), no output format, 2-line body | −25 total |
| 2 | .claude/skills/code-assist/SKILL.md | Vague quantifiers: appropriate ×3, relevant ×2, necessary ×2, reasonable ×1 | −16 |
| 3 | .claude/agents/ralph-e2e-verifier.md | Vague quantifiers: comprehensive ×3, actionable ×2, relevant ×2 | −14 |
| 4 | skills/ralph-loop/SKILL.md | No output format section; skill describes operations but not what the operator sees as a result | −10 |
| 5 | .claude/skills/pdd/SKILL.md | Single example (PDD mode only; description mode example is minimal); vague: appropriate, necessary, sufficient, relevant | −13 |
| 6 | .claude/skills/playwriter/SKILL.md | No explicit output format section; skill ends with Tips, no reporting structure; no type/version | −12 |
| 7 | .claude/skills/evaluate-presets/SKILL.md | Output format is implicit (eval logs in `.eval/`); no type/version field | −7 |
| 8 | .claude/skills/test-driven-development/SKILL.md | No dedicated output format section (backpressure emit covers completion but not the shape of delivered work); vague: appropriate, relevant | −9 |
| 9 | .claude/skills/tmux-terminal/SKILL.md | Reference-style skill; no output format section; no type/version | −5 |
| 10 | .claude/skills/tui-debug-in-pane/SKILL.md | No explicit output format; procedure ends at "Clean Up" without describing what the operator receives | −5 |
| 11 | .claude/agents/ralph-loop-runner.md | Vague: comprehensive, appropriate, relevant; haiku model appropriate for lightweight runner | −6 |
| 12 | .claude/skills/code-task-generator/SKILL.md | Vague: appropriate ×2, relevant, reasonable | −8 |

## Cross-Component
- **Sync coupling**: `scripts/sync-embedded-files.sh` mirrors `.claude/skills/code-task-generator/SKILL.md` to `crates/ralph-cli/sops/code-task-generator.md` for `include_str!()` packaging. Any edit to the SKILL.md must be followed by a sync run or CI will fail. This is documented but easy to miss in a fast edit.
- **Agent → skill name match**: The `code-assist` agent (`.claude/agents/code-assist.md`) and the skill (`.claude/skills/code-assist/SKILL.md`) share the name `code-assist`. The agent instructs the orchestrator to follow the "code-assist SOP" by loading the skill. This tight coupling is intentional and consistent.
- **ralph-loop-runner agent → ralph-loop skill**: The agent explicitly references `skills/ralph-loop` at runtime. The reference resolves correctly.
- **Test fixture isolation**: `crates/ralph-core/tests/fixtures/skills/complex-test-skill/SKILL.md` is embedded within the Rust test fixtures tree. Its low score is expected for a smoke-test fixture; it should not be treated as a production skill.
- **No orphaned components detected**: Every skill referenced by an agent exists; every agent's model declaration matches its task scope (opus for complex E2E and code implementation, haiku for lightweight loop runner).

## Recommendation

CLEAR — submit PRs for all Medium/Low security fixes. No critical or high security findings were detected and no registration-blocking bugs exist. The NL score of 91/100 is well above the default 70-point threshold.

**Highest-value PR targets:**
1. `scripts/sync-embedded-files.sh` — replace `source` with a variable parser, add checksum on `curl` output (addresses findings #1 and #4)
2. `.claude/skills/code-assist/SKILL.md` — reduce vague quantifiers (biggest quality penalty at −16)
3. `.claude/agents/ralph-e2e-verifier.md` — replace "comprehensive/actionable" with specific measurable terms (−14)
4. `skills/ralph-loop/SKILL.md` — add an "Output" section describing the operator-visible result of common loop operations
5. `scripts/test-fresh-install.sh` — switch `npm install` to `npm ci` for deterministic installs
