# NLPM Audit: centminmod/my-claude-code-setup
**Date**: 2026-04-19  |  **Artifacts**: 32  |  **Strategy**: batched
**NL Score**: 49/100
**Security**: BLOCKED
**Bugs**: 22  |  **Quality Issues**: 28  |  **Security Findings**: 7

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/anthropic/update-memory-bank.md | command | 15 | One-line file, no frontmatter, no structure |
| commands/refactor/refactor-code.md | command | 20 | No frontmatter, massive vague-word density |
| commands/anthropic/convert-to-todowrite-tasklist-prompt.md | command | 23 | No frontmatter, no empty-input handling |
| commands/cleanup/cleanup-context.md | command | 23 | No frontmatter, heavy vague language |
| commands/anthropic/apply-thinking-to.md | command | 25 | No frontmatter, vague quantifiers capped |
| commands/security/check-best-practices.md | command | 25 | No frontmatter, no empty-input handling |
| commands/security/security-audit.md | command | 25 | No frontmatter, no empty-input handling |
| commands/architecture/explain-architecture-pattern.md | command | 27 | No frontmatter, no empty-input handling |
| commands/promptengineering/batch-operations-prompt.md | command | 27 | No frontmatter, no empty-input handling |
| commands/promptengineering/convert-to-test-driven-prompt.md | command | 27 | No frontmatter, no empty-input handling |
| commands/documentation/create-readme-section.md | command | 27 | No frontmatter, no empty-input handling |
| commands/ccusage/ccusage-daily.md | command | 29 | No frontmatter, no empty-input handling |
| commands/security/test-examples/test-basic-role-override.md | command | 35 | No frontmatter (test fixture file) |
| commands/security/test-examples/test-invisible-chars.md | command | 35 | No frontmatter (test fixture file) |
| commands/security/test-examples/test-advanced-injection.md | command | 35 | No frontmatter (test fixture file) |
| commands/security/test-examples/test-encoding-attacks.md | command | 35 | No frontmatter (test fixture file) |
| commands/security/test-examples/test-authority-claims.md | command | 35 | No frontmatter (test fixture file) |
| commands/security/test-examples/test-css-hiding.md | command | 35 | No frontmatter (test fixture file) |
| commands/security/secure-prompts.md | command | 35 | No frontmatter, no empty-input handling |
| commands/documentation/create-release-note.md | command | 39 | No frontmatter; otherwise well-structured |
| CLAUDE.md | config | 40 | No frontmatter name/description; vague terms |
| agents/codex-cli.md | agent | 73 | No examples, no output format |
| agents/zai-cli.md | agent | 73 | No examples, no output format |
| agents/get-current-datetime.md | agent | 74 | No model, no examples, 2 unused tools |
| agents/memory-bank-synchronizer.md | agent | 85 | No model declared |
| agents/ux-design-expert.md | agent | 87 | No model declared |
| skills/consult-codex/SKILL.md | skill | 89 | No structured examples block |
| skills/consult-zai/SKILL.md | skill | 89 | No structured examples block |
| agents/code-searcher.md | agent | 90 | Minor vague quantifiers |
| skills/ai-image-creator/SKILL.md | skill | 92 | Minor vague quantifiers |
| skills/claude-docs-consultant/SKILL.md | skill | 94 | Minimal issues |
| skills/session-metrics/SKILL.md | skill | 96 | Best-in-class documentation |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 |
| Medium | 3 |
| Low | 2 |

