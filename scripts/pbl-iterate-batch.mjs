#!/usr/bin/env node
/**
 * 并行生成多组 PBL 项目 → 跑管线 → 打分 → 输出满意样本
 * 用法: node scripts/pbl-iterate-batch.mjs [--rounds=2] [--concurrency=3] [--only=key1,key2]
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, '..');
const OUT_DIR = path.join(ROOT, 'data', 'pbl-iterate');
const REPORT_FILE = path.join(OUT_DIR, 'latest-report.json');

const ROUNDS = parseInt((process.argv.find(a => a.startsWith('--rounds=')) || '').slice(9), 10) || 1;
const CONCURRENCY = parseInt((process.argv.find(a => a.startsWith('--concurrency=')) || '').slice(14), 10) || 3;
const ONLY = (process.argv.find(a => a.startsWith('--only=')) || '').slice(7).split(',').filter(Boolean);

const CASES = [
  {
    key: 'primary-bazaar',
    label: '四年级·班级义卖记账',
    goal: '设计班级义卖活动记账表，记录每件商品的收入与找零，统计总收入并制作简单图表',
    projectSpec: { gradeLevel: 'primary', gradeDetail: '4', subject: 'math', task: '义卖记账', deliverable: 'report' },
  },
  {
    key: 'primary-plant',
    label: '三年级·植物生长记录',
    goal: '观察教室盆栽一周生长情况，每天测量高度并记录，分析哪几天长得最快',
    projectSpec: { gradeLevel: 'primary', gradeDetail: '3', subject: 'science', task: '植物观察', deliverable: 'report' },
  },
  {
    key: 'primary-recycle',
    label: '五年级·垃圾分类调查',
    goal: '调查校园三个区域的垃圾分类执行情况，统计正确率并设计宣传海报',
    projectSpec: { gradeLevel: 'primary', gradeDetail: '5', subject: 'cross', task: '垃圾分类调查', deliverable: 'poster' },
  },
  {
    key: 'primary-shopping',
    label: '二年级·小卖部购物',
    goal: '模拟小卖部购物场景，用人民币学具完成付款和找零，制作购物小票',
    projectSpec: { gradeLevel: 'primary', gradeDetail: '2', subject: 'math', task: '购物找零', deliverable: 'artifact' },
  },
  {
    key: 'primary-water',
    label: '六年级·饮水调查统计',
    goal: '调查同学每日饮水量，汇总数据计算平均数，提出健康饮水建议',
    projectSpec: { gradeLevel: 'primary', gradeDetail: '6', subject: 'math', task: '饮水调查', deliverable: 'report' },
  },
  {
    key: 'junior-bridge',
    label: '初二·桥梁承重对比',
    goal: '用不同材料制作桥梁模型，测试承重并分析哪种结构更稳固',
    projectSpec: { gradeLevel: 'junior', gradeDetail: '8', subject: 'physics', task: '桥梁模型', deliverable: 'artifact' },
  },
];

function findJsonFiles(dir) {
  const out = [];
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) out.push(...findJsonFiles(p));
    else if (ent.name.endsWith('.json')) out.push(p);
  }
  return out;
}

function formatGradeLabel(grade, system) {
  if (!grade) return '';
  if (system === 'cn') {
    if (grade <= 6) return `小学${grade}年级`;
    if (grade <= 9) return `初中${grade - 6}年级`;
    if (grade <= 12) return `高中${grade - 9}年级`;
  }
  return `G${grade}`;
}

function loadAllNodes() {
  const treesDir = path.join(ROOT, 'data', 'trees');
  const systems = {
    cn: { label: '中国课标', tag: 'CN' },
    ap: { label: 'AP', tag: 'AP' },
    cambridge: { label: 'Cambridge', tag: 'CA' },
    ib: { label: 'IB', tag: 'IB' },
    us: { label: 'US CCSS', tag: 'US' },
  };
  const all = [];
  for (const [sysId, sysInfo] of Object.entries(systems)) {
    const sysDir = path.join(treesDir, sysId);
    if (!fs.existsSync(sysDir)) continue;
    for (const jsonFile of findJsonFiles(sysDir)) {
      try {
        const data = JSON.parse(fs.readFileSync(jsonFile, 'utf8'));
        (data.domains || []).forEach(domain => {
          (domain.nodes || []).forEach(node => {
            const grade = parseInt(node.grade, 10) || 0;
            all.push({
              ...node,
              id: node.id,
              name: node.name || node.name_zh || '',
              subject: node.subject || data.subject || '',
              domain: domain.name || node.domain || '',
              grade,
              system: sysId,
              systemTag: sysInfo.tag,
              gradeLabel: formatGradeLabel(grade, sysId),
              isExternal: false,
            });
          });
        });
      } catch (_e) { /* skip */ }
    }
  }
  return all;
}

