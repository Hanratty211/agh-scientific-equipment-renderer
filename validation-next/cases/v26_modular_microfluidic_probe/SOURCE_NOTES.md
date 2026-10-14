# V26 来源与建模依据（SOURCE_NOTES）

## 来源
- 论文：arXiv:2610.13796 — *Particle dynamics in a microfluidic T-junction vortex flow: the role of history force*
- 本地 PDF：`validation-next/source-check/arXiv-2610.13796.pdf`（30页，PyMuPDF 打开成功）
- 目标图版：Fig. 1（T-junction 数值域示意：5L×L 主臂，L 分支，Rc=0.4L 弯曲半径，inflow/outflow/branch outflow）

## 输入类别
A（工程图/通道图）—— Fig. 1 为数值域示意，含坐标、L/Rc 比例关系。

## 建模范围（v04 来源纠错后）
本地 PDF 全文检索确认 `BOS`、`schlieren`、`camera`、`laser`、`optical` 均无命中。本文是 OpenFOAM DNS 与粒子轨迹研究，不是光学实验装置论文。v04 仅重建 Fig. 1 数值域及正文粒子轨迹范围：

| 组件 | 来源依据 | 状态 |
|---|---|---|
| 90° T-junction square-section numerical domain | Fig. 1 与 §2：square cross-sections | 来源可见/正文依据 |
| 主臂左右 5L、分支 L、内圆角 Rc=0.4L | Fig. 1 标注 | 来源可见 |
| 一个 inflow 与两个 outflow 截面 | Fig. 1 标注 | 来源可见；v04 以截面环而非物理接头表达 |
| 流体域体积和边界墙 | DNS geometry / no-slip solid walls | 正文依据；颜色为示意 |
| 有限尺寸球形粒子及少量轨迹样本 | §2.2 particle trajectory；几何仅作代表性轨迹预览 | 正文依据＋建模示意 |
| BOS、schlieren、相机、激光、探测器、光学台、物理顶置端口 | PDF 无依据 | v04 全部删除 |

## 未定项 / 未知
- 论文采用与 Vigolo et al. 实验对应的 L=4.8×10⁻³ m，但 v04 只表达比例，不宣称制造尺寸复刻。
- v04 粒子颜色和轨迹采样点是可视化选择，不表示材料或某一条论文数值轨迹。
- Fig. 1 内圆角 Rc=0.4L 在 v04 低成本墙体中尚未做真实曲面，只保留在证据记录中。

## 来源限制
- Fig. 1 已由本地 PDF 第 5 页读取；它是数值域示意，不支持实物 wafer、端口接头或光学观察链。
- v01–v03 的 BOS/光学链属于本次执行误读，旧版本保留为失败历史；v04 缩回有据范围。
