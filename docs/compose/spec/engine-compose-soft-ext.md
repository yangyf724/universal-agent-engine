---
feature: engine-compose-soft-ext
status: delivered
updated: 2026-09-13
branch: optimize/v1.8-compose-soft-ext
commits: f421c98..1656d71
---

# Engine × Compose Soft Extensions (v1.8)

## Report

**What was built** — 在不改 compose-next 的前提下扩展 compose 会话 Soft 供给：**Soft-Research**（Grill 调研/论文/高星仓 → 研究卡 + 证据包≤40行，不拍板）；**Soft-Test**（Implement 视/听/跨模态测，默认 fan-out=0、高风险≤1 盲测，不宣布 feature 总 Verify）；**compose-token.md** 供给合同（单卡 JIT、禁七 mode/Full Gates 灌会话）。SKILL Soft 合并为一条并保持 body ≤3000。设计验证 PASS+AMENDMENTS（SE1–SE6）。

**Verification** — `python skill/tests/run_static_checks.py` → **135 pass / 0 fail**；body 2988 chars / 80 行；三路径 SKILL SHA `09ff1d0f06e3…`。独立评审 `f421c98..1656d71`：三类 PASS，无 critical；非 critical（D3 SE2 措辞、SE3 单指针、命名残留）已在 Finalize 前关闭。

**Journey log** —
1. compose-next 不会主动 load engine；Grill/测只能靠 **被需求触发的 Soft**，不能写成官方 hand-off。
2. Soft-Research 只供证据、不拍板，否则又变成第二编排。
3. 证据包≤40 行 + 单卡 JIT 是 C2 load-bearing；双 pointer 会把 token 打回灌协议。
4. fan-out 默认必须 0，否则「全模态测」会烧成多智能体会审。
5. Soft 改名后 D3/场景/正文要一次扫全，避免 exclusive 行滞后。

## [S1] Problem

用户希望 **compose-next 流程内** 三点增强，且 **不能改 compose-next 本体**（宿主内置、no internal hand-off）：

1. **Grill**：自动用全模态/联网（GitHub 高星仓、学术文献）细化需求分析与决策梳理。  
2. **Implement 测试**：用全模态测视觉/听觉等，降低模态 BUG；高风险可有限独立复测。  
3. **Token**：compose 会话更瘦——供给合同 + engine body 再压缩。  

现状 Soft Companion 只覆盖「媒体子任务」；Grill 外部证据与 Implement 模态测尚无自动 Soft 路径，也无 compose 供给 token 合同。

## [S2] Design

### 总原则（硬）

- **不改** compose-next；**不**让 compose-next 主动 load engine。  
- 同任务仍 **单编排层**；Soft 一律 **跳过 Step 2–6**。  
- Soft 只 JIT **指针点名的一个 reference**，禁止灌七 mode 表 / Full Gates / 全协议。

### Soft-Research（Grill）

| 项 | 合同 |
|---|---|
| 激活 A1 | 会话已在 compose-next Grill / P-domain 决策语境 |
| 激活 A2 | 信号：调研/对比/竞品/论文/文献/arXiv/高星仓/GitHub 案例/选型/丰富决策 |
| 供给 | **仅** RESEARCH 能力卡：websearch/webfetch、arxiv、`gh`/GitHub 检索、来源可信度标注 |
| 产物 | **compose-ready 证据包**（可用 R1 模板的 Evidence/Options 子集；≤ 约定行数） |
| 禁止 | 不替用户拍板 Grill 决策；不建 Spec/worktree；不展开 BUILD/FIX；无 compose 上下文 → 走 R2 全协议 RESEARCH |

细则落点：`references/compose-handoff.md` 新节 + `intent-router` D3 一行。

### Soft-Test（Implement/Verify）

