#!/usr/bin/env node
/**
 * 全量质检 community/ 下所有课件，输出 JSON 汇总报告
 * 用法: node scripts/qc-all.cjs [shardIndex] [shardCount]
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const COMMUNITY = path.join(__dirname, '..', 'community');
const VALIDATOR = path.join(__dirname, 'validate-courseware.cjs');
const shardIndex = parseInt(process.argv[2] || '0', 10);
const shardCount = parseInt(process.argv[3] || '1', 10);

const dirs = fs.readdirSync(COMMUNITY).filter(name => {
  const full = path.join(COMMUNITY, name);
  if (!fs.statSync(full).isDirectory()) return false;
  if (name === 'archive' || name.startsWith('_') || name.startsWith('.')) return false;
  return fs.existsSync(path.join(full, 'index.html'));
}).sort();

const stripAnsi = (s) => s.replace(/\x1b\[[0-9;]*m/g, '');
const mine = dirs.filter((_, i) => i % shardCount === shardIndex);
const results = [];
for (const name of mine) {
  const dirPath = path.join(COMMUNITY, name);
  let rec = { id: name, passed: 0, total: 22, failed: [] };
  try {
    const out = execSync(`node "${VALIDATOR}" "${dirPath}"`, { encoding: 'utf8', timeout: 60000, stdio: ['pipe', 'pipe', 'pipe'] });
    const m = out.match(/总评：(\d+)\/(\d+)/);
    if (m) { rec.passed = parseInt(m[1]); rec.total = parseInt(m[2]); }
    const fm = [...out.matchAll(/❌ #(\d+)\s+(.+?) —/g)];
    rec.failed = fm.map(x => `#${x[1]} ${x[2]}`);
  } catch (e) {
    const out = stripAnsi((e.stdout || '').toString());
    const m = out.match(/总评：(\d+)\/(\d+)/);
    if (m) { rec.passed = parseInt(m[1]); rec.total = parseInt(m[2]); }
    const fm = [...out.matchAll(/❌ #(\d+)\s+(.+?) —/g)];
    rec.failed = fm.map(x => `#${x[1]} ${x[2]}`);
    if (!m) rec.failed = ['FATAL: ' + (e.message || '').slice(0, 120)];
  }
  results.push(rec);
  console.error(`${rec.passed}/${rec.total} ${name}${rec.failed.length ? '  ✗ ' + rec.failed.join(' | ') : ''}`);
}
fs.writeFileSync(process.argv[4] || `qc-shard-${shardIndex}.json`, JSON.stringify(results, null, 2));
console.log(`done shard ${shardIndex}: ${results.length} items`);
