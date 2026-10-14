# 20_thermal｜低成本示意预览检查点（未验收）

DOI: https://doi.org/10.1038/s41467-025-56960-1。日期 2025-02-17（Crossref）。依据：Materials PDF p.11 铝塑壳与铜网芯；Fig.1c仅后版核形态；图/正文中文解释：铝塑壳和三维铜网芯做剖切。类别 D，指定完整范围：可编辑剖切柔性 AHP 的铝塑封装与铜网芯、两端换热面。

当前场景 `v01/scene.blend` / `v01/overview.png`；最新版 `v01`。构建脚本 `../../build_cases.py`、`../../build_more.py`、`../../render_core.py`；修订使用 `../../revise_cases.py`。Blender 5.1.2 EEVEE，900×640；独立进程重开 scene 并在该版本目录生成 `render_report.json`，存两 SHA256。v01 scene `df585ee2e775986d9e1aec7e62fce56905fc954c82421dfc2f2c45393ab1dd08`；PNG `d24ecd05cc2c1b7b872b440782a57e25ec0f173d2e9b88d09a8602a6e420f8e9`。这不证明像素、物理或装配。

主要三项差异：铜网层数猜测；直条非图示曲线；端部密封未知。建模假设：所有相对比例/尺寸/背景；未见的接口和内部结构不能按场景推为论文事实。开放未知：文字首版不使用图版测量路径、密封及内流动保持未知。本版变化：仅 v01 首版，未伪造失败后的 v02。人工优先核验：壳体封边和芯材形态，内流路不验。实际审阅：AGH 批次拼图捕获 3378，粗看而非逐例高清；其余无逐例 PNG 专项读图。外部模型未审，人工未审。

|检查点|来源位置|输出位置|证据类型|结论|待人工确认|
|---|---|---|---|---|---|
|范围与身份|Materials PDF p.11 铝塑壳与铜网芯；Fig.1c仅后版核形态|`v01/overview.png`|论文图/正文 + AGH 粗看|示意阶段/未验收|壳体封边和芯材形态，内流路不验|
|可见线路/装配|Materials PDF p.11 铝塑壳与铜网芯；Fig.1c仅后版核形态|`v01/scene.blend`|有限网格+渲染|未完成实端口逐跳验证|开孔、接头、遮挡及支撑|
|图像外观|见本地 `../../demo-assets/20_thermal/source/SOURCE.md`|`v01/overview.png`|AGH 实际读批次拼图|不作通过声明|对应实物形态|

## 外部人工复核后的非破坏候选版（尚未验收）
外部人工逐例读源依据与旧版 PNG 后指出的差异详见 `../../EXTERNAL_HUMAN_REVIEW.md`（审阅者：外部复核，目视，**针对旧版**）。新 `v02` 保存于 [`v02/scene.blend`](v02/scene.blend)、[`v02/overview.png`](v02/overview.png)，独立 Blender 进程重载并渲染。针对性修改：膜壳最终四边封+准备态三边封/预充液剖视分开；内循环只示意。绝对尺寸、比例、不可见接口与内部机理仍为建模假设/开放未知。 scene SHA256 `5ccebe9f87233318e1e60798a57be66ca65dbddb51e5234077082574a77f8fdf`；PNG SHA256 `2537e7bc8f69bbbd8a0b580ec70cd3255c63c228c19ee98d2d5ee14107cb2484`。**新图 AGH 未能 capture（apps discovery failed），也尚无新版本外部人工或用户验收；重载成功/几何项 PASS 不等于目视通过。**来源锚点在 `../../demo-assets/20_thermal/source/SOURCE.md`，本地含原图画布 `../../demo-assets/20_thermal/new_source_v01_v02_LOCAL.png` 不提交。 另有同源几何的 `v02_preseal_detail/scene.blend` 与 PNG 表示未封第四边的工艺状态，最终封装主览仍为 v02。

### 第二轮外部复核后：`v03` 候选（旧版不覆盖）
外部复核实际逐张目视旧 `v02` 后判失败；具体差异见 `../../EXTERNAL_HUMAN_REVIEW.md`，几何旧检查另列，不能跨版外推。`../../revise_connectivity_stage4.py` 从保存的 `v02/scene.blend` 另存 `v03/scene.blend`；**独立 Blender 进程重新打开**并写出 `v03/overview.png`。场景 SHA256 `d6cdf25c34a04b039eea1577511b23158bffa736894a309bac3c5e1ed3b7862c`；PNG SHA256 `c339f737dcbfe8fc9850e3dbbfd297832070ee99e716c06ae76ba6e3576af38b`。目标结构检查 `v03/target_audit.json` 4 项零 FAIL（作用面/身份局部检查）；它不验可视清晰、机械/光电功能。审阅者：AGH 对脚本与有限结构核查；**新图 AGH 读图服务失败，外部复核新版本待审**。本地源—被审旧版—新图画布 `../../demo-assets/20_thermal/stage4_source_v02_v03_LOCAL.png` 不提交。相关尺寸、材料外观、不可见连接/载荷/密封仍是未知或假设。
最终封装的薄箔折边为可编辑薄壳示意，实物弯曲半径未知；原 `v02_preseal_detail` 仍独立制造过程态，不作最终态。

### 第三轮外部复核后 `v04` 独立候选（不自动验收）
旧 `v03` 被**外部复核**实际逐张读图的判词在 `../../EXTERNAL_HUMAN_REVIEW.md` 第三表。候选文件 [`v04/scene.blend`](v04/scene.blend)、[`v04/overview.png`](v04/overview.png)，由另一 Blender 进程重开已保存场景后渲染。scene SHA `0ef4922e03fbd0d08213539f61c433700f4ec1c9b5ea2ea658fa3115b4838d2e`；PNG SHA `c40b0e9212ab2e0e7db924cec45dc2f4b03948a6d94181a5405936fecf920d2f`。`v04/target_audit.json` 仅审核 4 项可见对象/网格端点，FAIL=[]；非视觉/密封/强度/光电功能证据。**AGH GUI 读取失败，新版无人再次目视，外部复核待审**。本地含原图三栏 `../../demo-assets/20_thermal/stage5_source_v03_v04_LOCAL.png` 不提交。
v04 最终态新增右端物理箔膜封面及折边；能否目视完全遮住铜网尚未可视复核，`v02_preseal_detail` 原过程态单独保留。
