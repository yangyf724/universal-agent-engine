# Compose Handoff — 与 compose-next 的三角色互补

engine 是 compose-next 的**能力同伴**，不是它的子流程。同任务仍只加载一个编排层。

## 何时用哪一角色

| 角色 | 信号 | 你交付什么 | 你不做什么 |
|---|---|---|---|
| **R1 前置输入** | 用户要调研/选项/方案/验收草案，且下一步明显进 git 仓实现/合并/规格；或明说「喂给 / 帮我准备 compose-next」 | **compose-ready 包**（下节模板） | 不写 feature Spec；不建 worktree；不跑 Finish/独立 Review |
| **R2 能力补位** | 主产物是多模态/Office/媒体/交互，或非 git 的研究/方案/写作/答疑 | 正常 D1+D2 产物 + Lean Gates | 不接管 git feature；不在 compose-next 运行中再加载本协议 |
| **R3 拒绝回退** | 「直接修 / 不用 compose-next / without spec」或非 P 多步 | 轻量 BUILD/FIX 等 | 不强制补 Spec/Review |

## R1 判定（满足任一才走）

1. 用户点名要把结果用于 compose-next / Grill / Spec。
2. 未点名，但**同时**出现：git 仓语境 + 「要合并/发版/规格」意图 + 先要「调研/对比/选项/验收草案」。
3. 仅「改代码且要合并」、无前置输入需求 → **不要** R1；一句建议 `/compose-next …`。

## compose-ready 包模板

结构固定、可整段粘贴进 compose-next 的 Grill/Spec 作为**输入**，不是 feature 文档（无 status/commits/branch）：

```markdown
## Compose-ready Pack
### Problem
一句话用户可见问题（不是任务清单）。
### Constraints / Non-goals
硬约束；明确不做什么。
### Options + Recommendation
2–3 条可行路径（做法/代价/风险）+ 推荐一条与主要取舍。
### Acceptance draft
可观察验收 3–5 条（结果|如何验证|证据形态）。
### Open questions for Grill
仍需用户拍板的 1–3 问。
### Evidence / Sources
来源或工具证据指针；单源须标注。
```

## 交付纪律

- 包内关键结论仍过 Lean Gates：有证据；未验区 1 句掩码；禁止把猜测写成推荐依据。
- 交付包后**再**建议用户 `/compose-next …`；用户未确认前不进 feature 工作流。
- 已在 compose-next 会话中 → 不加载本 skill 全协议（compose-next 无内部 skill hand-off）。
- 单文件 Office/PDF 成稿 → official；GitHub 建仓/同步 → github-sync。

## 反例

| 错误 | 纠正 |
|---|---|
| 把 compose-ready 包写成 `docs/compose/spec/*.md` feature 文档 | 包只是输入；Spec 归属 compose-next |
| 用户只要「修 bug 并合并」却先做长调研 | 建议 `/compose-next`，不默认 R1 |
| compose-next 执行中双载 engine 全协议 | 只走 compose-next |
| 用 R1 回避 worktree/Review | 这些能力 engine 永不提供 |
