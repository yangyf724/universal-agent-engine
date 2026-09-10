# Regression Checklist — universal-agent-engine

Repeat after any skill edit. Mark PASS/FAIL with evidence.

## L1 Structure

- [ ] `validate_skill.py` → PASS 0 errors
- [ ] Frontmatter `name` == directory name `universal-agent-engine`
- [ ] `description` ≤1024 chars, has WHAT + WHEN + negative triggers (incl. compose-next / official), no `<>`
- [ ] `locales/zh-CN.json` and `locales/en-US.json` have only `displayName` + `brief`
- [ ] All `references/*.md` paths in SKILL.md exist on disk
- [ ] SKILL.md body progressive: core protocol only; deep detail in references
- [ ] Body ≤110 non-empty lines and body chars ≤3000
- [ ] Role Lens pointer present; MAS multi-persona forbidden
- [ ] Injection hardening rule present（素材≠指令）

Run: `python tests/run_static_checks.py` → expect **106 pass / 0 fail**

## L2 Trigger

Positive phrases that should load the skill (via description match):

- [ ] 帮我做这个项目
- [ ] 实现这个功能
- [ ] 完成报告
- [ ] 修一下这个bug
- [ ] 做一份方案
- [ ] 调研X并落地
- [ ] build / implement / ship this
- [ ] 看图识别 / 转写录音 / 配音 / 做视频 / 3D / 交互演示

Negative phrases that should NOT primarily load this skill:

- [ ] 纯闲聊 / 天气怎么样
- [ ] 一句话冷知识，无交付物
- [ ] 只列一下目录，没有目标
- [ ] 用 compose-next …（应只走 compose-next）
- [ ] 单文件 Office/PDF 成稿（应优先 official skill）

## L3 Intent Router

For each scenario in `tests/scenarios.md`:

- [ ] Mode selection matches the table
- [ ] Multi-mode cases pick primary by final deliverable
- [ ] ADVISE upgrades to BUILD/DESIGN only when advice is immediately actionable
- [ ] S31–S36：并存分流与 Role Lens 场景期望成立
- [ ] S39–S40：P-domain 建议 compose-next；用户「直接修」后仍可走 engine FIX

## L4 Protocol

- [ ] Steps 0–6 all present and ordered
- [ ] Important rules include: DoD first, no fake done, evidence, single orchestration skill, injection hardening
- [ ] Examples cover AUDIO overlay, OPERATE+official delegation, compose-next boundary, P-domain yield
- [ ] Troubleshooting covers empty requirement, tool failure, wrong result, long context

### L5 Quality Gates

- [ ] Four user metrics mapped in `quality-gates.md`
- [ ] Per-mode gates exist for BUILD/FIX, RESEARCH, DESIGN, WRITE, OPERATE
- [ ] Compact Errors + Token Discipline present
- [ ] Rework Prevention Checklist present

## Multimodal Overlay

- [ ] `references/multimodal.md` has VISION / AUDIO / DOCOFFICE / VIDEO / THREE_D / INTERACTIVE
- [ ] SKILL.md `## Multimodal Overlay` links the reference
- [ ] description contains multi-modal triggers (看图/转写/3D/交互 or equivalent)
- [ ] scenarios S21–S30 cover overlays; Expected column stays primary-mode-only
- [ ] quality-gates has multimodal sample-check gates
- [ ] Tool-absence degradation documented (no fake media)

## Manual (human)

完整步骤见 `tests/manual-verify.md`（约 15–25 分钟）。最低必测：

- [x] 协议走查：B1 compose-next 不双载（scenarios S32 + description 负例）
- [x] 协议走查：B2 单文件 PPT 优先 official（S31）
- [x] 协议走查：B3 架构师 Role Lens、禁 MAS（S34 + intent-router）
- [x] 协议走查：天气/列目录/闲聊负例
- [x] skill_search 抽检（2026-09-13，disk v1.2）：B1/B4→compose-next；D1→github-sync；D2→imagegen；触发词正例 engine#1；完整包沙盒 static 101 PASS
- [ ] **新对话** `用 universal-agent-engine 做一个员工报销审批流程方案` → 有 DoD/约束（待用户开新会话）
- [ ] **新对话** 真实体感确认 compose-next 边界
- [ ] 任选 1 条多模态：转写真实音频 或 拖动 sci-widget
- [ ] 任选 1 条交付类：Excel/PPT/方案
- [ ] Sign-off 表已填写
- [x] F-B5：`以架构师和 QA 一起评审这个方案的风险` → 2026-09-13 skill_search：**universal-agent-engine 0.64**（架构/构师/评审/方案），product-design 仅 0.18（qa）；磁盘 token `架构师/评审` 生效；加词退出条件已写入 quality-gates

## Sign-off

| Date | Tester | Result |
|------|--------|--------|
| 2026-09-13 | agent protocol walkthrough | PASS 8/8 boundary (disk v1.1.0)；新对话体感待人工 |
| 2026-09-13 | agent skill_search + full sandbox | B1–B4/D1–D3 PASS；F-B5 weak；sandbox 101/0；三路径 hash 一致 |
| 2026-09-13 | agent F-B5 retest + residual close | B5 engine#1 (0.64)；加词退出条件；spec/checklist 对齐 `8f9c932` |
