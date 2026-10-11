# 18 electrochemical_stack｜AGH v04 试用输出检查点

- Codex v03 **真实像素** R3 修改要求在 `../../CODEX_FEEDBACK_R3.md`；本例 v03 修正前配对图可能不是最终 v03 哈希，不能充当终版审查。v01/v02/v03 均保留。
- 本轮结构改变：12–14 三个单元换为四边实框＋不同内层/肋纹/紧固件；右侧四单元各有内板/流纹，不把显示色当电极材料确证；15/16 图注矛盾保留。
- Blender 5.1.2：`build_v04.py` 成功并落盘 `scene_v04.blend` + 无字 `overview_v04.png`；1380×800，sha256 `110a6f300ce3dc18fd575f9b487cc8878568a39337c170a584712333005c5feb`。
- 静态 `record_static_v04.json/.log` UNKNOWN exit 3；独立重开场景 `audit_scene_v04.json/.log` UNVERIFIED exit 3，FAIL 0；PNG `review_numeric_v04.json/.log` NUMERIC_ONLY exit 0。
- 源可见且**声明过**的物理线段 0；端点近接 0/0 PASS；接口 mesh 所属表面 0/0 PASS。样本世界单位容差 owner 0.09 / route 0.08；不是工程公差，未列的线段无分母。
- 最新本地参考–预览配对 `../../pair_18_latest_v03_v04_local.png`；v04 输出像素尚待 Codex/用户阅读，统计或 mesh 的 PASS 不是可读性或论文复刻验收。
- 未核：内部介质/力学/流体或信号功能、像素遮挡、完整原图观感与设备厂家 CAD。
- `mesh_audit_v04.json/.log` 在已保存场景按声明 1–17 中心 Y 射线面孔类别/12–14 内板分项 17/17，总状态 UNVERIFIED exit 3。旧 v03 checker 误判及新 checker 首轮 None bug 的报告留档，不据此宣称整个流道/密封成立。
