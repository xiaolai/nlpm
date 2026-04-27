# NLPM Audit: navapbc/digital-service-orchestra

**Repo**: navapbc/digital-service-orchestra  
**Audited at**: 2026-04-27  
**Auditor**: NLPM auditor-audit workflow  
**Commit**: HEAD (main, post-discovery 2026-04-27)  
**Artifacts scored**: 89 (31 agents, 26 commands, 32 skills)  
**Plugin NL Score (plugin artifacts only)**: **84.8 / 100**  
**Overall NL Score (all artifacts including shims)**: **66.8 / 100**  
**Security gate**: PASS — no Critical or High findings

---

## NL Score Summary

### Agents (31 files — `plugins/dso/agents/`)

All agents have complete YAML frontmatter (`name`, `description`, `model`, `color`). The primary penalty across most agents is a single worked-example block (-5 per agent). Twelve agents with 2+ worked examples earn no example penalty.

| Artifact | Score | Key Deductions |
|----------|-------|----------------|
| approach-decision-maker.md | 93 | none (2 ADR output formats) |
| bloat-blue-team.md | 90 | -5 (1 JSON example) |
| bloat-resolver.md | 90 | -5 (1 JSON example) |
| blue-team-filter.md | 90 | -5 (1 JSON example) |
| bot-psychologist.md | 90 | -2 (taxonomy count mismatch in RESULT schema) |
| code-reviewer-deep-arch.md | 90 | -5 (1 JSON example) |
| code-reviewer-deep-correctness.md | 90 | -5 (1 JSON example) |
| code-reviewer-deep-hygiene.md | 90 | -5 (1 JSON example) |
| code-reviewer-deep-verification.md | 90 | -5 (1 JSON example) |
| code-reviewer-light.md | 90 | -5 (1 JSON example) |
| code-reviewer-performance.md | 90 | -5 (1 JSON example) |
| code-reviewer-security-blue-team.md | 90 | -5 (1 JSON example) |
| code-reviewer-security-red-team.md | 90 | -5 (1 JSON example) |
| code-reviewer-standard.md | 90 | -5 (1 JSON example) |
| code-reviewer-test-quality.md | 90 | -5 (1 JSON example) |
| completion-verifier.md | 95 | none (sentinel-state table + 3 gate examples) |
| complexity-evaluator.md | 97 | none (6 worked B/F examples) |
| conflict-analyzer.md | 87 | -8 (classification criteria only, no worked input→output example) |
| cross-epic-interaction-classifier.md | 95 | none (2 signal examples) |
| doc-writer.md | 90 | -5 (1 JSON example) |
| feasibility-reviewer.md | 90 | -5 (1 JSON example) |
| huge-diff-refactor-anomaly.md | 87 | -5 (1 JSON example), -3 (self-contradicting REPO_ROOT guidance) |
| huge-diff-reviewer-light.md | 87 | -5 (1 JSON example), -3 (self-contradicting REPO_ROOT guidance) |
| huge-diff-reviewer-standard.md | 87 | -5 (1 JSON example), -3 (self-contradicting REPO_ROOT guidance) |
| intent-search.md | 95 | none (3 worked gate-signal examples) |
| plan-review.md | 85 | -15 (zero worked examples) |
| red-team-reviewer.md | 95 | none (2 taxonomy-category finding examples) |
| red-test-evaluator.md | 95 | none (5 verdict worked examples) |
| red-test-writer.md | 93 | none (GOOD/BAD pattern section counts as 2+ examples) |
| scope-drift-reviewer.md | 95 | none (in_scope / ambiguous / out_of_scope examples) |
| ui-designer.md | 90 | -5 (1 return payload example) |
| **Agent average** | **90.8** | |

### Commands — dispatch shims (23 files — `.claude/commands/`)

These files are auto-generated host-project dispatch shims. Each is a 7-line boilerplate that detects plugin installation and routes to either the Skill tool or the plugin SKILL.md. They have no YAML frontmatter, no model declaration, no examples, and no output format specification by design. Their low NL scores reflect structural absence, not semantic quality — they are infrastructure, not instruction files.

