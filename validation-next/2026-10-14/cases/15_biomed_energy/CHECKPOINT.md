# 15_biomed_energy｜低成本示意预览检查点（未验收）

DOI: https://doi.org/10.1038/s41467-025-60911-1。日期 2025-07-01。依据：Fig. 3a PDF p.5 图像、p.6 图注，穿戴传感器分层装配；图/正文中文解释：PV/PPG/BLE/双电池/fPCB/封装分层。类别 A，指定完整范围：PV、PPG、BLE、电池对、fPCB、硅胶封装分层。

当前场景 `v01/scene.blend` / `v01/overview.png`；最新版 `v03`（未实际读 PNG，不通过/未定）。构建脚本 `../../build_cases.py`、`../../build_more.py`、`../../render_core.py`；修订使用 `../../revise_cases.py`。Blender 5.1.2 EEVEE，900×640；独立进程重开 scene 并在该版本目录生成 `render_report.json`，存两 SHA256。v01 scene `0b15c95557a81d188afa00eb25dc9b21a9211ee86862f24adba935dd8e8198ab`；PNG `d33906727b50a4b820f02422d14d685d211d24c8c0b5539a09749b9abf999e68`。这不证明像素、物理或装配。

主要三项差异：v01 顶封装全挡 PV；v02 开窗后仍平板；电路假设多。建模假设：所有相对比例/尺寸/背景；未见的接口和内部结构不能按场景推为论文事实。开放未知：内部走线不凭空补。本版变化：v02 仅修受影响项；实际读图及不通过点见 `../../REVISIONS_04_15.md`。人工优先核验：开窗覆盖/电池端子/PPG作用面。实际审阅：AGH 批次拼图捕获 3378，粗看而非逐例高清；15 单独 capture 3586。外部模型未审，人工未审。

|检查点|来源位置|输出位置|证据类型|结论|待人工确认|
|---|---|---|---|---|---|
|范围与身份|Fig. 3a PDF p.5 图像、p.6 图注，穿戴传感器分层装配|`v01/overview.png`|论文图/正文 + AGH 粗看|示意阶段/未验收|开窗覆盖/电池端子/PPG作用面|
|可见线路/装配|Fig. 3a PDF p.5 图像、p.6 图注，穿戴传感器分层装配|`v01/scene.blend`|有限网格+渲染|未完成实端口逐跳验证|开孔、接头、遮挡及支撑|
|图像外观|见本地 `../../demo-assets/15_biomed_energy/source/SOURCE.md`|`v01/overview.png`|AGH 实际读批次拼图|不作通过声明|对应实物形态|

最新独立重载版本 `v03`：[`scene.blend`](v03/scene.blend) SHA256 `916c34984166b9f69ff2ac5105f1aba0020b24c7c0910922130a834e6000cd8d`；[`overview.png`](v03/overview.png) SHA256 `54dfb2959a90bb659ad4ab0044d4f3891a1f73421fc4fa606cd0f596761b89cf`。本轮图像访问故障，AGH 尚未读此版像素；不作视觉通过声明。

## 外部人工复核后的非破坏候选版（尚未验收）
外部人工逐例读源依据与旧版 PNG 后指出的差异详见 `../../EXTERNAL_HUMAN_REVIEW.md`（审阅者：外部复核，目视，**针对旧版**）。新 `v04` 保存于 [`v04/scene.blend`](v04/scene.blend)、[`v04/overview.png`](v04/overview.png)，独立 Blender 进程重载并渲染。针对性修改：统一贴片中心重排顶盖窗口/PV/双电池/fPCB/PL，多层爆炸支撑；电路未知。绝对尺寸、比例、不可见接口与内部机理仍为建模假设/开放未知。 scene SHA256 `6d41945250aa591eb2761a2fc2736618d62e31a10e2e1fd43eec775b82842619`；PNG SHA256 `f38aaa4204b4bb844c4786782e2443510e8e317aa7a416b9d4c575bd7034c03d`。**新图 AGH 未能 capture（apps discovery failed），也尚无新版本外部人工或用户验收；重载成功/几何项 PASS 不等于目视通过。**来源锚点在 `../../demo-assets/15_biomed_energy/source/SOURCE.md`，本地含原图画布 `../../demo-assets/15_biomed_energy/new_source_v01_v04_LOCAL.png` 不提交。

### 第二轮外部复核后：`v05` 候选（旧版不覆盖）
外部复核实际逐张目视旧 `v04` 后判失败；具体差异见 `../../EXTERNAL_HUMAN_REVIEW.md`，几何旧检查另列，不能跨版外推。`../../revise_connectivity_stage4.py` 从保存的 `v04/scene.blend` 另存 `v05/scene.blend`；**独立 Blender 进程重新打开**并写出 `v05/overview.png`。场景 SHA256 `7450be7a390668fb5ef53fc88e8270c926c29b5363c5369c9cb3158f470afe15`；PNG SHA256 `aca06694ec9a823bbcfcaf14ce14a9cc49dbf6516ce30b915a9c7423c6412f4b`。目标结构检查 `v05/target_audit.json` 3 项零 FAIL（作用面/身份局部检查）；它不验可视清晰、机械/光电功能。审阅者：AGH 对脚本与有限结构核查；**新图 AGH 读图服务失败，外部复核新版本待审**。本地源—被审旧版—新图画布 `../../demo-assets/15_biomed_energy/stage4_source_v04_v05_LOCAL.png` 不提交。相关尺寸、材料外观、不可见连接/载荷/密封仍是未知或假设。
