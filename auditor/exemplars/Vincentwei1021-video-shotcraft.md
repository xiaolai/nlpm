---
slug: Vincentwei1021-video-shotcraft
repo: Vincentwei1021/video-shotcraft
audited: 2026-08-07
commit_sha: 0022ec45d28800cecb5b16624a3179093c93f4e9
score: 100
exemplifies:
  - R04
  - R05
  - R06
  - R01
  - R08
---

# Exemplar: Vincentwei1021/video-shotcraft

**Score**: 100/100  |  **Date**: 2026-08-07  |  **Commit**: `0022ec45d28800cecb5b16624a3179093c93f4e9`

A bilingual (English/Chinese) Claude Code skill that turns a frontend project into a Remotion-rendered product video from a 104-card shot-recipe library; notable for a lean top-level `SKILL.md` that routes to large reference files by trigger condition, and shot cards whose numeric parameters are backed by real, runnable demo TSX.

## Per-rule evidence

### R04 — Description as trigger

The frontmatter `description` packs four distinct, quotable trigger phrases into one field instead of a generic feature summary — each maps to a different mode of the skill (full promo via template, full promo via freeform creation, naming the reference template by name, or pulling a single shot card).

> Real quote from `SKILL.md:3`:
>
> ```
> description: Create cinematic product videos from shot recipe cards, a validated template, and code/audio assets (Remotion + real page screenshots + 2.5D camera moves + beat-synced cuts + sound design). Use when the user asks to turn a frontend project or webpage into a product video, says "use video-shotcraft to make a video/promo", names the Ink Press template or asks to reproduce its effect, or wants a single shot card's motion.
> ```

The trigger phrases are literal enough to match real user requests ("use video-shotcraft to make a video/promo", "names the Ink Press template") rather than restating what the skill *is* — the difference between a trigger and a summary.

### R05 — Under 500 lines, split with cross-references

`SKILL.md` itself is 205 lines. The heavy content — six-stage pipeline, aesthetic rules, sound design, music-beat-sync methodology — lives in separate `references/*.md` files (`pipeline.md` at 23,986 bytes, `aesthetic-rules.md` at 24,507 bytes, `sound-design.md` at 23,650 bytes) that `SKILL.md` never inlines. A routing table tells Claude exactly which file to read for which situation instead of loading everything up front.

> Real quote from `SKILL.md:166-178` (`## 何时读哪个文件` — "when to read which file"):
>
> ```
> | 时机 | 读 |
> |------|----|
> | 项目启动且模式未定 | 最小只读检查，然后提供三种完整宣传片模式并推荐 |
> | 自主自由创作 | pipeline.md（Agent 自主完成阶段 0–7，不逐阶段等待确认） |
> | 共同创作 | guided-free-creation.md（确认阶段 0–3），再从 pipeline.md 阶段 4 继续 |
> | 用户已选 BGM | music-beat-sync.md（先分析再分镜） |
> | 走模板路线 | template/TEMPLATE.md 全文 |
> | 分镜设计 | sequences/ 桥段模板（全片骨架先填空）；shots/ 全部 frontmatter；选中的卡读全文 |
> | 逐镜头实现 | 该镜头卡全文 + 按"参考实现"定位的准确 demo 源码全文 + assets/lib/ 对应组件 |
> | 声音设计 | sound-design.md + assets/audio/ |
> | 验收 | final-review.md + aesthetic-rules.md 全文过 checklist（独立 subagent 执行） |
> ```

This is the difference between a skill that grows to 500+ lines because everything is inlined, and one that stays under budget because each reference file is loaded conditionally, only when its trigger condition is met.

### R06 — Code examples must be runnable

Each of the 104 shot-recipe cards under `references/shots/` cites a "参考实现" (reference implementation) pointing at real, runnable Remotion TSX under `demos/`, not pseudocode. The numeric parameters in the card's own parameter table match the literal constants in the cited demo file.

