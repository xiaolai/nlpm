---
slug: YishenTu-claudian
repo: YishenTu/claudian
audited: 2026-06-20
commit_sha: 2ca77f03c7ed91f9374d5fb4d41891fae6d45b11
score: 100
exemplifies:
  - R06
  - R08
  - R33
  - R34
  - R35
  - R38
---

# Exemplar: YishenTu/claudian

**Score**: 100/100  |  **Date**: 2026-06-20  |  **Commit**: `2ca77f03c7ed91f9374d5fb4d41891fae6d45b11`

An Obsidian plugin embedding multi-provider chat runtimes, with six CLAUDE.md files that use runnable code, gotcha catalogs, and active directives instead of prose description.

## Per-rule evidence

### R06 — Code examples must be runnable

The `src/core/CLAUDE.md` includes three TypeScript snippets that show real API surfaces, not pseudocode. Each snippet uses the actual class names and method signatures defined in the codebase.

> Real quote from `src/core/CLAUDE.md:41-57`:
>
> ```typescript
> const runtime = ProviderRegistry.createChatRuntime({ plugin, providerId });
> const preparedTurn = runtime.prepareTurn(request);
>
> for await (const chunk of runtime.query(preparedTurn, history)) {
>   // Feature layer consumes provider-neutral StreamChunk values.
> }
> ```
>
> ```typescript
> const titleService = ProviderRegistry.createTitleGenerationService(plugin);
> const refineService = ProviderRegistry.createInstructionRefineService(plugin, providerId);
> const inlineEditService = ProviderRegistry.createInlineEditService(plugin, providerId);
> ```

The comment inside the loop ("Feature layer consumes provider-neutral StreamChunk values") doubles as a constraint — it tells the reader what NOT to put in the loop body, adding behavioral guidance with zero extra lines.

### R08 — Patterns over theory

The provider CLAUDE.md files (`src/providers/claude/CLAUDE.md`, `src/providers/codex/CLAUDE.md`) organize non-obvious behaviors as named scenario entries rather than abstract descriptions. Each entry names the situation, states the mechanism, and adds the downstream consequence if the reader ignores it.

> Real quote from `src/providers/claude/CLAUDE.md:31-35`:
>
> ```
> ### SDK Amnesia Detection
>
> When the SDK returns a different session ID than the one provided in `resume`,
> `SessionManager.captureSession()` sets `needsHistoryRebuild = true`. `ClaudeChatRuntime`
> detects this and injects full conversation history into the next user message before
> dispatching the turn. This handles the case where the SDK silently lost context
> without explicit error signaling.
>
> **Fork interaction**: on the first `session_init` after a fork, `clearHistoryRebuild()`
> prevents the amnesia logic from triggering — the SDK legitimately returns a different
> session ID for forks.
> ```

The "Fork interaction" sub-note is the key quality signal: it disambiguates two situations that look identical at the surface (both produce a mismatched session ID) but require opposite responses.

### R33 — Include build/run command

The root `CLAUDE.md` lists all eight development commands in a single code block at line 18, covering the full dev/build/test/lint lifecycle.

> Real quote from `CLAUDE.md:17-27`:
>
> ```bash
> npm run dev
> npm run build
> npm run typecheck
> npm run lint
> npm run lint:fix
> npm run test
> npm run test:watch
> npm run test:coverage
> ```

No prose, no prose-wrapping, no guessing: an AI landing in this repo can emit the correct command for any standard workflow without reading further.

### R34 — Include test command

The Tests section (root `CLAUDE.md:45-53`) goes beyond the generic `npm run test` entry in the Commands block by providing project-selector flags for unit vs. integration runs.

> Real quote from `CLAUDE.md:45-53`:
>
> ```bash
> npm run test -- --selectProjects unit
> npm run test -- --selectProjects integration
> npm run test:coverage -- --selectProjects unit
> ```
>
> Tests mirror the `src/` layout under `tests/unit/` and `tests/integration/`.

