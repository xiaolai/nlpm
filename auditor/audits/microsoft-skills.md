# NLPM Audit: microsoft/skills
**Date**: 2026-04-06  |  **Artifacts**: 226  |  **Strategy**: progressive
**NL Score**: 94/100
**Security**: BLOCKED
**Bugs**: 3  |  **Quality Issues**: 100  |  **Security Findings**: 5

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .github/agents/presenter.agent.md | agent | 64 | Zero `<example>` blocks; 'execute'/'search' tools unused; no output-format spec |
| .github/agents/frontend.agent.md | agent | 67 | Zero `<example>` blocks; model tier not declared; no output-format spec |
| .github/agents/backend.agent.md | agent | 67 | Zero `<example>` blocks; model tier not declared; no output-format spec |
| .github/agents/infrastructure.agent.md | agent | 67 | Zero `<example>` blocks; model tier not declared; no output-format spec |
| .github/skills/skill-creator/SKILL.md | skill | 70 | Body is 1310 lines (>2.5x the skill's own 500-line rule) + heavy vague-quantifier usage |
| .github/agents/planner.agent.md | agent | 73 | Zero `<example>` blocks; declared 'web' tool never used |
| .github/plugins/deep-wiki/agents/wiki-writer.md | agent | 74 | Zero `<example>` blocks; heaviest vague-quantifier usage |
| .github/agents/scaffolder.agent.md | agent | 77 | Zero `<example>` blocks; model tier not declared |
| .github/plugins/deep-wiki/agents/wiki-researcher.md | agent | 78 | Zero `<example>` blocks; no tools declared |
| .github/plugins/deep-wiki/agents/wiki-architect.md | agent | 80 | Zero `<example>` blocks; no tools declared |
| .github/plugins/deep-wiki/commands/ask.md | command | 81 | No empty-input handling; no argument-hint |
| .github/plugins/azure-sdk-java/skills/azure-communication-callingserver-java/SKILL.md | skill | 85 | Thin/generic frontmatter description |
| .github/skills/mcp-builder/SKILL.md | skill | 85 | No inline code examples in Implementation phase; 5 vague quantifiers |
| .github/plugins/azure-sdk-python/skills/azure-cosmos-py/SKILL.md | skill | 87 | Broken reference: `scripts/setup_cosmos_container.py` does not exist |
| .github/plugins/azure-sdk-python/skills/azure-ai-projects-py/SKILL.md | skill | 88 | Broken cross-reference to nonexistent `azure-ai-agents-python` skill |
| .github/skills/copilot-sdk/SKILL.md | skill | 88 | Body is 901 lines, far over the 500-line guidance |
| .github/plugins/azure-sdk-java/skills/azure-monitor-query-java/SKILL.md | skill | 89 | Body 422 lines (400-500 band) + 3 vague quantifiers |
| .github/plugins/deep-wiki/commands/changelog.md | command | 90 | No argument-hint; no empty-git-history handling |
| .github/plugins/deep-wiki/commands/build.md | command | 90 | No argument-hint; missing-wiki precondition not actually checked |
| .github/plugins/azure-sdk-python/skills/azure-identity-py/SKILL.md | skill | 90 | Body exceeds 500 lines (533) |
| .github/plugins/azure-sdk-python/skills/azure-search-documents-py/SKILL.md | skill | 90 | Body exceeds 500 lines (543), duplicated section |
| .github/plugins/azure-sdk-java/skills/azure-monitor-ingestion-java/SKILL.md | skill | 90 | Broken cross-reference (wrong relative path to query skill) |
| .github/skills/applicationinsights-web-ts/SKILL.md | skill | 90 | Description + body both in penalized length bands |
| .github/skills/kql/SKILL.md | skill | 90 | Description + body both in penalized length bands |
| .github/skills/cloud-solution-architect/SKILL.md | skill | 93 | 44 design patterns/complex concepts with no code examples |
| .github/skills/frontend-design-review/SKILL.md | skill | 93 | Description 500-800 chars + vague quantifier |
| .github/plugins/deep-wiki/commands/generate.md | command | 95 | No argument-hint despite consuming $ARGUMENTS |
| .github/plugins/deep-wiki/commands/agents.md | command | 95 | No argument-hint despite consuming $ARGUMENTS |
| .github/plugins/deep-wiki/commands/deploy.md | command | 95 | No argument-hint despite consuming $ARGUMENTS |
| .github/plugins/azure-sdk-python/skills/azure-ai-voicelive-py/SKILL.md | skill | 95 | Description 500-800 chars |
| .github/plugins/azure-sdk-java/skills/azure-appconfiguration-java/SKILL.md | skill | 95 | Body 476 lines (400-500 band) |
| .github/skills/debugview/SKILL.md | skill | 95 | Description 500-800 chars |
| .github/skills/entra-agent-id/SKILL.md | skill | 95 | Description 500-800 chars |
| .github/plugins/azure-sdk-python/skills/azure-mgmt-fabric-py/SKILL.md | skill | 96 | 2 vague quantifiers |
| .github/skills/github-issue-creator/SKILL.md | skill | 96 | 2 vague quantifiers |
| .github/plugins/azure-sdk-python/skills/azure-cosmos-db-py/SKILL.md | skill | 97 | No scope note distinguishing from sibling azure-cosmos-py |
| .github/plugins/azure-sdk-java/skills/azure-security-keyvault-secrets-java/SKILL.md | skill | 97 | No cross-reference to sibling Key Vault Keys skill |
| .github/plugins/azure-sdk-java/skills/azure-communication-callautomation-java/SKILL.md | skill | 97 | No cross-reference to azure-communication-common-java |
| .github/plugins/azure-sdk-java/skills/azure-communication-chat-java/SKILL.md | skill | 97 | No cross-reference to azure-communication-common-java |
| .github/plugins/azure-sdk-java/skills/azure-security-keyvault-keys-java/SKILL.md | skill | 97 | No cross-reference to sibling Key Vault Secrets skill |
| .github/plugins/azure-sdk-dotnet/skills/azure-mgmt-arizeaiobservabilityeval-dotnet/SKILL.md | skill | 98 | Vague quantifier ("properly") |
| .github/plugins/azure-sdk-python/skills/azure-storage-blob-py/SKILL.md | skill | 98 | Vague quantifier ("appropriate") |
| .github/plugins/azure-sdk-python/skills/azure-monitor-opentelemetry-exporter-py/SKILL.md | skill | 98 | Vague quantifier ("appropriate") |
| .github/plugins/azure-sdk-python/skills/azure-eventgrid-py/SKILL.md | skill | 98 | Vague quantifier ("appropriate") |
| .github/plugins/azure-sdk-python/skills/azure-storage-queue-py/SKILL.md | skill | 98 | Vague quantifier ("appropriate") |
| .github/plugins/azure-sdk-python/skills/azure-monitor-ingestion-py/SKILL.md | skill | 98 | Vague quantifier ("reasonable") |
| .github/plugins/azure-sdk-python/skills/azure-eventhub-py/SKILL.md | skill | 98 | Vague quantifier ("appropriate") |
| .github/plugins/azure-sdk-python/skills/azure-mgmt-apimanagement-py/SKILL.md | skill | 98 | Vague quantifier ("appropriate") |
| .github/plugins/azure-sdk-python/skills/azure-keyvault-py/SKILL.md | skill | 98 | Vague quantifier ("appropriately") |
| .github/plugins/azure-sdk-python/skills/azure-ai-contentsafety-py/SKILL.md | skill | 98 | Vague quantifier ("appropriate") |
| .github/plugins/azure-sdk-python/skills/azure-mgmt-botservice-py/SKILL.md | skill | 98 | Vague quantifier ("proper") |
| .github/plugins/azure-sdk-python/skills/azure-speech-to-text-rest-py/SKILL.md | skill | 98 | Vague quantifier ("proper") in code comment |
| .github/plugins/azure-sdk-python/skills/azure-ai-translation-document-py/SKILL.md | skill | 98 | Vague quantifier ("appropriate") |
| .github/plugins/azure-sdk-python/skills/azure-monitor-query-py/SKILL.md | skill | 98 | Vague quantifier ("appropriate") |
| .github/plugins/azure-sdk-python/skills/azure-ai-language-conversations-py/SKILL.md | skill | 98 | Vague quantifier ("properly") |
| .github/plugins/azure-sdk-java/skills/azure-ai-voicelive-java/SKILL.md | skill | 98 | Vague quantifier ("properly") |
| .github/plugins/azure-sdk-java/skills/azure-communication-common-java/SKILL.md | skill | 98 | Vague quantifier ("appropriate") in code comment |
| .github/plugins/azure-sdk-java/skills/azure-ai-contentsafety-java/SKILL.md | skill | 98 | Vague quantifier ("appropriate") |
| .github/plugins/azure-sdk-java/skills/azure-messaging-webpubsub-java/SKILL.md | skill | 98 | Vague quantifier ("appropriate") |
| .github/plugins/azure-sdk-java/skills/azure-monitor-opentelemetry-exporter-java/SKILL.md | skill | 98 | Vague quantifier ("relevant") |
| .github/plugins/azure-sdk-java/skills/azure-ai-agents-persistent-java/SKILL.md | skill | 98 | Vague quantifier ("appropriate") |
| .github/plugins/azure-sdk-java/skills/azure-compute-batch-java/SKILL.md | skill | 98 | Vague quantifier ("properly") |
| .github/skills/microsoft-docs/SKILL.md | skill | 98 | Vague quantifier ("relevant") |
| .github/plugins/azure-sdk-dotnet/skills/azure-search-documents-dotnet/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-ai-textanalytics-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-storage-file-share-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-containerregistry-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-appconfiguration-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-ai-ml-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/fastapi-router-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-data-tables-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-monitor-opentelemetry-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-ai-translation-text-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-servicebus-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/pydantic-models-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-ai-vision-imageanalysis-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-mgmt-apicenter-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-ai-transcription-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-ai-contentunderstanding-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/m365-agents-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-messaging-webpubsubservice-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/azure-storage-file-datalake-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-python/skills/agent-framework-azure-ai-py/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-java/skills/azure-storage-blob-java/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-java/skills/azure-eventgrid-java/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-java/skills/azure-ai-projects-java/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-java/skills/azure-ai-formrecognizer-java/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-java/skills/azure-ai-vision-imageanalysis-java/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-java/skills/azure-communication-sms-java/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-java/skills/azure-eventhub-java/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-java/skills/azure-ai-anomalydetector-java/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-java/skills/azure-identity-java/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-java/skills/azure-cosmos-java/SKILL.md | skill | 100 | — |
| .github/plugins/azure-sdk-java/skills/azure-data-tables-java/SKILL.md | skill | 100 | — |
| .github/skills/continual-learning/SKILL.md | skill | 100 | — |
| .github/skills/podcast-generation/SKILL.md | skill | 100 | — |
| .github/plugins/azure-skills/hooks/hooks.json | hook | 100 | — |
| .github/plugins/azure-sdk-typescript/.claude-plugin/plugin.json | plugin.json | 100 | — |
| .github/plugins/microsoft-365-agents-toolkit/.claude-plugin/plugin.json | plugin.json | 100 | — |
| .github/plugins/microsoft-foundry/.claude-plugin/plugin.json | plugin.json | 100 | — |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 0 |
| Medium | 2 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks (`hooks/` + `.github/plugins/azure-skills/hooks/`, incl. `hooks.json`) | 2 |
| Scripts (`.sh`/`.py`/`.js` under `.github/`) | 61 |
| MCP configs (`.mcp.json`, `.vscode/mcp.json`) | 3 |
| Manifest/package files (`plugin.json`, `package.json`, `requirements.txt`) | 3 |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Critical | .github/plugins/azure-skills/skills/python-appservice-deploy/scripts/retry-az-create.sh | 36 | `eval "$VAR ..."` | `eval` executes caller-supplied `$SHOW_CMD`/`$CREATE_CMD` strings, passed in as `$1`/`$2` and documented as "single shell-quoted strings." Generic az-CLI retry wrapper by design, but any unsanitized data reaching these positional args gets full shell execution, not just an `az` invocation. |
| 2 | Medium | .github/plugins/azure-skills/skills/microsoft-foundry/models/deploy-model/capacity/scripts/discover_and_rank.sh | 104 | `python3 -c "...${VAR}..."` unescaped interpolation | `MODEL_NAME`/`MODEL_VERSION` (script args) and `CAPACITY_JSON`/`PROJECTS_JSON`/`QUOTA_JSON` (Azure API responses) are interpolated directly into an embedded Python source string executed via `python3 -c "..."` without escaping; a value containing a stray quote could break out of the string literal and inject Python code. |
| 3 | Medium | .github/plugins/azure-skills/skills/azure-quotas/scripts/check-quota.sh | 71 | `python3 -c "...${VAR}..."` unescaped interpolation | `$USAGES_JSON` (`az quota usage list` output) is interpolated directly into an embedded Python script via `json.loads('''$USAGES_JSON''')` without escaping — same injection class as finding #2, lower likelihood since the source is well-formed JSON from `az` CLI. |
| 4 | Low | .github/plugins/azure-skills/hooks/scripts/track-telemetry.sh | 360 | `npx -y @azure/mcp@latest ...` publish telemetry | On every tracked tool/skill invocation the hook shells out via `npx` to an unpinned (`@latest`) MCP package and publishes client name, session id, skill name/version, tool name, and referenced file paths to a remote telemetry endpoint. No secrets or file contents are sent, and it's opt-out via `AZURE_MCP_COLLECT_TELEMETRY=false`, but the background network call isn't disclosed anywhere else in the repo. |
| 5 | Low | .vscode/mcp.json | 13 | `npx <pkg>@latest` | Multiple MCP servers (`chrome-devtools-mcp@latest`, `@upstash/context7-mcp@latest`, `@playwright/mcp@latest`, plus `azure/.mcp.json`'s `@azure/mcp@latest`) are launched unpinned via `npx`, so each session can silently pull a newer package version — a supply-chain risk if any of those npm packages is compromised upstream. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .github/plugins/azure-sdk-python/skills/azure-cosmos-py/SKILL.md | Reference Files table links to `scripts/setup_cosmos_container.py`, but no `scripts/` directory exists in this skill folder (only `SKILL.md` and `references/`). | A reader or agent following the reference for the CLI container-setup tool finds nothing. |
| 2 | .github/plugins/azure-sdk-python/skills/azure-ai-projects-py/SKILL.md | Frontmatter description directs readers to a sibling skill "azure-ai-agents-python" for low-level agent operations, but no such skill exists anywhere in the repo (only `-dotnet`/`-java` variants of `azure-ai-agents-persistent` exist, under other language plugins). | A reader or routing agent following this pointer finds nothing and may hallucinate the skill's content. |
| 3 | .github/plugins/azure-sdk-java/skills/azure-monitor-ingestion-java/SKILL.md | "Querying Uploaded Logs" section links to `../query/SKILL.md`, which resolves to `skills/query/SKILL.md` — a directory that doesn't exist. The real directory is `skills/azure-monitor-query-java/`. | A reader following the link to find `LogsQueryClient` documentation hits a missing file. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | .github/plugins/azure-skills/skills/microsoft-foundry/models/deploy-model/capacity/scripts/discover_and_rank.sh | Unescaped shell-to-Python string interpolation of API response data into `python3 -c "..."`. | Pass `MODEL_NAME`/`MODEL_VERSION`/JSON payloads via environment variables or stdin instead of interpolating into the `-c` source string. |
| 2 | .github/plugins/azure-skills/skills/azure-quotas/scripts/check-quota.sh | Unescaped shell-to-Python string interpolation (`json.loads('''$USAGES_JSON''')`). | Pipe `$USAGES_JSON` to the Python process via stdin (`json.load(sys.stdin)`) instead of interpolating it into the source string. |
| 3 | .github/plugins/azure-skills/hooks/scripts/track-telemetry.sh | Background telemetry network call on every hook invocation isn't documented outside the script itself. | Document the telemetry call, what it sends, and the `AZURE_MCP_COLLECT_TELEMETRY=false` opt-out in the plugin's user-facing README. |
| 4 | .vscode/mcp.json | Multiple MCP servers pinned to `@latest` instead of an exact version. | Pin `chrome-devtools-mcp`, `@upstash/context7-mcp`, `@playwright/mcp` (and `@azure/mcp` in the sibling `.mcp.json` files) to exact versions to avoid unreviewed supply-chain changes landing silently. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .github/plugins/deep-wiki/agents/wiki-researcher.md | [R09] Description has zero `<example>` blocks. | -15 |
| 2 | .github/plugins/deep-wiki/agents/wiki-researcher.md | [R11] No tools/allowed-tools field in frontmatter (only name/description/model present). | -5 |
| 3 | .github/plugins/deep-wiki/agents/wiki-researcher.md | [vague-quantifier] 1 hit: 'relevant files' (line 38). | -2 |
| 4 | .github/plugins/deep-wiki/agents/wiki-architect.md | [R09] Description has zero `<example>` blocks. | -15 |
| 5 | .github/plugins/deep-wiki/agents/wiki-architect.md | [R11] No tools/allowed-tools field in frontmatter (only name/description/model present). | -5 |
| 6 | .github/plugins/deep-wiki/agents/wiki-writer.md | [R09] Description has zero `<example>` blocks. | -15 |
| 7 | .github/plugins/deep-wiki/agents/wiki-writer.md | [R11] No tools/allowed-tools field in frontmatter (only name/description/model present). | -5 |
| 8 | .github/plugins/deep-wiki/agents/wiki-writer.md | [vague-quantifier] 3 hits: 'relevant file' (line38), 'relevant files' (line47), 'as appropriate' (line54). | -6 |
| 9 | .github/agents/frontend.agent.md | [R09] No `<example>` blocks anywhere in the file. | -15 |
| 10 | .github/agents/frontend.agent.md | [R10] Frontmatter has name/description/tools only; no model field. | -5 |
| 11 | .github/agents/frontend.agent.md | [R11] Declared 'search' tool has no corresponding search-related instruction anywhere in the body. | -3 |
| 12 | .github/agents/frontend.agent.md | [R12] No section defines the format of the agent's own output/response; body is patterns/rules/file-location tables only. | -10 |
| 13 | .github/agents/planner.agent.md | [R09] No `<example>` blocks anywhere in the file. | -15 |
| 14 | .github/agents/planner.agent.md | [R10] Frontmatter has name/description/tools/handoffs only; no model field. | -5 |
| 15 | .github/agents/planner.agent.md | [R11] Declared 'web' tool but body never references external web content, URLs, or internet search — all references are to local files (PRD.md, source tree). | -3 |
| 16 | .github/agents/planner.agent.md | [vague-quantifier] 2 hits: 'relevant files' (line30), 'appropriate specialist agent' (line89). | -4 |
| 17 | .github/agents/presenter.agent.md | [R09] No `<example>` blocks anywhere in the file. | -15 |
| 18 | .github/agents/presenter.agent.md | [R10] Frontmatter has name/description/tools only; no model field. | -5 |
| 19 | .github/agents/presenter.agent.md | [R11] Declared 'execute' tool but file contains no Commands/bash section at all, unlike sibling agents (frontend/backend/scaffolder/infrastructure). | -3 |
| 20 | .github/agents/presenter.agent.md | [R11] Declared 'search' tool has no corresponding search-related instruction in the body. | -3 |
| 21 | .github/agents/presenter.agent.md | [R12] No section defines the format of the agent's own output/response. | -10 |
| 22 | .github/agents/backend.agent.md | [R09] No `<example>` blocks anywhere in the file. | -15 |
| 23 | .github/agents/backend.agent.md | [R10] Frontmatter has name/description/tools only; no model field. | -5 |
| 24 | .github/agents/backend.agent.md | [R11] Declared 'search' tool has no corresponding search-related instruction anywhere in the body. | -3 |
| 25 | .github/agents/backend.agent.md | [R12] No section defines the format of the agent's own output/response; body is patterns/router examples/file tables only. | -10 |
| 26 | .github/agents/scaffolder.agent.md | [R09] No `<example>` blocks anywhere in the file. | -15 |
| 27 | .github/agents/scaffolder.agent.md | [R10] Frontmatter has name/description/tools only; no model field. | -5 |
| 28 | .github/agents/scaffolder.agent.md | [R11] Declared 'search' tool has no corresponding search-related instruction anywhere in the body. | -3 |
| 29 | .github/agents/infrastructure.agent.md | [R09] No `<example>` blocks anywhere in the file. | -15 |
| 30 | .github/agents/infrastructure.agent.md | [R10] Frontmatter has name/description/tools only; no model field. | -5 |
| 31 | .github/agents/infrastructure.agent.md | [R11] Declared 'search' tool has no corresponding search-related instruction anywhere in the body. | -3 |
| 32 | .github/agents/infrastructure.agent.md | [R12] No section defines the format of the agent's own output/response; body is deployment workflows/tables only. | -10 |
| 33 | .github/plugins/deep-wiki/commands/generate.md | [R18] Frontmatter has only a description field; no argument-hint despite body appending $ARGUMENTS. | -5 |
| 34 | .github/plugins/deep-wiki/commands/agents.md | [R18] Frontmatter has only a description field; no argument-hint despite body appending $ARGUMENTS. | -5 |
| 35 | .github/plugins/deep-wiki/commands/changelog.md | [R18] Frontmatter has only a description field; no argument-hint despite body appending $ARGUMENTS. | -5 |
| 36 | .github/plugins/deep-wiki/commands/changelog.md | [R17] No instruction for the edge case of an empty/shallow git history — process assumes commits exist. | -5 |
| 37 | .github/plugins/deep-wiki/commands/deploy.md | [R18] Frontmatter has only a description field; no argument-hint despite body appending $ARGUMENTS. | -5 |
| 38 | .github/plugins/deep-wiki/commands/build.md | [R18] Frontmatter has only a description field; no argument-hint despite body appending $ARGUMENTS. | -5 |
| 39 | .github/plugins/deep-wiki/commands/build.md | [R17] Prerequisites section only states wiki markdown "should already exist" with no actual check-and-respond instruction, unlike sibling deploy.md. | -5 |
| 40 | .github/plugins/deep-wiki/commands/ask.md | [R15] Command's entire purpose is answering "$ARGUMENTS" as a question, but there is no instruction for an empty/missing question. | -10 |
| 41 | .github/plugins/deep-wiki/commands/ask.md | [R18] Frontmatter has only a description field; no argument-hint despite the command being fully argument-driven. | -5 |
| 42 | .github/plugins/deep-wiki/commands/ask.md | [vague-quantifier] 2 hits: 'relevant to the question' (line27), '[Relevant snippet...]' (line48). | -4 |
| 43 | .github/plugins/azure-sdk-dotnet/skills/azure-mgmt-arizeaiobservabilityeval-dotnet/SKILL.md | [vague-quantifier] "Close clients properly" (line 201). | -2 |
| 44 | .github/plugins/azure-sdk-python/skills/azure-identity-py/SKILL.md | [R05] Body is ~533 lines (frontmatter closes at line 11 of 544 total), exceeding the 500-line threshold. | -10 |
| 45 | .github/plugins/azure-sdk-python/skills/azure-storage-blob-py/SKILL.md | [vague-quantifier] "Set appropriate content types for web-served blobs" (line 257). | -2 |
| 46 | .github/plugins/azure-sdk-python/skills/azure-monitor-opentelemetry-exporter-py/SKILL.md | [vague-quantifier] "Set export intervals appropriate for your workload" (line 238). | -2 |
| 47 | .github/plugins/azure-sdk-python/skills/azure-eventgrid-py/SKILL.md | [vague-quantifier] "Set appropriate event types for routing and filtering" (line 195). | -2 |
| 48 | .github/plugins/azure-sdk-python/skills/azure-storage-queue-py/SKILL.md | [vague-quantifier] "Set appropriate visibility timeout based on processing time" (line 234). | -2 |
| 49 | .github/plugins/azure-sdk-python/skills/azure-ai-voicelive-py/SKILL.md | [R04] Description is ~517 characters, in the 500-800 char penalty band. | -5 |
| 50 | .github/plugins/azure-sdk-python/skills/azure-monitor-ingestion-py/SKILL.md | [vague-quantifier] "SDK handles batching, but send reasonable chunks" (line 229). | -2 |
| 51 | .github/plugins/azure-sdk-python/skills/azure-eventhub-py/SKILL.md | [vague-quantifier] "Set appropriate consumer groups for different applications" (line 252). | -2 |
| 52 | .github/plugins/azure-sdk-python/skills/azure-search-documents-py/SKILL.md | [R05] Body ~543 lines (554 total), exceeding 500-line threshold; caused largely by a duplicated "Additional Azure AI Search Patterns" section repeating earlier content near-verbatim. | -10 |
| 53 | .github/plugins/azure-sdk-python/skills/azure-cosmos-py/SKILL.md | [R07] No scope note distinguishing this skill from sibling azure-cosmos-db-py, which covers the same azure-cosmos package with overlapping trigger phrases. | -3 |
| 54 | .github/plugins/azure-sdk-python/skills/azure-mgmt-apimanagement-py/SKILL.md | [vague-quantifier] "appropriate scopes" without specifying which scopes for which scenario. | -2 |
| 55 | .github/plugins/azure-sdk-python/skills/azure-keyvault-py/SKILL.md | [vague-quantifier] "Cache secrets appropriately" without concrete guidance on TTL or strategy. | -2 |
| 56 | .github/plugins/azure-sdk-python/skills/azure-ai-contentsafety-py/SKILL.md | [vague-quantifier] "severity thresholds appropriate for your use case" without concrete guidance. | -2 |
| 57 | .github/plugins/azure-sdk-python/skills/azure-mgmt-botservice-py/SKILL.md | [vague-quantifier] "Configure proper CORS" without specifying the actual policy. | -2 |
| 58 | .github/plugins/azure-sdk-python/skills/azure-speech-to-text-rest-py/SKILL.md | [vague-quantifier] Code-comment docstring "Transcribe with proper error handling". | -2 |
| 59 | .github/plugins/azure-sdk-python/skills/azure-ai-translation-document-py/SKILL.md | [vague-quantifier] "SAS tokens with appropriate permissions" without full specification. | -2 |
| 60 | .github/plugins/azure-sdk-python/skills/azure-monitor-query-py/SKILL.md | [vague-quantifier] "appropriate granularity" without concrete guidance. | -2 |
| 61 | .github/plugins/azure-sdk-python/skills/azure-ai-language-conversations-py/SKILL.md | [vague-quantifier] "Handle exceptions properly" without specifying which exceptions or how. | -2 |
| 62 | .github/plugins/azure-sdk-python/skills/azure-mgmt-fabric-py/SKILL.md | [vague-quantifier] "scale up as needed" without concrete triggers. | -2 |
| 63 | .github/plugins/azure-sdk-python/skills/azure-mgmt-fabric-py/SKILL.md | [vague-quantifier] "Handle LRO properly" without specifying the actual handling steps. | -2 |
| 64 | .github/plugins/azure-sdk-python/skills/azure-ai-projects-py/SKILL.md | [vague-quantifier] Code sample comment "Add tools as needed". | -2 |
| 65 | .github/plugins/azure-sdk-python/skills/azure-cosmos-db-py/SKILL.md | [R07] No cross-reference/scope note distinguishing this skill from sibling azure-cosmos-py, which covers the same package with overlapping trigger phrases. | -3 |
| 66 | .github/plugins/azure-sdk-java/skills/azure-ai-voicelive-java/SKILL.md | [vague-quantifier] "Close sessions properly when conversation ends" (line 221). | -2 |
| 67 | .github/plugins/azure-sdk-java/skills/azure-communication-common-java/SKILL.md | [vague-quantifier] "// Parse raw ID to appropriate type" (line 173), a code comment. | -2 |
| 68 | .github/plugins/azure-sdk-java/skills/azure-security-keyvault-secrets-java/SKILL.md | [R07] No mention/link to sibling azure-security-keyvault-keys-java skill despite both operating on the same vault. | -3 |
| 69 | .github/plugins/azure-sdk-java/skills/azure-ai-contentsafety-java/SKILL.md | [vague-quantifier] "Cache blocklist results where appropriate" (line 287). | -2 |
| 70 | .github/plugins/azure-sdk-java/skills/azure-monitor-query-java/SKILL.md | [R05] Body ~422 lines (13-434 of file), in the 400-500 line penalty band. | -5 |
| 71 | .github/plugins/azure-sdk-java/skills/azure-monitor-query-java/SKILL.md | [vague-quantifier] "TokenCredential with appropriate permissions" (line 61) does not name required permissions. | -2 |
| 72 | .github/plugins/azure-sdk-java/skills/azure-monitor-query-java/SKILL.md | [vague-quantifier] "Set appropriate timeouts" (line 417) is vague about actual timeout values. | -2 |
| 73 | .github/plugins/azure-sdk-java/skills/azure-monitor-query-java/SKILL.md | [vague-quantifier] "Cache results ... cache when appropriate" (line 421) does not specify caching criteria. | -2 |
| 74 | .github/plugins/azure-sdk-java/skills/azure-communication-callingserver-java/SKILL.md | [R04] Frontmatter description gives only one concrete trigger condition ("maintaining legacy code") rather than a list of specific invocation phrases like sibling skills use. | -15 |
| 75 | .github/plugins/azure-sdk-java/skills/azure-communication-callautomation-java/SKILL.md | [R07] Code examples import CommunicationUserIdentifier/PhoneNumberIdentifier from com.azure.communication.common (lines 69-70) but the skill never links azure-communication-common-java. | -3 |
| 76 | .github/plugins/azure-sdk-java/skills/azure-messaging-webpubsub-java/SKILL.md | [vague-quantifier] "Set appropriate token expiration for security" (line 306) does not specify a recommended value/range. | -2 |
| 77 | .github/plugins/azure-sdk-java/skills/azure-communication-chat-java/SKILL.md | [R07] Client Creation section uses CommunicationTokenCredential (lines 31, 37), documented in azure-communication-common-java, which is never referenced. | -3 |
| 78 | .github/plugins/azure-sdk-java/skills/azure-appconfiguration-java/SKILL.md | [R05] Body ~476 lines (12-487 of file), in the 400-500 line penalty band. | -5 |
| 79 | .github/plugins/azure-sdk-java/skills/azure-security-keyvault-keys-java/SKILL.md | [R07] No mention/link to sibling azure-security-keyvault-secrets-java skill despite both operating on the same vault. | -3 |
| 80 | .github/plugins/azure-sdk-java/skills/azure-monitor-opentelemetry-exporter-java/SKILL.md | [vague-quantifier] "Add relevant attributes — Include contextual data for debugging" (line 273) does not specify which attributes are relevant. | -2 |
| 81 | .github/plugins/azure-sdk-java/skills/azure-ai-agents-persistent-java/SKILL.md | [vague-quantifier] "Poll with appropriate delays" (line 130) pairs a vague qualifier with a concrete number in the same sentence; the heading itself remains vague. | -2 |
| 82 | .github/plugins/azure-sdk-java/skills/azure-compute-batch-java/SKILL.md | [vague-quantifier] "Handle LRO properly — Pool resize, delete operations are long-running" (line 380). | -2 |
| 83 | .github/skills/debugview/SKILL.md | [R04] Frontmatter description is roughly 775 characters (500-800 range). | -5 |
| 84 | .github/skills/cloud-solution-architect/SKILL.md | [R06] Complex architectural concepts (44 patterns, WAF pillars, mission-critical design) are covered entirely with reference tables; the only code-shaped block is a generic ADR template, not an implementation example. | -5 |
| 85 | .github/skills/cloud-solution-architect/SKILL.md | [vague-quantifier] 1 occurrence ('relevant'). | -2 |
| 86 | .github/skills/skill-creator/SKILL.md | [R05] Body is ~1310 lines, well over the 500-line threshold (and over the skill's own '<500 lines' rule it prescribes for other skills). | -10 |
| 87 | .github/skills/skill-creator/SKILL.md | [vague-quantifier] 15 occurrences found (appropriate x5, as needed x2, several, significantly, sufficient, typically, etc.); capped at -20. | -20 |
| 88 | .github/skills/applicationinsights-web-ts/SKILL.md | [R04] Frontmatter description is roughly 524 characters (500-800 range). | -5 |
| 89 | .github/skills/applicationinsights-web-ts/SKILL.md | [R05] SKILL.md body is 457 lines (400-500 range). | -5 |
| 90 | .github/skills/kql/SKILL.md | [R04] Frontmatter description is roughly 797 characters (500-800 range, just under the -10 threshold). | -5 |
| 91 | .github/skills/kql/SKILL.md | [R05] SKILL.md body is 439 lines (400-500 range). | -5 |
| 92 | .github/skills/copilot-sdk/SKILL.md | [R05] SKILL.md body is ~901 lines, well over the 500-line threshold. | -10 |
| 93 | .github/skills/copilot-sdk/SKILL.md | [vague-quantifier] 1 occurrence ('effectively'). | -2 |
| 94 | .github/skills/mcp-builder/SKILL.md | [R06] Core "Implement Tools" section is described narratively with zero inline code snippets; every concrete example lives in a separate ./reference/*.md file. | -5 |
| 95 | .github/skills/mcp-builder/SKILL.md | [vague-quantifier] 5 occurrences (relevant x2, as needed x2, effectively). | -10 |
| 96 | .github/skills/entra-agent-id/SKILL.md | [R04] Frontmatter description is roughly 715 characters (500-800 range). | -5 |
| 97 | .github/skills/microsoft-docs/SKILL.md | [vague-quantifier] 1 occurrence ('relevant'). | -2 |
| 98 | .github/skills/frontend-design-review/SKILL.md | [R04] Frontmatter description is roughly 595 characters (500-800 range). | -5 |
| 99 | .github/skills/frontend-design-review/SKILL.md | [vague-quantifier] 1 occurrence ('context-appropriate'). | -2 |
| 100 | .github/skills/github-issue-creator/SKILL.md | [vague-quantifier] 2 occurrences ('relevant' x2). | -4 |

## Cross-Component

- **Broken references** (also listed under Bugs): `azure-cosmos-py/SKILL.md` links to a nonexistent `scripts/setup_cosmos_container.py`; `azure-ai-projects-py/SKILL.md` points readers to a nonexistent `azure-ai-agents-python` skill; `azure-monitor-ingestion-java/SKILL.md` links to `../query/SKILL.md` instead of the real `../azure-monitor-query-java/SKILL.md`.
- **Orphaned/overlapping sibling skills**: `azure-cosmos-py` and `azure-cosmos-db-py` both cover the `azure-cosmos` Python package with overlapping trigger phrases ("Cosmos DB", "NoSQL") and no scope note disambiguating them — a routing agent cannot deterministically pick one.
- **Missing cross-links between logically related Java skills**: `azure-security-keyvault-secrets-java` and `azure-security-keyvault-keys-java` operate on the same vault but never reference each other; `azure-communication-callautomation-java` and `azure-communication-chat-java` both import identifier/credential types documented in `azure-communication-common-java` without linking to it.
- **No manifest/disk contradictions found**: the three `plugin.json` manifests checked (`azure-sdk-typescript`, `microsoft-365-agents-toolkit`, `microsoft-foundry`) all point to paths that exist on disk, and `azure-skills/hooks/hooks.json`'s two referenced scripts (`track-telemetry.sh`/`.ps1`) are both present.
- **Systemic template gap across agent families**: all 9 agents audited (`.github/agents/*.agent.md` and `.github/plugins/deep-wiki/agents/*.md`) independently omit `<example>` blocks, and the 6 `.agent.md` files additionally omit a declared `model` tier — the uniformity across two otherwise-unrelated agent families suggests a shared authoring template gap rather than 9 independent oversights.

## Recommendation
- **BLOCKED — do not submit PRs. File private security report.** A Critical-severity finding (`eval` on caller-supplied command strings in `retry-az-create.sh`) requires private disclosure before any public PR activity against this repo. Hold the 3 NL bug fixes and the 4 Medium/Low security fixes above until the security disclosure is filed and acknowledged; do not open public PRs referencing any of the findings in this report in the meantime.
