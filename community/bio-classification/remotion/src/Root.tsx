import React from 'react';
import {Composition} from 'remotion';
import {BioClassification} from './compositions/BioClassification';

// 12 段 mp3 累计时长（秒），来自 ffprobe 实测
const SEG_DURS = [
  15.792, 22.680, 23.304, 22.056, 22.968,
  23.688, 26.040, 21.912, 24.288, 23.952,
  25.272, 19.056,
];
const TOTAL_SEC = SEG_DURS.reduce((a, b) => a + b, 0); // 271.008
const FPS = 30;
const DURATION_FRAMES = Math.ceil(TOTAL_SEC * FPS); // 8131

export const Root: React.FC = () => {
  return (
    <Composition
      id="BioClassification"
      component={BioClassification}
      durationInFrames={DURATION_FRAMES}
      fps={FPS}
      width={1280}
      height={720}
    />
  );
};
