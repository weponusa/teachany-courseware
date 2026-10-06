#!/usr/bin/env python3
"""生成 text-data.js —— 将课文原文内联到 JS 文件中，避免 file:// 下 fetch 失败"""
import os, json, re, glob

OUTPUT = 'data/text-data.js'
TEXTS_DIR = 'texts'
BOOK_DIR = f'{TEXTS_DIR}/快乐读书吧'
LESSON_INDEX_FILE = 'lesson_index.json'

def escape_js(s):
    """转义 JS 字符串中的特殊字符"""
    s = s.replace('\\', '\\\\')
    s = s.replace("'", "\\'")
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '')
    return s

def main():
    lesson_idx = json.load(open(LESSON_INDEX_FILE))
    entries = {}
    
    # 遍历每个年级目录
    for key, names in lesson_idx.items():
        if key == '快乐读书吧':
            continue
        dir_path = f'{TEXTS_DIR}/{key}'
        if not os.path.isdir(dir_path):
            continue
        for name in names:
            fpath = f'{dir_path}/{name}.txt'
            if not os.path.exists(fpath):
                # 尝试 fallback 文件名
                fpath2 = f'{dir_path}/{name}'
                if not os.path.exists(fpath2):
                    continue
                fpath = fpath2
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            # key = "一上/秋天"
            entry_key = f'{key}/{name}'
            entries[entry_key] = content

    # 遍历课外阅读（快乐读书吧）目录
    if os.path.isdir(BOOK_DIR):
        for fname in sorted(os.listdir(BOOK_DIR)):
            if not fname.endswith('.txt'):
                continue
            name = fname[:-4]  # 去掉 .txt
            fpath = os.path.join(BOOK_DIR, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            entry_key = f'快乐读书吧/{name}'
            entries[entry_key] = content
    
    # 生成 JS 文件
    lines = ['// 自动生成 - 课文原文内联数据', '// 由 scripts/build_text_data_js.py 生成', '', 'window.TEXT_DATA = window.TEXT_DATA || {};', '']
    for key, content in entries.items():
        escaped = escape_js(content)
        lines.append(f"window.TEXT_DATA['{key}'] = '{escaped}';")
    
    js_content = '\n'.join(lines)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"✅ {OUTPUT} 已生成: {len(entries)} 篇课文, {size_kb:.0f} KB")

if __name__ == '__main__':
    main()
