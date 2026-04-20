# NLPM Audit: caliber-ai-org/ai-setup
**Date**: 2026-04-20  |  **Artifacts**: 25  |  **Strategy**: batched
**NL Score**: 100/100
**Security**: CLEAR
**Bugs**: 4  |  **Quality Issues**: 4  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/skills/scoring-checks/SKILL.md | skill | 98 | Vague: "appropriate category section" |
| .claude/skills/save-learning/SKILL.md | skill | 98 | Vague: "appropriate type prefix" |
| .agents/skills/save-learning/SKILL.md | skill | 98 | Vague: "appropriate type prefix" |
| .cursor/skills/save-learning/SKILL.md | skill | 98 | Vague: "appropriate type prefix" |
| .claude/skills/llm-provider/SKILL.md | skill | 100 | None |
| .claude/skills/caliber-testing/SKILL.md | skill | 100 | None |
| .claude/skills/adding-a-command/SKILL.md | skill | 100 | None |
| .claude/skills/writers-pattern/SKILL.md | skill | 100 | None |
| .claude/skills/setup-caliber/SKILL.md | skill | 100 | None |
| .claude/skills/find-skills/SKILL.md | skill | 100 | None |
| .agents/skills/llm-provider/SKILL.md | skill | 100 | None |
| .agents/skills/scoring-checks/SKILL.md | skill | 100 | None |
| .agents/skills/caliber-testing/SKILL.md | skill | 100 | None |
| .agents/skills/adding-a-command/SKILL.md | skill | 100 | None |
| .agents/skills/writers-pattern/SKILL.md | skill | 100 | None |
| .agents/skills/setup-caliber/SKILL.md | skill | 100 | None |
| .agents/skills/find-skills/SKILL.md | skill | 100 | None |
| .cursor/skills/llm-provider/SKILL.md | skill | 100 | None |
| .cursor/skills/scoring-checks/SKILL.md | skill | 100 | None |
| .cursor/skills/caliber-testing/SKILL.md | skill | 100 | None |
| .cursor/skills/adding-a-command/SKILL.md | skill | 100 | None |
| .cursor/skills/writers-pattern/SKILL.md | skill | 100 | None |
| .cursor/skills/setup-caliber/SKILL.md | skill | 100 | None |
| .cursor/skills/find-skills/SKILL.md | skill | 100 | None |
| CLAUDE.md | context | 100 | None |

