#!/usr/bin/env python3
"""png2webp-batch.py — 全站 PNG → WebP 转换与引用更新（2026-10-15）

范围：
- community/*/assets/*.png （> 100KB）
- assets/*.png（站点级图标；> 50KB）
- webp 比 png 大的不替换（保留原 png 引用）
- 同步更新：同目录 *.html/*.css/*.js 中的引用（仅本课件内）
- 不动 og:image / twitter:image 等社交分享图

依赖：cwebp（libwebp），Python 3.10+
"""
import argparse, concurrent.futures, os, pathlib, re, subprocess, sys, time
ROOT = pathlib.Path(__file__).resolve().parent.parent
SOCIAL_META = re.compile(r'<(?:meta|link)[^>]+(?:og|image|twitter)[^>]*>', re.I)
REF_PNG = re.compile(
    r'(?P<attr>(?:src|href|data-src|data-background-image|content)\s*=\s*[\"\'])'
    r'(?P<url>[^\"\']+\.png)(?P<q>[\"\'])', re.I)
CSS_URL_PNG = re.compile(
    r'(?P<attr>url\(\s*[\"\']?)(?P<url>[^\"\'\)]+\.png)(?P<q>[\"\']?\s*\))', re.I)
REF_PNG_HTTPS = re.compile(
    r'(?P<attr>(?:src|href|data-src|data-background-image|content)\s*=\s*[\"\'])'
    r'(?P<url>https?://[^\"\']+\.png)(?P<q>[\"\'])', re.I)
URL_PATH = re.compile(r'^(?:https?://[^/]+)?(.*?)$')

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

def update_file(f: pathlib.Path, plan_keys: set[str], plan_full_to_webp: dict[str, str]) -> int:
    if not f.exists(): return 0
    text = f.read_text(encoding='utf-8', errors='ignore')
    social_lines = set()
    for i, line in enumerate(text.splitlines(keepends=True)):
        if SOCIAL_META.search(line):
            social_lines.add(i)
    n = 0
    out = []
    for i, line in enumerate(text.splitlines(keepends=True)):
        if i in social_lines:
            out.append(line); continue
        new = line
        def repl_attr(m):
            url = m.group('url'); q = m.group('q'); base = os.path.basename(url)
            if url in plan_full_to_webp:
                return m.group('attr') + plan_full_to_webp[url] + q
            if base in plan_keys and url.startswith(('./', '/', '')):
                # 相对引用：把 url 末尾 .png 换成 .webp
                return m.group('attr') + url[:-4] + '.webp' + q
            return m.group(0)
        new = REF_PNG.sub(repl_attr, new)
        new = REF_PNG_HTTPS.sub(repl_attr, new)  # https://www.teachany.cn/assets/x.png 改写需要再过滤
        def repl_css(m):
            url = m.group('url')
            base = os.path.basename(url)
            if base in plan_keys and url.startswith(('./', '/', '')):
                return m.group('attr') + url[:-4] + '.webp' + m.group('q')
            return m.group(0)
        new = CSS_URL_PNG.sub(repl_css, new)
        if new != line:
            n += 1
        out.append(new)
    new_text = ''.join(out)
    if new_text != text:
        f.write_text(new_text, encoding='utf-8')
    return n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--community", default=str(ROOT / "community"))
    ap.add_argument("--assets", default=str(ROOT / "assets"))
    ap.add_argument("--q", type=int, default=78)
    ap.add_argument("--threshold", type=int, default=100_000, help="仅转换 >threshold 字节的 png")
    ap.add_argument("--threshold-assets", type=int, default=50_000)
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 4)
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    community = pathlib.Path(args.community)
    assets = pathlib.Path(args.assets)
    plan: list[tuple[pathlib.Path, pathlib.Path]] = []
    print(f"🔍 扫描 community/{community.name}…")
    for course in community.iterdir():
        if not course.is_dir(): continue
        ca = course / "assets"
        if not ca.is_dir(): continue
        for p in ca.glob("*.png"):
            if p.stat().st_size > args.threshold:
                plan.append((p, p.with_suffix(".webp")))
    print(f"   {len(plan)} 个 community png 候选")
    if assets.is_dir():
        n_pre = len(plan)
        for p in assets.glob("*.png"):
            if p.stat().st_size > args.threshold_assets:
                plan.append((p, p.with_suffix(".webp")))
        print(f"   {len(plan) - n_pre} 个 assets png 候选")
    if args.dry:
        print("(dry) 仅展示计划，不实际转换")
        for s, d in plan[:20]:
            print(f"  {s.name}  {s.stat().st_size/1024:.0f}KB")
        return
    print(f"⚙️  并行转换 workers={args.workers}…")
    t0 = time.time()
    results: list[tuple] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for r in ex.map(cwebp_one, [(s, d, args.q) for s, d in plan]):
            results.append(r)
    new_count = sum(1 for r in results if r[0] == 'done')
    reuse = sum(1 for r in results if r[0] == 'reuse')
    fail = sum(1 for r in results if r[0] == 'fail')
    saved = sum(r[2] - r[3] for r in results if r[0] in ('done','reuse'))
    print(f"   ✅ new {new_count}  ♻ reuse {reuse}  ❌ fail {fail}   节省 {saved/1024/1024:.1f} MB  用时 {time.time()-t0:.1f}s")
    # 收集 实际可用的 png→webp 映射（仅 done/reuse 且 webp 更小或相等）
    usable: dict[str, str] = {}  # png 全路径 -> webp 路径
    keys: set[str] = set()      # png basename
    for tag, src, psz, wsz in results:
        if tag in ('done','reuse') and wsz > 0 and wsz <= psz:
            usable[str(src)] = str(src.with_suffix('.webp'))
            keys.add(src.name)
    # 找更新的文件
    print("📝 更新引用…")
    targets: set[pathlib.Path] = set()
    for s, _ in plan:
        # 同 course 的 *.html，*/*.html，*/*.css
        cdir = s.parent.parent  # course dir
        for ext in ('*.html', '*.css', '*.js'):
            for f in cdir.glob(ext):
                targets.add(f)
        # assets/scripts 也算
        for ext in ('*.css', '*.js'):
            for f in (s.parent / 'scripts').glob(ext):
                targets.add(f)
    n_files = 0
    for f in targets:
        n = update_file(f, keys, {})
        if n: n_files += 1
    print(f"   改了 {n_files} 个文件")
    # 处理根 assets/ 自身的引用（root html / scripts/ 引用 teachany-icon）
    print("📝 更新根 assets/ 引用（teachany-icon / teachany-logo）…")
    root_targets = []
    for pat in ('*.html', '*.css', '*.js'):
        root_targets += list(ROOT.glob(pat))
        root_targets += list((ROOT / 'scripts').glob(pat)) if (ROOT / 'scripts').is_dir() else []
        root_targets += list((ROOT / 'assets' / 'scripts').glob(pat)) if (ROOT / 'assets' / 'scripts').is_dir() else []
    n_root = 0
    seen = set()
    for f in root_targets:
        if f in seen or not f.exists(): continue
        seen.add(f)
        n = update_file(f, keys, {})
        if n: n_root += 1
    print(f"   根目录改了 {n_root} 个文件")
    print(f"\n🏁 完成。节省 {saved/1024/1024:.1f} MB；可清理（构建脚本会剪枝） {len(usable)} 个未引用 png")

if __name__ == "__main__":
    main()
