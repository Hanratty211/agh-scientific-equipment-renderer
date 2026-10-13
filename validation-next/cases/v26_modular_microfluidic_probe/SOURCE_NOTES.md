# V26 来源与建模依据（SOURCE_NOTES）

## 来源
- 论文：arXiv:2610.13796 — *Particle dynamics in a microfluidic T-junction vortex flow: the role of history force*
- 本地 PDF：`validation-next/source-check/arXiv-2610.13796.pdf`（30页，PyMuPDF 打开成功）
- 目标图版：Fig. 1（T-junction 数值域示意：5L×L 主臂，L 分支，Rc=0.4L 弯曲半径，inflow/outflow/branch outflow）

## 输入类别
A（工程图/通道图）—— Fig. 1 为数值域示意，含坐标、L/Rc 比例关系。

## 建模范围（首版 v01，低成本）
以下组件基于 Fig. 1 几何比例 + 正文文字（粒子追踪器、光学观察链路）保守建模：

| 组件 | 来源依据 | 状态 |
|---|---|---|
| 透明基底 wafer（PDMS-like） | 正文：microfluidic 通道，未明确材料；假设 PDMS 透明 | 建模假设 |
| T-junction 壁（inflow arm, outflow arm, branch arm） | Fig. 1 几何：W=L，arm=L，分支沿 Y | 来源可见 |
| 内部流体（inflow/outflow/branch） | Fig. 1 通道空间 | 来源可见 |
| 粒子追踪器（tracer particle，橙球） | 正文：finite-size particle 直径 ~ 0.4L（Rc=0.4L 为通道曲率半径，粒径 a*=0.2L）；假设 | 建模假设 |
| 顶部光学端口（3× 圆柱口 + 孔） | Fig. 1 三出口标注 inflow/outflow/branch outflow；保守估计端口在顶部 | 建模假设 |
| 观察光路（laser 侧臂 + beam） | 正文：schlieren / 背光照；BOS 方法提及光路 | 正文依据 |
| 检测块（detector block + lens） | 正文：BOS 相机记录折射率梯度 | 正文依据 |
| 支撑底板 | 通用实验台架假设 | 建模假设 |
| 相机机壳（camera body + lens） | 正文：camera records light path | 正文依据 |

## 未定项 / 未知
- 具体通道尺寸（L、W 绝对值）—— 论文为无量纲化数值域，无实际 mm 尺度
- 粒子材料（假设金属球，金色）
- 端口尺寸（假设 3 mm 直径）
- 光路具体配置（schlieren 还是纯 BOS 相机）—— 保守用单一入射光束表示
- 实验台架（假设标准光学面包板尺寸）

## 来源限制
- 无本地 Fig. 1 PNG 图像，几何依据正文文字和 Fig. 1 描述（5L×L 主臂，L 分支，Rc=0.4L）
- 无厂家实物外观参考；wafer/端口/光路组件均为代表性示意
