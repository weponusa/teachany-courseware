# 程序控制结构：顺序、分支与循环 课件计划

- node_id: `it-h-control-structures`
- 学段：高中信息技术 G10
- 课标领域：程序设计与数据结构
- 问题锚点：为什么程序不是一行一行写完就够了，还要分支和循环？
- 课标依据：从生活实例出发，概述算法的概念与特征，运用恰当的描述方法和控制结构表示简单算法。

## 1. 学习设计与问题锚点

学生已经接触过程序或算法描述，但常把程序设计理解成“照着语法写代码”。本课用真实校园信息系统任务切入，让学生理解：程序设计首先是把现实问题抽象成变量、结构、算法和可验证结果。

## 2. 模块级媒体策划表

| # | 模块名 | 知识点 | 媒体形式 | 资产文件名 | 生成命令 | 校验命令 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Hero 知识结构图 | 程序控制结构：顺序、分支与循环 | Hero 图 | assets/hero-infographic.svg | python3 inline-svg-generator | node scripts/validate-courseware.cjs community/it-h-control-structures |
| 2 | 开场与目标音频 | 问题锚点 | Edge TTS 音频 | tts/s01.mp3 | say+ffmpeg | node scripts/validate-courseware.cjs community/it-h-control-structures |
| 3 | 核心机制音频 | 概念解释 | Edge TTS 音频 | tts/s02.mp3 | say+ffmpeg | node scripts/validate-courseware.cjs community/it-h-control-structures |
| 4 | 互动模型 | 变量与结果 | Canvas 互动 | inline-canvas | HTML Canvas | node scripts/validate-courseware.cjs community/it-h-control-structures |
| 5 | 微课视频 | 过程回顾 | Remotion 视频 | assets/video/it-h-control-structures-micro.mp4 | ffmpeg | node scripts/validate-courseware.cjs community/it-h-control-structures |
| 6 | 知识图谱 | 前置后续关系 | 标准模块 | data-teachany-kg=it-h-control-structures | 复用公共模块 | python3 scripts/check-knowledge-graph.py |

## 3. 五件套自检清单

- [x] AI 学伴标准模块
- [x] Tutor card 导师卡片
- [x] TTS narrator 与连续音频播放器
- [x] Section hints 标准提示
- [x] Knowledge graph 标准知识图谱

## 4. Subagent 派遣与执行分工

本课由主执行流程统一完成教学设计、页面实现、资产生成和验证闭环。必要时可拆分为内容设计、前端互动、媒体资产和质量检查四个子任务，但最终以本目录产物和校验输出为准。

互动与评价设计：前测检查学生是否理解关键前提；核心互动用滑块改变变量，观察输出变化；概念测验提供错因诊断；迁移任务要求学生把知识应用到新的校园信息系统情境中。

## 5. 资源与实现说明

页面使用本地 SVG Hero、真实 mp3、真实 mp4、Canvas 互动和公共模块。所有本地资源都在课件目录内，不引用不存在的图片或脚本。

## 6. 验证与发布检查

```bash
cd /Users/wepon/CodeBuddy/一次函数/teachany-courseware
python3 scripts/check-plan.py community/it-h-control-structures
node scripts/validate-courseware.cjs community/it-h-control-structures
python3 scripts/rebuild-index.py
```