| 项 | 合同 |
|---|---|
| 激活 B1 | compose Implement/Verify 中，待测物含 UI 截图/音视频/图/交互/Office 页 |
| 激活 B2 | 信号：测一下/检查界面/听一下/验收视觉/全模态测试/有没有显示问题 |
| 供给 | **测试卡**：视觉抽检、听觉抽听、跨模态数字一致、可打开性、禁 Fake Done（指向 multimodal Universal Gates） |
| 有限 fan-out | **仅高风险**（对外发布物/安全相关/UI 关键路径）可 **1** 个独立子代理复看/复听；默认 T2 **不** fan-out |
| 禁止 | 不写业务实现；不宣布整个 feature Verify 通过（只回报模态测结论）；无 compose 上下文媒体交付 → R2 |

### Compose 供给 Token 合同

新 reference：`references/compose-token.md`（或并入 compose-handoff 若能控 body）：

1. compose 会话中 engine **禁止**注入七 mode 全表、Role Lens 会审、Full Gates 常读。  
2. Grill 证据包默认 ≤ **40 行**；只含 Problem 摘要/关键证据/2–3 选项要点/开放问。  
3. Soft-Research/Soft-Test 各只 JIT **一个** pointer（handoff 或 multimodal）。  
4. Deliver 用短表；证据用路径/一行命令输出摘要，不贴全 log。  
5. Token ROI：记录「是否 Soft / 读了哪些 ref / 粗估 token」；目标同等质量下不升。

### Body 再压缩（配合 Soft 新增）

- 新增 Soft-Research / Soft-Test 各 **≤2 行** Important 或 D3 指针。  
- 同步压缩现有可缩短句，保持 body **≤3000** 字符、≤110 非空行。  
- description 本轮 **不改**（避免路由面漂移）。

### 验收三门

| 门 | 定义 |
|---|---|
| C1 强互补 | 点名 compose-next 仍独占；Soft 不接管 Grill/Verify 所有权；无双编排 |
| C2 Token | Soft 只 JIT 单卡；供给合同可静态断言；body ≤3000 |
| C3 质量 | Soft-Test 仍强制抽检/禁 Fake；Soft-Research 来源可核对；有限 fan-out 默认关 |

### 证据矩阵（验证用）

| ID | 场景 | 期望 |
|---|---|---|
| W1 | Grill：「对比三种登录方案，查高星仓与论文」 | Soft-Research 证据包；决策仍用户/compose-next |
| W2 | Grill 点名 `/compose-next` 且无调研信号 | 只 compose-next，不 Soft-Research |
| W3 | Implement：「测一下登录页截图和提示音」 | Soft-Test 视觉+听觉结论；不写业务码 |
| W4 | 独立「把录音做成纪要」 | R2 全协议，非 Soft-Test |
| W5 | 高风险对外 UI | Soft-Test + 可选 1 个盲测子代理 |
| W6 | Token | compose 会话不读七 mode 表/Full Gates |

### 环境覆盖

会话隔离拦 worktree；分支 `optimize/v1.8-compose-soft-ext`（base `f421c98`）。不改 compose-next。

## [S3] Out of Scope

- 修改 compose-next 或让其内部调用 engine。  
- Soft 接管 Grill 决策或 feature Verify 总结论。  
- 常开多子代理会审 / MAS。  
- 改 description 堆词。  
- 实现 GitHub/arXiv 新后端（只用现有 websearch/webfetch/arxiv/gh 工具合同）。

## Tasks

- [x] T1: 设计验证矩阵裁定 — acceptance: 三门结论；PASS/PASS+AMENDMENTS/FAIL (covers: S2)
- [x] T2: Soft-Research + Soft-Test + D3/handoff 落地 — acceptance: 激活/供给/禁止齐全；static 断言；body ≤3000 (covers: S2; depends: T1 非 FAIL)
- [x] T3: compose-token 供给合同 + checklist/manual ROI — acceptance: 合同可执行；场景 W1–W6 覆盖 (covers: S2; depends: T2)
- [x] T4: 双安装 + static + live 抽检 — acceptance: 三路径 SHA 一致；0 fail；点名 compose-next 不双载 (covers: S2; depends: T2–T3)
