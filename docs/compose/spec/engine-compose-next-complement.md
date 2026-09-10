---
feature: engine-compose-next-complement
status: delivered
updated: 2026-09-13
branch: optimize/v1.3-compose-complement
commits: f1df40c..f39d56e
---

# Engine × Compose-next Complement

## Report

**What was built** — engine 与 compose-next 互补化（v1.3.0）：不删除 BUILD/FIX，将 git 仓内「要合并/发版/durable 规格」的多步实现定义为 **P-domain**，未点名时 engine 只建议 `/compose-next`、不进 Step 2–6；用户说「直接修 / 不用 compose-next / without spec」仍走 engine 轻量 BUILD/FIX。点名让位、E-domain（研究/写作/媒体/答疑/非仓交付）、Role Lens、多模态与 official 委托保持不变。description 本轮未改。

**Verification** — `python skill/tests/run_static_checks.py` → **106 pass / 0 fail**（仓库 + `~/.config/mimocode/skills` + `~/.claude/skills`，关键文件 SHA256 一致）。`skill_search`：点名 compose-next → compose-next 1.0；「调研竞品并落地成可运行脚本」→ universal-agent-engine 0.61。独立评审 `f1df40c..6eb3a12`：Spec 合规 10/10 PASS，无 critical；评审非关键项已在 `f39d56e` 关闭（D3 中文化、Important 回退措辞对齐、checklist sign-off、静态断言收紧）。

**Journey log** —
1. 会话隔离拦截 `git worktree add` → 在主检出开分支 `optimize/v1.3-compose-complement`（环境覆盖已记入 S2）。
2. 「功能一致即删」会误伤非 git/未点名实现 → 改为 **P-domain 让位** 而非删 mode。
3. description 仍含 修bug/build/implement/ship，未点名 P-domain 可能仍加载 engine 再靠 D3 让位——有意残留；live miss 再按加词退出条件处理。
4. 静态检查只能证明措辞存在，不能证明 BM25 排名；路由 claim 必须附 live 证据。
5. 评审非 critical 一致性缺口（ZH/EN、sign-off）应在 Finalize 前关掉，避免下一轮再提。

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
- `references/quality-gates.md` Token Discipline：一句 P-domain 让位指针。
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

- [x] T1: 扩写 SKILL.md Important 让位规则 + Examples — acceptance: 正文含点名让位与 P-domain 建议/直接修路径；body 行数 ≤110、chars ≤3000 (covers: S2)
- [x] T2: 扩写 intent-router.md D3 为 4 步可执行边界 — acceptance: D3 列出点名/P-domain/E-domain/official，且含「用户说直接修则走本 skill」 (covers: S2)
- [x] T3: scenarios 增 S39–S40 — acceptance: S39 Expected 含（不路由全协议）或等价 P-domain 建议；S40 Expected=FIX (covers: S2)
- [x] T4: run_static_checks 增 P-domain/D3 断言 — acceptance: 新断言失败条件与措辞对齐；全量 ≥101 pass 且 0 fail (covers: S2; depends: T1, T2)
- [x] T5: checklist + quality-gates 指针 — acceptance: L3/L4 含互补项；Token Discipline 一句 P-domain；checklist 期望 pass 数更新 (covers: S2)
- [x] T6: CHANGELOG 1.3.0 — acceptance: Changed 列表覆盖 T1–T5；比较链接占位正确 (covers: S2; depends: T1–T5)
- [x] T7: 双安装同步 + 静态验证 — acceptance: 仓库与双安装 skill 目录一致；`run_static_checks.py` 全绿 (covers: S2; depends: T1–T6)
