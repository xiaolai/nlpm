<!--
Auto-prepared disclosure body for SimoneAvogadro/android-reverse-engineering-skill.
Backfilled on 2026-05-05T01:29:58Z after the v0.7.x audit
workflow's disclosure-pending step wrote files but never committed them
(see auditor-audit.yml fix in v0.7.23). The audit ran successfully on
2026-05-05; only the queue-write step's commit was missing.

To file manually:

  gh issue create --repo SimoneAvogadro/android-reverse-engineering-skill \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/SimoneAvogadro-android-reverse-engineering-skill.md

After filing, record the URL with:
  jq '.repos["SimoneAvogadro/android-reverse-engineering-skill"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH | plugins/android-reverse-engineering/skills/android-reverse-engineering/scripts/install-dep.sh | 92, 99, 105 | SEC-sudo | `pkg_install()` invokes `sudo apt-get`, `sudo dnf`, `sudo pacman`; package names are hardcoded so no injection risk, but sudo elevation is unconditional if available |
| 2 | HIGH | plugins/android-reverse-engineering/skills/android-reverse-engineering/scripts/install-dep.sh | 144–163, 244, 309, 385 | SEC-path-modification | `add_to_profile()` appends `export PATH=...` and `export FERNFLOWER_JAR_PATH=...` to `~/.zshrc`, `~/.bashrc`, or `~/.profile` — persistent file writes outside the repo and permanent PATH modification |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm-for-claude)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm-for-claude/blob/main/auditor/audits/SimoneAvogadro-android-reverse-engineering-skill.md