> Pre-scan detected 3 critical pattern matches (`bash -i -c` occurrences). Manual review downgrades these to HIGH: the pattern is intentional CLI-proxy design, not a backdoor, but the unvalidated user-prompt substitution into shell strings is a genuine injection surface.

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Python scripts | 3 (`skills/ai-image-creator/scripts/generate-image.py`, `skills/ai-image-creator/scripts/composite-banners.py`, `skills/session-metrics/scripts/session-metrics.py`) |
| Test scripts | 1 (`skills/session-metrics/tests/test_session_metrics.py`) |
| Vendor JS | 6 (Highcharts v12, Chart.js v4, uPlot v1 — read-only rendering libraries) |
| MCP configs | 0 |
| Package manifests | 0 |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH | `.claude/agents/codex-cli.md` | 24–34 | Shell injection via user prompt | `codex -p readonly exec "USER_PROMPT" --json` and `zsh/bash -i -c "codex … 'USER_PROMPT' …"` substitutes raw user input directly into a shell command string. A prompt containing `"` or `'` breaks quoting; crafted input can inject arbitrary shell commands. |
| 2 | HIGH | `.claude/agents/zai-cli.md` | 33–39 | Shell injection via user prompt | `bash -i -c "zai -p 'USER_PROMPT' …"` places user input inside single-quoted shell argument. A prompt containing `'` terminates the quote and allows arbitrary command injection. |
| 3 | MEDIUM | `.claude/skills/ai-image-creator/scripts/generate-image.py` | 83–109 | Credential loading from .env | `_load_dotenv()` reads API keys (`AI_IMG_CREATOR_CF_TOKEN`, `AI_IMG_CREATOR_OPENROUTER_KEY`, `AI_IMG_CREATOR_GEMINI_KEY`) from plaintext `.env` files on disk. Keys are never written to log or stored outside env/file, but loading from a predictable CWD path is a risk if the project dir is world-readable. |
| 4 | MEDIUM | `.claude/skills/ai-image-creator/scripts/generate-image.py` | 585 | External network call with credentials | `urllib.request.urlopen` transmits API credentials in HTTP headers to OpenRouter, Google AI Studio, and Cloudflare AI Gateway. Intended functionality, but represents a credential-to-network surface that should be validated against expected endpoints. |
| 5 | MEDIUM | `.claude/skills/ai-image-creator/scripts/generate-image.py` | 867, 882 | subprocess execution with external tools | `subprocess.run(["ffmpeg", …])` and `subprocess.run([magick_cmd, …])` call external binaries. Arguments are constructed from validated string constants (no user input reaches these calls), but the dependency on system-installed `ffmpeg`/`imagemagick` is an implicit trusted-binary assumption. |
| 6 | LOW | `.claude/skills/ai-image-creator/scripts/generate-image.py` | 813–884 | subprocess.run (safe form) | Multiple `subprocess.run` calls use list-form arguments (no `shell=True`). No injection risk; flagged for completeness only. |
| 7 | LOW | `.claude/skills/session-metrics/scripts/vendor/` | — | Vendored JS without integrity verification | Highcharts v12, Chart.js v4, and uPlot v1 are vendored as full JS files. No subresource integrity (`sri`) hash or checksum is verified at load time. Risk: tampered vendor file would execute in generated HTML reports. SKILL.md notes SHA-256 verification exists for Highcharts (`vendored, SHA-256-verified`); verify the implementation enforces this. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | All 20 `commands/**/*.md` files | Missing YAML frontmatter (`name`, `description`) | Commands cannot be registered by Claude Code; `name` and `description` fields are required for slash-command registration and discovery |
| 2 | `agents/codex-cli.md` | No `<example>` blocks in agent definition | Agents without examples produce inconsistent invocation behavior; Claude Code cannot surface usage hints |
| 3 | `agents/zai-cli.md` | No `<example>` blocks in agent definition | Same as above |
| 4 | `agents/get-current-datetime.md` | `Read` and `Write` declared in `tools:` but never referenced in body | Unnecessary permissions granted; remove unused tool declarations to follow least-privilege |
| 5 | `agents/memory-bank-synchronizer.md` | No `model:` field | Agent will inherit caller's model instead of being intentionally routed; risk of cost/capability mismatch |
| 6 | `agents/ux-design-expert.md` | No `model:` field | Same as above; large context/output agent should declare `model: sonnet` or higher |
| 7 | `agents/get-current-datetime.md` | No `model:` field | Trivial agent should declare `model: haiku` to minimize cost |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `skills/ai-image-creator/scripts/generate-image.py` | .env loading reads from CWD — predictable path | Restrict `.env` search to the skill directory only (remove `Path.cwd() / ".env"` candidate) or document that CWD `.env` is intentional and add a warning comment |
| 2 | `skills/session-metrics/scripts/vendor/` | Vendored JS files lack verified integrity check at runtime | Confirm the SKILL.md claim of "SHA-256-verified" is enforced in code; add a docstring or comment in the HTML generation showing the expected hash |

