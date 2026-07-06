# TeachAny Community Courseware | 社区课件共享

TeachAny 社区课件允许用户把自己制作的互动课件发布到 `community/`，通过自动质检后出现在 Knowledge Map、Learning Path 和 Gallery 中。

## 推荐发布流程（零配置）

```text
在 AI 助手（WorkBuddy / Cursor / CodeBuddy 等）加载 TeachAny Skill
  ↓
生成课件（含 index.html + manifest.json）
  ↓
用户确认发布
  ↓
python3 scripts/submit-to-community.py <course-id>
  或浏览器：导入课件 → 我的 → 导入的 → 「提交到社区」
  ↓
POST https://teachany-community.pages.dev/api/submit
  ↓
GitHub Actions 开 PR → v7.3 质检 → 自动合并
  ↓
community-publish.yml 解包 → rebuild-index → Gallery 可见
```

**网页「制作课件」按钮不会自动上传**，只复制提示词并记录本地制作意图。

## 浏览器提交（无需 Python）

### 1. 导入课件（三选一）

| 入口 | 操作 |
|------|------|
| [Gallery](../index.html) | 拖入 `.teachany` / `.zip` / `.html`，或点社区区「➕ 添加我的课件」 |
| [我的 → 导入的](../my.html#imported) | 点「📦 导入课件」 |
| [知识地图](../tree.html) | 点击节点 →「📦 上传课件」 |

导入后课件保存在**本机浏览器**（IndexedDB），不会自动上传。

### 2. 提交到社区

1. 打开 [我的 → 导入的](../my.html#imported)
2. 点击课件卡片上的 **「🌐 提交到社区」**
3. 填写作者名；浏览器会先跑 **v7.3 教学质量预检**（与 CLI 相同规则）
4. 等待 GitHub Actions 二次质检并自动合并

**要求**：课件包须含 `index.html`、`manifest.json`，且 `manifest` 含 `node_id` / `name` / `subject` / `grade`；整包 ≤ 5 MB；须通过 v7.3 教学质量闸门（有效讲解文本、前测后测、课标对齐等）。

## 命令行提交

```bash
# 课件在 community/<course-id>/ 或 community/drafts/<course-id>/
python3 scripts/submit-to-community.py <course-id> --author "张老师" --message "欢迎审阅"

# 仅打包预览，不提交
python3 scripts/submit-to-community.py <course-id> --dry-run

# 高级：直连 GitHub（绕过 Worker）
TEACHANY_DIRECT_TOKEN=ghp_xxx python3 scripts/submit-to-community.py <course-id>
```

提交 API（默认，国内可访问）：`https://teachany-community.pages.dev/api/submit`

> 旧地址 `teachany-submit.weponusa.workers.dev` 已弃用（中国大陆 SNI 阻断）。

## 质检规则（CLI / 浏览器 / CI 统一）

三层校验，规则对齐 `scripts/validate-teaching-quality.py`：

1. **浏览器提交前**：`community-quality-gate.js` 预检（阻止明显不合格课件）
2. **CLI 提交前**：`submit-to-community.py` 运行同一 Python 闸门 + WebP 压缩
3. **PR 合并前**：`community-review.yml` 解包后再次运行 Python 闸门 + 假占位资产检测

本地自测：

```bash
python3 scripts/validate-teaching-quality.py community/<course-id>
```

## 在 Gallery 中查看用户课件

打开 [Gallery](../index.html)，在筛选栏选择 **「👤 用户共创」**。用户提交的课件带「用户共创」标签，并按最新上传时间排序。

## 提交规范

1. **质量要求**
   - 单文件 HTML 或 `.teachany` 课件包均可。
   - 必须包含学习目标、知识模块和测评。
   - 必须遵循 TeachAny 设计系统。
   - 必须声明 `<meta name="teachany-node">` 并匹配知识地图节点 ID。

2. **元数据要求**

   ```html
   <meta name="teachany-subject" content="math">
   <meta name="teachany-grade" content="8">
   <meta name="teachany-node" content="linear-function">
   <meta name="teachany-author" content="your-name">
   <meta name="teachany-version" content="1.0.0">
   ```

3. **文件大小**
   - 浏览器/Worker 提交：≤ 5 MB（`.teachany` zip）
   - CI pending 包上限：50 MB

4. **内容要求**
   - 原创或有合法授权。
   - 不包含未授权图片、视频、广告或外部追踪。
   - 内容适合 K-12 学生。

## 维护者手动发布（不推荐普通用户）

仓库维护者可直接将课件放入 `community/<course-id>/` 后运行索引重建：

```bash
python3 scripts/rebuild-index.py
git add -A
git commit -m "feat: 新增课件 <course-id>"
git push origin main
```

普通用户请走 Worker 流水线，以便自动质检与 PR 留痕。

## 同节点多课件

同一个知识节点可以挂载多份社区课件。`rebuild-index.py` 会基于 `manifest.json` 的 `node_id`、`author`、`variant`、`version` 自动整理 Registry 和知识树引用。

## 目录结构

```text
community/
├── <course-id>/         # 已发布社区课件
│   ├── index.html
│   ├── manifest.json
│   └── assets/
├── pending/             # 提交流水线暂存（CI 自动处理，勿手改）
├── drafts/              # 本地草稿，可预览后再发布
├── archive/             # 历史归档
└── README.md
```

## 相关文档

- [社区提交部署说明](../docs/COMMUNITY_SUBMIT_SETUP.md) — Pages Functions 部署
- [scripts/submit-to-community.py](../scripts/submit-to-community.py) — 命令行提交工具
- [scripts/community-submit-browser.js](../scripts/community-submit-browser.js) — 浏览器提交
- [scripts/community-quality-gate.js](../scripts/community-quality-gate.js) — 浏览器 v7.3 预检
