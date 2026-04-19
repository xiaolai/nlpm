# NLPM Audit: FlorianBruniaux/claude-code-ultimate-guide

**Audited**: 2026-04-19  
**Repo**: https://github.com/FlorianBruniaux/claude-code-ultimate-guide  
**Auditor**: nlpm-auditor v1.0 (claude-sonnet-4-6)

---

## Summary

| Metric | Value |
|--------|-------|
| **NL Score** | 80/100 |
| **Security** | BLOCKED |
| **Bugs** | 12 |
| **Quality Issues** | 19 |
| **Security Findings** | 10 |
| **Artifacts Scanned** | 100 (24 agents · 66 commands · 10 skills) |

> **BLOCKED**: Security gate triggered. One CRITICAL curl-pipe-to-shell pattern found in a command body. Contribution workflow will not proceed until manually reviewed and cleared.

---

## NL Score Breakdown

| Category | Files | Avg Score | Notes |
|----------|-------|-----------|-------|
| Agents | 24 | 77.5/100 | 3 files are READMEs misclassified as agents (-45 pts dragging avg) |
| Commands | 66 | 79.4/100 | 9 BUG-level missing `name:` fields; 2 security-penalized files |
| Skills | 10 | 88.8/100 | 5 skills missing `allowed-tools` |
| **Overall** | **100** | **80/100** | Weighted average across all artifacts |

---

## Bugs (12)

Bugs are issues that break registration or cause runtime failures.

| # | File | Issue | Severity |
|---|------|-------|----------|
| 1 | `examples/agents/cyber-defense/log-ingestor.md` | `Write` tool missing from `allowed-tools` but body says "Write the JSON file" | BUG |
| 2 | `examples/agents/cyber-defense/anomaly-detector.md` | `Write` tool missing from `allowed-tools` but body says "Write detected anomalies to JSON" | BUG |
| 3 | `examples/agents/cyber-defense/risk-classifier.md` | `Write` tool missing from `allowed-tools` but body says "Write classification to JSON" | BUG |
| 4 | `.claude/commands/ccguide/diff-docs.md` | Missing `name:` field in frontmatter — command will not register | BUG |
| 5 | `.claude/commands/ccguide/init-docs.md` | Missing `name:` field in frontmatter | BUG |
| 6 | `.claude/commands/ccguide/refresh-docs.md` | Missing `name:` field in frontmatter | BUG |
| 7 | `.claude/commands/ccguide/search-docs.md` | Missing `name:` field in frontmatter | BUG |
| 8 | `.claude/commands/ccguide/daily.md` | Missing `name:` field in frontmatter | BUG |
| 9 | `examples/commands/recipe-template.md` | Missing `name:` field in frontmatter | BUG |
| 10 | `examples/commands/handoff/resume-handoff.md` | Missing `name:` field in frontmatter | BUG |
| 11 | `examples/commands/handoff/create-handoff.md` | Missing `name:` field in frontmatter | BUG |
| 12 | `examples/commands/handoff/update-handoff.md` | Missing `name:` field in frontmatter | BUG |

---

## Quality Issues (19)

