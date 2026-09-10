# Multimodal Overlay — 全模态能力卡

多模态是**叠加层**，不是第八主模式。主 mode 仍由最终交付物决定；本文件提供输入/输出模态扫描、工具锚点与验收抽检。

## When to Apply

出现下列任一信号时进入 Modality Scan（静默，不必向用户播报）：

- 输入素材：图/截图/照片/PDF 页/录音/视频/数据表/3D 参考
- 期望产物：改图、配音、转写、PPT/Word/Excel、视频、3D、交互演示/图表/架构图
- 动词：看图、识别、OCR、听录音、转写、配音、做视频、建模、3D、交互演示、可视化、生成海报/封面/示意图

## Scan Order

1. **输入模态**：用户已提供什么？路径/附件类型？能否用 `read` 打开？
2. **输出模态**：用户要什么文件/体验？
3. **主 mode**：按交付物定（OPERATE=Office 文件；BUILD=可运行 3D/Web；WRITE=转写成文；RESEARCH=看图取证分析…）。
4. **工具可用性**：本机工具存在则用；缺失则降级并写明。

禁止：无工具时假装已生成媒体文件。

---

## VISION

- **输入**：png/jpg/webp/截图/PDF 某页
- **输出**：结构化描述、信息抽取、改图、设计稿、对比结论
- **过程**：用 `read` 打开图或 PDF 页 → 按任务抽取/生成 → 需要改图用 `image_edit`；从零生成用 `image_gen` → 回读结果核对
- **DoD**：关键信息与图一致；改图保留不变量；尺寸/主体无裁切问题；无水印/AI 残留则标注
- **降级**：无视觉读能力时，要求用户描述关键内容或提供可读文本层

## AUDIO

- **输入**：wav/mp3（建议 ≤90s/段；长录音先切分）
- **输出**：转写文本、会议纪要、配音 wav/mp3
- **过程**：转写用 `asr_transcribe`；配音用 `tts_speech`（默认中文 冰糖 / 英文 Mia）→ 落盘 → 抽听关键句
- **DoD**：转写关键专名正确；长音频分段顺序正确；TTS 文件可播；play 仅短反馈句
- **降级**：无 ASR/TTS 时输出处理步骤与期望脚本，不伪造音频

## DOCOFFICE

- **输入**：数据、大纲、模板偏好、素材图
- **输出**：xlsx / docx / pptx / pdf
- **过程**：加载对应官方 skill（`xlsx-official` 等）→ 生成 → 可能时转 PDF/截图抽检 → `present_files`
- **DoD**：文件可打开；关键页/单元格正确；Office 东向字体与布局符合 skill 约定
- **降级**：无 office 运行时则交付 Markdown/CSV 等价物并说明限制

## VIDEO

- **输入**：脚本、分镜、素材、时长约束
- **输出**：mp4/mov 等可预览视频
- **过程**：有编码工具则合成；否则先交付分镜+脚本+时间轴 → 提供可运行方案
- **DoD**：文件可播；含 `-movflags +faststart`（若经 ffmpeg）；首帧可预览；时长与脚本一致
- **降级**：无视频工具链时明确「仅脚本/分镜」，不假装已渲染

## THREE_D

- **输入**：文字场景、参考图、风格锚点
- **输出**：three.js/Blender 叙事站、3D 场景、模型资产
- **过程**：命中 3D 需求时加载 `3d-creation` skill → 按其规范建模/站点 → 运行时验证
- **DoD**：按 3D skill 标准；可打开/可交互；无外部死链资源
- **降级**：无 Blender/渲染环境则交付代码级 three.js 方案或 ASCII/示意图

## INTERACTIVE

- **输入**：关系/参数/流程，需要用户拖动观察
- **输出**：```sci-widget``` 内嵌交互、SVG 静态图、mermaid 流程/状态图
- **过程**：结构优先图；可调参数且「拖一下更懂」→ sci-widget；否则 SVG/mermaid。尺寸按内容，禁止 viewport 撑满
- **DoD**：widget 自包含、离线、中文文案、可交互；SVG/mermaid 标签清晰
- **降级**：无法内嵌 widget 时给静态图或分步说明

---

## Universal Multimodal Gates

1. 素材路径真实存在；交付前 `present_files` 或明确本地路径。
2. 抽检 ≥1 个关键样本（图/页/句/帧/单元格），禁止只报「已生成」。
3. 跨模态事实一致（图里的数字 = 表里的数字 = 文里的数字）。
4. 隐私：不把用户素材上传到无关第三方；生成服务按桌面既有能力使用。
5. 工具失败 → compact 错误 → 降级或换路径 → 仍失败则部分完成+限制说明。

## Tool Absence Matrix

| 能力 | 有工具 | 无工具 |
|---|---|---|
| 读图/PDF | read | 请用户描述 / 文本层 |
| 生图/改图 | image_gen / image_edit | 外部素材指引 + 设计规格 |
| 转写 | asr_transcribe | 分段人工流程说明 |
| 配音 | tts_speech | 交付文案脚本 |
| Office | office skills | md/csv 等价物 |
| 视频 | ffmpeg 等 | 分镜+脚本 |
| 3D | 3d-creation | three.js 代码或示意图 |
| 交互 | sci-widget / visualizer | 静态 SVG/mermaid |
