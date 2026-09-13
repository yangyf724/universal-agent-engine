# universal-agent-engine

跨行业通用智能体执行引擎（MiMo Desktop Skill）。

目标：**高效率、高完成率、低错误率、低返工率**。分析用户语句自动路由主模式，并可叠加全模态 I/O；角色为决策透镜（非多智能体），主体按 actionable 核心压缩以降低 token。

<!-- github-sync:begin -->
**Version:** 1.7.0  
**Last sync:** 2026-09-13
<!-- github-sync:end -->

## 安装

将仓库中的 **`skill/` 目录**复制为：

```text
~/.config/mimocode/skills/universal-agent-engine/
```

（兼容旧路径 `~/.claude/skills/universal-agent-engine/`。）

一步同步（Windows PowerShell）：

```powershell
$src = "D:\project\提示词工程\repos\universal-agent-engine\skill"
foreach ($dst in @(
  "$env:USERPROFILE\.config\mimocode\skills\universal-agent-engine",
  "$env:USERPROFILE\.claude\skills\universal-agent-engine"
)) {
  New-Item -ItemType Directory -Force -Path $dst | Out-Null
  Copy-Item -Path "$src\*" -Destination $dst -Recurse -Force
}
```

不要把仓库根目录的 README/CHANGELOG 拷进 skill 文件夹（桌面加载器会拒绝含 README 的 skill 包）。

新开对话后，在插件页应能看到「通用智能体执行引擎」。也可显式说：`用 universal-agent-engine …`。

边界：显式 `/compose-next`、git 仓内多步实现要合并/发版/规格且无前置输入（P-domain，未点名时建议 compose-next）、或单文件 Office/PDF 成稿时，不要加载本编排层全协议。要 worktree/Spec/独立 Review/Finish → compose-next。门禁默认走 quality-gates **Lean Gates**（信号触发 Anti-SC）。

互补辅助：**R1** 前置调研/选项/验收草案 → compose-ready 包再建议 compose-next；**R2** 多模态/Office/媒体/非 git 多步；**R3** 拒绝后轻量 BUILD/FIX。**Soft Companion（v1.7）**：compose-next/P-domain 运行中的多模态子任务 → 只读 multimodal.md + 抽检，跳过 Step 2–6，不建 Spec/worktree/Review。

## 能力

### 七主模式（按最终交付物路由）

| Mode | 典型信号 | 首要产物 |
|------|----------|----------|
| BUILD | 做/实现/部署/build | 可运行产物 + 验证 |
| FIX | 修 bug/fix/debug | 根因 + 修复 + 回归 |
| RESEARCH | 调研/分析/research | 带来源结论 |
| DESIGN | 方案/架构/plan | 可执行方案 |
| WRITE | 写文档/PRD/write | 成稿 + 自检 |
| OPERATE | PPT/Excel/报表 | 可打开文件 + 抽检 |
| ADVISE | 怎么做/咨询 | 直接答案 + 下一步 |

### 全模态叠加（非第八模式）

`VISION` / `AUDIO` / `DOCOFFICE` / `VIDEO` / `THREE_D` / `INTERACTIVE`

详见 `skill/references/multimodal.md`。

## 执行协议

Step 0 路由 → Intake → Plan(DoD) → Execute(ReAct) → Verify(Lean Gates) → Reflect → Deliver

## 回归

```powershell
python skill/tests/run_static_checks.py
# 期望：ALL CHECKS PASSED
```

人工验证步骤见 `skill/tests/manual-verify.md`。

## 目录

```text
skill/                    # 安装到 ~/.config/mimocode/skills/universal-agent-engine/（兼 ~/.claude/skills/）
  SKILL.md
  references/             # intent-router / quality-gates / compose-handoff / multimodal / research-citations
  locales/
  tests/
docs/compose/spec/        # 本仓 feature 规格（engine-compose-aux 等）
README.md
CHANGELOG.md
LICENSE
```

## License

MIT
