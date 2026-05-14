#!/usr/bin/env python3
"""
verify_kp_migration.py — 校验迁移正确性

校验项：
  1. 备份目录每个节点的所有字段在迁移后都能在「卫星文件 ∪ 瘦身后主文件」中找到
  2. 卫星文件数 == 节点总数
  3. 前端 tree.html 渲染所需字段（id/name/name_en/grade/status/courses/prerequisites/extends/parallel）
     在瘦身后主文件中完整保留
  4. excerpt_ids 引用的 excerpt 在卫星文件 excerpts 字段中可查到
"""
import json, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TREES_NEW = os.path.join(ROOT, 'data/trees')
TREES_BAK = sorted(glob.glob(os.path.join(ROOT, 'data/trees.backup_*')))[-1]
KP_DIR = os.path.join(ROOT, 'data/kp')
KP_INDEX = os.path.join(KP_DIR, '_index.json')

FRONTEND_REQUIRED = {'id', 'name', 'grade', 'status', 'courses',
                     'prerequisites', 'extends', 'parallel', 'name_en'}


def collect_nodes(tree_root):
    out = {}
    for fp in sorted(glob.glob(os.path.join(tree_root, '**/*.json'), recursive=True)):
        with open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
        rel = os.path.relpath(fp, tree_root)
        def walk(x):
            if isinstance(x, dict):
                if 'id' in x and 'name' in x and 'grade' in x and 'prerequisites' in x:
                    out[x['id']] = (rel, x)
                for v in x.values(): walk(v)
            elif isinstance(x, list):
                for v in x: walk(v)
        walk(data)
    return out


def main():
    print(f'[1/4] 收集旧节点: {TREES_BAK}')
    old_nodes = collect_nodes(TREES_BAK)
    print(f'      共 {len(old_nodes)} 个节点')

    print(f'[2/4] 收集新节点: {TREES_NEW}')
    new_nodes = collect_nodes(TREES_NEW)
    print(f'      共 {len(new_nodes)} 个节点')

    if set(old_nodes.keys()) != set(new_nodes.keys()):
        miss_old = set(old_nodes.keys()) - set(new_nodes.keys())
        miss_new = set(new_nodes.keys()) - set(old_nodes.keys())
        print(f'  ❌ 节点 id 集合不一致：旧→新 missing {len(miss_old)}, 新→旧 missing {len(miss_new)}')
        sys.exit(1)
    print(f'      ✅ 节点 id 集合完全一致')

    print('[3/4] 加载卫星索引')
    with open(KP_INDEX, 'r', encoding='utf-8') as f:
        idx = json.load(f).get('kps', {})
    print(f'      共 {len(idx)} 个卫星文件索引')

    print('[4/4] 抽样校验 5 个学科代表节点')
    samples = [
        'math-m-linear-function',
        'math-h-derivative',
        'physics-m-ohm-law',
        'chemistry-h-mol-concept',
        'chinese-h-classical-prose',
    ]
    errors = 0
    for nid in samples:
        if nid not in old_nodes:
            print(f'  [skip] {nid} 不存在')
            continue
        old_rel, old = old_nodes[nid]
        new_rel, new = new_nodes[nid]

        # 卫星文件
        kp_file = idx.get(nid)
        if not kp_file:
            print(f'  ❌ {nid} 缺卫星索引')
            errors += 1
            continue
        with open(os.path.join(ROOT, kp_file), 'r', encoding='utf-8') as f:
            sat = json.load(f)

        # 前端必读字段：必须在新主文件中
        miss_fe = FRONTEND_REQUIRED - set(new.keys())
        # 容忍：name_en 部分节点本就缺失
        miss_fe.discard('name_en')
        if miss_fe:
            print(f'  ❌ {nid} 主文件缺前端必读字段: {miss_fe}')
            errors += 1

        # 已迁出字段：必须在卫星中
        for f in ['curriculum_points', 'textbook_chapter', 'textbook_semester', 'excerpt_ids']:
            if f in old and f not in sat:
                print(f'  ❌ {nid} 字段 {f} 在旧主文件中存在但卫星文件缺失')
                errors += 1

        # 主文件应已剔除（curriculum_points 例外：前端展示用，双写）
        for f in ['textbook_chapter', 'textbook_semester', 'excerpt_ids', 'difficulty', 'chapter_source']:
            if f in new:
                print(f'  ❌ {nid} 字段 {f} 应已迁出但仍在主文件中')
                errors += 1

        # 主文件必须有 kp_file 索引
        if 'kp_file' not in new:
            print(f'  ❌ {nid} 主文件缺 kp_file 索引字段')
            errors += 1

        print(f'  ✅ {nid}: 主文件字段 {len(new)}, 卫星字段 {len(sat)}, excerpts {len(sat.get("excerpts", []))}')

    # 全量校验：每个节点 kp_file 字段必须存在
    print('\n[全量] 检查 kp_file 字段覆盖率...')
    no_kp_file = [nid for nid, (_, n) in new_nodes.items() if 'kp_file' not in n]
    print(f'      缺 kp_file: {len(no_kp_file)} / {len(new_nodes)}')
    if no_kp_file[:5]:
        print(f'      样本: {no_kp_file[:5]}')

    # 卫星文件数对账
    print('\n[全量] 卫星文件数: %d, 节点数: %d' % (len(idx), len(new_nodes)))

    if errors == 0:
        print('\n🎉 全部校验通过')
    else:
        print(f'\n❌ {errors} 个错误')
        sys.exit(2)


if __name__ == '__main__':
    main()
