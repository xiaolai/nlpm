# NLPM Audit: gadievron/raptor
**Date**: 2026-04-13  |  **Artifacts**: 50  |  **Strategy**: batched
**NL Score**: 93/100
**Security**: BLOCKED
**Bugs**: 4  |  **Quality Issues**: 31  |  **Security Findings**: 5

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/commands/codeql.md | Command | 85 | Missing allowed-tools; no empty-input handling |
| .claude/commands/diagram.md | Command | 85 | Missing allowed-tools; no empty-input handling |
| .claude/commands/crash-analysis.md | Command | 85 | Missing allowed-tools; no empty-input handling |
| .claude/commands/oss-forensics.md | Command | 85 | Missing allowed-tools; no empty-input handling |
| .claude/commands/agentic.md | Command | 85 | Missing allowed-tools; no empty-input handling |
| .claude/commands/analyze.md | Command | 85 | Missing allowed-tools; no empty-input handling |
| .claude/commands/patch.md | Command | 85 | Missing allowed-tools; no empty-input handling |
| .claude/commands/validate.md | Command | 85 | Missing allowed-tools; no empty-input handling |
| .claude/agents/oss-hypothesis-checker-agent.md | Agent | 83 | Zero invocation examples (-15); vague "appropriate" (-2) |
| .claude/agents/oss-report-generator-agent.md | Agent | 85 | Zero invocation examples (-15) |
| .claude/agents/oss-investigator-ioc-extractor-agent.md | Agent | 85 | Zero invocation examples (-15) |
| .claude/agents/crash-analysis-agent.md | Agent | 85 | Zero invocation examples (-15) |
| .claude/agents/oss-investigator-gh-archive-agent.md | Agent | 85 | Zero invocation examples (-15) |
| .claude/agents/oss-investigator-github-agent.md | Agent | 85 | Zero invocation examples (-15) |
| .claude/agents/oss-investigator-wayback-agent.md | Agent | 85 | Zero invocation examples (-15) |
| .claude/agents/oss-evidence-verifier-agent.md | Agent | 85 | Zero invocation examples (-15) |
| .claude/agents/oss-investigator-local-git-agent.md | Agent | 85 | Zero invocation examples (-15) |
| .claude/commands/commands.md | Command | 95 | Missing allowed-tools |
| .claude/commands/test-workflows.md | Command | 95 | Missing allowed-tools |
| .claude/commands/project.md | Command | 95 | Missing allowed-tools |
| .claude/commands/understand.md | Command | 95 | Missing allowed-tools |
| .claude/commands/scan.md | Command | 95 | Missing allowed-tools (alias) |
| .claude/commands/create-skill.md | Command | 95 | Missing allowed-tools |
| .claude/commands/raptor-fuzz.md | Command | 95 | Missing allowed-tools |
| .claude/commands/raptor-scan.md | Command | 95 | Missing allowed-tools |
| .claude/commands/raptor.md | Command | 95 | Missing allowed-tools |
| .claude/commands/fuzz.md | Command | 95 | Missing allowed-tools (alias) |
| .claude/commands/web.md | Command | 95 | Missing allowed-tools (alias) |
| .claude/commands/exploit.md | Command | 95 | Missing allowed-tools |
| .claude/commands/raptor-web.md | Command | 95 | Missing allowed-tools |
| .claude/agents/coverage-analysis-generator-agent.md | Agent | 95 | One example only (-5); missing tools field |
| .claude/agents/function-trace-generator-agent.md | Agent | 95 | One example only (-5); missing tools field |
| .claude/agents/crash-analyzer-checker-agent.md | Agent | 95 | One example only (-5) |
| .claude/agents/crash-analyzer-agent.md | Agent | 95 | One example only (-5) |
| .claude/agents/oss-hypothesis-former-agent.md | Agent | 95 | One example only (-5) |
| .claude/agents/offsec-specialist.md | Agent | 96 | Broken skill path reference (BUG); vague "appropriate"/"relevant" (-4) |
| .claude/agents/oss-investigator-github-agent.md | Agent | 85 | Zero invocation examples (-15) |
| .claude/agents/exploitability-validator-agent.md | Agent | 100 | None |
| .claude/skills/crash-analysis/line-execution-checker/SKILL.md | Skill | 100 | None |
| .claude/skills/crash-analysis/rr-debugger/SKILL.md | Skill | 100 | None |
| .claude/skills/crash-analysis/function-tracing/SKILL.md | Skill | 100 | None |
| .claude/skills/crash-analysis/gcov-coverage/SKILL.md | Skill | 100 | None |
| .claude/skills/code-understanding/SKILL.md | Skill | 100 | None |
| .claude/skills/exploitability-validation/SKILL.md | Skill | 100 | None |
| .claude/skills/oss-forensics/github-wayback-recovery/SKILL.md | Skill | 100 | None |
| .claude/skills/oss-forensics/github-evidence-kit/SKILL.md | Skill | 100 | None |
| .claude/skills/oss-forensics/orchestration/SKILL.md | Skill | 100 | None |
| .claude/skills/oss-forensics/github-commit-recovery/SKILL.md | Skill | 100 | None |
| .claude/skills/oss-forensics/github-archive/SKILL.md | Skill | 100 | None |
| plugins/coverage/hooks/hooks.json | Config | 100 | None |
| CLAUDE.md | Config | 100 | None |

