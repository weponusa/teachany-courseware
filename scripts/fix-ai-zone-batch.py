#!/usr/bin/env python3
"""批量为文科课件注入标准「AI 多模态互动区」（修复质检 #14）。

- slide 分页课件：在 slide-container 末尾追加一个 slide-page
- 连续滚动课件：在 posttest 前插入普通 section；无 posttest 则追加到 </body> 前
自带复制提示词 JS，提示词按课件名称定制。
"""
import json, os, re, html as htmllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BLOCK_TMPL = '''<section class="section" data-tts="ai-media" id="ai-media-zone">
<div class="card card-glow"><h2>🎨 AI 多模态互动</h2>
<p>复制提示词到 AI 学伴，生成「{name}」的{task}；也可以上传你手绘的示意图，请 AI 学伴点评。</p>
<textarea id="ai-prompt-box" rows="3" style="width:100%">{prompt}</textarea>
<button class="choice" id="copy-ai-prompt" type="button">📋 复制提示词</button>
<p class="feedback" id="ai-zone-feedback">复制后可粘贴到 AI 学伴继续对话。</p>
</div>
<script>(function(){{var b=document.getElementById('copy-ai-prompt');if(!b)return;b.addEventListener('click',function(){{var t=document.getElementById('ai-prompt-box');if(!t)return;t.focus();t.select();try{{document.execCommand('copy');}}catch(e){{}}if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t.value);var f=document.getElementById('ai-zone-feedback');if(f)f.textContent='✅ 已复制，去 AI 学伴粘贴吧';}});}})();</script>
</section>'''

TASKS = {
    'chinese': ('思维导图或赏析提纲', '请用表格总结「{name}」的核心意象、写作手法和一个易错点，并画一张文字版思维导图。'),
    'history': ('时间轴或事件提纲', '请用表格总结「{name}」的背景、经过、影响，并给出一条时间轴和一个易混点辨析。'),
    'english': ('mind map or summary table', 'Summarize "{name}" in a table: key rules, one example sentence, and one common mistake. Then describe a mind map.'),
    'geography': ('示意图或结构提纲', '请用表格总结「{name}」的核心概念、分布规律和形成原因，并描述一幅示意简图。'),
}

def course_name(cid, html):
    m = re.search(r'<meta\s+name=["\']teachany-name["\']\s+content=["\']([^"\']+)', html)
    if m: return m.group(1)
    m = re.search(r'<title>《?([^《》<·]+)》?', html)
    if m: return m.group(1).strip()
    try:
        mf = json.load(open(os.path.join(ROOT, 'community', cid, 'manifest.json'), encoding='utf-8'))
        if mf.get('name'): return mf['name']
    except Exception:
        pass
    return cid

def course_subject(cid, html):
    m = re.search(r'<meta\s+name=["\']teachany-subject["\']\s+content=["\']([^"\']+)', html)
    if m: return m.group(1).lower()
    p = cid.split('-')[0]
    return {'chn': 'chinese', 'hist': 'history', 'eng': 'english', 'geo': 'geography'}.get(p, p)

def find_container_end(html, start):
    """从 slide-container 开标签末尾起，找匹配的 </div> 结束位置。"""
    depth = 1
    for m in re.finditer(r'<div\b|</div>', html[start:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return start + m.start()
    return None

def inject(cid):
    hpath = os.path.join(ROOT, 'community', cid, 'index.html')
    html_src = open(hpath, encoding='utf-8').read()
    if 'ai-media-zone' in html_src or re.search(r'ai.?media|ai.?zone|ai.*互动|多模态|生成.*图|upload.*image', html_src, re.I):
        return 'already'
    name = course_name(cid, html_src)
    subj = course_subject(cid, html_src)
    task, prompt_t = TASKS.get(subj, TASKS['history'])
    prompt = prompt_t.format(name=name)
    block = BLOCK_TMPL.format(name=htmllib.escape(name), task=task, prompt=htmllib.escape(prompt))

    m = re.search(r'<div class="slide-container" id="slide-container">', html_src)
    if m:
        end = find_container_end(html_src, m.end())
        if end:
            n_pages = len(re.findall(r'class="slide-page"', html_src[:end]))
            slide = f'<section class="slide-page" data-page-index="{n_pages}" data-page-type="concept" data-tsh="AI 多模态互动">{block}</section>'
            html_src = html_src[:end] + slide + html_src[end:]
            open(hpath, 'w', encoding='utf-8').write(html_src)
            return 'slide'
    # 连续滚动：posttest 前插入
    m2 = re.search(r'<section[^>]*id="posttest"', html_src)
    if m2:
        html_src = html_src[:m2.start()] + block + '\n' + html_src[m2.start():]
    else:
        html_src = html_src.replace('</body>', block + '\n</body>', 1)
    open(hpath, 'w', encoding='utf-8').write(html_src)
    return 'scroll'

def main():
    recs = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
    f14 = [r['id'] for r in recs if any(x.startswith('#14') for x in r['failed'])]
    stats = {}
    for cid in f14:
        try:
            r = inject(cid)
        except Exception as e:
            r = f'error:{e}'
        stats[r] = stats.get(r, 0) + 1
    print(stats)

if __name__ == '__main__':
    main()
