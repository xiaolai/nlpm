---
name: writing-rules
description: How to write .claude/rules/ files that Claude actually follows. Use when creating, improving, or reviewing project rules.
metadata:
  version: 0.2.0
---

# Writing Rules

> Scope: covers `.claude/rules/` file authoring — a **Claude-Code-specific** concept (path-scoped, always-loaded instruction files with `paths:` glob frontmatter). Codex CLI and Antigravity have no exact `.claude/rules/` equivalent; their always-on project instructions live in the hierarchical memory file (`AGENTS.md` for Codex, `GEMINI.md` for Antigravity — both can be pointed at the canonical `AGENTS.md`; see [[nlpm:conventions-codex]] / [[nlpm:conventions-antigravity]]). The bold-imperative-plus-rationale writing technique here applies to any tool's instruction files. For CLAUDE.md / AGENTS.md conventions, see [[writing-plugins]]. For system prompts generally, see [[writing-prompts]].

## 1. The Golden Format

Every rule should have three parts:

```
**Use X, not Y.** Without X, [concrete bad thing happens]. Y causes [specific problem] because [mechanism].
```

| Part | Purpose | Example |
|------|---------|---------|
| Imperative | What to do | **Use `Result<T, AppError>` for all API handler returns.** |
| Consequence | What goes wrong without it | Without it, errors propagate as 500s with no context. |
| Mechanism | Why it fails | Raw panics bypass the error middleware and crash the worker. |

### One-Line Rules (when mechanism is obvious)

```markdown
**Use `const`/`let`, never `var`.** `var` hoists to function scope, causing stale-reference bugs.
```

### Multi-Line Rules (when mechanism needs explanation)

```markdown
**Use database transactions for multi-table writes.** Without transactions, partial writes leave the database in an inconsistent state. The ORM's `save()` method does not auto-wrap related writes -- you must explicitly call `db.transaction()`.
```

## 2. Positive Framing (Pink Elephant Effect)

Claude fixates on prohibited things. Saying "Don't use X" makes Claude think about X.

### Before (negative framing -- score 60)

```markdown
- Don't use var
- Don't mutate function parameters
- Don't use console.log in production code
```

### After (positive framing -- score 90)

```markdown
- **Use `const` for all bindings; use `let` only when reassignment is required.**
- **Return new objects instead of mutating function parameters.**
- **Use the `logger` service for all logging.** `console.log` is stripped in production builds.
```

### Conversion Pattern

| Negative (avoid) | Positive (use instead) |
|-------------------|----------------------|
| Don't use X | **Use Y** (where Y is the correct alternative) |
| Never do X | **Always do Y** |
| Avoid X because... | **Use Y because...** (flip the rationale) |
| X is deprecated | **Use Y, which replaced X in version N** |

## 3. Enforceability Test

Before writing a rule, ask: **"Can I check compliance in a 30-second code review?"** If no, it is not a rule.

### Enforceable (specific, testable)

| Rule | Test |
|------|------|
| **Use `Result<T, AppError>` for all API handler returns.** | Grep for handler functions, check return types |
| **All API endpoints require `@auth` decorator.** | Grep for route definitions, check for decorator |
| **Database queries use parameterized statements, not string concatenation.** | Grep for SQL strings, check for `+` or template literals |

### Not Enforceable (subjective, unmeasurable)

| Rule | Why it fails |
|------|-------------|
| "Write clean, maintainable code" | What is "clean"? No objective test. |
| "Keep functions small" | How small? 10 lines? 20? 50? |
| "Use meaningful variable names" | "Meaningful" is subjective. |
| "Follow best practices" | Which practices? Says nothing specific. |

### Making Vague Rules Enforceable

| Vague | Enforceable version |
|-------|-------------------|
| "Keep functions small" | **Functions must be under 40 lines.** Reference: enforced by `eslint max-lines-per-function` |
| "Use meaningful names" | **Variable names must be >= 3 characters except loop indices (`i`, `j`, `k`).** |
| "Handle errors properly" | **Every `catch` block must either re-throw, log + return error response, or call `reportError()`.** |

## 4. Budget Discipline

All rules across `.claude/rules/` must total **under 500 lines**. Every line costs tokens on every Claude interaction -- rules are always loaded.

### Token Cost

| Rule lines | Approx tokens per interaction | Annual cost at 100 interactions/day |
|-----------|------------------------------|-------------------------------------|
| 100 | ~400 | Negligible |
| 300 | ~1,200 | Noticeable |
| 500 | ~2,000 | Budget line |
| 800+ | ~3,200+ | Over budget -- consolidate |

### Line Reduction Strategies

| Strategy | Example | Lines saved |
|----------|---------|-------------|
| Defer to linter | "Reference: enforced by `pnpm lint`" instead of re-stating lint rules | 10-30 |
| Merge related rules | Combine 3 files about error handling into 1 | 15-25 |
| Delete training knowledge | Remove rules Claude follows without being told | 5-15 |
| Use tables instead of lists | 10 rules as list = 20 lines; as table = 12 lines | 5-10 |

