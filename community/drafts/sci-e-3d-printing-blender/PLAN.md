# PLAN.md · sci-e-3d-printing-blender
## 课件元信息
- **课件ID**：sci-e-3d-printing-blender  
- **主题**：3D建模入门：用Blender做3D打印模型
- **学段/年级**：小学 G4-G6（信息技术/STEM方向）  
- **课型**：新授课 + 活动驱动  
- **free_mode**：true（非标准课标内容，进入"其他知识"树）  
- **TeachAny版本**：7.9.15

## 教学骨架（ABT结构）
**And**：同学们知道画画可以用画笔，搭积木可以用积木块。  
**But**：如果想让自己设计的东西"打印"成真实的模型，用普通画笔和积木做不到。  
**Therefore**：我们要学习用电脑上的3D建模工具（Blender），把想象变成可以摸到的实体！

## 叙事主线（空间线 → 逻辑线）
定义概念 → 认识Blender界面 → 基本操作技能 → 搭积木式建模 → 3D打印规则

## 模块级媒体策划表

| 模块ID | 模块名称 | 媒体形式 | 资产文件名 | 校验命令 |
|:---|:---|:---|:---|:---|
| M1 | Hero知识结构主图 | Hero图（image_gen位图） | assets/sci-e-3d-printing-blender-hero.png | check-hero.py |
| M2 | 前测：你了解3D吗？ | HTML选择题 + JS反馈 | index.html #pretest | grep handleQuiz |
| M3 | 3D建模基本概念 | Canvas互动（顶点/边/面标注） | index.html #module-concepts | canvas元素存在 |
| M4 | Blender界面认识 | 情境插图 + TTS讲解 | assets/illustration-child-blender.png + tts/ | ls tts/*.mp3 |
| M5 | 基本操作技能 | Canvas互动（视角模拟器） | index.html #module-operations | canvas元素存在 |
| M6 | 搭积木建模 | Remotion视频（建模过程动画） | assets/video/blender-modeling-demo.mp4 | ffprobe |
| M7 | 3D打印规则 | 情境插图 + TTS讲解 | assets/illustration-3d-printing.png + tts/ | ls tts/*.mp3 |
| M8 | 综合任务：设计你的模型 | Canvas画板（3D草图） | index.html #task | canvas元素存在 |
| M9 | 知识图谱 | 标准公共模块 | data-teachany-kg="sci-e-3d-printing-blender" | check-knowledge-graph |
| M10 | TTS语音讲解 | Edge TTS mp3 | tts/seg01_zh.mp3 ~ tts/seg06_zh.mp3 | ls -la tts/*.mp3; file tts/*.mp3 |
| M11 | AI学伴 | 标准公共模块（五件套） | ai-tutor.js + tutor-card | validate-courseware |
