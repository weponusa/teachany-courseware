# TeachAny · 国内主站与 Cloudflare Pages 双端运维

> **现行状态（2026-11-22）**：`teachany.cn` / `www.teachany.cn` 已切到国内腾讯云 CVM `43.139.66.238`，
> Cloudflare Pages 继续作为境外镜像与回退入口。ICP 备案号 `京ICP备2026008947号-2`。
> 本文档描述**已上线的实际架构**；早期「Ubuntu 全新服务器初始化 / 未备案过渡 / 端口 22」的内容已废弃。

## 1. 架构

```
用户 ── Cloudflare 权威 DNS（DNS only / 灰云）──> 43.139.66.238  腾讯云 CVM（广州）
                                                    │
        ┌───────────────────────────────────────────┼───────────────────────────────────────┐
        │ 静态：nginx 1.14.1  root /var/www/teachany（9639 文件 / 1.41GB）                 │
        │ /api/：反代 → https://teachany-courseware.pages.dev → Pages Functions + D1/KV     │
        └───────────────────────────────────────────┬───────────────────────────────────────┘
                                                    │
push main ─> deploy-pages.yml 构建 _site ─> gh-pages 分支 ─> Cloudflare Pages 自动发布
                                    └──────> CVM cron 每 10 分钟主动拉取 gh-pages（同源同版本）
```

两边消费的是**同一份 `gh-pages` 产物**，不是两次独立构建，因此不存在版本漂移。

| 项 | 值 |
| --- | --- |
| 权威 DNS | Cloudflare（NS 未迁） |
| DNS 记录 | `teachany.cn` / `www.teachany.cn` → `A 43.139.66.238`，DNS only |
| 未改动的子域 | `audio` / `read` / `mcp`、`_acme-challenge` 与 `_dnsauth` TXT |
| 服务器 | TencentOS，nginx 1.14.1，sshd `36000`，站点 `/var/www/teachany` |
| 证书 | Let's Encrypt ECC，SAN `teachany.cn` + `www.teachany.cn`，HTTP-01 webroot 自动续期 |
| 动态层 | `functions/api/**` 依赖 Cloudflare D1 绑定与 secrets，保留在 Pages Functions |

## 2. 双端同步机制

### 主通道：CVM 主动拉取 `gh-pages`

服务器脚本 `/usr/local/bin/teachany-sync.py`（源码见 `out/备案切换/teachany-sync.py`），
cron 每 10 分钟执行一次，`flock` 防并发，日志 `/var/log/teachany-sync.log` 按月轮转：

```cron
*/10 * * * * flock -n /tmp/teachany-sync.lock /usr/bin/python3 /usr/local/bin/teachany-sync.py >> /var/log/teachany-sync.log 2>&1
```

工作流程：

1. 取 `branches/gh-pages` 的 commit sha，与 `/var/lib/teachany-sync/last_sha` 比较；相同即退出。
2. 取 `git/trees/<sha>?recursive=1` 得到每个 blob 的 git sha1。
3. 本地逐文件计算 `sha1("blob <len>\0" + data)` 比对，得出「需下载 / 需删除」。
4. 差异文件从 `raw.githubusercontent.com/<repo>/<sha>/<path>` 并发下载到临时目录，
   **逐个校验 blob sha 之后**才原子替换到站点根，再删除多余文件。
5. 任一步失败都保留旧 state，下次 cron 自动重试；线上文件不会被批量破坏。

安全阀：`truncated=true`、blob 数 < 5000、单次变更 > 3000 文件（除非 `--full`）一律中止。

```bash
python3 /usr/local/bin/teachany-sync.py --dry-run --force  # 只看差异
python3 /usr/local/bin/teachany-sync.py --force            # 强制全量比对并自愈
cat /var/lib/teachany-sync/last_sha
```

选用「服务器主动拉」而非「Actions 推送」的原因：CVM 的 SSH 36000 端口按白名单放行，
GitHub Actions runner 出口是大段动态 Azure 网段，放行成本与风险都过高；
而 `github.com` 从 CVM 直连超时、`api.github.com` 与 `raw.githubusercontent.com` 均可达，
故走 trees API + raw 下载，零入站端口、零私钥托管。

### 备用通道：`deploy-tencent.yml`（当前未启用）

`.github/workflows/deploy-tencent.yml` 仅在配置了 `TENCENT_HOST` / `TENCENT_SSH_KEY`
且该来源被安全组放行时才真正同步。**实测仓库 Actions secrets 为 0**，因此每次 push
该工作流都会显示 `success`，但 `Checkout / Build / Setup SSH / Rsync` 四步全部 `skipped`
—— 是假成功，**不代表镜像已同步**。

