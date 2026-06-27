# NLPM Audit: JoasASantos/ClaudeAdvancedPlugins
**Date**: 2026-04-06  |  **Artifacts**: 56  |  **Strategy**: batched
**NL Score**: 58/100
**Security**: CLEAR
**Bugs**: 1  |  **Quality Issues**: 9  |  **Security Findings**: 0

## NL Score Summary

All 56 artifacts are Claude Code slash commands (`plugins/*/commands/*.md`). Scoring base: 100 − 25 (no `description:` frontmatter) − 5 (no `allowed-tools:` declaration) − 10 (no empty `$ARGUMENTS` handling) = 60/100 floor for every file. Additional deductions applied for vague quantifiers and one missing output-format template.

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| plugins/memory-vault/commands/memory-vault.md | command | 48 | No output-format template; vague "intelligently" |
| plugins/context-manager/commands/context-manager.md | command | 50 | "relevant" ×3, "intelligently" ×1 |
| plugins/secure-code-review/commands/secure-code-review.md | command | 52 | "properly" ×4 in checklist items |
| plugins/blue-team-hardening/commands/blue-team-hardening.md | command | 52 | "unnecessary" ×4 without criteria |
| plugins/devsecops/commands/devsecops.md | command | 54 | "proper" + "unnecessary" ×2 |
| plugins/supply-chain-sec/commands/supply-chain-sec.md | command | 54 | "unnecessary" + "proper" ×2 |
| plugins/red-team-ops/commands/red-team-ops.md | command | 56 | "realistic" + "proper" |
| plugins/vuln-research/commands/vuln-research.md | command | 56 | "clean", "reliable" as vague descriptors |
| plugins/cloud-security/commands/cloud-security.md | command | 56 | "proper" ×2 |
| plugins/context-keeper/commands/context-keeper.md | command | 56 | "significant", "relevant" |
| plugins/blue-team-edr/commands/blue-team-edr.md | command | 56 | "unusual" ×2 without baseline definition |
| plugins/red-team-ops/commands/red-team-payload.md | command | 58 | "appropriate" in process step |
| plugins/gamedev-unreal/commands/gamedev-unreal.md | command | 58 | "judiciously" |
| plugins/backend-architect/commands/backend-api-design.md | command | 58 | "sensible" defaults |
| plugins/frontend-animations/commands/frontend-animations.md | command | 58 | "delightful" |
| plugins/blue-team-dfir/commands/blue-team-dfir.md | command | 58 | "proper" in evidence handling |
| plugins/blue-team-soc/commands/blue-team-soc.md | command | 58 | "proper" in ticket categorization |
| plugins/pentest-ad/commands/pentest-ad.md | command | 60 | Universal penalties only |
| plugins/pentest-network/commands/pentest-network.md | command | 60 | Universal penalties only |
| plugins/api-security/commands/api-security.md | command | 60 | Universal penalties only |
| plugins/frontend-micro/commands/frontend-micro.md | command | 60 | Universal penalties only |
| plugins/exploit-dev/commands/exploit-dev.md | command | 60 | Universal penalties only |
| plugins/exploit-dev/commands/exploit-ctf.md | command | 60 | Universal penalties only |
| plugins/reverse-protocol/commands/reverse-protocol.md | command | 60 | Universal penalties only |
| plugins/frontend-perf/commands/frontend-perf.md | command | 60 | Universal penalties only |
| plugins/backend-architect/commands/backend-architect.md | command | 60 | Universal penalties only |
| plugins/backend-architect/commands/backend-db-optimize.md | command | 60 | Universal penalties only |
| plugins/pentest-mobile/commands/pentest-mobile.md | command | 60 | Universal penalties only |
| plugins/gamedev-design/commands/gamedev-design.md | command | 60 | Universal penalties only |
| plugins/os-internals/commands/os-debug.md | command | 60 | Universal penalties only |
| plugins/os-internals/commands/os-internals.md | command | 60 | Universal penalties only |
| plugins/reverse-obfuscation/commands/reverse-obfuscation.md | command | 60 | Universal penalties only |
| plugins/reverse-firmware/commands/reverse-firmware.md | command | 60 | Universal penalties only |
| plugins/threat-modeler/commands/threat-modeler.md | command | 60 | Universal penalties only |
| plugins/pentest-report/commands/pentest-report.md | command | 60 | Universal penalties only |
| plugins/gamedev-threejs/commands/gamedev-threejs.md | command | 60 | Universal penalties only |
| plugins/crypto-analysis/commands/crypto-analysis.md | command | 60 | Universal penalties only |
| plugins/hallucination-guard/commands/hallucination-guard.md | command | 60 | Universal penalties only |
| plugins/gamedev-godot/commands/gamedev-godot.md | command | 60 | Universal penalties only |
| plugins/reverse-binary/commands/reverse-binary.md | command | 60 | Universal penalties only |
| plugins/pentest-toolkit/commands/pentest-web.md | command | 60 | Universal penalties only |
| plugins/pentest-toolkit/commands/pentest-toolkit.md | command | 60 | Universal penalties only |
| plugins/blue-team-siem/commands/blue-team-siem.md | command | 60 | Universal penalties only |
| plugins/gamedev-unity/commands/gamedev-unity.md | command | 60 | Universal penalties only |
| plugins/frontend-3d/commands/frontend-3d.md | command | 60 | Universal penalties only |
| plugins/reverse-malware/commands/reverse-malware.md | command | 60 | Universal penalties only |
| plugins/blue-team-threat-intel/commands/blue-team-threat-intel.md | command | 60 | Universal penalties only |
| plugins/pentest-cloud/commands/pentest-cloud.md | command | 60 | Universal penalties only |
| plugins/pentest-social/commands/pentest-social.md | command | 60 | Universal penalties only |
| plugins/blue-team-network-defense/commands/blue-team-network-defense.md | command | 60 | Universal penalties only |
| plugins/token-tracker/commands/token-tracker.md | command | 60 | Universal penalties only |
| plugins/frontend-dom/commands/frontend-dom.md | command | 60 | Universal penalties only |
| plugins/pentest-wireless/commands/pentest-wireless.md | command | 60 | Universal penalties only |
| plugins/blue-team-malware-analysis/commands/blue-team-malware-analysis.md | command | 60 | Universal penalties only |
| plugins/frontend-forge/commands/frontend-component.md | command | 60 | Universal penalties only |
| plugins/frontend-forge/commands/frontend-forge.md | command | 60 | Universal penalties only |

