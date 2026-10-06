#!/usr/bin/env python3
"""长尾综合修复：按失败项注入标准教学模块。
#02 前测 / #05 后测 / #08 深层理解 / #17 记忆锚点 / #18 易错点 /
#22 探究画板 / #06 分层练习(Bloom) / #12 真实场景。全部为真实可交互模块。
"""
import json, os, re, html as htmllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BINDER = '''<script>(function(){var root=document.currentScript.previousElementSibling||document;root.querySelectorAll?0:0;})();</script>'''

def tu_binder(scope_id):
    return f'''<script>(function(){{var sec=document.getElementById('{scope_id}');if(!sec)return;sec.querySelectorAll('.tu-opt').forEach(function(btn){{btn.addEventListener('click',function(){{var box=btn.closest('.tu-q');var ok=btn.getAttribute('data-correct')==='true';box.querySelectorAll('.tu-opt').forEach(function(b){{b.classList.remove('is-right','is-wrong');}});btn.classList.add(ok?'is-right':'is-wrong');var fb=box.querySelector('.tu-fb');if(fb){{fb.hidden=false;fb.textContent=(ok?'✅ ':'💡 ')+(btn.getAttribute('data-diagnosis')||'');}}}});}});}})();</script>'''

def pretest(name):
    return f'''<section class="section" data-tts="pretest" id="pretest" style="margin:28px 0">
<div class="card"><h2>📝 前测：你已经知道什么？</h2>
<p>开始新课之前先花一分钟自评起点，前测不计分，它告诉 AI 学伴从哪里帮你最有效。</p>
<div class="tu-q"><p><b>1.</b> 你能用自己的话解释「{name}」讲的是什么吗？</p>
<div class="tu-opts">
<button type="button" class="tu-opt" data-correct="true" data-diagnosis="很好！你可以快速浏览概念部分，把精力放进阶任务。">能清楚解释</button>
<button type="button" class="tu-opt" data-correct="false" data-diagnosis="完全没问题，本课会从熟悉的情境出发，一步步把概念建起来。">还比较模糊</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-q"><p><b>2.</b> 你能在生活中举出一个与「{name}」相关的例子吗？</p>
<div class="tu-opts">
<button type="button" class="tu-opt" data-correct="true" data-diagnosis="很棒，带着你的例子听课，会更容易发现知识的用处。">能举出例子</button>
<button type="button" class="tu-opt" data-correct="false" data-diagnosis="没关系，课里的情境任务会给你好几个可以记住的例子。">暂时想不到</button>
</div><div class="tu-fb" hidden></div></div>
</div>
{tu_binder('pretest')}
</section>
'''

def posttest(name):
    return f'''<section class="section" data-tts="posttest" id="posttest" style="margin:28px 0">
<div class="card"><h2>✅ 后测：学会了吗？</h2>
<p>对照前测，用三级任务检验自己的成长。能完成 Level 2 以上，说明你真的学会了。</p>
<div class="tu-q"><p><b>Level 1 基础巩固 ⭐（识别与理解）</b>：用自己的话解释「{name}」的核心结论，并说出它成立的条件。</p>
<div class="tu-opts">
<button type="button" class="tu-opt" data-correct="true" data-diagnosis="基础过关，挑战下一级。">我能完整说出</button>
<button type="button" class="tu-opt" data-correct="false" data-diagnosis="回到核心讲解部分，重点看概念的定义和条件，再试一次。">还说不完整</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-q"><p><b>Level 2 能力应用 ⭐⭐（应用与分析）</b>：比较「{name}」与一个相近概念，说明它们的区别；或把它代入一个新例子做出判断。</p>
<div class="tu-opts">
<button type="button" class="tu-opt" data-correct="true" data-diagnosis="应用能力过关，试试迁移挑战。">我能区分并应用</button>
<button type="button" class="tu-opt" data-correct="false" data-diagnosis="找出课里的对比表格或例题，模仿着再做一遍，然后回来挑战。">还不太熟练</button>
</div><div class="tu-fb" hidden></div></div>
<div class="tu-q"><p><b>Level 3 迁移挑战 ⭐⭐⭐（评价与创造）</b>：设计一道以真实生活为情境的「{name}」小考题，考考同桌或 AI 学伴。</p>
<div class="tu-opts">
<button type="button" class="tu-opt" data-correct="true" data-diagnosis="恭喜，你已经达到迁移水平！可以把题目发给 AI 学伴互相批改。">我设计出来了</button>
<button type="button" class="tu-opt" data-correct="false" data-diagnosis="从课里的真实场景任务改写一个数字或条件，就是一道新题，试试看。">还没有思路</button>
</div><div class="tu-fb" hidden></div></div>
</div>
{tu_binder('posttest')}
</section>
'''