该文件内的默认 SSH 端口仍是 `22`、跳过提示仍是普通日志而非 `::warning::`。
2026-11-22 曾尝试修正，但当前 Git 凭据为 OAuth App token
（scopes 仅 `admin:public_key, gist, read:org, repo`，缺 `workflow` scope），
`git push` 与 REST contents API 均被 GitHub 以 403 拒绝，故保持原样。
**这不影响主同步通道**：日常同步完全由上面的 CVM cron 承担，无需任何 GitHub Secrets。

如需修正该文件，使用带 `workflow` scope 的凭据，或在 GitHub 网页直接编辑
（网页会话不受此 scope 限制）。

### 日常不需要任何手工操作

push `main` → Pages 构建并发布 → 最多 10 分钟内 CVM 自动同步。

### 紧急手动兜底

```bash
cd /path/to/teachany-courseware
bash scripts/build-publish-site.sh _site
rsync -az --delete --delete-excluded --stats \
  -e "ssh -i /Users/wepon/.ssh/tencent_deploy -p 36000 -o StrictHostKeyChecking=no -o BatchMode=yes" \
  _site/ root@43.139.66.238:/var/www/teachany/
```

> `scripts/deploy-tencent.sh` 默认端口 22 且不带 `-i`，不要直接裸跑。
> 本地 `_site` 会多带 9 个开发日志/临时文件（不在 `gh-pages` 里），cron 下次会自动清掉。

## 3. nginx 要点

配置源：`out/备案切换/nginx-teachany-https.conf`，服务器副本 `/etc/nginx/conf.d/teachany.conf`。

- nginx 1.14.1 必须用 `listen 443 ssl http2;`，**不能用 `http2 on;`**（1.25.1+ 才有）。
- `_redirects` 只在 Cloudflare Pages 生效，切到 nginx 后已补等价 server 级 rewrite：
  裸域→www、`/teachany/*`、`/community/*/index.html`、`/submit`、`/reading-academy/*`、`reading.html`。
- `try_files $uri $uri.html $uri/ $uri/index.html =404;` 恢复 Pages 的 pretty URL，保证 `/pbl?auto=1` 可用。
- `/api/` 反代必须写**纯静态** `proxy_pass https://teachany-courseware.pages.dev;`。
  nginx 1.14.1 中只要 `proxy_pass` 含变量（如 `$request_uri`）就按变量形式处理并要求 `resolver`，
  否则运行时报 `no resolver defined to resolve ...` 并 502。
- 原有 `/etc/nginx/conf.d/mcp-gateway.conf`（按 `server_name 43.139.66.238` 服务 MCP 网关）**不要覆盖**。
- 80 端口保留 `location /.well-known/acme-challenge/ { root /var/www/letsencrypt; }` 供证书续期。

## 4. 证书

acme.sh 已从手动 DNS-01 切换为 HTTP-01 webroot，`Le_Webroot=/var/www/letsencrypt`，
续期由 acme.sh 自带的 cron（每天 2/8/14/20 点的 27 分）自动完成，无需 Cloudflare API Token。

```bash
/root/.acme.sh/acme.sh --list       # 查看 Renew 时间
/root/.acme.sh/acme.sh --cron       # 手动触发续期检查
openssl x509 -in /etc/letsencrypt/live/teachany.cn/fullchain.pem -noout -dates -ext subjectAltName
```

## 5. 验证判据

```bash
dig @119.29.29.29 +short www.teachany.cn A            # 43.139.66.238
curl -sSI https://www.teachany.cn/ | grep -i server    # nginx/1.14.1
curl -sS https://www.teachany.cn/ | grep -o '京ICP备[0-9]*号-[0-9]*'
curl -sS -o /dev/null -w '%{http_code} %{ssl_verify_result}\n' https://www.teachany.cn/api/images/quota
curl -sS https://www.teachany.cn/registry.json | wc -c
```

已验证基线（2026-11-22）：6 个关键文件 sha256 本地/CVM 逐字节一致；
首页 200 / 0.24s / 36921B / `ssl_verify=0`；`/api/images/quota` 200（`d1_configured:true`）、
`/api/feedback/` 200；`registry.json` 1410254 B；裸域 301 保留查询串。

## 6. 回滚

Cloudflare DNS 把两条记录改回（约 1 分钟生效）：

```text
teachany.cn       CNAME  teachany-courseware.pages.dev   Proxied  Auto
www.teachany.cn   CNAME  teachany-courseware.pages.dev   Proxied  Auto
```

CVM 与其他子域保持不动。切换前务必确认 Pages 侧仍可访问。

## 7. 遗留事项

- 公安联网备案需本人实名办理（`https://beian.mps.gov.cn`）；审核通过拿到编号前，
  footer 中的公安号占位块保持注释状态，**不得上线假号**。
- ~~`audio.teachany.cn` 404~~ 已修复，见第 9 节。
- CF DNS 上两条 DNS-01 遗留 `_acme-challenge` TXT 可择期清理，保留无害。

