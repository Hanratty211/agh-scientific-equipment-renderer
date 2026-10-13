# V29 verification notes

日期：2026-10-13
AGH 视觉读图：不可用（vision-skill 404）
像素统计：v01 非黑帧，mid-band 主导

## 来源
- 本地 PDF：validation-next/cases/v29_acoustic_black_hole_beam/source-materials/V29_springer_official.pdf（21 页）
- 正文参数：l1=50 mm，l2=5 mm，h2=8 mm，h1=1 mm，m=2，r=8 mm，s=110 mm，ρ=1160 kg/m³，E=2.46 GPa
- Fig. 12/13：实验流程图 + 设备照片

## AGH 已验证
- [x] Blender 运行成功 → scene_v01.blend + overview_v01.png（sha256=9ba8fb…）
- [x] 场景重开保存成功

## 已知未定项
- 梁体截面宽度（假设 20 mm）
- V-groove 支撑精确几何
- 激光测振器型号（代表性示意）
- 梁体总长度（6 周期 × 55 mm = 330 mm）

## 待外部审阅
- [ ] 6 周期 ABH 梁体 / 锥形楔块 / V-groove 支撑 / shaker / 激光测振头 / DAQ 是否清晰可辨
- [ ] 梁体尺寸是否与正文参数比例一致
