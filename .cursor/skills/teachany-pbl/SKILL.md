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
2. **Edit URL** — `https://www.teachany.cn/pbl?...` for chat refinement, node tweaks, courseware

The decomposition uses TeachAny's six-stage pipeline on teachany.cn (LLM + curriculum index). Do not invent knowledge nodes yourself.

## Workflow

1. Parse the user's project task and optional fields (see [references/parameters.md](references/parameters.md)).
2. Run the bundled CLI — prefer the standalone skill repo if cloned:

```bash
# 独立仓库（推荐）: github.com/weponusa/teachany-pbl
python3 scripts/pbl-decompose.py --goal "..." --grade junior -o ./pbl-output

# 或本仓 scripts/
python3 /path/to/teachany-courseware/scripts/pbl-decompose.py --goal "..." -o ./pbl-output
```

3. On first run: `pip install playwright && playwright install chromium`
4. Reply with PNG path, node counts, and **edit_url** (no `auto=1` in user links).
5. If Playwright fails, build edit URL per parameters — still return teachany.cn/pbl link.

## Output template

```markdown
## PBL 拆解结果

**项目**：{goal}

![PBL 知识路径拆解]({png_path})

- **图谱节点**：{nodeCount}（课标 {matched} · 外部 {external}）
- **继续编辑**：[在 TeachAny 打开]({edit_url})
```

## Additional resources

- Full skill package: https://github.com/weponusa/teachany-pbl
