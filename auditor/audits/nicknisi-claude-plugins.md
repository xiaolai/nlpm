---
target: nicknisi/claude-plugins
date: 2026-04-06
artifacts: 60
strategy: batched
nl_score: 90
security_status: CLEAR
bugs: 8
quality_issues: 23
security_findings: 6
---

# Audit: nicknisi/claude-plugins

**Target:** https://github.com/nicknisi/claude-plugins
**Date:** 2026-04-06
**Artifacts scored:** 60
**NL Score:** 90/100
**Security:** CLEAR
**Bugs:** 8 · **Quality issues:** 23 · **Security findings:** 6

---

## NL Score Summary

Sorted ascending by score. Score = 100 − Σ penalties; floor 0.

| Score | File | Type | Penalties applied |
|------:|------|------|-------------------|
| 35 | plugins/spec-driven/commands/check-prp.md | command | BUG-missing-frontmatter: no name −25, no description −25, no examples −15 |
| 35 | plugins/spec-driven/commands/check-spec.md | command | BUG-missing-frontmatter: no name −25, no description −25, no examples −15 |
| 35 | plugins/spec-driven/commands/execute-prp.md | command | BUG-missing-frontmatter: no name −25, no description −25, no examples −15 |
| 35 | plugins/spec-driven/commands/execute-spec.md | command | BUG-missing-frontmatter: no name −25, no description −25, no examples −15 |
| 35 | plugins/spec-driven/commands/generate-prp.md | command | BUG-missing-frontmatter: no name −25, no description −25, no examples −15 |
| 35 | plugins/spec-driven/commands/generate-spec.md | command | BUG-missing-frontmatter: no name −25, no description −25, no examples −15 |
| 66 | plugins/developer-experience/agents/security-agent.md | agent | R05 −5 (no model), R07 −15 (zero examples), R09 −10 (no output format), R11 −4 ("proper" ×2) |
| 75 | plugins/developer-experience/agents/typescript-pro.md | agent | R07 −15 (zero examples), R09 −10 (output format is quality criteria not format spec) |
| 78 | plugins/essentials/agents/git-committer.md | agent | R05 −5 (no model), R07 −15 (commit templates ≠ user/assistant examples), R11 −2 ("appropriate") |
| 84 | plugins/developer-experience/agents/dx-sdk-advocate.md | agent | R09 −10 (no output format), BUG-undeclared-tool −3 (BashOutput), BUG-undeclared-tool −3 (KillBash) |
| 85 | plugins/consultant/agents/claude-researcher.md | agent | R07 −15 (zero examples) |
| 85 | plugins/consultant/agents/codex-researcher.md | agent | R07 −15 (zero examples) |
| 85 | plugins/consultant/agents/gemini-researcher.md | agent | R07 −15 (zero examples) |
| 85 | plugins/consultant/agents/grok-researcher.md | agent | R07 −15 (zero examples) |
| 85 | plugins/consultant/agents/perplexity-researcher.md | agent | R07 −15 (zero examples) |
| 85 | plugins/consultant/agents/researcher.md | agent | R07 −15 (zero examples) |
| 85 | plugins/developer-experience/agents/dx-optimizer.md | agent | R07 −15 (zero examples) |
| 90 | plugins/essentials/skills/ultrathink/SKILL.md | skill | R09 −10 (no output format; mode-setting skill) |
| 90 | plugins/sandbox/agents/cunningham.md | agent | R09 −10 (no output format section) |
| 95 | plugins/developer-experience/agents/coder.md | agent | R05 −5 (no model declared) |
| 95 | plugins/developer-experience/agents/readme-writer.md | agent | R05 −5 (no model declared) |
| 95 | plugins/essentials/agents/thermo-nuclear-code-quality-review.md | agent | R09 −5 (output format deferred to loaded skill; partial credit) |
| 100 | CLAUDE.md | meta | — |
| 100 | plugins/consultant/.claude-plugin/plugin.json | meta | — |
| 100 | plugins/consultant/skills/consult/SKILL.md | skill | — |
| 100 | plugins/consultant/skills/deliberate/SKILL.md | skill | — |
| 100 | plugins/consultant/skills/research/SKILL.md | skill | — |
| 100 | plugins/content/.claude-plugin/plugin.json | meta | — |
| 100 | plugins/content/skills/blog-post-writer/SKILL.md | skill | — |
| 100 | plugins/content/skills/conference-talk-builder/SKILL.md | skill | — |
| 100 | plugins/content/skills/tighten-prose/SKILL.md | skill | — |
| 100 | plugins/developer-experience/.claude-plugin/plugin.json | meta | — |
| 100 | plugins/essentials/.claude-plugin/plugin.json | meta | — |
| 100 | plugins/essentials/agents/code-simplifier.md | agent | — |
| 100 | plugins/essentials/agents/security-auditor.md | agent | — |
| 100 | plugins/essentials/skills/codebase-rehab/SKILL.md | skill | — |
| 100 | plugins/essentials/skills/codebase-sweep/SKILL.md | skill | — |
| 100 | plugins/essentials/skills/de-slopify/SKILL.md | skill | — |
| 100 | plugins/essentials/skills/handoff/SKILL.md | skill | — |
| 100 | plugins/essentials/skills/link-reader/SKILL.md | skill | — |
| 100 | plugins/essentials/skills/pr/SKILL.md | skill | — |
| 100 | plugins/essentials/skills/prototype/SKILL.md | skill | — |
| 100 | plugins/essentials/skills/security-audit/SKILL.md | skill | — |
| 100 | plugins/essentials/skills/socratic-tutor/SKILL.md | skill | — |
| 100 | plugins/essentials/skills/squad-review/SKILL.md | skill | — |
| 100 | plugins/essentials/skills/thermo-nuclear-code-quality-review/SKILL.md | skill | — |
| 100 | plugins/essentials/skills/zoom-out/SKILL.md | skill | — |
| 100 | plugins/image-gen/.claude-plugin/plugin.json | meta | — |
| 100 | plugins/image-gen/skills/image-gen/SKILL.md | skill | — |
| 100 | plugins/meta/.claude-plugin/plugin.json | meta | — |
| 100 | plugins/meta/skills/autoskill/SKILL.md | skill | — |
| 100 | plugins/meta/skills/claude-code-analyzer/SKILL.md | skill | — |
| 100 | plugins/sandbox/.claude-plugin/plugin.json | meta | — |
| 100 | plugins/sidequest/.claude-plugin/plugin.json | meta | — |
| 100 | plugins/sidequest/commands/capture.md | command | — |
| 100 | plugins/sidequest/commands/execute.md | command | — |
| 100 | plugins/spec-driven/.claude-plugin/plugin.json | meta | — |
| 100 | plugins/tmux/.claude-plugin/plugin.json | meta | — |
| 100 | plugins/tmux/hooks/hooks.json | hook | — |
| 100 | plugins/tmux/skills/tmux/SKILL.md | skill | — |

