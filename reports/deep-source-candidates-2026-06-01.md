# deep_textbook_snippets 资料源候选与灌注方案

生成时间：2026-06-01 22:55

## 结论

当前中国课标 `866` 个节点已经全部有基础知识内容；还没有 `deep_textbook_snippets` 的节点有 `363` 个。后续不建议再用通用规则强灌，而应按学科接入更合适的资料源。

| 学科 | 总节点 | 已有 deep | 缺 deep | 推荐策略 |
|---|---:|---:|---:|---|
| 语文 | 130 | 0 | 130 | 公版文本库 + 篇目/技能映射，不用 OpenStax 写作指南硬灌 |
| 地理 | 72 | 0 | 72 | 地理 OER + AP Human Geography/Cambridge Geography + 地图案例库 |
| 英语 | 82 | 20 | 62 | Cambridge English + Common Core ELA + ESL/OER 语法自然拼读资源 |
| 历史 | 87 | 36 | 51 | 世界史/古代史 OER + 本地 AP/Cambridge 历史，避免无关 US History 误配 |
| 信息科技 | 10 | 0 | 10 | AP CSP/CSA + Cambridge Computing/ICT + Python/算法开放教材 |
| 数学 | 154 | 140 | 14 | 继续用 OpenStax + curriculum-standards，补几何/导数/统计专题 |
| 物理 | 96 | 82 | 14 | OpenStax 物理 + PhET/实验手册，补光学/声学/电磁工程类 |
| 生物 | 103 | 96 | 7 | OpenStax Biology/AP Biology，补初中人体/分类/跨学科实践 |
| 化学 | 83 | 81 | 2 | OpenStax Chemistry + 本地化学整理版，补原电池/制氧实验 |
| 科学 | 48 | 48 | 0 | 暂不优先 |

---

## 一、优先资料源

### 1. 语文：130 个缺 deep

**本地可用**

- `curriculum-standards/语文/`：102 个知识点 MD，适合作为课标与教学建议来源。
- `books/课标-整理版/cn/all/chinese.md`、`books/课标/md/chinese_curriculum.md`：学科课标源。
- `books/课标-整理版/cn/high/语文.md`：高中语文课标整理。

**建议新增/接入**

- `chinese-poetry` 开源古诗文数据集：适合古诗词背诵、意象、意境、诗歌鉴赏、文言文篇目。候选地址：`https://github.com/chinese-poetry/chinese-poetry`。
- 维基文库中文公版文本：适合古代诗文、古典散文、名著节选。候选地址：`https://zh.wikisource.org/`。
- 自建“语文技能样例库”：不要全靠教材；把语文节点分为拼音、识字、词语、句子、阅读、写作、古诗文、整本书阅读，每类写 20-50 条标准例题/材料。

**灌注方式**

- 古诗文节点：按篇目/作者/关键词匹配公版原文，写入 `deep_textbook_snippets`。
- 阅读/写作节点：不强行找教材正文，改用“材料片段 + 技能例题 + 答题支架”。
- 拼音/识字节点：构建专用 phonics/汉字结构小资料库，不从文学文本抽。

**优先级**

1. 古诗文和文言文：最快见效。
2. 阅读理解/赏析：用短文本样例库。
3. 写作/表达：用任务模板和范例片段。
4. 拼音识字：单独造结构化规则库。

---

### 2. 地理：72 个缺 deep

**本地可用**

- `curriculum-standards/地理/`：68 个知识点 MD。
- `books/课标-整理版/cn/middle/geography.md`、`books/课标-整理版/cn/high/地理.md`。
- `books/课标-整理版/ap/ap-human-geography.md`：可补高中人文地理、城市化、人口迁移、产业区位。
- `books/课标-整理版/cambridge/IGCSE/0460_Geography.md`：可补地图、地貌、气候、人口、产业等。
- `books/06_atmosphere_meteorology.md`：可补气候、大气、天气相关节点。

**建议新增/接入**

- OER Project Middle School Geography：`https://www.oerproject.com/topics/middle-school-geography`。
- OER Commons Geography / Open Textbook Library Geography：用于开放教材和案例检索。
- Natural Earth / NASA Earth Observatory 等开放图文资料：适合地图、气候、地貌案例，但要检查许可。