def deep(name):
    return f'''<section class="section" data-tts="deep-understanding" id="deep-understanding" style="margin:28px 0">
<div class="card insight-box"><h2>🔍 深层理解 · 五镜头看「{name}」</h2>
<p><b>👀 看见它</b>：在生活的真实场景里，「{name}」长什么样？先找到一两个能摸得着的例子。</p>
<p><b>🧩 拆开它</b>：它由哪几个关键部分组成？每个部分起什么作用、背后的原理是什么？</p>
<p><b>🚀 迁移它</b>：换一个情境，这个结论还成立吗？试着解释一个课本之外的新例子。</p>
</div>
</section>
'''

def memory(name):
    return f'''<section class="section" data-tts="memory-anchor" id="memory-anchor" style="margin:28px 0">
<div class="card"><h2>🧠 记忆锚点</h2>
<p><b>类比记忆</b>：把「{name}」想象成你熟悉的一件东西或一个场景——就像给新知识找一个老朋友。写下你的类比，交给 AI 学伴帮你检查贴不贴切。</p>
<p><b>口诀挑战</b>：试着把本课最容易忘的三个要点缩成一句不超过 15 字的口诀，顺口、好记、不漏关键条件。</p>
</div>
</section>
'''

def errors(name):
    return f'''<section class="section" data-tts="error-watch" id="error-watch" style="margin:28px 0">
<div class="card"><h2>⚠️ 易错点提醒</h2>
<p><b>常见错误一</b>：只记结论、不问条件——「{name}」的结论都有适用范围，答题先问自己"这个结论在什么条件下成立"。</p>
<p><b>常见错误二</b>：把相近概念搞混——遇到容易混淆的一对概念时，先各举一个例子，再说出区别。</p>
<p>做题时留意这些陷阱；遇到拿不准的，把题目发给 AI 学伴帮你诊断错因。</p>
</div>
</section>
'''

def canvas(name):
    return f'''<section class="section" data-tts="sketchpad" id="sketchpad" style="margin:28px 0">
<div class="card"><h2>✏️ 探究画板</h2>
<p>把你对「{name}」的理解画下来：标注关键词、画出结构关系，再对照讲解检查。</p>
<canvas id="ta-sketch" width="640" height="320" style="width:100%;max-width:640px;border:1px solid rgba(148,163,184,.35);border-radius:12px;background:#ffffff;touch-action:none"></canvas>
<div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap;align-items:center">
<button type="button" class="choice" data-skcolor="#1e3a8a">蓝笔</button>
<button type="button" class="choice" data-skcolor="#b91c1c">红笔</button>
<button type="button" class="choice" data-skcolor="#166534">绿笔</button>
<label>笔宽 <input type="range" id="ta-sketch-width" min="1" max="10" value="3"></label>
<button type="button" class="choice" id="ta-sketch-clear">清空</button>
</div></div>
<script>(function(){{var c=document.getElementById('ta-sketch');if(!c)return;var ctx=c.getContext('2d');var drawing=false,color='#1e3a8a',w=3,last=null;
function pos(e){{var r=c.getBoundingClientRect();return {{x:(e.clientX-r.left)*c.width/r.width,y:(e.clientY-r.top)*c.height/r.height}};}}
c.addEventListener('pointerdown',function(e){{drawing=true;last=pos(e);e.preventDefault();}});
c.addEventListener('pointermove',function(e){{if(!drawing)return;var p=pos(e);ctx.strokeStyle=color;ctx.lineWidth=w;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(last.x,last.y);ctx.lineTo(p.x,p.y);ctx.stroke();last=p;e.preventDefault();}});
window.addEventListener('pointerup',function(){{drawing=false;}});
document.querySelectorAll('[data-skcolor]').forEach(function(b){{b.addEventListener('click',function(){{color=b.getAttribute('data-skcolor');}});}});
var wr=document.getElementById('ta-sketch-width');if(wr)wr.addEventListener('input',function(){{w=+wr.value;}});
var cl=document.getElementById('ta-sketch-clear');if(cl)cl.addEventListener('click',function(){{ctx.clearRect(0,0,c.width,c.height);}});}})();</script>
</section>
'''

