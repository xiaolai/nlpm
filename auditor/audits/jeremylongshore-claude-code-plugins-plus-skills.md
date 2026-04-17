# Audit: jeremylongshore/claude-code-plugins-plus-skills

**NL Score**: 73/100
**Security**: REVIEW
**Artifacts**: 105 (31 agents, 74 commands)
**Bugs**: 18 mechanical issues requiring fixes
**Quality Issues**: 67 non-blocking quality improvements
**Security Findings**: 9 (0 critical, 2 high, 5 medium, 2 low)
**Audited**: 2026-04-17

---

## NL Score Summary

| Artifact | Type | Score | Top Penalty |
|----------|------|-------|-------------|
| `.claude/agents/skill-auditor.md` | agent | 30 | No YAML frontmatter at all (-70) |
| `workspace/lab/schema-optimization/agents/phase_1.md` | agent | 30 | No YAML frontmatter at all (-70) |
| `workspace/lab/schema-optimization/agents/phase_2.md` | agent | 30 | No YAML frontmatter at all (-70) |
| `workspace/lab/schema-optimization/agents/phase_3.md` | agent | 30 | No YAML frontmatter at all (-70) |
| `workspace/lab/schema-optimization/agents/phase_4.md` | agent | 30 | No YAML frontmatter at all (-70) |
| `workspace/lab/schema-optimization/agents/phase_5.md` | agent | 30 | No YAML frontmatter at all (-70) |
| `backups/.../backup-strategy-implementor/commands/backup-strategy.md` | command | 20 | Shell substitution in YAML frontmatter (-25 name, -25 desc, broken template) |
| `backups/.../sync-agent-context/commands/sync-agent-context.md` | command | 40 | No YAML frontmatter at all (-50 name+desc, -5 no allowed-tools) |
| `backups/.../overnight-setup/commands/overnight-setup.md` | command | 55 | Missing name (-25), no allowed-tools (-5), no model |
| `backups/.../discovery/commands/discovery.md` | command | 55 | Missing name (-25), no allowed-tools (-5), no model |
| `backups/.../sow/commands/sow.md` | command | 55 | Missing name (-25), no allowed-tools (-5), no model |
| `backups/.../make-builder/commands/make-builder.md` | command | 55 | Missing name (-25), no allowed-tools (-5), no model |
| `backups/.../zap/commands/zap.md` | command | 55 | Missing name (-25), no allowed-tools (-5), no model |
| `backups/.../n8n-builder/commands/n8n-builder.md` | command | 55 | Missing name (-25), no allowed-tools (-5), no model |
| `backups/.../roi/commands/roi.md` | command | 55 | Missing name (-25), no allowed-tools (-5), no model |
| `backups/.../mobile-test/commands/mobile-test.md` | command | 55 | Missing name (-25), no allowed-tools (-5), no model |
| `backups/.../fuzz-api/commands/fuzz-api.md` | command | 55 | Missing name (-25), no allowed-tools (-5), no model |
| `backups/.../generate-tests/commands/generate-tests.md` | command | 55 | Missing name (-25), no allowed-tools (-5), no model |
| `backups/.../scan-movers/commands/scan-movers.md` | command | 60 | Missing name (-25), no allowed-tools (-5), no empty-input (-10) |
| `backups/.../commit-smart/commands/commit-smart.md` | command | 60 | Missing name (-25), no allowed-tools (-5), no model |
| `templates/full-plugin/agents/example.md` | agent | 70 | No examples (-15), stub body (-10), model commented out (-5) |
| `plugins/database/nosql-data-modeler/agents/nosql-agent.md` | agent | 70 | No `<example>` blocks (-15), no output format section (-10), no model (-5) |
| `plugins/database/data-validation-engine/agents/validation-agent.md` | agent | 70 | No examples (-15), no output format (-10), no model (-5) |
| `backups/.../devops/commands/cloud-cost-optimizer.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/container-registry-manager.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/service-mesh-configurator.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/helm-chart-generator.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/infrastructure-as-code-generator.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/monitoring-stack-deployer.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/container-security-scanner.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/ansible-playbook-creator.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/disaster-recovery-planner.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/deployment-rollback-manager.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/infrastructure-drift-detector.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/log-aggregation-setup.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/load-balancer-configurator.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/deployment-pipeline-orchestrator.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/gitops-workflow-builder.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/docker-compose-generator.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/secrets-manager-integrator.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/terraform-module-builder.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../devops/commands/compliance-checker.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/test-coverage-analyzer.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/load-balancer-tester.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/test-orchestrator.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/test-environment-manager.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/contract-test-validator.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/snapshot-test-manager.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/visual-regression-tester.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/test-report-generator.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/database-test-manager.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/smoke-test-runner.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/integration-test-runner.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/browser-compatibility-tester.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/regression-test-tracker.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/e2e-test-framework.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/test-doubles-generator.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `backups/.../testing/commands/accessibility-test-scanner.md` | command | 72 | No allowed-tools (-5), vague quantifiers (-10), no examples (-15) |
| `templates/agent-plugin/agents/example.md` | agent | 80 | No `<example>` blocks (-15), model commented out (-5) |
| `plugins/database/orm-code-generator/agents/orm-agent.md` | agent | 80 | No `<example>` blocks (-15), no model (-5) |
| `plugins/database/freshie-inventory-manager/agents/discovery-scanner.md` | agent | 85 | No `<example>` blocks (-15) |
| `plugins/database/freshie-inventory-manager/agents/anomaly-detector.md` | agent | 85 | No `<example>` blocks (-15) |
| `plugins/database/freshie-inventory-manager/agents/compliance-validator.md` | agent | 85 | No `<example>` blocks (-15) |
| `plugins/geepers/agents/geepers_dashboard.md` | agent | 85 | 2 examples (-5), no explicit output format section (-10) |
| `backups/.../commit/commands/commit.md` | command | 88 | No allowed-tools (-5), hardcoded model version (-5), no empty-input handling (-2) |
| `backups/.../validate-consistency/commands/validate-consistency.md` | command | 88 | No allowed-tools (-5), non-standard `temperature: 0.0` field (-5), no examples (-2) |
| `backups/.../weather/commands/weather.md` | command | 88 | No allowed-tools (-5), numbered steps ✓, examples ✓ |
| `backups/.../travel/commands/travel.md` | command | 88 | No allowed-tools (-5), numbered steps ✓, examples ✓ |
| `backups/.../currency/commands/currency.md` | command | 88 | No allowed-tools (-5), numbered steps ✓, examples ✓ |
| `backups/.../fairdb/commands/fairdb-health-check.md` | command | 88 | No allowed-tools (-5), extensive sudo usage (-5), numbered steps ✓ |
| `backups/.../fairdb/commands/fairdb-onboard-customer.md` | command | 88 | No allowed-tools (-5), credential in env var (-2), numbered steps ✓ |
| `backups/.../fairdb/commands/fairdb-setup-backup.md` | command | 88 | No allowed-tools (-5), network call with webhook URL (-2), numbered steps ✓ |
| `backups/.../fairdb/commands/incident-p0-disk-full.md` | command | 85 | No allowed-tools (-5), `sudo rm -rf` in body (-10) |
| `backups/.../sop/commands/sop-001.md` | command | 88 | No allowed-tools (-5), numbered steps ✓, examples ✓ |
| `backups/.../sop/commands/sop-002.md` | command | 88 | No allowed-tools (-5), numbered steps ✓, examples ✓ |
| `backups/.../sop/commands/sop-003.md` | command | 88 | No allowed-tools (-5), numbered steps ✓, examples ✓ |
| `plugins/database/query-performance-analyzer/agents/performance-agent.md` | agent | 90 | One example (-5), no model (-5) |
| `plugins/geepers/agents/geepers_orchestrator_web.md` | agent | 91 | 2 examples (-5), truncated description (-2), no model (-2) |
| `plugins/geepers/agents/geepers_scalpel.md` | agent | 91 | 2 examples (-5), minor vague phrasing (-4) |
| `plugins/geepers/agents/geepers_a11y.md` | agent | 91 | 2 examples (-5), minor vague phrasing (-4) |
| `plugins/geepers/agents/geepers_links.md` | agent | 91 | 2 examples (-5), minor vague phrasing (-4) |
| `plugins/geepers/agents/geepers_tdd.md` | agent | 93 | 3 examples ✓, minor vague phrasing (-4), no model (-3) |
| `plugins/geepers/agents/geepers_schema.md` | agent | 93 | 3 examples ✓, minor vague phrasing (-4), no model (-3) |
| `plugins/geepers/agents/geepers_api.md` | agent | 93 | 3 examples ✓, minor vague phrasing (-4), no model (-3) |
| `plugins/geepers/agents/geepers_ci.md` | agent | 93 | 3 examples ✓, minor vague phrasing (-4), no model (-3) |
| `plugins/geepers/agents/geepers_perf.md` | agent | 93 | 3 examples ✓, minor vague phrasing (-4), no model (-3) |
| `plugins/geepers/agents/geepers_security.md` | agent | 93 | 3 examples ✓, minor vague phrasing (-4), no model (-3) |
| `plugins/geepers/agents/geepers_mobile.md` | agent | 93 | 3 examples ✓, minor vague phrasing (-4), no model (-3) |
| `plugins/geepers/agents/geepers_db.md` | agent | 93 | 3 examples ✓, minor vague phrasing (-4), no model (-3) |
| `plugins/geepers/agents/geepers_ux.md` | agent | 93 | 3 examples ✓, minor vague phrasing (-4), no model (-3) |
| `plugins/geepers/agents/geepers_i18n.md` | agent | 93 | 3 examples ✓, minor vague phrasing (-4), no model (-3) |

**Weighted average: 73/100**

Score distribution:
- 90–100 (Excellent): 14 artifacts (13%)
- 80–89 (Good): 26 artifacts (25%)
- 70–79 (Acceptable): 22 artifacts (21%)
- 55–69 (Below threshold): 36 artifacts (34%)
- 0–54 (Critical): 7 artifacts (7%)

---

## Security Scan

### Execution Surface Inventory

| Surface | Count | Risk Level |
|---------|-------|------------|
| Hooks (`hooks/` or `.hooks/`) | 0 | None found |
| Shell scripts (`scripts/**/*.sh`) | 1 | MEDIUM |
| Python scripts (`scripts/**/*.py`) | 10 | LOW |
| MCP configs (`.mcp.json`) | 0 | None found |
| Package manifests (`package.json`) | 1 | LOW |
| Embedded shell blocks in commands | ~15 files | HIGH |
| Backup archives (`backups/`) | ~690 (versioned copies) | Not scanned (archives) |

**Note on pre-scan discrepancy:** The pre-scan context reported 25 hook files, 690 scripts, and 26 MCP configs. Direct Glob scans found 0 hooks, 11 scripts, and 0 MCP configs in the active repo paths. The pre-scan numbers likely reflect the `backups/` directory tree (which contains versioned plugin snapshots from a mass-enhancement pipeline) rather than active execution surfaces. The backup archives were not individually scanned for security issues.

### Security Findings

| # | Severity | File | Line | Pattern | Notes |
|---|----------|------|------|---------|-------|
| 1 | HIGH | `backups/.../backup-strategy-implementor/commands/backup-strategy.md` | 1–5 | Shell substitution in YAML frontmatter | `description: $(echo "$description" \| cut -d' ' -f1-5)` and `# $(echo "$name" \| sed ...)` — template never instantiated; shell vars in YAML could cause unexpected behavior in YAML parsers that evaluate expressions |
| 2 | HIGH | `backups/.../fairdb/commands/incident-p0-disk-full.md` | ~143 | `sudo rm -rf` in instructed command | `sudo rm -rf /var/lib/postgresql/16/main/pgsql_tmp/*` — a misfire in the wrong directory could destroy the PostgreSQL data cluster |
| 3 | MEDIUM | `scripts/quick-test.sh` | 22 | Runtime global package install | `npm install -g pnpm@9.15.9` — installs globally during test run; could pollute system environment or be hijacked via supply chain |
| 4 | MEDIUM | `backups/.../fairdb/commands/fairdb-onboard-customer.md` | ~373 | Credential in env var | `PGPASSWORD=${DB_USER_PASS} psql ...` — credential passed via env var; visible in process table (`ps aux`) on most Linux systems |
| 5 | MEDIUM | `backups/.../fairdb/commands/fairdb-setup-backup.md` | ~167 | Network call with env-var URL | `curl -X POST $FAIRDB_MONITORING_WEBHOOK` — webhook URL from env; if env is compromised, exfiltration becomes trivial |
| 6 | MEDIUM | `scripts/deep_eval/llm_judge.py` | 49 | External API credential from env | `os.environ.get('GROQ_API_KEY')` — makes outbound calls to `api.groq.com`; key exfiltrated if process env is exposed |
| 7 | MEDIUM | Multiple devops commands | various | Pervasive `sudo` usage | `sudo systemctl`, `sudo apt`, `sudo ufw`, `sudo tee /etc/...` across 10+ command bodies; executing these without review grants root |
| 8 | LOW | `backups/.../fairdb/commands/fairdb-setup-backup.md` | ~49–53 | Placeholder credential strings | `"YOUR_WASABI_ACCESS_KEY"`, `repo1-cipher-pass=CHANGE_THIS_PASSPHRASE` — not real creds, but pattern could be mistaken for live secrets by automated scanners |
| 9 | LOW | `scripts/quick-test.sh` | various | Writes to `/tmp/` | Temp file creation in world-writable directory — low risk in CI, no symlink attack vector identified |

