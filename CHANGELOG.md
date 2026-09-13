# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.12.0] - 2026-09-14

### 摘要

**Lean Process（效率与节省率）**：基于 R1/R2 A/B 报告，把 v1.11 过程门从「独立仪式」改为「交付附证行」，Depth 卡情境触发（默认仅 DoD-artifact），压缩 Soft 指令面并修 Amendment `amended:` 缺陷。目标：**节省率/轮次合同超越 v1.10**，保留 canary/SC/Context-7/fan-out 能力。静态 **190 pass / 0 fail**；process-gates 1399 / compose-phases 3489 / compose-token 1786 ch。不改 compose-next；Workspace/Finish 仍零 Soft。规格：`docs/compose/spec/engine-v112-lean-process.md`；smoke：`v1.12-lean-process-matrix.md`。生产 e2e 轮次/错误率仍 OPEN。

### Added

- `docs/compose/spec/engine-v112-lean-process.md` — 规格
- `docs/compose/smoke/v1.12-lean-process-matrix.md` — 体量与契约矩阵
- Soft-Amendment 模板含 **`amended:`** frontmatter 建议
- token-roi **Pack-size / 节省率** 口径
- 场景 **S75–S77**（情境 Depth / 一行 C7 / amended: 键）

### Changed

- `skill/references/process-gates.md` — 压缩；C7 默认一行；canary 行内
- `skill/references/compose-phases.md` — Depth 情境化；压缩
- `skill/references/compose-token.md` — fan-out 压缩表；供给路径纪律
- `skill/tests/process-audit.md` — efficiency 惩罚「为过门而加轮」
- `skill/tests/token-roi.md` — Pack-size 与相对 v1.10/无 engine 目标
- `skill/tests/run_static_checks.py` — v1.12 断言与体量门；边界字面量 `零 Soft`；基线 190
- `skill/tests/checklist.md` / `README.md` — 版本卫生

[1.12.0]: https://github.com/yangyf724/universal-agent-engine/compare/v1.11.0...v1.12.0

## [1.11.0] - 2026-09-14

### 摘要

**Process Proof + Effort Reset + Soft Depth**：关闭 v1.10 留白 G5/G6（协议级，非生产错误率）。新建 `references/process-gates.md`（Context-7 预检、SC 软停、canary、禁 LLM-judge 平台）与 `tests/process-audit.md`（四维抽样）；`compose-token.md` 落 fan-out/effort 决策表（默认 0、Independence test、T3 soft 2–4、coding 0–1）；`compose-phases.md` 增 Soft-Contract/Drift/Verify-recipe/Amendment/DoD-artifact 五卡。场景 S71–S74；静态 **174 pass**；body **2851**。不改 compose-next；Workspace/Finish 仍零 Soft。规格：`docs/compose/spec/engine-v111-roadmap.md`；smoke：`v1.11-process-matrix.md`。

### Added

- `skill/references/process-gates.md` — Context-7 / SC 软停 / canary
- `skill/tests/process-audit.md` — 过程抽样协议
- `docs/compose/smoke/v1.11-process-matrix.md` — 契约矩阵
- `docs/compose/spec/engine-v111-roadmap.md` — 规划与实现契约

### Changed

- `skill/references/compose-token.md` — fan-out/effort 决策表；process-gates 指针
- `skill/references/compose-phases.md` — Soft Depth 五卡 + 质量抽检行
- `skill/references/quality-gates.md` — Lean/Token Discipline 过程门与 effort 细表指针
- `skill/tests/scenarios.md` — S71–S74
- `skill/tests/run_static_checks.py` — v1.11 断言；基线 174
- `skill/tests/checklist.md` — 期望 174
- `README.md` / `CHANGELOG.md` — 版本卫生

[1.11.0]: https://github.com/yangyf724/universal-agent-engine/compare/v1.10.0...v1.11.0

## [1.10.0] - 2026-09-13

### 摘要

