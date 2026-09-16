---
feature: quality-review-v3
status: designed
updated: 2026-09-14
branch: chore/quality-review-v3
commits: 17fb8d6..HEAD
---

# Quality Review v3 — Kill All Bugs

## Report

## [S1] Problem

v2.0.1 质量加固后静态门 85/0 仍绿，但全仓复审发现检查器假绿面、契约称谓漂移、发布卫生未兑现，以及换行符不一致：

1. **路由缺口（P0）**：`intent-gate.md` Priority 只覆盖「点名 compose-next **且无**独立模态子任务 → 只 compose-next」。已点名/会话已在 compose-next **且有**独立模态子任务时，会落入三出口，可能误专项委托，而不是 Soft。硬规则虽写了「compose-next 运行中禁止三出口」，但未进入 Priority，路由可走错。
2. **发布卫生假声明（P0）**：CHANGELOG `[2.0.1]` 与 `quality-review-v2.md` 声称 README「Last sync 带 short SHA」，README 实际只有日期无 SHA。
3. **协议称谓不一致（P1）**：同一禁令对象同时写作「五步」与「Intake→Plan→Execute→Deliver」（四段箭头链）与历史「六步」；Step 禁令正则锁 `Step 2–6`。读者/模型无法判断哪一个是权威名。
4. **EOL 卫生（P1）**：`skill/references/intent-gate.md` 为 LF，`SKILL.md`/`multimodal.md`/locales/checklist 为 CRLF；无 `.gitattributes`，字节级安装一致与 Soft JIT 字节指标漂移。
5. **检查器脆弱/假绿（P1）**：BOM 用源码字面量 U+FEFF；`read_text` 无解码失败转 FAIL；`tests/` 只锁文件名忽略子目录；无 EOL 一致断言；无 README/CHANGELOG/checklist 版本对齐断言；无 checklist 期望 pass 数对齐。
6. **文档漂移（P2）**：`checklist.md` 标题仍 v2.0.0 且硬规则未勾选；smoke 报告 §5 D5 表仍写 69/0 未带 85；`quality-review-v2.md` commits 写 `385c587..HEAD` 非具体范围。

## [S2] Design

不改 v2 双角色行为语义，只修路由可判定性、称谓唯一性、检查器真值与发布卫生。

### A. Soft 路由优先级（`intent-gate.md`）

Priority 改为显式三分支，先于三出口：

1. 会话已在 compose-next / P-domain，或点名 `/compose-next`，**且**存在独立模态子任务 → Soft（`multimodal.md`），不展开三出口。
2. 点名 `/compose-next` 且无独立模态子任务 → 只 compose-next，本 skill 不展开。
3. 无产物、纯聊天 → 不触发主流程。
4. 否则三出口（ADVISE / 建议 compose-next / 专项委托）。

硬规则「compose-next 运行中禁止三出口」保留，与 Priority 1 对齐。

### B. 协议称谓唯一化

- 权威禁令名固定为：**Intake→Plan→Execute→Deliver 全协议** 与 **七 mode 表**。
- 弃用「五步 / 六步」作为协议名；反例可写「开全协议执行」。
- `run_static_checks.py` 增加：corpus 中不得出现「五步/六步」协议指称（允许出现在明确 ban 语境）。
- Step 2–6 / BUILD/FIX 正则保留（历史字面量仍禁）。

### C. 静态检查器加固（`run_static_checks.py`）

- BOM：`raw.startswith("\ufeff")`，不用源码字面量。
- `read_text`：UTF-8 解码失败 → FAIL，不抛栈。
- `tests/`：`iterdir` 全量（含目录），仅允许 `run_static_checks.py` + `checklist.md`。
- **EOL**：`skill/SKILL.md`、两份 references、两份 locales、checklist 必须统一 CRLF；`.py` 允许 LF。
- **版本对齐**：README `Version:` == CHANGELOG 最新 `## [x.y.z]` == checklist 标题版本。
- **checklist pass 数**：checklist 声明的期望 pass 数（若写出）必须等于实跑 `SUMMARY passes=`。
- **称谓**：corpus 出现「五步/六步」且不在 ban 语境 → FAIL。
- 保留全部既有 85 断言语义；预期新增后 ≥90。

### D. 发布卫生

- README：`Version: 2.0.2`；`Last sync` 带 short SHA（交付时填 HEAD short）。
- CHANGELOG：`[2.0.2]` 记录本审查；更正 `[2.0.1]` 中「Last sync 带 short SHA」为「未兑现（见 2.0.2）」或改为事实描述。
- checklist：标题 2.0.2；结构项保持；硬规则改为「由静态门/负向自测覆盖」并勾选对应自动化项。
- smoke `v2.0.0-full-matrix-report.md` §5 D5：表内补 HEAD **85/0**，保留 tag 69/0 为历史。
- `quality-review-v2.md`：commits 改为具体 `385c587..5955f33`（或实际范围）。
- 新增根 `.gitattributes`：`* text=auto`；`skill/**/*.md` `text eol=crlf`；`*.py` `text eol=lf`。

### E. 不动

- 不改三出口信号语义（除 Soft 优先级显式化）。
- 不 retag；不删历史 docs。
- 不引入新 references/tests 文件（结构门仍 2+2）。
- 不改 locales 文案语义。

## [S3] Out of Scope

- 父仓 AGENTS.md 对齐。
- 生产 e2e / LLM 计费。
- 安装侧 `~/.config/mimocode/skills/...` 自动同步（交付说明即可）。
- worktree 隔离（本会话 `git worktree add` 被策略拦下，改用主仓分支 `chore/quality-review-v3`）。

## Tasks

- [ ] T1: 写入本规格 — acceptance: status=designed；S1/S2/S3 与任务可验收 (covers: S1)
- [ ] T2: 加固 `run_static_checks.py`（BOM/解码/tests 全量/EOL/版本/checklist pass/称谓） — acceptance: 新断言可 FAIL 负向；默认仍 ALL PASS (covers: S2C)
- [ ] T3: 修 `intent-gate.md` Soft Priority + 全仓协议称谓唯一化 — acceptance: Priority 1 为 Soft 早退；无「五步/六步」非 ban 指称 (covers: S2A,S2B)
- [ ] T4: 统一 skill EOL + `.gitattributes` — acceptance: skill 标记文件全 CRLF；检查器 EOL 断言 PASS (covers: S2C,S2D)
- [ ] T5: README/CHANGELOG/checklist/smoke/v2 spec 卫生 — acceptance: Version 2.0.2；Last sync 有 SHA；CHANGELOG 2.0.1 假声明纠正；D5 表含 85；v2 review commits 具体化 (covers: S2D)
- [ ] T6: 静态门 + 负向自测（抽 EOL/版本/称谓/Soft Priority 字面） — acceptance: 默认 ALL PASS；临时破坏可 FAIL (covers: S1,S2)
- [ ] T7: 独立 Reviewer 对照本 spec — acceptance: Spec/Correctness/Consistency 三类结论；critical 清零 (covers: S1,S2)
- [ ] T8: Finalize 本文档并提交 — acceptance: status=delivered；Report 填齐；commits 具体 (covers: S2)
