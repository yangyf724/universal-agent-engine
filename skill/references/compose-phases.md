# Compose Phases — compose-next 全阶段 Soft 供给

engine 是 compose-next 的**能力同伴**。同任务只一个编排层；compose 运行中只给 **Soft 卡**，**跳过 Step 2–6**。

前置包见 `compose-handoff.md`；token 合同见 `compose-token.md`；过程门见 `process-gates.md`。

## 九阶段矩阵

| 阶段 | engine 角色 | 交付 | 禁止 |
|---|---|---|---|
| Orient | Soft-Orient | 约束/工具/假设掩码（≤15 行） | 重跑全仓；灌七 mode |
| Grill | Soft-Research | 证据包 ≤40 行 | 拍板 |
| Workspace | **排除** | 无 | 永不 worktree/分支 |
| Spec | Soft-Spec-input | 可粘贴草稿片段 | 写盘 feature；填 status/commits |
| Implement | Soft-Test / Companion | 测试卡；媒体→multimodal | 写业务实现 |
| Verify | Soft-Evidence | `命令\|结果\|路径` | 宣布 feature 总 Verify |
| Review | Soft-Review-pack | Range+验收+验证表 | 派 Reviewer；三类结论 |
| Finalize | Soft-Report | What/Verification/Journey | 改 status；commit |
| Finish | **排除** | 无 | 永不 merge/PR/push |

## 激活与短路

1. 会话已在 compose-next / P-domain。
2. 对应阶段有**独立 Soft 请求**才供给。
3. 点名 `/compose-next` 且无 Soft 请求 → 不加载 engine 全协议。
4. **单卡 JIT**（见 compose-token）。
5. 跳过 Step 2–6；**Workspace / Finish 零 Soft**。

## Soft 阶段卡

### Soft-Orient
≤15 行：已知约束一句；工具一句；假设 1–3；未验掩码一句。

### Soft-Research
见 compose-token Grill 卡。证据包 ≤40 行。不拍板。

### Soft-Spec-input
可粘贴草稿（无 frontmatter/status）：

```markdown
### Spec-input Draft
#### [S1] Problem
#### Acceptance draft
- [ ] … | 验证: … | 证据: 路径/命令
#### Out of Scope
#### Tasks draft
- T1 … — acceptance: … (covers: S1)
```

≤30 行；禁止落盘 `docs/compose/spec/*.md`。

### Soft-Test / Soft-Companion
媒体 → 只 `multimodal.md`+抽检。模态测 → compose-token 测试卡。不写业务实现。

### Soft-Evidence
本 Soft 工作证据；过程注解**同行**：

```markdown
| 命令/抽检 | 结果 | 路径/摘要 |
|---|---|---|
| canary | PASS/FAIL/未设 | … |
| C1–C7 | OK \| gaps: … | 一行即可 |
```

失败标 FAIL。不替代仓库级 tests/build。

### Soft-Review-pack（≤25 行）
Range + 验收摘要 + 验证表 + 未验区。不派 Reviewer、不出三类结论。

### Soft-Report
`What was built` / `Verification` / `Journey log`（≤5）。不改 status、不 commit。

## Soft Depth（v1.12 情境触发；仍单卡 JIT）

**默认**：任一 Soft 交付只需 **Soft-DoD-artifact** 行内证据。其余 Depth 卡按下表触发；未触发 ≠ FAIL。

| 卡 | 触发 | 最低验收 | 禁止 |
|---|---|---|---|
| Soft-DoD-artifact | 默认 | ≥1 机读证据指针 | 无证据称 done |
| Soft-Contract | I/O 歧义或多输入 | 输入/输出/恢复点三行 | 接管 Workspace/Finish |
| Soft-Drift | 已有 Spec 且 diff 非平凡 | 漂移 1 句披露 | 擅自改 status |
| Soft-Verify-recipe | 命令≥2 或需复用 | ≤5 行可复跑命令 | 宣布总 Verify |
| Soft-Amendment | 范围曾变 | 见下节 | commit/写盘 feature |

### Soft-Amendment（含 amended: 键）

Finalize 前若范围曾变，草稿必须含：

```markdown
# frontmatter 建议
amended: YYYY-MM-DD

## Amendment A1  (或 [S#b] 追加节)
…变更说明…
```

并建议任务勾选同步。宿主写盘；Soft **不** commit。

## Soft 质量抽检（DoD）

| 卡 | 最低验收 | 禁止 |
|---|---|---|
| Soft-Orient | ≤15；假设/未验 | 重跑全仓 |
| Soft-Research | 来源；≤40；开放问 | 无来源结论 |
| Soft-Companion | 只 multimodal；产物可指 | 写业务实现 |
| Soft-Spec-input | 可粘贴；无 frontmatter | 写盘 feature |
| Soft-Test | ≥1 工具证据 | 只报已生成 |
| Soft-Evidence | 命令+PASS/FAIL；过程注解行 | 宣布总 Verify |
| Soft-Review-pack | Range+验收+未验 | 三类结论 |
| Soft-Report | 三段；Journey≤5 | 改 status/commit |
| Soft-DoD-artifact | ≥1 机读证据 | 无证据称 done |
| Soft-Amendment | 草稿含 `amended:` + 追加节 | commit/写盘 |

完整对照：`../tests/token-roi.md`。

## 与 R1/R2/R3

| 路径 | 何时 | 细则 |
|---|---|---|
| 前置/拒绝 | 未进 compose 或「直接修」 | `compose-handoff.md` |
| compose 运行中 | 已在九阶段 | 本文件 Soft 卡 |
| Token 合同 | 任何 Soft | `compose-token.md` |

## 反例

| 错误 | 纠正 |
|---|---|
| Soft-Spec-input 建 feature 文件 | 只给粘贴片段 |
| Soft-Review-pack 下 PASS | 只整理输入 |
| Soft-Report 改 delivered/commit | 只草稿正文 |
| 默认强制 4 张 Depth 卡 | 只 DoD-artifact；其余情境触发 |
| Amendment 只写章节不建议 `amended:` | 必须含 frontmatter 键 |
| compose 灌七 mode/Full Gates | 单卡 JIT |
| 用 Soft 回避 Workspace/Finish | 永不提供 |
