#!/usr/bin/env python3
"""interactive-kit.py — 课件自包含动画 & 互动组件（零外部依赖）
注入内容：
  A. SVG 元素依次入场动画 + 关键元素循环演示动画（CSS，自动施加）
  B. 分步过程播放器（播放/上一步/下一步/自动，逐步高亮 SVG 图元 + 解说）
  C. 参数滑块模拟器（拖动参数实时看结果变化，含公式与结论）
  D. 拖拽排序互动（拖动纸条排顺序，即时判定）
  E. 热点探究图（点击图元显示说明）
用法: python3 interactive-kit.py <cid>
"""
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_KEY = os.environ["OPENROUTER_API_KEY"]
MODEL = os.environ.get("ZH_MODEL", "deepseek/deepseek-chat-v3-0324")

CSS = """
/* ===== TeachAny 互动组件库 ===== */
.ta-kit{margin:22px 0;padding:18px 20px;border-radius:14px;background:linear-gradient(160deg,rgba(30,41,59,.55),rgba(15,23,42,.45));border:1px solid rgba(148,163,184,.22)}
.ta-kit h3{margin:0 0 4px;font-size:17px}
.ta-kit .ta-sub{font-size:13px;color:var(--muted);margin:0 0 12px}
/* B 分步播放器 */
.ta-stepper .ta-stage{background:rgba(10,21,32,.5);border:1px solid rgba(148,163,184,.18);border-radius:12px;padding:10px;min-height:60px}
.ta-stepper .ta-stage svg{max-height:280px}
.ta-stepper .ta-desc{font-size:15px;line-height:1.7;margin:12px 0;min-height:52px}
.ta-stepper .ta-desc b{color:#fbbf24}
.ta-stepper .ta-ctrl{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.ta-btn{background:rgba(59,130,246,.18);border:1px solid rgba(96,165,250,.45);color:#e2e8f0;padding:7px 14px;border-radius:9px;cursor:pointer;font-size:14px;transition:.18s}
.ta-btn:hover{background:rgba(59,130,246,.32);transform:translateY(-1px)}
.ta-btn:disabled{opacity:.4;cursor:not-allowed}
.ta-progress{height:5px;background:rgba(148,163,184,.2);border-radius:3px;overflow:hidden;margin:12px 0}
.ta-progress i{display:block;height:100%;background:linear-gradient(90deg,#3b82f6,#34d399);width:0;transition:width .35s}
.ta-step-badge{font-size:12px;background:rgba(52,211,153,.18);border:1px solid rgba(52,211,153,.4);padding:3px 10px;border-radius:20px}
/* C 参数滑块 */
.ta-sim .ta-row{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin:10px 0}
.ta-sim input[type=range]{flex:1;min-width:200px;accent-color:#3b82f6;height:5px}
.ta-sim .ta-val{font-variant-numeric:tabular-nums;font-size:19px;font-weight:700;color:#fbbf24;min-width:96px}
.ta-sim .ta-out{margin-top:12px;padding:14px;border-radius:11px;background:rgba(10,21,32,.55);border:1px solid rgba(148,163,184,.2)}
.ta-sim .ta-out .ta-formula{font-family:ui-monospace,Menlo,monospace;font-size:14px;color:#7dd3fc;margin-bottom:8px}
.ta-sim .ta-out .ta-concl{font-size:15px}
.ta-bar-wrap{height:22px;background:rgba(148,163,184,.15);border-radius:6px;overflow:hidden;margin-top:8px}
.ta-bar{height:100%;background:linear-gradient(90deg,#3b82f6,#34d399);width:0;transition:width .3s;display:flex;align-items:center;justify-content:flex-end;padding-right:8px;font-size:12px;color:#0b1220;font-weight:700}
/* D 拖拽排序 */
.ta-sort-list{list-style:none;padding:0;margin:12px 0;display:flex;flex-direction:column;gap:8px}
.ta-sort-item{padding:11px 14px;background:rgba(59,130,246,.14);border:1px solid rgba(96,165,250,.38);border-radius:9px;cursor:grab;user-select:none;font-size:15px;transition:.15s;display:flex;gap:10px;align-items:center}
.ta-sort-item:hover{background:rgba(59,130,246,.26)}
.ta-sort-item.dragging{opacity:.4}
.ta-sort-item.over{border-color:#34d399;background:rgba(52,211,153,.2)}
.ta-sort-item .ta-idx{width:22px;height:22px;border-radius:50%;background:rgba(148,163,184,.25);display:grid;place-items:center;font-size:12px;flex:none}
.ta-sort-item.ok{background:rgba(52,211,153,.2);border-color:rgba(52,211,153,.6)}
.ta-sort-item.ok .ta-idx{background:rgba(52,211,153,.55)}
.ta-fb{margin-top:10px;font-size:14px;min-height:20px}
.ta-fb.ok{color:#34d399}.ta-fb.no{color:#fbbf24}
/* SVG 动画 */
.ta-anim-svg [data-anim]{opacity:0;animation:taIn .5s ease forwards}
@keyframes taIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.ta-anim-svg [data-pulse]{animation:taPulse 1.8s ease-in-out infinite}
@keyframes taPulse{0%,100%{opacity:1}50%{opacity:.42}}
.ta-anim-svg [data-flow]{stroke-dasharray:7 5;animation:taFlow 1.1s linear infinite}
@keyframes taFlow{to{stroke-dashoffset:-24}}
.ta-hl{filter:drop-shadow(0 0 7px #fbbf24);transition:.3s}
.ta-dim{opacity:.22;transition:.3s}
@media (prefers-reduced-motion:reduce){.ta-anim-svg [data-anim],.ta-anim-svg [data-pulse],.ta-anim-svg [data-flow]{animation:none;opacity:1}}
"""

