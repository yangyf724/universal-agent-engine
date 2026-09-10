# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-09-10

### 摘要

首个正式发布：跨行业执行协议 + 语句路由 + 全模态叠加，附静态回归与人工验证指南，便于在 MiMo Desktop 中安装与验收。

### Added

- `SKILL.md` — 七主模式路由与六步执行协议 → 覆盖 BUILD/FIX/RESEARCH/DESIGN/WRITE/OPERATE/ADVISE，统一 DoD/验证/交付
- `references/intent-router.md` — 模式卡片与歧义规则 → 分析语句自选主模式，多模态只作 overlay
- `references/multimodal.md` — VISION/AUDIO/DOCOFFICE/VIDEO/THREE_D/INTERACTIVE 能力卡 → 对齐本机工具，缺失时降级披露
- `references/quality-gates.md` — 通用/分模式/多模态门禁 → 压低错误率与返工率
- `references/research-citations.md` — 方法论来源 → ReAct/Reflexion/CoVe/上下文工程等可追溯
- `locales/zh-CN.json` `locales/en-US.json` — 插件显示名 → 桌面可发现
- `tests/run_static_checks.py` — 自动化静态回归 → 当前基线 102 checks
- `tests/scenarios.md` `tests/checklist.md` `tests/manual-verify.md` — 场景/清单/人工验收 → 可重复验证

[1.0.0]: https://github.com/yangyf724/universal-agent-engine/releases/tag/v1.0.0