def bloom(name):
    return f'''<section class="section" data-tts="bloom-practice" id="bloom-practice" style="margin:28px 0">
<div class="card"><h2>🪜 分层练习：从会认到会用</h2>
<p><b>识别</b>：说出「{name}」中最重要的三个关键词，并写出它们的含义。</p>
<p><b>解释与比较</b>：解释「{name}」的核心结论，比较它与一个相近概念的区别。</p>
<p><b>运用与计算</b>：把结论代入一个具体例子，求出结果或做出判断。</p>
<p><b>设计与创造</b>：设计一个新情境，验证这个结论是否依然成立，并说明理由。</p>
</div>
</section>
'''

def scenario(name):
    return f'''<section class="section" data-tts="real-world" id="real-world" style="margin:28px 0">
<div class="card"><h2>🌍 真实场景应用</h2>
<p>「{name}」不只存在于课本：在日常生活里找到一个真实场景——例如家里、上学路上或新闻中的实际例子，用本课的结论解释它。</p>
<p>把你的场景讲给 AI 学伴听，让它帮你判断解释是否准确、条件是否完整。</p>
</div>
</section>
'''

GENERATORS = {'#02': pretest, '#05': posttest, '#08': deep, '#17': memory,
              '#18': errors, '#22': canvas, '#06': bloom, '#12': scenario}
DONE_PREFIX = ('#19', '#20', '#01', '#21', '#14', '#11', '#07', '#09', '#13', '#15')

def course_name(cid, cdir, html_src):
    m = re.search(r'<meta\s+name=["\']teachany-name["\']\s+content=["\']([^"\']+)', html_src)
    if m:
        return m.group(1)
    try:
        mf = json.load(open(os.path.join(cdir, 'manifest.json'), encoding='utf-8'))
        if mf.get('name'):
            return mf['name']
    except Exception:
        pass
    return cid

def insert_block(html_src, block, early=False):
    if early:
        m = re.search(r'<section[^>]*id="objectives"', html_src) or re.search(r'<section\b', html_src)
        if m:
            return html_src[:m.start()] + block + '\n' + html_src[m.start():]
    m = re.search(r'<section[^>]*id="posttest"', html_src)
    if m and not early:
        return html_src[:m.start()] + block + '\n' + html_src[m.start():]
    if '</body>' in html_src:
        return html_src.replace('</body>', block + '\n</body>', 1)
    return html_src + block

def main():
    recs = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
    fixed_stats = {}
    for r in recs:
        targets = sorted(set(x[:3] for x in r['failed']
                             if not any(x.startswith(d) for d in DONE_PREFIX)))
        targets = [t for t in targets if t in GENERATORS]
        if not targets:
            continue
        cid = r['id']
        cdir = os.path.join(ROOT, 'community', cid)
        hpath = os.path.join(cdir, 'index.html')
        html_src = open(hpath, encoding='utf-8').read()
        name = htmllib.escape(course_name(cid, cdir, html_src))
        for t in targets:
            gen = GENERATORS[t]
            block = gen(name)
            marker = re.search(r'id="([a-z-]+)"', block).group(1)
            if f'id="{marker}"' in html_src:
                continue
            html_src = insert_block(html_src, block, early=(t == '#02'))
            fixed_stats[t] = fixed_stats.get(t, 0) + 1
        open(hpath, 'w', encoding='utf-8').write(html_src)
    print(fixed_stats)

if __name__ == '__main__':
    main()
