<!--
Auto-prepared disclosure body for eze-is/web-access.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo eze-is/web-access \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/eze-is-web-access.md

After filing, record the URL with:
  jq '.repos["eze-is/web-access"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | scripts/cdp-proxy.mjs | 569 | SEC-path-traversal | `fs.writeFileSync(q.file, ...)` uses the raw `?file=` query parameter with no path validation; any local caller can write arbitrary data to any filesystem path accessible by the Node.js process |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/eze-is-web-access.md