---

## Bugs

Mechanical issues — artifacts are functionally broken or fail validation.

| # | File | Issue | Fix |
|---|------|-------|-----|
| 1 | `.claude/agents/skill-auditor.md` | Zero YAML frontmatter — no name, description, or model | Add `---\nname: skill-auditor\ndescription: "..."\n---` block |
| 2 | `workspace/lab/schema-optimization/agents/phase_1.md` | Zero YAML frontmatter | Add frontmatter with name, description |
| 3 | `workspace/lab/schema-optimization/agents/phase_2.md` | Zero YAML frontmatter | Add frontmatter with name, description |
| 4 | `workspace/lab/schema-optimization/agents/phase_3.md` | Zero YAML frontmatter | Add frontmatter with name, description |
| 5 | `workspace/lab/schema-optimization/agents/phase_4.md` | Zero YAML frontmatter | Add frontmatter with name, description |
| 6 | `workspace/lab/schema-optimization/agents/phase_5.md` | Zero YAML frontmatter | Add frontmatter with name, description |
| 7 | `backups/.../backup-strategy.md` | Shell command substitution in YAML `description` field — broken template never instantiated | Instantiate template with literal values, remove `$()` expressions from YAML |
| 8 | `backups/.../sync-agent-context.md` | Zero YAML frontmatter — raw markdown file without any frontmatter block | Add `---\nname: sync-agent-context\ndescription: "..."\n---` |
| 9 | `backups/.../overnight-setup.md` | Missing required `name` field in frontmatter | Add `name: overnight-setup` to frontmatter |
| 10 | `backups/.../discovery.md` | Missing required `name` field | Add `name: discovery` to frontmatter |
| 11 | `backups/.../sow.md` | Missing required `name` field | Add `name: sow` to frontmatter |
| 12 | `backups/.../make-builder.md` | Missing required `name` field | Add `name: make-builder` to frontmatter |
| 13 | `backups/.../zap.md` | Missing required `name` field | Add `name: zap` to frontmatter |
| 14 | `backups/.../n8n-builder.md` | Missing required `name` field | Add `name: n8n-builder` to frontmatter |
| 15 | `backups/.../roi.md` | Missing required `name` field | Add `name: roi` to frontmatter |
| 16 | `backups/.../mobile-test.md` | Missing required `name` field | Add `name: mobile-test` to frontmatter |
| 17 | `backups/.../fuzz-api.md` | Missing required `name` field | Add `name: fuzz-api` to frontmatter |
| 18 | `backups/.../commit-smart.md` | Missing required `name` field | Add `name: commit-smart` to frontmatter |

