<!--
Auto-prepared disclosure body for buildatscale-tv/claude-code-plugins.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo buildatscale-tv/claude-code-plugins \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/buildatscale-tv-claude-code-plugins.md

After filing, record the URL with:
  jq '.repos["buildatscale-tv/claude-code-plugins"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | plugins/buildatscale/hooks/file-guard.sh | 13 | eval-with-variables | `eval "$(echo "$input" \| jq -r '@sh "tool_name=... file_path=..."')"` — eval with jq-processed external input. jq's `@sh` operator mitigates the risk substantially, but `eval` on any external data is a dangerous pattern; a jq version with a `@sh` escaping bug would allow command injection via a crafted `file_path` value in the hook JSON. |
| 2 | High | plugins/buildatscale/hooks/file-write-cleanup.sh | 11 | file-write-outside-repo | `echo "$(date): Hook triggered with input: $input" >> /tmp/claude-hook-debug.log` — writes the full PostToolUse hook JSON payload to a world-readable /tmp path. The payload includes `tool_input` (file_path, and for Write hooks, the full file content), which can expose code and credentials to any process on the same machine. Debug artifact left in production. |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/buildatscale-tv-claude-code-plugins.md
