# NLPM Audit: rtk-ai/rtk
**Date**: 2026-04-19  |  **Artifacts**: 33  |  **Strategy**: batched
**NL Score**: 88/100
**Security**: BLOCKED
**Bugs**: 5  |  **Quality Issues**: 30  |  **Security Findings**: 9

---

## NL Score Summary

| File | Type | Score | Top Deductions |
|------|------|-------|----------------|
| `.claude/skills/pr-review/SKILL.md` | skill | 68 | missing `name` (-25), no output format (-5) |
| `.claude/skills/performance/SKILL.md` | skill | 71 | missing `name` (-25), no output format (-5) |
| `.claude/skills/repo-recap/SKILL.md` | skill | 71 | missing `name` (-25), space-separated allowed-tools |
| `.claude/agents/rust-rtk.md` | agent | 73 | no examples (-15), no output format (-10) |
| `.claude/agents/rtk-testing-specialist.md` | agent | 73 | no examples (-15), no output format (-10) |
| `.claude/skills/ship/SKILL.md` | skill | 73 | missing `name` (-25) |
| `.claude/skills/security-guardian/SKILL.md` | skill | 73 | missing `name` (-25) |
| `.claude/agents/technical-writer.md` | agent | 81 | no examples (-15), minor vague language (-2) |
| `.claude/commands/worktree.md` | command | 83 | no allowed-tools (-5), no empty input check (-10) |
| `.claude/commands/tech/worktree.md` | command | 83 | no allowed-tools (-5), no empty input check (-10) |
| `.claude/commands/test-routing.md` | command | 85 | no allowed-tools (-5), no empty input check (-5), mixed language (-3) |
| `.claude/skills/code-simplifier/SKILL.md` | skill | 88 | no output format (-10), minor vague language (-2) |
| `CLAUDE.md` | project | 88 | minor vague language (-6), no structured scoring section |
| `.github/hooks/rtk-rewrite.json` | hook | 90 | non-standard location (`.github/` vs `.claude/`) |
| `.claude/commands/diagnose.md` | command | 91 | no allowed-tools (-5), mixed language (-4) |
| `.claude/commands/tech/codereview.md` | command | 91 | no allowed-tools (-5), mixed language (-4) |
| `.claude/skills/design-patterns/SKILL.md` | skill | 91 | no output format (-5), minor vague language (-4) |
| `.claude/agents/system-architect.md` | agent | 93 | weak examples (-5), minor vague language (-2) |
| `.claude/skills/rtk-tdd/SKILL.md` | skill | 93 | minor vague language (-4), no triggers field |
| `.claude/skills/issue-triage/SKILL.md` | skill | 94 | minor vague quantifiers (-4), effort estimate range wide |
| `.claude/agents/debugger.md` | agent | 95 | minor vague language (-3), color only (-2) |
| `.claude/agents/code-reviewer.md` | agent | 95 | no tools declared (implicit all), minor vague (-5) |
| `.claude/commands/clean-worktree.md` | command | 95 | no allowed-tools (-5) |
| `.claude/commands/worktree-status.md` | command | 95 | no allowed-tools (-5) |
| `.claude/commands/clean-worktrees.md` | command | 95 | no allowed-tools (-5) |
| `.claude/commands/tech/clean-worktree.md` | command | 95 | no allowed-tools (-5) |
| `.claude/commands/tech/worktree-status.md` | command | 95 | no allowed-tools (-5) |
| `.claude/commands/tech/remove-worktree.md` | command | 95 | no allowed-tools (-5) |
| `.claude/commands/tech/clean-worktrees.md` | command | 95 | no allowed-tools (-5) |
| `.claude/skills/tdd-rust/SKILL.md` | skill | 96 | minor vague language (-2), no tags field |
| `.claude/skills/pr-triage/SKILL.md` | skill | 96 | minor vague language (-2), narrow effort range |
| `.claude/commands/tech/audit-codebase.md` | command | 96 | minor vague language (-4) |
| `.claude/skills/rtk-triage/SKILL.md` | skill | 98 | minor vague quantifiers (-2) |

**Weighted average**: 2894 / 33 = **87.7 → 88/100**

---

## Security Scan

**Pre-scan summary**: Hooks: 2 shell scripts + 1 JSON config | Scripts: 20 | Critical matches: 3 | High matches: 1

