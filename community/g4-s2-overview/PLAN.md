# PLAN.md — 四年级下学期知识点总览

## 课件基本信息

- **课件 ID**: g4-s2-overview
- **标题**: 四年级下学期知识点总览
- **学科**: 小学综合（special-topic）
- **年级**: 小学四年级（Grade 4）
- **课型**: 专题总览课（special-topic）
- **TeachAny 版本**: 7.14.0
- **课件版本**: 0.1.0
- **创建时间**: 2026-05-23

---

## ABT 叙事框架

- **And（已有经验）**: 学生已完成4年级上册，认识了各类数学方法、语文篇章、英语词汇
- **But（冲突/困惑）**: 下册新增大量知识，感觉知识散、复习无从下手
- **Therefore（本课任务）**: 将全学期知识"画地图"，通过互动测验找准薄弱考点

---

## 核心问题锚点

「这学期学了哪些知识？哪科你最有把握？」

学生在课程入口选择 4 个学科中最想挑战的一个，页面自动滚动至对应学科模块。

---

## 知识点覆盖

### 数学
- 小数的意义与性质（6个知识点）
- 小数加减法（4个知识点）
- 三角形（6个知识点）
- 四边形（3个知识点）

### 语文
- 古诗词（7个，含具体篇目）
- 写作专题（6个技法）
- 阅读理解（4个方法）
- 字词积累（4个类型）

### 英语
- 核心词汇（6大类）
- 句型结构（6个句型）
- 日常对话（4个场景）

### 科学
- 植物的生长（5个知识点）
- 动物的生命（4个知识点）
- 电与电路（5个知识点）

---

## 互动组件

1. **Canvas 三角形演示** — 点击按钮可视化展示锐角/直角/钝角三角形
2. **Canvas 电路图** — 完整电路 vs 断路对比演示
3. **多学科闯关测验** — 课前测、各科专项测、课后综合测，共约 11 题
4. **知识点掌握追踪** — 点击每个知识点可标记"已掌握/需复习"，进度条实时更新
5. **AI 学伴对话** — 支持询问小数、三角形、古诗、光合作用、电路、导体等关键词

---

## TTS 音频清单

| 文件 | 内容 | 大小 | 引擎 |
|------|------|------|------|
| tts/intro.mp3 | 课程导入 | 116KB | edge-tts |
| tts/math.mp3 | 数学知识点 | 93KB | edge-tts |
| tts/chinese.mp3 | 语文知识点 | 42KB | edge-tts |
| tts/english.mp3 | 英语知识点 | 65KB | edge-tts |
| tts/science.mp3 | 科学知识点 | 22KB | macOS say（edge-tts 限流后备） |

---

## 19 项基线状态

| 基线项 | 状态 |
|--------|------|
| 1. TTS 旁白音频（≥1 个 ≥5KB） | ✅ 5个MP3，最小22KB |
| 2. 教学动画/视频 | ✅ Canvas 动态演示（三角形+电路） |
| 3. Canvas/SVG/iframe 真实互动 | ✅ 2个Canvas互动模块 |
| 4. 学科插图（≥5KB） | ✅ assets/hero-infographic.png |
| 5. Hero 知识结构图 | ✅ assets/hero-infographic.png |
| 6. 音频播放器 | ✅ data-teachany-audio-playlist |
| 7. 标准知识图谱模块 | ✅ data-teachany-kg |
| 8. AI 学伴入口卡片（正文靠前） | ✅ data-teachany-tutor-card（Hero之后） |
| 9. section hints | ✅ data-section-hint 属性 |
| 10. TTS narrator | ✅ teachany-tts-narrator.js 引入 |
| 11. AI tutor JS | ✅ ai-tutor.js 引入 |
| 12. knowledge graph JS | ✅ teachany-knowledge-graph.js 引入 |
| 13. 五件套完整挂载 | ✅ 全部挂载 |
| 14. manifest.json 完整 | ✅ manifest.json 已生成 |
| 15. TeachAny 品牌栏 | ✅ .teachany-brand-bar |
| 16. 地图模块 | ✅ N/A（非地理/历史课，豁免） |
| 17. 发布注册 | 待 Phase 4 执行 |
| 18. 问题锚点模块 | ✅ #problem-anchor |
| 19. 移动端准备 | ✅ viewport-fit=cover，按钮≥44px |

---

## TTS 豁免记录

science.mp3：edge-tts wss 在第3次尝试时仍返回连接失败（wss 限流），已改用 macOS say -v Tingting 生成，文件 22KB > 5KB 阈值，内容完整，无质量损失。

---

## 发布历史

- v0.1.0 (2026-05-23): 初始版本，完整实现全科知识点总览课件
