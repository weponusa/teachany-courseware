import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

// ============================================================
// 12 段 narration 时长（秒）— 来自 ffprobe 实测
// ============================================================
const SEG_DURS = [
  15.792, 22.680, 23.304, 22.056, 22.968,
  23.688, 26.040, 21.912, 24.288, 23.952,
  25.272, 19.056,
];
const FPS = 30;
const SEG_FRAMES = SEG_DURS.map((d) => Math.round(d * FPS));
const SEG_STARTS = SEG_FRAMES.reduce<number[]>((acc, f, i) => {
  acc.push(i === 0 ? 0 : acc[i - 1] + SEG_FRAMES[i - 1]);
  return acc;
}, []);

// ============================================================
// 调色板 / 字体
// ============================================================
const PALETTE = {
  bg1: '#0f172a',
  bg2: '#1e293b',
  accent: '#10b981',
  accent2: '#34d399',
  warn: '#f59e0b',
  text: '#f1f5f9',
  sub: '#94a3b8',
  card: 'rgba(15,23,42,0.85)',
  border: '#334155',
};
const FONT = `"PingFang SC","Hiragino Sans GB","Noto Sans CJK SC",sans-serif`;

// 工具函数（不是 Hook） — 接收 frame 直接计算
const fadeAt = (frame: number, delay: number, dur = 18) =>
  interpolate(frame, [delay, delay + dur], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

const springAt = (frame: number, fps: number, delay: number) =>
  spring({frame: frame - delay, fps, config: {damping: 14, stiffness: 110}});

// ============================================================
// 顶部品牌条
// ============================================================
const Brand: React.FC = () => (
  <div
    style={{
      position: 'absolute',
      top: 24,
      left: 36,
      right: 36,
      display: 'flex',
      justifyContent: 'space-between',
      fontFamily: FONT,
      color: PALETTE.sub,
      fontSize: 18,
      letterSpacing: 2,
    }}
  >
    <span style={{color: PALETTE.accent2, fontWeight: 700}}>TeachAny · 八年级生物</span>
    <span>生物分类 · 界门纲目科属种</span>
  </div>
);

// ============================================================
// Scene 01 · 开场
// ============================================================
const Scene01: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t1 = fadeAt(frame, 8);
  const t2 = fadeAt(frame, 50);
  const t3 = springAt(frame, fps, 110);
  const t4 = fadeAt(frame, 220);
  return (
    <AbsoluteFill
      style={{background: `radial-gradient(ellipse at 50% 30%, ${PALETTE.bg2} 0%, ${PALETTE.bg1} 70%)`}}
    >
      <Brand />
      <div
        style={{
          position: 'absolute',
          top: '32%',
          left: 0,
          right: 0,
          textAlign: 'center',
          fontFamily: FONT,
          color: PALETTE.text,
        }}
      >
        <div style={{fontSize: 26, color: PALETTE.accent, opacity: t1, letterSpacing: 6}}>
          BIOLOGICAL CLASSIFICATION
        </div>
        <div
          style={{
            fontSize: 84,
            fontWeight: 800,
            marginTop: 18,
            opacity: t2,
            transform: `translateY(${(1 - t2) * 30}px)`,
            letterSpacing: 4,
          }}
        >
          生物分类
        </div>
        <div
          style={{
            fontSize: 28,
            color: PALETTE.sub,
            marginTop: 24,
            opacity: t3,
            transform: `scale(${0.9 + t3 * 0.1})`,
          }}
        >
          界 · 门 · 纲 · 目 · 科 · 属 · 种
        </div>
      </div>
      <div
        style={{
          position: 'absolute',
          bottom: 60,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontFamily: FONT,
          color: PALETTE.sub,
          fontSize: 22,
          opacity: t4,
        }}
      >
        从 200 万种生物 · 到 7 个等级的精确地址
      </div>
    </AbsoluteFill>
  );
};

