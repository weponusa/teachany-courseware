#!/usr/bin/env python3
"""Add topic-specific depth modules to geo-m shell courses.

Middle-school geography courses often pass via template sections but lack
topic-specific core teaching. Each course gets 知识精讲 + 方法范例
(worked example + diagnostic + 常见误区). No mp4. Idempotent via id="lesson-focus".
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-11"


def C(ct, cb, mt, mb, ex, q, opts, correct, fb, pit):
    return dict(
        concept_title=ct, concept_body=cb, method_title=mt, method_body=mb,
        example=ex, question=q, options=opts, correct=correct, feedback=fb, pitfall=pit,
    )


COURSES = {
    "geo-m-earth-basics": C(
        "地球基础知识",
        "地球是一个两极稍扁、赤道略鼓的不规则球体。认识地球要抓住形状、大小、表层海陆分布等基本事实。地球仪是地球的模型，可帮助建立空间观念。学习地理从“认识我们的家园”开始。",
        "方法：模型对照真实地球",
        "用地球仪观察赤道、两极、海陆轮廓；把抽象数据（半径、周长）与可感知现象联系。",
        "从太空看地球是蓝色星球，因海洋面积远大于陆地。",
        "地球表面海洋与陆地面积大约是？",
        ["各占一半", "海洋多于陆地（约七分海洋三分陆地）", "陆地远多于海洋", "只有海洋没有陆地"],
        1,
        "海陆比大约是七分海洋、三分陆地。",
        "常见误区是凭地图直觉以为陆地很多，忽视投影与视野偏差。",
    ),
    "geo-m-globe-coordinates": C(
        "经纬网与地球坐标",
        "经线指示南北，纬线指示东西；经度、纬度构成地球坐标。赤道是最长的纬线，本初子午线是 0° 经线。经纬网可确定任意地点位置，并判断大致方向与半球。",
        "方法：先分半球再读度数",
        "读点：写清东/西经、南/北纬。比较两地时先看纬度定南北，再看经度定东西。",
        "北京约 40°N、116°E，位于北半球、东半球。",
        "纬线指示的方向是？",
        ["南北", "东西", "垂直向上", "任意"],
        1,
        "纬线指示东西方向。",
        "常见误区是经纬线方向记反，或东西半球划分按 0°/180° 与 20°W/160°E 混淆。",
    ),
    "geo-m-map-reading": C(
        "地图的阅读",
        "地图三要素：比例尺、方向、图例。比例尺表示图上距离与实地距离的比；方向可用指向标或经纬网判断；图例说明符号含义。会读图、用图是地理基本技能。",
        "方法：比例尺换算 + 定向 + 读图例",
        "算实地距离：图上距离÷比例尺。没有指向标时，一般“上北下南左西右东”，有经纬网更准确。",
        "比例尺 1:100000，图上 1 厘米代表实地 1 千米。",
        "比例尺越大，表示的范围通常？",
        ["越大内容越简略", "越小内容越详细", "一定相同", "与内容无关"],
        1,
        "大比例尺地图范围较小、内容较详细。",
        "常见误区是比例尺“越大/越小”与范围关系搞反。",
    ),
    "geo-m-contour-topographic": C(
        "等高线地形图",
        "等高线是海拔相同点的连线。等高线密集表示坡陡，稀疏表示坡缓；闭合等高线中，数值外小内大多为山地，外大内小多为盆地。通过等高线可判读山顶、山脊、山谷、陡崖等。",
        "方法：疏密看坡度，弯曲看脊谷",
        "“凸高为谷，凸低为脊”：等高线向高处凸出是山谷，向低处凸出是山脊。算相对高度看两条等高线差值。",
        "两条等高线重叠处为陡崖；登山选稀疏处更省力。",
        "等高线越密集，坡度越？",
        ["缓", "陡", "一定平坦", "无法判断"],
        1,
        "密集表示单位水平距离内高度变化大，坡陡。",
        "常见误区是山脊山谷判读反了，或把等高距当成海拔本身。",
    ),
    "geo-m-continents-oceans": C(
        "大洲大洋与海陆变迁",
        "全球七大洲、四大洋。海陆分布不是固定不变的：沧海桑田有沉积、地壳运动等证据；大陆漂移与板块构造解释大洲大洋的形成与变化。认识“变动中的地球表面”。",
        "方法：名称位置 + 变迁证据",
        "先在地图上定位大洲大洋，再举化石、海岸线吻合、火山地震带等证据理解变迁。",
        "大西洋两岸大陆轮廓大致吻合，支持大陆曾经分离的观点。",
        "下列属于四大洋的是？",
        ["地中海", "太平洋", "黑海", "北海"],
        1,
        "太平洋是四大洋之一。",
        "常见误区是把海与洋混淆，或认为海陆轮廓自古不变。",
    ),
    "geo-m-earth-motion-m": C(
        "地球的自转与公转",
        "地球自西向东自转，产生昼夜交替和地方时差异；同时绕日公转，地轴倾斜导致昼夜长短变化与四季更替。自转周期约一天，公转周期约一年。两运动叠加形成我们感受到的时间与季节。",
        "方法：现象对应哪一种运动",
        "昼夜交替、日月星辰东升西落→自转；四季、五带、昼夜长短季节变化→公转（与黄赤交角有关）。",
        "同一瞬间东边时刻更早，因地球自西向东自转。",
        "昼夜交替的主要原因是？",
        ["地球公转", "地球自转", "月球绕转", "太阳绕地球"],
        1,
        "自转使地球各地轮流迎向和背向太阳。",
        "常见误区是把四季成因说成“离太阳远近为主”，忽视公转与地轴倾斜。",
    ),
    "geo-m-seasons-m": C(
        "四季更替与昼夜长短",
        "由于黄赤交角存在，太阳直射点在南北回归线之间移动，同一地点不同季节昼夜长短和正午太阳高度变化，形成四季。北半球夏至昼最长，冬至昼最短；赤道昼夜接近等长。",
        "方法：盯住太阳直射点",
        "直射北半球→北半球昼长夜短；直射南半球则相反。二分日全球昼夜平分。",
        "北半球夏季白昼长、正午太阳高度较大，获得太阳光热较多。",
        "北半球冬至日，北半球昼夜情况是？",
        ["昼最长", "昼最短", "昼夜等长", "极昼遍布全北半球"],
        1,
        "冬至北半球昼最短夜最长。",
        "常见误区是以为夏季因为地球离太阳更近（实际上近日点在北半球冬季附近）。",
    ),
    "geo-m-climate-basics": C(
        "气候基础：天气、气温与降水",
        "天气是短时间的大气状况，气候是长时间的平均状态。气温与降水是气候两大要素。气温日较差、年较差，降水季节分配，共同描述一个地方的气候特征。读气温曲线与降水量柱状图是基本功。",
        "方法：看图说话（温+水）",
        "先读最热/最冷月气温，再看降水总量与集中季节，最后归纳气候特征并用术语表达。",
        "“夏季高温多雨，冬季温和少雨”是对亚热带季风气候特征的概括示例。",
        "气候与天气的主要区别是？",
        ["气候是短时的", "气候是长时间大气平均状况", "天气不能变化", "气候没有降水要素"],
        1,
        "气候强调长时间规律，天气强调短时状态。",
        "常见误区是把某天下雨说成“气候多雨”，概念混用。",
    ),
    "geo-m-climate-m": C(
        "世界气候类型与分布",
        "世界主要气候类型受纬度、海陆、地形、洋流等因素影响，呈一定分布规律：如赤道附近多热带雨林气候，两极附近为寒带气候，中纬度大陆东岸常见季风气候。学习要“名称—特征—分布—成因”四合一。",
        "方法：以赤道为轴南北对称记忆",
        "先按热量带抓大类，再区分大陆东岸/西岸差异。读图定位比死背地名更有效。",
        "地中海气候分布在南北纬 30°–40° 大陆西岸，夏季炎热干燥、冬季温和多雨。",
        "热带雨林气候主要分布在？",
        ["极地", "赤道附近", "回归线大陆内部", "高山顶部唯一"],
        1,
        "赤道附近终年高温多雨。",
        "常见误区是只记名称不记分布规律，或把天气现象当成气候类型。",
    ),
    "geo-m-terrain-types": C(
        "世界地形类型",
        "陆地地形主要有山地、丘陵、平原、高原、盆地等。不同地形海拔、起伏状况不同，影响气候、河流与人类活动。读分层设色地形图可快速识别地形类型与地势起伏。",
        "方法：海拔 + 起伏 + 读图颜色",
        "平原海拔较低较平坦；高原海拔高但顶面较平；山地起伏大。结合例证记世界大地形区。",
        "亚马孙平原是世界最大平原之一；青藏高原是世界最高的大高原。",
        "海拔较高、顶面较平坦的地形一般是？",
        ["平原", "高原", "峡谷", "三角洲"],
        1,
        "高原海拔高且顶面相对平坦。",
        "常见误区是把高原与山地都简单说成“高”，不区分起伏特征。",
    ),
    "geo-m-population-distribution": C(
        "世界人口与人种",
        "世界人口分布不均匀：沿海、平原、气候适宜地区较稠密，干旱、高寒、湿热雨林等地区较稀疏。人口问题包括增长、迁移与老龄化等。人种划分是自然特征分类，要树立平等观念，反对种族歧视。",
        "方法：稠密稀疏找原因",
        "从自然（地形气候水源）与社会经济（交通工农业历史）两方面分析分布。",
        "东亚、南亚、欧洲西部、北美东部是人口稠密区的典型代表。",
        "人口分布稀疏的地区往往是？",
        ["温和平原沿海", "极端干旱或高寒地区", "大城市中心", "交通枢纽"],
        1,
        "自然条件过于恶劣处人口稀疏。",
        "常见误区是只谈自然原因忽视经济，或对人种持偏见。",
    ),
    "geo-m-world-countries": C(
        "世界主要国家",
        "认识日本、俄罗斯、美国、澳大利亚、巴西等国家，要抓住位置、地形气候、资源、工农业与文化特征，形成“一个国家一张名片”。比较学习比孤立记忆更牢。",
        "方法：位置—自然—经济三板斧",
        "每个国家先定位半球与邻国，再记 1–2 个自然特征与 1–2 个经济特征。",
        "日本多火山地震、海岸线曲折；美国农业地区专门化；巴西热带雨林与咖啡等农矿产品著名。",
        "学习国家地理最有效的抓手是？",
        ["只背首都名称", "位置、自然环境与经济特征结合", "只记面积数字", "忽略地图"],
        1,
        "要把位置、自然与人文经济联系起来。",
        "常见误区是堆砌知识点，缺少地图定位与比较。",
    ),
    "geo-m-world-regions": C(
        "世界地理分区",
        "世界可按地理位置与地理特征划分为不同区域。分区学习有助于把握区域共性与差异，如东南亚、中东、撒哈拉以南非洲、欧洲西部等各有突出特征。读图确定范围是第一步。",
        "方法：范围—突出特征—成因",
        "每个分区抓 2–3 个“标签”（如中东石油与淡水、欧洲西部发达工业与温带海洋性影响等）。",
        "中东地处三洲五海之地，石油资源丰富，淡水资源紧张。",
        "认识一个分区，首先应？",
        ["背诵所有城市", "在地图上明确范围与位置", "只看新闻标题", "忽略自然环境"],
        1,
        "先定位范围，再谈特征。",
        "常见误区是分区界线死记硬背却不会在地图上指认。",
    ),
    "geo-m-china-overview": C(
        "中国地理总论",
        "学习中国地理先建立整体框架：位置与疆域、地形地势、气候、河流、资源、人口民族、农业工业交通、四大区域等。整体把握后再深入专题，避免“只见树木不见森林”。",
        "方法：先总后分，图文结合",
        "用中国地图把山脉河流气候区叠加理解“地势西高东低”“季风影响显著”等总特征。",
        "地势西高东低使大河东流入海，水能资源西部丰富，东中部航运便利。",
        "认识中国地理应从？",
        ["只背省级行政区划全称", "建立位置、自然与人文的整体框架", "只看一个城市", "忽略地图"],
        1,
        "先有总论框架再学专题更有效。",
        "常见误区是一开始就陷入琐碎地名，缺少宏观结构。",
    ),
    "geo-m-china-location": C(
        "中国的地理位置与疆域",
        "中国位于亚欧大陆东部、太平洋西岸，海陆兼备。疆域辽阔，领陆、领水、领空构成领土。邻国众多，海岸线漫长。优越的位置对气候、交通、对外交往影响深远。",
        "方法：半球—大洲—海陆位置",
        "叙述位置按顺序：半球→大洲→与海洋关系→邻国与濒临海洋。结合地图指认。",
        "东临太平洋使我国东部降水较丰富，并便于海外贸易。",
        "中国地理位置的突出优点之一是？",
        ["深居内陆不靠海", "海陆兼备", "全在南半球", "没有陆上邻国"],
        1,
        "海陆兼备便于发展海洋事业与陆上交往。",
        "常见误区是把“国土面积大”与“位置优越”混为一谈，不会分层描述位置。",
    ),
    "geo-m-china-terrain": C(
        "中国地形与地势",
        "中国地形复杂多样，山区面积广大；地势西高东低，呈三级阶梯。山脉构成地形骨架，平原、高原、盆地分布有致。地势影响气候、河流流向、交通与农业格局。",
        "方法：三级阶梯 + 主要山脉",
        "记阶梯分界山脉（如昆仑山—祁连山—横断山脉等），再对应阶梯上的主要地形区。",
        "长江从第一级阶梯流到第三级，落差大，水能丰富。",
        "中国地势的总特征是？",
        ["东高西低", "西高东低", "北高南低唯一", "中部最高四周低"],
        1,
        "地势西高东低，分级阶梯明显。",
        "常见误区是阶梯分界线记混，或把“地形多样”说成只有山地。",
    ),
    "geo-m-china-climate": C(
        "中国气候",
        "中国气候复杂多样，季风气候显著。东部主要有温带、亚热带、热带季风气候，西北大陆性气候强，青藏高寒。夏季普遍高温，雨热同期对农业有利；降水自东南向西北递减。",
        "方法：季风 + 雨热同期",
        "抓冬夏季风源地与性质；用“高温期与多雨期一致”解释农业意义；注意旱涝、寒潮等灾害。",
        "南方雨季长、北方雨季短，与夏季风进退有关。",
        "中国东部气候的突出特征是？",
        ["终年干燥", "季风气候显著、雨热同期", "没有季节变化", "全为热带雨林气候"],
        1,
        "季风气候显著是中国气候重要特征。",
        "常见误区是以为全国气候单一，或忽视西北、青藏的特殊性。",
    ),
    "geo-m-china-rivers": C(
        "中国的河流与湖泊",
        "中国河流众多，外流河主要流入太平洋，长江、黄河是最重要的大河。河流水文特征受降水与地形影响。湖泊有淡水湖与咸水湖。防洪、灌溉、发电、航运是河流开发的重要主题。",
        "方法：源流—水文—治理利用",
        "每条大河记发源、流经、注入与一两个突出问题（如黄河泥沙、长江洪水）。",
        "黄河“几”字形流经，中游黄土高原水土流失导致下游“地上河”。",
        "长江最终注入？",
        ["印度洋", "太平洋", "北冰洋", "内陆湖"],
        1,
        "长江注入太平洋。",
        "常见误区是把黄河长江的问题张冠李戴，或只记长度不看治理。",
    ),
    "geo-m-china-resources": C(
        "中国自然资源",
        "中国自然资源总量大、种类多，但人均偏少，地区分布不均。土地、水、矿产、森林、能源等各有特征。树立节约集约与保护意识，理解“资源问题也是发展问题”。",
        "方法：总量—人均—分布—对策",
        "谈资源先说国情特征，再举一例（如水资源南多北少）并提出调配/节约措施。",
        "南水北调缓解北方缺水，但节约用水仍是根本。",
        "中国自然资源的基本国情之一是？",
        ["人均很多", "总量较大但人均不足、分布不均", "完全依赖进口", "只有石油没有煤炭"],
        1,
        "总量大、人均少、分布不均是重要特征。",
        "常见误区是只强调“地大物博”而忽视人均与分布问题。",
    ),
    "geo-m-china-population": C(
        "中国人口与民族",
        "中国人口基数大，分布东多西少；民族众多，汉族为主体，少数民族主要分布在东北、西北、西南等地，有大杂居、小聚居特点。人口政策与民族政策影响区域发展与社会和谐。",
        "方法：分布规律 + 政策意义",
        "用人口密度图说明东密西疏原因；民族问题强调平等团结与区域贡献。",
        "黑河—腾冲一线是人口分布的重要地理分界。",
        "中国人口分布的大致特点是？",
        ["西多东少", "东多西少", "均匀分布", "只集中在青藏"],
        1,
        "东部沿海与平原地区人口稠密。",
        "常见误区是忽视人口分布与自然、经济条件的关系。",
    ),
    "geo-m-china-industry": C(
        "中国工业",
        "中国工业门类齐全，空间上既有传统工业基地，也有高新技术产业快速发展地区。工业布局受原料、能源、市场、交通、技术、政策等因素影响。理解“因地制宜发展工业”。",
        "方法：区位因素对号入座",
        "分析某工业区为何在此：原料导向、市场导向、技术导向等。结合地图看工业分布变化。",
        "高新技术产业多靠近高校科研机构与交通便利的环境优美城市。",
        "影响工业区位的因素不包括？",
        ["原料与市场", "迷信传说", "交通与能源", "技术与劳动力"],
        1,
        "工业区位应基于经济与社会条件，而非迷信。",
        "常见误区是只会背基地名称，说不清布局理由。",
    ),
    "geo-m-china-transportation": C(
        "中国交通运输",
        "铁路、公路、水运、航空构成综合运输网。不同运输方式各有优劣：铁路运量大较连续，公路灵活，水运成本低但速度慢，航空速度快适合长距离客运与贵重急件。交通发展促进区域联系。",
        "方法：方式比较 + 线路意义",
        "选择题常用“最优运输方式”；读图认识主要铁路干线与枢纽城市。",
        "从北京到上海客运可优先高铁；大宗煤炭长距离常选铁路或下水联运。",
        "运送紧急救援药品到边疆偏远地区，较合适的是？",
        ["内河慢运", "航空运输", "只靠海运", "拒绝运输"],
        1,
        "航空速度快，适合紧急贵重物资。",
        "常见误区是认为某一种运输方式绝对最好，不看货物性质与距离。",
    ),
    "geo-m-china-regions": C(
        "中国四大地理区域",
        "依据自然与人文地理特征，中国划分为北方、南方、西北、青藏四大地理区域。秦岭—淮河是南北方重要分界；西北干旱半干旱，青藏高寒。分区是认识区域差异的钥匙。",
        "方法：分界线 + 主导因素",
        "北方南方比降水与气温；西北比干旱；青藏比高寒。用表格式对比最清晰。",
        "秦岭—淮河一线与 1 月 0℃ 等温线、800 mm 年等降水量线大致吻合。",
        "划分西北地区与北方地区的主导因素更突出的是？",
        ["语言", "降水（干湿状况）", "春节习俗唯一", "人口密度唯一"],
        1,
        "西北干旱半干旱特征与降水密切相关。",
        "常见误区是四大区域界线记混，或只用一个指标解释所有差异。",
    ),
    "geo-m-four-regions": C(
        "北方、南方、西北、青藏地区",
        "四大区域自然环境与生产生活差异明显：北方温带为主、耕地多旱地；南方亚热带热带、水田广布；西北牧场与绿洲农业；青藏高寒牧业与河谷农业。理解差异才能理解因地制宜。",
        "方法：自然→农业→文化景观",
        "每个区域写“气候/地形—农业类型—传统民居或交通”一条链。",
        "南方水乡与船运、西北帐篷与骆驼、青藏碉房与牦牛，都是适应环境的结果。",
        "青藏地区农业生产的主要限制因素是？",
        ["热量不足", "光照太少", "完全没有水源", "地势过低"],
        0,
        "高寒导致热量不足是重要限制。",
        "常见误区是把四大区域农业类型记串。",
    ),
    "geo-m-north-south": C(
        "北方与南方地区对比",
        "北方与南方以秦岭—淮河为界，在气候、河流水文、植被、农业、语言文化等方面差异显著。对比学习要抓住“同一指标下的不同表现”，形成清晰对照。",
        "方法：做对照表",
        "列气温、降水、耕地类型、作物熟制、传统主食等栏目逐项对比。",
        "北方耕地多旱地，小麦为主；南方多水田，水稻为主。",
        "南北方地理分界的重要界线是？",
        ["长城", "秦岭—淮河", "长江", "南岭唯一"],
        1,
        "秦岭—淮河是重要地理分界线。",
        "常见误区是把行政南北与地理南北混为一谈。",
    ),
    "geo-m-northwest-qinghai": C(
        "西北与青藏地区",
        "西北地区深居内陆，干旱少雨，荒漠与草原广布，绿洲农业依赖灌溉；青藏地区“高”和“寒”，太阳辐射强，畜牧业重要，农业多在河谷。两区生态环境脆弱，开发需保护先行。",
        "方法：干旱 vs 高寒",
        "西北抓“干”，青藏抓“高寒”；都强调生态脆弱与可持续发展。",
        "河西走廊依靠祁连山冰雪融水发展绿洲农业；雅鲁藏布江河谷是青藏重要农业区。",
        "西北地区自然景观以？",
        ["热带雨林为主", "荒漠与草原为主", "永久冰盖覆盖全境", "到处水田"],
        1,
        "干旱半干旱导致荒漠草原广布。",
        "常见误区是忽视两区生态脆弱，盲目套用东部发展模式。",
    ),
    "geo-m-yangtze-delta": C(
        "长江三角洲",
        "长三角地处长江入海口，地势低平，水网密布，气候湿润，交通便利，是我国经济最活跃的区域之一。城市密集，工商业发达，一体化发展强调协作与优势互补。",
        "方法：区位优势清单",
        "从位置、交通、腹地、人才、政策等列出发展条件，再谈城市化与产业。",
        "上海是重要港口与金融中心，辐射带动长三角城市群。",
        "长三角发展的突出优势包括？",
        ["远离海洋", "位置优越、交通便利、经济基础雄厚", "气候高寒", "人口极度稀少"],
        1,
        "综合性区位优势显著。",
        "常见误区是只知上海不知区域整体，或忽视洪涝等环境问题。",
    ),
    "geo-m-pearl-river-delta": C(
        "珠江三角洲",
        "珠三角位于广东省东南部，毗邻港澳，对外联系便利，是改革开放前沿与外向型经济发达地区。轻工业、制造业与高新技术产业并重，城镇化水平高。注意与长三角的比较。",
        "方法：外向型 + 港澳因素",
        "抓临海、侨乡、政策、与港澳合作等关键词，理解其发展路径。",
        "依托港口与开放政策，珠三角吸引外资，发展出口加工与现代服务业。",
        "珠三角外向型经济发达的重要条件是？",
        ["深居内陆", "毗邻港澳、对外交通便利", "没有港口", "完全封闭"],
        1,
        "区位与开放政策支持外向型发展。",
        "常见误区是把珠三角与长三角特征完全混同，不会比较差异。",
    ),
}


STYLE = """
<style id="geom-depth-css">
.geom-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.geom-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(251,146,60,.08);border:1px solid rgba(251,146,60,.28)}
.geom-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.geom-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.geom-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.geom-depth .geom-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.geom-depth .geom-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
</style>
"""

CHECK_SCRIPT = """
<script id="geom-depth-js">
function geomDepthCheck(button, isCorrect, feedbackId, explanation) {
  var box = button.closest('.module-check');
  if (!box || box.dataset.answered) return;
  box.dataset.answered = '1';
  box.querySelectorAll('button').forEach(function (item) {
    item.disabled = true;
    if (item.dataset.correct === '1') item.classList.add('correct');
  });
  if (!isCorrect) button.classList.add('wrong');
  var feedback = document.getElementById(feedbackId);
  if (feedback) {
    feedback.style.display = 'block';
    feedback.textContent = (isCorrect ? '正确。' : '再想想。') + explanation;
  }
}
</script>
"""


def build_block(cfg: dict) -> str:
    feedback_id = "geom-depth-feedback"
    options = []
    for idx, opt in enumerate(cfg["options"]):
        correct = idx == cfg["correct"]
        handler = "geomDepthCheck(this,{c},'{f}',{e})".format(
            c="true" if correct else "false",
            f=feedback_id,
            e=json.dumps(cfg["feedback"], ensure_ascii=False),
        )
        options.append(
            '<button type="button" data-correct="{flag}" onclick="{h}">{letter}. {opt}</button>'.format(
                flag="1" if correct else "0",
                h=html.escape(handler, quote=True),
                letter=chr(65 + idx),
                opt=html.escape(opt),
            )
        )
    return f"""
