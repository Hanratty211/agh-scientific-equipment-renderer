# V30 来源与建模依据（SOURCE_NOTES）

## 来源
- 论文：arXiv:2610.13525 — *UV Fluorescence Sensing of Medical-Chemical-Biological Analytes by an AlGaN/Si-on-Sapphire Optoelectronic Chip*（Richard Soref）
- 本地 PDF：`validation-next/source-check/arXiv-2610.13525.pdf`（31页，PyMuPDF 打开成功）
- 目标图版：Fig. 4（VCSEL 底部视图）、Fig. 5（VCSEL 3D 透视）、Fig. 10（顶部视图芯片布局）、Fig. 11（剖面：样品在顶面，光电芯片在底面）、Fig. 12（Wi-Fi 芯片底部视图）

## 输入类别
D（正文/方法文字为主）—— 无本地 Fig 高清 PNG，几何依据正文文字（芯片 2×5 cm、VCSEL 200μm 方、Mesa 140μm 直径、AlN 50μm、Si PD 3×5 mm、各芯片尺寸）保守估计。

## 建模范围（首版 v01，低成本）

| 组件 | 来源依据 | 状态 |
|---|---|---|
| 蓝宝石芯片体（20×50×4 mm，透明） | 正文：2 cm × 5 cm C-plane (0001) sapphire，UV-Vis transparent | 来源可见 |
| VCSEL p-DBR 层（13 层 AlN/AlGaN） | Fig. 4/5 正文：p-type DBR R=99.5% | 来源可见 |
| VCSEL 活性 Mesa（AlGaN，140μm 直径圆柱） | Fig. 5 正文：140 μm diameter active mesa | 来源可见 |
| AlN 衬底（50μm） | Fig. 5 正文：integral 50-μm AlN laser-die substrate | 来源可见 |
| p-pad（Pd/Au 圆盘）/ n-pad（Ti/Al/Au 矩形） | Fig. 4 正文 | 来源可见 |
| 金线键合（p-wire, n-wire） | Fig. 4/5 正文：gold wires to metal traces | 来源可见 |
| UV 增强 Si PD（3×5 mm，黑色方片） | 正文：large-area Si PD with UV-enhancement | 来源可见 |
| 长通滤光片（PD 顶面，蓝紫色半透明） | Fig. 10 正文：PD has a laser-blocking filter on its face | 来源可见 |
| 电子芯片：LD driver, TIA, ADC, MCU(ESP32) | Fig. 12 正文：PD feeds TIA → ADC → ESP32 | 来源可见 |
| TP4056 充电器 IC | Fig. 12 正文：TP4056 LiPo charger | 来源可见 |
| Boost 3.7V→7V 转换器 | Fig. 12 正文：boost-converter IC drives VCSEL | 来源可见 |
| LDO 3.3V 转换器 | Fig. 12 正文：LDO drives electronic digital circuits | 来源可见 |
| LiPo 电池（3.7V 400 mAh，紫色圆角块） | Fig. 12 正文：400 mAh LiPo cell | 来源可见 |
| USB-C 充电口 | Fig. 12 正文：USB-C charge port | 来源可见 |
| Wi-Fi 天线走线（5 段蛇形，50 Ω 射频馈线） | Fig. 12 正文：50-Ω RF lead from ESP32 to on-chip microwave antenna | 来源可见 |
| 3.3V / 7V 金轨 | Fig. 12 正文：3.3 V Ti/Au rail, 7 V Ti/Au rail | 来源可见 |
| 样品凹槽（顶面） | Fig. 11 正文：sample contacting top face, ~0.5 mm diameter excitation zone | 来源可见 |
| UV 激光锥（VCSEL→样品→PD 荧光路径） | Fig. 7/11 正文：3.7° FWHM cone, 0.4 mm spot at top face | 来源可见 |
| 顶面薄玻璃盖（极透明） | 保守假设 | 建模假设 |
| 外壳壳体（18 mm 厚、24×54 mm） | 正文：rectangular housing bonded to chip bottom | 来源可见 |
| 支撑脚（4 个） | 通用假设 | 建模假设 |

## 未定项 / 未知
- 芯片内各 IC 具体厂家型号（只标名称，不假设外观）
- 50 Ω RF 馈线实际走线拓扑（蛇形天线段数为保守估计）
- 样品区具体位置（假设在芯片中心）
- 外壳壳体与芯片的固定方式（假设直接键合）

## 来源限制
- 无 Fig 高清 PNG，几何尺寸从正文文字推断（芯片 20×50×4 mm）
- VCSEL 各 DBR 层厚度未精确建模（简化为单层块体）
- 金线键合为直线近似（非抛物线弧）
