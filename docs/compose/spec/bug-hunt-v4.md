---
feature: bug-hunt-v4
status: delivered
updated: 2026-09-18
branch: fix/bug-hunt-v4
commits: 30b7d54..c67285a  # implementation; this docs-only finalize follows
---

# Bug Hunt v4 — iterative-bug-hunter (code-only)

## Report

**What was built** — compose-next × iterative-bug-hunter 对 universal-agent-engine 做 code-only 抓 BUG 并修复。契约：`intent-gate` Priority 补全为 5 分支（Soft 仅「会话已在 compose-next/P-domain + 独立模态」；已在无模态 / 点名 compose-next → 不展开三出口）；standalone 无映射模态交付明确 ADVISE；SKILL/multimodal 禁令对齐 Soft-Orient。静态门 108→**145**：ban 极性收紧、Priority1–5 极性断言、指针含 multimodal、期望 pass 必填、Last-sync SHA 可解析、当前规格卫生、`--negative-self-test`（10 用例）。文档：v2-gate 称谓+Priority、smoke 指标序列、README/CHANGELOG 2.0.3、gitignore 工具目录。

**Verification** — `python skill/tests/run_static_checks.py` → **145/0 ALL CHECKS PASSED**。`python skill/tests/run_static_checks.py --negative-self-test` → **10/10 PASSED**。独立 Reviewer 初审 1 critical（Priority3 极性未锁）→ 已修 + N5b；复审 **critical=0 / PASS**。

**Journey log**
1. `git worktree add` 被会话隔离策略拦下；按用户选择回退为主仓分支 `fix/bug-hunt-v4`。
2. 负向矩阵先坐实 ban-context 假绿（「不再/零」通行证）与 Priority 缺口，再改检查器，避免假绿面扩大。
3. write 工具曾把 `\r` 写成字面量导致 body/frontmatter 解析失败；改为纯文本写入 + 脚本转 CRLF。
4. Windows 子进程默认 GBK 使 `--negative-self-test` 读不到 UTF-8 FAIL 文案；强制 `PYTHONUTF8`/`encoding=utf-8` 后 needle 校验才可信。
5. Review critical：Priority3 只锁「只 compose-next」不够，必须锁「不展开三出口」极性并配 N5b 负向用例。

## [S1] Problem

v2.0.2 静态门 108/0 全绿后，code-only bug-hunt 发现：Priority 与「compose-next 运行中禁止三出口」硬规则不一致；点名 compose-next + 独立模态时 Soft 激活面与 multimodal 文案分裂；检查器 ban-context/指针/期望 pass 存在假绿面；README 标为当前契约的 v2-gate 仍用「五步」且无 Soft Priority；smoke §0 权威数字停在 85/0。

## [S2] Design

### 组合关系

| 维度 | 主导 | 产物 |
|------|------|------|
| 流程/spec/review/finalize | compose-next | `docs/compose/spec/bug-hunt-v4.md` |
| 缺陷判定/quiet/degrade | iterative-bug-hunter | `.bug-hunter/REPORT.md`（本地，gitignore） |
| 冲突 | — | 流程听 compose-next；Confirmed 门槛听 bug-hunter |

### 路由契约（交付态）

1. Soft 早退：会话已在 compose-next / P-domain **且**独立模态 → Soft；不三出口。
2. 已在 compose-next 且无独立模态 → 本 skill 不展开。
3. 点名 compose-next → 只 compose-next；**不**展开三出口（模态待宿主 Soft）。
4. 无产物/纯聊天 → 不触发。
5. 否则三出口。

### 检查器

- ban 极性：禁止/不得/弃用/跳过+全协议等；裸「零/不再」不再放行。
- Priority 1–5 字面与极性均锁；结构门仍仅 2 个 tests 文件；负向模式内嵌 `--negative-self-test`。

## [S3] Out of Scope

- Web-visual / canvas / axe / 生产 LLM e2e
- 安装侧重测、worktree（策略拦下）
- 扩大三出口语义或恢复全协议

## Tasks

- [x] T1: 写入本规格 — acceptance: status 从 designed 推进到 delivered (covers: S1)
- [x] T2: Bootstrap `.bug-hunter` + 基线 108/0 (covers: S2)
- [x] T3: R1 hunt — static/meta-test/dynamic (covers: S2)
- [x] T4: Confirm/Reject 分类 (covers: S2)
- [x] T5: 修复 Confirmed 契约与文档 (covers: S2; depends: T4)
- [x] T6: 检查器加固 + `--negative-self-test` (covers: S2)
- [x] T7: 静态门 145/0 + 负向 10/10 (covers: S1,S2; depends: T5,T6)
- [x] T8: 独立 Reviewer；critical 修复后复审 PASS (covers: S1,S2)
- [x] T9: Finalize spec + REPORT + 分支提交 (covers: S2)
