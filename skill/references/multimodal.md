# Multimodal Plugin — 采集 + 测试 + Grill 研究

compose-next 运行中的 **Soft 能力卡**。主流程仍归 compose-next；本文件单卡 JIT，不灌全协议。

## When to Apply

会话已在 compose-next / P-domain，且出现独立子任务：

- 输入：图/截图/PDF 页/录音/视频/数据表/3D 参考
- 输出期望：改图、配音、转写、Office 产物、视频、3D、交互测
- Grill：需要调研/论文/高星仓/选型证据

## 1. Modality Scan（采集）

静默完成，不必向用户播报。

1. **输入模态**：路径/附件类型？能否用 `read` / `asr_transcribe` 打开？长音是否 ≤90s 需分段？
2. **输出模态**：用户要什么文件/体验？
3. **工具可用性**：本机工具存在则用；缺失见降级表。

### 工具锚点

| 模态 | 输入 | 输出/处理 |
|---|---|---|
| VISION | png/jpg/webp/截图/PDF 页 | `read`；改图 `image_edit`；生成 `image_gen` |
| AUDIO | wav/mp3 | 转写 `asr_transcribe`；配音 `tts_speech` |
| DOCOFFICE | 数据/大纲/素材 | 对应 `xlsx/docx/pptx/pdf-official` |
| VIDEO | 脚本/分镜/素材 | 编码工具；无则脚本+分镜 |
| THREE_D | 场景文字/参考图 | `3d-creation` 或 three.js 代码 |
| INTERACTIVE | 关系/参数/流程 | sci-widget / SVG / mermaid |

## 2. Soft-Test / Companion（测试）

不写业务实现；只做模态抽检与证据。

| 模态 | 最低抽检 | 证据形态 | 禁止 |
|---|---|---|---|
| 视觉/UI | 关键屏 1 次 | 路径+观察一句 | 只报已生成 |
| 听觉 | 关键句抽听；TTS 可播 | 命令/文件路径 | 未听称通过 |
| 跨模态 | 图=表=文数字 | 对照一句 | 不一致仍 done |
| 交互 | 可拖动/可点关键路径 | 截图或步骤结果 | 假交互 |
| Office | 可打开；关键页/单元格 | `present_files` 或路径 | 假打开 |
| 视频 | 可播；首帧/时长对齐脚本 | 路径+时长 | 未播称通过 |

通用门：

- 素材路径真实存在。
- 交付前 **≥1** 机读证据指针（`命令|结果|路径`）。
- 默认 fan-out=0；不宣布 feature 总 Verify。

## 3. Soft-Research（仅 Grill）

- **触发**：compose Grill / P 决策需要外部证据。
- **工具**：`websearch`/`webfetch`（URL+检索日）；`arxiv`（id）；仓路径一行。
- **产物**：证据包 **≤40 行**；区分事实/推断；冲突信息标明。
- **不拍板**：推荐与最终决策归 compose-next 宿主。
- 不并行扩 fan-out。

## 4. 跨模态一致门

- 图中数字 = 表中数字 = 文中数字。
- 多输入拼接顺序与用户叙述一致。
- 版本号/人名/日期跨源一致；不一致先披露再继续。

## 5. 降级表

| 能力 | 有工具 | 无工具 |
|---|---|---|
| 读图/PDF | read | 请用户描述 / 文本层 |
| 生图/改图 | image_gen / image_edit | 设计规格 + 素材指引 |
| 转写 | asr_transcribe | 分段人工流程 |
| 配音 | tts_speech | 文案脚本 |
| Office | office skills | md/csv 等价物 |
| 视频 | ffmpeg 等 | 分镜+脚本 |
| 3D | 3d-creation | three.js 代码或示意图 |
| 交互 | sci-widget / visualizer | 静态 SVG/mermaid |

**禁止**：无工具时假装已生成媒体文件。

## 硬规则

- 跳过五步/七 mode 全协议。
- 禁止 Soft-Spec-input / Soft-Review-pack / Soft-Report / 九阶段 / Soft Depth。
- Workspace / Finish **零 Soft**。
- 单卡 JIT：本次只需 Research 就只做 Research；需模态测就只做测试卡。
