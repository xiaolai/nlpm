<!--
Auto-prepared disclosure body for zubair-trabzada/ai-marketing-claude.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo zubair-trabzada/ai-marketing-claude \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/zubair-trabzada-ai-marketing-claude.md

After filing, record the URL with:
  jq '.repos["zubair-trabzada/ai-marketing-claude"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | README.md | 40 | curl piped to shell | One-command install instructs `curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/ai-marketing-claude/main/install.sh \| bash` — executes remote code with no integrity check (no checksum/signature pinning). Common installer pattern, but still an uncontrolled-execution surface per the rubric's literal CRITICAL criteria. |
| 2 | High | scripts/analyze_page.py | 306-308 | TLS certificate verification disabled | `fetch_page()` builds an SSL context with `check_hostname = False` and `verify_mode = ssl.CERT_NONE`, disabling certificate validation for all outbound HTTPS fetches (CWE-295). Enables MITM tampering of fetched marketing pages. |
| 3 | High | scripts/analyze_page.py | 342-344 | TLS certificate verification disabled | `fetch_sitemap()` repeats the same `CERT_NONE` / `check_hostname = False` pattern for the sitemap.xml fetch. |
| 4 | High | scripts/competitor_scanner.py | 177-179 | TLS certificate verification disabled | `fetch_page()` disables certificate verification identically to analyze_page.py, applied to every competitor URL scanned (including user- and LLM-supplied URLs). |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/zubair-trabzada-ai-marketing-claude.md
