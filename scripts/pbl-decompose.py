#!/usr/bin/env python3
"""
TeachAny PBL 拆解 CLI — 供 Cursor Skill / 自动化调用

输入 PBL 任务基本信息 → 调用线上 PBL 引擎拆解 → 输出长图 PNG + 可继续编辑的 TeachAny 链接

依赖（首次使用）:
    pip install playwright
    playwright install chromium

示例:
    python3 scripts/pbl-decompose.py --goal "设计一款水火箭并完成安全发射"
    python3 scripts/pbl-decompose.py --goal "家庭购车对比" --grade senior --deliverable decision-table -o ./out
    python3 scripts/pbl-decompose.py --goal "研学路线规划" --grade junior --subject geography --duration "4周"
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlencode, urlparse

DEFAULT_BASE = "https://www.teachany.cn/pbl"
HANDOFF_API = "https://www.teachany.cn/api/pbl/handoff"
TIMEOUT_MS = 360_000


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fa5]+", "-", (text or "pbl").strip()[:40]).strip("-")
    return s or "pbl-report"


def site_origin(base_url: str) -> str:
    p = urlparse(base_url or DEFAULT_BASE)
    return f"{p.scheme}://{p.netloc}"


def build_pbl_url(args: argparse.Namespace) -> str:
    params = {"auto": "1"}
    goal = (args.goal or args.task or "").strip()
    if not goal:
        raise SystemExit("缺少 --goal / --task")
    params["goal"] = goal
    if args.grade and args.grade != "any":
        params["grade"] = args.grade
    if args.subject and args.subject != "cross":
        params["subject"] = args.subject
    if args.deliverable and args.deliverable != "report":
        params["deliverable"] = args.deliverable
    if args.deliverable_custom:
        params["deliverableCustom"] = args.deliverable_custom
    if args.audience:
        params["audience"] = args.audience
    if args.duration:
        params["duration"] = args.duration
    if args.constraints:
        params["constraints"] = args.constraints
    base = (args.base_url or DEFAULT_BASE).split("?")[0].rstrip("/")
    return f"{base}?{urlencode(params)}"


def build_edit_url(args: argparse.Namespace) -> str:
    """仅作最后兜底：不含 handoff 时用户需重新拆解。"""
    params = {}
    goal = (args.goal or args.task or "").strip()
    if goal:
        params["goal"] = goal
    if args.grade and args.grade != "any":
        params["grade"] = args.grade
    if args.subject and args.subject != "cross":
        params["subject"] = args.subject
    if args.deliverable and args.deliverable != "report":
        params["deliverable"] = args.deliverable
    if args.deliverable_custom:
        params["deliverableCustom"] = args.deliverable_custom
    if args.audience:
        params["audience"] = args.audience
    if args.duration:
        params["duration"] = args.duration
    if args.constraints:
        params["constraints"] = args.constraints
    base = (args.base_url or DEFAULT_BASE).split("?")[0].rstrip("/")
    return f"{base}?{urlencode(params)}" if params else base


def post_handoff(goal: str, result: dict, spec: dict | None, api_url: str = HANDOFF_API) -> dict:
    body = json.dumps({"goal": goal, "result": result, "spec": spec}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        api_url,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def handoff_edit_url(handoff_id: str, base: str = DEFAULT_BASE) -> str:
    u = f"{base.split('?')[0].rstrip('/')}?handoff={handoff_id}"
    return u


async def run_decompose(args: argparse.Namespace) -> dict:
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("⛔ 未安装 playwright。请运行：", file=sys.stderr)
        print("   pip install playwright && playwright install chromium", file=sys.stderr)
        raise SystemExit(2)

    analyze_url = build_pbl_url(args)
    origin = site_origin(args.base_url or DEFAULT_BASE)
    handoff_api = f"{origin}/api/pbl/handoff"
    pbl_base = (args.base_url or DEFAULT_BASE).split("?")[0].rstrip("/")
    out_dir = Path(args.output or ".").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    png_path = out_dir / f"{slugify(args.goal)}.png"
    meta_path = out_dir / f"{slugify(args.goal)}.json"

    print(f"🔗 拆解 URL: {analyze_url}")
    print("⏳ 正在拆解（约 1–4 分钟，取决于 LLM 响应）…")

    handoff_error = None
    handoff_source = None
    edit_url = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 1200})
        page.set_default_timeout(TIMEOUT_MS)

        await page.goto(analyze_url, wait_until="domcontentloaded", timeout=120_000)

        await page.wait_for_function(
            """() => window.__pblLastAnalysisDone?.ok === true""",
            timeout=TIMEOUT_MS,
        )

        await page.wait_for_function(
            """() => {
              const r = window.TeachAnyPBLAutomation?.getResult?.();
              if (!r?.graphData?.nodes?.length) return false;
              const st = document.getElementById('pblStatus');
              if (st && st.style.display !== 'none') return false;
              const svg = document.querySelector('#pbl-graph-container svg');
              return !!svg;
            }""",
            timeout=120_000,
        )
        await page.wait_for_timeout(1500)

        payload = await page.evaluate(
            """() => {
              const getSnap = window.TeachAnyPBLAutomation?.getSerializableResult;
              const result = getSnap ? getSnap() : null;
              const spec = typeof getPBLProjectSpec === 'function' ? getPBLProjectSpec() : null;
              return { result, spec };
            }"""
        )

        result_summary = await page.evaluate(
            """() => {
              const r = window.TeachAnyPBLAutomation.getResult();
              const nodes = r.graphData?.nodes || [];
              return {
                goal: r.goal || '',
                matched: (r.matched || []).length,
                external: (r.external || []).length,
                nodeCount: nodes.length,
                systems: r.systems || [],
                hasBlueprint: !!(r.projectBlueprint && (r.projectBlueprint.schemes || []).length),
                hasTechRoute: !!(r.techRoute || r.pathPlan?.phases?.length),
              };
            }"""
        )

        snap = payload.get("result") or {}
        spec = payload.get("spec")
        goal_text = (snap.get("goal") or result_summary.get("goal") or args.goal or "").strip()

        if snap.get("graphData", {}).get("nodes"):
            try:
                h = post_handoff(goal_text, snap, spec, handoff_api)
                edit_url = handoff_edit_url(h["id"], pbl_base)
                handoff_source = "python"
            except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError) as e:
                handoff_error = str(e)
                try:
                    edit_url = await page.evaluate(
                        """async (base) => {
                          if (window.TeachAnyPBLAutomation?.createHandoff) {
                            return await window.TeachAnyPBLAutomation.createHandoff(base);
                          }
                          throw new Error('createHandoff unavailable');
                        }""",
                        pbl_base,
                    )
                    handoff_source = "browser"
                except Exception as e2:
                    handoff_error = f"{handoff_error}; browser: {e2}"

        if not edit_url or "handoff=" not in edit_url:
            run_id = await page.evaluate("() => window.TeachAnyPBLAutomation?.getRunId?.() || null")
            if run_id:
                edit_url = f"{pbl_base}?pbl={run_id}"
                handoff_source = handoff_source or "local-pbl-id"
            else:
                edit_url = build_edit_url(args)
                handoff_source = "goal-fallback"
                print("⚠️  handoff 失败，编辑链接仅为任务参数（打开后需重新拆解）", file=sys.stderr)
                if handoff_error:
                    print(f"   原因: {handoff_error}", file=sys.stderr)

        print("🖼️  正在生成长图…")
        png_bytes = await page.evaluate(
            """async () => {
              const { blob } = await window.TeachAnyPBLAutomation.exportImageBlob();
              const buf = await blob.arrayBuffer();
              return Array.from(new Uint8Array(buf));
            }"""
        )
        await browser.close()

    png_path.write_bytes(bytes(png_bytes))
    meta = {
        "goal": args.goal,
        "grade": args.grade,
        "subject": args.subject,
        "deliverable": args.deliverable,
        "audience": args.audience,
        "duration": args.duration,
        "constraints": args.constraints,
        "image": str(png_path),
        "edit_url": edit_url,
        "edit_url_fallback": build_edit_url(args),
        "handoff_source": handoff_source,
        "handoff_error": handoff_error,
        "summary": result_summary,
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return meta


def main() -> None:
    parser = argparse.ArgumentParser(description="TeachAny PBL 拆解 → 长图 + 编辑链接")
    parser.add_argument("--goal", "--task", dest="goal", required=True, help="PBL 项目任务描述（必填）")
    parser.add_argument("--grade", default="any", choices=["any", "primary", "junior", "senior", "university", "adult"])
    parser.add_argument("--subject", default="cross")
    parser.add_argument("--deliverable", default="report")
    parser.add_argument("--deliverable-custom", dest="deliverable_custom", default="")
    parser.add_argument("--audience", default="")
    parser.add_argument("--duration", default="")
    parser.add_argument("--constraints", default="")
    parser.add_argument("-o", "--output", default=".", help="输出目录")
    parser.add_argument("--base-url", default=DEFAULT_BASE, help="PBL 页面地址（默认线上 teachany.cn/pbl）")
    parser.add_argument("--json-only", action="store_true", help="仅打印结果 JSON 到 stdout")
    args = parser.parse_args()

    import asyncio

    meta = asyncio.run(run_decompose(args))

    if args.json_only:
        print(json.dumps(meta, ensure_ascii=False, indent=2))
    else:
        print()
        print("✅ PBL 拆解完成")
        print(f"   长图: {meta['image']}")
        s = meta["summary"]
        print(f"   节点: {s.get('nodeCount', 0)} 个（蓝图: {'有' if s.get('hasBlueprint') else '无'}）")
        print(f"   交接: {meta.get('handoff_source', '?')}")
        print(f"   继续编辑: {meta['edit_url']}")


if __name__ == "__main__":
    main()