### Severity Counts

| Severity | Count |
|----------|-------|
| CRITICAL | 3 |
| HIGH | 1 |
| MEDIUM | 3 |
| LOW | 2 |
| **Total** | **9** |

### Execution Surface Inventory

| File | Surface Type | Triggered By |
|------|-------------|-------------|
| `.claude/hooks/rtk-rewrite.sh` | PreToolUse shell hook | Claude Code tool calls |
| `.github/hooks/rtk-rewrite.json` | PreToolUse JSON hook config | Claude Code tool calls |
| `hooks/claude/rtk-rewrite.sh` | PreToolUse shell hook (alternate path) | Claude Code tool calls |
| `install.sh` | Installer script | Manual user execution / curl-pipe-sh |
| `scripts/benchmark.sh` | Benchmark runner | Manual developer execution |
| `scripts/test-all.sh` | Smoke test runner | Manual / CI execution |
| `scripts/update-readme-metrics.sh` | README updater | CI execution |

### Security Findings

| # | Severity | File | Line | Pattern | Finding |
|---|----------|------|------|---------|---------|
| 1 | CRITICAL | `scripts/benchmark.sh` | 47 | eval-with-var | `unix_out=$(eval "$unix_cmd" 2>/dev/null)` — eval executes arbitrary string from variable; attacker-controlled command names in `bench()` callers become code execution |
| 2 | CRITICAL | `scripts/benchmark.sh` | 48 | eval-with-var | `rtk_out=$(eval "$rtk_cmd" 2>/dev/null)` — same pattern; both eval calls inside `bench()` function accept caller-supplied strings without sanitization |
| 3 | CRITICAL | `install.sh` | 3 | curl-pipe-sh | Comment documents `curl -fsSL .../install.sh \| sh` as the canonical install method; executes remote code without review or integrity check |
| 4 | HIGH | `install.sh` | 82 | binary-no-checksum | `curl -fsSL "$DOWNLOAD_URL" -o "$ARCHIVE"` downloads release binary with no sha256sum/checksum verification before execution; MITM or CDN compromise delivers malicious binary |
| 5 | MEDIUM | `scripts/benchmark.sh` | 55–70 | external-network | `bench()` calls include `curl https://httpbin.org/...` in the benchmark suite; outbound network to third-party during CI/developer runs creates data-exfil surface and supply-chain dependency |
| 6 | MEDIUM | `install.sh` | 60–90 | unpinned-download | Download URL constructed from latest GitHub release tag at runtime; no commit-hash or content-hash pinning means a compromised release replaces binary silently |
| 7 | MEDIUM | `hooks/claude/rtk-rewrite.sh` | 12–18 | cache-race | Version-ok sentinel written to `$HOME/.cache/rtk-hook-version-ok`; world-readable cache file in shared environments can be pre-created to bypass version guard |
| 8 | LOW | `.claude/hooks/rtk-rewrite.sh` | 30–35 | sensitive-log | `printf` audit logging captures full `$CLAUDE_TOOL_INPUT` including file paths and content snippets; log may persist sensitive data on disk |
| 9 | LOW | `hooks/claude/rtk-rewrite.sh` | 14 | semver-string-cmp | Version comparison uses `[[ "$current" < "$required" ]]` (lexicographic); will misorder versions like `0.9.x > 0.23.x`; version guard can be bypassed on specific version strings |

