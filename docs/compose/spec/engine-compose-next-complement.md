---
feature: engine-compose-next-complement
status: designed
updated: 2026-09-13
branch: optimize/v1.3-compose-complement
commits: f1df40c..<head> # filled at delivery
---

# Engine × Compose-next Complement

## Report

## [S1] Problem

v1.2 只在「点名 compose-next」时让位。未点名的 git 仓内多步实现/修 bug 仍被 engine 全协议接走，缺少 worktree/Spec/独立 Review，与 compose-next 职责重叠，用户需反复记忆点名成本。需要把 compose-next 优先域（P-domain）从 engine 让出去，同时保留 engine 在研究/写作/媒体/非仓交付上的独占面。

## [S2] Design

### 域划分（互补，不删 mode）

| 域 | 归属 | 定义 |
|---|---|---|
| P-domain | compose-next 优先 | git 仓内多步实现/修 bug/方案落地，且要合并/发版/durable 文档，或用户点名 / 项目 AGENTS 预授权 |
| E-domain | engine | RESEARCH / DESIGN 方案本体 / WRITE / OPERATE / ADVISE、多模态、Role Lens、非 git 交付、脚本/配置/一次性多步、用户明确 without compose-next |

### 让位合同（engine 侧）

1. **点名让位（已有）**：`/compose-next` 或「用 compose-next 流程」→ 只走 compose-next，不加载 engine 全协议。
2. **P-domain 建议让位（新增）**：git 仓内且信号为实现/修 bug/上线/合并准备，用户**未**点名 → engine **不**进入 Step 2–6 全协议；输出一句建议 `/compose-next …`；用户确认前不开工。用户明确「直接修 / 不用 compose-next / without spec」→ 仍走 engine 轻量 BUILD/FIX。
3. **不引入**：engine 不实现 worktree、Spec 生命周期、Finish 合并、独立 Review 子代理合同。
4. **共享原则保留**：DoD / Evidence / No Fake Done / 委托 official。

### 文件契约

- `skill/SKILL.md` Important：扩展现有「同任务只加载一个编排层」为点名 + P-domain 让位。
- `skill/SKILL.md` Examples：增加 1 条 P-domain 让位示例（不扩 description）。
- `references/intent-router.md` D3：可执行 4 步边界规则（点名 / P-domain 建议 / E-domain 正常 / official/github-sync）。
- `tests/scenarios.md`：S39 P-domain 建议；S40 用户拒绝后 engine FIX。
- `tests/run_static_checks.py`：断言 SKILL 含 P-domain 让位措辞与 intent-router D3 规则。
- `tests/checklist.md`：L3/L4 勾选与 sign-off 行。
- `references/quality-gates.md` Token Discipline：一句 P-domain 让位指针（可选，保持短）。
- `CHANGELOG.md`：1.3.0 Changed 列表。
- **description 本轮不改**；live `skill_search` 出现 miss 再按加词退出条件处理。

### 环境覆盖

会话隔离拦截 `git worktree add`。本 feature 在主检出新建分支 `optimize/v1.3-compose-complement`（base `f1df40c`），不创建 linked worktree。不改 compose-next（宿主内置）。

## [S3] Out of Scope

- 删除 BUILD/FIX mode 或多模态/Role Lens。
- 修改 compose-next 技能本体或 description。
- 为「组合」在任一侧嵌套另一协议。
- 远程分支删除 / force-move / 改 main。
- 全局 AGENTS.md「实现即自动 compose-next」（用户可另选项目级预授权）。

## Tasks

- [ ] T1: 扩写 SKILL.md Important 让位规则 + Examples — acceptance: 正文含点名让位与 P-domain 建议/直接修路径；body 行数 ≤110、chars ≤3000 (covers: S2)
- [ ] T2: 扩写 intent-router.md D3 为 4 步可执行边界 — acceptance: D3 列出点名/P-domain/E-domain/official，且含「用户说直接修则走本 skill」 (covers: S2)
- [ ] T3: scenarios 增 S39–S40 — acceptance: S39 Expected 含（不路由全协议）或等价 P-domain 建议；S40 Expected=FIX (covers: S2)
- [ ] T4: run_static_checks 增 P-domain/D3 断言 — acceptance: 新断言失败条件与措辞对齐；全量 ≥101 pass 且 0 fail (covers: S2; depends: T1, T2)
- [ ] T5: checklist + quality-gates 指针 — acceptance: L3/L4 含互补项；Token Discipline 一句 P-domain；checklist 期望 pass 数更新 (covers: S2)
- [ ] T6: CHANGELOG 1.3.0 — acceptance: Changed 列表覆盖 T1–T5；比较链接占位正确 (covers: S2; depends: T1–T5)
- [ ] T7: 双安装同步 + 静态验证 — acceptance: 仓库与双安装 skill 目录一致；`run_static_checks.py` 全绿 (covers: S2; depends: T1–T6)
