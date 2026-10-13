# V29 来源与建模依据（SOURCE_NOTES）

## 来源
- 论文：10.1007/s42417-024-01645-0 — *Elastic Wave Modulation of Metamaterial Beams in Bidirectional Asymmetric Acoustic Black Holes*
- 本地 PDF：`validation-next/cases/v29_acoustic_black_hole_beam/source-materials/V29_springer_official.pdf`（21页，PyMuPDF 打开成功）
- 目标图版：Fig. 1（梁体几何：l1=50mm 锥区、l2=5mm 均匀区、h2=8mm、h1=1mm、m=2、r=8mm）、Fig. 12/13（实验装置照片）

## 输入类别
C（实验装置实拍图/安装照片）—— Fig. 12 为实验流程与设备照片，Fig. 13 为振动传递实验照片。

## 建模范围（首版 v01，低成本）

| 组件 | 来源依据 | 状态 |
|---|---|---|
| ABH 元材料梁（6 个周期单元，铝合金） | 正文：ρ=1160 kg/m3, E=2.46 GPa，6 个周期单元 | 来源可见 |
| 周期锥形 ABH 单元（交替正反 180°） | Fig. 1：bidirectional asymmetric，h(x)=ε·x^m | 来源可见 |
| 支撑底座（V-groove 型，3 处） | Fig. 12：beam on cradles | 来源可见 |
| 激励器（shaker，左端） | Fig. 12：excitation point | 来源可见 |
| 激光测振头（右端，红色光束至梁体） | Fig. 13：laser vibrometer | 来源可见 |
| DAQ 控制盒 | Fig. 12：primary test equipment | 来源可见 |
| 光学工作台 | 通用假设 | 建模假设 |
| 线缆（shaker→DAQ、sensor→DAQ） | Fig. 12 流程 | 来源可见 |

## 未定项 / 未知
- 梁体截面（假设宽度 20mm）
- 支撑 V-groove 精确几何
- 激光测振器型号（代表性示意）
- 梁体长度（假设 6 个周期 × 55mm = 330mm）

## 来源限制
- 无 Fig 高清 PNG，几何依据正文参数（l1, l2, h2, h1, m, r）
- 铝合金外观假设银灰色金属质感
