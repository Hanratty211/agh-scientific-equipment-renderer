# Case 15 retractable_sensor｜v01 低成本阶段记录

- 论文/DOI：Sensing of joint and spinal bending or stretching via a retractable and wearable badge reel; `10.1038/s41467-021-23207-8`，目标 Fig.1(c), main left exploded assembly。来源图与裁图 SHA 见 `../../targets.json`，源页 `https://www.nature.com/articles/s41467-021-23207-8/figures/1`；源图/目标图由 Codex 获取和输入选择检查，AGH 未将输入获取归为自己的执行。
- 要求范围：Reconstruct only the main left exploded sensor assembly: lid, rotor, coil spring/rope, stator and visible electrode rings. Exploded layers are intentionally separated; do not invent supports joining them. Exclude human/application scenes, inset electrode/SEM/photos and legend graphics.
- 输出：`build_v01.py`、`scene_v01.blend`、`overview_v01.png` (780×980, SHA256 `2933a4debc3a4a114970c0c1dd9c35663c5d3c8e9fd977c96acefc62853103e4`)，工作环境 Blender 5.1.2；全部尺寸为展示性 Blender 世界单位，无测量尺度。
- 源内有名组件映射记录：lid, rotor, stator, spring, retractable cord, electrode rings。相对位置/外观为 v01 建模假设，未逐像素审定；实际胶/孔/材料/内部接口不能由方块或文件存在证明。
- 工具：静态 `UNKNOWN` (exit 3)、保存场景独立审计 `UNVERIFIED` (exit 3，失败 0，未证 12), PNG `NUMERIC_ONLY` (exit 0)；报告和原始日志分别为 `record_static_v01.json/.log`、`audit_scene_v01.json/.log`、`review_numeric_v01.json/.log`。
- 场景仅声明有来源依据的部件存在，**没有**已核实的可见作用面接口/连接/支撑关系；端口、闭路、受力、遮挡、相机叠图及视觉一致性均未被该 QA 证明。不为 PASS 改用户范围；现有 required_components 只反映抽象组件清单，不声称路由已经可验证。
- 视觉审查者：Codex 已检查**原始输入的裁切选择**；AGH 对输出 PNG 未完成可靠读图，用户/Codex 输出对照审查待做。引用 `../../reference_vs_v01_local.png` 与 `../../pair_15_local.png`。
- 拆解层是展示态，不应按工作接触测试；弹簧/电极为示意形体，微观 inset 排除。
- v01 仅整体草稿；不得称装置、功能或论文图验收。
