# Compose Token Contract — compose 会话中的供给纪律

engine 在 compose-next/P-domain 会话里只做 **Soft 供给**，目标：同等质量下 token 不升。

九阶段 Soft 角色与卡模板：`references/compose-phases.md`。  
过程门（Context-7 / SC 软停 / canary）：`references/process-gates.md`；抽样协议 `tests/process-audit.md`。

## 硬规则

1. **禁止**把七 mode 全表、Role Lens 会审、Full Gates 常读灌进 compose 会话。
2. **每次 Soft 只 JIT 一个 pointer**（细则可在同一文件内展开；禁止并行灌第二份编排/门禁全文）：
   - 媒体子任务 → `references/multimodal.md`
   - Grill 调研 → 本文件（研究卡与证据包；完整 R1 模板仅用户要前置包时再读 handoff）
   - Orient / Spec / Review / Finalize 输入卡 / Verify 证据表 → `references/compose-phases.md` 对应卡
   - Implement 模态测 → `references/multimodal.md` Universal Gates 或本文件测试卡
3. **跳过 Step 2–6**；不建 Spec/worktree/Finish；不派独立 Reviewer；不出 feature 总 Verify 结论。
4. 点名 `/compose-next` 且无独立 Soft 请求 → **只** compose-next，engine 不加载。
5. **Workspace / Finish 零 Soft**（见 phases 矩阵排除行）。

## Grill 研究卡（Soft-Research）

| 工具 | 用途 | 证据 |
|---|---|---|
| `websearch` / `webfetch` | 公开网页、工程博客 | URL + 检索日 |
| arxiv skill | 学术论文 | arXiv id / DOI |
| `gh` / GitHub 检索 | 高星仓、issue 模式 | 仓库路径 + star/主题一行 |

- 交叉核对关键事实；区分事实/推断/观点。  
- 产物：**证据包 ≤40 行**（Problem 一句 / 关键证据 / 2–3 选项要点 / 开放问 1–3）。  
- **不**替用户在 Grill 拍板。

## Implement 测试卡（Soft-Test）

| 模态 | 最低抽检 | 禁止 |
|---|---|---|
| 视觉/UI | 关键屏/控件 1 次回读 | 只报「已生成」 |
| 听觉 | 关键句/提示音抽听 | 未听称通过 |
| 跨模态 | 图=表=文关键数字 | 数字不一致仍 done |
| 交互/Office | 可打开/可拖/关键页 | 假打开 |

- 高风险（对外发布/安全/关键 UI）可 **最多 1** 个独立子代理盲测；**默认不 fan-out**。  
- 只回报模态测结论，**不**宣布整个 feature Verify 通过。

## Fan-out / Effort 决策表（v1.11 G6）

Effort（T 档深度）与 fan-out（广度）**正交**。host 的 `effort: low…max` 只作建议映射，**不是** engine 功能。

| 条件 | Soft fan-out | 备注 |
|---|---|---|
| 默认（任何 Soft） | **0** | 对齐 MoRe 单代理 / MAS≈15× token |
| Soft-Test 高风险盲测 | **1** | 保持 |
| Soft-Review-pack | **0** | Review 归 compose |
| Soft-Spec-input / Soft-Report / Soft-Evidence | **0** | 保持 |
| **T3 且独立分支≥2 且低风险** | soft cap **2–4** | 仅广度研究；子代理回摘要、产物落盘 |
| 共享上下文 / Implement 耦合 / coding 主路径 | **强制 0–1** | Anthropic：coding 并行度低 |
| 用户点名要并行且价值可付 token | 可 raise，写明预算 | 禁止静默爆 fan-out |

Independence test（一行）：子代理任务能否互不依赖、结果可并集、无需共享同一工作副本？否则 fan-out 不得 >0。

Raise 路径必须在证据包或 Soft 卡备注写：为何独立、预算、回传摘要格式。

## Token ROI（对照协议）

固定四场景与可复填表：`tests/token-roi.md`。质量抽检：`compose-phases.md`。

| 会话 | Soft 类型/阶段 | 读过的 ref | 粗估 token/轮 | DoD 完成 | 判定 |
|---|---|---|---|---|---|
| | | | | | PASS/FAIL/未做 |

目标：同等完成质量下 token **不升**；质量掉档即 FAIL。
