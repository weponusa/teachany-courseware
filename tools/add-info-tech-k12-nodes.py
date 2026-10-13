#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把小学/初中信息科技补进知识体系（树 + 统一树 + 节点索引）。

背景
----
`data/trees/cn/elementary/info-tech.json`（16 个节点）和 `cn/middle/info-tech.json`（14 个）
早就存在、课件也都在，但：
  · `data/trees/cn-unified/info-tech.json` 的 `_meta.merged_from` 只有 `high/info-tech.json`
    —— 统一树从没在小学/初中建树后重跑过；
  · `data/node-index.json` 里 `it-e-*` / `it-m-*` 节点数为 0（只有 10 个 `it-h-*`）；
  · `tree.html` 的 TREES 清单里，小学/初中两段没有 info-tech 这一科（高中才有）。
结果：30 门信息科技课件（小学 16 + 初中 14）学生在知识地图里点不到。

本脚本只做前两步（树与索引），tree.html 的清单在文件里单独改。
幂等：重复跑不会重复加节点。

用法:  python3 tools/add-info-tech-k12-nodes.py [--dry]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TREES = ROOT / 'data' / 'trees'
UNIFIED = TREES / 'cn-unified' / 'info-tech.json'
NODE_INDEX = ROOT / 'data' / 'node-index.json'
REGISTRY = ROOT / 'registry.json'
SITE = 'https://www.teachany.cn'
STAGES = [('elementary', '小学'), ('middle', '初中'), ('high', '高中')]
STAGE_ZH = {'elementary': '小学', 'middle': '初中', 'high': '高中'}


def load(p: Path):
    return json.loads(p.read_text(encoding='utf-8'))


def stage_nodes(stage: str):
    """返回 (tree_dict, [(domain, node)])。"""
    d = load(TREES / 'cn' / stage / 'info-tech.json')
    out = []
    for dom in d.get('domains') or []:
        for n in dom.get('nodes') or []:
            out.append((dom, n))
    return d, out


def build_unified():
    doms, total, meta_from = [], 0, []
    spans = []
    for stage, zh in STAGES:
        d, pairs = stage_nodes(stage)
        meta_from.append(f'{stage}/info-tech.json')
        gr = d.get('grade_range') or []
        if len(gr) == 2 and all(isinstance(x, int) for x in gr):
            spans.append(tuple(gr))
        seen = set()
        for dom in d.get('domains') or []:
            nodes = dom.get('nodes') or []
            if not nodes:
                continue
            key = dom.get('id')
            if key in seen:
                continue
            seen.add(key)
            doms.append({
                'id': dom.get('id'),
                'name': f'{zh}·{dom.get("name")}',
                'color': dom.get('color', '#3b82f6'),
                'nodes': nodes,
            })
            total += len(nodes)
    first, last = (min(s[0] for s in spans), max(s[1] for s in spans)) if spans else (1, 12)
    return {
        'subject': 'info-tech',
        'name': '信息科技',
        'name_en': 'Information Technology',
        'grade_range': [first or 1, last or 12],
        'stage_coverage': [s for s, _ in STAGES],
        'total_nodes': total,
        'domains': doms,
        '_meta': {
            'merged_from': meta_from,
            'prereq_added': 0,          # data/stage-bridges.json 里没有 info-tech 跨学段桥接
            'skills_added': 0,
            'format_version': '2.0-unified',
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()

    reg = {c['id']: c for c in load(REGISTRY).get('courses', [])}
    idx = load(NODE_INDEX)
    nodes = idx['nodes']

    unified = build_unified()
    added, missing_course = [], []
    for stage, zh in STAGES[:2]:                     # 高中已在索引里，这里补小学/初中
        _d, pairs = stage_nodes(stage)
        for dom, n in pairs:
            nid = n.get('id')
            if not nid or nid in nodes:
                continue
            cids = [c for c in (n.get('courses') or []) if isinstance(c, str)]
            courses = []
            for cid in cids:
                r = reg.get(cid)
                if not r:
                    missing_course.append((nid, cid))
                    continue
                path = (r.get('path') or f'community/{cid}').strip('/')
                courses.append({'id': cid, 'name_zh': r.get('name') or cid,
                                'download_url': f'{SITE}/{path}/'})
            entry = {
                'node_id': nid,
                'name_zh': n.get('name', ''),
                'name_en': n.get('name_en', ''),
                'domain': dom.get('name', ''),
                'curriculum': 'cn',
                'stage': stage,
                'subject': 'info-tech',
                'tree_path': f'cn/{stage}/info-tech.json',
                'courses': courses,
                'md_path': f'skill/data/kp-md/kp-{nid}.md',
                'md_status': 'ready',
            }
            pre = [p for p in (n.get('prerequisites') or []) if isinstance(p, str) and p]
            if pre:
                entry['prereq_ids'] = pre
            nodes[nid] = entry
            added.append((nid, n.get('name'), stage, cids))

    m = idx.get('_meta', {})
    m['total_nodes'] = len(nodes)
    m['with_md'] = sum(1 for v in nodes.values() if v.get('md_status') == 'ready')
    m['with_hero'] = sum(1 for v in nodes.values() if v.get('hero_image'))
    m['with_prereq'] = sum(1 for v in nodes.values() if v.get('prereq_ids'))
    idx['_meta'] = m

    print(f'统一树：{unified["total_nodes"]} 个节点（{len(unified["domains"])} 个模块），'
          f'stage_coverage={unified["stage_coverage"]} grade_range={unified["grade_range"]}')
    print(f'节点索引：新增 {len(added)} 个节点 → 总计 {len(nodes)}（with_md={m["with_md"]} with_prereq={m["with_prereq"]}）')
    for a in added:
        print(f'   + {a[0]:34} {a[1]}  [{STAGE_ZH[a[2]]}]  courses={a[3]}')
    if missing_course:
        print('⚠️ 树里挂了但 registry 里找不到的课件：', missing_course)

    if args.dry:
        print('（dry-run，未写入）')
        return 0
    UNIFIED.write_text(json.dumps(unified, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    NODE_INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('✅ 已写入 data/trees/cn-unified/info-tech.json 与 data/node-index.json')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
