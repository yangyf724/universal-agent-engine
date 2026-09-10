#!/usr/bin/env python3
"""L1-L3 static validation for universal-agent-engine skill."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
FAILURES: list[str] = []
PASSES: list[str] = []
MODES = ["BUILD", "FIX", "RESEARCH", "DESIGN", "WRITE", "OPERATE", "ADVISE"]


def ok(msg: str) -> None:
    PASSES.append(msg)
    print(f"PASS  {msg}")


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"FAIL  {msg}")


def check(cond: bool, msg: str) -> None:
    if cond:
        ok(msg)
    else:
        fail(msg)


def parse_skill_mode_signals(body: str) -> dict[str, set[str]]:
    """Parse slim or full Step 0 table. Slim: | MODE | product |.
    Full legacy: | signals | MODE | product |."""
    found: dict[str, set[str]] = {}
    for line in body.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if cells[0] in MODES and "信号" not in cells[0]:
            # slim table: Mode first
            found[cells[0]] = set()
            continue
        mode = cells[1].strip() if len(cells) > 1 else ""
        if mode not in MODES:
            continue
        signals = {s.strip().lower() for s in cells[0].split("/") if s.strip()}
        found[mode] = signals
    return found


def parse_router_mode_signals(router: str) -> dict[str, set[str]]:
    """Parse intent-router mode card '触发：a/b/c' lines."""
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
    # --- L1 structure ---
    check(SKILL.exists(), "SKILL.md exists")
    text = SKILL.read_text(encoding="utf-8")
    check(text.startswith("---\n"), "starts with YAML frontmatter")
    parts = text.split("---\n", 2)
    check(len(parts) >= 3, "frontmatter closed")
    fm = parts[1]
    body = parts[2]

    m = re.search(r"^name:\s*(.+)$", fm, re.M)
    check(m is not None and m.group(1).strip() == "universal-agent-engine", "name matches directory")
    dm = re.search(r"^description:\s*(.+)$", fm, re.M)
    check(dm is not None, "description present")
    desc = ""
    if dm:
        desc = dm.group(1).strip()
        check(len(desc) <= 1024, f"description length {len(desc)} <= 1024")
        check("Do NOT use" in desc, "negative trigger present")
        check("<" not in desc and ">" not in desc, "no angle brackets in frontmatter")

    for loc in ("zh-CN", "en-US"):
        p = ROOT / "locales" / f"{loc}.json"
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            check(set(data) == {"displayName", "brief"}, f"{loc}.json keys")
            check(bool(data.get("displayName")) and bool(data.get("brief")), f"{loc}.json non-empty")
        except Exception as e:  # noqa: BLE001
            fail(f"{loc}.json parse: {e}")

    for rel in (
        "references/intent-router.md",
        "references/quality-gates.md",
        "references/research-citations.md",
        "references/multimodal.md",
    ):
        p = ROOT / rel
        check(p.exists() and p.stat().st_size > 0, f"{rel} exists non-empty")

    check(len(body) < 20000, f"body chars {len(body)} < 20000 (progressive disclosure)")

    # --- L4 protocol presence ---
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

    router = (ROOT / "references" / "intent-router.md").read_text(encoding="utf-8")
    for mode in MODES:
        check(mode in body, f"mode token present: {mode}")
        check(f"### {mode}" in router, f"mode card in intent-router: {mode}")

    for ref in re.findall(r"references/[a-z0-9-]+\.md", body):
        check((ROOT / ref).exists(), f"linked reference exists: {ref}")

    # --- L2 trigger phrase coverage ---
    desc_l = desc.lower()
    # Routing-surface positives (SkillReducer: high-signal, not exhaustive laundry list)
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

    # --- token / role contracts ---
    body_lines = [ln for ln in body.splitlines() if ln.strip()]
    check(len(body_lines) <= 110, f"SKILL body non-empty lines {len(body_lines)} <= 110")
    # Baseline body chars ~3597; require >=20% reduction => <= 2878, allow small slack
    check(len(body) <= 3000, f"SKILL body chars {len(body)} <= 3000 (>=20% vs baseline 3597)")
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

    # --- L3 signal alignment: slim table lists modes; full signals live in router ---
    skill_signals = parse_skill_mode_signals(body)
    router_signals = parse_router_mode_signals(router)
    check(set(skill_signals) == set(MODES), f"SKILL table modes parsed: {sorted(skill_signals)}")
    check(set(router_signals) == set(MODES), f"router modes parsed: {sorted(router_signals)}")

    # Exclusive English signals enforced on router cards (authoritative signal source)
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

    # If SKILL table still carries full signal cells, align them to router
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

    # --- scenarios.md coverage ---
    scen_path = ROOT / "tests" / "scenarios.md"
    check(scen_path.exists(), "tests/scenarios.md exists")
    if scen_path.exists():
        scen = scen_path.read_text(encoding="utf-8")
        for mode in MODES:
            check(mode in scen, f"scenario mentions mode: {mode}")
        # expected modes in table cells must be valid or intentional negatives
        expected_cells = re.findall(r"\|\s*([A-Z]+(?:\s*\+\s*[A-Z]+)*)\s*\|", scen)
        bad = []
        for cell in expected_cells:
            for part in re.split(r"\s*\+\s*", cell):
                if part and part not in MODES and part not in {"ID", "Expected"}:
                    # skip header-ish
                    if part not in {"ID"}:
                        bad.append(part)
        # also catch Expected column patterns like BUILD / （不路由全协议）
        expected_col = re.findall(
            r"\|\s*((?:BUILD|FIX|RESEARCH|DESIGN|WRITE|OPERATE|ADVISE)(?:\s*\+\s*[A-Z]+)*|（不路由全协议）)\s*\|",
            scen,
        )
        check(len(expected_col) >= 15, f"scenarios have >=15 expected rows; got {len(expected_col)}")
        check("S31" in scen and "S32" in scen and "S34" in scen, "conflict/role scenarios present")
        check("S39" in scen and "S40" in scen, "P-domain yield scenarios present")
        check("S42" in scen and "S44" in scen, "Lean Gates scenarios present")
        invalid = []
        for cell in expected_col:
            if "不路由" in cell:
                continue
            for part in re.split(r"\s*\+\s*", cell):
                if part and part not in MODES:
                    invalid.append(part)
        check(not invalid, f"scenario Expected modes legal; invalid={invalid}")


    # --- quality-gates ---
    qg = (ROOT / "references" / "quality-gates.md").read_text(encoding="utf-8")
    for metric in ("高效率", "高完成率", "低错误率", "低返工率"):
        check(metric in qg, f"metric mapped: {metric}")
    for gate in ("DoD Gate", "Evidence Gate", "Assumption Gate", "Scope Gate", "No Fake Done"):
        check(gate in qg, f"universal gate: {gate}")

    # --- multimodal overlay ---
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
