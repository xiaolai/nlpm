---
slug: ccch1mneyyy-dsh-TUI
repo: ccch1mneyyy/dsh-TUI
audited: 2026-09-30
commit_sha: 8540a58f4e7315c8b7abe9220a5af453f032c2f0
score: 95
exemplifies:
  - R04
  - R05
  - R07
  - R03
---

# Exemplar: ccch1mneyyy/dsh-TUI

**Score**: 95/100  |  **Date**: 2026-09-30  |  **Commit**: `8540a58f4e7315c8b7abe9220a5af453f032c2f0`

Nine skills (eight maintainer skills under `.agents/skills/` plus one user guide under `guide/`), each with a one-sentence trigger description that names a sibling skill to use instead, and a body of 4-5 numbered steps.

## Per-rule evidence

### R04 — Description as trigger

Every maintainer skill's description has three parts: what it produces, a "Use for ..." trigger (often including the slash command), and a redirect to the neighbouring skill for the adjacent case. The redirect keeps `vuln-check`, `audit`, `review` and `pr-comments` from competing for the same request.

> Real quote from `.agents/skills/vuln-check/SKILL.md:3`:
>
> ```
> description: Check resolved dependencies and relevant code paths for security vulnerabilities. Use for security checks or /vuln-check; use audit for a broader correctness and maintainability assessment.
> ```

> Real quote from `.agents/skills/pr-comments/SKILL.md:3`:
>
> ```
> description: Read and triage existing pull request review comments, or address them when requested. Use for PR comment requests or /pr-comments; use review to inspect code without existing reviewer feedback.
> ```

Both descriptions draw the boundary against a named sibling skill instead of leaving the model to guess between them.

### R05 — Body length

The `bug`, `release-notes` and `pr-comments` bodies are 5-12 lines of instruction after frontmatter. Each is a numbered procedure plus one closing paragraph of constraints, with no preamble or background section.

> Real quote from `.agents/skills/bug/SKILL.md:6-13`:
>
> ```
> Produce a concise report another person can reproduce or investigate. If the user asked for a fix, use the report as working context, continue the repair, and validate the result.
>
> 1. Extract the symptom, expected behavior, and reproduction details already supplied. Inspect available logs and relevant code before asking for facts the workspace can provide.
> 2. Ask only for missing information that materially affects reproduction or diagnosis, such as terminal mode or the triggering input. Continue independent investigation while waiting; label unknowns instead of guessing.
> 3. Include the symptom in the title, then the smallest known reproduction, expected versus actual result, relevant environment, and impact. Distinguish a reproduction you ran from one reported by the user.
> 4. Include a cause or workaround only when evidence supports it; label hypotheses and cite the relevant code. Omit empty sections and speculative severity labels.
> ```

Four steps cover extraction, questioning, report shape and speculation limits; every step carries a decision rule rather than restating the goal.

### R07 — Scope notes

Each skill ends by stating what it does not authorize. This separates drafting from publishing (`bug`, `release-notes`) and reporting from remediation (`vuln-check`).

> Real quote from `.agents/skills/release-notes/SKILL.md:13`:
>
> ```
> Deliver the notes as a draft unless publishing is part of the user's request. If it is, continue the authorized release workflow using the repository's version and tag rules.
> ```

> Real quote from `.agents/skills/vuln-check/SKILL.md:14`:
>
> ```
> Report potential secrets only by path, line, and type, never their value or a source excerpt. Do not run automatic dependency fixes as part of a check; for requested remediation, make targeted changes and validate the affected paths.
> ```

The boundary is stated as a condition ("unless publishing is part of the user's request") with the follow-on behaviour, so the model knows both the default and the exception.

### R03 — Positive framing

Where a negative is needed, the skills pair it with the action to take instead, and the `dsh-tui-guide` skill states its fallback for missing information.

> Real quote from `guide/dsh-tui-guide/SKILL.md:17-19`:
>
> ```
> 4. **给出处**：回答末尾写清来源（文件名 + 小节标题），用户能直接翻回去核对。
> 5. **别编**：手册没写的直说"手册没写"，再给保守建议；不要拿记忆里的旧行为顶替。
> ```

Rule 5 ("don't invent") gives the exact phrase to use and the next step (give conservative advice), so the prohibition comes with a replacement behaviour.

## Worth adopting

Pattern: Cross-reference the sibling skill in the description. Evidence: `.agents/skills/vuln-check/SKILL.md:3` ("use audit for a broader correctness and maintainability assessment"), `.agents/skills/pr-comments/SKILL.md:3`. Why it would be a useful rule: when a collection holds skills with overlapping domains, each description should name the neighbour that owns the adjacent case, so trigger selection is unambiguous.
