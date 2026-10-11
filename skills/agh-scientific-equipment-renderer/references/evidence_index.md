# v0.3 证据索引｜两例公开光学装置，非跨领域验收

路径相对本文件。每项只支持**指明的判断**；旧文件中有撤回的“通过”声明，必须连同更正阅读。案例尺寸、坐标、对象名、材质权重、视角数、采样数只属于案例证据，不作为 Skill 默认值。

| 方法/纠错 | case-1 可核查证据 | case-2 可核查证据 | 推广边界 |
|---|---|---|---|
| P1/P11 来源与预览 | [来源/实现状态](../../../case-1_87sr_cryo_lattice/notes_wavelengths_and_state.md)、[修订历史](../../../case-1_87sr_cryo_lattice/REVISION_LOG.md) | [原 PDF](../../../case-2_D2NN_OAM2/source_paper.pdf)、[原 Fig.2(a)](../../../case-2_D2NN_OAM2/reference_Fig2a.png)、[R7–R11 纠错与回到 3D](../../../case-2_D2NN_OAM2/REVISION_LOG_case2.md) | 案例 2 的 [早期证据基础](../../../case-2_D2NN_OAM2/evidence_base.md) 存在被撤回条目，**不可独立作最新布局依据** |
| P2/P3/P17 中心线、真实源端、工作面 | [case-1 v16 构建](../../../case-1_87sr_cryo_lattice/build_blender_v16.py)、[独立复算](../../../case-1_87sr_cryo_lattice/verify_v16.py) | [R4 bbox 反例](../../../case-2_D2NN_OAM2/verify_case2_r4_results.txt)、[R14 出口记录](../../../case-2_D2NN_OAM2/REVISION_LOG_case2.md)、[v7 核查](../../../case-2_D2NN_OAM2/verify_case2_v7_overview_results.txt) | case-2 的 laser_exit 壳内反例：共线/锚点贴面≠真实安装；v7 外置接嘴**仍是示意** |
| P4/P5/P9/P10 壁窗、独立材质/局部恢复与相机 | [v16 图审记录](../../../case-1_87sr_cryo_lattice/REVIEW_RECORD_v16.md) | [R7 地面/侧画外更正](../../../case-2_D2NN_OAM2/REVISION_LOG_case2.md)、[v10 独立保存场景核查](../../../case-2_D2NN_OAM2/verify_case2_v10_overview_results.txt) | 双窗/玻璃材质是 case-1 特定；case-2 BS 作为薄片示意而非厂家棱镜 CAD |
| P8/P18 表面求交/单位/镜法向/自命中反例 | [v0.2 行为反例](../behavior_results.txt) | [R10 五分类和逆转置反例 16 项](../../../case-2_D2NN_OAM2/verify_case2_r10_results.txt)、[v10 保存场景结果](../../../case-2_D2NN_OAM2/verify_case2_v10_overview_results.txt) | 自动 PASS 只证明测试覆盖对象和阈值，不作视觉成功判定 |
| P15 身份/类型更正 | [case-1 图示状态](../../../case-1_87sr_cryo_lattice/notes_wavelengths_and_state.md) | [R8 撤回透射式 SLM、R13 平凸图注](../../../case-2_D2NN_OAM2/REVISION_LOG_case2.md)、[v10 构建脚本](../../../case-2_D2NN_OAM2/build_case2_v10_overview.py) | 反射式型号数据表由外部提供，当轮无网络复核；平凸分类不提供曲率 |
| P16 轴与包络分离 | [case-1 v16 构建](../../../case-1_87sr_cryo_lattice/build_blender_v16.py) | [R13 v6 公共轴](../../../case-2_D2NN_OAM2/REVISION_LOG_case2.md)、[v9 修订](../../../case-2_D2NN_OAM2/REVISION_RECORD_v9.md)、[v10 半径与设置](../../../case-2_D2NN_OAM2/REVISION_RECORD_v10.md) | v10 上排形态经本会话用户外部读图认可；束腰/焦距不宣称实测 |
| P19 纤维截面、材质小样 | [v16 图审记录](../../../case-1_87sr_cryo_lattice/REVIEW_RECORD_v16.md) | [R5 0 面光纤撤回/R6 曲线修复](../../../case-2_D2NN_OAM2/REVISION_LOG_case2.md)、[v10 材质对比](../../../case-2_D2NN_OAM2/MATERIAL_COMPARISON_v10.md) | 外部判 v10 总览灰粉；三档比较只提供选择，**未应用到总览**，未称通过 |
| P6/P12/P13/P14/P20 读图/失败/执行 | [case-1 AGH 记录](../../../case-1_87sr_cryo_lattice/AGH_EXECUTION_RECORD_v16.md)、[更正](../../../case-1_87sr_cryo_lattice/REVISION_LOG.md) | [case-2 AGH 关键事件摘录](../../../case-2_D2NN_OAM2/AGH_EXECUTION_RECORD_case2.md)、[完整修订与撤回](../../../case-2_D2NN_OAM2/REVISION_LOG_case2.md)、[v9](../../../case-2_D2NN_OAM2/REVISION_RECORD_v9.md)、[v10](../../../case-2_D2NN_OAM2/REVISION_RECORD_v10.md) | E# 是摘要而非 ledger 行号；旧记录自称的成功可能被后续推翻，必须按时间与更正阅读 |

**状态（本轮用户指示）**：case-1 有正式图；case-2 低成本预览已迭代，用户允许开始 Skill 更新，未生成正式图。v10 红束材质未获外部通过；[候选对比](../../../case-2_D2NN_OAM2/MATERIAL_COMPARISON_v10.md)尚未应用总览。两个来源均为公开光学案例，其他科研领域及工程 CAD 可复用性仍待检验。
