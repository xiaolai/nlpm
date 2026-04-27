# NLPM Audit: kubesphere/kubesphere
**Date**: 2026-04-27  |  **Artifacts**: 21  |  **Strategy**: batched
**NL Score**: 89/100
**Security**: REVIEW
**Bugs**: 5  |  **Quality Issues**: 6  |  **Security Findings**: 5

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/kubesphere-devops-tenant/SKILL.md | skill | 77 | Hardcoded credential `P@88w0rd` in API examples; duplicate `Authorization` header in curl command |
| skills/kubesphere-devops-credentials/SKILL.md | skill | 78 | API examples use `type: Opaque` which contradicts the explicit warning that Opaque breaks Jenkins sync |
| skills/kubesphere-devops-overview/SKILL.md | skill | 84 | `Project Components` ASCII art block duplicated; `Key Resources` heading appears twice |
| skills/kubesphere-devops-pipeline/SKILL.md | skill | 86 | Missing closing `**` in bold markdown; duplicate Common Mistakes partial table |
| skills/kubesphere-fluid/SKILL.md | skill | 87 | YAML template syntax error: `low: "{{low}}` missing closing double-quote |
| skills/frontend-forge-fi-operations/SKILL.md | skill | 88 | Routing/decision skill; delegates to `references/` files without inline examples |
| skills/whizard-logging/SKILL.md | skill | 89 | Placeholder comment says "From Step 3" but only 2 steps are defined |
| skills/kubesphere-core/SKILL.md | skill | 90 | Clean; routing table is clear but examples are thin |
| skills/whizard-events/SKILL.md | skill | 90 | Clean; step-numbered prerequisites are exemplary |
| skills/opensearch/SKILL.md | skill | 90 | Clean; Output Contract section for inter-skill data sharing is exemplary |
| skills/kubesphere-cluster-management/SKILL.md | skill | 90 | Clean; explicit Out of Scope section is exemplary |
| skills/whizard-telemetry/SKILL.md | skill | 90 | Clean; delegates config generation to `generate-config.sh` |
| skills/kubesphere-openkruise/SKILL.md | skill | 91 | Clean; in-place update patterns well documented |
| skills/vector/SKILL.md | skill | 91 | Clean; prerequisite chaining to OpenSearch is clear |
| skills/kubesphere-multi-tenant-management/SKILL.md | skill | 91 | Clean; security guidelines and least-privilege defaults present |
| skills/whizard-auditing/SKILL.md | skill | 91 | Clean; mirrors whizard-events structure consistently |
| skills/kubesphere-devops-jenkins/SKILL.md | skill | 91 | Clean; CasC and LDAP/OIDC configuration well covered |
| skills/kubesphere-extension-management/SKILL.md | skill | 92 | Clean; InstallPlan CRD lifecycle and architecture diagram present |
| skills/kubesphere-devops-argocd/SKILL.md | skill | 93 | Duplicate Common Issues troubleshooting table (lines 640–649 and 677–684) |
| skills/kubesphere-volcano/SKILL.md | skill | 93 | Vague quantifier "appropriate" at line 713 without defining criterion |
| skills/frontend-integration-yaml/SKILL.md | skill | 93 | Clean; script delegation pattern is clean and well-bounded |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 4 |
| Low | 0 |

