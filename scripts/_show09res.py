#!/usr/bin/env python3
"""展示 14 个残余 #09 课件中超长卡片的结构（开标签 + 纯文本前 200 字 + HTML 前 500 字符）。"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD_RE = re.compile(r'<div[^>]*class="[^"]*card[^"]*"[^>]*>([\s\S]*?)</div>', re.I)
STRIP_RE = re.compile(r'<(script|style|svg|textarea|template)\b[\s\S]*?</\1>', re.I)
COURSES = ['bio-h-cell-structure', 'bio-h-endomembrane-system', 'bio-h-organelles',
           'eng-e-reading-skills-primary', 'eng-e-writing-skills-primary',
           'geo-m-continents-oceans', 'hist-h-cold-war-h', 'hist-m-greece-rome',
           'hist-m-industrial-revolution', 'hist-m-may-fourth-movement',
           'hist-m-opium-war', 'math-m-data-analysis', 'phy-light-refraction',
           'phy-pressure-buoyancy']
for cid in COURSES:
    html = open(os.path.join(ROOT, 'community', cid, 'index.html'), encoding='utf-8').read()
    for m in CARD_RE.finditer(html):
        inner_html = re.sub(r'^<div[^>]*>', '', m.group(0), flags=re.I)
        if re.search(r'class="[^"]*card', inner_html, re.I):
            continue
        t = STRIP_RE.sub('', m.group(1))
        t = re.sub(r'<[^>]+>', '', t)
        t = re.sub(r'\s+', '', t)
        if len(t) > 200:
            open_tag = m.group(0)[:m.group(0).index('>') + 1]
            print(f'=== {cid} len={len(t)} tag={open_tag[:100]}')
            print('TEXT:', t[:180])
            print('HTML:', m.group(1)[:300].replace('\n', ' '))
            break
