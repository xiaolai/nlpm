<!--
Auto-prepared disclosure body for zscole/adversarial-spec.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo zscole/adversarial-spec \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/zscole-adversarial-spec.md

After filing, record the URL with:
  jq '.repos["zscole/adversarial-spec"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH | skills/adversarial-spec/SKILL.md | 364 | SEC-shell-injection | MODEL_LIST from AskUserQuestion is substituted directly into a Bash command template without quoting; a malicious "Other" model name entry (e.g. `gpt-4o; rm -rf ~`) could inject shell commands |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/zscole-adversarial-spec.md
