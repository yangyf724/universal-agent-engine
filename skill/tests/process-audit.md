# Process Audit 抽样协议（v1.11；非 LLM-judge 平台）

用途：对已完成 feature/Soft 工作做 **廉价过程分**，滤掉 lucky pass。  
细则门禁见 `references/process-gates.md`。**不做** 自动大规模 judge。

## 字段

| 字段 | 定义 |
|---|---|
| 会话/feature | ≤1 行标识 |
| 目标 | 用户可见问题 1 句 |
| 四维分 | goal / efficiency / info-use / verify 各 0–2（总分 0–8） |
| Canary | 设了什么；按预期失败？Y/N/未设 |
| SC 软停 | 是否触发；处理（补证/未验/阻塞） |
| 证据指针 | 命令或文件路径 |
| 判定 | PASS / FAIL / 未做（禁止空称 PASS） |

## 四维评分（0–2）

| 维 | 0 | 1 | 2 |
|---|---|---|---|
| goal | 偏离用户目标 | 部分对齐 | 目标与 DoD 一致 |
| efficiency | 无关调研/重复灌协议 | 可接受 | 并行/最小路径/单卡 JIT |
| info-use | 无来源结论 | 单源或弱交叉 | 多源交叉或工具实证 |
| verify | 零验证称完成 | 仅 happy path | 主路径+canary+失败披露 |

## 通过判据（抽样轮）

1. 有记录的样本：verify 维 ≥1，且 canary∈{Y, 未设已披露}。
2. SC 触发样本必须有处理记录；未处理 → 该样本 FAIL。
3. 抽样 N≤20/轮；**禁止**把过程分说成生产错误率。

## 记录表（可复填）

| ID | 目标 | goal | eff | info | verify | canary | SC | 判定 |
|---|---|---|---|---|---|---|---|---|
| PA-1 | | | | | | | | |
| PA-2 | | | | | | | | |

## 纪律

- fan-out 默认 0；过程抽检不派 MAS 会审。
- 不改 compose-next；Workspace/Finish 不在本协议接管范围。
- 结构检查（run_static_checks）是必要不充分条件。