function setupFetch() {
  const nativeFetch = globalThis.fetch?.bind(globalThis);
  if (!nativeFetch) throw new Error('需要 Node 18+ 自带 fetch');
  global.fetch = async (url, opts = {}) => {
    const u = String(url);
    if (u.includes('/api/pbl/analyze')) {
      return nativeFetch('https://www.teachany.cn/api/pbl/analyze', opts);
    }
    let filePath = u.replace(/\?.*$/, '');
    if (filePath.startsWith('./')) filePath = path.join(ROOT, filePath.slice(2));
    if (filePath.startsWith('/')) filePath = path.join(ROOT, filePath.slice(1));
    if (!fs.existsSync(filePath)) {
      return { ok: false, status: 404, json: async () => ({}) };
    }
    const body = fs.readFileSync(filePath, 'utf8');
    return {
      ok: true,
      status: 200,
      json: async () => JSON.parse(body),
      text: async () => body,
    };
  };
}

async function bootstrapBuilder(allNodes) {
  global.window = global;
  global.localStorage = { getItem: () => null, setItem: () => {} };
  global.performance = { now: () => Date.now(), markResourceTiming: () => {}, measureResourceTiming: () => {} };
  global.location = { origin: 'https://www.teachany.cn', protocol: 'https:' };
  global.document = { write: () => {}, createElement: () => ({ textContent: '', innerHTML: '' }) };
  global.TeachAnyHub = { init: async () => {} };
  setupFetch();

  let code = fs.readFileSync(path.join(ROOT, 'assets/scripts/pbl-path.js'), 'utf8');
  code = code.replace('window.PBLPathBuilder = new PBLPathBuilder();', 'global.__PBLPathBuilderClass = PBLPathBuilder;');
  // eslint-disable-next-line no-eval
  eval(code);

  const builder = new global.__PBLPathBuilderClass();
  for (const n of allNodes) {
    builder.unifiedIndex.set(n.id, n);
    if (!builder.systemIndex.has(n.system)) builder.systemIndex.set(n.system, new Set());
    builder.systemIndex.get(n.system).add(n.id);
  }
  builder.loaded = true;
  await builder._loadKnowledgeGraph();
  await builder._ensureArchetypeData();
  return builder;
}

function curriculumNodes(result) {
  return (result.graphData?.nodes || result.matched || []).filter(
    n => n && !n.isExternal && n.layer !== 'external' && !String(n.id || '').startsWith('ext-')
  );
}

function evaluateResult(result, testCase) {
  const nodes = curriculumNodes(result);
  const issues = [];
  const spec = testCase.projectSpec || {};
  const isPrimary = spec.gradeLevel === 'primary';
  const maxGrade = isPrimary ? 6 : spec.gradeLevel === 'junior' ? 9 : 12;
  const minGrade = isPrimary ? 1 : spec.gradeLevel === 'junior' ? 7 : 1;

  const university = nodes.filter(n => n.isUniversity || (n.system === 'cn' && (parseInt(n.grade, 10) || 0) === 0));
  const overAge = nodes.filter(n => {
    const g = parseInt(n.grade, 10) || 0;
    return n.system === 'cn' && g > 0 && (g < minGrade || g > maxGrade);
  });
  const foreign = isPrimary ? nodes.filter(n => n.system !== 'cn') : [];

  if (nodes.length < 5) issues.push(`课内仅 ${nodes.length} 个（需≥5）`);
  if (university.length) issues.push(`含 ${university.length} 个大学节点: ${university.map(n => n.name).join('、')}`);
  if (overAge.length) issues.push(`含 ${overAge.length} 个超龄节点: ${overAge.map(n => `${n.name}(G${n.grade})`).join('、')}`);
  if (foreign.length) issues.push(`小学项目含 ${foreign.length} 个国际课标节点`);

  let score = 100;
  score -= Math.max(0, 5 - nodes.length) * 12;
  score -= university.length * 20;
  score -= overAge.length * 15;
  score -= foreign.length * 10;
  if (result.fallback) score -= 30;

  const satisfied = issues.length === 0 && nodes.length >= 5;
  return {
    score,
    satisfied,
    issues,
    curriculumCount: nodes.length,
    names: nodes.map(n => `${n.name}(${n.gradeLabel || 'G' + n.grade})`),
    universityCount: university.length,
    overAgeCount: overAge.length,
  };
}

function slimResult(result, testCase, evalResult) {
  return {
    key: testCase.key,
    label: testCase.label,
    goal: result.goal || testCase.goal,
    projectSpec: testCase.projectSpec,
    evaluation: evalResult,
    matched: curriculumNodes(result).map(n => ({
      id: n.id,
      name: n.name,
      subject: n.subject,
      grade: n.grade,
      gradeLabel: n.gradeLabel,
      pblRole: n.pblRole,
      matchReason: n.matchReason,
    })),
    stats: result.stats,
    knowledgeChain: result.knowledgeChain || result.pathPlan?.knowledgeChain || '',
    phases: (result.pathPlan?.phases || result.projectPhases || []).length,
    generatedAt: new Date().toISOString(),
  };
}