| Artifact | Score | Note |
|----------|-------|------|
| architect-foundation.md | 15 | dispatch shim, no frontmatter |
| brainstorm.md | 15 | dispatch shim, no frontmatter |
| debug-everything.md | 15 | dispatch shim, no frontmatter |
| design-review.md | 15 | dispatch shim, no frontmatter |
| dryrun.md | 15 | dispatch shim, no frontmatter |
| end-session.md | 15 | dispatch shim, no frontmatter |
| fix-bug.md | 15 | dispatch shim, no frontmatter |
| fix-cascade-recovery.md | 15 | dispatch shim, no frontmatter |
| generate-claude-md.md | 15 | dispatch shim, no frontmatter |
| implementation-plan.md | 15 | dispatch shim, no frontmatter |
| init.md | 15 | dispatch shim, no frontmatter |
| interface-contracts.md | 15 | dispatch shim, no frontmatter |
| onboarding.md | 15 | dispatch shim, no frontmatter |
| playwright-debug.md | 15 | dispatch shim, no frontmatter |
| preplanning.md | 15 | dispatch shim, no frontmatter |
| quick-ref.md | 15 | dispatch shim, no frontmatter |
| resolve-conflicts.md | 15 | dispatch shim, no frontmatter |
| retro.md | 15 | dispatch shim, no frontmatter |
| review-stats.md | 15 | dispatch shim, no frontmatter |
| roadmap.md | 15 | dispatch shim, no frontmatter |
| sprint.md | 15 | dispatch shim, no frontmatter |
| tickets-health.md | 15 | dispatch shim, no frontmatter |
| update-docs.md | 15 | dispatch shim, no frontmatter |
| **Shim average** | **15** | systemic; see Q001 |

### Commands — plugin commands (3 files — `plugins/dso/commands/`)

| Artifact | Score | Key Deductions |
|----------|-------|----------------|
| commit.md | 20 | -25 no YAML name, -25 no YAML description, -5 no model, -15 no examples, -10 no output format |
| end.md | 15 | 1-line redirect; all structural fields missing |
| review.md | 20 | -25 no YAML name, -25 no YAML description, -5 no model, -15 no examples, -10 no output format |
| **Plugin-commands average** | **18** | |

### Skills (32 files — `plugins/dso/skills/*/SKILL.md`)

All skills have `name`, `description`, and `allowed-tools` in frontmatter. None declare `model` (-5 each; skills inherit model from the dispatching orchestrator). Most have at least one usage code block. Major orchestrator skills (sprint, fix-bug, brainstorm, preplanning, debug-everything, implementation-plan, dryrun) have multiple usage variants (2+ examples, no example penalty).

| Artifact | Score | Key Deductions |
|----------|-------|----------------|
| architect-foundation/SKILL.md | 85 | -5 no model, -5 1 example, -5 informal output |
| brainstorm/SKILL.md | 90 | -5 no model, 2+ usage variants |
| create-bug/SKILL.md | 80 | -5 no model, -15 0 worked examples (references external template) |
| debug-everything/SKILL.md | 90 | -5 no model, 3 usage modes |
| design-review/SKILL.md | 85 | -5 no model, -5 1 example, -5 informal output |
| design-wireframe/SKILL.md | 85 | -5 no model, -5 1 example, -5 informal output |
| dryrun/SKILL.md | 90 | -5 no model, 2+ usage patterns |
| end-session/SKILL.md | 85 | -5 no model, -5 1 example |
| fix-bug/SKILL.md | 90 | -5 no model, multiple classification paths as usage |
| fix-cascade-recovery/SKILL.md | 85 | -5 no model, -5 1 example, -5 informal output |
| generate-claude-md/SKILL.md | 85 | -5 no model, -5 1 example |
| implementation-plan/SKILL.md | 90 | -5 no model, 2+ usage modes |
| init/SKILL.md | 85 | -5 no model, -5 1 usage block |
| interface-contracts/SKILL.md | 85 | -5 no model, -5 1 example |
| onboarding/SKILL.md | 85 | -5 no model, -5 1 example |
| oscillation-check/SKILL.md | 80 | -5 no model, -15 0 examples |
| plan-review/SKILL.md | 85 | -5 no model, -5 1 example |
| playwright-debug/SKILL.md | 85 | -5 no model, -5 1 example |
| preplanning/SKILL.md | 90 | -5 no model, 3 usage modes |
| quick-ref/SKILL.md | 85 | -5 no model, -5 1 usage block |
| resolve-conflicts/SKILL.md | 85 | -5 no model, -5 1 example |
| retro/SKILL.md | 85 | -5 no model, -5 1 example |
| review-protocol/SKILL.md | 83 | -5 no model, -5 1 example, -7 references external schema (partial output spec) |
| review-stats/SKILL.md | 85 | -5 no model, -5 1 example |
| roadmap/SKILL.md | 85 | -5 no model, -5 1 example |
| sprint/SKILL.md | 90 | -5 no model, 3+ usage modes |
| tickets-health/SKILL.md | 85 | -5 no model, -5 1 usage block |
| ui-discover/SKILL.md | 85 | -5 no model, -5 1 example |
| update-docs/SKILL.md | 85 | -5 no model, -5 1 example |
| using-dso/SKILL.md | 85 | -5 no model, -5 1 example |
| validate-work/SKILL.md | 85 | -5 no model, -5 1 example |
| verification-before-completion/SKILL.md | 83 | -5 no model, -5 1 example, -7 minimal output spec |
| **Skill average** | **85.8** | |

