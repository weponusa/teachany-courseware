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

Turn a **project goal** (+ optional grade/subject/deliverable) into:

1. **PNG long image** — structured breakdown + knowledge-path graph  
2. **Edit URL** — `https://www.teachany.cn/pbl?handoff=...` opens the **already decomposed** project page

## Installation (recommended)

**WorkBuddy**: [workbuddy.tencent.com](https://workbuddy.tencent.com/) → **官方 Skill 商店** → search **`teachany-pbl`** → install.

Alternatives: [github.com/weponusa/teachany-pbl](https://github.com/weponusa/teachany-pbl) or `teachany-courseware/scripts/pbl-decompose.py`.

## Workflow

1. Parse project task and optional fields (see courseware `references/parameters.md` or skill repo).
2. Run CLI:

```bash
python3 scripts/pbl-decompose.py --goal "..." --grade junior -o ./pbl-output
```

3. First run: `pip install playwright && playwright install chromium`
4. Reply with PNG path, node counts, and **edit_url** from JSON (prefer `?handoff=`; no `auto=1` in user links).
5. If Playwright fails, return teachany.cn/pbl link per fallback — still no `auto=1`.

## Output template

```markdown
## PBL 拆解结果

**项目**：{goal}

![PBL 知识路径拆解]({png_path})

- **图谱节点**：{nodeCount}（课标 {matched} · 外部 {external}）
- **继续编辑**：[在 TeachAny 打开]({edit_url})
```

## Additional resources

- Skill package: https://github.com/weponusa/teachany-pbl
