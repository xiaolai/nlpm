---
slug: gemini-cli-extensions-conductor
repo: gemini-cli-extensions/conductor
audited: 2026-07-20
commit_sha: fb6212e8faee3f9ecb69f0ee19bd5b2a0765bb0a
score: 90
exemplifies:
  - R04
  - R05
  - R06
  - R08
  - R12
  - R14
  - R17
---

# Exemplar: gemini-cli-extensions/conductor

**Score**: 90/100  |  **Date**: 2026-07-20  |  **Commit**: `fb6212e8faee3f9ecb69f0ee19bd5b2a0765bb0a`

A six-skill Spec-Driven-Development plugin (setup, new-track, implement, review, status, revert) where every skill runs the same numbered handshake-then-protocol shape, each with an explicit halt-and-ask branch for missing state and a literal output template at the end.

## Per-rule evidence

### R04 — Description as trigger

Two of the six descriptions name the exact condition under which the skill should fire, not just what the skill does.

> Real quote from `skills/conductor-setup/SKILL.md:3`:
>
> ```
> description: Scaffolds the project and sets up the Conductor environment. Use this whenever a project needs to be initialized or if the Conductor configuration is missing.
> ```

> Real quote from `skills/conductor-implement/SKILL.md:3`:
>
> ```
> description: Executes the tasks defined in the specified track's plan. Use this to start or continue working on a feature, bug fix, or chore.
> ```

Both descriptions state a triggering condition ("whenever a project needs to be initialized or if the Conductor configuration is missing", "to start or continue working on a feature, bug fix, or chore") rather than a bare capability summary — a Claude Code host matching by description gets a concrete firing condition, not a label.

### R05 — Body length

All six SKILL.md files stay well under the 500-line ceiling; the largest is under half that.

> Line counts (`wc -l skills/*/SKILL.md`):
>
> ```
>  139 skills/conductor-implement/SKILL.md
>  172 skills/conductor-new-track/SKILL.md
>  124 skills/conductor-revert/SKILL.md
>  222 skills/conductor-review/SKILL.md
>  241 skills/conductor-setup/SKILL.md
>   71 skills/conductor-status/SKILL.md
> ```

`conductor-setup/SKILL.md`, the longest file, still fits a full brownfield/greenfield detection tree, a six-step scaffolding sequence, and a literal output template in 241 lines — under half the ceiling — by using nested bullet branches instead of prose paragraphs for each decision point.

### R06 — Runnable examples

`conductor-setup/SKILL.md` gives the agent an exact, non-pseudocode shell sequence for the one step in the whole plugin that shells out to a third party, instead of describing the action in prose.

> Real quote from `skills/conductor-setup/SKILL.md:182-187`:
>
> ```
>     - **Execute Installation:** You MUST download the selected skill using exactly the following `curl` command sequence. Do not modify the parameters or add flags:
>
>         ```bash
>         mkdir -p .agents/skills/<skill_name>
>         curl -sSL <URL>SKILL.md -o .agents/skills/<skill_name>/SKILL.md
>         ```
> ```

The only placeholders are `<skill_name>` and `<URL>`, both resolved earlier in the same section from the loaded catalog — everything else is literal, copy-executable shell. (The sibling skill `conductor-new-track/SKILL.md:126` collapses the identical two-line sequence into a single unfenced inline-code span, which the underlying audit flagged as a bug precisely because it breaks the runnable-example contract this file honors.)

### R08 — Patterns over theory

`conductor-review/SKILL.md`'s track-cleanup step is written as three concrete branches with the exact file operation and commit message for each choice, not a general description of "cleaning up after a review."

> Real quote from `skills/conductor-review/SKILL.md:200-205`:
>
> ```
> 3. **If the user chooses "Archive":**
>     - Ensure `conductor/archive/` directory exists.
>     - Move the track folder to `conductor/archive/<track_id>/`.
>     - Remove the track section from the **Tracks Registry**.
>     - Stage changes and commit with message: `chore(conductor): Archive track '<track_name>'`.
>     - Announce to the user that the track has been archived.
> ```

