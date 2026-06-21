---
slug: quant-sentiment-ai-claude-equity-research
repo: quant-sentiment-ai/claude-equity-research
audited: 2026-06-21
commit_sha: 95130e5d9e410d879112644dc654c44428677e0f
score: 92
exemplifies:
  - R16
  - R18
  - R40
  - R43
---

# Exemplar: quant-sentiment-ai/claude-equity-research

**Score**: 92/100  |  **Date**: 2026-06-21  |  **Commit**: `95130e5d9e410d879112644dc654c44428677e0f`

A single Claude Code command plugin delivering equity research reports; exemplary for its exact output template, explicit parallel-search instruction, and clean five-layer prompt structure.

## Per-rule evidence

### R16 — Define output format

The command does not say "generate a research report" — it gives an exact template with labeled sections, placeholder syntax, and a closing summary table. The eight sections are named, each contains the precise text structure Claude must fill in, and the template itself appears verbatim inside the command body so there is no ambiguity about what the output looks like.

> Real quote from `commands/trading-ideas/commands/research.md:28-47`:
>
> ```
> # **$ARGUMENTS - ENHANCED EQUITY RESEARCH**
>
> ## EXECUTIVE SUMMARY
> **[BUY/SELL/HOLD]** with $[X] price target ([X]% upside/downside) over [timeframe]. [Key catalyst and investment thesis in 1-2 sentences]. [Risk-reward ratio description].
>
> ## FUNDAMENTAL ANALYSIS
> **Recent Financial Metrics**: [Specific revenue growth %, margins, key business KPIs with exact numbers and timeframes]
>
> **Peer Comparison**: [Valuation multiples vs competitors with specific P/E, P/S ratios and company names]
>
> **Forward Outlook**: [Management guidance, analyst consensus, growth projections with specific numbers]
>
> ## CATALYST ANALYSIS
> **Near-term (0-6 months)**: [Specific upcoming events with dates - earnings, product launches, regulatory decisions]
> **Medium-term (6-24 months)**: [Strategic initiatives, market expansion, competitive positioning changes]
> **Event-driven**: [M&A potential, index inclusion, spin-offs, special dividends]
>
> ## VALUATION & PRICE TARGETS
> Current consensus: $[X] (range $[low]-$[high]). Bull case $[X] assumes [specific scenario]. Base case $[X] reflects [scenario]. Bear case $[X] on [risk scenario]. Probability weighting: [X]%/[Y]%/[Z]%.
> ```

Each placeholder calls out specifically what must go there (dollar amounts, specific percentages, firm names), making "I need more data" the only legitimate reason a section stays empty — not ambiguity about what to write.

### R18 — `argument-hint` when command takes input

The frontmatter includes `argument-hint` showing both the required positional argument and the optional flag, so users see the usage pattern in `/help` without reading the full command body.

> Real quote from `commands/trading-ideas/commands/research.md:3`:
>
> ```
> argument-hint: [TICKER] [--detailed]
> ```

Convention is the bracket notation: `[required]` for required args, `[--flag]` for options. The hint fits in one line and covers both invocation forms.

### R40 — Five layers in order

The command opens with a role declaration, then narrows to the task (research framework), then specifies the exact output format (the template), then closes with quality constraints (QUALITY STANDARDS). The five-layer stack is auditable from the file structure alone.

> Real quote from `commands/trading-ideas/commands/research.md:7-14`:
>
> ```
> You are a professional equity research analyst providing institutional-grade trading analysis. When given a stock ticker, conduct comprehensive research and analysis using this exact framework:
>
> ## RESEARCH METHODOLOGY
>
> ### Required Search Strategy (Execute in Parallel):
> 1. **Financial Performance**: Search for recent earnings, revenue growth, margins, key business metrics, and analyst coverage
> 2. **Market Positioning**: Search for peer comparisons, sector performance, competitive analysis, and market share data
> 3. **Advanced Intelligence**: Search for technical analysis, options flow, insider activity, institutional ownership, and regulatory concerns
> ```

Role and task land in the first two sentences; the remaining body is template then constraints. The QUALITY STANDARDS section appended after the output template reinforces specific numeric expectations ("All financial metrics must include specific numbers and percentages") that the template placeholders imply but do not enforce by themselves.

### R43 — Parallel when independent

The search strategy is labeled "Execute in Parallel" and splits into three independent dimensions — financial, market, intelligence — each scoped to distinct data sources. The instruction is explicit rather than leaving Claude to decide whether searches can overlap.

> Real quote from `commands/trading-ideas/commands/research.md:11-14`:
>
> ```
> ### Required Search Strategy (Execute in Parallel):
> 1. **Financial Performance**: Search for recent earnings, revenue growth, margins, key business metrics, and analyst coverage
> 2. **Market Positioning**: Search for peer comparisons, sector performance, competitive analysis, and market share data
> 3. **Advanced Intelligence**: Search for technical analysis, options flow, insider activity, institutional ownership, and regulatory concerns
> ```

Without the "(Execute in Parallel)" annotation, an LLM that serializes by default will take three times as long and may run out of context budget before reaching later searches. Naming the pattern in the heading forces the behavior without relying on the model to infer it.

## Worth adopting

**Pattern: Closing summary table after an output template.** Evidence: `commands/trading-ideas/commands/research.md:64-76` — after the 8-section narrative template, the command appends a `| Metric | Value |` table that distills the six decision-critical fields (Rating, Conviction, Price Target, Timeframe, Upside/Downside, Position Size) into a scannable block. This separates "full analysis prose" from "the number the user actually needs to act." Why it would be a useful rule: when a command produces a multi-section report, a final summary table prevents the key decision metric from being buried in the last paragraph of a long output. Candidate: "**R-proposal. Append a decision table when command output exceeds four sections.** Distill the action-relevant fields into a final `| Key | Value |` table. Prevents key outputs from being buried in prose."
