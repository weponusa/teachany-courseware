# TeachAny · 腾讯云主站镜像 — 服务器初始化

> 适用：全新腾讯云轻量应用服务器 / CVM（Ubuntu 22.04+ 或 Debian 12+）。
> 全程 root；纯静态站，1C1G 足够，磁盘 ≥10GB（站点 3.9GB）。

## 1. 装 nginx 并落配置

```bash
apt update && apt install -y nginx rsync
```

把 `scripts/nginx-teachany.conf` 放到服务器 `/etc/nginx/sites-available/teachany`：

```bash
# 本地执行（TENCENT_HOST 换成服务器 IP）
scp -P 22 scripts/nginx-teachany.conf root@TENCENT_HOST:/etc/nginx/sites-available/teachany
ssh -p 22 root@TENCENT_HOST '
  ln -sf /etc/nginx/sites-available/teachany /etc/nginx/sites-enabled/teachany
  rm -f /etc/nginx/sites-enabled/default
  mkdir -p /var/www/teachany
  nginx -t && systemctl reload nginx
'
```

## 2. 首次同步

```bash
# 本地（或 scripts/.tencent-deploy.env 里固化变量）
TENCENT_HOST=TENCENT_HOST_IP bash scripts/deploy-tencent.sh /tmp/teachany-site-build
# 3.9GB 首传约 10-30 分钟（视带宽），之后增量秒级
```

## 3. 验证

```bash
curl -I http://TENCENT_HOST_IP/community/phy-m-resistance/   # 200
curl -I http://TENCENT_HOST_IP/assets/scripts/courseware-shell.css  # 200
```

## 4. 切流量（三选一，按备案与权限情况）

| 方案 | 条件 | 操作 |
| --- | --- | --- |
| **A. CF 回源切腾讯**（推荐，改动最小） | 域名已 ICP 备案 | Cloudflare → DNS → A 记录指向腾讯 IP（灰度/代理模式均可）；GitHub Pages 保留为回退镜像 |
| **B. DNSPod 直连国内** | 域名已 ICP 备案，要极致国内速度 | 域名 DNS 迁到 DNSPod，A 记录直指腾讯 IP；CF 退役为纯镜像 |
| **C. 未备案过渡** | 域名未备案 | 腾讯云 80/443 会被阻断，只能继续走 CF（CF 在境外回源腾讯 IP）或暂维持现状等备案 |

> **备案提醒**：teachany.cn 若未 ICP 备案，腾讯云国内服务器的标准 Web 端口会被服务商标识阻断。备案可在腾讯云控制台免费办理（个人主体，约 1-2 周）。

## 5. 自动同步

`.github/workflows/deploy-tencent.yml` 已就位：push main → 构建 _site → rsync 到服务器。
首次启用需在 GitHub 仓库 Settings → Secrets 添加：

| Secret | 值 |
| --- | --- |
| `TENCENT_HOST` | 服务器 IP |
| `TENCENT_USER` | SSH 用户（root） |
| `TENCENT_PORT` | SSH 端口（22） |
| `TENCENT_SSH_KEY` | 私钥全文（本地 `ssh-keygen -t ed25519 -f tencent_deploy` 生成，公钥放服务器 `~/.ssh/authorized_keys`） |

未配置 Secret 时该工作流自动跳过，不影响现有链路。

## 6. 回退

任何问题把 Cloudflare DNS 的 A 记录改回原值（或切回 GitHub Pages 源），1 分钟内生效。腾讯云仅作镜像期间可随时下线。
