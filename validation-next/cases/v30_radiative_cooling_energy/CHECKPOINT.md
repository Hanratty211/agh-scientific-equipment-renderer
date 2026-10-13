# V30 CHECKPOINT v02

日期：2026-10-13
分支：agh/validation-next-2026
来源：arXiv:2610.13525（UV fluorescence AlGaN/Si-on-Sapphire chip，31页 PDF 已落盘）

## 本轮状态
- [x] build_v01.py → scene_v01.blend + overview_v01.png（sha256=6335bb...）
  - 外部审阅者反馈：整张图只有白色半透明外壳和底板，VCSEL/PD/芯片/LiPo/USB-C/金线/光束全部不可见
- [x] build_v02.py → scene_v02.blend + overview_v02.png（sha256=c2b3e1...）
  - 修复：sapphire chip alpha=0.08（极低遮挡），housing alpha=0.30，相机改为下方仰视底面，3 盏灯从下方照亮底面；VCSEL、PD、7 个 IC 芯片、LiPo、USB-C、金线、UV beam、荧光 beam 透过芯片体可见
- [ ] 读图验收：AGH 内 vision-skill 不可用，视觉核验由外部审阅者完成

## 已知未定项
- IC 厂家型号（只标名称）
- 50 Ω 天线走线精确拓扑
- 样品区具体位置（假设芯片中心）
- VCSEL 各 DBR 层厚度未精确建模（简化为单层块体）
