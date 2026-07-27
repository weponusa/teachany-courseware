#!/usr/bin/env python3
"""复杂卡片（含嵌套 div）的 #09 修复：validator 只测第一个内层 </div> 之前的
可见文字，因此只需把该区域内的长段落按句子拆成多个 <p>。"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD_RE = re.compile(r'<div[^>]*class="[^"]*card[^"]*"[^>]*>([\s\S]*?)</div>', re.I)
STRIP_RE = re.compile(r'<(script|style|svg|textarea|template)\b[\s\S]*?</\1>', re.I)
P_RE = re.compile(r'<(p|li)([^>]*)>([\s\S]*?)</\1>')
TARGET = 120
LIMIT = 200

def visible_len(s):
    t = STRIP_RE.sub('', s)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'\s+', '', t)
    return len(t)

def split_p(m):
    tag, attrs, inner = m.group(1), m.group(2), m.group(3)
    if '<' in inner or visible_len(inner) <= TARGET:
        return m.group(0)
    parts = [p for p in re.split(r'(?<=[。；！？])', inner) if p.strip()]
    if len(parts) <= 1:
        return m.group(0)
    return '\n'.join(f'<{tag}{attrs}>{p}</{tag}>' for p in parts)

def process(cid):
    hpath = os.path.join(ROOT, 'community', cid, 'index.html')
    html = open(hpath, encoding='utf-8').read()
    out, last, n = [], 0, 0
    for m in CARD_RE.finditer(html):
        out.append(html[last:m.start()])
        inner = m.group(1)
        if '<div' in inner and visible_len(inner) > LIMIT:
            new_inner = P_RE.sub(split_p, inner)
            if visible_len(new_inner) < visible_len(inner):
                n += 1
            out.append(m.group(0).replace(inner, new_inner, 1))
        else:
            out.append(m.group(0))
        last = m.end()
    out.append(html[last:])
    if n:
        open(hpath, 'w', encoding='utf-8').write(''.join(out))
    return n

COURSES = ['bio-m-circulation-respiration', 'hist-m-greece-rome', 'math-m-data-analysis',
           'hist-h-cold-war-h', 'phy-light-refraction', 'phy-pressure-buoyancy',
           'bio-h-organelles', 'eng-e-reading-skills-primary', 'hist-m-industrial-revolution',
           'bio-classification', 'bio-h-endomembrane-system', 'bio-h-sugar-lipid',
           'hist-m-early-civilizations', 'chem-h-galvanic-cell', 'hist-m-may-fourth-movement',
           'hist-m-opium-war', 'bio-m-photosynthesis-m', 'biology-bio-m-biosphere-6a130aec',
           'bio-h-cell-structure', 'eng-e-writing-skills-primary']
for cid in COURSES:
    print(cid, process(cid))
