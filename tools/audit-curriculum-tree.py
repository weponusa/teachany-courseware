#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""课标 · 知识树 · 课件 三方一致性体检。

为什么需要
----------
「课件有没有、学生点不点得到」由四处共同决定（详见 skill §2m）：
  tree.html 学科清单 → 分学段树 data/trees/cn/<stage>/<subject>.json
  → 统一树 data/trees/cn-unified/<subject>.json → node-index.json
任何一处没跟上，就会出现「课件存在但知识地图上找不到」（2026-10-02 小学/初中信息科技就是这样）。

检查项
------
A 清单一致性：tree.html 列的分学段树 vs 磁盘实际文件（缺列 / 多列 / 死链）
B 统一树同步：cn-unified 是否覆盖三学段、节点集是否等于各学段之并
C 节点索引：分学段树节点是否都在 node-index 里
D 挂载一致性：树节点 courses ↔ 课件目录 ↔ manifest.node_id 回指（悬空 / 错配）
E 覆盖缺口：K12 节点没有课件的清单
F 课标对齐：节点缺 curriculum_points 的清单；metadata.curriculum.standard 版本分布
G 反向孤儿：有课件目录但没有任何节点挂载它

用法:  python3 tools/audit-curriculum-tree.py [--json /tmp/report.json]
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TREES = ROOT / 'data' / 'trees'
UNIFIED = TREES / 'cn-unified'
NODE_INDEX = ROOT / 'data' / 'node-index.json'
REGISTRY = ROOT / 'registry.json'
STAGES = ['elementary', 'middle', 'high']


def load(p: Path):
    return json.loads(p.read_text(encoding='utf-8'))


def cid_of(c):
    """courses 项可能是字符串，也可能是 {id,title,path,...} 字典（历史格式）。"""
    if isinstance(c, str):
        return c
    if isinstance(c, dict):
        return c.get('id') or c.get('course_id')
    return None


def tree_nodes(obj):
    """从树 dict 里取 [(domain, node)]。"""
    out = []
    if isinstance(obj, dict):
        for dom in obj.get('domains') or []:
            if not isinstance(dom, dict):
                continue
            for n in dom.get('nodes') or []:
                if isinstance(n, dict) and n.get('id'):
                    out.append((dom, n))
    return out


