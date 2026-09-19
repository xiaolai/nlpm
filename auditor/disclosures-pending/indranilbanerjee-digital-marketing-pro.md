<!--
Auto-prepared disclosure body for indranilbanerjee/digital-marketing-pro.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo indranilbanerjee/digital-marketing-pro \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/indranilbanerjee-digital-marketing-pro.md

After filing, record the URL with:
  jq '.repos["indranilbanerjee/digital-marketing-pro"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | scripts/output-publisher.py | 77 | file-write-outside-repo | `get_visible_publish_dir()` resolves to `~/Documents/DigitalMarketingPro/{brand}`; `_publish_file()` copies artifacts there via `shutil.copy2()` — a write outside the repo/plugin sandbox into the user's home directory (documented "publish" feature, not attacker-controlled, but matches the HIGH pattern literally) |
| 2 | High | scripts/sync_model_registry.sh | 52 | file-write-outside-repo | Destination path is computed via `../` traversal to a sibling checkout outside the repo root, then written by the embedded Python `json.dump` at line 93; no curl-pipe-sh or unvalidated remote download present, but the write target itself escapes the repo tree |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/indranilbanerjee-digital-marketing-pro.md
