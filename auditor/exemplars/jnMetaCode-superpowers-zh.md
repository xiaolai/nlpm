---
slug: jnMetaCode-superpowers-zh
repo: jnMetaCode/superpowers-zh
audited: 2026-05-13
commit_sha: 9a8d4e471ef178089c133118f64571f66a11ec33
score: 95
exemplifies:
  - R04
  - R06
  - R07
  - R08
  - R27
  - R30
---

# Exemplar: jnMetaCode/superpowers-zh

**Score**: 95/100  |  **Date**: 2026-05-13  |  **Commit**: `9a8d4e471ef178089c133118f64571f66a11ec33`

A Chinese-language skill collection (20 of 24 NL artifacts score 100/100) demonstrating how to write trigger-oriented descriptions, pattern-dense bodies, and cross-skill scope notes — in a non-English codebase where vague language would be even harder to detect.

## Per-rule evidence

### R04 — Description as trigger

The collection uses description fields that read as invocation conditions, not capability summaries. Three distinct strategies are visible:

**Multi-clause trigger** (`skills/brainstorming/SKILL.md:3`):

> ```
> description: "在任何创造性工作之前必须使用此技能——创建功能、构建组件、添加功能或修改行为。在实现之前先探索用户意图、需求和设计。"
> ```

Five trigger conditions in one sentence. "Creating features, building components, adding functionality, or modifying behavior — before implementation" makes the invocation window unambiguous.

**Symptom-plus-guard** (`skills/chinese-code-review/SKILL.md:3-4`):

> ```
> description: 中文 review 沟通参考——话术模板、分级标注（必须修复/建议修改/仅供参考）、国内团队常见反模式应对。仅在用户显式 /chinese-code-review 时调用，不要根据上下文自动触发。
> ```

Embeds an explicit non-auto-trigger guard directly in the description — preventing the skill from firing on every Chinese-language session. Only skill in the collection that does this; it's the right call for a domain-specific tool that would create noise if context-triggered.

**Boundary-defined trigger** (`skills/verification-before-completion/SKILL.md:3`):

> ```
> description: 在宣称工作完成、已修复或测试通过之前使用，在提交或创建 PR 之前——必须运行验证命令并确认输出后才能声称成功；始终用证据支撑断言
> ```

Names the exact moment of invocation ("before claiming done, before commit, before PR") rather than the skill's subject matter. Claude hits the boundary condition before it acts, not after.

### R06 — Runnable examples

Examples throughout this collection are concrete invocations, not pseudocode stubs.

`skills/dispatching-parallel-agents/SKILL.md:68-74`:

> ```typescript
> // 在 Claude Code / AI 环境中
> Task("修复 agent-tool-abort.test.ts 的失败")
> Task("修复 batch-completion-behavior.test.ts 的失败")
> Task("修复 tool-approval-race-conditions.test.ts 的失败")
> // 三个任务并发运行
> ```

Real file names, real test names. An agent adapting this knows exactly what to substitute.

The agent-prompt template in the same file (`skills/dispatching-parallel-agents/SKILL.md:92-110`) goes further — it's a fully-filled markdown block showing actual test failure messages and numbered fix instructions, not a `<fill in here>` skeleton.

`skills/finishing-a-development-branch/SKILL.md:46-48` shows real bash for detecting worktree state:

> ```bash
> GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
> GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
> ```

The 2>/dev/null error redirect and the `&&pwd -P` flag are not placeholders — the example is copy-paste ready.

### R07 — Scope note when related skills exist

Every skill that has a counterpart explicitly names the boundary.

`skills/subagent-driven-development/SKILL.md:34-39` opens with a direct comparison rather than letting the agent discover the distinction at invocation time:

> ```
> **与 Executing Plans（并行会话）的对比：**
> - 同一会话（无上下文切换）
> - 每个任务全新子智能体（无上下文污染）
> - 每个任务后两阶段审查：先规格合规性，再代码质量
> - 更快的迭代（任务间无需人工介入）
> ```

This collapses ambiguity at the moment of loading, not after an agent has already started the wrong workflow.

`skills/brainstorming/SKILL.md:66` names the exact terminal state and excludes alternatives by name:

