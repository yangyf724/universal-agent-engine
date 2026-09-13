# Compose Token Contract — compose 会话中的供给纪律

engine 在 compose-next/P-domain 会话里只做 **Soft 供给**，目标：同等质量下 token 不升。

## 硬规则

1. **禁止**把七 mode 全表、Role Lens 会审、Full Gates 常读灌进 compose 会话。
2. **每次 Soft 只 JIT 一个 pointer**（细则可在同一文件内展开；禁止并行灌第二份编排/门禁全文）：
   - 媒体子任务 → `references/multimodal.md`
   - Grill 调研 → `references/compose-token.md`（研究卡与证据包；完整 R1 模板仅用户要前置包时再读 handoff）
   - Implement 模态测 → `references/multimodal.md` Universal Gates / 对应模态卡
3. **跳过 Step 2–6**；不建 Spec/worktree/Finish/独立 Review。
4. 点名 `/compose-next` 且无独立 Soft 请求 → **只** compose-next，engine 不加载。

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

## Token ROI 记录（人工）

| 会话 | Soft 类型 | 读过的 ref | 粗估 token | 结论质量 | 备注 |
|---|---|---|---|---|---|
| | | | | | |

目标：同等完成质量下 token **不升**（相对无纪律双编排或灌全协议）。
