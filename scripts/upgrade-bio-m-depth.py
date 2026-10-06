#!/usr/bin/env python3
"""Add topic-specific depth modules to bio-m shell courses.

Middle-school biology courses often pass via template sections but lack
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
    "bio-m-cell-basics": C(
        "细胞基础",
        "细胞是生物体结构和功能的基本单位。植物细胞有细胞壁、叶绿体、液泡等，动物细胞没有细胞壁和叶绿体。细胞膜控制物质进出，细胞核是遗传信息库，细胞质中进行多种生命活动。观察细胞常用显微镜。",
        "方法：结构—功能对照记",
        "先分动植物细胞异同，再把每个结构对应一种功能。画简图标注比死背更牢。",
        "洋葱表皮有细胞壁无叶绿体；叶片细胞有叶绿体，能进行光合作用。",
        "动植物细胞都有的结构是？",
        ["细胞壁与叶绿体", "细胞膜、细胞质、细胞核", "只有液泡", "只有叶绿体"],
        1,
        "细胞膜、细胞质、细胞核是动植物细胞共有的基本结构。",
        "常见误区是把叶绿体当成所有植物细胞都有，或认为动物细胞有细胞壁。",
    ),
    "bio-m-cell-division-junior": C(
        "细胞分裂入门",
        "细胞分裂使细胞数目增多，是生物生长、发育、繁殖的基础。分裂时细胞核先一分为二，随后细胞质分裂。新细胞与亲代细胞一般具有相同的遗传物质。理解“一个变两个”。",
        "方法：抓分裂顺序",
        "记：核分裂→质分裂→形成两个子细胞。联系伤口愈合、植物长高。",
        "皮肤破损后周围细胞通过分裂增生，填补损伤部位。",
        "细胞分裂的结果是？",
        ["细胞体积无限增大", "细胞数目增多", "遗传物质消失", "只增加细胞壁"],
        1,
        "分裂使细胞数目增加。",
        "常见误区是以为长大只靠细胞体积增大，忽视数目增多。",
    ),
    "bio-m-cell-division-m": C(
        "从细胞到个体",
        "受精卵通过细胞分裂增加数量，再经细胞分化形成不同组织，进一步构成器官、系统，进而形成完整个体。分化是细胞在形态、结构和功能上发生稳定性差异的过程，遗传物质一般不丢失。",
        "方法：分裂—分化—组织器官",
        "画层级：细胞→组织→器官→系统→个体。强调分化后功能专一。",
        "肌肉细胞、神经细胞由相同受精卵发育而来，因分化而功能不同。",
        "细胞分化的结果是形成？",
        ["完全相同的细胞", "不同的组织", "只有细胞膜", "病毒"],
        1,
        "分化产生形态功能不同的细胞群，构成组织。",
        "常见误区是认为分化改变了遗传物质种类，或分裂与分化概念混淆。",
    ),
    "bio-m-plant-structure": C(
        "绿色植物的整体结构",
        "绿色植物通常有根、茎、叶、花、果实、种子等器官。根吸收与固着，茎运输与支持，叶是光合作用主要场所，花与果实种子关系到繁殖。器官分工合作，构成统一整体。",
        "方法：器官—功能—联系",
        "每器官抓 1–2 个核心功能，再用“根吸收的水运到叶”把结构串起来。",
        "叶制造的有机物通过茎中筛管运往根、花、果实等部位。",
        "光合作用的主要器官是？",
        ["根", "叶", "花瓣", "种子皮"],
        1,
        "叶含大量叶绿体，是光合作用主要场所。",
        "常见误区是只记器官名称，说不清各器官如何配合。",
    ),
    "bio-m-photosynthesis-m": C(
        "光合作用",
        "绿色植物利用光能，在叶绿体中把二氧化碳和水转化成有机物并释放氧气。公式可记：二氧化碳+水→（光能、叶绿体）→有机物+氧气。光合作用为生物界提供有机物和氧气，意义重大。",
        "方法：原料—条件—产物—场所",
        "实验常验证产物淀粉与氧气、原料二氧化碳等。答题按四要素回答。",
        "遮光叶片遇碘不变蓝，见光部分变蓝，说明光合作用需要光并产生淀粉。",
        "光合作用的能量来源是？",
        ["土壤肥力", "光能", "只靠呼吸作用", "月光唯一"],
        1,
        "光能是光合作用的能量来源。",
        "常见误区是把呼吸作用与光合作用原料产物搞反，或认为夜间植物只吸氧。",
    ),
    "bio-m-microorganism": C(
        "微生物",
        "微生物包括细菌、真菌、病毒等，个体微小、种类繁多。细菌无成形细胞核，真菌有细胞核，病毒无细胞结构、必须寄生。微生物有的使人致病，有的用于发酵、制药与生态循环。",
        "方法：三类对比表",
        "细菌/真菌/病毒：结构、繁殖、举例分列。强调“不全是有害的”。",
        "酵母菌发酵做面包馒头；青霉可用于生产青霉素。",
        "病毒的主要特点是？",
        ["有完整细胞结构", "无细胞结构，营寄生生活", "都能独立完成光合作用", "都是真菌"],
        1,
        "病毒没有细胞结构，必须寄生在活细胞中。",
        "常见误区是把所有微生物都当成细菌，或认为微生物全是有害的。",
    ),
    "bio-m-microorganism-health": C(
        "微生物与人类健康",
        "微生物与健康密切相关：正常菌群有益；病原微生物可引起传染病。卫生习惯、食品安全、疫苗接种与合理使用抗生素都是保护健康的重要措施。理解“预防为主”。",
        "方法：有益—有害—防护",
        "举例益生菌、致病菌；防护抓住传染源、传播途径、易感人群三个环节。",
        "勤洗手、食品加热煮熟，可减少病菌经口传播。",
        "预防传染病的措施中，接种疫苗主要是为了？",
        ["消灭所有细菌", "保护易感人群", "改变传播途径为唯一手段", "增加传染源"],
        1,
        "疫苗提高免疫力，保护易感人群。",
        "常见误区是滥用抗生素，或忽视日常卫生对预防的作用。",
    ),
    "bio-m-infectious-disease": C(
        "传染病与免疫",
        "传染病由病原体引起，可在人与人或人与动物间传播。流行需传染源、传播途径、易感人群三个基本环节。免疫是人体的防御功能，分非特异性免疫与特异性免疫；抗体、抗原是重要概念。",
        "方法：三环节对症预防",
        "控制传染源、切断传播途径、保护易感人群。疫苗属于特异性免疫应用。",
        "隔离患者是控制传染源；戴口罩可切断部分空气传播途径。",
        "传染病流行的三个基本环节是？",
        ["只与天气有关", "传染源、传播途径、易感人群", "只与遗传有关", "只有细菌没有病毒"],
        1,
        "三个环节缺一则传染病难以流行。",
        "常见误区是把所有疾病都当成传染病，或以为疫苗可治疗已形成的感染替代一切治疗。",
    ),
    "bio-m-circulatory-system": C(
        "血液循环系统",
        "血液由血浆和血细胞组成，在心脏推动下在血管中循环。动脉把血送出心脏，静脉送回心脏，毛细血管进行物质交换。体循环与肺循环构成完整路径，运输氧、养料、二氧化碳等。",
        "方法：心脏→血管→物质交换",
        "画简图：左心室→体动脉→…→右心房（体循环）；右心室→肺→左心房（肺循环）。",
        "血液流经肺部时二氧化碳减少、氧气增多，颜色变得更鲜红。",
        "进行物质交换的血管主要是？",
        ["主动脉", "毛细血管", "肺动脉唯一", "只有静脉"],
        1,
        "毛细血管管壁薄、血流慢，利于物质交换。",
        "常见误区是动静脉功能记反，或体循环肺循环路径混淆。",
    ),
    "bio-m-circulation-respiration": C(
        "循环与呼吸综合",
        "呼吸系统获取氧气、排出二氧化碳；循环系统运输气体与营养。肺泡是气体交换的关键场所，血红蛋白运输氧气。两系统密切配合，保证细胞呼吸所需原料与废物排出。",
        "方法：气体从哪里来到哪里去",
        "追踪一分子氧气：鼻腔→…→肺泡→血液→组织细胞。再追踪二氧化碳返回路径。",
        "剧烈运动时呼吸加快、心跳加快，以输送更多氧并排出更多二氧化碳。",
        "氧气进入血液主要发生在？",
        ["口腔", "肺泡处", "胃", "肾脏"],
        1,
        "肺泡与血液间进行气体交换。",
        "常见误区是以为呼吸只是“胸部起伏”，忽视气体运输与细胞利用。",
    ),
    "bio-m-urinary-nervous": C(
        "泌尿系统",
        "泌尿系统包括肾脏、输尿管、膀胱、尿道。肾脏是形成尿液的器官，通过滤过和重吸收等过程排出代谢废物，调节水盐平衡。尿液成分变化可反映健康状况。保护肾脏要合理饮水、避免滥用药物等。",
        "方法：结构顺序 + 尿的形成要点",
        "记解剖路径；理解原尿与终尿差别（如葡萄糖一般被重吸收）。",
        "血糖过高时尿中可能出现葡萄糖，与重吸收能力有关，需就医排查。",
        "形成尿液的主要器官是？",
        ["膀胱", "肾脏", "输尿管", "肝脏"],
        1,
        "肾脏形成尿液，膀胱暂时储存。",
        "常见误区是把膀胱当成造尿器官，或认为尿液形成与血液无关。",
    ),
    "bio-m-animal-diversity": C(
        "动物的主要类群",
        "动物可分为无脊椎动物与脊椎动物。无脊椎动物有腔肠、扁形、线形、环节、软体、节肢等类群；脊椎动物有鱼、两栖、爬行、鸟、哺乳。分类依据形态结构与生活习性等特征。",
        "方法：关键特征定类群",
        "每类群抓 1 个鉴别特征（如节肢动物有外骨骼与分节附肢，鸟类有羽毛等）。",
        "蝴蝶属于节肢动物；家鸽属于鸟类；猫属于哺乳动物。",
        "体内有由脊椎骨构成的脊柱的动物属于？",
        ["无脊椎动物", "脊椎动物", "真菌", "细菌"],
        1,
        "脊椎动物具有脊柱。",
        "常见误区是凭“会飞”就把蝙蝠当鸟类，忽视哺乳特征。",
    ),
    "bio-m-animal-behavior": C(
        "动物行为",
        "动物行为是动物的对外活动，包括取食、防御、繁殖、迁徙等。按获得途径可分为先天性行为与学习行为。行为有利于个体生存与种族延续，受神经系统和激素等调节。",
        "方法：先天 vs 学习",
        "生来就会、物种共有的多属先天性行为；通过生活经验和学习获得的属学习行为。举例对比。",
        "蜘蛛结网多为先天性行为；小狗算算术表演属于学习行为。",
        "小狗通过训练学会握手，这主要属于？",
        ["先天性行为", "学习行为", "植物向性", "细胞分裂"],
        1,
        "经训练获得，属于学习行为。",
        "常见误区是把所有复杂行为都当成先天，或否认动物有学习能力。",
    ),
    "bio-m-ecosystem-junior": C(
        "生态系统入门",
        "生态系统由生物部分和非生物部分组成。生物包括生产者、消费者、分解者。物质循环、能量流动沿着食物链和食物网进行。生态系统具有一定自我调节能力，但有限度。",
        "方法：找角色 + 串食物链",
        "先找生产者（绿色植物等），再找各级消费者，分解者单独点明。写食物链从生产者开始。",
        "草→兔→狐是简单食物链；能量沿食物链单向流动、逐级递减。",
        "生态系统中的生产者主要是？",
        ["老虎", "绿色植物", "蘑菇唯一", "只有人类"],
        1,
        "绿色植物能光合作用制造有机物，是主要生产者。",
        "常见误区是食物链写成循环箭头，或漏掉分解者与非生物部分。",
    ),
    "bio-m-biosphere": C(
        "生物圈",
        "生物圈是地球上所有生物及其生存环境的总称，是最大的生态系统，包括大气圈下部、水圈大部和岩石圈表面。生物圈为生物提供营养物质、阳光、空气、水等生存条件。保护生物圈就是保护人类家园。",
        "方法：范围—条件—保护",
        "明确生物圈厚度与位置；列出生存所需基本条件；联系污染、栖息地破坏等威胁。",
        "若全球气候与污染加剧，许多物种栖息地缩小，生物圈稳定性受影响。",
        "地球上最大的生态系统是？",
        ["一片森林", "生物圈", "一个池塘", "一座城市"],
        1,
        "生物圈是最大的生态系统。",
        "常见误区是把生物圈理解成“只有生物没有环境”，或以为与人类活动无关。",
    ),
    "bio-m-biosphere-scope": C(
        "生物圈的范围与意义",
        "生物圈以海平面为标准向上向下各延伸一定范围，绝大多数生物生活在地表以上和水面以下较薄的一层。它是生命繁衍的舞台，人类活动深刻影响其稳定。认识范围有助于理解环境保护的全局性。",
        "方法：空间范围 + 人类影响",
        "用“薄薄的生命层”建立直观印象；举例大气污染、海洋塑料等跨区域问题。",
        "黄河上游生态破坏可能影响中下游水质与生物多样性，说明联系是全局的。",
        "关于生物圈，正确的是？",
        ["只包括陆地不含海洋", "包括生物及其生活的无机环境", "与非生物环境无关", "只存在于地球内部核心"],
        1,
        "生物圈是生物与环境的统一整体。",
        "常见误区是认为环境保护只是局部小事，与生物圈稳定无关。",
    ),
    "bio-m-biodiversity-m": C(
        "生物多样性及其保护",
        "生物多样性包括生物种类、基因和生态系统多样性。它具有使用价值、潜在价值与科研美学等意义。栖息地破坏、污染、过度利用、外来物种等威胁多样性。保护措施包括就地保护、迁地保护、法制与宣传等。",
        "方法：价值—威胁—对策",
        "答题先点明多样性内涵，再举威胁，最后对应保护措施（自然保护区是就地保护典型）。",
        "建立自然保护区保护大熊猫栖息地，属于就地保护。",
        "保护生物多样性最有效的措施通常是？",
        ["全部迁入城市饲养唯一", "就地保护（如自然保护区）", "随意引入外来物种", "破坏栖息地开垦"],
        1,
        "就地保护能保存物种及其环境。",
        "常见误区是只保护“可爱动物”而忽视生态系统与遗传多样性。",
    ),
}


STYLE = """
<style id="biom-depth-css">
.biom-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.biom-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(251,146,60,.08);border:1px solid rgba(251,146,60,.28)}
.biom-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.biom-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.biom-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.biom-depth .biom-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.biom-depth .biom-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
</style>
"""

CHECK_SCRIPT = """
<script id="biom-depth-js">
function biomDepthCheck(button, isCorrect, feedbackId, explanation) {
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
    feedback_id = "biom-depth-feedback"
    options = []
    for idx, opt in enumerate(cfg["options"]):
        correct = idx == cfg["correct"]
        handler = "biomDepthCheck(this,{c},'{f}',{e})".format(
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
  <section class="section biom-depth core-knowledge-module text-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section biom-depth core-knowledge-module text-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="biom-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析要点</h3>
        <p>{html.escape(cfg['question'])}</p>
        {''.join(options)}
        <div class="biom-feedback" id="{feedback_id}" role="status"></div>
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
    if 'id="biom-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="biom-depth-js"' not in source:
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
