# universal-agent-engine

跨行业通用智能体执行引擎（MiMo Desktop Skill）。

目标：**高效率、高完成率、低错误率、低返工率**。分析用户语句自动路由主模式，并可叠加全模态 I/O。

<!-- github-sync:begin -->
**Version:** 1.0.0  
**Last sync:** 2026-09-10
<!-- github-sync:end -->

## 安装

将仓库中的 **`skill/` 目录**复制为：

```text
~/.claude/skills/universal-agent-engine/
```

不要把仓库根目录的 README/CHANGELOG 拷进 skill 文件夹（桌面加载器会拒绝含 README 的 skill 包）。

新开对话后，在插件页应能看到「通用智能体执行引擎」。也可显式说：`用 universal-agent-engine …`。

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

Step 0 路由 → Intake → Plan(DoD) → Execute(ReAct) → Verify(CoVe) → Reflect → Deliver

## 回归

```powershell
python skill/tests/run_static_checks.py
# 期望：ALL CHECKS PASSED
```

人工验证步骤见 `skill/tests/manual-verify.md`。

## 目录

```text
skill/                    # 安装到 ~/.claude/skills/universal-agent-engine/
  SKILL.md
  references/
  locales/
  tests/
README.md
CHANGELOG.md
LICENSE
```

## License

MIT