### Rules Claude Already Follows (safe to delete)

These are part of Claude's training and do not need rules:
- "Use descriptive variable names" (Claude already does this)
- "Add comments to complex code" (Claude already does this)
- "Handle null/undefined checks" (Claude already does this)
- "Use async/await instead of callbacks" (Claude already prefers this)

Only write rules for things **specific to your project** that Claude would not know.

## 5. Path Scoping

Rules without path scoping apply to every file -- expensive and often wrong.

```yaml
---
paths: ["src/api/**/*.ts"]
---
```

### Scoping Strategy

| Rule type | Scope | Example paths |
|-----------|-------|---------------|
| API conventions | API routes only | `src/api/**/*.ts`, `src/routes/**/*.ts` |
| Database rules | Data layer only | `src/db/**/*.ts`, `src/models/**/*.ts` |
| Test conventions | Test files only | `**/*.test.ts`, `**/*.spec.ts` |
| Universal rules | No scope (apply everywhere) | _(omit paths field)_ |

**Rule**: if a rule mentions a specific directory, technology, or layer -- scope it.

### Cost Impact of Scoping

| Scenario | Token cost |
|----------|-----------|
| Unscoped: 200-line rules file loaded on every interaction | 800 tokens always |
| Scoped: same rules split into 4 files with path scoping | 200 tokens per interaction (only relevant rules load) |

## 6. Conflict Prevention

Two rules must never contradict. If they could, put them in the **same file** with explicit conditions.

### Bad (separate files, contradictory)

`rules/api.md`:
```markdown
**Return raw JSON objects from API handlers.**
```

`rules/error-handling.md`:
```markdown
**Wrap all returns in Result<T, AppError>.**
```

### Good (same file, explicit conditions)

`rules/api-returns.md`:
```markdown
**Return `Result<T, AppError>` from API handler functions.** This ensures consistent error formatting through the error middleware.

**Return raw JSON from internal service functions.** Services are called by handlers, not directly by clients, so they do not need the Result wrapper.
```

### Conflict Detection Checklist

Before adding a new rule, check:
1. Search all existing rules for the same keywords
2. Does any existing rule say the opposite?
3. Does any existing rule cover a broader case that includes yours?
4. If conflict found: merge into the same file with explicit conditions

## 7. Worked Example

### Before (score 45/100) -- 800 lines, 12 files

```
.claude/rules/
  naming.md          (80 lines -- mostly restates ESLint rules)
  errors.md          (90 lines -- contradicts exceptions.md)
  exceptions.md      (70 lines -- contradicts errors.md)
  logging.md         (60 lines -- unscoped, only relevant to src/api/)
  testing.md         (85 lines -- includes Jest tutorial content)
  database.md        (95 lines -- unscoped, only relevant to src/db/)
  api.md             (70 lines -- overlaps with errors.md)
  security.md        (55 lines -- restates OWASP basics Claude already knows)
  performance.md     (45 lines -- vague advice like "write fast code")
  imports.md         (30 lines -- restates ESLint import rules)
  comments.md        (25 lines -- Claude already adds good comments)
  types.md           (95 lines -- half is TypeScript tutorial)
Total: 800 lines, 12 files
```

### After (score 92/100) -- 180 lines, 4 files

```
.claude/rules/
  api.md             (55 lines, scoped to src/api/**)
  database.md        (45 lines, scoped to src/db/**)
  testing.md         (40 lines, scoped to **/*.test.ts)
  universal.md       (40 lines, unscoped -- truly universal rules)
Total: 180 lines, 4 files
```

**What was removed:**
- `naming.md`: deleted (ESLint handles this, Claude defaults are fine)
- `errors.md` + `exceptions.md`: merged into `api.md` with explicit conditions
- `logging.md`: merged into `api.md`, scoped to `src/api/**`
- `security.md`: deleted (Claude already knows OWASP basics)
- `performance.md`: deleted (vague, unenforceable)
- `imports.md`: deleted (ESLint handles this)
- `comments.md`: deleted (Claude already writes good comments)
- `types.md`: reduced to 10 lines of project-specific type rules in `universal.md`

**Savings**: 800 -> 180 lines = **78% reduction**. Token cost per interaction dropped from ~3,200 to ~720.

## 8. Quality Checklist

Before shipping rules, verify:

- [ ] Every rule follows the golden format: imperative + consequence + mechanism
- [ ] Positive framing (no "Don't..." as the primary instruction)
- [ ] Every rule passes the 30-second enforceability test
- [ ] Total across all rule files < 500 lines
- [ ] Rules scoped via `paths:` frontmatter (e.g., `paths: ["src/api/**/*.ts"]`) when not universally applicable
- [ ] No contradictions between rule files
- [ ] No rules that Claude follows by default from training
- [ ] No rules that a linter already enforces (reference the linter instead)
