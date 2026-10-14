# 14_acoustic_alt｜低成本示意预览检查点（未验收）

DOI: https://doi.org/10.1038/s41598-025-24666-5。日期 2025-11-19。依据：Fig. 1c（辅以 Fig.1a），PDF p.3，Tiny-Lev 与振动台；图/正文中文解释：TinyLev 上下阵列、振动台、LDV测量。类别 C，指定完整范围：Fig.1c 可见 Tiny-Lev 上下阵列、悬浮物、振动台和 LDV，a 仅连接逻辑参考。

当前场景 `v01/scene.blend` / `v01/overview.png`；最新版 `v01`。构建脚本 `../../build_cases.py`、`../../build_more.py`、`../../render_core.py`；修订使用 `../../revise_cases.py`。Blender 5.1.2 EEVEE，900×640；独立进程重开 scene 并在该版本目录生成 `render_report.json`，存两 SHA256。v01 scene `3d8182f6ab80fec647619dd2c6b29edc58effebf255e40d48133aee526f4a29a`；PNG `29351e27a064420ecb7f3298b657bde9820f9d65db20351983a57465ddf7174a`。这不证明像素、物理或装配。

主要三项差异：上阵列发射面难见；LDV 对准未知；少周边支撑。建模假设：所有相对比例/尺寸/背景；未见的接口和内部结构不能按场景推为论文事实。开放未知：不将声场示意画成实体棒。本版变化：仅 v01 首版，未伪造失败后的 v02。人工优先核验：LDV 轴线和照片可辨仪器。实际审阅：AGH 批次拼图捕获 3378，粗看而非逐例高清；其余无逐例 PNG 专项读图。外部模型未审，人工未审。

|检查点|来源位置|输出位置|证据类型|结论|待人工确认|
|---|---|---|---|---|---|
|范围与身份|Fig. 1c（辅以 Fig.1a），PDF p.3，Tiny-Lev 与振动台|`v01/overview.png`|论文图/正文 + AGH 粗看|示意阶段/未验收|LDV 轴线和照片可辨仪器|
|可见线路/装配|Fig. 1c（辅以 Fig.1a），PDF p.3，Tiny-Lev 与振动台|`v01/scene.blend`|有限网格+渲染|未完成实端口逐跳验证|开孔、接头、遮挡及支撑|
|图像外观|见本地 `../../demo-assets/14_acoustic_alt/source/SOURCE.md`|`v01/overview.png`|AGH 实际读批次拼图|不作通过声明|对应实物形态|

## 外部人工复核后的非破坏候选版（尚未验收）
外部人工逐例读源依据与旧版 PNG 后指出的差异详见 `../../EXTERNAL_HUMAN_REVIEW.md`（审阅者：外部复核，目视，**针对旧版**）。新 `v02` 保存于 [`v02/scene.blend`](v02/scene.blend)、[`v02/overview.png`](v02/overview.png)，独立 Blender 进程重载并渲染。针对性修改：LDV 光轴下瞄悬浮样品，保留非接触阵列+振动台；光轴为假设图示。绝对尺寸、比例、不可见接口与内部机理仍为建模假设/开放未知。 scene SHA256 `0f3540a17731ba9672991dcaa49112a9e20f2158e1855ac8d4f38deeafcc5b95`；PNG SHA256 `5a0334fa696f499e057571ea55a5c6a2fe682f191374c8f56e104bb29ef66dbb`。**新图 AGH 未能 capture（apps discovery failed），也尚无新版本外部人工或用户验收；重载成功/几何项 PASS 不等于目视通过。**来源锚点在 `../../demo-assets/14_acoustic_alt/source/SOURCE.md`，本地含原图画布 `../../demo-assets/14_acoustic_alt/new_source_v01_v02_LOCAL.png` 不提交。

### 第二轮外部复核后：`v03` 候选（旧版不覆盖）
外部复核实际逐张目视旧 `v02` 后判失败；具体差异见 `../../EXTERNAL_HUMAN_REVIEW.md`，几何旧检查另列，不能跨版外推。`../../revise_connectivity_stage4.py` 从保存的 `v02/scene.blend` 另存 `v03/scene.blend`；**独立 Blender 进程重新打开**并写出 `v03/overview.png`。场景 SHA256 `efa0e3bb262115892bec0a38cf4e90d5fe20f7454db3dfe59bfc10efaba904b6`；PNG SHA256 `ca3374521d954c38f8c4382d55f468bbb5045156fba01b752ea890cb5c526f54`。目标结构检查 `v03/target_audit.json` 4 项零 FAIL（作用面/身份局部检查）；它不验可视清晰、机械/光电功能。审阅者：AGH 对脚本与有限结构核查；**新图 AGH 读图服务失败，外部复核新版本待审**。本地源—被审旧版—新图画布 `../../demo-assets/14_acoustic_alt/stage4_source_v02_v03_LOCAL.png` 不提交。相关尺寸、材料外观、不可见连接/载荷/密封仍是未知或假设。

### 第三轮外部复核后 `v04` 独立候选（不自动验收）
旧 `v03` 被**外部复核**实际逐张读图的判词在 `../../EXTERNAL_HUMAN_REVIEW.md` 第三表。候选文件 [`v04/scene.blend`](v04/scene.blend)、[`v04/overview.png`](v04/overview.png)，由另一 Blender 进程重开已保存场景后渲染。scene SHA `82301c961ff349faabd2d043486c61e5752dbcb042bc8154d530415c513cdbbc`；PNG SHA `4c50a08bb186569d18954ec3ae65f292a14bfc96c67b308526ba7940bdc9f940`。`v04/target_audit.json` 仅审核 3 项可见对象/网格端点，FAIL=[]；非视觉/密封/强度/光电功能证据。**AGH GUI 读取失败，新版无人再次目视，外部复核待审**。本地含原图三栏 `../../demo-assets/14_acoustic_alt/stage5_source_v03_v04_LOCAL.png` 不提交。
