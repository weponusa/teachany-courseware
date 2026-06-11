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
  或浏览器：我的 → 导入的 → 「提交到社区」
  ↓
POST https://teachany-community.pages.dev/api/submit
  ↓
GitHub Actions 开 PR → 自动质检 → 自动合并
  ↓
community-publish.yml 解包 → rebuild-index → Gallery 可见
```

**网页「制作课件」按钮不会自动上传**，只复制提示词并记录本地制作意图。

## 浏览器提交（无需 Python）

1. 将完成的 `.teachany` 课件导入到本站（Gallery 拖入或「我的」页）
2. 打开 [我的 → 导入的](../my.html#imported)
3. 点击课件卡片上的 **「提交到社区」**
4. 填写作者名，等待自动质检合并

要求：课件包须含 `index.html`、`manifest.json`，且 `manifest` 含 `node_id` / `name` / `subject` / `grade`；整包 ≤ 5 MB。

## 命令行提交

```bash
# 课件在 community/<course-id>/ 或 community/drafts/<course-id>/
python3 scripts/submit-to-community.py <course-id> --author "张老师" --message "欢迎审阅"

# 高级：直连 GitHub（绕过 Worker）
TEACHANY_DIRECT_TOKEN=ghp_xxx python3 scripts/submit-to-community.py <course-id>
```

Worker 地址（默认）：`https://teachany-community.pages.dev/api/submit`

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

- [社区提交部署说明](../docs/COMMUNITY_SUBMIT_SETUP.md) — Worker 一次性部署
- [scripts/submit-to-community.py](../scripts/submit-to-community.py) — 命令行提交工具
- [scripts/community-submit-browser.js](../scripts/community-submit-browser.js) — 浏览器提交
