---
feature: engine-lean-gates
status: delivered
updated: 2026-09-13
branch: optimize/v1.5-lean-gates
commits: 49a3f06..bc08e32
---

# Engine Lean Gates (v1.5.0 / AMEND G1–G7)

## Report

**What was built** — 在设计验证（PASS+AMENDMENTS）之后落地 **Lean Gates v1.5.0**：`quality-gates.md` 文首默认轻量门禁（G1），SKILL 门禁/Plan/Verify/Deliver 改为默认 Lean、有信号再读 Full（G2）；验证掩码=未验区 1 句且禁止强制双表（G3）；Deliver 前 1 个开放问（G4）；T2 可选「已验范围」行（G5）；固定 SC 信号词（G6）；独立 Review/Spec/worktree/Finish 明确让位 compose-next（G7）。description 未改；P-domain/点名让位保留。目标：效率接近 v1.2、风险时仍拦假完成。

**Verification** — `python skill/tests/run_static_checks.py` → **113 pass / 0 fail**（仓库 + 双安装，SKILL.md SHA256=`A0980EC2…` 三路径一致）。body **2836 chars / 75 行**（≤3000/≤110）。独立评审 `49a3f06..bc08e32`：G1–G7 全 PASS，无 critical。

**Journey log** —
1. 先验证后实施：无 AMEND 不直接改 skill，避免「未验证实现」。
2. G1 是效率 load-bearing：Lean 节必须在 Universal 之前，否则 JIT 灌全量。
3. 默认验证从「2–4 个 CoVe 问」收成 1 证据 + 关键结论才双通路，是验证过的 C2 取舍，不是漏门禁。
4. 会话隔离仍禁 worktree add；分支 `optimize/v1.5-lean-gates` 自验证头 `49a3f06` 开出。
5. 静态 pass 数以脚本为准（113），不以手工估算。

## [S1] Problem

v1.5 设计验证裁定 **PASS+AMENDMENTS**：须先合入 G1–G7，才能在保持与 compose-next 强互补的前提下，把完成率门禁从「常开」改为「默认轻量 + 信号触发」。未合入时效率会掉回 v1.4.2（全量 quality-gates JIT），或漏掉静默 happy-path 未验披露。

## [S2] Design

### 目标行为

| 场景 | 行为 |
|---|---|
| T0/T1 | 不读 Full Gates；DoD≤1 行；证据≤1 条 |
| T2 无风险话术 | 一行 DoD 勾选 + 可选「已验: …」；不强制双表/双开放问 |
| T2 有信号词 | 读 Lean Gates：补证或未验 1 句；零验证称完成→阻塞 |
| 要独立 Review / Spec / worktree / Finish | 建议 compose-next；engine 不提供 |

### AMEND 合同（实施验收）

| ID | 落点 |
|---|---|
| G1 | `quality-gates.md` 文首 `## Lean Gates`（约 ≤15 行）；其后标 Full Gates |
| G2 | `SKILL.md` 门禁指针改为「默认 Lean Gates；有信号再读 Full」 |
| G3 | 掩码=未验区 1 句，禁止强制双表 |
| G4 | Open Verify 收敛为 Deliver 前 1 问 |
| G5 | T2 可选一行「已验范围」 |
| G6 | 信号词表固定写入 Lean Gates |
| G7 | Lean Gates 写明 Review→compose-next |

### 约束

- description 不改。
- 不引入 worktree/Spec/Finish/独立 Review。
- SKILL body ≤110 非空行且 ≤3000 字符。
- D3/P-domain/S32/S39/S40 不回归。

### 环境覆盖

隔离拦 `worktree add`；在 `optimize/v1.5-lean-gates`（base 验证头 `49a3f06`）实施。

## [S3] Out of Scope

- 改 compose-next；扩 description；删 mode。
- 未测完成率百分比宣称。
- 全任务 Dual / Open×2 / 常开 SC 五条巡检。

## Tasks

- [x] T1: quality-gates 文首 Lean Gates + Full Gates 分界 — acceptance: G1/G3–G7 措辞齐全 (covers: S2)
- [x] T2: SKILL 门禁/Plan/Verify/Deliver 指针对齐 Lean — acceptance: G2；body 预算不破 (covers: S2)
- [x] T3: scenarios + 静态断言 + checklist/CHANGELOG — acceptance: 新增场景合法；static 0 fail (covers: S2)
- [x] T4: 双安装同步 — acceptance: 仓库与双安装 SHA 一致 (covers: S2; depends: T1–T3)