**Weighted average**: (48 + 50 + 52×2 + 54×2 + 56×5 + 58×6 + 60×39) / 56 = 3278 / 56 ≈ **58/100**

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts | 2 (`install.sh`, `uninstall.sh`) |
| MCP configs | 0 |
| Package manifests | 0 |

Both scripts were read and reviewed. `install.sh` copies `*.md` files from `plugins/*/commands/` to `~/.claude/commands/`. `uninstall.sh` removes those same files. Pattern matches for "file writes outside repo" were evaluated and determined to be intentional installer behaviour — false positives. No subprocess, eval, credential-exfiltration, curl-pipe-sh, or network-call patterns were found.

### Security Findings

No security findings.

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | All 56 command files | Missing `description:` frontmatter field | Commands appear without descriptions in Claude Code `/help` listing, reducing discoverability |

**Detail**: Every command file begins with a bare H1 heading and no YAML frontmatter block. Claude Code populates `/help` descriptions from `description:` in frontmatter. Adding this field to each file is a one-line change per file and immediately improves the user experience. The filename serves as the command name, so `name:` is optional, but `description:` has genuine discoverability value.

**Example fix for `pentest-ad.md`:**
```markdown
---
description: "Active Directory penetration testing — enumeration, credential attacks, privilege escalation, and defense recommendations"
---
# Active Directory Penetration Testing Plugin
...
```

## Security Fixes (PR-worthy, Medium/Low only)

No security fixes required.

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | All 56 command files | No `allowed-tools:` frontmatter declaration | −5 each |
| 2 | All 56 command files | No empty `$ARGUMENTS` guard — no usage hint if user invokes without arguments | −10 each |
| 3 | plugins/memory-vault/commands/memory-vault.md | No `## Output Format` section with concrete template | −10 |
| 4 | plugins/secure-code-review/commands/secure-code-review.md | "properly" used 4× in checklist without measurable criteria | −8 |
| 5 | plugins/blue-team-hardening/commands/blue-team-hardening.md | "unnecessary" used 4× without defining removal criteria | −8 |
| 6 | plugins/context-manager/commands/context-manager.md | "relevant" ×3 + "intelligently" ×1 without operational definition | −8 |
| 7 | plugins/devsecops/commands/devsecops.md | "proper" + "unnecessary" appear in body without specifics | −4 |
| 8 | plugins/supply-chain-sec/commands/supply-chain-sec.md | "unnecessary" + "proper" without measurable thresholds | −6 |
| 9 | plugins/red-team-ops/commands/red-team-ops.md | "realistic" + "proper" without reference criteria | −4 |

**Notes**:
- Q1 (`allowed-tools:`): Claude Code command frontmatter supports `allowed-tools:` to constrain which tools Claude can call while running the command. Declaring this is a security best practice for commands that should not invoke Write/Edit/Bash. Most read-only advisor commands (threat-modeler, hallucination-guard, etc.) would benefit.
- Q2 (empty input): All commands end with a bare `$ARGUMENTS` invocation. A pattern like `If no arguments are provided, describe available options with examples.` before `$ARGUMENTS` prevents silent no-op invocations.
- Q4–Q9: Vague quantifiers are flagged per the NLPM rubric. Substituting concrete criteria (CIS control IDs, tool names, measurable thresholds) would raise these files into the 60–65 range.

## Cross-Component

- **No broken references**: All 56 command files are self-contained. None cross-reference each other or shared skill files.
- **No orphaned components**: Every file in the audit list exists on disk and is reachable.
- **Consistent invocation pattern**: All commands use `$ARGUMENTS` at the end. Pattern is uniform and correct.
- **Category mapping is current**: `install.sh`'s `get_category_plugins()` function lists 8 categories covering all 56 files.
- **No plugin.json / marketplace.json found**: The repo appears to distribute commands as loose `.md` files installed by `install.sh` rather than as a packaged Claude Code plugin. There is no metadata manifest to audit for staleness.

## Recommendation

**CLEAR — submit PRs for Bug #1 (description frontmatter) across all 56 command files.**

The dominant finding is a uniform omission: missing `description:` frontmatter. This is low-risk, high-value, and mechanically reproducible — an ideal PR candidate. A single PR adding descriptions to all 56 files would bring the NL score from 58 to approximately 63/100 (the no-frontmatter penalty drops from −25 to −0 for description).

Secondary quality improvements (Q1 `allowed-tools:`, Q2 empty-input guards) are informational and can be addressed in a follow-up PR.

No security concerns were identified. Both scripts were reviewed and are clean standard installer patterns.
