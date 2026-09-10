---
feature: engine-v15-plan-validation
status: delivered
updated: 2026-09-13
branch: optimize/v1.5-plan-validation
commits: 7ee8c48..bd492f6
---

# Engine v1.5.0 Plan Validation

## Report

**What was built** — 对会话内 v1.5.0（Lean Gates）方案做**设计验证**（未实施 skill 改动）。按三门验收：C1 与 compose-next 强互补、C2 效率接近 v1.2、C3 稳定接近 v1.4.2。证据矩阵：`docs/compose/smoke/v1.5-plan-validation-matrix.md`。裁定：**PASS+AMENDMENTS**——允许进入 v1.5 实施，但必须先合入 AMEND G1–G7。C1 PASS；C2/C3 条件通过。skill 行为未改（SKILL.md 仍 5504 B）。

**Verification** — `python skill/tests/run_static_checks.py` → **106 pass / 0 fail**。独立评审 `7ee8c48..bd492f6`：Spec 合规 T1–T4 PASS，无 critical；非 critical（标签统一、Dual「关键结论」定义）已在 Finalize 前关闭。diff 仅 2 个 docs 文件。

**Journey log** —
1. 会话隔离仍禁 `worktree add`；验证在 `optimize/v1.5-plan-validation` 分支进行。
2. 不实施 Lean Gates 只做设计验证，避免「未验证的实现」与「未实现的验证」循环。
3. G1（Lean Gates 必须在 quality-gates 文首）是 C2 的 load-bearing 条件——粗指针会 JIT 灌全量门禁。
4. 信号触发 SC 覆盖不了「无风险话术的静默 happy-path」；G5 已验范围一行是诚实折中，非假 PASS。
5. 双开放问/强制双表会把效率打回 v1.4.2；已在效率合同中禁止。

## [S1] Problem

v1.5.0（Lean Gates）主张：完成率接近 v1.4.2、效率接近 v1.2、且与 compose-next 强互补。该主张此前只有方案文本，没有按可检查验收标准验证。需要在实施前给出 **PASS / PASS+AMENDMENTS / FAIL**，并锁定实施前必须修正的设计缺口。

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
3. Dual Agreement：仅关键结论（对外数字/版本/钱数/安全与合并结论/用户点名关键）。
4. Lean Gates 放 `quality-gates.md` 文首；SKILL 主体只留 1 行指针；无信号不读细则。
5. **禁止**把 SC-1..5 / 五元组表格写进 SKILL 主体。

### 稳定合同（不得为效率砍掉的硬点）

1. SC-1：说出「风险/该测」→ 必须补证或标未验。
2. Verification skip：改完零验证称完成 → 阻塞。
3. No Fake Done：阻塞/部分完成必须显式。
4. Reflect 写入 checklist：≥2 次同类 + 工具证据 + 责任侧。
5. P-domain 不因 Lean Gates 而静默全协议。

### 实施前必须锁定的缺口修正（AMEND G1–G7）

| ID | 威胁 | 修正 |
|---|---|---|
| G1 | 粗指针 JIT 灌全量 quality-gates，效率掉回 v1.4.2 | `quality-gates.md` 文首 `## Lean Gates`（≤15 行）；其余标 Full Gates |
| G2 | SKILL「见 quality-gates.md」过笼统 | 改为：无信号默认路径；有信号再读 **Lean Gates** 节 |
| G3 | 掩码写成必填表 → 回退 v1.4.2 | 未验区存在时 **1 句**；禁止强制两表 |
| G4 | Open Verify ≥2 | Deliver 自检 **1** 个开放问，与 Dual 合并 |
| G5 | 无风险话术时静默只测 happy path | T2 交付可选一行「已验范围」 |
| G6 | SC 信号词过窄漏触发 | 固定词表：风险/该测/可能有问题/应该没问题/大概/看起来完成 |
| G7 | 误以为 engine 也应独立 Review | 文档句：要 Review → compose-next；engine 不提供 |

完整走查与证据：`docs/compose/smoke/v1.5-plan-validation-matrix.md`。

## [S3] Out of Scope

- 本 feature **不实现** Lean Gates 全量改动（那是 v1.5 实施任务）。
- 不改 description；不改 compose-next；不删 BUILD/FIX。
- 不宣称未测的完成率百分比。

## Tasks

- [x] T1: 产出 C1/C2/C3 证据矩阵（含场景走查 V1–V6）— acceptance: 每门有 PASS/FAIL/条件与依据行 (covers: S2)
- [x] T2: 列出缺口与 AMEND 清单 — acceptance: 每条有「为何威胁 C1/C2/C3」与修正句 (covers: S2)
- [x] T3: 给出总体裁定 — acceptance: PASS / PASS+AMENDMENTS / FAIL 之一，且与矩阵一致 (covers: S2)
- [x] T4: 静态回归不回归 — acceptance: `run_static_checks.py` 0 fail（106 pass） (covers: S2)
