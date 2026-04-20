# Audit: alinaqi/claude-bootstrap

**Audited:** 2026-04-20  
**Repo:** https://github.com/alinaqi/claude-bootstrap  
**Auditor:** nlpm-auditor (sonnet)

---

## NL Score: 80/100

## Security: BLOCKED

---

## Summary

claude-bootstrap is a comprehensive Claude Code project template and agent team framework. It ships skills, agents, commands, scripts, hooks, and two embedded Python tools (iCPG, Mnemos). The NL artifact quality is **good for skills, poor for commands**: all 15 commands lack frontmatter entirely, pulling the overall score below what the strong skill library would otherwise earn. Two CRITICAL security findings in the installation scripts trigger the BLOCKED status, preventing contribution without manual remediation.

---

## Score Breakdown

| Type | Count | Avg Score | Total Points |
|------|-------|-----------|--------------|
| Agents | 6 | 85 | 510 |
| Commands | 15 | 40 | 606 |
| Skills | 61 | 89 | 5,429 |
| **Total** | **82** | **80** | **6,545** |

**Weighted NL Score: 80/100** (threshold: 70 — PASS)

---

## Agent Scores (`skills/agent-teams/agents/`)

All 6 agents have complete frontmatter (name, description, model, tools/disallowedTools, maxTurns, effort) but **zero example blocks** (-15 each).

| Agent | Model | Examples | Score |
|-------|-------|----------|-------|
| merger-agent | sonnet | 0 | 85 |
| team-lead | sonnet | 0 | 85 |
| review-agent | sonnet | 0 | 85 |
| feature-agent | inherit | 0 | 85 |
| security-agent | sonnet | 0 | 85 |
| quality-agent | sonnet | 0 | 85 |

**Top issue:** Zero example blocks across all agents. Adding one example per agent (+10 each) would raise agent average from 85 → 95.

---

## Command Scores (`commands/`)

**All 15 commands are missing frontmatter entirely.** This is the repo's most severe NL quality gap.

Base penalty for missing frontmatter: `-25` (name) + `-25` (description) + `-5` (no allowed-tools) = **-55 per command**.

| Command | Extra Penalties | Score |
|---------|----------------|-------|
| spawn-team.md | — | 45 |
| sync-contracts.md | — | 45 |
| icpg-drift.md | — | 45 |
| icpg-bootstrap.md | — | 45 |
| icpg-impact.md | — | 45 |
| icpg-why.md | — | 45 |
| maggy.md | — | 45 |
| maggy-init.md | — | 45 |
| update-code-index.md | — | 45 |
| analyze-workspace.md | — | 45 |
| analyze-repo.md | — | 45 |
| check-contributors.md | — | 45 |
| initialize-project.md | vague: "appropriate command" ×2 (-4) | 41 |
| mnemos-checkpoint.md | no empty-input handling (-10) | 35 |
| mnemos-status.md | no empty-input handling (-10) | 35 |

**Fix:** Adding frontmatter blocks to all 15 commands would raise command average from 40 → 87.

---

## Skill Scores (`skills/*/SKILL.md`)

61 skill files were scanned. All have proper frontmatter (`name`, `description`, `when-to-use`, `effort`). Quality is consistently high.

**Representative high scorers (93/100):**
- `playwright-testing` — comprehensive, rich code examples, dead-link detection requirement
- `code-review` — allowed-tools declared, user-invocable, thorough checklist
- `ui-web` — extensive component examples, accessibility guidance
- `react-web` — full TDD workflow documented
- `agentic-development` — Claude SDK + Pydantic AI patterns, multi-model coverage

**Representative mid scorers (88/100):**
- `azure-cosmosdb` — missing `# [Name] Skill` title heading
- `ms-teams-apps` — missing `paths` field
- `workspace` — user-invocable but paths not declared

**Vague quantifier occurrences:** Low across the skill library. No skill exceeded the -20 cap. Typical deduction: 0–4 points.

---

## Security Scan

**Result: BLOCKED**

Two CRITICAL patterns found. Contribution is blocked until both are remediated and manually cleared.

---

### CRITICAL Findings

#### [C1] Binary Download and Execute — `scripts/install-graph-tools.sh:94-103`

