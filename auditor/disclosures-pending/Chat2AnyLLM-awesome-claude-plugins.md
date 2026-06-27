<!--
Auto-prepared disclosure body for Chat2AnyLLM/awesome-claude-plugins.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo Chat2AnyLLM/awesome-claude-plugins \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/Chat2AnyLLM-awesome-claude-plugins.md

After filing, record the URL with:
  jq '.repos["Chat2AnyLLM/awesome-claude-plugins"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | scripts/metadata_catalog.py | 14 | SEC-credential-exfil | `_jget()` appends `Authorization: Bearer {token}` to every HTTP request, including calls with config-sourced `source["url"]` (line 22); no domain validation ensures token only goes to github.com; a malicious or compromised config.yaml (or the upstream awesome-repo-configs source it fetches from) can direct the GITHUB_TOKEN to an attacker-controlled host |
| 2 | High | .specify/scripts/bash/check-prerequisites.sh | 82 | SEC-new-function-eval | `eval $(get_feature_paths)` evaluates a heredoc that interpolates `$SPECIFY_FEATURE` env var via single-quoted assignment lines; a value containing `'` breaks heredoc single-quote delimiters and injects arbitrary shell commands; also reachable via a crafted git branch name if git's naming restrictions are bypassed |
| 3 | High | .specify/scripts/bash/update-agent-context.sh | 56 | SEC-new-function-eval | Same `eval $(get_feature_paths)` pattern; additionally writes output to CLAUDE.md and all other agent context files, meaning successful injection could backdoor agent context files served to developers |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/Chat2AnyLLM-awesome-claude-plugins.md
