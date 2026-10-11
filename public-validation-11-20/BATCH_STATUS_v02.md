# 11–20 批次｜v02 R1 结构修订状态

审查基线：Codex 2026-10-12 实际打开十组 v01 源图/输出 PNG，全部 **requires revision**；原文 `CODEX_FEEDBACK_R1.md`。AGH 按具体观察批量重建十例 v02，保留 v01。**本次 v02 PNG 尚无 Codex/用户外部像素评价**，不能宣称阶段认可或十例通过。源图收集/裁选属 Codex 输入工作，模型脚本/scene/QA 属 AGH 本轮执行。

| ID | v02 结构变更要点 | v02 输出与日志 | 静态 / 独立场景 / PNG 数值（真实退出码） | 待审 |
|---|---|---|---|---|
| 11 | 右侧激光与功率控组；二色镜处转向上下公共支路，上卤素/暗场/样品/物镜，下滤镜/镜片/sCMOS | `cases/11_optical_binding/` | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 光学面与束真正作用/偏转 |
| 12 | 左上/左下泵双入口、同轴摄像与倒置显微、独立封闭冲洗支和废液端 | `cases/12_capillary_microfluidics/` | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 透明端口/真实流路、密封 |
| 13 | 摄影式银色正面框/黑内舱、红头环线、排放屏/前传感屏/笔电，无浮块 | `cases/13_fff_printer/` | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 照片外形/尺寸/控件比对 |
| 14 | 上方朝下阵列/下方反射板间隙，双侧摄影/灯、斜探针和三件读出 | `cases/14_acoustic_levitation/` | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 阵列确切排布与可见线 |
| 15 | 薄树脂拆解盖真孔、转/定子及竖向间隔条纹与平面盘簧 | `cases/15_retractable_sensor/` | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 条纹数示意/实物透明层 |
| 16 | 箱顶红色供液驱动、透明展示切面、双倾斜 Vee、加热与箱外电源 | `cases/16_electrospinning/` | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | Vee 遮挡/端口走向 |
| 17 | 四柱框、上下线圈、夹具上半球、左右设备及可见管 | `cases/17_magnetic_shell/` | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 照片外形与气管边界 |
| 18 | 1–17 显示序列含 12–14 单元组；Y 方向真开口、差别层厚、四单元端板拉杆 | `cases/18_electrochemical_stack/` | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 15 未明、16 编号冲突，实孔/重复结构要目视 |
| 19 | 倾斜玻璃、抬升贮液/U 形管、喷嘴与电阻替代器/示波器分开 | `cases/19_triboelectric_glass/` | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 器件身份/引线走向 |
| 20 | 两块 Cu/内侧界面脂/窄桥样品/双边电极，下方 Peltier；删多余表盒 | `cases/20_thermoelectric_measurement/` | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 接触/双边电极布置 |

**每例落盘**：`build_v02.py`、`scene_v02.blend`、`overview_v02.png`、`record_v02.json`、`record_static_v02.json/.log`、`audit_scene_v02.json/.log`、`review_config_v02.json`、`review_numeric_v02.json/.log`、`qa_center_v02.png`、`qa_numeric_sheet_v02.png`、`V02_CHECKPOINT.md` 和原 `CHECKPOINT.md` 的更新。批次完整对照 `reference_v01_v02_contact_local.png`（1350×3450），逐例 `pair_11_v01_v02_local.png` … `pair_20_v01_v02_local.png`。脚本/轻量报告入 Git，源图/PNG/.blend/日志留本地。

**覆盖边界**：十例 `record_v02.json` 的必需组件由原范围与 R1 源图纠偏选择，均有模型对象且自动投影未报 FAIL。但所有 `ports=connections=supports=0`，静态为 UNKNOWN；这**不是**原用户要求的完整接口/路径审核，也不是物理错误判定。复杂光学转向、流体封口、真实装配承载/热接触、渲染透明材质和外形相似均未被工具证实；应基于 Codex v02 输出像素反馈再针对性修订，必要时补来源可确认的 port-to-port 记录，而不是稀释 required。15/18 是展示拆解，不强求工作接触。Skill 本轮保持 v0.6，不声称跨案例方法已验证。
