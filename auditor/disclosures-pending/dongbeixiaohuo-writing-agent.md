<!--
Auto-prepared disclosure body for dongbeixiaohuo/writing-agent.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo dongbeixiaohuo/writing-agent \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/dongbeixiaohuo-writing-agent.md

After filing, record the URL with:
  jq '.repos["dongbeixiaohuo/writing-agent"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | `.claude/skills/公众号文章获取/scripts/readability_loader.js` | 15–17, 28–30 | eval with variable input, attacker-influenceable path | `SKILL_PATH` defaults to a fixed string but is overridable via `globalThis.__WEB_ARTICLE_EXTRACTOR_PATH__` (line 15-17); that path is joined with a filename and read via `fs.readFileSync` (line 28-29), then passed straight to `eval()` (line 30). Any code path in the same JS execution context that can set `globalThis.__WEB_ARTICLE_EXTRACTOR_PATH__` before this IIFE runs controls what file gets read and `eval`'d — an arbitrary-file-read-into-eval primitive, not just a static self-eval of a first-party file. Mitigating context: today nothing in this repo actually sets that global, so it is currently dead/unreachable, and the file it reads by default is the first-party `readability_extractor.js` sitting next to it. |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/dongbeixiaohuo-writing-agent.md
