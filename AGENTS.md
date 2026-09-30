# Project Instructions

> nlpm

# nlpm

Natural-Language Programming Manager — multi-tool (Claude Code, Codex CLI, Antigravity) NL artifact scoring, checking, fixing, and testing. Delivered as a Claude Code plugin; the scoring rubric covers all three ecosystems via tier-aware overlays (see `analysis/multi-tool-design-2026-05.md`).

## Architecture

Commands orchestrate agents. Agents use skills as reference knowledge.
Each command does one thing -- no flags (except `--changed` on score).
Per-file roles, models and skill bindings: see `docs/architecture.md`.

- `commands/*.md` -- `/nlpm:` ls, score, check, fix, trend, test, init, security-scan, vocab-init, vocab-drift, report, spec-sync. `commands/shared/` (discover, classify, append-history) holds partials that are not user-invocable.
- `agents/*.md` -- scanner and vague-scanner (haiku, mechanical); scorer, checker, tester, security-scanner, vocab-drift-scanner, spec-researcher (sonnet). spec-researcher is read-only and never edits.
- `skills/nlpm/` -- auto-loaded via agent `skills:` frontmatter: conventions, conventions-claude, conventions-codex, conventions-antigravity, scoring, testing, security. Loaded on demand: rules (R01-R50, single source of truth), patterns, vocabulary (R51 registry, opt-in), and the writing-* and orchestration guides.
- `hooks/hooks.json` -- PostToolUse on Write|Edit|MultiEdit runs `scripts/check-artifact.sh`, which emits an advisory only for NL artifacts.
- `bin/nlpm-check` -- stdlib-only Python validator, the subset of `/nlpm:check` that runs without Claude Code (pre-commit, CI, pre-publish); templates in `templates/`, author guide in `docs/for-authors.md`.

When you add, rename or remove a command, agent or skill, update this list and `docs/architecture.md` in the same change, then run `/nlpm:check`.

## Self-Tests

- .nlpm-test/ -- NL-TDD spec files for 5 of the 8 agents (scanner, scorer, checker, vague-scanner, tester; dogfooding NL-TDD)
- tests/ -- Python unittest suite for bin/nlpm-check, bin/nlpm-badge and the auditor scripts

## Build & Run

No build step. Markdown plugin + single-file Python binary. Install with:
```
claude plugin install nlpm@xiaolai --scope project
```

Test by running `/nlpm:ls` on any project with NL artifacts.
Run `/nlpm:test` to verify agent specs pass.
Run `python3 -m unittest tests.test_nlpm_check` to verify the binary.
Run `python3 -m unittest discover tests` to run the full Python suite.
Run `python3 bin/nlpm-check . --strict` and `claude plugin validate --strict .claude-plugin/plugin.json` before a release.

## Prerequisites

- Slash commands (/nlpm:*) -- none. Pure markdown.
- Standalone bin/nlpm-check -- Python 3.11+ (stdlib only; no pip install).
- Auditor workflows -- CLAUDE_CODE_OAUTH_TOKEN, PAT_TOKEN, OPENAI_API_KEY secrets.

## Development

