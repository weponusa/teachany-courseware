# TeachAny Courseware

TeachAny **官方网站与课件资产**仓库，部署到 [www.teachany.cn](https://www.teachany.cn/)（Cloudflare Pages 生产分支 `gh-pages`；`main` 推送经 GitHub Actions 构建 `_site/` 后 force-push 到 `gh-pages`）。

| 仓库 | 用途 |
|------|------|
| [weponusa/teachany-courseware](https://github.com/weponusa/teachany-courseware)（本仓） | Gallery、社区课件、`data/` 课标树、PBL API、知识地图 |
| [weponusa/teachany](https://github.com/weponusa/teachany) | 轻量 **Skill** 安装包（`teachany/` 目录），供 AI 工具本地制作课件 |

## 目录

- `community/`：社区课件
- `data/`：知识树、课标索引、PBL 数据、全科图谱
- `assets/`：地图、脚本、站点资源
- `functions/`：Cloudflare Pages Functions（如 PBL API）
- `scripts/`：构建、校验、发布工具

## 部署

- **生产**：Cloudflare Pages 关联 `gh-pages` 分支（预构建 `_site/`），自定义域 `www.teachany.cn`；勿将生产分支设为 `main`（文件数超限会导致部署失败）
- **Skill 安装**：请使用 [weponusa/teachany](https://github.com/weponusa/teachany)，不要从本仓安装 Skill

<!-- deploy-retrigger: 2026-10-02 上次 Pages 部署在 Deploy 步骤 exit 2，本地 build-publish-site.sh 复现通过（9926 文件 / 3.1G < 19000 上限），此行仅用于重新触发部署 -->

<!-- deploy-retrigger-2: 2026-10-02 上次 Deploy 步骤 rsync 侧 exit 2（第 2 次），重触发 -->
