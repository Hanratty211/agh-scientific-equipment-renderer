# V27 CHECKPOINT v01

日期：2026-10-13
分支：agh/validation-next-2026
来源：arXiv:2610.07703（acoustic levitation liquid marble，8页 PDF 已落盘）

## 本轮状态
- [x] build_v01.py 已写（含声学悬浮腔、PZT 换能器、液滴核心 + Lycopodium 粒子壳、BOS 背光 + 光束、相机 + schlieren 镜片、支撑底座、控制电子盒）
- [x] Blender 运行成功 → scene_v01.blend + overview_v01.png（sha256=57bf7f...）
- [ ] 读图验收：AGH 内 vision-skill 不可用，视觉核验由外部审阅者完成

## 已知未定项
- 腔体材料（假设石英玻璃，alpha=0.15）
- 腔体精确尺寸（C_R=4cm，C_H=10cm 保守估计）
- 粒子壳厚度（核心半径 ×1.25 比例假设）
- 实验台架（标准光学面包板假设）

## 下一步
1. 外部审阅者读图
2. 记录问题 → v02 修复
