# PLAN.md — it-e-encoding-basics 编码初识

## 基本信息

| 项 | 值 |
|---|---|
| course_id | it-e-encoding-basics |
| node_id | it-e-encoding-basics（小学信息科技 · 数据与编码 · G4） |
| 标题 | 编码初识：把信息变成密码 |
| 学段 | elementary（body class `teachany-elementary`，暖白配色覆盖） |
| 课型 | new-concept |
| 版本 | 1.0.0 · skill v7.21.0 |

## 知识层引用（Phase 0.5）

KCP 为空（`knowledge_layer.py` 对 info-tech 无数据），按流程走 web_search 补充，`source: web_fallback`：

| 引用 | 内容 | 来源 |
|---|---|---|
| cp-web-1 | 学段目标（信息意识）：「知道数据编码的作用与意义，理解数据编码是保持信息社会组织与秩序的科学基础」 | 《义务教育信息科技课程标准（2022年版）》第二学段目标（广东教育资源平台 PDF 全文） |
| cp-web-2 | 学段目标：「能基于对事物的理解，按照一定的规则表达与交流信息。体验信息存储和传输过程中所必需的编码及解码步骤」 | 同上 |
| cp-web-3 | 内容要求（数据与编码）：「了解数字化表示信息的优势，体验信息存储和传输过程中所必需的编码和解码步骤，初步理解数据校验的目的和意义」 | 课标原文（教学基本功比赛通知引用） |
| ex-web-1 | 例题：把数字 5 用「点卡二进制」编码（8/4/2/1 四张卡，翻=1 不翻=0 → 0101） | 自编（依据 cp-web-3 设计，四年级数与代数范围） |
| ex-web-2 | 例题：同学甲用规则「A=1,B=2,…」把单词编码成数字串，解码还原 | 自编（依据课标实验教学主题「使用数字、字母或文字编码表示信息」） |
| err-web-1 | 易错点：以为编码可以随便改（规则一变，解码就乱——编码必须双方共用同一规则） | 自编 |
| err-web-2 | 易错点：把二进制读成十进制（0101 读成「一百零一」） | 自编 |

## 教学骨架（Phase 1）

- 问题锚点：同一个数字，为什么计算机里要写成 0101？/ 一句话怎么变成一串数字发出去？
- ABT：And（已经会用数字记录班级身高、成绩）→ But（计算机不认识汉字和数字，只认 0 和 1，信息怎么存、怎么传？）→ Therefore（本课学会用编码把信息变成一串数字，并能解码还原）。
- 互动设计：
  1. **二进制翻牌实验室**（Canvas）：8/4/2/1 四张点卡，点击翻面，实时显示二进制与十进制，挑战目标数字。
  2. **消息编码器**（Canvas/输入）：输入字母→A1Z26 编码输出，再互相解码。
- 评估：前测 1 题 + ConcepTest 1 题 + 后测 1 题 + 分层综合任务（L1/L2/L3）。
- 学习闭环：问题锚点 → 前测暴露直觉 → 概念 → 翻牌试错 → 编码器应用 → 习题讲解 → 后测迁移 → 总结回收锚点。

## 页面规划（v2，14 页 ≥12）

0 封面 / 1 问题锚点 / 2 学习目标 / 3 前测 / 4 概念：什么是编码 / 5 互动：二进制翻牌实验室 / 6 概念：字符编码与规则 / 7 互动：消息编码器 / 8 习题讲解（worked example） / 9 ConcepTest / 10 综合任务（分层） / 11 后测 / 12 小结 / 13 知识图谱 / 14 AI 学伴 —— 实际以 build 为准（≥12）。

## 视觉

- `teachany-elementary`：`--bg:#fffbf0`、珊瑚红 `#ff6b6b` + 薄荷绿 `#4ecdc4`、20px 圆角、第一关/第二关练习气质、鼓励式反馈语气。
- v2 深色壳全面覆盖为暖白：brand bar / toolbar / card / canvas-wrap / sidenav 均做小学化覆盖。
- Hero：ImageGen 生成知识结构信息图（中文标注）+ 2 张 section 教学示意图，全部真实内容图。

## 音频

`tts-engine.py`（Edge Neural zh-CN-XiaoyiNeural）为每个 `data-tts` 段生成真实 mp3；`data-teachany-audio-playlist` 全量映射；narrator 启用（无 `data-tts-disabled`）。

## 发布

Phase 3.5a 反馈密码询问教师；3.5b 询问上传；同意后 `TEACHANY_UPLOAD_CONFIRMED=1 hang_tree.py publish it-e-encoding-basics`。
