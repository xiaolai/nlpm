# NLPM Audit: indranilbanerjee/digital-marketing-pro
**Date**: 2026-04-06  |  **Artifacts**: 202  |  **Strategy**: progressive
**NL Score**: 91/100
**Security**: BLOCKED
**Bugs**: 3  |  **Quality Issues**: 101  |  **Security Findings**: 23

This pass scored 100 of the repo's 202 artifacts (24 agents, 65 skills, 9 commands, `hooks/hooks.json`, `.claude-plugin/plugin.json`) and ran a detailed security scan of all 87 executable scripts plus `package.json` / `scripts/requirements.txt`. `hooks/hooks.json` currently ships zero active hooks (all prior hooks were intentionally disabled and documented in-file — see `hooks/hooks-reference.example.json`).

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/backlink-gap.md | command | 75 | Bash + Write used without `allowed-tools` declared |
| agents/analytics-analyst.md | agent | 76 | Zero `<example>` blocks |
| agents/brand-guardian.md | agent | 76 | Zero `<example>` blocks |
| agents/execution-coordinator.md | agent | 77 | Zero `<example>` blocks |
| agents/content-creator.md | agent | 78 | Zero `<example>` blocks |
| agents/media-buyer.md | agent | 78 | Zero `<example>` blocks |
| agents/marketing-strategist.md | agent | 78 | Zero `<example>` blocks |
| agents/pr-outreach.md | agent | 78 | Zero `<example>` blocks |
| agents/memory-manager.md | agent | 78 | Zero `<example>` blocks |
| agents/performance-monitor-agent.md | agent | 78 | Zero `<example>` blocks |
| agents/market-intelligence.md | agent | 78 | Zero `<example>` blocks |
| agents/cro-specialist.md | agent | 80 | Zero `<example>` blocks |
| agents/influencer-manager.md | agent | 80 | Zero `<example>` blocks |
| agents/intelligence-curator.md | agent | 80 | Zero `<example>` blocks |
| agents/journey-orchestrator.md | agent | 80 | Zero `<example>` blocks |
| agents/marketing-scientist.md | agent | 80 | Zero `<example>` blocks |
| agents/growth-engineer.md | agent | 80 | Zero `<example>` blocks |
| agents/social-media-manager.md | agent | 80 | Zero `<example>` blocks |
| agents/competitive-intel.md | agent | 80 | Zero `<example>` blocks |
| agents/crm-manager.md | agent | 80 | Zero `<example>` blocks |
| agents/agency-operations.md | agent | 80 | Zero `<example>` blocks |
| agents/localization-specialist.md | agent | 80 | Zero `<example>` blocks |
| agents/seo-specialist.md | agent | 80 | Zero `<example>` blocks |
| agents/email-specialist.md | agent | 80 | Zero `<example>` blocks |
| commands/email-sequence.md | command | 83 | Multi-step sequence design not numbered |
| agents/quality-assurance.md | agent | 85 | Zero `<example>` blocks |
| commands/competitor-analysis.md | command | 85 | `Task` tool used without `allowed-tools` declaration |
| commands/seo-audit.md | command | 85 | `Bash` used without `allowed-tools` declared |
| commands/check.md | command | 90 | No empty-input handling for required argument |
| commands/execute-action.md | command | 90 | No empty-input handling for required `--action` flag |
| skills/marketing-automation/SKILL.md | skill | 92 | 4 vague quantifiers ("reasonable"/"appropriate"/"correctly") |
| skills/review-response/SKILL.md | skill | 92 | 4 vague quantifiers ("relevant"/"appropriate") |
| skills/send-report/SKILL.md | skill | 94 | 3 vague quantifiers ("appropriate") |
| skills/client-proposal/SKILL.md | skill | 94 | 3 vague quantifiers ("relevant") |
| skills/launch-campaign/SKILL.md | skill | 94 | 2 unused declared tools (Glob, Grep) |
| commands/cowork-setup.md | command | 95 | Missing `allowed-tools` frontmatter field |
| commands/brand-setup.md | command | 95 | Missing `allowed-tools` frontmatter field |
| skills/language-audit/SKILL.md | skill | 96 | 2 vague quantifiers ("relevant"/"correctly") |
| skills/lead-import/SKILL.md | skill | 96 | 2 vague quantifiers ("relevant"/"correctly") |
| skills/live-dashboard/SKILL.md | skill | 96 | 2 vague quantifiers ("appropriate") |
| skills/add-integration/SKILL.md | skill | 96 | 2 vague quantifiers ("appropriate") |
| skills/campaign-orchestrator/SKILL.md | skill | 96 | 2 vague quantifiers ("correctly"/"appropriate") |
| skills/programmatic-seo/SKILL.md | skill | 98 | 1 vague quantifier ("sufficient") |
| skills/executive-dashboard/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/import-template/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/analytics-insights/SKILL.md | skill | 98 | 1 vague quantifier ("correctly") |
| skills/eval-content/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/prompt-test/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/entity-audit/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/pr-pitch/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/qbr-plan/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/webinar-plan/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/eval-config/SKILL.md | skill | 98 | 1 vague quantifier ("appropriate") |
| skills/martech-audit/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/funnel-audit/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/seo-audit/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/journey-design/SKILL.md | skill | 98 | 1 vague quantifier ("objective-appropriate") |
| skills/local-seo-audit/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/cro/SKILL.md | skill | 98 | 1 vague quantifier ("sufficient") |
| skills/team-assign/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/campaign-plan/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/aeo-audit/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/performance-report/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/pipeline-update/SKILL.md | skill | 98 | 1 vague quantifier ("relevant") |
| skills/what-if/SKILL.md | skill | 100 | none |
| skills/budget-tracker/SKILL.md | skill | 100 | none |
| skills/dark-funnel/SKILL.md | skill | 100 | none |
| skills/quality-report/SKILL.md | skill | 100 | none |
| skills/audience-intelligence/SKILL.md | skill | 100 | none |
| skills/c2pa-metadata/SKILL.md | skill | 100 | none |
| skills/recall/SKILL.md | skill | 100 | none |
| skills/intelligence-report/SKILL.md | skill | 100 | none |
| skills/seo-plan/SKILL.md | skill | 100 | none |
| skills/ab-test-plan/SKILL.md | skill | 100 | none |
| skills/focus-group/SKILL.md | skill | 100 | none |
| skills/share-of-voice/SKILL.md | skill | 100 | none |
| skills/autopilot-status/SKILL.md | skill | 100 | none |
| skills/campaign-audit/SKILL.md | skill | 100 | none |
| skills/agency-dashboard/SKILL.md | skill | 100 | none |
| skills/status/SKILL.md | skill | 100 | none |
| skills/influencer-creator/SKILL.md | skill | 100 | none |
| skills/sop-library/SKILL.md | skill | 100 | none |
| skills/search-knowledge/SKILL.md | skill | 100 | none |
| skills/market-weather/SKILL.md | skill | 100 | none |
| skills/simulate/SKILL.md | skill | 100 | none |
| skills/language-config/SKILL.md | skill | 100 | none |
| skills/local-seo/SKILL.md | skill | 100 | none |
| skills/narrative-tracker/SKILL.md | skill | 100 | none |
| skills/client-report/SKILL.md | skill | 100 | none |
| skills/content-repurpose/SKILL.md | skill | 100 | none |
| skills/cohort-analysis/SKILL.md | skill | 100 | none |
| skills/send-notification/SKILL.md | skill | 100 | none |
| skills/redirect-manager/SKILL.md | skill | 100 | none |
| skills/anomaly-scan/SKILL.md | skill | 100 | none |
| skills/four-core-documents/SKILL.md | skill | 100 | none |
| skills/competitor-pages/SKILL.md | skill | 100 | none |
| skills/integrations/SKILL.md | skill | 100 | none |
| commands/doctor.md | command | 100 | none |
| hooks/hooks.json | config | 100 | none |
| .claude-plugin/plugin.json | config | 100 | none |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 |
| Medium | 20 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | `hooks/hooks.json` (1 file; declares zero active hooks) |
| Scripts | `scripts/*.py` (86) + `scripts/sync_model_registry.sh` (1) = 87 files |
| MCP configs | none found (no `.mcp.json` in repo) |
| Package manifests | `package.json` (root, npm), `scripts/requirements.txt` (pip) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | scripts/output-publisher.py | 77 | file-write-outside-repo | `get_visible_publish_dir()` resolves to `~/Documents/DigitalMarketingPro/{brand}`; `_publish_file()` copies artifacts there via `shutil.copy2()` — a write outside the repo/plugin sandbox into the user's home directory (documented "publish" feature, not attacker-controlled, but matches the HIGH pattern literally) |
| 2 | High | scripts/sync_model_registry.sh | 52 | file-write-outside-repo | Destination path is computed via `../` traversal to a sibling checkout outside the repo root, then written by the embedded Python `json.dump` at line 93; no curl-pipe-sh or unvalidated remote download present, but the write target itself escapes the repo tree |
| 3 | Medium | scripts/ai-visibility-checker.py | 164 | env-var-access | Reads `os.environ.get("OPENAI_API_KEY")` to authenticate outbound OpenAI API calls |
| 4 | Medium | scripts/ai-visibility-checker.py | 173 | network-call | Sends user-supplied query text to the OpenAI chat completions API |
| 5 | Medium | scripts/ai-visibility-checker.py | 204 | env-var-access | Reads `os.environ.get("ANTHROPIC_API_KEY")` to authenticate outbound Anthropic API calls |
| 6 | Medium | scripts/ai-visibility-checker.py | 213 | network-call | Sends user-supplied query text to the Anthropic messages API |
| 7 | Medium | scripts/brand-voice-scorer.py | 73 | network-call | `nltk.download()` silently fetches tokenizer/tagger corpus data from NLTK's remote server on first run |
| 8 | Medium | scripts/competitor-scraper.py | 75 | network-call | Fetches `robots.txt` from a host derived from the user-supplied `--url` argument (destination not hardcoded) |
| 9 | Medium | scripts/competitor-scraper.py | 168 | network-call | Fetches full page content from the user-supplied `--url` argument (arbitrary destination) |
| 10 | Medium | scripts/connector_executor.py | 269 | env-var-access | Loads entire `os.environ` as the default credential source (SLACK_BOT_TOKEN, HUBSPOT_PRIVATE_APP_TOKEN, KLAVIYO_PRIVATE_KEY, SENDGRID_API_KEY, BREVO_API_KEY, CUSTOMERIO_APP_API_KEY, MAILCHIMP_API_KEY, AHREFS_API_KEY, etc.) |
| 11 | Medium | scripts/connector_executor.py | 331 | network-call | Fires outbound HTTP requests via `urllib` to hardcoded per-connector vendor endpoints (e.g. api.hubapi.com, a.klaviyo.com) with injected credentials |
| 12 | Medium | scripts/credential-manager.py | 173 | env-var-access | `os.environ.get(v)` reads arbitrary env-var names from a stored profile JSON to check whether platform credentials are configured (boolean presence check only, no value exfiltration) |
| 13 | Medium | scripts/embed-c2pa.py | 104 | runtime-package-install | `subprocess.check_call` runs `pip install --quiet c2pa-python>=0.32` at runtime if the module is missing |
| 14 | Medium | scripts/crm-sync.py | 367 | env-var-access | `os.environ.get(env_var)` reads secret-sounding CRM token vars (SALESFORCE_ACCESS_TOKEN, HUBSPOT_ACCESS_TOKEN, ZOHO_REFRESH_TOKEN, PIPEDRIVE_API_TOKEN) to report connection status (boolean check only) |
| 15 | Medium | scripts/memory-manager.py | 360 | env-var-access | `os.environ.get(env_var)` reads secret-sounding memory-service API key vars (PINECONE_API_KEY, QDRANT_API_KEY, SUPERMEMORY_API_KEY, GRAPHITI_API_KEY) to report connection status (boolean check only) |
| 16 | Medium | scripts/refresh_models.py | 53 | env-var-access + network-call | Reads `ANTHROPIC_API_KEY` and sends it as an `x-api-key` header to hardcoded `https://api.anthropic.com/v1/models` |
| 17 | Medium | scripts/refresh_models.py | 66 | env-var-access + network-call | Reads `OPENAI_API_KEY` and sends it as a Bearer token to hardcoded `https://api.openai.com/v1/models` |
| 18 | Medium | scripts/refresh_models.py | 79 | env-var-access + network-call | Reads `GEMINI_API_KEY` and appends it as a `?key=` query param to hardcoded `generativelanguage.googleapis.com` |
| 19 | Medium | scripts/refresh_models.py | 96 | env-var-access + network-call | Reads `EVOLINK_API_KEY` and sends it as a Bearer token to hardcoded `https://direct.evolink.ai/v1/models` (lesser-known third-party host) |
| 20 | Medium | scripts/tech-seo-auditor.py | 134 | network-call-ssrf | `opener.open()` fetches an arbitrary caller-supplied URL (from `--url`/`--urls`/`--file`) with manual redirect-following and no destination allow-list — inherent to the tool's stated purpose but unrestricted network egress |
| 21 | Medium | scripts/setup.py | 274 | runtime-package-install | `subprocess.check_call()` invokes `pip install` at runtime for LITE_DEPS/FULL_DEPS package lists |
| 22 | Medium | scripts/setup.py | 285 | network-call | `nltk.download()` fetches NLTK corpus data from NLTK's remote distribution servers at runtime |
| 23 | Low | scripts/requirements.txt | 10 | unpinned-semver | `nltk>=3.8`, `textstat>=0.7`, `beautifulsoup4>=4.12`, `requests>=2.31` all use `>=` range pins instead of exact `==` pins |

