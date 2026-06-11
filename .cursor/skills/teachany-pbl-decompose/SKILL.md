---
name: teachany-pbl-decompose
description: >-
  将 PBL 项目任务拆解为知识路径图谱并导出长图，返回 TeachAny 可继续编辑的链接。
  用于用户提到 PBL 拆解、项目式学习路径、知识图谱拆解、TeachAny PBL、
  「帮我拆这个项目」「研学/水火箭/购车」类跨学科任务规划时。
---

# TeachAny PBL 拆解 Skill

用户只需提供 **项目任务** 和少量可选信息，即可得到：
1. **拆解长图**（PNG，含结构化拆解 + 知识路径图谱）
2. **TeachAny 编辑链接**（在浏览器中继续调整节点、对话修改、导出课件）

## 必填 / 可选输入

| 字段 | CLI 参数 | 说明 | 默认 |
|------|----------|------|------|
| 项目任务 | `--goal` | 要做什么（必填） | — |
| 学段 | `--grade` | primary / junior / senior / university / adult / any | any |
| 学科取向 | `--subject` | math, physics, chinese, cross… | cross |
| 产出类型 | `--deliverable` | report, app-software, decision-table… | report |
| 受众 | `--audience` | 班级展示、家庭决策… | — |
| 周期 | `--duration` | 4 周、8 课时… | — |
| 约束 | `--constraints` | 预算、设备… | — |

从用户自然语言中提取上述字段；缺省项不必追问，用默认值直接跑。

## 执行步骤（必须跑脚本，不要手写拆解）

在 **teachany-courseware** 仓库根目录执行：

```bash
python3 scripts/pbl-decompose.py \
  --goal "用户的项目任务原文" \
  --grade junior \
  --subject cross \
  --deliverable report \
  -o ./pbl-output
```

按需追加 `--audience` `--duration` `--constraints` `--deliverable-custom`。

### 首次环境

```bash
pip install playwright
playwright install chromium
```

若 `playwright` 不可用，仍应生成 **编辑链接** 给用户（见下方「仅链接兜底」），并说明需安装依赖后重试出图。

### 输出解读

脚本 stdout 示例：

```text
✅ PBL 拆解完成
   长图: /path/to/研学路线规划.png
   节点: 18 个
   继续编辑: https://www.teachany.cn/pbl.html?goal=...
```

同目录还有 `{slug}.json` 元数据（`edit_url`、`summary`）。

## 回复用户模板

拆解完成后，用此结构回复：

```markdown
## PBL 拆解结果

**项目**：{goal}

![PBL 知识路径拆解]({png 相对或绝对路径})

- **图谱节点**：{nodeCount} 个（课标 {matched} · 外部 {external}）
- **继续编辑**：[在 TeachAny 打开]({edit_url})

在 TeachAny 页面你可以：
- 对话修改拆解（「减少外部节点」「加强实验环节」）
- 勾选/替换知识点
- 从节点一键「制作课件」
```

若在当前对话中能展示图片，**必须**附上生成的 PNG。

## 仅链接兜底（无法跑 Playwright 时）

手动拼编辑链接（不含 `auto=1`）：

```
https://www.teachany.cn/pbl.html?goal={urlencode(task)}&grade={grade}&subject={subject}
```

告知用户打开后点击 **「拆解项目路径」**，完成后可导出长图。

## 本地调试

对本地 Pages 预览：

```bash
python3 scripts/pbl-decompose.py --goal "..." \
  --base-url "http://localhost:8788/pbl.html" -o ./pbl-output
```

## 禁止事项

- **不要**用通用 LLM 臆造知识点列表代替 TeachAny 六步拆解流水线
- **不要**省略 `edit_url`；用户需要可在网站上继续改
- **不要**把 `auto=1` 放进给用户的编辑链接（仅 CLI 内部自动化使用）

## 参考

- 拆解页面：`pbl.html`
- 自动化 API：`window.TeachAnyPBLAutomation`
- CLI 源码：`scripts/pbl-decompose.py`
