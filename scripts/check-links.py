#!/usr/bin/env python3
"""check-links.py — 批量检查课件中的外部链接可达性（并发 HEAD/GET 探测）
用法: python3 check-links.py [cid...]  不传则查全库
      python3 check-links.py --fix      尝试用已知映射修复失效链接
输出: 失效链接清单（URL / 所在课件 / HTTP 状态）
"""
import concurrent.futures as cf
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# 只检查这些外部资源（排除 SVG 命名空间等伪 URL）
SKIP_HOST = {"www.w3.org", "schemas.microsoft.com", "purl.org", "ns.adobe.com"}
SKIP_EXT = (".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2", ".mp3", ".mp4")

# 误报白名单：URL 中包含这些片段即跳过（非供用户点击的"链接"）
# - API endpoint：裸路径本就返回 404，属正常
# - {xxx} 模板变量：运行时才替换，静态探测必然失败
# - localhost：本地预览服务提示，仅 file:// 下出现
SKIP_SUBSTR = (
    "/v1/chat/completions", "/v1/", "api.openai.com", "agentai.cn",
    "localhost", "127.0.0.1", "0.0.0.0",
    "{x}", "{y}", "{z}", "{fontstack}", "{range}", "{",
)
# 已知反爬站点：curl 被拦(403/412)，但浏览器可正常访问 → 标记 WARN 而非 FAIL
ANTIBOT_HOST = {"baike.baidu.com", "www.bilibili.com", "bilibili.com",
                "www.zhihu.com", "zhihu.com", "weibo.com"}

# 已知失效 → 修复映射（PhET 改名 / 路径变更）
FIX_MAP = {
    "charges-and-fields": "charges-and-fields",          # 存在
    "faradays-law": "faradays-law",                      # 存在
    "circuit-construction-kit-dc": "circuit-construction-kit-dc",
}


def fetch(url, timeout=25):
    """返回 (ok, status, note)。HEAD 不被支持时退化为 GET Range。"""
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return True, r.status, ""
    except urllib.error.HTTPError as e:
        return False, e.code, str(e.reason)[:40]
    except Exception as e:
        return False, 0, type(e).__name__ + ":" + str(e)[:40]


def extract_links(html):
    """抽取 HTML 中的外部链接（含 iframe src / href / JS 字符串）"""
    urls = set()
    for m in re.finditer(r'(?:src|href)\s*=\s*["\'](https?://[^"\']+)["\']', html):
        urls.add(m.group(1))
    for m in re.finditer(r'["\'](https?://[^"\'\s<>]+)["\']', html):
        urls.add(m.group(1))
    out = set()
    for u in urls:
        u = u.rstrip(".,;")
        p = urllib.parse.urlparse(u)
        if p.scheme not in ("http", "https"):
            continue
        if p.netloc in SKIP_HOST:
            continue
        if p.path.lower().endswith(SKIP_EXT):
            continue
        if any(s in u for s in SKIP_SUBSTR):
            continue
        out.add(u)
    return out


def collect():
    """返回 {url: [cid...]}"""
    m = defaultdict(list)
    for d in sorted(COMMUNITY.iterdir()):
        p = d / "index.html"
        if not p.exists():
            continue
        for u in extract_links(p.read_text(encoding="utf-8", errors="replace")):
            m[u].append(d.name)
    return m


def main():
    fix_mode = "--fix" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    urlmap = collect()
    if cids:
        urlmap = {u: v for u, v in urlmap.items() if set(v) & set(cids)}
    print(f"待检查 {len(urlmap)} 个唯一外部链接…\n")

    results = []
    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(fetch, u): u for u in urlmap}
        for f in cf.as_completed(futs):
            u = futs[f]
            ok, status, note = f.result()
            results.append((ok, status, u, urlmap[u], note))

    def is_antibot(u):
        return urllib.parse.urlparse(u).netloc in ANTIBOT_HOST

    def is_bare(u):
        """裸域名 / CDN 基址常量：本身不含具体文件名，404/400 属正常"""
        p = urllib.parse.urlparse(u)
        if p.path in ("", "/") and not p.query:
            return True
        # jsDelivr / unpkg 的 pkg@branch 形式且无扩展名 → 运行时拼接的基址
        last = p.path.rsplit("/", 1)[-1]
        if p.netloc.endswith(("jsdelivr.net", "unpkg.com")) and "@" in last \
                and not Path(last).suffix:
            return True
        return False

    bad, warn = [], []
    for r in results:
        if r[0]:
            continue
        if is_antibot(r[2]) or is_bare(r[2]):
            warn.append(r)
        else:
            bad.append(r)
    good = [r for r in results if r[0]]
    print(f"✅ 可达 {len(good)}    ❌ 失效 {len(bad)}    ⚠️ 疑似(反爬/裸域) {len(warn)}\n")

    if warn:
        print("--- ⚠️ 疑似误报（浏览器可正常访问，非真失效）---")
        for ok, st, u, cs, note in sorted(warn, key=lambda x: x[2]):
            print(f"  [{st or 'ERR'}] {u}  ({note})")
        print()

    if bad:
        # 按域名分组，便于一眼看出是哪类资源挂了
        byhost = defaultdict(list)
        for ok, st, u, cs, note in bad:
            byhost[urllib.parse.urlparse(u).netloc].append((st, u, cs, note))
        for host, items in sorted(byhost.items(), key=lambda x: -len(x[1])):
            print(f"=== {host} ({len(items)}) ===")
            for st, u, cs, note in sorted(items, key=lambda x: x[1]):
                cs_s = ",".join(sorted(cs)[:4]) + ("…" if len(cs) > 4 else "")
                print(f"  [{st or 'ERR'}] {u}")
                print(f"         {note}  ← {cs_s}")
            print()
    else:
        print("全部链接可达 🎉")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
