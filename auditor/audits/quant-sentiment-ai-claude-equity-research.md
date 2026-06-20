# NLPM Audit: quant-sentiment-ai/claude-equity-research
**Date**: 2026-04-06  |  **Artifacts**: 3  |  **Strategy**: single
**NL Score**: 92/100
**Security**: CLEAR
**Bugs**: 2  |  **Quality Issues**: 3  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/trading-ideas/.claude-plugin/plugin.json | plugin | 90 | Missing CLAUDE.md in plugin root (R49, −10) |
| commands/trading-ideas/commands/research.md | command | 90 | No empty input handling (R15, −10) |
| commands/README.md | doc | 95 | Relative link `../docs/` breaks on individual-file install |

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
| Hooks | 0 |
| Scripts | 0 |
| MCP configs | 0 |
| Package manifests | 0 |

No hooks, shell scripts, MCP configs, or package.json/requirements.txt were found. The README's installation instructions use `curl -o` (save-to-file), not `curl | sh` — no pipe-to-shell risk.

### Security Findings
No security findings.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/trading-ideas/.claude-plugin/plugin.json | No CLAUDE.md exists at the plugin root (`commands/trading-ideas/`). R49 requires a CLAUDE.md for Claude Code to surface plugin context. | Plugin operates without integration context; −10 scoring penalty applied. |
| 2 | commands/README.md | Command naming mismatch: README Usage section shows `/trading-ideas AAPL` (direct-file install name) while plugin.json description explicitly says "via /trading-ideas:research command" (plugin install name). Neither install path is explained as producing a different command name. | Users installing via `claude plugin install` will invoke the wrong name, silently failing. |

## Security Fixes (PR-worthy, Medium/Low only)
No security findings to fix.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/trading-ideas/commands/research.md | R15: No empty input handling. Command opens with "When given a stock ticker" but provides no fallback when `$ARGUMENTS` is empty — undefined behavior on bare invocation. | −10 |
| 2 | commands/trading-ideas/commands/research.md | `argument-hint` declares `[--detailed]` but the command body has no conditional branch for this flag. The flag appears in README usage examples (`/trading-ideas HOOD --detailed`) with no observable effect. | — |
| 3 | commands/trading-ideas/.claude-plugin/plugin.json | No `commands` array declared. Claude Code's directory-based auto-discovery may suffice, but explicit declaration makes the manifest self-documenting and guards against discovery regressions. (Low confidence — runtime behavior unverified.) | — |

## Cross-Component
**Command name mismatch (Bugs #2):** `commands/README.md` line 26 shows `/trading-ideas AAPL`; `plugin.json` description says "via /trading-ideas:research command". The direct-file install (`curl -o ~/.claude/commands/trading-ideas.md`) produces `/trading-ideas`, while the plugin install produces `/trading-ideas:research`. Both are valid but undifferentiated in the README, leaving plugin users with a broken invocation path.

**Undocumented `--detailed` flag:** The flag appears in `commands/README.md` line 29 and in `research.md` `argument-hint` but is implemented nowhere in the command body. The README implies enhanced output (`# Enhanced Robinhood analysis`), creating a false expectation.

**No other orphaned components, broken `@` imports, or stale file references detected.** `plugin.json` and `marketplace.json` version fields agree (1.0.1). All `allowed-tools` declared in `research.md` (`WebSearch`, `WebFetch`) are actively invoked in the command body.

## Recommendation
CLEAR — submit PRs for all bugs and quality fixes.

Priority order:
1. **Bug #1** (CLAUDE.md): create `commands/trading-ideas/CLAUDE.md` with plugin overview, command usage (`/trading-ideas:research TICKER`), and customization guidance.
2. **Bug #2** (command name): update README Usage section to explain both install paths and the resulting command names.
3. **Quality #1** (R15): add an opening guard — if no arguments provided, ask the user for a ticker before proceeding.
4. **Quality #2** (`--detailed`): either implement enhanced output when the flag is passed or remove it from `argument-hint` and README examples.
