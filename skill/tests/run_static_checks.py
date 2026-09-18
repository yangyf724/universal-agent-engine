#!/usr/bin/env python3
"""v2 static validation for universal-agent-engine skill.

校验 v2 双角色契约：
  - 结构：仅 2 份 references、2 份 tests、frontmatter、body 预算、locales schema
  - 路由：Priority 完整性、三出口、委托映射、禁止自执行全协议
  - Soft：模态采集/测试/Grill Research；禁令集合对齐；禁止非模态 Soft 卡
  - 指针：SKILL/gate/multimodal 仅指向 2 份允许 references
  - 卫生：EOL、版本三处对齐、ban 极性、Last-sync SHA 可解析、负向自测入口

运行:
    python skill/tests/run_static_checks.py
    # 期望：ALL CHECKS PASSED
    python skill/tests/run_static_checks.py --negative-self-test
    # 期望：NEGATIVE SELF-TEST PASSED
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
SKILL = ROOT / "SKILL.md"
REFS = ROOT / "references"
TESTS = ROOT / "tests"
LOCALES = ROOT / "locales"
FAILURES: list[str] = []
PASSES: list[str] = []

CHECKER_MARKER = "v2 static validation for universal-agent-engine skill"
NEGATIVE_FLAG = "--negative-self-test"
MIN_ASSERTIONS = 120

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

STEP_BAN_RE = re.compile(r"Step\s+[2-6]\b")
BUILD_FIX_RE = re.compile(r"BUILD\s*/\s*FIX")
STEP_NAME_RE = re.compile(r"[五六]步")

# ban 极性：仅显式禁令，不再把「零/不再/删除」当作通行证
STRONG_BAN_RE = re.compile(
    r"(禁止|不得|不要|不用|勿用|弃用|不再使用|不再采用|不再指称|不再作为|已移除|已删除|砍掉)"
)
PROTOCOL_SKIP_RE = re.compile(
    r"跳过[^\n]{0,64}(全协议|七\s*mode|Step\s+[2-6]|五步|六步)|全协议与七\s*mode"
)
POSITIVE_LEAK_RE = re.compile(r"(可开放|恢复启用|允许加载|作草稿入口|联动执行)")

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

# SKILL / multimodal 禁令集合必须同时点名的 Soft 卡
SOFT_BAN_PARITY = [
    "Soft-Spec-input",
    "Soft-Review-pack",
    "Soft-Report",
    "Soft-Orient",
    "九阶段",
    "Soft Depth",
]

CRLF_ASSETS = [
    SKILL,
    REFS / "intent-gate.md",
    REFS / "multimodal.md",
    TESTS / "checklist.md",
    LOCALES / "zh-CN.json",
    LOCALES / "en-US.json",
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


def safe_read(path: Path) -> str | None:
    """Read UTF-8 text; None on missing or undecodable file (already FAILed)."""
    if not path.exists():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{path.name} decodes as UTF-8: {exc}")
        return None


def normalize_text(raw: str) -> str:
    if raw.startswith("\ufeff"):
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
    """True only when the line documents an explicit ban/negation."""
    if STRONG_BAN_RE.search(line):
        if POSITIVE_LEAK_RE.search(line) and not re.search(r"(禁止|不得|弃用)", line):
            return False
        return True
    return bool(PROTOCOL_SKIP_RE.search(line))


def latest_changelog_version(changelog: str) -> str | None:
    m = re.search(r"^##\s*\[(\d+\.\d+\.\d+)\]", changelog, re.M)
    return m.group(1) if m else None


def readme_version(readme: str) -> str | None:
    m = re.search(r"\*\*Version:\*\*\s*(\d+\.\d+\.\d+)", readme)
    return m.group(1) if m else None


def checklist_version(checklist: str) -> str | None:
    m = re.search(r"^#\s*v?(\d+\.\d+\.\d+)\s+Checklist", checklist, re.M)
    return m.group(1) if m else None


def eol_profile(data: bytes) -> tuple[int, int]:
    crlf = data.count(b"\r\n")
    lf_only = data.count(b"\n") - crlf
    return crlf, lf_only


def token_hits(line: str, token: str) -> bool:
    """Case/whitespace-insensitive containment for banned tokens."""
    norm_line = re.sub(r"\s+", " ", line).lower()
    norm_tok = re.sub(r"\s+", " ", token).lower()
    return norm_tok in norm_line


def priority_item(prio_text: str, index: int) -> str:
    """Return the numbered Priority item body (1-based), or empty string."""
    m = re.search(rf"^{index}\.\s*(.*?)(?=^\d+\.\s|\Z)", prio_text, re.M | re.S)
    return m.group(1).strip() if m else ""


def main() -> int:
    # ------------------------------------------------------------------
    # Meta / structure
    # ------------------------------------------------------------------
    checker_src = Path(__file__).read_text(encoding="utf-8")
    check(CHECKER_MARKER in checker_src, "checker docstring marker present")
    check(NEGATIVE_FLAG in checker_src, "checker implements --negative-self-test")

    check(SKILL.exists(), "SKILL.md exists")
    raw = safe_read(SKILL)
    check(raw is not None, "SKILL.md readable as UTF-8")
    if raw is None:
        print()
        print(f"SUMMARY passes={len(PASSES)} failures={len(FAILURES)}")
        return 1
    text = normalize_text(raw)
    check(text.startswith("---\n"), "starts with YAML frontmatter")
    fm, body, fm_closed = parse_frontmatter(text)
    check(fm_closed, "frontmatter closed")
    check(
        re.search(r"^name:\s*universal-agent-engine\s*$", fm, re.M) is not None,
        "name is exactly universal-agent-engine",
    )

    desc_m = re.search(
        r"^description:\s*(.+?)(?=\n[A-Za-z0-9_-]+:|\n---|\Z)",
        fm,
        re.M | re.S,
    )
    desc = desc_m.group(1) if desc_m else ""
    check(bool(desc), "description parsed")
    check(
        re.search(r"(?i)\bgate\b", desc) is not None or "门控" in desc,
        "description mentions gate",
    )
    check("multimodal" in desc.lower(), "description mentions multimodal")
    check("compose-next" in desc, "description mentions compose-next")
    check(
        re.search(r"(?i)7\s*mode|七\s*mode|七Mode|七模式|seven-mode|七种模式|BUILD\s*/\s*FIX", desc)
        is None,
        "description drops 7-mode claim",
    )
    check(
        "Do NOT" in desc or "不" in desc,
        "description includes negative exits",
    )

    body_len = len(body)
    check(body_len <= 2500, f"body length {body_len} <= 2500")
    check(body_len >= 800, f"body length {body_len} >= 800 (not empty)")

    ref_entries = sorted(p.name for p in REFS.iterdir()) if REFS.exists() else []
    check(ref_entries == ["intent-gate.md", "multimodal.md"], f"references only 2 files, got {ref_entries}")

    test_entries = sorted(
        p.name
        for p in TESTS.iterdir()
        if not p.name.startswith(".")
        and not p.name.endswith(".baiduyun.uploading.cfg")
        and ".baiduyun." not in p.name
        and not p.name.endswith(".tmp")
    ) if TESTS.exists() else []
    check(
        set(test_entries) == {"run_static_checks.py", "checklist.md"},
        f"tests only static+checklist, got {test_entries}",
    )

    # locales
    locale_data: dict[str, dict] = {}
    for loc in ("zh-CN.json", "en-US.json"):
        p = LOCALES / loc
        check(p.exists(), f"locales/{loc} exists")
        if not p.exists():
            continue
        raw_loc = safe_read(p)
        if raw_loc is None:
            check(False, f"locales/{loc} readable as UTF-8")
            continue
        try:
            data = json.loads(raw_loc)
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

    # EOL skill text assets CRLF; checker .py LF
    for path in CRLF_ASSETS:
        if not path.exists():
            check(False, f"EOL asset exists: {path.name}")
            continue
        crlf, lf_only = eol_profile(path.read_bytes())
        check(
            lf_only == 0 and crlf > 0,
            f"EOL CRLF-only: {path.name} (crlf={crlf}, bare_lf={lf_only})",
        )
    py_path = TESTS / "run_static_checks.py"
    if py_path.exists():
        crlf_py, lf_py = eol_profile(py_path.read_bytes())
        check(
            crlf_py == 0 and lf_py > 0,
            f"EOL LF-only: run_static_checks.py (crlf={crlf_py}, bare_lf={lf_py})",
        )

    # versions + checklist expected pass
    readme_p = REPO / "README.md"
    changelog_p = REPO / "CHANGELOG.md"
    checklist_p = TESTS / "checklist.md"
    readme_raw = safe_read(readme_p)
    changelog_raw = safe_read(changelog_p)
    checklist_raw = safe_read(checklist_p)
    check(readme_raw is not None, "README.md readable")
    check(changelog_raw is not None, "CHANGELOG.md readable")
    check(checklist_raw is not None, "checklist.md readable")
    expected_pass = None
    if readme_raw and changelog_raw and checklist_raw:
        rv = readme_version(readme_raw)
        cv = latest_changelog_version(changelog_raw)
        kv = checklist_version(checklist_raw)
        check(rv is not None, f"README Version parsed, got {rv}")
        check(cv is not None, f"CHANGELOG latest version parsed, got {cv}")
        check(kv is not None, f"checklist title version parsed, got {kv}")
        check(rv == cv == kv, f"version aligned README/CHANGELOG/checklist: {rv}/{cv}/{kv}")
        sha_m = re.search(r"Last sync:.*?([0-9a-f]{7,40})", readme_raw)
        check(sha_m is not None, "README Last sync includes short SHA")
        if sha_m:
            sha = sha_m.group(1)
            git_dir = REPO / ".git"
            if git_dir.exists():
                try:
                    r = subprocess.run(
                        ["git", "-C", str(REPO), "rev-parse", "--verify", f"{sha}^{{commit}}"],
                        capture_output=True,
                        text=True,
                    )
                    check(r.returncode == 0, f"README Last sync SHA exists in git: {sha}")
                except OSError as exc:
                    fail(f"git verify Last sync SHA failed to run: {exc}")
            else:
                ok(f"Last sync SHA present (no .git to verify): {sha}")
        m_pass = re.search(r"期望 pass：\s*(\d+)", checklist_raw)
        check(m_pass is not None, "checklist declares 期望 pass：N")
        expected_pass = int(m_pass.group(1)) if m_pass else None

    # current-contract docs hygiene (README-designated)
    spec_p = REPO / "docs" / "compose" / "spec" / "v2-gate-multimodal.md"
    check(spec_p.exists(), "current spec v2-gate-multimodal.md exists")
    spec_raw = safe_read(spec_p) if spec_p.exists() else None
    if spec_raw is not None:
        spec_n = normalize_text(spec_raw)
        check("status: delivered" in spec_n, "current spec status delivered")
        spec_lines = spec_n.splitlines()
        bad_spec_step = [
            ln
            for ln in spec_lines
            if STEP_NAME_RE.search(ln) and not ban_keywords(ln)
        ]
        check(
            not bad_spec_step,
            f"current spec has no non-ban 五步/六步, bad={bad_spec_step[:3]}",
        )
        check(
            "Priority" in spec_n or "Soft 早退" in spec_n,
            "current spec mentions Soft Priority / early-exit",
        )
        if readme_raw:
            check(
                "v2-gate-multimodal.md" in readme_raw,
                "README tree lists v2-gate-multimodal.md",
            )

    # ------------------------------------------------------------------
    # L2 路由 / Priority
    # ------------------------------------------------------------------
    for token in REQUIRED_GATES:
        check(token in body, f"SKILL body has exit token: {token}")
    check(
        re.search(r"禁止.*自执行|不再是一般编排|禁止本 skill 自", body) is not None,
        "body forbids self full protocol",
    )
    check("映射表" in body or "intent-gate" in body, "body points to intent-gate")

    gate_path = REFS / "intent-gate.md"
    gate_raw = safe_read(gate_path)
    gate = normalize_text(gate_raw) if gate_raw is not None else ""
    check(gate_raw is not None, "intent-gate.md readable")
    check("### 1. ADVISE" in gate, "gate has ADVISE section")
    check("### 2. 建议 compose-next" in gate, "gate has compose-next section")
    check("### 3. 专项委托" in gate, "gate has delegate section")
    for skill in DELEGATE_SKILLS:
        check(f"`{skill}`" in gate, f"gate maps delegate skill: {skill}")
    check(re.search(r"禁止[^\n]*全协议|全协议[^\n]*禁止", gate) is not None, "gate hard-bans full protocol")
    check("反例" in gate, "gate has anti-examples")

    prio_m = re.search(r"##\s*Priority\s*\n(.*?)(?=\n##\s)", gate, re.S)
    prio_text = prio_m.group(1) if prio_m else ""
    check(bool(prio_text), "gate has Priority section")
    prio_items = re.findall(r"^\d+\.\s*", prio_text, re.M)
    check(len(prio_items) >= 4, f"Priority has >=4 numbered branches, got {len(prio_items)}")

    item1 = priority_item(prio_text, 1)
    item2 = priority_item(prio_text, 2)
    item3 = priority_item(prio_text, 3)
    item4 = priority_item(prio_text, 4)
    item5 = priority_item(prio_text, 5)

    check("Soft" in item1 and "独立模态子任务" in item1, "Priority1 Soft requires independent modality")
    check(
        re.search(r"会话已在 compose-next|compose-next / P-domain", item1) is not None,
        "Priority1 names already-in compose-next / P-domain",
    )
    check(
        re.search(r"不.*展开三出口|不.*三出口", item1) is not None,
        "Priority1 Soft path skips three exits",
    )
    check(
        re.search(r"无独立模态", item2) is not None
        and re.search(r"不展开|不 Soft|不三出口|不专项委托", item2) is not None,
        "Priority2 compose-next without modality does not expand",
    )
    check(
        re.search(r"不.*展开三出口|不三出口", item2) is not None,
        "Priority2 explicitly skips three exits",
    )
    check(
        re.search(r"点名", item3) is not None
        and re.search(r"只\s*compose-next|只 compose-next", item3) is not None,
        "Priority3 named compose-next is compose-next only",
    )
    check(
        re.search(r"不.*展开三出口|不.*三出口", item3) is not None,
        "Priority3 named compose-next skips three exits",
    )
    check(
        re.search(r"纯聊天|无产物", item4) is not None,
        "Priority4 pure chat / no artifact does not trigger",
    )
    check(
        re.search(r"否则", item5) is not None and "三出口" in item5,
        "Priority5 else falls to three exits",
    )
    check(
        re.search(r"无映射|转写|配音", gate) is not None,
        "gate documents standalone unmapped modality rule",
    )

    check(
        re.search(r"有独立模态|否则不展开", gate) is not None,
        "gate hard-rule parenthetical qualifies Soft vs no-expand",
    )

    # ------------------------------------------------------------------
    # L3 Soft / multimodal
    # ------------------------------------------------------------------
    for token in REQUIRED_SOFT:
        check(token in body, f"SKILL body has Soft token: {token}")
    check("零 Soft" in body, "body states Workspace/Finish zero Soft")

    multi_path = REFS / "multimodal.md"
    multi_raw = safe_read(multi_path)
    multi = normalize_text(multi_raw) if multi_raw is not None else ""
    check(multi_raw is not None, "multimodal.md readable")
    check("Modality Scan" in multi, "multimodal has Modality Scan")
    check("Soft-Test" in multi, "multimodal has Soft-Test")
    check("Soft-Research" in multi, "multimodal has Soft-Research")
    check(
        re.search(r"证据包[^\n]*≤\s*40|≤\s*40[^\n]*证据包|Soft-Research[^\n]*≤\s*40", multi) is not None,
        "multimodal research pack size bound",
    )
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
    check(
        re.search(r"会话已在 compose-next", multi) is not None,
        "multimodal activation requires already-in compose-next",
    )

    # Soft ban parity: SKILL body + multimodal must both name the set
    body_soft_ban_line = next((ln for ln in body.splitlines() if "Soft-Spec-input" in ln), "")
    multi_soft_ban_line = next((ln for ln in multi.splitlines() if "Soft-Spec-input" in ln), "")
    for tok in SOFT_BAN_PARITY:
        check(tok in body_soft_ban_line, f"SKILL ban list includes {tok}")
        check(tok in multi_soft_ban_line, f"multimodal ban line includes {tok}")

    # ------------------------------------------------------------------
    # L4 禁词 + 指针
    # ------------------------------------------------------------------
    corpus_lines = (body + "\n" + gate + "\n" + multi + "\n" + desc).splitlines()

    step_hits = [
        ln for ln in corpus_lines
        if STEP_BAN_RE.search(ln) and not ban_keywords(ln)
    ]
    check(not step_hits, f"Step 2-6 only in ban context or absent, bad={step_hits[:3]}")

    build_hits = [
        ln for ln in corpus_lines
        if BUILD_FIX_RE.search(ln) and not ban_keywords(ln)
    ]
    check(not build_hits, f"BUILD/FIX only in ban context or absent, bad={build_hits[:3]}")

    step_name_hits = [
        ln for ln in corpus_lines
        if STEP_NAME_RE.search(ln) and not ban_keywords(ln)
    ]
    check(
        not step_name_hits,
        f"legacy step-count names (五步/六步) only in ban context, bad={step_name_hits[:3]}",
    )

    for word in BANNED_BODY:
        if word in ("Step 2", "Step 3", "Step 4", "Step 5", "Step 6", "BUILD / FIX", "BUILD/FIX"):
            continue  # already handled by regex
        hits = [ln for ln in corpus_lines if token_hits(ln, word)]
        if not hits:
            ok(f"legacy token absent: {word}")
            continue
        bad = [ln for ln in hits if not ban_keywords(ln)]
        check(
            not bad,
            f"banned token {word} only appears in ban polarity, bad={bad[:2]}",
        )

    pointer_corpus = body + "\n" + gate + "\n" + multi
    pointers = re.findall(r"(?:references/)?([A-Za-z0-9_-]+\.md)", pointer_corpus)
    # Only constrain references/*.md pointers and explicit references/*.md paths
    ref_pointers = re.findall(r"references/([\w-]+\.md)", pointer_corpus)
    bad_ptrs = sorted(set(ref_pointers) - ALLOWED_REFS)
    check(not bad_ptrs, f"pointers only to 2 refs, bad={bad_ptrs}")
    # bare md names that look like deleted v1 refs
    banned_bare = {
        "compose-phases.md",
        "process-gates.md",
        "compose-token.md",
        "quality-gates.md",
        "compose-handoff.md",
        "intent-router.md",
        "research-citations.md",
        "extra.md",
    }
    bare_bad = sorted({p for p in pointers if p in banned_bare})
    check(not bare_bad, f"no banned bare ref names, bad={bare_bad}")
    body_ptrs = set(re.findall(r"references/([\w-]+\.md)", body))
    check(
        "intent-gate.md" in body_ptrs and "multimodal.md" in body_ptrs,
        f"body points to both refs, got {sorted(body_ptrs)}",
    )
    check(
        "multimodal.md" in gate,
        "gate references multimodal.md explicitly",
    )

    # checklist standalone must not advertise compose Soft as standalone exit
    if checklist_raw:
        cl_n = normalize_text(checklist_raw)
        route_sec = re.search(r"##\s*路由自检（standalone）\s*\n(.*?)(?=\n##\s|\Z)", cl_n, re.S)
        if route_sec:
            bad_route = [
                ln
                for ln in route_sec.group(1).splitlines()
                if "compose Soft" in ln and "不提前 Soft" not in ln and "Soft 仅" not in ln
            ]
            check(not bad_route, f"standalone checklist rows avoid compose Soft exit, bad={bad_route[:2]}")
        else:
            check(False, "checklist has standalone routing section")

    # ------------------------------------------------------------------
    # 汇总
    # ------------------------------------------------------------------
    check(len(PASSES) >= MIN_ASSERTIONS, f"assertion floor {MIN_ASSERTIONS} met, got {len(PASSES)}")
    if expected_pass is not None:
        projected = len(PASSES) + 1  # this meta-check itself
        check(
            expected_pass == projected,
            f"checklist expected pass {expected_pass} matches projected {projected}",
        )
    else:
        check(False, "checklist expected pass missing — meta-gate required")

    print()
    print(f"SUMMARY passes={len(PASSES)} failures={len(FAILURES)}")
    if FAILURES:
        print("FAILURES:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("ALL CHECKS PASSED")
    return 0


def _write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _inject_crlf_append(path: Path, text: str) -> None:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    # normalize to CRLF then append
    t = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    t = t + "\n" + text.replace("\r\n", "\n") + "\n"
    out = t.replace("\n", "\r\n").encode("utf-8")
    _write_bytes(path, out)


def _run_checker_on_repo(repo: Path) -> tuple[int, str]:
    script = repo / "skill" / "tests" / "run_static_checks.py"
    r = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        cwd=str(repo),
        encoding="utf-8",
        errors="replace",
        env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"},
    )
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def negative_self_test() -> int:
    """Copy package to temp, inject breaks, expect default gate to FAIL for the right reason."""
    print("NEGATIVE SELF-TEST")
    src_repo = REPO
    cases_failed: list[str] = []
    cases_passed: list[str] = []

    def clone() -> Path:
        tmp = Path(tempfile.mkdtemp(prefix="uae-neg-"))
        shutil.copytree(src_repo / "skill", tmp / "skill")
        for name in ("README.md", "CHANGELOG.md"):
            if (src_repo / name).exists():
                shutil.copy2(src_repo / name, tmp / name)
        docs_src = src_repo / "docs" / "compose" / "spec"
        if docs_src.exists():
            dest = tmp / "docs" / "compose" / "spec"
            dest.mkdir(parents=True, exist_ok=True)
            for name in ("v2-gate-multimodal.md", "bug-hunt-v4.md"):
                src = docs_src / name
                if src.exists():
                    shutil.copy2(src, dest / name)
        return tmp

    def expect_fail(label: str, mutate, needle: str | None = None) -> None:
        tmp = clone()
        try:
            mutate(tmp)
            rc, out = _run_checker_on_repo(tmp)
            if rc == 0:
                cases_failed.append(f"{label}: expected FAIL, got PASS")
                print(f"NEG-FAIL  {label}: checker stayed green")
            elif needle and needle not in out:
                cases_failed.append(f"{label}: FAIL but missing needle {needle!r}")
                print(f"NEG-FAIL  {label}: wrong failure (missing {needle!r})")
                print(out[-500:])
            else:
                cases_passed.append(label)
                print(f"NEG-PASS  {label}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # N1 false-green ban context
    def m1(tmp: Path) -> None:
        _inject_crlf_append(tmp / "skill/references/intent-gate.md", "历史不再用五步编排。")

    expect_fail("N1-五步+不再", m1, "五步")

    # N2 Soft-Spec-input non-ban
    def m2(tmp: Path) -> None:
        _inject_crlf_append(tmp / "skill/references/multimodal.md", "Soft-Spec-input 可选卡。")

    expect_fail("N2-Soft-Spec非ban", m2, "Soft-Spec-input")

    # N4 七 mode + 零
    def m4(tmp: Path) -> None:
        _inject_crlf_append(tmp / "skill/references/intent-gate.md", "结果七 mode 零通过。")

    expect_fail("N4-七mode+零", m4, "七 mode")

    # N5 Priority2 weaken — remove 无独立模态 branch line
    def m5(tmp: Path) -> None:
        p = tmp / "skill/references/intent-gate.md"
        t = p.read_text(encoding="utf-8")
        t2 = t.replace("2. **compose-next 已运行且无独立模态**", "2. **compose-next 点名**")
        t2 = re.sub(r"无独立模态子任务 → 本 skill \*\*不展开\*\*", "无特殊分支", t2)
        data = t2.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8")
        _write_bytes(p, data)

    expect_fail("N5-Priority无模态分支", m5, "Priority2")

    # N5b Priority3 polarity
    def m5b(tmp: Path) -> None:
        pth = tmp / "skill/references/intent-gate.md"
        raw = pth.read_text(encoding="utf-8")
        mutated = raw.replace("；**不**展开三出口。", "。")
        data = mutated.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8")
        _write_bytes(pth, data)

    expect_fail("N5b-Priority3缺不展开三出口", m5b, "Priority3")

    # N7 checklist expected pass omitted
    def m7(tmp: Path) -> None:
        p = tmp / "skill/tests/checklist.md"
        t = p.read_text(encoding="utf-8")
        t2 = re.sub(r"# 期望 pass：\s*\d+\r?\n", "", t)
        data = t2.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8")
        _write_bytes(p, data)

    expect_fail("N7-期望pass缺失", m7, "期望 pass")

    # N9 multimodal extra pointer
    def m9(tmp: Path) -> None:
        _inject_crlf_append(tmp / "skill/references/multimodal.md", "细则见 references/extra.md")

    expect_fail("N9-multimodal-extra指针", m9, "extra.md")

    # N12 SKILL ban list drop Soft-Orient
    def m12(tmp: Path) -> None:
        p = tmp / "skill/SKILL.md"
        t = p.read_text(encoding="utf-8")
        t2 = t.replace("/ Soft-Orient /", "/ ")
        data = t2.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8")
        _write_bytes(p, data)

    expect_fail("N12-SKILL缺Soft-Orient", m12, "Soft-Orient")

    # N13 EOL flip intent-gate to LF
    def m13(tmp: Path) -> None:
        p = tmp / "skill/references/intent-gate.md"
        t = p.read_text(encoding="utf-8")
        data = t.replace("\r\n", "\n").encode("utf-8")
        _write_bytes(p, data)

    expect_fail("N13-intent-gate-LF", m13, "EOL")

    # N14 version mismatch
    def m14(tmp: Path) -> None:
        p = tmp / "README.md"
        t = p.read_text(encoding="utf-8")
        t2 = t.replace("**Version:** 2.0.3", "**Version:** 9.9.9")
        data = t2.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8")
        _write_bytes(p, data)

    expect_fail("N14-README版本", m14, "version")

    print()
    print(f"NEGATIVE cases_passed={len(cases_passed)} cases_failed={len(cases_failed)}")
    if cases_failed:
        print("NEGATIVE FAILURES:")
        for c in cases_failed:
            print(f"  - {c}")
        print("NEGATIVE SELF-TEST FAILED")
        return 1
    print("NEGATIVE SELF-TEST PASSED")
    return 0


if __name__ == "__main__":
    if NEGATIVE_FLAG in sys.argv:
        sys.exit(negative_self_test())
    sys.exit(main())
