---
slug: firecrawl-firecrawl-claude-plugin
repo: firecrawl/firecrawl-claude-plugin
audited: 2026-06-27
commit_sha: 52b6c0970b904b10641f223dbeb8f6b35643521c
score: 97
exemplifies:
  - R04
  - R05
  - R06
  - R07
  - R08
  - R21
---

# Exemplar: firecrawl/firecrawl-claude-plugin

**Score**: 97/100  |  **Date**: 2026-06-27  |  **Commit**: `52b6c0970b904b10641f223dbeb8f6b35643521c`

A 10-skill Claude Code plugin for the Firecrawl web-scraping CLI; 8 of 10 skills score 100/100 through disciplined trigger phrases, sub-500-line bodies, and a shared escalation pattern that routes the agent without duplication.

## Per-rule evidence

### R04 — Description as trigger

`firecrawl-scrape/SKILL.md` packs 7 quoted user phrases, a capability statement, a tool-replacement directive, and a "whenever" opener into a single description field:

> Real quote from `skills/firecrawl-scrape/SKILL.md:3-4`:
>
> ```
> description: |
>   Extract clean markdown from any URL, including JavaScript-rendered SPAs. Use this skill whenever the user provides a URL and wants its content, says "scrape", "grab", "fetch", "pull", "get the page", "extract from this URL", or "read this webpage". Handles JS-rendered pages, multiple concurrent URLs, and returns LLM-optimized markdown. Use this instead of WebFetch for any webpage content extraction.
> ```

What makes this strong: the description names literal strings users type ("scrape", "grab", "fetch", "pull"), covers a concrete capability boundary (JS-rendered SPAs), and explicitly replaces a built-in alternative ("Use this instead of WebFetch"). The master skill adds a negative trigger to prevent false fires:

> Real quote from `skills/firecrawl-cli/SKILL.md:3-4`:
>
> ```
> description: |
>   Search, scrape, and interact with the web via the Firecrawl CLI. ... Do NOT trigger for local file operations, git commands, deployments, or code editing tasks.
> ```

Two-clause descriptions are common; including a hard negative exclusion in the same description is rarer and eliminates the most likely false-positive triggers (a user saying "fetch this config file" should not fire a web-scrape skill).

### R05 — Body length

Eight of ten skills land under 100 lines; the longest non-CLI skill is `firecrawl-monitor/SKILL.md` at 246 lines. The master skill (`firecrawl-cli`) holds all shared decision logic at 322 lines; sub-skills stay short by declaring their position in the shared escalation chain and cross-referencing rather than re-explaining.

> Real quote from `skills/firecrawl-scrape/SKILL.md:17-18`:
>
> ```
> - Step 2 in the [workflow escalation pattern](firecrawl-cli): search → **scrape** → map → crawl → interact
> ```

`firecrawl-map/SKILL.md` is the tightest: 51 lines covering options table, two quick-start examples, and a "See also" block. It does not restate the escalation decision logic — it anchors itself within it and links out.

### R06 — Code examples must be runnable

Every skill opens with a `## Quick start` section of real `bash` commands with inline comments. `firecrawl-scrape` shows 6 progressive examples before the options table:

> Real quote from `skills/firecrawl-scrape/SKILL.md:21-40`:
>
> ```bash
> # Basic markdown extraction
> firecrawl scrape "<url>" -o .firecrawl/page.md
>
> # Main content only, no nav/footer
> firecrawl scrape "<url>" --only-main-content -o .firecrawl/page.md
>
> # Wait for JS to render, then scrape
> firecrawl scrape "<url>" --wait-for 3000 -o .firecrawl/page.md
>
> # Multiple URLs (each saved to .firecrawl/)
> firecrawl scrape https://example.com https://example.com/blog https://example.com/docs
>
> # Get markdown and links together
> firecrawl scrape "<url>" --format markdown,links -o .firecrawl/page.json
>
> # Ask a question about the page
> firecrawl scrape "https://example.com/pricing" --query "What is the enterprise plan price?"
> ```

Each example is a copy-pasteable shell command. The progression from basic → filtered → JS-wait → multi-URL → format-combo → query covers the six most common real user needs without pseudocode.

### R07 — Scope note when related skills exist

`firecrawl-cli/SKILL.md` devotes a dedicated `## When to Load References` section that maps every decision branch to the correct sub-skill with a one-line scope description:

