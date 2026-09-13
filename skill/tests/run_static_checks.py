#!/usr/bin/env python3
"""L1–L3 static validation for universal-agent-engine skill.

用途
----
在不加载真实模型会话的前提下，回归校验 skill 包契约：
  - L1 结构：frontmatter、locales、references 存在性、body 预算
  - L2 路由面：description 正/负触发词、compose-next 互补与 Soft 边界
  - L3 场景与信号：scenarios 覆盖、mode 独占信号、Lean/Soft 断言
  - L4 协议骨架：Step 0–6 / Multimodal / Examples 等章节齐全

运行
----
    python skill/tests/run_static_checks.py
    # 期望：SUMMARY passes=N failures=0 且 ALL CHECKS PASSED
    # N 以 checklist.md 记载的期望值为准（当前 135）

设计约定
--------
- 只读 skill/ 目录，不访问网络、不改文件。
- 断言失败记入 FAILURES 并继续跑完，便于一次看全缺口。
- 模式信号的权威来源是 intent-router.md 的 Mode Card「触发：」行；
  SKILL 表若仍带信号格，必须与 router 对齐（防双源漂移）。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# skill 包根（…/skill/），与 SKILL.md、references/、tests/ 同级
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
FAILURES: list[str] = []
PASSES: list[str] = []
# 七个主 mode（非第八模态）；与 SKILL Step 0 表、router Mode Card 一致
MODES = ["BUILD", "FIX", "RESEARCH", "DESIGN", "WRITE", "OPERATE", "ADVISE"]


def ok(msg: str) -> None:
    """记录并通过一条检查。"""
    PASSES.append(msg)
    print(f"PASS  {msg}")


def fail(msg: str) -> None:
    """记录一条失败（不中断，便于汇总）。"""
    FAILURES.append(msg)
    print(f"FAIL  {msg}")


def check(cond: bool, msg: str) -> None:
    """统一入口：cond 为真则 PASS，否则 FAIL。"""
    if cond:
        ok(msg)
    else:
        fail(msg)


def parse_skill_mode_signals(body: str) -> dict[str, set[str]]:
    """解析 SKILL Step 0 表中的 mode 信号。

    支持两种表型：
      - 瘦表（现行）：| MODE | 首要产物 |  → 返回 mode → 空集合
      - 旧宽表：| 信号a/b | MODE | 产物 | → 返回 mode → 信号集合（小写）
    """
    found: dict[str, set[str]] = {}
    for line in body.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        # 瘦表：首列即 MODE 名
        if cells[0] in MODES and "信号" not in cells[0]:
            found[cells[0]] = set()
            continue
        # 旧宽表：第二列是 MODE，首列是斜杠分隔信号
        mode = cells[1].strip() if len(cells) > 1 else ""
        if mode not in MODES:
            continue
        signals = {s.strip().lower() for s in cells[0].split("/") if s.strip()}
        found[mode] = signals
    return found


def parse_router_mode_signals(router: str) -> dict[str, set[str]]:
    """解析 intent-router 中 `### MODE` 卡片下的「触发：a/b/c」行。

    这是路由信号的权威源；用于独占词校验（如 fix 只能属于 FIX）。
    """
    found: dict[str, set[str]] = {}
    current: str | None = None
    for line in router.splitlines():
        m = re.match(r"^###\s+([A-Z]+)\s*$", line)
        if m and m.group(1) in MODES:
            current = m.group(1)
            found[current] = set()
            continue
        if current and "触发：" in line:
            raw = line.split("触发：", 1)[1]
            found[current] = {s.strip().lower() for s in raw.split("/") if s.strip()}
            current = None
    return found


def main() -> int:
    """执行全部静态检查；全部通过返回 0，否则 1。"""

    # ------------------------------------------------------------------
    # L1 — 文件结构与 frontmatter
    # ------------------------------------------------------------------
    check(SKILL.exists(), "SKILL.md exists")
    text = SKILL.read_text(encoding="utf-8")
    check(text.startswith("---\n"), "starts with YAML frontmatter")
    # split 限 2 段：[前空, frontmatter, body]
    parts = text.split("---\n", 2)
    check(len(parts) >= 3, "frontmatter closed")
    fm = parts[1]
    body = parts[2]

    # name 必须与安装目录名一致，否则宿主加载器会拒包
    m = re.search(r"^name:\s*(.+)$", fm, re.M)
    check(m is not None and m.group(1).strip() == "universal-agent-engine", "name matches directory")
    # description：路由面；须含负例；禁止 <>（frontmatter 解析安全）
    dm = re.search(r"^description:\s*(.+)$", fm, re.M)
    check(dm is not None, "description present")
    desc = ""
    if dm:
        desc = dm.group(1).strip()
        check(len(desc) <= 1024, f"description length {len(desc)} <= 1024")
        check("Do NOT use" in desc, "negative trigger present")
        check("<" not in desc and ">" not in desc, "no angle brackets in frontmatter")

    # locales：仅允许 displayName + brief 两键（桌面插件页契约）
    for loc in ("zh-CN", "en-US"):
        p = ROOT / "locales" / f"{loc}.json"
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            check(set(data) == {"displayName", "brief"}, f"{loc}.json keys")
            check(bool(data.get("displayName")) and bool(data.get("brief")), f"{loc}.json non-empty")
        except Exception as e:  # noqa: BLE001
            fail(f"{loc}.json parse: {e}")

    # 必备 reference 文件（空文件视为损坏）
    for rel in (
        "references/intent-router.md",
        "references/quality-gates.md",
        "references/research-citations.md",
        "references/multimodal.md",
        "references/compose-handoff.md",
        "references/compose-token.md",
        "references/compose-phases.md",
    ):
        p = ROOT / rel
        check(p.exists() and p.stat().st_size > 0, f"{rel} exists non-empty")

    # 渐进披露：body 不得膨胀成全文手册
    check(len(body) < 20000, f"body chars {len(body)} < 20000 (progressive disclosure)")

    # ------------------------------------------------------------------
    # L4 — 协议骨架章节
    # ------------------------------------------------------------------
    required_headers = [
        "## Important",
        "## Step 0",
        "## Multimodal Overlay",
        "## Step 1",
        "## Step 2",
        "## Step 3",
        "## Step 4",
        "## Step 5",
        "## Step 6",
        "## Examples",
        "## Troubleshooting",
    ]
    for h in required_headers:
        check(h in body, f"section present: {h}")

    # 七 mode：body 必须出现 token，router 必须有 Mode Card
    router = (ROOT / "references" / "intent-router.md").read_text(encoding="utf-8")
    for mode in MODES:
        check(mode in body, f"mode token present: {mode}")
        check(f"### {mode}" in router, f"mode card in intent-router: {mode}")

    # body 里所有 references/*.md 链接必须落盘（防死链）
    for ref in re.findall(r"references/[a-z0-9-]+\.md", body):
        check((ROOT / ref).exists(), f"linked reference exists: {ref}")

    # ------------------------------------------------------------------
    # L2 — description / 边界 / Lean·Soft 契约
    # ------------------------------------------------------------------
    desc_l = desc.lower()
    # 高信号正例（禁止穷举长尾词堆砌，见 v1.2 SkillReducer 结论）
    positive_phrases = [
        "build", "implement", "ship",
        "端到端做完", "从需求到交付", "修bug", "做方案", "调研落地",
        "架构师", "评审",
        "orchestration",
    ]
    missing_pos = [p for p in positive_phrases if p.lower() not in desc_l]
    check(not missing_pos, f"positive triggers in description; missing={missing_pos}")
    check(
        "完成报告" not in desc,
        "description avoids exhaustive trigger laundry list",
    )
    check("chit-chat" in desc_l or "闲聊" in desc, "negative: chit-chat excluded")
    check("compose-next" in desc_l, "negative: compose-next boundary in description")
    check(
        "P-domain" in body or "P-domain" in router,
        "P-domain yield present in SKILL or intent-router",
    )

    qg_early = (ROOT / "references" / "quality-gates.md").read_text(encoding="utf-8")
    # Lean Gates 必须在 Full/Universal 之前，否则 JIT 会灌全量门禁（v1.5 G1）
    lean_idx = qg_early.find("## Lean Gates")
    full_idx = qg_early.find("## Universal Gates")
    check(0 <= lean_idx < full_idx, "Lean Gates section before Full/Universal Gates")
    check("风险" in qg_early[lean_idx:lean_idx+800] or "该测" in qg_early[lean_idx:lean_idx+800],
          "Lean Gates lists SC signal words")
    check("阻塞" in qg_early[lean_idx:lean_idx+900], "Lean Gates blocks verification skip")
    check("compose-next" in qg_early[lean_idx:lean_idx+1200], "Lean Gates yields independent Review to compose-next")
    check("Lean Gates" in body, "SKILL body points at Lean Gates")
    check("禁止强制双表" in qg_early, "G3 mask not forced dual tables")
    check(
        "建议" in body and "compose-next" in body and "P-domain" in body,
        "SKILL Important has P-domain suggest compose-next path",
    )
    check("### D3" in router or "D3 技能边界" in router, "intent-router D3 boundary section")
    check(
        "直接修" in router or "without spec" in router or "不用 compose-next" in router,
        "D3 documents user opt-out to stay on engine",
    )
    check(
        "official" in desc_l or "xlsx" in desc_l,
        "negative: office official boundary in description",
    )
    # v1.6+ 互补辅助信号
    check(
        "complementary" in desc_l or "互补" in desc,
        "description signals compose-next complement",
    )
    check(
        "pre-feature" in desc_l or "research/option" in desc_l,
        "description signals pre-feature research packs",
    )
    check("references/compose-handoff.md" in body, "SKILL links compose-handoff.md")
    check(
        "compose-ready" in body or "compose-ready" in router,
        "compose-ready pack referenced in SKILL or router",
    )
    check(
        ("R1" in router or "R1" in body) and ("前置" in router or "前置" in body or "pre-feature" in desc_l),
        "R1 pre-work path documented",
    )
    check(
        "包≠" in qg_early or "包≠feature" in qg_early,
        "quality-gates marks pack is not feature Spec",
    )
    # Soft 必须在 Plan 之前短路，否则 compose 会话仍进全编排（双权威）
    check("Soft" in body and "跳过 Step 2" in body, "SKILL Soft short-circuits orchestration")
    check(body.find("Soft") < body.find("## Step 2"), "Soft appears before Step 2 Plan")
    check("Soft-Research" in router and "Soft-Test" in router, "intent-router Soft-Research/Test")
    check("compose-token" in body or "compose-token" in qg_early, "compose-token contract referenced")
    check((ROOT / "references" / "compose-token.md").exists(), "compose-token.md exists")
    # Grill 证据包行数上限（token 合同 load-bearing）
    check("≤40" in (ROOT / "references" / "compose-token.md").read_text(encoding="utf-8") or "40 行" in (ROOT / "references" / "compose-token.md").read_text(encoding="utf-8"), "evidence pack line cap documented")
    # v1.9 — compose-next 九阶段 Soft 矩阵
    phases = (ROOT / "references" / "compose-phases.md").read_text(encoding="utf-8")
    check("compose-phases" in body, "SKILL links compose-phases.md")
    check("Workspace" in phases and "Finish" in phases, "phases documents Workspace/Finish")
    check("排除" in phases and "永不" in phases, "phases hard-excludes Workspace/Finish")
    for card in ("Soft-Orient", "Soft-Spec-input", "Soft-Evidence", "Soft-Review-pack", "Soft-Report"):
        check(card in phases, f"phases card present: {card}")
    check("派 Reviewer" in phases and "不" in phases[phases.find("Soft-Review-pack"):phases.find("Soft-Review-pack")+800], "Soft-Review-pack does not dispatch reviewer")
    check("compose-phases" in router, "intent-router points at compose-phases")
    check("Soft-Review-pack" in phases and "Soft-Spec-input" in phases, "Spec/Review input cards named")
    # v1.10 Soft Proof — quality DoD + Token ROI protocol
    check("质量抽检" in phases, "phases Soft quality DoD section")
    check((ROOT / "tests" / "token-roi.md").exists(), "token-roi.md exists")
    token_text = (ROOT / "references" / "compose-token.md").read_text(encoding="utf-8")
    check("token-roi" in token_text, "compose-token points at token-roi")
    # v1.11 — process gates + effort table + Soft depth
    pg_path = ROOT / "references" / "process-gates.md"
    check(pg_path.exists(), "process-gates.md exists")
    if pg_path.exists():
        pg = pg_path.read_text(encoding="utf-8")
        check("Context-7" in pg or "Context 7" in pg, "process-gates has Context-7 preflight")
        check("canary" in pg.lower(), "process-gates has canary")
        check("软停" in pg, "process-gates has SC soft-halt")
        check("LLM-judge" in pg and "平台" in pg, "process-gates forbids full LLM-judge platform")
    check((ROOT / "tests" / "process-audit.md").exists(), "process-audit.md exists")
    audit = (ROOT / "tests" / "process-audit.md").read_text(encoding="utf-8")
    check("verify" in audit and "canary" in audit.lower(), "process-audit has verify+canary fields")
    check("goal" in audit and "efficiency" in audit, "process-audit four dimensions")
    check("Independence test" in token_text or "independence" in token_text.lower(), "compose-token independence test")
    check("2–4" in token_text or "2-4" in token_text, "compose-token T3 soft cap documented")
    check("默认" in token_text and "**0**" in token_text, "compose-token default fan-out 0")
    for card in ("Soft-Contract", "Soft-Drift", "Soft-Verify-recipe", "Soft-Amendment", "Soft-DoD-artifact"):
        check(card in phases, f"phases Soft depth card: {card}")
    check("process-gates" in qg_early, "Lean Gates points at process-gates")
    check("process-gates" in token_text or "process-gates" in phases, "Soft supply references process-gates")

    # ------------------------------------------------------------------
    # Token / 角色 / 注入加固
    # ------------------------------------------------------------------
    body_lines = [ln for ln in body.splitlines() if ln.strip()]
    check(len(body_lines) <= 110, f"SKILL body non-empty lines {len(body_lines)} <= 110")
    # 相对历史基线 ~3597 至少瘦 20%；v1.10 腾空目标 2880（保留 ≥120 余量）
    check(len(body) <= 2880, f"SKILL body chars {len(body)} <= 2880 (v1.10 headroom)")
    check("Role Lens" in body, "SKILL body references Role Lens")
    check("Role Lens" in router or "决策透镜" in router, "intent-router has Role Lens section")
    check(
        "注入" in body or "不是指令" in body,
        "SKILL has injection hardening rule",
    )
    check(
        "禁止" in body and ("MAS" in body or "会审" in body or "并行发言" in body),
        "SKILL forbids multi-persona MAS",
    )

    # ------------------------------------------------------------------
    # L3 — mode 信号对齐与独占
    # ------------------------------------------------------------------
    skill_signals = parse_skill_mode_signals(body)
    router_signals = parse_router_mode_signals(router)
    check(set(skill_signals) == set(MODES), f"SKILL table modes parsed: {sorted(skill_signals)}")
    check(set(router_signals) == set(MODES), f"router modes parsed: {sorted(router_signals)}")

    # 英文独占信号：防 BUILD 卡误写 fix 等路由冲突
    check("fix" not in router_signals.get("BUILD", set()), "BUILD router-card does not contain 'fix'")
    check("fix" in router_signals.get("FIX", set()), "FIX router-card contains 'fix'")
    exclusive = {
        "fix": "FIX",
        "build": "BUILD",
        "research": "RESEARCH",
        "design": "DESIGN",
        "write": "WRITE",
    }
    for sig, owner in exclusive.items():
        owners = [m for m, sigs in router_signals.items() if sig in sigs]
        check(owners == [owner], f"exclusive signal '{sig}' only on {owner}; owners={owners}")

    # 若 SKILL 仍是宽表，信号必须能在 router 对应卡中找到
    for mode in MODES:
        sk = skill_signals.get(mode, set())
        if not sk:
            continue
        rt = router_signals.get(mode, set())
        still_missing = set()
        for s in sk:
            if not any(s in r or r in s for r in rt):
                still_missing.add(s)
        check(not still_missing, f"signals aligned SKILL→router {mode}; missing={sorted(still_missing)}")

    # ------------------------------------------------------------------
    # scenarios.md 覆盖
    # ------------------------------------------------------------------
    scen_path = ROOT / "tests" / "scenarios.md"
    check(scen_path.exists(), "tests/scenarios.md exists")
    if scen_path.exists():
        scen = scen_path.read_text(encoding="utf-8")
        for mode in MODES:
            check(mode in scen, f"scenario mentions mode: {mode}")
        expected_cells = re.findall(r"\|\s*([A-Z]+(?:\s*\+\s*[A-Z]+)*)\s*\|", scen)
        bad = []
        for cell in expected_cells:
            for part in re.split(r"\s*\+\s*", cell):
                if part and part not in MODES and part not in {"ID", "Expected"}:
                    if part not in {"ID"}:
                        bad.append(part)
        # Expected 列：合法 mode、mode+mode，或有意负例「（不路由全协议）」
        expected_col = re.findall(
            r"\|\s*((?:BUILD|FIX|RESEARCH|DESIGN|WRITE|OPERATE|ADVISE)(?:\s*\+\s*[A-Z]+)*|（不路由全协议）)\s*\|",
            scen,
        )
        check(len(expected_col) >= 15, f"scenarios have >=15 expected rows; got {len(expected_col)}")
        # 关键里程碑场景锚点（改表时勿静默删行）
        check("S31" in scen and "S32" in scen and "S34" in scen, "conflict/role scenarios present")
        check("S39" in scen and "S40" in scen, "P-domain yield scenarios present")
        check("S42" in scen and "S44" in scen, "Lean Gates scenarios present")
        check("S45" in scen and "S48" in scen, "compose-aux R1-R3 scenarios present")
        check("compose-ready" in scen, "scenarios mention compose-ready pack")
        check("S49" in scen and "S54" in scen, "soft companion scenarios present")
        check("Soft" in scen or "Soft Companion" in scen, "scenarios mention Soft Companion")
        check("S55" in scen and "S60" in scen, "soft-research/test scenarios present")
        check("Soft-Research" in scen and "Soft-Test" in scen, "scenarios name Soft-Research/Test")
        check("S61" in scen and "S70" in scen, "compose-phase matrix scenarios present")
        check("S71" in scen and "S74" in scen, "v1.11 process/effort/depth scenarios present")
        check("Soft-Contract" in scen or "Soft-Amendment" in scen, "scenarios name Soft depth cards")
        check("Independence" in scen or "fan-out" in scen, "scenarios cover fan-out discipline")
        check("Soft-Spec-input" in scen and "Soft-Review-pack" in scen, "scenarios name Spec/Review packs")
        invalid = []
        for cell in expected_col:
            if "不路由" in cell:
                continue
            for part in re.split(r"\s*\+\s*", cell):
                if part and part not in MODES:
                    invalid.append(part)
        check(not invalid, f"scenario Expected modes legal; invalid={invalid}")

    # ------------------------------------------------------------------
    # quality-gates 四指标与 Universal Gates
    # ------------------------------------------------------------------
    qg = (ROOT / "references" / "quality-gates.md").read_text(encoding="utf-8")
    for metric in ("高效率", "高完成率", "低错误率", "低返工率"):
        check(metric in qg, f"metric mapped: {metric}")
    for gate in ("DoD Gate", "Evidence Gate", "Assumption Gate", "Scope Gate", "No Fake Done"):
        check(gate in qg, f"universal gate: {gate}")

    # ------------------------------------------------------------------
    # multimodal 六卡与触发可见性
    # ------------------------------------------------------------------
    mm = (ROOT / "references" / "multimodal.md").read_text(encoding="utf-8")
    check("## When to Apply" in mm, "multimodal: When to Apply section")
    for card in ("VISION", "AUDIO", "DOCOFFICE", "VIDEO", "THREE_D", "INTERACTIVE"):
        check(f"## {card}" in mm, f"multimodal card: {card}")
    check("降级" in mm, "multimodal: degradation documented")
    check("Multimodal Overlay" in body, "SKILL has Multimodal Overlay section")
    check("references/multimodal.md" in body, "SKILL links multimodal.md")
    for token in ("3D", "交互", "转写", "配音"):
        check(token in desc or token in body, f"multimodal trigger visible: {token}")
    check("VISION" in qg and "AUDIO" in qg, "quality-gates covers VISION/AUDIO")

    # ------------------------------------------------------------------
    # 汇总
    # ------------------------------------------------------------------
    print()
    print(f"SUMMARY passes={len(PASSES)} failures={len(FAILURES)}")
    if FAILURES:
        print("FAILURES:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
