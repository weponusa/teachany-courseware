#!/usr/bin/env python3
"""Add topic-specific depth modules to it-h shell courses.

High-school IT courses often pass via template sections but lack topic-specific
core teaching. Each course gets 知识精讲 + 方法范例 (worked example + diagnostic
+ 常见误区). No mp4. Idempotent via id="lesson-focus". Unique prefix: ith-depth-*.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-20"


def C(ct, cb, mt, mb, ex, q, opts, correct, fb, pit):
    return dict(
        concept_title=ct, concept_body=cb, method_title=mt, method_body=mb,
        example=ex, question=q, options=opts, correct=correct, feedback=fb, pitfall=pit,
    )


COURSES = {
    "it-h-algorithm-concept": C(
        "算法：有穷、确定、可行的解题步骤",
        "算法是解决一类问题的有穷步骤序列，通常具备输入、输出、有穷性、确定性和可行性。同一问题可有多种算法，评价常看正确性、时间复杂度和空间复杂度。时间复杂度用大O记号描述规模n增大时运算次数的增长趋势，如O(1)、O(n)、O(n log n)、O(n²)。高中阶段重在建立“先想步骤再写代码”的意识，并能比较不同算法的效率差异。",
        "方法：先抽象步骤，再估复杂度",
        "读题先明确输入输出与约束；再写出伪代码或流程图；最后用典型规模估算比较：循环套循环常接近O(n²)，分治/二分常见O(n log n)。答题时说明“为何正确”和“为何更快/更省空间”。",
        "在n个有序数中找目标：顺序查找最坏约n次比较，二分查找约log₂n次，规模越大差距越明显。",
        "算法必须具备的性质之一是？",
        ["步骤可以无限执行下去", "有穷性（有限步内结束）", "只能用一种语言实现", "不需要输入输出"],
        1,
        "算法步骤必须有穷，不能无限进行下去。",
        "常见误区是把“能跑出结果的一段代码”等同于好算法，忽视正确性边界与复杂度；或误以为大O越小就一定最好，而不看问题规模与常数开销。",
    ),
    "it-h-control-structures": C(
        "程序控制结构：顺序、分支与循环",
        "任何程序逻辑都可由三种基本控制结构组合而成：顺序（按书写次序执行）、分支（按条件选择路径）和循环（在条件成立时重复执行）。分支常用 if/else、多分支选择；循环有计数型（for）与条件型（while）。掌握三种结构，才能把自然语言解题过程准确翻译成可执行程序，并避免死循环与条件写反。",
        "方法：画流程再落代码",
        "先画流程图或列步骤：哪里判断、哪里重复、循环变量如何变化与何时退出。再写代码时检查：条件是否取反、循环变量是否更新、边界（等于还是小于）是否正确。复杂逻辑可嵌套，但层次不宜过深，可拆成函数。",
        "求1到100的和：初始化s=0，用循环让i从1到100执行s=s+i，属于典型的计数型循环。",
        "下列哪一项属于分支结构？",
        ["依次执行三条赋值语句", "根据成绩是否≥60输出及格或不及格", "重复打印10次“你好”", "定义一个变量"],
        1,
        "根据条件选择不同输出路径，属于分支结构。",
        "常见误区是循环条件写错导致少循环一次或多循环一次（差一错误），以及在循环体内忘记更新循环变量造成死循环。",
    ),
    "it-h-data-structures": C(
        "数据结构：组织数据的方式决定效率",
        "数据结构研究如何组织与存储数据，以支持高效的插入、删除、查找等操作。线性结构有列表（数组/顺序表）、栈（后进先出LIFO）、队列（先进先出FIFO）；非线性结构有树（层次关系）与图（多对多关系）。选择结构时要看操作模式：频繁在两端进出用栈/队列，需要随机访问用列表，表达层级用树，表达网络关系用图。",
        "方法：按“操作需求”选型",
        "先问：数据之间是什么关系？最频繁的操作是什么？需要随机访问、还是只在一端进出？再对照列表、栈、队列、树、图的特点选型，并说明时间代价直觉（如链表插入快但随机访问慢）。",
        "浏览器“后退”用栈保存访问历史：后打开的页面先退出；打印任务排队用队列：先提交的任务先打印。",
        "栈的典型特征是？",
        ["先进先出", "后进先出", "随机访问最快", "只能存数字"],
        1,
        "栈是后进先出（LIFO）结构。",
        "常见误区是把栈和队列混用，或认为“会用数组就够了”而忽视问题本身的结构关系；学习时应把结构特征与生活/程序场景一一对应。",
    ),
    "it-h-functions-modules": C(
        "函数与模块化：拆分、复用、降低耦合",
        "函数把一段完成特定功能的代码封装起来，通过参数传入数据、通过返回值给出结果。模块化是把程序按职责拆成多个函数/模块，降低复杂度、便于测试与协作。好的函数应职责单一、命名清晰、避免过多全局变量。参数传递、局部变量作用域、返回值是理解函数调用的关键。",
        "方法：先定接口再写实现",
        "设计函数先写清：函数名、输入参数、返回值含义与前置条件；再实现内部逻辑。重复出现的代码优先提取为函数。模块之间通过明确接口通信，减少互相修改内部细节。",
        "把“判断素数”写成 is_prime(n)，主程序循环调用它统计素数个数，主逻辑更短、也更易单独测试该函数。",
        "函数设计较合理的做法是？",
        ["一个函数做尽量多不相关的事", "职责单一、接口清晰、便于复用", "尽量多用全局变量共享状态", "函数名越短越好不必表意"],
        1,
        "单一职责与清晰接口有利于复用、测试和维护。",
        "常见误区是把所有代码堆在一个超长主程序里，或函数之间靠大量全局变量“偷偷传参”，导致难调试、难复用。",
    ),
    "it-h-information-security": C(
        "信息安全与隐私保护",
        "信息安全目标常概括为CIA：机密性（Confidentiality）、完整性（Integrity）、可用性（Availability）。常见威胁包括恶意软件、网络钓鱼、弱口令、未授权访问与数据泄露。防护手段有身份认证、访问控制、加密传输与存储、备份、安全更新与安全意识。隐私保护强调最小化收集、知情同意与合规使用个人数据。",
        "方法：威胁—资产—对策对照",
        "分析安全问题先明确要保护的资产（账号、成绩、隐私），再识别威胁与薄弱点，最后选对策：认证加强（强密码+双因素）、传输加密（HTTPS）、最小权限、定期备份与警惕钓鱼链接。个人层面也要管好权限与分享范围。",
        "公共Wi-Fi上登录重要账号时，优先使用HTTPS网站并开启双因素认证，降低窃听与撞库风险。",
        "CIA三元组中的“完整性”主要指？",
        ["数据随时可访问", "数据不被未授权篡改", "数据只有自己看得见", "网速足够快"],
        1,
        "完整性关注数据真实、完整、不被未授权修改。",
        "常见误区是只靠“复杂密码”而忽视钓鱼与软件更新，或把隐私分享给不可信应用；安全是技术措施与行为习惯的组合。",
    ),
    "it-h-internet-applications": C(
        "互联网应用：Web、HTTP 与邮件",
        "常见互联网应用基于客户端—服务器模式。Web 用浏览器访问服务器上的资源；HTTP/HTTPS 规定请求与响应的格式与语义（方法如 GET/POST、状态码如 200/404）。电子邮件通过 SMTP 发送、用 POP3/IMAP 接收。理解“协议+端口+资源定位（URL）”有助于判断应用如何通信、为何打不开网页或邮件失败。",
        "方法：跟一次完整请求路径",
        "以访问网页为例：解析URL→DNS查IP→建立连接（HTTPS还握手）→发送HTTP请求→服务器返回响应→浏览器渲染。排错时看域名、网络、证书、状态码分别对应哪一环。邮件则分清发信与收信协议角色不同。",
        "输入 https://example.com/a 时，浏览器向该主机请求路径 /a；若返回 404，说明连接可能成功但资源不存在。",
        "HTTPS 相对 HTTP 的主要增强是？",
        ["页面一定更快", "传输加密与身份校验，提升安全性", "不再需要域名", "只能用于邮件"],
        1,
        "HTTPS 在 HTTP 之上提供加密与证书校验，保护传输安全。",
        "常见误区是把“能上网”等同于“应用层协议都懂”，或混淆 HTTP 状态码含义；应把 URL、DNS、HTTP、渲染分成环节理解。",
    ),
    "it-h-network-basics": C(
        "计算机网络基础与 TCP/IP",
        "计算机网络按覆盖范围可分为局域网、广域网等；互联网是全球互联的网络集合。TCP/IP 协议族分层协作：应用层（HTTP、DNS等）、传输层（TCP可靠、UDP尽力而为）、网络层（IP寻址与路由）、网络接口层。IP 地址标识主机，端口区分应用进程。理解分层能解释“为什么网页慢/连不上/能ping但不能浏览”等现象落在哪一层。",
        "方法：分层定位故障",
        "排错自上而下或自下而上：先看物理/链路（网线、Wi-Fi），再看IP与网关，再测端口连通，最后查应用配置。记住 TCP 面向连接、适合可靠传输；UDP 开销小，适合实时音视频等可容忍少量丢失的场景。",
        "浏览器打不开网站但能 ping 通IP：多半是DNS或应用层/端口问题，而非完全断网。",
        "传输层中更强调可靠传输的是？",
        ["UDP", "TCP", "IP", "HTTP"],
        1,
        "TCP 提供面向连接的可靠传输；UDP 不保证可靠。",
        "常见误区是把 IP 地址与 MAC、端口混为一谈，或认为所有应用都必须用 TCP；应按分层与业务需求选择协议。",
    ),
    "it-h-programming-basics": C(
        "程序设计基础：变量与数据类型",
        "程序用变量保存可变数据，变量有名字、类型与当前值。常见基本类型包括整数、浮点数、字符串、布尔值；复合类型如列表/字典在后续结构中展开。赋值是把值写入变量；表达式求值后再用于运算或输出。类型决定能做哪些运算（如字符串不宜直接与数字相加而不转换）。养成“先想数据表示，再写语句”的习惯。",
        "方法：名正、型对、值清",
        "命名用有意义标识符；明确每个变量存什么、类型是否匹配运算；对输入做类型转换（如字符串转整数）。调试时打印关键变量，检查是否未初始化或类型错误。",
        "从键盘读入的年龄若是字符串 \"16\"，计算成年与否前应转为整数，再与 18 比较。",
        "变量最核心的作用是？",
        ["美化代码缩进", "在程序运行过程中保存可变数据", "替代所有函数", "提高网速"],
        1,
        "变量用于在程序运行中保存和更新数据。",
        "常见误区是变量未赋值就使用、类型不匹配仍强行运算，或用难以理解的单字母命名导致逻辑混乱。",
    ),
    "it-h-recursion": C(
        "递归与分治：自己调用自己解决问题",
        "递归是函数直接或间接调用自身。正确递归通常具备：明确的递归边界（基准情形）、问题规模逐步缩小、向基准情形收敛。分治把大问题分解为相似子问题，分别解决后合并结果（如归并排序、二分思想）。递归调用借助系统调用栈保存现场；过深递归可能导致栈溢出，可用迭代或尾递归优化思路理解。",
        "方法：先写边界，再写递推式",
        "设计递归：①定义函数含义；②写出最小规模直接答案；③假设子问题已解决，写出如何合并。用小例子手推调用展开与返回过程，确认不会无限递归。",
        "阶乘：n!=n×(n-1)!，边界 0!=1；斐波那契也可用递归，但朴素写法存在大量重复计算，需注意效率。",
        "递归函数必须具备的要素是？",
        ["可以没有结束条件", "基准情形（递归边界）与问题规模缩小", "只能用于排序", "不能有返回值"],
        1,
        "必须有边界且规模缩小，否则会无限递归。",
        "常见误区是缺少边界条件，或子问题规模没有真正变小；另一误区是把所有问题都硬套递归，不顾重复计算与栈深度。",
    ),
    "it-h-sorting-searching": C(
        "排序与查找：让数据有序、让目标可达",
        "排序将数据按关键字排列，常见有冒泡、插入、选择（易理解，多约O(n²)）以及更快的归并、快速排序等（平均约O(n log n)）。查找在集合中定位目标：无序多用顺序查找；有序可用二分查找，时间约O(log n)。算法选择取决于数据规模、是否近似有序、稳定性需求与内存限制。",
        "方法：先看是否有序，再选策略",
        "若需多次查找，可先排序再二分；若只查一次且数据很小，顺序查找更直接。比较算法时关注最坏/平均复杂度与是否稳定。动手模拟2–3轮冒泡或一次二分区间收缩，建立过程直觉。",
        "在已按升序排好的1000个学号中查某人：二分每次排除一半，大约10次内可定位，远快于从头扫到尾。",
        "二分查找适用的前提通常是？",
        ["数据任意无序即可", "数据已按关键字有序（或可随机访问的有序序列）", "只能用于字符串", "数据必须用栈存储"],
        1,
        "二分查找要求序列有序（并通常支持随机访问）。",
        "常见误区是对无序数据直接套二分，或只记名称不模拟过程；应理解有序性前提，并能比较不同排序在小规模教学场景下的取舍。",
    ),
}


STYLE = """
<style id="ith-depth-css">
.ith-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.ith-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(96,165,250,.08);border:1px solid rgba(96,165,250,.28)}
.ith-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.ith-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.ith-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.ith-depth .ith-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.ith-depth .ith-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
</style>
"""

CHECK_SCRIPT = """
<script id="ith-depth-js">
function ithDepthCheck(button, isCorrect, feedbackId, explanation) {
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
    feedback_id = "ith-depth-feedback"
    options = []
    for idx, opt in enumerate(cfg["options"]):
        correct = idx == cfg["correct"]
        handler = "ithDepthCheck(this,{c},'{f}',{e})".format(
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
  <section class="section ith-depth core-knowledge-module text-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section ith-depth core-knowledge-module text-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="ith-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析要点</h3>
        <p>{html.escape(cfg['question'])}</p>
        {''.join(options)}
        <div class="ith-feedback" id="{feedback_id}" role="status"></div>
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
    if 'id="ith-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="ith-depth-js"' not in source:
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
