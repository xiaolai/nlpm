<!--
Auto-prepared disclosure body for KKKKhazix/khazix-skills.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo KKKKhazix/khazix-skills \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/KKKKhazix-khazix-skills.md

After filing, record the URL with:
  jq '.repos["KKKKhazix/khazix-skills"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | README.md | 129 | curl-pipe-to-shell | `curl -fsSL https://aihot.virxact.com/aihot-skill/install.sh \| bash` — remote script piped directly into `bash` with no local review step shown at this point in the doc; the script's contents live outside this repo and cannot be verified from source control. |
| 2 | Critical | README.en.md | 129 | curl-pipe-to-shell | English mirror of finding #1, identical command. |
| 3 | High | aihot/README.md | 29 | curl-pipe-to-shell (process substitution) | `bash <(curl -fsSL .../install.sh) --target claude` — functionally equivalent to `curl \| bash` (downloads and executes without persisting a reviewable file first). |
| 4 | High | aihot/README.md | 32 | curl-pipe-to-shell (process substitution) | Same pattern, `--target codex`. |
| 5 | High | aihot/README.md | 35 | curl-pipe-to-shell (process substitution) | Same pattern, `--target gemini`. |
| 6 | High | aihot/README.md | 38 | curl-pipe-to-shell (process substitution) | Same pattern, `--target copilot`. |
| 7 | High | aihot/README.md | 41 | curl-pipe-to-shell (process substitution) | Same pattern, `--target opencode`. |
| 8 | High | aihot/README.md | 44 | curl-pipe-to-shell (process substitution) | Same pattern, `--target agents`. |
| 9 | High | aihot/README.md | 50 | curl-pipe-to-shell (process substitution) | Same pattern, custom `--dir` variant. |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/KKKKhazix-khazix-skills.md
