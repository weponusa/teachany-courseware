#!/usr/bin/env node
/**
 * 为全部学期覆盖包子 PBL 生成拆解演示数据
 * 输出：
 *   data/decompose/index.json
 *   data/decompose/{project-id}.json  × N
 */
import { readFileSync, writeFileSync, readdirSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { buildDecomposeRecord, mergeImportedDemo } from './lib/decompose-demo-builder.mjs';

const __dir = dirname(fileURLToPath(import.meta.url));
const root = join(__dir, '..');
const plansDir = join(root, 'data/plans');
const outDir = join(root, 'data/decompose');

/** 子项目 id → 使用完整手工拆解的策划包 id */
const RICH_DEMO_MAP = {
  'g5-spring-p2': 'g5-community-map',
};

const planCache = new Map();
function loadPlan(planId) {
  if (planCache.has(planId)) return planCache.get(planId);
  try {
    const data = JSON.parse(readFileSync(join(plansDir, `${planId}.json`), 'utf8'));
    planCache.set(planId, data);
    return data;
  } catch {
    return null;
  }
}

function buildRecord(project, pack) {
  const richPlanId = RICH_DEMO_MAP[project.id];
  if (richPlanId) {
    const plan = loadPlan(richPlanId);
    if (plan?.decomposeDemo) {
      return mergeImportedDemo(plan, project, pack);
    }
  }
  return buildDecomposeRecord(project, pack);
}

const packFiles = readdirSync(plansDir).filter((f) => f.endsWith('-pack.json'));
const records = [];
const byGrade = {};

packFiles.forEach((file) => {
  const pack = JSON.parse(readFileSync(join(plansDir, file), 'utf8'));
  (pack.projects || []).forEach((project) => {
    const record = buildRecord(project, pack);
    records.push(record);
    if (!byGrade[pack.grade]) byGrade[pack.grade] = [];
    byGrade[pack.grade].push({
      id: record.id,
      packId: record.packId,
      title: record.title,
      themeChain: record.themeChain,
      drivingQuestion: record.drivingQuestion,
      weeks: record.weeks,
      stats: record.stats,
      planRef: record.planRef,
      richDemo: !!RICH_DEMO_MAP[project.id],
      demoUrl: `demo.html?project=${record.id}`,
      packUrl: `pack.html?id=${record.packId}`,
    });
  });
});

records.sort((a, b) => {
  if (a.grade !== b.grade) return a.grade - b.grade;
  if (a.semester !== b.semester) return a.semester === 'autumn' ? -1 : 1;
  return a.id.localeCompare(b.id);
});

mkdirSync(outDir, { recursive: true });
records.forEach((rec) => {
  writeFileSync(join(outDir, `${rec.id}.json`), JSON.stringify(rec, null, 2), 'utf8');
});

const index = {
  version: '1.0.0',
  model: 'pbl-decompose-index',
  title: 'K12 子 PBL 拆解索引',
  generatedAt: new Date().toISOString(),
  summary: {
    totalProjects: records.length,
    semesterPacks: packFiles.length,
    richDemos: Object.keys(RICH_DEMO_MAP).length,
    byGradeBand: {
      primary: records.filter((r) => r.gradeBand === 'primary').length,
      junior: records.filter((r) => r.gradeBand === 'junior').length,
      senior: records.filter((r) => r.gradeBand === 'senior').length,
    },
  },
  projects: records.map((r) => ({
    id: r.id,
    packId: r.packId,
    grade: r.grade,
    gradeBand: r.gradeBand,
    semester: r.semester,
    title: r.title,
    themeChain: r.themeChain,
    drivingQuestion: r.drivingQuestion,
    weeks: r.weeks,
    stats: r.stats,
    planRef: r.planRef,
    richDemo: !!RICH_DEMO_MAP[r.id],
    demoUrl: `demo.html?project=${r.id}`,
  })),
  byGrade,
};

writeFileSync(join(outDir, 'index.json'), JSON.stringify(index, null, 2), 'utf8');

console.log('Wrote', records.length, 'decompose demos to data/decompose/');
console.log('Rich demos:', Object.keys(RICH_DEMO_MAP).join(', '));