Each of the three choices (Archive / Delete / Skip) gets its own literal directory path and commit-message template — an agent following this never has to infer what "archiving" means in this codebase.

### R12 — Output format defined in body

`conductor-review/SKILL.md` ends its analysis phase with a literal report template, not an instruction to "summarize the findings."

> Real quote from `skills/conductor-review/SKILL.md:112-125`:
>
> ```
> ### 2.4 Output Findings
> **Format your output strictly as follows:**
>
> # Review Report: [Track Name / Context]
>
> ## Summary
> [Single sentence description of the overall quality and readiness]
>
> ## Verification Checks
> - [ ] **Plan Compliance**: [Yes/No/Partial] - [Comment]
> - [ ] **Style Compliance**: [Pass/Fail]
> - [ ] **New Tests**: [Yes/No]
> - [ ] **Test Coverage**: [Yes/No/Partial]
> - [ ] **Test Results**: [Passed/Failed] - [Summary of failing tests or 'All passed']
> ```

The word "strictly" plus a literal markdown skeleton (checkbox fields, bracketed placeholders) means every invocation of this skill produces a structurally identical report, which is what makes the report machine-parseable across runs.

### R14 — Steps must be numbered

Every multi-step section across all six skills is a numbered list, including nested sub-decisions — never unnumbered prose.

> Real quote from `skills/conductor-implement/SKILL.md:64-90` (section "3. Track Implementation"):
>
> ```
> 1.  **Announce Action:** Announce which track you are beginning to implement.
>
> 2.  **Update Status to 'In Progress':**
>     -   Before beginning any work, update the status of the selected track to `[~]` in the **Tracks Registry** file.
>     -   Stage the file and commit: `chore(conductor): Mark track '<track_description>' as in progress`.
>
> 3.  **Load Track Context:**
>     ...
> 4.  **Execute Tasks and Update Track Plan:**
>     ...
> 5.  **Finalize Track:**
>     -   After all tasks are completed, update the track status to `[x]` in the **Tracks Registry**.
> ```

The numbering survives even where a step has five bullet sub-clauses (step 3) — the top-level sequence is never left to be inferred from paragraph breaks.

### R17 — Specify error paths

All six skills open with the identical two-tier missing-file check: missing index file, and missing files the index links to. Each tier names its own halt-and-recovery path instead of failing silently.

> Real quote from `skills/conductor-implement/SKILL.md:26-37`:
>
> ```
> 1.  **Locate Index:** Check for the existence of `conductor/index.md` in the project root.
>     -   **If Missing:**
>         -   Announce: *"Conductor is not initialized properly. I cannot find the `conductor/index.md` file."*
>         -   Ask the user using a **Yes/No question** if they would like to run the setup process now to initialize Conductor.
>         -   **If Approved:** Internally invoke the `conductor-setup` skill.
>         -   **If Denied:** HALT and await further instructions.
>
> 2.  **Load & Verify Context:** Read `conductor/index.md` and use the provided links to locate the core files:
>     ...
>     -   **Health Check:** You MUST verify that every linked file actually exists. If ANY of these core files are missing, HALT immediately. Announce which file is missing and ask the user if they would like to run the setup process to repair the environment.
> ```

Both branches name the exact user-facing announcement and the exact recovery action (invoke `conductor-setup`) — there's no path where a missing file produces an unexplained failure or a silent fallback.

## Worth adopting

Pattern: **Recommended-first multiple-choice with a mandatory custom escape hatch.** Evidence: `skills/conductor-setup/SKILL.md:18-22` — "You MUST provide either single-choice or multiple-choice options based on context-aware suggestions. If a specific option is preferred... list it first, suffix it with '(Recommended: *\<explanation\>*)'... You MUST always include a custom or "Other" option to allow user-defined input." Why it would be a useful rule: repeated verbatim across all six skills in this repo, it structurally prevents two common interactive-agent failures at once — the agent picking silently on the user's behalf, and the agent trapping the user inside an enumerated list with no way to say something else. Could be codified as: "When asking the user to choose among generated options, rank a recommended option first with its rationale, and always include a free-text escape option — never present a closed list as if it were exhaustive."