```bash
if curl -fsSL "$DOWNLOAD_URL" -o "$TEMP_DIR/codebase-memory-mcp.tar.gz"; then
    tar xzf "$TEMP_DIR/codebase-memory-mcp.tar.gz" -C "$TEMP_DIR"
    mv "$TEMP_DIR/codebase-memory-mcp" "$INSTALL_DIR/codebase-memory-mcp"
    chmod +x "$INSTALL_DIR/codebase-memory-mcp"
    "$INSTALL_DIR/codebase-memory-mcp" install 2>/dev/null || true
fi
```

Downloads a pre-compiled binary from `github.com/DeusData/codebase-memory-mcp/releases/latest/download/codebase-memory-mcp-${OS}-${ARCH}.tar.gz` and immediately executes it. No checksum or signature verification. Pattern: **curl-download-and-execute**.

**Risk:** An adversary who compromises the GitHub release (supply chain attack, DNS hijack, MITM) delivers arbitrary code that runs with user privileges.

**Remediation:** Verify SHA256 checksum against a pinned value before executing. Pin to a specific release tag, not `latest`.

---

#### [C2] Same Pattern Embedded in NL Command — `commands/initialize-project.md:575-581`

```bash
if curl -fsSL "$DOWNLOAD_URL" -o "$TEMP_DIR/codebase-memory-mcp.tar.gz"; then
    tar xzf "$TEMP_DIR/codebase-memory-mcp.tar.gz" -C "$TEMP_DIR"
    mv "$TEMP_DIR/codebase-memory-mcp" "$INSTALL_DIR/codebase-memory-mcp"
    chmod +x "$INSTALL_DIR/codebase-memory-mcp"
    "$INSTALL_DIR/codebase-memory-mcp" install 2>/dev/null || true
fi
```

Same binary download-execute pattern duplicated as inline bash inside a natural language command definition. Claude executes this when asked to initialize a project.

**Risk:** Identical to C1. Additionally, being embedded in a NL command makes it invisible to users who review shell scripts but not markdown files.

**Remediation:** Same as C1 — checksum verification before execute. Consider delegating to the shell script (single source of truth) rather than duplicating the pattern.

---

### MEDIUM Findings

#### [M1] Runtime Package Install — `scripts/install-graph-tools.sh:177-178`

```bash
$PYTHON_CMD -m pip install -r "$CODEBADGER_DIR/requirements.txt"
```

Installs Python packages at runtime without version pinning or hash verification visible in context. The requirements.txt for the CodeBadger component is fetched from a just-cloned external repo (see M2).

**Risk:** Dependency confusion, unpinned package versions installed.

#### [M2] External `git clone` at Install Time — `scripts/install-graph-tools.sh:166`

```bash
git clone https://github.com/lekssays/joern-mcp.git
```

Clones an external repo during install. No pinned commit hash or tag — always pulls latest HEAD.

**Risk:** Breaks reproducibility. A compromised commit in `joern-mcp` becomes part of the bootstrap.

**Remediation:** Pin to a specific commit hash: `git clone --depth 1 && git checkout <sha>`.

#### [M3] Unquoted Variable in Hook — `hooks/pre-push:61`

```bash
if claude --print "/code-review $changed_files" > "$review_output" 2>&1; then
```

`$changed_files` is a space-separated list of file paths passed unquoted to the claude CLI. Filenames with special characters or spaces could cause unexpected behavior. The variable is built by grepping changed files for known extensions, which reduces (but does not eliminate) the exposure.

**Risk:** Low in practice but violates shell quoting best practices. Potential argument injection with adversarially named files.

**Remediation:** Pass files as a quoted list or newline-delimited stdin. Consider `printf '%s\n' $changed_files | claude --print "/code-review"`.

#### [M4] Claude CLI Invocation in Post-Commit Hook — `hooks/workspace/post-commit-contracts.sh:56`

```bash
claude --print "/sync-contracts --lightweight" > /dev/null 2>&1
```

Spawns the full Claude CLI as a post-commit side effect. This could consume API credits unexpectedly on every commit that touches contract files.

**Risk:** Unintended API spend, hook hangs if CLI unavailable, user surprise.

**Remediation:** Already guarded by `command -v claude &> /dev/null`. Consider an opt-in mechanism (env var `CLAUDE_BOOTSTRAP_AUTO_SYNC=1`).

---

