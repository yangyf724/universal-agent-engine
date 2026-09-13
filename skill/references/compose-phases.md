# Compose Phases — compose-next 全阶段 Soft 供给矩阵

engine 是 compose-next 的**能力同伴**。同任务仍只加载一个编排层；compose 运行中 engine 只提供 **Soft 能力卡**，**跳过 Step 2–6**。

细则与包模板：前置 R1/R2/R3 见 `compose-handoff.md`；token 合同见 `compose-token.md`。

## 九阶段矩阵

| 阶段 | engine 角色 | 你交付什么 | 你不做什么 |
|---|---|---|---|
| **Orient** | Soft-Orient | 已知约束/工具可用性/假设掩码（≤15 行） | 不重跑全仓 Orient；不灌七 mode 表 |
| **Grill** | Soft-Research | 研究卡 + 证据包 ≤40 行 | **不替 Grill 拍板** |
| **Workspace** | — **排除** | 无 | **永不**建 worktree / 管分支 |
| **Spec** | Soft-Spec-input | 可粘贴的 Problem / DoD / Out-of-Scope / Tasks **草稿片段** | **不**写/改 `docs/compose/spec/*.md`；**不**填 status/commits/branch |
| **Implement** | Soft-Test / Soft-Companion | 测试卡；媒体子任务只 `multimodal.md` | 不写业务实现 |
| **Verify** | Soft-Evidence | 本 Soft 工作的证据表：`命令\|结果\|路径` | **不**宣布 feature 总 Verify 通过 |
| **Review** | Soft-Review-pack | 验收摘要 + diff 范围 + 验证一行表（供 compose 交给其 Reviewer） | **不**派 Reviewer；**不**出 Spec 合规/正确性结论 |
| **Finalize** | Soft-Report | What was built / Verification / Journey log **草稿片段** | **不**改 status；**不** commit feature 文档 |
| **Finish** | — **排除** | 无 | **永不** merge / PR / push / worktree remove |

## 激活与短路

1. 会话已在 compose-next / P-domain 流程。
2. 用户在对应阶段提出**独立 Soft 请求**（调研、测模态、写验收草案、汇总证据、整理 Review 输入、起草 Report）。
3. **点名 `/compose-next` 且无上述独立请求** → 只走 compose-next，engine 不加载。
4. 每次 Soft **只 JIT 一个** pointer（见 `compose-token.md`）；细则读本文件对应卡或 `multimodal.md`。
5. Soft 一律**跳过 Step 2–6**；Workspace / Finish 无 Soft 卡。

## Soft 卡模板

### Soft-Orient（Orient）

≤15 行：会话/仓内**已知**约束一句；工具可用性一句；假设 1–3 条；未验区掩码一句。不展开七 mode、不重做路由表。

### Soft-Research（Grill）

见 `compose-token.md` Grill 研究卡。产物：证据包 ≤40 行。**不拍板**。

### Soft-Spec-input（Spec）

可整段粘进 feature 文档当**输入**（不是 feature 文档本身，无 frontmatter/status/commits）：

```markdown
### Spec-input Draft
#### [S1] Problem
一句话用户可见问题。
#### Acceptance draft
- [ ] … | 验证: … | 证据: 路径/命令
#### Out of Scope
- 明确不做什么
#### Tasks draft
- T1 … — acceptance: … (covers: S1)
- T2 … — acceptance: … (depends: T1)
```

- ≤30 行；锚点用 `[S1]` 风格占位，最终编号归 compose-next Spec。
- **禁止**落盘 `docs/compose/spec/*.md` 或改已有 feature 文档。

### Soft-Test / Soft-Companion（Implement）

- 媒体子任务 → 只 `multimodal.md` + 抽检。
- 模态测 → 见 `compose-token.md` 测试卡；高风险可 ≤1 盲测（默认关）。
- 不写业务实现；不宣布 feature 总 Verify。

### Soft-Evidence（Verify）

只汇总**本 Soft 工作**的证据，供 compose 写入其 Verify 记录：

```markdown
| 命令/抽检 | 结果 | 路径/输出摘要 |
|---|---|---|
| … | PASS/FAIL/PRE-EXISTING | … |
```

- 默认 1 行 1 证据；失败必须标 FAIL/未验，禁止 Fake Done。
- **不**替代 compose 的仓库级 tests/typecheck/build。

### Soft-Review-pack（Review）

供 compose-next 派**独立 Reviewer** 的输入包（≤25 行）：

```markdown
## Review-input Pack
### Acceptance
来自 Spec/会话的可观察验收摘要。
### Range
base-sha..head-sha；workspace 路径。
### Verification summary
| cmd | result |
|---|---|
| … | PASS / FAIL / PRE-EXISTING |
### Open risks / 未验区
1 句掩码。
```

- engine **不**派子代理 Reviewer，**不**输出三类 Review 结论。
- compose 仍按其合同自备 diff 与验收；本包只降重复粘贴成本。

### Soft-Report（Finalize）

可粘进 feature 文档 `## Report` 的草稿片段：

```markdown
**What was built** — 1–3 段最终行为。
**Verification** — 命令与观察结果。
**Journey log** — ≤5 条可迁移教训。
```

- **不**改 `status: delivered`、**不**填 `commits:`、**不** commit。
- 最终写入与 Finalize commit 仍归 compose-next。

## 与 R1/R2/R3 的关系

| 路径 | 何时 | 细则 |
|---|---|---|
| **前置 / 拒绝** | 未进 compose，或用户「直接修」 | `compose-handoff.md`（R1/R2/R3） |
| **compose 运行中** | 已在 compose-next 阶段 | **本文件** Soft 卡 |
| **Token 合同** | 任何 Soft | `compose-token.md` |

## 反例

| 错误 | 纠正 |
|---|---|
| Soft-Spec-input 直接创建 `docs/compose/spec/x.md` | 只给可粘贴片段；文件归 compose-next |
| Soft-Review-pack 自己下「PASS / 符合 Spec」 | 只整理输入；结论归 compose 的 Reviewer |
| Soft-Report 把 status 改成 delivered 或 commit | 只草稿三段正文 |
| 用 Soft 回避 Workspace/Finish | 这两阶段 engine **永不**提供 |
| compose 会话灌七 mode 表 / Full Gates | 只 JIT 单卡 |
| 点名 compose-next 仍加载 engine 全协议 | 只 compose-next，除非另有独立 Soft 请求 |
