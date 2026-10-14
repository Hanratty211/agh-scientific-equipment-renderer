# V23 来源与建模依据（SOURCE_NOTES）

## 来源
- 论文：arXiv:2610.12867 — *Topologically steerable ultra-flat electro-optic combs via non-Hermitian frequency lattices*
- 本地 PDF：`validation-next/source-check/arXiv-2610.12867.pdf`（8页，PyMuPDF 打开成功）
- 目标依据：正文 Fig. 1–2 对非厄米 EO 梳原理与实验结果的说明，以及正文明确的 TFLN PM/AM 光纤环；Fig. 6(a) 仅是双谐振环扩展概念。**本地 8 页主文没有实验装置图，补充材料未取得。**

## 输入类别
B（系统架构图）

## 建模范围（首版 v01，低成本）

| 组件 | 来源依据 | 状态 |
|---|---|---|
| CW 激光输入 | EO 梳实验所需光学输入；主文未给厂家/波长盒体外观 | 正文依据，代表性外观 |
| TFLN PM 电光调制器 | 正文明确 optical fiber loop with TFLN phase modulator | 正文依据 |
| TFLN AM 电光调制器 | 正文明确 optical fiber loop with TFLN amplitude modulator | 正文依据 |
| 谐振光纤环与耦合器 | 正文描述 resonant EOFC / optical fiber loop | 正文依据，路径为示意 |
| RF/DC 驱动盒及两条驱动线 | 正文有 modulation 与 variable DC bias，但无仪器型号 | 正文依据，代表性外观 |
| Ring A / Ring B 双环概念插图 | Fig. 6(a) two coupled resonant rings；不是 Fig. 2 实验装置 | 来源可见，独立概念区 |
| OSA、示波器、独立 1480 nm 泵浦、EDFA | 主文检索未找到足够支持 | v02 删除；若补充材料取得再评估 |

## 未定项 / 未知
- CW 激光、耦合器与 RF/DC 驱动的厂家型号和尺寸
- 光纤环真实长度、弯曲半径和接口
- 主文所引用补充材料中的完整实验装置
- Fig. 6 双环概念的真实封装尺寸

## 来源限制
- 原记录把 Fig. 2(b) 光谱结果误写成实验装置，且把 Fig. 6 双环扩展误并入主实验链；本轮已纠正。
- 本地主文没有 OSA、oscilloscope、1480 nm 或独立泵浦的文字命中；这些 v01 具体器件不能据主文保留。
- v02 将 Fig. 6 双环放在独立抬高概念底座，与正文支持的 PM/AM 光纤环分开。
