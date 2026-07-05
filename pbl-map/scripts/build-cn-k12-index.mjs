#!/usr/bin/env node
/**
 * 构建 CN 小初高课标节点索引 + 补充信息科技树
 * 用法: node scripts/build-cn-k12-index.mjs [--engine ../engine]
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, '..');

const engineArg = process.argv.indexOf('--engine');
const engineBase = engineArg >= 0
  ? path.resolve(process.argv[engineArg + 1])
  : path.join(root, 'engine');

const metaPath = path.join(engineBase, 'data', 'nodes-metadata.json');
const outPath = path.join(root, 'data', 'cn-k12-nodes.json');
const legacyPrimaryPath = path.join(root, 'data', 'primary-cn-nodes.json');

/** 暂不纳入覆盖审计的学科（音体美等） */
const EXCLUDED_SUBJECTS = new Set(['art', 'pe', 'music', 'design', 'physical-education']);

const SUPPLEMENT_TREES = [
  { file: path.join(root, 'data/trees/cn/elementary/info-tech.json'), graph_path: 'cn/elementary/info-tech.json', stage: 'elementary' },
  { file: path.join(root, 'data/trees/cn/middle/info-tech.json'), graph_path: 'cn/middle/info-tech.json', stage: 'middle' },
  { file: path.join(engineBase, 'data/trees/cn/high/info-tech.json'), graph_path: 'cn/high/info-tech.json', stage: 'high' },
];

function gradeBand(grade) {
  const g = parseInt(String(grade), 10);
  if (g >= 1 && g <= 6) return 'primary';
  if (g >= 7 && g <= 9) return 'junior';
  if (g >= 10 && g <= 12) return 'senior';
  return 'unknown';
}

function isCNPath(gp) {
  const p = String(gp || '');
  return p.startsWith('cn/') || p.startsWith('cn-unified/')
    || p.includes('/elementary/') || p.includes('/middle/') || p.includes('/high/');
}

function isCNK12MetadataNode(node) {
  const gp = node.graph_path || node.path || node.treePath || '';
  if (!isCNPath(gp)) return false;
  const grade = node.grade ?? node.grades;
  if (grade == null) return false;
  const g = parseInt(String(grade).replace(/\D/g, ''), 10);
  if (g < 1 || g > 12) return false;
  const sub = node.subject || 'unknown';
  return !EXCLUDED_SUBJECTS.has(sub);
}

function slimNode(n, extra = {}) {
  return {
    id: n.id,
    name: n.name || n.label || n.display_name,
    subject: n.subject,
    grade: n.grade,
    gradeBand: n.gradeBand || gradeBand(n.grade),
    graph_path: n.graph_path || n.path || n.treePath,
    stage: n.stage,
    source: n.source || 'metadata',
    ...extra,
  };
}

function extractNodesFromTree(tree, graph_path, stage) {
  const subject = tree.subject || 'info-tech';
  const nodes = [];
  const push = (node, domain) => {
    nodes.push(slimNode({
      ...node,
      subject: node.subject || subject,
      graph_path,
      stage,
      source: 'supplement-tree',
    }, { domain: domain?.name || domain?.id || '' }));
  };
  (tree.domains || []).forEach((domain) => {
    (domain.nodes || []).forEach((node) => push(node, domain));
  });
  (tree.nodes || []).forEach((node) => push(node, null));
  return nodes;
}

function loadSupplementNodes() {
  const all = [];
  for (const spec of SUPPLEMENT_TREES) {
    if (!fs.existsSync(spec.file)) {
      console.warn('跳过缺失树文件:', spec.file);
      continue;
    }
    const tree = JSON.parse(fs.readFileSync(spec.file, 'utf8'));
    const nodes = extractNodesFromTree(tree, spec.graph_path, spec.stage);
    console.log(`补充 ${spec.stage} info-tech: ${nodes.length} 节点 ← ${path.basename(spec.file)}`);
    all.push(...nodes);
  }
  return all;
}

if (!fs.existsSync(metaPath)) {
  console.error(`找不到 ${metaPath}`);
  process.exit(1);
}

console.log('读取', metaPath);
const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
const arr = Array.isArray(meta.nodes) ? meta.nodes : Object.values(meta.nodes || meta);
const fromMeta = arr.filter(isCNK12MetadataNode).map((n) => slimNode({
  ...n,
  graph_path: n.graph_path || n.treePath,
  source: 'metadata',
}));

const supplement = loadSupplementNodes();
const byId = new Map();
fromMeta.forEach((n) => byId.set(String(n.id), n));
supplement.forEach((n) => {
  if (!byId.has(String(n.id))) byId.set(String(n.id), n);
});

const nodes = [...byId.values()].sort((a, b) => {
  if (a.grade !== b.grade) return (a.grade || 0) - (b.grade || 0);
  return String(a.subject).localeCompare(String(b.subject));
});

const bySubject = {};
const byBand = { primary: 0, junior: 0, senior: 0 };
nodes.forEach((n) => {
  bySubject[n.subject] = (bySubject[n.subject] || 0) + 1;
  if (byBand[n.gradeBand] != null) byBand[n.gradeBand] += 1;
});

const out = {
  version: '2.0.0',
  description: 'CN 小初高课标节点索引（含补充信息科技树；不含音体美）',
  generatedAt: new Date().toISOString(),
  source: metaPath,
  total: nodes.length,
  bySubject,
  byGradeBand: byBand,
  excludedSubjects: [...EXCLUDED_SUBJECTS],
  supplementTrees: SUPPLEMENT_TREES.map((t) => t.graph_path),
  nodes,
};

fs.writeFileSync(outPath, JSON.stringify(out, null, 2));
console.log(`写入 ${nodes.length} 节点 → ${outPath}`);
console.log('学段:', byBand);
console.log('学科:', bySubject);

const primaryNodes = nodes.filter((n) => n.gradeBand === 'primary');
fs.writeFileSync(legacyPrimaryPath, JSON.stringify({
  ...out,
  total: primaryNodes.length,
  nodes: primaryNodes,
  note: 'legacy alias; prefer cn-k12-nodes.json',
}, null, 2));
console.log(`同步小学子集 ${primaryNodes.length} 节点 → ${legacyPrimaryPath}`);
