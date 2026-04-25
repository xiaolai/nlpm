# NLPM Audit: 0xmariowu/Autosearch
**Date**: 2026-04-06  |  **Artifacts**: 74  |  **Strategy**: progressive
**NL Score**: 92/100
**Security**: BLOCKED
**Bugs**: 1  |  **Quality Issues**: 14  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| CLAUDE.md | project-rules | 50 | Not in NL artifact format; no frontmatter |
| tests/fixtures/skills/missing_required/SKILL.md | skill-fixture | 65 | Intentionally missing `name` field (test fixture) |
| commands/autosearch.md | command | 70 | Missing `name` frontmatter field |
| .claude-plugin/plugin.json | config | 75 | JSON config, no NL prose body |
| autosearch/skills/channels/twitter/SKILL.md | skill-channel | 88 | No When to Choose / How To Search / Known Quirks sections |
| autosearch/skills/channels/tieba/SKILL.md | skill-channel | 88 | Minimal structured guidance; partial Chinese body |
| autosearch/skills/channels/linkedin/SKILL.md | skill-channel | 88 | Thin body; minimal guidance sections |
| tests/fixtures/skills/bad_fallback/SKILL.md | skill-fixture | 90 | No Quality Bar section (test fixture) |
| tests/fixtures/skills/bad_requires_token/SKILL.md | skill-fixture | 90 | No Quality Bar section (test fixture) |
| tests/fixtures/skills/valid_tool/SKILL.md | skill-fixture | 90 | No Quality Bar section (test fixture) |
| tests/fixtures/skills/channels/stub_cookie/SKILL.md | skill-fixture | 90 | No body beyond frontmatter (test fixture) |
| tests/fixtures/skills/channels/stub_ok/SKILL.md | skill-fixture | 90 | No body beyond frontmatter (test fixture) |
| tests/fixtures/skills/valid_channel/SKILL.md | skill-fixture | 90 | Minimal body, no Quality Bar (test fixture) |
| autosearch/skills/channels/papers/SKILL.md | skill-channel | 90 | No When to Choose / How To Search sections |
| autosearch/skills/channels/stackoverflow/SKILL.md | skill-channel | 90 | No When to Choose / How To Search sections |
| autosearch/skills/channels/podcast_cn/SKILL.md | skill-channel | 90 | No When to Choose / How To Search sections |
| autosearch/skills/channels/devto/SKILL.md | skill-channel | 90 | No When to Choose / How To Search sections |
| autosearch/skills/channels/wikipedia/SKILL.md | skill-channel | 90 | No When to Choose / How To Search sections |
| autosearch/skills/channels/searxng/SKILL.md | skill-channel | 90 | No Known Quirks section |
| autosearch/skills/channels/dockerhub/SKILL.md | skill-channel | 90 | Missing Known Quirks section |
| autosearch/skills/channels/wikidata/SKILL.md | skill-channel | 90 | No When to Choose / How To Search sections |
| autosearch/skills/channels/sogou_weixin/SKILL.md | skill-channel | 90 | No When to Choose / How To Search sections |
| autosearch/skills/channels/infoq_cn/SKILL.md | skill-channel | 90 | No When to Choose / How To Search sections |
| autosearch/skills/channels/package_search/SKILL.md | skill-channel | 90 | No When to Choose / How To Search sections |
| autosearch/skills/channels/google_news/SKILL.md | skill-channel | 90 | No When to Choose / How To Search sections |
| autosearch/skills/channels/reddit/SKILL.md | skill-channel | 90 | No When to Choose / How To Search sections |
| autosearch/skills/channels/kr36/SKILL.md | skill-channel | 90 | No When to Choose / How To Search sections |
| autosearch/skills/channels/instagram/SKILL.md | skill-channel | 92 | `experience_digest: experience/experience.md` deviates from project standard |
| autosearch/skills/channels/pubmed/SKILL.md | skill-channel | 92 | Missing Known Quirks section |
| autosearch/skills/channels/discourse_forum/SKILL.md | skill-channel | 92 | Thin body; no Known Quirks |
| .github/agents/test-sufficiency.md | agent | 93 | No complete I/O examples; vague "adequately" in description |
| autosearch/skills/channels/hackernews/SKILL.md | skill-channel | 93 | How To Search uses repeated identical method bullets |
| autosearch/skills/channels/xueqiu/SKILL.md | skill-channel | 93 | Thin Known Quirks; non-standard Quality Bar |
| autosearch/skills/channels/wechat_channels/SKILL.md | skill-channel | 93 | `experience_digest: experience/experience.md` deviates from project standard |
| autosearch/skills/channels/douyin/SKILL.md | skill-channel | 94 | Planned methods include cookie-based route not in fallback_chain |
| autosearch/skills/channels/v2ex/SKILL.md | skill-channel | 95 | Clean |
| autosearch/skills/channels/crossref/SKILL.md | skill-channel | 95 | Clean |
| autosearch/skills/channels/github/SKILL.md | skill-channel | 95 | How To Search sections are marked "(Planned)" |
| autosearch/skills/channels/youtube/SKILL.md | skill-channel | 95 | How To Search sections are marked "(Planned)" |
| autosearch/skills/channels/ddgs/SKILL.md | skill-channel | 95 | Clean |
| autosearch/skills/channels/dblp/SKILL.md | skill-channel | 95 | Clean |
| autosearch/skills/channels/zhihu/SKILL.md | skill-channel | 95 | How To Search sections are marked "(Planned)" |
| autosearch/skills/channels/kuaishou/SKILL.md | skill-channel | 95 | Clean |
| autosearch/skills/channels/tiktok/SKILL.md | skill-channel | 95 | Clean |
| autosearch/skills/channels/arxiv/SKILL.md | skill-channel | 95 | How To Search sections are marked "(Planned)" |
| autosearch/skills/channels/sec_edgar/SKILL.md | skill-channel | 95 | Clean |
| autosearch/skills/channels/weibo/SKILL.md | skill-channel | 95 | Clean |
| autosearch/skills/channels/xiaohongshu/SKILL.md | skill-channel | 95 | Clean |
| autosearch/skills/channels/bilibili/SKILL.md | skill-channel | 95 | How To Search sections are marked "(Planned)" |
| autosearch/skills/channels/huggingface_hub/SKILL.md | skill-channel | 96 | Clean |
| autosearch/skills/channels/openalex/SKILL.md | skill-channel | 96 | Clean |
| autosearch/skills/meta/context-retention-policy/SKILL.md | skill-meta | 96 | Clean |
| autosearch/skills/meta/model-routing/SKILL.md | skill-meta | 96 | Clean |
| autosearch/skills/meta/perspective-questioning/SKILL.md | skill-meta | 96 | Clean |
| autosearch/skills/meta/tikhub-fallback/SKILL.md | skill-meta | 96 | Clean |
| autosearch/skills/meta/trace-harvest/SKILL.md | skill-meta | 96 | Clean |
| autosearch/skills/meta/citation-index/SKILL.md | skill-meta | 97 | Clean |
| autosearch/skills/meta/graph-search-plan/SKILL.md | skill-meta | 97 | Clean |
| autosearch/skills/meta/recent-signal-fusion/SKILL.md | skill-meta | 97 | Clean |
| autosearch/skills/meta/delegate-subtask/SKILL.md | skill-meta | 97 | Clean |
| autosearch/skills/meta/experience-compact/SKILL.md | skill-meta | 97 | Clean |
| autosearch/skills/meta/reflective-search-loop/SKILL.md | skill-meta | 97 | Clean |
| autosearch/skills/meta/channel-selection/SKILL.md | skill-meta | 97 | Clean |
| autosearch/skills/meta/experience-capture/SKILL.md | skill-meta | 97 | Clean |
| autosearch/skills/router/SKILL.md | skill-router | 97 | Clean |
| autosearch/skills/tools/mcporter/SKILL.md | skill-tool | 97 | Clean |
| autosearch/skills/tools/fetch-playwright/SKILL.md | skill-tool | 97 | Recommends unpinned `npx @playwright/mcp@latest` |
| autosearch/skills/tools/fetch-jina/SKILL.md | skill-tool | 97 | Clean |
| autosearch/skills/tools/video-to-text-bcut/SKILL.md | skill-tool | 98 | Clean |
| autosearch/skills/tools/video-to-text-local/SKILL.md | skill-tool | 98 | Clean |
| autosearch/skills/tools/fetch-firecrawl/SKILL.md | skill-tool | 98 | Clean |
| autosearch/skills/tools/video-to-text-groq/SKILL.md | skill-tool | 98 | Clean |
| autosearch/skills/tools/fetch-crawl4ai/SKILL.md | skill-tool | 98 | Clean |
| autosearch/skills/tools/video-to-text-openai/SKILL.md | skill-tool | 98 | Clean |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 2 |
| Low | 1 |

