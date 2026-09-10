# Research Citations — 本 skill 的方法论来源

设计本引擎时综合了公开论文、开源指南与工程实践。执行任务时若需对外引用学术结论，请回到原文核对。

## Core Algorithms Encoded in the Protocol

| 机制 | 来源 | 落地位置 |
|---|---|---|
| 推理与行动交替 (ReAct) | arXiv:2210.03629 | Step 3 Execute |
| 失败后言语反思 (Reflexion) | arXiv:2303.11366 | Step 5 Reflect |
| 多路径探索 (Tree of Thoughts) | arXiv:2305.10601 | 难任务 DESIGN 时可列备选 |
| 验证链降幻觉 (CoVe) | arXiv:2309.11495 | Step 4 Verify |
| 采样投票提升可靠性 (Agent Forest) | arXiv:2402.05120 | 关键判断可做多方案对比 |
| 长程任务与真实环境难度 | arXiv:2307.13854 WebArena | 强制验证，不轻信「看起来完成」 |
| 提示技术分类学 | arXiv:2406.06608 The Prompt Report | 技术选型参考 |

## Engineering Sources

| 来源 | 要点 |
|---|---|
| Anthropic — Effective context engineering for AI agents (2025-09) | 高信号 token、just-in-time 检索、compaction、结构化笔记、子代理 |
| humanlayer/12-factor-agents | 拥有 prompt/上下文/控制流；压缩错误；小而专注的智能体 |
| dair-ai/Prompt-Engineering-Guide | CoT、self-consistency、RAG、工具使用等经典技术索引 |
| promptslab/Awesome-Prompt-Engineering | 论文与工具清单的导航入口 |
| OpenAI Cookbook — chat formatting | system/user 角色、少样本示例模式 |
| Multimodal prompting / SoM / audio-LLM 实践 | arXiv:2310.11441 等；落地为 VISION/AUDIO 叠加，不在主路由抢 mode |

## How to Refresh This Skill

1. 用 `websearch`/`webfetch` 检索 agent reliability / context engineering / prompt optimization 新进展。
2. 优先采信：arXiv 正式论文、官方工程博客、高星维护仓库。
3. 将**可操作**的新机制写入 SKILL.md 或 quality-gates，而不是堆砌引用。
4. 更新本文件的来源表，注明日期。
