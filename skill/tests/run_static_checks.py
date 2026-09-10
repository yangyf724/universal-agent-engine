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
    """Parse Step 0 table rows: | signals | MODE | ... |"""
    found: dict[str, set[str]] = {}
    for line in body.splitlines():
        if not line.startswith("|") or line.startswith("|---") or "Mode" in line and "产物" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        mode = cells[1].strip()
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
    positive_phrases = [
        "帮我做", "实现", "完成报告", "修一下", "做一份方案", "调研",
        "build", "implement", "ship", "fix", "research", "design", "write",
    ]
    missing_pos = [p for p in positive_phrases if p.lower() not in desc_l]
    check(not missing_pos, f"positive triggers in description; missing={missing_pos}")
    check("chit-chat" in desc_l or "闲聊" in desc, "negative: chit-chat excluded")

    # --- L3 signal alignment SKILL table <-> intent-router cards ---
    skill_signals = parse_skill_mode_signals(body)
    router_signals = parse_router_mode_signals(router)
    check(set(skill_signals) == set(MODES), f"SKILL table modes parsed: {sorted(skill_signals)}")
    check(set(router_signals) == set(MODES), f"router modes parsed: {sorted(router_signals)}")

    # Exclusive English signal 'fix' must not appear in BUILD
    build_en = skill_signals.get("BUILD", set())
    check("fix" not in build_en, "BUILD skill-table does not contain exclusive signal 'fix'")
    check("fix" in skill_signals.get("FIX", set()), "FIX skill-table contains 'fix'")
    check("fix" not in router_signals.get("BUILD", set()), "BUILD router-card does not contain 'fix'")
    check("fix" in router_signals.get("FIX", set()), "FIX router-card contains 'fix'")

    # Every SKILL table signal should appear in corresponding router card (alignment)
    for mode in MODES:
        sk = skill_signals.get(mode, set())
        rt = router_signals.get(mode, set())
        missing = {s for s in sk if s not in rt}
        # allow Chinese signals that are substrings of router tokens
        still_missing = set()
        for s in missing:
            if not any(s in r or r in s for r in rt):
                still_missing.add(s)
        check(not still_missing, f"signals aligned SKILL→router {mode}; missing={sorted(still_missing)}")

    # Cross-mode exclusive English signals
    exclusive = {
        "fix": "FIX",
        "build": "BUILD",
        "research": "RESEARCH",
        "design": "DESIGN",
        "write": "WRITE",
    }
    for sig, owner in exclusive.items():
        owners = [m for m, sigs in skill_signals.items() if sig in sigs]
        check(owners == [owner], f"exclusive signal '{sig}' only on {owner}; owners={owners}")

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
        expected_col = re.findall(r"\|\s*((?:BUILD|FIX|RESEARCH|DESIGN|WRITE|OPERATE|ADVISE)(?:\s*\+\s*[A-Z]+)*|（不路由全协议）)\s*\|", scen)
        check(len(expected_col) >= 15, f"scenarios have >=15 expected rows; got {len(expected_col)}")
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
