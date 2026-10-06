# 学科知识文件格式与知识量平衡性审计

生成时间：2026-06-02 09:27

## 结论

中国课标知识点文件整体已经可用，格式主干基本统一，但仍存在“字段齐全度统一、内容量不均衡、deep 来源类型差异大”的问题。

- 中国课标节点总数：`866`
- 基础知识内容缺失：`0`
- deep 覆盖：`815/866`，覆盖率 `94.1%`
- 主要缺口集中在历史类节点，本报告只做结构统计，不展开历史内容。
- 非历史学科 deep 已全覆盖。

## 一、格式统一性

### 1. 主干字段基本统一

绝大多数字段都已统一存在：

- `kp_id`
- `name`
- `subject`
- `subject_name`
- `curriculum`
- `stage`
- `grade`
- `domain_id`
- `domain_name`
- `tree_file`
- `curriculum_points`
- `excerpts`
- `interactive_resources`
- `supplements`
- `errors`
- `exercises`
- `real_world`
- `_meta`

按必备字段统计，除两个特殊情况外，主干格式一致。

### 2. 仍有少量字段缺失

| 学科 | 缺失情况 |
|---|---|
| biology | 无 |
| chemistry | 无 |
| chinese | 无 |
| english | 无 |
| geography | 无 |
| info-tech | 无 |
| math | 无 |
| physics | 无 |
| science | 无 |
| history | `interactive_resources` 缺 1 个 |
| other | `curriculum`、`stage`、`interactive_resources` 各缺 1 个 |

`other` 实际是一个用户生成语文课件节点，建议后续归并到 `chinese` 或补齐 `curriculum=cn`、`stage=elementary`。

### 3. 可选字段不统一但可接受

以下字段是可选历史遗留字段，不要求所有文件都有：

- `textbook_chapter`
- `textbook_semester`
- `chapter_source`
- `courseVersion`
- `course_variants`
- `siblings`
- `excerpt_ids`

这些字段不统一不影响 KCP 使用，但建议未来迁移到统一的 `supplements.references` 或 `_meta.legacy_fields`。

## 二、知识量平衡性

| 学科 | 节点数 | 平均课标点 | 平均摘录 | 平均习题 | 平均易错 | 平均 deep 条数 | 平均 MD 字数 | 平均 deep 字数 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| biology | 103 | 2.8 | 36.4 | 2.0 | 2.0 | 3.9 | 1227.5 | 5212.9 |
| chemistry | 83 | 2.6 | 43.0 | 2.0 | 2.0 | 3.8 | 1351.0 | 4970.9 |
| chinese | 130 | 2.6 | 4.2 | 2.0 | 2.0 | 2.0 | 1462.3 | 242.8 |
| english | 82 | 2.9 | 11.6 | 2.0 | 2.0 | 1.9 | 1235.7 | 2253.6 |
| geography | 72 | 2.7 | 7.5 | 2.0 | 2.0 | 2.2 | 1220.7 | 1972.2 |
| history | 87 | 2.6 | 24.4 | 2.0 | 2.0 | 1.3 | 1273.4 | 1666.5 |
| info-tech | 10 | 2.8 | 2.8 | 2.0 | 2.0 | 2.9 | 1100.7 | 4300.1 |
| math | 154 | 2.9 | 6.1 | 2.8 | 2.2 | 3.6 | 2108.2 | 5278.5 |
| other | 1 | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 | 1305.0 | 283.0 |
| physics | 96 | 2.6 | 24.9 | 2.0 | 2.0 | 3.6 | 1559.4 | 4802.7 |
| science | 48 | 2.5 | 2.4 | 2.0 | 2.0 | 4.0 | 922.4 | 6140.1 |

## 三、平衡性判断

### 1. 基础层基本平衡

基础字段层面已经比较平衡：

- 每科平均课标点约 `2.5–2.9` 条。
- 每科习题基本为 `2` 条，数学略高，为 `2.8`。
- 每科易错点基本为 `2` 条。
- `real_world` 也已经至少有 1 条。

这说明基础 KCP 可用性已经比较稳定。

### 2. deep 内容量不平衡

差异主要体现在 deep 字数和来源类型：

- `science`、`math`、`biology`、`chemistry`、`physics` deep 字数明显较高，平均约 `4800–6100` 字。
- `english`、`geography` 中等，平均约 `1900–2200` 字。
- `chinese` 明显偏低，平均约 `243` 字，因为当前主要来自 `curated_subject_pack`，不是长篇教材/原文。
- `history` 仍未全覆盖，平均 deep 条数偏低。

### 3. 来源类型差异较大

| 学科 | 主要 deep 来源类型 |
|---|---|
| math | `local_textbook_markdown` 为主，少量 pack/OER |
| physics | `local_textbook_markdown` + `existing_textbook_excerpt` |
| chemistry | `existing_textbook_excerpt` + `local_textbook_markdown` |
| biology | `existing_textbook_excerpt` + `local_textbook_markdown` |
| science | `local_textbook_markdown` |
| info-tech | `local_oer_curriculum_md` |
| english | `local_oer_curriculum_md` + `curated_subject_pack` |
| geography | `local_oer_curriculum_md` + `curated_subject_pack` |
| chinese | 几乎全是 `curated_subject_pack` |

这说明：STEM 更像“教材片段库”，语文更像“技能资料包”。两者用途不同，不能简单按字数比较。

## 四、主要问题

### 问题 1：语文 deep 字数偏少

语文已全覆盖，但多数是短资料包片段，不是篇目原文或阅读材料。适合作为教学支架，不足以作为“教材文本”。

建议后续接入：

- `chinese-poetry`
- 维基文库公版文本
- 自建短文阅读材料库
- 写作范例库

### 问题 2：地理和英语部分内容是任务型资料，不是教材正文

这类内容可用于课件活动设计，但若要“教材感”，还需要：

- 地理地图案例、区域案例、数据图表
- 英语例句、短对话、短文、语法结构表

### 问题 3：历史 deep 覆盖不足

历史仍有 `51` 个节点无 deep，当前仅保留基础知识层和审计信息。建议只做人工审核来源，不自动灌正文。

### 问题 4：少量格式字段仍需补齐

建议补齐：

- 历史 1 个节点的 `interactive_resources`
- `other` 节点的 `curriculum`、`stage`、`interactive_resources`

## 五、建议统一规范

建议把每个知识点的最低标准定为：

```json
{
  "curriculum_points": ">=2",
  "excerpts": ">=2",
  "exercises": ">=2",
  "errors": ">=2",
  "real_world": ">=1",
  "supplements.curriculum_md_raw": "存在",
  "supplements.textbook_summary": "存在",
  "supplements.deep_textbook_snippets": "非历史学科 >=1，历史人工审核",
  "interactive_resources": "建议 >=1"
}
```

建议新增统一字段：

```json
"quality": {
  "baseline_complete": true,
  "deep_coverage": true,
  "deep_source_type": "local_textbook_markdown | curated_subject_pack | local_oer_curriculum_md",
  "needs_human_review": false
}
```

## 六、结论

- **格式统一性：8.5/10**。主干字段已经统一，少量遗留字段不一致。
- **基础知识量平衡：8/10**。每科课标、习题、易错、教学建议基本平衡。
- **deep 知识量平衡：6.5/10**。STEM 较丰富，语文偏短，历史未全覆盖。
- **可用于课件生成：8/10**。KCP 已能读取 deep，非历史学科可用。
- **可称为高质量教材知识库：仍需人工抽检与语文/地理/英语专用资料增强。**
