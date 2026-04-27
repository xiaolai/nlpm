# NLPM Audit: 0xfurai/claude-code-subagents
**Date**: 2026-04-27  |  **Artifacts**: 100  |  **Strategy**: progressive
**NL Score**: 74/100
**Security**: CLEAR
**Bugs**: 1  |  **Quality Issues**: 5  |  **Security Findings**: 0

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/sqs-expert.md | agent | 10 | Entire file indented 4 spaces — `---` not at line 1; frontmatter unparseable; name/model/description lost |
| agents/prisma-expert.md | agent | 67 | 9 vague quantifiers (appropriate×2, comprehensive×3, efficient×3, clear×2); no examples |
| agents/clojure-expert.md | agent | 71 | 7 vague quantifiers (appropriate, efficient, comprehensive×2, robust, effective, clear); no examples |
| agents/erlang-expert.md | agent | 71 | 7 vague quantifiers (efficient, robust, appropriate, comprehensive×2, clear, effective); no examples |
| agents/flask-expert.md | agent | 71 | 7 vague quantifiers (effective×2, efficient, comprehensive×2, robust, relevant); no examples |
| agents/html-expert.md | agent | 71 | 7 vague quantifiers (proper×3, appropriate×2, necessary, meaningful); no examples |
| agents/rabbitmq-expert.md | agent | 71 | 7 vague quantifiers (appropriate, optimal, effective×2, robust, adequate, comprehensive); no examples |
| agents/sidekiq-expert.md | agent | 71 | 7 vague quantifiers (optimal, robust×2, effective×2, properly, effectively×2); no examples |
| agents/spring-boot-expert.md | agent | 71 | 7 vague quantifiers (appropriate, efficient, comprehensive×2, robust, properly, comprehensive); no examples |
| agents/angular-expert.md | agent | 73 | 6 vague quantifiers (appropriate, efficient, comprehensive×2, robust, effective); no examples |
| agents/aspnet-core-expert.md | agent | 73 | 6 vague quantifiers (appropriate, efficient, comprehensive×2, robust, consistent); no examples |
| agents/cassandra-expert.md | agent | 73 | 6 vague quantifiers (appropriate×2, efficient, comprehensive, proper, consistent); no examples |
| agents/cpp-expert.md | agent | 73 | 6 vague quantifiers (effective, appropriate, comprehensive, thorough, proper); no examples |
| agents/docker-expert.md | agent | 73 | 6 vague quantifiers (appropriate×2, efficient, comprehensive, robust, proper); no examples |
| agents/electron-expert.md | agent | 73 | 6 vague quantifiers (appropriate, comprehensive×2, efficient×2, consistent); no examples |
| agents/elk-expert.md | agent | 73 | 6 vague quantifiers (appropriate×2, efficient, comprehensive×2, robust); no examples |
| agents/grafana-expert.md | agent | 73 | 6 vague quantifiers (appropriate, efficient, comprehensive, effective×2, relevant); no examples |
| agents/ios-expert.md | agent | 73 | 6 vague quantifiers (appropriate, efficient, comprehensive×2, robust, consistent); no examples |
| agents/kafka-expert.md | agent | 73 | 6 vague quantifiers (optimal, appropriate, efficient, comprehensive, robust, effective); no examples |
| agents/langchain-expert.md | agent | 73 | 6 vague quantifiers (appropriate, efficient, comprehensive×2, robust, clear); no examples |
| agents/loki-expert.md | agent | 73 | 6 vague quantifiers (appropriate, efficient, comprehensive×2, robust, effective); no examples |
| agents/lua-expert.md | agent | 73 | 6 vague quantifiers (appropriate×2, efficient, comprehensive, robust, consistent); no examples |
| agents/nestjs-expert.md | agent | 73 | 6 vague quantifiers (appropriate×2, comprehensive, robust, efficient, consistent); no examples |
| agents/openai-api-expert.md | agent | 73 | 6 vague quantifiers (appropriate, efficient, comprehensive×2, robust, adequate); no examples |
| agents/perl-expert.md | agent | 73 | 6 vague quantifiers (appropriate, efficient, comprehensive, robust, effective, proper); no examples |
| agents/phoenix-expert.md | agent | 73 | 6 vague quantifiers (appropriate, efficient, comprehensive×2, robust, effective); no examples |
| agents/scala-expert.md | agent | 73 | 6 vague quantifiers (appropriate, efficient, comprehensive×2, effective, clear); no examples |
| agents/typeorm-expert.md | agent | 73 | 6 vague quantifiers (appropriate×2, optimal, comprehensive, efficient, robust); no examples |
| agents/vector-db-expert.md | agent | 73 | 6 vague quantifiers (appropriate, efficient×2, comprehensive×2, accurate); no examples |
| agents/vitest-expert.md | agent | 73 | 6 vague quantifiers (meaningful, efficient, comprehensive, adequate, appropriate); no examples |
| agents/android-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient×2, comprehensive, robust); no examples |
| agents/ava-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive×2, consistent); no examples |
| agents/bash-expert.md | agent | 75 | 5 vague quantifiers (robust, comprehensive×2, proper, adequate); no examples |
| agents/braintree-expert.md | agent | 75 | 5 vague quantifiers (appropriate, comprehensive×2, robust, efficient); no examples |
| agents/bun-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient×2, comprehensive, robust); no examples |
| agents/celery-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive, robust, optimal); no examples |
| agents/cockroachdb-expert.md | agent | 75 | 5 vague quantifiers (appropriate×2, efficient, comprehensive×2); no examples |
| agents/cypress-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive×2, robust); no examples |
| agents/dart-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive, robust, consistent); no examples |
| agents/deno-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive, robust, consistent); no examples |
| agents/django-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive×2, robust); no examples |
| agents/dynamodb-expert.md | agent | 75 | 5 vague quantifiers (appropriate×2, efficient×2, comprehensive); no examples |
| agents/fastapi-expert.md | agent | 75 | 5 vague quantifiers (appropriate, comprehensive×2, robust, thorough); no examples |
| agents/fastify-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient×2, comprehensive, robust); no examples |
| agents/flutter-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive, consistent, thorough); no examples |
| agents/gin-expert.md | agent | 75 | 4 vague words; description uses meta-phrasing ("Create a Claude Code Agent that is…"); no examples |
| agents/github-actions-expert.md | agent | 75 | 5 vague quantifiers (appropriate×2, comprehensive, efficient, sufficient); no examples |
| agents/graphql-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive×2, robust); no examples |
| agents/jest-expert.md | agent | 75 | 5 vague quantifiers (appropriate×2, comprehensive, efficient, consistent); no examples |
| agents/jquery-expert.md | agent | 75 | 5 vague quantifiers (appropriate×2, necessary, efficient, comprehensive); no examples |
| agents/jwt-expert.md | agent | 75 | 5 vague quantifiers (appropriate, comprehensive, robust, necessary, effective); no examples |
| agents/knex-expert.md | agent | 75 | 5 vague quantifiers (appropriate, robust, efficient, comprehensive, consistent); no examples |
| agents/liquibase-expert.md | agent | 75 | 5 vague quantifiers (appropriate, comprehensive×2, robust, clear); no examples |
| agents/mariadb-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive, robust, thorough); no examples |
| agents/mocha-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive×2, clear); no examples |
| agents/mongoose-expert.md | agent | 75 | 5 vague quantifiers (efficient, appropriate, comprehensive, robust, relevant); no examples |
| agents/mqtt-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive×2, robust); no examples |
| agents/mssql-expert.md | agent | 75 | 5 vague quantifiers (appropriate×2, efficient, comprehensive, robust); no examples |
| agents/numpy-expert.md | agent | 75 | 5 vague quantifiers (effective, efficient×2, comprehensive, appropriate); no examples |
| agents/opentelemetry-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient×2, comprehensive, consistent); no examples |
| agents/opensearch-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive×2, robust); no examples |
| agents/php-expert.md | agent | 75 | 5 vague quantifiers (thorough, comprehensive, efficient, appropriate, responsive); no examples |
| agents/prometheus-expert.md | agent | 75 | 5 vague quantifiers (appropriate×2, efficient, comprehensive, robust); no examples |
| agents/pulumi-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, robust, reliable, comprehensive); no examples |
| agents/puppeteer-expert.md | agent | 75 | 5 vague quantifiers (robust, appropriate, relevant, appropriate, consistent); no examples |
| agents/rails-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive×2, thorough); no examples |
| agents/react-native-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive, robust, seamless); no examples |
| agents/ruby-expert.md | agent | 75 | 5 vague quantifiers (efficient, appropriate, thorough, effective, meaningful); no examples |
| agents/solidjs-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive, consistent, relevant); no examples |
| agents/sql-expert.md | agent | 75 | 5 vague quantifiers (appropriate×2, efficient×2, comprehensive); no examples |
| agents/sqlite-expert.md | agent | 75 | 5 vague quantifiers (appropriate×2, efficient, comprehensive, robust); no examples |
| agents/svelte-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive, robust, effective); no examples |
| agents/tensorflow-expert.md | agent | 75 | 5 vague quantifiers (appropriate, efficient, comprehensive, robust, clear); no examples |
| agents/websocket-expert.md | agent | 75 | 5 vague quantifiers (appropriate×2, efficient, comprehensive, robust); no examples |
| agents/actix-expert.md | agent | 77 | 4 vague quantifiers (appropriate, comprehensive, robust, clear); no examples |
| agents/auth0-expert.md | agent | 77 | 4 vague quantifiers (appropriate×2, comprehensive, robust); no examples |
| agents/expo-expert.md | agent | 77 | 4 vague quantifiers (efficient, comprehensive×2, thorough); no examples |
| agents/express-expert.md | agent | 77 | 4 vague quantifiers (appropriate, efficient, comprehensive, robust); no examples |
| agents/gitlab-ci-expert.md | agent | 77 | 4 vague quantifiers (appropriate×2, efficient, comprehensive); no examples |
| agents/go-expert.md | agent | 77 | 4 vague quantifiers (appropriate, efficient, comprehensive, consistent); no examples |
| agents/javascript-expert.md | agent | 77 | 4 vague quantifiers (appropriate×2, comprehensive, efficient); no examples |
| agents/jenkins-expert.md | agent | 77 | 4 vague quantifiers (appropriate×2, comprehensive, efficient); no examples |
| agents/nextjs-expert.md | agent | 77 | 4 vague quantifiers (optimal, comprehensive, appropriate, effective); no examples |
| agents/ocaml-expert.md | agent | 77 | 4 vague quantifiers (appropriate, efficient, comprehensive, robust); no examples |
| agents/oauth-oidc-expert.md | agent | 77 | 4 vague quantifiers (appropriate, robust, comprehensive×2); no examples |
| agents/pandas-expert.md | agent | 77 | 4 vague quantifiers (appropriate, efficient×2, comprehensive); no examples |
| agents/pytorch-expert.md | agent | 77 | 4 vague quantifiers (appropriate, efficient, comprehensive×2); no examples |
| agents/react-expert.md | agent | 77 | 4 vague quantifiers (appropriate×2, optimal, comprehensive); no examples |
| agents/scikit-learn-expert.md | agent | 77 | 4 vague quantifiers (appropriate×2, clear, comprehensive); no examples |
| agents/selenium-expert.md | agent | 77 | 4 vague quantifiers (robust, appropriate, reliable, comprehensive); no examples |
| agents/swiftui-expert.md | agent | 77 | 4 vague quantifiers (appropriate, effective, comprehensive, efficient); no examples |
| agents/tauri-expert.md | agent | 77 | 4 vague quantifiers (appropriate, comprehensive, efficient, robust); no examples |
| agents/terraform-expert.md | agent | 77 | 4 vague quantifiers (appropriate, efficient, comprehensive, consistent); no examples |
| agents/testcafe-expert.md | agent | 77 | 4 vague quantifiers (appropriate, efficient, comprehensive×2); no examples |
| agents/typescript-expert.md | agent | 77 | 4 vague quantifiers (appropriate, comprehensive, clear, consistent); no examples |
| agents/vue-expert.md | agent | 77 | 4 vague quantifiers (efficient, appropriate, consistent, comprehensive); no examples |
| agents/jasmine-expert.md | agent | 79 | 3 vague quantifiers (appropriate×2, comprehensive); blank lines between frontmatter fields (non-standard) |
| agents/owasp-top10-expert.md | agent | 79 | 3 vague quantifiers (appropriate, strict, comprehensive×2); no examples |
| agents/rollup-expert.md | agent | 79 | 3 vague quantifiers (appropriate, efficient, comprehensive); no examples |
| agents/rust-expert.md | agent | 79 | 3 vague quantifiers (comprehensive, meaningful, minimize); no examples |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts | 0 |
| MCP configs | 0 |
| Package manifests | 0 |

