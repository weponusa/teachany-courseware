# 二次函数图像变换：从 y=x² 到 y=a(x-h)²+k 课件计划

- node_id: `math-m-quadratic-function`
- course_id: `math-m-quadratic-transformations`
- 学段：初中数学 G9
- 课标领域：数与代数
- 问题锚点：为什么 y=(x-3)²+2 不是向左移 3，而是向右移 3？
- 课标依据：会用配方法将数字系数二次函数的表达式化为 y=a(x-h)²+k 的形式，能由此得出二次函数图象顶点坐标，说出图象开口方向，得出最大值或最小值，并能确定相应自变量的值，解决简单的实际问题。

## 1. 学习设计与问题锚点

学生已认识 y=x² 和二次函数基本图像，但常把顶点式中的 h、k 与平移方向机械记反。本课用动态滑块和图像对照，让学生从“顶点在哪里”理解图像变换，而不是死背口诀。

## 2. 模块级媒体策划表

| # | 模块名 | 知识点 | 媒体形式 | 资产文件名 | 生成命令 | 校验命令 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Hero 知识结构图 | 二次函数图像变换 | Hero 图 | assets/hero-infographic.svg | python3 svg-generator | node scripts/validate-courseware.cjs community/math-m-quadratic-transformations |
| 2 | 过程图 | a/h/k 三参数 | SVG 插图 | assets/process-diagram.svg | python3 svg-generator | node scripts/validate-courseware.cjs community/math-m-quadratic-transformations |
| 3 | 应用图 | 喷泉轨迹建模 | SVG 插图 | assets/application-scene.svg | python3 svg-generator | node scripts/validate-courseware.cjs community/math-m-quadratic-transformations |
| 4 | 连续讲解 | 问题锚点/机制/迁移 | Edge TTS 音频 | tts/s01.mp3 tts/s02.mp3 tts/s03.mp3 | say+ffmpeg | node scripts/validate-courseware.cjs community/math-m-quadratic-transformations |
| 5 | 微课视频 | 图像变换回顾 | Remotion 视频 | assets/video/math-m-quadratic-transformations-micro.mp4 | ffmpeg | node scripts/validate-courseware.cjs community/math-m-quadratic-transformations |
| 6 | 知识图谱 | 二次函数节点 | 标准模块 | data-teachany-kg=math-m-quadratic-function | 复用公共模块 | python3 scripts/check-knowledge-graph.py |

## 3. 五件套自检清单

- [x] AI 学伴标准模块
- [x] Tutor card 导师卡片
- [x] TTS narrator 与连续音频播放器
- [x] Section hints 标准提示
- [x] Knowledge graph 标准知识图谱

## 4. Subagent 派遣与执行分工

本课由主流程完成内容设计、前端互动、媒体资产、质量检查和发布同步。若后续扩展，可拆为数学内容审稿、交互图像调优、音视频生成、发布验证四个子任务。

## 5. 资源与实现说明

页面包含 Canvas 抛物线互动、GeoGebra 图形工具入口、三张本地 SVG、三段 TTS、带音频流 MP4。核心设计强调“从顶点理解平移”，避免只背左加右减。

## 6. 验证与发布检查

```bash
python3 scripts/check-plan.py community/math-m-quadratic-transformations
node scripts/validate-courseware.cjs community/math-m-quadratic-transformations
python3 scripts/validate-courseware.py math-m-quadratic-transformations
```
