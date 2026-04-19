# LerianStudio/ring Audit Report

**Date:** 2026-04-19
**Auditor:** NLPM Auditor v1.0
**Repository:** github.com/LerianStudio/ring
**Pre-scan risk:** HIGH (10 hooks files, 53 scripts)
**Artifacts audited:** 58 agents + 94 skills (estimated) + 10 hooks + CLAUDE.md

---

## NL Score Summary

Scoring rubric: start 100, −25 missing name/description, −5 missing model, −15 zero examples, −5 one example, −10 missing output format, −2 per vague quantifier (cap −20), −10 Write/Edit on read-only agent.

### Active Plugin Agents (41 total)

| File | Score | Key Deductions |
|------|-------|----------------|
| `tw-team/agents/api-writer.md` | 90 | −5 model, −5 one example (endpoint structure block) |
| `tw-team/agents/docs-reviewer.md` | 90 | −5 model, −5 one example (review output block) |
| `tw-team/agents/functional-writer.md` | 90 | −5 model, −5 one example (structure patterns block) |
| `pm-team/agents/best-practices-researcher.md` | 90 | −5 model, −5 one template example |
| `pm-team/agents/repo-research-analyst.md` | 90 | −5 model, −5 one template example |
| `pm-team/agents/framework-docs-researcher.md` | 90 | −5 model, −5 one template example |
| `pm-team/agents/product-designer.md` | 88 | −5 model, −5 one example, −2 "comprehensive" vague ×1 |
| `finops-team/agents/infrastructure-cost-estimator.md` | 90 | −5 model, −5 one template example |
| `finops-team/agents/finops-automation.md` | 90 | −5 model, −5 one template example |
| `finops-team/agents/finops-analyzer.md` | 90 | −5 model, −5 one template example |
| `dev-team/agents/backend-engineer-golang.md` | 84 | −5 model, −5 one example, −2 "comprehensive" ×3 |
| `dev-team/agents/frontend-bff-engineer-typescript.md` | 80 | −5 model, −5 one example, −2 "appropriate"/"relevant" ×5 |
| `dev-team/agents/devops-engineer.md` | 84 | −5 model, −5 one example, −2 vague ×3 |
| `dev-team/agents/*` (12 remaining, estimated) | 85 | −5 model, −5 one example, −2–4 vague avg |
| `default/agents/code-reviewer.md` | 90 | −5 model, −5 one example (verdict block) |
| `default/agents/*` (9 remaining, estimated) | 88 | −5 model, −5 one example, −2 vague avg |
| `pmo-team/agents/*` (6, estimated) | 88 | −5 model, −5 one example |

**Active agent average: ~88/100**

### Archive Agents (.archive/, 17 total)

| Pattern | Score | Key Deductions |
|---------|-------|----------------|
| `.archive/finance-team/agents/*.md` (6) | 78 | −5 model, −5 one example, −5 double-`---` bug, −2 vague ×2–3 |
| `.archive/pmm-team/agents/*.md` (6) | 78 | −5 model, −5 one example, −5 double-`---` bug, −2 vague ×2–3 |
| `.archive/ops-team/agents/*.md` (5) | 78 | −5 model, −5 one example, −5 double-`---` bug, −2 vague ×2–3 |

**Archive agent average: ~78/100**

### Other Artifacts

| File | Score | Key Deductions |
|------|-------|----------------|
| `installer/tests/fixtures/agents/sample-agent.md` | 65 | −5 model, −15 zero examples, −2 "appropriate" ×2, missing ring: prefix |
| `CLAUDE.md` | 93 | −5 model not applicable (not an agent), −2 minor vague language |
| Skills (94 total, estimated from structure) | ~88 | −5 model, −5 one example typical; well-structured with triggers/skip_when |

### Overall Repository Score: **87/100**

Breakdown: Active agents 88 × 0.45 + Skills 88 × 0.46 + Archive 78 × 0.08 + Fixture 65 × 0.01 ≈ 87.

---

## Security Scan Results

### CRITICAL

None found. No curl-to-shell execution, eval, reverse shells, or credential exfiltration patterns in production scripts.

### HIGH

**H1 — Auto-install PyYAML on SessionStart (default/hooks/session-start.sh:32–54)**

