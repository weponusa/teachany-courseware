# PBL Map — 信息架构

```
PBL Map
├── 首页 index.html          模式入口 + 统计
├── 目录 catalog.html        24 学期覆盖包 · 子 PBL 列表
├── 覆盖包 pack.html?id=…    单学期 K 子 PBL + 个人台账
├── 推演 roadmap.html        小学 6 年多 PBL 可行性
├── 策划包 plan.html?id=…    单项目教研样例（可挂到子 PBL）
├── 拆解目录 decompose.html    104 子 PBL 拆解材料索引
├── 拆解演示 demo.html?project= 单个子 PBL 五步拆解 walkthrough
├── 学生自主 student.html    主题壳 + 驱动问 → TeachAny
├── 覆盖看板 coverage.html   课标驱动 / 地图驱动
├── 班级差异度 class.html    同主题 Jaccard
└── TeachAny engine/pbl.html 拆解执行层
```

## 数据流

```
cn-k12-nodes + semester-themes
        ↓
build-k12-pbl-curriculum.mjs
        ↓
data/plans/{semester}-pack.json（学期覆盖包）
data/k12-pbl-curriculum.json（24 包索引）
        ↓
学生完成子 PBL → personalLedger（M/C/gap）
        ↓
学期关门：personalLedger.gapCount === 0
        ↓
buildCoverageMatrix（班级/学校审计）
```

## 学期覆盖包 Schema（概要）

| 字段 | 说明 |
|------|------|
| `id` | 如 `g11-spring-pack` |
| `model` | `semester-coverage-pack` |
| `themeShell` | 主题链、驱动问、周期、约束 |
| `projects[]` | K 个子 PBL：`mandatoryNodeIds` · `certifiedNodeIds` |
| `partitionRule` | `disjoint-union-equals-semester-pool` |
| `completionRule` | 学生/项目/学期关门条件 |
| `personalLedgerSchema` | M · C · gap 状态机 |

## 策划包 JSON（子 PBL 样例）

| 字段 | 说明 |
|------|------|
| `id` | 如 `g3-our-campus` |
| `projectMode` | `cross-disciplinary` |
| `project` | TeachAny `subject=cross` |
| `coverageAnchors[]` | 教研审计用（`auditOnly: true`） |

策划包通过 `projects[].planRef` 挂接到学期覆盖包的某一子 PBL。
