#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把课标元信息更新到当前有效版本（并补上缺失的学科）。

依据（2026-10 核实）
-------------------
教育部 **教材〔2025〕1 号** 印发《义务教育、普通高中课程方案和课程标准**日常修订版**》，
标准全称变为：
  · 义教：`义务教育X课程标准（2022年版2025年修订）`
  · 高中：`普通高中X课程标准（2017年版2025年修订）`（此前是“2017年版2020年修订”）
来源：课程教材研究所各学科修订组解读（数学/物理/语文/生物/英语等）。

心理健康教育**没有国家课程标准**：依据是教育部《中小学心理健康教育指导纲要（2012年修订）》
（教基一〔2012〕15 号，2012-12-07 印发）。本脚本按“指导纲要（非课程标准）”标注，
不硬套课标名义。

本脚本只改 `metadata.curriculum` 的**版本字段**，不动节点与 `curriculum_points`：
内容点仍是原版摘录，因此另写 `grounded_on` / `standard_note` 说明摘录依据，
避免把旧版摘录误标成修订版原文。

用法:  python3 tools/update-curriculum-standard.py [--dry]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CN = ROOT / 'data' / 'trees' / 'cn'
STAGES = ['elementary', 'middle', 'high']

ZH = {
    'chinese': '语文', 'math': '数学', 'english': '英语', 'science': '科学',
    'physics': '物理', 'chemistry': '化学', 'biology': '生物学', 'geography': '地理',
    'history': '历史',
}
OVERRIDE = {('elementary', 'politics'): '道德与法治', ('middle', 'politics'): '道德与法治',
            ('high', 'politics'): '思想政治',
            ('elementary', 'info-tech'): '信息科技', ('middle', 'info-tech'): '信息科技',
            ('high', 'info-tech'): '信息技术'}
EN = {
    'chinese': 'Chinese Language', 'math': 'Math', 'english': 'English', 'science': 'Science',
    'physics': 'Physics', 'chemistry': 'Chemistry', 'biology': 'Biology', 'geography': 'Geography',
    'history': 'History', 'politics': 'Morality and Law', 'info-tech': 'Information Technology',
}
EN_HIGH_POL = 'Ideological and Political'
PSY_STD = '中小学心理健康教育指导纲要（2012年修订）'
PSY_EN = 'Guidelines for Mental Health Education in Primary and Secondary Schools (2012 rev.)'
NOTE = ('本树节点的 curriculum_points 摘录自 {on}；{cur} 属日常修订，'
        '内容框架与核心概念未变，个别表述与时代主题有更新，逐条核对修订版文本可作为后续工作。')


def target(stage: str, subj: str, old: str | None):
    """返回 (standard, standard_en, issued, kind, note_on) 或 None（不处理）。"""
    if subj == 'psychology':
        return PSY_STD, PSY_EN, '2012-12', '教育部指导纲要（非课程标准）', PSY_STD
    zh = OVERRIDE.get((stage, subj)) or ZH.get(subj)
    if not zh:
        return None
    if stage == 'high':
        en = EN_HIGH_POL if (subj == 'politics') else EN.get(subj, subj)
        std = f'普通高中{zh}课程标准（2017年版2025年修订）'
        en_std = f'Senior High {en} Curriculum Standard (2017, rev. 2025)'
        on = re.sub(r'（2017年版2025年修订）', '（2017年版2020年修订）', std)
        return std, en_std, '2025-12', '课程标准', on
    en = EN.get(subj, subj)
    std = f'义务教育{zh}课程标准（2022年版2025年修订）'
    en_std = f'Compulsory Education {en} Curriculum Standard (2022 ed., rev. 2025)'
    on = re.sub(r'（2022年版2025年修订）', '（2022年版）', std)
    return std, en_std, '2025-12', '课程标准', on


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()

    changed = []
    for stage in STAGES:
        d = CN / stage
        if not d.is_dir():
            continue
        for f in sorted(d.glob('*.json')):
            if f.name.startswith('_'):
                continue
            obj = json.loads(f.read_text(encoding='utf-8'))
            subj = f.stem
            meta = obj.setdefault('metadata', {})
            cur = meta.setdefault('curriculum', {})
            t = target(stage, subj, cur.get('standard'))
            if not t:
                print(f'  ↷ {stage}/{f.name}: 无对应课标（跳过）')
                continue
            std, en_std, issued, kind, on = t
            before = cur.get('standard')
            # 中/小学段共用一个义教标准，保留原有「· 初中学段」这类后缀
            suffix = ''
            if before:
                m = re.search(r'）(.*)$', before)
                suffix = (m.group(1) if m else '')
            if kind == '课程标准':
                note = NOTE.format(on=before or on, cur=std + suffix)
            else:
                note = ('心理健康教育没有国家课程标准，依据是 ' + std +
                        '；本树节点的 curriculum_points 摘录自该纲要，未套用课标名义。')
            cur.update({
                'standard': std + suffix,
                'standard_en': en_std + suffix,
                'source': cur.get('source') or '中华人民共和国教育部',
                'issued': issued,
                'standard_kind': kind,
                'standard_revision': '日常修订版（2025）' if kind == '课程标准' else '现行有效',
                'grounded_on': before or on,
                'standard_note': note,
            })
            if cur.get('standard') != before or not before:
                changed.append((f'{stage}/{f.name}', before, cur['standard']))
            meta['curriculum'] = cur
            if not args.dry:
                f.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print(f'\n{"（dry-run）" if args.dry else ""}更新 {len(changed)} 个树文件的课标元信息：')
    for name, before, after in changed:
        print(f'   {name:26} {before} → {after}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