**Weighted average**: (21 × 100 + 4 × 98) / 25 = **99.68 → 100/100**

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | None |
| Scripts | scripts/postinstall.js, scripts/demo-init.sh, scripts/demo-output.sh, scripts/demo-shell.sh |
| MCP configs | None |
| Package manifests | package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | package.json | 20 | postinstall-adjacent lifecycle script | `"prepare": "husky"` runs on every `npm install`, modifying `.git/hooks/`. Standard pattern but writes files outside the repo working tree on user machines. |
| 2 | Medium | package.json | 36 | analytics/telemetry dependency | `posthog-node` is listed as a production dependency. This library sends CLI usage events to PostHog servers. Users running `caliber` commands may not be aware their usage is tracked externally. |
| 3 | Low | package.json | 23–38 | unpinned dependency versions | 22 production and dev dependencies use `^` ranges (e.g. `"@anthropic-ai/sdk": "^0.78.0"`). Minor/patch updates pick up automatically, which could introduce breaking changes or supply-chain drift. |
| 4 | Low | scripts/postinstall.js | 1–16 | unused executable artifact | File exists with executable content (console output with ANSI color) but is not wired into `package.json` `scripts` object — no `"postinstall"` key. It is dead code that could be confused for an active hook. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `*/skills/llm-provider/SKILL.md` | Contradictory `LLMProvider` interface signatures across platforms: `.claude/` defines `call(options: LLMCallOptions): Promise<string>` with `stream(options, callbacks): Promise<void>`; `.agents/` defines `stream()` as `AsyncGenerator<string>`; `.cursor/` defines `stream()` as `AsyncIterable<StreamChunk>`. Only one of these can reflect the actual `src/llm/types.ts` interface. | Agents following different platform skills will generate incompatible provider implementations that fail TypeScript type checking at build time. |
| 2 | `*/skills/scoring-checks/SKILL.md` | Contradictory check function signatures across platforms: `.claude/` uses `checkCategory(dir: string): Check[]` (dir-based, named export); `.agents/` uses a default export with `(ctx: ScoringContext): Check[]` (context-based); `.cursor/` uses `(fingerprint, config): Check[]` (two-param named export). | Three different patterns means agents cannot reliably produce interoperable scoring checks; two of the three signatures will produce code that fails to register in `src/scoring/index.ts`. |
| 3 | `*/skills/adding-a-command/SKILL.md` | `.cursor/` version specifies `export default async (options, ctx: CLIContext)` (default export), while `.claude/` and `.agents/` specify named exports (`export async function myCommand(...)`). CLI command files in this project cannot be simultaneously default and named exports. | Agents following the Cursor skill will generate command files that fail to register correctly in `src/cli.ts`, which expects named imports. |
| 4 | `*/skills/writers-pattern/SKILL.md` | Three incompatible writer signatures: `.claude/` specifies synchronous `write<Platform>Config(config): string[]`; `.agents/` specifies async `(config: WriterConfig, skillLines: SkillLine[]): Promise<string[]>` (default export, two params); `.cursor/` specifies async `writeSetup(setup: WriteSetup): Promise<string[]>`. | `src/writers/index.ts` can only call one of these signatures. The other two will produce writers that fail at runtime when orchestrated by `writeSetup()`. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | package.json | `posthog-node` telemetry without visible disclosure | Add a note in README and `caliber init` output disclosing that anonymous usage analytics are collected; provide an opt-out env var (e.g. `CALIBER_NO_TELEMETRY=1`). |
| 2 | package.json | Unpinned dependencies | Pin exact versions for production dependencies in `package-lock.json` and consider locking `@anthropic-ai/sdk`, `openai`, and `posthog-node` to exact versions in `package.json` to reduce supply-chain risk. |
| 3 | scripts/postinstall.js | Unused executable artifact | Either wire it into `package.json` as `"postinstall": "node scripts/postinstall.js"` if intentional, or remove the file to avoid confusion and reduce attack surface. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/skills/scoring-checks/SKILL.md | Vague quantifier: "Add constants below the **appropriate** category section" — "appropriate" is unspecified; reader must infer which category applies. | -2 |
| 2 | .claude/skills/save-learning/SKILL.md | Vague quantifier: "Refine the instruction into a clean, actionable learning bullet with an **appropriate** type prefix" — no decision rule for choosing among convention/pattern/anti-pattern/preference/context. | -2 |
| 3 | .agents/skills/save-learning/SKILL.md | Same vague quantifier as .claude/ version: "appropriate type prefix". | -2 |
| 4 | .cursor/skills/save-learning/SKILL.md | Same vague quantifier as .claude/ version: "appropriate type prefix". | -2 |

## Cross-Component
**Systematic skill divergence — four skill types document contradictory implementations of the same codebase APIs:**

The same eight skill files are deployed across three platforms (`.claude/`, `.agents/`, `.cursor/`). For four of the eight skills (`llm-provider`, `scoring-checks`, `adding-a-command`, `writers-pattern`), the three platform copies diverge significantly in the TypeScript interfaces, function signatures, and integration patterns they describe. These are not cosmetic differences — they contradict each other on:

- **Method signatures** (`call()`, `stream()`, `writeSetup()`, check functions)
- **Export style** (named vs. default)
- **Sync/async** (`string[]` vs `Promise<string[]>`)
- **Parameter types** (`dir: string` vs `ScoringContext` vs `(fingerprint, config)`)

The four "stable" skills (`save-learning`, `find-skills`, `setup-caliber`, `caliber-testing`) are consistent across platforms and well-authored.

**Root cause**: The platform-specific skills appear to have been independently authored or updated at different times, rather than being generated from a single source of truth and distributed. The `.claude/` versions are the most detailed and match the CLAUDE.md architecture description most closely (7-step guides with full code blocks). The `.agents/` versions are condensed summaries. The `.cursor/` versions appear to describe a different internal API shape entirely.

**Recommendation**: Elect one platform version as authoritative for each skill (most likely `.claude/`), verify it against `src/llm/types.ts`, `src/scoring/index.ts`, `src/cli.ts`, and `src/writers/index.ts`, then regenerate the `.agents/` and `.cursor/` copies from the same source.

**Orphaned artifact**: `scripts/postinstall.js` is not referenced in `package.json` scripts. It may be a leftover from a previous release setup.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes.

The NL artifacts are individually high quality (100/100 weighted average). All four bugs stem from the same root cause: cross-platform skill divergence rather than individual file defects. The security profile is clean with no Critical or High findings.

**Priority order for PRs:**
1. Fix `llm-provider` skill signatures across platforms (highest developer impact — wrong signatures break builds)
2. Fix `writers-pattern` skill signatures (sync/async mismatch causes runtime failures)
3. Fix `adding-a-command` export style (named vs. default export breaks CLI registration)
4. Fix `scoring-checks` function signatures (prevents correct check registration)
5. Add telemetry disclosure and opt-out mechanism (trust/transparency)
6. Pin critical production dependency versions (supply chain hygiene)
