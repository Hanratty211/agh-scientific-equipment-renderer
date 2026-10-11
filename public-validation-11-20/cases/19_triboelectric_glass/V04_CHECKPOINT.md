# 19 triboelectric_glass｜AGH v04 试用输出检查点

- Codex v03 **真实像素** R3 修改要求在 `../../CODEX_FEEDBACK_R3.md`；本例 v03 修正前配对图可能不是最终 v03 哈希，不能充当终版审查。v01/v02/v03 均保留。
- 本轮结构改变：膜本地左右点经 film.matrix_world 转换为实际斜面的 lead 起点；半透 film 有细边，极小黑标示而无悬空金块；左右两条可见线止于两仪器侧面。
- Blender 5.1.2：`build_v04.py` 成功并落盘 `scene_v04.blend` + 无字 `overview_v04.png`；1100×800，sha256 `b48401e5c216fb8363868b4e323203a3853daf0f3fc8b8895bb81ef6306efc9c`。
- 静态 `record_static_v04.json/.log` UNKNOWN exit 3；独立重开场景 `audit_scene_v04.json/.log` UNVERIFIED exit 3，FAIL 0；PNG `review_numeric_v04.json/.log` NUMERIC_ONLY exit 0。
- 源可见且**声明过**的物理线段 2；端点近接 2/2 PASS；接口 mesh 所属表面 4/4 PASS。样本世界单位容差 owner 0.09 / route 0.08；不是工程公差，未列的线段无分母。
- 最新本地参考–预览配对 `../../pair_19_latest_v03_v04_local.png`；v04 输出像素尚待 Codex/用户阅读，统计或 mesh 的 PASS 不是可读性或论文复刻验收。
- 未核：内部介质/力学/流体或信号功能、像素遮挡、完整原图观感与设备厂家 CAD。
- 首轮 v04 hidden QA marker 导致 PORT_RENDER FAIL，保留 `audit_scene_v04_initial.json/.log`，改极小真实膜表面 marker；另 `leads_audit_v04.json/.log` 在 saved scene 检查 film 最近面，两端间距 ~8.43e−8 / 3.73e−9 世界单位，exit 3（信号功能仍未知）。
