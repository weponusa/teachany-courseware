#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build-nodes-selector.py
========================
从权威数据源（data/trees/**/*.json）重建 path.html（学习路径页）使用的
data/nodes-selector.json 快照。

背景：path.html 的学科/年级筛选器依赖 data/nodes-selector.json，历史上
是手工维护的 2026-04-17 旧快照，rebuild-index 未自动维护导致：
    - 新增/修改的知识点（特别是 cn/middle/*）不会出现在选择器
    - 用户选择"地理 · 初中"时出现"该学科/年级暂无知识点"

输出格式（兼容 path.html 现有读取逻辑）：
    [
      {"id": "...", "name": "...", "subject": "...", "grade": N, "domain": "..."},
      ...
    ]

学科白名单：math/chinese/physics/biology/english/chemistry/history/geography/info-tech/science/politics/psychology
年级约定：1-6 = 小学；7-9 = 初中；10-12 = 高中；0 = 通识
"""
import json
import sys
from pathlib import Path
from collections import Counter

REPO_ROOT = Path(__file__).resolve().parent.parent
TREES_DIR = REPO_ROOT / 'data' / 'trees'
OUT_FILE = REPO_ROOT / 'data' / 'nodes-selector.json'

# path.html 的 subject 筛选下拉只接受这几个代码
VALID_SUBJECTS = {
    'math', 'chinese', 'physics', 'biology', 'english',
    'chemistry', 'history', 'geography', 'info-tech',
    'science',  # K5 科学综合
    'politics', 'psychology',
    'ela',      # 英语语言艺术（美式）
}

SYSTEM_LABELS = {
    'cn': '中国课标',
    'cn-unified': '中国课标',
    'cambridge': 'Cambridge',
    'ib': 'IB',
    'us': 'US CCSS',
    'ap': 'AP',
    'other': '其他',
}


def load_json(p: Path):
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        print(f'  ⚠️  读取失败 {p.relative_to(REPO_ROOT)}: {e}', file=sys.stderr)
        return None


def infer_subject(tree_data: dict, tree_path: Path) -> str:
    """优先用 tree.subject，否则从文件路径推断（如 cn/middle/geography.json → geography）"""
    subj = tree_data.get('subject')
    if subj:
        return subj
    return tree_path.stem  # 文件名去扩展


def infer_system(tree_path: Path) -> str:
    try:
        rel = tree_path.relative_to(TREES_DIR)
    except ValueError:
        return 'other'
    parts = rel.parts
    return parts[0] if parts else 'other'


def infer_curriculum_label(system: str, tree_path: Path) -> str:
    path = str(tree_path).replace('\\', '/').lower()
    if system in ('cn', 'cn-unified'):
        return '中国课标'
    if system == 'cambridge':
        if '/primary/' in path:
            return 'Cambridge Primary'
        if '/lsec/' in path:
            return 'Cambridge Lower Secondary'
        if '/igcse/' in path:
            return 'Cambridge IGCSE'
        if '/al/' in path:
            return 'Cambridge A Level'
        return 'Cambridge'
    if system == 'ib':
        if '/pyp/' in path:
            return 'IB PYP'
        if '/myp/' in path:
            return 'IB MYP'
        if '/dp/' in path:
            return 'IB DP'
        return 'IB'
    return SYSTEM_LABELS.get(system, system)


def format_grade_label(grade: int, system: str, tree_path: Path) -> str:
    path = str(tree_path).replace('\\', '/').lower()
    if grade <= 0:
        if 'university' in path or 'college' in path:
            return '大学'
        return '通识'
    if system in ('cn', 'cn-unified'):
        if grade <= 6:
            return f'小学{grade}年级'
        if grade <= 9:
            return f'初中{grade - 6}年级'
        return f'高中{grade - 9}年级'
    if 'primary' in path or 'elementary' in path or 'pyp' in path:
        return f'Primary G{grade}' if grade <= 6 else f'G{grade}'
    if 'middle' in path or 'myp' in path or 'lsec' in path:
        return f'Middle G{grade}'
    if 'high' in path or 'igcse' in path or 'dp' in path or 'ap' in path:
        return f'High G{grade}'
    return f'G{grade}'


def extract_nodes(tree_data: dict, default_subject: str, tree_path: Path):
    """从一棵知识树的 domains[*].nodes[*] 中抽取节点"""
    system = infer_system(tree_path)
    curriculum_label = infer_curriculum_label(system, tree_path)
    out = []
    for dom in tree_data.get('domains', []) or []:
        domain_id = dom.get('id') or dom.get('slug') or ''
        for n in dom.get('nodes', []) or []:
            nid = n.get('id')
            name = n.get('name') or n.get('title')
            if not nid or not name:
                continue
            grade = n.get('grade')
            # 兼容 grade 为字符串的数据
            if isinstance(grade, str):
                try:
                    grade = int(grade)
                except ValueError:
                    grade = 0
            if grade is None:
                grade = 0
            subj = n.get('subject') or default_subject
            out.append({
                'id': nid,
                'name': name,
                'subject': subj,
                'grade': grade,
                'domain': domain_id,
                'system': system,
                'curriculumLabel': curriculum_label,
                'gradeLabel': format_grade_label(grade, system, tree_path),
                'treePath': str(tree_path.relative_to(TREES_DIR)).replace('\\', '/'),
            })
    return out


def main():
    if not TREES_DIR.exists():
        print(f'❌ 未找到 {TREES_DIR}', file=sys.stderr)
        sys.exit(1)

    all_nodes = []
    seen_ids = set()
    dup_count = 0
    trees_seen = 0

    for tree_path in sorted(TREES_DIR.rglob('*.json')):
        # 跳过 other/user-generated.json（由 rebuild-index 填充，且都是课件而非知识点）
        if tree_path.name in ('_template.json',):
            continue
        tree_data = load_json(tree_path)
        if not isinstance(tree_data, dict):
            continue
        subj = infer_subject(tree_data, tree_path)
        nodes = extract_nodes(tree_data, subj, tree_path)
        if not nodes:
            continue
        trees_seen += 1
        for n in nodes:
            if n['id'] in seen_ids:
                dup_count += 1
                continue
            seen_ids.add(n['id'])
            all_nodes.append(n)

    # 排序：中国课标优先，再 subject / grade / name（避免同名国际节点排在前面）
    system_rank = {'cn': 0, 'cn-unified': 1, 'cambridge': 2, 'ib': 3, 'us': 4, 'ap': 5}
    all_nodes.sort(key=lambda x: (
        x['subject'],
        x['grade'],
        x['name'],
        system_rank.get(x.get('system'), 9),
        x['id'],
    ))

    OUT_FILE.write_text(
        json.dumps(all_nodes, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

    # 统计
    by_subj = Counter(n['subject'] for n in all_nodes)
    geo_middle = sum(1 for n in all_nodes if n['subject'] == 'geography' and 7 <= n.get('grade', 0) <= 9)

    print(f'✅ nodes-selector.json 已重建：共 {len(all_nodes)} 个节点（覆盖 {trees_seen} 棵知识树，去重 {dup_count} 个）')
    print(f'   按学科：', end='')
    print(', '.join(f'{s}={c}' for s, c in by_subj.most_common()))
    print(f'   抽检 · 地理初中(7-9年级)：{geo_middle} 个节点')


if __name__ == '__main__':
    main()