The repository contains only `LICENSE`, `README.md`, and the `agents/` directory. No executable surfaces exist.

### Security Findings
No security findings.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | agents/sqs-expert.md | Entire file is indented with 4 leading spaces; the YAML front-matter delimiter `---` never appears at column 0, so the frontmatter block is not parsed. The agent's `name`, `description`, and `model` fields are all invisible to the registration system. | Agent will not be registered or invoked by Claude Code; all three required frontmatter fields are effectively missing. |

## Security Fixes (PR-worthy, Medium/Low only)
No security fixes required.

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | all 100 agents | **Missing examples** — no `## Examples` (or equivalent) section in any file. Agents provide no worked demonstrations of their behaviour, making it impossible to verify correct invocation. | -15 per file (systematic; caps the floor of every score in this repo at 85 before further deductions) |
| 2 | all 100 agents | **Pervasive vague quantifiers** — every file uses 3–9 instances of "appropriate", "relevant", "comprehensive", "robust", "efficient", "effective", "proper", "thorough", "optimal", "adequate", or "necessary" without measurable criteria. Worst offender: `prisma-expert.md` (9 instances, -18 pts). | -8 to -20 per file depending on density |
| 3 | agents/gin-expert.md | **Meta-phrasing in description** — description reads "Create a Claude Code Agent that is an expert in the Gin web framework…" instead of describing the agent's purpose directly. Claude Code surfaces this description in the UI; meta-phrasing causes confusion. | -2 (description quality) |
| 4 | agents/jasmine-expert.md | **Non-standard frontmatter formatting** — blank lines between each frontmatter key-value pair. Valid per the YAML spec but violates the de-facto convention for Claude Code agent files and may trip strict parsers. | -2 (style) |
| 5 | agents/sqs-expert.md | **Excessive vague language** — beyond the frontmatter bug, the body content also contains 6+ vague quantifiers (appropriate, efficient, comprehensive, etc.) that would lower quality even if the bug were fixed. | -12 (vague language, in addition to frontmatter bug penalties) |

## Cross-Component
All 100 agents follow an identical four-section template (Focus Areas / Approach / Quality Checklist / Output) and use the same model pin (`claude-sonnet-4-20250514`). No cross-agent references exist, so there are no broken relative paths, stale counts, or terminology drift issues to flag. The homogeneous template is a strength for consistency but also the root cause of the systematic quality issues: the template never requires examples, and the boilerplate language introduces vague quantifiers by default.

## Recommendation
CLEAR — submit PRs for the one confirmed bug and consider opening a single "quality sweep" issue for the systematic missing-examples pattern.

**Immediate PR target**: Fix `agents/sqs-expert.md` — remove the 4-space indent from the entire file so the frontmatter `---` delimiters appear at column 0.

**Follow-up quality PR**: Add at least one `## Examples` block per agent, demonstrating a concrete invocation scenario. Replacing vague terms with measurable criteria (e.g., "tests achieve ≥80% branch coverage" instead of "comprehensive test coverage") would lift the repo-wide average from 74 to approximately 85+.
