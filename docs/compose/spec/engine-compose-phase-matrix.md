---
feature: engine-compose-phase-matrix
status: delivered
updated: 2026-09-13
branch: optimize/v1.9-compose-phases
commits: 32565b6..pending
---

# Engine × compose-next 全阶段能力矩阵 (v1.9)

## Report

**What was built** — 在不改 compose-next 的前提下，把 engine Soft 供给扩展到 compose-next **九阶段**：Orient→Soft-Orient；Grill→Soft-Research；Workspace/Finish **硬排除**；Spec→Soft-Spec-input（可粘贴草稿，不落盘 feature 文档）；Implement→Soft-Test/Companion；Verify→Soft-Evidence（命令|结果|路径）；Review→Soft-Review-pack（只供输入，不派 Reviewer）；Finalize→Soft-Report（三段草稿，不改 status）。新建 `compose-phases.md`；handoff 收缩回纯 R1/R2/R3；token/router/qg/SKILL Soft 全部指针化。

**Verification** — `python skill/tests/run_static_checks.py` → **150 pass / 0 fail**；body **2991** chars / 80 非空行；三路径 SKILL SHA `A05D0B42447A…` 一致。独立评审 `32565b6..7dcdde1`：三门 MET；1 条非 critical（token JIT 将 Verify 误指 multimodal）已修并重装。

**Journey log** —
1. 「全阶段」不等于接管：Workspace/Finish 必须显式排除行，否则 Soft 会漂成第二编排。
2. Review 只能供输入包；写结论或派 Reviewer 就破坏 compose-next 所有权。
3. Soft-Evidence/Orient 必须进 JIT 指针表，否则 Verify 阶段会读错文件。
4. body 已 2991/3000，Important 只能指针化；细则永远在 references。

## [S1] Problem

v1.8 只在 compose-next 的 **Grill（Soft-Research）** 与 **Implement/Verify（Soft-Test）** 有 Soft 供给；其余阶段（Orient / Spec / Review / Finalize）无定义，会话中要么退回全协议（双编排），要么无法互补。用户要求 **engine 落实到 compose-next 所有流程环节**，且：

1. **不能改** compose-next 本体；
2. Workspace / Finish 硬护栏**永不**提供（不建 worktree、不 Finish/独立 Review 所有权）；
3. Review 阶段只供**输入包**，不派 Reviewer、不出 Review 结论；
4. 文档职责最干净：新建 `compose-phases.md` + 收缩 `compose-handoff.md` 回纯 R1/R2/R3；
5. body 仍 ≤3000 / ≤110 行；单卡 JIT；点名 compose-next 仍独占。

## [S2] Design

### 总原则（硬）

- 不改 compose-next；不让其主动 load engine。
- 同任务仍**单编排层**；compose 运行中 Soft 一律**跳过 Step 2–6**。
- 每次 Soft 只 JIT **一个** pointer（细则可同文件展开）。
- Workspace / Finish：**零 Soft**，矩阵中显式排除。
- Review：只供 Review 输入包；engine **永不**派 Reviewer / 出 Review 结论。
- Feature Spec 生命周期（status/commits/branch、写盘 `docs/compose/spec/*.md`）仍归 compose-next。

### 九阶段矩阵（`references/compose-phases.md`）

| compose-next 阶段 | engine Soft 角色 | 供给 | 禁止 |
|---|---|---|---|
| Orient | Soft-Orient | 会话内已知约束/工具可用性/假设掩码（≤15 行） | 不重跑全仓 Orient；不灌七 mode |
| Grill | Soft-Research（已有） | 研究卡 + 证据包 ≤40 行 | 不拍板 |
| Workspace | **排除** | — | 永不建 worktree / 管分支 |
| Spec | **Soft-Spec-input** | 可粘贴的 [S1]/DoD/Out-of-Scope/任务验收**草稿片段**（不落盘 feature 文档） | 不写/改 `docs/compose/spec/*.md`；不填 status/commits |
| Implement | Soft-Test / Soft-Companion（已有） | 测试卡 / 媒体子任务 | 不写业务实现 |
| Verify | **Soft-Evidence** | Soft 工作的证据表：`命令 \| 结果 \| 路径`（一行一证据） | 不宣布 feature 总 Verify 通过 |
| Review | **Soft-Review-pack** | 验收摘要 + diff 范围 + 验证一行表（供 compose 交给其 Reviewer） | 不派 Reviewer；不出 Spec 合规/正确性结论 |
| Finalize | **Soft-Report** | What was built / Verification / Journey log **草稿片段** | 不改 status；不 commit |
| Finish | **排除** | — | 永不 merge/PR/push/worktree remove |

### Soft 卡模板（同文件内）

**Soft-Spec-input**（≤30 行草稿，可整段粘进 feature 文档当输入）：

```markdown
### Spec-input Draft
#### [Sn] Problem — <一句话>
#### Acceptance draft
- [ ] … | 验证: … | 证据: …
#### Out of Scope
- …
#### Tasks draft (acyclic)
- T1 … — acceptance: …
```