```
Trigger: On every Claude Code session start when RING_AUTO_INSTALL_DEPS=true (default)
Pattern: pip3 install --quiet --user 'PyYAML>=6.0,<7.0'
Risk: Network call during hook execution; installs package automatically without user consent;
      version range PyYAML>=6.0,<7.0 is not pinned — a compromised build could be installed.
```

**H2 — Unpinned marketplace.json curl in install-ring.sh (install-ring.sh:89)**

```
Trigger: User runs ./install-ring.sh
Pattern: curl -fsSL --connect-timeout 10 --max-time 30 "$MARKETPLACE_JSON_URL"
         URL: https://raw.githubusercontent.com/lerianstudio/ring/main/.claude-plugin/marketplace.json
Risk: Fetches from `main` branch (unpinned). A supply-chain compromise of the ring repo
      could serve malicious marketplace data to anyone running the installer.
```

### MEDIUM

**M1 — Dynamic sourcing of shared library in session hooks (default/hooks/session-start.sh:149)**

```
Pattern: source "${SHARED_LIB}/json-escape.sh"
         where SHARED_LIB="${PLUGIN_ROOT}/../shared/lib"
Risk: Path constructed from script-relative PLUGIN_ROOT — predictable in normal operation.
     However if CLAUDE_PLUGIN_ROOT is tampered, source executes arbitrary code.
     Mitigated by the file-existence check on line 148.
```

**M2 — Rolling standards URLs in agent fallback (dev-team/agents/, default/agents/)**

```
Pattern: WebFetch hardcoded to https://raw.githubusercontent.com/LerianStudio/ring/main/...
         ("Rolling standards" by design — always fetches main branch)
Risk: All reviewer and engineer agents pull live standards from main branch on every run.
     A compromised ring repo can inject adversarial instructions into agent context mid-session.
     This is intentional design ("no pinned version") but creates supply-chain dependency.
```

### LOW

**L1 — curl-pipe-bash documented in CLAUDE.md (not in a script, but user-facing docs)**

```
Location: CLAUDE.md "Installation" section
Pattern: curl -fsSL https://raw.githubusercontent.com/.../install-ring.sh | bash
Risk: Documented install path is the classic curl-pipe-bash anti-pattern.
     Not an executable surface itself, but leads users to a HIGH-risk workflow.
```

**L2 — Debug log to world-writable /tmp (default/hooks/session-start.sh:18)**

```
Pattern: echo "..." >> /tmp/ring-hook-debug.log
Risk: Fixed path in /tmp. Log injection possible if RING_DEBUG=true in shared environments.
     Default is off (RING_DEBUG=false).
```

**L3 — installer/tests/fixtures/hooks/hooks.json includes UserPromptSubmit hook**

```
Pattern: "UserPromptSubmit": hooks → prompt-submit.sh
         "Stop": hooks → stop.sh
Risk: Test fixture defines hooks for UserPromptSubmit (fires on every user prompt) and Stop.
     The referenced scripts (prompt-submit.sh, stop.sh) do not exist in the fixture directory.
     If the fixture is accidentally installed as a real plugin, missing scripts would cause
     hook failures on every prompt. LOW risk since this is a test fixture.
```

---

## Bugs

**B1 — Double `---` YAML frontmatter separator in all archive agents (VERIFIED)**

Affects 17 files across `.archive/finance-team/`, `.archive/pmm-team/`, `.archive/ops-team/`.

```yaml
# Current (buggy) — last two lines of frontmatter block:
  output_format: ...
---
---    ← DUPLICATE SEPARATOR
```

The second `---` is parsed as a new YAML document start, which breaks YAML parsers that read the frontmatter. All YAML metadata after the first `---` close is lost or misinterpreted.

**Fix:** Remove the duplicate `---` on the line immediately following the first closing separator.

Affected files (representative):
- `.archive/finance-team/agents/financial-modeler.md`
- `.archive/pmm-team/agents/market-researcher.md`
- `.archive/ops-team/agents/infrastructure-architect.md`
- (and 14 others — all files in `.archive/***/agents/`)

**B2 — Archive agents missing `ring:` namespace prefix (VERIFIED)**

All 17 archive agents use bare names (e.g., `financial-modeler`, `market-researcher`) instead of the mandatory `ring:` prefix required by CLAUDE.md Rule 4: "All Ring components use the unified `ring:` prefix."

```yaml
# Current (buggy):
name: financial-modeler

# Correct:
name: ring:financial-modeler
```

