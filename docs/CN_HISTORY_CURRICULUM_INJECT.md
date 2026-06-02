# 中国史课标知识灌注说明

## 目标

为 `data/kp/history/*.json` 与 `community/*/knowledge-context.json` 提供**符合国家课标与统编教材口径**的知识上下文，避免：

- OCR 前言、修订说明等非教学内容灌入
- 西方中心论或与课标主线相悖的表述
- 传说与考古结论混同、割裂民族史与边疆史

## 数据源（优先级）

1. **树节点 `curriculum_points`** — 普高/义教内容要求（权威，与教材一致）
2. **义务教育历史课程标准（2022年版）** — `books/课标-整理版/cn/middle/history.md`
   - 中国古代史 1.1–1.7、学业要求、教学提示
   - 中国近代史、世界古代史总述
3. **普通高中历史课程标准（2017年版2020年修订）** — 树课标点为主（整理版 OCR 不全）

## 脚本

```bash
# 灌注全部历史卫星
python3 scripts/inject-cn-history-curriculum.py

# 并重新生成 community 历史课 KCP
python3 scripts/inject-cn-history-curriculum.py --re-emit-kcp
```

## 卫星字段

| 字段 | 含义 |
|------|------|
| `excerpts` | 以课标「内容要求」句为主，`source: 国家课标·内容要求` |
| `textbook_content.values_framework` | 核心素养与价值导向（古代/近代/世界分轨） |
| `textbook_content.teaching_guidance` | 义教课标教学提示摘录 |
| `textbook_content.textbook_alignment` | 与统编《中国历史》《世界历史》叙事对齐说明 |
| `exercises` | 【课标探究】口吻，强调史料类型与统一多民族国家线索 |
| `errors` | 常见违背课标口径的误区（分古代/近代/世界） |

## 分轨

- **ancient** — `domain_id` 含 `ancient-china`：统一多民族国家、考古实证、中华民族共同体
- **modern** — 近代史节点：反帝反封建、民族独立、中国共产党领导革命
- **world** — `domain_id` 含 `world`：文明多元、区域互动，避免西方中心论

## 与 Stage7 关系

`kp-md-pipeline/stage7_textbook_inject.py` 对 **history/cn** 仅作关键词兜底；**正式灌注请用本脚本**。
