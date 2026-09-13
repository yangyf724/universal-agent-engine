#!/usr/bin/env python3
"""v2 static validation for universal-agent-engine skill.

校验 v2 双角色契约：
  - 结构：仅 2 份 references、2 份 tests、frontmatter、body 预算
  - 路由：三出口、委托映射、禁止自执行全协议
  - Soft：模态采集/测试/Grill Research；禁止非模态 Soft 卡与九阶段
  - 指针：SKILL 只指向 intent-gate.md / multimodal.md

运行:
    python skill/tests/run_static_checks.py
    # 期望：ALL CHECKS PASSED
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFS = ROOT / "references"
TESTS = ROOT / "tests"
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
    "process-gates",
    "compose-phases",
    "compose-token",
    "compose-handoff",
    "intent-router",
    "research-citations",
    "quality-gates",
    "BUILD / FIX",
]

REQUIRED_GATES = ["ADVISE", "compose-next", "专项委托"]
REQUIRED_SOFT = ["Modality Scan", "Soft-Test", "Soft-Research", "fan-out"]
DELEGATE_SKILLS = [
    "pptx-official",
    "docx-official",
    "xlsx-official",
    "pdf-official",
    "3d-creation",
    "imagegen",
    "deep-research",
    "github-sync",
]


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


def body_of(text: str) -> str:
    parts = text.split("---\n", 2)
    return parts[2] if len(parts) >= 3 else text


def fm_of(text: str) -> str:
    parts = text.split("---\n", 2)
    return parts[1] if len(parts) >= 3 else ""


def main() -> int:
    # ------------------------------------------------------------------
    # L1 结构
    # ------------------------------------------------------------------
    check(SKILL.exists(), "SKILL.md exists")
    text = SKILL.read_text(encoding="utf-8")
    check(text.startswith("---\n"), "starts with YAML frontmatter")
    parts = text.split("---\n", 2)
    check(len(parts) >= 3, "frontmatter closed")
    fm = fm_of(text)
    body = body_of(text)
    check("name: universal-agent-engine" in fm, "name is universal-agent-engine")

    desc_m = re.search(r"^description:\s*(.+?)(?=\n[a-zA-Z-]+:|\n---|$)", fm, re.M | re.S)
    desc = desc_m.group(1) if desc_m else ""
    check(bool(desc), "description parsed")
    check("gate" in desc.lower(), "description mentions gate")
    check("multimodal" in desc.lower(), "description mentions multimodal")
    check("compose-next" in desc, "description mentions compose-next")
    # 负触发：不应再宣称七 mode 编排执行
    check("BUILD/FIX" not in desc and "七 mode" not in desc, "description drops 7-mode claim")

    # body 体量：v2 目标 ≤2500
    body_len = len(body)
    check(body_len <= 2500, f"body length {body_len} <= 2500")
    check(body_len >= 800, f"body length {body_len} >= 800 (not empty)")

    # references 仅 2 文件
    ref_files = sorted(p.name for p in REFS.glob("*.md")) if REFS.exists() else []
    check(ref_files == ["intent-gate.md", "multimodal.md"], f"references only 2 files, got {ref_files}")

    # tests 仅 2 文件
    test_files = sorted(p.name for p in TESTS.iterdir() if p.is_file()) if TESTS.exists() else []
    check(
        set(test_files) == {"run_static_checks.py", "checklist.md"},
        f"tests only static+checklist, got {test_files}",
    )

    # locales
    for loc in ("zh-CN.json", "en-US.json"):
        p = ROOT / "locales" / loc
        check(p.exists(), f"locales/{loc} exists")

    # ------------------------------------------------------------------
    # L2 路由三出口
    # ------------------------------------------------------------------
    for token in REQUIRED_GATES:
        check(token in body, f"SKILL body has exit token: {token}")
    check(
        ("禁止**自执行" in body) or ("禁止本 skill 自" in body) or ("不再是一般编排" in body),
        "body forbids self full protocol",
    )
    check("映射表" in body or "intent-gate" in body, "body points to intent-gate")

    gate = (REFS / "intent-gate.md").read_text(encoding="utf-8") if (REFS / "intent-gate.md").exists() else ""
    check("### 1. ADVISE" in gate, "gate has ADVISE section")
    check("### 2. 建议 compose-next" in gate, "gate has compose-next section")
    check("### 3. 专项委托" in gate, "gate has delegate section")
    for skill in DELEGATE_SKILLS:
        check(skill in gate, f"gate maps delegate skill: {skill}")
    check("禁止" in gate and "全协议" in gate, "gate hard-bans full protocol")
    check("反例" in gate, "gate has anti-examples")

    # ------------------------------------------------------------------
    # L3 Soft / multimodal
    # ------------------------------------------------------------------
    for token in REQUIRED_SOFT:
        check(token in body, f"SKILL body has Soft token: {token}")
    check("零 Soft" in body, "body states Workspace/Finish zero Soft")

    multi = (REFS / "multimodal.md").read_text(encoding="utf-8") if (REFS / "multimodal.md").exists() else ""
    check("Modality Scan" in multi, "multimodal has Modality Scan")
    check("Soft-Test" in multi, "multimodal has Soft-Test")
    check("Soft-Research" in multi, "multimodal has Soft-Research")
    check(re.search(r"≤\s*40", multi) is not None, "multimodal research pack size bound")
    check("降级" in multi, "multimodal has degradation table")
    check("跨模态" in multi, "multimodal has cross-modal gate")
    check("禁止" in multi and "假装" in multi, "multimodal forbids fake media")
    check("Soft-Spec-input" in multi and "禁止" in multi, "multimodal bans Spec-input")
    check("Workspace" in multi and "Finish" in multi, "multimodal states Workspace/Finish exclusion")

    # ------------------------------------------------------------------
    # L4 禁词（body + 2 refs）
    # ------------------------------------------------------------------
    corpus = body + "\n" + gate + "\n" + multi
    ban_ok_tokens = {
        "Soft-Spec-input",
        "Soft-Review-pack",
        "Soft-Report",
        "九阶段",
        "七 mode",
        "Soft Depth",
        "Soft-Depth",
    }
    for word in BANNED_BODY:
        if word not in corpus:
            ok(f"legacy token absent: {word}")
            continue
        if word in ban_ok_tokens:
            lines = corpus.splitlines()
            allowed = any(
                word in ln and ("禁止" in ln or "零" in ln or "砍" in ln or "跳过" in ln)
                for ln in lines
            )
            check(allowed, f"banned token {word} only appears in ban context")
        else:
            check(False, f"legacy token should be absent: {word}")

    # 指针只指向 2 refs
    pointers = re.findall(r"references/([\w-]+\.md)", body + gate)
    allowed_ptrs = {"intent-gate.md", "multimodal.md"}
    bad_ptrs = sorted(set(pointers) - allowed_ptrs)
    check(not bad_ptrs, f"pointers only to 2 refs, bad={bad_ptrs}")

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
