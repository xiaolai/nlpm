<!--
Auto-prepared disclosure body for fivetaku/gptaku_plugins.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo fivetaku/gptaku_plugins \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/fivetaku-gptaku_plugins.md

After filing, record the URL with:
  jq '.repos["fivetaku/gptaku_plugins"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | plugins/insane-crawl/commands/insane-crawl.md | 15 | Bash + unsanitized `$ARGUMENTS` | User arguments are interpolated unquoted into `python3 -m engine $ARGUMENTS` with Bash allowed, so shell metacharacters can inject commands. |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/fivetaku-gptaku_plugins.md