<section class="slide-page" data-page-type="content" data-tsh="精讲">
  <section class="section geom-depth core-knowledge-module text-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section geom-depth core-knowledge-module text-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="geom-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析要点</h3>
        <p>{html.escape(cfg['question'])}</p>
        {''.join(options)}
        <div class="geom-feedback" id="{feedback_id}" role="status"></div>
      </div>
    </div>
  </section>
</section>
"""


def upgrade(course_id: str, cfg: dict) -> tuple[bool, str]:
    path = ROOT / "community" / course_id / "index.html"
    if not path.exists():
        return False, "missing index.html"
    source = path.read_text(encoding="utf-8")
    if 'id="lesson-focus"' in source:
        return False, "already upgraded"
    dpos = -1
    for anchor in ('id="deep-understanding"', 'id="transfer-task"', 'id="posttest"', 'id="summary"'):
        dpos = source.find(anchor)
        if dpos >= 0:
            break
    if dpos < 0:
        return False, "insert anchor not found"
    marker = source.rfind('<section class="slide-page"', 0, dpos)
    insert_at = marker if marker >= 0 else source.rfind("<section", 0, dpos)
    if insert_at < 0:
        return False, "insert marker not found"
    source = source[:insert_at] + build_block(cfg) + "\n" + source[insert_at:]
    if 'id="geom-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="geom-depth-js"' not in source:
        source = source.replace("</body>", CHECK_SCRIPT + "\n</body>", 1)
    source = re.sub(r"[ \t]+\n", "\n", source)
    path.write_text(source, encoding="utf-8")
    manifest_path = path.parent / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        changed = False
        for key, value in {"version": COURSE_VERSION, "updated_at": UPDATED_AT}.items():
            if manifest.get(key) != value:
                manifest[key] = value
                changed = True
        if changed:
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
    return True, "2 depth modules + metadata"


def main() -> int:
    changed = failed = 0
    for course_id, cfg in COURSES.items():
        ok, msg = upgrade(course_id, cfg)
        if ok:
            changed += 1
            print(f"OK {course_id}: {msg}")
        elif msg == "already upgraded":
            print(f"SKIP {course_id}: {msg}")
        else:
            failed += 1
            print(f"FAIL {course_id}: {msg}")
    print(f"done: changed={changed} failed={failed} of {len(COURSES)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
