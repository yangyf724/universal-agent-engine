---
feature: engine-v111-roadmap
status: in-progress
updated: 2026-09-14
branch: plan/v111-roadmap
commits: 8377f61..HEAD # implementation train started
---

# Engine v1.11 Roadmap — v1.10 短板总账与一次补齐规划

## Report

**What was built** —
本 feature 为 **v1.11 规划规格**（非 skill 实现）。完成：
1. v1.10 短板总账 H1–H5 + 历史残留 R1–R6 回扫（可追溯 smoke/spec/token-roi）。
2. 全模态联网证据包 ≥10 源（Context-7 / SC / Anthropic effort / MoRe / agentskills / SkillReducer / 过程评测 / 轻量 Judge 等），事实与推断分列。
3. 推荐 **A Process Proof + B Effort Reset + C Soft Depth** 三主轴同列车；不变量：不改 compose-next、Workspace/Finish 零 Soft、body≤2880。
4. 设计契约 §2.4（过程门、fan-out 决策表、Soft 深度五卡、验收四门 P1–P4）。
5. compose-next 短板双清单：A 本仓 Soft 可补 7 项；B 宿主本体 6 项仅建议草案，不进实现任务。

**Verification** —
- 规格结构：frontmatter + S1/S2/S3 + Tasks covers/acceptance 齐全；`status: designed`→本轮交付后 `delivered`（实现未开始）。
- 证据可追溯：§2.2 含 arXiv id 与 Anthropic 原文；仓内对照 `v1.10-soft-proof-matrix.md` / `engine-v110-roadmap.md`。
- 独立评审 `general-4`：三类结论均 MET/PASS，**0 critical**；非 critical（R5 归因、部分 arXiv id、任务勾选）已在 Finalize 前关闭。
- 未做：skill 本体改动、静态 153、生产 e2e token/错误率、LLM-judge 平台（见 S3）。

**Journey log** —
1. 用户要求「一次补齐」→ 采用可闭环优先级全集：能进本仓契约的进 A/C，宿主与生产度量进 B/边界，禁止假 CLOSED。
2. websearch 本会话不可用 → webfetch 主源 + 百度中文源 + 3 路子代理证据包交叉。
3. G5 关闭口径定为「协议存在 + ≥1 次对照抽检」，而非生产错误率下降。
4. G6 采用风险×独立度表，默认 fan-out=0 对齐 MoRe/15× MAS 证据；host effort 旋钮不伪造成 engine 功能。
5. Review over-finding / Spec amendment 双写来自 compose-next 实践缺口，已映射为 Soft-Drift / Soft-Amendment。

## [S1] Problem

v1.10.0 Soft Proof 已交付质量抽检与 Token ROI 四场景对照（Soft 指令上下文约为全协议灌入的 2–4%），但 smoke 明确 **未验区**：生产 compose 会话全链路 token/错误率、LLM-judge、fan-out 缩放；且 **G5 过程门**、**G6 effort/fan-out 细粒度** 仍 OPEN（CLOSED 6/9 ≈67%）。

用户目标：对 v1.10 短板做总结，经全模态联网分析列出 **v1.11 规划方案**，并以「可闭环优先级全集」口径，一次覆盖 **v1.1–v1.10 历史残留** 与 **compose-next 可观测短板**。边界：本仓改不了 compose-next 宿主本体；生产 A/B 与全自动 LLM-judge 平台不能假装本轮 CLOSED。

本轮交付物 = 本规格（分析 + 证据 + 可实施契约 + 宿主改法草案附录）。实现等用户拍板后开第二阶段。

## [S2] Design

### 2.1 v1.10 短板总账（证据：本仓 @ `75f9331` / tag `v1.10.0`）

#### 2.1.1 v1.10 自身 OPEN / 未验

| ID | 短板 | 证据 | 严重度 |
|---|---|---|---|
| H1 | **G5 过程门缺位** | 工程侧只测结构；无 end-state/轨迹信号（Strained Coherence、Context 七维） | 高 |
| H2 | **G6 fan-out/effort 仍粗** | Soft fan-out 默认 0 / 高风险≤1 / Review 0；无风险×独立度表 | 中高 |
| H3 | **ROI 口径非生产 e2e** | `token-roi.md` = 指令上下文 chars→tok；非全会话/错误率 | 中 |
| H4 | **无 LLM-judge / 过程抽样协议** | v1.10 Out-of-Scope 明确不做平台；亦未留轻量抽样协议 | 中 |
| H5 | **双路径安装依赖实现轮** | smoke A4 后补 PASS；卫生列车依赖人工双路径同步 | 低（已过门，防复发） |

