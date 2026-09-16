#!/usr/bin/env python3
"""v2 static validation for universal-agent-engine skill.

校验 v2 双角色契约：
  - 结构：仅 2 份 references、2 份 tests、frontmatter、body 预算、locales schema
  - 路由：三出口、委托映射（16 skill id）、禁止自执行全协议
  - Soft：模态采集/测试/Grill Research；禁止非模态 Soft 卡与九阶段
  - 指针：SKILL 必须同时指向 intent-gate.md 与 multimodal.md

运行:
    python skill/tests/run_static_checks.py
    # 期望：ALL CHECKS PASSED
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFS = ROOT / "references"
TESTS = ROOT / "tests"
LOCALES = ROOT / "locales"
FAILURES: list[str] = []
PASSES: list[str] = []

# v2 契约：不应再出现在 skill 包内的遗留协议词
BANNED_BODY = [
    "七 mode",
    "Step 2",
    "Step 3",
    "Step 4",
    "Step 5",
    "Step 6",
    "Role Lens",
    "Soft-Depth",
    "Soft Depth",
    "九阶段",
    "Soft-Spec-input",
    "Soft-Review-pack",
    "Soft-Report",
    "Soft-Orient",
    "process-gates",
    "compose-phases",
    "compose-token",
    "compose-handoff",
    "intent-router",
    "research-citations",
    "quality-gates",
    "BUILD / FIX",
    "BUILD/FIX",
]

# 允许出现在 ban 语境（同行含 禁止/零/砍/跳过）的词
BAN_OK_TOKENS = {
    "Soft-Spec-input",
    "Soft-Review-pack",
    "Soft-Report",
    "Soft-Orient",
    "九阶段",
    "七 mode",
    "Soft Depth",
    "Soft-Depth",
}

# 需要词边界匹配的 Step 系列（避免 Step 20 / Step 2.1 假阳性）
STEP_BAN_RE = re.compile(r"Step\s+[2-6]\b")
BUILD_FIX_RE = re.compile(r"BUILD\s*/\s*FIX")

REQUIRED_GATES = ["ADVISE", "compose-next", "专项委托"]
REQUIRED_SOFT = ["Modality Scan", "Soft-Test", "Soft-Research", "fan-out"]

# intent-gate.md 映射表中出现的全部 skill id（15 行 / 16 id）
DELEGATE_SKILLS = [
    "pptx-official",
    "docx-official",
    "xlsx-official",
    "pdf-official",
    "3d-creation",
    "threejs-game-skills",
    "imagegen",
    "deep-research",
    "arxiv",
    "research-paper-writing",
    "github-sync",
    "figma",
    "visualizer",
    "product-design",
    "frontend-design",
    "mate",
]

ALLOWED_REFS = {"intent-gate.md", "multimodal.md"}
LOCALE_KEYS = {"displayName", "brief"}


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


def normalize_text(raw: str) -> str:
    if raw.startswith("﻿"):
        raw = raw[1:]
    return raw.replace("\r\n", "\n").replace("\r", "\n")


def parse_frontmatter(text: str) -> tuple[str, str, bool]:
    """Return (fm, body, closed). body is full text when FM is missing/unclosed."""
    if not text.startswith("---\n"):
        return "", text, False
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return "", text, False
    return parts[1], parts[2], True


def ban_keywords(line: str) -> bool:
    return any(k in line for k in ("禁止", "零", "砍", "跳过", "不再", "删除"))


def main() -> int:
    # ------------------------------------------------------------------
    # L1 结构
    # ------------------------------------------------------------------
    check(SKILL.exists(), "SKILL.md exists")
    raw = SKILL.read_text(encoding="utf-8")
    text = normalize_text(raw)
    check(text.startswith("---\n"), "starts with YAML frontmatter")
    fm, body, fm_closed = parse_frontmatter(text)
    check(fm_closed, "frontmatter closed")
    check("name: universal-agent-engine" in fm, "name is universal-agent-engine")

    desc_m = re.search(
        r"^description:\s*(.+?)(?=\n[A-Za-z0-9_-]+:|\n---|\Z)",
        fm,
        re.M | re.S,
    )
    desc = desc_m.group(1) if desc_m else ""
    check(bool(desc), "description parsed")
    check("gate" in desc.lower(), "description mentions gate")
    check("multimodal" in desc.lower(), "description mentions multimodal")
    check("compose-next" in desc, "description mentions compose-next")
    check(
        "BUILD/FIX" not in desc and "BUILD / FIX" not in desc and "七 mode" not in desc,
        "description drops 7-mode claim",
    )

    body_len = len(body)
    check(body_len <= 2500, f"body length {body_len} <= 2500")
    check(body_len >= 800, f"body length {body_len} >= 800 (not empty)")

    # references 全量（文件+目录）
    ref_entries = sorted(p.name for p in REFS.iterdir()) if REFS.exists() else []
    check(ref_entries == ["intent-gate.md", "multimodal.md"], f"references only 2 files, got {ref_entries}")

    test_files = sorted(p.name for p in TESTS.iterdir() if p.is_file()) if TESTS.exists() else []
    check(
        set(test_files) == {"run_static_checks.py", "checklist.md"},
        f"tests only static+checklist, got {test_files}",
    )

    # locales: 存在 + JSON + 键
    locale_data: dict[str, dict] = {}
    for loc in ("zh-CN.json", "en-US.json"):
        p = LOCALES / loc
        check(p.exists(), f"locales/{loc} exists")
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"locales/{loc} valid JSON: {exc}")
            continue
        ok(f"locales/{loc} valid JSON")
        check(isinstance(data, dict), f"locales/{loc} is object")
        check(
            LOCALE_KEYS <= set(data),
            f"locales/{loc} has displayName/brief, keys={sorted(data)}",
        )
        check(
            all(isinstance(data.get(k), str) and data[k].strip() for k in LOCALE_KEYS),
            f"locales/{loc} displayName/brief non-empty strings",
        )
        locale_data[loc] = data
    if len(locale_data) == 2:
        check(
            set(locale_data["zh-CN.json"]) == set(locale_data["en-US.json"]),
            "locale key parity zh/en",
        )

    # ------------------------------------------------------------------
    # L2 路由三出口
    # ------------------------------------------------------------------
    for token in REQUIRED_GATES:
        check(token in body, f"SKILL body has exit token: {token}")
    check(
        re.search(r"禁止.*自执行|不再是一般编排|禁止本 skill 自", body) is not None,
        "body forbids self full protocol",
    )
    check("映射表" in body or "intent-gate" in body, "body points to intent-gate")

    gate_path = REFS / "intent-gate.md"
    gate = normalize_text(gate_path.read_text(encoding="utf-8")) if gate_path.exists() else ""
    check("### 1. ADVISE" in gate, "gate has ADVISE section")
    check("### 2. 建议 compose-next" in gate, "gate has compose-next section")
    check("### 3. 专项委托" in gate, "gate has delegate section")
    for skill in DELEGATE_SKILLS:
        check(
            f"`{skill}`" in gate,
            f"gate maps delegate skill: {skill}",
        )
    check(re.search(r"禁止[^\n]*全协议|全协议[^\n]*禁止", gate) is not None, "gate hard-bans full protocol")
    check("反例" in gate, "gate has anti-examples")

    # ------------------------------------------------------------------
    # L3 Soft / multimodal
    # ------------------------------------------------------------------
    for token in REQUIRED_SOFT:
        check(token in body, f"SKILL body has Soft token: {token}")
    check("零 Soft" in body, "body states Workspace/Finish zero Soft")

    multi_path = REFS / "multimodal.md"
    multi = normalize_text(multi_path.read_text(encoding="utf-8")) if multi_path.exists() else ""
    check("Modality Scan" in multi, "multimodal has Modality Scan")
    check("Soft-Test" in multi, "multimodal has Soft-Test")
    check("Soft-Research" in multi, "multimodal has Soft-Research")
    check(re.search(r"证据包[^\n]*≤\s*40|≤\s*40[^\n]*证据包|Soft-Research[^\n]*≤\s*40", multi) is not None,
        "multimodal research pack size bound")
    check("降级" in multi, "multimodal has degradation table")
    check("跨模态" in multi, "multimodal has cross-modal gate")
    check(
        re.search(r"禁止[^\n]*假装|假装[^\n]*禁止", multi) is not None,
        "multimodal forbids fake media",
    )
    check(
        re.search(r"禁止[^\n]*Soft-Spec-input", multi) is not None,
        "multimodal bans Spec-input on same line",
    )
    check(
        re.search(r"禁止[^\n]*Soft-Orient", multi) is not None,
        "multimodal bans Soft-Orient on same line",
    )
    check(
        re.search(r"Workspace[^\n]*Finish|Finish[^\n]*Workspace", multi) is not None
        and "零 Soft" in multi,
        "multimodal states Workspace/Finish zero Soft",
    )

    # ------------------------------------------------------------------
    # L4 禁词（body + 2 refs + description）
    # ------------------------------------------------------------------
    corpus_lines = (body + "\n" + gate + "\n" + multi + "\n" + desc).splitlines()
    # Step 2–6 用词边界
    step_hits = [
        ln for ln in corpus_lines
        if STEP_BAN_RE.search(ln) and not ban_keywords(ln)
    ]
    check(not step_hits, f"Step 2-6 only in ban context or absent, bad={step_hits[:3]}")

    # BUILD / FIX 归一
    build_hits = [
        ln for ln in corpus_lines
        if BUILD_FIX_RE.search(ln) and not ban_keywords(ln)
    ]
    check(not build_hits, f"BUILD/FIX only in ban context or absent, bad={build_hits[:3]}")

    for word in BANNED_BODY:
        if word in ("Step 2", "Step 3", "Step 4", "Step 5", "Step 6", "BUILD / FIX", "BUILD/FIX"):
            continue  # 已由正则处理
        hits = [ln for ln in corpus_lines if word in ln]
        if not hits:
            ok(f"legacy token absent: {word}")
            continue
        if word in BAN_OK_TOKENS:
            bad = [ln for ln in hits if not ban_keywords(ln)]
            check(
                not bad,
                f"banned token {word} only appears in ban context, bad={bad[:2]}",
            )
        else:
            check(False, f"legacy token should be absent: {word}")

    # 指针：禁指向其他 refs（扫 body+gate）；body 必须同时指向 2 refs
    pointer_corpus = body + "\n" + gate
    pointers = re.findall(r"references/([\w-]+\.md)", pointer_corpus)
    bad_ptrs = sorted(set(pointers) - ALLOWED_REFS)
    check(not bad_ptrs, f"pointers only to 2 refs, bad={bad_ptrs}")
    body_ptrs = set(re.findall(r"references/([\w-]+\.md)", body))
    check(
        "intent-gate.md" in body_ptrs and "multimodal.md" in body_ptrs,
        f"body points to both refs, got {sorted(body_ptrs)}",
    )

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
