---
slug: dontbesilent2025-dbskill
repo: dontbesilent2025/dbskill
audited: 2026-05-13
commit_sha: HEAD
score: 90
exemplifies:
  - R04
  - R05
  - R07
  - R08
---

# Exemplar: dontbesilent2025/dbskill

**Score**: 90/100  |  **Date**: 2026-05-13  |  **Commit**: `HEAD`

A 12-skill business-diagnostic suite for Chinese-speaking entrepreneurs, notable for bilingual trigger phrase coverage, a lean router design, and a signal-pattern system that embeds psychological theory as observable behavior templates rather than abstract prose.

## Per-rule evidence

### R04 — Description as trigger

Every skill in this collection packs Chinese and English trigger phrases into the `description` field — not summaries, but verbatim phrases a user would actually type. The result fires the skill from slash-command invocation and natural-language queries in either language.

> Real quote from `skills/dbs-action/SKILL.md:3-7`:
>
> ```
> dontbesilent 执行力诊断。用阿德勒心理学框架诊断你「知道该做什么但就是不做」的真正原因。
> 触发方式：/dbs-action、/action、「我知道该怎么做但就是不做」「为什么我总是拖延」
> Execution block diagnosis using Adlerian psychology framework.
> Trigger: /dbs-action, "I know what to do but can't do it", "why do I procrastinate"
> ```

What makes this strong: the description names the framework (Adlerian psychology), states the symptom in the user's exact words ("知道该做什么但就是不做"), and provides natural-language triggers in both languages across 4 phrases. A description that said "execution skill" would match nothing.

### R05 — Body length

The router (`skills/dbs/SKILL.md`) is 85 lines for 11 routed skills. The deepest diagnostic skill (`skills/dbs-action/SKILL.md`) is 251 lines including a full inline case library. Both stay well under 500. The router achieves this with a three-column table (signal, destination, one-sentence description) and no explanatory prose outside the workflow and edge-case sections.

> Real quote from `skills/dbs/SKILL.md:1-8`:
>
> ```
> ---
> name: dbs
> description: |
>   dontbesilent 商业工具箱主入口。根据你的问题自动路由到最合适的诊断工具。
>   触发方式：/dbs、/商业、「帮我看看」
>   Main entry point for dontbesilent business toolkit. Routes to the right diagnostic skill.
>   Trigger: /dbs, "help me with my business"
> ---
> ```

A router that answers "what does this do?" and "how do I invoke it?" — plus routing table, two-step workflow, and three edge cases — in 85 total lines shows what R05 discipline looks like when applied to an orchestration layer.

### R07 — Scope note when related skills exist

Each deep diagnostic skill ends with a conditional routing table naming exactly which skill to invoke, under which observable condition. This isn't a generic "see also" — it's a decision tree that gives Claude both the judgment criterion and the exact invocation string.

> Real quote from `skills/dbs-action/SKILL.md:196-201`:
>
> ```
> | 触发条件 | 推荐话术 |
> |---|---|
> | 用户想行动，但不知道做什么 | 「回到 `/dbs-diagnosis` 重新看商业模式，或 `/dbs-benchmark` 找个对标。」 |
> | 用户的卡点和商业模式本身有关 | 「执行力没问题，问题在商业模式。用 `/dbs-diagnosis` 看看。」 |
> | 用户做不动是因为目标本身就是空转的（说「我想做有影响力的内容」「想变得更好」这类愿望语法）| 「你做不动不是执行力问题，是目标本身不能驱动行动。先用 `/dbs-goal` 把目标审计成可检查的样子。」 |
> | 用户不是做不动，而是在关键方法选择上总想找更快的路 | 「你卡的不是行动本身，是方法选错了。试试 `/dbs-slowisfast`。」 |
> ```

The scope note fires only after the diagnostic phase, keyed to an observable post-diagnosis user state. This is more useful than an unconditional "see also `/dbs-diagnosis`" because it gives Claude the triggering condition, not just the pointer. Skills also link deep knowledge-base files via a consistent footnote — `> 📚 深度参考：知识库/Skill知识包/action_心理诊断框架.md` — keeping inline content lean while making richer references available on demand.

### R08 — Patterns over theory

The diagnostic skills teach through named signal patterns. Each pattern has a label, observable user phrases, a one-line mechanism, and a one-sentence verdict. Adlerian psychology and other frameworks appear only as the *mechanism explanation* inside a pattern — never as standalone theory sections.

> Real quote from `skills/dbs-action/SKILL.md:64-74`:
>
> ```
> #### 信号 A：执行模拟器
>
> **表现**：用户把所有人和工具都变成「模拟器」——不是在执行，是在模拟执行。
>
> - 「你觉得这个方案怎么样？」（你是他的方案模拟器）
> - 「如果我发给 Claude Code 会怎样？」（你是他的 Claude Code 模拟器）
> - 「你帮我看看这个能不能做」（你是他的市场调研模拟器）
>
> **诊断**：模拟到执行的比例是 1/2000。因为无法承受任何微小的失败风险，所以凡事都要在大脑中进行提前模拟。
>
> **一句话**：你不是在准备执行，你是在用准备替代执行。
> ```

Six signals (A–F) follow this exact three-part template: observable behavior + user-phrase examples → mechanism → one-sentence verdict. Claude can match a user's words to a signal and apply the diagnosis without reasoning from abstract psychological theory. The theory informs the mechanism line; the pattern does the triggering work.

## Worth adopting

Pattern: **Bilingual description block for multilingual skills.** Evidence: `skills/dbs-action/SKILL.md:3-7`, `skills/dbs-content/SKILL.md:3-8`, `skills/dbs-xhs-title/SKILL.md:3-7` — every skill carries Chinese trigger phrases on lines 1–2 of the description and English trigger phrases on lines 3–4. Why it would be a useful rule: R04 requires 3+ specific action phrases but doesn't address skills that serve users in multiple languages; without language-matched trigger phrases, Claude Code will fail to fire a skill from queries written in any language not represented in the `description` field. Candidate rule: **When a skill serves users in more than one language, include trigger phrases in each language in the `description` field.** Matching the user's query language to the description is the triggering mechanism; a Chinese-only description will not fire from English queries and vice versa.