**Mean:** 5373 / 60 = 89.55 → **90/100**

---

## Security Scan

### Execution Surface Inventory

| Surface type | Count | Paths |
|--------------|------:|-------|
| Hook scripts | 1 | plugins/tmux/hooks/tmux-awareness.sh |
| Shell scripts | 7 | plugins/tmux/scripts/{find-panes,run-in-pane,wait-for-text,safe-send,find-sessions}.sh; plugins/meta/skills/claude-code-analyzer/scripts/{fetch-features,github-discovery}.sh |
| MCP configs | 2 | plugins/consultant/.mcp.json; plugins/sidequest/.mcp.json |
| MCP server (compiled) | 1 | plugins/consultant/mcp-server/dist/index.js |
| Package manifests | 2 | package.json; plugins/consultant/mcp-server/package.json |

### Security Gate Result: **CLEAR**

No CRITICAL or HIGH patterns found. No `eval`-with-variable-expansion, no curl-pipe-sh, no credential exfiltration, no reverse-shell constructs. The tmux hook script correctly exits silently when `$TMUX` is unset, limiting blast radius to tmux-active sessions only.

### Security Findings

| Severity | File | Line | Pattern | Evidence |
|----------|------|-----:|---------|---------|
| MEDIUM | plugins/consultant/.mcp.json | 5 | unpinned-npx | `npx -y @perplexity-ai/mcp-server` — no version pin; supply-chain risk on every session start |
| MEDIUM | plugins/consultant/.mcp.json | 12 | unpinned-npx | `npx -y gemini-mcp-tool` — no version pin |
| MEDIUM | plugins/consultant/.mcp.json | 19 | unpinned-npx | `npx -y @chinchillaenterprises/mcp-grok` — no version pin; third-party org with low download counts |
| MEDIUM | plugins/sidequest/.mcp.json | 5 | unpinned-npx | `npx -y omnifocus-mcp-enhanced` — no version pin |
| LOW | plugins/meta/skills/claude-code-analyzer/scripts/fetch-features.sh | 3 | outbound-http | `curl -s -L "$CLAUDE_DOCS_URL"` — outbound HTTP to docs.claude.com; fails silently if network unavailable |
| LOW | plugins/meta/skills/claude-code-analyzer/scripts/github-discovery.sh | 1 | outbound-api | `gh search code` — outbound GitHub API call; rate-limit exposure if token absent |

---

## Bugs

Bugs are findings that prevent correct plugin registration or runtime execution.