No CRITICAL patterns were found in any of the 87 scripts scanned: no `eval`/`exec` on untrusted input, no curl/wget-piped-to-shell, no reverse shells, no base64-decode-then-exec, no credential exfiltration over the network, and no backdoors. No `subprocess(shell=True)`, `os.system()`, `sudo`, PATH manipulation, or postinstall auto-run scripts were found. No `bash_arg_injection` findings were found in any of the 9 scanned commands (none pass `$ARGUMENTS`/`$1` directly into an unsanitized shell invocation).

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/backlink-gap.md | Body instructs running `scripts/backlink_gap.py` (Bash) and writing `PLAN.md` (Write), but frontmatter declares no `allowed-tools` at all | Command may be denied or prompt for unexpected permissions at runtime since neither tool is authorized in frontmatter |
| 2 | commands/competitor-analysis.md | Body instructs dispatching "seven parallel `Task` tool calls" but `Task` is not declared in `allowed-tools` (frontmatter has none) | Same — undeclared tool use breaks the least-privilege contract and risks runtime denial |
| 3 | commands/seo-audit.md | Body instructs running `scripts/link-profile-analyzer.py` via Bash but no `allowed-tools` is declared | Same — undeclared Bash use |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/ai-visibility-checker.py:164,204 | Reads OpenAI/Anthropic API keys from env for outbound calls | Document required env vars in the script's docstring/README and confirm keys are never logged; no code change required if this is intentional |
| 2 | scripts/brand-voice-scorer.py:73 | `nltk.download()` performs a silent first-run network fetch | Pre-bundle the NLTK corpus in the package or gate the download behind an explicit `--allow-network-fetch` flag with a printed warning |
| 3 | scripts/competitor-scraper.py:75,168 | Fetches arbitrary user-supplied URLs (robots.txt + page content) | Add a scheme allow-list (http/https only) and reject `file://`/`localhost`/private-IP targets to reduce SSRF surface |
| 4 | scripts/connector_executor.py:269 | Loads entire `os.environ` to source credentials rather than an explicit named list | Read only the specific env-var names required per connector instead of the full environment dict |
| 5 | scripts/connector_executor.py:331 | Outbound requests to vendor endpoints with injected credentials | Confirm TLS is enforced and credentials are never included in error/log output |
| 6 | scripts/credential-manager.py:173 | Iterates arbitrary env-var names from a stored profile | Validate profile env-var names against an allow-list before calling `os.environ.get()` |
| 7 | scripts/embed-c2pa.py:104 | Runtime `pip install` of `c2pa-python` when missing | Move to a declared `requirements.txt`/`pyproject.toml` dependency and fail with a clear install instruction instead of auto-installing |
| 8 | scripts/crm-sync.py:367 | Reads CRM token env vars for presence-check only | No behavior change needed; add a comment noting only presence (not value) is read, to make the intent auditable |
| 9 | scripts/memory-manager.py:360 | Reads memory-service API key env vars for presence-check only | Same as above — document intent inline |
| 10 | scripts/refresh_models.py:53,66,79,96 | Reads 4 provider API keys and sends them to 4 hardcoded external hosts (including the lesser-known `direct.evolink.ai`) | Document all 4 outbound hosts in the script header; consider making the EVOLINK provider opt-in via a flag since it's a non-major vendor |
| 11 | scripts/tech-seo-auditor.py:134 | Unrestricted URL fetch (SSRF surface) from caller-supplied targets | Add a private-IP/localhost block-list before opening the connection |
| 12 | scripts/setup.py:274 | Runtime `pip install` of dependency lists | Prefer `requirements.txt` + documented `pip install -r requirements.txt` setup step over an in-script installer |
| 13 | scripts/setup.py:285 | `nltk.download()` network fetch at runtime | Same as brand-voice-scorer.py — pre-bundle or gate behind explicit flag |
| 14 | scripts/requirements.txt:10-15 | `nltk`, `textstat`, `beautifulsoup4`, `requests` pinned with `>=` instead of `==` | Pin exact versions (or use a lockfile) to make builds reproducible and avoid surprise upstream breakage |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/analytics-analyst.md | No `model:` field in frontmatter | -5 |
| 2 | agents/analytics-analyst.md | Zero `<example>` blocks in agent body | -15 |
| 3 | agents/analytics-analyst.md | 2 vague quantifiers ("appropriate", "sufficient") | -4 |
| 4 | agents/cro-specialist.md | No `model:` field in frontmatter | -5 |
| 5 | agents/cro-specialist.md | Zero `<example>` blocks | -15 |
| 6 | agents/influencer-manager.md | No `model:` field in frontmatter | -5 |
| 7 | agents/influencer-manager.md | Zero `<example>` blocks | -15 |
| 8 | agents/content-creator.md | No `model:` field in frontmatter | -5 |
| 9 | agents/content-creator.md | Zero `<example>` blocks | -15 |
| 10 | agents/content-creator.md | 1 vague quantifier ("appropriate") | -2 |
| 11 | agents/intelligence-curator.md | No `model:` field in frontmatter | -5 |
| 12 | agents/intelligence-curator.md | Zero `<example>` blocks | -15 |
| 13 | agents/journey-orchestrator.md | No `model:` field in frontmatter | -5 |
| 14 | agents/journey-orchestrator.md | Zero `<example>` blocks | -15 |
| 15 | agents/media-buyer.md | No `model:` field in frontmatter | -5 |
| 16 | agents/media-buyer.md | Zero `<example>` blocks | -15 |
| 17 | agents/media-buyer.md | 1 vague quantifier ("appropriate") | -2 |
| 18 | agents/marketing-scientist.md | No `model:` field in frontmatter | -5 |
| 19 | agents/marketing-scientist.md | Zero `<example>` blocks | -15 |
| 20 | agents/growth-engineer.md | No `model:` field in frontmatter | -5 |
| 21 | agents/growth-engineer.md | Zero `<example>` blocks | -15 |
| 22 | agents/social-media-manager.md | No `model:` field in frontmatter | -5 |
| 23 | agents/social-media-manager.md | Zero `<example>` blocks | -15 |
| 24 | agents/marketing-strategist.md | No `model:` field in frontmatter | -5 |
| 25 | agents/marketing-strategist.md | Zero `<example>` blocks | -15 |
| 26 | agents/marketing-strategist.md | 1 vague quantifier ("appropriate") | -2 |
| 27 | agents/quality-assurance.md | Zero `<example>` blocks | -15 |
| 28 | agents/brand-guardian.md | No `model:` field in frontmatter | -5 |
| 29 | agents/brand-guardian.md | Zero `<example>` blocks | -15 |
| 30 | agents/brand-guardian.md | 2 vague quantifiers ("appropriate" x2) | -4 |
| 31 | agents/pr-outreach.md | No `model:` field in frontmatter | -5 |
| 32 | agents/pr-outreach.md | Zero `<example>` blocks | -15 |
| 33 | agents/pr-outreach.md | 1 vague quantifier ("relevant") | -2 |
| 34 | agents/competitive-intel.md | No `model:` field in frontmatter | -5 |
| 35 | agents/competitive-intel.md | Zero `<example>` blocks | -15 |
| 36 | agents/crm-manager.md | No `model:` field in frontmatter | -5 |
| 37 | agents/crm-manager.md | Zero `<example>` blocks | -15 |
| 38 | agents/memory-manager.md | No `model:` field in frontmatter | -5 |
| 39 | agents/memory-manager.md | Zero `<example>` blocks | -15 |
| 40 | agents/memory-manager.md | 1 vague quantifier ("appropriate") | -2 |
| 41 | agents/agency-operations.md | No `model:` field in frontmatter | -5 |
| 42 | agents/agency-operations.md | Zero `<example>` blocks | -15 |
| 43 | agents/localization-specialist.md | No `model:` field in frontmatter | -5 |
| 44 | agents/localization-specialist.md | Zero `<example>` blocks | -15 |
| 45 | agents/performance-monitor-agent.md | No `model:` field in frontmatter | -5 |
| 46 | agents/performance-monitor-agent.md | Zero `<example>` blocks | -15 |
| 47 | agents/performance-monitor-agent.md | 1 vague quantifier ("sufficient") | -2 |
| 48 | agents/execution-coordinator.md | No `model:` field in frontmatter | -5 |
| 49 | agents/execution-coordinator.md | Zero `<example>` blocks | -15 |
| 50 | agents/execution-coordinator.md | `Edit` declared in `tools:` but never referenced in body | -3 |
| 51 | agents/market-intelligence.md | No `model:` field in frontmatter | -5 |
| 52 | agents/market-intelligence.md | Zero `<example>` blocks | -15 |
| 53 | agents/market-intelligence.md | 1 vague quantifier ("relevant") | -2 |
| 54 | agents/seo-specialist.md | No `model:` field in frontmatter | -5 |
| 55 | agents/seo-specialist.md | Zero `<example>` blocks | -15 |
| 56 | agents/email-specialist.md | No `model:` field in frontmatter | -5 |
| 57 | agents/email-specialist.md | Zero `<example>` blocks | -15 |
| 58 | skills/send-report/SKILL.md | 3 vague quantifiers ("appropriate" x3) | -6 |
| 59 | skills/programmatic-seo/SKILL.md | 1 vague quantifier ("sufficient") | -2 |
| 60 | skills/executive-dashboard/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 61 | skills/marketing-automation/SKILL.md | 4 vague quantifiers ("reasonable", "appropriate", "correctly", "appropriate") | -8 |
| 62 | skills/import-template/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 63 | skills/analytics-insights/SKILL.md | 1 vague quantifier ("correctly") | -2 |
| 64 | skills/eval-content/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 65 | skills/prompt-test/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 66 | skills/entity-audit/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 67 | skills/pr-pitch/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 68 | skills/qbr-plan/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 69 | skills/webinar-plan/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 70 | skills/language-audit/SKILL.md | 2 vague quantifiers ("relevant", "correctly") | -4 |
| 71 | skills/client-proposal/SKILL.md | 3 vague quantifiers ("relevant" x3) | -6 |
| 72 | skills/eval-config/SKILL.md | 1 vague quantifier ("appropriate") | -2 |
| 73 | skills/lead-import/SKILL.md | 2 vague quantifiers ("relevant", "correctly") | -4 |
| 74 | skills/martech-audit/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 75 | skills/live-dashboard/SKILL.md | 2 vague quantifiers ("appropriate" x2) | -4 |
| 76 | skills/funnel-audit/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 77 | skills/add-integration/SKILL.md | 2 vague quantifiers ("appropriate" x2) | -4 |
| 78 | skills/seo-audit/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 79 | skills/journey-design/SKILL.md | 1 vague quantifier ("objective-appropriate") | -2 |
| 80 | skills/local-seo-audit/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 81 | skills/cro/SKILL.md | 1 vague quantifier ("sufficient") | -2 |
| 82 | skills/team-assign/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 83 | skills/campaign-plan/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 84 | skills/aeo-audit/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 85 | skills/campaign-orchestrator/SKILL.md | 2 vague quantifiers ("correctly", "appropriate") | -4 |
| 86 | skills/launch-campaign/SKILL.md | `Glob` declared in `allowed-tools` but never used | -3 |
| 87 | skills/launch-campaign/SKILL.md | `Grep` declared in `allowed-tools` but never used | -3 |
| 88 | skills/performance-report/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 89 | skills/pipeline-update/SKILL.md | 1 vague quantifier ("relevant") | -2 |
| 90 | skills/review-response/SKILL.md | 4 vague quantifiers ("relevant", "appropriate", "relevant", "relevant") | -8 |
| 91 | commands/email-sequence.md | Missing `allowed-tools` frontmatter field | -5 |
| 92 | commands/email-sequence.md | Multi-stage Sequence Design section (architecture, per-email blueprint, branching, deliverability checklist) presented as unordered headers/bullets, not a numbered process | -10 |
| 93 | commands/email-sequence.md | 1 vague quantifier ("appropriate") | -2 |
| 94 | commands/cowork-setup.md | Missing `allowed-tools` frontmatter field | -5 |
| 95 | commands/check.md | No empty-input handling for required `<file-or-content>` argument | -10 |
| 96 | commands/backlink-gap.md | Missing `allowed-tools` frontmatter field | -5 |
| 97 | commands/backlink-gap.md | Required domain/competitor arguments have no "if not provided" fallback (unlike sibling commands) | -10 |
| 98 | commands/competitor-analysis.md | Missing `allowed-tools` frontmatter field | -5 |
| 99 | commands/execute-action.md | No empty-input handling for required `--action <id>` flag | -10 |
| 100 | commands/brand-setup.md | Missing `allowed-tools` frontmatter field | -5 |
| 101 | commands/seo-audit.md | Missing `allowed-tools` frontmatter field | -5 |

