#!/usr/bin/env python3
"""Default Leaflet map config for auto-generated CN history/geography specs."""
from __future__ import annotations

import re

WORLD_HINTS = (
    "世界", "全球", "欧洲", "美洲", "美国", "英国", "法国", "俄国", "苏联",
    "联合国", "冷战", "全球化", "工业革命", "文艺复兴", "启蒙", "殖民",
    "一战", "二战", "两次大战", "世界大战", "资本主义", "社会主义",
    "古希腊", "古罗马", "中世纪", "新航路", "探索", "近代化",
)
CHINA_ERA_RULES = (
    (r"史前|远古|原始", "bce-3000", "史前", "#94a3b8"),
    (r"夏商周|青铜|先秦|商朝|周朝", "qin-dynasty", "先秦—秦", "#6366f1"),
    (r"秦汉|秦统一|汉武帝|西汉|东汉", "west-han-dynasty", "秦汉", "#f59e0b"),
    (r"三国|魏晋|南北朝|东晋", "three-kingdoms", "三国两晋", "#ef4444"),
    (r"隋唐|贞观|开元|隋朝|唐朝", "tang-dynasty", "隋唐", "#10b981"),
    (r"宋|辽|金|宋元", "song-dynasty", "宋代", "#8b5cf6"),
    (r"元|蒙古", "yuan-dynasty", "元代", "#a855f7"),
    (r"明|明清", "ming-dynasty", "明代", "#0ea5e9"),
    (r"清|鸦片|洋务|维新|辛亥|近代|民国", "qing-dynasty", "清代", "#64748b"),
)
WORLD_ERA_RULES = (
    (r"古代|希腊|罗马|古典|城邦", "bce-500", "古典时代", "#0ea5e9"),
    (r"中世纪|封建", "ce-1000", "中世纪", "#8b5cf6"),
    (r"文艺复兴|宗教改革|启蒙", "ce-1600", "近代早期", "#6366f1"),
    (r"工业革命|近代化", "ce-1815-vienna", "工业革命", "#f59e0b"),
    (r"一战|二战|世界大战|冷战", "ce-1914-wwi", "20世纪", "#ef4444"),
    (r"全球化|当代|联合国", "ce-2000", "当代世界", "#22c55e"),
)


def _match_era(text: str, rules: tuple) -> tuple[str, str, str] | None:
    for pattern, file_key, label, color in rules:
        if re.search(pattern, text):
            return file_key, label, color
    return None


def _era_entry(file_key: str, label: str, color: str, desc: str, cities: list | None = None) -> dict:
    eid = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-") or "era"
    return {
        "id": eid,
        "label": label,
        "file": f"{file_key}.geojson",
        "fill": color,
        "stroke": color,
        "desc": desc,
        "cities": cities or [],
    }


def is_world_scope(title: str, node_id: str = "") -> bool:
    blob = f"{title} {node_id}"
    return any(h in blob for h in WORLD_HINTS)


def default_map_config(spec: dict) -> dict | None:
    subject = (spec.get("subject") or "").lower()
    title = spec.get("title") or spec.get("node_id", "本课")
    node_id = spec.get("node_id", "")
    if subject not in ("history", "geography"):
        return None

    if subject == "geography":
        return {
            "title": f"{title} · 区域地图",
            "scope": "china",
            "center": [35, 105],
            "zoom": 4,
            "fitBounds": [[18, 73], [54, 135]],
            "terrain": True,
            "eras": [
                _era_entry(
                    "tang-dynasty",
                    "中国疆域",
                    "#22c55e",
                    f"<strong>{title}</strong>：运用地图阅读区域位置、范围与空间联系。",
                    [
                        [39.90, 116.40, "北京", "Beijing", "首都"],
                        [31.23, 121.47, "上海", "Shanghai", "东部沿海"],
                        [34.34, 108.94, "西安", "Xi'an", "西北枢纽"],
                        [23.13, 113.26, "广州", "Guangzhou", "南方门户"],
                    ],
                )
            ],
            "overlays": [
                {
                    "id": "provinces",
                    "label": "省界",
                    "file": "china-provinces.json",
                    "style": {"color": "#3b82f6", "weight": 1},
                    "visible": True,
                },
                {
                    "id": "rivers",
                    "label": "河流",
                    "file": "rivers-historical.geojson",
                    "style": {"color": "#0ea5e9", "weight": 2},
                    "visible": False,
                },
            ],
        }

    world = is_world_scope(title, node_id)
    if world:
        picked = []
        blob = f"{title} {node_id}"
        for pattern, file_key, label, color in WORLD_ERA_RULES:
            if re.search(pattern, blob):
                picked.append(_era_entry(file_key, label, color, f"<strong>{label}</strong>：{title}相关世界史地图。"))
        if not picked:
            picked = [
                _era_entry("ce-1700", "1700 前夜", "#94a3b8", f"<strong>{title}</strong>：工业革命前的世界格局。"),
                _era_entry("ce-1815-vienna", "工业革命", "#6366f1", f"<strong>{title}</strong>：工业化与全球扩张。"),
                _era_entry("ce-1914-wwi", "一战前夜", "#ef4444", f"<strong>{title}</strong>：20世纪世界巨变。"),
            ]
        return {
            "title": f"{title} · 世界历史地图",
            "scope": "world",
            "center": [45, 15],
            "zoom": 3,
            "fitBounds": [[25, -15], [60, 50]],
            "terrain": True,
            "eras": picked[:4],
        }

    picked = []
    blob = f"{title} {node_id}"
    for pattern, file_key, label, color in CHINA_ERA_RULES:
        if re.search(pattern, blob):
            picked.append(_era_entry(file_key, label, color, f"<strong>{label}</strong>：{title}相关史实地图。"))
    if not picked:
        picked = [
            _era_entry("west-han-dynasty", "秦汉", "#f59e0b", f"<strong>{title}</strong>：中国古代历史地图。"),
            _era_entry("tang-dynasty", "隋唐", "#10b981", f"<strong>{title}</strong>：盛世与制度演变。"),
            _era_entry("qing-dynasty", "清代", "#64748b", f"<strong>{title}</strong>：近代前夜的中国。"),
        ]
    return {
        "title": f"{title} · 历史地图",
        "scope": "china",
        "center": [34, 108],
        "zoom": 4,
        "fitBounds": [[18, 72], [52, 140]],
        "terrain": True,
        "eras": picked[:4],
        "overlays": [
            {
                "id": "capitals",
                "label": "古都",
                "file": "capitals-extended.geojson",
                "style": {"color": "#a855f7", "radius": 4},
                "visible": False,
            }
        ],
    }
