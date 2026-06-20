<!--
Auto-prepared disclosure body for AKCodez/hackingtool-plugin.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo AKCodez/hackingtool-plugin \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/AKCodez-hackingtool-plugin.md

After filing, record the URL with:
  jq '.repos["AKCodez/hackingtool-plugin"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | `scripts/ht_run.py` | 204–216, 347–348 | `bash-lc-string-concat` | `run_native` and `run_wsl` pass a concatenated command string (`cmds[0] + " " + args.args`) directly to `bash -lc`; user-supplied `--args` (e.g., target hostnames) land in that string unquoted, enabling shell injection via embedded metacharacters |
| 2 | High | `scripts/ht_run.py` | 204, 210, 386–407 | `sudo-auto-escalation` | On any `permission_denied` error, the runner automatically retries the full command with `sudo -n` without explicit per-invocation user consent; a tool that fails due to unrelated issues could escalate privileges silently |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/AKCodez-hackingtool-plugin.md
