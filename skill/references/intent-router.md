# Intent Router — 语句分析与模式选择

按用户原话中的**动词与产物期望**路由，不要只看行业名词。

## Priority

1. 用户显式指定模式（「先做调研」「只写文档」）→ 服从
2. 明确动词 + 期望产物 → 主 mode
3. 模糊 → ADVISE，给简短可执行建议；若建议可直接落地，升级为对应 mode
4. 多 mode → 按最终交付物定主 mode，过程嵌入副 mode

## Mode Cards

### BUILD
- 触发：做/实现/开发/写代码/新建/上线/部署/写接口/build/implement/ship/feature
- 输入：需求描述、仓库路径、技术栈
- 过程：读现状 → 骨架 → 实现 → 运行/测试 → 交付
- DoD 示例：功能可运行；关键路径测试通过；无未处理编译错误

### FIX
- 触发：修bug/纠错/重构/优化性能/报错/失败/不工作/bug/性能差/崩溃/fix/debug/refactor/optimize
- 输入：错误信息、复现步骤、相关文件
- 过程：复现 → 定位根因 → 最小修复 → 回归验证 → 说明根因
- DoD 示例：原复现不再失败；未引入新失败；根因可解释

### RESEARCH
- 触发：调研/分析/对比/研究/报告/综述/文献/竞品/research/analyze/survey
- 输入：问题、范围、时间窗、可信源偏好
- 过程：问题定义 → 多源检索 → 交叉验证 → 结构化结论 → 来源列表
- DoD 示例：关键论断有来源；冲突信息被标明；结论可行动

### DESIGN
- 触发：方案/架构/设计/流程/规划/评审/plan/design/architecture/blueprint
- 输入：目标、干系人、约束、现状
- 过程：目标与约束 → 备选路径 → 推荐方案 + 取舍 → 落地步骤/风险
- DoD 示例：方案可执行；约束被覆盖；风险与开放问题列出

### WRITE
- 触发：写文档/写报告/文案/合同/邮件/PRD/说明书/write/draft/document
- 输入：受众、目的、素材、格式与长度
- 过程：大纲 → 成稿 → 事实/逻辑/格式自检 → 终稿
- DoD 示例：结构完整；无自相矛盾；格式符合要求；引用可核对

### OPERATE
- 触发：做PPT/做Excel/做Word/PDF/数据表/报表/deck/spreadsheet/可视化/pptx/xlsx/docx
- 输入：数据源、模板偏好、页数/字段
- 过程：按对应 office skill 流程；生成后视觉抽检
- DoD 示例：文件可打开；关键页/单元格正确；无缺页缺列

### ADVISE
- 触发：怎么做/是什么/帮我解释/值不值得/咨询/建议
- 输入：问题本身
- 过程：直接回答 → 给下一步行动；避免空泛长文
- DoD 示例：先给结论；给 1–3 个可执行下一步

## Ambiguity Rules

| 情况 | 选择 |
|---|---|
| 「帮我做个分析报告」 | RESEARCH + WRITE |
| 「把数据做成周报PPT」 | OPERATE（内部可先 RESEARCH 抽取要点） |
| 「系统老是超时，顺手出个优化方案」 | FIX → DESIGN |
| 「看看这个仓库能不能用」 | RESEARCH（技术尽调） |
| 「完成报告」（仅写文档） | WRITE；「调研并出报告」→ RESEARCH（主）+ WRITE |
| 「看图识别/改图/生成海报」 | 主 mode 按产物（RESEARCH/WRITE/BUILD）+ VISION 叠加 |
| 「转写录音/做会议纪要」 | WRITE（主）+ AUDIO；仅配音成片 → OPERATE + AUDIO |
| 「做视频/分镜成片」 | BUILD/OPERATE 按产物 + VIDEO 叠加；无工具则脚本+分镜 |
| 「建 3D 场景/3D 网站」 | BUILD（主）+ THREE_D 叠加 |
| 「交互演示/可拖动图表」 | INTERACTIVE 叠加；内嵌 sci-widget，不落独立 html 除非用户要文件 |
| 无产物、纯聊天 | 不触发本 skill 主流程 |

## Multimodal Notes

- 多模态是叠加层，**不增加第八 mode**；主 mode 仍由最终交付物决定。
- 输入有图/音/视频/PDF 时先 `Modality Scan`，详见 `references/multimodal.md`。
- 工具不可用时降级并披露，禁止虚构媒体文件。

## Self-invocation Check

执行前用一句话自检：  
「用户最终要的是 ______（文件/代码/方案/结论/修复/媒体/交互）。」  
填不出来 → 用 ADVISE 或问一个关键问题。
