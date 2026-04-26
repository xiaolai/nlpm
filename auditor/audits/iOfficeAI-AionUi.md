# NLPM Audit: iOfficeAI/AionUi

**Date**: 2026-04-26  |  **Artifacts**: 39  |  **Strategy**: batched
**NL Score**: 79/100
**Bugs**: 13  |  **Quality Issues**: 14

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `examples/hello-world-extension/agents/hello-researcher-context.md` | agent | 20 | No frontmatter, no model, no examples, no output format |
| `examples/hello-world-extension/agents/hello-coder-context.md` | agent | 20 | No frontmatter, no model, no examples, no output format |
| `.claude/commands/package-assistant.md` | command | 35 | No frontmatter, no allowed-tools, no empty input handling |
| `CLAUDE.md` | project-config | 70 | Pointer-only file (`@AGENTS.md`); no standalone content |
| `src/process/resources/skills/officecli-docx/SKILL.md` | skill | 72 | Malformed frontmatter; version marker repeated as body section header 7× |
| `src/process/resources/skills/morph-ppt/SKILL.md` | skill | 78 | Terse description; vague "various" |
| `src/process/resources/skills/moltbook/SKILL.md` | skill | 78 | Non-standard frontmatter fields; credential handling guidance lacks precision |
| `src/process/resources/skills/officecli-financial-model/SKILL.md` | skill | 80 | Malformed frontmatter — YAML comment breaks AionUi parser |
| `src/process/resources/skills/officecli-data-dashboard/SKILL.md` | skill | 80 | Malformed frontmatter — YAML comment breaks AionUi parser |
| `src/process/resources/skills/officecli-pitch-deck/SKILL.md` | skill | 80 | Malformed frontmatter — YAML comment breaks AionUi parser |
| `src/process/resources/skills/officecli-pptx/SKILL.md` | skill | 80 | Malformed frontmatter — YAML comment breaks AionUi parser |
| `src/process/resources/skills/officecli-academic-paper/SKILL.md` | skill | 80 | Malformed frontmatter — YAML comment breaks AionUi parser |
| `src/process/resources/skills/officecli-xlsx/SKILL.md` | skill | 80 | Malformed frontmatter — YAML comment breaks AionUi parser |
| `src/process/resources/skills/x-recruiter/SKILL.md` | skill | 82 | Clean; references external Playwright scripts |
| `src/process/resources/skills/star-office-helper/SKILL.md` | skill | 82 | References star_office_doctor.sh / setup.sh; nohup background launch |
| `src/process/resources/skills/xiaohongshu-recruiter/SKILL.md` | skill | 82 | Clean; Playwright automation dependency |
| `src/process/resources/skills/story-roleplay/SKILL.md` | skill | 82 | Clean; references parse-character-card.js |
| `src/process/resources/skills/aionui-webui-setup/SKILL.md` | skill | 84 | Clean |
| `src/process/resources/skills/openclaw-setup/SKILL.md` | skill | 84 | Clean; references multiple bundled reference files |
| `src/process/resources/skills/morph-ppt-3d/SKILL.md` | skill | 84 | Clean |
| `src/process/resources/skills/pdf/SKILL.md` | skill | 84 | Clean |
| `src/process/resources/skills/_builtin/aionui-skills/SKILL.md` | skill | 85 | Network fetch to external URL in install instructions |
| `src/process/resources/skills/_builtin/office-cli/SKILL.md` | skill | 85 | CRITICAL security: curl\|bash and irm\|iex in install instructions |
| `.claude/skills/pr-ship/SKILL.md` | skill | 85 | Clean |
| `.claude/skills/pr-fix/SKILL.md` | skill | 85 | Clean |
| `.claude/skills/fix-issues/SKILL.md` | skill | 85 | Clean |
| `.claude/skills/fix-sentry/SKILL.md` | skill | 85 | Clean |
| `.claude/skills/pr-automation/SKILL.md` | skill | 85 | Clean |
| `.claude/skills/pr-verify/SKILL.md` | skill | 87 | Hardcoded `/tmp/aionui-verify-*` path prefix |
| `src/process/resources/skills/_builtin/skill-creator/SKILL.md` | skill | 88 | Vague: "appropriate" ×2 |
| `.claude/skills/pr-review/SKILL.md` | skill | 88 | Clean |
| `.claude/skills/architecture/SKILL.md` | skill | 88 | Clean |
| `.claude/skills/bump-version/SKILL.md` | skill | 88 | Clean |
| `.claude/skills/i18n/SKILL.md` | skill | 88 | Clean |
| `.claude/skills/oss-pr/SKILL.md` | skill | 88 | Clean |
| `.claude/skills/testing/SKILL.md` | skill | 88 | Clean |
| `src/process/resources/skills/_builtin/cron/SKILL.md` | skill | 90 | Clean protocol spec |
| `src/process/resources/skills/mermaid/SKILL.md` | skill | 90 | Clean |
| `src/process/resources/skills/weixin-file-send/SKILL.md` | skill | 92 | Clean protocol spec |

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `examples/hello-world-extension/agents/hello-researcher-context.md` | No YAML frontmatter — `name` and `description` absent | Agent unknown to Claude Code; -50 pts |
| 2 | `examples/hello-world-extension/agents/hello-coder-context.md` | No YAML frontmatter — `name` and `description` absent | Agent unknown to Claude Code; -50 pts |
| 3 | `.claude/commands/package-assistant.md` | No YAML frontmatter — `name` and `description` absent | Command metadata invisible; -50 pts |
| 4 | `src/process/resources/skills/officecli-financial-model/SKILL.md` | `# officecli: v1.0.24` as first line inside `---` block; AionUi's regex YAML parser drops the skill | Skill never appears in Skills Center |
| 5 | `src/process/resources/skills/officecli-data-dashboard/SKILL.md` | Same YAML comment bug | Same |
| 6 | `src/process/resources/skills/officecli-pitch-deck/SKILL.md` | Same YAML comment bug | Same |
| 7 | `src/process/resources/skills/officecli-pptx/SKILL.md` | Same YAML comment bug (`# officecli: v1.0.23`) | Same |
| 8 | `src/process/resources/skills/officecli-academic-paper/SKILL.md` | Same YAML comment bug | Same |
| 9 | `src/process/resources/skills/officecli-xlsx/SKILL.md` | Same YAML comment bug | Same |
| 10 | `src/process/resources/skills/officecli-docx/SKILL.md` | YAML comment bug AND the string `# officecli: v1.0.23` is repeated 7× in the body as section separators | Parser failure + cluttered body |
| 11 | `.claude/commands/package-assistant.md` | No `allowed-tools` declaration | Claude selects tools unconstrained; -5 pts |
| 12 | `.claude/commands/package-assistant.md` | No empty-`$ARGUMENTS` guard; command silently proceeds with no input | Undefined behavior on empty invocation; -10 pts |
| 13 | `.claude/commands/package-assistant.md` | Hardcoded local path `/Users/veryliu/Documents/GitHub/officecli/` | Command broken on all non-author machines |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `hello-researcher-context.md` | No model declaration | -5 |
| 2 | `hello-researcher-context.md` | Zero example interaction blocks | -15 |
| 3 | `hello-researcher-context.md` | No output format section | -10 |
| 4 | `hello-coder-context.md` | No model declaration | -5 |
| 5 | `hello-coder-context.md` | Zero example interaction blocks | -15 |
| 6 | `hello-coder-context.md` | No output format section | -10 |
| 7 | `src/process/resources/skills/_builtin/skill-creator/SKILL.md` | "appropriate" appears twice as vague qualifier | -4 |
| 8 | `src/process/resources/skills/morph-ppt/SKILL.md` | Description is a single terse sentence; "various" used once | -2 |
| 9 | `src/process/resources/skills/officecli-docx/SKILL.md` | "properly", "correctly" each appear once | -4 |
| 10 | `src/process/resources/skills/officecli-pptx/SKILL.md` | "properly", "various" appear once each | -4 |
| 11 | `src/process/resources/skills/officecli-financial-model/SKILL.md` | "properly", "various" appear once each | -4 |
| 12 | `src/process/resources/skills/officecli-data-dashboard/SKILL.md` | "properly", "various" appear once each | -4 |
| 13 | `src/process/resources/skills/moltbook/SKILL.md` | Non-standard frontmatter fields (`version`, `homepage`, `metadata`) with no schema | informational |
| 14 | `.claude/skills/pr-verify/SKILL.md` | Worktree path `/tmp/aionui-verify-<PR_NUMBER>` is hardcoded; not configurable via env | informational |