> Real quote from `references/shots/camera/crash-zoom-punch.md:23-29` (parameter table):
>
> ```
> | 参数 | 典型值 | 调节手感 |
> |------|--------|----------|
> | 急推时长 | 6f（4–8f） | >10f 读作普通推近，冲击感消失 |
> | 目标 zoom | 2.4–2.8 | 终点构图以目标卡占画面 60–75% 为准 |
> | 回弹幅度 | zoom 的 3–6% | 过大读作弹簧玩具 |
> ```

> Real quote from `demos/camera/crash-zoom-punch/CrashZoomReal.tsx:17-20`:
>
> ```
> const zoom = interpolate(frame, [40, 46, 51], [1, 2.6, 2.45], {
>     extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
>     easing: Easing.bezier(0.55, 0, 0.7, 1),
>   });
> ```

The card's "6f duration, 2.4–2.8 target zoom" is not aspirational prose — `[40, 46]` is a literal 6-frame span and `2.6` sits inside the stated 2.4–2.8 range. An agent implementing this shot copies calibrated code instead of re-deriving easing curves from a text description.

### R01 — No vague quantifiers without criteria

Where a weaker skill would write "hold briefly" or "keep the zoom subtle," this repo states frame counts, thresholds, and percentages throughout, including in the top-level aesthetic principles, not just the per-card parameter tables.

> Real quote from `SKILL.md:119-123` (principle 4, on pacing):
>
> ```
> 4. 每个镜头只讲一个动效；关键信息落定后必须呼吸。
>    一种动画手法（飞入/堆叠/翻页）全片只当一次主角，重复镜头、重复
>    tagline 一律删。节奏偏好是单向的：历史反馈全部指向"放慢/停留"，
>    从未有一次"太慢了"——品牌字标落定 hold ≥1s、批量动效收尾留 0.5s
>    静止、开场主体动作给足 3s。排时间线时预先给 hold/rest 留帧预算。
> ```

"品牌字标落定 hold ≥1s" (brand mark hold ≥1s) and "批量动效收尾留 0.5s 静止" (0.5s static after batch motion) are measurable criteria an agent can act on directly; "hold appropriately" would not be.

### R08 — Patterns over theory

Principle 4 above isn't a general animation-theory statement about pacing — it's a specific, falsifiable claim ("historically feedback always points toward slowing down, never once toward 'too slow'") that resolves into a concrete situational rule with numbers attached. The same style repeats in principle 6 on shot-card reuse.

> Real quote from `SKILL.md:132-138` (principle 6):
>
> ```
> 6. 用镜头卡动效必须先解析 Gallery 索引并读准确的 demo 实现代码。
>    先用 `gallery/api/library.json` 校验卡名与 `style-key`，再按卡片文档的
>    "参考实现"定位具体 TSX。配方卡给的是语义和参数表，准确的 demo 源码
>    才是调校过的参数真相（缓动、时值
>    配比、摘罩时机、已知坑的规避写法）。允许适配性改动，但卡上
>    "已知坑/命门"标注的参数不得降档——质量标准只升不降。凭卡名和
>    理解新写＝放弃全部调校积累。
> ```

Rather than teaching "reuse existing components when possible" as an abstract principle, this tells the agent exactly which file resolves a card name (`gallery/api/library.json`), exactly which section of the card to trust for the real implementation ("参考实现"), and names the specific failure mode of skipping this ("写自己的实现 = 放弃全部调校积累" — writing your own from the card description alone throws away all of the tuning work already captured in the demo file).

## Worth adopting

Pattern: mode-lock exceptions stated as concrete trigger phrases. Evidence: `SKILL.md:47-57` — two explicit "例外" (exception) blocks that name the literal user phrasing that short-circuits the mode-selection question ("用 Ink Press 模板给我的产品做宣传片" skips straight to template mode; naming specific shot-card names locks in a constraint without triggering the full-promo mode question). Why it would be a useful rule: many skills describe a decision tree but leave the "when does the agent skip asking and just act" boundary implicit; stating the exact phrases that satisfy a decision point, not just the decision points themselves, removes an entire class of "why did it ask when I already told it" complaints.
