#!/usr/bin/env node
/**
 * 本地对比 PBL decompose：DeepSeek V4 Flash vs GLM-4-Flash
 * 用法：OPENROUTER_KEY=sk-or-... PARATERA_KEY=sk-... node scripts/test-pbl-model.mjs
 */
import { buildPBMessages } from '../functions/_lib/pbl-prompts.js';

const GOAL = process.argv[2] || '食堂的汤盐含量测定';

const chains = [
  { label: 'DeepSeek V4 Flash', backendId: 'openrouter', model: 'deepseek/deepseek-v4-flash', key: process.env.OPENROUTER_KEY },
  { label: 'GLM-4-Flash', backendId: 'paratera', model: 'GLM-4-Flash', key: process.env.PARATERA_KEY },
];

const backends = {
  openrouter: { baseUrl: 'https://openrouter.ai/api/v1', extraHeaders: { 'HTTP-Referer': 'https://www.teachany.cn', 'X-Title': 'TeachAny-PBL-Test' } },
  paratera: { baseUrl: 'https://llmapi.paratera.com/v1', extraHeaders: {} },
};

async function callModel(chain, messages) {
  if (!chain.key) return { error: 'missing API key' };
  const backend = backends[chain.backendId];
  const t0 = Date.now();
  const resp = await fetch(`${backend.baseUrl}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${chain.key}`,
      ...backend.extraHeaders,
    },
    body: JSON.stringify({
      model: chain.model,
      messages,
      stream: false,
      temperature: 0.35,
      max_tokens: 4500,
    }),
  });
  const text = await resp.text();
  const ms = Date.now() - t0;
  if (!resp.ok) return { error: `${resp.status} ${text.slice(0, 300)}`, ms };
  const data = JSON.parse(text);
  const content = data.choices?.[0]?.message?.content || '';
  const hasTitration = /滴定|硝酸银|AgNO/.test(content);
  const hasConductivity = /电导率/.test(content);
  const hasSchemes = /"schemes"/.test(content);
  return { content, ms, hasTitration, hasConductivity, hasSchemes };
}

const messages = buildPBMessages('decompose', { goal: GOAL, complex: false });

for (const chain of chains) {
  console.log(`\n=== ${chain.label} (${chain.model}) ===`);
  try {
    const r = await callModel(chain, messages);
    if (r.error) {
      console.log('FAIL:', r.error);
      continue;
    }
    console.log(`耗时: ${r.ms}ms | schemes: ${r.hasSchemes} | 滴定: ${r.hasTitration} | 电导率: ${r.hasConductivity}`);
    console.log(r.content.slice(0, 1200));
  } catch (e) {
    console.log('ERR:', e.message);
  }
}