### Score Aggregation

| Category | Count | Avg Score | Total Points |
|----------|-------|-----------|--------------|
| Agents | 31 | 90.8 | 2815 |
| Dispatch shims (.claude/commands) | 23 | 15.0 | 345 |
| Plugin commands (plugins/dso/commands) | 3 | 18.0 | 55 |
| Skills | 32 | 85.8 | 2746 |
| **All artifacts** | **89** | **66.7** | **5961** |
| **Plugin artifacts only** | **66** | **87.0** | **5616** |

> The 23 dispatch shim files score 15/100 each by design (no frontmatter by construction). Excluding them, the plugin's NL quality is **87.0/100**, well above the 70-point threshold.

---

## Security Scan

### Critical / High

None found.

### Medium

**SEC-001 — `eval` on user-configurable config batch output (`plugins/dso/hooks/lib/config-paths.sh:57`)**

```bash
# eval is safe: read-config.sh --batch single-quotes every value and only
# emits KEY='value' assignments ...
eval "$_cfg_batch_raw" 2>/dev/null || true
```

`eval` executes the raw output of `read-config.sh --batch`, which is trusted to single-quote each value. If a config value contains a single-quote escape sequence or if `read-config.sh` has a quoting defect, this becomes a code injection vector. The code comment documents awareness but relies on an external safety invariant that is not enforced at the call site.

**Recommended fix**: Replace `eval` with a safer config-loader (e.g., parse `KEY=VALUE` pairs line-by-line using `read` + variable assignment without eval).

---

**SEC-002 — Sudo privilege escalation in deps.sh (`plugins/dso/hooks/lib/deps.sh:227`)**

```bash
sudo -n systemctl start docker 2>/dev/null || return 1
```

On Linux systems where the user has passwordless sudo, this hook attempts to start the Docker daemon automatically. The `-n` flag prevents interactive prompting but succeeds silently when sudo is configured with `NOPASSWD`. A compromised hook environment could leverage this to escalate privileges.

**Recommended fix**: Remove the automatic `sudo systemctl start docker`; emit an actionable error message instructing the user to start Docker manually.

---

**SEC-003 — Binary download without integrity verification (`plugins/dso/scripts/onboarding/acli-version-resolver.sh:99`)**

```bash
if ! curl -fsSL -o "$ACLI_BIN" "$LATEST_URL"; then
```

Downloads the Atlassian CLI binary from `https://acli.atlassian.com` directly to a temp path and then executes it (`chmod +x "$ACLI_BIN"` followed by `"$ACLI_BIN" --version`). No SHA-256 checksum or GPG signature is verified before execution. While HTTPS provides transport integrity, a compromised CDN or MITM (e.g., corporate proxy) could serve a malicious binary.

**Recommended fix**: Pin to a specific version and verify a published SHA-256 or GPG signature before executing the downloaded binary.

### Low

**SEC-004 — `eval` on user-configured format command (`plugins/dso/hooks/auto-format.sh:155`)**

```bash
if ! eval "$FORMAT_CMD" >/dev/null 2>&1; then
```

`FORMAT_CMD` is read from project config (`read-config.sh`). If an attacker can write to `.claude/dso-config.conf`, they can inject arbitrary shell commands. This is inherently lower risk than SEC-001 because the format command is user-supplied project configuration; a user who controls the config file also controls the repo. Nonetheless, explicit command injection via config is worth documenting.

**Recommended fix**: Validate `FORMAT_CMD` against an allowlist or use `"$SHELL" -c "$FORMAT_CMD"` with a no-op safety wrapper.

### Clean (no issues found)

- No `curl | bash` or `curl | sh` execution (the reference in `validate-nava-platform-headless.sh` is an `echo` to stderr for user instructions, not execution)
- No reverse shell patterns (`/dev/tcp`, `ncat`, `nc -e`)
- No base64+exec chains
- No credential exfiltration to unknown endpoints (Anthropic API calls in `enrich-file-impact.sh` use `ANTHROPIC_API_KEY` to call `api.anthropic.com`, the expected service)
- No postinstall scripts in `package.json`
- No `.mcp.json` files with broad permissions found

