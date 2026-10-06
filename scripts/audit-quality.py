#!/usr/bin/env python3
"""TeachAny 课件质检审计（L0–L5 分层）

用法：
  python3 scripts/audit-quality.py --mode static --out /tmp/qa-static.json
  python3 scripts/audit-quality.py --mode render --sample 0.05 --out /tmp/qa-render.json
  python3 scripts/audit-quality.py --mode map --out /tmp/qa-map.json
  python3 scripts/audit-quality.py --score /tmp/qa-static.json [/tmp/qa-render.json] [--out /tmp/qa-score.json]

设计原则：
  - L0 合规 / L2 渲染 = 硬阻断（硬伤，内容再好也不能发）
  - L1 结构 / L3 内容 / L4 资产 / L5 深度 = 记分（0–100），进排行榜
"""
import argparse, glob, json, os, re, statistics as st, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ★ 注意：不要把「占位」列入 —— 它在小学数学里是正当术语
#   （"哪一位上一个单位也没有就写 0 占位""数位表占位"），
#   实测 9 门"硬阻断"里 8 门是它造成的误报。单列一个不阻断的软信号。
# 中文占位词（大小写无关）
PLACEHOLDER_CI = [r'待补充', r'待完善', r'Lorem', r'此处省略',
                  r'敬请期待', r'即将上线', r'待生成', r'示例文本', r'暂无内容']
# ★ TODO 必须**大小写敏感**：`"status": "todo"` 是知识点状态枚举（表示后续未开课），
#   不是占位符。实测它造成了 1 门误报。
PLACEHOLDER_CS = [r'\bTODO\b']
SOFT_TERM = [r'占位']


def count_placeholders(html):
    n = sum(len(re.findall(p, html, re.I)) for p in PLACEHOLDER_CI)
    n += sum(len(re.findall(p, html)) for p in PLACEHOLDER_CS)
    return n
# 外链「库」（可本地化） vs 外链「应用」（只能做降级提示）
LIB_HOSTS = ('unpkg.com', 'cdn.jsdelivr.net', 'd3js.org', '3Dmol.org', 'cdnjs.cloudflare.com')
APP_HOSTS = ('phet.colorado.edu', 'www.geogebra.org', 'basic.smartedu.cn')
VENDOR_MAP = {  # 期望的本地化目标（用于 L4 判定）
    'leaflet': 'assets/vendor/leaflet/leaflet.js',
    'd3': 'assets/vendor/d3.min.js',
    '3dmol': 'assets/vendor/3dmol/3Dmol-min.js',
}

CANON_PAGES = 16  # v2 标准页数


def iter_courses():
    for base in ('community', 'examples'):
        d = ROOT / base
        if not d.is_dir():
            continue
        for c in sorted(d.iterdir()):
            if c.is_dir() and not c.name.startswith(('_', '.')) and (c / 'index.html').exists():
                yield c


