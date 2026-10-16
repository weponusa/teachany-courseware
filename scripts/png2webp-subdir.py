#!/usr/bin/env python3
"""png2webp-subdir.py — 补扫 community/*/assets/** 子目录里的 PNG（递归）。

与 png2webp-batch.py 的区别：递归扫描子目录（illustrations/、media/ 等）。
逻辑一致：webp 不更小则跳过；只改同 course 的 *.html/*.css/*.js 引用。
"""
import concurrent.futures, os, pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
SOCIAL_META = re.compile(r'<(?:meta|link)[^>]+(?:og|image|twitter)[^>]*>', re.I)
REF_PNG = re.compile(
    r'(?P<attr>(?:src|href|data-src|data-background-image|content)\s*=\s*[\"\'])'
    r'(?P<url>[^\"\']+\.png)(?P<q>[\"\'])', re.I)
CSS_URL_PNG = re.compile(
    r'(?P<attr>url\(\s*[\"\']?)(?P<url>[^\"\'\)]+\.png)(?P<q>[\"\']?\s*\))', re.I)

def cwebp_one(args):
    src, dst, q = args
    src = pathlib.Path(src); dst = pathlib.Path(dst)
    if dst.exists() and dst.stat().st_size > 0 and dst.stat().st_size <= src.stat().st_size:
        return ('reuse', src, src.stat().st_size, dst.stat().st_size)
    dst.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["cwebp", "-q", str(q), "-m", "6", "-mt", "-quiet", str(src), "-o", str(dst)],
                       capture_output=True)
    if r.returncode != 0 or not dst.exists():
        return ('fail', src, src.stat().st_size, 0)
    return ('done', src, src.stat().st_size, dst.stat().st_size)

def update_file(f, keys, full):
    if not f.exists(): return 0
    text = f.read_text(encoding='utf-8', errors='ignore')
    sl = set(i for i, l in enumerate(text.splitlines(keepends=True)) if SOCIAL_META.search(l))
    out = []; n = 0
    for i, line in enumerate(text.splitlines(keepends=True)):
        if i in sl: out.append(line); continue
        new = line
        def repl(m):
            url = m.group('url'); q = m.group('q')
            base = os.path.basename(url)
            if url in full: return m.group('attr') + full[url] + q
            if base in keys: return m.group('attr') + url[:-4] + '.webp' + q
            return m.group(0)
        new = REF_PNG.sub(repl, new)
        def repl_css(m):
            url = m.group('url'); base = os.path.basename(url)
            if base in keys: return m.group('attr') + url[:-4] + '.webp' + m.group('q')
            return m.group(0)
        new = CSS_URL_PNG.sub(repl_css, new)
        if new != line: n += 1
        out.append(new)
    nt = ''.join(out)
    if nt != text: f.write_text(nt, encoding='utf-8')
    return n

def main():
    community = ROOT / "community"
    plan = []
    for course in community.iterdir():
        if not course.is_dir(): continue
        ca = course / "assets"
        if not ca.is_dir(): continue
        for p in ca.rglob("*.png"):
            if p.parent == ca: continue  # 顶层已在上一轮处理
            if p.stat().st_size > 100_000:
                plan.append((p, p.with_suffix(".webp")))
    print(f"补扫候选 {len(plan)} 个子目录 png")
    if not plan: return
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
        for r in ex.map(cwebp_one, [(s, d, 78) for s, d in plan]):
            results.append(r)
    new = sum(1 for r in results if r[0] == 'done')
    reuse = sum(1 for r in results if r[0] == 'reuse')
    fail = sum(1 for r in results if r[0] == 'fail')
    saved = sum(r[2] - r[3] for r in results if r[0] in ('done','reuse'))
    print(f"✅ new {new}  ♻ {reuse}  ❌ {fail}   节省 {saved/1024/1024:.1f} MB")
    keys = set(); full = {}
    for tag, src, psz, wsz in results:
        if tag in ('done','reuse') and wsz > 0 and wsz <= psz:
            full[str(src)] = str(src.with_suffix('.webp'))
            keys.add(src.name)
    # 更新引用
    files = set()
    for s, _ in plan:
        cdir = s.parent.parent
        for ext in ('*.html', '*.css', '*.js'):
            for f in cdir.glob(ext): files.add(f)
    n = 0
    for f in files:
        if update_file(f, keys, full): n += 1
    print(f"📝 改了 {n} 个文件")

if __name__ == "__main__":
    main()
