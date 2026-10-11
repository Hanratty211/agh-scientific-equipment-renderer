# 14 acoustic_levitation｜AGH v04 试用输出检查点

- Codex v03 **真实像素** R3 修改要求在 `../../CODEX_FEEDBACK_R3.md`；本例 v03 修正前配对图可能不是最终 v03 哈希，不能充当终版审查。v01/v02/v03 均保留。
- 本轮结构改变：相机改左、LED 改右，探针加大且前移，斜杆可见并以可见线接功放；显示器不伪造声波曲线；3 条声明线路的几何端点分别查。
- Blender 5.1.2：`build_v04.py` 成功并落盘 `scene_v04.blend` + 无字 `overview_v04.png`；1140×830，sha256 `84647b1240de75dbc8a0b6386157938508b669640ee58cd65ec8b97558966f38`。
- 静态 `record_static_v04.json/.log` UNKNOWN exit 3；独立重开场景 `audit_scene_v04.json/.log` UNVERIFIED exit 3，FAIL 0；PNG `review_numeric_v04.json/.log` NUMERIC_ONLY exit 0。
- 源可见且**声明过**的物理线段 3；端点近接 3/3 PASS；接口 mesh 所属表面 6/6 PASS。样本世界单位容差 owner 0.09 / route 0.08；不是工程公差，未列的线段无分母。
- 最新本地参考–预览配对 `../../pair_14_latest_v03_v04_local.png`；v04 输出像素尚待 Codex/用户阅读，统计或 mesh 的 PASS 不是可读性或论文复刻验收。
- 未核：内部介质/力学/流体或信号功能、像素遮挡、完整原图观感与设备厂家 CAD。

- 为防 0.070 世界单位的 array 内部假锚点被 .09 容差掩盖，将其从 top holder 体内移至真实顶面 z=2.745，不改变容差；重建后网格面最近距离 0.0050001 世界单位。旧审计 `audit_scene_v04_pre_surface.json/.log` 留档。
