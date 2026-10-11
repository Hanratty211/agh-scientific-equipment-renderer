# Public validation 11–20｜AGH v0.6 / v01 阶段总表

来源：`SOURCE_LEDGER.md` 与 `targets.json` 为 Codex 的出版方公开图页输入选取；AGH 已核 SHA/尺寸并读取图注，**不是 AGH 下载**。目标是各指定子图范围。`cases/*/build_v01.py` 是 AGH 本轮新写的展示性 Blender 脚本；场景、PNG、数值截图/拼图与原版图均留本地。低成本 v01 草图不是十例系统通过；用户/Codex 须实际对照读图。CLI 工具只检查声明项，尚未绑定真实端口/路径，不能把几何 PASS 或对象数当复刻验收。

| ID | v01 局部目录 | 场景/总览 | 静态/场景 (实际退出码) | PNG 数值 (退出码) | 仍未覆盖/视觉 |
|---|---|---|---|---|---|
| 11 光学绑定 | `cases/11_optical_binding` | `scene_v01.blend` / `overview_v01.png` | UNKNOWN(3) / UNVERIFIED(3) | NUMERIC_ONLY(0) | 光轴作用面/反射次序与原图、样品 inset 排除：待外审 |
| 12 毛细流控 | `cases/12_capillary_microfluidics` | 同名 v01 | UNKNOWN(3) / UNVERIFIED(3) | NUMERIC_ONLY(0) | 两泵与显微记录全装置已初建；密封分支/可见端口、流路未证 |
| 13 FFF 打印 | `cases/13_fff_printer` | 同名 v01 | UNKNOWN(3) / UNVERIFIED(3) | NUMERIC_ONLY(0) | 相片 frame/head/bed/display/sensors/laptop 比例、细部待外审 |
| 14 声悬浮 | `cases/14_acoustic_levitation` | 同名 v01 | UNKNOWN(3) / UNVERIFIED(3) | NUMERIC_ONLY(0) | 相向阵列/反射板/探针/读出已初建，驱动/声场未证 |
| 15 回缩传感器 | `cases/15_retractable_sensor` | 同名 v01 | UNKNOWN(3) / UNVERIFIED(3) | NUMERIC_ONLY(0) | 仅主左拆解；故意分层，不要求装配接触；弹簧/电极示意待外审 |
| 16 Vee-shield | `cases/16_electrospinning` | 同名 v01 | UNKNOWN(3) / UNVERIFIED(3) | NUMERIC_ONLY(0) | 仅 b；透明腔/供液与采集形状、实际 Vee 接口待外审 |
| 17 磁壳 | `cases/17_magnetic_shell` | 同名 v01 | UNKNOWN(3) / UNVERIFIED(3) | NUMERIC_ONLY(0) | 成对 coil、壳、泵、传感器、供电初建；未证电/气连接 |
| 18 四单元堆 | `cases/18_electrochemical_stack` | 同名 v01 | UNKNOWN(3) / UNVERIFIED(3) | NUMERIC_ONLY(0) | 按 Fig.6(c) 图注顺序初建；首次 VERTICAL 画外 FAIL 已调相机复查，无接触/循环验证 |
| 19 雨滴玻璃 | `cases/19_triboelectric_glass` | 同名 v01 | UNKNOWN(3) / UNVERIFIED(3) | NUMERIC_ONLY(0) | g 面倾斜玻璃/供滴/读出初建；隐藏电极路径未知 |
| 20 热电夹具 | `cases/20_thermoelectric_measurement` | 同名 v01 | UNKNOWN(3) / UNVERIFIED(3) | NUMERIC_ONLY(0) | Cu 块/脂/样品/电极/Peltier 初建；真实接触/测量线拓扑未证 |

**每例具体落盘**：`build_v01.py`、`scene_v01.blend`、`overview_v01.png`、`record_v01.json`、`CASE_NOTES.md`、`CHECKPOINT.md`、`build_v01.log`、`record_static_v01.json/.log`、`audit_scene_v01.json/.log`、`review_config_v01.json`、`review_numeric_v01.json/.log`、`qa_center_v01.png`、`qa_numeric_sheet_v01.png`。参考–v01 全批对照：`reference_vs_v01_local.png`（900×3380）；单行 `pair_11_local.png` 至 `pair_20_local.png`。按目标选的截图是**数值裁图而非视觉验收**；外部输出审查者：待 Codex / 用户。

**核查边界**：静态 UNKNOWN 意味着未声明可证 port/connection/support，不是物理错误；场景 UNVERIFIED 主要因路径/可见性未覆盖。案例 18 初次静态 UNKNOWN、场景 FAIL（`VERTICAL:c11`），原报告 `cases/18_electrochemical_stack/audit_scene_v01_initial.json/.log` 保留，调整相机后仅相机边界部分过，场景仍 UNVERIFIED。`record_v01.json` 的 `required_components` 是第一轮已建模组件清单，原用户全文仍记录在 `task.scope`，绝非全面覆盖或用户最终验收。可见端点的真实接口和来源方向需由输出读图者反馈再修 v02，不得借少列连接凑 PASS。
