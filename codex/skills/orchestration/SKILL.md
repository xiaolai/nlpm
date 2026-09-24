---
name: orchestration
description: Multi-agent workflow patterns for Claude Code -- parallel dispatch, sequential pipelines, QC gates, retry loops, shared partials. Use when designing systems with multiple agents, commands, or processing stages.
metadata:
  version: 0.1.0
---

# Orchestration

> Scope: covers multi-agent workflow design. For individual agent authoring, see [[writing-agents]]. For plugin architecture, see [[writing-plugins]].

## 1. Four Orchestration Patterns

### Pattern A: Parallel Dispatch

Multiple agents run simultaneously on independent work. A command dispatches them via the Task tool and synthesizes results.

```
Command dispatches via Task:
  |-- agent-1 (analyzes security)
  |-- agent-2 (analyzes performance)
  |-- agent-3 (analyzes architecture)
  --> Command synthesizes all results into final report
```

**Use when**: agents don't depend on each other's output.

**Real examples**:
- grill plugin: 6 review agents analyze code from different angles in parallel
- docs-guardian: 4 agents (staleness, accuracy, coverage, quality) run simultaneously

**Implementation pattern in command body**:
```markdown
## Execution
1. Dispatch the following agents in parallel using Task:
   - security-agent: analyze for vulnerabilities
   - performance-agent: analyze for bottlenecks
   - architecture-agent: analyze for structural issues
2. Collect all agent outputs
3. Synthesize into a unified report with cross-references
```

**Key decisions**:
| Decision | Recommendation |
|----------|---------------|
| Max parallel agents | 6 (diminishing returns above this) |
| Timeout per agent | 120 seconds for sonnet, 300 for opus |
| Failure handling | Continue with other agents if one fails |
| Result merging | Deduplicate findings that appear in multiple agents |

### Pattern B: Sequential Pipeline

Each stage feeds into the next. Output of stage N is input to stage N+1.

```
parse --> chunk --> summarize --> QC --> output
```

**Use when**: each stage depends on the previous stage's output.

**Real examples**:
- reading-assistant: parse PDF -> chunk content -> summarize chunks -> QC summaries -> output
- tdd-guardian: discover tests -> run tests -> check coverage -> analyze failures -> report -> enforce

**Implementation pattern**:
```markdown
## Execution
### Phase 1: Parse (haiku)
1. Scan input files
2. Extract structured content
3. Output: parsed data as JSON

### Phase 2: Process (sonnet)
4. Receive parsed data from Phase 1
5. Analyze and transform
6. Output: processed results

### Phase 3: QC (sonnet)
7. Verify Phase 2 output meets quality bar
8. Output: pass/warn/fail verdict

### Phase 4: Output
9. If QC passed: format and deliver final report
10. If QC failed: report failures and stop
```

**Key decisions**:
| Decision | Recommendation |
|----------|---------------|
| Phase boundary | Each phase should have a clear input type and output type |
| Error propagation | Fail fast -- don't continue past a failed phase |
| State passing | Use structured output (JSON) between phases |
| Resumability | Track phase status for long pipelines (see section 4) |

### Pattern C: QC Gate

AI processing followed by quality verification before output reaches the user.

```
Phase 1: Mechanical prep (haiku)
Phase 2: AI work (sonnet)
Phase 3: QC verification (sonnet/opus)
  --> pass: proceed to output
  --> warn: output with warnings
  --> fail: stop, report issues
Phase 4: Output
```

**Use when**: AI output needs verification before the user sees it.

**Threshold design**:
| Verdict | Condition | Action |
|---------|-----------|--------|
| PASS | All checks green | Deliver output directly |
| WARN | Minor issues (< 3 low-severity) | Deliver output with warnings section |
| FAIL | Any critical finding OR > 5 total findings | Stop, report what failed, suggest re-run |

**Real examples**:
- reading-assistant: QC agents verify summaries for accuracy, completeness, fidelity
- codex-toolkit audit-fix: audit -> fix -> verify loop

