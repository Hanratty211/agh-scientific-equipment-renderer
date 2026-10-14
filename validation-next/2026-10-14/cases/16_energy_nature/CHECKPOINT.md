# 16_energy_nature｜低成本示意预览检查点（未验收）

DOI: https://doi.org/10.1038/s41467-025-64306-0。日期 2025-10-17。依据：Methods PDF p.9 段落（每次单程蠕动泵供液）；Fig.1b仅后版核系统逻辑；图/正文中文解释：Methods 单程蠕动泵供液至电解池。类别 D，指定完整范围：单程泵→反应池→出口的外部有据链与双电极示意主体。

当前场景 `v01/scene.blend` / `v01/overview.png`；最新版 `v01`。构建脚本 `../../build_cases.py`、`../../build_more.py`、`../../render_core.py`；修订使用 `../../revise_cases.py`。Blender 5.1.2 EEVEE，900×640；独立进程重开 scene 并在该版本目录生成 `render_report.json`，存两 SHA256。v01 scene `4a79d782ec85802c115c004a19bc82a5594d3e48b895946ba9a3430cd16b1814`；PNG `c5e1b15c089f5d73e4d224bc2009f9ebeb03b23be561705fcc127f36e3b7f240`。这不证明像素、物理或装配。

主要三项差异：容器系假设；接头浮环；流池双电极内部未知。建模假设：所有相对比例/尺寸/背景；未见的接口和内部结构不能按场景推为论文事实。开放未知：具体流通池几何与内部回路未知；后续引图需另版。本版变化：仅 v01 首版，未伪造失败后的 v02。人工优先核验：泵口、流池进出及 MFC 不得假称已建。实际审阅：AGH 批次拼图捕获 3378，粗看而非逐例高清；其余无逐例 PNG 专项读图。外部模型未审，人工未审。

|检查点|来源位置|输出位置|证据类型|结论|待人工确认|
|---|---|---|---|---|---|
|范围与身份|Methods PDF p.9 段落（每次单程蠕动泵供液）；Fig.1b仅后版核系统逻辑|`v01/overview.png`|论文图/正文 + AGH 粗看|示意阶段/未验收|泵口、流池进出及 MFC 不得假称已建|
|可见线路/装配|Methods PDF p.9 段落（每次单程蠕动泵供液）；Fig.1b仅后版核系统逻辑|`v01/scene.blend`|有限网格+渲染|未完成实端口逐跳验证|开孔、接头、遮挡及支撑|
|图像外观|见本地 `../../demo-assets/16_energy_nature/source/SOURCE.md`|`v01/overview.png`|AGH 实际读批次拼图|不作通过声明|对应实物形态|

## 外部人工复核后的非破坏候选版（尚未验收）
外部人工逐例读源依据与旧版 PNG 后指出的差异详见 `../../EXTERNAL_HUMAN_REVIEW.md`（审阅者：外部复核，目视，**针对旧版**）。新 `v02` 保存于 [`v02/scene.blend`](v02/scene.blend)、[`v02/overview.png`](v02/overview.png)，独立 Blender 进程重载并渲染。针对性修改：去无据两杯、液泵外路线；CO2和Ar各自 MFC 和背面气端；进料源容器未画。绝对尺寸、比例、不可见接口与内部机理仍为建模假设/开放未知。 scene SHA256 `bb101c3674b842b86e4af7cc2dd00f74f0dade4024e495b3eb02c0544c4264a5`；PNG SHA256 `46271489587e81e720a37c9d92db111d60dc3d6c6c3812bc962ede99628483a5`。**新图 AGH 未能 capture（apps discovery failed），也尚无新版本外部人工或用户验收；重载成功/几何项 PASS 不等于目视通过。**来源锚点在 `../../demo-assets/16_energy_nature/source/SOURCE.md`，本地含原图画布 `../../demo-assets/16_energy_nature/new_source_v01_v02_LOCAL.png` 不提交。

### 第二轮外部复核后：`v03` 候选（旧版不覆盖）
外部复核实际逐张目视旧 `v02` 后判失败；具体差异见 `../../EXTERNAL_HUMAN_REVIEW.md`，几何旧检查另列，不能跨版外推。`../../revise_connectivity_stage4.py` 从保存的 `v02/scene.blend` 另存 `v03/scene.blend`；**独立 Blender 进程重新打开**并写出 `v03/overview.png`。场景 SHA256 `9b0860620783b9605c341ccaf81d9aa8ecfcd9fc7d27d7017e41c4b859e1009e`；PNG SHA256 `3f255e5b8a2f6e91b48459c29056f7273a7f7fa7fbfda9f3ecd200c442b09329`。目标结构检查 `v03/target_audit.json` 8 项零 FAIL（作用面/身份局部检查）；它不验可视清晰、机械/光电功能。审阅者：AGH 对脚本与有限结构核查；**新图 AGH 读图服务失败，外部复核新版本待审**。本地源—被审旧版—新图画布 `../../demo-assets/16_energy_nature/stage4_source_v02_v03_LOCAL.png` 不提交。相关尺寸、材料外观、不可见连接/载荷/密封仍是未知或假设。
