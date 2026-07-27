#!/usr/bin/env python3
"""为 #20 失败课件注入标准连续音频播放清单（audio-config + playlist JSON）。
数据源：tts/manifest.json；缺省时按 tts/*.mp3 文件名生成。
"""
import json, os, re, html as htmllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def build_pages(cdir, cid, course_name):
    tts_dir = os.path.join(cdir, 'tts')
    if not os.path.isdir(tts_dir):
        return []
    entries = []
    mpath = os.path.join(tts_dir, 'manifest.json')
    if os.path.exists(mpath):
        try:
            data = json.load(open(mpath, encoding='utf-8'))
            if isinstance(data, dict):
                data = data.get('items') or data.get('pages') or []
            for e in data:
                src = (e.get('src') or '').lstrip('./')
                label = e.get('title') or e.get('label') or e.get('id') or ''
                entries.append((e.get('id') or '', src, label))
        except Exception:
            pass
    if not entries:
        for f in sorted(os.listdir(tts_dir)):
            if f.endswith('.mp3'):
                entries.append((f[:-4], f'tts/{f}', f'{course_name} 讲解 {f[:-4]}'))
    pages = []
    for eid, src, label in entries:
        if not src.endswith('.mp3'):
            continue
        p = os.path.join(cdir, src)
        if os.path.exists(p) and os.path.getsize(p) >= 20 * 1024:
            pages.append({'id': eid or src, 'src': src, 'label': (label or eid)[:40]})
    return pages

def course_name(cid, cdir):
    try:
        mf = json.load(open(os.path.join(cdir, 'manifest.json'), encoding='utf-8'))
        if mf.get('name'):
            return mf['name']
    except Exception:
        pass
    return cid

def fix(cid):
    cdir = os.path.join(ROOT, 'community', cid)
    hpath = os.path.join(cdir, 'index.html')
    html_src = open(hpath, encoding='utf-8').read()
    if re.search(r'<script[^>]+data-teachany-audio-playlist', html_src):
        # 已有播放清单，但可能引用了不存在的文件 → 重建
        pass
    name = course_name(cid, cdir)
    pages = build_pages(cdir, cid, name)
    if len(pages) < 3:
        return f'skip:only-{len(pages)}-valid-mp3'
    playlist = json.dumps({'version': '2.0', 'pages': pages}, ensure_ascii=False)
    block = ('\n<!-- Audio Config (hidden) -->\n'
             '<div id="audio-config" data-teachany-audio hidden>\n'
             '  <script type="application/json" data-teachany-audio-playlist>\n'
             + playlist + '\n  </script>\n</div>\n')
    if re.search(r'<script[^>]+data-teachany-audio-playlist', html_src):
        # 替换旧清单内容
        html_src = re.sub(
            r'(<script type="application/json" data-teachany-audio-playlist>\s*)[\s\S]*?(\s*</script>)',
            lambda m: m.group(1) + playlist + m.group(2), html_src, count=1)
    elif '</body>' in html_src:
        html_src = html_src.replace('</body>', block + '</body>', 1)
    else:
        html_src += block
    open(hpath, 'w', encoding='utf-8').write(html_src)
    return f'ok:{len(pages)}'

def main():
    recs = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
    f20 = [r['id'] for r in recs if any(x.startswith('#20') for x in r['failed'])]
    stats = {}
    for cid in f20:
        try:
            r = fix(cid)
        except Exception as e:
            r = f'error:{e}'
        stats[r] = stats.get(r, 0) + 1
        if not r.startswith('ok'):
            print(cid, r)
    print(stats)

if __name__ == '__main__':
    main()
