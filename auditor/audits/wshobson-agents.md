# Audit Report: wshobson/agents

**Repo**: wshobson/agents  
**Stars**: 33K  
**Artifacts audited**: 100 (64 agents + 36 commands)  
**Audit date**: 2026-04-17  
**Auditor**: NLPM auditor pipeline  
**Overall NL Score**: **82 / 100** (Gold tier)

---

## NL Score Summary

Scores use the 100-point scale: −25 missing `name`, −25 missing `description`, −5 missing `model`, −15 zero examples, −5 one example, −10 missing output format, −5 missing `allowed-tools` (commands), −10 no empty-input handling, −2 per vague quantifier (cap −20).

| Plugin | Artifacts | Avg Score | Notes |
|--------|-----------|-----------|-------|
| agent-teams | 4 agents | 91 | All Opus tier, read-only reviewers correct |
| startup-business-analyst | 4 (1a+3c) | 90 | Commands have allowed-tools ✓ |
| comprehensive-review | 3 agents | 90 | High quality; code-reviewer duplicated elsewhere |
| frontend-mobile-development | 2 agents | 90 | Solid |
| data-validation-suite | 1 agent | 90 | Solid |
| python-development | 3 agents | 90 | All Opus, good examples |
| observability-monitoring | 4 agents | 90 | performance-engineer duplicated |
| database-design | 2 agents | 91 | |
| performance-testing-review | 2 agents | 91 | |
| dotnet-contribution | 1 agent | 92 | |
| conductor | 7 (1a+6c) | 88 | Commands lack allowed-tools (−5 each) |
| ui-design | 3 agents | 88 | |
| llm-application-dev | 6 (3a+3c) | 86 | Commands lack allowed-tools |
| distributed-debugging | 2 agents | 86 | |
| game-development | 2 agents | 86 | minecraft-bukkit-pro lacks examples |
| reverse-engineering | 3 agents | 86 | No formal "Example Interactions" |
| customer-sales-automation | 2 agents | 85 | sales-automator lacks examples |
| functional-programming | 2 agents | 84 | elixir-pro/haskell-pro no example section |
| c4-architecture | 5 (4a+1c) | 84 | c4-architecture command missing frontmatter |
| debugging-toolkit | 2 agents | 83 | No formal example interactions |
| seo-analysis-monitoring | 3 agents | 80 | No formal example interactions |
| tdd-workflows | 4 commands | 80 | tdd-refactor missing frontmatter; rest good |
| code-documentation | 3 agents | 85 | code-reviewer duplicated |
| jvm-languages | 3 agents | 81 | scala-pro has zero examples (−15) |
| arm-cortex-microcontrollers | 1 agent | 82 | tools: [] (empty array) |
| dependency-management | 1 agent | 82 | |
| database-migrations | 2 commands | 82 | tool_access field (non-standard) |
| block-no-verify | 1 command | 87 | |
| full-stack-orchestration | 1 command | 87 | Borderline OVER_CONSTRAINED |
| application-performance | 1 command | 87 | |
| framework-migration | 3 commands | 67 | code-migrate + deps-upgrade missing frontmatter |
| deployment-validation | 2 (1a+1c) | 74 | config-validate missing frontmatter |
| meigen-ai-design | 3 agents | 72 | **All 3 agents missing `name` field — BUGS** |
| protect-mcp | 1 hook | — | See Security Scan |
| security-scanning | 2 agents | 55 | **threat-modeling-expert: NO frontmatter — BUG** |
| accessibility-compliance | 1 command | 57 | **Missing frontmatter — BUG** |
| codebase-cleanup | 3 commands | 57 | **All 3 missing frontmatter — BUGS** |
| database-cloud-optimization | 1 command | 57 | **Missing frontmatter — BUG** |
| javascript-typescript | 1 command | 57 | **Missing frontmatter — BUG** |
| systems-programming | 1 command | 57 | **Missing frontmatter — BUG** |
| error-diagnostics | 3 commands | 57 | **All 3 missing frontmatter — BUGS** |

**Agent average**: 86 / 100  
**Command average**: 74 / 100  
**Overall weighted average**: **82 / 100**