The mirror-layout note tells an AI where to create a new test file without scanning the directory tree.

### R35 — Include architecture overview

The root `CLAUDE.md` has a ten-row architecture table linking six sub-modules to their respective CLAUDE.md files. Four of the six cells are clickable cross-references; the remaining two carry inline descriptions where no sub-file exists.

> Real quote from `CLAUDE.md:30-44`:
>
> ```
> | Layer | Purpose | Details |
> |-------|---------|---------|
> | **app** | Shared defaults and plugin-level storage helpers | `defaultSettings`, `ClaudianSettingsStorage`, `SharedStorageService` |
> | **core** | Provider-neutral contracts and infrastructure | See [`src/core/CLAUDE.md`](src/core/CLAUDE.md) |
> | **providers/claude** | Claude SDK adaptor | See [`src/providers/claude/CLAUDE.md`](src/providers/claude/CLAUDE.md) |
> | **providers/codex** | Codex app-server adaptor | See [`src/providers/codex/CLAUDE.md`](src/providers/codex/CLAUDE.md) |
> | **features/chat** | Main sidebar interface | See [`src/features/chat/CLAUDE.md`](src/features/chat/CLAUDE.md) |
> | **features/inline-edit** | Inline edit modal and provider-backed edit services | `InlineEditModal` plus provider-owned inline edit services |
> | **features/settings** | Shared settings shell with provider tabs | General tab plus provider-owned Claude and Codex tab renderers |
> | **shared** | Reusable UI building blocks | Dropdowns, modals, mention UI, icons |
> | **i18n** | Internationalization | 10 locales |
> | **utils** | Cross-cutting utilities | env, path, markdown, diff, context, file-link, image, browser, canvas, session, subagent helpers |
> | **style** | Modular CSS | See [`src/style/CLAUDE.md`](src/style/CLAUDE.md) |
> ```

Six out of eleven detail cells are concrete key-file lists or links rather than restatements of the purpose column — the table does not duplicate itself.

### R38 — More instructive than descriptive

The "Development Notes" section of the root `CLAUDE.md` (lines 73-80) reads as a set of active directives, not a project README. Each bullet tells the AI what to do, in what order, and why — not what the project is.

> Real quote from `CLAUDE.md:73-80`:
>
> ```
> - **Provider-native first**: Prefer the official Claude SDK and Codex app-server behavior
>   over reimplementing provider features locally. When the provider already owns a
>   capability, adapt to it instead of shadowing it.
> - **Runtime exploration**: For provider integrations, inspect real runtime output first.
>   Claude data lands under `~/.claude/` and Codex data under `~/.codex/`. Real transcripts
>   beat guessed event shapes. Put throwaway local scripts in `.context/`; only promote
>   durable tooling into `dev/`.
> - **TDD workflow**: For new behavior or bug fixes, write the failing test first in the
>   mirrored `tests/` path, make it pass, then refactor.
> - Run `npm run typecheck && npm run lint && npm run test && npm run build` after editing.
> - No `console.*` in production code.
> ```

The "Real transcripts beat guessed event shapes" line is the signal: it gives the AI a concrete decision rule for a non-obvious situation (how to reverse-engineer provider wire formats) that no linter or test would enforce.

## Worth adopting

**Pattern**: Named design decisions with explicit "why not" framing.  
**Evidence**: `src/providers/claude/CLAUDE.md:7-9` — `### Persistent Query — Why Not Restart` — and `src/providers/codex/CLAUDE.md:17-23` — `### Live Streaming Uses Raw JSON-RPC` — each name the rejected alternative and explain the failure mode that would result.  
**Why it would be a useful rule**: "When documenting a non-obvious architecture choice, name the alternative you rejected and state what breaks if a reader reverses it. Without the rejected alternative, AI and human readers cannot distinguish intentional design from accidental omission and are likely to 'fix' the design toward the rejected pattern."