def scan_static():
    rows = []
    for c in iter_courses():
        h = (c / 'index.html').read_text(encoding='utf-8', errors='ignore')
        m = {}
        try:
            m = json.loads((c / 'manifest.json').read_text(encoding='utf-8'))
        except Exception:
            pass
        body = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', '', h, flags=re.I)
        text = ' '.join(t.strip() for t in re.findall(r'>([^<>]{2,400})<', body))
        cn = len(re.findall(r'[\u4e00-\u9fff]', text))
        pages = len(re.findall(r'class="slide-page', h))
        ad, td = c / 'assets', c / 'tts'
        ext_lib, ext_app = {}, {}
        for u in re.findall(r'(?:src|href)="(https?://[^"]+)"', h):
            host = re.match(r'https?://([^/]+)', u).group(1)
            if host in LIB_HOSTS:
                ext_lib[host] = ext_lib.get(host, 0) + 1
            elif host in APP_HOSTS:
                ext_app[host] = ext_app.get(host, 0) + 1
        row = {
            'id': c.name, 'dir': str(c.relative_to(ROOT)),
            'subject': m.get('subject', ''), 'grade': str(m.get('grade', '')),
            'title': m.get('title') or m.get('name') or '',
            'bytes': len(h), 'cn_chars': cn, 'pages': pages,
            'cn_per_page': round(cn / pages) if pages else cn,
            'sections': len(re.findall(r'<section', h, re.I)),
            'imgs': len(re.findall(r'<img', h, re.I)),
            'canvas': len(re.findall(r'<canvas', h, re.I)),
            'ta_figure': len(re.findall(r'ta-standard-figure', h)),
            'v2_paged': ('slide-page' in h and 'sidenav' in h),
            'placeholder_hits': count_placeholders(h),
            'soft_term_hits': sum(len(re.findall(p, h, re.I)) for p in SOFT_TERM),
            'has_tutor': 'ai-tutor' in h or 'TeachAnyTutor' in h,
            'has_kg': 'data-teachany-kg' in h or 'teachany-knowledge-graph' in h,
            # 标记经 433 门 v2 课件校准（2026-09-22）：
            #   深层理解 97% · 基础巩固 72% · class="choice" 73%
            'has_homework': any(m in h for m in ('作业分层', '基础巩固', '迁移挑战')),
            'has_insight': ('深层理解' in h) or ('insight' in h.lower()),
            'has_quiz': any(m in h for m in ('错因提醒', 'class="choice"', 'data-answer', '选择题')),
            'ext_lib': ext_lib, 'ext_app': ext_app,
            'map_like': len(re.findall(r'geojson|map-host|map-scope|leaflet', h, re.I)),
            'webp': len(list(ad.glob('*.webp'))) if ad.is_dir() else 0,
            'png': len(list(ad.glob('*.png'))) if ad.is_dir() else 0,
            'svg': len(list(ad.glob('*.svg'))) if ad.is_dir() else 0,
            'mp4': len(list(ad.glob('*.mp4'))) if ad.is_dir() else 0,
            'tts_mp3': len(list(td.glob('*.mp3'))) if td.is_dir() else 0,
        }
        rows.append(row)
    return rows


def scan_map():
    """L0 地图合规 + L4 依赖检查"""
    out = {'geojson': [], 'issues': []}
    for g in sorted((ROOT / 'assets' / 'maps').rglob('*.geojson')):
        try:
            d = json.loads(g.read_text(encoding='utf-8'))
        except Exception:
            continue
        names = []
        for ft in d.get('features', []):
            p = ft.get('properties', {}) or {}
            names.append(str(p.get('name') or p.get('NAME') or p.get('adcode') or ''))
        cn_map = 'china' in str(g).lower() or 'chrono-cn' in str(g)
        item = {'file': str(g.relative_to(ROOT)), 'features': len(names),
                'is_china': cn_map,
                'has_nanhai': any(('南海' in n) or ('诸岛' in n) or ('九段' in n) or ('十段' in n) for n in names)}
        out['geojson'].append(item)
        if cn_map and not item['has_nanhai']:
            out['issues'].append({'layer': 'L0', 'code': 'MAP_MISSING_NANHAI', 'file': item['file']})
    return out