**灌注方式**

- 地理不能只按关键词抽文本，要按“地图技能 / 自然地理 / 中国地理 / 世界地理 / 人文地理”分源。
- `deep_textbook_snippets` 应优先包含：地图读图方法、区域案例、图表数据、自然过程解释。
- 对 `经纬网`、`地球运动`、`等高线` 这类节点，应优先从本地课标 MD 和地图技能案例抽，不应抽泛泛的区域介绍。

**优先级**

1. 地图工具与经纬网。
2. 气候、水循环、地貌等自然地理。
3. 人口迁移、城市化、产业区位。
4. 中国区域地理案例。

---

### 3. 英语：62 个缺 deep

**本地可用**

- `books/课标-整理版/cn/elementary/english.md`、`middle/english.md`、`high/英语.md`。
- `books/课标-整理版/cambridge/cambridge-primary-english.md`。
- `books/课标-整理版/cambridge/cambridge-lsec-english.md`。
- `books/课标-整理版/us/common-core-ela.md`。
- `books/language_arts/OpenStax_Writing_Guide_Handbook.md`：只适合高中写作，不适合小学语法/自然拼读。

**建议新增/接入**

- COERLL OER language resources：`https://coerll.utexas.edu/coerll/`。
- OER Commons English/ESL resources：用于语法、词汇、阅读材料检索。
- CUNY ELC OER writing/grammar materials：适合基础写作和句子层面训练。

**灌注方式**

- 自然拼读节点：建立 phonics 规则库，不从普通英语教材大段抽取。
- 语法节点：抽“form-meaning-use”结构化例句，而不是抽教学原则。
- 词汇节点：按主题词表 + 例句 + 交际任务灌注。
- 阅读/写作节点：用 Common Core ELA / Cambridge English 的任务描述和样例。

**优先级**

1. 自然拼读与音素。
2. 小学基础语法：be 动词、一般现在时、there be、冠词、介词。
3. 主题词汇。
4. 阅读与写作技能。

---

### 4. 历史：51 个缺 deep

**本地可用**

- `curriculum-standards/历史/`：50 个知识点 MD。
- `books/课标-整理版/cn/middle/history.md`、`high/历史.md`。
- `books/课标-整理版/ap/ap-world-history.md`。
- `books/课标-整理版/ap/ap-european-history.md`。
- `books/social_studies/OpenStax_US_History.md`：只适合美国史相关背景，不应泛配所有世界史/中国史。
- `books/课标-整理版/us/c3-framework.md`：适合历史思维和材料分析任务，不适合作为史实教材。

**建议新增/接入**

- World History Since 1500 OER：`https://dc.etsu.edu/etsu-oer/13/`。
- Open Textbook Library / LibreTexts World History OER。
- 维基文库公版历史文献：用于古代史/文献材料节选。

**灌注方式**

- 中国古代史：优先本地 `curriculum-standards/历史/` + 公版史料节选。
- 世界近现代史：AP World History / World History OER。
- 历史方法类：C3 Framework 只作为“材料分析方法”，不作为史实。
- 严格避免仅因 `revolution`、`empire`、`war` 命中而误配到无关事件。

**优先级**

1. 世界史缺 deep 节点：工业革命、科学革命、殖民体系、民族解放。
2. 中国古代史节点：用本地历史 MD + 公版文献。
3. 专题史：经济史、文化史、制度史。

---

### 5. 信息科技：10 个缺 deep

**本地可用**

- `books/课标-整理版/cn/high/信息技术.md`。
- `books/课标-整理版/ap/ap-computer-science-a.md`。
- `books/课标-整理版/ap/ap-computer-science-principles.md`。
- `books/课标-整理版/cambridge/cambridge-lsec-computing.md`。
- `books/课标-整理版/cambridge/cambridge-lsec-ict.md`。

**建议新增/接入**

- Runestone Academy 开放 CS 教材：适合 Python、数据结构、算法基础。
- OpenDSA：适合数据结构与算法。
- CS50 资料可作为参考，但需单独确认许可和使用边界。
- 国家智慧教育平台/高校公开课只做索引，不建议直接抓正文。