### Pattern D: Retry Loop

On failure, re-dispatch with error context. The agent gets a second chance with specific feedback about what went wrong.

```
agent produces output
  --> QC checks output
    --> pass: done
    --> fail: re-dispatch agent with error context
      --> QC re-checks
        --> pass: done
        --> fail (attempt 2): re-dispatch again
          --> max retries reached: fail with report
```

**Use when**: quality failures are recoverable by re-trying with more context.

**Implementation**:
```markdown
## Retry Protocol
- Max retries: 3
- On retry, include in the agent prompt:
  - Previous output (or summary if too long)
  - Specific failures from QC
  - Instruction: "Fix ONLY the listed failures. Do not change passing sections."
- If max retries exhausted: output best attempt with failure annotations
```

**Key decisions**:
| Decision | Recommendation |
|----------|---------------|
| Max retries | 3 (rarely succeeds after 3 if it failed 3 times) |
| Error context | Include specific failures, not "try again" |
| Scope of retry | Fix only failures, preserve passing output |
| Cost cap | Each retry costs full agent invocation -- budget accordingly |

## 2. Shared Partials for DRY

Extract common logic into `commands/shared/*.md` with `user-invocable: false` in frontmatter.

### When to Extract

| Situation | Extract? |
|-----------|----------|
| Same logic in 3+ commands | Yes -- always extract |
| Same logic in 2 commands, complex (> 20 lines) | Yes -- extract |
| Same logic in 2 commands, simple (< 10 lines) | No -- duplication is fine |
| Logic used by 1 command but might be reused | No -- wait until it's actually reused |

### Good Candidates for Extraction

| Partial | What it contains | Who includes it |
|---------|-----------------|-----------------|
| `shared/load-config.md` | Read and validate plugin config file | All commands that need config |
| `shared/discover-files.md` | Find target files by pattern/extension | Commands that scan the repo |
| `shared/validate-prereqs.md` | Check tool availability, environment | Commands with external dependencies |
| `shared/format-report.md` | Common report header, footer, severity colors | Commands that output reports |

### Partial File Structure

```yaml
---
user-invocable: false
description: "Shared config loading logic — reads and validates the plugin config file"
---
```

```markdown
## Config Loading

1. Look for `.config.md` in the project root
2. If not found, look for `.config.yaml`
3. If neither found, output error: "Run `/plugin:init` first to create a config file"
4. Parse the config file
5. Validate required fields: [list fields]
6. Return parsed config
```

## 3. Cost Gates

For expensive AI pipelines, add a cost estimation step between mechanical prep and AI processing.

### Implementation

```
Phase 1: Parse and discover (haiku -- cheap)
  --> Count items to process
  --> Estimate cost: items x model cost per item
  --> Display estimate to user

User confirms or adjusts scope

Phase 2: AI processing (sonnet/opus -- expensive)
  --> Process confirmed scope
```

### Cost Estimation Table

| Model | Approx cost per item | 10 items | 100 items | 1000 items |
|-------|---------------------|----------|-----------|------------|
| haiku | $0.001 | $0.01 | $0.10 | $1.00 |
| sonnet | $0.01 | $0.10 | $1.00 | $10.00 |
| opus | $0.03 | $0.30 | $3.00 | $30.00 |

"Item" = one agent invocation processing one unit of work (one file, one chunk, one artifact).

### User Confirmation Pattern

```markdown
## Cost Gate
After Phase 1, display:
- Items to process: {N}
- Estimated model: {model}
- Estimated cost: ~${amount}
- Estimated time: ~{minutes} minutes

Ask: "Proceed with {N} items? (You can reduce scope with --filter)"
```

## 4. Pipeline State

For resumable pipelines (long-running, expensive, or failure-prone), track state in a JSON file.

### State File Schema

