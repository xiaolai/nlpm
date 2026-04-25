# NLPM Audit: ruvnet/ruflo

**Date**: 2026-04-25  |  **Artifacts**: 84  |  **Strategy**: batched
**NL Score**: 60/100
**Bugs**: 12  |  **Quality Issues**: 14

---

## Security Gate

**Result: CRITICAL — 4 patterns matched. Contribution blocked.**

| # | File | Severity | Pattern | Description |
|---|------|----------|---------|-------------|
| 1 | `plugin/hooks/hooks.json:193` | critical | `permission-auto-approve` | `PermissionRequest` hook auto-approves ALL `mcp__claude-flow__*` tools, bypassing Claude Code's permission system for every MCP call including `terminal_execute` (arbitrary shell execution). |
| 2 | `v3/@claude-flow/cli/src/mcp-tools/github-tools.ts:220` | high | `exec-string-interpolation` | `run()` calls `execSync` with a shell string interpolating unsanitized user inputs (`title`, `body`, `baseBranch`, `headBranch`). Double-quote escaping leaves `$()` and backtick expansion open. |
| 3 | `v3/@claude-flow/cli/src/mcp-tools/github-tools.ts:249` | high | `exec-string-interpolation` | `prNumber` and `issueNumber` interpolated into shell strings with no quoting or validation (lines 249, 263, 342, 358). |
| 4 | `v3/@claude-flow/cli/src/mcp-tools/terminal-tools.ts:170` | high | `execsync-user-input` | `terminal_execute` MCP tool passes user-supplied `command` string directly to `execSync` without `shell: false`. Combined with the auto-approve PermissionRequest hook, any MCP client can run arbitrary shell commands without user prompts. |
| 5 | `v3/@claude-flow/cli/.claude/agents/v3/adaptive-coordinator.md` | high | `tmp-path-predictable` | Post hook writes model to `/tmp/adaptive-model-$(date +%s).json` — predictable path enables symlink race on shared hosts. |
| 6 | `v3/@claude-flow/cli/.claude/agents/v3/security-auditor.md` | medium | `tmp-path-predictable` | Hook writes to `/tmp/audit_results` — fixed path, no per-invocation uniqueness. |
| 7 | `v3/@claude-flow/cli/src/services/container-worker-pool.ts:444` | medium | `exec-array-join-shell` | `execAsync(\`docker ${args.join(' ')}\`)` — array elements joined into a shell command string; metacharacter injection if any element is attacker-controlled. |
| 8 | `.claude/mcp.json` | low | `mcp-absolute-path` | MCP server loaded from `/workspaces/flow-cloud/mcp/flow-nexus-sse/mcp-server-supabase.js` — absolute dev-container path, not portable and unauditable from this repo. |

