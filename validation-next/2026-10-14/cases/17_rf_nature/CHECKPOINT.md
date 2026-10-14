# 17_rf_nature｜低成本示意预览检查点（未验收）

DOI: https://doi.org/10.1038/s41598-026-39831-7。日期 2026-02-13。依据：Fig. 1a–d，PDF p.4，馈线/双椭圆槽/辐射体；图/正文中文解释：锥台/圆环介质辐射体、接地板双椭圆槽、馈线。类别 A，指定完整范围：完整辐射体、接地板真实椭圆槽、馈线与基座。

当前场景 `v01/scene.blend` / `v01/overview.png`；最新版 `v01`。构建脚本 `../../build_cases.py`、`../../build_more.py`、`../../render_core.py`；修订使用 `../../revise_cases.py`。Blender 5.1.2 EEVEE，900×640；独立进程重开 scene 并在该版本目录生成 `render_report.json`，存两 SHA256。v01 scene `bfe3f33471c5433b01515d3a2f1c8769a9ca91f2f0920c3ac1f69a48706a5730`；PNG `dae806373087d1d77f10ca03ec9d7d6f3fb0f4a346681e502acd99c8005ecdf1`。这不证明像素、物理或装配。

主要三项差异：透明本体过淡；槽比例待图；馈电物理接点未知。建模假设：所有相对比例/尺寸/背景；未见的接口和内部结构不能按场景推为论文事实。开放未知：槽/馈线几何代表性，电性能不验。本版变化：仅 v01 首版，未伪造失败后的 v02。人工优先核验：双槽真实开孔、馈电接触与图注配对。实际审阅：AGH 批次拼图捕获 3378，粗看而非逐例高清；其余无逐例 PNG 专项读图。外部模型未审，人工未审。

|检查点|来源位置|输出位置|证据类型|结论|待人工确认|
|---|---|---|---|---|---|
|范围与身份|Fig. 1a–d，PDF p.4，馈线/双椭圆槽/辐射体|`v01/overview.png`|论文图/正文 + AGH 粗看|示意阶段/未验收|双槽真实开孔、馈电接触与图注配对|
|可见线路/装配|Fig. 1a–d，PDF p.4，馈线/双椭圆槽/辐射体|`v01/scene.blend`|有限网格+渲染|未完成实端口逐跳验证|开孔、接头、遮挡及支撑|
|图像外观|见本地 `../../demo-assets/17_rf_nature/source/SOURCE.md`|`v01/overview.png`|AGH 实际读批次拼图|不作通过声明|对应实物形态|

## 外部人工复核后的非破坏候选版（尚未验收）
外部人工逐例读源依据与旧版 PNG 后指出的差异详见 `../../EXTERNAL_HUMAN_REVIEW.md`（审阅者：外部复核，目视，**针对旧版**）。新 `v02` 保存于 [`v02/scene.blend`](v02/scene.blend)、[`v02/overview.png`](v02/overview.png)，独立 Blender 进程重载并渲染。针对性修改：近贴主基板辐射体与馈线触点，保留真实椭圆槽；导电匹配未证。绝对尺寸、比例、不可见接口与内部机理仍为建模假设/开放未知。 scene SHA256 `10b3878521df901447d9eb3475229f9a0628a96fe5abb0ac373bbc1ef8208851`；PNG SHA256 `8912513d08439448035b48399bc95ac6c99c3429a268f751ea8493724272cf2f`。**新图 AGH 未能 capture（apps discovery failed），也尚无新版本外部人工或用户验收；重载成功/几何项 PASS 不等于目视通过。**来源锚点在 `../../demo-assets/17_rf_nature/source/SOURCE.md`，本地含原图画布 `../../demo-assets/17_rf_nature/new_source_v01_v02_LOCAL.png` 不提交。

### 第二轮外部复核后：`v03` 候选（旧版不覆盖）
外部复核实际逐张目视旧 `v02` 后判失败；具体差异见 `../../EXTERNAL_HUMAN_REVIEW.md`，几何旧检查另列，不能跨版外推。`../../revise_connectivity_stage4.py` 从保存的 `v02/scene.blend` 另存 `v03/scene.blend`；**独立 Blender 进程重新打开**并写出 `v03/overview.png`。场景 SHA256 `e58495116ea62f8f880dcb9ec4cab15e9fd57f34f48b455781b42e6b1813779a`；PNG SHA256 `b66c011a53de07c58c5ddee27ac05a3ced92104d8ef76b818f67d743b36ba557`。目标结构检查 `v03/target_audit.json` 5 项零 FAIL（作用面/身份局部检查）；它不验可视清晰、机械/光电功能。审阅者：AGH 对脚本与有限结构核查；**新图 AGH 读图服务失败，外部复核新版本待审**。本地源—被审旧版—新图画布 `../../demo-assets/17_rf_nature/stage4_source_v02_v03_LOCAL.png` 不提交。相关尺寸、材料外观、不可见连接/载荷/密封仍是未知或假设。
Fig.1a–d 表示基板与接地层是有层次的：本轮按同一 laminate 接触而非把有据两材料强合成同材；馈线铜迹线只作示意，RF 匹配未知。

### 第三轮外部复核：保留 `v03` 候选，不扩范围
审阅者：**外部复核**，实际逐张看当前源图/渲染，意见见 `../../EXTERNAL_HUMAN_REVIEW.md` 第三表；该版尚未最终验收。本轮不改模型、不重渲旧版。独立本地三栏 `../../demo-assets/17_rf_nature/stage5_source_v02_v03_LOCAL.png` 仅供本地复核。有限结构 QA 不构成视觉通过。
