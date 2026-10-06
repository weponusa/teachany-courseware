/**
 * TeachAny v7.3 教学质量闸门（浏览器端）
 * 与 scripts/validate-teaching-quality.py 规则对齐，供浏览器提交前预检。
 */
(function (global) {
  'use strict';

  const EXT_NODE_RE = /^ext-[a-f0-9]{6,12}$/i;
  const MIN_IMAGE_BYTES = 5 * 1024;
  const MIN_AUDIO_BYTES = 5 * 1024;

  const PLACEHOLDER_PATTERNS = [
    /TODO/i, /待补/, /待填写/, /占位/, /\bplaceholder\b/i, /lorem ipsum/i,
    /这里(填写|补充|插入)/, /请在此/, /示例文本/, /\bxxx\b/i, /【[^】]{0,30}】/,
  ];
  const GENERIC_PHRASES = [
    '本节课我们将学习', '通过本节课的学习', '掌握相关知识', '提升学习兴趣',
    '加深理解', '培养能力', '重要知识点', '核心概念', '拓展延伸',
  ];
  const DIAGNOSTIC_WORDS = ['错因', '诊断', '因为', '误区', '提示', '再想', '错误', '不是', '关键在于'];
  const PRODUCTION_WORDS = ['解释', '说明', '设计', '分析', '论证', '产出', '开放任务', '迁移', '探究'];

  function normalizePath(path) {
    return String(path || '').replace(/^\.?\//, '').replace(/\\/g, '/');
  }

  function stripTags(html) {
    return String(html || '')
      .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ' ')
      .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, ' ')
      .replace(/<[^>]+>/g, ' ')
      .replace(/&[a-zA-Z]+;/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function countChineseLike(text) {
    return (String(text || '').match(/[\u4e00-\u9fffA-Za-z0-9]/g) || []).length;
  }

  function extractSections(html) {
    const sections = [];
    const sectionRe = /<section\b[^>]*>([\s\S]*?)<\/section>/gi;
    let m;
    while ((m = sectionRe.exec(html)) !== null) sections.push(m[1]);
    if (sections.length) return sections;
    const divRe = /<div\b[^>]*class=['"][^'"]*(?:section|module|card)[^'"]*['"][^>]*>([\s\S]*?)<\/div>/gi;
    while ((m = divRe.exec(html)) !== null) sections.push(m[1]);
    return sections;
  }

  function issue(level, message) {
    return { level, message };
  }

  function validateFakeAssets(files, courseName) {
    const errors = [];
    for (const file of files || []) {
      const path = normalizePath(file.path);
      const size = file.blob?.size || 0;
      const base = path.split('/').pop() || path;
      if (/^assets\//i.test(path) && /\.(png|jpe?g|webp)$/i.test(path) && size < MIN_IMAGE_BYTES) {
        errors.push(issue('error', `${courseName}: 图片 ${base}（${size} 字节，疑似占位图）`));
      }
      if (/^tts\//i.test(path) && /\.(mp3|wav|ogg|m4a)$/i.test(path) && size < MIN_AUDIO_BYTES) {
        errors.push(issue('error', `${courseName}: 音频 ${base}（${size} 字节，疑似静音占位）`));
      }
    }
    return errors;
  }

  function validateHtmlContent(html, manifest, courseName) {
    const issues = [];
    if (!html) {
      issues.push(issue('error', `${courseName}: 缺少 index.html，无法进行教学质量审查`));
      return issues;
    }

    const text = stripTags(html);
    const textLen = countChineseLike(text);
    if (textLen < 1800) {
      issues.push(issue('error', `${courseName}: 有效教学文本仅 ${textLen} 字符 < 1800，疑似只有框架没有实质讲解`));
    }

    const htmlNoInputPlaceholder = html.replace(/\bplaceholder\s*=\s*['"][^'"]*['"]/gi, '');
    for (const pat of PLACEHOLDER_PATTERNS) {
      if (pat.test(htmlNoInputPlaceholder)) {
        issues.push(issue('error', `${courseName}: 检测到模板/占位残留`));
        break;
      }
    }

    let genericCount = 0;
    for (const phrase of GENERIC_PHRASES) {
      let idx = 0;
      while (html.indexOf(phrase, idx) !== -1) {
        genericCount += 1;
        idx += phrase.length;
      }
    }
    if (genericCount >= 8 && textLen < 3500) {
      issues.push(issue('error', `${courseName}: 泛化套话过多（${genericCount} 处）且文本偏少，疑似批量模板化输出`));
    }

    const sections = extractSections(html);
    const substantialSections = sections.filter((s) => countChineseLike(stripTags(s)) >= 120);
    if (substantialSections.length < 5) {
      issues.push(issue('error', `${courseName}: 实质 section 仅 ${substantialSections.length} 个 < 5，每个模块需有可读讲解、例子或任务`));
    }

    const moduleLike = sections.filter((s) => /module|concept|section|lesson|knowledge|核心|模块|知识/i.test(s));
    if (moduleLike.length < 3) {
      issues.push(issue('error', `${courseName}: 核心知识模块少于 3 个，无法构成完整课件`));
    }

    const hasPre = /pretest|前测|课前诊断/i.test(html);
    const hasPost = /posttest|后测|学习检测|达标检测/i.test(html);
    if (!hasPre || !hasPost) {
      issues.push(issue('error', `${courseName}: 缺少前测或后测，无法形成学习闭环`));
    }

    const nodeId = String(manifest?.node_id || '');
    const isExt = EXT_NODE_RE.test(nodeId);
    const isPblSup = manifest?.lesson_type === 'pbl-supplement' || isExt;

    const bloomLevels = new Set((html.match(/data-bloom-level=['"]([^'"]+)['"]/gi) || [])
      .map((s) => s.replace(/.*=['"]([^'"]+)['"].*/, '$1')));
    if (bloomLevels.size < 3) {
      issues.push(issue(isPblSup ? 'warn' : 'error', `${courseName}: Bloom 层级覆盖不足（${bloomLevels.size} 级），需至少 3 级并标注 data-bloom-level`));
    }

    const scaffolds = new Set((html.match(/data-scaffold=['"]([^'"]+)['"]/gi) || [])
      .map((s) => s.replace(/.*=['"]([^'"]+)['"].*/, '$1')));
    if (scaffolds.size < 2) {
      issues.push(issue(isPblSup ? 'warn' : 'error', `${courseName}: 脚手架分级不足，需至少 2 种 data-scaffold（full/partial/none）`));
    }

    if (!/data-conceptest=['"]true['"]/i.test(html)) {
      issues.push(issue(isPblSup ? 'warn' : 'error', `${courseName}: 缺少 ConcepTest 检查点（data-conceptest="true"）`));
    }

    if (!DIAGNOSTIC_WORDS.some((w) => text.includes(w))) {
      issues.push(issue('error', `${courseName}: 未检测到诊断性反馈关键词，练习不能只判对错`));
    }
    if (!PRODUCTION_WORDS.some((w) => text.includes(w))) {
      issues.push(issue('error', `${courseName}: 未检测到解释/分析/设计/迁移类产出任务，疑似只有讲解和选择题`));
    }

    const curriculum = manifest?.curriculum || 'cn-national';
    const standards = manifest?.curriculum_standards;
    if ((curriculum === 'cn-national' || curriculum === 'cn') && !standards) {
      if (isPblSup) {
        const pblCtx = manifest?.pbl_context;
        if (!pblCtx || typeof pblCtx !== 'object' || !String(pblCtx.project_goal || '').trim()) {
          issues.push(issue('warn', `${courseName}: PBL 补充课未填 curriculum_standards，建议 manifest.pbl_context.project_goal 说明课标外依据`));
        }
      } else {
        issues.push(issue('error', `${courseName}: manifest.curriculum_standards 为空，未证明课件对齐真实课标`));
      }
    } else if (Array.isArray(standards)) {
      const bad = standards.filter((s) => !s || typeof s !== 'object' || !s.content || !s.source);
      if (bad.length) {
        issues.push(issue('error', `${courseName}: curriculum_standards 存在缺 content/source 的条目`));
      }
    }

    return issues;
  }

  async function validateImportedCourse(record) {
    const files = record?.files || [];
    const manifest = record?.manifest || {};
    const courseName = manifest.name || manifest.node_id || record?.id || 'courseware';

    const allIssues = validateFakeAssets(files, courseName);

    const indexFile = files.find((f) => normalizePath(f.path) === 'index.html');
    let html = '';
    if (indexFile?.blob) {
      html = await indexFile.blob.text();
    }
    allIssues.push(...validateHtmlContent(html, manifest, courseName));

    const errors = allIssues.filter((i) => i.level === 'error').map((i) => i.message);
    const warnings = allIssues.filter((i) => i.level === 'warn').map((i) => i.message);

    return {
      ok: errors.length === 0,
      errors,
      warnings,
      textLength: countChineseLike(stripTags(html)),
      sections: extractSections(html).length,
    };
  }

  global.TeachAnyQualityGate = {
    validateImportedCourse,
    validateHtmlContent,
    validateFakeAssets,
  };
})(typeof window !== 'undefined' ? window : globalThis);