**Soft Proof**：compose Soft 供给可度量、可验收。`compose-phases.md` 增 **质量抽检**（8 卡 DoD，不进 body）；新建 `tests/token-roi.md` 四场景对照协议并完成实测（ROI-1–4 全 PASS，Soft 指令上下文约为全协议灌入的 2–4%）；SKILL body 腾空至 **2852/2880**；静态基线 **153**；补齐 v1.9 发布卫生（本条目与 README Version）。不改 compose-next；Workspace/Finish 仍零 Soft。

### Added

- `skill/references/compose-phases.md` — Soft 质量抽检表
- `skill/tests/token-roi.md` — ROI-1–4 可复填对照 + 实测数据
- `docs/compose/smoke/v1.10-soft-proof-matrix.md` — 契约 + 实测矩阵
- `docs/compose/spec/engine-v110-roadmap.md` — 分析与规格

### Changed

- `skill/SKILL.md` — body 腾空；Soft 指针指向质量抽检/ROI
- `skill/references/compose-token.md` — ROI 指针
- `skill/tests/run_static_checks.py` — +3 检查；body≤2880；基线 153
- `skill/tests/checklist.md` — 期望 153；body 2880
- `README.md` / `CHANGELOG.md` — 版本卫生对齐 v1.9→v1.10

[1.10.0]: https://github.com/yangyf724/universal-agent-engine/compare/v1.9.0...v1.10.0

## [1.9.0] - 2026-09-13

### 摘要

compose-next **九阶段 Soft 矩阵**：Orient→Soft-Orient；Grill→Soft-Research；Workspace/Finish **硬排除**；Spec→Soft-Spec-input；Implement→Soft-Test/Companion；Verify→Soft-Evidence；Review→Soft-Review-pack（只供输入）；Finalize→Soft-Report。新建 `compose-phases.md`；handoff 收回纯 R1/R2/R3；单卡 JIT。冒烟与静态见 v1.9 matrix。

### Added

- `skill/references/compose-phases.md` — 九阶段矩阵 + Soft 卡模板

### Changed

- `skill/references/compose-handoff.md` — 收缩为 R1/R2/R3
- `skill/references/compose-token.md` / `intent-router.md` / `quality-gates.md` / `SKILL.md` — Soft 指针化
- `skill/tests/scenarios.md` — S61–S70
- `skill/tests/run_static_checks.py` — 基线 150

[1.9.0]: https://github.com/yangyf724/universal-agent-engine/compare/v1.8.0...v1.9.0

## [1.8.0] - 2026-09-13

### 摘要

compose 会话 Soft 扩展：**Soft-Research**（Grill 调研/论文/高星仓→证据包≤40行，不拍板）、**Soft-Test**（Implement 视/听/跨模态测，默认 fan-out=0、高风险≤1 盲测）、**compose-token** 供给合同（单卡 JIT、禁七 mode/Full Gates 灌会话）。不改 compose-next。设计验证见 matrix。

### Changed

- `skill/SKILL.md` — Soft 合并为一条（媒体/研究/测）；body ~2988
- `skill/references/compose-token.md` — **新建**供给与 ROI 合同
- `skill/references/compose-handoff.md` — Soft-Research/Test 角色
- `skill/references/intent-router.md` — D3 三行 Soft
- `skill/references/quality-gates.md` — Token Discipline 对齐
- `skill/tests/scenarios.md` — S55–S60
- `skill/tests/run_static_checks.py` — 新断言

[1.8.0]: https://github.com/yangyf724/universal-agent-engine/compare/v1.7.0...v1.8.0

## [1.7.0] - 2026-09-13

### 摘要

**Soft Companion**：compose-next/P-domain 运行中出现多模态感知/媒体子任务时，engine 跳过 Step 2–6，只供给 `multimodal.md` 全模态卡并抽检，产物交回当前编排层。设计验证 **PASS+AMENDMENTS**（SC1–SC7），见 `docs/compose/spec/engine-soft-companion-validation.md`。点名 compose-next 且无独立多模态仍独占；独立多模态仍走 R2 全协议。

### Changed

