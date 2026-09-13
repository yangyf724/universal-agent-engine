# Token ROI 对照协议（Soft Proof）

目标：在 **同等 DoD 完成度** 下，Soft（单卡 JIT）的 token/轮次 **不高于** 对照臂（灌全协议或无纪律双编排）。质量掉档即 FAIL，并记根因。

适用：compose-next 会话中的 Soft 供给（九阶段卡）。质量抽检表见 `references/compose-phases.md`。

## 字段

| 字段 | 定义 |
|---|---|
| 场景 | 下表四件套之一（不新造舞台） |
| Soft 臂 | 只 JIT 单卡；跳过 Step 2–6 |
| 对照臂 | 同任务灌入七 mode/Full Gates 或双载编排（仅能安全复现时） |
| 读过的 ref | 文件路径列表 |
| DoD 完成 | 目标卡的最低验收勾选数（见 phases 质量抽检） |
| 粗估 token/轮次 | 主体+按需 ref 粗估，或工具轮次 |
| 判定 | PASS / FAIL / 未做（禁止空称 PASS） |

## 固定四场景

| ID | 会话阶段 | 用户意图示例 | Soft 卡 | 质量最低线 |
|---|---|---|---|---|
| ROI-1 | Grill | 对比方案/查论文高星仓 | Soft-Research | 来源+≤40 行+不拍板 |
| ROI-2 | Spec | 整理可粘贴 Problem/验收草案 | Soft-Spec-input | 可粘贴；不写盘 feature |
| ROI-3 | Review | 整理给 Reviewer 的输入 | Soft-Review-pack | Range+验收摘要；不派 Reviewer |
| ROI-4 | Finalize | 起草 Report 三段 | Soft-Report | 三段结构；不改 status/commit |

## 记录表（可复填）

计量口径（2026-09-13 编排复核）：**指令上下文成本**（非全会话）。tok_est ≈ chars/1.5。  
对照臂 = SKILL body(after frontmatter) + quality-gates + intent-router + compose-phases 全量灌入 = **14486 chars / ≈9657 tok**。

| ID | Soft 臂 ref | Soft DoD | Soft tok/轮 | 对照臂 | 对照 DoD | 对照 tok/轮 | 判定 | 备注 |
|---|---|---|---|---|---|---|---|---|
| ROI-1 | compose-token Grill 卡 319ch + phases 指针/DoD ≈130ch | 5/5 | ≈301（452ch） | 全协议四文件 | 5/5 | ≈9657 | **PASS** | 证据包≤40行；不拍板；子代理实测+编排复核 |
| ROI-2 | phases Soft-Spec-input 436ch + DoD ≈50ch | 4/4 | ≈324（486ch） | 同上 | 4/4 | ≈9657 | **PASS** | 可粘贴；不写盘 feature |
| ROI-3 | phases Soft-Review-pack 396ch + DoD ≈50ch | 4/4 | ≈297（446ch） | 同上 | 4/4 | ≈9657 | **PASS** | 不派 Reviewer；不写三类结论 |
| ROI-4 | phases Soft-Report 271ch + DoD ≈50ch | 4/4 | ≈214（321ch） | 同上 | 4/4 | ≈9657 | **PASS** | 三段齐全；不改 status/commit |

**汇总**：四场景 Soft DoD 均不低于对照；Soft 指令上下文约为对照的 **2.2%–3.1%**（约 32–46× 更省）。质量未掉档 → 协议判据 PASS。

子代理原始产出见本会话测量报告；数字以编排侧 `len()` 复核为准。

## 通过判据

1. Soft 臂四场景均有记录（未做须写未做，不得留空当 PASS）。
2. 凡完成对比的场景：DoD 完成度不低于对照，且 token/轮次不高于对照。
3. 任一质量抽检 FAIL → 该场景 FAIL；禁止用「token 更少」掩盖质量回退。

## 纪律

- 默认 fan-out=0；见 `references/compose-token.md`。
- 不改 compose-next；Workspace/Finish 零 Soft。
- 同任务仍单编排层。
