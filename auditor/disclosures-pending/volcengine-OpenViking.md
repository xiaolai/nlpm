<!--
Auto-prepared disclosure body for volcengine/OpenViking.
The audit workflow's GITHUB_TOKEN cannot file issues on third-party
repos, so this body sits here pending manual filing:

  gh issue create --repo volcengine/OpenViking \
    --title 'Security findings in executable artifacts' \
    --body-file auditor/disclosures-pending/volcengine-OpenViking.md

After filing, record the URL with:
  jq '.repos["volcengine/OpenViking"] += {disclosure_url: "<URL>", disclosure_filed_at: "<ISO8601>", disclosure_filed_by: "manual"}' \
    auditor/registry/repos.json > /tmp/r.json && mv /tmp/r.json auditor/registry/repos.json
-->

## Security Findings in Executable Artifacts

While auditing NL programming artifacts in this repository, our scanner detected potential security issues in executable files.

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | openviking_cli/utils/ollama.py | 146 | curl-pipe-sh | `install_ollama()` macOS fallback runs `bash -c "curl -fsSL https://ollama.com/install.sh \| sh"` via `subprocess.run` at CLI runtime, no checksum/pin verification |
| 2 | Critical | openviking_cli/utils/ollama.py | 153 | curl-pipe-sh | Same function's Linux branch, identical unpinned remote-script execution |
| 3 | Critical | bot/deploy/Dockerfile | 7 | curl-pipe-bash | `curl -fsSL https://deb.nodesource.com/setup_20.x \| bash -` during image build |
| 4 | Critical | bot/deploy/Dockerfile | 10 | curl-pipe-sh | `curl -LsSf https://astral.sh/uv/install.sh \| sh` during image build |
| 5 | Critical | bot/deploy/docker/Dockerfile | 9 | curl-pipe-bash | Duplicate NodeSource pattern in the second (mounted-volume) deployment Dockerfile |
| 6 | Critical | bot/deploy/docker/Dockerfile | 11 | curl-pipe-sh | Duplicate uv-installer pattern in the second Dockerfile |
| 7 | Critical | .github/workflows/api_test.yml | 498 | curl-pipe-bash | CI step runs `curl -fsSL http://openviking.tos-cn-beijing.volces.com/cli/install.sh \| bash` (first-party domain, CI-only, but plain HTTP and no signature check) |
| 8 | High | bot/workspace/skills/opencode/opencode_utils.py | 18 | subprocess-shell-true | `execute_cmd()` runs an arbitrary string via `subprocess.run(cmd, shell=True, ...)`; this helper backs an LLM-driven bot skill, so the string can originate from model output |
| 9 | High | examples/openclaw-plugin/tests/e2e/test-archive-expand.py | 844 | subprocess-shell-true | `shell=True` call in test harness code; test-only scope, no production trigger |

### About This Report

These findings come from [NLPM](https://github.com/xiaolai/nlpm)'s security scanner, which checks executable surfaces (hooks, scripts, MCP configs, dependencies) against known-dangerous patterns.

We may be wrong — false positives happen. If any finding is intentional or already mitigated, please close this issue. If a finding is genuine and you'd like a fix PR, let us know.

Full audit report: https://github.com/xiaolai/nlpm/blob/main/auditor/audits/volcengine-OpenViking.md
