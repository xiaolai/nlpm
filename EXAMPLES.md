# NLPM Examples

Real before/after examples showing NLPM improving actual artifacts. Each example shows the original artifact, the issues detected, the fixes applied, and the resulting score improvement.

---

## Example 1: Fixing a Weak Agent (29 --> 92)

### Before

```markdown
---
name: code-reviewer
description: "Helps with code review"
model: opus
tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebSearch"]
---

You are a code review assistant. Look at the code and provide appropriate
feedback. Check for issues as needed and make sure the code follows relevant
best practices. Handle edge cases properly and suggest improvements where
you see fit.
```

### Score breakdown: 29/100

| Penalty | Points | Rule |
|---------|--------|------|
| Zero `<example>` blocks | -15 | R09 |
| Description names no situation the agent is not for | -5 | R09 |
| Description is generic ("Helps with code review" -- 0 specific phrases) | -15 | R04 |
| `opus` for a code review task (sonnet is the correct tier for analysis) | -5 | R10 |
| Write and Edit declared on a review agent (read-only task) | -10 | R11 |
| WebSearch declared but never referenced in body | -3 | R11 |
| No output format defined | -10 | R12 |
| "appropriate" without criteria | -2 | R01 |
| "as needed" without criteria | -2 | R01 |
| "relevant" without criteria | -2 | R01 |
| "properly" without criteria | -2 | R01 |
| **Total penalties** | **-71** | |

### After

```markdown
---
name: code-reviewer
description: |
  Reviews pull request diffs for correctness, performance, and maintainability
  issues. Use when reviewing a PR before merge, auditing code changes for
  security vulnerabilities, or checking that new code follows project
  conventions. Not for fixing the code or running tests; it reports only.

  <example>
  Context: Developer reviewing a teammate's PR that adds a new API endpoint
  user: Review the changes in this PR for the /api/users endpoint
  assistant: I'll review the PR diff for the /api/users endpoint, checking
  correctness, error handling, and security patterns...

  ## Code Review: /api/users endpoint

  ### Summary
  3 files changed | 2 issues found | 1 suggestion

  ### Issues
  | File | Line | Severity | Finding |
  |------|------|----------|---------|
  | src/api/users.ts | 42 | High | SQL injection: user input interpolated into query |
  | src/api/users.ts | 67 | Medium | Missing error handler for database timeout |

  ### Suggestions
  - src/api/users.ts:23 -- Extract validation logic into `validateUserInput()` for reuse
  </example>
model: sonnet
color: green
tools: ["Read", "Glob", "Grep", "Bash"]
---

You are a code review agent. Read the specified files or diff and analyze
each change for correctness, performance, security, and maintainability.

## Steps

1. Read the target files or PR diff
2. For each changed function or block, check:
   - Correctness: logic errors, off-by-one, null handling
   - Security: injection, auth bypass, data exposure
   - Performance: N+1 queries, unnecessary allocations, missing indexes
   - Maintainability: naming, duplication, complexity >10 cyclomatic
3. Classify each finding as High, Medium, or Low severity
4. Generate the report in the format below

## Output Format

### Summary
N files changed | N issues found | N suggestions

### Issues
| File | Line | Severity | Finding |
|------|------|----------|---------|

### Suggestions
- file:line -- description

## Boundaries

Do not modify any files. Do not run tests. Report only -- all changes
require human approval.
```

### Score breakdown: 92/100

| Check | Points | Notes |
|-------|--------|-------|
| Description: 3+ specific phrases | 0 | "reviewing a PR", "auditing code changes for security", "checking conventions" |
| 1 `<example>` block | 0 | Context + user + assistant; one is full credit |
| "Not for" clause | 0 | "Not for fixing the code or running tests" |
| Description ≤1,200 characters | 0 | Examples included |
| Model: sonnet for analysis | 0 | Correct tier |
| Tools: only Read, Glob, Grep, Bash | 0 | No Write/Edit on a read-only agent |
| Output format defined | 0 | Table structure specified |
| No vague quantifiers | 0 | All criteria are specific |
| Minor: Bash declared, body does not explicitly invoke it | -3 | One unused tool |
| Minor: no scope note | -5 | No cross-reference to related agents |
| **Final** | **92/100** | |

### What changed

