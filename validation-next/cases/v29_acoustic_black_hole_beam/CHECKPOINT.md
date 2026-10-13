# V29 CHECKPOINT v01

日期：2026-10-13
分支：agh/validation-next-2026
来源：10.1007/s42417-024-01645-0（双向非对称 ABH 元材料梁，C 类，21页 Springer PDF 已落盘）

## 本轮状态
- [x] build_v01.py 已写（6 周期 ABH 梁体 + 锥形楔块交替 180° + V-groove 支撑×3 + shaker 激励器 + 激光测振头（红 beam）+ DAQ 盒 + 线缆）
- [x] Blender 运行成功 → scene_v01.blend + overview_v01.png（sha256=9ba8fb...）
- [ ] 读图验收：AGH 内 vision-skill 不可用，视觉核验由外部审阅者完成

## 已知未定项
- 梁体截面宽度（假设 20mm）
- 支撑 V-groove 精确几何
- 激光测振器型号（代表性示意）
- 梁体总长度（假设 6 周期 × 55mm = 330mm）

## 来源
- 正文参数：l1=50mm 锥区，l2=5mm 均匀区，h2=8mm，h1=1mm，m=2，r=8mm，ρ=1160 kg/m³，E=2.46 GPa
- Fig. 12：实验流程图 + 主测试设备照片
- Fig. 13：弯曲/纵向振动传递实验照片
