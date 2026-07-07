<!--
Auto-prepared disclosure body for mxyhi/ok-skills.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo mxyhi/ok-skills \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/mxyhi-ok-skills.md

After filing, record the URL with:
  jq '.repos["mxyhi/ok-skills"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | huashu-design/scripts/render-narration.sh | 79 | SEC-shell-injection | `$TIMELINE` (raw `--timeline=` CLI arg) is spliced unescaped into a single-quoted JS string inside `node -e "..."`; a path containing `'` or `` ` `` breaks out of the string and injects arbitrary JS executed by `node`. |
| 2 | High | huashu-design/scripts/render-narration.sh | 80 | SEC-shell-injection | Same unescaped `$TIMELINE` interpolation pattern, second `node -e` invocation reading `voiceover` path. |
| 3 | High | huashu-design/scripts/render-narration.sh | 89 | SEC-shell-injection | `$TOTAL_DURATION` (output of the line-79 `node -e`, itself reachable via the same injection chain) is re-interpolated unescaped into a further `node -e` arithmetic expression. |
| 4 | High | minimax-docx/scripts/setup.sh | 109, 111, 136, 139 | SEC-download-execute | Downloads Microsoft's `dotnet-install.sh` from `https://dot.net/v1/dotnet-install.sh` to `/tmp` via `wget`/`curl`, then `chmod +x` and executes it directly — no checksum or signature verification of the fetched script. |
| 5 | High | minimax-docx/scripts/setup.sh | 112, 113, 140, 141 | SEC-path-modification | Prepends `$HOME/.dotnet` to `PATH` for the current shell and permanently appends the same export line to `~/.bashrc`, mutating the user's shell startup config outside the repo. |
| 6 | High | minimax-docx/scripts/setup.sh | 107, 108, 117, 120, 123 | SEC-sudo-usage | Runs `sudo apt-get`/`dnf`/`pacman`/`zypper install` unprompted in every package-manager branch of the setup dispatch. |
| 7 | High | minimax-xlsx/scripts/xlsx_add_column.py | 94 | SEC-path-traversal | `find_ws_path()` builds `os.path.join(work_dir, "xl", rel.get("Target"))` from `workbook.xml.rels` `Target` (attacker-controlled xlsx content) with no `../` sanitization, then opens/overwrites that path — zip-slip on a crafted `.xlsx`. |
| 8 | High | minimax-xlsx/scripts/xlsx_insert_row.py | 88 | SEC-path-traversal | Identical unsanitized `rel.get("Target")` → `os.path.join` → parse/overwrite pattern as finding #7. |
| 9 | High | minimax-xlsx/scripts/style_audit.py | 467 | SEC-path-traversal | `_load_from_dir()` builds `os.path.join(unpacked_dir, "xl", rel_path)` from the same unsanitized rels `Target`; substring/`startswith` checks do not block `../` segments, allowing arbitrary file read into the audit report. |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/mxyhi-ok-skills.md
