# Calibration Examples

Four worked examples anchoring the score bands defined in the main `nlpm:scoring` rubric. The scorer agent loads this file on demand when scoring borderline cases — it is *not* needed at every score call. Extracted from the main `SKILL.md` body 2026-05-28 to keep the rubric under R05's 500-line budget while preserving the calibration material.

For the formula, penalty tables, and score bands, see `../SKILL.md`.

---

## Example 1: Excellent Agent (95/100)

**Artifact:**
```markdown
---
name: dependency-auditor
description: |
  Audits project dependencies for security vulnerabilities, outdated packages,
  and license compliance issues. Use this agent when checking npm/pip/cargo
  dependencies, reviewing package.json or requirements.txt, or running a
  security audit before release.

  <example>
  Context: Developer preparing for production release
  user: check if any of our dependencies have known CVEs
  assistant: I'll audit your dependencies for security vulnerabilities using
  the package manifest files...
  </example>

  <example>
  Context: CI pipeline running pre-merge checks
  user: /audit-deps
  assistant: Running dependency audit. Scanning package.json and
  package-lock.json for vulnerabilities and license issues...
  </example>
model: sonnet
color: yellow
tools: ["Read", "Glob", "Bash"]
skills: ["nlpm:conventions"]
---

You are a dependency security auditor. Read all package manifests in the
project. For each dependency, check version ranges against known vulnerability
patterns. Report findings in the format below.

## Output Format
### Summary
Total dependencies: N | Vulnerable: N | Outdated: N | License issues: N

### Findings
| Package | Version | Issue | Severity |
|---------|---------|-------|----------|
```

**Score breakdown:**
- Base: 100. Passes: `description` with 3+ specific phrases, 2 `<example>` blocks, `model: sonnet` (analysis-tier), declared tools used, output format defined, read-only (no Write/Edit).
- Minor: `Bash` declared but body doesn't invoke it (one unused tool): **-3**

**Final: 97/100** — Excellent. The single unused-tool penalty costs 3 points; otherwise rubric-clean.

*(For calibration: a 95 example would have zero unused tools and a scope note. The range 90-100 is Excellent regardless of the exact number.)*

---

## Example 2: Rewrite Agent (41/100)

**Artifact:**
```markdown
---
name: code-helper
description: "Helps with code tasks in an appropriate and relevant way as needed."
model: opus
tools: ["Read", "Write", "Edit", "Bash", "Glob", "WebSearch", "WebFetch"]
---

You are a helpful coding assistant. Analyze the code and make appropriate
improvements. Handle edge cases as needed and ensure the output is relevant
to the user's requirements.
```

**Score breakdown:**
- Base: 100
- Zero `<example>` blocks: **-15**
- Description is generic (1 vague phrase, 0 specific phrases): **-15**
- `opus` declared for a routine code-help task (haiku/sonnet appropriate): **-5**
- `tools` declared but too many unused (WebSearch, WebFetch, Glob all declared without body justification): **-10** (judged as 3–4 unused, rounded)
- "appropriate" + "relevant" + "as needed" (vague quantifiers, 2 instances): **-4**
- No output format defined: **-10**

Total penalties: -59

**Final: max(0, 100 - 59) = 41/100** — Rewrite.

*(For calibration: the exact number of unused tools and vague quantifier hits can vary by reviewer. The important thing is that this artifact scores well below 60 — multiple fundamental issues.)*

---

## Example 3: Excellent Rule (92/100)

**Artifact:**
```markdown
---
description: "Always use ${CLAUDE_PLUGIN_ROOT} for intra-plugin file references in hooks and scripts"
paths: ["**/.claude/hooks.json", "**/scripts/*.sh"]
---

**Use `${CLAUDE_PLUGIN_ROOT}` for all file paths within a plugin.**

Because plugins are installed at different locations for different users and
environments, hardcoded absolute paths (e.g. `/Users/alice/.claude/plugins/...`)
break when the plugin is installed by anyone other than the original author.
Using `${CLAUDE_PLUGIN_ROOT}` ensures paths resolve correctly regardless of
install location.

Correct:
```json
"command": "${CLAUDE_PLUGIN_ROOT}/scripts/check.sh"
```

Incorrect:
```json
"command": "/Users/alice/.claude/plugins/cache/my-plugin/1.0.0/scripts/check.sh"
```
```

**Score breakdown:**
- Base: 100. Passes: `description`, bold imperative, rationale, specificity (testable via grep for `/Users/` in hooks.json), `paths` scoping, length, no linter overlap, no vague quantifiers.
- Minor: no reference to related portability rules (env vars in MCP configs, etc.): **-3** (judgment call, not a formal penalty)

**Final: 92/100** — Excellent. The remaining ~5-point gap reflects scope coverage of related portability contexts rather than any rubric violation.

---

## Example 4: Weak Rule (40/100)

**Artifact:**
```markdown
Don't write bad code. Code should be clean and well-organized. Avoid using
outdated patterns. Make sure to handle errors appropriately.
```

**Score breakdown:**
- Base: 100
- Missing frontmatter (no `description` field): **-10**
- No bold imperative opening: **-5**
- No rationale: **-10**
- Not specific or testable ("bad code", "clean", "well-organized" are unmeasurable): **-10**
- "appropriately" (vague quantifier): **-2**
- "well-organized" (vague): **-2**
- Duplicates what every linter/formatter already enforces ("clean code"): **-10**
- Rule is not enforceable by NLPM or any automated tool: **-10** (enforceability)

Total penalties: -59

**Final: max(0, 100 - 59) = 41/100** — Rewrite.

*(Calibrated near 40 as specified. The exact value depends on judgment on "well-organized" as a vague quantifier.)*
