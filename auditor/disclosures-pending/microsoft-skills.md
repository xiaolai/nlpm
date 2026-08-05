<!--
Auto-prepared disclosure body for microsoft/skills.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo microsoft/skills \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/microsoft-skills.md

After filing, record the URL with:
  jq '.repos["microsoft/skills"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | .github/plugins/azure-skills/skills/python-appservice-deploy/scripts/retry-az-create.sh | 36 | `eval "$VAR ..."` | `eval` executes caller-supplied `$SHOW_CMD`/`$CREATE_CMD` strings, passed in as `$1`/`$2` and documented as "single shell-quoted strings." Generic az-CLI retry wrapper by design, but any unsanitized data reaching these positional args gets full shell execution, not just an `az` invocation. |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/microsoft-skills.md