JS = """
/* ===== TeachAny 互动组件库 ===== */
(function(){
  // A. SVG 依次入场 + 循环动画
  document.querySelectorAll('svg.math-fig').forEach(function(svg){
    if(svg.dataset.animDone) return; svg.dataset.animDone='1';
    svg.classList.add('ta-anim-svg');
    var shapes=[].filter.call(svg.children,function(e){return e.tagName!=='defs';});
    shapes.forEach(function(el,i){
      if(el.tagName==='rect'&&(!el.getAttribute('fill')||el.getAttribute('fill')==='#0a1520')) return;
      el.setAttribute('data-anim','');
      el.style.animationDelay=(i*0.07)+'s';
    });
    // 箭头/连线流动动画
    [].forEach.call(svg.querySelectorAll('[marker-end],polyline[stroke],path[stroke^="#"]'),function(el){
      if(el.tagName==='path'||el.tagName==='polyline'||el.tagName==='line'){
        if(!el.hasAttribute('data-anim')) el.setAttribute('data-anim','');
        el.setAttribute('data-flow','');
      }
    });
    // 圆形/关键节点呼吸
    [].forEach.call(svg.querySelectorAll('circle'),function(el,i){
      if(i<3) el.setAttribute('data-pulse','');
    });
  });

  // B. 分步播放器
  function initStepper(box){
    var steps=(JSON.parse(decodeURIComponent(escape(atob(box.getAttribute('data-ta-cfg')||'')))||'{}')).steps||[];
    if(!steps.length) return;
    var stage=box.querySelector('.ta-stage'), desc=box.querySelector('.ta-desc'),
        bar=box.querySelector('.ta-progress i'), badge=box.querySelector('.ta-step-badge'),
        btnP=box.querySelector('[data-act=prev]'), btnN=box.querySelector('[data-act=next]'),
        btnA=box.querySelector('[data-act=auto]'), btnR=box.querySelector('[data-act=reset]');
    var cur=0, timer=null;
    var svgs=[].slice.call(document.querySelectorAll('svg.math-fig'));
    function paint(){
      var st=steps[cur];
      desc.innerHTML='<b>'+st.title+'</b>：'+st.desc;
      badge.textContent='第 '+(cur+1)+' / '+steps.length+' 步';
      bar.style.width=((cur+1)/steps.length*100)+'%';
      btnP.disabled=cur===0; btnN.disabled=cur===steps.length-1;
      // 高亮：把当前步骤指定的关键词对应的图元点亮（无匹配时不变暗，避免整图发灰）
      var kws=(st.hl||'').split('|').filter(function(x){return x;});
      var hit=0;
      if(kws.length){
        svgs.forEach(function(svg){
          [].forEach.call(svg.children,function(el){
            el.classList.remove('ta-hl','ta-dim');
            var t=(el.textContent||'')+(el.getAttribute('aria-label')||'');
            if(t&&kws.some(function(k){return t.indexOf(k)>=0;})){ el.classList.add('ta-hl'); hit++; }
          });
        });
        if(hit>0){
          svgs.forEach(function(svg){
            [].forEach.call(svg.children,function(el){
              if(!el.classList.contains('ta-hl')) el.classList.add('ta-dim');
            });
          });
        } else {
          svgs.forEach(function(svg){
            [].forEach.call(svg.children,function(el){ el.classList.remove('ta-dim'); });
          });
        }
      } else {
        svgs.forEach(function(svg){
          [].forEach.call(svg.children,function(el){ el.classList.remove('ta-hl','ta-dim'); });
        });
      }
    }
    function go(d){
      cur=Math.max(0,Math.min(steps.length-1,cur+d)); paint();
    }
    btnP&&btnP.addEventListener('click',function(){stop();go(-1);});
    btnN&&btnN.addEventListener('click',function(){stop();go(1);});
    btnR&&btnR.addEventListener('click',function(){stop();cur=0;paint();});
    function stop(){ if(timer){clearInterval(timer);timer=null;btnA&&(btnA.textContent='▶ 自动播放');} }
    btnA&&btnA.addEventListener('click',function(){
      if(timer){stop();return;}
      btnA.textContent='⏸ 暂停';
      timer=setInterval(function(){ if(cur>=steps.length-1){stop();return;} go(1); },2600);
    });
    paint();
  }
  // 统一启动（可重入：页面重渲染后仍能初始化）
  function boot(){
    [].forEach.call(document.querySelectorAll('[data-ta-cfg]'),function(box){
      if(box.getAttribute('data-ta-inited')) return;
      try{
        if(box.classList.contains('ta-stepper')) initStepper(box);
        else if(box.classList.contains('ta-sim')) initSim(box);
        else if(box.classList.contains('ta-sort')) initSort(box);
        box.setAttribute('data-ta-inited','1');
      }catch(e){ console.error('[ta-kit] 组件初始化失败', e); }
    });
  }
  boot();
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot);
  window.addEventListener('load',boot);
  setTimeout(boot,1200); setTimeout(boot,3000);

  // C. 参数滑块模拟器
  function initSim(box){
    var cfg=JSON.parse(decodeURIComponent(escape(atob(box.getAttribute('data-ta-cfg')||'')))||'{}');
    if(!cfg.items) return;
    var wrap=box.querySelector('.ta-items'), out=box.querySelector('.ta-out');
    cfg.items.forEach(function(it,i){
      var row=document.createElement('div'); row.className='ta-row';
      row.innerHTML='<span style="min-width:130px;font-size:14px">'+it.label+'</span>'+
        '<input type="range" min="'+it.min+'" max="'+it.max+'" step="'+it.step+'" value="'+(it.value!=null?it.value:it.def)+'">'+
        '<span class="ta-val" data-i="'+i+'"></span>';
      wrap.appendChild(row);
    });
    var inputs=[].slice.call(box.querySelectorAll('input[type=range]'));
    var vals=[].slice.call(box.querySelectorAll('.ta-val'));
    function num(v){return Math.round(v*100)/100;}
    function render(){
      var v=inputs.map(function(el){return parseFloat(el.value);});
      vals.forEach(function(el,i){ el.textContent=num(v[i])+' '+(cfg.items[i].unit||''); });
      var res;
      try{
        var fn=new Function('v','with(Math){'+cfg.expr+'}');
        res=fn(v);
      }catch(e){ res=null; }
      var html='<div class="ta-formula">'+cfg.formula+'</div>';
      if(res!=null){
        html+='<div class="ta-bar-wrap"><div class="ta-bar" style="width:'+
          Math.max(2,Math.min(100,cfg.pct?Math.min(100,res*100/cfg.pct):50))+'%">'+num(res)+' '+(cfg.unit||'')+'</div></div>';
        var idx=cfg.bands?cfg.bands.findIndex(function(b){return res<b[0];}):-1;
        if(idx<0&&cfg.bands) idx=cfg.bands.length-1;
        html+='<div class="ta-concl" style="margin-top:10px">'+
          (idx>=0?cfg.bands[idx][1]:(cfg.note||''))+'</div>';
      }
      out.innerHTML=html;
    }
    inputs.forEach(function(el){ el.addEventListener('input',render); });
    render();
  }

  // D. 拖拽排序
  function initSort(box){
    var cfg=JSON.parse(decodeURIComponent(escape(atob(box.getAttribute('data-ta-cfg')||'')))||'{}');
    if(!cfg.items) return;
    var ul=box.querySelector('.ta-sort-list'), fb=box.querySelector('.ta-fb'),
        btn=box.querySelector('[data-act=check]'), btnR2=box.querySelector('[data-act=shuffle]');
    function draw(order){
      ul.innerHTML='';
      order.forEach(function(txt,i){
        var li=document.createElement('li');
        li.className='ta-sort-item'; li.draggable=true; li.dataset.i=i;
        li.innerHTML='<span class="ta-idx">'+(i+1)+'</span><span>'+txt+'</span>';
        ul.appendChild(li);
      });
      bind();
    }
    function bind(){
      var dragEl=null;
      [].forEach.call(ul.children,function(li){
        li.addEventListener('dragstart',function(){dragEl=li;li.classList.add('dragging');});
        li.addEventListener('dragend',function(){li.classList.remove('dragging');
          [].forEach.call(ul.children,function(x){x.classList.remove('over');});});
        li.addEventListener('dragover',function(e){e.preventDefault();li.classList.add('over');});
        li.addEventListener('dragleave',function(){li.classList.remove('over');});
        li.addEventListener('drop',function(e){
          e.preventDefault(); li.classList.remove('over');
          if(!dragEl||dragEl===li) return;
          var arr=[].map.call(ul.children,function(x){return x.textContent.replace(/^\\d+/,'');});
          var from=[].indexOf.call(ul.children,dragEl), to=[].indexOf.call(ul.children,li);
          arr.splice(to,0,arr.splice(from,1)[0]);
          draw(arr); fb.textContent=''; fb.className='ta-fb';
        });
      });
    }
    btn&&btn.addEventListener('click',function(){
      var now=[].map.call(ul.children,function(x){return x.textContent.replace(/^\\d+/,'');});
      var ok=now.every(function(t,i){return t===cfg.items[i];});
      [].forEach.call(ul.children,function(li,i){
        if(now[i]===cfg.items[i]) li.classList.add('ok'); else li.classList.remove('ok');
      });
      fb.className='ta-fb '+(ok?'ok':'no');
      fb.textContent=ok?('✅ 完全正确！'+(cfg.why||''))
        :('❌ 顺序还不对，'+(cfg.hint||'再想想各步骤的先后逻辑'));
    });
    btnR2&&btnR2.addEventListener('click',function(){
      var a=cfg.items.slice(); for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}
      draw(a); fb.textContent=''; fb.className='ta-fb';
    });
    draw(cfg.items.slice().sort(function(){return Math.random()-.5;}));
  }
})();
"""

