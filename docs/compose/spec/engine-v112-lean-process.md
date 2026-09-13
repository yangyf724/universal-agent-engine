---
feature: engine-v112-lean-process
status: in-progress
updated: 2026-09-14
branch: feat/v112-lean-process
commits: f05c771..HEAD # filled at finalize
---

# Engine v1.12 — Lean Process（效率与节省率）

## Report

## [S1] Problem

R1/R2 A/B 报告（`docs/compose-next-ab-test/report.md`、`…-hard/report.md`）证明 v1.11 过程门可落地，但代价过高：

| 指标 | 无 engine | v1.10 | v1.11 | 缺口 |
|---|---:|---:|---:|---|
| Soft 面 ch（R1） | 0 | 3056 | **4079** | Soft +33.5% |
| 指令节省 vs 全协议（R1） | 85.6% | 64.5% | **57.4%** | 落后 7.1pp |
| 指令节省 vs 全协议（R2） | 59.4% | 38.3% | **31.2%** | 落后 7.1pp |
| turnCount（R2） | 32 | **25** | **40** | +60% |
| 墙钟 min（R2） | 9.0 | **6.5** | **9.8** | +51% |

根因（报告 §3/§5/§11）：

1. **过程门被做成独立仪式**：Context-7 七行表、canary 独立节、Depth 强制 4 卡，推高 Soft 指令面与执行轮次。
2. **Depth 卡「建议至少 4 张」** 与情境无关，coding 主路径仍强制 Contract+Drift+Verify-recipe+DoD-artifact。
3. **缺陷**：Amendment 路径只写了 `[S2b]` 章节，Spec frontmatter 缺 `amended:` 键（R2 §8 残留）。
4. **过程分天花板**（三臂 8/8）：效率维未惩罚「为过门而加轮」。

目标：**节省率超越 v1.10 并尽量接近无 engine；效率（轮次/墙钟）超越 v1.10**；保留 v1.11 过程可证能力；修 `amended:` 缺陷。

## [S2] Design

### 2.0 不变量

- 不改 compose-next 本体；Workspace / Finish **零 Soft**；同任务单编排层；body ≤2880。
- 保留：SC 软停、canary 概念、fan-out 默认 0 + Independence test、Soft 所有权边界。
- 禁止：LLM-judge 平台、伪造生产错误率、新开 Soft 阶段卡。

### 2.1 D1 — 过程门 = 交付附证，不是额外阶段

| 门 | v1.11 | v1.12 |
|---|---|---|
| Context-7 | 七行表常填 | **默认一行** `C1–C7: OK \| gaps: …`；仅出现 gap 时才列缺失维 |
| canary | 独立章节 | **Soft-Evidence 表一行** `canary\|PASS/FAIL/未设\|…` |
| SC 软停 | 触发规则 | **保持**（已便宜且高价值） |
| 过程分 | 四维可复填 | **保持**；`efficiency` 维明确惩罚「为过门而加轮」 |

**合同**：过程门 **不得** 要求额外 Soft 阶段或额外 fan-out；是交付物上的注解行。

### 2.2 D2 — Depth 卡情境触发

| 卡 | 默认 | 触发条件 |
|---|---|---|
| Soft-DoD-artifact | **默认唯一**（任一 Soft 交付） | 总是：≥1 机读证据指针 |
| Soft-Contract | 关 | 阶段 I/O 歧义 / 多输入合并 |
| Soft-Drift | 关 | 已有 Spec 且 diff 非平凡 |
| Soft-Verify-recipe | 关 | 验证命令 ≥2 或需复用 |
| Soft-Amendment | 关 | 范围曾变 |

禁止：默认要求 4 张 Depth 卡；禁止把「未触发」写成 FAIL。

### 2.3 D3 — 压缩 Soft 指令面

| 文件 | v1.11 体量 | v1.12 目标 |
|---|---:|---:|
| `process-gates.md` | 2114 ch | **≤1400** |
| `compose-phases.md` | 6044 ch | **≤5200** |
| `compose-token.md` | 2718 ch | **≤2300** |
| `process-audit.md` | 1185 ch | **≤1100**（efficiency 注记 ≤1 句） |
| Soft 相关合计 | ~12061 | **≤10000**；目标接近 v1.10 tag 合计 6222 的**供给路径**口径 |

供给路径口径（compose Soft 单次 JIT）：

- coding 会话默认读：`compose-token` 硬规则+fan-out 压缩表 + `compose-phases` 当前阶段卡 +（仅触发时）单张 Depth 卡。
- **禁止** 一次灌 process-gates 全文 + 全部 Depth 卡 + 全质量表（R1/R2 pack 膨胀根因）。
- `tests/token-roi.md` 增补 **Pack-size 行**：记录 Soft 包 ch/tok 与相对 v1.10/无 engine 的节省率。