def scan_render(sample_ratio=0.05, seed=42):
    import random
    from playwright.sync_api import sync_playwright
    rows = scan_static()
    random.seed(seed)
    by = defaultdict(list)
    for r in rows:
        by[bool(r['v2_paged'])].append(r)
    pick = []
    for k, v in by.items():
        pick += random.sample(v, max(1, int(len(v) * sample_ratio)))
    pick += [r for r in rows if r['map_like'] > 3][:6]
    MEASURE = """() => {
      const out={pages:[]};
      const pages=[...document.querySelectorAll('.slide-page')];
      const target=pages.length?pages:[document.body];
      const vw=innerWidth;
      for(const pg of target){
        const r0=pg.getBoundingClientRect();
        const m={h:Math.round(r0.height),overflow:0,offscreen:0,overlap:0,minFont:999,tiny:0,broken:0,texts:0};
        const els=[...pg.querySelectorAll('p,li,span,h1,h2,h3,h4,td,th,label,div')].filter(e=>
          e.childNodes.length===1&&e.firstChild&&e.firstChild.nodeType===3&&e.textContent.trim().length>3);
        m.texts=els.length; const bx=[];
        for(const e of els){
          const cs=getComputedStyle(e); const fs=parseFloat(cs.fontSize)||0;
          if(fs>0) m.minFont=Math.min(m.minFont,fs);
          if(fs>0&&fs<12) m.tiny++;
          if(e.scrollWidth>e.clientWidth+2&&cs.overflow!=='visible') m.overflow++;
          const r=e.getBoundingClientRect();
          if(r.width>0){ if(r.right>vw+2||r.left<-2) m.offscreen++; bx.push([r.left,r.top,r.right,r.bottom]); }
        }
        for(let i=0;i<bx.length;i++)for(let j=i+1;j<bx.length;j++){
          const a=bx[i],b=bx[j];
          if(Math.min(a[2],b[2])-Math.max(a[0],b[0])>6&&Math.min(a[3],b[3])-Math.max(a[1],b[1])>6) m.overlap++;
        }
        for(const im of pg.querySelectorAll('img')) if(!im.naturalWidth) m.broken++;
        out.pages.push(m);
      }
      out.leaflet=typeof window.L!=='undefined';
      out.mapHosts=document.querySelectorAll('[class*=map-host],[class*=map-scope],.leaflet-container').length;
      return out;
    }"""
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for r in pick:
            pg = b.new_page(viewport={'width': 1440, 'height': 900})
            try:
                pg.goto('file://' + str((ROOT / r['dir']).resolve()) + '/index.html',
                        wait_until='domcontentloaded', timeout=45000)
                pg.wait_for_timeout(1500)
                n = pg.eval_on_selector_all('.slide-page', 'e=>e.length')
                for i in range(min(n, 20)):
                    pg.evaluate(f"() => document.querySelectorAll('.sidenav-dot')[{i}]?.click()")
                    pg.wait_for_timeout(250)
                m = pg.evaluate(MEASURE)
                ps = m['pages']
                out.append({'id': r['id'], 'v2': r['v2_paged'], 'pages': len(ps),
                            'overflow': sum(x['overflow'] for x in ps),
                            'offscreen': sum(x['offscreen'] for x in ps),
                            'overlap': sum(x['overlap'] for x in ps),
                            'tiny': sum(x['tiny'] for x in ps),
                            'broken': sum(x['broken'] for x in ps),
                            'minFont': min((x['minFont'] for x in ps if x['minFont'] < 999), default=None),
                            'maxPageH': max((x['h'] for x in ps), default=0),
                            'leaflet': m['leaflet'], 'mapHosts': m['mapHosts']})
            except Exception as e:
                out.append({'id': r['id'], 'error': str(e)[:80]})
            pg.close()
        b.close()
    return out


