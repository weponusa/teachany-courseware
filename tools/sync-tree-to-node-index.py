#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把「分学段树 ↔ node-index」对齐，并清掉树里的失效课件引用。

做四件事
--------
A 树引用清理：删掉指向不存在目录的课件 id（历史导出残留）；
              删掉「manifest.node_id 与所在节点不一致」的课件（通常是跳转桩，
              它 redirect 到哪个节点就在哪个节点挂着，不该出现在别的节点下）。
B 索引回填：分学段树里有、node-index 里没有的节点，按已有节点的字段形状补进去
            （domain/curriculum/stage/subject/tree_path/courses/md_path/md_status/prereq_ids）。
C 重算 _meta 计数。
D 幂等：重复跑不产生重复节点。

为什么不用 scripts/sync-node-index-courses.py：那个只更新**已存在**节点的 courses，
不会新增节点（小学/初中信息科技就是这么漏掉的）。

用法:  python3 tools/sync-tree-to-node-index.py [--dry]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TREES = ROOT / 'data' / 'trees'
NODE_INDEX = ROOT / 'data' / 'node-index.json'
REGISTRY = ROOT / 'registry.json'
SITE = 'https://www.teachany.cn'
STAGES = ['elementary', 'middle', 'high']


def load(p: Path):
    return json.loads(p.read_text(encoding='utf-8'))


def cid_of(c):
    if isinstance(c, str):
        return c
    if isinstance(c, dict):
        return c.get('id') or c.get('course_id')
    return None


def course_dirs():
    out = set()
    for base in ('community', 'examples'):
        d = ROOT / base
        if d.is_dir():
            out |= {p.name for p in d.iterdir() if p.is_dir() and (p / 'manifest.json').is_file()}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()

    dirs = course_dirs()
    reg = {c['id']: c for c in load(REGISTRY).get('courses', [])}
    idx = load(NODE_INDEX)
    nodes = idx['nodes']

    dropped_missing, dropped_mismatch = [], []

    def node_manifest_nid(cid):
        for base in ('community', 'examples'):
            p = ROOT / base / cid / 'manifest.json'
            if p.is_file():
                return load(p).get('node_id')
        return None

    # ---------- A 清理树里的失效引用 ----------
    tree_files = [f for st in STAGES for f in sorted((TREES / 'cn' / st).glob('*.json'))
                  if not f.name.startswith('_')]
    tree_files += [f for f in sorted((TREES / 'cn-unified').glob('*.json')) if not f.name.startswith('_')]
    for f in tree_files:
        obj = load(f)
        touched = False
        for dom in obj.get('domains') or []:
            for n in dom.get('nodes') or []:
                nid = n.get('id')
                cs = n.get('courses') or []
                keep = []
                for c in cs:
                    cid = cid_of(c)
                    if not cid:
                        continue
                    if cid not in dirs:
                        dropped_missing.append({'树': str(f.relative_to(ROOT)), '节点': nid, '课件': cid, '原因': '目录不存在'})
                        touched = True
                        continue
                    mn = node_manifest_nid(cid)
                    if mn and nid and mn != nid:
                        dropped_mismatch.append({'树': str(f.relative_to(ROOT)), '节点': nid, '课件': cid,
                                                 'manifest.node_id': mn, '原因': '跳转桩/归属不符'})
                        touched = True
                        continue
                    keep.append(c)
                if touched:
                    n['courses'] = keep
        if touched and not args.dry:
            f.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # ---------- B 索引回填 ----------
    added = []
    for st in STAGES:
        d = TREES / 'cn' / st
        if not d.is_dir():
            continue
        for f in sorted(d.glob('*.json')):
            if f.name.startswith('_'):
                continue
            subj = f.stem
            obj = load(f)
            for dom in obj.get('domains') or []:
                for n in dom.get('nodes') or []:
                    nid = n.get('id')
                    if not nid or nid in nodes:
                        continue
                    courses = []
                    for c in n.get('courses') or []:
                        cid = cid_of(c)
                        if not cid:
                            continue
                        r = reg.get(cid, {})
                        path = (r.get('path') or f'community/{cid}').strip('/')
                        courses.append({'id': cid, 'name_zh': r.get('name') or cid,
                                        'download_url': f'{SITE}/{path}/'})
                    entry = {
                        'node_id': nid,
                        'name_zh': n.get('name') or n.get('name_zh') or '',
                        'name_en': n.get('name_en') or '',
                        'domain': dom.get('name') or '',
                        'curriculum': 'cn',
                        'stage': st,
                        'subject': subj,
                        'tree_path': f'cn/{st}/{f.name}',
                        'courses': courses,
                        'md_path': f'skill/data/kp-md/kp-{nid}.md',
                        'md_status': 'ready',
                    }
                    pre = [p for p in (n.get('prerequisites') or []) if isinstance(p, str) and p]
                    if pre:
                        entry['prereq_ids'] = pre
                    nodes[nid] = entry
                    added.append((nid, entry['name_zh'], st, subj, [c['id'] for c in courses]))

    # ---------- C 重算 _meta ----------
    m = idx.get('_meta', {})
    m['total_nodes'] = len(nodes)
    m['with_md'] = sum(1 for v in nodes.values() if v.get('md_status') == 'ready')
    m['with_hero'] = sum(1 for v in nodes.values() if v.get('hero_image'))
    m['with_prereq'] = sum(1 for v in nodes.values() if v.get('prereq_ids'))
    idx['_meta'] = m

    print(f'A 清理失效引用：目录不存在 {len(dropped_missing)} 条，归属不符 {len(dropped_mismatch)} 条')
    for x in dropped_missing:
        print('    ✗', json.dumps(x, ensure_ascii=False))
    for x in dropped_mismatch:
        print('    ✗', json.dumps(x, ensure_ascii=False))
    print(f'\nB 回填索引：新增 {len(added)} 个节点 → 总计 {len(nodes)}')
    for a in added[:12]:
        print('    +', a)
    if len(added) > 12:
        print(f'    …其余 {len(added) - 12}')
    print(f'\nC _meta: total={m["total_nodes"]} with_md={m["with_md"]} with_hero={m["with_hero"]} with_prereq={m["with_prereq"]}')

    if args.dry:
        print('\n（dry-run，未写入）')
        return 0
    NODE_INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('\n✅ 已写入 node-index.json（树文件已在 A 步就地清理）')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