**Score breakdown**: Agents (16 files) avg 89.6 | Commands (21 files) avg 91.2 | Skills/Config (13 files) avg 100.0

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 1 |
| Medium | 2 |
| Low | 1 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks | 1 (`plugins/coverage/hooks/hooks.json`) |
| Python scripts | ~270 (packages/, libexec/, test/data/, core/) |
| Shell scripts | 7 (`test/*.sh`) |
| MCP configs | 0 |
| Package manifests | 1 (`requirements.txt`) |
| Container configs | 1 (`.devcontainer/Dockerfile`) |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | CRITICAL | `.devcontainer/Dockerfile` | 158 | curl pipe to shell | `curl -fsSL https://deb.nodesource.com/setup_20.x \| bash -` — downloads and executes arbitrary code from NodeSource without checksum or signature verification. If the NodeSource CDN or the TLS connection is compromised, attacker-controlled code executes as root inside the container build. |
| 2 | HIGH | `test/data/python_sql_injection.py` | 58 | subprocess shell=True with f-string | `subprocess.run(f"convert {filename} output.jpg", shell=True)` — intentional test fixture demonstrating command injection, but the file is live Python that could be executed. Filename comes directly from Flask request form data with no sanitization. |
| 3 | MEDIUM | `requirements.txt` | 5–6 | Unpinned upper bounds | `requests>=2.31.0` and `pydantic>=2.9.2` use `>=` without an upper bound. Future major versions with breaking changes or newly introduced vulnerabilities are automatically pulled in on fresh installs. |
| 4 | MEDIUM | `plugins/coverage/hooks/hooks.json` | 9 | Environment variable in hook command | Hook command is `${CLAUDE_PLUGIN_ROOT}/libexec/raptor-hook-read` — if `CLAUDE_PLUGIN_ROOT` is unset or tampered with prior to hook execution, the resolved binary path could point to attacker-controlled code. The hook runs on every Read tool use (PostToolUse, async). |
| 5 | LOW | `test/data/python_sql_injection.py` | 26 | Hardcoded credential in source | `DATABASE_PASSWORD = "admin123!SuperSecret"` — hardcoded credential committed to version control. This is intentional test data, but the credential is real-looking and may be flagged by secret-scanning tools, creating noise and potentially training bad habits. |

**Note on test/data/ files**: `python_sql_injection.py` and `javascript_xss.js` are intentional vulnerable fixtures for testing RAPTOR's detection capabilities. The HIGH finding at line 58 is real code that runs, not just a comment — it should be wrapped in a clearly non-executable form (e.g., string literal or doc-only) if it is never meant to be invoked.

