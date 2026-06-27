<!--
Auto-prepared disclosure body for zhaoxuya520/reverse-skill.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo zhaoxuya520/reverse-skill \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/zhaoxuya520-reverse-skill.md

After filing, record the URL with:
  jq '.repos["zhaoxuya520/reverse-skill"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | — | See full report | — | Multiple patterns | Critical/High patterns detected — see audit report for details |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/zhaoxuya520-reverse-skill.md
