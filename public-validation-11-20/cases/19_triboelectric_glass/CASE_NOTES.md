# Case 19 triboelectric_glass｜v01 低成本阶段记录

- 论文/DOI：Integrated triboelectric nanogenerator and radiative cooler for all-weather transparent glass surfaces; `10.1038/s41467-024-50872-2`，目标 Fig.2(g)。来源图与裁图 SHA 见 `../../targets.json`，源页 `https://www.nature.com/articles/s41467-024-50872-2/figures/2`；源图/目标图由 Codex 获取和输入选择检查，AGH 未将输入获取归为自己的执行。
- 要求范围：Reconstruct the g-panel tilted glass/drop delivery test and electrical readout instruments. Do not turn droplet time-series states e/f into simultaneous hardware or invent concealed electrode routes.
- 输出：`build_v01.py`、`scene_v01.blend`、`overview_v01.png` (990×690, SHA256 `855c4a2a4ba5eea0ceb4c9645888e6bc6070425405c8dae73b5061676197bff9`)，工作环境 Blender 5.1.2；全部尺寸为展示性 Blender 世界单位，无测量尺度。
- 源内有名组件映射记录：tilted test fixture, TeRC glass, film, drop dispenser, electrical readout。相对位置/外观为 v01 建模假设，未逐像素审定；实际胶/孔/材料/内部接口不能由方块或文件存在证明。
- 工具：静态 `UNKNOWN` (exit 3)、保存场景独立审计 `UNVERIFIED` (exit 3，失败 0，未证 9), PNG `NUMERIC_ONLY` (exit 0)；报告和原始日志分别为 `record_static_v01.json/.log`、`audit_scene_v01.json/.log`、`review_numeric_v01.json/.log`。
- 场景仅声明有来源依据的部件存在，**没有**已核实的可见作用面接口/连接/支撑关系；端口、闭路、受力、遮挡、相机叠图及视觉一致性均未被该 QA 证明。不为 PASS 改用户范围；现有 required_components 只反映抽象组件清单，不声称路由已经可验证。
- 视觉审查者：Codex 已检查**原始输入的裁切选择**；AGH 对输出 PNG 未完成可靠读图，用户/Codex 输出对照审查待做。引用 `../../reference_vs_v01_local.png` 与 `../../pair_19_local.png`。
- v01 仅整体草稿；不得称装置、功能或论文图验收。