**Note on Dockerfile**: `.devcontainer/` is a development environment file, not part of RAPTOR's operational runtime. The curl-pipe-bash pattern is common in dev container setups but represents a genuine supply-chain risk during contributor onboarding.

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `.claude/agents/offsec-specialist.md` | References skill path `.claude/skills/SecOpsAgentKit/skills/offsec/` which does not exist in the repository. The agent's Phase 1 workflow instructs it to list and load skills from this directory, which will always silently fail. | Agent operates without its intended skill toolkit; security testing methodology degrades to generic LLM knowledge |
| 2 | `CLAUDE.md` | Documents `oss-forensics-agent` as the main orchestrator for `/oss-forensics`, but no such agent file exists. The orchestration is done inline by the main Claude via the orchestration skill. | Documentation mismatch confuses contributors about the agent inventory |
| 3 | `CLAUDE.md` | Names `oss-investigator-gh-api-agent` and `oss-investigator-gh-recovery-agent` in the OSS Forensics agent list, but the actual files are `oss-investigator-github-agent.md` and `oss-investigator-wayback-agent.md` respectively. | Contributor navigation broken; any tooling that indexes agents by documented name will fail |
| 4 | `.claude/agents/coverage-analysis-generator-agent.md` and `function-trace-generator-agent.md` | Both agents have no `tools:` field in frontmatter. They require Bash to run compiler and coverage commands, but without declared tools the runtime default applies, which may not include Bash in all invocation contexts. | Agents may silently fail to execute build/instrumentation steps |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `requirements.txt` | Unpinned upper bounds on `requests` and `pydantic` allow uncontrolled version upgrades | Pin with compatible-release specifiers: `requests~=2.31`, `pydantic~=2.9` to allow patch updates but block major bumps |
| 2 | `plugins/coverage/hooks/hooks.json` | Hook binary path resolved via `${CLAUDE_PLUGIN_ROOT}` with no fallback guard | Add a wrapper script that validates `CLAUDE_PLUGIN_ROOT` is set and points within expected directory before exec; or hardcode relative path anchored to the plugin manifest |
| 3 | `test/data/python_sql_injection.py` | Hardcoded credential on line 26 committed to VCS | Replace with clearly fake sentinel: `DATABASE_PASSWORD = "INTENTIONALLY_VULNERABLE_PLACEHOLDER"` to suppress secret-scanner alerts |

**Critical/High findings require private disclosure, not public PRs.**

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | oss-hypothesis-checker-agent.md | No invocation example showing orchestrator calling the agent | -15 |
| 2 | oss-hypothesis-checker-agent.md | Vague quantifier: "appropriate given evidence strength" (line 57) | -2 |
| 3 | oss-report-generator-agent.md | No invocation example | -15 |
| 4 | oss-investigator-ioc-extractor-agent.md | No invocation example | -15 |
| 5 | crash-analysis-agent.md | No invocation example | -15 |
| 6 | oss-investigator-gh-archive-agent.md | No invocation example | -15 |
| 7 | oss-investigator-github-agent.md | No invocation example | -15 |
| 8 | oss-investigator-wayback-agent.md | No invocation example | -15 |
| 9 | oss-evidence-verifier-agent.md | No invocation example | -15 |
| 10 | oss-investigator-local-git-agent.md | No invocation example | -15 |
| 11 | offsec-specialist.md | Vague quantifiers: "appropriate authorization" (body line 27), "relevant skills" (Phase 1 step 1) | -4 total |
| 12 | coverage-analysis-generator-agent.md | Missing `tools:` field; agent needs at minimum Bash, Read, Write | -0 (not penalized by rule, but a quality gap) |
| 13 | function-trace-generator-agent.md | Missing `tools:` field; same issue | -0 |
| 14 | All 21 commands | No `allowed-tools` field in frontmatter — Claude Code commands should declare which tools they use | -5 each |
| 15 | codeql.md | No empty-input handling: if run with no `--repo`, the Python command fails with no guidance to user | -10 |
| 16 | diagram.md | No empty-input handling: if run with no `<out-dir>`, libexec script will error with no user guidance | -10 |
| 17 | crash-analysis.md | No empty-input handling: two required URLs with no handler for empty invocation | -10 |
| 18 | oss-forensics.md | No empty-input handling: `{rest of command arguments}` is empty string with no check or prompt | -10 |
| 19 | agentic.md | No empty-input handling: `python3 raptor.py agentic --repo <path>` requires path, not guarded | -10 |
| 20 | analyze.md | No empty-input handling: requires both `--repo` and `--sarif`, no guard | -10 |
| 21 | patch.md | No empty-input handling: requires SARIF from prior scan, no guard | -10 |
| 22 | validate.md | No empty-input handling: `<target_path>` required but no fallback or prompt if omitted | -10 |
| 23 | coverage-analysis-generator-agent.md | Only one internal example (validation section), no orchestrator-calling example | -5 |
| 24 | function-trace-generator-agent.md | Only one internal example (validation section), no orchestrator-calling example | -5 |
| 25 | crash-analyzer-checker-agent.md | Only one example (output template), no orchestrator-calling example | -5 |
| 26 | crash-analyzer-agent.md | Only one example (required format section), no orchestrator-calling example | -5 |
| 27 | oss-hypothesis-former-agent.md | Only one inline example (evidence-request template), no orchestrator-calling example | -5 |
| 28 | understand.md | No `allowed-tools` and multi-step workflow references libexec scripts (Bash) that aren't declared | -5 |
| 29 | raptor-web.md | Marked as "STUB" / alpha but presented as a primary command with no deprecation notice | Informational |
| 30 | commands.md | Instructs agent to "derive the list from the available skills" without specifying which Read paths to check | Informational |
| 31 | offsec-specialist.md | Model is `inherit` with no recommended tier note; this is a sensitive security-ops agent that benefits from the most capable model | Informational |