*Note: Pre-scan reported 2 critical pattern matches. After full analysis both resolved to false positives: binary download patterns in `hack/` build scaffolding scripts (downloading kubectl, helm, kind for CI) and a vendor utility — neither is a maintainer-controlled executable surface that agents invoke. The 1 High (xargs sh -c) was confirmed in the ks-crds Helm post-delete hook.*

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks (Helm) | `config/ks-core/charts/ks-crds/scripts/install.sh`, `config/ks-core/charts/ks-crds/scripts/post-delete.sh`, `config/ks-core/scripts/post-delete.sh` |
| Shell scripts | `skills/whizard-telemetry/scripts/generate-config.sh` |
| Python scripts | `skills/kubesphere-core/scripts/ks_api.py`, `skills/kubesphere-multi-tenant-management/scripts/ks_api.py`, `skills/frontend-integration-yaml/scripts/generate_frontend_integration.py` |
| MCP configs | 0 |
| Package manifests | 0 (no package.json or requirements.txt in scope) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | config/ks-core/charts/ks-crds/scripts/post-delete.sh | 33 | xargs-shell-injection | `kubectl get … | awk … | xargs -n 3 sh -c 'kubectl patch $2 -n $0 $1...'` interpolates resource names directly into a shell string; CRD/resource names cannot contain shell metacharacters in practice but the pattern matches the HIGH injection signature |
| 2 | Medium | skills/whizard-telemetry/scripts/generate-config.sh | 354 | plaintext-credential-output | `echo "  Password: ${OS_PASSWORD}"` prints the OpenSearch password (read from the `vector-sinks` Kubernetes Secret) to stdout; credential leaks to shell logs and terminal scrollback |
| 3 | Medium | skills/kubesphere-core/scripts/ks_api.py | 28 | insecure-token-storage | OAuth token cached to `~/.kubesphere_token` without `os.chmod(TOKEN_FILE, 0o600)`; world-readable on multi-user systems |
| 4 | Medium | skills/kubesphere-multi-tenant-management/scripts/ks_api.py | 28 | insecure-token-storage | Identical to kubesphere-core/scripts/ks_api.py (file is duplicated verbatim); same insecure token storage pattern |
| 5 | Medium | skills/kubesphere-devops-tenant/SKILL.md | 130 | hardcoded-credential | Password `P@88w0rd` hardcoded in documentation examples at lines 130, 803, and 867; readers may copy this into production configs |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | skills/kubesphere-devops-credentials/SKILL.md | API examples at lines 111, 134, and 469 use `"type": "Opaque"` — contradicts the explicit warning at lines 56–70 that Opaque type breaks Jenkins credential sync; the correct type is `credential.devops.kubesphere.io/basic-auth` (or the matching domain-specific type) | Agents following the examples will create credentials that silently fail to sync with Jenkins |
| 2 | skills/kubesphere-fluid/SKILL.md | YAML template at line 410: `low: "{{low}}` is missing its closing double-quote, producing invalid YAML | InstallPlan generated from this template will fail to parse |
| 3 | skills/whizard-logging/SKILL.md | Placeholder comment at line 106 says `# From Step 3` but the installation section defines only Step 1 and Step 2; correct reference is `From Step 2` | Agents will look for a non-existent step 3, causing confusion during installation |
| 4 | skills/kubesphere-devops-pipeline/SKILL.md | Line 323: `**Step 3b: For Private Repository (with credential):` is missing the closing `**`; the bold formatting is unclosed | Broken markdown renders incorrectly in rendered output; agents may misparse the section boundary |
| 5 | skills/kubesphere-devops-overview/SKILL.md | `Project Components` ASCII architecture diagram block appears twice (introduced at lines 92–125 and again later in the same file) | Redundant content increases cognitive load; automated doc tools may extract duplicate data |

