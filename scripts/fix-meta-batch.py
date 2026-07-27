#!/usr/bin/env python3
"""批量补齐课件 <head> 中的 teachany-* meta 标签（修复 #11/#13/#07）。

数据来源优先级：
1. 课件 manifest.json（node_id/subject/grade/domain/prerequisites/difficulty/author）
2. data/nodes-metadata.json 与 data/kp/<subject>/<node_id>.json（前置节点 id → 中文名）

只补缺，不覆盖已有标签。
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMUNITY = os.path.join(ROOT, 'community')

# ── 节点 id → 中文名 映射 ──
def load_node_names():
    names = {}
    # 1) data/kp/<subject>/<id>.json
    kp_root = os.path.join(ROOT, 'data', 'kp')
    for sub in os.listdir(kp_root):
        sub_dir = os.path.join(kp_root, sub)
        if not os.path.isdir(sub_dir) or sub.startswith('_'):
            continue
        for f in os.listdir(sub_dir):
            if not f.endswith('.json'):
                continue
            try:
                d = json.load(open(os.path.join(sub_dir, f), encoding='utf-8'))
                if d.get('kp_id') and d.get('name'):
                    names[d['kp_id']] = d['name']
            except Exception:
                pass
    # 2) nodes-metadata.json（递归收集含 id+name 的对象）
    nm_path = os.path.join(ROOT, 'data', 'nodes-metadata.json')
    if os.path.exists(nm_path):
        def walk(o):
            if isinstance(o, dict):
                if 'id' in o and 'name' in o and isinstance(o['name'], str):
                    names.setdefault(o['id'], o['name'])
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        try:
            walk(json.load(open(nm_path, encoding='utf-8')))
        except Exception as e:
            print('nodes-metadata parse warn:', e)
    # 3) trees json 同样递归收集
    trees_root = os.path.join(ROOT, 'data', 'trees')
    for dirpath, _, files in os.walk(trees_root):
        for f in files:
            if not f.endswith('.json'):
                continue
            try:
                def walk(o):
                    if isinstance(o, dict):
                        if 'id' in o and 'name' in o and isinstance(o['name'], str) and len(o['name']) < 60:
                            names.setdefault(o['id'], o['name'])
                        for v in o.values():
                            walk(v)
                    elif isinstance(o, list):
                        for v in o:
                            walk(v)
                walk(json.load(open(os.path.join(dirpath, f), encoding='utf-8')))
            except Exception:
                pass
    return names

META_RE = re.compile(r'<meta\s+name=["\'](teachany-[a-z-]+)["\'][^>]*>', re.I)

def existing_metas(html):
    return set(m.group(1).lower() for m in META_RE.finditer(html))

def resolve_prereq_names(ids, names):
    out = []
    for i in ids:
        if isinstance(i, dict):
            i = i.get('id') or i.get('node_id') or ''
        nm = names.get(i)
        out.append(nm if nm else str(i))
    return out

def fix_course(course_id, names, node_prereqs):
    cdir = os.path.join(COMMUNITY, course_id)
    mpath = os.path.join(cdir, 'manifest.json')
    hpath = os.path.join(cdir, 'index.html')
    if not os.path.exists(hpath):
        return None
    manifest = {}
    if os.path.exists(mpath):
        try:
            manifest = json.load(open(mpath, encoding='utf-8'))
        except Exception:
            pass
    html = open(hpath, encoding='utf-8').read()
    have = existing_metas(html)

    node_id = manifest.get('node_id') or manifest.get('nodeId') or ''
    subject = manifest.get('subject') or ''
    grade = manifest.get('grade')
    stage = manifest.get('stage') or ''
    domain = manifest.get('domain') or ''
    version = manifest.get('teachany_version') or ('v' + str(manifest.get('version', '1.0.0')))
    difficulty = manifest.get('difficulty') or ''
    author = manifest.get('author') or ''

    # 前置知识：manifest.prerequisites → 节点自身 prerequisites → 空
    pre_ids = manifest.get('prerequisites') or []
    if not pre_ids and node_id:
        pre_ids = node_prereqs.get(node_id) or []
    pre_names = resolve_prereq_names(pre_ids, names)
    pre_content = '、'.join(pre_names) if pre_names else '本课为起点内容，无前置知识要求'

    want = {
        'teachany-node': node_id,
        'teachany-subject': subject,
        'teachany-grade': str(grade) if grade not in (None, '') else '',
        'teachany-stage': stage,
        'teachany-domain': domain,
        'teachany-version': version if str(version).startswith('v') else 'v' + str(version),
        'teachany-prerequisites': pre_content,
        'teachany-difficulty': str(difficulty) if difficulty != '' else '',
        'teachany-author': author,
    }
    to_add = [(k, v) for k, v in want.items() if k not in have and v]
    if 'teachany-prerequisites' not in have and ('teachany-prerequisites', pre_content) not in to_add:
        to_add.append(('teachany-prerequisites', pre_content))
    if not to_add:
        return False

    block = ''.join(f'  <meta name="{k}" content="{v}">\n' for k, v in to_add)
    # 插入到最后一个 teachany meta 之后；否则 </head> 之前
    matches = list(META_RE.finditer(html))
    if matches:
        pos = matches[-1].end()
        html = html[:pos] + '\n' + block.rstrip('\n') + html[pos:]
    else:
        html = html.replace('</head>', block + '</head>', 1)
    open(hpath, 'w', encoding='utf-8').write(html)
    return True

def main():
    report = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
    targets = [r['id'] for r in report if any(
        x.startswith('#11') or x.startswith('#13') or x.startswith('#07') for x in r['failed'])]
    print(f'targets: {len(targets)}')
    names = load_node_names()
    print(f'node names: {len(names)}')
    # 节点自身 prerequisites（用于 manifest 缺省时兜底）
    node_prereqs = {}
    nm_path = os.path.join(ROOT, 'data', 'nodes-metadata.json')
    if os.path.exists(nm_path):
        def walk(o):
            if isinstance(o, dict):
                if 'id' in o and isinstance(o.get('prerequisites'), list):
                    node_prereqs.setdefault(o['id'], o['prerequisites'])
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        try:
            walk(json.load(open(nm_path, encoding='utf-8')))
        except Exception:
            pass
    fixed, skipped = 0, 0
    for cid in targets:
        r = fix_course(cid, names, node_prereqs)
        if r:
            fixed += 1
        else:
            skipped += 1
    print(f'fixed: {fixed}, skipped(no-change): {skipped}')

if __name__ == '__main__':
    main()
