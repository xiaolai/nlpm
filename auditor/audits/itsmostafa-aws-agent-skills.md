# NLPM Audit: itsmostafa/aws-agent-skills
**Date**: 2026-04-06  |  **Artifacts**: 18  |  **Strategy**: single
**NL Score**: 99/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 13  |  **Security Findings**: 6

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/ecs/SKILL.md | skill | 96 | 2× vague quantifiers: "properly", "appropriate" |
| skills/sqs/SKILL.md | skill | 96 | 2× vague quantifiers: "appropriate" × 2 |
| skills/api-gateway/SKILL.md | skill | 98 | Vague "appropriately" in reliability best practice |
| skills/bedrock/SKILL.md | skill | 98 | Vague "appropriate" in cost-optimization tip |
| skills/cloudwatch/SKILL.md | skill | 98 | Vague "meaningful" in metrics best practice |
| skills/cognito/SKILL.md | skill | 98 | Vague "proper" in UX best practice |
| skills/ec2/SKILL.md | skill | 98 | Vague "appropriate" in performance best practice |
| skills/eventbridge/SKILL.md | skill | 98 | Vague "meaningful" in event-design best practice |
| skills/lambda/SKILL.md | skill | 98 | Vague "appropriate" in cost-optimization tip |
| skills/rds/SKILL.md | skill | 98 | Vague "appropriate" in HA best practice |
| skills/step-functions/SKILL.md | skill | 98 | Vague "appropriate" in performance best practice |
| skills/cloudformation/SKILL.md | skill | 100 | None |
| skills/dynamodb/SKILL.md | skill | 100 | None |
| skills/eks/SKILL.md | skill | 100 | None |
| skills/iam/SKILL.md | skill | 100 | None |
| skills/s3/SKILL.md | skill | 100 | None |
| skills/secrets-manager/SKILL.md | skill | 100 | None |
| skills/sns/SKILL.md | skill | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 4 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | None |
| Scripts | scripts/check-aws-updates.py, scripts/generate-update-issues.py |
| MCP configs | None |
| Package manifests | scripts/requirements.txt |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | scripts/check-aws-updates.py | 138, 171 | network-call | feedparser.parse() makes outbound HTTP requests to AWS RSS feeds and the AWS What's New feed — expected for a doc-sync script but represents a network egress surface |
| 2 | Medium | scripts/check-aws-updates.py | 257–260 | env-var-access | Reads GITHUB_OUTPUT env var and writes pipeline outputs to it — standard GitHub Actions pattern but worth noting as env-var consumption |
| 3 | Low | scripts/generate-update-issues.py | 69–82 | subprocess-untrusted-input | subprocess.run() passes RSS-derived title and body as arguments to `gh issue create`; shell=False prevents injection, but untrusted content flows into CLI arguments without sanitisation |
| 4 | Low | scripts/requirements.txt | 1 | unpinned-semver | feedparser>=6.0.0 — lower-bound only; could resolve to any future major version including breaking changes |
| 5 | Low | scripts/requirements.txt | 2 | unpinned-semver | requests>=2.28.0 — lower-bound only; also appears unused (not imported by either script — likely a transitive pin for feedparser) |
| 6 | Low | scripts/requirements.txt | 3 | unpinned-semver | PyYAML>=6.0 — lower-bound only; not imported by either script in this repo |

## Bugs (PR-worthy)
No bugs found. All 18 skill files have required `name` and `description` frontmatter. No broken references or undeclared tool usage detected.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/check-aws-updates.py | feedparser.parse() has no timeout | Pass `handlers` or wrap call: set socket timeout before calling; or use `requests` with timeout and pass raw feed text to feedparser |
| 2 | scripts/generate-update-issues.py | RSS-derived strings passed to subprocess without length or character validation | Truncate/sanitise title and body to safe lengths before building the `cmd` list |
| 3 | scripts/requirements.txt | feedparser pinned with lower-bound only | Pin to exact version: `feedparser==6.0.11` (or latest known-good) |
| 4 | scripts/requirements.txt | requests listed but not directly used | Remove from requirements.txt if only a transitive dep, or pin it: `requests==2.32.3` |
| 5 | scripts/requirements.txt | PyYAML listed but not imported | Remove unused dependency or pin: `PyYAML==6.0.2` |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/api-gateway/SKILL.md | "Configure timeout **appropriately**" (Reliability best practices, ~line 275) — no criteria given | R01 -2 |
| 2 | skills/bedrock/SKILL.md | "Use **appropriate** models: Smaller models for simple tasks" (Cost Optimization, ~line 271) — "appropriate" without measurable threshold | R01 -2 |
| 3 | skills/cloudwatch/SKILL.md | "Set **meaningful** units for custom metrics" (Metrics best practices, ~line 301) — "meaningful" without definition | R01 -2 |
| 4 | skills/cognito/SKILL.md | "Implement **proper** error handling" (User Experience best practices, ~line 261) — "proper" without specification | R01 -2 |
| 5 | skills/ec2/SKILL.md | "Choose **appropriate** EBS volume type" (Performance best practices, ~line 272) — "appropriate" without criteria | R01 -2 |
| 6 | skills/ecs/SKILL.md | "Configure health checks **properly**" (Reliability best practices, ~line 251) — "properly" without specification | R01 -2 |
| 7 | skills/ecs/SKILL.md | "Set **appropriate** deregistration delay" (Reliability best practices, ~line 252) — "appropriate" without criteria | R01 -2 |
| 8 | skills/eventbridge/SKILL.md | "Use **meaningful** source names" (Event Design best practices, ~line 254) — "meaningful" without definition | R01 -2 |
| 9 | skills/lambda/SKILL.md | "Set **appropriate** timeout" (Cost Optimization, ~line 213) — "appropriate" without criteria | R01 -2 |
| 10 | skills/rds/SKILL.md | "Configure **appropriate** backup retention" (High Availability best practices, ~line 257) — "appropriate" without criteria | R01 -2 |
| 11 | skills/sqs/SKILL.md | "Configure **appropriate** visibility timeout (> processing time)" (Message Processing, ~line 245) — "appropriate" without numeric guidance | R01 -2 |
| 12 | skills/sqs/SKILL.md | "Set **appropriate** maxReceiveCount (usually 3-5)" (Dead-Letter Queues, ~line 250) — "appropriate" weakens the useful concrete range given | R01 -2 |
| 13 | skills/step-functions/SKILL.md | "Set **appropriate** timeouts" (Performance best practices, ~line 338) — "appropriate" without criteria | R01 -2 |

## Cross-Component
All 18 skill files share an identical structure (frontmatter → ToC → Core Concepts → Common Patterns → CLI Reference → Best Practices → Troubleshooting → References) and were batch-updated on the same date (`last_updated: "2026-01-07"`). No cross-references between skills exist, so no broken relative paths or circular references are present.

The automation scripts (`scripts/check-aws-updates.py`, `scripts/generate-update-issues.py`) reference the `skills/{service}/SKILL.md` path pattern in comments only — they don't parse or read the skill files directly, so there is no hard coupling that could break.

Four services (`cloudformation`, `cognito`, `eventbridge`, `bedrock`) have no dedicated AWS RSS feeds and fall back to the AWS What's New feed in `check-aws-updates.py`; this is intentional and documented in the script.

No orphaned components, stale counts, or terminology drift detected.

## Recommendation
CLEAR — submit PRs for all 13 quality issues (replace vague quantifiers with measurable guidance) and all 5 medium/low security fixes (pin dependencies, add subprocess sanitisation). No private disclosure required; no critical or high findings.
