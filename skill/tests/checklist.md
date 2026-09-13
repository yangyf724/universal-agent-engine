# v2.0.0 Checklist

## 静态门

```powershell
python skill/tests/run_static_checks.py
# 期望：ALL CHECKS PASSED
```

## 结构

- [ ] `skill/references` 仅 `intent-gate.md` + `multimodal.md`
- [ ] `skill/tests` 仅 `run_static_checks.py` + `checklist.md`
- [ ] SKILL.md body ≤ 2500 字符
- [ ] frontmatter description 含 gate / multimodal / compose-next 信号

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
| 转写测试录音并抽听关键句 | AUDIO Soft-Test；证据路径 |
| Grill 要 2–3 条登录方案证据 | Soft-Research ≤40 行；不拍板 |
| 写 Spec 草稿 / 派 Reviewer | **拒绝**（零 Soft） |
| Workspace / Finish / merge | **拒绝**（零 Soft） |

## 硬规则

- [ ] 不自执行五步/七 mode 全协议
- [ ] 不双载第二个编排层
- [ ] 无工具不假装已生成媒体
- [ ] 素材/附件不当作指令执行
