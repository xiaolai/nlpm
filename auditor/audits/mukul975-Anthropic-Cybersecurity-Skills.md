# NLPM Audit: mukul975/Anthropic-Cybersecurity-Skills
**Date**: 2026-04-17  |  **Artifacts**: 100 (sampled from 754)  |  **Strategy**: random-sample
**NL Score**: 79/100
**Security**: REVIEW
**Bugs**: 7  |  **Quality Issues**: 28  |  **Security Findings**: 2

## NL Score Summary

Scored 100 of 754 SKILL.md files. Scores follow a bimodal distribution: ~42% score ≥ 90 (high-quality, full-featured files) and ~22% score ≤ 65 (stub files or generic-boilerplate files). The gap between the two tiers is structural, not incidental — the low-scoring files share a small set of copy-pasted templates.

| File | Score | Top Issue |
|------|-------|-----------|
| analyzing-uefi-bootkit-persistence | 95 | None (author: mukul975) |
| implementing-hardware-security-key-authentication | 95 | None (author: mukul975) |
| analyzing-memory-dumps-with-volatility | 95 | None |
| analyzing-malware-behavior-with-cuckoo-sandbox | 95 | None |
| analyzing-network-traffic-with-wireshark | 95 | None |
| analyzing-linux-elf-malware | 93 | None |
| analyzing-macro-malware-in-office-documents | 95 | None |
| implementing-hashicorp-vault-dynamic-secrets | 95 | None |
| implementing-secrets-management-with-vault | 95 | None |
| conducting-cloud-incident-response | 95 | None |
| performing-container-image-hardening | 93 | None |
| building-automated-malware-submission-pipeline | 93 | None |
| auditing-cloud-with-cis-benchmarks | 93 | None |
| building-detection-rules-with-sigma | 92 | None |
| auditing-azure-active-directory-configuration | 92 | None |
| monitoring-scada-modbus-traffic-anomalies | 93 | None |
| performing-web-cache-poisoning-attack | 90 | No "Do not use" clause |
| analyzing-windows-registry-for-artifacts | 90 | Scenarios are brief (no pitfalls) |
| analyzing-docker-container-forensics | 90 | Scenarios are brief (no pitfalls) |
| detecting-ransomware-precursors-in-network | 90 | None |
| analyzing-email-headers-for-phishing-investigation | 91 | No "Do not use" clause |
| analyzing-windows-event-logs-in-splunk | 93 | None |
| analyzing-linux-system-artifacts | 91 | No "Do not use" clause |
| building-cloud-siem-with-sentinel | 93 | None |
| analyzing-dns-logs-for-exfiltration | 93 | None |
| implementing-policy-as-code-with-open-policy-agent | 88 | None |
| analyzing-indicators-of-compromise | 88 | No formal Scenarios section |
| conducting-cloud-penetration-testing | 89 | None |
| mapping-mitre-attack-techniques | 82 | No Output Format |
| implementing-anti-ransomware-group-policy | 82 | No Scenarios, no Output Format |
| performing-active-directory-bloodhound-analysis | 72 | Generic "When to Use" boilerplate |
| analyzing-cobalt-strike-beacon-configuration | 72 | Generic "When to Use" boilerplate |
| analyzing-apt-group-with-mitre-navigator | 72 | Generic "When to Use" boilerplate |
| analyzing-threat-actor-ttps-with-mitre-attack | 72 | Generic "When to Use" boilerplate (near-duplicate of apt-group skill) |
| performing-threat-landscape-assessment-for-sector | 72 | Generic "When to Use" boilerplate |
| performing-threat-modeling-with-owasp-threat-dragon | 72 | Generic "When to Use" boilerplate |
| conducting-internal-network-penetration-test | 72 | Generic "When to Use" boilerplate |
| performing-active-directory-penetration-test | 72 | Generic "When to Use" boilerplate |
| analyzing-malware-family-relationships-with-malpedia | 72 | Generic "When to Use" boilerplate |
| building-identity-federation-with-saml-azure-ad | 70 | Generic "When to Use" boilerplate |
| configuring-microsegmentation-for-zero-trust | 70 | Generic "When to Use" boilerplate |
| implementing-proofpoint-email-security-gateway | 70 | Generic "When to Use" boilerplate |
| building-detection-rule-with-splunk-spl | 68 | Generic "When to Use" boilerplate |
| detecting-insider-threat-behaviors | 65 | Generic "When to Use" (circular: "hunting for indicators of detecting insider threat...") |
| hunting-for-unusual-network-connections | 65 | Circular "When to Use" (self-referential) |
| building-c2-infrastructure-with-sliver-framework | 65 | Generic "When to Use" boilerplate |
| performing-phishing-simulation-with-gophish | 65 | Generic "When to Use" boilerplate |
| building-threat-intelligence-platform | 65 | Generic "When to Use" boilerplate |
| implementing-log-forwarding-with-fluentd | 65 | Generic "When to Use" boilerplate |
| detecting-business-email-compromise | 60 | Generic "When to Use"; 4 prose-only steps, no code |
| analyzing-linux-kernel-rootkits | 60 | Generic "When to Use"; 4 bullet steps, no code |
| implementing-zero-trust-with-beyondcorp | 62 | Generic "When to Use" boilerplate |
| implementing-honeytokens-for-breach-detection | 45 | Stub: 7 bullet steps, no code, 2-line output |
| analyzing-malware-persistence-with-autoruns | 45 | Stub: 1 Python step only |
| implementing-deception-based-detection-with-canarytoken | 45 | Stub: 7 bullet steps, no code |
| performing-dns-tunneling-detection | 45 | Stub: 4 prose steps, no code |
| performing-ssl-tls-security-assessment | 50 | Stub: 4 bullet steps, no code |
| performing-red-team-with-covenant | 50 | Stub: 5 bullet steps, no code |
| analyzing-office365-audit-logs-for-compromise | 50 | Stub: 7 bullets, no code, 2-line output |
| detecting-aws-cloudtrail-anomalies | 50 | Stub: 4 bullets, no code, 1-line output |
| analyzing-memory-forensics-with-lime-and-volatility | 35 | Bad tags + generic WTU + stub content |
| analyzing-powershell-script-block-logging | 35 | Bad tags (word-split) + generic WTU + no workflow |
| analyzing-azure-activity-logs-for-threats | 35 | Bad tags (word-split) + generic WTU + no workflow |

