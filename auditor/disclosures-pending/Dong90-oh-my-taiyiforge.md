<!--
Auto-prepared disclosure body for Dong90/oh-my-taiyiforge.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo Dong90/oh-my-taiyiforge \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/Dong90-oh-my-taiyiforge.md

After filing, record the URL with:
  jq '.repos["Dong90/oh-my-taiyiforge"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | scripts/taiyi-forge.sh | 71 | SEC-new-function-eval | `eval "$TAIYI_CLI" "$@"` — eval with variable in main execution path; TAIYI_CLI can be attacker-controlled via TAIYI_FORGE_ROOT env var or `.taiyi/forge-root` file content, enabling arbitrary command injection |
| 2 | High | scripts/taiyi-forge.sh | 53 | SEC-new-function-eval | `_out=$(eval "$TAIYI_CLI" "$@" 2>"$_err")` — same eval-with-variable pattern inside npx fallback error handler; same command injection vector |
| 3 | High | package.json | 52 | SEC-postinstall-script | `"postinstall": "node postinstall.mjs"` — automatically executes build code on `npm install`; supply chain attack surface if package registry is compromised |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/Dong90-oh-my-taiyiforge.md
