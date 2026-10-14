# V21 来源与建模依据（SOURCE_NOTES）

## 来源
- 论文：arXiv:2610.10294 — *Sub-shot-noise mid-infrared photothermal measurements using twin beams*
- SELECTION.md 记录：B 类；本轮另用 `curl.exe` 下载 arXiv PDF（临时文件 `v21.pdf`，SHA-256 `3758623acd22038bf3ead7d716a162f6c7d087ddb75619090bd70c5767a0f3a3`，2026-10-13 UTC），未把临时缓存纳入仓库
- 目标范围：twin-beam MIP 系统 1.5 µm 飞秒激光、FBG/fiber amplifier、SHG/PPLN OPA、seed 滤波与延迟线、QCL/AOM、sample cell、BPD/RFSA 链路

## 输入类别
B（系统架构图）

## 建模范围（v02 来源纠错后）
根据 PDF Fig.1、正文 §2–5 和 Methods/Supplementary 文字建立分支拓扑；v02 不再把系统简化为横向串联盒体：

| 组件 | 来源依据 | 状态 |
|---|---|---|
| 1.5 µm 飞秒激光器（左端盒子） | SELECTION.md 组件清单 | 来源可见 |
| FBG（光纤布拉格光栅，蓝色小块） | 组件清单 | 来源可见 |
| EDFA（掺铒光纤放大器，棕色盒子） | 组件清单 | 来源可见 |
| PPLN OPA 晶体（蓝紫色透明方块） | 组件清单：SHG/PPLN OPA | 来源可见 |
| Seed filter（紫粉色小方块） | 组件清单：seed 滤波 | 来源可见 |
| 延迟线（黑色方框，光纤盘绕） | 组件清单：延迟线 | 来源可见 |
| QCL 激光器（深蓝盒子） | 组件清单：QCL | 来源可见 |
| AOM（深灰小块） | 组件清单：AOM | 来源可见 |
| 样品池（开放玻璃池 + 吸收体） | 组件清单：sample cell | 来源可见 |
| BPD（平衡探测器盒子） | 组件清单：BPD | 来源可见 |
| RFSA（示波器/频谱仪，带屏幕） | 组件清单：RFSA 链路 | 来源可见 |
| 双路光路（seed 橙、QCL 青、输出黄） | twin-beam 架构 | 建模假设 |
| 光纤连线（各组件间灰色细管） | 光学系统 | 来源可见 |

## 未定项 / 未知
- 无本地 PDF，组件外观/尺寸为代表性示意
- PPLN 晶体实际尺寸、延迟线光纤长度未精确
- BPD 具体厂家型号
- RFSA 显示波形内容（静态屏幕，非实际数据）

## 来源限制
- Fig.1 是系统示意图，不提供全部厂家外观或精确空间尺度。
- v02 使用代表性几何；光纤走线仍是低成本曲线路径，不等于实测装配。
- Supplementary/Methods 明确的 FBG、EDFA、PPLN、QCL/AOM、CaF2 cell、BPD、RFSA 已按功能分列；真实接口和镜片安装仍未确认。
