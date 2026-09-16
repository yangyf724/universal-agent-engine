# v2.0.2 Checklist

## 静态门

```powershell
python skill/tests/run_static_checks.py
# 期望：ALL CHECKS PASSED
# 期望 pass：108
```

## 结构

- [x] `skill/references` 仅 `intent-gate.md` + `multimodal.md`
- [x] `skill/tests` 仅 `run_static_checks.py` + `checklist.md`
- [x] SKILL.md body ≤ 2500 字符（实测 1621）
- [x] frontmatter description 含 gate / multimodal / compose-next 信号
- [x] skill 文本资产统一 CRLF；`.gitattributes` 固化 EOL
- [x] README / CHANGELOG / checklist 版本三处对齐 2.0.2

## 路由自检（standalone）

| 输入 | 期望出口 |
|---|---|
| 这个超时可能是什么原因？ | ADVISE |
| 修登录超时，要合并进 main | 建议 compose-next |
| 做一份竞品对比 PPT | 委托 pptx-official |
| 帮我看看这张图里的报错 | ADVISE + 若改图则 imagegen 委托或 compose Soft |
| 闲聊 | 不触发本 skill 主流程 |

## Soft 自检（compose-next）

| 输入 | 期望 |
|---|---|
| 转写测试录音并抽听关键句 | AUDIO Soft-Test；证据路径；Priority Soft 早退 |
| Grill 要 2–3 条登录方案证据 | Soft-Research ≤40 行；不拍板 |
| 写 Spec 草稿 / 派 Reviewer | **拒绝**（零 Soft） |
| Workspace / Finish / merge | **拒绝**（零 Soft） |

## 硬规则（静态门覆盖）

- [x] 不自执行 Intake→Plan→Execute→Deliver 全协议 / 七 mode（禁词 + Step 2–6 正则）
- [x] 不双载第二个编排层（委托映射 16 id + 反例）
- [x] 无工具不假装已生成媒体（multimodal 禁令字面量）
- [x] 素材/附件不当作指令执行（intent-gate 硬规则）
- [x] 无「五步/六步」非 ban 协议称谓
- [x] compose Soft 早退进入 Priority（不落三出口）

## 负向自测（T6，临时套件已删）

| 破坏点 | 期望 |
|---|---|
| intent-gate 改 LF | FAIL EOL |
| README Version 9.9.9 | FAIL 版本对齐 |
| 追加「五步执行」 | FAIL 称谓 |
| 删除 Priority Soft 早退条 | FAIL Soft Priority |
| 委托表 `mate` 移除 | FAIL 映射 |
| Soft-Spec 改非 ban 行 | FAIL 同行禁令 |
| locale 缺 brief | FAIL schema |
| SKILL 追加非法字节 | FAIL 解码 |