**Soft-Evidence**：

```markdown
| 命令/抽检 | 结果 | 路径/输出摘要 |
|---|---|---|
```

**Soft-Review-pack**（≤25 行）：

```markdown
## Review-input Pack
### Acceptance (from Spec/conversation)
### Range
base..head + workspace path
### Verification summary
| cmd | PASS/FAIL/PRE-EXISTING |
### Open risks / 未验区
```

**Soft-Report**（Finalize 片段，仍由 compose 写入 feature 文档）：

```markdown
**What was built** — …
**Verification** — …
**Journey log** — ≤5 entries
```

### 文件职责切分

| 文件 | 职责 |
|---|---|
| `references/compose-phases.md` | **新建**：九阶段矩阵 + Soft 卡模板 + 激活/禁止 + 反例 |
| `references/compose-handoff.md` | **收缩**：只保留 R1/R2/R3 角色表 + compose-ready 包；Soft 行删除，指向 phases |
| `references/compose-token.md` | 指针改为 phases；保留 ≤40 行 / 单卡 JIT / fan-out 预算 |
| `SKILL.md` Important Soft 行 | 合并为 1–2 行指针：`compose-phases.md` + 跳过 Step 2–6 + Workspace/Finish 永不 |
| `intent-router.md` D3 | Soft 行收敛为「全阶段见 compose-phases」+ 点名独占 |
| `quality-gates.md` Token Discipline | Soft 指针改 phases |

### Body 预算

- Soft Important 行改为**指针型**（约 −40～80 chars vs 三路径枚举）。
- 新增 phases 不进 body；静态检查仍断言 body ≤3000 / ≤110 行。
- description **本轮不改**（避免路由面漂移）。

### 验收三门

| 门 | 定义 |
|---|---|
| C1 强互补 | 点名 compose-next 仍独占；九阶段均有明确供给或排除；Workspace/Finish 零 Soft；Review 不出结论 |
| C2 Token | Soft 单卡 JIT；证据包≤40 行；body ≤3000；compose 会话不读七 mode/Full Gates |
| C3 质量 | Soft-Spec-input 不落盘；Soft-Evidence 强制命令/路径；Soft-Review-pack 不派 Reviewer；禁 Fake Done |

### 证据矩阵

| ID | 场景 | 期望 |
|---|---|---|
| X1 | Grill：对比方案+论文 | Soft-Research 证据包；不拍板 |
| X2 | Spec：「帮我整理可粘贴的 Problem/验收草案」 | Soft-Spec-input 片段；不写 feature 文件 |
| X3 | Workspace：「建个 worktree」 | 排除；引导 compose-next Workspace |
| X4 | Implement：测截图+提示音 | Soft-Test；不写业务码 |
| X5 | Verify：「汇总你刚才 Soft 测的证据」 | Soft-Evidence 表；不宣布总 Verify |
| X6 | Review：「整理给 Reviewer 的输入」 | Soft-Review-pack；不派代理、不出结论 |
| X7 | Finalize：「起草 Report 三段」 | Soft-Report 片段；不改 status/commit |
| X8 | Finish：「合并/开 PR」 | 排除；compose-next Finish |
| X9 | 点名 compose-next 且无独立 Soft 请求 | 只 compose-next |
| X10 | Token | body ≤3000；单卡 JIT；不灌 Full Gates |

### 环境覆盖

会话隔离拦 `worktree add`；分支 `optimize/v1.9-compose-phases`（base `32565b6`）在主仓检出。不改 compose-next。

## [S3] Out of Scope

- 修改 compose-next 或让其内部调用 engine。
- engine 接管 Workspace/Finish/独立 Review/feature Spec 生命周期。
- 常开 MAS / 多子代理会审。
- 改 description 堆词。
- 实现新检索后端。
- 路线图 P1/P2（fan-out 预算细化、评测卡）可并入但非本 Spec 必达（本 Spec 已含 fan-out 既有约束）。

## Tasks

- [x] T1: 设计验证矩阵裁定 — acceptance: 三门结论 PASS/PASS+AMENDMENTS/FAIL (covers: S2)
- [x] T2: 新建 compose-phases.md（矩阵+卡模板）— acceptance: 九阶段齐全；排除行明确；模板可粘贴 (covers: S2)
- [x] T3: 收缩 handoff + 更新 token/router/qg 指针 — acceptance: handoff 仅 R1–R3；Soft 指向 phases；无死链 (covers: S2; depends: T2)
- [x] T4: SKILL Soft 行指针化 + body ≤3000 — acceptance: Soft 在 Step 2 前短路；Workspace/Finish 永不可见；静态 0 fail (covers: S2; depends: T3)
- [x] T5: 场景 S61–S70 + static 断言 + 双安装 — acceptance: 矩阵场景覆盖；checklist 期望数更新；仓内+双路径 SHA (covers: S2; depends: T4)