## Cross-Component

**Broken references:**
- `offsec-specialist.md` → `.claude/skills/SecOpsAgentKit/skills/offsec/` — directory does not exist. The rest of the skill tree is under `.claude/skills/{crash-analysis,code-understanding,exploitability-validation,oss-forensics}/`. The `SecOpsAgentKit` namespace is absent.
- `CLAUDE.md` → `oss-forensics-agent`, `oss-investigator-gh-api-agent`, `oss-investigator-gh-recovery-agent` — none of these agent names match actual files. Actual files: no `oss-forensics-agent.md`; `oss-investigator-github-agent.md`; `oss-investigator-wayback-agent.md`.

**Naming inconsistencies:**
- `crash-analysis-agent.md` step 11 refers to "crash-analysis-checker" agent; the file is `crash-analyzer-checker-agent.md` (with "analyzer" not "analysis"). Step 10 correctly says "crash-analyzer". Mixed naming across the orchestration description.
- `CLAUDE.md` describes the `/crash-analysis` workflow agents as `crash-analysis-checker-agent` but the filename is `crash-analyzer-checker-agent.md`.

**Orphaned components:**
- The `offsec-specialist.md` agent's entire skill loading infrastructure (Phase 1) references a non-existent skill directory, making its workflow non-functional as written. The body is otherwise well-structured and reachable through the `/scan` or direct agent dispatch, but the skills phase will always fail silently.

**Skill coverage gaps:**
- `crash-analysis-agent.md` orchestrates sub-agents but has no example of the full multi-agent workflow (traces → coverage → rr → analyzer → checker loop). Only the step list is present; showing a worked example would raise confidence.
- All OSS forensics investigator agents (`gh-archive`, `github`, `wayback`, `local-git`, `ioc-extractor`) lack invocation examples, making it hard to verify correct orchestrator prompting against the orchestration/SKILL.md template.

**Consistency win:**
- The exploitability validation pipeline is the best-documented component: `exploitability-validator-agent.md` has two complete worked examples, `exploitability-validation/SKILL.md` has gated execution rules, and validate.md has explicit stage-by-stage instructions. This is the reference model for the rest of the plugin.

## Recommendation

BLOCKED — do not submit PRs. File private security report.

**Reason**: One Critical security finding exists in `.devcontainer/Dockerfile` (curl piped to bash without integrity verification). Per policy, Critical findings require private disclosure before any public contribution activity. Additionally, the `test/data/python_sql_injection.py` HIGH finding (subprocess shell=True with user input) warrants private review to confirm it cannot be reached in any production invocation path.

**After private disclosure is resolved:**
- Submit NL fix PRs for the 4 documented bugs (broken skill path in offsec-specialist, CLAUDE.md agent name mismatches, missing tools fields on coverage/trace agents).
- Submit Medium/Low security fixes as listed above (pin requirements, harden hook path, replace hardcoded credential in test fixture).
- Quality improvements (adding invocation examples to 9 agents, adding allowed-tools to all 21 commands) can be batched into a single "NL quality" PR after security issues are closed.
