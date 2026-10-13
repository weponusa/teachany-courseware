# TeachAny 课件制作 Checklist

> **目标**：让任何 agent 产品生成的课件一次性通过 `validate-courseware.py` 的 13 条硬规则（0 error）。
> 
> **最后更新**：2026-05-22

---

## Phase 0: 开始前

- [ ] **确定课程 ID**（如 `math-m-linear-function`），格式：`<学科>-<学段>-<主题>`
- [ ] **确定 node_id**，与知识树 `data/trees/*.json` 中的节点 ID 对应
- [ ] **确认仓库位置**：课件文件放在 `teachany-courseware/community/<course-id>/`

---

## Phase 1: 生成课件 HTML（8 个必含 section）

### 最小 HTML 骨架

```
index.html 必须包含以下 section（硬规则 #21）：
├── Hero 封面（#hero）
├── 问题锚点（#problem-anchor）
├── 学习目标（#objectives）
├── 前测（#pretest）
├── 知识模块 ≥3 个（每个有实质性讲解内容）
├── ConcepTest（#conceptest）
├── 后测/总结（#summary）
└── 知识图谱（#knowledge-graph）
```

### ⚠️ 常见错误
- ❌ 生成空壳 HTML（只有 2 个 section，其余全是占位符）
- ❌ 用 `placeholder`、`占位` 等占位词
- ❌ 有效教学文本 < 1800 字符

---

## Phase 2: 补充资源文件

### 2.1 manifest.json（硬规则 #18）

```json
{
  "name": "课件中文名称",
  "subject": "math",
  "grade": 8,
  "node_id": "math-m-linear-function",
  "teachany_version": "7.15",
  "curriculum_standards": "义务教育数学课程标准 2022版 ...",
  "prerequisites": ["math-m-proportional-function"],
  "domain": "function"
}
```

### 2.2 Hero 封面图（硬规则 #57）

1. 先查 L1-L3（本地/图床/精选版）是否已有
2. 没有则生成 SVG hero 图
3. **SVG 中文必须 text-to-path**（规则 #70）：
   - 有 Inkscape → `inkscape --export-text-to-path`
   - 有 fonttools → `python3 scripts/svg-text-to-path.py input.svg output.svg`
   - 都没有 → **SVG 中不写 `<text>`**，中文标题用 HTML 覆盖在 SVG 上方
4. HTML 中引用：`<img class="hero-cover-img" src="./assets/<id>-hero.png">`

### 2.3 插图 ≥2 张（硬规则 #34）

- 每个 knowledge section 至少 1 张插图
- 图片放在 `assets/` 目录
- HTML 中用 `<img src="./assets/xxx.png">` 引用
- 路径层级注意：从 `community/<id>/index.html` 引用 `assets/`，相对路径是 `./assets/`

### 2.4 TTS 语音（硬规则 #16）

- 用 edge-tts 生成 ≥3 个 mp3 文件（导入/核心/总结各一个）
- 放在 `tts/` 目录
- HTML 中需要标准音频播放器 UI（`data-teachany-audio-playlist`）

### 2.5 AI 学伴模块（硬规则 #45）

HTML `<head>` 中：
```html
<link rel="stylesheet" href="../../assets/scripts/ai-tutor.css">
```

`</body>` 前：
```html
<script src="../../assets/scripts/ai-tutor.js" defer></script>
<script>
window.__TEACHANY_TUTOR_CONFIG__ = {
  courseTitle: "课件标题",
  subject: "math",
  grade: 8,
  learningObjectives: ["目标1", "目标2"],
  getContext: () => "当前学习内容描述"
};
</script>
```

### 2.6 知识图谱模块（硬规则 #24）

HTML body 底部（footer 前）：
```html
<div data-teachany-kg="<node_id>">
  <canvas class="tkg-fallback-canvas" width="720" height="120"></canvas>
</div>
```

引入：
```html
<link rel="stylesheet" href="../../assets/scripts/teachany-knowledge-graph.css">
<script src="../../assets/scripts/teachany-knowledge-graph.js" defer></script>
```

---

## Phase 3: 必含标注属性

以下属性加在对应的 `<section>` 上：

| 属性 | 值 | 说明 |
|:---|:---|:---|
| `data-bloom-level` | `remember/understand/apply/analyze/evaluate/create` | Bloom 认知层级（至少覆盖 3 级） |
| `data-scaffold` | `full/partial/none` | 脚手架分级（至少 2 种） |
| `data-conceptest` | `true` | 标记 ConcepTest 检查点 |

---

## Phase 4: 发布前自检

### 运行质检
```bash
cd teachany-courseware
python3 scripts/validate-courseware.py <course-id>
```
**必须 0 error 才能发布**。

### 路径检查清单
- [ ] CSS/JS 引用路径正确：`../../assets/scripts/xxx.{css,js}`
- [ ] 图片引用路径正确：`./assets/xxx.png`
- [ ] Hero 图片引用路径正确：`./assets/<id>-hero.png`
- [ ] 所有引用的文件都实际存在（无 404）

### 注册信息检查
- [ ] `manifest.json` 的 `node_id` 在 `data/trees/*.json` 中存在
- [ ] `manifest.curriculum_standards` 已填写（非空字符串）

---

## ⛔ 禁止事项

| 禁止 | 原因 |
|:---|:---|
| SVG 中用 `<text>` 渲染中文但未做 text-to-path | 其他设备上会变方块乱码 |
| 路径用 `../../../assets/` 从 `community/<id>/` | 应为 `../../assets/`（多了一级） |
| HTML 中 `</svg>` 未闭合 | 浏览器解析异常 |
| 模板占位符（placeholder/占位）残留 | 质检不通过 |
| 直接 push 到 main 绕过质检 | 违反发布流程 |
| 在 HTML/JS 中硬编码 API Key | 安全红线 |

---

## 常见问题 FAQ

**Q: 没有 image_gen 工具怎么办？**
A: 用 SVG 生成 hero 图，但中文必须 text-to-path。如果连 fontTools 都没有，就让 SVG 只画图形（节点、连线、色块），中文标题用 HTML 绝对定位叠在上面。

**Q: 没有 Remotion 怎么生成 mp4？**
A: 硬规则 #32 要求 mp4，但如果环境不支持 Remotion，在 manifest 中声明并获取用户豁免。

**Q: 没有边缘 TTS 怎么生成语音？**
A: `pip install edge-tts` 安装后用 `edge-tts --text "..." --voice zh-CN-YunxiNeural --write-media output.mp3` 生成。

**Q: CSS/JS 路径怎么确定？**
A: 从 `community/<id>/index.html` 到 `assets/scripts/` 需要向上两级：`../../assets/scripts/`。