---

## Security Scan

Scanned: 1 hook file, 2 shell scripts, 20+ Python scripts, 1 requirements.txt. No `.mcp.json` or `package.json` found.

| Severity | File | Pattern | Finding |
|----------|------|---------|---------|
| MEDIUM | `plugins/protect-mcp/hooks/hooks.json` | Runtime install + broad matcher | `npx protect-mcp@latest` runs on every tool call (all tools, `".*"` matcher). Downloads and executes npm package code at runtime without version pinning. Intentional security tool but introduces supply-chain risk. |
| LOW | `plugins/protect-mcp/hooks/hooks.json` | Unpinned dependency | `protect-mcp@latest` — version can change silently. Should pin to a specific version (e.g., `protect-mcp@1.2.3`). |
| LOW | `tools/requirements.txt` | Loose version constraints | All 5 deps use `>=` (min version only), not exact pins. Acceptable for tools but increases reproducibility risk. |

No CRITICAL or HIGH severity findings. Shell scripts (`validate-chart.sh`) are clean — no dangerous patterns, proper `set -e`, no credential handling.

---

## Bugs

Issues that break registration or core functionality.

| # | File | Issue | Impact |
|---|------|-------|--------|
| B-01 | `plugins/security-scanning/agents/threat-modeling-expert.md` | No YAML frontmatter at all (file starts with `# Threat Modeling Expert`) | Agent will not register — name, description, model all missing. Score: 20/100. |
| B-02 | `plugins/meigen-ai-design/agents/prompt-crafter.md` | Missing `name` field in frontmatter | Agent registration broken; Claude Code cannot identify this agent. |
| B-03 | `plugins/meigen-ai-design/agents/gallery-researcher.md` | Missing `name` field in frontmatter | Same as B-02. |
| B-04 | `plugins/meigen-ai-design/agents/image-generator.md` | Missing `name` field in frontmatter | Same as B-02. All 3 meigen agents share this bug. |
| B-05 | `plugins/deployment-validation/commands/config-validate.md` | No YAML frontmatter (starts with `# Configuration Validation`) | Command not registered; slash command unavailable. |
| B-06 | `plugins/c4-architecture/commands/c4-architecture.md` | No YAML frontmatter (starts with `# C4 Architecture Documentation Workflow`) | Command not registered. |
| B-07 | `plugins/systems-programming/commands/rust-project.md` | No YAML frontmatter (starts with `# Rust Project Scaffolding`) | Command not registered. |
| B-08 | `plugins/framework-migration/commands/code-migrate.md` | No YAML frontmatter (starts with `# Code Migration Assistant`) | Command not registered. |
| B-09 | `plugins/framework-migration/commands/deps-upgrade.md` | No YAML frontmatter (starts with `# Dependency Upgrade Strategy`) | Command not registered. |
| B-10 | `plugins/accessibility-compliance/commands/accessibility-audit.md` | No YAML frontmatter (starts with `# Accessibility Audit and Testing`) | Command not registered. |
| B-11 | `plugins/codebase-cleanup/commands/tech-debt.md` | No YAML frontmatter | Command not registered. |
| B-12 | `plugins/codebase-cleanup/commands/deps-audit.md` | No YAML frontmatter | Command not registered. |
| B-13 | `plugins/codebase-cleanup/commands/refactor-clean.md` | No YAML frontmatter | Command not registered. |
| B-14 | `plugins/database-cloud-optimization/commands/cost-optimize.md` | No YAML frontmatter | Command not registered. |
| B-15 | `plugins/javascript-typescript/commands/typescript-scaffold.md` | No YAML frontmatter | Command not registered. |
| B-16 | `plugins/tdd-workflows/commands/tdd-refactor.md` | No YAML frontmatter (starts with plain prose) | Command not registered; breaks tdd-workflows plugin symmetry. |
| B-17 | `plugins/error-diagnostics/commands/error-trace.md` | No YAML frontmatter | Command not registered. |
| B-18 | `plugins/error-diagnostics/commands/error-analysis.md` | No YAML frontmatter | Command not registered. |
| B-19 | `plugins/error-diagnostics/commands/smart-debug.md` | No YAML frontmatter | Command not registered. |