## Security Fixes (PR-worthy, Medium/High)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | config/ks-core/charts/ks-crds/scripts/post-delete.sh | `xargs -n 3 sh -c` with kubectl-sourced resource names | Replace with `while read -r ns name crd; do kubectl patch "$crd" -n "$ns" "$name" ...; done` to avoid shell string interpolation |
| 2 | skills/whizard-telemetry/scripts/generate-config.sh | OpenSearch password echoed to stdout | Replace `echo "  Password: ${OS_PASSWORD}"` with `echo "  Password: [redacted — read from vector-sinks secret]"` |
| 3 | skills/kubesphere-core/scripts/ks_api.py | Token file world-readable | Add `os.chmod(TOKEN_FILE, 0o600)` immediately after writing the token; consider consolidating with the identical script in kubesphere-multi-tenant-management |
| 4 | skills/kubesphere-multi-tenant-management/scripts/ks_api.py | Identical insecure token storage; file duplicated verbatim from kubesphere-core | Apply same chmod fix; then deduplicate by making skills reference a shared ks_api.py or consolidating into one script location |
| 5 | skills/kubesphere-devops-tenant/SKILL.md | Hardcoded `P@88w0rd` in documentation at lines 130, 803, 867 | Replace all occurrences with `<YOUR_SECURE_PASSWORD>` placeholder |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/kubesphere-devops-argocd/SKILL.md | Common Issues troubleshooting table duplicated at lines 640–649 and 677–684; identical rows appear twice | -5 |
| 2 | skills/kubesphere-devops-pipeline/SKILL.md | Common Mistakes partial table at lines 1277–1282 is a duplicate of content earlier in the file | -3 |
| 3 | skills/kubesphere-devops-overview/SKILL.md | `Key Resources` heading appears twice, creating an ambiguous document structure | -3 |
| 4 | skills/kubesphere-devops-tenant/SKILL.md | `-H "Authorization: Bearer ${API_TOKEN}"` header appears twice in the List Pipelines curl example (lines 247–249); duplicate header in HTTP request | -2 |
| 5 | skills/kubesphere-devops-tenant/SKILL.md | Hardcoded password `P@88w0rd` used as example credential (lines 130, 803, 867); appears realistic enough that readers may use it in production | -5 |
| 6 | skills/kubesphere-volcano/SKILL.md | Vague quantifier "appropriate" at line 713 with no definition of what constitutes an appropriate value in context | -2 |

## Cross-Component
**Duplicated `ks_api.py`**: `skills/kubesphere-core/scripts/ks_api.py` and `skills/kubesphere-multi-tenant-management/scripts/ks_api.py` are byte-for-byte identical (245 lines each). Both carry the same insecure token storage pattern. Any fix must be applied to both files until they are consolidated; the security finding is currently double-counted because of the duplication. **Recommend extracting to a shared utility location.**

**Undocumented runtime dependency in `generate-config.sh`**: `skills/whizard-telemetry/scripts/generate-config.sh` reads the OpenSearch password from a Kubernetes Secret named `vector-sinks` (created by the vector extension). This cross-extension dependency is not documented in `skills/whizard-telemetry/SKILL.md` or `skills/vector/SKILL.md`. Agents invoking the script without vector installed will get a silent empty credential or script failure. **Recommend adding a prerequisite note to whizard-telemetry/SKILL.md.**

**Credential type contradiction in `kubesphere-devops-credentials`**: The skill explicitly warns (lines 56–70) that `type: Opaque` breaks Jenkins credential sync, yet the API examples at lines 111, 134, and 469 use `"type": "Opaque"`. This is an internal contradiction in a single file, but it also contradicts the usage documented in `skills/kubesphere-devops-tenant/SKILL.md` which creates credentials via the DevOps API without specifying `Opaque`. **The credential examples must be corrected before this skill can be trusted for PR-worthy output.**

## Recommendation
REVIEW — safe to submit PRs for bugs and medium/low security fixes; hold on high severity until confirmed.

**Reason**: One High-severity finding (`xargs -n 3 sh -c` in the ks-crds Helm post-delete hook) matches the shell injection pattern. Practical exploit risk is low because Kubernetes resource names are constrained characters, but the pattern must be fixed before the hook can be considered clean. No Critical patterns were confirmed in maintainer-controlled code.

**Action path**:
1. Submit PR for the `xargs sh -c` fix in `config/ks-core/charts/ks-crds/scripts/post-delete.sh` (High security).
2. Submit PR for the credential type bug in `skills/kubesphere-devops-credentials/SKILL.md` (lines 111, 134, 469) — highest-impact bug; silently breaks Jenkins sync.
3. Submit PR for `skills/kubesphere-fluid/SKILL.md` YAML syntax error (line 410).
4. Submit PR for `skills/whizard-telemetry/scripts/generate-config.sh` password echo (Medium security).
5. Submit PR to add `os.chmod(TOKEN_FILE, 0o600)` to both `ks_api.py` copies and open a follow-up issue to consolidate them (Medium security).
6. Submit PR for remaining doc bugs (wrong step ref in whizard-logging, missing `**` in devops-pipeline, hardcoded credential in devops-tenant).
7. File a quality PR for duplicate content in devops-argocd, devops-overview, devops-pipeline, devops-tenant, and the vague quantifier in volcano.