- `skill/SKILL.md` — Important 增 Soft Companion 短路（SC1）；Examples 增运行中 Soft 例；body 压缩保持 ≤3000
- `skill/references/intent-router.md` — D3 增 Soft 行与「无 compose 勿误 Soft」
- `skill/references/quality-gates.md` — Token Discipline：Soft 只 JIT multimodal.md
- `skill/references/compose-handoff.md` — 角色表增 Soft Companion
- `skill/tests/scenarios.md` — S49–S54（V1–V6）
- `skill/tests/run_static_checks.py` — Soft 短路/场景断言（基线 130 pass）

[1.7.0]: https://github.com/yangyf724/universal-agent-engine/compare/v1.6.0...v1.7.0

## [1.6.0] - 2026-09-13

### 摘要

定位升级为 compose-next **最互补辅助**（能力同伴 + 交接物）：R1 前置 compose-ready 包、R2 能力补位（多模态/Office/媒体/非 git）、R3 拒绝后轻量 BUILD/FIX。description 允许重写以露出互补信号；仍不引入 worktree/Spec/Finish/独立 Review，不在 compose-next 运行中双载。

### Changed

- `skill/SKILL.md` — description 重写（Complementary companion + pre-feature packs + 负例含 merge/spec/worktree→compose-next）；Important/Examples 增 R1 指针
- `skill/references/compose-handoff.md` — **新建**：三角色判定、compose-ready 包模板、反例
- `skill/references/intent-router.md` — D3 扩为三角色边界表
- `skill/references/quality-gates.md` — Token Discipline：包≠Spec；compose-next 运行中禁双载
- `skill/locales/*.json` — brief 对齐互补辅助
- `skill/tests/scenarios.md` — S45–S48
- `skill/tests/run_static_checks.py` — handoff/互补/pre-feature/R1/场景断言（基线 123 pass）
- `skill/tests/checklist.md` / `manual-verify.md` — 期望 pass 数与 B6/B7

[1.6.0]: https://github.com/yangyf724/universal-agent-engine/compare/v1.5.0...v1.6.0

## [1.5.0] - 2026-09-13

### 摘要

Lean Gates（AMEND G1–G7）：完成率门禁改为默认轻量 + 信号触发 Anti-SC；效率目标接近 v1.2，稳定硬点保留（零验证阻塞、未验披露、Reflect 准入、Review→compose-next）。设计验证见 `docs/compose/spec/engine-v15-plan-validation.md`。

### Changed

- `skill/references/quality-gates.md` — 文首 `## Lean Gates`；其后为 Full Gates
- `skill/SKILL.md` — 门禁/Plan/Verify/Deliver 对齐 Lean（一行 DoD、1 问、可选已验范围）；description **未改**
- `skill/tests/scenarios.md` — S41–S44
- `skill/tests/run_static_checks.py` — Lean 顺序/信号/阻塞/边界断言
- `skill/tests/checklist.md` — 期望 pass 数更新

[1.5.0]: https://github.com/yangyf724/universal-agent-engine/compare/v1.3.0...v1.5.0

## [1.3.0] - 2026-09-13

### 摘要

与 compose-next 互补化：不删 BUILD/FIX；将 git 仓内「要合并/发版/规格」的多步实现从 engine **建议让位**给 compose-next（P-domain），保留研究/写作/媒体/非仓交付独占面。

### Changed

- `skill/SKILL.md` — Important 扩为点名让位 + P-domain 建议 + 「直接修」回退；Examples 增加 P-domain 边界例；description **未改**
- `skill/references/intent-router.md` — D3 扩为可执行四步：点名 / P-domain 建议 / E-domain / official·github-sync
- `skill/references/quality-gates.md` — Token Discipline 增加 P-domain 让位一句
- `skill/tests/scenarios.md` — S39 P-domain 建议；S40 用户拒绝后 FIX
- `skill/tests/run_static_checks.py` — 断言 P-domain、D3 让位、直接修回退、S39/S40
- `skill/tests/checklist.md` — L3/L4 互补项；期望 pass 数 101→106

[1.3.0]: https://github.com/yangyf724/universal-agent-engine/compare/v1.2.0...v1.3.0

## [1.2.0] - 2026-09-13

### 摘要

