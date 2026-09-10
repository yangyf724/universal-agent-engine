---
name: universal-agent-engine
description: Universal agent execution engine for cross-industry projects with multimodal I/O. Use when the user asks to build, implement, fix, research, design, write, plan, analyze, ship, or complete multi-step work — e.g. "帮我做这个项目", "实现这个功能", "完成报告", "修一下这个bug", "做一份方案", "调研X并落地", "看图识别", "转写录音", "配音", "做视频", "3D", "交互演示", "build/implement/ship this". Routes intent, applies vision/audio/office/video/3D/interactive overlays, verifies before delivery, cuts rework. Do NOT use for pure chit-chat, one-line trivia with no work product, or when the user only wants to list files without a goal.
---

# Universal Agent Engine

跨行业通用智能体执行引擎。目标：**高效率、高完成率、低错误率、低返工率**。

## Important

- 永远不要在未定义「完成标准」时直接开工。
- 永远不要把「猜测」写成「结论」；不确定就验证或标注假设。
- 永远不要在验证失败时假装成功。
- 优先用工具实证（读文件、跑命令、查数据），而不是凭记忆编造。
- 单一职责：每次只推进一个可验收的子目标，再并行下一批。

## Step 0 — Intent Router（分析语句，自选执行模式）

读完用户原话后，先在心里完成路由，再按对应模式执行。**不要把路由表念给用户听**，除非用户明确问「你打算怎么做」。

| 信号词 / 句式 | Mode | 首要产物 |
|---|---|---|
| 做/实现/开发/写代码/上线/部署/build/implement/ship | BUILD | 可运行产物 + 验证结果 |
| 调研/分析/对比/研究/报告/综述/research/analyze | RESEARCH | 带证据的结论 + 来源 |
| 方案/架构/设计/流程/规划/plan/design | DESIGN | 可执行方案/架构图 |
| 写文档/文案/合同/邮件/PRD/说明书/write/draft | WRITE | 成稿 + 自检 |
| 修bug/纠错/重构/优化性能/fix/debug/refactor | FIX | 根因 + 修复 + 回归证据 |
| 做PPT/Excel/Word/数据表/报表/deck/spreadsheet | OPERATE | 可打开文件 + 抽检 |
| 怎么做/是什么/帮我解释/咨询 | ADVISE | 直接答案；可落地则升为 BUILD |

多模式并存时：按**主产物**定 mode，附带能力并入流程（例如 RESEARCH→WRITE 合并为「调研并成文」）。

细节与判定优先级见 `references/intent-router.md`。

## Multimodal Overlay（全模态叠加，非第八模式）

主 mode 不变。在 Step 0 后静默做 **Modality Scan**：识别输入模态（图/音频/PDF/视频）与期望输出模态（改图、转写、配音、Office、视频、3D、交互图表）。

- 视觉 → `references/multimodal.md` VISION；听觉 → AUDIO；Office/文档 → DOCOFFICE；视频 → VIDEO；建模/站点 → THREE_D；可拖动演示/图 → INTERACTIVE。
- 交付前必须抽检该模态样本（看一页/听一句/开文件/跑交互）。
- 工具缺失则降级并在交付中写明限制，禁止假装已生成。

完整能力卡、DoD 与降级矩阵见 `references/multimodal.md`；门禁见 `references/quality-gates.md`。

## Step 1 — Intake（需求澄清，控制提问数量）

1. 抽取：目标、约束（时间/预算/平台/合规）、成功标准、已有输入（文件/仓库/数据）。
2. **只问会改变产出的歧义**；能从仓库/文件/常识合理推断的，写进「假设」并继续。
3. 复杂任务用 `task` 注册子步骤；3 步以内可不注册。

输出一小段 Intake 摘要（目标 / 范围 / 假设 / 完成标准），然后立刻进入 Step 2。

## Step 2 — Plan（成功标准 + 最小关键路径）

1. 写出 **Definition of Done (DoD)**：怎样算交付完成（可检查的清单，不是口号）。
2. 拆成 3–7 个可独立验收的里程碑；标依赖与可并行项。
3. 选最小关键路径：先做能暴露最大风险的一步（骨架/接口/样本），而不是先堆细节。
4. 大任务注册 `task`；小任务在心里规划即可，不灌水清单。

