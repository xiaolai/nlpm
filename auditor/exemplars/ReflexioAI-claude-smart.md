---
slug: ReflexioAI-claude-smart
repo: ReflexioAI/claude-smart
audited: 2026-06-20
commit_sha: 3d1612c53f1497bd39ceecbffb0bde276ddc2cef
score: 92
exemplifies:
  - R04
  - R06
  - R07
  - R08
  - R22
---

# Exemplar: ReflexioAI/claude-smart

**Score**: 92/100  |  **Date**: 2026-06-20  |  **Commit**: `3d1612c53f1497bd39ceecbffb0bde276ddc2cef`

A Claude Code plugin packaging browser automation, FastAPI conventions, and PR workflow skills; the 100-scoring artifacts demonstrate trigger-dense descriptions, exhaustive runnable examples, project-specific scope overrides, and pattern-over-theory teaching across five skill files.

## Per-rule evidence

### R04 — Description as trigger

Every 100-scoring skill packs the description field with quoted user-facing trigger phrases rather than abstract capability summaries. The `agent-browser` skill names seven distinct surface verbs; `create-pr` names seven entry conditions; `ralph` names four; `update-public-docs` names five — all in the description frontmatter where they fire skill recall.

> Real quote from `.claude/skills/agent-browser/SKILL.md:3`:
>
> ```
> description: Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data from a page", "test this web app", "login to a site", "automate browser actions", or any task requiring programmatic web interaction.
> ```

Compare to a weak description: "Provides browser automation capabilities." The quote above packs 7 explicit trigger phrases in quotation marks inside the description itself, making it impossible for the model to miss when any of those phrasings appears in user input.

> Real quote from `.claude/skills/ralph/SKILL.md:4`:
>
> ```
> description: "Convert PRDs to prd.json format for the Ralph autonomous agent system. Use when you have an existing PRD and need to convert it to Ralph's JSON format. Triggers on: convert this prd, turn this into ralph format, create prd.json from this, ralph json."
> ```

The `Triggers on:` suffix is a reliable pattern here — each trigger is a literal user phrase, not a category name.

### R06 — Runnable examples

`agent-browser/SKILL.md` (633 lines) devotes the majority of its body to bash code blocks: core workflow, command chaining, five authentication options, parallel sessions, visual diff, JS evaluation via heredoc, iOS simulator interaction, and seven pattern sections — each with copy-paste commands. Every behavior has an accompanying code block rather than prose-only description.

> Real quote from `.claude/skills/agent-browser/SKILL.md:13-47`:
>
> ```
> ## Core Workflow
>
> Every browser automation follows this pattern:
>
> 1. **Navigate**: `agent-browser open <url>`
> 2. **Snapshot**: `agent-browser snapshot -i` (get element refs like `@e1`, `@e2`)
> 3. **Interact**: Use refs to click, fill, select
> 4. **Re-snapshot**: After navigation or DOM changes, get fresh refs
>
> ```bash
> agent-browser open https://example.com/form
> agent-browser snapshot -i
> # Output: @e1 [input type="email"], @e2 [input type="password"], @e3 [button] "Submit"
>
> agent-browser fill @e1 "user@example.com"
> agent-browser fill @e2 "password123"
> agent-browser click @e3
> agent-browser wait --load networkidle
> agent-browser snapshot -i  # Check result
> ```
> ```

The workflow section leads with the pattern, then immediately instantiates it in runnable code — the prose and the example are never more than two sentences apart throughout the file.

> Real quote from `.claude/skills/ralph/SKILL.md:151-228` (complete end-to-end JSON example — condensed here):
>
> ```
> ## Example
>
> **Input PRD:**
> ```markdown
> # Task Status Feature
> Add ability to mark tasks with different statuses.
> ...
> ```
>
> **Output prd.json:**
> ```json
> {
>   "project": "TaskApp",
>   "branchName": "ralph/task-status",
>   ...
>   "userStories": [
>     {
>       "id": "US-001",
>       "title": "Add status field to tasks table",
>       "acceptanceCriteria": [
>         "Add status column: 'pending' | 'in_progress' | 'done' (default 'pending')",
>         "Generate and run migration successfully",
>         "Typecheck passes"
>       ],
>       ...
>     }
>   ]
> }
> ```
> ```

The `ralph` skill's worked example pairs a markdown PRD input with a full `prd.json` output, showing exact field values rather than template placeholders. The agent can produce the correct output by following the structural correspondence, not by inferring it.

### R07 — Scope notes

The `fastapi` skill starts its body with a project-specific override note that narrows the skill's generic instructions to this codebase's actual startup path.

> Real quote from `.claude/skills/fastapi/SKILL.md:9-11`:
>
> ```
> > **Project note**: This project starts the server via `./run_services.sh` (uvicorn), not `fastapi dev`. The patterns below still apply to all endpoint/model code.
> ```

This is the correct R07 shape: one sentence of local exception, one sentence confirming that the rest of the document still applies. Without it, `fastapi dev` instructions would mislead agents on this project.