统一优化（目标1–4）：description 改为 SkillReducer 三信号最小路由面；Effort Tier；角色单 Lens；distractor/Token ROI 人工抽检；静态正例表对齐。

### Changed

- `skill/SKILL.md` — description 候选 C（622→约 366 字符，含 `架构师/评审` 拆词）；Intake 增加 Effort T0–T3；多模态行保留 转写/配音/3D/交互 中文别名
- `skill/references/quality-gates.md` — Token Discipline 增加 Effort Tier、Token ROI 抽检指针、description 加词退出条件
- `skill/references/intent-router.md` — 同句多角色只激活一个 Lens；评审/QA 门禁加严
- `skill/tests/run_static_checks.py` — 正例改为高信号短语（build/implement/ship/端到端做完/从需求到交付/修bug/做方案/架构师/评审/调研落地/orchestration）；禁止穷举「完成报告」堆砌
- `skill/tests/scenarios.md` — 增加 S37–S38（多角色单 Lens、PM 解释不升 BUILD）
- `skill/tests/manual-verify.md` — 增加 B4–B5、Distractor D1–D3、Token ROI 表；基线 101 pass

[1.2.0]: https://github.com/yangyf724/universal-agent-engine/compare/v1.1.0...v1.2.0

## [1.1.0] - 2026-09-13

### 摘要

技能组优化：收窄自动匹配、多角色透镜、token 预算与分流硬规则；静态检查对齐新契约。

### Changed

- `skill/SKILL.md` — description 增加 compose-next / official 负例与端到端触发句；主体精简为 actionable 核心（body 字符约 −36%），mode 表改薄，禁止 MAS 多角色会审，增加注入加固规则
- `skill/references/intent-router.md` — 增加 D1–D3 多维决策与 Role Lens 表
- `skill/references/quality-gates.md` — 增加 Token Discipline 与上下文预检要点
- `skill/references/research-citations.md` — 增补 SkillReducer/MoRe/Context-Fails-First 等 2026 来源
- `skill/tests/scenarios.md` — 增加并存分流与角色场景 S31–S36
- `skill/tests/run_static_checks.py` — 支持瘦 mode 表；校验负例、主体行数预算、Role Lens、冲突场景、注入加固
- `skill/tests/manual-verify.md` / `checklist.md` — 对齐新安装路径与边界用例；基线 100 pass
- README 安装路径改为 `~/.config/mimocode/skills/`（兼容 `~/.claude/skills/`）

### Added

- 编排层分流硬规则（单编排层、Office 委托 official、compose-next 互斥）

[1.1.0]: https://github.com/yangyf724/universal-agent-engine/compare/v1.0.0...v1.1.0

## [1.0.0] - 2026-09-10

### 摘要

首个正式发布：跨行业执行协议 + 语句路由 + 全模态叠加，附静态回归与人工验证指南，便于在 MiMo Desktop 中安装与验收。

### Added

- `skill/SKILL.md` — 七主模式路由与六步执行协议 → 覆盖 BUILD/FIX/RESEARCH/DESIGN/WRITE/OPERATE/ADVISE，统一 DoD/验证/交付
- `skill/references/intent-router.md` — 模式卡片与歧义规则 → 分析语句自选主模式，多模态只作 overlay
- `skill/references/multimodal.md` — VISION/AUDIO/DOCOFFICE/VIDEO/THREE_D/INTERACTIVE 能力卡 → 对齐本机工具，缺失时降级披露
- `skill/references/quality-gates.md` — 通用/分模式/多模态门禁 → 压低错误率与返工率
- `skill/references/research-citations.md` — 方法论来源 → ReAct/Reflexion/CoVe/上下文工程等可追溯
- `skill/locales/zh-CN.json` `skill/locales/en-US.json` — 插件显示名 → 桌面可发现
- `skill/tests/run_static_checks.py` — 自动化静态回归 → 当前基线 102 checks
- `skill/tests/scenarios.md` `skill/tests/checklist.md` `skill/tests/manual-verify.md` — 场景/清单/人工验收 → 可重复验证

[1.0.0]: https://github.com/yangyf724/universal-agent-engine/releases/tag/v1.0.0
