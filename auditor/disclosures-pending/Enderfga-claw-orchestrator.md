<!--
Auto-prepared disclosure body for Enderfga/claw-orchestrator.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo Enderfga/claw-orchestrator \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/Enderfga-claw-orchestrator.md

After filing, record the URL with:
  jq '.repos["Enderfga/claw-orchestrator"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | CLAUDE.md | 113 | security-disclosure-obfuscation | Documents a policy requiring developers to "Frame as a bland refactor" when patching previously hard-coded secrets, and to omit words like "security", "hard-coded", or "sanitize" from commit messages, CHANGELOG, release title, and release body. This actively prevents users of the npm package from identifying security-relevant releases and making informed upgrade decisions — a supply chain transparency anti-pattern. |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/Enderfga-claw-orchestrator.md