#### 2.1.2 历史版本残留（回扫 v1.1–v1.9）

| ID | 来源 | 残留 | 是否仍应关 |
|---|---|---|---|
| R1 | v1.3 | description 含 修bug/build/implement/ship（有意残留，靠 D3 让位） | 低优先；无 live miss 证据则保持 |
| R2 | v1.5 | S-c：无风险话术时静默 happy-path（接受残留风险；仅「可选已验范围」） | 是 → 并入 G5 过程门 |
| R3 | v1.9 P1 | fan-out 预算细化未做 | 是 → G6 |
| R4 | v1.9 P2 | 评测卡未做 | 是 → G5 轻量抽样 |
| R5 | v1.6–1.9 缺口分析 | Soft 全阶段矩阵已铺开，但 **阶段 I/O 契约、Spec 漂移、Verify 配方、Amendment 双写** 无 Soft 卡（absence-based，非历史 OPEN ID） | 是 → Soft 深度 |
| R6 | v1.10 | body 余量 2852/2880（128 chars）——新 Important 必须指针化 | 持续约束 |

#### 2.1.3 架构现状（不变量）

```text
compose-next 九阶段（宿主）
  Orient ── Soft-Orient
  Grill ─── Soft-Research（证据包≤40）
  Workspace ─ EXCLUDED（永不）
  Spec ───── Soft-Spec-input（可粘贴，不落盘）
  Implement ─ Soft-Test / Soft-Companion
  Verify ─── Soft-Evidence（命令|结果|路径）
  Review ─── Soft-Review-pack（只供输入）
  Finalize ─ Soft-Report（三段草稿）
  Finish ─── EXCLUDED（永不）
```

**v1.11 不变量**：不改 compose-next 本体；Workspace/Finish 零 Soft；单卡 JIT；同任务单编排层；body ≤2880。

### 2.2 全模态联网证据包（检索日：2026-09-12/14）

事实/推断已区分。中文源经百度；英文/学术经 arXiv abs + Anthropic 原文 + agentskills.io。

