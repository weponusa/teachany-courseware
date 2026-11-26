# NOTICE — GitHub 开源知识图谱与题库增强层

本目录是 TeachAny 知识图谱与题库的**旁挂增强层**，用于公开发布场景。遵循 `data/external/cn-math-taxonomy/NOTICE.md` 确立的同一套红线。

## 数据来源与授权

| 源 | 内容 | 授权 | 本目录使用方式 |
|:---|:---|:---|:---|
| [Open Knowledge Graph](https://github.com/open-knowledge-graph/okg) | 15,290 个概念、19 学科；YAML frontmatter 中的 hard/soft 前置关系；每个主题的 Questions 段 | **CC BY-SA 4.0**（内容）/ MIT（工具） | 概念索引、候选前置关系、英文题（带答案与解析）；保留原作者署名与协议 |
| [rainewhk/gaokao](https://github.com/rainewhk/gaokao) | 2010–2024 高考九科 3,126 道真题，含解析 | **Apache-2.0**（仓库） | 题干、答案、解析按题录入；见下方版权说明 |
| [CMATH](https://huggingface.co/datasets/weitianwen/cmath) | 小学 1–6 年级数学应用题 1,698 道 | **CC BY 4.0** | 题干与数值答案；署名见下 |

### 已排除的 NC / 研究限定源（不得引入本目录）

- K12-KGraph（北大，CC BY-NC-SA 4.0）——图谱与题库均不引入
- CJEval（初中 2.6 万题，README 明示禁止商用）
- cn-math-taxonomy 题库正文（CC BY-NC 4.0）——仅保留既有编号+深链范式
- C-Eval 数据集（CC BY-NC-SA 4.0）
- NexData 1.3 亿题（无明确开放授权）

## 版权与合规声明

1. **高考真题**：仓库本身为 Apache-2.0，但上游 README 明示「试题原文版权归原出题机构所有，仅供研究和学术用途」。本目录仅作教学研究与样例展示；商业上线前须由法务确认边界，必要时改为深链或剔除。
2. **CC BY-SA 4.0 相同方式共享**：OKG 概念与英文题衍生数据如需公开发布，须保留署名，并以 CC BY-SA 4.0 同协议提供本 overlay（本 NOTICE 即声明）。
3. **CC BY 4.0 署名**：CMATH 数据来自 weitianwen/cmath，原数据集由小米团队发布。
4. **NC 红线**：本目录不含任何 NC / 研究限定数据正文，避免公开发布时的授权冲突。

## 数据使用边界（与前例一致）

- **不改权威源**：`data/trees/**`、`data/kp/**`、`data/knowledge-map-data.json` 均不修改。
- **不写课标原文**：`curriculum_points` 只由课标检索库逐字带出；本目录不产出该字段。
- **关系仅作候选**：OKG 前置关系标 `review: candidate`，须教师审核后才可进入权威边。
- **对齐仅作候选**：`alignment.json` 的 kp↔topic 映射标 `confidence` / `review: candidate`，`low` 置信不得直接用于自动出题。
- **题库为参考层**：中文主力仍为站内自有题；英文题仅作教师参考，不进入面向学生的正式测评。

## 文件

| 文件 | 说明 |
|:---|:---|
| `topics.json` | OKG 概念索引（id/title/domain/course/stage/prerequisites） |
| `questions.json` | 三源统一 schema 题库（stem/options/answer/explanation/license/source） |
| `alignment.json` | TeachAny kp ↔ OKG topic 分级对齐（term overlap + subject anchor） |
| `report.json` | 生成时间、来源、统计、质量策略 |

## 生成方式

```bash
python3 scripts/build-open-kg-enrichment.py
```

脚本只读外部源与本地 kp 索引，幂等；不修改任何权威数据。

> 免责：上游数据按 AS-IS 提供；本站仅作本地预览与教学研究，商用前需逐源法务确认。
