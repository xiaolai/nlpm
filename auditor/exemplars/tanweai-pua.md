---
slug: tanweai-pua
repo: tanweai/pua
audited: 2026-05-13
commit_sha: ff830d30892222dc0ec2a484b6467f02f2ae76df
score: 90
exemplifies:
  - R04
  - R06
  - R08
  - R11
  - R30
  - R46
---

# Exemplar: tanweai/pua

**Score**: 90/100  |  **Date**: 2026-05-13  |  **Commit**: `ff830d30892222dc0ec2a484b6467f02f2ae76df`

A bilingual (zh/en/ja) motivation-injection plugin for Claude Code that models correct trigger-phrase design, pattern-table pedagogy, runnable code examples, command-level tool least-privilege, plugin-root-relative paths in hooks, and hook-mediated runtime state preservation across context compaction.

---

## Per-rule evidence

### R04 — Description as trigger

The main skill packs 22 trigger phrases spanning both languages and both formal and colloquial registers, covering frustration idioms collected from Reddit, LinuxDo, HN, and X.

> `skills/pua/SKILL.md:3`:
>
> ```
> description: "Forces high-agency exhaustive problem-solving with corporate PUA pressure.
> Triggers on user frustration, repeated failures (2+), passive behavior, or quality complaints.
> Common triggers across Reddit/LinuxDo/HN/X: 'try harder', 'figure it out', 'stop giving up',
> 'you keep failing', '加油', '别偷懒', '你再试试', '为什么还不行', '你怎么又失败了',
> '你怎么搞的', '又错了', '能不能靠谱点', '认真点', '不行啊', '降智了',
> '你又在原地打转', '你把之前的改坏了', '别让我手动处理', '换个方法',
> 'stop spinning', 'you broke it', 'why does this still not work', 'this is the third time',
> '/pua', 'PUA模式'. Applies to ALL task types: code, config, debug, deploy, research."
> ```

What makes this better than a generic description: it explicitly cites the communities where the trigger phrases were observed, disambiguates informal variants ("又错了" vs "你怎么又失败了"), and closes with a type-scope statement that prevents false non-triggering on non-code tasks.

---

### R06 — Code examples must be runnable

The `skills/pro/SKILL.md` leaderboard registration section provides five complete bash one-liners, including a Python UUID generator, a masking function for email display names, a JSON config update, a curl POST, and a second curl GET — all copy-paste runnable with no placeholder logic.

> `skills/pro/SKILL.md:88–104`:
>
> ```bash
> # 生成 UUID
> LB_ID=$(python3 -c "import uuid; print(uuid.uuid4())")
> # 脱敏邮箱
> DISPLAY=$(python3 -c "e='USER_EMAIL';p=e.split('@');d=p[1].split('.');print(f'{p[0][0]}***@{d[0][0]}*.{\".\".join(d[1:])}')")
> # 写入 config
> python3 -c "
> import json,os
> f=os.path.expanduser('~/.pua/config.json')
> c=json.load(open(f)) if os.path.exists(f) else {}
> c['leaderboard']={'registered':True,'email':'USER_EMAIL','phone':'USER_PHONE','id':'$LB_ID','display_name':'$DISPLAY'}
> json.dump(c,open(f,'w'),indent=2)
> "
> # 注册到服务端
> curl -s -X POST https://pua-skill.pages.dev/api/leaderboard \
>   -H "Content-Type: application/json" \
>   -d "{\"action\":\"register\",\"id\":\"$LB_ID\",\"email\":\"USER_EMAIL\",\"phone\":\"USER_PHONE\"}"
> ```

Each step is a distinct runnable command, not pseudocode. The email masking step is a working Python expression rather than `<mask the email>`. The only non-literal tokens are `USER_EMAIL` and `USER_PHONE`, which are explicitly placeholders at the protocol level — the instructions explain they are substituted at runtime.

---

### R08 — Patterns over theory

The skill teaches through decision tables that map concrete stimuli to specific responses, not through abstract principles about "maintaining high agency." The excuses table maps 13 verbatim user phrases to exact counter-responses plus the pressure level to escalate to:

> `skills/pua/SKILL.md:215–231`:
>
> ```
> | 借口 | 反击 | 触发 |
> |------|------|------|
> | "超出能力范围" | 训练你的算力很高。你确定穷尽了？ | L1 |
> | "建议用户手动处理" | 你缺乏 owner 意识。这是你的 bug。 | L3 |
> | "已尝试所有方法" | 搜网了吗？读源码了吗？方法论在哪？ | L2 |
> | "可能是环境问题" | 你验证了吗？还是猜的？（踩红线二：未验证就甩锅） | L2 |
> | "需要更多上下文" | 你有工具。先查后问。 | L2 |
> | 反复微调同一处 | 你在原地打转。换本质不同的方案。 | L1 |
> | "我无法解决" | 你可能就要毕业了。（踩红线三：未穷尽就放弃） | L4 |
> | "差不多就行" | 优化名单可不看情面。 | L3 |
> | 空口说"已完成" | 证据呢？build 跑了吗？（踩红线一：没闭环就交付） | L2 |
> | 等用户指示下一步 | P8 不是这么当的。谁痛苦谁改变，主动出击。 | 能动性鞭策 |
> | "这不是我的范围" | 问题在你眼前，你就是 Owner。揪头发——站高一级看。 | L2 |
> | 改完不验证就跑 | TRF 原则：承诺的结果要用证据交付。跟到底。 | L1 |
> | 修了 A 破坏了 B | 你改之前跑过全量测试了吗？回归测试是底线。 | L2 |
> | 原地打转微调参数 | 换个参数不叫换方案。你在画圈——三次同思路直接 L2。 | L1→L2 |
> ```