**19 bugs total**: 4 agent registration failures, 15 command registration failures.

**Root cause pattern**: The missing-frontmatter commands all contain rich, detailed content (100–1000+ lines of code examples) but were never wrapped in YAML frontmatter. This suggests a batch authoring workflow where frontmatter was added inconsistently.

---

## Security Fixes

No CRITICAL or HIGH security issues found. The one actionable fix:

| # | File | Severity | Fix |
|---|------|----------|-----|
| S-01 | `plugins/protect-mcp/hooks/hooks.json` | MEDIUM | Pin `protect-mcp` to a specific version instead of `@latest` to prevent silent supply-chain changes. Change `npx protect-mcp@latest` → `npx protect-mcp@<pinned-version>`. |

---

## Quality Issues

Issues that reduce effectiveness but don't break registration.

| # | File(s) | Issue | Penalty |
|---|---------|-------|---------|
| Q-01 | `plugins/security-scanning/agents/security-auditor.md` | Identical copy of `plugins/comprehensive-review/agents/security-auditor.md` — full duplication, no differentiation | Maintenance burden; changes must be applied twice |
| Q-02 | `plugins/code-documentation/agents/code-reviewer.md` | Identical copy of `plugins/comprehensive-review/agents/code-reviewer.md` | Same as Q-01 |
| Q-03 | `plugins/observability-monitoring/agents/performance-engineer.md` | Identical copy of `plugins/performance-testing-review/agents/performance-engineer.md` | Same as Q-01 |
| Q-04 | `plugins/jvm-languages/agents/scala-pro.md` | Zero example interactions — the "Output" section lists capability areas but no concrete example prompts | −15 (zero examples) |
| Q-05 | `plugins/database-migrations/commands/sql-migrations.md`, `migration-observability.md` | Use `tool_access:` field instead of standard `allowed-tools:`. Claude Code likely ignores this non-standard field. | Non-standard — tools not enforced |
| Q-06 | 30+ commands across all plugins | Missing `allowed-tools` declaration — commands can invoke any tool, circumventing least-privilege intent | −5 per command |
| Q-07 | `plugins/arm-cortex-microcontrollers/agents/arm-cortex-expert.md` | `tools: []` (empty array) — agent has no tool access, cannot read files or search code; severely limits usefulness for a deep-technical embedded systems agent | Functionally crippled |
| Q-08 | `plugins/full-stack-orchestration/commands/full-stack-feature.md`, `plugins/tdd-workflows/commands/tdd-cycle.md`, `plugins/application-performance/commands/performance-optimization.md`, `plugins/tdd-workflows/commands/tdd-red.md`, `plugins/tdd-workflows/commands/tdd-green.md` | CRITICAL BEHAVIORAL RULES blocks with 10–15 MUST/DO NOT/NEVER imperatives — borderline OVER_CONSTRAINED (threshold: >15) | Near-threshold; reduces model flexibility |
| Q-09 | `plugins/functional-programming/agents/elixir-pro.md`, `haskell-pro.md`, `plugins/jvm-languages/agents/csharp-pro.md`, `plugins/game-development/agents/minecraft-bukkit-pro.md`, and 8 others | No formal "## Example Interactions" section — output format present but examples missing | −5 (one example) or −15 (zero examples) |
| Q-10 | `plugins/arm-cortex-microcontrollers/agents/arm-cortex-expert.md` | Uses `model: inherit` for deeply technical embedded/ARM Cortex firmware work. CLAUDE.md tier guide assigns Opus for production coding and architecture. | Model tier mismatch |

---

## Cross-Component Analysis

### Plugin-Level Bug Clusters

Three plugins have uniform registration failures across all their commands, suggesting batch authoring without frontmatter:

- **codebase-cleanup**: 3/3 commands broken (tech-debt, deps-audit, refactor-clean)
- **error-diagnostics**: 3/3 commands broken (error-trace, error-analysis, smart-debug)
- **meigen-ai-design**: 3/3 agents broken (all missing `name` field) — the only plugin with this specific failure mode

