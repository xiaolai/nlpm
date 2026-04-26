# NLPM Audit: Xquik-dev/x-twitter-scraper
**Date**: 2026-04-06  |  **Artifacts**: 46  |  **Strategy**: batched
**NL Score**: 97/100
**Security**: CLEAR
**Bugs**: 5  |  **Quality Issues**: 7  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| commands/post.md | Command | 60 | Missing `name` frontmatter, no numbered steps |
| commands/search.md | Command | 70 | Missing `name` frontmatter |
| commands/trending.md | Command | 70 | Missing `name` frontmatter |
| commands/user.md | Command | 70 | Missing `name` frontmatter |
| .claude-plugin/plugin.json | Plugin manifest | 100 | None |
| skills/check-mutuals/SKILL.md | Skill | 100 | None |
| skills/clean-followers/SKILL.md | Skill | 100 | None |
| skills/export-tweets-csv/SKILL.md | Skill | 100 | None |
| skills/extract-followers/SKILL.md | Skill | 100 | None |
| skills/find-bangers/SKILL.md | Skill | 100 | None |
| skills/find-influencers/SKILL.md | Skill | 100 | None |
| skills/find-viral-tweets/SKILL.md | Skill | 100 | None |
| skills/follow-unfollow/SKILL.md | Skill | 100 | None |
| skills/for-you-feed/SKILL.md | Skill | 100 | None |
| skills/going-viral/SKILL.md | Skill | 100 | None |
| skills/grow-followers/SKILL.md | Skill | 100 | None |
| skills/monitor-accounts/SKILL.md | Skill | 100 | None |
| skills/optimize-tweets/SKILL.md | Skill | 100 | None |
| skills/post-tweets/SKILL.md | Skill | 100 | None |
| skills/run-giveaway/SKILL.md | Skill | 100 | None |
| skills/search-tweets/SKILL.md | Skill | 100 | None |
| skills/send-dms/SKILL.md | Skill | 100 | None |
| skills/top-replies/SKILL.md | Skill | 100 | None |
| skills/track-competitors/SKILL.md | Skill | 100 | None |
| skills/track-hashtags/SKILL.md | Skill | 100 | None |
| skills/track-mentions/SKILL.md | Skill | 100 | None |
| skills/trending-news/SKILL.md | Skill | 100 | None |
| skills/tweet-analytics/SKILL.md | Skill | 100 | None |
| skills/tweet-ideas/SKILL.md | Skill | 100 | None |
| skills/tweet-replies/SKILL.md | Skill | 100 | None |
| skills/tweet-style/SKILL.md | Skill | 100 | None |
| skills/tweet-webhooks/SKILL.md | Skill | 100 | None |
| skills/update-x-profile/SKILL.md | Skill | 100 | None |
| skills/user-tweets/SKILL.md | Skill | 100 | None |
| skills/who-liked/SKILL.md | Skill | 100 | None |
| skills/who-quoted/SKILL.md | Skill | 100 | None |
| skills/who-retweeted/SKILL.md | Skill | 100 | None |
| skills/write-threads/SKILL.md | Skill | 100 | None |
| skills/write-tweets/SKILL.md | Skill | 100 | None |
| skills/x-articles/SKILL.md | Skill | 100 | None |
| skills/x-bookmarks/SKILL.md | Skill | 100 | None |
| skills/x-communities/SKILL.md | Skill | 100 | None |
| skills/x-lists/SKILL.md | Skill | 100 | None |
| skills/x-spaces/SKILL.md | Skill | 100 | None |
| skills/x-trends/SKILL.md | Skill | 100 | None |
| skills/x-twitter-scraper/SKILL.md | Skill | 100 | None |