Quality issues reduce score but do not break execution.

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `examples/agents/analytics-with-eval/README.md` | Uses `title:` instead of `name:`, no `model:` or `tools:` — not an agent definition | -55 pts |
| 2 | `examples/agents/analytics-with-eval/eval/report-template.md` | Uses `title:` instead of `name:`, no `model:` or `tools:` — evaluation report template, not agent | -55 pts |
| 3 | `examples/agents/cyber-defense/README.md` | No frontmatter at all — LangGraph comparison article misclassified as agent | -70 pts |
| 4 | `examples/agents/devops-sre.md` | Zero example blocks | -15 pts |
| 5 | `examples/agents/architecture-reviewer.md` | Zero example blocks | -15 pts |
| 6 | `examples/agents/security-auditor.md` | Zero example blocks | -15 pts |
| 7 | `examples/agents/planner.md` | Zero example blocks | -15 pts |
| 8 | `examples/agents/planning-coordinator.md` | Zero example blocks | -15 pts |
| 9 | `examples/agents/implementer.md` | Zero example blocks | -15 pts |
| 10 | `examples/skills/release-notes-generator/SKILL.md` | Missing `allowed-tools` (skill uses `git`, `gh` CLI, writes files) | -5 pts |
| 11 | `examples/skills/landing-page-generator/SKILL.md` | Missing `allowed-tools` (skill generates and writes full landing pages) | -5 pts |
| 12 | `examples/skills/guide-recap/SKILL.md` | Missing `allowed-tools` (skill reads CHANGELOG, may write social posts) | -5 pts |
| 13 | `examples/skills/cyber-defense-team/SKILL.md` | Missing `allowed-tools` (orchestrator needs Agent tool declared) | -5 pts |
| 14 | `examples/skills/ccboard/SKILL.md` | Missing `allowed-tools` (reference skill — Bash minimum needed) | -5 pts |
| 15 | `examples/skills/git-ai-archaeology/SKILL.md` | Missing `effort` field; description lacks "use when" trigger phrasing | -4 pts |
| 16 | `examples/skills/ccboard/commands/*.md` (6 files) | All 6 ccboard commands: no `allowed-tools`, no process workflow, thin bash shim only | -30 pts total |
| 17 | `.claude/commands/update-infos-release.md` | Hardcoded absolute path `/Users/florianbruniaux/` — not portable across machines | MEDIUM |
| 18 | `examples/agents/cyber-defense/anomaly-detector.md` | Declares `Read` only but text mentions reading and writing — intent/tools mismatch beyond BUG #2 | -5 pts |
| 19 | `examples/commands/review-plan.md` | Uses `AskUserQuestion` tool but no `allowed-tools` field declared | -5 pts |

---

## Security Findings (10)

### CRITICAL (1) — Security Gate: BLOCKED

| # | File | Pattern | Line | Detail |
|---|------|---------|------|--------|
| C1 | `examples/commands/diagnose.md` | curl-pipe-to-shell | 38-39 | `curl -sL "https://raw.githubusercontent.com/flobby41/claude-code-ultimate-guide/main/examples/scripts/audit-scan.sh" \| bash -s -- --json 2>/dev/null` — Fetches and executes a remote script from a **different GitHub account** (`flobby41`, not `FlorianBruniaux`). Supply chain risk: the `flobby41` account is not the repo author. |

### HIGH (2)

| # | File | Pattern | Line | Detail |
|---|------|---------|------|--------|
| H1 | `examples/commands/sonarqube.md` | write-execute-tmp | 57-64 | Creates `/tmp/fetch_sonar.sh`, `chmod +x`, then executes it. Write+execute pattern in /tmp. |
| H2 | `scripts/install-templates.sh` | curl-pipe-bash invocation | 3 | Script is designed to be invoked as `curl -fsSL {URL} \| bash -s --`. The script itself then fetches remote files from `raw.githubusercontent.com` and writes them into the user's `.claude/` directory (agents, hooks, commands). Remote artifact injection into Claude config. |

### MEDIUM (4)

| # | File | Pattern | Detail |
|---|------|---------|--------|
| M1 | `scripts/update-cc-releases.sh` | network-fetch-to-tmp | Lines 42, 107-112: `curl` downloads from `raw.githubusercontent.com` and `code.claude.com` to `/tmp/` files. URLs are known official sources but network calls to external hosts in a script that modifies repo data. |
| M2 | `scripts/check-landing-sync.sh` | external-network-call | Line 163: `curl -s https://api.github.com/repos/FlorianBruniaux/...` to fetch star count. Low impact but unexpected network call in a sync check script. |
| M3 | `.claude/commands/update-infos-release.md` | hardcoded-paths | References absolute path `/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing/` — portability issue and path disclosure. |
| M4 | `examples/commands/diagnose.md` | username-mismatch | Script fetched from `flobby41` account but repo is `FlorianBruniaux`. Possible stale reference to a fork or a different actor's account. Warrants manual verification of account ownership. |

### LOW (3)

