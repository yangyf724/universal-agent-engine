# Process Gates — 过程可证（v1.12 Lean）

T2+ 或信号触发才 JIT。默认 Lean Gates；本文件**不**增加 Soft 阶段、**不**要求额外 fan-out。过程信号是交付物上的**注解行**。

来源：Context Fails First；Strained Coherence；PROCTOR canary；ClawTrack。

## 何时读

- T2+ 且存在未验区 / SC 信号 / 关键结论。
- Soft-DoD-artifact / Soft-Evidence 交付前自检。
- 用户要「过程抽检 / 预检 / canary」。

T0/T1 无信号不读。

## Context-7（默认一行）

与行为结果隔离。**默认**在 Deliver/Soft 交付注解：

```text
C1–C7: OK | gaps: …
```

仅出现 gap 时列出缺失维（C1 Role / C2 Guardrail / C3 Instruction / C4 Tool / C5 Grounding / C6 Injection / C7 Token）。缺 C5/C6 → 补证或标未验。**禁止**无 gap 仍填七行仪式表。

## SC 软停（Verify 后半 / Deliver 前）

触发：风险 / 该测 / 可能有问题 / 应该没问题 / 大概 / 看起来完成；或「承认冲突仍继续」。

| 观察 | 动作 |
|---|---|
| 说出风险且未补证 | **阻塞 done**；补证或强制未验 1 句 |
| 零验证称完成 | 阻塞 |
| 首旗标出现在验证后期 | 软停；换根因或上报 |

禁止把软停写成必填双表。

## Canary（确定性优先；行内）

T2+ 至少 **1** 条「若完美通过则可疑」检查，写在 **Soft-Evidence 表一行**：

```text
canary|PASS/FAIL/未设|预期失败是否发生/路径
```

任选：故意缺失应检出；应失败命令应 FAIL；数字抽算暴露不一致。完美绿且未解释 → 阻塞。无 canary 则披露「未设」。

## 过程抽样分

四维 0–2：goal / efficiency / info-use / **verify**。协议：`../tests/process-audit.md`。结构检查不能代替过程分。efficiency **惩罚**为过门而加的可避免轮次。

## Soft / compose-next 边界

- 不派 Reviewer；Review 归 compose-next。
- Soft-DoD-artifact：≥1 机读证据指针。
- Workspace / Finish 仍零 Soft。
- 禁止常开 LLM-judge 平台。

## 反例

| 错误 | 纠正 |
|---|---|
| 无 gap 仍填七行 C 表 | 一行 `C1–C7: OK` |
| canary 单开章节并加轮 | Evidence 表一行 |
| canary 全绿未解释 | 阻塞 |
| 承认风险仍标 done | SC 软停 |
| 只跑静态检查称过程 PASS | 另需 canary/证据路径 |
