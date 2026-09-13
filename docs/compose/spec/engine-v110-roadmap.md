---
feature: engine-v110-roadmap
status: in-progress
updated: 2026-09-13
branch: plan/v110-iteration
commits: 9870790..(impl)
---

# Engine v1.10 Roadmap — v1.9 系统分析与迭代规划

## Report

**What was built** — 对 v1.9 九阶段 Soft 矩阵做了仓内可追溯的系统分析（150 静态检查、body 2991/3000、CHANGELOG/README 仍停 1.8.0 等缺口 G1–G6），并汇入 8 路联网证据（SkillReducer、Token ROI、Context Fails First、MoRe、Strained Coherence、Anthropic context/multi-agent、agentskills）。比较三条主轴后推荐 **A Soft Proof**（Soft 质量卡 + Token ROI 对照）并捆绑发布卫生与 body 腾空；写出可实施契约（质量抽检表、四场景 ROI 协议、body≤2880、P1–P3 三门）。本轮**未改 skill 行为**，实现任务 T6/T7 留待拍板后执行。

**Verification** — `python skill/tests/run_static_checks.py` → **150 pass / 0 fail**（docs-only，基线未变）；规格无 TBD；路径锚点（compose-phases/token/phase-matrix/v1.9 smoke）均存在。独立评审 `general-1`：六项 AC 全 MET，**REVIEW_PASS**，无 critical；已吸收非阻塞修订（Soft-Orient/Companion 质量行、`skill/tests/` 全路径、SkillReducer 版本史 framing）。

**Journey log** —
1. 沙箱禁止 `git worktree add`（共享 registry）→ 用 `git clone --local --shared` 到 `.worktrees/v110-plan` 作隔离 workspace，需在交付说明中披露。
2. v1.9 能力面已闭合；再扩 Soft 卡枚举 ROI 低——应先补「可证明」台架。
3. body 2991/3000 是硬墙：任何新 Important 必须先腾空（§2.4.3）。
4. 发布卫生（CHANGELOG/README）与 tag v1.9.0 脱节，应并入下一列车，避免文档债复利。
5. 联网检索在 websearch 不可用时走 webfetch 直达原文（Anthropic/arXiv/agentskills），比二手中文综述更可引用。

## [S1] Problem

v1.9 已交付 compose-next **九阶段 Soft 矩阵**（tag `v1.9.0`，静态 150 pass，冒烟 PASS），但：

1. **契约有、实证无**：Soft 卡只做静态/文档契约验收，没有「同等完成质量下 token 不升」与 Soft 质量的可重复度量。
2. **发布卫生滞后**：CHANGELOG 仍停在 `[1.8.0]`；仓 README Version=1.8.0；父目录 README 写 v1.8.0——与 tag/代码不一致。
3. **body 预算见顶**：SKILL body **2991/3000** chars、80 行，几乎无法再往 Important 塞规则；后续任何新能力只能靠指针化与文件拆分。
4. **外部实践在推进**：SkillReducer / Token ROI / Context Fails First / agentskills 渐进披露等给出可操作的新机制，需要判断是否吸收进 v1.10，而不是继续扩 Soft 卡枚举。

本轮需要：**系统分析 v1.9** + **联网证据** + **2–3 条 v1.10 主轴与推荐**，形成可实施规格草案（不立刻改 skill 本体）。

## [S2] Design

### 2.1 v1.9 系统分析（证据：本仓 @ `9870790` / tag `v1.9.0`）

#### 已建成

| 层 | 内容 | 证据 |
|---|---|---|
| Soft 矩阵 | Orient/Grill/Spec/Implement/Verify/Review/Finalize 有卡；Workspace/Finish 硬排除 | `skill/references/compose-phases.md` |
| 卡模板 | Soft-Orient / Spec-input / Evidence / Review-pack / Report | 同上 |
| Token 合同 | 单卡 JIT；证据包≤40 行；fan-out 默认 0、盲测≤1、Review 包 0 | `compose-token.md` |
| 边界 | 点名 compose-next 仍独占；不改 compose-next；不派 Reviewer | SKILL Important + router D3 |
| 自动化 | 150 pass / 0 fail | `python skill/tests/run_static_checks.py` |
| 场景 | S61–S70 覆盖九阶段 | `skill/tests/scenarios.md` |
| 冒烟 | Gate A–E 全 PASS | `docs/compose/smoke/v1.9-phase-matrix-multimodal.md` |
| 规格 | status=delivered，`32565b6..47abe82` | `docs/compose/spec/engine-compose-phase-matrix.md` |

