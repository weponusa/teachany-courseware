# 仓库瘦身与媒体策略

> **当前策略**：课件媒体（mp3/mp4/png 等）**继续留在本仓库**，通过 GitHub → teachany.cn 同源路径发布；**不做媒体外置**。  
> 仅清理 Git **历史中的垃圾路径**，并优化工作区跟踪规则。

## 发布链路（不变）

| 环节 | 说明 |
|------|------|
| 源码 | `weponusa/teachany-courseware` → `main` |
| 站点 | [https://www.teachany.cn/](https://www.teachany.cn/)（`deploy-pages.yml` → `gh-pages`） |
| 课件 URL | `https://www.teachany.cn/community/<id>/index.html` |
| 媒体 URL | `https://www.teachany.cn/community/<id>/tts/…`、`…/assets/video/…`（相对路径，无需 CDN） |

`deploy-pages.yml` 会 rsync 整个 `community/`（媒体在内）。**不要**从 Git 删除正常课件媒体，否则线上会直接 404。

## 历史瘦身（推荐流程）

**会改写历史**，协作者需重新 `clone`；只 `force-push` 到 GitHub `origin`，不再使用 Gitee。

### 1. 提交当前工作区

```bash
git status   # 须干净
```

### 2. 备份

```bash
./scripts/backup-and-slim-github-history.sh backup-only
```

产出目录默认：`../teachany-courseware-backups/`（`git-bundle-*.bundle` + `community-media-*.tar.gz`）。

### 3. 清理历史（默认保留所有课件媒体）

```bash
./scripts/backup-and-slim-github-history.sh slim
```

从**全部提交**中移除（不影响当前 HEAD 里的正常媒体）：

| 路径 | 原因 |
|------|------|
| `_archive_*/**` | 一次性备份 |
| `**/remotion/out/**` | 可再生渲染产物 |
| `**/remotion/.remotion/**` | Remotion 缓存 |
| `community/archive/duplicates-*/**` | 重复归档 |
| `community/archive/pending-duplicates-*/**` | 待处理重复 |
| `community/*/*.teachany` | 应解包后的提交包，不应进树 |
| `community/*/**/.teachany` | 同上 |

可选（约再减 60MB 历史，**不部署到 teachany.cn**）：

```bash
./scripts/backup-and-slim-github-history.sh slim --with-physical
```

会去掉 `assets/maps/physical/**`；地理课本地用图见 `assets/maps/README.md` 重新下载说明。

### 4. 推送

```bash
git push origin main --force
```

### 5. 仅做 GC（已 slim 过）

```bash
./scripts/backup-and-slim-github-history.sh gc
```

## 工作区维护

### 占位媒体

```bash
python3 scripts/audit-and-clean-placeholder-media.py          # 审计
python3 scripts/audit-and-clean-placeholder-media.py --apply  # 删除 0 字节 mp3、假 mp4 等
```

删除后对相关课件重新跑 TTS/Remotion（`references/media-pipeline.md`）。

### 幻灯片页码

```bash
python3 scripts/fix-slide-page-index.py
```

### `.gitignore`（已配置）

- `**/remotion/out/`、`_archive_*/`、`community/archive/duplicates-*`
- `community/*/*.teachany`（`community/pending/*.teachany` 仍可用于提交流程）

## 预期效果说明

| 项目 | 说明 |
|------|------|
| 历史垃圾清理 | 约减 **80–120MB** 量级（归档 + 旧 remotion + teachany 包等） |
| 主体积 | **community 媒体仍在 pack 中**，`.git` 仍可能 **~1GB+** —— 这是「媒体在仓内」的正常结果 |
| 若要 **<300MB** 的 Git 仓 | 只能二选一：媒体外置，或接受 LFS/更大 GitHub 配额 |

**媒体外置**仅在未来 GitHub/Pages 硬超限再考虑；当前文档与脚本默认 **不外置**。

## 高中历史三课样本

| 课件 | 状态 |
|------|------|
| `ancient-china-h` | 时间轴 + 3 互动 + 5 题；`tts/` 正常 |
| `hist-h-ancient-civ` | 考古排序 + 社会复杂度模拟 + 证据分类 |
| `hist-h-early-state` | 政治演进排序 + 王权模拟 + 材料分类 |