---

## Bugs

**BUG-001 — Self-contradicting REPO_ROOT guidance in three huge-diff reviewer agents** (severity: medium)

Three agents — `huge-diff-reviewer-standard.md`, `huge-diff-reviewer-light.md`, and `huge-diff-refactor-anomaly.md` — each exhibit the same contradictory pattern:

- **Step 1 / Step 3 code blocks** (what the agent executes):
  ```bash
  REPO_ROOT=$(git rev-parse --show-toplevel)
  "$REPO_ROOT/.claude/scripts/dso" verify-review-diff.sh "$DIFF_FILE_PATH"
  ```
- **Step 2 explicit warning** in the same agent:
  > "Do NOT re-derive REPO_ROOT via `git rev-parse --show-toplevel` — in worktree sessions the command returns the worktree path, which may differ from the repo root passed to you"

The code blocks re-derive `REPO_ROOT` via `git rev-parse` for the purpose of resolving the `.claude/scripts/dso` shim path. The Step 2 warning is intended to prevent using this re-derived value for *context lookups* (grep, Read, Glob on source files). However, the warning is phrased as an absolute prohibition, directly contradicting the Step 1/3 code blocks. A model following these instructions encounters a genuine conflict: the code says "do X", the warning says "do NOT do X".

**Risk**: In worktree sessions, the agent may use the worktree REPO_ROOT for source-file context lookups rather than the dispatch-prompt REPO_ROOT, leading to grep returning no matches and producing false-positive or false-negative review findings.

**Affected files**:
- `plugins/dso/agents/huge-diff-reviewer-standard.md` lines 70, 81, 247
- `plugins/dso/agents/huge-diff-reviewer-light.md` lines 70, 81, 247
- `plugins/dso/agents/huge-diff-refactor-anomaly.md` lines 61, 74, 207

**Suggested fix**: Distinguish the two uses explicitly. In Step 1/3, annotate the code block:
```bash
# Use git rev-parse here ONLY to locate the shim script in the agent's working tree.
# Do NOT use this REPO_ROOT for source-file context lookups in Step 2.
REPO_ROOT=$(git rev-parse --show-toplevel)
```
Update the Step 2 warning to say "Do NOT use the git-rev-parse REPO_ROOT value for source-file context lookups — use the REPO_ROOT from your dispatch prompt instead."

---

**BUG-002 — `bot-psychologist.md` RESULT schema names "15-point taxonomy" but defines 16 failure modes** (severity: low)

The agent's `taxonomy_item` RESULT schema field is documented as:
```
"taxonomy_item": "Name of the failure mode from the 15-point taxonomy"
```

But the taxonomy section lists 16 distinct failure modes (Context Window Exhaustion, Hallucination, Reasoning Fallacy, Instruction Following Failure, Tool Use Failure, Context Mismatch, Meta-Cognitive Failure, Boundary Violation, Anchoring Bias, Framing Effect, Availability Heuristic, Planning Fallacy, Sycophancy, Skill Gap, Self-Reference Loop, Cascade Failure). The frontmatter `description` correctly states "16-point failure taxonomy". The `taxonomy_item` schema comment is stale.

**Risk**: Consumers that validate `taxonomy_item` values against a count-based expectation may incorrectly flag valid "16th mode" taxonomy items (Cascade Failure) as out-of-schema.

**Affected file**: `plugins/dso/agents/bot-psychologist.md` line 112

**Suggested fix**: Change `"Name of the failure mode from the 15-point taxonomy"` to `"Name of the failure mode from the 16-point taxonomy"`.

---

## Quality Issues

**Q001 — 23 dispatch shim commands lack all NLPM frontmatter fields** (severity: low / systemic)

All 23 files in `.claude/commands/` are 7-line dispatch shims generated by the DSO plugin installer. They have no YAML frontmatter (`name`, `description`, `model`, `allowed-tools`), no worked examples, and no output format specification. Each scores 15/100 under the NLPM rubric, pulling the overall artifact average from 87.0 to 66.8.

These files are infrastructure boilerplate, not user-facing NL instruction artifacts. Their low scores reflect structural design, not semantic quality.

