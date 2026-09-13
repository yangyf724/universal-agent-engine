---
feature: engine-compose-aux
status: in-progress
updated: 2026-09-13
branch: optimize/v1.6-compose-aux
commits: 8aaf352..<head> # filled at delivery
---

# Engine × Compose-next Auxiliary (能力同伴 + 交接物)

## Report

## [S1] Problem

v1.3–v1.5 把互补做成了「负空间」：P-domain 让位、不引入 worktree/Spec/Review/Finish。这降低了冲突，但 engine 仍像 compose-next 的「邻居」，而不是**辅助**——用户进入 compose-next 之前缺调研/选项/验收草案时、或要 compose-next 不管的多模态/Office/媒体交付时，没有一条清晰的「engine 产出 → compose-next 可消费」路径。目标变更为：engine 成为 compose-next **最互补的辅助 skill**（能力同伴 + 交接物），在不双载、不越界的前提下主动补位。

## [S2] Design

### 三角色定位（互补，不删 mode，不引入 compose-next 合同）

| 角色 | 触发 | engine 行为 | 产物 |
|---|---|---|---|
| R1 前置输入 | 用户要调研/选项/方案/验收草案，且下一步明显是 git 仓内实现/合并/规格（或用户明说「喂给 compose-next」） | 走 RESEARCH/DESIGN/WRITE，按交接包模板交付 | **compose-ready 包**（可直接贴进 Grill/Spec） |
| R2 能力补位 | 主产物是多模态/Office/媒体/交互演示，或非 git 的调研/方案/写作 | 正常 D1+D2 路由 + Lean Gates | 媒体/Office/文稿；**不**接管 git feature |
| R3 拒绝回退 | 用户拒绝 compose-next（「直接修 / without spec / 不用 compose-next」）或非 P 多步 | 轻量 BUILD/FIX 等 | 可运行产物 + 证据 |

**边界不变量（硬）：**

1. 点名 `/compose-next` → 只走 compose-next，本 skill 不加载全协议。
2. P-domain 未点名且**无前置输入需求** → 仍一句建议 `/compose-next …`，不进 Step 2–6。
3. P-domain 未点名但**用户先要调研/选项/验收草案** → 走 R1，交付 compose-ready 包后再建议 `/compose-next`（包是输入，不是 feature 文档）。
4. 已在 compose-next 工作流内 → **禁止**再加载本 skill 全协议；compose-next 无内部 skill hand-off。
5. 本 skill **不**实现 worktree / Spec 生命周期 / Finish / 独立 Review。
6. 单文件 Office/PDF 成稿仍委托 official；GitHub 建仓/同步仍 github-sync。

### compose-ready 包合同（R1 交付模板）

结构固定、可粘贴；不是 feature Spec，不写 commits/branch/status：

```markdown
## Compose-ready Pack
### Problem
### Constraints / Non-goals
### Options (2–3) + Recommendation + Tradeoffs
### Acceptance draft (observable)
### Open questions for Grill
### Evidence / Sources
```

细则与字段说明放 `references/compose-handoff.md`；SKILL body 只保留指针 + 一句何时产出。

### D3 路由更新

| 信号 | 行为 |
|---|---|
| 点名 compose-next | 只 compose-next |
| P-domain + 要合并/规格 + 无前置输入 | 建议 compose-next，不进 Step 2–6 |
| P-domain + 先要调研/选项/验收草案（或点名喂 compose-next） | R1 → 产出 compose-ready 包 → 建议 compose-next |
| E-domain（研究/方案本体/写作/Office/媒体/答疑/非 git） | 正常路由（R2） |
| 用户拒绝 compose-next | R3 轻量 BUILD/FIX |
| official / github-sync | 委托（不变） |

### description 重写（本轮允许）

目标：路由面可见「互补辅助」，不抢 compose-next 点名/合并/规格触发。

- **保留**：orchestration protocol、端到端交付、修bug/做方案/调研落地/多模态触发、official 与 chit-chat 负例、compose-next 负例。
- **新增信号（语义，非堆词）**：pre-feature research/option packs；multimodal/office/media；non-git multi-step。
- **禁止进 description**：worktree、spec lifecycle、merge、finish、review process、`/compose-next` 正触发。
- 长度 ≤1024；改后跑完整 `skill_search` 抽检（点名 compose-next / 调研落地 / 转写 / 修bug / 闲聊 / 单文件 PPT）。

### 文件契约

| 文件 | 改动 |
|---|---|
| `skill/SKILL.md` | description 重写；Important 三角色一句；Examples 增 R1；指针 `compose-handoff.md` |
| `skill/references/compose-handoff.md` | **新建**：包模板 + R1/R2/R3 判定 + 禁止项 |
| `skill/references/intent-router.md` | D3 扩为三角色表；P-domain+前置输入路径 |
| `skill/references/quality-gates.md` | Token Discipline：R1 包不是 Spec；compose-next 运行中不双载 |
| `skill/tests/scenarios.md` | S45–S48：R1 前置包、R1 后建议 compose-next、R2 主产物媒体、R3 拒绝回退 |
| `skill/tests/run_static_checks.py` | 断言：三角色、handoff 链接、D3 R1、description 边界词、新场景 |
| `skill/tests/checklist.md` | 期望 pass 数；L3/L4 互补项 |
| `skill/tests/manual-verify.md` | skill_search 抽检表更新 |
| `skill/locales/*.json` | brief 对齐互补辅助（displayName 不变） |
| `README.md` / `CHANGELOG.md` | v1.6.0 定位与变更 |
| **不改** | compose-next 本体；BUILD/FIX；mode 数（仍 7）；worktree/Spec/Review/Finish |

### 环境覆盖

会话隔离拦 `git worktree add`。本 feature 在主检出分支 `optimize/v1.6-compose-aux`（base `8aaf352`），不创建 linked worktree。双安装同步仍执行。

## [S3] Out of Scope

- 修改 compose-next 技能或 description。
- 在 compose-next 运行中注入 engine / 嵌套双编排。
- 引入 worktree、Spec 生命周期、Finish、独立 Review 到 engine。
- 删除 BUILD/FIX 或增加第八 mode。
- 未 live 抽检的 description 堆词；未测完成率百分比宣称。
- 远程分支删除 / force-move / 改 main。

## Tasks

- [ ] T1: 重写 description + locales brief — acceptance: 含互补信号与负例；不含 worktree/spec/merge/finish；≤1024 chars (covers: S2)
- [ ] T2: 新建 compose-handoff.md + SKILL/Important/Examples 指针 — acceptance: 包模板六节齐全；SKILL 含 R1 指针与边界；body ≤110 行 / ≤3000 chars (covers: S2)
- [ ] T3: intent-router D3 三角色 + quality-gates Token Discipline — acceptance: D3 表含 R1 前置输入路径；quality-gates 写明包≠Spec、运行中不双载 (covers: S2)
- [ ] T4: scenarios S45–S48 + run_static_checks 新断言 — acceptance: 新场景合法；全量 ≥114 pass 且 0 fail (covers: S2; depends: T1–T3)
- [ ] T5: checklist / manual-verify / README / CHANGELOG 1.6.0 — acceptance: 文档与 pass 数/定位一致 (covers: S2; depends: T4)
- [ ] T6: 双安装同步 + 静态验证 + skill_search live 抽检 — acceptance: 三路径 SHA 一致；static 0 fail；点名 compose-next 不双载；R1 信号仍进 engine (covers: S2; depends: T1–T5)
