<!--
Auto-prepared disclosure body for Gentleman-Programming/gentle-ai.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo Gentleman-Programming/gentle-ai \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/Gentleman-Programming-gentle-ai.md

After filing, record the URL with:
  jq '.repos["Gentleman-Programming/gentle-ai"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | deploy/telemetry/install.sh | 215 | curl piped to shell | Fallback `curl -fsS https://rclone.org/install.sh \| bash` runs a remote script as root, with no checksum or pin, when `dnf install rclone` fails. |
| 2 | High | scripts/install.sh | 565 | sudo usage | `sudo -- bash -c 'install ... && mv ...'` runs when the install dir is not writable. Arguments are quoted positionals, so it looks safe but is still privilege escalation. |
| 3 | High | e2e/lib.sh | 139 | PATH modification | Test helper prepends a fake bin dir to PATH. This is scoped to the test harness. |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/Gentleman-Programming-gentle-ai.md
