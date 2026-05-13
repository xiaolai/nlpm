---
slug: lackeyjb-playwright-skill
repo: lackeyjb/playwright-skill
audited: 2026-05-13
commit_sha: bb7e920d376022958214e349ef25498a2644e189
score: 98
exemplifies:
  - R04
  - R05
  - R06
  - R07
  - R08
---

# Exemplar: lackeyjb/playwright-skill

**Score**: 98/100  |  **Date**: 2026-05-13  |  **Commit**: `bb7e920d376022958214e349ef25498a2644e189`

Single-skill Playwright automation plugin; 454 lines, 6 runnable patterns, scope-delegated API reference, and a description that reads like a user's search bar.

## Per-rule evidence

### R04 — Description as trigger

The frontmatter description doesn't describe what Playwright is — it enumerates what a user would type when they want this skill loaded. It packs 8 distinct trigger scenarios into two sentences, mixing imperative capability phrases ("Auto-detects dev servers", "writes clean test scripts") with explicit user-query phrasing ("Use when user wants to test websites…").

> Real quote from `skills/playwright-skill/SKILL.md:3`:
>
> ```
> description: Complete browser automation with Playwright. Auto-detects dev servers, writes
> clean test scripts to /tmp. Test pages, fill forms, take screenshots, check responsive
> design, validate UX, test login flows, check links, automate any browser task. Use when
> user wants to test websites, automate browser interactions, validate web functionality,
> or perform any browser-based testing.
> ```

What makes this strong is the "Use when…" tail: it directly mirrors the retrieval signal Claude sees when deciding which skill to invoke. Most skill descriptions stop at capability; this one closes the retrieval loop.

### R05 — Body length

The file is 454 lines — 46 lines under the 500-line ceiling. The author avoids padding by deferring all advanced API documentation to a companion `API_REFERENCE.md` rather than inlining it. The skill stays dense: every section contains executable code or imperative steps, with no expository filler between them.

> Real quote from `skills/playwright-skill/SKILL.md:372-373`:
>
> ```
> ## Advanced Usage
>
> For comprehensive Playwright API documentation, see [API_REFERENCE.md](API_REFERENCE.md):
> ```

The body-length discipline here is structural, not accidental: the file knows where it ends and where the reference starts.

### R06 — Code examples must be runnable

Six named pattern blocks appear in the "Common Patterns" section, each a complete, self-contained JavaScript file with a shebang-equivalent comment (the `/tmp/playwright-test-*.js` filename comment), real selectors, real assertions, and explicit `browser.close()` calls. A seventh inline-execution example shows the non-file path. Every example targets a distinct scenario rather than varying the same boilerplate.

> Real quote from `skills/playwright-skill/SKILL.md:64-89`:
>
> ```javascript
> // /tmp/playwright-test-page.js
> const { chromium } = require('playwright');
>
> // Parameterized URL (detected or user-provided)
> const TARGET_URL = 'http://localhost:3001'; // <-- Auto-detected or from user
>
> (async () => {
>   const browser = await chromium.launch({ headless: false });
>   const page = await browser.newPage();
>
>   await page.goto(TARGET_URL);
>   console.log('Page loaded:', await page.title());
>
>   await page.screenshot({ path: '/tmp/screenshot.png', fullPage: true });
>   console.log('📸 Screenshot saved to /tmp/screenshot.png');
>
>   await browser.close();
> })();
> ```

The examples are runnable as-is: copy, paste `$SKILL_DIR`, run. The comment `// <-- Auto-detected or from user` marks the one substitution Claude must make, eliminating ambiguity without breaking executability.

### R07 — Scope note when related skills exist

Rather than embedding the full Playwright API reference inline, the skill explicitly names the companion file and lists what lives there, so Claude knows when to follow the pointer rather than guess or hallucinate.

> Real quote from `skills/playwright-skill/SKILL.md:372-382`:
>
> ```
> ## Advanced Usage
>
> For comprehensive Playwright API documentation, see [API_REFERENCE.md](API_REFERENCE.md):
>
> - Selectors & Locators best practices
> - Network interception & API mocking
> - Authentication & session management
> - Visual regression testing
> - Mobile device emulation
> - Performance testing
> - Debugging techniques
> - CI/CD integration
> ```

The bulleted list under the link is the scope note: it tells Claude exactly what `API_REFERENCE.md` covers, so Claude can decide without opening the file whether the current task requires it.

### R08 — Patterns over theory

The "Common Patterns" section names six distinct automation scenarios and provides a complete script for each. There is no introductory theory about what Playwright is or how browser automation works — the file opens with a CRITICAL WORKFLOW block and immediately delegates to concrete steps.

> Real quote from `skills/playwright-skill/SKILL.md:93-118`:
>
> ```javascript
> ### Test a Page (Multiple Viewports)
>
> // /tmp/playwright-test-responsive.js
> const { chromium } = require('playwright');
>
> const TARGET_URL = 'http://localhost:3001'; // Auto-detected
>
> (async () => {
>   const browser = await chromium.launch({ headless: false, slowMo: 100 });
>   const page = await browser.newPage();
>
>   // Desktop test
>   await page.setViewportSize({ width: 1920, height: 1080 });
>   await page.goto(TARGET_URL);
>   console.log('Desktop - Title:', await page.title());
>   await page.screenshot({ path: '/tmp/desktop.png', fullPage: true });
>
>   // Mobile test
>   await page.setViewportSize({ width: 375, height: 667 });
>   await page.screenshot({ path: '/tmp/mobile.png', fullPage: true });
>
>   await browser.close();
> })();
> ```

Six named patterns (page test, login flow, form submit, broken-link check, screenshot with error handling, responsive design) replace any need for Claude to improvise from first principles. The pattern names also match how users phrase requests ("test login", "check broken links", "responsive design").

## Worth adopting

Pattern: **Self-location preamble.** Evidence: `skills/playwright-skill/SKILL.md:6-13`. Why it would be a useful rule: Skills installed via the plugin system, manually to `~/.claude/skills/`, or project-locally have different absolute paths. This skill opens with explicit instructions for Claude to discover the installation path before running any commands, storing it as `$SKILL_DIR`, then uses `$SKILL_DIR` in every subsequent `bash` block. A rule codifying this pattern — "When a skill executes shell commands against its own directory, open with a path-discovery section listing known installation paths and instruct Claude to resolve `$SKILL_DIR` before any execution step" — would prevent all class of 'module not found' errors caused by running from the wrong working directory.