#### 架构现状（简图）

```text
compose-next 九阶段
  Orient ── Soft-Orient (≤15行)
  Grill ─── Soft-Research (证据包≤40)
  Workspace ─ EXCLUDED
  Spec ───── Soft-Spec-input (可粘贴，不落盘)
  Implement ─ Soft-Test / Soft-Companion
  Verify ─── Soft-Evidence (命令|结果|路径)
  Review ─── Soft-Review-pack (只供输入)
  Finalize ─ Soft-Report (三段草稿)
  Finish ─── EXCLUDED
         │
         ▼  单卡 JIT
  compose-token.md ──► compose-phases.md | multimodal.md | handoff(R1/R2/R3)
```

#### 缺口与风险（按优先级）

| ID | 缺口 | 为何现在重要 | 严重度 |
|---|---|---|---|
| G1 | **无 Soft/Token ROI 实证** | 目标句是「同等质量 token 不升」，但 ROI 表为空、无基线对照协议 | 高 |
| G2 | **发布文档不一致** | tag v1.9.0 已存在；CHANGELOG/README 仍 1.8.0，破坏可追溯与安装信任 | 高（卫生） |
| G3 | **body 2991/3000** | 任何 v1.10 新 Important 行都会顶预算；SkillReducer 显示 ~60% body 可非 actionable 化 | 高 |
| G4 | **Soft 质量门未定义** | 卡「写了」≠ 卡「可用」；Review-pack/Evidence 无抽检清单与失败样例 | 中高 |
| G5 | **评测/过程门缺位** | 工程侧只测结构；无 end-state / 轨迹信号（Strained Coherence、Context 七维） | 中 |
| G6 | **fan-out/effort 仍粗** | v1.9 Out-of-Scope 留了 P1/P2；与 Anthropic「按查询复杂度缩放 effort」不完全对齐 | 中低 |

#### 版本史脉络（便于选主轴）

- v1.2–1.3：路由压缩 + 与 compose-next 互补边界（已吸收 SkillReducer/Effort 等来源）  
- v1.5：Lean Gates  
- v1.6–1.8：R1/R2/R3 + Soft Companion + Soft-Research/Test + token 合同  
- v1.9：九阶段 Soft 矩阵（能力面基本闭合）  
→ **下一跳更适合「从契约扩展 → 可证明质量/ROI」**，而不是再扩阶段枚举；v1.10 证据包是**复核与加深度**，非首次引入该文献。

### 2.2 联网证据（Soft-Research 风格证据包）

检索日：2026-09-13。事实/推断已区分。

| 主题 | 来源 | 关键可操作结论 |
|---|---|---|
| Context engineering | Anthropic *Effective context engineering* (2025-09) | 最小高信号 token；JIT 身份符；progressive disclosure；compaction；结构化笔记；子代理只回摘要 |
| Skill token | arXiv:2603.29919 SkillReducer | 55k skills：26.4% 无路由 description；body 仅 **38.5%** core rule；desc −48% / body −39% 且质量 +2.8%（less-is-more）；reference 灌入可达数万 tok |
| Token ROI | arXiv:2607.17528 | 相近完成度下 ROI 可差 **141×**；需要 process-level 评价，不只 end score |
| Context 预检 | arXiv:2607.14275 Context Fails First | 七维：role/guardrail/instruction/tool schema/grounding/injection/token；context 分是**领先指标** |
| 单代理多角色 | arXiv:2608.27338 MoRe | 相对 MAS 降 token ~20×；支持本仓「Role Lens 禁 MAS」 |
| 失败前信号 | arXiv:2606.07889 Strained Coherence | 承认风险仍硬做 → 失败率 94% vs 46%；对应 Lean Anti-SC |
| 多代理研究 | Anthropic multi-agent research (2025-06) | 广度任务才并行；token ≈15× chat；必须 effort 分档；小样本评测立刻开始 |
| 开放标准 | agentskills.io | 三级渐进披露（meta → body → refs）已成跨客户端标准；与本仓 references JIT 同构 |

**推断（非论文原话）**：v1.10 最大 ROI 不在「再加 Soft 卡」，而在 **度量 Soft 是否省 token 且不掉质量**，并 **释放 body 预算** 以免后续迭代被 3000 字符墙堵死。