def score_rows(static, render=None, maps=None):
    rmap = {r['id']: r for r in (render or [])}
    mmap = {g['file']: g for g in (maps or {}).get('geojson', [])}
    out = []
    for r in static:
        issues = []
        # L0 合规
        if r['placeholder_hits'] > 0:
            issues.append({'layer': 'L0', 'code': 'PLACEHOLDER_TEXT', 'count': r['placeholder_hits']})
        # L1 结构（40 分）
        s1 = 40
        if not r['v2_paged']:
            s1 -= 20; issues.append({'layer': 'L1', 'code': 'NOT_V2_PAGED'})
        if r['v2_paged'] and r['pages'] != CANON_PAGES:
            s1 -= 6; issues.append({'layer': 'L1', 'code': 'PAGE_COUNT_OFF', 'pages': r['pages']})
        for key, code in [('has_tutor', 'NO_TUTOR'), ('has_kg', 'NO_KG'), ('has_quiz', 'NO_QUIZ')]:
            if not r[key]:
                s1 -= 4; issues.append({'layer': 'L1', 'code': code})
        # L3 内容（25 分）
        s3 = 25
        dens = r['cn_per_page']
        if r['v2_paged'] and dens < 120:
            s3 -= 10; issues.append({'layer': 'L3', 'code': 'LOW_DENSITY', 'cn_per_page': dens})
        if r['cn_chars'] < 1500:
            s3 -= 8; issues.append({'layer': 'L3', 'code': 'THIN_CONTENT', 'cn_chars': r['cn_chars']})
        if r['ta_figure'] == 0:
            s3 -= 4; issues.append({'layer': 'L3', 'code': 'NO_BODY_FIGURE'})
        # L4 资产（20 分）
        s4 = 20
        if r['tts_mp3'] == 0:
            s4 -= 8; issues.append({'layer': 'L4', 'code': 'NO_TTS'})
        elif r['tts_mp3'] < 8:
            s4 -= 4; issues.append({'layer': 'L4', 'code': 'TTS_PARTIAL', 'tts': r['tts_mp3']})
        if r['ext_lib']:
            s4 -= 6; issues.append({'layer': 'L4', 'code': 'EXTERNAL_LIB', 'hosts': list(r['ext_lib'])})
        if r['webp'] == 0 and r['png'] == 0 and r['svg'] == 0:
            s4 -= 6; issues.append({'layer': 'L4', 'code': 'NO_IMAGE_ASSET'})
        # L5 深度（15 分）
        s5 = 15
        if not r['has_homework']:
            s5 -= 8; issues.append({'layer': 'L5', 'code': 'NO_LAYERED_HOMEWORK'})
        if not r['has_insight']:
            s5 -= 7; issues.append({'layer': 'L5', 'code': 'NO_INSIGHT'})
        # L2 渲染（来自抽样）
        rr = rmap.get(r['id'])
        if rr and 'error' not in rr:
            if rr['overflow'] or rr['offscreen']:
                issues.append({'layer': 'L2', 'code': 'RENDER_HARD', 'overflow': rr['overflow'], 'offscreen': rr['offscreen']})
            if rr['overlap'] > 3:
                issues.append({'layer': 'L2', 'code': 'TEXT_OVERLAP', 'count': rr['overlap']})
            if rr['tiny'] > 0:
                issues.append({'layer': 'L2', 'code': 'TINY_TEXT', 'count': rr['tiny']})
            if rr['broken'] > 0:
                issues.append({'layer': 'L2', 'code': 'BROKEN_IMAGE', 'count': rr['broken']})
        tot = max(0, s1) + max(0, s3) + max(0, s4) + max(0, s5)
        hard = [i for i in issues if i['layer'] in ('L0', 'L2') and i['code'] in
                ('PLACEHOLDER_TEXT', 'RENDER_HARD')]
        out.append({'id': r['id'], 'subject': r['subject'], 'grade': r['grade'], 'title': r['title'],
                    'score': tot, 'band': 'A' if tot >= 90 else 'B' if tot >= 75 else 'C' if tot >= 60 else 'D',
                    'hard_block': bool(hard), 'issues': issues,
                    'sub': {'L1': max(0, s1), 'L3': max(0, s3), 'L4': max(0, s4), 'L5': max(0, s5)}})
    out.sort(key=lambda x: x['score'])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['static', 'render', 'map'])
    ap.add_argument('--score', nargs='*')
    ap.add_argument('--sample', type=float, default=0.05)
    ap.add_argument('--out', default=None)
    a = ap.parse_args()

    if a.mode == 'static':
        rows = scan_static()
        print(f"静态画像 {len(rows)} 门")
        _dump(rows, a.out or '/tmp/qa-static.json')
    elif a.mode == 'render':
        rows = scan_render(a.sample)
        print(f"渲染审计 {len(rows)} 门")
        _dump(rows, a.out or '/tmp/qa-render.json')
    elif a.mode == 'map':
        res = scan_map()
        print(f"地图检查：{len(res['geojson'])} 个 geojson，问题 {len(res['issues'])}")
        for i in res['issues']:
            print('   ', i['code'], i['file'])
        _dump(res, a.out or '/tmp/qa-map.json')
    elif a.score:
        static = json.loads(Path(a.score[0]).read_text())
        # 自动识别：list = 渲染审计；dict 且含 geojson = 地图检查
        render = maps = None
        for extra in a.score[1:]:
            obj = json.loads(Path(extra).read_text())
            if isinstance(obj, dict) and 'geojson' in obj:
                maps = obj
            elif isinstance(obj, list):
                render = obj
        scored = score_rows(static, render, maps)
        print(f"出分 {len(scored)} 门")
        bands = Counter(s['band'] for s in scored)
        print("  分档:", dict(bands))
        print("  硬阻断:", sum(1 for s in scored if s['hard_block']))
        codes = Counter(i['code'] for s in scored for i in s['issues'])
        print("  问题 Top10:", codes.most_common(10))
        print("  最差 10 门:")
        for s in scored[:10]:
            print(f"    {s['score']:3d} {s['band']} {s['id'][:34]:34s} {[i['code'] for i in s['issues']][:4]}")
        _dump(scored, a.out or '/tmp/qa-score.json')
    else:
        ap.print_help()


def _dump(obj, path):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False), encoding='utf-8')
    print(f"  → {path}")


if __name__ == '__main__':
    main()
