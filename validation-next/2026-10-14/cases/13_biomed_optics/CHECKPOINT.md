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

### 第二轮外部复核后：`v03` 候选（旧版不覆盖）
外部复核实际逐张目视旧 `v02` 后判失败；具体差异见 `../../EXTERNAL_HUMAN_REVIEW.md`，几何旧检查另列，不能跨版外推。`../../revise_connectivity_stage4.py` 从保存的 `v02/scene.blend` 另存 `v03/scene.blend`；**独立 Blender 进程重新打开**并写出 `v03/overview.png`。场景 SHA256 `189e6b81b72b127b1eefd948fce7568360d80a860260405f58584b3a8a5b2b21`；PNG SHA256 `ea5b92f87695949fc9103aec8de916921f118f2c4e4d66847451b45a83144d2b`。目标结构检查 `v03/target_audit.json` 9 项零 FAIL（作用面/身份局部检查）；它不验可视清晰、机械/光电功能。审阅者：AGH 对脚本与有限结构核查；**新图 AGH 读图服务失败，外部复核新版本待审**。本地源—被审旧版—新图画布 `../../demo-assets/13_biomed_optics/stage4_source_v02_v03_LOCAL.png` 不提交。相关尺寸、材料外观、不可见连接/载荷/密封仍是未知或假设。

### 第三轮外部复核后 `v04` 独立候选（不自动验收）
旧 `v03` 被**外部复核**实际逐张读图的判词在 `../../EXTERNAL_HUMAN_REVIEW.md` 第三表。候选文件 [`v04/scene.blend`](v04/scene.blend)、[`v04/overview.png`](v04/overview.png)，由另一 Blender 进程重开已保存场景后渲染。scene SHA `0f39887cb6f8f4fcf6336c69b95051233fde3c326f0a66ecd2eaca10b6088925`；PNG SHA `ea10603dd1e22556e14c9e7f70e5a625c42c3106de58113df40707d077700f73`。`v04/target_audit.json` 仅审核 9 项可见对象/网格端点，FAIL=[]；非视觉/密封/强度/光电功能证据。**AGH GUI 读取失败，新版无人再次目视，外部复核待审**。本地含原图三栏 `../../demo-assets/13_biomed_optics/stage5_source_v03_v04_LOCAL.png` 不提交。

### 第四轮外部人工视觉复核后 Stage6 `v06` 候选（待看新图）
外部复核从磁盘逐张阅读 `v04` 与源图的判词见 `../../EXTERNAL_HUMAN_REVIEW.md` 第四表；不对本次新图外推“通过”。新场景 [`v06/scene.blend`](v06/scene.blend)、独立重载图 [`v06/overview.png`](v06/overview.png)；scene SHA256 `f0be0382f165d6a62d25d2ce3d3139f8cc3979567d455f873c98e15c325e1815`、PNG SHA256 `9e794e7126e831b74ea594d0ac90b5165c22cfb629cc801fc6255f92d2645433`。`v06/target_audit.json` 仅 5 个已声明几何断言 FAIL=[]，不测全图像素/内部功能；审阅者此轮：AGH 脚本/局部结构，**新图外部复核待审**。本地含源图三栏 `../../demo-assets/13_biomed_optics/stage6_source_v04_v06_LOCAL.png` 不提交。
中间 v05 场景/图/报告独立保留；第一版审计错误使用旋转 cylinder 的 local dimensions.y，纠正成世界 y 后 v05 也通过有限长度项；v06 是探头轮廓再延长，并非证实 v05 仍断连。Fig1a 外形与 Fig1c 三个后端纤维分别取证，细长头尺寸仍假设。

### 第五轮外部人工复核后 Stage7 `v07` 候选（未验收）
审阅者：**外部复核**，已从磁盘逐张读 stage6 旧 `v06` PNG 与来源；判词独立于数值在 `../../EXTERNAL_HUMAN_REVIEW.md` 第五轮表。只修本例限定目标：v07 保留三束独立后端线/主缆及细长探头，前端加锥度实物罩、可辨两圈层与透光端窗，尺寸是展示假设，未建内部光路。 [`v07/scene.blend`](v07/scene.blend) 经独立 Blender 重开渲染 [`v07/overview.png`](v07/overview.png)，scene SHA `50892655bdc49af239bb0a24f21cabcc5c946ec55311881be23a51216fd69ffc`，PNG SHA `5201684242f676a0a086e5b7331545f5e1e4999ff3e0088b7e3c1f96c2910c88`；`v07/target_audit.json` 仅 6 项局部网格/曲线存在性检查 FAIL=[]，**不代表像素/光学/强度验收**。新 PNG 尚无人目视，AGH GUI 仍故障。本地含源图三栏 `../../demo-assets/13_biomed_optics/stage7_source_v06_v07_LOCAL.png` 不入 Git。