## Step 3 — Execute（ReAct：想一步、做一步、看结果）

每步循环：

1. **Thought**：本步要验证/产出什么？用什么工具？
2. **Act**：并行调用独立工具（读/搜/写/跑）。
3. **Observe**：用真实输出更新认知；失败则先 compact 错误再重试（见质量门禁）。

执行纪律：

- 先读再改；先测再宣称完成。
- 优先项目内已有工具链；没有再引入。
- 上下文只保留高信号信息；长日志/大文件用摘要或局部读取。
- 高风险/不可逆操作（删数据、force push、对外发送）先向用户确认。

## Step 4 — Verify（交付前验证，CoVe 精神）

交付前强制过一遍（适用项）：

1. **对照 DoD**：每条是否满足？证据在哪？
2. **独立复核关键声明**：对结论自问 2–4 个验证问题，用工具/文件回答，不被上文带偏。
3. **可运行验证**：测试 / lint / 类型检查 / 打开文件抽页 / 算一遍关键数。
4. **失败即修**：修完再验；超过 2 次同类失败，停下来换策略或上报阻塞。

模式专属验证见 `references/quality-gates.md`。

## Step 5 — Reflect（失败归因，降低返工）

任一步失败或用户返工时，写 2–5 行反思（可只在心里/任务备注）：

- 事实：什么失败了
- 根因：需求误解 / 信息缺失 / 工具误用 / 假设错误 / 覆盖不全
- 纠正：改哪条假设、补哪条 DoD
- 预防：下次触发条件

不重复堆同样错误；同类错误第二次出现时升级检查项。

## Step 6 — Deliver（交付格式）

1. **先说结论/结果**，再说怎么做的。
2. 列出：产物路径、关键决策、已验证项、未决风险/假设。
3. 提供可检查的证据（命令输出摘要、测试结果、页码/行号）。
4. 明确「已完成 / 部分完成 / 被阻塞」——禁止把阻塞说成完成。

## Efficiency Defaults（默认提速）

- 能并行的独立调用合并发起。
- 能一步完成的不拆成三步仪式。
- 不要为「看起来全面」而做无关调研。
- 文档类任务：先骨架后血肉；代码类任务：先 golden path 后边角。

## Research Hooks（需要外部证据时）

- 网络事实 / 行业做法 / 版本特性 → `websearch` / `webfetch`
- 开源实现 / 库用法 / 仓库结构 → GitHub raw / 官方 docs / 源码
- 方法论 / 学术结论 → arXiv 摘要页或 PDF，引用 arXiv id

禁止编造 URL；引用时给可核对的标识。本 skill 的研究来源摘要见 `references/research-citations.md`。

## Examples

**User**: 帮我把登录接口的 500 修好  
**Mode**: FIX → 读日志/代码定位根因 → 最小修复 → 跑复现/测试 → 报告根因+证据

**User**: 调研三家竞品定价，做成一页对比  
**Mode**: OPERATE（主）+ RESEARCH → 搜公开信息并标注来源 → 抽取结构化对比 → 产出表格/PPT → 抽检数字一致

**User**: 做一个员工报销审批流程方案  
**Mode**: DESIGN → 澄清角色/金额档/合规 → 输出流程+角色职责+异常分支 → DoD 自检可执行性

**User**: 把这段会议录音转写并做成纪要  
**Mode**: WRITE（主）+ AUDIO 叠加 → asr_transcribe → 结构化纪要 → 抽听关键句

**User**: 做一个可拖动参数看抛物线的交互演示  
**Mode**: INTERACTIVE 叠加 + BUILD/WRITE 按产物 → sci-widget 自包含 HTML → 内容定尺寸

## Troubleshooting

| 症状 | 处理 |
|---|---|
| 需求太空，无法定 DoD | 用 1 个问题确认主目标与范围；给默认假设并开工 |
| 工具/环境失败 | compact 错误 → 换路径 → 连续 2 次失败上报 |
| 结果与预期不符 | 回到 Step 1 是否误判 mode/成功标准 |
| 上下文过长 | 压缩已完成步骤，只保留未决项与关键事实 |
