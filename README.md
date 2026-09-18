# universal-agent-engine

**v2.0.4** — 门控路由 + compose-next 全模态插件（bug-hunt v4 / Priority 补全 + 静态门加固）。

目标：standalone 时分析需求并路由到正确出口；compose-next 运行中补齐全模态感知、测试与 Grill 研究证据。**不再**是一般编排执行引擎。

<!-- github-sync:begin -->
**Version:** 2.0.4  
**Last sync:** 2026-09-18 · `fc4038c`
<!-- github-sync:end -->

## 安装

将仓库中的 **`skill/` 目录**复制为：

```text
~/.config/mimocode/skills/universal-agent-engine/
```

一步同步（在仓库根目录执行，Windows PowerShell）：

```powershell
$src = Join-Path (Get-Location) 'skill'
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
| compose-next | git 多步 + 合并/规格；或点名 compose-next | 建议 `/compose-next …`（不展开三出口） |
| 专项委托 | Office/PDF/3D/生图/深研… | 加载**一个**专项 skill |

细则与委托映射（canonical seed 18 类 + 表外已装专项 JIT）：`skill/references/intent-gate.md`。

### 2. compose-next Multimodal Plugin（Soft）

| 卡 | 作用 |
|----|------|
| Modality Scan | 输入/输出模态扫描 + 工具锚点 |
| Soft-Test / Companion | 视/听/交互/Office/跨模态抽检 |
| Soft-Research | Grill 证据包 ≤40 行（不拍板） |

**禁止**：Spec-input / Review-pack / Report / Soft-Orient / 九阶段 / Soft Depth；Workspace/Finish 零 Soft；默认 fan-out=0。

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
docs/compose/spec/
  v2-gate-multimodal.md    # 当前行为规格（v2，经 2.0.2/2.0.3 修订）
  quality-review-v3.md     # 2.0.2 质量审查
  bug-hunt-v4.md           # 2.0.3 bug-hunt 规格（当前）
  quality-review-v2.md     # 2.0.1 历史审查
  engine-*.md              # v1 历史规格（status: superseded）
docs/compose/smoke/
  v2.0.0-full-matrix-*.md  # v2 冒烟协议/报告
  v1.*-matrix.md           # v1 历史矩阵（Historical）
README.md
CHANGELOG.md
LICENSE
```

历史 docs 仅作考古；当前契约以 `skill/` + `v2-gate-multimodal.md`（Priority/称谓以 skill 与 2.0.3 修订为准）+ `bug-hunt-v4.md` 修复记录为准。

## 回归

```powershell
python skill/tests/run_static_checks.py
# 期望：ALL CHECKS PASSED
python skill/tests/run_static_checks.py --negative-self-test
# 期望：NEGATIVE SELF-TEST PASSED
```

## License

MIT
