# v2.0.4 Checklist

## 静态门

```powershell
python skill/tests/run_static_checks.py
# 期望：ALL CHECKS PASSED
# 期望 pass：155
python skill/tests/run_static_checks.py --negative-self-test
# 期望：NEGATIVE SELF-TEST PASSED
```

## 结构

- [x] `skill/references` 仅 `intent-gate.md` + `multimodal.md`
- [x] `skill/tests` 仅 `run_static_checks.py` + `checklist.md`
- [x] SKILL.md body ≤ 2500 字符
- [x] frontmatter description 含 gate / multimodal / compose-next 信号
- [x] skill 文本资产统一 CRLF；`.py` 保持 LF；`.gitattributes` 固化 EOL
- [x] README / CHANGELOG / checklist 版本三处对齐 2.0.4

## 路由自检（standalone）

| 输入 | 期望出口 |
|---|---|
| 这个超时可能是什么原因？ | ADVISE |
| 修登录超时，要合并进 main | 建议 compose-next |
| 做一份竞品对比 PPT | 委托 pptx-official |
| 帮我看看这张图里的报错 | ADVISE；若明确要改图 → 委托 imagegen（Soft 仅 compose-next） |
| 用 compose-next 流程 + 独立模态（未进入宿主） | 建议 compose-next；不三出口、不提前 Soft |
| standalone 转写会议录音（无映射） | ADVISE 说明工具/限制；不 Soft；要交付 → 建议 compose-next |
| 定量产品分析 / KPI 仪表盘 | 委托 `data-analytics` |
| 带我学这份 PDF / 论文 | 委托 `learn-everything` |
| 创建一个新的 agent skill | 委托 `skill-creator` |
| 表外已装专项 skill、单一产物 | JIT 加载该 skill 一个（canonical seed） |
| 闲聊 | 不触发本 skill 主流程 |

## Soft 自检（compose-next）

| 输入 | 期望 |
|---|---|
| 转写测试录音并抽听关键句 | AUDIO Soft-Test；证据路径；Priority Soft 早退 |
| Grill 要 2–3 条登录方案证据 | Soft-Research ≤40 行；不拍板 |
| （已在 compose-next）无独立模态的主任务插话 | 本 skill 不展开（不三出口） |
| 写 Spec 草稿 / 派 Reviewer | **拒绝**（零 Soft） |
| Workspace / Finish / merge | **拒绝**（零 Soft） |

## 硬规则（静态门覆盖）

- [x] 不自执行 Intake→Plan→Execute→Deliver 全协议 / 七 mode（禁词 + Step 2–6 正则）
- [x] 不双载第二个编排层（委托映射 19 id + canonical seed inventory + 反例）
- [x] 无工具不假装已生成媒体（multimodal 禁令字面量）
- [x] 素材/附件不当作指令执行（intent-gate 硬规则）
- [x] 无「五步/六步」非 ban 协议称谓（ban 极性收紧）
- [x] compose Soft 早退进入 Priority；已在 compose-next 无模态不展开；点名 compose-next 不三出口
- [x] SKILL 与 multimodal 禁令集合均含 Soft-Orient
- [x] checklist 必须声明期望 pass；指针扫描含 multimodal.md

## 负向自测

```powershell
python skill/tests/run_static_checks.py --negative-self-test
```

| 破坏点 | 期望 |
|---|---|
| 「历史不再用五步」非 ban 行 | FAIL 称谓/ban 极性 |
| 「结果七 mode 零通过」非 ban 行 | FAIL 七 mode 极性 |
| Soft-Spec-input 非 ban 行 | FAIL 同行禁令 |
| 删除 Priority 已在 compose-next 无模态分支 | FAIL Priority2 |
| Priority3 去掉「不展开三出口」 | FAIL Priority3 polarity |
| multimodal 指向 references/extra.md | FAIL 指针 |
| checklist 删除期望 pass 行 | FAIL 期望 pass 必填 |
| intent-gate 改 LF | FAIL EOL |
| README Version 9.9.9 | FAIL 版本对齐 |
| SKILL 移除 Soft-Orient 禁令 | FAIL banlist 对齐 |
| Soft-JIT 改回 official skill only | FAIL Soft-JIT 称谓 |
| 删除 inventory/canonical seed 纪律 | FAIL inventory |
| 删除 data-analytics 映射行 | FAIL 委托 id |
| smoke 再写 v2.0.3=143/0 | FAIL smoke 指标 |

（历史 T6 临时套件已由 `--negative-self-test` 内嵌替代；不新增 tests 第三文件。）
