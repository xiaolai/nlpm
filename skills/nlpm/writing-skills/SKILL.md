---
name: writing-skills
description: "How to write SKILL.md files that trigger reliably and teach effectively — crafting trigger descriptions, structuring YAML frontmatter, organizing body sections, and using progressive disclosure. Use when creating, improving, or reviewing Claude Code skills, writing skill files, building custom skills, or writing skill descriptions."
version: 0.1.0
---

# Writing Skills

> Scope: covers SKILL.md authoring. For agent writing, see [[writing-agents]]. For plugin architecture, see [[writing-plugins]].

## 1. The Description is Everything

The `description` field determines when Claude loads this skill. It is not a summary -- it is a **trigger mechanism**.

**Bad:**
```yaml
description: "Helpful skill for React development"
```

**Good:**
```yaml
description: "Use when building React components, debugging re-renders, optimizing performance with useMemo/useCallback, or fixing hook dependency arrays"
```

### Description Checklist

| Criterion | Test |
|-----------|------|
| 3+ trigger phrases | Count distinct action phrases separated by commas |
| Action-oriented | Starts with "Use when..." or "How to..." |
| Includes tool/framework name | The technology name appears explicitly |
| Matches real queries | Would a user's actual question contain any of your trigger words? |

### Trigger Phrase Construction

Map real user queries to trigger phrases:

| User says | Trigger phrase to include |
|-----------|--------------------------|
| "My component re-renders too much" | "debugging re-renders" |
| "How do I memoize this?" | "optimizing performance with useMemo/useCallback" |
| "My useEffect runs in a loop" | "fixing hook dependency arrays" |
| "I need a new component for..." | "building React components" |

**Rule**: if you can't list 3 real user queries that match your description, rewrite it.

## 2. Body Structure

### Section Order

1. **Scope note** (if related skills exist) -- tells Claude when to use THIS skill vs another
2. **Most commonly needed patterns** -- what users ask about 80% of the time
3. **Decision matrices** -- when to use A vs B (tables)
4. **Worked examples** -- before/after with scores
5. **Common mistakes** -- anti-patterns to avoid
6. **References** -- links to deep dives

### Heading Rules

- H1 (`#`): skill title only (one per file)
- H2 (`##`): major sections (numbered: `## 1. Section Name`)
- H3 (`###`): subsections within a major section
- Never skip heading levels (no H2 followed directly by H4)

### Code Examples

Every code example must show the **problem**, then the **solution**:

```markdown
### Bad (breaks on concurrent requests)
` ` `python
global_state = {}  # shared mutable state
` ` `

### Good (request-scoped)
` ` `python
def handler(request):
    state = {}  # local to this request
` ` `
```

**Rules for code examples:**
- Runnable, not pseudocode
- Contextual -- show enough surrounding code to understand placement
- Annotated -- comment the critical line, not every line

## 3. Progressive Disclosure

Keep SKILL.md under 500 lines. Use the file system for depth:

```
skills/my-domain/my-skill/
  SKILL.md          # core patterns (< 500 lines)
  references/       # deep dives, edge cases, full API docs
    advanced.md
    api-reference.md
  examples/         # working code samples
    basic-setup.ts
    advanced-config.ts
  scripts/          # utility scripts
    validate.sh
```

### When to Extract to references/

| Content type | Keep in SKILL.md? | Extract to references/? |
|-------------|-------------------|------------------------|
| Top 5 patterns everyone needs | Yes | No |
| Full API reference (50+ entries) | No | Yes |
| Edge cases (< 5% of users) | No | Yes |
| Configuration matrix (20+ options) | No | Yes |
| Quick decision table (< 10 rows) | Yes | No |

## 4. Worked Example: Improving a Skill

### Before

```yaml
---
name: docker-helper
description: "Information about Docker"
version: 0.1.0
---
```

```markdown
# Docker Helper

Docker is a containerization platform. Here are some useful commands.

## Commands
- `docker build` - builds an image
- `docker run` - runs a container
- `docker ps` - lists containers

## Dockerfile
A Dockerfile contains instructions for building an image.

## Docker Compose
Docker Compose is for multi-container applications.
```

**Problems:**
- Description is a label, not a trigger mechanism (0 trigger phrases)
- Body teaches theory Claude already knows from training
- No code examples showing problem/solution
- No decision matrices
- No scope note

### After

```yaml
---
name: docker-helper
description: "Use when writing Dockerfiles, debugging container networking, optimizing image size with multi-stage builds, or configuring Docker Compose services. Covers build cache, volume mounts, health checks, and compose profiles."
version: 0.1.0
---
```

```markdown
# Docker Helper

> Scope: covers Docker CLI, Dockerfiles, and Compose. For Kubernetes deployment, see [[k8s-deploy]].

## 1. Image Size Optimization

Problem/solution pair showing multi-stage builds, then a decision table for base image selection.

## 2. Base Image Selection

| Use case | Base image | Size |
|----------|-----------|------|
| Node.js production | node:20-slim | 180 MB |
| Python production | python:3.12-slim | 150 MB |
| Static files only | nginx:alpine | 40 MB |
| From scratch (Go/Rust) | scratch | < 20 MB |
```

**Changes made:**
1. Description: 0 trigger phrases -> 8 trigger phrases
2. Scope note added
3. Replaced theory with problem/solution examples
4. Added decision matrix
5. Removed content Claude knows from training (-15 lines)

## 5. Common Mistakes

| Mistake | Why it hurts | Fix |
|---------|-------------|-----|
| Description is a feature list | Claude can't match user queries to the skill | Rewrite as trigger phrases starting with "Use when..." |
| Body teaches theory | Wastes tokens on content Claude already knows | Show patterns and decisions, not definitions |
| Over 500 lines | Bloats context window, penalized by linters | Extract to references/, keep core patterns only |
| No scope note | Claude doesn't know when to use THIS skill vs a related one | Add scope note referencing related skills |
| Pseudocode examples | Not actionable, can't be copy-pasted | Use runnable code with enough context |
| Every section has equal weight | Buries the most useful content | Lead with the 80% patterns, push edge cases to references/ |

## 6. Quality Checklist

Before shipping a skill, verify:

- [ ] Description has 3+ specific trigger phrases
- [ ] Description starts with "Use when..." or "How to..."
- [ ] Scope note present (if related skills exist)
- [ ] H2 sections numbered, H3 subsections under them
- [ ] Code examples show problem then solution
- [ ] Decision tables for A-vs-B choices
- [ ] Total lines < 500
- [ ] No content Claude already knows from training
- [ ] At least one worked example with before/after