---

## Security Fixes Required

| # | File | Issue | Priority |
|---|------|-------|----------|
| 1 | `backups/.../backup-strategy.md` | Shell substitution expressions in YAML frontmatter (`$(echo ...)`) — broken template that could cause YAML parser confusion | HIGH — fix before any deployment |
| 2 | `backups/.../incident-p0-disk-full.md` | `sudo rm -rf` instructed against a PostgreSQL data directory — narrow the target path with an explicit safety check | HIGH — add `[[ -d "$TARGET_DIR" ]] &&` guard |
| 3 | `scripts/quick-test.sh` | `npm install -g pnpm@9.15.9` at runtime — pin via `.npmrc` or `corepack enable` instead of global install | MEDIUM |
| 4 | `backups/.../fairdb-onboard-customer.md` | `PGPASSWORD=` in env — document alternative: `~/.pgpass` file or `PGSSLMODE` cert auth | MEDIUM |
| 5 | `backups/.../fairdb-setup-backup.md` | Webhook curl with env-var URL — add a `[[ -n "$FAIRDB_MONITORING_WEBHOOK" ]]` guard before the curl call | MEDIUM |

---

## Quality Issues

| # | File | Issue |
|---|------|-------|
| 1–6 | All `schema-optimization/agents/phase_*.md` | No `<example>` blocks — contract agents are functional but undiscoverable by Claude |
| 7 | `skill-auditor.md` | Substantial body (detailed audit methodology) wasted — Claude will never load this agent without frontmatter |
| 8–10 | `nosql-agent.md`, `validation-agent.md`, `orm-agent.md` | No model specified — will inherit session default instead of being assigned appropriate reasoning tier |
| 11–13 | `nosql-agent.md`, `validation-agent.md`, `data-validation-engine` | Code examples in body but no agent `<example>` blocks — examples show usage pattern, not Claude invocation scenarios |
| 14 | `templates/full-plugin/agents/example.md` | Stub body ("Agent instructions here.") — template gives no scaffold for what to write |
| 15 | `templates/agent-plugin/agents/example.md` | Model field commented out — should show active model value as default |
| 16 | `backups/.../commit.md` | Hardcoded `model: claude-sonnet-4-5-20250929` — use model alias (`sonnet`) not versioned ID; will break when model is deprecated |
| 17 | `backups/.../validate-consistency.md` | Non-standard `temperature: 0.0` frontmatter field — not a recognized Claude Code frontmatter key |
| 18 | `geepers_orchestrator_web.md` | Description truncated mid-sentence ("...building and revie...") — description field cut off |
| 19–22 | `geepers_dashboard.md`, `geepers_scalpel.md`, `geepers_a11y.md`, `geepers_links.md` | Only 2 `<example>` blocks — minimum viable but three is the recommended floor |
| 23–55 | All devops/testing backup commands (33 files) | No `allowed-tools` field — commands can call any tool; constraining to relevant tools improves predictability |
| 56–67 | All backup commands with missing `name` + all schema agents | Missing `model` field — inheriting session default means these run on whatever model is active |

