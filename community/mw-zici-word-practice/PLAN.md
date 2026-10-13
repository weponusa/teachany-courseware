# 小学语文生字组词练习（明湾）· TeachAny 课件计划

## 定位

- **course_id**: `mw-zici-word-practice`
- **node_id**: `ext-7f3a91c2`（其他知识树 · 用户扩展知识点）
- **前置**: `chn-e-pinyin-reading`, `chn-e-char-recognition-1`
- **后续**: `chn-e-char-writing-1`, `chn-e-char-structure`

## 学习设计

- **问题锚点**: 按进度打印组词练习 / 分清三种字格 / 题量不足如何补词
- **核心互动**: 字格状态小测 + Canvas 示意 + 内嵌 `practice.html` 全功能练习工具
- **评估**: 前测式选择题（大地·「大」= 伴读字）

## 资产

| 资产 | 路径 |
| --- | --- |
| Hero 图 | `assets/hero-infographic.svg` |
| 流程图 | `assets/concept-diagram.svg` |
| TTS | `tts/s01–s03.mp3` |
| 练习引擎 | `practice.html`（源自 `语文生字练习.html`） |

## 发布说明

1. 将 `teachany-courseware/community/mw-zici-word-practice/` 复制到主仓 `teachany-courseware/community/`。
2. 合并 `data/trees/other/user-generated.json` 中的 `ext-7f3a91c2` 节点。
3. 运行 `rebuild-index.py` 后走 `teachany-publish.sh mw-zici-word-practice`（需 Phase 3.5 反馈密码与上传确认）。

## 本地预览

在 `teachany-courseware` 根目录启动静态服务后访问：

`/community/mw-zici-word-practice/index.html`

`assets` 已通过符号链接指向主仓 `teachany-courseware/assets`，标准模块脚本可正常加载。
