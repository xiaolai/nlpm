<!--
Auto-prepared disclosure body for refly-ai/refly.
Backfilled on 2026-05-05T01:29:58Z after the v0.7.x audit
workflow's disclosure-pending step wrote files but never committed them
(see auditor-audit.yml fix in v0.7.23). The audit ran successfully on
2026-05-05; only the queue-write step's commit was missing.

To file manually:

  gh issue create --repo refly-ai/refly \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/refly-ai-refly.md

After filing, record the URL with:
  jq '.repos["refly-ai/refly"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | scripts/check-i18n-consistency.js | 91 | eval-equivalent (new Function) | `new Function(\`return ${str}\`)()` evaluates translation file content as JavaScript; if a translation file is maliciously crafted, arbitrary code executes in the developer's environment |
| 2 | High | package.json | 42 | postinstall-script | `"prepare": "husky"` runs automatically on `npm install`; standard husky pattern but executes code on install — see false_positive note in sidecar |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm-for-claude)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm-for-claude/blob/main/auditor/audits/refly-ai-refly.md