---

## Cross-Component

**Geepers plugin (well-structured):** The 15 Geepers agents form a coherent multi-agent web development team. Naming is consistent (`geepers_*`), descriptions follow a common pattern, and all have 2–3 `<example>` blocks. The `geepers_orchestrator_web` agent coordinates the others — this relationship is clear from the descriptions. No cross-reference inconsistencies detected.

**Schema optimization lab (broken pipeline):** The five `phase_*.md` agents in `workspace/lab/schema-optimization/` form a sequential pipeline (Phase 1 → 5) with well-defined JSON I/O contracts. However, none have YAML frontmatter, making them unusable as actual agents. They read as documentation or planning artifacts rather than deployable agents. They also reference absolute paths (`/absolute/path/to/...`) that would require manual substitution before use.

**Freshie inventory agents (coherent):** The three `freshie-inventory-manager` agents (`discovery-scanner`, `anomaly-detector`, `compliance-validator`) have consistent frontmatter and clear separation of concerns. No gaps in their workflow coverage.

**Database plugins (inconsistent quality):** The five database plugins (`nosql-data-modeler`, `data-validation-engine`, `orm-code-generator`, `freshie-inventory-manager`, `query-performance-analyzer`) vary from 70–90/100. The freshie agents are the strongest; the nosql and validation agents are the weakest. All are missing `model` declarations.

