# 11 optical_binding v03｜R2 外部像素纠偏之后的 AGH 执行记录

- 外部审查来源：Codex 实际阅读 v02 的 `../../codex-review/pair_11_v02.png`，要求 v03；不是用户验收，也不是 AGH 自己已读 v03。原用户 panel/scope 保留于 `record_v03.json.task.scope`。
- 实际改动：将 BS 放在两 HWP 之间，二色镜从 XY 改为 XZ 入射面，接通水平/竖直下成像路径；基于保存 mesh 面法向检查入射 -X 与反射 +Z。只审声明的 10 条可见轴段，非完整物理光路。
- Blender 5.1.2 低成本输出：`build_v03.py`, `scene_v03.blend`, `overview_v03.png`，1000×820，SHA256 `a1122732071a7a301abff3a32269abf703cc7f7e723c79fee6f8aa89dbcb72a6`；v01/v02 不覆盖。原版出版方 PNG/本例输出 scene/PNG/raw logs 全部留本地。
- v0.6 静态 `record_static_v03.json/.log`：UNKNOWN (exit 3)；独立重开磁盘场景 `audit_scene_v03.json/.log`：UNVERIFIED (exit 3), failures 0, unverified 46。图数值 `review_numeric_v03.json/.log`：NUMERIC_ONLY (exit 0)。
- 当前声明的可证路线 10 条：owner 最近面 20/20 分项 PASS；实际曲线端点 10/10 分项 PASS。**非全任务路径数、非画面遮挡/物理输运通过**；没声明的连接不在分母。容差为本场景展示世界单位 owner 0.09/端点 0.08，不能挪作通用物理配合公差。
- v03 输出视觉审查者：未完成，等 Codex/用户读 `../../pair_11_v01_v02_v03_local.png`。自动通过不能取代图版相似、真实界面/隐藏拓扑、热流体物理或工程 CAD。
- 额外 `reflection_audit_v03.json/.log`：实际 evaluated dichroic 网格面法向反射中心轴 dot=1.0，exit 3（光学其余物理/输出视觉未证）。
