---
slug: TheDecipherist-claude-code-mastery
repo: TheDecipherist/claude-code-mastery
audited: 2026-07-04
commit_sha: 0f05fa1a384c6886b9c4cfda8a9a75be9b0448ee
score: 94
exemplifies:
  - R04
  - R05
  - R06
  - R08
  - R14
  - R31
  - R32
  - R38
---

# Exemplar: TheDecipherist/claude-code-mastery

**Score**: 94/100  |  **Date**: 2026-07-04  |  **Commit**: `0f05fa1a384c6886b9c4cfda8a9a75be9b0448ee`

A documentation-and-templates repo teaching Claude Code configuration: 2 skills, 4 slash commands, 5 hooks, and a CLAUDE.md memory file — notable for hook exit-code discipline and skill descriptions that read as search queries rather than summaries.

## Per-rule evidence

### R04 — Description is a trigger, not a summary

Both skill frontmatter blocks pack multiple concrete trigger phrases instead of a generic label.

> Real quote from `skills/commit-messages/SKILL.md:3`:
>
> ```
> description: Generate clear, conventional commit messages from git diffs. Use when writing commit messages, reviewing staged changes, or preparing releases.
> ```

> Real quote from `skills/security-audit/SKILL.md:3`:
>
> ```
> description: Audit code and dependencies for security vulnerabilities. Use when reviewing PRs, checking dependencies, preparing for deployment, or when user mentions security, vulnerabilities, or audit.
> ```

Each description lists 3+ distinct scenarios ("reviewing staged changes", "preparing releases", "checking dependencies", "preparing for deployment") rather than one abstract sentence — the difference between a description Claude's skill matcher can actually fire on and one it can only stumble into.

### R05 — Under 500 lines

Both skills stay well inside the cap despite covering substantial checklists: `skills/commit-messages/SKILL.md` is 127 lines and `skills/security-audit/SKILL.md` is 229 lines — an 8-item audit checklist (secrets, dependencies, input validation, auth, transport, error handling, file upload, API security) with commands and pass criteria for each, still under half the ceiling.

> Real quote — section headers from `skills/security-audit/SKILL.md`:
>
> ```
> ### 1. Secrets Exposure
> ### 2. Dependency Vulnerabilities
> ### 3. Input Validation
> ### 4. Authentication & Authorization
> ### 5. HTTPS & Transport Security
> ### 6. Error Handling
> ### 7. File Upload Security
> ### 8. API Security
> ```

Eight audit domains in 229 lines works because each section is a checklist plus a runnable command, not prose explaining why the domain matters.

### R06 — Code examples must be runnable

`skills/security-audit/SKILL.md` pairs each vulnerable pattern with a real-syntax BAD/GOOD contrast instead of describing the fix in words.

> Real quote from `skills/security-audit/SKILL.md:88-103`:
>
> ```javascript
> // BAD: SQL injection
> db.query(`SELECT * FROM users WHERE id = ${userId}`)
>
> // GOOD: Parameterized query
> db.query('SELECT * FROM users WHERE id = ?', [userId])
> ```
> ```python
> # BAD: Command injection
> os.system(f"convert {user_file}")
>
> # GOOD: Use subprocess with list
> subprocess.run(["convert", user_file], check=True)
> ```

This is copy-pasteable and languages-correct (real `subprocess.run` signature, real parameterized-query placeholder syntax) — not pseudocode standing in for "sanitize your inputs."

### R08 — Patterns over theory

The "Secrets Exposure" section gives the exact `grep` invocations to run rather than instructing Claude to "check for hardcoded secrets" in the abstract.

> Real quote from `skills/security-audit/SKILL.md:22-27`:
>
> ```
> **Check for hardcoded secrets:**
> grep -rn "API_KEY\|SECRET\|TOKEN\|PASSWORD" --include="*.{js,ts,py,go,rb,java}" .
> grep -rn "sk-\|pk_\|api_\|secret_" --include="*.{js,ts,py,go,rb,java}" .
> ```

A skill that says "look for hardcoded secrets" produces a different search every invocation; one that hands over the exact regex produces the same search every time.

### R14 — Steps must be numbered

`skills/commit-messages/SKILL.md`'s core workflow is a numbered list, not a paragraph describing the process.

> Real quote from `skills/commit-messages/SKILL.md:16-21`:
>
> ```
> ## Process
>
> 1. **Analyze changes**: Run `git diff --staged` to see what's being committed
> 2. **Identify the type**: Determine the primary change category
> 3. **Find the scope**: Identify the main area affected
> 4. **Write the message**: Follow the format below
> ```

