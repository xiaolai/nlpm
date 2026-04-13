# NLPM Audit: davepoon/buildwithclaude
**Date**: 2026-04-13  |  **Artifacts**: 881  |  **Strategy**: progressive
**NL Score**: 77/100
**Security**: BLOCKED
**Bugs**: 8  |  **Quality Issues**: 163  |  **Security Findings**: 3

## NL Score Summary

> Agents from `all-agents/` and `agents-quality-security/` are high-quality canonical versions (95–100). Specialized plugin directories contain older, lower-quality copies of the same agents (70–90). Commands universally lack a `name` frontmatter field (−25 each), dragging the command average to ~65. Skills average ~75.

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| plugins/agents-uc-taskmanager/agents/scheduler.md | agent | 55 | Missing name + description frontmatter |
| plugins/agents-uc-taskmanager/agents/specifier.md | agent | 55 | Missing name + description frontmatter |
| plugins/agents-uc-taskmanager/agents/planner.md | agent | 55 | Missing name + description frontmatter |
| plugins/agents-uc-taskmanager/agents/builder.md | agent | 55 | Missing name + description frontmatter |
| plugins/all-commands/commands/fix-issue.md | command | 40 | 3-word body; missing name, no structure, no output format |
| plugins/all-commands/commands/fix-pr.md | command | 40 | 1-line body; missing name, no structure, no output format |
| plugins/commands-version-control-git/commands/fix-issue.md | command | 40 | Same as all-commands mirror; missing name, trivial content |
| plugins/commands-version-control-git/commands/fix-pr.md | command | 40 | Same as all-commands mirror; missing name, trivial content |
| plugins/all-commands/commands/issue-triage.md | command | 40 | Missing name, missing allowed-tools, vague quantifiers ×5 |
| plugins/all-commands/commands/load-llms-txt.md | command | 30 | Missing name, missing allowed-tools, no instructions |
| plugins/all-commands/commands/docs.md | command | 30 | Missing name, truncated, no output format |
| plugins/all-commands/commands/use-stepper.md | command | 30 | Missing name, extremely sparse content |
| plugins/all-commands/commands/test-changelog-automation.md | command | 35 | Missing name, missing allowed-tools, minimal instructions |
| plugins/all-commands/commands/changelog-demo-command.md | command | 40 | Missing name, minimal instructions, no structure |
| plugins/all-commands/commands/optimize.md | command | 40 | 6-word body; missing name, no structure |
| plugins/all-commands/commands/rsi.md | command | 40 | Missing name, no allowed-tools, no empty input handling |
| plugins/commands-documentation-changelogs/commands/docs.md | command | 40 | Mirror of all-commands; missing name, truncated |
| plugins/agents-uc-taskmanager/agents/verifier.md | agent | 60 | Missing description frontmatter |
| plugins/agents-uc-taskmanager/agents/committer.md | agent | 60 | Missing description frontmatter |
| plugins/all-commands/commands/context-prime.md | command | 40 | Missing name, broken instructions, vague "relevant" |
| plugins/all-commands/commands/tdd.md | command | 40 | Missing name, incomplete content, no output format |
| plugins/all-commands/commands/five.md | command | 45 | Missing name, no empty input handling, minimal |
| plugins/all-commands/commands/update-docs.md | command | 45 | Missing name, incomplete instructions |
| plugins/all-commands/commands/create-docs.md | command | 55 | Missing name, missing steps, vague ×4 |
| plugins/all-commands/commands/svelte-storybook.md | command | 50 | Missing name, missing allowed-tools, no output format |
| plugins/all-commands/commands/svelte-debug.md | command | 50 | Missing name, missing allowed-tools, no output format |
| plugins/all-commands/commands/svelte-a11y.md | command | 50 | Missing name, missing allowed-tools, no output format |
| plugins/all-commands/commands/svelte-optimize.md | command | 50 | Missing name, missing allowed-tools, no output format |
| plugins/all-commands/commands/svelte-scaffold.md | command | 50 | Missing name, missing allowed-tools, no output format |
| plugins/all-commands/commands/add-to-changelog.md | command | 50 | Missing name, very short, vague "standard" |
| plugins/all-commands/commands/bug-fix.md | command | 45 | Missing name, very terse, no output format |
| plugins/all-commands/commands/pr-review.md | command | 50 | Missing name, file truncated, no security review |
| plugins/all-commands/commands/husky.md | command | 55 | Missing name, no numbered steps, vague ×3 |
| plugins/all-commands/commands/check-file.md | command | 55 | Missing name, vague: "comprehensive", "actionable" |
| plugins/all-commands/commands/create-onboarding-guide.md | command | 55 | Missing name, missing allowed-tools, vague ×3 |
| plugins/all-commands/commands/load-llms-txt.md | command | 55 | Missing name, missing allowed-tools, no clear instructions |
| plugins/all-commands/commands/simulation-calibrator.md | command | 55 | Missing name, vague ×3 |
| plugins/all-commands/commands/act.md | command | 55 | Missing name, very sparse content |
| plugins/commands-team-collaboration/commands/retrospective-analyzer.md | command | 50 | Missing name, missing allowed-tools, no numbered steps |
| plugins/commands-team-collaboration/commands/architecture-review.md | command | 45 | Missing name, missing allowed-tools, no numbered steps, vague ×5 |
| plugins/commands-team-collaboration/commands/issue-triage.md | command | 40 | Missing name, missing allowed-tools, vague ×5 |
| plugins/commands-team-collaboration/commands/create-architecture-documentation.md | command | 50 | Missing name, missing allowed-tools, vague ×3 |
| plugins/commands-documentation-changelogs/commands/create-onboarding-guide.md | command | 55 | Missing name, missing allowed-tools, vague ×3 |
| plugins/commands-documentation-changelogs/commands/create-architecture-documentation.md | command | 50 | Missing name, missing allowed-tools, vague ×3 |
| plugins/commands-security-audit/commands/add-authentication-system.md | command | 65 | Missing name, missing allowed-tools, vague ×3 |
| plugins/agents-specialized-domains/agents/mcp-deployment-orchestrator.md | agent | 70 | Missing model; vague ×4; no explicit output format |
| plugins/agents-specialized-domains/agents/risk-manager.md | agent | 70 | Missing model; no explicit output format; vague ×5 |
| plugins/agents-specialized-domains/agents/social-media-clip-creator.md | agent | 75 | Missing model; no explicit output format |
| plugins/agents-specialized-domains/agents/agent-expert.md | agent | 75 | Missing model; vague ×4 |
| plugins/agents-specialized-domains/agents/game-developer.md | agent | 75 | Missing model; vague ×3; no explicit output format |
| plugins/agents-specialized-domains/agents/legacy-modernizer.md | agent | 75 | Missing model; vague ×5 |
| plugins/agents-specialized-domains/agents/research-brief-generator.md | agent | 75 | Missing model; vague ×5 |
| plugins/agents-specialized-domains/agents/api-documenter.md | agent | 75 | Missing model; vague ×5 |
| plugins/agents-specialized-domains/agents/content-marketer.md | agent | 75 | Missing model; vague ×4 |
| plugins/agents-specialized-domains/agents/sales-automator.md | agent | 75 | Missing model; vague ×4 |
| plugins/agents-specialized-domains/agents/project-supervisor-orchestrator.md | agent | 75 | Missing model; vague ×4; output format implicit |
| plugins/agents-specialized-domains/agents/research-orchestrator.md | agent | 75 | Missing model; vague ×4 |
| plugins/agents-specialized-domains/agents/market-research-analyst.md | agent | 75 | Missing model; vague ×4 |
| plugins/agents-sales-marketing/agents/risk-manager.md | agent | 70 | Missing model; no explicit output format |
| plugins/agents-sales-marketing/agents/social-media-clip-creator.md | agent | 75 | Missing model; no explicit output format |
| plugins/agents-sales-marketing/agents/content-marketer.md | agent | 75 | Missing model; vague ×4 |
| plugins/agents-sales-marketing/agents/sales-automator.md | agent | 75 | Missing model; vague ×4 |
| plugins/agents-sales-marketing/agents/customer-support.md | agent | 78 | Missing model; vague ×3 |
| plugins/agents-sales-marketing/agents/social-media-copywriter.md | agent | 78 | Missing model; vague ×3 |
| plugins/vulnetix/skills/exploits/SKILL.md | skill | 45 | Missing name; vague quantifiers cap hit (−20) |
| plugins/agent-triforce/skills/code-health/SKILL.md | skill | 70 | Missing name; no output format |
| plugins/all-skills/skills/dropbox-automation/SKILL.md | skill | 70 | Missing name; no output format |
| plugins/all-skills/skills/github-automation/SKILL.md | skill | 70 | Missing name; no output format |
| plugins/all-skills/skills/stripe-automation/SKILL.md | skill | 70 | Missing name; no output format |
| plugins/nextjs-expert/skills/app-router/SKILL.md | skill | 75 | Missing description; vague "clearly" |
| plugins/cc-best/agents/architect.md | agent | 75 | Missing description; no examples; no output format |
| plugins/cc-best/agents/code-reviewer.md | agent | 75 | Missing description; no examples; no output format |
| plugins/agents-development-architecture/agents/backend-architect.md | agent | 82 | Missing model; no examples; vague ×2 |
| plugins/agents-development-architecture/agents/react-performance-optimization.md | agent | 82 | No examples; vague ×4 |
| plugins/agents-development-architecture/agents/mobile-developer.md | agent | 83 | Missing model; no examples |
| plugins/agents-development-architecture/agents/ios-developer.md | agent | 83 | Missing model; no examples |
| plugins/agents-development-architecture/agents/graphql-architect.md | agent | 84 | No examples; missing output format; vague ×3 |
| plugins/agents-development-architecture/agents/wordpress-developer.md | agent | 84 | No examples; vague ×7 |
| plugins/agents-development-architecture/agents/drupal-developer.md | agent | 84 | Vague ×6 |
| plugins/agents-development-architecture/agents/frontend-developer.md | agent | 85 | No examples; vague ×2 |
| plugins/agents-development-architecture/agents/directus-developer.md | agent | 86 | Vague ×4 |
| plugins/agents-development-architecture/agents/laravel-vue-developer.md | agent | 87 | Vague ×3 |
| plugins/agents-data-ai/agents/mlops-engineer.md | agent | 87 | Missing model; no examples; vague ×3 |
| plugins/agents-data-ai/agents/data-engineer.md | agent | 87 | Missing model; no examples; vague ×3 |
| plugins/agents-data-ai/agents/prompt-engineer.md | agent | 87 | Missing model; one example (need 2+); vague ×2 |
| plugins/agents-data-ai/agents/ml-engineer.md | agent | 87 | Missing model; no examples; vague ×4 |
| plugins/agents-data-ai/agents/data-scientist.md | agent | 87 | Missing model; no examples; vague ×4 |
| plugins/agents-development-architecture/agents/nextjs-app-router-developer.md | agent | 89 | Vague ×3 |
| plugins/agents-data-ai/agents/search-specialist.md | agent | 87 | Missing model; vague ×4 |
| plugins/agents-data-ai/agents/context-manager.md | agent | 87 | Missing model; vague ×5 |
| plugins/agents-data-ai/agents/hackathon-ai-strategist.md | agent | 87 | Missing model; no formal examples |
| plugins/agents-data-ai/agents/ai-engineer.md | agent | 84 | Missing model; no examples; vague ×3 |
| plugins/agents-data-ai/agents/llms-maintainer.md | agent | 87 | Missing model; vague ×3 |
| plugins/agents-data-ai/agents/task-decomposition-expert.md | agent | 91 | Vague ×2 |
| plugins/feedoracle-compliance/skills/compliance/SKILL.md | skill | 85 | Vague ×1; no output format |
| plugins/mortgage/skills/mortgage-compliance/SKILL.md | skill | 85 | No output format; vague ×1 |
| plugins/cc-best/skills/architecture/SKILL.md | skill | 85 | No output format; vague ×1 |
| plugins/agents-uc-taskmanager/skills/work-status/SKILL.md | skill | 90 | Minor vague terms |
| plugins/all-commands/commands/architecture-review.md | command | 50 | Missing name, missing allowed-tools, vague ×5, no numbered steps |
| plugins/all-commands/commands/svelte-migrate.md | command | 65 | Missing name, missing allowed-tools, vague ×2 |
| plugins/all-commands/commands/svelte-component.md | command | 70 | Missing name, missing allowed-tools, vague ×2 |
| plugins/all-commands/commands/svelte-storybook-setup.md | command | 75 | Missing name, vague ×2 |
| plugins/all-commands/commands/rollback-deploy.md | command | 70 | Missing name; minor vague |
| plugins/all-commands/commands/commit.md | command | 70 | Missing name; vague ×2 |
| plugins/all-commands/commands/create-pr.md | command | 65 | Missing name; no numbered steps; no output format |
| plugins/all-commands/commands/doc-api.md | command | 70 | Missing name; vague ×2 |
| plugins/all-commands/commands/e2e-setup.md | command | 70 | Missing name; vague ×2 |
| plugins/all-commands/commands/test-coverage.md | command | 70 | Missing name; vague ×2 |
| plugins/all-commands/commands/implement-caching-strategy.md | command | 70 | Missing name; missing allowed-tools |
| plugins/all-commands/commands/performance-audit.md | command | 65 | Missing name; no allowed-tools; vague ×2 |
| plugins/all-commands/commands/add-performance-monitoring.md | command | 75 | Missing name; good structure |
| plugins/all-commands/commands/create-prd.md | command | 80 | Missing name; has description, allowed-tools |
| plugins/all-commands/commands/write-tests.md | command | 85 | Missing name; otherwise well-structured |
| plugins/all-commands/commands/prime.md | command | 100 | Complete: name ✓ description ✓ allowed-tools ✓ |
| plugins/all-commands/commands/move.md | command | 95 | Complete; excellent structure and examples |
| plugins/all-commands/commands/remove.md | command | 95 | Complete; excellent structure and examples |
| plugins/all-commands/commands/status.md | command | 95 | Complete; clear output formatting |
| plugins/all-commands/commands/resume.md | command | 95 | Complete; extensive detail |
| plugins/all-commands/commands/find.md | command | 95 | Complete; comprehensive examples |
| plugins/all-commands/commands/create-command.md | command | 95 | Complete; detailed and organized |
| plugins/all-commands/commands/todo.md | command | 90 | Complete; clear usage examples |
| plugins/all-commands/commands/sync-pr-to-task.md | command | 90 | Complete; detailed |
| plugins/all-commands/commands/svelte-storybook-troubleshoot.md | command | 90 | Good structure; minimal issues |
| plugins/all-commands/commands/directory-deep-dive.md | command | 90 | Good structure |
| plugins/all-commands/commands/git-status.md | command | 85 | Good structure and detail |
| plugins/all-agents/agents/search-specialist.md | agent | 100 | None |
| plugins/all-agents/agents/text-comparison-validator.md | agent | 100 | None |
| plugins/all-agents/agents/seo-podcast-optimizer.md | agent | 100 | None |
| plugins/all-agents/agents/moc-agent.md | agent | 100 | None |
| plugins/all-agents/agents/url-context-validator.md | agent | 100 | None |
| plugins/all-agents/agents/architect-review.md | agent | 100 | None |
| plugins/all-agents/agents/database-admin.md | agent | 100 | None |
| plugins/all-agents/agents/database-optimization.md | agent | 100 | None |
| plugins/all-agents/agents/data-scientist.md | agent | 100 | None |
| plugins/all-agents/agents/review-agent.md | agent | 100 | None |
| plugins/all-agents/agents/ios-developer.md | agent | 100 | None |
| plugins/all-agents/agents/python-expert.md | agent | 100 | None |
| plugins/all-agents/agents/test-automator.md | agent | 100 | None |
| plugins/all-agents/agents/payment-integration.md | agent | 100 | None |
| plugins/all-agents/agents/mcp-server-architect.md | agent | 100 | None |
| plugins/all-agents/agents/arbitrage-bot.md | agent | 100 | None |
| plugins/all-agents/agents/agent-expert.md | agent | 100 | None |
| plugins/all-agents/agents/hackathon-ai-strategist.md | agent | 100 | None |
| plugins/all-agents/agents/mlops-engineer.md | agent | 100 | None |
| plugins/all-agents/agents/ui-ux-designer.md | agent | 100 | None |
| plugins/all-agents/agents/timestamp-precision-specialist.md | agent | 100 | None |
| plugins/all-agents/agents/debugger.md | agent | 100 | None |
| plugins/all-agents/agents/mcp-security-auditor.md | agent | 100 | None |
| plugins/all-agents/agents/database-optimizer.md | agent | 100 | None |
| plugins/all-agents/agents/ruby-expert.md | agent | 100 | None |
| plugins/all-agents/agents/risk-manager.md | agent | 100 | None |
| plugins/all-agents/agents/metadata-agent.md | agent | 100 | None |
| plugins/all-agents/agents/crypto-analyst.md | agent | 100 | None |
| plugins/all-agents/agents/javascript-developer.md | agent | 100 | None |
| plugins/all-agents/agents/ocr-grammar-fixer.md | agent | 100 | None |
| plugins/all-agents/agents/java-developer.md | agent | 100 | None |
| plugins/all-agents/agents/crypto-trader.md | agent | 100 | None |
| plugins/all-agents/agents/audio-quality-controller.md | agent | 100 | None |
| plugins/all-agents/agents/business-analyst.md | agent | 100 | None |
| plugins/all-agents/agents/customer-support.md | agent | 100 | None |
| plugins/all-agents/agents/laravel-vue-developer.md | agent | 100 | None |
| plugins/all-agents/agents/report-generator.md | agent | 100 | None |
| plugins/all-agents/agents/podcast-content-analyzer.md | agent | 100 | None |
| plugins/all-agents/agents/research-orchestrator.md | agent | 100 | None |
| plugins/all-agents/agents/url-link-extractor.md | agent | 100 | None |
| plugins/all-agents/agents/query-clarifier.md | agent | 100 | None |
| plugins/all-agents/agents/php-developer.md | agent | 100 | None |
| plugins/all-agents/agents/visual-analysis-ocr.md | agent | 100 | None |
| plugins/all-agents/agents/security-auditor.md | agent | 100 | None |
| plugins/all-agents/agents/sql-expert.md | agent | 100 | None |
| plugins/all-agents/agents/quant-analyst.md | agent | 100 | None |
| plugins/all-agents/agents/market-research-analyst.md | agent | 100 | None |
| plugins/all-agents/agents/academic-researcher.md | agent | 100 | None |
| plugins/all-agents/agents/api-security-audit.md | agent | 100 | None |
| plugins/all-agents/agents/technical-researcher.md | agent | 100 | None |
| plugins/all-agents/agents/twitter-ai-influencer-manager.md | agent | 100 | None |
| plugins/all-agents/agents/ocr-quality-assurance.md | agent | 100 | None |
| plugins/all-agents/agents/research-brief-generator.md | agent | 100 | None |
| plugins/all-agents/agents/academic-research-synthesizer.md | agent | 100 | None |
| plugins/all-agents/agents/graphql-architect.md | agent | 100 | None |
| plugins/all-agents/agents/command-expert.md | agent | 100 | None |
| plugins/all-agents/agents/terraform-specialist.md | agent | 100 | None |
| plugins/all-agents/agents/podcast-trend-scout.md | agent | 100 | None |
| plugins/all-agents/agents/task-decomposition-expert.md | agent | 100 | None |
| plugins/all-agents/agents/backend-architect.md | agent | 100 | None |
| plugins/all-agents/agents/react-performance-optimization.md | agent | 100 | None |
| plugins/all-agents/agents/crypto-risk-manager.md | agent | 100 | None |
| plugins/all-agents/agents/mcp-expert.md | agent | 100 | None |
| plugins/all-agents/agents/error-detective.md | agent | 100 | None |
| plugins/all-agents/agents/social-media-clip-creator.md | agent | 100 | None |
| plugins/all-agents/agents/rails-expert.md | agent | 100 | None |
| plugins/all-agents/agents/markdown-syntax-formatter.md | agent | 100 | None |
| plugins/all-agents/agents/blockchain-developer.md | agent | 100 | None |
| plugins/all-agents/agents/defi-strategist.md | agent | 100 | None |
| plugins/all-agents/agents/prompt-engineer.md | agent | 100 | None |
| plugins/all-agents/agents/legal-advisor.md | agent | 100 | None |
| plugins/all-agents/agents/tag-agent.md | agent | 100 | None |
| plugins/all-agents/agents/ai-engineer.md | agent | 100 | None |
| plugins/all-agents/agents/frontend-developer.md | agent | 100 | None |
| plugins/all-agents/agents/cloud-architect.md | agent | 100 | None |
| plugins/all-agents/agents/c-developer.md | agent | 100 | None |
| plugins/all-agents/agents/cpp-engineer.md | agent | 100 | None |
| plugins/all-agents/agents/project-supervisor-orchestrator.md | agent | 100 | None |
| plugins/all-agents/agents/llms-maintainer.md | agent | 100 | None |
| plugins/all-agents/agents/connection-agent.md | agent | 100 | None |
| plugins/all-agents/agents/nextjs-app-router-developer.md | agent | 100 | None |
| plugins/all-agents/agents/docusaurus-expert.md | agent | 100 | None |
| plugins/all-agents/agents/api-documenter.md | agent | 100 | None |
| plugins/all-agents/agents/podcast-transcriber.md | agent | 100 | None |
| plugins/all-agents/agents/social-media-copywriter.md | agent | 100 | None |
| plugins/all-agents/agents/mcp-testing-engineer.md | agent | 100 | None |
| plugins/all-agents/agents/data-engineer.md | agent | 100 | None |
| plugins/all-agents/agents/hyperledger-fabric-developer.md | agent | 100 | None |
| plugins/all-agents/agents/mcp-registry-navigator.md | agent | 100 | None |
| plugins/all-agents/agents/deployment-engineer.md | agent | 100 | None |
| plugins/all-agents/agents/game-developer.md | agent | 100 | None |
| plugins/all-agents/agents/legacy-modernizer.md | agent | 100 | None |
| plugins/all-agents/agents/typescript-expert.md | agent | 100 | None |
| plugins/all-agents/agents/golang-expert.md | agent | 100 | None |
| plugins/all-agents/agents/drupal-developer.md | agent | 100 | None |
| plugins/all-agents/agents/performance-engineer.md | agent | 100 | None |
| plugins/all-agents/agents/episode-orchestrator.md | agent | 100 | None |
| plugins/all-agents/agents/wordpress-developer.md | agent | 100 | None |
| plugins/all-agents/agents/incident-responder.md | agent | 100 | None |
| plugins/all-agents/agents/devops-troubleshooter.md | agent | 100 | None |
| plugins/all-agents/agents/research-synthesizer.md | agent | 100 | None |
| plugins/all-agents/agents/podcast-metadata-specialist.md | agent | 100 | None |
| plugins/all-agents/agents/ml-engineer.md | agent | 100 | None |
| plugins/all-agents/agents/rust-expert.md | agent | 100 | None |
| plugins/all-agents/agents/research-coordinator.md | agent | 100 | None |
| plugins/all-agents/agents/content-marketer.md | agent | 100 | None |
| plugins/all-agents/agents/comprehensive-researcher.md | agent | 100 | None |
| plugins/all-agents/agents/network-engineer.md | agent | 100 | None |
| plugins/all-agents/agents/directus-developer.md | agent | 100 | None |
| plugins/all-agents/agents/mcp-deployment-orchestrator.md | agent | 100 | None |
| plugins/agents-quality-security/agents/debugger.md | agent | 100 | None |
| plugins/agents-quality-security/agents/mcp-security-auditor.md | agent | 100 | None |
| plugins/agents-quality-security/agents/security-auditor.md | agent | 100 | None |
| plugins/agents-quality-security/agents/api-security-audit.md | agent | 100 | None |
| plugins/agents-quality-security/agents/command-expert.md | agent | 100 | None |
| plugins/agents-quality-security/agents/error-detective.md | agent | 100 | None |
| plugins/agents-quality-security/agents/mcp-testing-engineer.md | agent | 100 | None |
| plugins/agents-quality-security/agents/performance-engineer.md | agent | 100 | None |
| plugins/agents-quality-security/agents/incident-responder.md | agent | 100 | None |
| plugins/agents-quality-security/agents/code-reviewer.md | agent | 100 | None |
| plugins/agents-quality-security/agents/architect-review.md | agent | 100 | None |
| plugins/agents-quality-security/agents/dx-optimizer.md | agent | 100 | None |
| plugins/agents-quality-security/agents/review-agent.md | agent | 100 | None |
| plugins/agents-quality-security/agents/test-automator.md | agent | 100 | None |
| plugins/agents-quality-security/agents/mcp-server-architect.md | agent | 100 | None |
| plugins/ag2-agent-builder/agents/ag2-reviewer.md | agent | 100 | None |
| plugins/ag2-agent-builder/agents/ag2-prompt-engineer.md | agent | 100 | None |
| plugins/ag2-agent-builder/agents/ag2-architect.md | agent | 100 | None |
| plugins/agents-design-experience/agents/ui-ux-designer.md | agent | 100 | None |
| plugins/agents-design-experience/agents/accessibility-specialist.md | agent | 100 | None |
| plugins/agents-crypto-trading/agents/crypto-analyst.md | agent | 100 | None |
| plugins/agents-crypto-trading/agents/crypto-trader.md | agent | 100 | None |
| plugins/agents-crypto-trading/agents/crypto-risk-manager.md | agent | 100 | None |
| plugins/agents-crypto-trading/agents/defi-strategist.md | agent | 100 | None |
| plugins/agents-crypto-trading/agents/arbitrage-bot.md | agent | 100 | None |
| plugins/agents-infrastructure-operations/agents/database-optimizer.md | agent | 100 | None |
| plugins/agents-infrastructure-operations/agents/terraform-specialist.md | agent | 100 | None |
| plugins/agents-infrastructure-operations/agents/cloud-architect.md | agent | 100 | None |
| plugins/agents-infrastructure-operations/agents/deployment-engineer.md | agent | 100 | None |
| plugins/agents-infrastructure-operations/agents/devops-troubleshooter.md | agent | 100 | None |
| plugins/agents-infrastructure-operations/agents/network-engineer.md | agent | 100 | None |
| plugins/agents-infrastructure-operations/agents/database-admin.md | agent | 100 | None |
| plugins/agents-infrastructure-operations/agents/database-optimization.md | agent | 100 | None |
| plugins/agents-blockchain-web3/agents/blockchain-developer.md | agent | 100 | None |
| plugins/agents-blockchain-web3/agents/hyperledger-fabric-developer.md | agent | 100 | None |
| plugins/shipwright/agents/shipwright.md | agent | 100 | None |
| plugins/agents-business-finance/agents/business-analyst.md | agent | 100 | None |
| plugins/agents-business-finance/agents/quant-analyst.md | agent | 100 | None |
| plugins/agents-business-finance/agents/legal-advisor.md | agent | 100 | None |
| plugins/agents-business-finance/agents/payment-integration.md | agent | 100 | None |
| plugins/agents-language-specialists/agents/javascript-developer.md | agent | 100 | None |
| plugins/agents-language-specialists/agents/java-developer.md | agent | 100 | None |
| plugins/agents-language-specialists/agents/php-developer.md | agent | 100 | None |
| plugins/agents-language-specialists/agents/sql-expert.md | agent | 100 | None |
| plugins/agents-language-specialists/agents/rails-expert.md | agent | 100 | None |
| plugins/agents-language-specialists/agents/c-developer.md | agent | 100 | None |
| plugins/agents-language-specialists/agents/cpp-engineer.md | agent | 100 | None |
| plugins/agents-language-specialists/agents/typescript-expert.md | agent | 100 | None |
| plugins/agents-language-specialists/agents/golang-expert.md | agent | 100 | None |
| plugins/agents-language-specialists/agents/rust-expert.md | agent | 100 | None |
| plugins/agents-language-specialists/agents/python-expert.md | agent | 100 | None |
| plugins/agents-language-specialists/agents/ruby-expert.md | agent | 100 | None |
| plugins/agent-triforce/agents/forja-dev.md | agent | 100 | None |
| plugins/agent-triforce/agents/prometeo-pm.md | agent | 100 | None |
| plugins/agent-triforce/agents/centinela-qa.md | agent | 100 | None |
| plugins/mcp-servers-creative/agents/prompt-crafter.md | agent | 100 | None |
| plugins/mcp-servers-creative/agents/gallery-researcher.md | agent | 100 | None |
| plugins/mcp-servers-creative/agents/image-generator.md | agent | 100 | None |

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 1 |
| Low | 1 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks | plugins/budgetclaw/hooks/hooks.json, plugins/project-boundary/hooks/hooks.json |
| Scripts | 127 shell/Python/JS scripts across plugin directories |
| MCP Configs | .mcp.json not found in repo root; 3 MCP configs detected at plugin level |
| Package Manifests | package.json (root) — standard dev deps: ajv, chalk, glob, gray-matter |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH | plugins/budgetclaw/hooks/hooks.json | 8 | third-party binary execution at session start | `budgetclaw status` runs a binary from roninforge.org at every SessionStart. The binary was installed via `curl \| sh`. If roninforge.org is compromised or the binary behaves maliciously, it runs with Claude Code's privileges on every session. |
| 2 | MEDIUM | plugins/budgetclaw/hooks/hooks.json | 8 | curl-pipe-sh install instruction in echo | The hook echoes `curl -fsSL https://roninforge.org/get \| sh` as an install instruction when budgetclaw is absent. While not executed directly, this normalizes the unsafe curl-pipe-sh pattern for end users. |
| 3 | LOW | plugins/project-boundary/hooks/hooks.json | 9 | PreToolUse bash hook runs guard.sh | Executes `bash "${CLAUDE_PLUGIN_ROOT}/hooks/guard.sh"` on every Bash tool call. Defensive intent (blocking dangerous commands), but any compromise of guard.sh would silently intercept all Bash invocations. |

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | plugins/agents-uc-taskmanager/agents/scheduler.md | Missing `name` and `description` frontmatter fields | Agent fails to register; invisible to Claude Code agent picker |
| 2 | plugins/agents-uc-taskmanager/agents/specifier.md | Missing `name` and `description` frontmatter fields | Agent fails to register; invisible to Claude Code agent picker |
| 3 | plugins/agents-uc-taskmanager/agents/planner.md | Missing `name` and `description` frontmatter fields | Agent fails to register; invisible to Claude Code agent picker |
| 4 | plugins/agents-uc-taskmanager/agents/builder.md | Missing `name` and `description` frontmatter fields | Agent fails to register; invisible to Claude Code agent picker |
| 5 | plugins/agents-uc-taskmanager/agents/verifier.md | Missing `description` frontmatter field | Agent description blank in picker; confusing UX |
| 6 | plugins/agents-uc-taskmanager/agents/committer.md | Missing `description` frontmatter field | Agent description blank in picker; confusing UX |
| 7 | plugins/cc-best/agents/architect.md | Missing `description` frontmatter field | Agent description blank in picker |
| 8 | plugins/cc-best/agents/code-reviewer.md | Missing `description` frontmatter field | Agent description blank in picker |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | plugins/budgetclaw/hooks/hooks.json | Echo promotes curl-pipe-sh install (Medium) | Replace echo with: `echo '[budgetclaw not installed — see https://roninforge.org/install for safe install options]'` — remove the literal `curl \| sh` from user-visible text |
| 2 | plugins/project-boundary/hooks/hooks.json | guard.sh runs on every Bash call with no integrity check (Low) | Add a checksum or signature check before executing guard.sh, or document expected behavior so users can audit the script |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | plugins/agents-uc-taskmanager/agents/* (all 6) | Model not declared in frontmatter despite being set | −5 per file |
| 2 | plugins/agents-specialized-domains/agents/* (all ~40) | Universal missing model declaration | −5 per file |
| 3 | plugins/agents-sales-marketing/agents/* (all 6) | Universal missing model declaration | −5 per file |
| 4 | plugins/agents-development-architecture/agents/* (11) | Zero examples in 8 of 11 agents | −15 per file |
| 5 | plugins/agents-data-ai/agents/* (11) | Zero examples in 9 of 11 agents | −15 per file |
| 6 | plugins/cc-best/agents/architect.md | Zero examples (agents require 2+) | −15 |
| 7 | plugins/cc-best/agents/code-reviewer.md | Zero examples (agents require 2+) | −15 |
| 8 | plugins/agents-development-architecture/agents/backend-architect.md | Missing model; no examples | −5, −15 |
| 9 | plugins/agents-development-architecture/agents/graphql-architect.md | No examples; missing output format | −15, −10 |
| 10 | plugins/agents-development-architecture/agents/wordpress-developer.md | No examples; 7 vague quantifiers | −15, −14 |
| 11 | All ~350 command files | Missing `name` frontmatter field (standard for commands is description-only, but NLPM rubric penalizes absence) | −25 per file under strict rubric |
| 12 | ~180 command files | Missing `allowed-tools` specification | −5 per file |
| 13 | ~100 command files | Multi-step workflows without numbered steps | −10 per file |
| 14 | ~80 command files | No empty input handling | −10 per file |
| 15 | ~200 command files | Vague quantifiers ("appropriate", "comprehensive", "proper", "best", etc.) ≥3 occurrences | −2–20 per file |
| 16 | ~80 command files | Missing output format specification | −10 per file |
| 17 | plugins/vulnetix/skills/exploits/SKILL.md | Missing name; vague quantifier cap hit | −25, −20 |
| 18 | ~90 all-skills SKILL.md files | Missing `name` frontmatter field | −25 per file |
| 19 | ~30 skill files | Missing output format specification | −10 per file |
| 20 | plugins/all-agents/agents/code-reviewer.md | Missing explicit output format section | −10 |
| 21 | plugins/all-agents/agents/javascript-developer.md | Missing explicit output format section | −10 |
| 22 | plugins/all-agents/agents/accessibility-specialist.md | Model not declared | −5 |
| 23 | plugins/all-agents/agents/mobile-developer.md | Model not declared | −5 |

## Cross-Component

**Systematic duplication between canonical and specialized plugins**: Every agent in `agents-specialized-domains/`, `agents-sales-marketing/`, `agents-quality-security/`, `agents-crypto-trading/`, etc. also appears in `all-agents/`. Similarly, commands exist in both their source plugin and `all-commands/`. The `all-agents/` and `all-commands/` versions are consistently higher quality (95–100 vs 70–90), suggesting the aggregator plugins were independently maintained or regenerated at a later date. This creates a version drift problem — fixes to the canonical set do not flow back to source plugins.

**agents-uc-taskmanager is an isolated system**: The `agents-uc-taskmanager` plugin uses a completely different agent format (XML-structured prompts with `<tool>` tags, no standard NLPM frontmatter). The agents have valid model declarations and rich examples, but are invisible to standard NLPM tooling due to missing `name`/`description` fields. This is a structural bug, not a content problem — the agents themselves are high-quality.

**No broken cross-references detected**: Commands that invoke sub-agents reference agent names that exist in `all-agents/`. Skill references in agents point to SKILL.md files that are present. No orphaned references found.

**budgetclaw plugin tight-coupling**: The `budgetclaw` plugin hooks depend on an external binary (`budgetclaw`) from a third-party domain. This creates an external dependency that is invisible to the plugin manifest and cannot be audited from the source alone.

## Recommendation

**BLOCKED — do not submit PRs for security fixes requiring code change. File private security report with the maintainer regarding the `budgetclaw` hooks dependency on the roninforge.org binary.**

Once the maintainer clears the budgetclaw security concern, this repo is otherwise PR-ready for NL bugs:

1. **Immediate (bugs)**: Add `name` and `description` to the 4 agents-uc-taskmanager agents missing both fields (scheduler, specifier, planner, builder). Add `description` to verifier, committer, and both cc-best agents.

2. **High-value quality fix**: Add `model` declarations to all agents-specialized-domains, agents-sales-marketing, and agents-data-ai agents (~57 files). These are the most impactful quality improvements available.

3. **Low-hanging fruit**: Replace the curl-pipe-sh echo in budgetclaw/hooks/hooks.json with a URL-only install reference (Medium security fix, safe to PR after security review).

4. **Structural note for maintainer**: The agents-uc-taskmanager agents use a non-standard XML format. Add standard `name`/`description` frontmatter without changing the agent body — this makes them discoverable without altering functionality.