```json
{
  "pipeline": "my-pipeline",
  "startedAt": "2024-01-15T10:00:00Z",
  "configFingerprint": "sha256:abc123",
  "phases": {
    "parse": {
      "status": "completed",
      "startedAt": "2024-01-15T10:00:00Z",
      "completedAt": "2024-01-15T10:00:05Z",
      "itemsProcessed": 42,
      "output": "parse-output.json"
    },
    "analyze": {
      "status": "running",
      "startedAt": "2024-01-15T10:00:06Z",
      "itemsProcessed": 15,
      "itemsTotal": 42
    },
    "qc": {
      "status": "pending"
    }
  },
  "lock": {
    "pid": 12345,
    "acquiredAt": "2024-01-15T10:00:00Z"
  }
}
```

### State Transitions

```
pending --> running --> completed
                   --> failed
                   --> skipped (if previous phase failed)
```

### Resumability Rules

1. On start: check for existing state file
2. If state exists and `configFingerprint` matches: resume from last incomplete phase
3. If state exists and `configFingerprint` differs: warn user, offer fresh start or resume
4. If lock exists: check if PID is alive. If dead, clear stale lock. If alive, abort.

## 5. Model Tier Allocation

Assign models by cognitive load, not by importance.

```
Mechanical / IO:     haiku    (parser, scanner, formatter, counter)
Reasoning / AI:      sonnet   (summarizer, extractor, reviewer, linter)
Judgment / QC:       opus     (coordinator, architect, final reviewer)
```

### Pipeline Model Assignment Example

```
Phase 1: Discover files          → haiku  (just glob + read)
Phase 2: Parse and chunk         → haiku  (mechanical splitting)
Phase 3: Analyze each chunk      → sonnet (requires judgment)
Phase 4: QC all analyses         → sonnet (verify, not create)
Phase 5: Synthesize final report → opus   (cross-reference, prioritize)
```

### Cost Optimization

| Optimization | How | Savings |
|-------------|-----|---------|
| Batch mechanical work | One haiku call processes all files, not one per file | 5-10x |
| Pre-filter before AI | Use grep/glob to skip irrelevant files before sonnet | 2-5x |
| Cache phase outputs | Don't re-run completed phases on retry | 1-3x |
| Scope reduction | Let user filter to subset before expensive phases | Variable |

## 6. Error Propagation

### Rules

1. **Phase fails -> STOP.** Set status "failed" + error message in state. Do not continue to next phase.
2. **Agent fails -> report and continue** (in parallel dispatch). One agent's failure shouldn't block others.
3. **Retry fails -> escalate.** After max retries, surface the failure to the user with full context.
4. **Never swallow errors silently.** Every failure must be visible in the final output.

### Error Report Format

```markdown
## Pipeline Error

**Phase**: {phase_name}
**Status**: FAILED
**Error**: {error_message}

### Context
- Items processed before failure: {N} of {M}
- Last successful item: {item_id}
- Time elapsed: {duration}

### Recovery Options
1. Fix the finding and run `/command --resume` to continue from this phase
2. Run `/command --restart` to start fresh
3. Run `/command --skip-phase {phase_name}` to skip this phase (not recommended)
```

### Fallback Paths

Always offer a manual fallback when automation fails:

```markdown
## Fallback
If the pipeline fails after 3 retries:
1. Output all successfully processed items
2. List failed items with error context
3. Suggest manual analysis for failed items
```

## 7. Pattern Selection Guide

| Your situation | Pattern | Why |
|---------------|---------|-----|
| Multiple independent analyses of same input | A: Parallel | No dependencies, maximize throughput |
| Each step needs previous step's output | B: Sequential | Data flows in one direction |
| AI output must be verified before delivery | C: QC Gate | Catch errors before user sees them |
| Quality failures are recoverable with feedback | D: Retry | Cheaper than manual re-run |
| Complex multi-stage with verification | B + C | Pipeline with QC gates between expensive phases |
| Multiple analyses with quality bar | A + C | Parallel dispatch, then QC all results |
