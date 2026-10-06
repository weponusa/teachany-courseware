/**
 * 知识点中文显示名（全科图谱 / PBL / 详情面板共用）
 */
(function (global) {
  'use strict';

  function hasCjk(text) {
    return /[\u4e00-\u9fff]/.test(String(text || ''));
  }

  function resolveNodeDisplayName(node) {
    if (!node) return '';
    const display = node.display_name || node.displayName;
    if (display && String(display).trim()) return String(display).trim();
    const nameZh = node.name_zh;
    if (nameZh && hasCjk(nameZh)) return String(nameZh).trim();
    const name = String(node.name || '').trim();
    if (hasCjk(name)) return name;
    const en = String(node.name_en || '').trim();
    return name || en || String(node.id || '');
  }

  function resolveNodeEnglishSubtitle(node) {
    if (!node) return '';
    const primary = resolveNodeDisplayName(node);
    const en = String(node.name_en || '').trim();
    if (!en || en === primary) return '';
    if (hasCjk(primary) && !hasCjk(en)) return en;
    return '';
  }

  function applyDisplayFields(node) {
    if (!node || typeof node !== 'object') return node;
    const displayName = resolveNodeDisplayName(node);
    node.display_name = displayName;
    if (hasCjk(displayName) && !hasCjk(node.name) && node.name && !node.name_en) {
      node.name_en = node.name;
      node.name = displayName;
    }
    return node;
  }

  global.KnowledgeNodeDisplay = {
    hasCjk,
    resolveNodeDisplayName,
    resolveNodeEnglishSubtitle,
    applyDisplayFields,
  };
})(typeof window !== 'undefined' ? window : globalThis);