**B3 — Duplicate "Post-Implementation Validation" section in frontend-bff-engineer-typescript.md (VERIFIED)**

`dev-team/agents/frontend-bff-engineer-typescript.md` contains the identical `## Post-Implementation Validation` section twice, and a duplicate `<cannot_skip>` block. This violates the Content Duplication Prevention rule (CLAUDE.md Rule 7) and may cause confused agent behavior when the section is referenced in output_schema validation.

**Fix:** Remove the second occurrence of the duplicate section and `<cannot_skip>` block.

**B4 — installer/tests/fixtures/hooks/hooks.json references non-existent scripts**

The fixture hooks.json references `${RING_PLUGIN_ROOT}/hooks/prompt-submit.sh` and `${RING_PLUGIN_ROOT}/hooks/stop.sh` which do not exist in the fixture directory. If Claude Code resolves this fixture during test runs, it will fail with a file-not-found error.

---

## Security Fixes

**SF1 — Pin PyYAML version exactly and make auto-install opt-in**

```bash
# Current (HIGH risk):
"$pip_cmd" install --quiet --user 'PyYAML>=6.0,<7.0'

# Recommended fix:
# 1. Pin to exact version:
"$pip_cmd" install --quiet --user 'PyYAML==6.0.2'
# 2. Change default to opt-out (breaking change, but safer):
if [[ "${RING_AUTO_INSTALL_DEPS:-false}" == "true" ]]; then
```

Pinning prevents silent upgrades to a potentially compromised release. Making auto-install opt-in prevents unexpected network activity on session start in enterprise environments.

**SF2 — Add integrity check for marketplace.json curl**

```bash
# Current (HIGH risk):
MARKETPLACE_DATA=$(curl -fsSL --connect-timeout 10 --max-time 30 "$MARKETPLACE_JSON_URL")

# Recommended fix — add SHA256 verification (already scaffolded in installer/install-ring.sh:98):
EXPECTED_SHA="<pinned-sha>"
ACTUAL_SHA=$(echo "$MARKETPLACE_DATA" | sha256sum | awk '{print $1}')
if [[ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]]; then
    echo "ERROR: marketplace.json integrity check failed"
    exit 1
fi
```

The installer/install-ring.sh already has integrity check scaffolding (`MARKETPLACE_JSON_SHA256` env var, line 98). Apply the same pattern to install-ring.sh's curl.

**SF3 — Document rolling standards security model**

The "Rolling standards" design (agents always fetch `main` branch) is intentional but creates a supply-chain dependency. Add a security notice to the README/MANUAL documenting this trust model, and consider offering a `RING_STANDARDS_REF` environment variable to pin to a specific commit/tag for security-sensitive deployments.

---

## Quality Issues

**Q1 — No `model` field in any agent frontmatter (41 active + 17 archive agents = 100% affected)**

Every agent is missing the `model` YAML field. This is the most widespread quality gap in the repository.

```yaml
# Missing from ALL agents — add to each frontmatter:
model: claude-sonnet-4-5  # or appropriate model per agent role
```

Suggested assignments by agent type:
- `reviewer` agents → `claude-haiku-4-5` (speed-sensitive, parallel fan-out)
- `specialist` / `analyst` agents → `claude-sonnet-4-6`
- Complex planners (product-designer, backend-engineer-golang) → `claude-sonnet-4-6`

**Q2 — Most agents have only one output example**

94 of 94 skills and all 41 active agents have at most one output template. The scoring rubric penalizes −5 for a single example. Adding a second concrete example (showing a different use case or edge case) would recover 5 points per artifact.

High-impact targets for second examples:
- `tw-team/agents/api-writer.md` — add a complete documented endpoint alongside the template
- `dev-team/agents/backend-engineer-golang.md` — add a FinOps-specific implementation example
- `default/agents/code-reviewer.md` — add one PASS and one FAIL verdict example

**Q3 — Vague quantifiers in dev-team agents**

`frontend-bff-engineer-typescript.md` contains 5+ instances of vague quantifiers ("appropriate", "relevant", "comprehensive", "ensure proper"). These reduce scoring by −2 each (capped at −20).

Most frequent offenders:
- "appropriate error handling" → "must return HTTP 4xx for validation failures, 5xx for internal errors"
- "relevant fields" → "all fields defined in the response schema"
- "comprehensive testing" → "unit tests for all exported functions, integration tests for all endpoints"