PROMPT = """你是中国{stage}{subject}教师，也是课件互动设计师。课件《{title}》要加入动画互动组件。

知识背景：
{current}

请设计 3 个互动组件的**内容**（不需要写代码），直接输出 JSON（无 markdown 围栏）：

{{
  "steps": [
    {{"title": "步骤名（4-8字）", "desc": "这一步发生什么、为什么，40-70字，可含<em>强调</em>", "hl": "该步要在这课件的SVG图中高亮的中文词，多个用|分隔（如：活塞|进气门），没有则空字符串"}},
    ...（严格 4-6 步，描述一个完整的动态过程，首尾呼应）
  ],
  "sim": {{
    "title": "模拟器名称（6-15字）",
    "desc": "一句说明这个模拟器演示什么关系（20-40字）",
    "items": [{{"label": "参数名", "unit": "单位", "min": 数字, "max": 数字, "step": 数字, "def": 默认数字}}],
    "expr": "JS表达式，用 v[0]、v[1] 表示各参数值，可用 Math.*，返回数字结果（例如：return v[0]*v[1]/100;）",
    "formula": "结果=公式的文字版（如：效率 = 有用功 W有 ÷ 总功 W总 × 100%）",
    "unit": "结果单位（如 %、J、℃）",
    "pct": 结果满量程数值（用于进度条，如实质的百分比填100，若结果范围0-50填50）,
    "bands": [[数值上界, "结果在这个范围时的结论说明（25-45字，说明含义）"], [更大的上界, "结论"], [999999, "结论"]]
  }},
  "sort": {{
    "title": "排序题标题（8-18字）",
    "prompt": "任务指令（如：把下列实验步骤按正确顺序排列）",
    "items": ["正确顺序的第1项（8-20字）", "第2项", "第3项", "第4项"],
    "why": "正确顺序背后的逻辑（30-50字）",
    "hint": "错误时的提示（15-30字）"
  }}
}}

要求：
1. steps 必须是一个真实、连贯、可逐步演示的过程（如化学制氧的"查-装-定-点-收-离-熄"、物理四冲程、生物ATP循环、数学证明步骤、语文写作步骤、英语时态构成、地理区位分析流程、信息技术的请求响应过程）
2. sim 必须是本学科真实定量关系（有公式、单位），参数 1-3 个，数值范围符合教学实际
3. sort 的 items 严格按正确顺序给出 4 项，是真实的操作/思维步骤
4. 全部中文，术语准确，符合{stage}{subject}教材"""


