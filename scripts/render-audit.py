#!/usr/bin/env python3
"""render-audit.py — 全库渲染级验收关卡（KG 图谱 + 按钮交互）。

背景
----
字符串级质检看不见「渲染出来空不空、按钮点下去活不活」——死按钮 4325 个、
图谱断链 6 门都是用户点爆后才发现。本工具把两类「必须真实打开浏览器才能看见」
的验收固化下来，建议在每次大批量生成/迁移后运行。

用法
----
  # 先在仓库根起本地服务：python3 -m http.server 8899
  python3 scripts/render-audit.py --kg        # 图谱渲染验收
  python3 scripts/render-audit.py --buttons   # 按钮运行时验收 + 抽样实点
  python3 scripts/render-audit.py --all       # 两者
  可选项：--workers 6（默认）--port 8899 --out /tmp/render-audit.json

判定标准（与 2026-10-10 两轮全库验收一致）：
  KG：data-teachany-kg 容器内 SVG 元素 ≥10 且无「加载失败」文案；
  按钮：运行时 typeof window[fn] === 'function'（动态挂载算数），
        每门均匀抽样 4 个按钮实点，pageerror 非空即记。
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1] / "community"
EXE = str(Path.home() / "Library/Caches/ms-playwright/chromium-1247/"
          "chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/"
          "Google Chrome for Testing")

KG_JUDGE = """() => {
    const box = document.querySelector('[data-teachany-kg]');
    if (!box) return {ok:false, why:'容器不存在'};
    const svg = box.querySelector('svg');
    const errTxt = box.textContent.includes('加载失败') || box.textContent.includes('manifest-not-found');
    const n = svg ? svg.querySelectorAll('*').length : 0;
    return {ok: !!svg && n >= 10 && !errTxt, svgN: n,
            why: !svg ? '无SVG' : (n < 10 ? '节点过少:'+n : (errTxt ? '加载失败' : 'OK'))};
}"""

BTN_AUDIT = """() => {
    const dead = new Set();
    let alive = 0;
    for (const el of document.querySelectorAll('[onclick]')) {
        const m = el.getAttribute('onclick').match(/^([A-Za-z_$][\\w$]*)\\s*\\(/);
        if (!m) continue;
        if (typeof window[m[1]] !== 'function') dead.add(m[1]); else alive++;
    }
    return {dead: [...dead], alive};
}"""

BTN_CLICK = """(idxs) => {
    const out = [];
    const els = [...document.querySelectorAll('[onclick]')];
    for (const i of idxs) {
        const el = els[i];
        if (!el) continue;
        const fn = el.getAttribute('onclick').match(/^([A-Za-z_$][\\w$]*)/);
        try { el.click(); out.push((fn ? fn[1] : '?') + ':OK'); }
        catch (e) { out.push((fn ? fn[1] : '?') + ':ERR ' + e.message.slice(0, 60)); }
    }
    return out;
}"""


def collect_targets(kind: str) -> list[str]:
    out = []
    for f in sorted(ROOT.glob("*/index.html")):
        h = f.read_text(encoding="utf-8", errors="ignore")
        if kind == "kg" and re.search(r'data-teachany-kg="[^"]+"', h):
            out.append(f.parent.name)
        elif kind == "buttons" and "onclick=" in h:
            out.append(f.parent.name)
    return out


def run_batch(kind: str, batch: list[str], base: str):
    results = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=EXE)
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        for cid in batch:
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            try:
                pg.goto(f"{base}/{cid}/", wait_until="domcontentloaded", timeout=30000)
                pg.wait_for_timeout(2000)
                head = pg.content()[:5000]
                if 'location.replace' in head or 'http-equiv="refresh"' in head:
                    pg.wait_for_timeout(2500)
                if kind == "kg":
                    r = pg.evaluate(KG_JUDGE)
                    r["id"] = cid
                    results.append(r)
                else:
                    a = pg.evaluate(BTN_AUDIT)
                    n = pg.evaluate("() => document.querySelectorAll('[onclick]').length")
                    rec = {"id": cid, "dead": a["dead"], "alive": a["alive"]}
                    if n > 0:
                        idxs = sorted({0, n // 3, (2 * n) // 3, n - 1})[:4]
                        before = len(errs)
                        rec["clicks"] = pg.evaluate(BTN_CLICK, idxs)
                        rec["clickErrs"] = errs[before:]
                    else:
                        rec["clicks"] = []
                        rec["clickErrs"] = []
                    results.append(rec)
            except Exception as e:
                results.append({"id": cid, "ok": False, "open_err": str(e)[:80]})
        b.close()
    return results


def run(kind: str, base: str, workers: int) -> list[dict]:
    targets = collect_targets(kind)
    print(f"[{kind}] 目标 {len(targets)} 门", flush=True)
    B = 20
    batches = [targets[i:i + B] for i in range(0, len(targets), B)]
    all_res = []
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(run_batch, kind, b, base): i for i, b in enumerate(batches)}
        for fu in cf.as_completed(futs):
            all_res.extend(fu.result())
            print(f"  批次 {futs[fu] + 1}/{len(batches)}", flush=True)
    return all_res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kg", action="store_true")
    ap.add_argument("--buttons", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--port", type=int, default=8899)
    ap.add_argument("--out", default="/tmp/render-audit.json")
    a = ap.parse_args()
    if a.all:
        a.kg = a.buttons = True
    if not a.kg and not a.buttons:
        ap.error("需指定 --kg / --buttons / --all")
    if not Path(EXE).exists():
        print(f"警告：chromium 不在 {EXE}，playwright 会用默认浏览器", file=sys.stderr)

    base = f"http://127.0.0.1:{a.port}/community"
    report = {}
    if a.kg:
        res = run("kg", base, a.workers)
        bad = [r for r in res if not r.get("ok")]
        report["kg"] = {"total": len(res), "passed": len(res) - len(bad), "bad": bad}
        print(f"[kg] 通过 {len(res) - len(bad)}/{len(res)}，未过 {len(bad)}")
        for r in bad[:10]:
            print(f"  ✗ {r['id']}: {r.get('why', r.get('open_err', ''))}")
    if a.buttons:
        res = run("buttons", base, a.workers)
        dead = [r for r in res if r.get("dead")]
        click = [r for r in res if r.get("clickErrs")]
        report["buttons"] = {"total": len(res), "dead_courses": dead, "click_errors": click}
        print(f"[buttons] 运行时死按钮课件 {len(dead)} 门，实点报错课件 {len(click)} 门")
        for r in dead[:10]:
            print(f"  ✗ {r['id']}: {r['dead']}")

    Path(a.out).write_text(json.dumps(report, ensure_ascii=False, indent=1),
                           encoding="utf-8")
    print(f"→ {a.out}")


if __name__ == "__main__":
    main()