**Verdict: BLOCKED** — 3 Critical findings. `scripts/benchmark.sh` uses `eval` with unsanitized variables (findings #1, #2). `install.sh` documents curl-pipe-sh as canonical install (finding #3). Contribution gate must not proceed until Critical findings are resolved by upstream maintainers.

---

## Bugs (PR-worthy)

These are registration-breaking or functional defects — not style issues.

### BUG-1: Five Skills Missing Required `name` Field

**Severity**: Registration-breaking (Claude Code cannot register skill without `name`)

**Files affected**:
- `.claude/skills/performance/SKILL.md`
- `.claude/skills/pr-review/SKILL.md`
- `.claude/skills/repo-recap/SKILL.md`
- `.claude/skills/ship/SKILL.md`
- `.claude/skills/security-guardian/SKILL.md`

**Fix**: Add `name: <skill-identifier>` to each frontmatter block. Example:
```yaml
---
name: performance
description: Performance profiling and optimization workflow for RTK filters
allowed-tools: Read Grep Glob Bash
---
```

**Impact**: Without `name`, these skills cannot be invoked by name in Claude Code. They may still load as context but are undiscoverable via `/skills list`.

---

## Security Fixes (PR-worthy — Medium/Low only)

Critical and High findings (#1–#4) require upstream maintainer action. Medium/Low fixes are safe to contribute.

### SEC-FIX-1: Replace `eval` in `benchmark.sh` with direct execution

**Finding**: #1, #2 (CRITICAL — listed for completeness, not contribution target)

**Note**: Not contributing this PR per policy; flagging for upstream.

### SEC-FIX-2: Add checksum verification to `install.sh`

**Finding**: #4 (HIGH)

**Note**: Not contributing; flagging for upstream.

### SEC-FIX-3: Remove httpbin.org dependency from benchmark suite

**Finding**: #5 (MEDIUM)

**File**: `scripts/benchmark.sh`

**Fix**: Replace `curl https://httpbin.org/...` benchmark calls with a local mock endpoint or remove the network benchmark from the default suite. Use `--network` flag to opt in.

### SEC-FIX-4: Restrict permissions on version cache file

**Finding**: #7 (MEDIUM)

**File**: `hooks/claude/rtk-rewrite.sh`

**Fix**: After writing cache sentinel, apply `chmod 600 "$HOME/.cache/rtk-hook-version-ok"` to restrict read access to owner only.

### SEC-FIX-5: Fix semver comparison in version guard

**Finding**: #9 (LOW)

**File**: `hooks/claude/rtk-rewrite.sh`

**Fix**: Replace string comparison with proper semver logic. Minimal fix:
```bash
# Replace lexicographic [[ "$current" < "$required" ]] with:
version_lt() { [ "$(printf '%s\n' "$1" "$2" | sort -V | head -1)" = "$1" ] && [ "$1" != "$2" ]; }
if version_lt "$current" "$required"; then ...
```

---

## Quality Issues

These are non-blocking but reduce effectiveness and consistency.

### QI-1: 12 Commands Missing `allowed-tools`

All commands except `tech/audit-codebase.md` omit `allowed-tools` in frontmatter. Claude Code uses this field to scope tool access; without it, the command runs with whatever tools are available in context.

**Affected**: `worktree.md`, `clean-worktree.md`, `worktree-status.md`, `test-routing.md`, `clean-worktrees.md`, `diagnose.md`, `tech/worktree.md`, `tech/clean-worktree.md`, `tech/worktree-status.md`, `tech/codereview.md`, `tech/clean-worktrees.md`, `tech/remove-worktree.md`

**Fix**: Add `allowed-tools: [Bash]` (or appropriate subset) to each command's frontmatter.

### QI-2: 2 Agents Missing Examples

**Files**: `rust-rtk.md`, `rtk-testing-specialist.md`

Both agents describe complex workflows but provide zero `<example>` blocks. Without examples, Claude Code agents struggle to calibrate when and how to invoke the agent.

**Fix**: Add at minimum 2 `<example>` blocks showing: (a) a trigger scenario and (b) what the expected output looks like.

### QI-3: 2 Agents Missing Output Format

**Files**: `rust-rtk.md`, `rtk-testing-specialist.md`

No "Output Format" or "Response Format" section. For agents that write files and run tests, users need to know what structured output to expect.

### QI-4: 2 Commands Missing Empty Input Guard

**Files**: `worktree.md`, `tech/worktree.md`

Both take a `$ARGUMENTS` branch name but do not check `if [ -z "$ARGUMENTS" ]`. If invoked without an argument, they proceed with an empty branch name, likely producing confusing git errors.

**Fix**: Add guard at top of script body:
```bash
if [ -z "$ARGUMENTS" ]; then
  echo "Usage: /worktree <branch-name>" >&2
  exit 1
fi
```

### QI-5: Mixed French/English in 3 Commands

**Files**: `test-routing.md`, `diagnose.md`, `tech/codereview.md`

Section headers and step labels mix French and English (e.g., `Étape 1:`, `Options de déploiement:`). This is inconsistent with the rest of the repository (English-only) and may cause localization issues in Claude Code rendering.

**Fix**: Translate French section headers to English or add a language declaration in frontmatter.

### QI-6: Hook Config in Non-Standard Location

**File**: `.github/hooks/rtk-rewrite.json`

Claude Code looks for hook configurations in `.claude/hooks/`. Placing the JSON config in `.github/hooks/` means it will not be auto-discovered by `rtk init` or Claude Code's hook loading mechanism.

**Fix**: Move or symlink to `.claude/hooks/rtk-rewrite.json`.

### QI-7: Space-Separated `allowed-tools` in 3 Skills

**Files**: `repo-recap/SKILL.md` (`allowed-tools: Bash Read Grep`), `ship/SKILL.md`, `security-guardian/SKILL.md`

The Claude Code skill schema expects `allowed-tools` as a YAML list (`[Bash, Read, Grep]`) or block list. Space-separated strings may parse incorrectly depending on the YAML parser version.

**Fix**: Convert to bracket notation:
```yaml
allowed-tools: [Bash, Read, Grep]
```

### QI-8: Vague Quantifiers Throughout

Pattern `"ensure"`, `"appropriate"`, `"relevant"`, `"good"`, `"properly"` appear frequently across agents and skills. Examples:
- `debugger.md`: "ensure root cause is identified" (what evidence counts?)
- `technical-writer.md`: "appropriate level of detail" (what's the threshold?)
- `rust-rtk.md`: "properly handle errors" (vs. the concrete `.context("desc")?` rule)

**Recommendation**: Replace with measurable criteria. E.g., "ensure root cause is identified" → "identify the exact file:line where the failure originates and state the invariant violated."

---

## Cross-Component Consistency

### CC-1: Duplicated Worktree Commands (root vs `tech/`)

`.claude/commands/worktree.md` and `.claude/commands/tech/worktree.md` are near-identical. The `tech/` version appears to be a copy with minor enhancements. Both have the same `allowed-tools` gap (QI-1) and empty input gap (QI-4).

**Recommendation**: Consolidate to one canonical version in `tech/` and remove the root duplicate, or add a note to root version redirecting to `tech/`.

### CC-2: Hook Path Inconsistency

Three hook files exist across three paths:
- `.claude/hooks/rtk-rewrite.sh` — Claude Code path, shell
- `.github/hooks/rtk-rewrite.json` — Non-standard path, JSON config
- `hooks/claude/rtk-rewrite.sh` — Non-standard path, shell

Only `.claude/hooks/rtk-rewrite.sh` will be auto-loaded by Claude Code. The other two require manual configuration. The JSON config at `.github/hooks/` overlaps in function with the shell scripts.

**Recommendation**: Standardize on `.claude/hooks/` as the single hook location. Document the alternate paths as installation options, not parallel active hooks.

### CC-3: RTK Version References

`hooks/claude/rtk-rewrite.sh` checks for rtk >= 0.23.0 but `CLAUDE.md` references version 0.28.2. The version guard will always pass for any modern installation, making it dead code. Update the minimum version check to reflect actual minimum required version, or remove if not meaningful.

### CC-4: Agent Tool Scope vs. Skill Tool Scope

Several agents (`technical-writer.md`, `rust-rtk.md`) declare `Write` and `Edit` in their tools list, while the NLPM scoring rubric flags Write/Edit on read-only agents. These agents are explicitly write-agents (they produce output files), so this is correct — but the skill files that omit `name` (BUG-1) may be loaded as read-only context where write operations would be unexpected.

---

## Recommendation

**BLOCKED** — Do not proceed with contribution workflow.

**Reason**: 3 Critical security findings must be resolved by upstream maintainers before any PR contribution:
1. `eval` with unsanitized variables in `scripts/benchmark.sh:47-48` (arbitrary code execution)
2. Documented `curl-pipe-sh` install pattern in `install.sh:3` (remote code execution)
3. Binary download without integrity verification in `install.sh:82` (supply chain attack)

**Next steps**:
1. Label this issue `security-blocked`
2. File upstream issue in `rtk-ai/rtk` flagging Critical findings #1–#3 and High finding #4
3. Re-audit after upstream security fixes are merged and released
4. The 5 skill `name` bugs (BUG-1) and Medium/Low security fixes (SEC-FIX-3 through SEC-FIX-5) are ready to contribute once the security gate clears
