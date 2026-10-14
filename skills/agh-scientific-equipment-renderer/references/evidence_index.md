# 证据索引｜v1.0 历史与 v1.1 新十篇，均非跨域验收

2026-10-14 v1.1 的新增门槛只根据[新十例逐篇锚点、版本哈希、外部人工失败与有限数值](validation_2026_10_14.md)形成；[建模前身份/端口表](identity_port_gate_v11.md)与[原文对照、实际路由/资产归因](source_render_and_demo_v11.md)为新版程序。14 Fig.1a 示意有笔电/示波器，选定 Fig.1c 照片渲染未显示它们；**不声称示波器连线已被本批验证**。旧 P1–P30 原则已含实物身份/接口和像素核对，不据执行失败倒推旧原则不存在；阶段 PNG 不会随 Skill 文字升级自动改善。

新增 [十篇公开论文 11–20 的自包含简表](public_validation_11_20.md)：给 DOI/图版、实际外部多轮阶段结论及技术边界。以下旧案例相对路径是**开发仓库可选档案**；Skill 复制到新目录后缺少这些档案不影响主流程、示例与脚本。每项只支持**指明的判断**；旧文件中有撤回的“通过”声明，必须连同更正阅读。案例尺寸、坐标、对象名、材质权重、视角数、采样数只属于案例证据，不作为 Skill 默认值。

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