## 8. 2026-11-22 端到端实测后的加固

用真实教学需求跑通全部功能线后，针对实测暴露的问题做了以下修正（详见
`out/e2e-2026-11-22/测试报告.md`）：

**同步脚本 `/usr/local/bin/teachany-sync.py`**：11:30 那轮 cron 检测到 1 个差异文件，
但从 `raw.githubusercontent.com` 单文件读取超时 180s 后整轮中断（旧 state 保留）。
现改为 `curl` 下载 + 四源回退（raw.githubusercontent.com →
`api.github.com/repos/.../git/blobs/<blob_sha>` → github.com/raw →
teachany-courseware.pages.dev）+ connect 15s / 单源 25s 超时 + 3 轮重试；
**任何来源都必须通过 git blob sha1 校验才允许落盘**，Pages 镜像若处于传播延迟
返回旧内容会被直接拒绝。**按 blob sha 取内容的 GitHub API 源不受任何传播延迟影响**，
是第二轮 11:50 再次遇到「raw 超时 + Pages 未更新」后补上的关键源。
落盘前统一 `chmod 644`，避免 600 权限文件被同步进来导致 nginx 403。
备份：`/root/teachany-sync.py.bak-e2e-20261122`。

**nginx `/etc/nginx/conf.d/teachany.conf`**（备份 `/root/conf.d.bak.e2e-20261122`）：

- `/community/*/index.html` 的 rewrite 改为只匹配原始 `$request_uri`，消除
  `try_files` 内部重写导致的 301 死循环；
- 新增精确 `location = /api/like` 反代 `teachany-community.pages.dev`（该 Function
  不在 courseware 项目中）；
- 静态文件权限统一 644（Cloudflare Pages 托管时不暴露此问题）。

**Gallery 封面**：发布构建会剔除「课件页面未引用、已有同名 webp」的 png，
而 `registry.json` 中 736 条 `hero_image` 仍指向 png。现由
`scripts/unified-loader.js` 优先请求同名 webp，并保留 webp↔png 双向兜底与
emoji 最终占位，消除卡片封面大面积 404。

**验证口径补充**：Actions success、HTTP 200、`cf-cache-status` 都不能作为上线判据；
自定义域有 5–10 分钟传播延迟，必须 `GET` 实际内容 grep 标记并逐字节比对。
`/api/` 的异常响应要与 `teachany-courseware.pages.dev` 直连对照，才能区分
「切换回归」与「上游既有状态」。

## 9. 2026-11-22 下午追加修复（真实需求 E2E 的后续）

**`audio.teachany.cn` TTS 全量 404 已修复**。根因不是 DNS 或自定义域绑定，而是
Cloudflare Pages 项目 `teachany-audio` 的**部署内容为空**（自定义域与 pages.dev 都返回
404 / 0B）。仓库本地仍保留 10,324 个 `community/*/tts/*.mp3`（2.36 GB），
课件引用 10,254 个 `https://audio.teachany.cn/<course-id>/tts/<file>.mp3`。

重建方式（硬链接镜像，不额外占磁盘）：

```bash
# 由 teachany-courseware/community 生成 out/audio-dist，保留 <course-id>/tts/ 路径
wrangler pages deploy out/audio-dist --project-name teachany-audio --commit-dirty=true
```

复验：`audio.teachany.cn/sci-e-bridge-structure/tts/s01-hero.mp3` →
`200 audio/mpeg 136944B`；课件页浏览器冒烟 `HTTP 4xx = 0`、audio 404 清零。
本机跨境链路偶发读取截断（已用多次请求与字节数确认文件本身完整），非服务端问题。

**课件 hero 生图改为本地 agent 能力**。`scripts/agnes-image-gen.py` 与 skill 内同名脚本
改为不联网的兼容层，转交新增的 `scripts/local-hero-image.py`：由本地图像生成能力
产出图片后，规范化为 1536×1024 PNG + webp 变体，写
`.teachany-image-gen-probe.json`（`source: local-agent-imagegen`）。
旧批量脚本可通过 `TEACHANY_LOCAL_IMAGE_DIR=<本地图片目录>` 离线运行。
线上 `functions/api/images/agnes.js` 保留给站点访客使用，与本地课件生成链路解耦。

**材料拆解学科错配已修复并双端部署**（`teachany-mcp`）：
`concepts.js` 补数学概念词表、收紧跨学科泛词、增加学科约束；
`segments.js` 收紧 `physics` / `comprehensive-practice` 等误判词；
`decompose.js` 把显式学科传给概念推断。本地 `npm test` 44/0；
Worker 与 Pages 两端均已重新部署，Pages 备用域实跑验证知识点全部回到数学、
命中 `math-m-linear-function` 真实课标原文。
