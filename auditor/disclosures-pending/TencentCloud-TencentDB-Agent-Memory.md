<!--
Auto-prepared disclosure body for TencentCloud/TencentDB-Agent-Memory.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo TencentCloud/TencentDB-Agent-Memory \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/TencentCloud-TencentDB-Agent-Memory.md

After filing, record the URL with:
  jq '.repos["TencentCloud/TencentDB-Agent-Memory"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | MemoryCore/scripts/install-openclaw-plugin.sh | 247 | curl-pipe-sh | `curl -fsSL https://get.openclaw.dev \| bash`, run when `INSTALL_OPENCLAW=1`. It is opt-in and uses HTTPS, but there is no checksum or pin. |
| 2 | Critical | MemoryCore/scripts/install-hermes-plugin.sh | 11 | eval-variable | `eval echo "~$USERNAME"`. `USERNAME` comes from `INSTALL_AS_USER` or `SUDO_USER`, so a crafted value runs arbitrary commands. Often runs as root. |
| 3 | Critical | MemoryCore/scripts/install_hermes_memory_tencentdb.sh | 47 | eval-variable | `eval echo ~$USERNAME`, same issue with unquoted input. |
| 4 | Critical | agents/setup-proxy.sh | 27 | eval-variable | `prompt_input` runs `eval "$varname=\"${val:-$default}\""` on interactive input. `$(...)` or backticks in the answer are executed. |
| 5 | Critical | agents/setup-proxy.sh | 31 | eval-variable | `eval "$varname=\"$val\""` on user-typed input, same issue. |
| 6 | Critical | agents/skills/setup-proxy/setup-proxy.sh | 27 | eval-variable | Duplicate of #4 in the skill copy. |
| 7 | Critical | agents/skills/setup-proxy/setup-proxy.sh | 31 | eval-variable | Duplicate of #5 in the skill copy. |
| 8 | High | MemoryCore/scripts/install_hermes_memory_tencentdb.sh | 271 | sudo / write outside repo | `sudo tee /etc/profile.d/memory-tencentdb-env.sh` writes a system-wide profile script that is sourced by every login shell. `GATEWAY_CMD` is interpolated unescaped. |
| 9 | High | MemoryCore/package.json | 48 | postinstall-script | `postinstall` runs `bash scripts/openclaw-after-tool-call-messages.patch.sh 2>/dev/null \|\| true`. The script is not in the repo (see Bug #1), and the error suppression hides that. If a file with this name is ever added, it runs on every consumer's install. |
| 10 | High | MemoryProxy/scripts/proxy.sh | 47 | eval-variable | `eval "$(fnm env)"` executes the output of an external binary found on PATH. This is the common fnm idiom, so it is low-risk in practice. |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/TencentCloud-TencentDB-Agent-Memory.md
