# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
