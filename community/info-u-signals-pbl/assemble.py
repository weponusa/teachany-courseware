#!/usr/bin/env python3
from pathlib import Path

root = Path("/Users/wepon/CodeBuddy/一次函数/teachany-courseware/community/info-u-signals-pbl")
html = (root / "index.html").read_text(encoding="utf-8")
sections = (root / "assets" / "content-sections.html").read_text(encoding="utf-8")
extra_css = (root / "assets" / "extra.css").read_text(encoding="utf-8")

start = html.find("<!--\n================================================")
end = html.find("-->", start)
if start != -1 and end != -1:
    html = html[:start] + html[end + 3:]

html = html.replace("<body>", '<body class="teachany-high">')
# Do not put the literal "</style>" in CSS comments: HTML parsers close the
# style element as soon as they see that sequence, even inside a comment.
if "/* extra course CSS */" not in html:
    html = html.replace("</style>", extra_css + "\n</style>", 1)
html = html.replace('data-tts-disabled="true"', "")

repl = {
    "{{TITLE}}": "信号与处理：从学生提问出发",
    "{{DESCRIPTION}}": "大学信息类核心课 PBL 课程设计：从听不清的广播提出问题，经采样、LTI/卷积、DFT/窗、FIR/IIR 四关，交付可答辩的处理链路。",
    "{{COURSE_ID}}": "info-u-signals-pbl",
    "{{SUBJECT}}": "info-tech",
    "{{STAGE_GRADE}}": "大学·信息类",
    "{{GRADE}}": "12",
    "{{STAGE}}": "high",
    "{{NODE_ID}}": "ext-c84e21c6",
    "{{DOMAIN}}": "数字信号处理",
    "{{PREREQ_COURSE_IDS}}": "",
    "{{NEXT_COURSE_ID}}": "",
    "{{COURSE_VERSION}}": "1.0.0",
    "{{TEACHANY_VERSION}}": "7.21.0",
    "{{LESSON_TYPE}}": "inquiry-project",
    "{{FREE_MODE}}": "false",
    "{{PREREQUISITE_NAMES}}": "高等数学；大学物理波动基础",
    "{{HERO_QUESTION}}": "广播听不清，你的第一个真正的问题是什么？",
    "{{HERO_IMAGE_ALT}}": "信号与处理 PBL 知识结构：学生提问到采样、LTI 卷积、DFT 窗函数、FIR/IIR 滤波",
    "{{HERO_FIGCAPTION}}": "课程不从定义开始。先把听不清写成可检验的问题，四道关卡逼出核心课深度。",
    "{{SLIDE_COUNT}}": "27",
    "{{KG_PAGE_INDEX}}": "25",
    "{{TUTOR_PAGE_INDEX}}": "26",
    "{{OPTIONAL_MAP_HEAD}}": "",
    "{{OPTIONAL_MAP_TAIL}}": "",
}

anchors = """
          <button class="choice" data-anchor-choice="为什么把广播开得更响，字反而更糊？">为什么把广播开得更响，字反而更糊？</button>
          <button class="choice" data-anchor-choice="语谱图上那条横线是什么？怎样只去掉它？">语谱图上那条横线是什么？怎样只去掉它？</button>
          <button class="choice" data-anchor-choice="怎样证明一种处理比另一种更好，而不是听起来还行？">怎样证明一种处理比另一种更好，而不是「听起来还行」？</button>
"""
objectives = """
          <li>能把现象句升级为可检验命题，并据此设计对照实验</li>
          <li>能依据采样定理论证 fs、抗混叠与量化</li>
          <li>能鉴定处理块是否 LTI，并用卷积解释输入输出</li>
          <li>能用 DFT 做可辩护的频谱分析（Δf、窗、泄漏）</li>
          <li>能按指标比较 FIR 与 IIR，解释相位与群延迟</li>
"""
playlist = """[
    {"id": "hero", "title": "开场", "src": "tts/hero.mp3"},
    {"id": "problem-anchor", "title": "问题锚点", "src": "tts/problem-anchor.mp3"},
    {"id": "objectives", "title": "学习目标", "src": "tts/objectives.mp3"}
  ]"""

repl["{{PROBLEM_ANCHOR_CHOICES}}"] = anchors
repl["{{LEARNING_OBJECTIVES}}"] = objectives
repl["{{AUDIO_PLAYLIST_JSON}}"] = playlist
repl["{{CONTENT_SECTIONS}}"] = sections

for k, v in repl.items():
    html = html.replace(k, v)

html = html.replace(
    "getContext: () => {\n      const current = pages[currentPage];\n      return (current || document.body).innerText.slice(0, 3000);\n    }\n  };",
    """getContext: () => {
      const current = pages[currentPage];
      return (current || document.body).innerText.slice(0, 3000);
    },
    suggestedQuestions: [
      '为什么放大之后可懂度可能下降？',
      'fs 低于 2f 时重建频率为什么不是原来的 f？',
      '零填充能不能提高频率分辨率？',
      'FIR 线性相位的代价是什么？'
    ],
    teachingStance: '先追问学生的问题属于 L1/L2/L3，再给最小定理提示，不要直接给完整设计。'
  };""",
)

lab_tag = '<script src="./assets/dsp-labs.js" defer></script>\n'
html = html.replace(
    '<script src="../../assets/scripts/ai-tutor.js"></script>',
    lab_tag + '<script src="../../assets/scripts/ai-tutor.js"></script>',
)

(root / "index.html").write_text(html, encoding="utf-8")
left = [line.strip() for line in html.splitlines() if "{{" in line]
print("placeholders left:", left[:12], "count", len(left))
print("pages", html.count('class="slide-page"'))
print("bytes", len(html.encode()))
