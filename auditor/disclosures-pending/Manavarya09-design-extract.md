<!--
Auto-prepared disclosure body for Manavarya09/design-extract.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo Manavarya09/design-extract \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/Manavarya09-design-extract.md

After filing, record the URL with:
  jq '.repos["Manavarya09/design-extract"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH | package.json | 11 | SEC-postinstall-script | postinstall auto-runs `npx playwright install chromium --with-deps` on every `npm install`; `--with-deps` triggers OS-level system package installation (apt/brew) and may invoke sudo on Linux |
| 2 | HIGH | commands/battle.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang battle $ARGUMENTS` without quoting or sanitization; malformed or adversarial input can inject arbitrary shell commands |
| 3 | HIGH | commands/brand.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang brand $ARGUMENTS` without quoting or sanitization |
| 4 | HIGH | commands/extract.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang $ARGUMENTS` without quoting or sanitization |
| 5 | HIGH | commands/grade.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang grade $ARGUMENTS` without quoting or sanitization |
| 6 | HIGH | commands/pack.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang pack $ARGUMENTS` without quoting or sanitization |
| 7 | HIGH | commands/pair.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang pair $ARGUMENTS` without quoting or sanitization |
| 8 | HIGH | commands/remix.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang remix $ARGUMENTS` without quoting or sanitization |
| 9 | HIGH | commands/theme-swap.md | 9 | SEC-shell-injection | `$ARGUMENTS` interpolated into `npx designlang theme-swap $ARGUMENTS` without quoting or sanitization |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm-for-claude)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm-for-claude/blob/main/auditor/audits/Manavarya09-design-extract.md
