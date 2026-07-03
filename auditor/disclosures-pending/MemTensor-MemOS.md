<!--
Auto-prepared disclosure body for MemTensor/MemOS.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo MemTensor/MemOS \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/MemTensor-MemOS.md

After filing, record the URL with:
  jq '.repos["MemTensor/MemOS"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | apps/memos-local-openclaw/site/public/SKILL.md | 500 | curl-pipe-to-shell | `curl -fsSL https://cdn.memtensor.com.cn/memos-local-openclaw/install.sh \| bash` run as an unattended fallback installer with no checksum/signature verification |
| 2 | Critical | apps/memos-local-openclaw/site/public/SKILL.md | 505 | irm-pipe-iex | `irm https://cdn.memtensor.com.cn/memos-local-openclaw/install.ps1 \| iex` — PowerShell equivalent of curl\|bash, same lack of verification |
| 3 | Critical | apps/memos-local-openclaw/site/public/SKILL.md | 1182 | curl-pipe-to-shell | Same install.sh curl\|bash pattern repeated in the "Update" section |
| 4 | Critical | apps/memos-local-openclaw/site/public/SKILL.md | 1187 | irm-pipe-iex | Same irm\|iex pattern repeated in the "Update" section |
| 5 | Critical | apps/memos-local-openclaw/install.sh | 93 | download-then-exec-as-root | Downloads NodeSource's `setup_22.x` script over HTTPS to a temp file and immediately runs it via `bash` under `sudo`/root — functionally equivalent risk to curl\|bash with a file in between |
| 6 | Critical | apps/memos-local-plugin/install.sh | 178 | download-then-exec-as-root | Same NodeSource download-then-`run_with_privilege bash` pattern |
| 7 | High | apps/memos-local-openclaw/install.sh | 44 | sudo usage | `run_with_privilege()` transparently escalates any command to `sudo "$@"` whenever not already root |
| 8 | High | apps/memos-local-plugin/install.sh | 152 | sudo usage | Same `sudo "$@"` escalation helper |
| 9 | High | apps/memos-local-openclaw/package.json | 36 | postinstall script | `"postinstall": "node scripts/postinstall.cjs"` runs unattended on every `npm install`, including transitive installs |
| 10 | High | apps/memos-local-plugin/package.json | 63 | postinstall script | Same postinstall pattern (this package's script is a documented no-op unless `MEMOS_FORCE_POSTINSTALL=1`, which lowers practical risk) |
| 11 | High | apps/memos-local-openclaw/site/public/SKILL.md | 124 | pre-authorized remote-code-execution | "Granted permissions" section pre-authorizes the agent to run `curl \| bash` / `irm \| iex` installers "without further approval," removing the human-confirmation gate that would normally sit in front of finding #1 |
| 12 | High | apps/memos-local-openclaw/skill/browserwing-admin/SKILL.md | 52 | exposed remote-debugging port | Documents launching Chrome with `--remote-debugging-address=0.0.0.0 --no-sandbox`, exposing the full DevTools Protocol (arbitrary JS execution, file access) to the entire network with no authentication |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/MemTensor-MemOS.md