### 2.3 候选主轴（3 条）与推荐

| 主轴 | 一句话 | 做什么 | 主要代价 | 何时选 |
|---|---|---|---|---|
| **A Soft Proof** | 证明 Soft 更好 | Soft 质量卡 + Token ROI 对照协议 + 抽检脚本/表；把「不升」变成可复验 | 需设计基线与人工抽检流程 | 默认推荐 |
| **B Budget Reset** | 释放 body + 补卫生 | CHANGELOG/README 对齐 v1.9；SkillReducer 式 body 再分层；引用表瘦身 | 对用户体感弱；易做成纯重构 | 预算墙已痛时 |
| **C Route/Context Upgrade** | 吸收外部预检与 effort | Context 七维轻量预检；fan-out/effort 缩放表；description 仅在失败时加词 | 易与 A 抢焦点；description 漂移风险 | A 完成后做下一轮 |

**推荐主轴：A Soft Proof，并捆绑 B 的卫生子集（G2）+ 轻量 budget 头（G3 只做「腾空间」不重写协议）**。

理由：

1. v1.9 能力面已闭合，缺的是证据；与仓库目标四元组（效率/完成率/错误率/返工）直接对齐。  
2. SkillReducer / Token ROI 都说明：**压缩与 ROI 必须带质量守恒门**，否则会假省。  
3. G2 是低成本高信任修复，应并入同一发布列车，避免 v1.10 再欠文档债。  
4. C 依赖 A 的基线数据；先有 ROI 台架再改路由/预检，避免盲调。

否决并行大改 description：v1.9 明确 description 本轮不改；无 skill_search 失败证据前不堆词（quality-gates 退出条件）。

### 2.4 v1.10 设计（推荐主轴落地契约）

**目标句**：在 **不改 compose-next、不双载编排层、Workspace/Finish 仍排除** 前提下，使 Soft 供给具备：

1. 可重复的 **质量验收**（每卡 3–5 条可观察检查）；  
2. 可重复的 **Token ROI 对照**（Soft vs 灌全协议/双编排，同任务）；  
3. body 预算 **余量 ≥ 120 chars**（或等价：再引入 1 条指针型 Important 仍 ≤3000）；  
4. 发布文档与 tag **一致**。

#### 2.4.1 Soft 质量卡（新 reference 或并入 compose-phases 附录）

每卡增加「DoD 抽检」最小集（不进 SKILL body，JIT 时读）：

| 卡 | 最低可观察验收 | 禁止 |
|---|---|---|
| Soft-Research | 证据包含来源标识；≤40 行；有开放问；事实/推断可分 | 无来源「结论」 |
| Soft-Spec-input | 片段可粘贴；无 frontmatter/status；任务有 acceptance | 写盘 feature 文档 |
| Soft-Evidence | 每行含命令或抽检 + PASS/FAIL；失败未隐藏 | 宣布 feature 总 Verify |
| Soft-Review-pack | 有 Range 与验收摘要；有未验区掩码 | 三类 Review 结论 / 派 Reviewer |
| Soft-Report | 三段结构齐全；Journey ≤5 | 改 status/commit |
| Soft-Test | 每模态至少 1 次工具证据路径 | 只报「已生成」 |
| Soft-Orient | ≤15 行；含假设/未验区掩码 | 重跑全仓 Orient 或灌七 mode |
| Soft-Companion | 只走 multimodal 卡；产物路径可指 | 写业务实现 |

实现轮可把上表落在 `compose-phases.md` 附录或独立 eval 附录，**不进 SKILL body**。

#### 2.4.2 Token ROI 对照协议（人工 + 半自动）

在 `skill/tests/manual-verify.md`（或新 `skill/tests/token-roi.md`）固化：

| 字段 | 定义 |
|---|---|
| 任务摘要 | ≤1 行 |
| 对照臂 | Soft（单卡 JIT） vs 全协议灌入 vs 双编排（能安全复现才做） |
| 观测 | 是否加载 Soft / 读了哪些 ref / 完成质量（DoD 勾选数）/ 粗估 token 或轮次 |
| 通过判据 | **同等 DoD 完成度下 Soft 臂 token/轮次不高于对照臂**；若质量掉则 FAIL 并记根因 |

首批固定 4 个场景（与 S61–S70 对齐，不新造舞台）：Grill 调研、Spec 草案、Review 输入、Finalize Report 草稿。