**灌注方式**

- 编程基础：AP CSA + Runestone/Python OER。
- 算法复杂度、排序查找、递归：OpenDSA / Runestone。
- 网络和安全：Cambridge ICT + AP CSP。
- 每个节点写入：概念定义、伪代码/代码片段、常见错误、任务案例。

**优先级**

1. 程序设计基础、控制结构、函数模块。
2. 排序查找、递归、数据结构。
3. 网络基础、互联网应用、信息安全。

---

## 二、已有资料可以马上用的灌注映射

| 缺 deep 学科 | 立即可用本地源 | 用法 |
|---|---|---|
| 语文 | `curriculum-standards/语文/`、`books/课标-整理版/cn/all/chinese.md` | 课标和教学建议；不够做文本教材，需要接公版文本库 |
| 地理 | `curriculum-standards/地理/`、`ap-human-geography.md`、`0460_Geography.md`、`06_atmosphere_meteorology.md` | 人文地理、自然地理、地图技能案例 |
| 英语 | `cambridge-primary-english.md`、`cambridge-lsec-english.md`、`common-core-ela.md` | 语法/阅读/写作任务；自然拼读需单独规则库 |
| 历史 | `curriculum-standards/历史/`、`ap-world-history.md`、`ap-european-history.md`、`OpenStax_US_History.md` | 世界史和材料分析；中国古代史需公版史料 |
| 信息科技 | `ap-computer-science-a.md`、`ap-computer-science-principles.md`、`cambridge-lsec-computing.md`、`cambridge-lsec-ict.md` | 编程、算法、网络、安全 |
| 数学 | `OpenStax_CollegeAlgebra.md`、`Prealgebra_2e.md`、`HS_Statistics.md`、`curriculum-standards/数学/` | 补剩余几何、统计、导数等 |
| 物理 | `OpenStax_HighSchool_Physics.md`、`LabManual.md`、`curriculum-standards/物理/` | 补光学、声学、机械、电磁 |
| 生物 | `OpenStax_Biology_2e.md`、`AP_Biology.md`、`curriculum-standards/生物/` | 补初中人体、分类、跨学科实践 |
| 化学 | `OpenStax_Chemistry.md`、`03_introductory_chemistry.md`、`curriculum-standards/化学/` | 补原电池、氧气制取 |

---

## 三、下一步建议

### Step 1：先建源清单 JSON

建议新增：

`data/textbook-source-map-cn.json`

结构：

```json
{
  "chinese": {
    "sources": [
      {"type": "local", "path": "curriculum-standards/语文", "usage": "curriculum"},
      {"type": "external", "url": "https://github.com/chinese-poetry/chinese-poetry", "usage": "classical_poetry"},
      {"type": "external", "url": "https://zh.wikisource.org/", "usage": "public_domain_text"}
    ]
  }
}
```

### Step 2：按学科写专用抽取器

不要一个 `deep-textbook-enrich` 通吃所有学科。建议拆成：

- `enrich_chinese_texts.py`
- `enrich_geography_cases.py`
- `enrich_english_grammar_phonics.py`
- `enrich_history_oer.py`
- `enrich_info_tech_cs.py`

### Step 3：每次补灌后抽样验收

继续使用：

`reports/deep-textbook-snippets-manual-review-2026-06-01.md`

下一轮建议每个新增资料源抽 10 条，看是否真相关。

---

## 四、优先灌注顺序

1. **信息科技 10 个**：本地 AP/Cambridge 资料已经足够，最容易补齐。
2. **数学 14 个、物理 14 个、化学 2 个、生物 7 个**：已有 OpenStax/本地资料，少量定向补齐即可。
3. **英语 62 个**：先补自然拼读和语法，收益高。
4. **地理 72 个**：需要地图/区域案例源，建议第二批。
5. **语文 130 个**：工作量最大，需接公版文本库和语文技能样例库。
6. **历史 51 个**：优先世界史和古代史；中国近现代史节点只保留课标和公开史料，谨慎扩展。