- **Description**: "Helps with code review" --> 3 specific trigger phrases (+15)
- **Examples**: Added 1 full example with context, user message, and assistant response (+15)
- **Exclusion**: Added "Not for fixing the code or running tests" to the description (+5)
- **Model**: opus --> sonnet (correct tier for analysis work, +5)
- **Tools**: Removed Write, Edit, WebSearch; kept only read-path tools (+13)
- **Output format**: Added table structure with severity levels (+10)
- **Vague language**: Replaced "appropriate", "as needed", "relevant", "properly" with specific criteria (+8)

---

## Example 2: Fixing Bloated Rules (38 --> 88)

### Before

```markdown
Don't use var in JavaScript. Always use const or let.

Don't write functions longer than 50 lines. Break them up into smaller
pieces that are more manageable and easier to test.

Don't use any in TypeScript. Always use proper types.

Don't forget to handle errors. Every async function should have try/catch
or .catch(). Make sure error messages are appropriate and helpful.

Don't use console.log in production code. Use a proper logging library
like pino or winston. Configure it appropriately.

Don't commit code without tests. Every new function needs at least one
unit test. Tests should cover the relevant edge cases and be comprehensive.

Don't use magic numbers. Extract them into named constants that clearly
describe what the value represents. This makes the code more readable
and maintainable for other developers.

Don't use default exports. Always use named exports so that imports are
consistent and refactoring tools work properly across the codebase.

Don't skip code review. Every PR needs at least one approval before
merging. Reviewers should check for appropriate test coverage, code
quality, and adherence to our standards.

Don't ignore TypeScript errors. Fix them properly instead of using
@ts-ignore or any. If you truly need to suppress an error, use
@ts-expect-error with a comment explaining why.

Ensure all API endpoints validate input appropriately before processing.
Use zod or joi for schema validation. Handle validation errors with
proper HTTP status codes.

Make sure database queries are optimized and don't cause N+1 problems.
Use eager loading when fetching related data. Index columns that appear
in WHERE clauses.
```

**120 lines** (part of a project with 600 total lines of rules).

### Score breakdown: 38/100

| Penalty | Points | Rule |
|---------|--------|------|
| Missing frontmatter (no `description`) | -10 | R21 |
| No bold imperative format | -5 | R21 |
| No rationale on any rule | -10 | R21 |
| Not enforceable: "more manageable", "comprehensive", "clearly describe" | -10 | R22 |
| Duplicates eslint (`no-var`, `no-console`, `@typescript-eslint/no-explicit-any`) | -10 | R24 |
| "appropriate" x3, "properly" x3, "relevant" x1 = 7 vague quantifiers | -14 | R01 |
| No path scoping | -3 | R25 |
| **Total penalties** | **-62** | |

### After

```markdown
---
description: "TypeScript API project conventions: error handling, validation, database queries, exports"
paths: ["src/**/*.ts"]
---

**Use named exports exclusively.** Default exports break automated refactoring (rename-symbol misses them) and produce inconsistent import names across the codebase. Enforced by `eslint-plugin-import/no-default-export`.

**Wrap every async call in error handling with context.** Unhandled rejections crash the process. Pattern:
```ts
try {
  const user = await db.users.findById(id);
} catch (err) {
  throw new AppError("Failed to fetch user", { cause: err, userId: id });
}
```

**Validate all API inputs with zod at the controller boundary.** Unvalidated input causes runtime crashes deep in business logic where the error message is useless. Pattern:
```ts
const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

// In controller
const body = CreateUserSchema.parse(req.body);  // throws ZodError with field-level details
```
Return 400 with the zod error `.issues` array on validation failure.

**Use `.include()` or `$fetchGraph()` for related data -- never loop queries.** A loop that queries inside a `.map()` produces N+1 database calls. Fix:
```ts
// N+1 (bad)
const orders = await db.orders.findAll();
for (const order of orders) {
  order.items = await db.items.findByOrderId(order.id);  // N queries
}

// Eager load (good)
const orders = await db.orders.findAll({ include: [{ model: Item }] });  // 1 query
```

**Suppress TypeScript errors only with `@ts-expect-error` + a tracking comment.** `@ts-ignore` silently hides errors that may become real bugs after refactoring. `@ts-expect-error` fails if the underlying error is fixed, which is the desired behavior. Always add why:
```ts
// @ts-expect-error -- legacy API returns untyped JSON, tracked in PROJ-1234
const data = legacyApi.fetch();
```
```

