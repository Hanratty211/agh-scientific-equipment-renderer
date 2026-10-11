# Case 18 electrochemical_stack｜v01 低成本阶段记录

- 论文/DOI：A self-breathing electrode enabled by interface regulation and gradient wettability engineering for industrial H2O2 electrosynthesis; `10.1038/s41467-026-68436-x`，目标 Fig.6(c)。来源图与裁图 SHA 见 `../../targets.json`，源页 `https://www.nature.com/articles/s41467-026-68436-x/figures/6`；源图/目标图由 Codex 获取和输入选择检查，AGH 未将输入获取归为自己的执行。
- 要求范围：Reconstruct the ordered exploded stack and assembled four-cell stack shown in c. Consult caption for material/layer names and repeats; do not merge panels b cabinet or d tubing into the target. Exploded spacings are presentation choices, not working contact gaps.
- 输出：`build_v01.py`、`scene_v01.blend`、`overview_v01.png` (1280×700, SHA256 `49b90ed6a86577ff0ae01606f0c9b0de920c86299aec8ccd0baabcf7fc84ff38`)，工作环境 Blender 5.1.2；全部尺寸为展示性 Blender 世界单位，无测量尺度。
- 源内有名组件映射记录：exploded end plate 1, exploded gasket 2, exploded bipolar plate 3, exploded GDE 4, exploded cathode flow 6, exploded membrane 7, exploded anode 8, exploded anode flow 10, exploded collector 16, exploded end plate 17, four-cell assembled。相对位置/外观为 v01 建模假设，未逐像素审定；实际胶/孔/材料/内部接口不能由方块或文件存在证明。
- 工具：静态 `UNKNOWN` (exit 3)、保存场景独立审计 `UNVERIFIED` (exit 3，失败 0，未证 15), PNG `NUMERIC_ONLY` (exit 0)；报告和原始日志分别为 `record_static_v01.json/.log`、`audit_scene_v01.json/.log`、`review_numeric_v01.json/.log`。
- 场景仅声明有来源依据的部件存在，**没有**已核实的可见作用面接口/连接/支撑关系；端口、闭路、受力、遮挡、相机叠图及视觉一致性均未被该 QA 证明。不为 PASS 改用户范围；现有 required_components 只反映抽象组件清单，不声称路由已经可验证。
- 视觉审查者：Codex 已检查**原始输入的裁切选择**；AGH 对输出 PNG 未完成可靠读图，用户/Codex 输出对照审查待做。引用 `../../reference_vs_v01_local.png` 与 `../../pair_18_local.png`。
- 拆解层和旁侧组装四单元为展示态，不将爆炸间隙判功能接触；首次画外 FAIL 经相机修复，初始报告保留。
- v01 仅整体草稿；不得称装置、功能或论文图验收。