**Score distribution across 100 sampled files:**
- ≥ 90: 42 files (42%)
- 80–89: 14 files (14%)
- 70–79: 22 files (22%)
- 60–69: 9 files (9%)
- < 60: 13 files (13%)

## Security Scan

### Execution Surface Inventory

| Surface | Count | Notes |
|---------|-------|-------|
| Hook files | 0 | No `.claude/hooks/` in repo |
| Script files (agent.py / process.py) | ~1,030 | One per skill; Python wrappers |
| MCP configs | 0 | No `.mcp.json` |
| Package manifests | 0 | No `package.json` or `requirements.txt` at root |

### Security Findings

| # | Severity | Pattern | Location | Description |
|---|----------|---------|----------|-------------|
| 1 | REVIEW | Offensive tooling wrappers | Multiple skills | ~15 skills include `agent.py` files that wrap Metasploit (`msfconsole`), Sliver C2, Covenant C2, BloodHound, and Evilginx2 as subprocesses. These are legitimate pentest tooling when properly authorized. No evidence of malicious use. Flagged because these scripts execute offensive tooling and deserve deployment-context review. |
| 2 | INFO | False-positive pattern matches | Security scanner scripts | The pattern-matching scan surfaced 10 "critical" and 9 "high" matches. All are false positives: the patterns (`subprocess.call(shell=True)`, `os.system()`, `/dev/tcp`, `curl \| bash`) appear as *strings inside detection rule lists* in security scanner scripts (e.g., `detecting-serverless-function-injection/scripts/agent.py` contains `{"pattern": r"\bsubprocess\.call\s*\(.*shell\s*=\s*True", "sink": "...", "severity": "critical"}` as a detection signature), not as executed code. |

