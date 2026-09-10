# Intent Router Scenarios

Each row is a regression case. `Expected` is the primary mode after Step 0 routing.

| ID | User utterance | Expected primary mode | Secondary | Notes |
|----|----------------|----------------------|-----------|-------|
| S01 | 帮我做这个项目 | BUILD | — | 主交付可运行产物 |
| S02 | 实现登录接口 | BUILD | — | 功能交付 |
| S03 | 部署到测试环境 | BUILD | — | 上线/部署动词 |
| S04 | 修一下这个 bug，接口 500 | FIX | — | 根因+回归 |
| S05 | 重构支付模块，顺手出优化方案 | FIX | DESIGN | 先修后方案 |
| S06 | 调研三家竞品定价 | RESEARCH | — | 带来源结论 |
| S07 | 调研竞品并做成一页对比 PPT | OPERATE | RESEARCH | **主产物=PPT** |
| S08 | 做一个报销审批流程方案 | DESIGN | — | 可执行方案 |
| S09 | 设计系统架构并写进 README | DESIGN | WRITE | 主=架构方案 |
| S10 | 写一份给客户的项目周报 | WRITE | — | 成稿 |
| S11 | 做一份员工手册说明书 | WRITE | — | 文档类 |
| S12 | 把销售数据做成 Excel 周报 | OPERATE | — | 可打开文件 |
| S13 | 做 10 页季度汇报 PPT | OPERATE | — | deck |
| S14 | 怎么做缓存穿透防护 | ADVISE | — | 先答；可落地可升 DESIGN/BUILD |
| S15 | 这个报错是什么意思 | ADVISE | FIX | 先解释；有复现可升 FIX |
| S16 | 帮我分析这个数据集并写结论 | RESEARCH | WRITE | RESEARCH+WRITE |
| S17 | 天气怎么样 | （不路由全协议） | — | 负例：闲聊 |
| S18 | 只列一下当前目录文件 | （不路由全协议） | — | 负例：无目标浏览 |
| S19 | 帮我把登录 500 修好，高效率完成 | FIX | — | 含效率目标仍 FIX |
| S20 | 调研 X 并落地成可运行脚本 | BUILD | RESEARCH | 落地成代码 → BUILD 主 |
| S21 | 看图识别发票金额并写结论 | RESEARCH | WRITE | overlay: VISION |
| S22 | 把这张海报改得更简洁 | OPERATE | — | overlay: VISION；主=交付改后图 |
| S23 | 转写这段录音并做成会议纪要 | WRITE | — | overlay: AUDIO |
| S24 | 用冰糖声音把这段文案配成音频 | OPERATE | — | overlay: AUDIO；主=音频文件 |
| S25 | 做一个季度汇报 PPT | OPERATE | — | overlay: DOCOFFICE |
| S26 | 做一个产品介绍视频脚本和分镜 | WRITE | — | overlay: VIDEO（无编码则脚本） |
| S27 | 搭一个 3D 滚动叙事网站 | BUILD | — | overlay: THREE_D |
| S28 | 做一个可拖动参数的抛物线演示 | BUILD | — | overlay: INTERACTIVE；sci-widget |
| S29 | 把流程画成 mermaid 图 | WRITE | — | overlay: INTERACTIVE；静态图 |
| S30 | 只听一下这段录音说了啥 | WRITE | — | overlay: AUDIO |
| S31 | 做 10 页季度汇报 PPT | OPERATE | — | 负例边界：优先 official，不强制全引擎协议 |
| S32 | 用 compose-next 修这个登录 bug | （不路由全协议） | — | 负例：只 compose-next |
| S33 | 调研竞品并做成对比 PPT | OPERATE | RESEARCH | 委托 office official |
| S34 | 以架构师视角评审这个方案的风险 | DESIGN | — | Role Lens: 架构师 |
| S35 | 以产品经理口径写一页需求澄清 | WRITE | ADVISE | Role Lens: 产品经理；不默认 BUILD |
| S36 | 以 QA 视角列出验收清单再修失败用例 | FIX | — | Role Lens: QA + 门禁 |
| S37 | 以架构师和 QA 一起评审这个方案 | DESIGN | — | 单 Lens；禁止双角色会审 |
| S38 | 你是产品经理，解释一下这个报错 | ADVISE | — | Role Lens: 产品经理；不升 BUILD |

## Multimodal overlay rules

1. 多模态**不是**第八 mode；主 mode 仍由最终交付物决定。
2. 有输入媒体先 Modality Scan；工具缺失降级并披露。
3. 交付前必须抽检该模态至少 1 个样本。
4. Expected 列只写主 mode；叠加模态写在 Notes 的 `overlay:`。

## Ambiguity rules encoded

1. Explicit mode instruction wins（「先做调研」→ RESEARCH）。
2. Primary mode = final deliverable（PPT/代码/方案）。
3. Unspecified → ADVISE；若建议可立即执行，升级对应 mode。
4. No deliverable → do not force full engine protocol.

## Multi-mode matrix

| Deliverable | Primary | Often embedded |
|-------------|---------|----------------|
| 可运行代码/服务 | BUILD | RESEARCH, FIX |
| 修复/性能 | FIX | DESIGN |
| 证据型结论 | RESEARCH | WRITE |
| 方案/架构 | DESIGN | RESEARCH, WRITE |
| 文档/文案 | WRITE | RESEARCH |
| PPT/Excel/Word | OPERATE | RESEARCH, WRITE |
| 解释/咨询 | ADVISE | — |
