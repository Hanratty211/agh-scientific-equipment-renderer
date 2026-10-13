# V27 verification notes

日期：2026-10-13
AGH 视觉读图：不可用（vision-skill 404）
像素统计：v01 非黑帧，mid-band 主导

## 来源
- 本地 PDF：validation-next/source-check/arXiv-2610.07703.pdf（8 页）
- 目标：声学悬浮腔 + liquid marble + BOS 背光 + 相机

## AGH 已验证
- [x] Blender 运行成功 → scene_v01.blend + overview_v01.png（sha256=57bf7f…）
- [x] 场景重开保存成功

## 已知未定项
- 腔体材料（假设石英玻璃，alpha=0.15）
- 腔体精确尺寸（C_R=4 cm，C_H=10 cm 保守估计）
- 粒子壳厚度（核心半径 ×1.25 比例假设）

## 待外部审阅
- [ ] 声学悬浮腔 / PZT 换能器 / 液滴核心 / Lycopodium 粒子壳 / BOS 背光 / 相机是否清晰可辨
