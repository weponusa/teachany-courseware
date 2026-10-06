#!/usr/bin/env python3
"""standardize-layout.py — 统一呈现基线：连续网页 + 宽度对齐 + 模块标准化

解决的问题：
  1. 部分课件被生成为「分页放映」形态——.slide-container 锁定视口高度并
     自带滚动（height:100dvh; overflow-y:auto; scroll-snap-type），
     .slide-page 每页占满一屏（min-height:100dvh）并垂直居中。
     这导致各课件观感割裂：有的像幻灯片，有的像普通网页。
  2. 主容器宽度五花八门（1080 / 960 / 900 / 920 / 860 / 780 / 1160…），
     且左右对齐方式不一致，整体不像同一套产品。

做法：在 </head> 前注入一段覆盖样式（不改动原有内容，可整体回退）：
  - 解除分页：容器不再锁定视口高度、不再滚动吸附，取消整屏分页与居中
  - 统一宽度：主容器 max-width 统一为 1080px 并水平居中
  - 统一节奏：section 上下间距、内边距取一致值

用法: python3 standardize-layout.py [cid...]     处理指定课件
      python3 standardize-layout.py --all         处理全库
      python3 standardize-layout.py --dry         只报告不写入
      python3 standardize-layout.py --remove      移除已注入的基线
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

MARK_BEGIN = "/* ===== TeachAny 统一呈现基线 ===== */"
MARK_END = "/* ===== /TeachAny 统一呈现基线 ===== */"

BASELINE = MARK_BEGIN + """
/* 1. 取消分页放映：连续网页，容器不锁视口高度、不滚动吸附 */
.slide-container{height:auto!important;max-height:none!important;
  overflow:visible!important;scroll-snap-type:none!important}
.slide-page{min-height:0!important;display:block!important;
  justify-content:flex-start!important;align-items:stretch!important;
  scroll-snap-align:none!important}
html,body{scroll-snap-type:none!important}

/* 2. 统一宽度与水平对齐：主容器一律 1080px 居中。
      必须 !important —— 部分课件在 body 内的 <style> 或内联 style 里
      另写了 .section{max-width:900px}，按普通优先级会盖掉基线。 */
.slide-container,.slide-inner{width:100%!important;max-width:1080px!important;
  margin-left:auto!important;margin-right:auto!important}
.section{max-width:1080px!important;margin-left:auto!important;
  margin-right:auto!important}

/* 3. 统一纵向节奏：模块间距一致，避免有的挤有的散 */
.slide-page{padding:34px 20px!important}
.section{padding-left:20px!important;padding-right:20px!important}

/* 窄屏仍退化为满宽，保证小屏可读 */
@media (max-width:1120px){
  .slide-container,.slide-inner,.section{max-width:100%!important}
}
""" + MARK_END


def has_baseline(html):
    return MARK_BEGIN in html


def apply(html):
    """注入基线；已存在则先移除再注入，保证幂等"""
    html = remove(html)
    # 插到 </head> 前，确保能覆盖此前的所有样式
    m = re.search(r"\s*</head>", html)
    css = f"\n<style>\n{BASELINE}\n</style>\n"
    if m:
        return html[:m.start()] + css + html[m.start():]
    # 没有 head 则插到 <body> 后
    m = re.search(r"<body[^>]*>", html)
    if m:
        return html[:m.end()] + css + html[m.end():]
    return None


def remove(html):
    """移除已注入的基线（含包裹的 style 标签）"""
    return re.sub(
        r"\n?<style>\s*" + re.escape(MARK_BEGIN) + r"[\s\S]*?"
        + re.escape(MARK_END) + r"\s*</style>\n?", "\n", html)


def process(cid, dry=False, do_remove=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    if do_remove:
        if not has_baseline(html):
            return 0
        new = remove(html)
    else:
        new = apply(html)
    if new is None or new == html:
        return 0
    if not dry:
        P.write_text(new, encoding="utf-8")
    return 1


def main():
    dry = "--dry" in sys.argv
    do_remove = "--remove" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--all" in sys.argv or not cids:
        cids = sorted(p.name for p in COMMUNITY.iterdir() if (p / "index.html").exists())
    n = 0
    for c in cids:
        try:
            n += process(c, dry, do_remove)
        except Exception as e:
            print(f"  ❌ {c}: {str(e)[:60]}")
    act = "移除" if do_remove else "注入"
    print(f"{act}统一呈现基线：{n} 个课件" + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
