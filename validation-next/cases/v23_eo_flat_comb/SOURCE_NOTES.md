# V23 来源与建模依据（SOURCE_NOTES）

## 来源
- 论文：arXiv:2610.12867 — *Topologically steerable ultra-flat electro-optic combs via non-Hermitian frequency lattices*
- 本地 PDF：`validation-next/source-check/arXiv-2610.12867.pdf`（8页，PyMuPDF 打开成功）
- 目标图版：Fig. 2(b) 实验装置（PM、AM、EDFA、Ring A、Ring B、spectrum 链）

## 输入类别
B（系统架构图）

## 建模范围（首版 v01，低成本）

| 组件 | 来源依据 | 状态 |
|---|---|---|
| 1550 nm CW 激光器 | 正文：laser source | 来源可见 |
| PM 电光调制器（含偏置 T 接头） | Fig. 2(b)：PM | 来源可见 |
| AM 电光调制器（含偏置 T 接头） | Fig. 2(b)：AM | 来源可见 |
| EDFA（含 1480 nm 泵浦激光器） | Fig. 2(b)：EDFA | 来源可见 |
| Ring A 微环（torus + Si 芯片基底） | Fig. 2(b)：Ring A | 来源可见 |
| Ring B 微环（torus + Si 芯片基底） | Fig. 2(b)：Ring B（双梳） | 来源可见 |
| OSA（含屏幕） | 正文：spectrum 测量 | 来源可见 |
| 示波器（RF 信号源，驱动 AM/PM 偏置 T） | 正文：bias voltage V | 来源可见 |
| 光纤连线（6 段，光路 绿/蓝/黄） | 光路拓扑 | 来源可见 |
| 光学面包板（4 腿 + V-groove 槽） | 通用假设 | 建模假设 |

## 未定项 / 未知
- Ring 实际直径（假设 8mm）
- 各组件厂家型号（代表性示意）
- 光路走线为保守直线段，非实际光纤弯曲路径
- 示波器显示波形内容（静态屏幕）

## 来源限制
- 无 Fig 高清 PNG，组件尺寸/比例基于 Fig. 2(b) 文字描述
- 双梳 Ring A/B 布局为保守直线排列