| # | Rule | File | Line | Description | Suggested fix |
|---|------|------|-----:|-------------|---------------|
| 1 | BUG-missing-frontmatter | plugins/spec-driven/commands/check-prp.md | 1 | File starts with `# Check PRP` — no YAML frontmatter block; `name` and `description` missing; plugin system cannot register command | Add `---\nname: check-prp\ndescription: …\nallowed-tools: …\n---` before the H1 |
| 2 | BUG-missing-frontmatter | plugins/spec-driven/commands/check-spec.md | 1 | No YAML frontmatter; command unregisterable | Same fix pattern as #1 |
| 3 | BUG-missing-frontmatter | plugins/spec-driven/commands/execute-prp.md | 1 | No YAML frontmatter; command unregisterable | Same fix pattern as #1 |
| 4 | BUG-missing-frontmatter | plugins/spec-driven/commands/execute-spec.md | 1 | No YAML frontmatter; command unregisterable | Same fix pattern as #1 |
| 5 | BUG-missing-frontmatter | plugins/spec-driven/commands/generate-prp.md | 1 | No YAML frontmatter; command unregisterable | Same fix pattern as #1 |
| 6 | BUG-missing-frontmatter | plugins/spec-driven/commands/generate-spec.md | 1 | No YAML frontmatter; command unregisterable | Same fix pattern as #1 |
| 7 | BUG-undeclared-tool | plugins/developer-experience/agents/dx-sdk-advocate.md | 4 | `tools: [BashOutput, KillBash, …]` — `BashOutput` is not a standard Claude Code tool (standard set: Bash, Read, Write, Edit, MultiEdit, Glob, Grep, LS, WebFetch, WebSearch, Task, TodoWrite) | Replace `BashOutput` with `Bash` |
| 8 | BUG-undeclared-tool | plugins/developer-experience/agents/dx-sdk-advocate.md | 4 | `KillBash` is not a standard Claude Code tool | Remove `KillBash`; Bash tool covers process control |

---

## Security Fixes

Ordered by severity. CLEAR status is unaffected by these fixes; they are advisory.

| Severity | File | Fix |
|----------|------|-----|
| MEDIUM | plugins/consultant/.mcp.json | Pin `@perplexity-ai/mcp-server` to a specific version: `npx -y @perplexity-ai/mcp-server@<version>` |
| MEDIUM | plugins/consultant/.mcp.json | Pin `gemini-mcp-tool` to a specific version |
| MEDIUM | plugins/consultant/.mcp.json | Pin `@chinchillaenterprises/mcp-grok` to a specific version; audit org provenance |
| MEDIUM | plugins/sidequest/.mcp.json | Pin `omnifocus-mcp-enhanced` to a specific version |
| LOW | plugins/meta/skills/claude-code-analyzer/scripts/fetch-features.sh | Add `|| true` with fallback path; document the external dependency in the skill's SKILL.md |
| LOW | plugins/meta/skills/claude-code-analyzer/scripts/github-discovery.sh | Check for `gh` auth before running; gracefully degrade if unauthenticated |

---

## Quality Issues

Ordered by file then rule. Only deducting penalties listed here; files not listed scored 100.

