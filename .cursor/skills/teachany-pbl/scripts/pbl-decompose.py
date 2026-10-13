#!/usr/bin/env python3
"""
TeachAny PBL 拆解 CLI — 供 Cursor / WorkBuddy Skill 调用

输入 PBL 任务 → 调用 www.teachany.cn PBL 引擎 → PNG 长图 + 编辑链接

依赖:
    pip install playwright
    playwright install chromium
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlencode, urlparse

DEFAULT_BASE = "https://www.teachany.cn/pbl"
TIMEOUT_MS = 360_000


def _configure_stdio() -> None:
    """Windows GBK 终端下避免 emoji/中文 print 触发 UnicodeEncodeError。"""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def _log(msg: str, *, err: bool = False) -> None:
    print(msg, file=sys.stderr if err else sys.stdout)


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fa5]+", "-", (text or "pbl").strip()[:40]).strip("-")
    return s or "pbl-report"


def site_origin(base_url: str) -> str:
    p = urlparse(base_url or DEFAULT_BASE)
    return f"{p.scheme}://{p.netloc}"


def _goal_query_params(args: argparse.Namespace, *, include_auto: bool = False) -> dict[str, str]:
    params: dict[str, str] = {}
    if include_auto:
        params["auto"] = "1"
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
    return params


def build_pbl_url(args: argparse.Namespace) -> str:
    base = (args.base_url or DEFAULT_BASE).split("?")[0].rstrip("/")
    return f"{base}?{urlencode(_goal_query_params(args, include_auto=True))}"


def build_edit_url(args: argparse.Namespace) -> str:
    """仅作最后兜底：不含 handoff 时用户需重新拆解。"""
    params = _goal_query_params(args)
    base = (args.base_url or DEFAULT_BASE).split("?")[0].rstrip("/")
    return f"{base}?{urlencode(params)}" if params.get("goal") else base


def post_handoff(goal: str, result: dict, spec: dict | None, api_url: str) -> dict:
    body = json.dumps({"goal": goal, "result": result, "spec": spec}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        api_url,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def handoff_edit_url(handoff_id: str, base: str) -> str:
    return f"{base.split('?')[0].rstrip('/')}?handoff={handoff_id}"


async def _wait_analysis_done(page) -> None:
    deadline = asyncio.get_event_loop().time() + TIMEOUT_MS / 1000
    while asyncio.get_event_loop().time() < deadline:
        state = await page.evaluate(
            """() => {
              const d = window.__pblLastAnalysisDone;
              const r = window.TeachAnyPBLAutomation?.getResult?.();
              return {
                doneOk: !!(d && d.ok),
                doneErr: d && d.ok === false ? (d.error || 'PBL 拆解失败') : null,
                nodes: r?.graphData?.nodes?.length || 0,
                blueprint: (r?.projectBlueprint?.schemes || []).length,
              };
            }"""
        )
        if state.get("doneErr"):
            raise RuntimeError(state["doneErr"])
        if state.get("doneOk"):
            return
        await asyncio.sleep(2)
    raise TimeoutError(f"PBL 拆解超时（{TIMEOUT_MS // 1000}s 无响应）")


async def _resolve_edit_url(page, args, pbl_base, handoff_api, snap, spec, goal_text) -> tuple[str | None, str | None, str | None]:
    """返回 (edit_url, handoff_source, handoff_error)。优先浏览器同源 handoff。"""
    has_result = bool(snap.get("graphData", {}).get("nodes")) or bool(
        (snap.get("projectBlueprint") or {}).get("schemes")
    )
    if not has_result:
        return None, None, "无拆解结果，无法创建 handoff"

    handoff_error = None
    edit_url = None
    handoff_source = None

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
    except Exception as e:
        handoff_error = f"browser: {e}"
        try:
            h = post_handoff(goal_text, snap, spec, handoff_api)
            edit_url = handoff_edit_url(h["id"], pbl_base)
            handoff_source = "python"
            handoff_error = None
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError) as e2:
            handoff_error = f"{handoff_error}; python: {e2}"

    if not edit_url or "handoff=" not in edit_url:
        run_id = await page.evaluate("() => window.TeachAnyPBLAutomation?.getRunId?.() || null")
        if run_id:
            return f"{pbl_base}?pbl={run_id}", handoff_source or "local-pbl-id", handoff_error
        return build_edit_url(args), "goal-fallback", handoff_error

    return edit_url, handoff_source, handoff_error


async def run_decompose(args: argparse.Namespace) -> dict:
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        _log("[ERR] 未安装 playwright。请运行：", err=True)
        _log("      pip install playwright && playwright install chromium", err=True)
        raise SystemExit(2)

    analyze_url = build_pbl_url(args)
    origin = site_origin(args.base_url or DEFAULT_BASE)
    handoff_api = f"{origin}/api/pbl/handoff"
    pbl_base = (args.base_url or DEFAULT_BASE).split("?")[0].rstrip("/")
    out_dir = Path(args.output or ".").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(args.goal)
    png_path = out_dir / f"{slug}.png"
    meta_path = out_dir / f"{slug}.json"

    _log(f"[INFO] 拆解 URL: {analyze_url}")
    _log("[INFO] 正在拆解（通常 3–8 分钟，取决于 teachany.cn LLM 响应）…")

    handoff_error = None
    handoff_source = None
    edit_url = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 1200})
        page.set_default_timeout(TIMEOUT_MS)

        await page.goto(analyze_url, wait_until="domcontentloaded", timeout=120_000)
        await _wait_analysis_done(page)

        await page.wait_for_function(
            """() => {
              const r = window.TeachAnyPBLAutomation?.getResult?.();
              const hasGraph = (r?.graphData?.nodes?.length || 0) > 0;
              const hasBlueprint = (r?.projectBlueprint?.schemes || []).length > 0;
              if (!hasGraph && !hasBlueprint) return false;
              const st = document.getElementById('pblStatus');
              if (st && st.style.display !== 'none') return false;
              if (!hasGraph) return true;
              return !!document.querySelector('#pbl-graph-container svg');
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

        edit_url, handoff_source, handoff_error = await _resolve_edit_url(
            page, args, pbl_base, handoff_api, snap, spec, goal_text
        )
        if handoff_source == "goal-fallback":
            _log("[WARN] handoff 失败，编辑链接仅为任务参数（打开后需重新拆解）", err=True)
            if handoff_error:
                _log(f"       原因: {handoff_error}", err=True)

        _log("[INFO] 正在生成长图…")
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
        "deliverable_custom": args.deliverable_custom,
        "audience": args.audience,
        "duration": args.duration,
        "constraints": args.constraints,
        "image": png_path.as_posix(),
        "meta": meta_path.as_posix(),
        "edit_url": edit_url,
        "edit_url_fallback": build_edit_url(args),
        "handoff_source": handoff_source,
        "handoff_error": handoff_error,
        "summary": result_summary,
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return meta


def main() -> None:
    _configure_stdio()
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
    parser.add_argument("--base-url", default=DEFAULT_BASE, help="PBL 页面地址（默认 https://www.teachany.cn/pbl）")
    parser.add_argument("--json-only", action="store_true", help="仅打印结果 JSON 到 stdout")
    args = parser.parse_args()

    meta = asyncio.run(run_decompose(args))

    if args.json_only:
        print(json.dumps(meta, ensure_ascii=False, indent=2))
    else:
        print()
        _log("[OK] PBL 拆解完成")
        _log(f"     长图: {meta['image']}")
        s = meta["summary"]
        _log(f"     元数据: {meta['meta']}")
        _log(f"     节点: {s.get('nodeCount', 0)} 个（蓝图: {'有' if s.get('hasBlueprint') else '无'}）")
        _log(f"     交接: {meta.get('handoff_source', '?')}")
        _log(f"     继续编辑: {meta['edit_url']}")


if __name__ == "__main__":
    main()