// ============================================================
// Scene 02 · 200 万物种规模
// ============================================================
const Scene02: React.FC = () => {
  const frame = useCurrentFrame();
  const num = interpolate(frame, [10, 80], [0, 200], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const t2 = fadeAt(frame, 100);
  const t3 = fadeAt(frame, 180);
  const t4 = fadeAt(frame, 280);
  const cards = [
    {opa: t2, num: '~140万', label: '动物', color: PALETTE.accent},
    {opa: t3, num: '~37万', label: '植物', color: PALETTE.accent2},
    {opa: t4, num: '~10万', label: '真菌 + 微生物', color: PALETTE.warn},
  ];
  return (
    <AbsoluteFill style={{background: PALETTE.bg1}}>
      <Brand />
      <div style={{position: 'absolute', top: 110, left: 80, right: 80, fontFamily: FONT, color: PALETTE.text}}>
        <div style={{fontSize: 32, color: PALETTE.accent2}}>地球上的生命有多丰富？</div>
        <div
          style={{
            fontSize: 160,
            fontWeight: 800,
            marginTop: 24,
            color: PALETTE.warn,
            fontVariantNumeric: 'tabular-nums',
          }}
        >
          {Math.round(num)}
          <span style={{fontSize: 56, color: PALETTE.text, marginLeft: 16}}>万 +</span>
        </div>
        <div style={{fontSize: 28, color: PALETTE.sub, marginTop: 8}}>已被科学命名的物种</div>
      </div>
      <div
        style={{
          position: 'absolute',
          bottom: 70,
          left: 80,
          right: 80,
          display: 'flex',
          gap: 24,
          fontFamily: FONT,
          color: PALETTE.text,
        }}
      >
        {cards.map((c) => (
          <div
            key={c.label}
            style={{
              flex: 1,
              padding: '24px 28px',
              background: PALETTE.card,
              borderRadius: 16,
              border: `2px solid ${c.color}`,
              opacity: c.opa,
              transform: `translateY(${(1 - c.opa) * 30}px)`,
            }}
          >
            <div style={{fontSize: 42, fontWeight: 800, color: c.color}}>{c.num}</div>
            <div style={{fontSize: 22, color: PALETTE.sub, marginTop: 6}}>{c.label}</div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// ============================================================
// Scene 03 · 分类的三把钥匙
// ============================================================
const Scene03: React.FC = () => {
  const frame = useCurrentFrame();
  const t1 = fadeAt(frame, 10);
  const lenses = [
    {
      opa: fadeAt(frame, 90),
      icon: '🌿',
      tt: '形态结构',
      en: 'Morphology',
      desc: '看外形——脊柱、叶脉、骨骼',
      ex: '有无脊椎，分两大支',
      color: PALETTE.accent,
    },
    {
      opa: fadeAt(frame, 180),
      icon: '🫀',
      tt: '生理功能',
      en: 'Physiology',
      desc: '看本事——光合、呼吸、繁殖',
      ex: '种子 vs 孢子；恒温 vs 变温',
      color: PALETTE.accent2,
    },
    {
      opa: fadeAt(frame, 280),
      icon: '🧬',
      tt: '遗传亲缘',
      en: 'Phylogeny',
      desc: '看血缘——DNA 序列比对',
      ex: '现代分类的"金标准"',
      color: PALETTE.warn,
    },
  ];
  return (
    <AbsoluteFill style={{background: PALETTE.bg1}}>
      <Brand />
      <div
        style={{
          position: 'absolute',
          top: 100,
          left: 80,
          fontFamily: FONT,
          color: PALETTE.text,
          fontSize: 44,
          fontWeight: 700,
          opacity: t1,
        }}
      >
        分类的三把钥匙
      </div>
      <div
        style={{
          position: 'absolute',
          top: 160,
          left: 80,
          fontFamily: FONT,
          color: PALETTE.sub,
          fontSize: 22,
          opacity: t1,
        }}
      >
        Three Lenses for Classification
      </div>
      <div
        style={{
          position: 'absolute',
          top: 230,
          left: 80,
          right: 80,
          bottom: 60,
          display: 'flex',
          gap: 28,
          fontFamily: FONT,
          color: PALETTE.text,
        }}
      >
        {lenses.map((c) => (
          <div
            key={c.tt}
            style={{
              flex: 1,
              padding: '28px 30px',
              background: PALETTE.card,
              borderRadius: 18,
              border: `2px solid ${c.color}`,
              opacity: c.opa,
              transform: `translateY(${(1 - c.opa) * 40}px)`,
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <div style={{fontSize: 64}}>{c.icon}</div>
            <div style={{fontSize: 32, fontWeight: 700, marginTop: 8, color: c.color}}>{c.tt}</div>
            <div style={{fontSize: 16, color: PALETTE.sub, letterSpacing: 1}}>{c.en}</div>
            <div style={{fontSize: 22, color: PALETTE.text, marginTop: 18, lineHeight: 1.6}}>
              {c.desc}
            </div>
            <div
              style={{
                marginTop: 'auto',
                fontSize: 18,
                color: PALETTE.sub,
                borderTop: `1px solid ${PALETTE.border}`,
                paddingTop: 12,
              }}
            >
              例：{c.ex}
            </div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// ============================================================
// Scene 04 · 林奈七级阶梯
// ============================================================
const RANKS = [
  {zh: '界', en: 'Kingdom', color: '#ef4444'},
  {zh: '门', en: 'Phylum', color: '#f97316'},
  {zh: '纲', en: 'Class', color: '#eab308'},
  {zh: '目', en: 'Order', color: '#22c55e'},
  {zh: '科', en: 'Family', color: '#06b6d4'},
  {zh: '属', en: 'Genus', color: '#6366f1'},
  {zh: '种', en: 'Species', color: '#a855f7'},
];

const Scene04: React.FC = () => {
  const frame = useCurrentFrame();
  const head = fadeAt(frame, 8);
  return (
    <AbsoluteFill style={{background: PALETTE.bg1}}>
      <Brand />
      <div
        style={{
          position: 'absolute',
          top: 70,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontFamily: FONT,
          opacity: head,
        }}
      >
        <div style={{fontSize: 44, color: PALETTE.text, fontWeight: 700}}>林奈七级分类阶梯</div>
        <div style={{fontSize: 20, color: PALETTE.sub, marginTop: 6, letterSpacing: 3}}>
          范围由大 → 小 · 亲缘由远 → 近
        </div>
      </div>
      <div style={{position: 'absolute', top: 180, left: 120, right: 120, bottom: 60, fontFamily: FONT}}>
        {RANKS.map((r, idx) => {
          const op = fadeAt(frame, 30 + idx * 60);
          const indent = idx * 38;
          return (
            <div
              key={r.zh}
              style={{
                marginTop: idx === 0 ? 0 : 14,
                marginLeft: indent,
                width: `calc(${100 - idx * 8}% - ${indent}px)`,
                padding: '10px 20px',
                background: r.color,
                color: '#fff',
                fontSize: 28,
                fontWeight: 700,
                borderRadius: 10,
                opacity: op,
                transform: `translateX(${(1 - op) * -40}px)`,
                display: 'flex',
                alignItems: 'center',
                gap: 18,
                boxShadow: `0 6px 20px ${r.color}33`,
              }}
            >
              <span style={{fontSize: 36}}>{r.zh}</span>
              <span style={{opacity: 0.85, fontSize: 22, letterSpacing: 1}}>{r.en}</span>
              <span style={{marginLeft: 'auto', fontSize: 16, opacity: 0.7}}>第 {idx + 1} 级</span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ============================================================
// Scene 05 · 家猫七级地址
// ============================================================
const CAT_ADDR = [
  {rank: '界', val: '动物界', en: 'Animalia'},
  {rank: '门', val: '脊索动物门', en: 'Chordata'},
  {rank: '纲', val: '哺乳纲', en: 'Mammalia'},
  {rank: '目', val: '食肉目', en: 'Carnivora'},
  {rank: '科', val: '猫科', en: 'Felidae'},
  {rank: '属', val: '猫属', en: 'Felis'},
  {rank: '种', val: '家猫', en: 'F. catus'},
];

const Scene05: React.FC = () => {
  const frame = useCurrentFrame();
  const head = fadeAt(frame, 8);
  return (
    <AbsoluteFill style={{background: PALETTE.bg1}}>
      <Brand />
      <div
        style={{
          position: 'absolute',
          top: 80,
          left: 80,
          right: 80,
          fontFamily: FONT,
          color: PALETTE.text,
          opacity: head,
        }}
      >
        <div style={{fontSize: 42, fontWeight: 700}}>🐱 家猫的"七级地址"</div>
        <div style={{fontSize: 22, color: PALETTE.sub, marginTop: 6}}>
          就像门牌号——从大到小，逐层定位
        </div>
      </div>
      <div style={{position: 'absolute', top: 200, left: 80, right: 80, bottom: 70, fontFamily: FONT}}>
        {CAT_ADDR.map((c, idx) => {
          const op = fadeAt(frame, 60 + idx * 70);
          return (
            <div
              key={c.rank}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 16,
                marginTop: idx === 0 ? 0 : 8,
                opacity: op,
                transform: `translateX(${(1 - op) * 60}px)`,
              }}
            >
              <div style={{width: 80, fontSize: 26, fontWeight: 700, color: RANKS[idx].color}}>
                {c.rank}
              </div>
              <div
                style={{
                  flex: 1,
                  fontSize: 30,
                  fontWeight: 600,
                  color: PALETTE.text,
                  background: PALETTE.card,
                  padding: '10px 22px',
                  borderRadius: 10,
                  border: `1px solid ${RANKS[idx].color}66`,
                }}
              >
                {c.val}
                <span style={{fontSize: 20, color: PALETTE.sub, marginLeft: 14, fontWeight: 400}}>
                  {c.en}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ============================================================
// Scene 06 · 亲缘黄金规则
// ============================================================
const Rule: React.FC<{opa: number; left: string; right: string; color: string; example: string}> = ({
  opa,
  left,
  right,
  color,
  example,
}) => (
  <div
    style={{
      display: 'flex',
      alignItems: 'center',
      marginTop: 24,
      gap: 28,
      opacity: opa,
      transform: `translateX(${(1 - opa) * 50}px)`,
    }}
  >
    <div
      style={{
        flex: '0 0 280px',
        fontSize: 30,
        fontWeight: 700,
        color: PALETTE.text,
        textAlign: 'right',
      }}
    >
      {left}
    </div>
    <div style={{fontSize: 36, color}}>→</div>
    <div style={{flex: 1, fontSize: 28, color, fontWeight: 700}}>
      {right}
      <div style={{fontSize: 20, color: PALETTE.sub, marginTop: 6, fontWeight: 400}}>例：{example}</div>
    </div>
  </div>
);

const Scene06: React.FC = () => {
  const frame = useCurrentFrame();
  const head = fadeAt(frame, 8);
  return (
    <AbsoluteFill style={{background: PALETTE.bg1}}>
      <Brand />
      <div
        style={{
          position: 'absolute',
          top: 90,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontFamily: FONT,
          color: PALETTE.text,
          opacity: head,
        }}
      >
        <div style={{fontSize: 46, fontWeight: 800, color: PALETTE.warn}}>亲缘黄金规则</div>
        <div style={{fontSize: 24, color: PALETTE.sub, marginTop: 8}}>共同等级越低 = 亲缘关系越近</div>
      </div>
      <div style={{position: 'absolute', top: 240, left: 80, right: 80, fontFamily: FONT, color: PALETTE.text}}>
        <Rule
          opa={fadeAt(frame, 80)}
          left="同界不同门"
          right={'只是"远房亲戚"'}
          color={PALETTE.sub}
          example="家猫 vs 蚯蚓 → 都在动物界"
        />
        <Rule
          opa={fadeAt(frame, 200)}
          left="同科不同属"
          right={'是"近亲"'}
          color={PALETTE.accent}
          example="家猫 vs 老虎 → 都在猫科"
        />
        <Rule
          opa={fadeAt(frame, 320)}
          left="同属同种"
          right={'就是"自家人"'}
          color={PALETTE.warn}
          example="家犬 ≡ 灰狼（同种异亚种）"
        />
      </div>
    </AbsoluteFill>
  );
};

// ============================================================
// Scene 07 · 大熊猫反直觉
// ============================================================
const Scene07: React.FC = () => {
  const frame = useCurrentFrame();
  const head = fadeAt(frame, 8);
  const card1 = fadeAt(frame, 80);
  const arrow = fadeAt(frame, 200);
  const card2 = fadeAt(frame, 280);
  const conclusion = fadeAt(frame, 420);
  return (
    <AbsoluteFill style={{background: PALETTE.bg1}}>
      <Brand />
      <div
        style={{
          position: 'absolute',
          top: 80,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontFamily: FONT,
          color: PALETTE.text,
          opacity: head,
        }}
      >
        <div style={{fontSize: 42, fontWeight: 800}}>🐼 大熊猫——名字带"猫"，其实是熊</div>
        <div style={{fontSize: 22, color: PALETTE.sub, marginTop: 8}}>直觉判断 vs 科学分类</div>
      </div>
      <div
        style={{
          position: 'absolute',
          top: 220,
          left: 60,
          right: 60,
          display: 'flex',
          alignItems: 'stretch',
          gap: 40,
          fontFamily: FONT,
          color: PALETTE.text,
        }}
      >
        <div
          style={{
            flex: 1,
            padding: '28px 30px',
            background: PALETTE.card,
            borderRadius: 18,
            border: `2px dashed ${PALETTE.sub}`,
            opacity: card1,
            transform: `scale(${0.9 + card1 * 0.1})`,
          }}
        >
          <div style={{fontSize: 22, color: PALETTE.sub}}>❌ 听名字猜</div>
          <div style={{fontSize: 32, marginTop: 8, fontWeight: 700}}>"猫熊" → 猫科</div>
          <ul style={{fontSize: 20, color: PALETTE.sub, marginTop: 14, lineHeight: 1.8}}>
            <li>名字带"猫"</li>
            <li>圆头 + 大眼睛</li>
            <li>看起来像放大版的猫</li>
          </ul>
        </div>
        <div
          style={{
            flex: '0 0 80px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: 60,
            color: PALETTE.warn,
            opacity: arrow,
          }}
        >
          ⇒
        </div>
        <div
          style={{
            flex: 1,
            padding: '28px 30px',
            background: PALETTE.card,
            borderRadius: 18,
            border: `2px solid ${PALETTE.accent}`,
            opacity: card2,
            transform: `scale(${0.9 + card2 * 0.1})`,
          }}
        >
          <div style={{fontSize: 22, color: PALETTE.accent}}>✅ DNA 检测</div>
          <div style={{fontSize: 32, marginTop: 8, fontWeight: 700}}>食肉目 · 熊科 · 大熊猫属</div>
          <ul style={{fontSize: 20, color: PALETTE.sub, marginTop: 14, lineHeight: 1.8}}>
            <li>共祖时间 ~1900 万年</li>
            <li>与黑熊、棕熊同科</li>
            <li>"竹子是后期改吃的"</li>
          </ul>
        </div>
      </div>
      <div
        style={{
          position: 'absolute',
          bottom: 50,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontSize: 22,
          color: PALETTE.warn,
          fontFamily: FONT,
          opacity: conclusion,
        }}
      >
        🔑 看血缘，不要看长相——这就是"遗传亲缘"
      </div>
    </AbsoluteFill>
  );
};

// ============================================================
// Scene 08 · 家犬 ≡ 灰狼
// ============================================================
const Animal: React.FC<{opa: number; emoji: string; zh: string; sci: string}> = ({opa, emoji, zh, sci}) => (
  <div style={{textAlign: 'center', opacity: opa, transform: `translateY(${(1 - opa) * 30}px)`}}>
    <div style={{fontSize: 140}}>{emoji}</div>
    <div style={{fontSize: 32, fontWeight: 700, marginTop: 6}}>{zh}</div>
    <div style={{fontSize: 18, color: PALETTE.sub, fontStyle: 'italic'}}>{sci}</div>
  </div>
);

const Scene08: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const head = fadeAt(frame, 8);
  const dog = fadeAt(frame, 80);
  const wolf = fadeAt(frame, 160);
  const equal = springAt(frame, fps, 240);
  const proof = fadeAt(frame, 340);
  return (
    <AbsoluteFill style={{background: PALETTE.bg1}}>
      <Brand />
      <div
        style={{
          position: 'absolute',
          top: 80,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontFamily: FONT,
          color: PALETTE.text,
          opacity: head,
        }}
      >
        <div style={{fontSize: 42, fontWeight: 800}}>家犬 = 灰狼？</div>
        <div style={{fontSize: 22, color: PALETTE.sub, marginTop: 8}}>同种异亚种 · 同种地址</div>
      </div>
      <div
        style={{
          position: 'absolute',
          top: 220,
          left: 0,
          right: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 60,
          fontFamily: FONT,
          color: PALETTE.text,
        }}
      >
        <Animal opa={dog} emoji="🐕" zh="家犬" sci="Canis lupus familiaris" />
        <div
          style={{
            fontSize: 100,
            fontWeight: 800,
            color: PALETTE.accent,
            transform: `scale(${equal})`,
          }}
        >
          ≡
        </div>
        <Animal opa={wolf} emoji="🐺" zh="灰狼" sci="Canis lupus" />
      </div>
      <div
        style={{
          position: 'absolute',
          bottom: 60,
          left: 80,
          right: 80,
          padding: '20px 30px',
          background: PALETTE.card,
          borderRadius: 14,
          border: `2px solid ${PALETTE.accent}`,
          color: PALETTE.text,
          fontFamily: FONT,
          fontSize: 22,
          lineHeight: 1.7,
          opacity: proof,
        }}
      >
        <strong style={{color: PALETTE.accent}}>判定依据：</strong>
        交配能产生有生育力的后代 + DNA 高度同源 → 同属同种，仅家犬是 1.5 万年前驯化出的亚种。
      </div>
    </AbsoluteFill>
  );
};

// ============================================================
// Scene 09 · 本地物种探究引导
// ============================================================
const Scene09: React.FC = () => {
  const frame = useCurrentFrame();
  const head = fadeAt(frame, 8);
  const items = [
    {opa: fadeAt(frame, 80), emoji: '🌳', zh: '校园那棵大树', q: '是被子还是裸子？'},
    {opa: fadeAt(frame, 170), emoji: '🦋', zh: '花坛上的蝴蝶', q: '昆虫纲 · 鳞翅目'},
    {opa: fadeAt(frame, 260), emoji: '🐦', zh: '清晨的麻雀', q: '雀形目 · 文鸟科'},
    {opa: fadeAt(frame, 350), emoji: '🐠', zh: '池塘里的金鱼', q: '鲤形目 · 鲤科'},
  ];
  return (
    <AbsoluteFill style={{background: PALETTE.bg1}}>
      <Brand />
      <div
        style={{
          position: 'absolute',
          top: 80,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontFamily: FONT,
          color: PALETTE.text,
          opacity: head,
        }}
      >
        <div style={{fontSize: 42, fontWeight: 700}}>🔍 把分类带回校园</div>
        <div style={{fontSize: 22, color: PALETTE.sub, marginTop: 8}}>身边的每一个生命都有 7 级地址</div>
      </div>
      <div
        style={{
          position: 'absolute',
          top: 230,
          left: 80,
          right: 80,
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 24,
          fontFamily: FONT,
          color: PALETTE.text,
        }}
      >
        {items.map((it) => (
          <div
            key={it.zh}
            style={{
              padding: '24px 28px',
              background: PALETTE.card,
              borderRadius: 16,
              border: `1px solid ${PALETTE.border}`,
              opacity: it.opa,
              transform: `translateY(${(1 - it.opa) * 30}px)`,
              display: 'flex',
              alignItems: 'center',
              gap: 24,
            }}
          >
            <div style={{fontSize: 70}}>{it.emoji}</div>
            <div>
              <div style={{fontSize: 28, fontWeight: 700}}>{it.zh}</div>
              <div style={{fontSize: 22, color: PALETTE.accent2, marginTop: 6}}>{it.q}</div>
            </div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// ============================================================
// Scene 10 · 探究方法五步
// ============================================================
const STEPS = [
  {n: '1', t: '观察', d: '记录形态特征'},
  {n: '2', t: '比对', d: '查图鉴 / 检索表'},
  {n: '3', t: '验证', d: 'DNA / 解剖 / 教师确认'},
  {n: '4', t: '定位', d: '填入界门纲目科属种'},
  {n: '5', t: '画图', d: '绘制亲缘关系树'},
];

const Scene10: React.FC = () => {
  const frame = useCurrentFrame();
  const head = fadeAt(frame, 8);
  return (
    <AbsoluteFill style={{background: PALETTE.bg1}}>
      <Brand />
      <div
        style={{
          position: 'absolute',
          top: 80,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontFamily: FONT,
          color: PALETTE.text,
          opacity: head,
        }}
      >
        <div style={{fontSize: 42, fontWeight: 700}}>探究方法 · 五步法</div>
        <div style={{fontSize: 22, color: PALETTE.sub, marginTop: 8}}>从田野到分类阶梯</div>
      </div>
      <div
        style={{
          position: 'absolute',
          top: 230,
          left: 50,
          right: 50,
          display: 'flex',
          alignItems: 'stretch',
          gap: 14,
          fontFamily: FONT,
          color: PALETTE.text,
        }}
      >
        {STEPS.map((s, idx) => {
          const op = fadeAt(frame, 60 + idx * 80);
          return (
            <React.Fragment key={s.n}>
              <div
                style={{
                  flex: 1,
                  padding: '24px 18px',
                  background: PALETTE.card,
                  borderRadius: 14,
                  border: `2px solid ${PALETTE.accent}`,
                  opacity: op,
                  transform: `translateY(${(1 - op) * 40}px)`,
                  textAlign: 'center',
                }}
              >
                <div
                  style={{
                    width: 56,
                    height: 56,
                    borderRadius: 28,
                    background: PALETTE.accent,
                    color: '#0f172a',
                    fontSize: 30,
                    fontWeight: 800,
                    lineHeight: '56px',
                    margin: '0 auto',
                  }}
                >
                  {s.n}
                </div>
                <div style={{fontSize: 26, fontWeight: 700, marginTop: 14}}>{s.t}</div>
                <div style={{fontSize: 18, color: PALETTE.sub, marginTop: 8, lineHeight: 1.5}}>
                  {s.d}
                </div>
              </div>
              {idx < STEPS.length - 1 && (
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    color: PALETTE.accent2,
                    fontSize: 36,
                    opacity: fadeAt(frame, 80 + idx * 80),
                  }}
                >
                  →
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ============================================================
// Scene 11 · 三个带走核心
// ============================================================
const Scene11: React.FC = () => {
  const frame = useCurrentFrame();
  const head = fadeAt(frame, 8);
  const points = [
    {opa: fadeAt(frame, 80), n: '01', tt: '7 级地址', d: '界门纲目科属种，由大到小', color: PALETTE.accent},
    {opa: fadeAt(frame, 220), n: '02', tt: '亲缘黄金规则', d: '共同等级越低 = 亲缘越近', color: PALETTE.accent2},
    {opa: fadeAt(frame, 370), n: '03', tt: '看血缘不看长相', d: 'DNA 是分类的金标准', color: PALETTE.warn},
  ];
  return (
    <AbsoluteFill style={{background: `linear-gradient(135deg, ${PALETTE.bg1} 0%, ${PALETTE.bg2} 100%)`}}>
      <Brand />
      <div
        style={{
          position: 'absolute',
          top: 90,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontFamily: FONT,
          opacity: head,
        }}
      >
        <div style={{fontSize: 46, color: PALETTE.text, fontWeight: 800}}>带走这三件事</div>
        <div style={{fontSize: 22, color: PALETTE.sub, marginTop: 8}}>The Three Takeaways</div>
      </div>
      <div
        style={{
          position: 'absolute',
          top: 230,
          left: 80,
          right: 80,
          display: 'flex',
          gap: 28,
          fontFamily: FONT,
          color: PALETTE.text,
        }}
      >
        {points.map((p) => (
          <div
            key={p.n}
            style={{
              flex: 1,
              padding: '32px 28px',
              background: PALETTE.card,
              borderRadius: 18,
              border: `2px solid ${p.color}`,
              opacity: p.opa,
              transform: `scale(${0.9 + p.opa * 0.1})`,
              textAlign: 'center',
            }}
          >
            <div style={{fontSize: 56, fontWeight: 800, color: p.color, fontFamily: 'Georgia, serif'}}>
              {p.n}
            </div>
            <div style={{fontSize: 28, fontWeight: 700, marginTop: 14}}>{p.tt}</div>
            <div style={{fontSize: 20, color: PALETTE.sub, marginTop: 16, lineHeight: 1.7}}>{p.d}</div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// ============================================================
// Scene 12 · 告别
// ============================================================
const Scene12: React.FC = () => {
  const frame = useCurrentFrame();
  const t1 = fadeAt(frame, 8);
  const t2 = fadeAt(frame, 60);
  const t3 = fadeAt(frame, 140);
  return (
    <AbsoluteFill
      style={{background: `radial-gradient(ellipse at 50% 50%, ${PALETTE.bg2} 0%, ${PALETTE.bg1} 75%)`}}
    >
      <Brand />
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          fontFamily: FONT,
          color: PALETTE.text,
        }}
      >
        <div style={{fontSize: 32, color: PALETTE.accent2, opacity: t1, letterSpacing: 4}}>恭喜你 · 完成本课</div>
        <div
          style={{
            fontSize: 64,
            fontWeight: 800,
            marginTop: 30,
            opacity: t2,
            transform: `translateY(${(1 - t2) * 30}px)`,
          }}
        >
          继续探索身边的 200 万种生命
        </div>
        <div style={{fontSize: 22, color: PALETTE.sub, marginTop: 36, opacity: t3, textAlign: 'center'}}>
          下一课：植物分类与被子植物的多样性
          <br />
          <span style={{color: PALETTE.accent}}>TeachAny · AI 学伴随时为你解答</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ============================================================
// 主合成
// ============================================================
const SCENES = [
  Scene01, Scene02, Scene03, Scene04, Scene05, Scene06,
  Scene07, Scene08, Scene09, Scene10, Scene11, Scene12,
];

export const BioClassification: React.FC = () => {
  return (
    <AbsoluteFill style={{background: PALETTE.bg1}}>
      {/* 全程音轨 */}
      <Audio src={staticFile('audio/narration.mp3')} />

      {/* 12 个场景按时长串接 */}
      {SCENES.map((Scene, idx) => (
        <Sequence key={idx} from={SEG_STARTS[idx]} durationInFrames={SEG_FRAMES[idx]}>
          <Scene />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
