---
feature: quality-review-v2
status: delivered
updated: 2026-09-14
branch: chore/quality-review-v2
commits: 385c587..5955f33
---

# Quality Review v2 + Fixes

## Report

**What was built** — 全仓多维质量审查（BUG / 检查器 / 目录 / Spec 合规 / 发布卫生）并落地全部可修项。静态门从弱 69 断言加固为 **85**（委托 16 id 全锁、ban-context 逐行、FM BOM/CRLF、locales schema、指针 body 双 ref 必达、Soft-Orient 字面禁令）。10 份 v1 spec + 7 份 v1 smoke 标为 Historical；README 相对安装路径与目录树；CHANGELOG `[2.0.1]` 注明 tag `v2.0.0` 不含 A01 多角色禁令；v2 Spec/Smoke 指标回填至 `385c587` 口径。

**Verification** — `python skill/tests/run_static_checks.py` → **85/0 ALL CHECKS PASSED**。负向自测：抽掉 `mate` 映射 / Soft-Orient 非 ban 行 / body 超预算 / 非法 locale JSON 均正确 FAIL（临时套件已删）。独立 Reviewer：T1–T7 全 Met，无 critical。

**Journey log**
1. `git worktree add` 被会话隔离策略拦下（与 v2 时相同），改用主仓分支 `chore/quality-review-v2`。
2. 批量写 Historical 横幅时 Python `'\v'` 被解析为垂直制表符，18 文件横幅损坏；改脚本修复。
3. 负向测试用 PowerShell `Get-Content/Set-Content` 破坏了 `intent-gate.md` 编码；按已知内容重写恢复（content diff 为空，仅 EOL）。
4. 委托 skill 匹配曾用裸 `in`，`mate` 会命中 `mate-gone`；改为反引号整词。
5. Soft JIT/字节指标对换行符敏感；报告已注明 CRLF 口径与测量 commit。

## [S1] Problem

v2.0.0 交付后（tag `v2.0.0` = `a186373`）又打上 A01 多角色补丁（`385c587`），静态门 69/0 仍绿，但：

1. **发布卫生**：tag 不含 A01 禁令，CHANGELOG/Spec/Smoke 仍写 body 1585/5614/19902（实际 1597/5732/20172）。
2. **检查器假绿**：ban-context 用 `any()`；委托映射只锁 8/15；frontmatter 不进禁词语料；CRLF/BOM 解析脆；locales 只查存在。
3. **目录/文档**：10 份 v1 spec 仍 `status: delivered` 且无 superseded 横幅；README 安装路径写死错误绝对路径；目录树漏 smoke/历史。
4. **契约缺口**：S2 要求禁 `Soft-Orient` 独立卡但 skill 内无字面量；compose Soft 与门控委托 Office 双载边界未写清。

## [S2] Design

修复面（不改 v2 双角色行为，只修契约锁与发布卫生）：

### A. 静态检查器加固（`run_static_checks.py`）

- FM 解析：strip BOM、规范化 `\r\n`、FM 未闭合则 FAIL。
- 禁词：`all()` 逐出现行；语料含 body+gate+multi+description；`Step\s+[2-6]\b` 词边界；统一 `BUILD\s*/\s*FIX`。
- 委托映射：16 个 skill id 全锁（含 product-design/frontend-design 双目标）。
- locales：JSON 解析 + displayName/brief + zh/en 键对齐。
- references：`iterdir` 全量，非 2 文件即 FAIL。
- 指针：要求 body 同时指向两份 refs。
- Soft 硬规则：同行上下文（禁止…Soft-Spec-input 等）。

### B. 文档契约

- `multimodal.md`：补 Soft-Orient 禁令字面量；写明 Soft 内 Office 委托为能力 JIT、不重入门控。
- README：安装用相对路径；目录树标注历史 docs；Version 含 short SHA。
- CHANGELOG：`[2.0.1]` 记录 A01 补丁与质量加固；2.0.0 条目注明 tag 基线。
- v2 Spec / Smoke：回填实测数字；commits 含 `385c587`；报告注明 A01 为 post-tag。
- 10 份 v1 spec + 8 份 v1 smoke：frontmatter `status: superseded` + 一行历史横幅。

### C. 不动

- 不 retag `v2.0.0`（破坏性；在 CHANGELOG 说明即可）。
- 不删除历史 docs（仅标记）。
- 不改三出口/Soft 行为语义。
- 不追补 v1.4 空洞版本（历史事实；CHANGELOG 加一句考古注即可）。

## [S3] Out of Scope

- 父仓 AGENTS.md 对齐（仓外）。
- 生产 e2e / LLM 计费度量。
- 外部 A/B 报告 vendoring（缺文件，仅标注 external）。
- 工作树隔离（本会话 `git worktree add` 被策略拦下，改用主仓分支）。

## Tasks

- [x] T1: 加固 `run_static_checks.py`（FM/禁词 all/委托 16/locales/指针/同行上下文） — acceptance: 全量委托映射与 Soft 同行规则有断言；故意破坏可 FAIL；默认仍 ALL PASS (covers: S2A)
- [x] T2: 补 `multimodal.md` Soft-Orient 禁令与 Office Soft 委托边界 — acceptance: 字面量与边界句存在 (covers: S2B)
- [x] T3: 标记 v1 specs/smoke 为 superseded + 历史横幅 — acceptance: 10 spec + 7 smoke 非 v2 均有 status/banner (covers: S2B)
- [x] T4: 修 README 安装路径/目录树/版本卫生 — acceptance: 相对路径可复制；树含 docs 说明 (covers: S2B)
- [x] T5: CHANGELOG 2.0.1 + 2.0.0 tag 基线注 + 1.4 考古注 — acceptance: 含 A01 post-tag 与质量修复条目 (covers: S2B)
- [x] T6: 回填 v2 Spec/Smoke 实测数字与 commits — acceptance: 1597/5732/20172 与 `385c587` 一致 (covers: S2B)
- [x] T7: 跑静态门 + 负向破坏自测 — acceptance: 默认 ALL PASS；临时破坏委托行/禁词能 FAIL (covers: S1,S2)