### LOW Findings

#### [L1] No Package Manifests Found

No `package.json` or `requirements.txt` at the repo root. The Python tools (`icpg/`, `mnemos/`) lack a top-level manifest, making dependency auditing (`npm audit`, `pip-audit`) impossible.

#### [L2] Python `subprocess` Usage Without `shell=True` (Safe)

`scripts/icpg/*.py` and `scripts/mnemos/*.py` use `subprocess.run()` extensively. All calls use list form (no `shell=True`), which is safe. No eval, os.system, or shell injection vectors found.

---

## Top Recommendations

### Priority 1 (Blocks contribution): Security

1. **Add checksum verification** before executing the `codebase-memory-mcp` binary (C1, C2). Pin the release URL to a specific version tag and verify SHA256.
2. **Pin `git clone`** to a specific commit hash for `joern-mcp` (M2).
3. After remediating C1/C2, manually clear the `security-blocked` label for re-audit.

### Priority 2 (High NL impact): Add frontmatter to commands

All 15 commands are missing `name`, `description`, and `allowed-tools` frontmatter. Adding these three fields to each command would raise the command average from 40 → ~85 and push the overall repo NL score from **80 → ~90**.

Minimal frontmatter block needed:
```yaml
---
name: command-name
description: One-line description of what this command does
allowed-tools: [Read, Bash, Write]
---
```

### Priority 3 (Medium NL impact): Add example blocks to agents

All 6 agents score 85/100 due to zero example blocks. Adding one example per agent raises the score to 95. Two examples per agent achieves maximum (+0 penalty).

### Priority 4 (Low NL impact): Empty-input handling

`mnemos-checkpoint.md` and `mnemos-status.md` have no guidance for what happens when invoked with no relevant state. Add a brief handling note ("If no checkpoint exists, report that no session is active") to recover the -10 each.

---

## Files Audited

**Agents (6):**
`skills/agent-teams/agents/merger.md`, `team-lead.md`, `code-review.md`, `feature.md`, `security.md`, `quality.md`

**Commands (15):**
`commands/spawn-team.md`, `sync-contracts.md`, `icpg-drift.md`, `initialize-project.md`, `icpg-bootstrap.md`, `maggy-init.md`, `icpg-impact.md`, `mnemos-checkpoint.md`, `maggy.md`, `update-code-index.md`, `analyze-workspace.md`, `mnemos-status.md`, `analyze-repo.md`, `icpg-why.md`, `check-contributors.md`

**Skills (61):**
All `skills/*/SKILL.md` files including: `base`, `security`, `session-management`, `code-review`, `ui-web`, `ui-mobile`, `ui-testing`, `typescript`, `react-web`, `react-native`, `flutter`, `android-java`, `android-kotlin`, `pwa-development`, `nodejs-backend`, `python`, `commit-hygiene`, `playwright-testing`, `user-journeys`, `agentic-development`, `agent-teams`, `code-deduplication`, `code-graph`, `cpg-analysis`, `icpg`, `codex-review`, `gemini-review`, `ai-models`, `llm-patterns`, `credentials`, `workspace`, `existing-repo`, `team-coordination`, `site-architecture`, `web-content`, `aeo-optimization`, `web-payments`, `posthog-analytics`, `klaviyo`, `reddit-api`, `reddit-ads`, `shopify-apps`, `woocommerce`, `medusa`, `firebase`, `supabase`, `supabase-nextjs`, `supabase-node`, `supabase-python`, `aws-aurora`, `aws-dynamodb`, `cloudflare-d1`, `azure-cosmosdb`, `database-schema`, `ms-teams-apps`, `maggy`, `mnemos`, `iterative-development`, `project-tooling`, `ticket-craft`, `site-architecture`

**Executable Surfaces Scanned:**
`scripts/install-graph-tools.sh`, `scripts/install-hooks.sh`, `hooks/pre-push`, `hooks/post-commit-graph`, `hooks/workspace/check-contract-freshness.sh`, `hooks/workspace/post-commit-contracts.sh`, `hooks/workspace/check-graph-freshness.sh`, `hooks/workspace/pre-push-contracts.sh`, `scripts/icpg/*.py`, `scripts/mnemos/*.py`

---

*Generated by nlpm-auditor · nlpm v0.x · 2026-04-20*
