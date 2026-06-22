#!/usr/bin/env python3
"""
对于引用了不存在 PNG 的课件，有两种策略：
1. 移除 figure 块（干净但失去占位）
2. 恢复为 SVG 占位（至少有个图标显示）

本脚本采用策略2：对于缺失图片的引用，恢复为 Cursor 创建的 SVG 占位符
（因为 SVG 占位符至少能显示一个示意图形，比 404 更好）。

同时确保课件本地有 SVG 占位文件。
"""

import os
import re
import json
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO_ROOT)

COMMIT = "77afbab0"

# SVG 占位符内容（简约版）
HERO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400">
  <rect width="800" height="400" fill="#1e293b"/>
  <circle cx="400" cy="180" r="60" fill="none" stroke="#60a5fa" stroke-width="3"/>
  <path d="M370 180 L400 150 L430 180 L400 210 Z" fill="#60a5fa" opacity="0.3"/>
  <text x="400" y="280" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="18">课件封面</text>
</svg>'''

CONCEPT_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500">
  <rect width="800" height="500" fill="#1e293b"/>
  <circle cx="400" cy="200" r="80" fill="none" stroke="#60a5fa" stroke-width="2"/>
  <circle cx="250" cy="350" r="50" fill="none" stroke="#34d399" stroke-width="2"/>
  <circle cx="550" cy="350" r="50" fill="none" stroke="#f59e0b" stroke-width="2"/>
  <line x1="350" y1="260" x2="280" y2="310" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="450" y1="260" x2="520" y2="310" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="400" y="205" text-anchor="middle" fill="#e2e8f0" font-family="system-ui" font-size="16">核心概念</text>
  <text x="250" y="355" text-anchor="middle" fill="#e2e8f0" font-family="system-ui" font-size="14">要素A</text>
  <text x="550" y="355" text-anchor="middle" fill="#e2e8f0" font-family="system-ui" font-size="14">要素B</text>
  <text x="400" y="460" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="14">核心概念示意图</text>
</svg>'''

PROCESS_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400">
  <rect width="800" height="400" fill="#1e293b"/>
  <rect x="80" y="160" width="140" height="80" rx="12" fill="none" stroke="#60a5fa" stroke-width="2"/>
  <rect x="280" y="160" width="140" height="80" rx="12" fill="none" stroke="#34d399" stroke-width="2"/>
  <rect x="480" y="160" width="140" height="80" rx="12" fill="none" stroke="#f59e0b" stroke-width="2"/>
  <path d="M220 200 L270 200" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M420 200 L470 200" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow)"/>
  <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8"/></marker></defs>
  <text x="150" y="205" text-anchor="middle" fill="#e2e8f0" font-family="system-ui" font-size="14">明确概念</text>
  <text x="350" y="205" text-anchor="middle" fill="#e2e8f0" font-family="system-ui" font-size="14">掌握方法</text>
  <text x="550" y="205" text-anchor="middle" fill="#e2e8f0" font-family="system-ui" font-size="14">情境练习</text>
  <text x="400" y="320" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="14">方法与应用示意图</text>
</svg>'''


def get_affected_dirs():
    """获取受影响的课件目录"""
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{COMMIT}^..{COMMIT}"],
        capture_output=True, text=True
    )
    files = result.stdout.strip().split('\n')
    dirs = set()
    for f in files:
        if f.startswith("community/") and "/index.html" in f:
            dirs.add(os.path.dirname(f))
    return sorted(dirs)


def check_images_exist(course_dir):
    """检查课件目录中图片是否存在"""
    index_path = os.path.join(course_dir, "index.html")
    if not os.path.exists(index_path):
        return True, []  # 无需处理
    
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    missing = []
    for match in re.finditer(r'src="(\./assets/[^"]+\.png)"', html):
        img_path = match.group(1)
        full_path = os.path.join(course_dir, img_path.lstrip('./'))
        if not os.path.exists(full_path):
            missing.append(img_path)
    
    return len(missing) == 0, missing


def fix_course(course_dir, missing_images):
    """修复单个课件：将缺失 PNG 引用替换为 SVG 占位符"""
    index_path = os.path.join(course_dir, "index.html")
    manifest_path = os.path.join(course_dir, "manifest.json")
    assets_dir = os.path.join(course_dir, "assets")
    
    os.makedirs(assets_dir, exist_ok=True)
    
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    replacements = {}
    
    for img in missing_images:
        # 判断类型
        basename = os.path.basename(img)
        if 'hero' in basename:
            svg_name = "hero-infographic.svg"
            svg_content = HERO_SVG
        elif 'section1' in basename or 'concept' in basename:
            svg_name = "concept-diagram.svg"
            svg_content = CONCEPT_SVG
        elif 'section2' in basename or 'process' in basename:
            svg_name = "process-diagram.svg"
            svg_content = PROCESS_SVG
        else:
            svg_name = "hero-infographic.svg"
            svg_content = HERO_SVG
        
        svg_path = os.path.join(assets_dir, svg_name)
        if not os.path.exists(svg_path):
            with open(svg_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
        
        replacements[img] = f"./assets/{svg_name}"
    
    # 替换 HTML
    for old, new in replacements.items():
        html = html.replace(f'src="{old}"', f'src="{new}"')
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 修复 manifest
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            try:
                manifest = json.load(f)
            except json.JSONDecodeError:
                return
        
        if 'assets' in manifest:
            assets = manifest['assets']
            # 修复 hero
            hero_val = assets.get('hero', '')
            for old, new in replacements.items():
                old_manifest = old.lstrip('./')
                new_manifest = new.lstrip('./')
                if hero_val == old_manifest:
                    assets['hero'] = new_manifest
                if 'images' in assets:
                    assets['images'] = [new_manifest if x == old_manifest else x for x in assets['images']]
            
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
                f.write('\n')


def main():
    dirs = get_affected_dirs()
    print(f"检查 {len(dirs)} 个课件目录...")
    print("=" * 60)
    
    fixed = 0
    ok = 0
    
    for d in dirs:
        all_ok, missing = check_images_exist(d)
        if all_ok:
            ok += 1
        else:
            fix_course(d, missing)
            fixed += 1
            print(f"  🔧 {d} (修复 {len(missing)} 个缺失图片)")
    
    print("=" * 60)
    print(f"完成: {ok} 个课件图片完整, {fixed} 个课件已用 SVG 占位修复")


if __name__ == "__main__":
    main()
