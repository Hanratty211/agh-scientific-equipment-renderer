# 04_microfluidics｜低成本示意预览检查点（未验收）

DOI: https://doi.org/10.1038/s41526-025-00470-3。日期 2025-05-06。依据：Fig. 3C，PDF p.4，面板安装注射器至芯片；Fig.3A仅核外形；图/正文中文解释：五路注射器与芯片右侧入口和左侧绿色出口/气囊（以 Fig.3C 图注为准）。类别 B，指定完整范围：Fig.3C 的五支注射器架、芯片、右侧五条外管与左侧绿色出口/储液段。

当前场景 `v01/scene.blend` / `v01/overview.png`；最新版 `v05`（外部端点审核零 FAIL，**新 PNG 尚未实际读图，非验收**）。构建脚本 `../../build_cases.py`、`../../build_more.py`、`../../render_core.py`；修订使用 `../../revise_cases.py` / `../../revise_micro_v04.py` / `../../revise_micro_v05.py`。Blender 5.1.2 EEVEE，900×640；独立进程重开 scene 并在该版本目录生成 `render_report.json`，存两 SHA256。v01 scene `18999ba90b2a7ce18cac3c6b4061aea55d2974fb4007416312d9224c60e1c293`；PNG `e382f344bf06fdbe90113b0718b5633b7406bb63d54c04adb3ce20a4318ae186`。这不证明像素、物理或装配。

主要三项差异：v01 浮环假孔；v02 管线悬起；左侧气囊缺失。建模假设：所有相对比例/尺寸/背景；未见的接口和内部结构不能按场景推为论文事实。开放未知：示意图非密封结构；正文支持五个流路，未证内部回流。本版变化：v02 修后回退，v03 添加左侧储液筒仍有断连；v04 独立检查暴露五路注射器起点皆断，v05 修端点；严格结论见 `../../REVISIONS_04_15.md` 与 `../../REVISIONS_04_V04_V05.md`，v05 图像未实读。人工优先核验：每路入口实际是否入孔、管线连接及芯片装配。实际审阅：AGH 批次拼图捕获 3378，粗看而非逐例高清；单独 capture 3223/3533。外部模型未审，人工未审。

|检查点|来源位置|输出位置|证据类型|结论|待人工确认|
|---|---|---|---|---|---|
|范围与身份|Fig. 3C，PDF p.4，面板安装注射器至芯片；Fig.3A仅核外形|`v01/overview.png`|论文图/正文 + AGH 粗看|示意阶段/未验收|每路入口实际是否入孔、管线连接及芯片装配|
|可见线路/装配|Fig. 3C，PDF p.4，面板安装注射器至芯片；Fig.3A仅核外形|`v01/scene.blend`|有限网格+渲染|未完成实端口逐跳验证|开孔、接头、遮挡及支撑|
|图像外观|见本地 `../../demo-assets/04_microfluidics/source/SOURCE.md`|`v01/overview.png`|AGH 实际读批次拼图|不作通过声明|对应实物形态|

最新独立重载版本 `v05`：[`scene.blend`](v05/scene.blend) SHA256 `0c04967e4a8e4ebe7ca8619731f805bda66eac3e8cbe2ff8a86f18c2c5ed1dcb`；[`overview.png`](v05/overview.png) SHA256 `030be22f931483b2cbc5ff1110a2dd5b793856b740a243225e0bb0a30c1d2904`。本轮图像访问故障，AGH 尚未读此版像素；不作视觉通过声明。

## 外部人工复核后的非破坏候选版（尚未验收）
外部人工逐例读源依据与旧版 PNG 后指出的差异详见 `../../EXTERNAL_HUMAN_REVIEW.md`（审阅者：外部复核，目视，**针对旧版**）。新 `v06` 保存于 [`v06/scene.blend`](v06/scene.blend)、[`v06/overview.png`](v06/overview.png)，独立 Blender 进程重载并渲染。针对性修改：五路蓝软管接注射器外端及芯片两侧外接头，左五路绿 balloon 扩展；无实孔/内流/气密。绝对尺寸、比例、不可见接口与内部机理仍为建模假设/开放未知。 scene SHA256 `3c74e24c6a8f0854ccc8647b47af415105a3eb7fd067c647765629d004624229`；PNG SHA256 `88dc7e90184b07490e9bd12adec1e4c264e2b18a091aaee79e62cf8d67824199`。**新图 AGH 未能 capture（apps discovery failed），也尚无新版本外部人工或用户验收；重载成功/几何项 PASS 不等于目视通过。**来源锚点在 `../../demo-assets/04_microfluidics/source/SOURCE.md`，本地含原图画布 `../../demo-assets/04_microfluidics/new_source_v01_v06_LOCAL.png` 不提交。

### 第二轮外部复核
审阅者：**外部复核**，逐张核 Fig.3C 和 v06，反馈五条蓝管—芯片—左绿囊关系“大体可读”，但要求逐路看每端是否落可辨接头/囊口；**只留候选，目视未通过、实孔/流体功能未知**。本轮不改 v06、不伪造 v07。源图—v01—v06 新本地画布 `../../demo-assets/04_microfluidics/stage4_source_v01_v06_LOCAL.png`；有限外部几何报告仍是 `v06/boundary_audit.json` 40 项零 FAIL，非视觉。