**Backup commands vs active commands:** The `backups/` directory appears to be a development artifact — timestamped versioned snapshots created during a bulk plugin enhancement pipeline. These should not be confused with active plugin deliverables. Many backup commands have structural defects (missing `name`) that suggest they were captured before the enhancement pass completed.

**Internal tooling (`.claude/agents/`):** `skill-auditor.md` is a sophisticated audit methodology document with zero frontmatter. Its instructions for multi-phase analysis are detailed, but it cannot function as a Claude Code agent in its current state.

---

## Recommendation

**APPROVE WITH FIXES**

The repository contains strong production-quality work (Geepers agents, Freshie pipeline, FairDB operational commands) alongside significant technical debt in backup archives and experimental workspace files. The core deliverable plugins score well above threshold.

**Required before approval:**
1. Fix the 7 files with zero YAML frontmatter (bugs #1–7) — these agents cannot function
2. Resolve the broken template in `backup-strategy.md` (bug #7, security fix #1) — shell substitution in YAML frontmatter is a correctness defect
3. Address the `sudo rm -rf` guard in `incident-p0-disk-full.md` (security fix #2)

**Strongly recommended:**
4. Add `name` field to the 10 backup commands missing it (bugs #9–18)
5. Replace hardcoded model version in `commit.md` with `model: sonnet` alias
6. Add `<example>` blocks to the 6 database plugin agents — they have good content but are currently under-discoverable

**Good patterns to propagate:**
- Geepers agents show the right structure: name + description + model + 3 `<example>` blocks + clear output format
- FairDB commands demonstrate good operational runbook structure with numbered steps and safety callouts
- `freshie-inventory-manager` agents demonstrate correct `model: inherit` usage for multi-agent pipelines
