#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将全部课件标准化为「标准图谱模块 v7.7.4」+「标准 AI 学伴模块 v7.7」。
稳健策略（幂等、可重入、杜绝重复 id）：
- 图谱：删除所有 id="knowledge-graph" 的旧区块与旧标记注释，注入唯一标准区块。
- 学伴：删除所有 id="teachany-ai-tutor-card" 的旧区块与旧标记注释，注入唯一标准区块。
- 始终补齐：head CSS、body 脚本(ai-tutor.js/teachany-tutor-card.js/teachany-knowledge-graph.js)、
  window.__TEACHANY_TUTOR_CONFIG__ 配置、knowledgeGraphData 变量。
- 拷贝 6 个标准资源文件到各课件 assets/scripts/（保证本地预览与版本一致）。
仅改 index.html + 补 assets/scripts。
"""
import json, os, re, shutil, sys

COMMUNITY = "/Users/wepon/CodeBuddy/一次函数/teachany-courseware/community"
SHARED = "/Users/wepon/CodeBuddy/一次函数/teachany-courseware/assets/scripts"
ASSET_FILES = [
    "ai-tutor.css", "ai-tutor.js",
    "teachany-tutor-card.css", "teachany-tutor-card.js",
    "teachany-knowledge-graph.css", "teachany-knowledge-graph.js",
]
PPT_ANCHOR = "<!-- ═══ PPT 播放控件"

def esc(s):
    return (s or "").replace('\\', '\\\\').replace('"', '\\"')

def load_manifest(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return {}

def remove_all_sections(html, sec_id):
    return re.sub(r'<section\b[^>]*\bid="' + re.escape(sec_id) + r'"[^>]*>.*?</section>', '', html, flags=re.S)

def insert_before(html, token, block):
    if token in html:
        return html.replace(token, block + token, 1)
    return html.replace("</body>", block + "</body>", 1)

def ensure_css(html, css):
    if css not in html:
        html = html.replace("</head>", f'  <link rel="stylesheet" href="/assets/scripts/{css}">\n</head>', 1)
    return html

def ensure_script(html, src):
    if src not in html:
        html = insert_before(html, PPT_ANCHOR, f'<script src="/assets/scripts/{src}" defer></script>\n')
    return html

def build_kg_data(m, node_id, title):
    pre = m.get("prerequisites") or []
    ext = m.get("extends") or []
    def norm(lst):
        out = []
        for x in lst:
            if isinstance(x, dict):
                out.append({"id": x.get("id", ""), "name": x.get("name", x.get("id", ""))})
            else:
                out.append({"id": str(x), "name": str(x)})
        return out
    return {"prerequisites": norm(pre),
            "current": {"id": node_id, "name": title, "status": "active"},
            "extends": norm(ext)}

def extract_node(html, m, d):
    om = re.search(r'data-teachany-kg="([^"]+)"', html)
    return om.group(1) if om else (m.get("node_id") or d)

def standardize(html, m, d):
    title = m.get("title") or m.get("name") or d
    title = re.sub(r"[（(].*?[)）]", "", str(title)).strip() or d
    subject = m.get("subject") or "general"
    grade = m.get("grade")
    try:
        grade = int(grade)
    except Exception:
        grade = 0

    # ===== 学伴模块 =====
    html = re.sub(r'<!-- ⭐ v7.7 标准 AI 学伴入口卡片（必须显式存在，不能仅依赖 FAB） -->\s*', '', html)
    html = remove_all_sections(html, "teachany-ai-tutor-card")
    html = ensure_css(html, "ai-tutor.css")
    html = ensure_css(html, "teachany-tutor-card.css")
    if 'window.__TEACHANY_TUTOR_CONFIG__' not in html:
        cfg = ('<!-- ⭐ v6.11 AI 学伴配置（必须在 ai-tutor.js 加载前定义） -->\n'
               '<script>\nwindow.__TEACHANY_TUTOR_CONFIG__ = {\n'
               f'  courseTitle: "{esc(title)}",\n  subject: "{esc(str(subject))}",\n  grade: {grade},\n  learningObjectives: []\n}};\n</script>\n')
        if 'ai-tutor.js' in html:
            html = html.replace('<script src="/assets/scripts/ai-tutor.js"', cfg + '<script src="/assets/scripts/ai-tutor.js"', 1)
        else:
            html = insert_before(html, PPT_ANCHOR, cfg)
    html = ensure_script(html, "ai-tutor.js")
    html = ensure_script(html, "teachany-tutor-card.js")
    std_card = ('<!-- ⭐ v7.7 标准 AI 学伴入口卡片（必须显式存在，不能仅依赖 FAB） -->\n'
                '<section class="ta-standard-section" id="teachany-ai-tutor-card">\n'
                '  <div data-teachany-tutor-card></div>\n</section>\n')
    html = insert_before(html, PPT_ANCHOR, std_card)

    # ===== 图谱模块 =====
    html = re.sub(r'<!-- v7.7.4 标准知识图谱模块 -->\s*', '', html)
    html = remove_all_sections(html, "knowledge-graph")
    html = ensure_css(html, "teachany-knowledge-graph.css")
    node_id = extract_node(html, m, d)
    fullname = m.get("name") or title
    std_graph = ('<!-- v7.7.4 标准知识图谱模块 -->\n'
                 '<section class="section" id="knowledge-graph" style="max-width:1080px;margin:24px auto;padding:0 20px;">\n'
                 f'  <h2 class="section-title">🗺️ 知识图谱：{esc(title)} — {esc(str(fullname))}</h2>\n'
                 f'  <div data-teachany-kg="{esc(node_id)}">\n'
                 '    <canvas class="tkg-fallback-canvas" width="720" height="120" aria-label="知识图谱互动画布" style="display:block;width:100%;max-height:140px;border-radius:12px;"></canvas>\n'
                 '  </div>\n</section>\n')
    html = insert_before(html, PPT_ANCHOR, std_graph)
    if 'knowledgeGraphData' not in html:
        kg = build_kg_data(m, node_id, title)
        kg_json = json.dumps(kg, ensure_ascii=False)
        html = insert_before(html, PPT_ANCHOR,
                             f'<script>const knowledgeGraphData={kg_json};\n// auto-injected standard graph data</script>\n')
    html = ensure_script(html, "teachany-knowledge-graph.js")

    # 拷贝标准资源文件
    adir = os.path.join(COMMUNITY, d, "assets", "scripts")
    os.makedirs(adir, exist_ok=True)
    for f in ASSET_FILES:
        src = os.path.join(SHARED, f)
        if os.path.isfile(src):
            shutil.copy(src, os.path.join(adir, f))
    return html

def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    done = 0
    for d in sorted(os.listdir(COMMUNITY)):
        dp = os.path.join(COMMUNITY, d)
        ip = os.path.join(dp, "index.html")
        if not os.path.isdir(dp) or not os.path.isfile(ip):
            continue
        m = load_manifest(os.path.join(dp, "manifest.json"))
        html = open(ip, encoding="utf-8").read()
        # 仅当确实需要改动时才写（避免无谓写入；但 remove+inject 对已是标准的也会重写，此处统一重写以保证一致）
        new_html = standardize(html, m, d)
        open(ip, "w", encoding="utf-8").write(new_html)
        done += 1
        if limit and done >= limit:
            break
    print(f"处理课件数: {done}")

if __name__ == "__main__":
    main()
