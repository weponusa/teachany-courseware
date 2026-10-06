# PBL Map

基于 [TeachAny](https://www.teachany.cn) PBL 拆解引擎的**小初高项目式学习地图**工具。

覆盖 CN 课标 **小学 · 初中 · 高中**（1189 节点），并补充 **信息科技** 独立课标树（小 16 + 初 14 + 高 10 = 40 节点）。音体美暂不纳入审计范围。

## 节点规模

| 学段 | 节点数 | 主要学科 |
|------|--------|----------|
| 小学 | 263 | 语数英科道法心理 + **信息科技 16** |
| 初中 | 367 | 语数英物化生史地政心理 + **信息科技 14** |
| 高中 | 559 | 语数英物化生史地政心理 + **信息科技 10** |

信息科技树来源：
- 小学/初中：`data/trees/cn/{elementary,middle}/info-tech.json`（PBL Map 补充，对齐 2022 课标）
- 高中：`engine/data/trees/cn/high/info-tech.json`（TeachAny 已有）

## 快速开始

```bash
node scripts/build-cn-k12-index.mjs   # 生成 data/cn-k12-nodes.json
npm run build:k12                     # 生成 24 学期覆盖包 + K12 目录
npm run build:decompose               # 生成 104 子 PBL 拆解材料
npm run serve                         # http://localhost:3456

## 挂载到 TeachAny（teachany.cn）

TeachAny 首页已增加 **K12 PBL Map** 入口（导航栏 · Hero 标签 · 产品筛选）。

本地联调时在 `teachany-courseware` 根目录创建 symlink：

```bash
ln -sfn ../../finalpbl /path/to/teachany-courseware/pbl-map
```

访问：`https://teachany.cn/pbl-map/index.html`（或本地 `http://localhost:PORT/pbl-map/index.html`）

生产部署需将 `finalpbl` 目录一并发布到站点 `pbl-map/` 路径（symlink 或 CI 拷贝均可）。
```

## K12 完整材料（v2 · 学期覆盖包）

**每学期 = 1 覆盖包 = K 个子 PBL**（G1–G12 共 24 包、104 子项目）。节点无交叠；学生个人台账 `gap=0` 过关。

| 入口 | 说明 |
|------|------|
| [`catalog.html`](catalog.html) | 交互目录：24 学期包 · 展开子 PBL · 按学段筛选 |
| [`decompose.html`](decompose.html) | **104 子 PBL 拆解目录** · 按年级浏览 |
| [`demo.html?project=g1-autumn-p1`](demo.html?project=g1-autumn-p1) | 单个子 PBL 拆解演示 |
| [`roadmap.html`](roadmap.html) | 小学 6 年多 PBL 覆盖推演 |
| [`docs/K12-PBL-CURRICULUM.md`](docs/K12-PBL-CURRICULUM.md) | Markdown 全文（可打印/分享） |
| [`data/k12-pbl-curriculum.json`](data/k12-pbl-curriculum.json) | 机器可读索引 |
| [`docs/MULTI-PBL-FULL-COVERAGE.md`](docs/MULTI-PBL-FULL-COVERAGE.md) | 多 PBL 人人全覆盖设计说明 |

重新生成：`npm run build:k12` · 拆解材料：`npm run build:decompose`

## Phase 1 样例

| 样例 | 入口 |
|------|------|
| G3 覆盖包 | [`pack.html?id=g3-autumn-pack`](pack.html?id=g3-autumn-pack) |
| G3 策划包 | [`plan.html?id=g3-our-campus`](plan.html?id=g3-our-campus) |
| G5 拆解演示 | [`demo.html?id=g5-community-map`](demo.html?id=g5-community-map) |

- 文档：`docs/PRD.md` · `docs/IA.md`

## 三种工作模式

1. **项目驱动** → `engine/pbl.html`
2. **课标驱动** → `coverage.html?mode=curriculum`（按学段/学科筛缺口）
3. **地图驱动** → `coverage.html?mode=map`

## 数据结构

```
data/
├── cn-k12-nodes.json              # 小初高课标索引（主文件）
├── k12-pbl-curriculum.json        # 24 学期覆盖包索引（v2）
├── plans/
│   ├── {semester-id}-pack.json    # 24 个学期覆盖包
│   ├── k12-full-roadmap.json      # 全周期推演
│   ├── primary-6year-roadmap.json # 小学 6 年推演
│   ├── g3-our-campus.json       # 策划包样例
│   └── g5-community-map.json    # 拆解演示样例
├── pbl-semester-pack.schema.json
└── semester-themes.json
docs/
└── K12-PBL-CURRICULUM.md          # 完整材料（Markdown）
```

## 排除学科

覆盖审计**不包含**：`art` · `pe` · `music` · `design`（音体美等后续再补）

## 许可

TeachAny 引擎遵循原仓库许可；本扩展层 MIT。
