# Compose Token Contract — compose 会话供给纪律

engine 只做 **Soft 供给**；目标：同等质量下 token **不升**，效率 **不差于** v1.10。

阶段卡：`references/compose-phases.md`。过程门：`references/process-gates.md`；抽样：`tests/process-audit.md`。

## 硬规则

1. **禁止**灌七 mode 全表、Role Lens 会审、Full Gates 进 compose 会话。
2. **每次 Soft 只 JIT 一个 pointer**：
   - 媒体 → `multimodal.md`
   - Grill → 本文件研究卡（R1 模板仅前置包时读 handoff）
   - Orient/Spec/Review/Finalize/Verify 输入卡 → `compose-phases.md` 对应卡
   - Implement 模态测 → `multimodal.md` 或本文件测试卡
3. **跳过 Step 2–6**；不建 Spec/worktree/Finish；不派 Reviewer；不出 feature 总 Verify。
4. 点名 `/compose-next` 且无独立 Soft 请求 → **只** compose-next。
5. **Workspace / Finish 零 Soft**（见 phases 矩阵排除行）。
6. **供给路径（v1.12）**：coding 默认不灌 process-gates 全文与全部 Depth 卡；过程信号是注解行。禁止「一次打包五卡+全门」。

## Grill 研究卡（Soft-Research）

| 工具 | 用途 | 证据 |
|---|---|---|
| websearch/webfetch | 公开网页 | URL+检索日 |
| arxiv | 论文 | arXiv id |
| gh | 高星仓/issue | 仓路径+主题一行 |

- 交叉核对；区分事实/推断。产物：**证据包 ≤40 行**。**不拍板**。

## Implement 测试卡（Soft-Test）

| 模态 | 最低抽检 | 禁止 |
|---|---|---|
| 视觉/UI | 关键屏 1 次 | 只报已生成 |
| 听觉 | 关键句抽听 | 未听称通过 |
| 跨模态 | 图=表=文数字 | 不一致仍 done |
| 交互/Office | 可打开/关键页 | 假打开 |

高风险可 ≤1 盲测；**默认 fan-out=0**。不宣布 feature 总 Verify。

## Fan-out / Effort（v1.12 压缩表）

Effort（深度）与 fan-out（广度）**正交**。host effort 仅建议映射。

| 条件 | Soft fan-out |
|---|---:|
| 默认（任何 Soft） | **0** |
| 高风险盲测 | **1** |
| Review/Spec/Report/Evidence | **0** |
| T3 且独立分支≥2 且低风险 | **2–4**（仅广度研究；回摘要） |
| 共享上下文 / Implement 耦合 / coding | **强制 0–1** |
| 用户点名并行且价值可付 | 可 raise；写明预算 |

Independence test（一行）：子代理任务能否互不依赖、结果可并集、无需共享同一工作副本？否则不得 >0。Raise 须写：为何独立、预算、回传格式。

## Token ROI

协议与 Pack-size：`tests/token-roi.md`。质量抽检：`compose-phases.md`。

| 会话 | Soft 类型 | 读过的 ref | tok/轮 | DoD | 判定 |
|---|---|---|---|---|---|
| | | | | | PASS/FAIL/未做 |

同等完成质量下 token **不升**；质量掉档即 FAIL。