## Cross-Component
No broken references, orphaned components, or contradictions were detected among the 100 scored artifacts — none of the four scoring passes flagged a single `broken_reference` finding (all `[[skill]]` cross-links and `scripts/*.py` references checked resolved to real files on disk).

`plugin.json`'s description claims "158 skills, 24 agents," which matches the on-disk directory listing exactly (`ls skills/ | wc -l` = 158, `ls agents/ | wc -l` = 24) — no manifest-vs-disk drift.

`hooks/hooks.json` intentionally ships zero active hooks; the prior hook set (SessionStart, PreToolUse Write/Edit, PreToolUse `mcp_.*`, SessionEnd) is preserved with rationale at `hooks/hooks-reference.example.json` rather than deleted, so no orphaned/dangling hook references exist.

The systemic pattern across all 24 scored agents is identical: every one is missing both a declared `model:` tier and any `<example>` blocks — this reads as a repo-wide authoring gap (a shared agent template that was never updated) rather than 24 independent oversights, and a single template fix would resolve ~55% of all quality-issue rows in one pass.

## Recommendation
**BLOCKED — do not submit PRs. File private security report.**

Two HIGH-severity findings (out-of-repo file writes in `scripts/output-publisher.py` and `scripts/sync_model_registry.sh`) trigger the block per policy, even though neither shows evidence of attacker control — both look like intentional product features (a "publish to my Documents folder" export, and a sibling-checkout registry sync) rather than exploits. A human security reviewer should confirm intent and either clear the block or file a private report with the maintainer before any contribution activity proceeds. The 3 NL bugs (undeclared `Bash`/`Write`/`Task` tool use in `commands/backlink-gap.md`, `commands/competitor-analysis.md`, `commands/seo-audit.md`) and the 14 Medium/Low security fixes are queued and PR-ready once the security block clears — none of them depend on resolving the two HIGH findings first.