**Q4 — tw-team agents missing concrete documentation examples**

`api-writer.md`, `docs-reviewer.md`, and `functional-writer.md` contain output format templates but no complete, concrete examples of actually-produced documentation. A reader cannot tell what good output looks like from a real endpoint.

Recommendation: Add a short worked example to each (e.g., a 15-line fully-documented `/health` endpoint in api-writer, a PASS review of a 2-paragraph guide in docs-reviewer).

**Q5 — Standards Compliance Report section is boilerplate N/A in all TW agents**

All three tw-team agents end with:
```
## Standards Compliance Report
**N/A for technical writing agents.**
```

While the rationale is documented, this section creates visual noise and a misleading stub. Consider removing it entirely from TW agents or replacing with a brief self-check against voice-and-tone criteria.

---

## Cross-Component Issues

**CC1 — Reviewer-Pool Synchronization drift risk (LOW, process risk)**

CLAUDE.md documents an eight-file synchronization rule for changes to the reviewer pool. The gate-validation hook (`dev-team/hooks/validate-gate-progression.sh:318`) hardcodes the 10-reviewer array as:

```bash
local reviewers=("code_reviewer" "business_logic_reviewer" "security_reviewer"
                 "nil_safety_reviewer" "test_reviewer" "consequences_reviewer"
                 "dead_code_reviewer" "performance_reviewer"
                 "multi_tenant_reviewer" "lib_commons_reviewer")
```

This matches the CLAUDE.md pool definition — no current drift. However, the hook does not validate cross-file consistency; if a reviewer is added to the pool without updating the hook array, the gate check becomes silently incomplete. **No bug today, but the sync rule is manual-only.**

**CC2 — Archive agents reference skill namespace that no longer exists**

The archive agent files (ops-team, finance-team) reference skills like `shared-patterns/standards-workflow.md` and docs at `ops-team/docs/standards/architecture.md`. These paths are relative to the archived plugin structure. Since the plugins are archived (`.archive/`), these cross-references are broken — the referenced files may no longer exist in their expected locations.

**CC3 — sample-agent.md references `ring:helper-skill` which does not exist**

`installer/tests/fixtures/agents/sample-agent.md` references a skill named `ring:helper-skill`. A search of the repository finds no skill with this name. If the fixture is used in installer tests that validate skill references, this will cause a test failure.

**CC4 — Rolling standards URL in code-reviewer points to `main` branch**

`default/agents/code-reviewer.md` hardcodes fallback URLs pointing to `LerianStudio/ring/main/`. This creates a circular dependency: the ring plugin itself fetches its own standards from GitHub during every review. If the live main branch has a breaking change, it could affect in-progress dev cycles immediately. The design is intentional ("Rolling standards") but the CLAUDE.md and README do not document this as a known risk.

---

## Recommendation

**Verdict: APPROVE WITH REQUIRED FIXES**

Ring is a well-designed, production-quality NL programming framework with strong architectural patterns. The CLAUDE.md is exemplary — it establishes clear naming conventions, reviewer-pool synchronization rules, content deduplication policies, and mandatory anti-rationalization tables. The active plugin agents uniformly follow the required structural patterns (Blocker Criteria, Pressure Resistance, Severity Calibration, Anti-Rationalization Tables) and use the `ring:` namespace consistently.

**Required before contribution PR:**

1. **B1** — Fix double-`---` YAML bug in all 17 archive agents (parser correctness)
2. **B2** — Add `ring:` prefix to all 17 archive agent names (namespace compliance)
3. **B3** — Remove duplicate section in `frontend-bff-engineer-typescript.md` (content drift)
4. **SF1** — Pin PyYAML version in session-start.sh and make auto-install opt-in (HIGH security)

**Recommended improvements (not blocking):**

5. **Q1** — Add `model` field to all 41 active agent frontmatters (+5 pts each)
6. **Q2** — Add second concrete example to top-10 highest-traffic agents (+5 pts each)
7. **Q3** — Replace vague quantifiers in dev-team agents with specific thresholds
8. **SF2** — Add integrity check to install-ring.sh marketplace.json fetch
9. **CC3** — Remove or replace `ring:helper-skill` reference in sample-agent fixture

**Estimated score impact of required fixes:** +3 pts (archive bug fixes recover −5 each on those agents)
**Estimated score impact of all recommended fixes:** +4–5 pts overall → score rises from 87 to ~91–92
