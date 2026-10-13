# V27 来源与建模依据（SOURCE_NOTES）

## 来源
- 论文：arXiv:2610.07703 — *Airborne liquid marble: Evaporation dynamics of liquid marble in acoustic levitation*
- 本地 PDF：`validation-next/source-check/arXiv-2610.07703.pdf`（8页，PyMuPDF 打开成功）
- 目标图版：实验装置（声学悬浮腔 + liquid marble + BOS 背光 + 相机）

## 输入类别
A（装置图）—— RSC 格式模板，Fig. 2 描述 LM 制备流程；BOS 测量在 §3.2 文字中描述

## 建模范围（首版 v01，低成本）

| 组件 | 来源依据 | 状态 |
|---|---|---|
| 声学悬浮腔（顶部/底部共振器 + 锥形过渡 + 中央窄部） | 正文：acoustic levitation cavity，standing wave node | 来源可见 |
| PZT 换能器（腔体底部黑色圆盘） | 正文：transducer generates standing wave | 来源可见 |
| 液滴核心（半透明蓝，水） | 正文：water droplet | 来源可见 |
| Lycopodium 粒子外壳（浅棕发光球体） | 正文：hydrophobic particles (LYCO spores) | 来源可见 |
| 支撑底座 + 4 条腿 | 通用假设 | 建模假设 |
| BOS 背光（黄色发光矩形面板，-X 侧） | §3.2：BOS method with background illumination | 正文依据 |
| BOS 光束（从背光穿透腔体至 +X） | §3.2：camera records light path | 正文依据 |
| 相机（+Y 侧，含 schlieren 镜片） | §3.2：camera records light path | 正文依据 |
| 控制电子盒 | 通用假设 | 建模假设 |

## 未定项 / 未知
- 腔体材料（假设石英玻璃，alpha=0.15 可见内部）
- 腔体精确尺寸（C_R=4cm，C_H=10cm 保守估计）
- 粒子壳厚度（核心半径 ×1.25 比例假设）
- 声学节点位置假设在腔体中部

## 来源限制
- 无 Fig 高清 PNG（RSC 模板页，无明确装置照片）
- BOS 光路配置为保守单光束表示
