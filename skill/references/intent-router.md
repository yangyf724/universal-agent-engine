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

## Multi-Dimension Decision (D1–D3)

| 维 | 决策 |
|---|---|
| D1 主产物 | BUILD / FIX / RESEARCH / DESIGN / WRITE / OPERATE / ADVISE |
| D2 模态叠加 | VISION / AUDIO / DOCOFFICE / VIDEO / THREE_D / INTERACTIVE |
| D3 技能边界 | 本编排层 vs compose-next vs official/专项（见下） |

### D3 技能边界（互补让位 + 三角色）

engine 是 compose-next 的能力同伴，不是子流程。细则与包模板：`references/compose-handoff.md`。

| 信号 | 行为 |
|---|---|
| 点名 `/compose-next` 或「用 compose-next 流程」且无独立 Soft 请求 | 只走 compose-next；本 skill 不加载全协议 |
| 会话已在 compose-next/P-domain + 独立子任务（媒体/调研/Spec 草稿/证据/Review 输入/Report 草稿） | **Soft**：只读 `compose-phases.md` 对应卡或 `multimodal.md`；跳过 Step 2–6 |
| compose Grill/P 决策 + 调研/论文/高星仓/选型 | **Soft-Research**：研究卡 + 证据包（≤40 行）；不拍板 |
| compose Implement/Verify + UI/音视频/图/交互待测 | **Soft-Test**：测试卡；高风险可 1 盲测（默认关）；不宣布总 Verify |
| compose Workspace / Finish | **排除**：永不建 worktree / Finish；引导 compose-next |
| P-domain（git 多步 + 要合并/发版/规格）且**无**前置输入 | **不**进 Step 2–6；一句建议 `/compose-next …`；等确认 |
| P-domain + 先要调研/选项/验收草案，或点名喂 Grill/Spec | **R1**：RESEARCH/DESIGN/WRITE → compose-ready 包 → 再建议 `/compose-next` |
| E-domain（研究/方案本体/写作/Office/媒体/答疑/非 git） | **R2**：正常 D1 路由（多模态可叠加） |
| 用户「直接修 / 不用 compose-next / without spec」 | **R3**：轻量 BUILD/FIX 等 |
| 单文件 Office/PDF；GitHub 建仓/同步 | 委托 official / github-sync |

**不变量**：不引入 worktree / Spec 生命周期 / Finish / 独立 Review；Review 只供输入包；Soft 时禁止再展开全编排；无 compose 上下文的独立多模态 → **R2 全协议**（勿误 Soft）。细则：`compose-phases.md` / `compose-handoff.md`。

## Role Lens（决策透镜，非多智能体）

用户以角色口吻提出时切换对应透镜，仍走同一套 Step。**禁止**多角色并行发言或 MAS 会审；同句多角色只激活一个 Lens。评审/QA Lens 时 Verify 门禁加严（证据与 No Fake Done 必过）。

| 角色 | 强调 | 偏向 |
|---|---|---|
| 需求方 / 产品经理 | D1 范围约束 | Intake、ADVISE、DESIGN 范围 |
| 架构师 / 方案负责人 | D1 DESIGN + D3 边界 | 备选、风险、非目标 |
| 工程师 | D1 BUILD/FIX | 可运行、回归 |
| 研究员 / 分析师 | D1 RESEARCH + D2 输入 | 来源、交叉验证 |
| 作者 / 编辑 | D1 WRITE | 结构、受众 |
| 数据 / 运营执行 | D1 OPERATE + D2 DOCOFFICE | 可打开文件、抽检 |
| 评审 / QA | Verify 门禁 | 证据、No Fake Done |

例：「你是架构师，评审这个方案」→ 架构师 Lens + DESIGN + 质量门禁。