## case-3 新增证据（逐项限定）
| 方法 | 本例实际观察与更正 | 尚不能证明 |
|---|---|---|
| P21/P22 逐跳与连接类型 | [v02 位置检查](../../../case-3_soft_robotics/V02_NOTES.md)→[v03 收窄措辞](../../../case-3_soft_robotics/V03_NOTES.md)→[v04 灰夹体局限](../../../case-3_soft_robotics/V04_NOTES.md)→[v05 高分辨率纠错](../../../case-3_soft_robotics/V05_NOTES.md)。外部指出「附着外观≠白管气动连接」 | 隐藏孔口、气密性、流向与背面连接；没有电连接实测案例 |
| P23 证据不足停于遮挡 | 出版方 [Fig.3b](https://www.nature.com/articles/s41467-023-39691-z) 原始 2001×1572 图像支持连续白管→蓝套→深色双线组件遮挡；旧灰短节/灰夹体撤回，v01–v05 保留于 [案例目录](../../../case-3_soft_robotics/STAGE_ACCEPTANCE.md) | 可见邻接不证明组件的孔道、内部流路、机械固定或压力表接口 |
| P24 外观/材料分层 | [v01–v05 记录](../../../case-3_soft_robotics/STAGE_ACCEPTANCE.md)与论文 Methods `soft-foamed body`；早期织物纹理是建模猜测，软指分段从块状/横条修正 | 材料配方、力学变形、精确比例或跨柔性装置复刻能力 |

**前例状态**：case-1 有正式图；case-2 低成本预览无正式图，v10 材质候选未应用总览；case-3 [v05 阶段收口](../../../case-3_soft_robotics/STAGE_ACCEPTANCE.md)获用户阶段认可但隐藏气路未知。

## 03–10 本批证据与可推广程度（均为低成本形态草案）
| 方法 | 已存脚本/检查点与外部阶段反馈 | 不可推广的特定值及未证实项 |
|---|---|---|
| P25 整体装配/朝向/实孔 | [05 v05 构建](../../../case-05_acoustic_materials/build_scene_v05.py)、[材料与 bbox 核验](../../../case-05_acoustic_materials/V05_CHECKPOINT.md)；[08 v03 阵列](../../../case-08_radio_frequency/V03_CHECKPOINT.md)及[10 v04 顶部贴片](../../../case-10_ultrasound/V04_CHECKPOINT.md)；[03 v04 筒环/小片](../../../case-03_radiative_cooling/V04_CHECKPOINT.md) | 孔径/数目与金属类别、条纹数、贴片实际层次皆案例代理；颜色/图片坐标不构成工程尺寸 |
| P26 连接与残留 | [09 v02 弹簧](../../../case-09_mechanical_memory/V02_CHECKPOINT.md)、[07 v03 测试装配](../../../case-07_flow_battery/V03_CHECKPOINT.md)、[03 v04 跨柱线](../../../case-03_radiative_cooling/V04_CHECKPOINT.md)、[10 v04 前壁删件](../../../case-10_ultrasound/V04_CHECKPOINT.md) | 弹簧附着不等于力学；07 只恢复泵/容器/堆/支撑**范围**，功能流路与回流未验证；04 端口数是示意 |
| P27 透射与相机 | [05 v04 入框](../../../case-05_acoustic_materials/V04_CHECKPOINT.md)及[05 v05 引擎/透射](../../../case-05_acoustic_materials/V05_CHECKPOINT.md)，外部读图反馈在[批次最终状态](../../../FINAL_EXTERNAL_REVIEW_STATUS.md) | Cycles 透射/采样/IOR 为本例展示参数，不代表实际板材性质；轴向裁剪不是横纵投影或遮挡 |
| P28 批次裁图与证据分层 | [最终外部模型读图状态](../../../FINAL_EXTERNAL_REVIEW_STATUS.md)、[07 v3 裁图与检查点](../../../FINAL_REFERENCE_CROP_V3_CHECKPOINT.md)、[最新版拼图](../../../cases_03-10_reference_previous_latest_final_montage_v2.png) | 外部模型后续确认 b/标签完整且排除 a/data，仅证明**参考范围**；非 AGH 亲眼读图、非用户最终验收/全域通过 |

**最新版索引**：03/04/10 v04；05 v05；06/09 v02；07/08 v03。03/04/05/06/08/09/10 的外部模型仅作有限视觉反馈；07 特别标为“范围改善，功能拓扑未验证”。以上经验把**行动与边界**提升，不把具体源图像素坐标、布尔面数、材质参数或接头数量写成通用默认。

## v0.6 自包含合成工具证据（拷贝 Skill 后可运行）
- [`examples/valid_record.json`](../examples/valid_record.json) 是 2 组件、2 锚点、一条合成机械线与一条支撑的非科学小例；[记录格式](project_record.md) 和 [`scripts/validate_project_record.py`](../scripts/validate_project_record.py) 明确静态检查边界。
- [`examples/make_synthetic_scene.py`](../examples/make_synthetic_scene.py) 生成临时 `.blend`；[`scripts/audit_saved_scene.py`](../scripts/audit_saved_scene.py) 独立读已存场景，报告世界几何端点/有限支撑近接及横、纵、深度。[`examples/run_v06_regression.py`](../examples/run_v06_regression.py) 的有效与可失败反例只证明这些工具在合成场景的分项行为。前轮纠错回归 31/31；末轮限定复核 44/44，新增非法嵌套类型静态短路、仅单器件、面内接触采样漏报、四类 render 路径反例。render inclusion 仍未完整核实，故有效几何场景总状态为 UNVERIFIED 而非 PASS；support_gap 可能伴随端口/投影等其他 FAIL，但 SUPPORT 分项必须 UNVERIFIED。
- [`scripts/review_images.py`](../scripts/review_images.py) 和 [`examples/review_config.json`](../examples/review_config.json) 演示 PNG 哈希、归一化裁框、Alpha/分辨率数值；[`scripts/make_svg_labels.py`](../scripts/make_svg_labels.py) 输出有字 SVG 或拒绝无字记录。这些均**不**建立源图观感、照片标签正确性、接触功能、设备身份或用户最终验收。

## v1.0 实物/接口纠错证据索引（仅可选开发仓库档案）

| 来源与作者 | 针对实际缺陷及版本 | 能支持的判断／不能支持的判断 |
|---|---|---|
| [R1 外部反馈](../../../public-validation-11-20/PHYSICAL_FEEDBACK_R1.md)；[R1 AGH 结果](../../../public-validation-11-20/PHYSICAL_FEEDBACK_R1_AGH_RESULT.md) | 笔记本机械连贯与类属控制面改善；12 供液管被宽前缀误删、12/17 barrel-tip 断开、数据口实心/线碰屏；14 amp→scope 修复 | 审阅者区分；旧 FAIL 保留，局部几何或相邻关系不证明功能 |
| [R2 外部反馈](../../../public-validation-11-20/PHYSICAL_FEEDBACK_R2.md)；[R2 AGH 检查点](../../../public-validation-11-20/PHYSICAL_FEEDBACK_R2_AGH_CHECKPOINT.md) | 12/17 保存场景与构建进程 PNG 筒方向不一致；16/19 尚有硬折；另进程重载更新图，原图不覆盖 | 已保存场景与 PNG 哈希追踪，独立审图另行进行；缓存 `.pyc` 使运行 revision 漂移并非源码修改 |
| [R3 AGH 检查点](../../../public-validation-11-20/PHYSICAL_FEEDBACK_R3_AGH_CHECKPOINT.md) | 16 两个 Perspex 壁实际开孔/绝缘座，但可见彩色尾在缓冲旁折出；旧中心环审计 FAIL/UNVERIFIED 留档 | 有限实体检查及仍失败/未知的像素问题分开；安装材料/电气安全未知 |
| [R4 AGH 检查点](../../../public-validation-11-20/PHYSICAL_FEEDBACK_R4_AGH_CHECKPOINT.md)；[Codex 独立实际像素审查](../../../public-validation-11-20/codex-review/physical_r4_actual_pixel_review.json)；[六例最终交付](../../../public-validation-11-20/GITHUB_DELIVERY_R4.md) | 相机后板真 +Y 面→座→插头→缓冲→线、16 两根线轴向入座；旧失败近景保留。会话转达独立外部模型的代表性低成本预览阶段反馈，非用户本人目检 | Codex 像素审查**不**归 AGH 第一手读图；真实 mesh/曲线有限检查不等于像素；阶段结论不等于人类最终、工业 CAD、安全、密封或隐藏路径验证 |

从 R1–R4 提炼的通用程序参见 [实物与接口方法](physical_equipment_and_interfaces.md)、[故障经验 P29–P32](pitfalls_and_fixes.md)。`agh-equipment/0.6` schema 与现有 helper/API **不变**；v1.0 的新增方法文字不等于旧审计脚本具备每一种孔/装配/Bezier 末段检验。
