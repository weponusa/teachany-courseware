# 中国课标缺口课件生成计划（v1）

更新时间：2026-05-31

## 1. 当前盘点

- 范围：`data/trees/cn/**`
- 总节点：`985`
- 已有课件：`685`
- 缺口节点：`300`
- 覆盖率：`69.5%`

缺口最多的树（Top）：

1. `cn/high/history.json`：34
2. `cn/middle/geography.json`：31
3. `cn/middle/history.json`：31
4. `cn/high/chinese.json`：30
5. `cn/high/english.json`：30
6. `cn/middle/english.json`：27
7. `cn/elementary/science.json`：21

## 2. 目标与原则

目标：仅做中国课标，把 300 个缺口节点全部补齐并挂树。

执行原则：

- 先覆盖，再提质：先做到每个缺口有可用课件，再做音视频/互动升级。
- 课标内节点必须挂正式课标树；不走 `other/user-generated`。
- 每个课件完成后先问用户是否上传：不拒绝才上传挂树。

## 3. 分批策略

### 批次 A（高优先，100 节点）

- 高中历史（34）
- 初中地理（31）
- 初中历史（31）
- 初中英语（4，先补关键题型）

### 批次 B（中优先，100 节点）

- 高中语文（30）
- 高中英语（30）
- 初中英语（剩余 23）
- 小学科学（17）

### 批次 C（收尾，100 节点）

- 小学科学（剩余 4）
- 高中信息技术（8）
- 高中生物（8）
- 高中数学（13）
- 高中化学（10）
- 高中物理（10）
- 初中生物（6）
- 初中物理（6）
- 初中语文（5）
- 初中化学（5）
- 高中地理（4）
- 小学语文（8）
- 小学英语（6）
- 小学数学（4）
- 初中数学（3）

## 4. 每节点流水线（标准）

1. 定位节点：`node_id + name + grade + subject`
2. 生成课件：`community/<course-id>/index.html + manifest.json`
3. 质检：`validate-courseware` + 可打开性检查
4. 用户确认：是否上传
5. 上传后挂树：`rebuild-index.py`
6. 验证：URL 200 + 对应树 `status=active` 且 `courses` 包含新 ID

## 5. 每日节奏

- 日产目标：20-35 节点（按学科难度浮动）
- 每日交付：
  - 新增节点数
  - 失败节点与原因
  - 待你确认上传的课件列表
  - 已上线 URL 与挂树校验结果

## 6. 第一批（立即开工，30 节点）

建议先从 `cn/high/history.json` 开始，先打通高中文综主干（以下为当前树内真实缺口 ID）：

1. `ancient-china-h`（中国古代史）
2. `hist-h-ancient-civ`（中华文明起源）
3. `hist-h-early-state`（早期国家）
4. `hist-h-pre-qin`（先秦）
5. `hist-h-feudal-system`（秦汉统一与中央集权）
6. `hist-h-qin-han-empire`（秦汉帝国）
7. `hist-h-wei-jin-tang`（三国两晋南北朝与隋唐）
8. `hist-h-ancient-economy`（古代经济）
9. `hist-h-ancient-culture`（古代思想文化）
10. `hist-h-ancient-thought`（古代思想文化专题）
11. `modern-china-h`（中国近现代史）
12. `hist-h-opium-war-h`（鸦片战争）
13. `hist-h-semi-colonial`（半殖民地半封建形成）
14. `hist-h-reform-revolution-h`（戊戌变法与辛亥革命）
15. `hist-h-xinhai-modern`（辛亥革命与民国）
16. `hist-h-new-democracy`（新民主主义革命）
17. `hist-h-prc-establishment`（新中国成立）
18. `hist-h-reform-opening`（改革开放）
19. `world-ancient-h`（世界古代中世纪史）
20. `hist-h-medieval-h`（中古时期）
21. `world-modern-h`（世界近现代史）
22. `hist-h-age-of-exploration`（新航路与殖民扩张）
23. `hist-h-enlightenment`（启蒙运动）
24. `hist-h-bourgeois-revolution`（资产阶级革命）
25. `hist-h-marxism-russian`（马克思主义与俄国革命）
26. `hist-h-colonialism-liberation`（殖民体系与民族解放）
27. `hist-h-two-world-wars`（两次世界大战）
28. `hist-h-globalization-h`（全球化与多极化）
29. `thematic-history`（专题史）
30. `hist-h-political-system-evolution`（中外政治制度演变）

> 生成前统一做 `node_id` 校验，确保与树 ID 完全一致后再批量产出。

