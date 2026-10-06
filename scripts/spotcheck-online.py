#!/usr/bin/env python3
"""spotcheck-online.py — 线上课件抽查（随机抽样 + 多维体检）

检查维度：
  1. 部署同步：线上 HTML 与本地是否一致（防止改了没上线）
  2. 可访问：HTTP 200、页面体积合理
  3. 结构健康：section/div 配平、有无空模块与占位符
  4. 互动装配：SVG 示意图 / iframe 仿真 / Canvas / 测验题
  5. 资源可用：页面引用的图片、脚本是否 404

用法: python3 spotcheck-online.py [数量] [--seed N] [--cid a,b,c]
"""
import concurrent.futures as cf
import random
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
BASE = "https://www.teachany.cn/community/{cid}/"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

PLACEHOLDER = [r"待补充", r"待完善", r"敬请期待", r"TODO", r"[xX]{3,}", r"示例文本"]


def get(url, timeout=30, bust=False):
    """bust=True 时加时间戳参数 + no-cache 头，穿透 CDN 缓存取源站最新版本。

    不加会拿到上一版页面（实测刚推送后 8 分钟仍返回旧内容），
    导致把已修复的课件误判为「未配平」。
    """
    if bust:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}_t={int(time.time() * 1000)}"
    headers = {"User-Agent": UA}
    if bust:
        headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        headers["Pragma"] = "no-cache"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return 0, b""


def text_of(raw):
    return raw.decode("utf-8", errors="replace")


def pick(n, seed=None):
    cids = sorted(p.name for p in COMMUNITY.iterdir() if (p / "index.html").exists())
    # 按学科前缀分层抽样，保证覆盖度
    by_sub = {}
    for c in cids:
        by_sub.setdefault(c.split("-")[0], []).append(c)
    rnd = random.Random(seed)
    subs = sorted(by_sub, key=lambda s: -len(by_sub[s]))
    out = []
    # 主学科（课件数 >= 10）每个至少抽 1 个
    main = [s for s in subs if len(by_sub[s]) >= 10]
    for s in main:
        out.append(rnd.choice(by_sub[s]))
    # 剩余名额随机补齐
    rest = [c for c in cids if c not in out]
    out += rnd.sample(rest, max(0, min(n - len(out), len(rest))))
    return out[:n]


def check(cid):
    """返回 (cid, issues[list], stats[dict])"""
    issues, stats = [], {}
    local_p = COMMUNITY / cid / "index.html"
    local = local_p.read_text(encoding="utf-8", errors="replace") if local_p.exists() else ""

    status, raw = get(BASE.format(cid=cid), bust=True)
    stats["http"] = status
    if status != 200:
        issues.append(f"不可访问 HTTP {status}")
        return cid, issues, stats
    on = text_of(raw)
    stats["size"] = len(raw)

    # 1. 部署同步：去掉空白后比对（线上可能有 CDN 注入，用关键片段判定）
    key_local = re.sub(r"\s+", "", local)
    key_online = re.sub(r"\s+", "", on)
    stats["synced"] = key_local[:2000] == key_online[:2000]
    if not stats["synced"]:
        # 找出差异比例，区分"未部署"和"CDN 轻微改写"
        m = min(len(key_local), len(key_online))
        if m > 0:
            same = sum(1 for a, b in zip(key_local[:m], key_online[:m]) if a == b)
            stats["sync_ratio"] = round(same / m, 3)
            if stats["sync_ratio"] < 0.98:
                issues.append(f"线上与本地不一致（相似度 {stats['sync_ratio']}）")

    # 2. 结构配平
    for tag in ("section", "div", "figure"):
        o = len(re.findall(rf"<{tag}\b", on))
        c = len(re.findall(rf"</{tag}>", on))
        stats[f"{tag}_pair"] = f"{o}/{c}"
        if o != c:
            issues.append(f"<{tag}> 未配平 {o}/{c}")

    # 3. 空模块 / 占位符
    for pat in PLACEHOLDER:
        if re.search(pat, on):
            issues.append(f"占位内容「{pat}」")

    # 4. 互动装配
    svg_n = len(re.findall(r"<svg\b", on))
    iframe_n = len(re.findall(r"<iframe\b", on))
    canvas_n = len(re.findall(r"<canvas\b", on))
    quiz_n = len(re.findall(r"data-correct|quiz-option|check-answer", on))
    stats["svg"], stats["iframe"], stats["canvas"], stats["quiz"] = svg_n, iframe_n, canvas_n, quiz_n
    if svg_n == 0:
        issues.append("无 SVG 示意图")
    if quiz_n == 0:
        issues.append("无互动测验")
    if svg_n + iframe_n + canvas_n == 0:
        issues.append("零可视化/互动模块")

    # 5. 资源可用性（图片、脚本），最多查 8 个
    res = re.findall(r'(?:src|href)="((?:\./|assets/)[^"]+\.(?:png|webp|jpg|svg|js|css))"', on)
    bad_res = []
    for r in list(dict.fromkeys(res))[:8]:
        u = BASE.format(cid=cid) + r.lstrip("./")
        st, _ = get(u, timeout=20)
        if st != 200:
            bad_res.append(f"{r}({st})")
    if bad_res:
        issues.append("资源 404: " + ", ".join(bad_res[:3]))

    return cid, issues, stats


def main():
    def opt(name, default=None, cast=str):
        """支持 --name=value 与 --name value 两种写法"""
        for i, a in enumerate(sys.argv[1:], 1):
            if a == f"--{name}" and i + 1 < len(sys.argv):
                return cast(sys.argv[i + 1])
            if a.startswith(f"--{name}="):
                return cast(a.split("=", 1)[1])
        return default

    args = [a for a in sys.argv[1:] if not a.startswith("--") and a.isdigit()]
    seed = opt("seed", 42, int)
    cidarg = opt("cid")

    if cidarg:
        cids = [c.strip() for c in cidarg.split(",")]
    else:
        n = int(args[0]) if args else 12
        cids = pick(n, seed)

    print(f"抽查 {len(cids)} 个课件（seed={seed}）\n")
    rows = []
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for cid, issues, stats in ex.map(check, cids):
            rows.append((cid, issues, stats))

    ok = [r for r in rows if not r[1]]
    bad = [r for r in rows if r[1]]
    for cid, issues, stats in rows:
        flag = "✅" if not issues else "❌"
        s = stats
        print(f"{flag} {cid}")
        print(f"   HTTP {s.get('http')} · {s.get('size', 0)//1024}KB · "
              f"svg{s.get('svg','-')} iframe{s.get('iframe','-')} "
              f"canvas{s.get('canvas','-')} quiz{s.get('quiz','-')}")
        if s.get("sync_ratio") is not None and s["sync_ratio"] < 1:
            print(f"   同步相似度 {s['sync_ratio']}")
        for i in issues:
            print(f"   ⚠ {i}")
    print(f"\n{'='*50}\n通过 {len(ok)}/{len(rows)}   问题 {len(bad)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