> ```
> **终止状态是调用 writing-plans。** 不要调用 frontend-design、mcp-builder 或任何其他实现技能。头脑风暴之后你唯一要调用的技能是 writing-plans。
> ```

Naming the wrong choices prevents the agent from rationalizing "this seems like an implementation skill" as acceptable.

`skills/finishing-a-development-branch/SKILL.md:268-276` closes with a bidirectional integration map — which skills call it, which skills it works alongside — so an agent loading it can resolve the calling graph without searching:

> ```
> **被以下技能调用：**
> - **subagent-driven-development**（步骤 7）- 所有任务完成后
> - **executing-plans**（步骤 5）- 所有批次完成后
>
> **配合使用：**
> - **using-git-worktrees** - 清理由该技能创建的工作树
> ```

### R08 — Patterns over theory

The collection consistently teaches by contrast table rather than prose principle.

`skills/dispatching-parallel-agents/SKILL.md:114-124` — four "wrong vs right" pairs, each scoped to a specific mistake:

> ```
> **错误做法：太宽泛：** "修复所有测试" - 智能体会迷失方向
> **正确做法：具体明确：** "修复 agent-tool-abort.test.ts" - 聚焦的范围
>
> **错误做法：无上下文：** "修复竞态条件" - 智能体不知道在哪里
> **正确做法：提供上下文：** 粘贴错误信息和测试名称
> ```

Each pair encodes the failure mode and its fix in the same breath. An agent reading this has a decision procedure, not a principle to reinterpret.

`skills/verification-before-completion/SKILL.md:44-48` uses a three-column table (claim → what's required → what doesn't qualify) that eliminates rationalization surface:

> ```
> | 结论 | 需要 | 不够格 |
> |------|------|--------|
> | 测试通过 | 测试命令输出：0 failures | 之前的运行结果、"应该会通过" |
> | Linter 无报错 | Linter 输出：0 errors | 部分检查、推断 |
> | 构建成功 | 构建命令：exit 0 | linter 通过、日志看起来没问题 |
> ```

The third column names the specific substitution the agent is likely to reach for, then disqualifies it explicitly.

`skills/verification-before-completion/SKILL.md:65-75` adds a rationalization counter-table — each borrowed excuse mapped to a one-line refusal:

> ```
> | 借口 | 现实 |
> |------|------|
> | "应该能行了" | 运行验证命令 |
> | "我有信心" | 信心 ≠ 证据 |
> | "就这一次" | 没有例外 |
> ```

This pattern (rationalization → flat denial) appears in at least four skills in this collection. It's the primary enforcement mechanism for discipline-type skills.

### R27 — Event names are case-sensitive

`hooks/hooks.json:3` uses correct PascalCase:

> ```json
> "hooks": {
>   "SessionStart": [
> ```

`SessionStart` not `sessionstart` or `session-start`. With multiple hook event names in the Claude Code spec, this is a common failure point. The file is clean.

### R30 — Use `${CLAUDE_PLUGIN_ROOT}` for paths

`hooks/hooks.json:8` references the hook script via the plugin-root variable, not a hardcoded path:

> ```json
> "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" session-start"
> ```

The outer quotes handle spaces in the path. The inner `${CLAUDE_PLUGIN_ROOT}` ensures portability across install locations. Both layers are present.

## Worth adopting

**Pattern: Explicit subagent-context gate sentinel.** `skills/using-superpowers/SKILL.md:6-8` opens with:

```
<SUBAGENT-STOP>
如果你是作为子智能体被分派来执行特定任务的，跳过此技能。
</SUBAGENT-STOP>
```

Bootstrap skills that load at session start should not run inside subagents that have a narrow task scope. Without this sentinel, the bootstrap overhead fires on every `Task()` dispatch. This is not codified in R04–R08 or anywhere in the 50 Rules. Candidate rule: **When a skill is intended for session-level orchestration only, open the body with an explicit subagent-stop sentinel to prevent loading by task-scoped subagents.** Evidence: `skills/using-superpowers/SKILL.md:6-8`. Why it would be a useful rule: bootstrap skills often contain skill-routing instructions that actively mislead a subagent about its own task scope, wasting tokens and potentially overriding its injected instructions.
