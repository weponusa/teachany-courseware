---
name: teachany-pbl
description: >-
  Decompose a PBL project goal via teachany.cn into a knowledge-path PNG and
  editable link. Use for 项目式学习拆解、知识路径图谱、PBL 拆解、课标对齐项目路径.
  Not for generic lesson plans or interactive courseware HTML.
compatibility: Python 3.9+, playwright + chromium, network access to www.teachany.cn
---

# TeachAny PBL

将**项目任务**（+ 可选学段/学科/产出）拆解为：

1. **PNG 长图** — 结构化蓝图 + 知识路径图谱  
2. **编辑链接** — `https://www.teachany.cn/pbl?handoff=...`（或 `?pbl=...`），打开即为已拆解项目页

拆解由 teachany.cn 六阶段管线完成（LLM + 多课标索引）。**禁止**自行编造知识点节点或用手写列表代替 CLI 产出。

## 何时不用

- 只要普通教案、无项目交付物 → 不用本 skill  
- 要生成交互课件 HTML → 用 TeachAny courseware skill  
- 无法访问 teachany.cn / Playwright 安装失败 → 见 [references/fallback.md](references/fallback.md)

## Workflow

1. 从用户话术中提取参数（见 [references/parameters.md](references/parameters.md)）；缺省用默认值，**不必逐项追问**。  
   `deliverable=other` 时加 `--deliverable-custom "自定义产出名"`。
2. 在 **本 skill 目录**（`SKILL.md` 所在处）执行 CLI：

```bash
python3 scripts/pbl-decompose.py \
  --goal "用户的项目任务原文" \
  --grade junior \
  --subject science \
  --deliverable design-proposal \
  -o ./pbl-output
```

3. 首次缺依赖：`pip install playwright && playwright install chromium`  
4. 读取输出 JSON（路径见下），向用户回复 PNG、`summary` 统计、`edit_url`。  
5. **不要**在 CLI 已跑过的情况下由 Agent 再次自动重试同一命令；仅当 Playwright 完全不可用时走 fallback。  
6. 耗时通常 **3–8 分钟**（复杂项目可能接近 10 分钟），告知用户耐心等待。

### 输出文件（`-o` 目录下）

| 文件 | 说明 |
|------|------|
| `{slug}.png` | 长图（`slug` 由 `--goal` 生成） |
| `{slug}.json` | 元数据：`image`、`edit_url`、`handoff_source`、`summary` |

`edit_url` 优先含 `?handoff=`；若为 `?pbl=` 亦可编辑；仅 `?goal=` 表示 handoff 失败，需说明用户打开后须再点「拆解项目路径」。

## 回复模板

```markdown
## PBL 拆解结果

**项目**：{goal}

![PBL 知识路径拆解]({png_path})

- **图谱节点**：{nodeCount}（课标 {matched} · 外部 {external}）
- **继续编辑**：[在 TeachAny 打开]({edit_url})

可在 TeachAny 对话修改拆解、调整知识点、一键制作课件。
```

环境支持时展示 PNG 长图。

## 示例

用户：「初中科学，设计水火箭并安全发射，要工程原型」

```bash
python3 scripts/pbl-decompose.py \
  --goal "设计一款水火箭并完成安全发射" \
  --grade junior --subject science --deliverable engineering-prototype \
  -o ./pbl-output
```

## 参考

- 参数表：[references/parameters.md](references/parameters.md)  
- Playwright 不可用 / 网络异常：[references/fallback.md](references/fallback.md)