*Note: Pre-scan reported 4 critical pattern matches. Two were false positives on analysis: `release-gate.sh:164` (curl|sh inside an echo message, never executed) and `scripts/e2b/scenarios/p_desktop_gui.py:124` (base64 used as transport into an E2B sandbox, not obfuscated execution).*

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Shell scripts | `scripts/install.sh`, `scripts/bump-version.sh`, `scripts/nightly-local.sh`, `scripts/release-gate.sh`, `scripts/dev/start-searxng.sh`, `scripts/validate/init_channel_experience.sh` |
| Python scripts | 38 files across `scripts/e2b/`, `scripts/validate/`, `scripts/bench/` |
| Node.js scripts | `npm/bin/autosearch-ai.js` |
| MCP configs | 0 |
| Package manifests | `package.json` (dev deps: husky, commitlint), `npm/package.json` (npm installer wrapper) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | npm/bin/autosearch-ai.js | 198 | curl-pipe-bash | npm wrapper downloads and executes remote install.sh via `bash -c "curl -fsSL … | bash"` without cryptographic verification; triggered on `npx autosearch-ai` if autosearch is not installed |
| 2 | Medium | scripts/e2b/bench_channels.py | 184 | curl-pipe-sh | Sandbox setup string contains `curl -LsSf https://astral.sh/uv/install.sh \| sh` to bootstrap uv inside E2B sandbox; no checksum verification |
| 3 | Medium | scripts/e2b/sandbox_runner.py | 202 | unpinned-git-install | `pip3 install git+https://github.com/0xmariowu/Autosearch.git` installs from GitHub HEAD without a version pin or commit hash |
| 4 | Low | scripts/install.sh | 134 | path-modification | Installer appends `export PATH="$HOME/.local/bin:$PATH"` to `~/.zshrc`, `~/.bashrc`, or `~/.profile` without a dry-run guard for CI |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/autosearch.md | Missing `name` field in YAML frontmatter | NLPM scanner cannot register this command; `name` is required for command discovery |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/e2b/bench_channels.py | curl-pipe-sh installs uv without checksum in CI sandbox | Pin uv version: `curl -LsSf https://astral.sh/uv/install.sh | sh -s -- --version x.y.z` or use `uv self install x.y.z` |
| 2 | scripts/e2b/sandbox_runner.py | pip install from git HEAD (no version pin) | Pin to a specific tag or commit: `git+https://github.com/0xmariowu/Autosearch.git@vX.Y.Z` |
| 3 | autosearch/skills/tools/fetch-playwright/SKILL.md | Install example recommends `npx @playwright/mcp@latest` (unpinned) | Document a pinned version: `npx @playwright/mcp@0.x.y` |
| 4 | autosearch/skills/tools/mcporter/SKILL.md | Install example uses `npx -y @mcporter/mcp-router` (unpinned) | Pin or document version verification before trusting the package |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/autosearch.md | No explicit empty-input guard; `$ARGUMENTS` passed directly to `run_clarify` with no empty-string check | -5 |
| 2 | .github/agents/test-sufficiency.md | Zero complete I/O examples; only an output template is shown | -5 |
| 3 | .github/agents/test-sufficiency.md | Vague qualifier "adequately" in description line 3 | -2 |
| 4 | CLAUDE.md | Project rules document, not an NL artifact; no YAML frontmatter; NLPM cannot score it meaningfully | informational |
| 5 | .claude-plugin/plugin.json | JSON config file; no NL prose body; scoring is limited to field presence | informational |
| 6 | tests/fixtures/skills/*/SKILL.md (6 files) | No `# Quality Bar` section; test fixtures intentionally minimal | -10 each (expected) |
| 7 | autosearch/skills/channels/twitter/SKILL.md | Missing "When to Choose It", "How To Search", and "Known Quirks" structural sections | -12 |
| 8 | autosearch/skills/channels/tieba/SKILL.md | How To Search is a single sentence; body partially in Chinese while frontmatter is English | -12 |
| 9 | autosearch/skills/channels/linkedin/SKILL.md | Body is three short sentences; "Known Quirks" is two stub bullets | -12 |
| 10 | autosearch/skills/channels/instagram/SKILL.md | `experience_digest` field uses `experience/experience.md` (subdirectory path) vs. project-wide standard `experience.md` | -3 |
| 11 | autosearch/skills/channels/wechat_channels/SKILL.md | Same `experience_digest: experience/experience.md` path deviation as instagram | -3 |
| 12 | autosearch/skills/channels/hackernews/SKILL.md | "How To Search (Planned)" section repeats the same method name (`algolia_search`) as three separate bullets with no distinguishing content | -4 |
| 13 | autosearch/skills/channels/douyin/SKILL.md | Body references `via_douyin_mcp` method and `cookie:douyin` requirement but neither appears in the frontmatter `methods` or `fallback_chain` | -4 |
| 14 | Multiple channel skills (github, youtube, zhihu, arxiv, bilibili) | "How To Search" sections marked "(Planned)" — implementation does not yet match the described behavior | informational |

## Cross-Component
**experience_digest path inconsistency**: `autosearch/skills/channels/instagram/SKILL.md` and `autosearch/skills/channels/wechat_channels/SKILL.md` declare `experience_digest: experience/experience.md`, using a nested subdirectory path. All other 50+ skills in the project use `experience_digest: experience.md` (sibling file). The runtime loader at `autosearch/skills/experience.py:107` (`load_experience_digest`) resolves this path relative to the skill directory. The deviating paths will correctly resolve if the loader uses the literal value, but if it normalises to a basename, the two skills' digests will never be found. **Recommend aligning both to `experience.md`.**

**Router group references**: `autosearch/skills/router/SKILL.md` declares `loads:` for 14 group index files under `references/groups/`. All 14 files (`channels-chinese-ugc.md`, `channels-cn-tech.md`, `channels-academic.md`, `channels-code-package.md`, `channels-market-product.md`, `channels-community-en.md`, `channels-social-career.md`, `channels-generic-web.md`, `channels-video-audio.md`, `tools-fetch-render.md`, `workflow-planning.md`, `workflow-quality.md`, `workflow-synthesis.md`, `workflow-growth.md`) are confirmed present. ✓

**Planned methods undeclared**: `autosearch/skills/channels/douyin/SKILL.md` body describes a `via_douyin_mcp` implementation path with `cookie:douyin` dependency, but the frontmatter `methods` list only declares `via_tikhub`. Users reading the skill will expect two search paths; only one is registered.

## Recommendation
BLOCKED — do not submit PRs. File private security report.

**Reason**: `npm/bin/autosearch-ai.js` contains a `curl … | bash` pipeline (High severity) that downloads and executes a remote installer script without cryptographic verification. While the wrapper requires user confirmation before firing and does not run on `npm install`, the pattern is a supply-chain risk if the GitHub raw CDN or the install.sh URL is compromised.

**Action path**:
1. File private security report to 0xmariowu describing the npm curl-pipe-bash finding (Finding #1).
2. After maintainer acknowledges, submit separate PRs for:
   - NL bug: add `name:` field to `commands/autosearch.md`
   - Medium security: pin uv version in `scripts/e2b/bench_channels.py`
   - Medium security: pin autosearch install in `scripts/e2b/sandbox_runner.py`
   - Cross-component: align `experience_digest` path in `instagram/SKILL.md` and `wechat_channels/SKILL.md`
