#!/usr/bin/env node
/**
 * 用当前 PBLPathBuilder + teachany.cn /api/pbl/analyze 重新生成示范项目 JSON
 * 用法: node scripts/regenerate-pbl-demos.mjs [--force]
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, '..');
const OUT_DIR = path.join(ROOT, 'data', 'pbl-demos');
const FORCE = process.argv.includes('--force');
const ONLY = (process.argv.find(a => a.startsWith('--only=')) || '').slice(7).split(',').filter(Boolean);

const DEMOS = [
  { key: 'smart-home-temp', goal: '设计一个智能家居温度控制系统，利用传感器实时监测室温，自动调节空调或暖气，实现节能恒温' },
  { key: 'weather-app', goal: '制作一个天气预报App，从公开API获取气象数据，展示温度、湿度、风速，并用图表展示7天趋势' },
  { key: 'traffic-analysis', goal: '分析城市交通拥堵问题，收集高峰期车流量数据，建立拥堵模型，提出优化方案' },
  { key: 'auto-watering', goal: '设计一个自动浇花系统，通过土壤湿度传感器判断是否需要浇水，用微型水泵自动灌溉' },
  { key: 'word-memory', goal: '制作一个英文单词记忆游戏，利用间隔重复算法安排复习，追踪用户记忆曲线' },
  { key: 'water-quality', goal: '分析本地河流水质，采集pH值、溶解氧、浊度数据，评估污染程度并提出治理建议' },
  { key: 'encryption-tool', goal: '设计一个简易加密通信工具，实现凯撒密码和RSA加密，理解对称加密与非对称加密的原理' },
  { key: 'solar-system', goal: '构建一个太阳系模拟器，用物理引擎模拟行星轨道运动，展示开普勒定律和万有引力' }
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
    us: { label: 'US CCSS', tag: 'US' }
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
              name_en: node.name_en || '',
              subject: node.subject || data.subject || '',
              domain: domain.name || node.domain || '',
              grade,
              definition: node.definition || node.description || '',
              key_concepts: node.key_concepts || [],
              prerequisites: node.prerequisites || [],
              extends: node.extends || [],
              parallel: node.parallel || [],
              curriculum_points: node.curriculum_points || [],
              system: sysId,
              systemTag: sysInfo.tag,
              systemLabel: sysInfo.label,
              gradeLabel: formatGradeLabel(grade, sysId),
              treePath: path.relative(treesDir, jsonFile),
              isExternal: false
            });
          });
        });
      } catch (e) {
        console.warn('skip', jsonFile, e.message);
      }
    }
  }
  return all;
}

function slimNode(n) {
  return {
    id: n.id,
    name: n.name,
    name_en: n.name_en,
    subject: n.subject,
    domain: n.domain,
    domainColor: n.domainColor,
    grade: n.grade,
    gradeLabel: n.gradeLabel,
    status: n.status,
    courses: n.courses,
    prerequisites: n.prerequisites,
    extends: n.extends,
    parallel: n.parallel,
    system: n.system,
    systemTag: n.systemTag,
    systemLabel: n.systemLabel,
    definition: n.definition,
    layer: n.layer,
    pathStep: n.pathStep,
    pblRole: n.pblRole,
    confidence: n.confidence,
    matchReason: n.matchReason,
    isExternal: n.isExternal
  };
}

function slimResult(result) {
  const pathPlan = result.pathPlan || null;
  return {
    goal: result.goal,
    systems: result.systems,
    matched: (result.matched || []).map(slimNode),
    external: (result.external || []).map(slimNode),
    techRoute: result.techRoute,
    knowledgeChain: result.knowledgeChain || pathPlan?.knowledgeChain || '',
    projectPhases: pathPlan?.phases || result.projectPhases || [],
    pathPlan,
    graphData: {
      nodes: (result.graphData?.nodes || []).map(slimNode),
      links: result.graphData?.links || []
    },
    stats: result.stats,
    complexProject: result.complexProject,
    generatedAt: new Date().toISOString(),
    generator: 'regenerate-pbl-demos.mjs'
  };
}

async function bootstrapBuilder(allNodes) {
  global.window = global;
  global.localStorage = { getItem: () => null, setItem: () => {} };
  global.performance = {
    now: () => Date.now(),
    markResourceTiming: () => {},
    measureResourceTiming: () => {}
  };
  global.location = { origin: 'https://www.teachany.cn', protocol: 'https:' };
  global.document = {
    write: () => {},
    createElement: () => ({ textContent: '', innerHTML: '' })
  };
  global.TeachAnyHub = { init: async () => {} };

  let code = fs.readFileSync(path.join(ROOT, 'assets/scripts/pbl-path.js'), 'utf8');
  code = code.replace('window.PBLPathBuilder = new PBLPathBuilder();', 'global.__PBLPathBuilderClass = PBLPathBuilder;');
  // eslint-disable-next-line no-eval
  eval(code);

  const Builder = global.__PBLPathBuilderClass;
  const builder = new Builder();
  for (const n of allNodes) {
    builder.unifiedIndex.set(n.id, n);
    if (!builder.systemIndex.has(n.system)) builder.systemIndex.set(n.system, new Set());
    builder.systemIndex.get(n.system).add(n.id);
  }
  builder.loaded = true;
  return builder;
}

async function main() {
  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  console.log('Loading knowledge index...');
  const allNodes = loadAllNodes();
  console.log(`Loaded ${allNodes.length} nodes`);

  const builder = await bootstrapBuilder(allNodes);

  const todo = ONLY.length ? DEMOS.filter(d => ONLY.includes(d.key)) : DEMOS;

  for (let i = 0; i < todo.length; i++) {
    const demo = todo[i];
    const outFile = path.join(OUT_DIR, `${demo.key}.json`);
    if (!FORCE && fs.existsSync(outFile)) {
      try {
        const prev = JSON.parse(fs.readFileSync(outFile, 'utf8'));
        if (prev.generator === 'regenerate-pbl-demos.mjs') {
          console.log(`[${i + 1}/${todo.length}] skip ${demo.key} (already regenerated)`);
          continue;
        }
      } catch (_e) { /* regenerate */ }
    }
    console.log(`\n[${i + 1}/${todo.length}] ${demo.key}`);
    try {
      let result;
      try {
        result = await builder.analyzePBLGoal(demo.goal, ['all']);
      } catch (e) {
        console.warn(`  ⚠️ LLM 失败 (${e.message})，降级关键词匹配...`);
        result = await builder.searchByKeywords(demo.goal, ['all']);
        result.fallback = true;
      }
      if (!result.pathPlan && typeof builder.buildPathPlanFromResult === 'function') {
        result.pathPlan = builder.buildPathPlanFromResult(result);
        result.projectPhases = result.pathPlan?.phases || result.projectPhases;
        result.knowledgeChain = result.pathPlan?.knowledgeChain || result.knowledgeChain;
        result.techRoute = builder._buildTechRouteFromPathPlan?.(result.pathPlan) || result.techRoute;
      }
      const slim = slimResult(result);
      fs.writeFileSync(outFile, JSON.stringify(slim, null, 2), 'utf8');
      console.log(`  ✅ graph=${slim.stats.graphNodes} matched=${slim.stats.matchedCount} phases=${(slim.projectPhases || []).length}${result.fallback ? ' (fallback)' : ''}`);
    } catch (e) {
      console.error(`  ❌ ${e.message}`);
    }
    if (i < todo.length - 1) await new Promise(r => setTimeout(r, 2500));
  }
  console.log('\nDone.');
}

main().catch(e => { console.error(e); process.exit(1); });
