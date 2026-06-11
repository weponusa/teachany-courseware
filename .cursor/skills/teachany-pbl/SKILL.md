---
name: teachany-pbl
description: >-
  Runs TeachAny PBL project decomposition: knowledge-path graph, PNG report, and
  editable teachany.cn link. Use whenever the user wants PBL breakdown, project-based
  learning paths, curriculum mapping for a project, 项目式学习拆解, 知识路径图谱,
  teachany-pbl, or describes a cross-disciplinary student project (研学、水火箭、
  购车对比、智能温室、义卖策划) — even if they only give a one-line project goal.
  Do not use for generic lesson plans without a project deliverable, or for creating
  interactive courseware HTML (use TeachAny courseware skill instead).
compatibility: Python 3.9+, playwright + chromium, network access to www.teachany.cn
---

# TeachAny PBL

**CRITICAL**: MUST run `scripts/pbl-decompose.py` — NEVER hand-write nodes or use `?goal=` as primary edit link.

## Installation

**WorkBuddy**: [workbuddy.tencent.com](https://workbuddy.tencent.com/) → **官方 Skill 商店** → **`teachany-pbl`**

## Workflow

```bash
python3 scripts/pbl-decompose.py --goal "..." --grade junior -o ./pbl-output
```

- `edit_url` must contain `?handoff=` (completed project page)
- Show PNG from JSON `image` field — full report, not a self-written summary
- If handoff fails, retry CLI once before fallback

## Output

```markdown
## PBL 拆解结果
**项目**：{goal}
![拆解报告]({png_path})
- **节点**：{nodeCount}（蓝图 {hasBlueprint}）
- **继续编辑**：[TeachAny]({edit_url})  ← 必须含 handoff=
```

Package: https://github.com/weponusa/teachany-pbl
