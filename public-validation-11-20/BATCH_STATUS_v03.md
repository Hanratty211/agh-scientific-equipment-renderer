# 公开图 11–20｜Codex R2 → AGH v03 低成本批次

Codex 实际打开十幅 v02 源图/输出对，按用户本轮 R2 要求全数修订；**v03 输出像素尚未由 Codex 或用户阅读/接受**。此批不改 Skill v0.6，不做正式渲染，不复用原 Scientific-System-Renderer 代码。Codex 负责来源图/前轮像素反馈；AGH 负责本轮 scene/PNG/记录/审计。所有论文原图与输出大件留本地。

| ID | R2 结构矫正 | 声明/端点通过的**可见**线路 | v0.6 静态 / 独立场景 / 数值图片（退出码） | 仍待外审 |
|---|---|---:|---|---|
| 11 | HWP–BS–HWP 顺序、二色镜 XZ 面、上下轴接通 | 10 / 10 | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | actual optical face/reflection limited audit dot 1.0；整图光学尺度/外观未审 |
| 12 | 废液真开口 rim、笔电、双泵真实 syringe 属主 | 3 / 3 | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 封口和液路内部仍未知 |
| 13 | 悬空排放屏/传感器加支架，开敞打印框和头部 U 环 | 0 / 0 | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 电/信号路径未核，不把电线不明解释为无连接 |
| 14 | 下部矩形反射板、斜麦克风及外机身/功放线、笔电 | 0 / 0 | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 探针/电缆端点及阵列确切排布未核 |
| 15 | 同一平面矩形带盘簧、树脂薄壁/贴壁条带 | 0 / 0 | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 拆解展示，不应虚构工作连接；材料观感未审 |
| 16 | 外部左 DC、红机导轨、针支撑、圆柱加热/侧 IR | 2 / 2 | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 仅红绿外露电缆两段，箱内 HV 与沉积不证 |
| 17 | 顶部开架、两端气管到样品夹具/泵/传感器 | 2 / 2 | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 气动隐段/泵内部与磁场不证 |
| 18 | 1–17 分类层厚/正面实孔、实体端板螺孔/四单元重复 | 0 / 0 | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 拆解不强制路由；17 个中央 Y 射线实/空测试通过，整面与身份未证 |
| 19 | 单条 U 管下喷嘴、透明膜、两 socket 端点 | 2 / 2 | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 暗线/读出逻辑未知，不证明电流测量 |
| 20 | 窄竖 Peltier、内侧界面脂、双侧多电极 | 0 / 0 | UNKNOWN(3) / UNVERIFIED(3) / NUMERIC_ONLY(0) | 真实热接触/边缘导线功能未核 |

**支持路由的含义**：仅 11/12/16/17/19 五例对来源可见片段做了有限记录：20/6/4/3/4 个端口，10/3/2/2/2 条 route。实际 v0.6 独立读取最终 `.blend`，分项 owner 表面最近距离及 spline 两端距离均在**本例声明容差**内；world 单位是示意尺度，port 0.09 / route 0.08 不是通用公差，路由身份/功能还要核源。初次 12/17/19 审计因锚点离所有者真实面或废液段端点偏离而 FAIL，初始 JSON+log 留本地，修改真实锚位置/owner 后重建并审计，无缩范围、无调宽容差。其余未列路径是**未覆盖**；13/14/20 并非证明装置无电线/支架。15/18 分离层不当成工作连接。

**11 补充实际网格反射核查**：独立重开保存场景，用 evaluated 面法向测入射 -X 与反射 +Z，dot 1.0（`cases/11_optical_binding/reflection_audit_v03.json`，命令 exit 3，单项 PASS；未证其他光学传播）。**18 补充实际网格孔核查**：17 个位置各单条中央 Y 向 BVH 射线按模型声明实/空分类 17/17（`cases/18_electrochemical_stack/mesh_audit_v03.json`，exit 3；非孔道/密封全面检查），原图图注 16 一号多指与 15 不明保留 UNKNOWN。

**落盘**：每例 `build_v03.py`、`scene_v03.blend`、`overview_v03.png`、`record_v03.json`、`record_static_v03.json/.log`、`audit_scene_v03.json/.log`、`route_coverage_v03.json`、`review_config_v03.json`、`review_numeric_v03.json/.log`、局部 `qa_center_v03.png`、`qa_numeric_sheet_v03.png`、`V03_CHECKPOINT.md`、更新后的 `CHECKPOINT.md`。全批 `reference_v01_v02_v03_contact_local.png`（1800×3500）与逐例 `pair_11_v01_v02_v03_local.png` 至 `pair_20_v01_v02_v03_local.png` 待 Codex/用户实际读图。临时 `.blend1` 非本版交付，不同步。