async function runCase(builder, testCase, round, attempt = 1) {
  const t0 = Date.now();
  try {
    let result = await builder.analyzePBLGoal(testCase.goal, ['all'], null, {
      projectSpec: testCase.projectSpec,
    });
    if (!result.pathPlan && typeof builder.buildPathPlanFromResult === 'function') {
      result.pathPlan = builder.buildPathPlanFromResult(result);
    }
    const evaluation = evaluateResult(result, testCase);
    const elapsed = ((Date.now() - t0) / 1000).toFixed(1);
    return {
      ok: true,
      round,
      elapsed,
      slim: slimResult(result, testCase, evaluation),
      evaluation,
    };
  } catch (e) {
    const retriable = /aborted|timeout|520|502|503|429/i.test(e.message) && attempt < 2;
    if (retriable) {
      console.log(`         retry ${testCase.key} (${e.message})`);
      await new Promise(r => setTimeout(r, 3000));
      return runCase(builder, testCase, round, attempt + 1);
    }
    return {
      ok: false,
      round,
      error: e.message,
      evaluation: { score: 0, satisfied: false, issues: [e.message], curriculumCount: 0, names: [] },
    };
  }
}

async function runPool(builder, cases, round) {
  const results = [];
  let idx = 0;
  async function worker() {
    while (idx < cases.length) {
      const i = idx++;
      const c = cases[i];
      console.log(`  [R${round}] start ${c.key} (${c.label})`);
      const r = await runCase(builder, c, round);
      results.push({ case: c, ...r });
      const mark = r.evaluation?.satisfied ? '✅' : '⚠️';
      console.log(`  [R${round}] ${mark} ${c.key} score=${r.evaluation?.score ?? 0} nodes=${r.evaluation?.curriculumCount ?? 0} ${r.elapsed || '?'}s`);
      if (r.evaluation?.issues?.length) console.log(`         ${r.evaluation.issues.join('; ')}`);
    }
  }
  await Promise.all(Array.from({ length: Math.min(CONCURRENCY, cases.length) }, () => worker()));
  return results;
}

async function main() {
  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  const todo = ONLY.length ? CASES.filter(c => ONLY.includes(c.key)) : CASES;
  console.log(`Loading index... (${todo.length} cases, concurrency=${CONCURRENCY}, rounds=${ROUNDS})`);
  const allNodes = loadAllNodes();
  const builder = await bootstrapBuilder(allNodes);
  console.log(`Loaded ${allNodes.length} nodes\n`);

  const allRuns = [];
  for (let r = 1; r <= ROUNDS; r++) {
    console.log(`=== Round ${r}/${ROUNDS} ===`);
    const runs = await runPool(builder, todo, r);
    allRuns.push(...runs);
    for (const run of runs) {
      if (run.ok && run.slim) {
        const out = path.join(OUT_DIR, `${run.case.key}-r${r}.json`);
        fs.writeFileSync(out, JSON.stringify(run.slim, null, 2), 'utf8');
      }
    }
  }

  const ranked = allRuns
    .filter(r => r.ok)
    .sort((a, b) => (b.evaluation?.score || 0) - (a.evaluation?.score || 0));

  const satisfied = ranked.filter(r => r.evaluation?.satisfied);
  const picks = (satisfied.length >= 3 ? satisfied : ranked).slice(0, 5);

  const report = {
    generatedAt: new Date().toISOString(),
    rounds: ROUNDS,
    concurrency: CONCURRENCY,
    total: allRuns.length,
    satisfiedCount: satisfied.length,
    picks: picks.map(r => ({
      key: r.case.key,
      label: r.case.label,
      round: r.round,
      score: r.evaluation.score,
      curriculumCount: r.evaluation.curriculumCount,
      names: r.evaluation.names,
      issues: r.evaluation.issues,
    })),
    all: ranked.map(r => ({
      key: r.case.key,
      round: r.round,
      score: r.evaluation?.score,
      satisfied: r.evaluation?.satisfied,
      curriculumCount: r.evaluation?.curriculumCount,
      issues: r.evaluation?.issues,
    })),
  };

  fs.writeFileSync(REPORT_FILE, JSON.stringify(report, null, 2), 'utf8');

  console.log('\n========== 满意样本 TOP ==========');
  picks.forEach((r, i) => {
    console.log(`${i + 1}. [${r.evaluation.score}分] ${r.case.label} (R${r.round})`);
    console.log(`   课内 ${r.evaluation.curriculumCount}：${r.evaluation.names.join('、')}`);
  });
  console.log(`\n报告: ${REPORT_FILE}`);
}

main().catch(e => { console.error(e); process.exit(1); });
