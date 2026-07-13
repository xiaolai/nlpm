<!--
Auto-prepared disclosure body for composio-community/awesome-claude-plugins.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo composio-community/awesome-claude-plugins \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/composio-community-awesome-claude-plugins.md

After filing, record the URL with:
  jq '.repos["composio-community/awesome-claude-plugins"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | skill-bus/commands/list-subs.md | 28 | unsanitized-arg-into-shell | `python3 "$SB_CLI" simulate <skill-name> --cwd "$PWD" --timing <pre\|post\|complete>` substitutes user-supplied values directly into the shell command line with no quoting |
| 2 | High | skill-bus/commands/report.md | 33 | unsanitized-arg-into-shell | `python3 "$SB_CLI" simulate [skill] --cwd "$PWD"` substitutes a suggestion-derived value directly into the shell command with no quotes |
| 3 | High | perf/commands/perf.md | 59 | arg-into-js-string-literal | `const args = argumentParser.parseArguments('$ARGUMENTS');` splices the raw `$ARGUMENTS` placeholder into a JS string literal executed via `node`, with no escaping |
| 4 | High | audit-project/commands/audit-project.md | 59 | arg-into-bash-conditional | `RESUME_MODE=$([ "${ARGUMENTS}" != "${ARGUMENTS%--resume*}" ] && echo true \|\| echo false)` interpolates raw `${ARGUMENTS}` into a bash test expression with no quoting |
| 5 | High | ship/commands/ship.md | 81 | arg-into-js-string-literal | `const args = '$ARGUMENTS'.split(' ');` splices the raw `$ARGUMENTS` placeholder into a JS string literal executed via `node`, with no escaping |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/composio-community-awesome-claude-plugins.md