When modifying this plugin:
- Run `/nlpm:score ./` after changes; every changed NL artifact must score at least 95 (the pre-release gate's floor)
- Run `/nlpm:check` to verify cross-artifact references
- Run `/nlpm:test` to verify agent specs pass
- Bump version in plugin.json AND marketplace.json
- Push plugin repo, then update central marketplace

## Scoring

100-point scale. Start at 100, apply deterministic penalties.
Floor: 0. Ceiling: 100.
Threshold configurable via .claude/nlpm.local.md (default: 70).
Rule overrides supported (suppress, enabled, max_penalty, threshold, min_examples adjustments; see `nlpm:conventions` §6).

## Auditor rules

The `auditor/` pipeline (`.github/workflows/auditor-*.yml`) discovers, audits, and contributes to NL plugin/skill repos on GitHub, then feeds the outcomes back into NLPM's rules. Workflow and data inventories, the loop, gate evidence, script catalogue and the `bin/nlpm-build-docs` reference builder: see `docs/auditor.md`. Record contracts: `auditor/SCHEMAS.md`.

- Commit from every auditor workflow through `auditor/scripts/commit-via-pr.sh` (one auto-merging `auditor-bot` PR per commit). Never push to main directly.
- Write `auditor/registry/repos.json` only through `auditor/scripts/atomic-registry-write.sh`.
- Treat `auditor/findings.jsonl`, `auditor/disagreements.jsonl`, `auditor/logs/events.jsonl` and `auditor/vocab-advisories.jsonl` as append-only.
- Mutate NLPM's own rulebook only through `auditor-refine-rules`, and only by opening a PR for human review — never by merging.
- Keep the security scan ahead of the NL audit. If it finds a Critical pattern, label the issue `security-blocked` and skip contribution; `auditor-contribute` must refuse to run while that label is present, and only a manual review clears it.
- Contribute PRs for verified bugs only: at most 3 on first contact with a repo, 5 thereafter. Stamp each PR body with the `nlpm-metadata` block. Never open an umbrella or summary issue on the target.
- Drop any finding whose file an open PR on the target already modifies (the duplicate-detection gate).
- Keep the three contribute policy gates (no-external-PRs, CLA-required, pushback-gated); they skip PR creation and preserve the audit data. Clear pushback-gated with a `gate_override` event only when the maintainer has explicitly invited a follow-up. CLA recovery steps: `docs/auditor.md` § Policy Gates.
- Keep `auditor-vocab-drift` advisory only: it never opens PRs and never gates contribute.
- Keep the pre-release quality gate at 95/100 for every changed NL artifact plus zero enforced vocabulary drift; `bin/nlpm-check` is the exact floor.
- When Anthropic retires the model pinned in `auditor-classify` (`claude-haiku-4-5-20251001`), update the ID and note the migration in the commit message. Leave every other workflow on the claude-code-action default.

## nlpm.com site

The VitePress site lives in `site/` and publishes to the `gh-pages` branch at <https://nlpm.com>. Page map, passthrough outputs and PR-preview workflows: see `docs/site.md`.

- Rebuild locally with `bash site/build.sh` (output: `site/.vitepress/dist/`, gitignored).
- Edit the canonical `skills/nlpm/*/SKILL.md` sources, not `site/reference/*.md`; `bin/nlpm-build-reference-md` generates those pages.
- Keep the legacy single-page `docs/index.html` on the site; reports cross-link into it (`/docs/index.html#R06`).
- Do not copy into `gh-pages` by hand: `.github/workflows/deploy-site.yml` deploys on pushes to `main` that touch site sources or their generators, daily at `0 23 * * *` UTC, and on `workflow_dispatch`. Force an off-cycle deploy with `gh workflow run deploy-site.yml`.
- Commit `site/pnpm-lock.yaml`; keep `node_modules/`, `.vitepress/cache/`, `.vitepress/dist/` and `public/` untracked.

## Shared Memory

**Always write new instructions, rules, and memory to `AGENTS.md` only.**
Put reference material (inventories, narrative, evidence) in `docs/` and link it from here; keep this file under 200 lines.

Never modify `GEMINI.md` directly — it only imports `AGENTS.md`. There is no `CLAUDE.md`: Claude Code 2.1.277+ reads `AGENTS.md` natively, and a `CLAUDE.md` at the plugin root would only draw a plugin-validator warning.
This keeps Claude Code, Codex CLI, and Gemini CLI on the same context.

## Project Structure

- `commands/`, `agents/`, `skills/nlpm/`, `hooks/` — the plugin artifacts, at repo root (auto-discovered by Claude Code)
- `docs/` — `for-authors.md` (author guide); `architecture.md`, `auditor.md` and `site.md` (maintainer reference moved out of this file)
- `.claude/` — gitignored except `.claude/nlpm.local.md` (project NLPM config)
- `.codex/prompts/` — Codex slash-command prompts
- `.codex/hooks.json` / `.codex/config.toml` — Codex hooks/config (optional)
- `.gemini/skills/`, `.gemini/commands/` — Gemini skills and TOML commands
- `.mcp.json` — dev-only MCP registration (cc-suite Codex delegation); gitignored, never shipped. Claude Code auto-registers a plugin-root `.mcp.json`, so it must stay untracked in this plugin repo.