**Weighted average**: (60+70+70+70) + (42 × 100) / 46 = 4470 / 46 = 97.17 → **97/100**

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | None |
| Scripts | scripts/check-versions.mjs |
| MCP configs | .mcp.json |
| Package manifests | package.json |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | .mcp.json | 3 | SEC-mcp-external-server | MCP config routes all tool calls through external server `https://xquik.com/mcp` via streamable-http; API key injected from user config. Expected and documented as first-party by the skill; flagged for disclosure. |
| 2 | Low | package.json | 51 | SEC-unpinned-semver | devDependency `@tanstack/intent` pinned to `"latest"` — resolves to a moving target on every install, supply-chain risk for developers building the package. |
| 3 | Low | package.json | 48 | SEC-postinstall-script | `prepublishOnly` lifecycle script runs `node scripts/check-versions.mjs` before `npm publish`. Script is a read-only version-drift checker with no network calls or exec; risk is limited to the publishing workflow. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | commands/post.md | Missing `name` field in frontmatter | Slash-command registration fails; Claude Code cannot register `/post` without a name |
| 2 | commands/search.md | Missing `name` field in frontmatter | Slash-command registration fails; `/search` cannot be registered |
| 3 | commands/trending.md | Missing `name` field in frontmatter | Slash-command registration fails; `/trending` cannot be registered |
| 4 | commands/user.md | Missing `name` field in frontmatter | Slash-command registration fails; `/user` cannot be registered |
| 5 | skills/track-competitors/SKILL.md | `POST /extractions with tool=post_extractor` uses wrong parameter key; all other skills use `toolType=` | Following the example as written will cause a 400 `invalid_input` error from the API |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | package.json | `@tanstack/intent: "latest"` unpinned devDependency | Pin to a specific semver (e.g., `"1.0.0"`) to prevent silent upstream changes |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | commands/post.md | Missing `allowed-tools` declaration — command needs at least `xquik` and `explore` MCP tools declared | -5 |
| 2 | commands/post.md | Multi-step command (confirm → check account → post → show result) lacks numbered steps | -10 |
| 3 | commands/search.md | Missing `allowed-tools` declaration — command needs `xquik` MCP tool declared | -5 |
| 4 | commands/trending.md | Missing `allowed-tools` declaration — command needs `xquik` MCP tool declared | -5 |
| 5 | commands/user.md | Missing `allowed-tools` declaration — command needs `xquik` MCP tool declared | -5 |
| 6 | skills/track-competitors/SKILL.md | Example at line 43 uses `GET /x/users/{id}/tweets?limit=50&sort=top`; user-tweets SKILL.md explicitly documents that `limit` and `sort` are not supported by this endpoint | informational |
| 7 | skills/going-viral/SKILL.md | Endpoint table at line 33 shows `GET /x/tweets/search?sort=top&min_faves=5000`; search-tweets SKILL.md shows the sort parameter is `queryType=Top`, not `sort=top` | informational |

## Cross-Component
**Inconsistent endpoint parameter documentation (track-competitors ↔ user-tweets)**: `skills/track-competitors/SKILL.md` line 43 passes `sort=top` and `limit=50` to `GET /x/users/{id}/tweets`, but `skills/user-tweets/SKILL.md` line 80 explicitly states: "no `limit`, no `sort`". An agent reading only `track-competitors` will send unsupported parameters and receive an empty or malformed response.

**Inconsistent search parameter (going-viral ↔ search-tweets)**: `skills/going-viral/SKILL.md` line 33 shows `GET /x/tweets/search?sort=top&min_faves=5000`, but `skills/search-tweets/SKILL.md` documents the sort mode as the `queryType` parameter (`queryType=Top`), not `sort`. The `going-viral` endpoint table needs to be updated to match the canonical search-tweets reference.

**No broken relative-path references found**: all `[x-twitter-scraper](../x-twitter-scraper/SKILL.md)` links in sibling skills resolve correctly to the master skill file.

**Command name field gap is systemic**: all four commands are missing the `name` frontmatter field. This is consistent pattern, not four independent oversights — likely a missing step in the command authoring template.

## Recommendation
CLEAR — submit PRs for all bugs and medium/low security fixes. The four missing `name` fields in commands are the highest-priority fix (they block slash-command registration entirely). The `tool=` → `toolType=` typo in `track-competitors` is second priority (silent API failures). Pin `@tanstack/intent` to a fixed version before the next publish. The MCP server connection and prepublishOnly script are expected behaviors for this plugin type; no private disclosure required.