def course_dirs():
    out = {}
    for base in ('community', 'examples'):
        d = ROOT / base
        if not d.is_dir():
            continue
        for p in d.iterdir():
            if p.is_dir() and (p / 'manifest.json').is_file():
                out[p.name] = f'{base}/{p.name}'
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', default='')
    args = ap.parse_args()
    report = {}

    # ---- 载入 ----
    stage_files = {}
    stage_nodes = {}          # (stage, subject) -> {node_id: node}
    stage_meta = {}
    for st in STAGES:
        d = TREES / 'cn' / st
        if not d.is_dir():
            continue
        for f in sorted(d.glob('*.json')):
            if f.name.startswith('_'):
                continue
            obj = load(f)
            pairs = tree_nodes(obj)
            stage_files[(st, f.stem)] = f
            stage_nodes[(st, f.stem)] = {n['id']: n for _dom, n in pairs}
            stage_meta[(st, f.stem)] = (obj.get('metadata') or {}).get('curriculum') or {}

    unified_nodes = {}
    for f in sorted(UNIFIED.glob('*.json')):
        if f.name.startswith('_'):
            continue
        obj = load(f)
        unified_nodes[f.stem] = {n['id']: n for _dom, n in tree_nodes(obj)}
    unified_raw = {f.stem: obj for f in sorted(UNIFIED.glob('*.json')) if not f.name.startswith('_')
                   for obj in [load(f)]}

    idx = load(NODE_INDEX)
    idx_nodes = idx['nodes']
    idx_meta = idx.get('_meta', {})
    reg = {c['id']: c for c in load(REGISTRY).get('courses', [])}
    dirs = course_dirs()

    # ---- A 清单一致性 ----
    html = (ROOT / 'tree.html').read_text(encoding='utf-8')
    listed = {re.sub(r'\.json$', '', x) for x in re.findall(r"file:\s*'data/trees/([^']+)'", html)}
    actual = {f'cn/{st}/{sub}' for (st, sub) in stage_files}
    a = {
        'html_未列出的树文件': sorted(actual - listed),
        'html_列了但文件不存在': sorted(listed - actual),
        'html_条目数': len(listed), '树文件数': len(actual),
    }

    # ---- B 统一树同步 ----
    b = []
    subjects = sorted({sub for _st, sub in stage_files})
    for sub in subjects:
        sts = [st for st in STAGES if (st, sub) in stage_nodes]
        sum_nodes = sum(len(stage_nodes[(st, sub)]) for st in sts)
        u = unified_nodes.get(sub)
        obj = unified_raw.get(sub) or {}
        if u is None:
            b.append({'subject': sub, 'stages': sts, '问题': 'cn-unified 缺该学科文件'})
            continue
        cov = obj.get('stage_coverage') or []
        merged = (obj.get('_meta') or {}).get('merged_from') or []
        union_ids = set()
        for st in sts:
            union_ids |= set(stage_nodes[(st, sub)])
        missing = sorted(union_ids - set(u))
        extra = sorted(set(u) - union_ids)
        if missing or extra or set(cov) != set(sts) or len(u) != len(union_ids):
            b.append({'subject': sub, 'stages': sts, 'unified节点': len(u), '应为': len(union_ids),
                      'stage_coverage': cov, 'merged_from': merged,
                      '缺节点': missing[:8], '多节点': extra[:8],
                      '缺节点数': len(missing)})

    # ---- C 节点索引 ----
    tree_all = {nid: (st, sub) for (st, sub), m in stage_nodes.items() for nid in m}
    c_nodes = sorted(nid for nid in tree_all if nid not in idx_nodes)

    # ---- D 挂载一致性 ----
    dangling, mismatch = [], []
    for (st, sub), m in stage_nodes.items():
        for nid, node in m.items():
            for cid in (cid_of(c) for c in (node.get('courses') or [])):
                if not cid:
                    continue
                if cid not in dirs:
                    dangling.append({'node': nid, 'course': cid, '所在': f'{st}/{sub}'})
                    continue
                mf = ROOT / dirs[cid] / 'manifest.json'
                try:
                    mn = load(mf).get('node_id')
                except Exception:
                    mn = None
                if mn and mn != nid:
                    mismatch.append({'node': nid, 'course': cid, 'manifest.node_id': mn})

    # ---- E 覆盖缺口（K12 口径）----
    mounted = {cid for m in stage_nodes.values() for n in m.values()
               for cid in (cid_of(c) for c in (n.get('courses') or [])) if cid}
    mounted |= {cid for m in unified_nodes.values() for n in m.values()
                for cid in (cid_of(c) for c in (n.get('courses') or [])) if cid}
    k12 = {nid: (st, sub, n) for (st, sub), m in stage_nodes.items() for nid, n in m.items()}
    gaps = sorted(nid for nid, (_st, _sub, n) in k12.items()
                  if not [c for c in (cid_of(x) for x in (n.get('courses') or [])) if c])

    # ---- F 课标对齐 ----
    no_cp = sorted(nid for nid, (_st, _sub, n) in k12.items() if not (n.get('curriculum_points') or []))
    std = collections.Counter()
    for (st, sub), meta in stage_meta.items():
        std[str((meta or {}).get('standard') or '(缺 standard 字段)')] += 1

    # ---- G 反向孤儿 ----
    # 注意：挂在 other/（用户生成·拓展）与 ap/ib/cambridge/us 树上的课件**不算孤儿**；
    # 跳转桩目录（redirect stub）也不该出现在树里。两者都要排除。
    all_tree_mounts = set()
    for tf in TREES.rglob('*.json'):
        if tf.name.startswith('_'):
            continue
        try:
            o = load(tf)
        except Exception:
            continue
        for _dom, nd in tree_nodes(o):
            for _cid in (cid_of(x) for x in (nd.get('courses') or [])):
                if _cid:
                    all_tree_mounts.add(_cid)

    def is_stub(name: str) -> bool:
        for base in ('community', 'examples'):
            p = ROOT / base / name / 'index.html'
            if p.is_file():
                t = p.read_text(encoding='utf-8', errors='ignore')
                return bool(re.search(r'http-equiv="refresh"|location\.replace', t)) and 'teachany.cn' in t
        return False

    unmounted = sorted(d for d in dirs
                       if d not in all_tree_mounts and not is_stub(d))

    report = {
        'A_清单一致性': a,
        'B_统一树未同步': b,
        'C_不在节点索引的树节点': c_nodes,
        'D_悬空课件引用': dangling,
        'D_manifest与节点不一致': mismatch,
        'E_无课件的K12节点': gaps,
        'F_缺课标原文的节点': no_cp,
        'F_课标版本分布': dict(std),
        'G_未挂树的课件目录': unmounted,
        '规模': {'分学段树节点': len(tree_all), 'cn-unified学科': len(unified_nodes),
                 'node-index节点': len(idx_nodes), '课件目录': len(dirs)},
    }

    def p(k, v, limit=10):
        n = len(v) if isinstance(v, (list, dict)) else v
        print(f'\n### {k}  → {n}')
        if isinstance(v, list):
            for x in v[:limit]:
                print('   ', json.dumps(x, ensure_ascii=False) if not isinstance(x, str) else x)
            if len(v) > limit:
                print(f'    …其余 {len(v) - limit}')

    print('规模：', json.dumps(report['规模'], ensure_ascii=False))
    p('A 清单一致性（明细）', a)
    p('B 统一树未同步', b)
    p('C 不在节点索引的树节点', c_nodes)
    p('D 悬空课件引用', dangling)
    p('D manifest 与节点不一致', mismatch)
    p('E 无课件的 K12 节点', gaps)
    p('F 缺课标原文的节点', no_cp)
    print('\n### F 课标版本分布')
    for k, v in std.most_common():
        print(f'    {v:4d}  {k}')
    p('G 未挂树的课件目录', unmounted, limit=60)

    if args.json:
        Path(args.json).write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
        print('\n→', args.json)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