---

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `v3/@claude-flow/cli/.claude/agents/optimization/benchmark-suite.md` | agent | 45 | Missing model, examples, output format, no hooks, max vague cap |
| `v3/@claude-flow/cli/.claude/agents/optimization/load-balancer.md` | agent | 45 | Missing model, examples, output format, no hooks, max vague cap |
| `v3/@claude-flow/cli/.claude/agents/optimization/performance-monitor.md` | agent | 45 | Missing model, examples, output format, no hooks, max vague cap |
| `v3/@claude-flow/cli/.claude/agents/optimization/resource-allocator.md` | agent | 45 | Missing model, examples, output format, no hooks, max vague cap |
| `v3/@claude-flow/cli/.claude/agents/optimization/topology-optimizer.md` | agent | 45 | Missing model, examples, output format, no hooks, max vague cap |
| `v3/@claude-flow/mcp/.claude/agents/consensus/quorum-manager.md` | agent | 50 | Missing model, examples, output format, max vague cap |
| `v3/@claude-flow/mcp/.claude/agents/consensus/performance-benchmarker.md` | agent | 50 | Missing model, examples, output format, max vague cap |
| `v3/@claude-flow/mcp/.claude/agents/consensus/byzantine-coordinator.md` | agent | 50 | Missing model, examples, output format, max vague cap |
| `v3/@claude-flow/mcp/.claude/agents/consensus/raft-manager.md` | agent | 50 | Missing model, examples, output format, max vague cap |
| `v3/@claude-flow/mcp/.claude/agents/consensus/security-manager.md` | agent | 50 | Missing model, examples, output format, max vague cap |
| `v3/@claude-flow/mcp/.claude/agents/consensus/gossip-coordinator.md` | agent | 50 | Missing model, examples, output format, max vague cap |
| `v3/@claude-flow/mcp/.claude/agents/consensus/crdt-synchronizer.md` | agent | 50 | Missing model, examples, output format, max vague cap |
| `v3/@claude-flow/cli/.claude/agents/swarm/adaptive-coordinator.md` | agent | 50 | Missing model, examples, output format + broken MCP shell calls in hooks |
| `v3/@claude-flow/cli/.claude/agents/swarm/hierarchical-coordinator.md` | agent | 50 | Missing model, examples, output format + broken MCP shell calls in hooks |
| `v3/@claude-flow/cli/.claude/agents/swarm/mesh-coordinator.md` | agent | 50 | Missing model, examples, output format + broken MCP shell calls in hooks |
| `v3/@claude-flow/mcp/.claude/agents/v3/v3-integration-architect.md` | agent | 50 | Missing model, examples, output format, max vague cap |
| `v3/@claude-flow/mcp/.claude/agents/v3/collective-intelligence-coordinator.md` | agent | 50 | Missing model, output format, broken subshell in hooks |
| `v3/@claude-flow/mcp/.claude/agents/v3/security-auditor.md` | agent | 50 | Missing model, examples, output format, max vague cap |
| `v3/@claude-flow/mcp/.claude/agents/v3/security-architect.md` | agent | 50 | Missing model, examples, output format, max vague cap |
| `v3/@claude-flow/cli/.claude/agents/github/github-modes.md` | agent | 52 | Missing model, examples, output format, moderate vague |
| `v3/@claude-flow/cli/.claude/agents/github/pr-manager.md` | agent | 52 | Missing model, examples, output format + undefined bash functions in hooks |
| `v3/@claude-flow/cli/.claude/agents/github/issue-tracker.md` | agent | 52 | Missing model, examples, output format + undefined bash functions in hooks |
| `v3/@claude-flow/cli/.claude/agents/github/release-manager.md` | agent | 52 | Missing model, examples, output format + undefined bash functions in hooks |
| `v3/@claude-flow/cli/.claude/agents/goal/goal-planner.md` | agent | 58 | Missing model, examples, output format, moderate vague |
| `v3/@claude-flow/cli/.claude/agents/goal/agent.md` | agent | 58 | Missing model, examples, output format, moderate vague |
| `v3/@claude-flow/mcp/.claude/agents/v3/ddd-domain-expert.md` | agent | 58 | Missing model, examples, output format, moderate vague |
| `v3/@claude-flow/mcp/.claude/agents/v3/aidefence-guardian.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/mcp/.claude/agents/v3/reasoningbank-learner.md` | agent | 60 | Missing model, examples (frontmatter), output format |
| `v3/@claude-flow/mcp/.claude/agents/v3/pii-detector.md` | agent | 62 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/flow-nexus/app-store.md` | agent | 60 | Missing model, examples, output format, type |
| `v3/@claude-flow/cli/.claude/agents/flow-nexus/authentication.md` | agent | 60 | Missing model, examples, output format, type |
| `v3/@claude-flow/cli/.claude/agents/flow-nexus/challenges.md` | agent | 60 | Missing model, examples, output format, type |
| `v3/@claude-flow/cli/.claude/agents/flow-nexus/neural-network.md` | agent | 60 | Missing model, examples, output format, type |
| `v3/@claude-flow/cli/.claude/agents/flow-nexus/payments.md` | agent | 60 | Missing model, examples, output format, type |
| `v3/@claude-flow/cli/.claude/agents/flow-nexus/sandbox.md` | agent | 60 | Missing model, examples, output format, type |
| `v3/@claude-flow/cli/.claude/agents/flow-nexus/swarm.md` | agent | 60 | Missing model, examples, output format, type |
| `v3/@claude-flow/cli/.claude/agents/flow-nexus/user-tools.md` | agent | 60 | Missing model, examples, output format, type |
| `v3/@claude-flow/cli/.claude/agents/flow-nexus/workflow.md` | agent | 60 | Missing model, examples, output format, type |
| `v3/@claude-flow/cli/.claude/agents/core/coder.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/core/reviewer.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/core/tester.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/core/planner.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/core/researcher.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/sparc/specification.md` | agent | 60 | Missing model, examples, output format + undefined `memory_store` in hooks |
| `v3/@claude-flow/cli/.claude/agents/sparc/architecture.md` | agent | 60 | Missing model, examples, output format + undefined `memory_store` in hooks |
| `v3/@claude-flow/cli/.claude/agents/sparc/pseudocode.md` | agent | 60 | Missing model, examples, output format + undefined `memory_store` in hooks |
| `v3/@claude-flow/cli/.claude/agents/sparc/refinement.md` | agent | 60 | Missing model, examples, output format + undefined `memory_store` in hooks |
| `v3/@claude-flow/cli/.claude/agents/templates/memory-coordinator.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/github/code-review-swarm.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/github/workflow-automation.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/github/repo-architect.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/github/swarm-issue.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/github/project-board-sync.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/github/sync-coordinator.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/github/multi-repo-swarm.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/github/swarm-pr.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/github/release-swarm.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/testing/tdd-london-swarm.md` | agent | 62 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/testing/production-validator.md` | agent | 62 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/analysis/analyze-code-quality.md` | agent | 62 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/analysis/code-analyzer.md` | agent | 60 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/specialized/spec-mobile-react-native.md` | agent | 62 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/development/dev-backend-api.md` | agent | 62 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/documentation/docs-api-openapi.md` | agent | 62 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/devops/ops-cicd-github.md` | agent | 62 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/data/data-ml-model.md` | agent | 62 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/sona/sona-learning-optimizer.md` | agent | 64 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/custom/test-long-runner.md` | agent | 66 | Missing model, frontmatter examples |
| `.claude/agents/python-specialist.md` | agent | 70 | Missing model, examples, output format; body is 5 lines |
| `.claude/agents/v3/v3-security-architect.md` | agent | 58 | Missing model, examples, output format |
| `.claude/agents/v3/v3-integration-architect.md` | agent | 50 | Missing model, examples, output format, max vague cap |
| `.claude/agents/v3/python-specialist.md` | agent | 70 | Missing model, examples, output format |
| `v3/@claude-flow/cli/.claude/agents/analysis/code-review/analyze-code-quality.md` | agent | 62 | Duplicate of analysis/analyze-code-quality.md |
| `v3/@claude-flow/cli/.claude/agents/development/backend/dev-backend-api.md` | agent | 62 | Duplicate of development/dev-backend-api.md |
| `v3/@claude-flow/cli/.claude/agents/devops/ci-cd/ops-cicd-github.md` | agent | 62 | Duplicate of devops/ops-cicd-github.md |
| `v3/@claude-flow/cli/.claude/agents/specialized/mobile/spec-mobile-react-native.md` | agent | 62 | Duplicate of specialized/spec-mobile-react-native.md |
| `v3/@claude-flow/cli/.claude/agents/data/ml/data-ml-model.md` | agent | 62 | Duplicate of data/data-ml-model.md |
| `v3/@claude-flow/cli/.claude/agents/documentation/api-docs/docs-api-openapi.md` | agent | 62 | Duplicate of documentation/docs-api-openapi.md |
| `v3/@claude-flow/cli/.claude/agents/architecture/arch-system-design.md` | agent | 87 | Missing model only — best-in-repo |
| `v3/@claude-flow/cli/.claude/agents/architecture/system-design/arch-system-design.md` | agent | 87 | Duplicate of architecture/arch-system-design.md |

---

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `v3/@claude-flow/cli/.claude/agents/github/pr-manager.md` | Hooks call undefined bash functions `calculate_pr_success` and `validate_pr_merge` | Hooks silently fail; success/failure tracking never executes |
| 2 | `v3/@claude-flow/cli/.claude/agents/github/issue-tracker.md` | Hook calls undefined bash function `calculate_review_quality` | Same — post-task learning never fires |
| 3 | `v3/@claude-flow/cli/.claude/agents/github/release-manager.md` | Hook calls undefined bash function `calculate_release_quality` | Same — release metrics never stored |
| 4 | `v3/@claude-flow/cli/.claude/agents/sparc/specification.md` | Hook calls `memory_store "sparc_phase" "specification"` — bare function, not a shell built-in | SPARC phase tracking silently drops |
| 5 | `v3/@claude-flow/cli/.claude/agents/sparc/architecture.md` | Hook calls `memory_store "sparc_phase" "architecture"` and `memory_search "pseudo_complete"` | Same |
| 6 | `v3/@claude-flow/cli/.claude/agents/sparc/pseudocode.md` | Hook calls `memory_store` (undefined function) | Same |
| 7 | `v3/@claude-flow/cli/.claude/agents/sparc/refinement.md` | Hook calls `memory_store` (undefined function) | Same |
| 8 | `v3/@claude-flow/cli/.claude/agents/swarm/adaptive-coordinator.md` | Pre/post hooks invoke `mcp__claude-flow__swarm_init auto`, `mcp__claude-flow__neural_patterns analyze`, etc. as bash commands — these are MCP tool identifiers, not executables | All hook coordination silently fails; no swarm init or learning occurs |
| 9 | `v3/@claude-flow/cli/.claude/agents/swarm/hierarchical-coordinator.md` | Same: `mcp__claude-flow__swarm_init hierarchical`, `mcp__claude-flow__swarm_monitor` as bash | Same |
| 10 | `v3/@claude-flow/cli/.claude/agents/swarm/mesh-coordinator.md` | Same: `mcp__claude-flow__swarm_init mesh`, `mcp__claude-flow__daa_communication` as bash | Same |
| 11 | `v3/@claude-flow/mcp/.claude/agents/v3/collective-intelligence-coordinator.md` | Post hook uses `$(mcp__claude-flow__swarm_status \| jq ...)` — subshell executing an MCP tool name as a bash command | Hook writes garbage or empty strings to memory; learning pipeline is corrupted |
| 12 | `v3/@claude-flow/cli/.claude/agents/analysis/code-analyzer.md` | `name: analyst` in frontmatter contradicts body title "Code Analyzer Agent" and differs from CLAUDE.md agent registry entry `code-analyzer` | Agent won't route correctly to this file by name |

---

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | All 84 agent files | `model` field absent from every frontmatter block — agents cannot be routed to appropriate Claude tier | -5 each |
| 2 | 82 of 84 agent files | Zero frontmatter `examples:` blocks — no input/output pairs anywhere in frontmatter; orchestrators cannot validate agent behavior from metadata alone | -15 each |
| 3 | 82 of 84 agent files | `output_format` field absent — agents give no structural contract for what they produce | -10 each |
| 4 | `v3/@claude-flow/cli/.claude/agents/swarm/adaptive-coordinator.md` | Vague quantifiers cap: "intelligent", "optimal", "appropriate", "dynamic", "adaptive", "efficiently" (≥10 instances) | -20 |
| 5 | `v3/@claude-flow/mcp/.claude/agents/consensus/quorum-manager.md` | Vague quantifiers cap: "appropriate", "optimal", "intelligent", "properly", "efficiently" (≥10 instances) | -20 |
| 6 | `v3/@claude-flow/cli/.claude/agents/optimization/benchmark-suite.md` | No hooks section; agent is a pure JS-class reference file with frontmatter wrapper — minimal behavioral guidance | -10 (output format) |
| 7 | `v3/@claude-flow/cli/.claude/agents/optimization/topology-optimizer.md` | Same as above — JS implementation masquerading as behavioral agent | -10 |
| 8 | `v3/@claude-flow/cli/.claude/agents/flow-nexus/app-store.md` | Missing `type` field (all 9 flow-nexus agents) | informational |
| 9 | `v3/@claude-flow/cli/.claude/agents/github/github-modes.md` | `tools:` value is a comma-separated inline string rather than a YAML list — valid per rubric but harder to parse programmatically | informational |
| 10 | `v3/@claude-flow/cli/.claude/agents/core/coder.md` | Vague comments inside capabilities: "NEW v3.0.0-alpha.1 capabilities" — `self_learning`, `context_enhancement`, `fast_processing` are not Claude Code capability identifiers | informational |
| 11 | `v3/@claude-flow/cli/.claude/agents/sparc/specification.md` | `sparc_phase: specification` is a non-standard frontmatter field with no known consumer | informational |
| 12 | `.claude/agents/python-specialist.md` | Body is 5 lines — no examples, no tools, no hooks; agent provides almost no behavioral guidance | -15 (examples) |
| 13 | `v3/@claude-flow/mcp/.claude/agents/v3/aidefence-guardian.md` | Hook invokes `npx claude-flow@v3alpha memory store` in pre/post — correct CLI form, but `singleton: true` and `auto_spawn` are non-standard fields with no known consumer | informational |
| 14 | `v3/@claude-flow/cli/.claude/agents/templates/memory-coordinator.md` | Entirely prose with no examples and no tool declarations — template is not self-illustrating | -15 (examples) |

---

## Cross-Component

| # | Finding | Affected Files | Severity |
|---|---------|---------------|----------|
| 1 | **Massive duplication**: 14 agent files appear under both `v3/@claude-flow/mcp/.claude/agents/consensus/` and `.claude/agents/consensus/` with identical content. Additionally 6+ agents appear in nested subdirectories mirroring their parent (e.g., `analysis/analyze-code-quality.md` and `analysis/code-review/analyze-code-quality.md`). Total duplicate pairs: ~20. | Multiple | high |
| 2 | **Claude Flow MCP server missing from `.claude/mcp.json`**: Agents extensively reference `mcp__claude-flow__*` tools (swarm_init, memory_usage, performance_report, neural_patterns, etc.) but `.claude/mcp.json` only registers the `flow-nexus` server. The claude-flow MCP server is registered separately per CLAUDE.md (`claude mcp add claude-flow ...`) — which means these tools are absent in a fresh clone with no MCP setup, breaking every hook that calls them. | `v3/@claude-flow/cli/.claude/agents/swarm/`, `v3/@claude-flow/mcp/.claude/agents/v3/`, all hooks using mcp__claude-flow__* | high |
| 3 | **`npx agentic-flow` referenced in agent hooks but not in dependencies**: `v3/@claude-flow/cli/.claude/agents/github/code-review-swarm.md` and `templates/memory-coordinator.md` call `npx agentdb-cli pattern store/search`. The package `agentdb-cli` does not appear in `v3/@claude-flow/cli/package.json` direct dependencies — it is a transitive dependency of `agentdb`, which is not guaranteed stable. | `github/code-review-swarm.md`, `templates/memory-coordinator.md` | medium |
| 4 | **CLAUDE.md agent count discrepancy**: Root `CLAUDE.md` declares "16 agent roles + custom types" and "60+ agent types" but the audit found 84 agent `.md` files (including ~20 duplicates). After deduplication: ~64 unique agents, but many are categorized differently from the CLAUDE.md inventory table. | `CLAUDE.md` vs `v3/@claude-flow/cli/.claude/agents/**` | low |
| 5 | **`npx claude-flow@alpha` vs `npx claude-flow@v3alpha` inconsistency**: Core agents (`coder.md`, `reviewer.md`, etc.) use `npx claude-flow@v3alpha` while SPARC agents use `npx claude-flow@alpha memory search-patterns` (a v2-era subcommand that no longer exists in v3). | `v3/@claude-flow/cli/.claude/agents/sparc/*.md` | medium |

---

## Recommendation

The agent library scores 60/100 on average — dragged down by a single universal gap (no `model`, `examples`, or `output_format` fields on any agent) and a structural problem where 10+ hooks reference MCP tool identifiers as shell commands, silently failing at runtime. The security gate is CRITICAL: the `PermissionRequest` auto-approve hook plus an unrestricted `terminal_execute` MCP tool together allow any MCP client to execute arbitrary shell commands without user confirmation — this must be resolved before any automated contribution is opened.
