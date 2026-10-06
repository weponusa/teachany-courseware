#!/usr/bin/env python3
"""
恢复 77afbab0 提交造成的破坏性图片引用替换。

该提交将真实 PNG 图片引用替换为通用占位 SVG：
  - xxx-hero.png → hero-infographic.svg
  - section1.png / concept-diagram.png → concept-diagram.svg
  - section2.png / process-diagram.png → process-diagram.svg

本脚本：
1. 从 git 历史获取提交前（77afbab0^）每个文件的真实图片引用
2. 将当前文件中的 SVG 引用替换回原始 PNG 引用
3. 保留路径修正（./assets/scripts/ 不还原为 /assets/scripts/）
4. 同时修复 manifest.json 中的引用
"""

import subprocess
import re
import os
import json

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO_ROOT)

COMMIT = "77afbab0"

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

def get_old_file_content(filepath):
    """获取提交前的文件内容"""
    result = subprocess.run(
        ["git", "show", f"{COMMIT}^:{filepath}"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return result.stdout
    return None

def extract_image_refs(html_content):
    """从 HTML 中提取图片引用"""
    refs = {}
    # hero image
    hero_match = re.search(r'class="hero-cover-img"\s+src="([^"]+)"', html_content)
    if hero_match:
        refs['hero'] = hero_match.group(1)
    # concept diagram (section1)
    concept_match = re.search(r'核心概念示意[^<]*</figcaption></figure>', html_content)
    if concept_match:
        img_match = re.search(r'<img\s+src="([^"]+)"[^>]*alt="[^"]*核心概念', html_content)
        if img_match:
            refs['concept'] = img_match.group(1)
    # process diagram (section2)
    process_match = re.search(r'方法与应用[^<]*</figcaption></figure>', html_content)
    if process_match:
        img_match = re.search(r'<img\s+src="([^"]+)"[^>]*alt="[^"]*方法与应用', html_content)
        if img_match:
            refs['process'] = img_match.group(1)
    return refs

def restore_course(course_dir):
    """恢复单个课件的图片引用"""
    index_path = os.path.join(course_dir, "index.html")
    manifest_path = os.path.join(course_dir, "manifest.json")
    
    if not os.path.exists(index_path):
        return False, "index.html 不存在"
    
    # 获取旧版本的图片引用
    old_html = get_old_file_content(index_path)
    if not old_html:
        return False, "无法获取旧版本"
    
    old_refs = extract_image_refs(old_html)
    if not old_refs:
        return False, "旧版本无图片引用"
    
    # 读取当前文件
    with open(index_path, 'r', encoding='utf-8') as f:
        current_html = f.read()
    
    modified = False
    
    # 替换 hero 图片
    if 'hero' in old_refs:
        old_hero = old_refs['hero']
        # 当前可能是 ./assets/hero-infographic.svg
        if 'hero-infographic.svg' in current_html:
            current_html = current_html.replace(
                './assets/hero-infographic.svg', old_hero
            )
            modified = True
    
    # 替换 concept diagram
    if 'concept' in old_refs:
        old_concept = old_refs['concept']
        if 'concept-diagram.svg' in current_html:
            current_html = current_html.replace(
                './assets/concept-diagram.svg', old_concept
            )
            modified = True
    
    # 替换 process diagram
    if 'process' in old_refs:
        old_process = old_refs['process']
        if 'process-diagram.svg' in current_html:
            current_html = current_html.replace(
                './assets/process-diagram.svg', old_process
            )
            modified = True
    
    if modified:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(current_html)
    
    # 修复 manifest.json
    manifest_modified = False
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            try:
                manifest = json.load(f)
            except json.JSONDecodeError:
                manifest = None
        
        if manifest and 'assets' in manifest:
            assets = manifest['assets']
            # 恢复 hero
            if 'hero' in old_refs and assets.get('hero') == 'assets/hero-infographic.svg':
                # 去掉 ./ 前缀
                hero_val = old_refs['hero'].lstrip('./')
                assets['hero'] = hero_val
                manifest_modified = True
            
            # 恢复 images 列表
            if 'images' in assets:
                new_images = []
                for img in assets['images']:
                    if img == 'assets/hero-infographic.svg' and 'hero' in old_refs:
                        new_images.append(old_refs['hero'].lstrip('./'))
                        manifest_modified = True
                    elif img == 'assets/concept-diagram.svg' and 'concept' in old_refs:
                        new_images.append(old_refs['concept'].lstrip('./'))
                        manifest_modified = True
                    elif img == 'assets/process-diagram.svg' and 'process' in old_refs:
                        new_images.append(old_refs['process'].lstrip('./'))
                        manifest_modified = True
                    else:
                        new_images.append(img)
                assets['images'] = new_images
            
            if manifest_modified:
                with open(manifest_path, 'w', encoding='utf-8') as f:
                    json.dump(manifest, f, ensure_ascii=False, indent=2)
                    f.write('\n')
    
    return modified or manifest_modified, old_refs

def main():
    dirs = get_affected_dirs()
    print(f"受影响的课件目录: {len(dirs)} 个")
    print("=" * 60)
    
    restored = 0
    skipped = 0
    errors = []
    
    for d in dirs:
        success, info = restore_course(d)
        if success:
            restored += 1
            refs_str = ", ".join(f"{k}={v}" for k, v in info.items()) if isinstance(info, dict) else str(info)
            print(f"  ✅ {d}")
            print(f"     恢复: {refs_str}")
        else:
            skipped += 1
            if "无图片引用" not in str(info):
                errors.append((d, info))
                print(f"  ⚠️  {d}: {info}")
    
    print("=" * 60)
    print(f"恢复完成: {restored} 个课件已修复, {skipped} 个跳过")
    if errors:
        print(f"异常: {len(errors)} 个")
        for d, err in errors:
            print(f"  - {d}: {err}")

if __name__ == "__main__":
    main()
