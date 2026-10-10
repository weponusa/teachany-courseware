#!/usr/bin/env python3
"""tts-fill.py — 把语音不全的课件补到 8 段（TTS_PARTIAL 661 门）。

结构事实（2026-10-10 盘点）：500 门课件只有 s01-s03 三段（早期标准就是 3 段），
而页面 data-tts 标记了 15~19 个讲解段，其余无音频。本工具从 data-tts 段序列里
按教学优先级挑选未覆盖的段，用 Edge TTS 生成 mp3，并把播放列表 JSON 追加条目。

段选择优先级（未覆盖段中依序补足到 8 段）：
  objectives → lesson-focus → lesson-method → deep-understanding → summary
  → practice → pretest → conceptest-* → module-* → main-interaction → 其他

文件命名与现有一致：tts/sNN-<sectionId>.mp3（NN 续现有最大编号）。
播放列表 src 用 https://audio.teachany.cn/<cid>/tts/<file>（自建 CDN，
与 2026-10-09 品牌域切换后的现网一致）；新 mp3 需跑 build-audio-dist.py +
wrangler pages deploy 同步（本脚本不部署）。

用法：
  python3 scripts/tts-fill.py --ids bio-m-animal-behavior --apply
  python3 scripts/tts-fill.py --from-file /tmp/tts-partial.txt --workers 4 --apply
  python3 scripts/tts-fill.py --all --workers 6 --apply
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
CDN = "https://audio.teachany.cn"
TARGET = 8

sys.path.insert(0, str(ROOT / "scripts"))
from tts_engine import synthesize  # noqa: E402

PLAYLIST_RE = re.compile(
    r'(<script\b[^>]*data-teachany-audio-playlist[^>]*>)([\s\S]*?)(</script>)')
TTS_MARK_RE = re.compile(r'data-tts="([^"]+)"')

PRIORITY = ["objectives", "lesson-focus", "lesson-method", "deep-understanding",
            "summary", "practice", "pretest", "conceptest", "module", "main-interaction",
            "worked-example", "error-clinic", "memory-anchor", "problem-anchor",
            "matching-exercise", "hero"]


def prio(sid: str) -> int:
    for i, k in enumerate(PRIORITY):
        if sid.startswith(k) or sid == k:
            return i
    return len(PRIORITY) + 1


TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def section_text(html: str, sid: str, start: int = 0, full: bool = False) -> tuple[str, str]:
    """找 data-tts=sid 所在元素（兜底按 id 找 section），取标题与正文。

    start>0 时为「续读段」：跳过前 start 字后取 450 字（长 section 拆多段语音用）。"""
    m = re.search(r'<(section|div)[^>]*data-tts="%s"[^>]*>' % re.escape(sid), html)
    if not m:
        # 二级来源的小节没有 data-tts 标记，按 id 找
        m = re.search(r'<section\b[^>]*id="%s"[^>]*>' % re.escape(sid), html, re.I)
    if not m:
        return "", ""
    # 元素范围：到下一个同级 section 或页面尾部，粗取 3000 字符
    seg = html[m.end():m.end() + 3000]
    title_m = re.search(r"<h([1-3])[^>]*>([\s\S]*?)</h\1>", seg)
    title = WS.sub(" ", TAG.sub("", title_m.group(2))).strip() if title_m else sid
    body = WS.sub(" ", TAG.sub("", seg)).strip()
    # 一段语音约 1~2 分钟，450 字截断；start>0 时取续读段
    if full:
        return title[:40], body
    if start:
        return title[:40], body[start:start + 450]
    return title[:40], body[:450]


def process(cid: str, apply: bool, voice: str) -> tuple[str, str]:
    f = COMMUNITY / cid / "index.html"
    tts_dir = COMMUNITY / cid / "tts"
    if not f.is_file():
        return cid, "NO-FILE"
    h = f.read_text(encoding="utf-8", errors="ignore")
    pm = PLAYLIST_RE.search(h)
    if not pm:
        return cid, "NO-PLAYLIST"
    try:
        playlist = json.loads(pm.group(2))
    except Exception:
        return cid, "PLAYLIST-BAD"
    if len(playlist) >= TARGET:
        return cid, "SKIP(已≥8)"

    have_sections = {e.get("section") or e.get("sectionId") for e in playlist}
    marks = TTS_MARK_RE.findall(h)
    todo = [s for s in marks if s not in have_sections]
    todo.sort(key=lambda x: prio(x if isinstance(x, str) else x[0]))
    todo = todo[: TARGET - len(playlist)]

    # 二级来源：data-tts 段用尽仍不足 8 段时，降级用「任意有实质文本的小节」。
    # 254 门残余即此类——它们的 data-tts 标记少于 8 个或部分段文本过短。
    fallback = []
    if len(todo) < TARGET - len(playlist):
        seen_txt = set()
        for sm in re.finditer(r'<section\b([^>]*)>([\s\S]*?)</section>', h, re.I):
            attrs, body = sm.group(1), sm.group(2)
            idm = re.search(r'id="([^"]+)"', attrs)
            sid = idm.group(1) if idm else ""
            if not sid or sid in have_sections or sid in todo:
                continue
            if re.search(r'data-teachany-audio|audio-player|knowledge-graph|tutor-card', body):
                continue
            txt = WS.sub(" ", TAG.sub("", body)).strip()
            if len(txt) < 80:
                continue
            key = txt[:60]
            if key in seen_txt:
                continue
            seen_txt.add(key)
            fallback.append(sid)
        fallback.sort(key=lambda x: prio(x if isinstance(x, str) else x[0]))
    todo = (todo + fallback)[: TARGET - len(playlist)]

    # 三级来源：已覆盖但全文超 450 字的长 section，续读后半段（拆段朗读）。
    # todo 条目支持 (sid, start) 元组，生成循环按 offset 取续读文本。
    if len(todo) < TARGET - len(playlist):
        for e in playlist:
            sec = e.get("section") or e.get("sectionId")
            if not sec:
                continue
            _, full = section_text(h, sec, 0, full=True)
            if len(full) > 500 and len(todo) < TARGET - len(playlist):
                todo.append((sec, 450))

    if not todo:
        return cid, "NO-SEGMENT"

    # 现有最大编号
    nums = [int(m.group(1)) for e in playlist
            if (m := re.match(r"s(\d+)$", str(e.get("id", ""))))]
    n = max(nums) if nums else len(playlist)

    made = []
    covered0 = {e.get("section") or e.get("sectionId") for e in playlist}
    if not tts_dir.exists():       # macOS 偶发 exist_ok=True 仍报 EEXIST，显式判断更稳
        tts_dir.mkdir(parents=True)

    def gen(sid: str, start: int = 0):
        """生成一段；文本过短或 TTS 失败返回 None（不中断整门，换下一段补足）。"""
        nonlocal n
        title, text = section_text(h, sid, start)
        if len(text) < 40:
            return None
        n += 1
        fname = f"s{n:02d}-{sid[:24].replace('_', '-')}.mp3"
        out = tts_dir / fname
        if apply and (not out.exists() or out.stat().st_size < 200):
            # ⚠ 0 字节/过小文件必须删除重生成——Edge TTS 并发下会静默写出 0 字节
            # 文件（曾一次产生 630 个），若仅以「文件存在」跳过，坏文件会永远留存。
            ok, engine = synthesize(text=text, voice=voice, output=str(out))
            if not ok or not out.exists() or out.stat().st_size < 200:
                if out.exists() and out.stat().st_size < 200:
                    out.unlink()
                return None
        return {"id": f"s{n:02d}", "src": f"{CDN}/{cid}/tts/{fname}",
                "title": title or sid, "section": sid}

    def need() -> int:
        return TARGET - len(playlist) - len(made)

    # 一级：data-tts 未覆盖段
    for item in todo:
        sid, start = item if isinstance(item, tuple) else (item, 0)
        e = gen(sid, start)
        if e:
            made.append(e)
        if need() <= 0:
            break

    # 二级：一级候选提取失败（todo 数量够但质量不行）时，逐门补任意 ≥80 字小节
    if 0 < need():
        covered_now = covered0 | {e["section"] for e in made}
        secs = []
        for sm in re.finditer(r"<section\b([^>]*)>([\s\S]*?)</section>", h, re.I):
            idm = re.search(r'id="([^"]+)"', sm.group(1))
            if not idm or idm.group(1) in covered_now:
                continue
            body = sm.group(2)
            if re.search(r"knowledge-graph|tutor-card|audio-player|teachany-kg", body):
                continue
            txt = WS.sub(" ", TAG.sub("", body)).strip()
            if len(txt) >= 80:
                secs.append((prio(idm.group(1)), idm.group(1)))
        secs.sort()
        for _, sid in secs:
            e = gen(sid)
            if e:
                made.append(e)
            if need() <= 0:
                break

    # 三级：仍不足时，长 section 续读后半段
    if 0 < need():
        for e in playlist + made:
            sec = e.get("section")
            if not sec:
                continue
            _, full = section_text(h, sec, 0, full=True)
            if len(full) > 500 and need() > 0:
                e2 = gen(sec, 450)
                if e2:
                    made.append(e2)
            if need() <= 0:
                break

    if not made:
        return cid, "NO-TEXT"
    if apply:
        new_list = playlist + made
        new_block = (pm.group(1) + "\n" + json.dumps(new_list, ensure_ascii=False, indent=2)
                     + "\n  " + pm.group(3))
        h = h[:pm.start()] + new_block + h[pm.end():]
        f.write_text(h, encoding="utf-8")
    return cid, f"OK(+{len(made)}段)"


def load_ids(a):
    if a.ids:
        return [x.strip() for x in a.ids.split(",") if x.strip()]
    if a.from_file:
        return [l.strip() for l in Path(a.from_file).read_text().splitlines()
                if l.strip() and not l.startswith("#")]
    rows = json.load(open("/tmp/qa-final.json", encoding="utf-8"))
    return [r["id"] for r in rows if 0 < r["tts_mp3"] < TARGET]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids")
    ap.add_argument("--from-file")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--voice", default="zh-CN-XiaoxiaoNeural")
    a = ap.parse_args()
    if not any([a.ids, a.from_file, a.all]):
        ap.error("需指定 --ids / --from-file / --all 之一")

    ids = load_ids(a)
    print(f"目标 {len(ids)} 门 apply={a.apply} workers={a.workers}", flush=True)
    results = []
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(process, cid, a.apply, a.voice): cid for cid in ids}
        done = 0
        for fu in cf.as_completed(futs):
            r = fu.result()
            results.append(r)
            done += 1
            if done % 25 == 0 or done == len(ids):
                print(f"  进度 {done}/{len(ids)}", flush=True)

    ok = [r for r in results if r[1].startswith("OK")]
    skip = [r for r in results if r[1].startswith(("SKIP", "NO-SEGMENT"))]
    bad = [r for r in results if not r[1].startswith(("OK", "SKIP", "NO-SEGMENT"))]
    print(f"\n完成：OK {len(ok)}  跳过 {len(skip)}  失败 {len(bad)}")
    for cid, s in bad[:15]:
        print(f"  ✗ {cid}: {s}")


if __name__ == "__main__":
    main()
