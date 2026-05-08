<!--
Auto-prepared disclosure body for Q00/ouroboros.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo Q00/ouroboros \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/Q00-ouroboros.md

After filing, record the URL with:
  jq '.repos["Q00/ouroboros"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | skills/setup/SKILL.md | 185 | curl-pipe-sh | Skill instructs Claude to present `curl -LsSf https://astral.sh/uv/install.sh \| sh` inside a Bash code block. Claude Code may execute this directly when the user chooses "set up now", piping an external shell script into sh without integrity verification. |
| 2 | Critical | scripts/install.sh | 3 | curl-pipe-bash | The script is designed to be invoked via `curl -fsSL https://raw.githubusercontent.com/Q00/ouroboros/main/scripts/install.sh \| bash` (documented in line 3 comment and confirmed by project README). Any compromise of the GitHub repository or CDN delivers arbitrary code to installing users. |
| 3 | High | scripts/install.sh | 118 | curl-pipe-sh (echo) | `echo "Or switch to uv (recommended): curl -LsSf https://astral.sh/uv/install.sh \| sh"` — script instructs users to pipe a second external script into sh, compounding supply-chain risk. |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm-for-claude)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm-for-claude/blob/main/auditor/audits/Q00-ouroboros.md