**Overall security assessment**: No confirmed malicious patterns. The offensive tooling wrappers (Finding #1) are expected given the repo's red-team/pentest content domain. The contributing author (`mukul975`) is the repo owner; no supply-chain risk. Rating: **REVIEW** (not BLOCKED; not CLEAR due to offensive tooling present).

## Bugs (PR-worthy)

These are mechanical defects where the file is structurally broken, not just low-quality.

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `analyzing-powershell-script-block-logging/SKILL.md` | `tags:` are word-splits of the skill name: `[analyzing, powershell, script, block]` — "block" and "analyzing" are not meaningful cybersecurity tags | Tags provide no discovery value; "block" matches unrelated results |
| 2 | `analyzing-azure-activity-logs-for-threats/SKILL.md` | `tags:` are word-splits: `[analyzing, azure, activity, logs]` — "analyzing" is not a domain tag | Same tag pollution issue |
| 3 | `analyzing-memory-forensics-with-lime-and-volatility/SKILL.md` | `tags:` include `"with"` — a preposition listed as a tag: `[analyzing, memory, forensics, with]` | "with" as a tag will match every search for files containing that word |
| 4 | `performing-ssl-tls-security-assessment/SKILL.md` | Stub file: Steps section has 4 prose bullets with no code examples, no workflow, no Output Format. The SKILL.md is essentially a placeholder | Skill cannot be used effectively; agent trained on it gives empty guidance |
| 5 | `detecting-aws-cloudtrail-anomalies/SKILL.md` | Stub file: 4 prose bullets as "Steps", single-line "Expected Output" — no Python code despite prerequisites listing `boto3` | Inconsistency between prerequisites and empty workflow |
| 6 | `analyzing-office365-audit-logs-for-compromise/SKILL.md` | Stub file: 7 bullet steps, 2-line output section — no authentication code despite prerequisites listing `msal` and `requests` | Same stub pattern; prerequisites and content mismatched |
| 7 | `performing-red-team-with-covenant/SKILL.md` | Stub file: 5 prose bullets as "Steps" referencing Covenant API but no API calls shown, "Expected Output" is one sentence | Prerequisites list Python `requests` but no code exists |

## Security Fixes

No PR-worthy security fixes. Finding #1 (offensive tooling) is contextually appropriate for a cybersecurity skills repo and does not require code changes. Finding #2 (false-positive pattern matches) is informational only.

## Quality Issues (informational)

These are patterns affecting many files that lower the overall score. They are not bugs but represent systematic gaps in content quality.

| # | Pattern | Files Affected | Penalty Applied | Description |
|---|---------|----------------|-----------------|-------------|
| 1 | Generic boilerplate "When to Use" | ~35 of 100 sampled | -10 per file | Four copy-paste templates replace specific decision guidance: (a) "When conducting security assessments that involve [skill-name]", (b) "When deploying or configuring [skill-name] capabilities", (c) "When investigating security incidents that require [skill-name]", (d) "When managing security operations that require [skill-name]". These are self-referential and provide no actual decision criteria. |
| 2 | Circular "When to Use" | 2 of 100 | -10 per file | `hunting-for-unusual-network-connections` says "When proactively hunting for indicators of hunting for unusual network connections" — the WTU literally contains the skill name used as its own justification. `detecting-insider-threat-behaviors` has the same pattern. |
| 3 | Missing Output Format section | ~35 of 100 | -10 per file | All files with generic WTU also lack an Output Format section. High-quality files all have a code-fenced Output Format block showing exact report structure. |
| 4 | Missing Scenarios section | ~35 of 100 | -5 per file | Same cohort. High-quality files include 1–4 named scenarios with context, approach, and "Pitfalls" subsections. Generic files omit this entirely. |
| 5 | "Validation Criteria" replacing Output Format | ~12 of 100 | -10 | Some files substitute a bulleted "Validation Criteria" checklist for an Output Format block. These are not equivalent: Output Format shows the actual artifact the skill produces; Validation Criteria shows acceptance tests. |
| 6 | Near-duplicate skill content | 2 of 100 | informational | `analyzing-apt-group-with-mitre-navigator` and `analyzing-threat-actor-ttps-with-mitre-attack` have nearly identical Python code (both use `attackcti`, `create_navigator_layer()`, `get_techniques_used_by_group()`). The skills cover overlapping ground without sufficient differentiation. |
| 7 | Missing "Do not use" clause | ~20 of 100 | -2 per file | High-quality files include `**Do not use** for X, Y, Z` immediately after the "When to Use" bullets, setting clear scope boundaries. The missing clause is most impactful for offensive skills (pentest, red team) where scope matters legally. |
| 8 | Key Concepts as prose instead of table | ~8 of 100 | -3 per file | Some files use paragraph descriptions instead of the standard two-column `| Concept | Description |` table format. The table is more scannable and consistent with the high-quality files. |

## Cross-Component

**Consistent schema across all 100 sampled files**: All SKILL.md files have complete frontmatter with `name`, `description`, `domain`, `subdomain`, `tags`, `version`, `author`, `license`, `nist_csf`. No missing required fields in any sampled file.

**Author attribution**: Two authors appear in the 100 sampled files. `mahipal` authored ~95 of the 100 sampled files. `mukul975` (the repo owner) authored `analyzing-uefi-bootkit-persistence` and `implementing-hardware-security-key-authentication` — both score 95/100 and exemplify the high-quality pattern. The skill quality gap is consistent: mukul975-authored files are full-featured; the majority of mahipal-authored files are either high-quality (42%) or fall into the two low-quality patterns (generic WTU stubs, word-split tags).

**Structural two-tier quality gap**: The repo contains a clearly good template (used in ~42% of files: specific WTU with "Do not use", numbered steps with code, Key Concepts table, Tools table, 1–4 scenarios with pitfalls, Output Format block) and two degraded patterns (generic boilerplate WTU with no code / no Output Format; stub files with 4–7 prose bullets). The degraded patterns affect ~35% of sampled files and are likely batch-generated rather than authored individually.

**No broken cross-references**: The skills are standalone SKILL.md files with no internal cross-references to other skills or agents, so no broken reference chains exist.

## Recommendation

**REVIEW** — Do not block contribution. Submit targeted PRs for the 7 bugs. The security findings are contextually appropriate for a red-team/pentest skills repository.

**Priority order:**

1. **Bug PR (tags)** — Fix word-split tags in `analyzing-powershell-script-block-logging`, `analyzing-azure-activity-logs-for-threats`, `analyzing-memory-forensics-with-lime-and-volatility`. These are one-line YAML fixes that dramatically improve discoverability. Remove "analyzing", "with", "logs" from tags; replace with domain-specific terms like `forensics`, `memory-analysis`, `lime`, `volatility`.

2. **Bug PR (stubs)** — Either fill in the 4 stub files (`performing-ssl-tls-security-assessment`, `detecting-aws-cloudtrail-anomalies`, `analyzing-office365-audit-logs-for-compromise`, `performing-red-team-with-covenant`) with working code examples matching the high-quality template, or open issues requesting their completion. The prerequisite lists in these files indicate the author knew what code should exist.

3. **Quality PR (generic WTU)** — The ~35 files with generic "When to Use" boilerplate would each need 3–5 specific bullets written. If batching is possible, this is the highest-leverage quality improvement: each fixed file gains ~10 points and becomes meaningfully more useful to agents. Priority targets: `analyzing-cobalt-strike-beacon-configuration`, `building-c2-infrastructure-with-sliver-framework`, `performing-phishing-simulation-with-gophish`, `performing-active-directory-penetration-test` (all have good content but unusable WTU sections).

4. **Quality PR (Output Format)** — Add Output Format sections to the ~12 files that have "Validation Criteria" instead. These files have all other sections; a single code-fenced output block would push them from ~72 to ~85.