Four discrete, ordered actions — no ambiguity about what happens first versus what happens once the type/scope are known.

### R31 — Fail-open by default

`hooks/block-dangerous-commands.sh` only exits 2 (block) on an explicit pattern match; every other path — no command, or a command that matches nothing — falls through to `exit 0` (allow). CLAUDE.md states this as policy for anyone extending the hook set.

> Real quote from `hooks/block-dangerous-commands.sh:121-124`:
>
> ```
> # -----------------------------------------------------------------------------
> # Command is safe, allow it
> # -----------------------------------------------------------------------------
> exit 0
> ```

> Real quote from `CLAUDE.md:62`:
>
> ```
> When editing **hooks/**: Include usage instructions in file header. Explain exit codes. Fail open (exit 0) on unexpected errors.
> ```

The hook denylists ~10 specific patterns (destructive `rm`, force-push to protected branches, `chmod 777`, curl/wget-pipe-to-shell, `dd` to disk devices, `mkfs`, `.env` reads) and allows everything else — a false negative on an unlisted dangerous command is possible, but a false positive blocking legitimate work is not, which is the correct asymmetry for a hook a developer can't easily debug interactively.

### R32 — Block on PreToolUse, advise on PostToolUse

The repo cleanly splits its 5 hooks by whether the moment can still prevent an action. `block-dangerous-commands.sh` and `block-secrets.py` fire on `PreToolUse` and use exit code 2 to block; `after-edit.sh` fires on `PostToolUse` (formatting, after the edit already happened) and `end-of-turn.sh` fires on `Stop` (quality gates, after the whole turn already happened).

> Real quote from `hooks/block-dangerous-commands.sh:2-11`:
>
> ```
> # PreToolUse Hook: Block Dangerous Bash Commands
> #
> # This hook runs BEFORE bash commands execute.
> # It blocks destructive patterns like rm -rf, force pushes, etc.
> #
> # Exit codes:
> #   0 = Allow command
> #   2 = Block command (stderr fed back to Claude)
> ```

> Real quote from `hooks/after-edit.sh:3-8`:
>
> ```
> # PostToolUse Hook: After File Edit
> #
> # This hook runs AFTER Claude edits or writes a file.
> # Use it for fast operations like formatting that should run immediately.
> #
> # For heavier checks (tests, full linting), use the end-of-turn (Stop) hook.
> ```

CLAUDE.md reinforces the same split in its exit-code table (`CLAUDE.md:46-50`, code 2 = "Block operation"), so a reader can't confuse the two hook classes' authority.

### R38 — More instructive than descriptive

CLAUDE.md's "Working With This Repo" section tells Claude what to *do* when touching each directory, not what each directory *is* (that's already covered earlier in "Repository Structure").

> Real quote from `CLAUDE.md:56-64`:
>
> ```
> ## Working With This Repo
>
> When editing **GUIDE.md**: This is the viral Reddit guide. Maintain tone, structure, and citation style. Update "What's new in V2" section when adding features.
>
> When editing **templates/**: These are copy-paste targets. Keep them self-contained. Use placeholders like `YourUsername`, `[DATE]`, `[e.g., PostgreSQL]`.
>
> When editing **hooks/**: Include usage instructions in file header. Explain exit codes. Fail open (exit 0) on unexpected errors.
>
> When editing **skills/**: SKILL.md requires frontmatter with `name` and `description`. Description must explain when to activate.
> ```

Each line is an imperative bound to a specific directory — "use placeholders like `YourUsername`" is an instruction Claude can act on; a description-only CLAUDE.md would instead say something like "templates/ contains template files," which changes no behavior.

## Worth adopting

Pattern: annotate defensive pattern-matching literals in security hooks to preempt scanner false positives. Evidence: `hooks/block-dangerous-commands.sh:79,87` — the blocklist's own `grep -qE` regex text contains the literal substrings `curl\s+.*\|\s*(ba)?sh` and `wget\s+.*\|\s*(ba)?sh` as the strings being matched *against* incoming commands, not executed code, and this audit's own pre-scan flagged both lines as Critical curl/wget-pipe-to-shell findings before manual review cleared them as false positives (see `auditor/audits/TheDecipherist-claude-code-mastery.md` findings #1–#2). Why it would be a useful rule: a one-line comment on each denylist entry (e.g. `# pattern text, not executed`) would let both human reviewers and automated security scanners skip re-deriving that a blocklist string isn't the thing it blocks, saving a verification pass on every audit of every hook that denylists shell substrings.
