<!--
Auto-prepared disclosure body for VoltAgent/awesome-claude-code-subagents.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo VoltAgent/awesome-claude-code-subagents \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/VoltAgent-awesome-claude-code-subagents.md

After filing, record the URL with:
  jq '.repos["VoltAgent/awesome-claude-code-subagents"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | tools/subagent-catalog/fetch.md | 51 | unsanitized-arg-interpolation | `grep -iF "{{NAME}}" "$SUBAGENT_CATALOG_CACHE_FILE"` — the `{{NAME}}` placeholder is filled in from user-supplied `$ARGUMENTS` and substituted directly into the shell command template with no escaping guidance; an argument containing a `"` plus shell metacharacters can break out of the quoted string when the interpreting agent builds the literal Bash call. |
| 2 | High | tools/subagent-catalog/fetch.md | 60 | unsanitized-arg-interpolation | `curl -sf "$SUBAGENT_CATALOG_REPO_URL/{{PATH}}" -o "$tmp_file"` — `{{PATH}}` is substituted unsanitized into a curl URL/shell command with no validation of its contents, enabling path traversal or shell injection if the substituted value contains shell metacharacters. |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/VoltAgent-awesome-claude-code-subagents.md
