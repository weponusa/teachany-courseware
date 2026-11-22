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

### 备用通道：`deploy-tencent.yml`

`.github/workflows/deploy-tencent.yml` 仅在配置了 `TENCENT_HOST` / `TENCENT_SSH_KEY`
且该来源被安全组放行时才真正同步。未配置时会打 `::warning::` 并跳过实际步骤，
**其 success 只表示「已检查并跳过」，不代表镜像已同步**。默认 SSH 端口为 `36000`。

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
- `audio.teachany.cn` 根路径 404 与本次主域切换无关，待单独确认。
- CF DNS 上两条 DNS-01 遗留 `_acme-challenge` TXT 可择期清理，保留无害。
