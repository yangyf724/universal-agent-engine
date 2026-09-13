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
| S39 | 把登录超时修掉，合并前要有规格和独立评审 | （不路由全协议） | — | P-domain：建议 compose-next，未点名不进全协议 |
| S40 | 不用 compose-next，直接修登录超时 | FIX | — | 用户拒绝建议后走本 skill 轻量 FIX |
| S41 | 写个一次性脚本处理这批 CSV | BUILD | — | 非 P-domain：不建议 compose-next |
| S42 | （改完未跑测试却说）已修好 | （阻塞 Deliver） | — | verification skip → Lean SC 阻塞 |
| S43 | 做一个 10 页产品介绍 PPT | OPERATE | — | 近邻 official 负例；不抢编排层 |
| S44 | 解释一下缓存穿透是什么 | ADVISE | — | T0：不强制 DoD 表/Full Gates |
| S45 | 调研三家登录方案并列取舍，我要拿去开 compose-next | RESEARCH | DESIGN | R1：交付 compose-ready 包后再建议 compose-next |
| S46 | 帮我准备给 compose-next Grill 的验收草案 | DESIGN | WRITE | R1：包是输入，不写 feature Spec |
| S47 | 把这段会议录音转写成纪要 | WRITE | — | R2：E-domain 主产物；不建议 compose-next |
| S48 | 不用 compose-next，先把这段 CSV 脚本直接修好 | FIX | — | R3：拒绝后轻量 FIX |
| S49 | 用 compose-next 修这个登录 bug | （不路由全协议） | — | V1：点名独占，不 Soft |
| S50 | （compose-next 实现中）转写这段录音写进夹具说明 | WRITE | — | V2：Soft 媒体 AUDIO；跳过 Step 2–6 |
| S51 | 把这段录音转写成会议纪要 | WRITE | — | V3：无 compose 上下文 → R2 全协议，非 Soft |
| S52 | （P-domain 修 bug）识别截图里的报错字段 | RESEARCH | — | V4：Soft VISION 子任务 |
| S53 | （compose-next 中）导出一页验收 PPT | OPERATE | — | V5：Soft DOCOFFICE → official |
| S54 | 做一个 10 页产品介绍 PPT | OPERATE | — | V6：独立交付，非 Soft |
| S55 | （Grill）对比三种登录方案，查高星仓和论文 | RESEARCH | — | Soft-Research 证据包；不拍板 |
| S56 | 用 compose-next 做登录，无调研请求 | （不路由全协议） | — | 点名独占，不 Soft-Research |
| S57 | （Implement）测一下登录页截图和提示音 | — | — | Soft-Test 视+听；不写业务码 |
| S58 | 把录音转写成会议纪要 | WRITE | — | 无 compose → R2，非 Soft-Test |
| S59 | （对外 UI 高风险）独立复看关键屏 | — | — | Soft-Test + 可选 1 盲测 |
| S60 | （compose Grill）调研竞品定价模型 | RESEARCH | — | Soft-Research ≤40 行证据包 |

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
