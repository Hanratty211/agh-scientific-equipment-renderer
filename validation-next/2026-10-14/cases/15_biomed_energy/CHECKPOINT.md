# 15_biomed_energy｜低成本示意预览检查点（未验收）

DOI: https://doi.org/10.1038/s41467-025-60911-1。日期 2025-07-01。依据：Fig. 3a PDF p.5 图像、p.6 图注，穿戴传感器分层装配；图/正文中文解释：PV/PPG/BLE/双电池/fPCB/封装分层。类别 A，指定完整范围：PV、PPG、BLE、电池对、fPCB、硅胶封装分层。

当前场景 `v01/scene.blend` / `v01/overview.png`；最新版 `v02`。构建脚本 `../../build_cases.py`、`../../build_more.py`、`../../render_core.py`；修订使用 `../../revise_cases.py`。Blender 5.1.2 EEVEE，900×640；独立进程重开 scene 并在该版本目录生成 `render_report.json`，存两 SHA256。v01 scene `0b15c95557a81d188afa00eb25dc9b21a9211ee86862f24adba935dd8e8198ab`；PNG `d33906727b50a4b820f02422d14d685d211d24c8c0b5539a09749b9abf999e68`。这不证明像素、物理或装配。

主要三项差异：v01 顶封装全挡 PV；v02 开窗后仍平板；电路假设多。建模假设：所有相对比例/尺寸/背景；未见的接口和内部结构不能按场景推为论文事实。开放未知：内部走线不凭空补。本版变化：v02 仅修受影响项；实际读图及不通过点见 `../../REVISIONS_04_15.md`。人工优先核验：开窗覆盖/电池端子/PPG作用面。实际审阅：AGH 批次拼图捕获 3378，粗看而非逐例高清；15 单独 capture 3586。外部模型未审，人工未审。

|检查点|来源位置|输出位置|证据类型|结论|待人工确认|
|---|---|---|---|---|---|
|范围与身份|Fig. 3a PDF p.5 图像、p.6 图注，穿戴传感器分层装配|`v01/overview.png`|论文图/正文 + AGH 粗看|示意阶段/未验收|开窗覆盖/电池端子/PPG作用面|
|可见线路/装配|Fig. 3a PDF p.5 图像、p.6 图注，穿戴传感器分层装配|`v01/scene.blend`|有限网格+渲染|未完成实端口逐跳验证|开孔、接头、遮挡及支撑|
|图像外观|见本地 `../../demo-assets/15_biomed_energy/source/SOURCE.md`|`v01/overview.png`|AGH 实际读批次拼图|不作通过声明|对应实物形态|