> Real quote from `skills/firecrawl-cli/SKILL.md:211-223`:
>
> ```
> ## When to Load References
>
> - **Searching the web or finding sources first** -> [firecrawl-search](../firecrawl-search/SKILL.md)
> - **Scraping a known URL** -> [firecrawl-scrape](../firecrawl-scrape/SKILL.md)
> - **Finding URLs on a known site** -> [firecrawl-map](../firecrawl-map/SKILL.md)
> - **Bulk extraction from a docs section or site** -> [firecrawl-crawl](../firecrawl-crawl/SKILL.md)
> - **AI-powered structured extraction from complex sites** -> [firecrawl-agent](../firecrawl-agent/SKILL.md)
> - **Clicks, forms, login, pagination, or post-scrape browser actions** -> [firecrawl-interact](../firecrawl-interact/SKILL.md)
> - **Downloading a site to local files** -> [firecrawl-download](../firecrawl-download/SKILL.md)
> - **Parsing a local file (PDF, DOCX, XLSX, HTML, etc.)** -> [firecrawl-parse](../firecrawl-parse/SKILL.md)
> - **Detecting content changes on a website and getting notified by webhook or email (pricing, jobs, posts, docs, status pages, anything ongoing)** -> [firecrawl-monitor](../firecrawl-monitor/SKILL.md)
> - **Install, auth, or setup problems** -> [rules/install.md](rules/install.md)
> - **Output handling and safe file-reading patterns** -> [rules/security.md](rules/security.md)
> ```

Each entry is a condition clause ("when X") followed by a path-linked skill name. This lets the agent self-route at task-execution time without re-reading all sub-skills. The sub-skills return the favor: each has a terse "See also" block listing the neighbors they border in the escalation chain.

### R08 — Patterns over theory

`firecrawl-cli` teaches the escalation decision as a numbered workflow plus a lookup table — no prose explanation of when to use each command:

> Real quote from `skills/firecrawl-cli/SKILL.md:50-70`:
>
> ```
> Follow this escalation pattern:
>
> 1. **Search** - No specific URL yet. Find pages, answer questions, discover sources.
> 2. **Scrape** - Have a URL. Extract its content directly.
> 3. **Map + Scrape** - Large site or need a specific subpage. Use `map --search` to find the right URL, then scrape it.
> 4. **Crawl** - Need bulk content from an entire site section (e.g., all /docs/).
> 5. **Monitor** - Need recurring checks or ongoing alerts.
> 6. **Interact** - Scrape first, then interact with the page (pagination, modals, form submissions, multi-step navigation).
>
> | Need                        | Command               | When                                                      |
> | --------------------------- | --------------------- | --------------------------------------------------------- |
> | Find pages on a topic       | `search`              | No specific URL yet                                       |
> | Get a page's content        | `scrape`              | Have a URL, page is static or JS-rendered                 |
> | Find URLs within a site     | `map`                 | Need to locate a specific subpage                         |
> | Bulk extract a site section | `crawl`               | Need many pages (e.g., all /docs/)                        |
> | AI-powered data extraction  | `agent`               | Need structured data from complex sites                   |
> | Interact with a page        | `scrape` + `interact` | Content requires clicks, form fills, pagination, or login |
> ```

The numbered list gives the agent ordering (try search before scrape); the table gives the same information as a lookup (what does the user need → which command). Having both means the agent can orient by narrative position or by random-access lookup. The monitor section extends this with a worked goal-writing algorithm — five concrete before/after examples rather than a description of what a good goal looks like.

### R21 — Bold imperative + rationale in rules files

`skills/firecrawl-cli/rules/security.md` uses a bulleted list of imperatives, each followed by the rationale for why the constraint exists:

> Real quote from `skills/firecrawl-cli/rules/security.md:13-20`:
>
> ```
> - **File-based output isolation**: All commands use `-o` to write results to `.firecrawl/` files rather than returning content directly into the agent's context window. This avoids overflowing the context with large web pages.
> - **Incremental reading**: Never read entire output files at once. Use `grep`, `head`, or offset-based reads to inspect only the relevant portions, limiting exposure to injected content.
> - **Gitignored output**: `.firecrawl/` is added to `.gitignore` so fetched content is never committed to version control.
> - **User-initiated only**: All web fetching is triggered by explicit user requests. No background or automatic fetching occurs.
> - **URL quoting**: Always quote URLs in shell commands to prevent command injection.
> ```

Each bullet names what to do (bold label), then states why in one clause. The pattern is not "don't do X" but "do Y because Z" — positive framing (R03) and imperative form (R21) together. The rationale is concrete ("avoid overflowing the context", "prevent command injection") rather than generic ("for security").

## Worth adopting

**Pattern: Negative trigger in skill description.** Evidence: `skills/firecrawl-cli/SKILL.md:4` ("Do NOT trigger for local file operations, git commands, deployments, or code editing tasks."). Why it would be a useful rule: R04 requires positive trigger phrases but does not address disambiguation. When a skill competes with built-in Claude tools or adjacent skills for similar user phrases, an explicit negative exclusion in the description reduces misfires. Candidate rule: "Add a `Do NOT trigger for` clause to descriptions where the skill's trigger overlaps with built-in tools or sibling skills."

**Pattern: Escalation position anchor in sub-skill.** Evidence: `skills/firecrawl-scrape/SKILL.md:18` ("Step 2 in the [workflow escalation pattern](firecrawl-cli): search → **scrape** → map → crawl → interact"). Why it would be a useful rule: when a plugin defines a shared execution order across multiple skills, each sub-skill can declare its step number and link to the master. This tells the agent both where it sits and what comes before and after without loading the master skill. Candidate rule: "In multi-skill plugins with a shared escalation pattern, each sub-skill should state its step position and link to the master skill's workflow section."
