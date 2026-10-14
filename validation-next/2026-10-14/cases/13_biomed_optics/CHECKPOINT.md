# 13_biomed_optics｜低成本示意预览检查点（未验收）

DOI: https://doi.org/10.1038/s44303-026-00161-y。日期 2026-05-04。依据：Fig. 1a,c，PDF p.3，内窥镜与三个照明口；图/正文中文解释：内窥镜台车与接头端三个外部照明口。类别 B，指定完整范围：镜管接头端、临床系统、三入射纤维和远端视窗的可见外部段。

当前场景 `v01/scene.blend` / `v01/overview.png`；最新版 `v01`。构建脚本 `../../build_cases.py`、`../../build_more.py`、`../../render_core.py`；修订使用 `../../revise_cases.py`。Blender 5.1.2 EEVEE，900×640；独立进程重开 scene 并在该版本目录生成 `render_report.json`，存两 SHA256。v01 scene `b7fc0225f32849633b8f4424de5435ee583bbf03f8cf3cf448a67455c5c0f047`；PNG `3a5f39e8ed66c18b3c0d9712040ea9968d6105a41dbf9fcc9103024172161491`。这不证明像素、物理或装配。

主要三项差异：台车比例偏通用；镜身折线过硬；接头三路线未核。建模假设：所有相对比例/尺寸/背景；未见的接口和内部结构不能按场景推为论文事实。开放未知：不虚构镜身内部束走向。本版变化：仅 v01 首版，未伪造失败后的 v02。人工优先核验：光纤插入深度/镜身实际柔曲。实际审阅：AGH 批次拼图捕获 3378，粗看而非逐例高清；其余无逐例 PNG 专项读图。外部模型未审，人工未审。

|检查点|来源位置|输出位置|证据类型|结论|待人工确认|
|---|---|---|---|---|---|
|范围与身份|Fig. 1a,c，PDF p.3，内窥镜与三个照明口|`v01/overview.png`|论文图/正文 + AGH 粗看|示意阶段/未验收|光纤插入深度/镜身实际柔曲|
|可见线路/装配|Fig. 1a,c，PDF p.3，内窥镜与三个照明口|`v01/scene.blend`|有限网格+渲染|未完成实端口逐跳验证|开孔、接头、遮挡及支撑|
|图像外观|见本地 `../../demo-assets/13_biomed_optics/source/SOURCE.md`|`v01/overview.png`|AGH 实际读批次拼图|不作通过声明|对应实物形态|

## 外部人工复核后的非破坏候选版（尚未验收）
外部人工逐例读源依据与旧版 PNG 后指出的差异详见 `../../EXTERNAL_HUMAN_REVIEW.md`（审阅者：外部复核，目视，**针对旧版**）。新 `v02` 保存于 [`v02/scene.blend`](v02/scene.blend)、[`v02/overview.png`](v02/overview.png)，独立 Blender 进程重载并渲染。针对性修改：屏支架/脚轮并入推车，光源到镜尾三外纤与柔性镜管；光纤接头内部未知。绝对尺寸、比例、不可见接口与内部机理仍为建模假设/开放未知。 scene SHA256 `cf8175c9cb2a0b7288dcec4df47bbc87375c9c6fe4672034ba5f6824e985dce3`；PNG SHA256 `336047f7cc96eeb2e13aa93e509fa0d5019e6e6f4131be78b7cbbae9abcb6d86`。**新图 AGH 未能 capture（apps discovery failed），也尚无新版本外部人工或用户验收；重载成功/几何项 PASS 不等于目视通过。**来源锚点在 `../../demo-assets/13_biomed_optics/source/SOURCE.md`，本地含原图画布 `../../demo-assets/13_biomed_optics/new_source_v01_v02_LOCAL.png` 不提交。
