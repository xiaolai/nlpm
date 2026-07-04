<!--
Auto-prepared disclosure body for multica-ai/multica.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo multica-ai/multica \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/multica-ai-multica.md

After filing, record the URL with:
  jq '.repos["multica-ai/multica"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | scripts/install.sh | 5, 8, 430, 468 | SEC-curl-pipe-sh | Documented/advertised self-install invocation `curl -fsSL https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.sh \| bash`, mirrored as the PowerShell equivalent `irm ... \| iex` at `scripts/install.ps1:4,7`. This is the standard installer idiom used by rustup/Homebrew/Deno and is served from the project's own `raw.githubusercontent.com` path over HTTPS (not attacker-controlled), but it matches the CRITICAL pattern definition literally — pipe-to-shell of remote content with no local review step. |
| 2 | High | scripts/install.sh | 157-162 | SEC-missing-integrity-check | `install_cli_binary` downloads the release `.tar.gz` via `curl -fsSL ... -o` and extracts/installs it with **no checksum or signature verification** — contrast with the sibling `install.ps1:263-294`, which SHA256-verifies the same release asset against `checksums.txt` before installing. Deterministic gap: diffing the two installers for the same release artifact shows one path is unverified. |
| 3 | High | scripts/install.sh | 169-170 | SEC-sudo-usage | `install_cli_binary` falls back to `sudo mv "$tmp_dir/multica" "$bin_dir/multica"` when `/usr/local/bin` is not writable. Scoped to a single `mv` of a file already downloaded in the same function (not parameterized by external input), but sudo escalation in a piped installer is a real trust-boundary widening. |
| 4 | High | scripts/install.sh | 178-179, 187-195 | SEC-path-modification | `install_cli_binary` exports `PATH` for the current shell and `add_to_path()` appends an `export PATH=...` line to `~/.bashrc` / `~/.zshrc` when the target bin dir isn't already on `PATH`. |
| 5 | High | apps/desktop/package.json, apps/web/package.json, apps/docs/package.json | 33, 13, 12 | SEC-postinstall-script | `postinstall` scripts present: `electron-builder install-app-deps` (desktop), `fumadocs-mdx` (web, docs). Both are well-known, actively maintained framework tools invoked with no extra arguments or network calls beyond their normal build responsibilities — recorded per pattern match; reviewed content is benign. |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/multica-ai-multica.md
