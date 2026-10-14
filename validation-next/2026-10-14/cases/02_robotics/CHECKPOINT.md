# 02_robotics｜低成本示意预览检查点（未验收）

DOI: https://doi.org/10.1038/s41467-025-56025-3。日期 2025-02-06。依据：Fig. 3b，PDF p.4，拉伸夹具与柔性试样；图/正文中文解释：照片中双爪夹住两色柔软试样。类别 C，指定完整范围：可见双夹爪、试样与支承，非 Fig.1 时序设计。

当前场景 `v01/scene.blend` / `v01/overview.png`；最新版 `v01`。构建脚本 `../../build_cases.py`、`../../build_more.py`、`../../render_core.py`；修订使用 `../../revise_cases.py`。Blender 5.1.2 EEVEE，900×640；独立进程重开 scene 并在该版本目录生成 `render_report.json`，存两 SHA256。v01 scene `561f4c84e39179a30c46d1f740d47f03996e095005ca79a946a743b4f8666759`；PNG `de892287f84c3de43402ea3b6474146132860aaa3870e3e94709733e46d234be`。这不证明像素、物理或装配。

主要三项差异：测试机柱架极简；夹面似断连；软试样太直。建模假设：所有相对比例/尺寸/背景；未见的接口和内部结构不能按场景推为论文事实。开放未知：夹具型号和内部受力未知。本版变化：仅 v01 首版，未伪造失败后的 v02。人工优先核验：上夹钳和试样触点、受力方向。实际审阅：AGH 批次拼图捕获 3378，粗看而非逐例高清；其余无逐例 PNG 专项读图。外部模型未审，人工未审。

|检查点|来源位置|输出位置|证据类型|结论|待人工确认|
|---|---|---|---|---|---|
|范围与身份|Fig. 3b，PDF p.4，拉伸夹具与柔性试样|`v01/overview.png`|论文图/正文 + AGH 粗看|示意阶段/未验收|上夹钳和试样触点、受力方向|
|可见线路/装配|Fig. 3b，PDF p.4，拉伸夹具与柔性试样|`v01/scene.blend`|有限网格+渲染|未完成实端口逐跳验证|开孔、接头、遮挡及支撑|
|图像外观|见本地 `../../demo-assets/02_robotics/source/SOURCE.md`|`v01/overview.png`|AGH 实际读批次拼图|不作通过声明|对应实物形态|

## 外部人工复核后的非破坏候选版（尚未验收）
外部人工逐例读源依据与旧版 PNG 后指出的差异详见 `../../EXTERNAL_HUMAN_REVIEW.md`（审阅者：外部复核，目视，**针对旧版**）。新 `v02` 保存于 [`v02/scene.blend`](v02/scene.blend)、[`v02/overview.png`](v02/overview.png)，独立 Blender 进程重载并渲染。针对性修改：圆形上下夹具和实体试样端接，机架导轨增厚；真实夹紧载荷未知。绝对尺寸、比例、不可见接口与内部机理仍为建模假设/开放未知。 scene SHA256 `63eeadc15ba3315017465956a6cf5e2912db4aefe0c45533a53a3de132ae1e84`；PNG SHA256 `5b2f692715bf6d1f9b5f9b4c86fe3eede65079f11b130c699bda0a5e58a1a82c`。**新图 AGH 未能 capture（apps discovery failed），也尚无新版本外部人工或用户验收；重载成功/几何项 PASS 不等于目视通过。**来源锚点在 `../../demo-assets/02_robotics/source/SOURCE.md`，本地含原图画布 `../../demo-assets/02_robotics/new_source_v01_v02_LOCAL.png` 不提交。

数值反例保留：v02 `target_audit.json` upper_coupon_z_inside_grip=FAIL；单独 v03 定点延长上试样后独立重载审计该项不再 FAIL，`v03/scene.blend` + `v03/overview.png` + `v03/target_audit.json`。外部人工尚未读 v03，不能说夹持通过；本地 4 栏源/失败版/候选对比 `../../demo-assets/02_robotics/new_source_v01_v02_v03_LOCAL.png`。

### 第二轮外部复核后：`v04` 候选（旧版不覆盖）
外部复核实际逐张目视旧 `v03` 后判失败；具体差异见 `../../EXTERNAL_HUMAN_REVIEW.md`，几何旧检查另列，不能跨版外推。`../../revise_connectivity_stage4.py` 从保存的 `v03/scene.blend` 另存 `v04/scene.blend`；**独立 Blender 进程重新打开**并写出 `v04/overview.png`。场景 SHA256 `f81d15b1ff3243fd4f1cdf5ff329c7e7e4248d5b0662599e21358294007b9ac7`；PNG SHA256 `12fc1a58e53fe17fbd7d10aaf943c1d0b734b47d659ab8b07e9e330a62ab9d81`。目标结构检查 `v04/target_audit.json` 6 项零 FAIL（作用面/身份局部检查）；它不验可视清晰、机械/光电功能。审阅者：AGH 对脚本与有限结构核查；**新图 AGH 读图服务失败，外部复核新版本待审**。本地源—被审旧版—新图画布 `../../demo-assets/02_robotics/stage4_source_v03_v04_LOCAL.png` 不提交。相关尺寸、材料外观、不可见连接/载荷/密封仍是未知或假设。

### 第三轮外部复核后 `v05` 独立候选（不自动验收）
旧 `v04` 被**外部复核**实际逐张读图的判词在 `../../EXTERNAL_HUMAN_REVIEW.md` 第三表。候选文件 [`v05/scene.blend`](v05/scene.blend)、[`v05/overview.png`](v05/overview.png)，由另一 Blender 进程重开已保存场景后渲染。scene SHA `55a7de0f40cc4d81ae0c30e779c894b47f3f8fb8f58c7d2ec386916433405399`；PNG SHA `daf2a49a5bc5d540097091212649088efcbd88e791cc9434c84ccd0bf40fc6dc`。`v05/target_audit.json` 仅审核 8 项可见对象/网格端点，FAIL=[]；非视觉/密封/强度/光电功能证据。**AGH GUI 读取失败，新版无人再次目视，外部复核待审**。本地含原图三栏 `../../demo-assets/02_robotics/stage5_source_v04_v05_LOCAL.png` 不提交。
