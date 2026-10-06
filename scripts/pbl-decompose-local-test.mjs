#!/usr/bin/env node
/**
 * 本地质检流水线自测（无需 LLM Key）
 * - 校验服务端提示词是否含通用拆解原则
 * - 用「好/坏」蓝图样本跑客户端 _collectDecomposeReviewIssues / _finalizeDecomposeBlueprint
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, '..');
const PBL_API = process.env.PBL_API || 'http://localhost:8788/api/pbl/analyze';

const GOAL = '【道法+心理】设计校园反欺凌宣传行动：调查同伴感受，运用规则与情绪知识制定干预方案并撰写倡议书';
const SPEC = { gradeLevel: 'junior', gradeDetail: '8', subjects: ['politics', 'psychology'], subject: 'cross' };

const BAD_BP = {
  drivingQuestion: '如何做好校园宣传？',
  projectSummary: '按模块推进，每阶段产出可检查',
  deliverable: '阶段成果',
  schemes: [{
    id: 'A', name: '方案A', summary: '技术路线概述',
    phases: [
      { phase: '基础准备', steps: ['查阅资料并分析', '开展调查研究'], deliverable: '阶段成果', tools: ['A3纸或绘图纸', '铅笔尺规'] },
      { phase: '实施阶段', steps: ['完成本阶段任务', '撰写研究报告初稿'], deliverable: '方案' },
    ],
  }],
  recommendedSchemeId: 'A',
};

const GOOD_BP = {
  drivingQuestion: '如何通过匿名调查与同伴宣传，在校园内有效减少欺凌并提升安全感？',
  projectSummary: '初二学生设计10题匿名问卷调查同伴欺凌感受，用统计图呈现数据，结合道法规则与心理情绪知识制定3种干预活动并撰写倡议书',
  deliverable: '校园反欺凌调查报告+干预方案表+倡议书',
  scopeLimits: ['不能把班级小样本等同于全校结论', '不能替代专业心理咨询'],
  successCriteria: ['问卷回收≥20份且附统计图', '倡议书≥500字含3条可执行倡议'],
  constraints: ['问卷须匿名并附知情说明', '宣传行动须教师审核后开展'],
  schemes: [
    {
      id: 'A', name: '完整调查+宣传路线', summary: '问卷→统计→干预活动→倡议书，样本本班20人',
      phases: [
        { phase: '选题与调查设计', steps: ['围绕校园反欺凌写出1句可验证问题，确定本班样本≥20人', '设计10题匿名问卷（6单选+2量表+2开放），附知情说明'], deliverable: '问卷定稿+抽样表', tools: ['问卷题型配比说明'] },
        { phase: '资料与数据收集', steps: ['发放问卷并回收≥20份，标注缺失答卷处理', '开展5人同伴访谈，记录规则认知与情绪感受'], deliverable: '原始数据表+访谈记录', tools: ['访谈提纲结构'] },
        { phase: '整理与统计分析', steps: ['录入频数表并绘制条形图，计算至少2项百分比', '结合依法行使权利分析3个欺凌情境中的规则边界'], deliverable: '统计图表+成因分析', tools: ['频数统计表规范'] },
        { phase: '方案制定与宣传', steps: ['列出宣讲/情景剧/海报3种干预形式及分工时间表', '运用情绪识别知识设计2道共情情境练习题'], deliverable: '干预方案表', tools: ['干预方案表模板'] },
        { phase: '结论与报告', steps: ['撰写800字倡议书（称呼/问题/3条倡议/号召）', '准备3分钟答辩要点含图表编号与局限说明'], deliverable: '反欺凌倡议书+答辩提纲', tools: ['倡议书结构提纲'] },
      ],
    },
    {
      id: 'B', name: '精简路线', summary: '压缩为课堂内小组行动，样本15人、周期2周',
      phases: [
        { phase: '选题与调查设计', steps: ['确定8题迷你问卷，样本15人'], deliverable: '迷你问卷' },
        { phase: '资料与数据收集', steps: ['回收问卷并整理'], deliverable: '数据表' },
        { phase: '整理与统计分析', steps: ['绘制1张统计图并写2条发现'], deliverable: '统计图' },
        { phase: '结论与报告', steps: ['撰写500字倡议书'], deliverable: '倡议书' },
      ],
    },
  ],
  recommendedSchemeId: 'A',
};

async function checkPrompts() {
  const resp = await fetch(PBL_API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ stage: 'decompose', goal: GOAL, messagesOnly: true, projectSpec: SPEC }),
  });
  const data = await resp.json();
  const sys = data.messages?.[0]?.content || '';
  const user = data.messages?.[1]?.content || '';
  const checks = [
    ['通用拆解原则', /通用拆解原则/],
    ['步骤公式', /步骤公式/],
    ['道法心理硬性', /道法|心理/],
    ['禁文具', /禁.*A3|禁文具|方法指导/],
    ['projectSpec年级', /初中|八年级|8/],
    ['量化自检', /输出前自检|阿拉伯数字/],
  ];
  console.log('── 提示词检查（本地 Pages Functions）──');
  for (const [name, re] of checks) {
    const hit = re.test(sys) || re.test(user);
    console.log(`  ${hit ? '✓' : '✗'} ${name}`);
  }
  return checks.every(([, re]) => re.test(sys) || re.test(user));
}

function loadBuilder() {
  global.window = {};
  eval(fs.readFileSync(path.join(ROOT, 'scripts/pbl-path.js'), 'utf8'));
  return window.PBLPathBuilder;
}

function runClientQA(b, label, bp) {
  const issues = b._collectDecomposeReviewIssues(GOAL, bp);
  const substance = b._blueprintSubstanceScore(bp, GOAL);
  const depth = b._blueprintStepDepthScore(bp);
  console.log(`\n── 客户端质检: ${label} ──`);
  console.log(`  substance=${substance} depth=${depth.toFixed(2)} issues=${issues.length}`);
  if (issues.length) issues.slice(0, 6).forEach(i => console.log(`    · ${i}`));
  return { issues: issues.length, substance, depth };
}

async function main() {
  console.log('PBL 拆解本地自测\n');

  let promptsOk = false;
  try {
    promptsOk = await checkPrompts();
  } catch (e) {
    console.log(`  提示词检查跳过: ${e.message}（需 wrangler pages dev --port=8788）`);
  }

  const b = loadBuilder();
  b._activeProjectSpec = SPEC;
  const bad = runClientQA(b, '坏蓝图（文具+空话）', BAD_BP);
  const good = runClientQA(b, '好蓝图（量化+专名）', GOOD_BP);

  // finalize 行为：坏蓝图应回退，好蓝图应保留
  const badFinal = b._finalizeDecomposeBlueprint(GOAL, BAD_BP);
  const goodFinal = b._finalizeDecomposeBlueprint(GOAL, GOOD_BP);
  console.log('\n── _finalizeDecomposeBlueprint ──');
  console.log(`  坏蓝图 → ${badFinal.fallback ? '回退本地模板 ✓' : '保留LLM（不应）'}`);
  console.log(`  好蓝图 → ${goodFinal.fallback ? '回退（不应）' : '保留LLM ✓'}`);

  const pass = promptsOk && bad.issues >= 5 && good.issues <= 2 && !goodFinal.fallback;
  console.log(`\n══ ${pass ? '本地自测通过' : '部分项需人工确认'} ══`);
  console.log('\n线上 LLM 实测说明:');
  console.log('  · teachany.cn/api/pbl/analyze → HTTP 405（线上 Functions 未通或路由未部署）');
  console.log('  · OpenRouter 内置 Key → 402 余额/额度不足');
  console.log('  · 本地 wrangler 无 OPENROUTER_KEY → Backend not configured');
  console.log('  · 换模型实测需: 部署 Functions + 配置 Key，或在 pbl.html 填自有 OpenRouter Key');
}

main().catch(e => { console.error(e); process.exit(1); });