**32 lines** (down from 120, freeing 88 lines of rules budget).

### Score breakdown: 88/100

| Check | Points | Notes |
|-------|--------|-------|
| Frontmatter with description | 0 | Present and specific |
| Bold imperative format on every rule | 0 | All 5 rules use it |
| Rationale on every rule | 0 | Each explains why |
| Enforceable: all rules have specific, testable criteria | 0 | Can verify in code review |
| No tooling duplication | 0 | References eslint rule instead of restating it |
| Path-scoped | 0 | `src/**/*.ts` |
| Vague quantifiers: zero | 0 | All replaced with specifics |
| Minor: could reference related rules file for test conventions | -5 | |
| Minor: 5 rules covering broad scope | -7 | Could benefit from tighter scope per file |
| **Final** | **88/100** | |

### What changed

- **Frontmatter**: Added description and path scope (+13)
- **Format**: "Don't use X" --> "**Use Y.** Without it, Z breaks because W" (+15)
- **Deduplication**: Removed 6 rules that eslint already enforces (+10)
- **Specificity**: Replaced vague criteria with code examples and measurable conditions (+24)
- **Size**: 120 lines --> 32 lines (freed 88 lines of the 500-line budget)

---

## Example 3: Sharpening a Skill Description (55 --> 90)

### Before

```markdown
---
name: react-patterns
description: "Useful React skill for component development"
version: 0.1.0
---

# React Patterns

This skill covers React development patterns and best practices.

## Components

Components should be well-structured and maintainable. Here are some
guidelines for writing good components.

### Function Components

Use function components with hooks. Class components are discouraged.

Example:
```
function MyComponent(props) {
  // handle state
  const [data, setData] = useState()

  // handle effects
  useEffect(() => {
    // fetch data or something
  })

  // render
  return <div>{/* component JSX */}</div>
}
```

### State Management

State should be managed appropriately. Use useState for local state
and useContext or a state library for global state. Choose the right
approach for your situation.

### Performance

Performance is important. Use React.memo, useMemo, and useCallback
when appropriate to prevent unnecessary re-renders. Profile your
components to find bottlenecks.

### Error Boundaries

Wrap components in error boundaries to handle errors gracefully.

### Testing

Test your components thoroughly. Use React Testing Library for
component tests and write tests that reflect how users interact
with the component.

[... continues for 520 total lines with similar density ...]
```

### Score breakdown: 55/100

| Penalty | Points | Rule |
|---------|--------|------|
| Description is generic ("Useful React skill" -- 0 specific phrases) | -15 | R04 |
| Over 500 lines | -10 | R05 |
| Code examples are pseudocode (`// fetch data or something`, `{/* component JSX */}`) | -5 | R06 |
| No scope note (related skills not mentioned) | -3 | R07 |
| "appropriately" without criteria | -2 | R01 |
| "appropriate" without criteria | -2 | R01 |
| "thoroughly" without criteria | -2 | R01 |
| "gracefully" without criteria | -2 | R01 |
| Theory-heavy, pattern-light (abstract advice without concrete situations) | -4 | R08 |
| **Total penalties** | **-45** | |

### After

```markdown
---
name: react-patterns
description: "React component patterns for Claude Code. Use when debugging React re-renders, fixing hook dependency arrays, optimizing with useMemo/useCallback, implementing error boundaries with recovery, or structuring components with the container/presenter split."
version: 0.2.0
---

# React Component Patterns

Patterns for writing, debugging, and optimizing React function components.

> **Scope:** Covers component structure, hooks, performance, and error handling. For routing patterns, see `react-routing`. For server components and RSC patterns, see `react-server`.

## Re-render Debugging

When a component re-renders unexpectedly, check these three causes in order:

### 1. Unstable reference in parent

```tsx
// Bug: items is a new array on every parent render, causing Child to re-render
function Parent() {
  return <Child items={data.filter(d => d.active)} />;
}