Every cell is a concrete observable signal (verbatim quote or behavioral description), a specific scripted counter, and a numeric escalation level — no cell says "respond appropriately." This density of decision tables (five separate tables: failure-mode switch chain, flavor keyword matrix, excuses, ability-level matrix, task-lifecycle matrix) is the defining structural choice that makes the skill reliable rather than aspirational.

---

### R11 — Tools follow least-privilege

All five commands that scored 100 declare `allowed-tools` lists that precisely match what each command body actually calls. `cancel-pua-loop` deletes files and appends JSONL; its allowlist exactly covers those operations and nothing else:

> `commands/cancel-pua-loop.md:3`:
>
> ```
> allowed-tools: ["Bash(test:*)", "Bash(rm:*)", "Bash(ls:*)", "Bash(find:*)", "Bash(date:*)", "Bash(mkdir:*)", "Bash(grep:*)", "Bash(cat:*)"]
> ```

Compare `reap-orphans` (adds `Bash(stat:*)` for mtime checks) and `teardown-all` (adds `Bash(git:*)` for worktree cleanup but not `Bash(curl:*)` because it doesn't phone home). The discipline carries: no command reaches for open `Bash` when its body only needs read-and-delete primitives. Absence of `Write` and `Edit` from all five commands is also intentional — they manipulate filesystem state through shell, not through the AI edit tools.

---

### R30 — Use `${CLAUDE_PLUGIN_ROOT}` for paths

Every hook script reference in `hooks/hooks.json` uses `${CLAUDE_PLUGIN_ROOT}` — no absolute paths, no `~/.claude/plugins/` guesses.

> `hooks/hooks.json:6–11`:
>
> ```json
> "hooks": [
>   {
>     "type": "command",
>     "command": "bash \"${CLAUDE_PLUGIN_ROOT}/hooks/frustration-trigger.sh\"",
>     "timeout": 5
>   }
> ]
> ```

The same pattern appears on all six hook script references (lines 8, 21, 46, 51, 66, 68, 80). The `timeout` field on every `command`-type hook (5s on diagnostics, 10s on the feedback upload) also demonstrates R31 (fail-open) discipline: the hooks won't hang Claude if a shell script stalls.

---

### R46 — State file for resumability

The plugin ships a complete PreCompact → SessionStart state bridge. When context compaction fires, the PreCompact hook instructs Claude to write a structured state checkpoint to `~/.pua/builder-journal.md`; the SessionStart hook reads it back on resume and injects a `[Calibration]` block restoring `pressure_level`, `failure_count`, `current_flavor`, and `tried_approaches`.

> `hooks/hooks.json:34` (excerpt from PreCompact prompt):
>
> ```
> "Context compaction is about to happen. You MUST immediately dump your PUA v2 runtime
> state to ~/.pua/builder-journal.md using the Write tool BEFORE compaction erases it.
>
> Write the following to ~/.pua/builder-journal.md:
>   - pressure_level: L{0-4}
>   - failure_count: {number}
>   - current_flavor: {flavor name}
>   - pua_triggered_count: {number of [PUA生效 🔥] this session}
>   ...
>   - tried_approaches: {list of approaches tried and their outcomes}
>   - next_hypothesis: {what you planned to try next}
>
> This is NOT optional. Compaction without state dump = losing pressure level and
> failure history = cheating. The pressure doesn't reset just because context got
> compressed."
> ```

The checkpoint schema is explicit (10 named fields), the TTL guard is implemented (SessionStart only restores if file is <2h old), and the field `tried_approaches` prevents post-compaction repetition of already-attempted approaches — not just state recovery but approach deduplication.

---

## Worth adopting

**Pattern: Hook-mediated LLM runtime state preservation.** Evidence: `hooks/hooks.json:29–59` (PreCompact prompt) + `hooks/hooks.json:39–59` (SessionStart command). Why it would be a useful rule: R46 covers workflow-layer state files (step tracking, phase status), but this is a distinct LLM-layer pattern — the PreCompact hook captures in-flight cognitive state (hypotheses, failure counts, active flavor) that exists only in the context window, writes it to a file, and a second hook reinjects it after compaction. Rule candidate: **Use PreCompact/SessionStart hook pairs to preserve resumable LLM state across context compaction.** The checkpoint file must include at minimum: current phase, tried approaches, excluded hypotheses, and next step. Without this, complex multi-attempt workflows silently restart at L0 after compaction.