#### 2.4.3 Body 腾空策略（只腾不扩）

1. 复盘 SKILL Examples/Troubleshooting 是否可指针化到 references（保持步骤语义）。  
2. 重复禁令句合并；Important 保持「指针型」，细则进 phases/token。  
3. 验收：`body chars ≤ 2880`（3000−120）或文档记录「仅卫生轮不减 body 时的例外」。  
4. **不**在 v1.10 做 description 重写；**不**引入第八 mode。

#### 2.4.4 发布卫生（捆绑）

- CHANGELOG 增加 `[1.9.0]`（九阶段矩阵摘要 + compare 链接）。  
- README `Version` / Last sync → 1.9.0（及 v1.10 完成后再 bump）。  
- 父目录 `提示词工程/README.md` 当前版本表同步。  
- 双路径安装 SHA 抽检保留。

#### 2.4.5 文件职责

| 文件 | v1.10 动作 |
|---|---|
| `docs/compose/spec/engine-v110-roadmap.md` | 本文件：分析+设计+任务 |
| `docs/compose/smoke/v1.10-soft-proof-matrix.md` | （实现轮）ROI+质量验收矩阵 |
| `skill/references/compose-phases.md` | 附 Soft 质量抽检小节或指向 eval 附录 |
| `skill/references/compose-token.md` | ROI 字段与场景四件套指针 |
| `skill/tests/manual-verify.md` / 新 ROI 表 | 固化对照协议 |
| `CHANGELOG.md` / `README.md` | 补 1.9；v1.10 发布时再写 |
| `SKILL.md` | 仅在腾空后允许 ≤1 条指针微调；默认不改 description |

#### 2.4.6 验收三门（v1.10 实现轮）

| 门 | 定义 |
|---|---|
| P1 互补不变 | 点名 compose-next 独占；Workspace/Finish 仍零 Soft；不改 compose-next |
| P2 可证明 ROI | ≥4 个固定场景完成对照表；有 PASS/FAIL 与 token/轮次记录 |
| P3 质量不回退 | 质量卡抽检全过；静态 ≥150（或更新基线且 0 fail）；body 预算满足 2.4.3 |

### 2.5 交付物（本 feature）

- 规格：分析 + 证据 + 主轴推荐 + 实施契约（首轮）。
- 实现（用户拍板「继续实现」后并入本分支）：质量抽检、`tests/token-roi.md`、body 腾空、CHANGELOG/README 卫生、smoke 矩阵。
- **不**改 compose-next；**不**重写 description；**不**发 v1.10 tag（待合并与双路径安装后再定）。

## [S3] Out of Scope

- 修改 compose-next 本体或让其 load engine。  
- engine 接管 Workspace/Finish/独立 Review/feature Spec 生命周期。  
- 重写 description、加词堆路由、引入第八 mode。  
- 常开 MAS / 多子代理会审。  
- 真实音视频 e2e 资产管线。  
- 自动 LLM-judge 大规模评测平台（v1.10 只做可复验人工/半自动协议）。  
- Fan-out 细粒度策略表全面改版（留 v1.11；本轮至多文档占位）。

## Tasks

- [x] T1: Workspace 隔离（沙箱禁 worktree add → local clone 替代）— acceptance: 独立分支可改文档且不污染 main 工作树 (covers: S2)
- [x] T2: v1.9 系统分析写入本规格（建成物/缺口/版本史）— acceptance: §2.1 可追溯到仓内路径与 150 pass 证据 (covers: S2)
- [x] T3: 联网证据包 ≥6 源且标注可操作结论 — acceptance: §2.2 含 SkillReducer/Token ROI/Context/MoRe/Anthropic/agentskills (covers: S2)
- [x] T4: 三主轴比较 + 推荐 Soft Proof（捆绑卫生）— acceptance: §2.3 有否决理由与依赖顺序 (covers: S2)
- [x] T5: v1.10 设计契约（质量卡/ROI 协议/body 腾空/卫生/三门）— acceptance: §2.4 任务可独立验收；Out-of-Scope 明确 (covers: S2)
- [x] T6: 实现轮落地质量卡与 ROI 四场景 — acceptance: smoke 矩阵文档 + token-roi 表可复填；静态 0 fail (covers: S2)
- [x] T7: body 腾空 + CHANGELOG/README 卫生 — acceptance: body≤2880；CHANGELOG `[1.9.0]`；README Version 1.9.0 (covers: S2)
