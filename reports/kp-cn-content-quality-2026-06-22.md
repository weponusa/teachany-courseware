# 中国课标 KP 内容质量审计报告

生成时间：2026-06-22（已全量升级）

## 升级结果（950 个 CN KP）

| 指标 | 升级前 | 升级后 |
|---|---:|---:|
| 真实课标原文 `curriculum_points` | 873 / 77 占位 | **950 / 0** |
| 模板习题 `exercises` | 950 | **0**（全部学科化 + 教材摘录题） |
| 模板易错点 `errors` | 950 | **0**（学科化易错点） |
| `real_world` 情境 | 0 | **950** |
| `deep_textbook_snippets` | 0 | **419**（数理化生等，可追溯本地教材 MD） |
| 升级标记 | — | **950**（`kp_content_upgrade_2026-06-22`） |

**第二轮补全（同日）**：扩展课标 MD 源 + 课标原文 fallback → **950/950** 均有可追溯摘录。

执行命令：`python3 scripts/upgrade-cn-kp-content.py`

备份目录：`data/kp/_backups/upgrade-cn-kp-20260622-*`

## 升级内容说明

1. **课标树同步**：`curriculum_points` / `excerpt_ids` 以 `data/trees/cn/**` 为权威源
2. **教材摘录**：从 `books/课标-整理版`、`books/math|science/OpenStax_*.md` 等匹配 `deep_textbook_snippets`
3. **习题替换**：清除 `cn-curriculum-common` 套话；有摘录时首题为「根据教材片段…」；另附 1–2 道学科模板题
4. **易错点替换**：按学科灌入具体错因（非「套公式不求理解」类通用句）
5. **清除 AI 摘要**：删除「由课标要点生成」类 `textbook_summary`

## 仍待深化（531 门无 deep snippets）

~~语文、地理、政治、心理、信息科技等学科本地教材 MD 匹配较少~~

**已解决**：950/950 均有 `deep_textbook_snippets`（教材 MD 匹配 + 课标原文 fallback）。

长期仍可补：

- 补 `books/课标-整理版/cn/` 分学科 MD
- 对语文/英语灌入课文摘录库
- 运行 `deep-textbook-enrich-cn-kp.py --subject chinese` 增量补灌

## 历史记录（升级前问题）

<details>
<summary>升级前审计摘要</summary>

- 77 个 KP 课标点为 AI 占位「学段目标：理解并掌握…」
- 习题答案多为「应答覆盖课标要点，体现掌握与应用」
- 仅历史 87 门有 `section_excerpt` 课标摘录

</details>

详细机器可读清单：

- `data/kp/_backups/upgrade-cn-kp-*/upgrade-report.json`
- `reports/kp-cn-content-tier-audit.json`
- `scripts/upgrade-cn-kp-content.py`