| 主题 | 来源 | 关键可操作结论 | 类型 |
|---|---|---|---|
| Context 七维预检 | arXiv:2607.14275 Context Fails First | 七维（role/guardrail/instruction/tool-schema/grounding/injection/token）为**领先指标**；context 分与行为分隔离 → 非循环 | 事实 |
| 失败前信号 | arXiv:2606.07889 Strained Coherence | 旗标轨迹失败率 94% vs 46%；首旗标出现在轨迹 **83–84%** 时点 → 适合 **Verify 后半段软停**，非早期预警；需 think 基底 | 事实 |
| 过程评测 | TRAIL arXiv:2505.08638；ClawTrack 2607.28037 | 过程分（goal/efficiency/info-use/**verify**）可滤掉 lucky pass；result-verification 是系统瓶颈 | 事实 |
| 轻量 Judge | trajectory-judge 2609.00038；PROCTOR 2609.02246；ExecRubrics 2608.22559 | outcome-only judge 漏 ~45% 静默错；确定性守卫 + **canary** 优于只靠 LLM judge；完美分=作弊证据 | 事实 |
| 结构≠效果 | ACES SkillEvaluator | 扫描结构门 vs 真跑 Skill Lift：**ρ=0.14** | 事实 |
| Effort 缩放 | Anthropic multi-agent research (2025-06) | 简单 1 agent/3–10 calls；对比 2–4 sub/10–15；复杂 >10。MAS≈**15×** chat token；token 解释 ~80% 方差；coding 并行度低于 research | 事实 |
| 单代理优先 | arXiv:2608.27338 MoRe | 单代理多角色 ≈ MAS 质量、token 约 **1/20** | 事实 |
| Skill 标准 | agentskills.io | 三级渐进披露：meta ~100 tok → body <5k tok → refs 按需；SKILL <500 行 | 事实 |
| Skill 压缩 | arXiv:2603.29919 SkillReducer | body 仅 38.5% core rule；desc −48%/body −39% 且质量 +2.8% | 事实 |
| Spec 工程实践 | Anthropic *Best practices for Claude Code*；OpenSpec/Spec-Kit 实践文（百度检索 2026-09） | verify 层级：tests → goal → Stop hook → 独立 reviewer；**Review over-finding** 是明确失败模式；Spec 需双写 amendment；过度规格会被忽略 | 事实+中文二手 |

**推断（非原话）**：v1.11 最大 ROI 不是再扩 Soft 枚举，而是 **(1) 把 G5 变成可观察的过程门（Context-7 预检 + Verify 后软停 + canary）**，**(2) 用风险×独立度表收口 G6**，**(3) 补 Soft 的阶段契约/漂移/Verify 配方/Amendment 四类深度卡**。全自动 LLM-judge 平台与生产 A/B 仍 OUT。

### 2.3 候选主轴（3 条）与推荐

| 主轴 | 一句话 | 做什么 | 代价 | 何时选 |
|---|---|---|---|---|
| **A Process Proof** | 过程可证 | Context-7 预检表 + Verify 后 SC 软停 + canary + 抽样过程分协议 | 需定义廉价检查清单，不建平台 | 默认并列主轴 |
| **B Effort Reset** | 收口 fan-out | 风险×独立度矩阵 + Anthropic 分档对照 + 默认单代理 | 需可判定的 independence test | 并列主轴（关 G6） |
| **C Soft Depth** | 补 compose 会话深度卡 | Soft-Contract / Drift / Verify-recipe / Amendment / DoD-artifact | 新 reference 或并入 phases；body 不增 | 并列主轴（关 compose 短板 A 表） |

**推荐：A+B+C 三主轴同一发布列车**（用户要求「一次补齐」）；**B 清单（宿主）只出附录草案，不实现**。

否决：本轮再扩第七张 Soft 阶段卡或改 description 堆词（无 skill_search 失败证据；SkillReducer 显示 less-is-more）。

### 2.4 v1.11 设计契约（实现轮落地）

**目标句**：在 **不改 compose-next、不双载、Workspace/Finish 仍排除、body≤2880** 前提下：

1. G5 关闭为「**可复验过程门协议存在并过 ≥1 次对照抽检**」，非生产错误率下降宣称；
2. G6 关闭为「**fan-out/effort 决策表已写入 token 合同且静态检查覆盖**」；
3. compose-next 可观测短板 A 表 7 项中，**本仓可 Soft 填补的 5 项有卡**；宿主项出草案附录；
4. 历史 R2/R3/R4/R5 被上述契约覆盖；R1/R6 保持显式约束。

#### 2.4.1 主轴 A — Process Proof（关 G5 / R2 / R4）

| 件 | 落点 | 契约 |
|---|---|---|
| Context-7 预检 | `references/quality-gates.md` Lean 附录或独立 `process-gates.md` | 7 项勾选（role/guardrail/instruction/tool-schema/grounding/injection/token）；**T2+ 或信号触发才填**；分与行为结果隔离记录 |
| SC 软停 | 同上 + Lean Gates 信号行扩展 | Verify 后半段 / Deliver 前：若出现「承认风险仍硬做」句式 → **阻塞 done** 或强制未验 1 句；词表沿用 v1.5 信号 + SC 扩展 |
| Canary | 同上 | 每个 T2+ feature 至少 1 条「若完美通过则可疑」检查（测试故意失败、必填字段缺失、文件不存在）；**确定性优先于 LLM judge** |
| 过程抽样协议 | 新 `skill/tests/process-audit.md`（或并入 manual-verify） | 字段：goal/efficiency/info-use/verify 四维 0–2；抽样 N≤20/轮次；**不做**自动 judge 平台 |
| 实现轮验收 | smoke `v1.11-process-matrix.md` | ≥1 次 Soft vs 全协议对照的过程分记录；禁止空 PASS |

**禁止**：宣称生产错误率下降；把结构静态检查说成过程分；常开 LLM-judge。

#### 2.4.2 主轴 B — Effort Reset（关 G6 / R3）

决策表写入 `references/compose-token.md`（Fan-out 预算节替换）：

| 条件 | Soft fan-out | 备注 |
|---|---|---|
| 默认（任何 Soft） | **0** | 与 MoRe / MAS 15× 证据对齐 |
| 高风险盲测 | **1** | 保持 |
| Review pack / Spec-input / Report / Evidence | **0** | 保持 |
| **T3 且独立分支≥2 且低风险** | soft cap **2–4** | 仅引擎研究/广度；子代理回摘要 |
| 共享上下文 / Implement 耦合 / coding 主路径 | **强制 0–1** | Anthropic：coding 并行度低 |
| 用户点名要并行且价值可付 token | 可 raise，须写明预算 | 禁止静默爆 fan-out |

Effort 与 fan-out **正交**：T 档管深度/是否全协议；fan-out 管广度。host 的 `effort: low…max` / Explore thoroughness **只写建议映射，不伪造成 engine 功能**。

**实现轮验收**：静态检查断言决策表存在且默认 0；场景 S 新增 ≥2（应 fan-out / 应拒 fan-out）。

#### 2.4.3 主轴 C — Soft Depth（关 R5 / compose A 表）

新增（优先并入 `compose-phases.md` 附录，避免新文件爆炸；body 不进）：

| 新卡 | 阶段 | 最低验收 | 禁止 |
|---|---|---|---|
| Soft-Contract | 任一 Soft 交付前 | 输入/输出/恢复点三行；与当前 compose 阶段对齐 | 接管 Workspace/Finish |
| Soft-Drift | Spec↔Implement 边界 | 抽检 Spec 锚点 vs diff：漂移 1 句披露 | 擅自改 Spec status |
| Soft-Verify-recipe | Verify / 项目复用 | 本仓/本 feature 的验证命令 ≤5 行可复跑 | 宣布 feature 总 Verify 通过 |
| Soft-Amendment | Finalize 前（若范围曾变） | amendment 草稿片段 + 任务勾选同步建议；**不** commit | 写盘 feature 文档 |
| Soft-DoD-artifact | Implement/Verify | 可机读证据指针（路径/命令输出）≥1 | 无工具证据称 done |

激活仍遵守：单卡 JIT、跳过 Step 2–6、Workspace/Finish 零 Soft。

#### 2.4.4 卫生与 body（捆绑）

- body 保持 ≤2880；新规则一律指针化。
- 实现轮：CHANGELOG `[1.11.0]`；README Version；父 README 版本表；静态基线 ≥153（只增不减）。
- 双路径安装 SHA 抽检。

#### 2.4.5 文件职责

| 文件 | v1.11 动作 |
|---|---|
| `docs/compose/spec/engine-v111-roadmap.md` | 本规格 |
| `docs/compose/smoke/v1.11-process-matrix.md` | （实现轮）过程门 + effort 对照矩阵 |
| `skill/references/process-gates.md` 或并入 quality-gates | Context-7 + SC 软停 + canary |
| `skill/tests/process-audit.md` | 抽样过程分协议 |
| `skill/references/compose-token.md` | Fan-out 决策表 |
| `skill/references/compose-phases.md` | Soft Depth 五卡 + 质量抽检行 |
| `skill/tests/run_static_checks.py` | 新断言与基线 |
| `skill/tests/scenarios.md` | 新场景覆盖 G5/G6/深度卡 |
| `SKILL.md` | 默认不改 description；Important 至多 ≤1 条指针微调 |
| `CHANGELOG.md` / `README.md` | 实现轮卫生 |

#### 2.4.6 验收四门（v1.11 实现轮）

| 门 | 定义 |
|---|---|
| P1 互补不变 | 点名 compose-next 独占；Workspace/Finish 零 Soft；不改 compose-next |
| P2 过程可证 | Context-7/SC/canary 协议存在；≥1 次对照抽检有分；抽样表可复填 |
| P3 Effort 可执行 | 决策表进 token 合同；静态 + 场景覆盖默认 0 与 raise 路径 |
| P4 质量不回退 | 质量抽检含新卡；静态 0 fail；body≤2880；ROI 四场景不回退 |

### 2.5 compose-next 短板双清单

#### A — engine Soft 可填补（本轮契约内）

| id | 症状 | Soft 动作 |
|---|---|---|
| A1 | 无机器证据的 Fake Done | Soft-DoD-artifact |
| A2 | Spec 漂移静默 | Soft-Drift |
| A3 | 阶段 I/O 契约不清 | Soft-Contract |
| A4 | 关键步未验就推进 | Context-7 + SC 软停 + canary |
| A5 | Verify 配方每次重造 | Soft-Verify-recipe |
| A6 | 编排指令上下文过重 | 保持单卡 JIT + PD（已达标，持续） |
| A7 | Amendment 不双写 | Soft-Amendment |

#### B — 宿主 compose-next 本体（只建议，附录草案）

| id | 症状 | 建议（不实现） |
|---|---|---|
| B1 | Grill 疲劳：一轮一问可打穿 | Grill 预算：默认 max 3 轮或首次 Never-Ask 后收束 |
| B2 | Review theater：必挑刺 | findings 分级 critical\|major\|optional；仅 critical 阻塞 |
| B3 | Worktree 坑：.env/LFS/hook/merge | Workspace enter/exit checklist |
| B4 | Spec 过度规格被忽略 | prune-if-derivable 一句；自包含文件与 e2e 验证 |
| B5 | Writer 自评 | Review 必须引用 Spec+tasks，禁止只引对话记忆 |
| B6 | 硬停偏软 | Verify 可选映射 host 门（tests/\|goal\|Stop hook\|独立子代理） |

### 2.6 版本史脉络（为何是这三主轴）

- v1.2–1.3：路由压缩 + P-domain 让位  
- v1.5：Lean Gates（效率优先，接受 S-c）  
- v1.6–1.9：R1/R2/R3 + Soft 全阶段矩阵（能力面闭合）  
- v1.10：Soft Proof（契约可证明；G5/G6 留白）  
- **v1.11：过程门 + effort 收口 + Soft 深度** —— 从「有卡/可省 token」到「过程可证、预算可执行、compose 会话少漂移」。

## [S3] Out of Scope

- 修改 compose-next 本体或让其 load engine（附录 B 仅草案）。
- 生产 compose 会话 A/B 错误率、全会话 token 仪表。
- 自动 LLM-judge 平台 / TRAIL 级轨迹标注管线。
- 重写 description、加词堆路由、第八 mode、常开 MAS。
- 真实音视频 e2e 资产管线。
- 伪称 G5/G6 在无实现轮证据时 CLOSED。
- engine 接管 Workspace/Finish/独立 Review/feature Spec 生命周期。

## Tasks

## Tasks

- [x] T1: Workspace 分支就绪 — acceptance: `plan/v111-roadmap` 可改文档且工作树干净（本轮已建） (covers: S2)
- [x] T2: v1.10 短板总账 + 历史残留回扫写入本规格 — acceptance: §2.1 表可追溯仓内路径 (covers: S2)
- [x] T3: 联网证据包 ≥8 源且标注事实/推断 — acceptance: §2.2 含 Context-7/SC/Anthropic effort/MoRe/agentskills/质量门 (covers: S2)
- [x] T4: 三主轴 + 推荐 A+B+C 同列车 — acceptance: §2.3 有否决理由；实现边界与 §S3 一致 (covers: S2)
- [x] T5: 设计契约（过程门/effort 表/Soft 深度/四门）— acceptance: §2.4 各件可独立验收 (covers: S2)
- [x] T6: compose-next 双清单 + 宿主修订草案 — acceptance: §2.5 A/B 分离；B 不进入实现任务 (covers: S2)
- [x] T7: 实现轮：process-gates + audit 协议 + token 决策表 + Soft 深度卡 + 场景/静态/smoke — acceptance: 静态 174/0；body 2851；S71–S74；smoke 矩阵 PASS（P1–P4 契约级） (covers: S2)
- [ ] T8: 实现轮评审 + 版本发布 — acceptance: 无 critical；静态 0 fail；tag `v1.11.0`（merge 后打 tag） (covers: S2)

> 本 feature 本轮交付 = **规划规格 T1–T6**。T7–T8 不阻塞规划验收，待用户拍板「继续实现」后执行。
