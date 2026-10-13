#!/usr/bin/env node
/**
 * 从 TeachAny nodes-metadata 提取 CN 小学节点索引（轻量 JSON）
 * 用法: node scripts/build-primary-index.mjs [--engine ../engine]
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
const outPath = path.join(root, 'data', 'primary-cn-nodes.json');

function isPrimaryCNNode(node) {
  const gp = String(node.graph_path || node.path || node.treePath || '');
  const isCN = gp.startsWith('cn/') || gp.startsWith('cn-unified/') || gp.includes('/elementary/');
  if (!isCN) return false;
  const grade = node.grade ?? node.grades;
  if (grade == null) return false;
  const g = parseInt(String(grade).replace(/\D/g, ''), 10);
  return g >= 1 && g <= 6;
}

function slimNode(n) {
  return {
    id: n.id,
    name: n.name || n.label,
    subject: n.subject,
    grade: n.grade,
    gradeBand: n.gradeBand || n.gradeLevel,
    path: n.path || n.treePath,
  };
}

if (!fs.existsSync(metaPath)) {
  console.error(`找不到 ${metaPath}`);
  console.error('请确保 engine symlink 指向 teachany-courseware');
  process.exit(1);
}

console.log('读取', metaPath);
const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
const arr = Array.isArray(meta.nodes) ? meta.nodes : Object.values(meta.nodes || meta);
const primary = arr.filter(isPrimaryCNNode).map(slimNode);

const bySubject = {};
primary.forEach((n) => {
  const s = n.subject || 'unknown';
  bySubject[s] = (bySubject[s] || 0) + 1;
});

const out = {
  version: '1.0.0',
  generatedAt: new Date().toISOString(),
  source: metaPath,
  total: primary.length,
  bySubject,
  nodes: primary,
};

fs.writeFileSync(outPath, JSON.stringify(out, null, 2));
console.log(`写入 ${primary.length} 个节点 → ${outPath}`);
console.log('学科分布:', bySubject);