## Cross-Component

**Hardcoded developer path in command:**
`.claude/commands/package-assistant.md` references `/Users/veryliu/Documents/GitHub/officecli/` as the source directory for packaging OfficeCLI skills. This is a developer-local absolute path that will fail silently on every other machine. The command also documents the frontmatter YAML comment bug in OfficeCLI skills, suggesting awareness of the issue without providing a fix path — creating inconsistency between the documented bug and the 7 skill files that still carry it.

**OfficeCLI version coupling:**
All 7 `officecli-*` skills track their version via `# officecli: vX.X.X` comments in frontmatter rather than a `version:` YAML field. This pattern is mentioned in `package-assistant.md` as a known parser issue, yet the skills remain unpatched. The mismatch between the documented fix and the actual file state represents a maintenance drift risk.

**Missing `hello-world-extension` wiring:**
Both agent context files under `examples/hello-world-extension/agents/` lack frontmatter entirely. This suggests the example extension was not updated when the frontmatter convention was adopted, potentially misleading contributors who use the example as a template.

## Security

**Status: BLOCKED — CRITICAL patterns found**

Security scan covered: 18 script files (`scripts/*.{sh,js}`), all NL skill instruction files. No `.mcp.json` found. No `requirements.txt` found.

| Severity | Pattern | Location | Count |
|----------|---------|----------|-------|
| CRITICAL | `curl -fsSL … \| bash` | `office-cli/SKILL.md` + 7 OfficeCLI skill files | 8 occurrences |
| HIGH | `irm … \| iex` (PowerShell) | `_builtin/office-cli/SKILL.md` | 1 occurrence |
| MEDIUM | `curl -s … >` to local config path | `_builtin/aionui-skills/SKILL.md` | 1 occurrence |
| LOW | `--dangerously-skip-permissions` in Claude invocations | `scripts/pr-automation.sh`, `fix-sentry-daemon.sh`, `fix-issues-daemon.sh` | 3 occurrences |

