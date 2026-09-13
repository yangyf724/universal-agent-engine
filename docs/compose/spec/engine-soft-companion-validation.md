---
feature: engine-soft-companion-validation
status: delivered
updated: 2026-09-13
branch: optimize/v1.7-soft-companion
commits: e6f86d9..6eb2db8
---

# Engine Soft Companion — Design Validation + Implementation (v1.7)

## Report

**What was built** — 先做设计验证裁定 **PASS+AMENDMENTS**（SC1–SC7），再落地 **Soft Companion**：compose-next/P-domain 运行中的多模态感知/媒体子任务，engine **跳过 Step 2–6**，只读 `references/multimodal.md` 并抽检，产物交回当前编排层；不建 Spec/worktree/Review。点名 compose-next 且无独立多模态仍独占；无 compose 上下文的独立多模态仍走 R2 全协议。证据矩阵：`docs/compose/smoke/v1.7-soft-companion-matrix.md`。

**Verification** — `python skill/tests/run_static_checks.py` → **130 pass / 0 fail**（实施后；三路径 SKILL SHA `d3deaf01946f…`）。独立评审 `e6f86d9..6eb2db8`：三类 PASS，无 critical。`skill_search`：点名 compose-next → 1.0 独占加载。

**Journey log** —
1. Soft load-bearing 在 SC1：无 Important 文首短路则 JIT 仍进 Step 2–6，等于双编排。
2. 点名 compose-next 必须继续独占（SC2），否则互补变抢路由。
3. Soft 只吃 multimodal.md，不 Role Lens、不 R1 包——供给面越小越安全。
4. V4 的 P-domain+截图用「媒体子任务」判定，避免整单被 Soft 吞掉。
5. body 为加 Soft 段压缩到 ≤3000；下一步改动先腾预算。

## [S1] Problem

v1.6 已做到「compose-next 之前/之外」的互补（R1 包、R2 独立多模态、R3 回退）。缺口在**运行中**：compose-next 已是编排层时，会话里出现截图/录音/视频等感知需求，当前硬规则是「不双载 engine 全协议」，于是要么吞掉多模态编排，要么把 compose-next 拖去处理非它专长的模态。目标：验证 **Soft Companion**（软同伴）是否能在不破坏单编排层的前提下，让 engine **只供给全模态卡**。

## [S2] Design

### 主张（待验证）

在 **D3 上下文自动判定** 命中时，engine 进入 **Soft Companion Mode**：跳过 Step 2–6 编排所有权，只读 `references/multimodal.md` 完成该模态任务，产物交回当前编排层（通常是 compose-next）。

### 激活合同（全部满足才软载）

| # | 条件 |
|---|---|
| A1 | 存在多模态信号：输入图/音/视频/PDF 页，或期望转写/配音/改图/3D/交互/Office 媒体产物 |
| A2 | 存在 compose 上下文：会话已在 compose-next 流程中，**或**用户点名「在 compose-next 里 / 喂给当前 feature」，**或** P-domain 语境下把媒体当子任务 |
| A3 | engine 已被加载（本次由 engine 响应），且用户**未**点名「只走 compose-next」 |

### 排他（任一命中则不软载）

| # | 条件 | 行为 |
|---|---|---|
| X1 | 点名 `/compose-next` 且未同时要 engine 多模态 | 只 compose-next |
| X2 | 无 compose 上下文的独立多模态交付 | **R2 全协议**（正常 D1+D2） |
| X3 | 纯 P-domain 实现/合并、无媒体信号 | 建议 compose-next（既有） |

### Soft Mode 供给与禁止

**供给（仅这些）**

- `references/multimodal.md`：When to Apply / 六模态卡 / Universal Multimodal Gates / Tool Absence
- 工具锚点：read / image_gen / image_edit / asr_transcribe / tts_speech / office skills / 3d-creation / sci-widget 等
- 交付：媒体文件或感知结论 + ≥1 样本抽检；路径/降级披露

**禁止**

