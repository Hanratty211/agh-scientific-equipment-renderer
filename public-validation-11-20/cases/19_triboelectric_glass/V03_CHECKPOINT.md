# 19 triboelectric_glass v03｜R2 外部像素纠偏之后的 AGH 执行记录

- 外部审查来源：Codex 实际阅读 v02 的 `../../codex-review/pair_19_v02.png`，要求 v03；不是用户验收，也不是 AGH 自己已读 v03。原用户 panel/scope 保留于 `record_v03.json.task.scope`。
- 实际改动：U 调节管改为连续尾端朝下并对齐可见单滴；薄膜改半透明，双输出止于两仪器侧面 socket，不停在屏上；玻璃旋转后锚点初次偏离真实面，拒绝、移动锚点、重审。
- Blender 5.1.2 低成本输出：`build_v03.py`, `scene_v03.blend`, `overview_v03.png`，1100×800，SHA256 `ea6f3848cf9f7541707d55c375ffb20ef83225b7ccd8d0a1ccb128dd5d451fb0`；v01/v02 不覆盖。原版出版方 PNG/本例输出 scene/PNG/raw logs 全部留本地。
- v0.6 静态 `record_static_v03.json/.log`：UNKNOWN (exit 3)；独立重开磁盘场景 `audit_scene_v03.json/.log`：UNVERIFIED (exit 3), failures 0, unverified 19。图数值 `review_numeric_v03.json/.log`：NUMERIC_ONLY (exit 0)。
- 当前声明的可证路线 2 条：owner 最近面 4/4 分项 PASS；实际曲线端点 2/2 分项 PASS。**非全任务路径数、非画面遮挡/物理输运通过**；没声明的连接不在分母。容差为本场景展示世界单位 owner 0.09/端点 0.08，不能挪作通用物理配合公差。
- v03 输出视觉审查者：未完成，等 Codex/用户读 `../../pair_19_v01_v02_v03_local.png`。自动通过不能取代图版相似、真实界面/隐藏拓扑、热流体物理或工程 CAD。
- 首轮 audit_scene_v03_initial.json/.log 保留了界面 owner/端点拒绝证据；只在核对真实网格最近面后改对应锚点/owner，再独立运行审计，没有通过调宽容差或缩 required 绕过。
