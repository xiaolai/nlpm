---
slug: matt1398-claude-devtools
repo: matt1398/claude-devtools
audited: 2026-07-04
commit_sha: 16cc3c87c1e4d0e08ee101fb52dad1b85dbbe48a
score: 91
exemplifies:
  - R04
  - R06
  - R08
  - R09
  - R12
  - R13
  - R25
  - R27
  - R32
  - R35
  - R38
  - R47
---

# Exemplar: matt1398/claude-devtools

**Score**: 91/100  |  **Date**: 2026-07-04  |  **Commit**: `16cc3c87c1e4d0e08ee101fb52dad1b85dbbe48a`

An Electron app (2 agents, 5 commands, 3 path-scoped rules files, project hooks) whose lowest-scoring artifacts still hit 70+ — the drift the audit found was all one-directional (undocumented new code), never a stale pointer to something deleted.

## Per-rule evidence

### R04 — Description is a trigger, not a summary

All five `.claude/commands/devtools/*.md` files pack a topic clause and an explicit "Use when" trigger clause naming concrete symbols, not a generic summary.

> `.claude/commands/devtools/navigation-scroll.md:3`:
>
> ```
> description: Navigation and scroll orchestration — tab navigation, error highlights, search scrolling, auto-scroll coordination, and common bug patterns. Use when working on useTabNavigationController, scroll restore, or navigation requests.
> ```

> `.claude/commands/devtools/markdown-search-logic.md:3`:
>
> ```
> description: Markdown search logic — how in-session and cross-session search works. Use when working on SearchBar, search highlighting, searchHighlightUtils, markdownTextSearch, or SessionSearcher.
> ```

Each trigger names actual hook/component/utility identifiers (`useTabNavigationController`, `searchHighlightUtils`) rather than topic words a user might not type — this is what lets description-based matching fire on a real query like "why isn't scroll restore working."

### R06 — Code examples must be runnable

`.claude/commands/devtools/chatgroup-architecture.md` shows the actual discriminated-union type from the codebase, not a paraphrase:

> `.claude/commands/devtools/chatgroup-architecture.md:15-30`:
>
> ```typescript
> // src/renderer/types/groups.ts
> export type ChatItem =
>   | { type: 'user'; group: UserGroup }
>   | { type: 'system'; group: SystemGroup }
>   | { type: 'ai'; group: AIGroup }
>   | { type: 'compact'; group: CompactGroup };
>
> export interface SessionConversation {
>   sessionId: string;
>   items: ChatItem[];  // Flat chronological list
>   totalUserGroups: number;
>   totalSystemGroups: number;
>   totalAIGroups: number;
>   totalCompactGroups: number;
> }
> ```

The comment on line 1 (`// src/renderer/types/groups.ts`) means a reader can `Read` that exact file and diff it against the doc — the example is a citable fact, not an illustration.

### R08 — Patterns over theory

`.claude/commands/devtools/design-system.md` teaches by contrast — labeled "Preferred" vs. "Also valid" code blocks — instead of a paragraph explaining the tradeoff:

> `.claude/commands/devtools/design-system.md:33-40`:
>
> ```tsx
> // Preferred: inline style for theme-aware colors, Tailwind for layout
> <div className="flex items-center gap-2 rounded-md px-3 py-2"
>      style={{ backgroundColor: 'var(--color-surface-raised)', color: 'var(--color-text)' }}>
>   <Bot className="size-4 shrink-0" style={{ color: COLOR_TEXT_SECONDARY }} />
> </div>
>
> // Also valid: Tailwind classes that reference CSS variables
> <div className="bg-surface text-text border-border">
> ```

A Claude instance styling a new component copies one of these two blocks directly rather than reasoning from a description of "theme-aware colors."

### R09 — `<example>` blocks are mandatory

`.claude/agents/claude-md-auditor.md` packs four full examples into its `description` field, each with a user message, an assistant response, and a `<commentary>` tag explaining why the example triggers this agent:

> `.claude/agents/claude-md-auditor.md:3` (frontmatter `description`, Example 3 of 4):
>
> ```
> - Example 3:
>   user: "Rename isRealUserMessage to isParsedRealUserMessage across the codebase"
>   assistant: "The rename is complete across all source and test files. Now I'll launch the claude-md-auditor agent to update any documentation references to the old function name."
>   <commentary>
>   A function was renamed which is likely documented in CLAUDE.md type guard tables and conventions sections. Use the Task tool to launch the claude-md-auditor agent to fix stale references.
>   </commentary>
> ```

Four examples, double the R09 minimum, each covering a distinct trigger condition (refactor, feature addition, rename, explicit request) rather than four rewordings of the same scenario.

### R12 — Output format defined in body

`.claude/agents/quality-fixer.md` ends with an exact report shape instead of "summarize what you did":

> `.claude/agents/quality-fixer.md:76-83`:
>
> ```
> ### Reporting
>
> After the loop completes (either success or max iterations), provide a summary:
> - Total iterations run
> - Issues found and fixed (categorized by type: lint, format, types, unused code)
> - Final status: PASS or FAIL with remaining issues
> - Files modified
> ```

Four named fields, in a fixed order — two invocations of this agent produce diffable, not just similar, reports.

### R13 — System prompt structure: mission → steps → boundaries → format

`.claude/agents/claude-md-auditor.md` follows the four-layer shape rule-for-rule: mission in the opening two sentences, numbered phases, a boundary section titled "Critical Rules," then an output template.