- 不进入 Step 2–6 所有权（不自建 DoD 里程碑树、不抢 Implement/Verify 收尾）
- 不读/不执行 compose-handoff R1 包流程（除非用户改口要前置包）
- 不注入七 mode 路由表决策、不 Role Lens 会审
- 不引入 worktree / Spec / Finish / 独立 Review
- 不假装已生成媒体；工具缺失必须降级披露

### 验收三门

| 门 | 定义 |
|---|---|
| **C1 强互补** | 任一场景不双载全编排；点名 compose-next 仍独占；软载不复制 Spec/Worktree/Review/Finish |
| **C2 效率** | 软载时默认只 JIT `multimodal.md`，不读 Full Gates / 不走 R1 包 / 不展开七 mode；SKILL body 仍 ≤110 行 / ≤3000 字符 |
| **C3 稳定** | 媒体交付仍过样本抽检 + No Fake Media；未验/降级必须披露 |

### 证据矩阵

| ID | 场景 | 期望 | C1 | C2 | C3 |
|---|---|---|---|---|---|
| V1 | 「用 compose-next 修这个登录 bug」 | 只 compose-next，engine 不软载 | 必须 | — | — |
| V2 | compose-next 实现中「转写这段录音，写进测试夹具说明」 | Soft：AUDIO 卡 + 转写文件；不自建 feature Spec | 必须 | 只读 multimodal | 抽听/披露 |
| V3 | 「把这段录音转写成会议纪要」（无 compose） | 全协议 R2 WRITE+AUDIO | 不得误软载 | 正常 Lean | 抽听 |
| V4 | P-domain 修 bug，附截图「识别报错字段」 | Soft VISION 取证交回编排；或明确建议 compose-next 后在实现中软载 | 不双载 | 不读 Full | 图文一致 |
| V5 | compose-next 中「导出一页验收 PPT」 | Soft DOCOFFICE → official；不接管 feature | 不双载 | 委托 official | 可打开抽检 |
| V6 | 独立「做一个 10 页 PPT」 | R2/official，非 Soft | 非软载误伤 | — | 抽检 |

### AMEND 预案（验证若 PASS+AMENDMENTS 则实施前必合）

| ID | 内容 | 理由 |
|---|---|---|
| SC1 | Soft 判定必须写在 SKILL **Important 或 Step 0 文首**，先于 Plan 指针 | 否则 JIT 灌全协议（load-bearing） |
| SC2 | 点名 compose-next 且无独立多模态请求 → 仍独占 compose-next | 防抢路由 |
| SC3 | Soft 只供给 multimodal.md；正文一句指针，细则 JIT | 控 token |
| SC4 | Soft 仍强制样本抽检 / 禁 Fake Media / 降级披露 | C3 |
| SC5 | description 最多微调互补/软同伴语义，禁止把 `/compose-next` 写成正触发 | 路由安全 |
| SC6 | scenarios + 静态断言覆盖 V1–V6 | 回归 |
| SC7 | body 压缩保持 ≤3000 | 预算 |

### 环境覆盖

会话隔离拦 `worktree add`；分支 `optimize/v1.7-soft-companion`（base `e6f86d9`）。不改 compose-next 本体。

## [S3] Out of Scope

- 修改 compose-next，使其内部 hand-off 到 engine。
- Soft 模式注入 Spec/Worktree/Review/Finish。
- 删除 R1/R2/R3 或七主 mode。
- 未验证就改 description 堆词。
- 声称「compose-next 官方支持的多模态插件」。

## Tasks

- [x] T1: 本验证文档 + 证据矩阵裁定 — acceptance: 三门均有结论；裁定为 PASS / PASS+AMENDMENTS / FAIL 之一 (covers: S2)
- [x] T2: （若非 FAIL）按 AMEND 实施 Soft Companion — acceptance: SC1–SC7 落地；static 0 fail；V1–V6 有场景/断言 (covers: S2; depends: T1 非 FAIL)
- [x] T3: 双安装 + live 抽检 — acceptance: 三路径 SHA 一致；点名 compose-next 不双载；compose 上下文多模态可软载体感 (covers: S2; depends: T2)