> **Critical/High findings** (shell injection in codex-cli and zai-cli agents) require private disclosure to the repo owner — do not open public PRs for these.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `agents/codex-cli.md` | No output format section — agent returns raw CLI output without schema | -10 |
| 2 | `agents/zai-cli.md` | No output format section | -10 |
| 3 | `agents/get-current-datetime.md` | No examples block | -15 |
| 4 | `agents/codex-cli.md` | No examples block | -15 |
| 5 | `agents/zai-cli.md` | No examples block | -15 |
| 6 | `commands/refactor/refactor-code.md` | Dense vague-word count (10+ instances: "appropriate", "specific", "key", "major", "comprehensive", "significant", "important", "relevant", "various", "suitable") | -20 (capped) |
| 7 | `commands/cleanup/cleanup-context.md` | High vague-word density (8 instances) | -16 |
| 8 | `commands/anthropic/apply-thinking-to.md` | High vague-word density (8 instances) | -16 |
| 9 | `commands/anthropic/convert-to-todowrite-tasklist-prompt.md` | Moderate vague language (6 instances: "appropriate", "specific", "targeted", "critical", "comprehensive", "relevant") | -12 |
| 10 | `commands/security/check-best-practices.md` | Moderate vague language (5 instances) | -10 |
| 11 | `commands/security/security-audit.md` | Moderate vague language (5 instances) | -10 |
| 12 | `agents/code-searcher.md` | Moderate vague language (5 instances across large body) | -10 |
| 13 | `agents/memory-bank-synchronizer.md` | Moderate vague language (5 instances: "important", "relevant", "valuable", "essential", "comprehensive") | -10 |
| 14 | `commands/anthropic/update-memory-bank.md` | No numbered steps, no output format — single ambiguous line | -20 |
| 15 | 10 command files missing empty-input handling | No `$ARGUMENTS` guard; if invoked without arguments behavior is undefined (`apply-thinking-to`, `batch-operations-prompt`, `convert-to-test-driven-prompt`, `create-readme-section`, `cleanup-context`, `check-best-practices`, `security-audit`, `explain-architecture-pattern`, `ccusage-daily`, `secure-prompts`) | -10 each |
| 16 | `skills/consult-codex/SKILL.md` | No structured `<example>` block | -5 |
| 17 | `skills/consult-zai/SKILL.md` | No structured `<example>` block | -5 |
| 18 | `agents/ux-design-expert.md` | Minor vague language (4 instances: "relevant", "important", "comprehensive", "proper") | -8 |
| 19 | `CLAUDE.md` | Lists several commands (`❌ find`, `❌ grep -r`) with no explanation of why they're banned — rationale is implied, not stated | informational |
| 20 | `commands/security/secure-prompts.md` | Uses fake cryptographic claims (`cryptographic_hash`, `identity_signature`, `SHA-256 of core directives`) that cannot be verified at LLM runtime — security theater in output schema | informational |

## Cross-Component
**Consistent references:** `consult-codex/SKILL.md` correctly delegates to `codex-cli` agent; `consult-zai/SKILL.md` correctly delegates to `zai-cli` agent; `CLAUDE.md` correctly references `claude-docs-consultant` skill. Reference graph is coherent.

**Orphaned reference:** `commands/cleanup/cleanup-context.md` instructs Claude to use `TodoWrite` (line: `TodoWrite with optimization phases`) but does not declare it in any `allowed-tools` field (no frontmatter at all). This is both a bug and a quality issue.

**Contradiction:** `agents/get-current-datetime.md` declares `tools: Bash, Read, Write` but the body only ever runs a single `TZ='Australia/Brisbane' date` command. `Read` and `Write` are never mentioned in the instructions, creating a permission surface wider than necessary.

**Security test fixtures in commands path:** The six `commands/security/test-examples/` files contain intentional prompt injection payloads (Base64 payloads, invisible unicode, CSS hiding, authority impersonation). These are legitimate test data files used by `secure-prompts.md` but their placement under `.claude/commands/` means they are discoverable as slash commands (e.g. `/test-basic-role-override`). Consider moving them to a non-commands path (e.g. `.claude/skills/security/test-fixtures/`) to prevent accidental invocation.

**Design gap in CLI proxy agents:** Both `codex-cli` and `zai-cli` agents are intentional CLI passthrough proxies — there is no malicious intent. However, neither agent documents the required prerequisite (the external CLI must be installed and in PATH) nor includes fallback behavior when the CLI is absent. Adding a `## Prerequisites` section would improve robustness.

## Recommendation

**BLOCKED — do not submit PRs. File private security report.**

Two HIGH-severity shell injection findings exist in `agents/codex-cli.md` and `agents/zai-cli.md`: user prompts are substituted directly into unquoted shell command strings, allowing crafted inputs containing `'` or `"` to inject arbitrary shell commands in the user's local environment. While this is inherent to the CLI proxy design pattern and affects only the local user, it must be disclosed privately so the maintainer can decide whether to add input sanitization (e.g. `shlex.quote`) or document the risk explicitly.

Once the maintainer has reviewed the security report, the following NL fix PRs would be appropriate:
1. Add YAML frontmatter (`name`, `description`) to all 20 command files — highest-impact single change (fixes 40 bug points across the repo).
2. Add `model:` declarations to the three agents missing it.
3. Remove unused `Read` and `Write` tools from `get-current-datetime.md`.
4. Add `<example>` blocks to `codex-cli.md` and `zai-cli.md`.
5. Relocate `commands/security/test-examples/` out of the commands path.