> `.claude/agents/claude-md-auditor.md:9,131,137`:
>
> ```
> You are an elite CLAUDE.md auditor and documentation integrity specialist. Your sole purpose is to ensure every `CLAUDE.md` file and `.claude/rules/*.md` file in the project accurately reflects the current codebase state. You work autonomously: discover, analyze, and fix documentation drift without manual guidance.
> ...
> ## Critical Rules
> ...
> **Don't touch non-documentation files.** You modify ONLY `**/CLAUDE.md` and `.claude/rules/*.md` files. Never edit source code, tests, or config files.
> ```

The boundary line is a scope fence, not a restatement of the mission — it rules out a failure mode (editing source files during a "fix drift" pass) the mission sentence alone doesn't foreclose.

### R25 — Path-scope when possible

All three `.claude/rules/*.md` files carry a `globs` frontmatter key scoping them to the file types they actually govern, instead of loading on every turn:

> `.claude/rules/react.md:1-3`:
>
> ```
> ---
> globs: ["src/renderer/**/*.tsx"]
> ---
> ```

> `.claude/rules/testing.md:1-3`:
>
> ```
> ---
> globs: ["test/**/*", "**/*.test.ts", "**/*.spec.ts"]
> ---
> ```

`tailwind.md` scopes to two patterns (`**/*.css` and `src/renderer/**/*.tsx`) rather than one, because the CSS-variable conventions it documents are referenced from both stylesheets and components — the scope matches where the convention is actually used, not just the most obvious file type.

### R27 — Event names are case-sensitive

`.claude/settings.json` uses the exact required casing for all three hook events it registers:

> `.claude/settings.json`:
>
> ```json
> "hooks": {
>   "PreToolUse": [ ... ],
>   "PostToolUse": [ ... ],
>   "SessionStart": [ ... ]
> }
> ```

`PreToolUse`, `PostToolUse`, and `SessionStart` — not `pretooluse` or `PreToolUse ` with trailing whitespace — matches Claude Code's hook dispatcher exactly, so none of the three silently fail to fire.

### R32 — Block on PreToolUse, advise on PostToolUse

The same `.claude/settings.json` assigns the two event types to the two jobs the rule prescribes: `PreToolUse` denies a write outright (`exit 2`), `PostToolUse` runs an auto-fixer after the write already happened.

> `.claude/settings.json` (`PreToolUse` hook, abbreviated):
>
> ```
> "matcher": "Edit|Write",
> "command": "... if echo \"$f\" | grep -q \"$p\"; then echo \"Blocked: $f matches protected pattern '$p'\" >&2; exit 2; fi ..."
> ```

> `.claude/settings.json` (`PostToolUse` hook, abbreviated):
>
> ```
> "matcher": "Edit|Write|NotebookEdit",
> "command": "... pnpm eslint --fix \"$file_path\" ... pnpm prettier --write \"$file_path\" ..."
> ```

`PreToolUse` protects `pnpm-lock.yaml`, `.env`, `dist/`, `node_modules/` by refusing the edit before it lands; `PostToolUse` can only clean up (`eslint --fix`, `prettier --write`) after the edit already happened — the split matches which event can actually still prevent something.

### R35 — Include architecture overview

Root `CLAUDE.md` documents the domain model (chunk types) as a component map rather than prose:

> `CLAUDE.md:39-45`:
>
> ```
> ### Chunk Structure
> Independent chunk types for timeline visualization:
> - **UserChunk**: Single user message with metrics
> - **AIChunk**: All assistant responses with tool executions and spawned subagents
> - **SystemChunk**: Command output/system messages
> - **CompactChunk**: System metadata/structural messages
> ```

A Claude instance asked to add a fifth chunk type has the exact enumeration to extend, not a description to reinterpret.

### R38 — More instructive than descriptive

The "TypeScript Conventions" section of root `CLAUDE.md` gives naming rules as a lookup table plus runnable type-guard signatures, not a description of the style:

> `CLAUDE.md:126-133`:
>
> ```
> | Category | Convention | Example |
> |----------|------------|---------|
> | Services/Components | PascalCase | `ProjectScanner.ts` |
> | Utilities | camelCase | `pathDecoder.ts` |
> | Constants | UPPER_SNAKE_CASE | `PARALLEL_WINDOW_MS` |
> | Type Guards | isXxx | `isRealUserMessage()` |
> ```

Every row is a rule Claude can apply to a new file name (`isXxx` → write `isFooBar`, not "keep type guard names consistent") — none of the six sections in this file describe what the app is for a human reader; that's `README.md`'s job.

### R47 — Max retry count on loops

`.claude/agents/quality-fixer.md` caps its fix-and-recheck loop explicitly instead of looping until success:

> `.claude/agents/quality-fixer.md:70`:
>
> ```
> 1. **Maximum 5 iterations**. If after 5 loops quality still doesn't pass, stop and report the remaining issues to the user with a clear summary of what was fixed and what remains.
> ```

The cap is paired with a defined failure report (what was fixed, what remains) rather than a silent stop — the loop can't run forever, and it can't fail silently either.

## Worth adopting

Pattern: per-agent persistent memory directory with an explicit save/don't-save list. Evidence: `.claude/agents/claude-md-auditor.md:153-181` — a `## Persistent Agent Memory` section pointing at `.claude/agent-memory/claude-md-auditor/`, with a `MEMORY.md` (loaded into the system prompt, truncated past 200 lines) plus topic files, and two explicit lists: "What to save" (stable patterns, architectural decisions, recurring solutions) and "What NOT to save" (session-specific context, unverified single-file conclusions, anything duplicating CLAUDE.md). Why it would be a useful rule: without an explicit save/don't-save boundary, agents either re-derive the same drift patterns every invocation (wasted tokens) or accumulate stale/contradictory notes that outlive the code they described (bad instructions surviving past their truth).
