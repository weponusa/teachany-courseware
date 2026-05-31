# 文艺复兴与宗教改革 · TeachAny 课件

**课件 ID**：`hist-m-renaissance`
**版本**：v1.0.0
**适用**：部编版世界历史九年级上册 第 14 课
**时长**：45 分钟

## 课件内容

以"人重新发现自己"为叙事主线，讲解 14-17 世纪欧洲两场塑造现代世界的思想运动：文艺复兴 + 宗教改革。

包含 7 个核心 section + 自适应 4 分支 + ConcepTest + 知识图谱。

## 本地预览

```bash
# 直接在浏览器打开
open index.html

# 或启动本地服务器（推荐，以测试 PWA）
python3 -m http.server 8000
# 访问 http://localhost:8000
```

## 14 项基线交付状态

| # | 基线项 | 状态 | 备注 |
|:-:|:---|:---:|:---|
| ① | TTS 旁白音频 + `data-tts` | ✅ | 7 段 MP3，共 1.2MB，edge-tts 引擎 |
| ② | Remotion MP4 视频 | ⚠️ 待补 | v1.0 先交付静态课件，v1.1 计划补"佛罗伦萨 → 威登堡"90s 动画 |
| ③ | Canvas 互动（真实计算）| ✅ | "印刷术传播速度"模拟器（参数滑块 → 实时计算扩散天数）|
| ④ | AI 插画（学科特定，≥2 张）| ✅ | 三杰代表作 + 1517 年钉论纲场景 |
| ⑤ | Hero 知识结构图 | ✅ | 文艺复兴+宗教改革双翼结构，贴在顶部 |
| ⑥ | 音频播放器模块 | ✅ | 7 轨播放列表，每条有自解释标题 |
| ⑦ | 知识图谱区块 | ✅ | `<section id="knowledge-graph">` 占位 |
| ⑧ | AI 学伴卡片 | ✅ | `<section id="ai-tutor-card">` 占位，tutor-card.js 挂载 |
| ⑨ | 段落提示（Section Hints）| ✅ | 每个 section 带 `data-tsh` 属性 |
| ⑩ | TTS 朗读叠加层 | ✅ | data-tts 属性 + tts-narrator.js 挂载 |
| ⑪ | ai-tutor.js | ✅ | 从 `../../scripts/` 加载 |
| ⑫ | knowledge-graph.js | ✅ | 从 `../../scripts/` 加载 |
| ⑬ | 五件套同时挂载 | ✅ | 5 个 CSS + 5 个 JS 齐全 |
| ⑭ | manifest.json + node_id | ✅ | `hist-m-renaissance` 已在知识树 `data/trees/cn/middle/history.json` 中 |

**完成度：13/14 = 93%**（Remotion 视频 v1.1 补）

## 自适应 4 分支内容

| 分支 | 内容 | Bloom 层级 |
|:---|:---|:---|
| `review-prereq` | 60 秒回顾中世纪欧洲 3 特征（适合前置不牢的学生）| Remember/Understand |
| `scaffold` | worked example：5 步判断一幅画的时期 | Understand/Apply |
| `normal`（默认）| 3 道分层练习（理解/应用/综合）| Apply/Analyze |
| `challenge` | 反事实+迁移+评判 3 道（无印刷术 / 互联网类比 / 批评错误概念）| Analyze/Evaluate |

每个分支都是**实质内容**，不是空壳 toast。

## 新增增强模块

除 14 项基线外，本课件还包含：

- **ConcepTest**：1 道精心设计的概念题（30-70% 甜点区），支持二次投票
- **5 镜法回顾卡**：See/Break/Compare/Transfer/Evaluate 5 个视角总结
- **互动地图**：本地 SVG 地图，4 个关键城市（佛罗伦萨/罗马/威登堡/伦敦）可点开看详情（不用 XYZ 在线瓦片）
- **时间轴**：8 个关键事件，从 1304 彼特拉克到 1648 威斯特伐利亚
- **PWA 离线**：manifest.webmanifest + sw.js，支持教室断网场景

## 待办

- [ ] v1.1：补 Remotion MP4 视频（基线②完整交付）
- [ ] 迭代 Hero 图：已生成的版本中字体可进一步优化
- [ ] 补充 AI 学伴预设追问 5-10 条

## 发布

见 `/Users/wepon/.codebuddy/skills/teachany/skill/references/packaging.md`

URL（发布后）：
- 课件仓 GitHub Pages：https://www.teachany.cn/community/hist-m-renaissance/
- Gallery 跳转入口：https://www.teachany.cn/community/hist-m-renaissance/

---

© TeachAny · 2026 · MIT License
