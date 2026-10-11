# 15 retractable_sensor｜AGH v04 试用输出检查点

- Codex v03 **真实像素** R3 修改要求在 `../../CODEX_FEEDBACK_R3.md`；本例 v03 修正前配对图可能不是最终 v03 哈希，不能充当终版审查。v01/v02/v03 均保留。
- 本轮结构改变：局部色材改为烟灰透树脂、金属薄边，深色扁带盘簧；分层 lid/rotor/hub/stator 与贴壁金/暗条纹。拆解层间距不当成工作支撑。
- Blender 5.1.2：`build_v04.py` 成功并落盘 `scene_v04.blend` + 无字 `overview_v04.png`；820×1070，sha256 `307f788bf15f384b3c45d6e4b78306a760938e42f6c649e0610b98188015eb76`。
- 静态 `record_static_v04.json/.log` UNKNOWN exit 3；独立重开场景 `audit_scene_v04.json/.log` UNVERIFIED exit 3，FAIL 0；PNG `review_numeric_v04.json/.log` NUMERIC_ONLY exit 0。
- 源可见且**声明过**的物理线段 0；端点近接 0/0 PASS；接口 mesh 所属表面 0/0 PASS。样本世界单位容差 owner 0.09 / route 0.08；不是工程公差，未列的线段无分母。
- 最新本地参考–预览配对 `../../pair_15_latest_v03_v04_local.png`；v04 输出像素尚待 Codex/用户阅读，统计或 mesh 的 PASS 不是可读性或论文复刻验收。
- 未核：内部介质/力学/流体或信号功能、像素遮挡、完整原图观感与设备厂家 CAD。
- 拆解无工作态连接，不要为审核制造工作接触/支撑；材质色是展示试选，非论文材料配方。