### Duplication Topology

Three agents exist verbatim in two locations each:

```
comprehensive-review/agents/security-auditor.md
    └── security-scanning/agents/security-auditor.md  [exact copy — Q-01]

comprehensive-review/agents/code-reviewer.md
    └── code-documentation/agents/code-reviewer.md    [exact copy — Q-02]

performance-testing-review/agents/performance-engineer.md
    └── observability-monitoring/agents/performance-engineer.md  [exact copy — Q-03]
```

The `comprehensive-review` plugin appears to be the canonical source for security-auditor and code-reviewer. The other copies should either be removed or differentiated with domain-specific focus.

### Orchestration Command Quality Gap

The 5 orchestration commands that use phased workflows with checkpoints (full-stack-feature, tdd-cycle, performance-optimization, tdd-red, tdd-green) are the highest-quality commands in the repo — excellent state management, interactive Q&A, parallel agent dispatch, and resume capability. The contrast with the 15 commands missing frontmatter entirely is sharp. Half the command portfolio is non-functional.

### Allowed-Tools Consistency

The `startup-business-analyst` plugin is the only non-orchestration plugin to properly declare `allowed-tools` on its commands, earning the highest command scores (92). The other 30+ commands all omit `allowed-tools`. This is a repo-wide pattern, not an isolated oversight.

### Model Tier Alignment

Agent model assignments are generally appropriate:
- Opus: security-auditor, code-reviewer, architect-review, team-*, malware-analyst, firmware-analyst, java-pro, python-pro, fastapi-pro, django-pro, database-architect, unity-developer, minecraft-bukkit-pro — appropriate for production-grade work
- Sonnet: cloud-architect, c4-context, c4-container, c4-component, backend-security-coder, dotnet-architect, network-engineer, docs-architect, tutorial-engineer, debugger, dx-optimizer, seo-authority-builder, legacy-modernizer — appropriate for docs/testing/debugging
- Haiku: c4-code, seo-cannibalization-detector, seo-content-refresher, customer-support, sales-automator — appropriate for fast/simple ops
- Inherit: most complex generalist agents — user-controlled, acceptable

One exception: `arm-cortex-expert` uses `inherit` but the depth of knowledge (bare-metal programming, interrupt vectors, DMA, RTOS) suggests Opus is more appropriate.

---

## Recommendation

**Approve with required fixes before production use.**

wshobson/agents is a high-quality, comprehensive plugin marketplace with 33K stars well-deserved. The **agent portfolio (avg 86/100, Gold tier)** is strong: rich capability descriptions, appropriate model tier selection, thorough output formats, and several standout orchestration agents (`full-stack-feature`, `tdd-cycle`, `performance-optimization`) that represent best-in-class multi-agent workflow design.

The **command portfolio (avg 74/100)** has a significant structural problem: **15 of 36 commands have no YAML frontmatter and will silently fail to register**. Users installing this plugin will find roughly 40% of slash commands simply absent with no error message. This is the primary issue to fix.

### Required before contribution PR:

1. **Add frontmatter to 15 broken commands** (B-05 through B-19) — a mechanical fix, no content changes needed. Minimum required:
   ```yaml
   ---
   description: "One sentence explaining what this command does"
   ---
   ```

2. **Add `name` field to 3 meigen agents** (B-02, B-03, B-04) — one-line fix per file.

3. **Add frontmatter to threat-modeling-expert** (B-01) — needs name, description, and model.

4. **Pin protect-mcp version** (S-01) — supply chain hygiene.

### Recommended quality improvements (non-blocking):

5. Remove or differentiate the 3 duplicate agents (Q-01 through Q-03).
6. Add `allowed-tools` to conductor and llm-application-dev commands.
7. Fix `arm-cortex-expert` tools: remove `tools: []` and set `model: opus`.
8. Fix `tool_access:` → `allowed-tools:` in database-migrations commands.
9. Add example interactions to scala-pro, haskell-pro, csharp-pro, elixir-pro.

Once B-01 through B-04 are fixed, the agent portfolio is contribution-ready. The command portfolio needs the frontmatter sweep first.
