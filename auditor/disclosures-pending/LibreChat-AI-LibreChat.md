<!--
Auto-prepared disclosure body for LibreChat-AI/LibreChat.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo LibreChat-AI/LibreChat \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/LibreChat-AI-LibreChat.md

After filing, record the URL with:
  jq '.repos["LibreChat-AI/LibreChat"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | config/deployed-update.js | 39 | sudo usage | Runs `sudo docker compose ...` (lines 39, 46, 53, 60, 69, 73) in an operator-run deployment update script. The commands are intended, not malicious. |
| 2 | High | config/update.js | 70 | sudo usage | Optional `sudo ` prefix for docker commands, selected by a `useSudo` flag. |
| 3 | High | scripts/static-checks.mts | 321 | spawn with shell: true | `shell: true` is used only on win32 for the fixed `npm.cmd` executable. No user input reaches the shell. Low real risk. |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/LibreChat-AI-LibreChat.md