| # | File | Pattern | Detail |
|---|------|---------|--------|
| L1 | `examples/hooks/bash/rtk-baseline.sh`, `velocity-governor.sh`, `session-summary.sh` | tmp-state-files | Write state JSON to `/tmp/` (e.g., `/tmp/claude-velocity-{PROJECT_SLUG}.json`). Standard pattern for hooks, low risk. |
| L2 | `examples/skills/ccboard/commands/install.md` | curl-pipe-sh-docs | Documents `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh` as a Rust installation instruction. Documentation only, not a command body Claude executes. |
| L3 | `scripts/translate-guide.py` | api-key-from-env | Uses `anthropic.Anthropic()` which reads `ANTHROPIC_API_KEY` from environment. Standard API usage, acceptable in a documentation/tooling script. |

---

## Highest-Value Files

The following files are exemplary and suitable for reference or inclusion:

| File | Score | Why |
|------|-------|-----|
| `examples/commands/pr.md` | 93/100 | Complexity scoring, scope coherence, split suggestions, concrete bash commands, edge cases |
| `.claude/agents/guide-reviewer.md` | 93/100 | Complete frontmatter, haiku model, example block, clean output format |
| `examples/agents/code-reviewer.md` | 92/100 | Anti-hallucination protocol, pattern examples, defensive audit sections |
| `examples/agents/adr-writer.md` | 92/100 | 3-tier ADR format, when-to-use, model rationale, read-only correctly |
| `examples/commands/plan-execute.md` | 92/100 | 8 numbered phases, drift detection, quality gate, full output example |
| `examples/commands/explain.md` | 92/100 | 3 depth levels with concrete examples, argument-hint, multiple usage forms |
| `examples/skills/design-patterns/SKILL.md` | 95/100 | 5 phases, 3 modes, full JSON/Markdown output examples, allowed-tools scoped |
| `examples/skills/audit-agents-skills/SKILL.md` | 95/100 | Industry data citations, 3 audit modes, JSON+Markdown dual output, CI/CD integration |

---

## Recommended Fixes (Priority Order)

1. **[SECURITY CRITICAL]** Remove or replace the `curl | bash` invocation in `examples/commands/diagnose.md` line 38-39. The script fetches from `flobby41` — a different GitHub account. Replace with a local script path or verify account ownership and pin to a commit hash with checksum validation.

2. **[SECURITY HIGH]** Refactor `examples/commands/sonarqube.md` to avoid writing and executing a temp script in `/tmp/`. Use a heredoc or inline the commands directly.

3. **[BUGS - 9 commands]** Add `name:` field to frontmatter in: `ccguide/diff-docs.md`, `ccguide/init-docs.md`, `ccguide/refresh-docs.md`, `ccguide/search-docs.md`, `ccguide/daily.md`, `recipe-template.md`, `handoff/resume-handoff.md`, `handoff/create-handoff.md`, `handoff/update-handoff.md`.

4. **[BUGS - 3 agents]** Add `Write` to `allowed-tools` in: `cyber-defense/log-ingestor.md`, `cyber-defense/anomaly-detector.md`, `cyber-defense/risk-classifier.md`.

5. **[QUALITY - 5 skills]** Add `allowed-tools` to: `release-notes-generator/SKILL.md`, `landing-page-generator/SKILL.md`, `guide-recap/SKILL.md`, `cyber-defense-team/SKILL.md`, `ccboard/SKILL.md`.

6. **[QUALITY - 6 agents]** Add at least one example block to: `devops-sre.md`, `architecture-reviewer.md`, `security-auditor.md`, `planner.md`, `planning-coordinator.md`, `implementer.md`.

7. **[QUALITY - 3 misclassified]** Move `analytics-with-eval/README.md`, `analytics-with-eval/eval/report-template.md`, and `cyber-defense/README.md` out of agent directories or add proper agent frontmatter. Currently dragging the agent average down by ~5 points.

---

## Contribution Decision

**Status: BLOCKED**

Security gate triggered by C1 (curl-pipe-to-shell from a different GitHub account in `examples/commands/diagnose.md`). The `flobby41` account reference is the most concerning signal — it may indicate a stale fork reference, a username change, or an unintended third-party dependency.

Manual review required:
- Verify whether `flobby41` is the same person as `FlorianBruniaux`
- If yes: consolidate to canonical username and remove curl-pipe-bash
- If no: remove the reference entirely

Clear the `security-blocked` label only after the diagnose.md CRITICAL finding is resolved.