**CRITICAL detail:** Every OfficeCLI skill instructs Claude to run:
```
curl -fsSL https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.sh | bash
```
When a user invokes any `officecli-*` skill, Claude will execute this command on the user's machine without further prompting. The remote script is not pinned to a commit hash — a compromise of the `iOfficeAI/OfficeCLI` repository or a CDN interception would result in arbitrary code execution.

**Daemon scripts:** `--dangerously-skip-permissions` is intentional in the PR automation and bug-fix daemons (they run in a CI-equivalent context). This is architectural, not a vulnerability, but it means any prompt injection in a PR body or Sentry issue could trigger unrestricted tool use.

**Script files:** The 18 shell/JS scripts in `scripts/` are legitimate build and release tooling. `install-ubuntu.sh` documents that it is itself distributed via `curl | bash` in its header comment, but the script body only downloads a `.deb` file — it does not pipe shell output.

**Recommendation:** Pin the OfficeCLI install URL to a specific commit SHA or a content-addressed artifact. Replace the bare `curl | bash` pattern in skill instructions with a checksum-verified download step. The HIGH `irm | iex` pattern carries the same risk on Windows.

## Recommendation

The `.claude/skills/` PR-workflow suite (12 skills) is well-crafted and production-ready (85–92/100), but the repository ships with two unfixable-as-is example agents and a command that are missing all frontmatter, and 7 OfficeCLI skills that silently fail to register in AionUi's Skills Center due to a one-line YAML comment bug — fixing those 10 files would lift the overall score from 79 to approximately 87 without any other changes; the CRITICAL curl-pipe-bash pattern in skill instructions requires separate remediation before the repo can be considered contribution-safe.