// Fix: stabilize with useMemo
function Parent() {
  const items = useMemo(() => data.filter(d => d.active), [data]);
  return <Child items={items} />;
}
```

### 2. Missing dependency in useEffect

```tsx
// Bug: effect runs on every render because fetchUser is recreated each time
function Profile({ userId }: { userId: string }) {
  const fetchUser = () => api.get(`/users/${userId}`);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]); // new reference every render = infinite loop

  // Fix: move function inside effect, depend on primitive
  useEffect(() => {
    api.get(`/users/${userId}`);
  }, [userId]); // stable primitive dependency
}
```

### 3. Context causing subtree re-renders

```tsx
// Bug: every consumer re-renders when ANY value in context changes
const AppContext = createContext({ user: null, theme: 'light', locale: 'en' });

// Fix: split into focused contexts
const UserContext = createContext<User | null>(null);
const ThemeContext = createContext<'light' | 'dark'>('light');
```

## Error Boundaries with Recovery

```tsx
class ErrorBoundary extends Component<
  { fallback: ReactNode; onReset?: () => void; children: ReactNode },
  { error: Error | null }
> {
  state = { error: null };

  static getDerivedStateFromError(error: Error) {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    reportError(error, info.componentStack);
  }

  reset = () => {
    this.setState({ error: null });
    this.props.onReset?.();
  };

  render() {
    if (this.state.error) {
      return (
        <div role="alert">
          <p>Something broke: {this.state.error.message}</p>
          <button onClick={this.reset}>Try again</button>
        </div>
      );
    }
    return this.props.children;
  }
}

// Usage: wrap route-level components
<ErrorBoundary fallback={<CrashPage />} onReset={() => queryClient.clear()}>
  <Dashboard />
</ErrorBoundary>
```

## Container/Presenter Split

Separate data fetching (container) from rendering (presenter) to make components testable without mocking APIs:

```tsx
// Presenter: pure rendering, easy to test and storybook
function UserCard({ name, avatar, role }: UserCardProps) {
  return (
    <div className="user-card">
      <img src={avatar} alt={name} />
      <h3>{name}</h3>
      <span className="role">{role}</span>
    </div>
  );
}

// Container: handles data fetching
function UserCardContainer({ userId }: { userId: string }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => api.getUser(userId),
  });

  if (isLoading) return <UserCardSkeleton />;
  if (error) return <UserCardError error={error} />;
  return <UserCard name={data.name} avatar={data.avatar} role={data.role} />;
}
```

[... total: 390 lines, all with runnable code examples ...]
```

### Score breakdown: 90/100

| Check | Points | Notes |
|-------|--------|-------|
| Description: 5 specific trigger phrases | 0 | "debugging re-renders", "hook dependency arrays", "useMemo/useCallback", "error boundaries", "container/presenter" |
| Under 500 lines (390) | 0 | Within limit |
| Code examples: all runnable tsx with real types | 0 | No pseudocode |
| Scope note: references react-routing and react-server | 0 | Clear boundaries |
| Vague quantifiers: zero | 0 | All criteria specific |
| Pattern-first: each section starts with a situation | 0 | "When a component re-renders unexpectedly" |
| Minor: could add more cross-references | -5 | |
| Minor: 3 sections could link to external React docs | -5 | |
| **Final** | **90/100** | |

### What changed

- **Description**: "Useful React skill" --> 5 specific trigger phrases (+15)
- **Size**: 520 --> 390 lines (trimmed filler, kept density, +10)
- **Examples**: Pseudocode --> runnable tsx with types and real patterns (+5)
- **Scope note**: Added cross-references to related skills (+3)
- **Structure**: Theory-first --> situation-first pattern teaching (+4)
- **Vague language**: Removed "appropriately", "appropriate", "thoroughly", "gracefully" (+8)

---

## Example 4: Cross-Component Check Catches a Bug

Running `/nlpm:check` on a plugin produces this output:

```
NLPM Cross-Component Check

References
--------------------------------------------------------------
BROKEN  commands/process.md:8 references commands/shared/helpers.md
        -- file not found (renamed to commands/shared/utilities.md)

BROKEN  agents/analyzer.md frontmatter lists skill "nlpm:linting"
        -- skill not found (renamed to "nlpm:scoring")

Orphans
--------------------------------------------------------------
ORPHAN  commands/shared/legacy-format.md
        -- not referenced by any command (dead partial)

Contradictions
--------------------------------------------------------------
CONFLICT  .claude/rules/testing.md:3 says "Run tests with pnpm test"
          CLAUDE.md:45 says "Run tests with npm test"
          -- same concept, different commands

--------------------------------------------------------------
2 broken references | 1 orphan | 1 contradiction
```

