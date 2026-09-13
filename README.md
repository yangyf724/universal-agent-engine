# universal-agent-engine

**v2.0.0** — 门控路由 + compose-next 全模态插件。

目标：standalone 时分析需求并路由到正确出口；compose-next 运行中补齐全模态感知、测试与 Grill 研究证据。**不再**是一般编排执行引擎。

<!-- github-sync:begin -->
**Version:** 2.0.0  
**Last sync:** 2026-09-14
<!-- github-sync:end -->

## 安装

将仓库中的 **`skill/` 目录**复制为：

```text
~/.config/mimocode/skills/universal-agent-engine/
```

一步同步（Windows PowerShell）：

```powershell
$src = "D:\project\提示词工程\repos\universal-agent-engine\skill"
$dst = "$env:USERPROFILE\.config\mimocode\skills\universal-agent-engine"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item -Path "$src\*" -Destination $dst -Recurse -Force
```

不要把仓库根目录的 README/CHANGELOG 拷进 skill 文件夹。

新开对话后生效。也可显式说：`用 universal-agent-engine …`。

## 双角色

### 1. Standalone Intent Gate

| 出口 | 信号 | 行为 |
|------|------|------|
| ADVISE | 解释/咨询，无文件交付 | 直接结论 + 下一步 |
| compose-next | git 多步 + 合并/规格 | 建议 `/compose-next …` |
| 专项委托 | Office/PDF/3D/生图/深研… | 加载**一个**专项 skill |

细则与委托映射（15 类）：`skill/references/intent-gate.md`。

### 2. compose-next Multimodal Plugin（Soft）

| 卡 | 作用 |
|----|------|
| Modality Scan | 输入/输出模态扫描 + 工具锚点 |
| Soft-Test / Companion | 视/听/交互/Office/跨模态抽检 |
| Soft-Research | Grill 证据包 ≤40 行（不拍板） |

**禁止**：Spec-input / Review-pack / Report / 九阶段 / Soft Depth；Workspace/Finish 零 Soft；默认 fan-out=0。

细则：`skill/references/multimodal.md`。

## 目录

```text
skill/
  SKILL.md                 # 双角色主体（≤2500 ch）
  references/
    intent-gate.md         # 三出口门控 + 委托映射
    multimodal.md          # 采集 + 测试 + Grill 研究
  locales/
  tests/
    run_static_checks.py   # v2 契约静态门
    checklist.md
docs/compose/spec/v2-gate-multimodal.md
README.md
CHANGELOG.md
LICENSE
```

## 回归

```powershell
python skill/tests/run_static_checks.py
# 期望：ALL CHECKS PASSED
```

## License

MIT