**Recommended action**: If NLPM is used to gate plugin releases, exclude `.claude/commands/` dispatch shims from aggregate scoring via a rule override or scope exclusion. Alternatively, add a minimal 3-line frontmatter block to the shim template:
```yaml
---
name: <skill-name>
description: Dispatch shim — routes to /dso:<skill-name> via Skill tool or SKILL.md fallback
---
```
This would raise each shim from 15/100 to ~60/100 (still penalized for missing model, examples, output format).

---

**Q002 — All 32 SKILL.md files missing `model` field in frontmatter** (severity: low / systemic)

Skills inherit the model from their dispatching orchestrator and are intended to run at whatever model tier the orchestrator selects. The absence of `model:` is intentional but incurs a -5 NLPM penalty per file (32 × -5 = -160 aggregate quality impact).

**Recommended action**: Add a rule override to suppress `NL-MISSING-MODEL` for the `plugins/dso/skills/**` path scope in `.claude/nlpm.local.md`:
```yaml
rule_overrides:
  - rule: NL-MISSING-MODEL
    scope: plugins/dso/skills/**
    action: suppress
    reason: Skills inherit model from dispatching orchestrator; model is not a fixed property
```

---

**Q003 — `plan-review` agent has zero worked examples** (severity: medium)

`plugins/dso/agents/plan-review.md` is the only agent with no example output blocks. The agent body is 5 lines and defers all logic to an external template at `${CLAUDE_PLUGIN_ROOT}/docs/workflows/prompts/plan-review-dispatch.md`. Without an example, consumers cannot confirm the expected output format without reading the external template.

**Score impact**: -15 (zero examples vs -5 for one example)

**Suggested fix**: Add a minimal worked example showing a plan that passes and one that fails, conforming to the output schema in `plan-review-dispatch.md`.

---

**Q004 — `plugins/dso/commands/` plugin commands missing YAML frontmatter** (severity: medium)

`commit.md`, `review.md`, and `end.md` in `plugins/dso/commands/` are real NL artifacts (not dispatch shims) but lack YAML frontmatter. They have descriptive headings and numbered steps in their body, but NLPM scoring requires frontmatter fields.

**Score impact**: 20/100 each vs ~80/100 if frontmatter were added

**Suggested fix**: Add frontmatter to each:
```yaml
---
name: commit
description: Create a git commit through mandatory test, format, and review gates
allowed-tools: Read, Bash
---
```

---

**Q005 — Eleven generated code-reviewer agents each have exactly one JSON example** (severity: low)

The eleven single-pass reviewer agents (code-reviewer-light, code-reviewer-standard, code-reviewer-deep-hygiene, code-reviewer-deep-correctness, code-reviewer-deep-verification, code-reviewer-performance, code-reviewer-security-red-team, code-reviewer-security-blue-team, code-reviewer-test-quality, doc-writer, feasibility-reviewer) each contain one JSON example showing a finding object.

**Score impact**: -5 per agent × 11 = -55 aggregate quality impact

**Suggested fix**: Add a second contrasting example (e.g., a `triggered: false` / `triggered: true` pair, or a `critical` vs `minor` severity pair) to each generated agent. This can be automated via the `build-review-agents.sh` generation script.

---

## Cross-Component

**CC001 — `scope-drift-reviewer` agent name is intentionally un-prefixed; REVIEW-DEFENSE block is clear** (informational)

`plugins/dso/agents/scope-drift-reviewer.md` frontmatter has `name: scope-drift-reviewer` (not `dso:scope-drift-reviewer`). The agent includes a 200-word `REVIEW-DEFENSE` comment documenting that the plugin framework auto-prefixes agent names at registration time, so the un-prefixed form correctly registers as `dso:scope-drift-reviewer`. All sibling agents follow the same convention.

**Status**: No action required. The invariant is correctly documented. Monitor if the plugin framework behavior changes.

---

**CC002 — All 31 agents are registered in `plugin.json`; no orphans or missing registrations** (informational)

Cross-checked the 31 agent files in `plugins/dso/agents/` against the `agents` array in `plugins/dso/.claude-plugin/plugin.json`. All 31 match exactly. The CLAUDE.md routing table is consistent with plugin.json. No agents are missing from registration; no orphaned agent files exist.

---

**CC003 — Skills that reference external phase files are not scored separately** (informational)

Several SKILL.md files (brainstorm, preplanning, sprint) reference phase files loaded on demand (`phases/convert-to-epic.md`, `phases/post-scrutiny-handlers.md`, etc.). These phase files are not in scope for the current audit. If NLPM scores these phase files separately in future audits, the aggregate skill score for brainstorm/preplanning/sprint should be recomputed as the minimum of the SKILL.md score and its phase file scores.
