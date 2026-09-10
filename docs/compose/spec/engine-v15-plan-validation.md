---
feature: engine-v15-plan-validation
status: in-progress
updated: 2026-09-13
branch: optimize/v1.5-plan-validation
commits: 7ee8c48..<head>
---

# Engine v1.5.0 Plan Validation

## Report

## [S1] Problem

v1.5.0（Lean Gates）主张：完成率接近 v1.4.2、效率接近 v1.2、且与 compose-next 强互补。该主张目前只有方案文本，没有按可检查验收标准做过验证。需要在实施前给出 **PASS / PASS+AMENDMENTS / FAIL**，并锁定实施前必须修正的设计缺口。

## [S2] Design

### 验收维度（三门全过才算方案可实施）

| 门 | 名称 | 通过定义 |
|---|---|---|
| **C1** | 强互补 | compose-next 独占能力不被 engine 复制；任一场景不双载编排层；P-domain 让位保留 |
| **C2** | 效率≈v1.2 | T0/T1 无强制双表/双开放问/常开 SC 巡检；主体预算 ≤110 行 / ≤3000 字符；默认不读全量 quality-gates |
| **C3** | 稳定≈v1.4.2 | 风险信号触发后仍能拦「假完成/strained coherence」；存在未验区时必须披露；Reflect 准入防错误经验写入 |

### 互补对照表（验证用）

| 能力 | compose-next | engine v1.3 现状 | v1.5 计划 | 判定 |
|---|---|---|---|---|
| Worktree 所有权 | 独占 | 无 | 不引入 | C1 保持 |
| Spec 生命周期 | 独占 | 无 | 不引入 | C1 保持 |
| 独立 Review 子代理 | 独占 | 无 | 不引入 | C1 保持 |
| Finish/合并收尾 | 独占 | 无 | 不引入 | C1 保持 |
| 点名让位 | 进入条件 | 有 | 保持 | C1 保持 |
| P-domain 建议让位 | 接手 | 有 | 保持 | C1 保持 |
| DoD/证据/No Fake Done | Spec acceptance | Quality Gates | Lean Gates 信号触发 | 共享原则，合同不同 |
| Role Lens / 多模态 | 无 | 有 | 保留 | E-domain 独占 |
| 单编排层 | 有 | 有 | 有 | C1 |

### 效率合同（v1.5 相对 v1.4.2 的削减）

1. T0/T1：DoD ≤1 行；证据 ≤1 条；不强制验证掩码表；不强制 Open×2。
2. T2：DoD 勾选行；掩码仅当存在未验区时 1 句；SC 仅信号触发。
3. Dual Agreement：仅关键结论。
4. Lean Gates 放 `quality-gates.md` 文首；SKILL 主体只留 1 行指针；无信号不读细则。
5. **禁止**把 SC-1..5 / 五元组表格写进 SKILL 主体。

### 稳定合同（不得为效率砍掉的硬点）

1. SC-1：说出「风险/该测」→ 必须补证或标未验。
2. Verification skip：改完零验证称完成 → 阻塞。
3. No Fake Done：阻塞/部分完成必须显式。
4. Reflect 写入 checklist：≥2 次同类 + 工具证据 + 责任侧。
5. P-domain 不因 Lean Gates 而静默全协议。

### 实施前必须锁定的缺口修正（AMEND）

在验证实施中若发现缺口，写入下节；实施 v1.5 前必须按 AMEND 改方案，不得原样落地。

## [S3] Out of Scope

- 本 feature **不实现** Lean Gates 全量改动（那是 v1.5 实施任务）。
- 不改 description；不改 compose-next；不删 BUILD/FIX。
- 不宣称未测的完成率百分比。

## Tasks

- [ ] T1: 产出 C1/C2/C3 证据矩阵（含场景走查 V1–V6）— acceptance: 每门有 PASS/FAIL/条件与依据行 (covers: S2)
- [ ] T2: 列出缺口与 AMEND 清单 — acceptance: 每条有「为何威胁 C1/C2/C3」与修正句 (covers: S2)
- [ ] T3: 给出总体裁定 — acceptance: PASS / PASS+AMENDMENTS / FAIL 之一，且与矩阵一致 (covers: S2)
- [ ] T4: 静态回归不回归 — acceptance: `run_static_checks.py` 0 fail（本验证不改 skill 行为时仍应 106 pass） (covers: S2)