### 2.4 D4 — 缺陷修复

1. **`amended:` 键**：Soft-Amendment 草稿模板必须含 frontmatter 片段建议：
   ```text
   amended: YYYY-MM-DD
   ```
   并附加式章节（`## Amendment A#` 或 `[S#b]`）+ 任务勾选同步。宿主写盘；Soft 不 commit。
2. **反例**：「只写 Amendment 章节、不建议 `amended:`」→ 纠正。
3. **process-audit efficiency 0 分定义**追加：为过门强制独立七行表/多卡导致可避免轮次膨胀。

### 2.5 D5 — 效率合同（相对 v1.10）

| 门槛 | 定义 | 验收 |
|---|---|---|
| E1 Soft 包 | 同类 compose 模拟包 Soft 面 **≤3056 ch**（v1.10） | 源文件压缩 + pack 生成指引 |
| E2 默认 Depth | coding 默认 **0** 张情境 Depth（仅 DoD-artifact 行内） | 文档合同 + 场景 |
| E3 过程门轮次 | 过程信号是注解，不新增 Soft 阶段 | process-gates/phases 合同句 |
| E4 节省率方向 | Soft 相关引用体量下降；token-roi 汇总行更新 | 静态 + 文档 |

**不得**在本轮伪造「已超越 v1.10 轮次」的生产 A/B 数字；用协议合同 + 体量静态证明方向，并标明生产 e2e 仍 OPEN。

### 2.6 文件职责

| 文件 | 动作 |
|---|---|
| `docs/compose/spec/engine-v112-lean-process.md` | 本规格 |
| `skill/references/process-gates.md` | 压缩；一行预检；canary 行内 |
| `skill/references/compose-phases.md` | Depth 情境化；压缩；Quality 表与卡对齐 |
| `skill/references/compose-token.md` | fan-out 表压缩；Soft 供给路径纪律 |
| `skill/tests/process-audit.md` | efficiency 惩罚句 |
| `skill/tests/token-roi.md` | Pack-size / 节省率汇总行 |
| `skill/tests/scenarios.md` | S75–S77（情境 Depth / 一行 C7 / amended: 键） |
| `skill/tests/run_static_checks.py` | 新断言 + 基线 |
| `skill/tests/checklist.md` | 期望 pass 数 |
| `CHANGELOG.md` / `README.md` | 1.12.0 |
| `docs/compose/smoke/v1.12-lean-process-matrix.md` | 体量+契约矩阵 |
| `SKILL.md` | 默认不改 description；至多 Soft 指针微调 |

### 2.7 验收门

| 门 | 定义 |
|---|---|
| L1 边界 | 不改 compose-next；Workspace/Finish 零 Soft；body≤2880 |
| L2 体量 | process-gates≤1400；compose-phases≤5200；compose-token≤2300；静态 0 fail |
| L3 效率合同 | 默认 0 情境 Depth；C7 一行；canary 行内；过程门无额外阶段 |
| L4 缺陷 | Soft-Amendment 含 `amended:` 建议；场景与静态覆盖 |
| L5 质量不回退 | 既有 Soft DoD / fan-out 默认 0 / SC / canary 概念仍在 |

## [S3] Out of Scope

- 修改 compose-next 本体。
- 生产 compose 会话 LLM 计费 token / 线上错误率 A/B。
- 自动 LLM-judge 平台。
- fan-out>0 实跑（研究 2–4、盲测 1）。
- 重写 description / 加词堆路由。
- engine 接管 Workspace/Finish/Review/Spec 生命周期。
- 声称「生产效率已超越 v1.10」（无 e2e 计时则禁止）。

## Tasks

- [ ] T1: Workspace 分支就绪 — acceptance: `feat/v112-lean-process` 可改且从 v1.11.0 起 (covers: S2)
- [ ] T2: 压缩 process-gates / compose-phases / compose-token 并落 D1–D3 合同 — acceptance: 体量达标；一行 C7；情境 Depth；canary 行内 (covers: S2)
- [ ] T3: 修 Soft-Amendment `amended:` + process-audit efficiency 惩罚 + token-roi pack-size — acceptance: 模板含键；场景 S75–S77 (covers: S2)
- [ ] T4: 静态检查与基线 — acceptance: `run_static_checks.py` 0 fail；checklist 对齐 (covers: S2)
- [ ] T5: smoke `v1.12-lean-process-matrix.md` 体量与契约矩阵 — acceptance: L1–L5 可勾；未验区 1 句 (covers: S2)
- [ ] T6: 独立评审 0 critical — acceptance: 评审记录；critical 已修或有据驳回 (covers: S2)
- [ ] T7: Finalize 规格 + CHANGELOG/README 1.12.0 — acceptance: status delivered；Report 三段 (covers: S2)