| File | Rule | Penalty | Description | Suggested fix |
|------|------|--------:|-------------|---------------|
| plugins/developer-experience/agents/coder.md | R05 | −5 | No `model:` field in frontmatter | Add `model: claude-sonnet-4-6` (or appropriate tier) |
| plugins/developer-experience/agents/dx-optimizer.md | R07 | −15 | Zero user/assistant interaction examples | Add ≥2 `User:`/`Assistant:` examples covering core workflows |
| plugins/developer-experience/agents/dx-sdk-advocate.md | R09 | −10 | No output format section; agent describes capabilities but not response structure | Add `## Output Format` section specifying structure, length, and code-block conventions |
| plugins/developer-experience/agents/readme-writer.md | R05 | −5 | No `model:` field in frontmatter | Add `model:` declaration |
| plugins/developer-experience/agents/security-agent.md | R05 | −5 | No `model:` field in frontmatter | Add `model:` declaration |
| plugins/developer-experience/agents/security-agent.md | R07 | −15 | Zero user/assistant examples | Add ≥2 concrete interaction examples |
| plugins/developer-experience/agents/security-agent.md | R09 | −10 | No output format section | Add `## Output Format` with severity labels and finding structure |
| plugins/developer-experience/agents/security-agent.md | R11 | −2 | Vague quantifier: "proper" (occurrence 1) | Replace with specific requirement, e.g. "OWASP-compliant" |
| plugins/developer-experience/agents/security-agent.md | R11 | −2 | Vague quantifier: "proper" (occurrence 2) | Same as above |
| plugins/developer-experience/agents/typescript-pro.md | R07 | −15 | Zero user/assistant examples; "Output Standards" section lists quality criteria, not interaction examples | Add ≥2 `User:`/`Assistant:` pairs |
| plugins/developer-experience/agents/typescript-pro.md | R09 | −10 | "Output Standards" is a quality rubric, not an output format specification | Add `## Output Format` specifying response schema and length guidance |
| plugins/essentials/agents/git-committer.md | R05 | −5 | No `model:` field in frontmatter | Add `model:` declaration |
| plugins/essentials/agents/git-committer.md | R07 | −15 | "Example Commit Messages" are commit body templates, not user/assistant interaction examples | Add ≥2 examples showing user request → assistant response (with commit output) |
| plugins/essentials/agents/git-committer.md | R11 | −2 | Vague quantifier: "appropriate" in "Stage Appropriate Files" | Replace with explicit rule, e.g. "Stage files modified by this session" |
| plugins/essentials/agents/thermo-nuclear-code-quality-review.md | R09 | −5 | Output format delegated to skill via reference rather than specified inline; partial credit since skill is loaded | Document the output format inline or cite the skill section explicitly |
| plugins/consultant/agents/claude-researcher.md | R07 | −15 | Zero user/assistant examples | Add ≥2 interaction examples |
| plugins/consultant/agents/codex-researcher.md | R07 | −15 | Zero user/assistant examples | Add ≥2 interaction examples |
| plugins/consultant/agents/gemini-researcher.md | R07 | −15 | Zero user/assistant examples | Add ≥2 interaction examples |
| plugins/consultant/agents/grok-researcher.md | R07 | −15 | Zero user/assistant examples | Add ≥2 interaction examples |
| plugins/consultant/agents/perplexity-researcher.md | R07 | −15 | Zero user/assistant examples | Add ≥2 interaction examples |
| plugins/consultant/agents/researcher.md | R07 | −15 | Zero user/assistant examples | Add ≥2 interaction examples |
| plugins/essentials/skills/ultrathink/SKILL.md | R09 | −10 | Mode-setting skill has no output format section | Add brief `## Output Format` noting that this skill modifies reasoning depth, not response shape |
| plugins/sandbox/agents/cunningham.md | R09 | −10 | No output format section | Add `## Output Format` section |

---

## Cross-Component

### spec-driven: Systemic frontmatter omission (all 6 commands)

All six commands in the `spec-driven` plugin (`check-prp`, `check-spec`, `execute-prp`, `execute-spec`, `generate-prp`, `generate-spec`) start directly with an H1 heading — no `---` frontmatter block at all. This is a systemic omission, not a per-file oversight. The plugin.json correctly describes the plugin, but without frontmatter the commands cannot be registered by the Claude Code plugin system. All six must be fixed together.

Confidence: high (reproduced on direct read of each file).

### consultant: Researcher agents declare no tools

All six researcher agents (claude-researcher, codex-researcher, gemini-researcher, grok-researcher, perplexity-researcher, researcher) omit `tools:` from frontmatter. This appears intentional — the agents rely on whichever tools Claude Code grants by default — but it means the tool set is undeclared and may silently expand if defaults change. Advisory: if the researcher agents only need WebFetch/WebSearch, declaring `tools: [WebFetch, WebSearch]` would scope them explicitly and satisfy a future R-strict audit.

Confidence: medium (design intent inferred from consistency across all 6 agents; no documentation of the choice).

### essentials: prototype skill references bundled resources without path declarations

`plugins/essentials/skills/prototype/SKILL.md` references `LOGIC.md` and `UI.md` as companion files (both are present in the same directory). The SKILL.md does not declare these as dependencies or explain how they are loaded. If Claude Code's skill loader does not automatically co-load sibling files, the references will silently fail at runtime. Advisory: add an explicit note in the skill's SKILL.md explaining how to load the companion files, or consolidate into a single SKILL.md.

Confidence: low (exact skill-loader behavior for sibling files is unverified).

---

## Recommendation

**CLEAR — contribute PRs.**

Priority order:
1. **spec-driven bugs (all 6)**: Add YAML frontmatter to every command in the spec-driven plugin. This is the highest-impact fix: six commands are completely unregisterable. A single PR fixing all six is appropriate given the systemic nature of the omission.
2. **dx-sdk-advocate bugs (2)**: Replace `BashOutput` → `Bash` and remove `KillBash`. One-line frontmatter fix.
3. **Security MEDIUM (4)**: Pin all four `npx -y` MCP packages to explicit versions. Low-effort, meaningful supply-chain improvement.
4. **Quality — missing examples (10 agents)**: Add ≥2 user/assistant examples to each agent. The seven consultant researchers are the highest-volume opportunity; a single PR covering all seven would be efficient.
5. **Quality — missing model (4 agents)**: Add `model:` to coder, readme-writer, security-agent, git-committer.
6. **Quality — output format (5 artifacts)**: Add `## Output Format` sections to security-agent, typescript-pro, cunningham, ultrathink SKILL.md, dx-sdk-advocate.
