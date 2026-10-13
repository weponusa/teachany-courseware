#!/usr/bin/env python3
"""分析 #20 失败原因：缺 mp3 / mp3 太小 / 缺播放器。"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recs = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
f20 = [r['id'] for r in recs if any(x.startswith('#20') for x in r['failed'])]
MP3_RE = re.compile(r'''["']([^"']+\.mp3)["']''', re.I)
SKIP = re.compile(r'^(https?:|data:|blob:)', re.I)
import collections
stats = collections.Counter()
detail = {}
for cid in f20:
    cdir = os.path.join(ROOT, 'community', cid)
    html = open(os.path.join(cdir, 'index.html'), encoding='utf-8').read()
    refs = [r for r in MP3_RE.findall(html) if not SKIP.match(r)]
    valid = 0
    for r in refs:
        t = r.split('?')[0].split('#')[0]
        p = os.path.join(ROOT, t.lstrip('/')) if t.startswith('/') else os.path.join(cdir, t)
        if os.path.exists(p) and os.path.getsize(p) >= 20*1024:
            valid += 1
    has_player = bool(re.search(r'data-teachany-audio-playlist|teachany-audio-player\.js|audioPlaylist', html, re.I))
    # 目录里实际有多少 mp3
    disk = []
    tts_dir = os.path.join(cdir, 'tts')
    if os.path.isdir(tts_dir):
        disk = [f for f in os.listdir(tts_dir) if f.endswith('.mp3') and os.path.getsize(os.path.join(tts_dir, f)) >= 20*1024]
    key = (min(valid, 3), has_player, len(disk) >= 3)
    stats[key] += 1
    detail[cid] = {'refs': len(refs), 'valid': valid, 'player': has_player, 'disk_mp3': len(disk)}
print('(valid( capped3), player, disk>=3) -> count')
for k, v in stats.most_common():
    print(k, v)
json.dump(detail, open(os.path.join(ROOT, 'qc-20-detail.json'), 'w'), ensure_ascii=False, indent=1)