The `update-public-docs` skill uses an explicit INCLUDE/EXCLUDE section to prevent scope drift when the same source-tree has both public and internal API surfaces.

> Real quote from `.claude/skills/update-public-docs/SKILL.md:69-82`:
>
> ```
> ### Step 4: Scope Rules
>
> **INCLUDE:**
> - All methods in `ReflexioClient`
> - All public Pydantic models used by those methods
> - All enums
> - Config models
>
> **EXCLUDE:**
> - Internal API endpoints (`api.py` internals) — only document what's exposed through `client.py`
> - Skill-related features (disabled)
> - Private/internal helper methods
> - Implementation details
> ```

Naming the excluded surfaces explicitly prevents the agent from documenting internals or disabled features — a common failure mode for doc-sync skills.

The `pythonic-code.md` rules file also uses a scope note to carve out a performance exception within a general rule:

> Real quote from `.claude/rules/pythonic-code.md:35-36`:
>
> ```
> - Prefer EAFP (try/except) over LBYL (if/then check) for high-level logic (file access, network calls, duck-typing)
> - In hot loops where failure rate exceeds ~5-10%, prefer LBYL — exception overhead is significant at scale
> ```

The exception is quantified (`~5-10%`) rather than vague ("in some cases"), giving the agent a decision boundary.

### R08 — Patterns over theory

`fastapi/SKILL.md` uses side-by-side DO/DO NOT code blocks throughout to show the preferred and discouraged patterns together, without prose explanation of why one is preferred — the code makes the argument.

> Real quote from `.claude/skills/fastapi/SKILL.md:48-82`:
>
> ```
> ## Use `Annotated`
>
> Always prefer the `Annotated` style for parameter and dependency declarations.
>
> It keeps the function signatures working in other contexts, respects the types, allows reusability.
>
> ### In Parameter Declarations
>
> Use `Annotated` for parameter declarations, including `Path`, `Query`, `Header`, etc.:
>
> ```python
> @app.get("/items/{item_id}")
> async def read_item(
>     item_id: Annotated[int, Path(ge=1, description="The item ID")],
>     q: Annotated[str | None, Query(max_length=50)] = None,
> ):
>     return {"message": "Hello World"}
> ```
>
> instead of:
>
> ```python
> # DO NOT DO THIS
> @app.get("/items/{item_id}")
> async def read_item(
>     item_id: int = Path(ge=1, description="The item ID"),
>     q: str | None = Query(default=None, max_length=50),
> ):
>     return {"message": "Hello World"}
> ```
> ```

Each section repeats the `instead of: / # DO NOT DO THIS` pattern — five times across the file. The agent learns the pattern by seeing the contrast rather than reading an explanation of why.

`ralph/SKILL.md` teaches story sizing through labeled examples rather than size definitions.

> Real quote from `.claude/skills/ralph/SKILL.md:46-63`:
>
> ```
> ### Right-sized stories:
> - Add a database column and migration
> - Add a UI component to an existing page
> - Update a server action with new logic
> - Add a filter dropdown to a list
>
> ### Too big (split these):
> - "Build the entire dashboard" - Split into: schema, queries, UI components, filters
> - "Add authentication" - Split into: schema, middleware, login UI, session handling
> - "Refactor the API" - Split into one story per endpoint or pattern
>
> **Rule of thumb:** If you cannot describe the change in 2-3 sentences, it is too big.
> ```

"Right-sized vs Too big" with concrete task examples is more actionable than "stories should be small." The rule-of-thumb sentence caps it with a test the agent can apply.

### R22 — Paths-scoped rules

Both `.claude/rules/` files use `paths:` frontmatter to limit the rule to files where it applies, preventing the architectural guardrails from applying outside the Python codebase.

> Real quote from `.claude/rules/reflexio-patterns.md:1-6`:
>
> ```
> ---
> paths:
>   - "reflexio/**/*.py"
> ---
>
> # Reflexio Architecture Guardrails
> ```

> Real quote from `.claude/rules/python-docstrings.md:1-4`:
>
> ```
> ---
> paths:
>   - "**/*.py"
> ---
>
> # Python Docstring Format
> ```

`reflexio/**/*.py` narrows the architectural guardrails to this monorepo package; `**/*.py` applies the docstring convention project-wide. Both rules lead immediately with a code example after the header, with no preamble.

## Worth adopting

**Pattern: Project-override blockquote in shared skills.** Evidence: `.claude/skills/fastapi/SKILL.md:10-11`. A `> **Project note**: ...` callout at the top of a generic skill body lets teams install a vendor-supplied skill unchanged while injecting a single local exception. The note is visually distinct (blockquote), placed before the first instruction, and ends with a sentence confirming the rest of the document still applies. Why it would be a useful rule: shared skills are often vendor-authored and not editable; a project-note convention lets adopters embed local context without forking the skill file, and it's trivially greppable for audit.
