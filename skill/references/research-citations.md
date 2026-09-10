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

## Skill Packaging & Token Efficiency (2026)

| 来源 | 可操作结论 |
|---|---|
| arXiv:2603.29919 SkillReducer | description/body 双阶段压缩；actionable vs supplementary；less-is-more；限制 reference 注入体积 |
| arXiv:2608.27338 MoRe | 多角色用单智能体透镜，避免 MAS token 膨胀 |
| arXiv:2607.14275 Context Fails First | 上下文七维预检：角色清晰/护栏/指令一致/工具 schema/grounding/注入/token |
| arXiv:2608.09290 OpenCodeReview | 确定性 dispatch + 有界工具，优于自由探索 |
| arXiv:2605.00410 Agent Capsules | 合并调用需质量门禁；盲目扩 context 有害 |
| arXiv:2607.02911 CoACT | 观察压缩须保持下一动作 |
| arXiv:2607.17528 Token ROI | 同等质量下比 token/成本 |
| arXiv:2604.03088 SkVM | 跨 harness 技能编译有价值（本 skill 暂不引入） |

## How to Refresh This Skill

1. 用 `websearch`/`webfetch` 检索 agent reliability / context engineering / prompt optimization 新进展。
2. 优先采信：arXiv 正式论文、官方工程博客、高星维护仓库。
3. 将**可操作**的新机制写入 SKILL.md 或 quality-gates，而不是堆砌引用。
4. 更新本文件的来源表，注明日期。