### Fix 1: Broken partial reference

The `commands/shared/helpers.md` file was renamed to `commands/shared/utilities.md` during a refactor, but `commands/process.md` still references the old name.

**In `commands/process.md`:**
```diff
- @commands/shared/helpers.md
+ @commands/shared/utilities.md
```

### Fix 2: Broken skill reference

The `skills/nlpm/linting/` directory was renamed to `skills/nlpm/scoring/`, but the agent frontmatter still lists the old name.

**In `agents/analyzer.md`:**
```diff
  skills:
-   - "nlpm:linting"
+   - "nlpm:scoring"
```

### Fix 3: Orphaned partial

`commands/shared/legacy-format.md` was used by a command that was deleted two versions ago. The partial itself was never cleaned up. Since nothing references it, delete it:

```bash
git rm commands/shared/legacy-format.md
```

### Fix 4: Contradicting test commands

CLAUDE.md says `npm test` while a rules file says `pnpm test`. The project uses pnpm (confirmed by `pnpm-lock.yaml` in the repo root). Fix CLAUDE.md:

**In `CLAUDE.md`:**
```diff
- Run tests with npm test
+ Run tests with pnpm test
```

After fixing all four issues, `/nlpm:check` reports clean:

```
NLPM Cross-Component Check

0 broken references | 0 orphans | 0 contradictions
All clear.
```

---

## Example 5: Trend Report Catches Regression

Running `/nlpm:trend` after a week of work on a plugin:

```
NLPM Trend Report

Snapshot: 2026-03-28 (4th snapshot, 3 previous)

File                              Score   Previous  Delta
--------------------------------------------------------------
agents/scorer.md                  95      92        +3 improved
agents/scanner.md                 90      90         0 unchanged
commands/score.md                 95      88        +7 improved
commands/check.md                 90      87        +3 improved
commands/fix.md                   92      92         0 unchanged
commands/ls.md                    88      88         0 unchanged
skills/nlpm/scoring/SKILL.md      90      90         0 unchanged
skills/nlpm/rules/SKILL.md        92      92         0 unchanged
.claude/rules/testing.md          70      82       -12 DEGRADED

Overall: 89/100 (was 88, +1)

Degraded (needs attention):
  .claude/rules/testing.md  82 -> 70 (-12)
    Penalties added since last snapshot:
    -  "as needed" without criteria (-2)  [line 23]
    -  "properly" without criteria (-2)   [line 31]
    -  "appropriate" without criteria (-2) [line 38]
    -  Rationale removed from rule 4 (-10) [line 27]
    +  Removed tooling duplication (+4)    [line 15]
    Net: -12

Trend: 4 snapshots -- 82 -> 85 -> 88 -> 89 (improving)

Action items:
  1. .claude/rules/testing.md regressed -12 -- review recent edits
     Likely cause: refactor on 2026-03-27 added vague language and
     removed a rationale block
```

### What happened

Most files improved or held steady. The overall score went from 88 to 89. But `.claude/rules/testing.md` dropped 12 points because during a refactor on March 27th, someone:

1. Added "as needed", "properly", and "appropriate" to three rules (3 vague quantifiers = -6)
2. Removed the rationale from rule 4, leaving just the imperative with no "why" (-10)
3. Did remove a duplicate eslint rule, which gained back +4

Net result: -12 on that file.

### The fix

Open `.claude/rules/testing.md` and:

1. Replace "as needed" on line 23 with the specific condition: "when the function has more than 2 code paths"
2. Replace "properly" on line 31 with the specific pattern: "using `expect().toThrow(SpecificError)`"
3. Replace "appropriate" on line 38 with the specific criteria: "covering the happy path and each error path"
4. Restore the rationale on rule 4: "Without a rationale, developers treat the rule as arbitrary and skip it during time pressure."

After fixing, `/nlpm:score .claude/rules/testing.md` shows `70 -> 86 (+16)`, recovering past the previous high of 82.