def llm_json(body, max_tokens=3500):
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps({"model": MODEL, "messages": [{"role": "user", "content": body}],
                                 "temperature": 0.6, "max_tokens": max_tokens}).encode(),
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json",
                         "HTTP-Referer": "https://teachany.cn", "X-OpenRouter-Title": "interactive-kit"})
            with urllib.request.urlopen(req, timeout=220) as r:
                txt = json.load(r)["choices"][0]["message"]["content"]
            t = re.sub(r"```(?:json)?", "", txt)
            b = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", t[t.find("{"):])
            try:
                obj, _ = json.JSONDecoder().raw_decode(b)
                return obj
            except json.JSONDecodeError:
                return json.loads(re.sub(r",\s*([}\]])", r"\1", b[:b.rfind("}") + 1]))
        except Exception as e:
            last = e
            time.sleep((attempt + 1) * 12)
    raise last


def b64(obj):
    """JSON → base64（避免引号/尖括号/换行破坏 HTML 属性）"""
    import base64 as _b
    return _b.b64encode(json.dumps(obj, ensure_ascii=False).encode("utf-8")).decode()


def esc(s):
    """HTML 文本/属性转义（属性值一律用双引号包裹，转义 & < > " '）"""
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#39;"))


def build_stepper(steps, cid):
    if not steps:
        return ""
    return (f'<div class="ta-kit ta-stepper" data-ta-cfg="{b64({"steps": steps})}">'
            f'<h3>🎬 过程演示：分步动画</h3>'
            f'<p class="ta-sub">点击「下一步」逐步观看，或「自动播放」连续演示；图片中会高亮当前步骤的关键部位。</p>'
            f'<div class="ta-stage">'
            f'<svg viewBox="0 0 480 320" class="math-fig" style="max-height:240px">'
            f'<text x="240" y="160" font-size="16" fill="#94a3b8" text-anchor="middle">点击下方按钮开始分步演示 ↓</text></svg>'
            f'</div>'
            f'<p class="ta-desc"></p>'
            f'<div class="ta-progress"><i></i></div>'
            f'<div class="ta-ctrl"><button type="button" class="ta-btn" data-act="prev">← 上一步</button>'
            f'<button type="button" class="ta-btn" data-act="next">下一步 →</button>'
            f'<button type="button" class="ta-btn" data-act="auto">▶ 自动播放</button>'
            f'<button type="button" class="ta-btn" data-act="reset">↺ 重置</button>'
            f'<span class="ta-step-badge"></span></div></div>')


def build_sim(sim):
    if not sim or not sim.get("items"):
        return ""
    cfg = {"items": sim.get("items", []), "expr": sim.get("expr", "return 0;"),
           "formula": sim.get("formula", ""), "unit": sim.get("unit", ""),
           "pct": sim.get("pct", 100), "bands": sim.get("bands", [])}
    return (f'<div class="ta-kit ta-sim" data-ta-cfg="{b64(cfg)}">'
            f'<h3>🎛️ {esc(sim.get("title", "参数模拟器"))}</h3>'
            f'<p class="ta-sub">{esc(sim.get("desc", ""))}</p>'
            f'<div class="ta-items"></div><div class="ta-out"></div></div>')


def build_sort(sort):
    if not sort or not sort.get("items"):
        return ""
    cfg = {"items": sort["items"], "why": sort.get("why", ""), "hint": sort.get("hint", "再想想先后逻辑")}
    return (f'<div class="ta-kit ta-sort" data-ta-cfg="{b64(cfg)}">'
            f'<h3>🖱️ {esc(sort.get("title", "排序练习"))}</h3>'
            f'<p class="ta-sub">{esc(sort.get("prompt", "拖动条目排成正确顺序"))}（按住条目上下拖动）</p>'
            f'<ul class="ta-sort-list"></ul>'
            f'<div class="ta-ctrl"><button type="button" class="ta-btn" data-act="check">✓ 检查顺序</button>'
            f'<button type="button" class="ta-btn" data-act="shuffle">🔀 打乱重排</button></div>'
            f'<div class="ta-fb"></div></div>')


def process(cid):
    P = ROOT / "community" / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    if "data-ta-cfg" in html:
        print(f"[{cid}] 已有互动组件")
        return
    if "data-ta-stepper" in html:  # 清理旧版残留
        html = re.sub(r'<div class="ta-kit ta-stepper"[\s\S]*?</div>\s*</div>', '', html)
        html = re.sub(r'<script>\s*/\s*\*\s*=+\s*TeachAny 互动组件库[\s\S]*?</script>', '', html)
    subject = cid.split("-")[0]
    stage = {"h": "高中", "m": "初中", "e": "小学"}.get(cid.split("-")[1], "初中")

    tm = re.search(r"<title>([^<·《》]+)", html)
    title = tm.group(1).strip()[:40] if tm else cid
    m = re.search(r'id="lesson-focus"[\s\S]*?</section>', html)
    current = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(0))).strip()[:500] if m else title

    print(f"[{cid}] 生成互动内容…")
    g = llm_json(PROMPT.format(stage=stage, subject=subject, title=title, current=current))

    # 数值合理性校验：默认参数代入后结果应落在合理区间，否则重生成一次
    def eval_sim(sim, v):
        expr = (sim.get("expr") or "").strip()
        if not expr:
            return None
        body = expr if "\n" in expr else "    " + expr
        src = "def _f(v):\n" + ("\n".join("    " + l for l in expr.splitlines()) if "\n" in expr else "    " + expr)
        try:
            ns = {}
            exec(compile(src, "<sim>", "exec"), {"__builtins__": __builtins__, "Math": __import__("math")}, ns)
            return ns["_f"](v)
        except Exception:
            return None

    def sim_ok(sim):
        items = sim.get("items", []) if sim else []
        if not items:
            return False
        v = [it.get("def", it.get("min", 0)) for it in items]
        res = eval_sim(sim, v)
        pct = (sim.get("pct") or 100)
        return isinstance(res, (int, float)) and 0.5 <= res <= pct * 1.5

    if not sim_ok(g.get("sim", {})):
        print("  模拟器数值不合理，重新生成…")
        try:
            g2 = llm_json(PROMPT.format(stage=stage, subject=subject, title=title, current=current))
            if sim_ok(g2.get("sim", {})):
                g = g2
            else:
                print("  仍不合理，跳过模拟器")
                g.pop("sim", None)
        except Exception:
            g.pop("sim", None)

    blocks = [build_stepper(g.get("steps", []), cid), build_sim(g.get("sim", {})), build_sort(g.get("sort", {}))]
    blocks = [b for b in blocks if b]
    if not blocks:
        print(f"[{cid}] 内容生成失败")
        return

    if "ta-stepper .ta-stage" not in html:
        html = html.replace("</style>", CSS + "\n</style>", 1)

    # 插到知识图谱前（页面后半段）
    anchor = re.search(r'<section\b[^>]*id="knowledge-graph"', html)
    if anchor:
        html = html[:anchor.start()] + "\n".join(blocks) + "\n" + html[anchor.start():]
    else:
        mp = re.search(r'<section\b[^>]*id="posttest"', html)
        html = html[:mp.start()] + "\n".join(blocks) + "\n" + html[mp.start():] if mp else html.replace("</body>", "\n".join(blocks) + "\n</body>", 1)

    if "function boot()" not in html:
        html = html.replace("</body>", "<script>\n" + JS + "\n</script>\n</body>", 1)

    P.write_text(html, encoding="utf-8")
    print(f"[{cid}] 注入 {len(blocks)} 个互动组件")


if __name__ == "__main__":
    process(sys.argv[1])
