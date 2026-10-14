# 08_biomedical｜低成本示意预览检查点（未验收）

DOI: https://doi.org/10.3991/ijoe.v22i03.59657。日期 2026-03-05。依据：Fig.3 left, PDF p.6, 三层装配示意（非严格爆炸）；图/正文中文解释：三层人工皮肤/胶层/导电硅胶 P1。类别 A，指定完整范围：人工皮肤基底、双面粘结硅胶、中上层导电 P1 与有图线端。

当前场景 `v01/scene.blend` / `v01/overview.png`；最新版 `v01`。构建脚本 `../../build_cases.py`、`../../build_more.py`、`../../render_core.py`；修订使用 `../../revise_cases.py`。Blender 5.1.2 EEVEE，900×640；独立进程重开 scene 并在该版本目录生成 `render_report.json`，存两 SHA256。v01 scene `d2e4225dab9487e4a6a9f2ad23dd9f49a631ab23470dbfeef6b1092e77e7015c`；PNG `3a0be835b0aa07bed3894e6c1a10ea26d6064aad40080f2d59544541ad68ea41`。这不证明像素、物理或装配。

主要三项差异：层次过于平板；接触点只简画；右照片电极未知。建模假设：所有相对比例/尺寸/背景；未见的接口和内部结构不能按场景推为论文事实。开放未知：照片另作外形参考，不当首版 CAD。本版变化：仅 v01 首版，未伪造失败后的 v02。人工优先核验：两电极真实接点与层间贴合。实际审阅：AGH 批次拼图捕获 3378，粗看而非逐例高清；其余无逐例 PNG 专项读图。外部模型未审，人工未审。

|检查点|来源位置|输出位置|证据类型|结论|待人工确认|
|---|---|---|---|---|---|
|范围与身份|Fig.3 left, PDF p.6, 三层装配示意（非严格爆炸）|`v01/overview.png`|论文图/正文 + AGH 粗看|示意阶段/未验收|两电极真实接点与层间贴合|
|可见线路/装配|Fig.3 left, PDF p.6, 三层装配示意（非严格爆炸）|`v01/scene.blend`|有限网格+渲染|未完成实端口逐跳验证|开孔、接头、遮挡及支撑|
|图像外观|见本地 `../../demo-assets/08_biomedical/source/SOURCE.md`|`v01/overview.png`|AGH 实际读批次拼图|不作通过声明|对应实物形态|

## 外部人工复核后的非破坏候选版（尚未验收）
外部人工逐例读源依据与旧版 PNG 后指出的差异详见 `../../EXTERNAL_HUMAN_REVIEW.md`（审阅者：外部复核，目视，**针对旧版**）。新 `v02` 保存于 [`v02/scene.blend`](v02/scene.blend)、[`v02/overview.png`](v02/overview.png)，独立 Blender 进程重载并渲染。针对性修改：导电 P1 图案与 measurement point 可辨，层材分别命名；引线仅外部段。绝对尺寸、比例、不可见接口与内部机理仍为建模假设/开放未知。 scene SHA256 `5a219b0ef6808214648f71a271f4928d29a5c5575a78802cfceb490bbe559743`；PNG SHA256 `ed196142f65a25a6c961bf3e97e9e729a26a334ec29b30a3a6bf243cadc8b4c3`。**新图 AGH 未能 capture（apps discovery failed），也尚无新版本外部人工或用户验收；重载成功/几何项 PASS 不等于目视通过。**来源锚点在 `../../demo-assets/08_biomedical/source/SOURCE.md`，本地含原图画布 `../../demo-assets/08_biomedical/new_source_v01_v02_LOCAL.png` 不提交。

### 第二轮外部复核后：`v03` 候选（旧版不覆盖）
外部复核实际逐张目视旧 `v02` 后判失败；具体差异见 `../../EXTERNAL_HUMAN_REVIEW.md`，几何旧检查另列，不能跨版外推。`../../revise_connectivity_stage4.py` 从保存的 `v02/scene.blend` 另存 `v03/scene.blend`；**独立 Blender 进程重新打开**并写出 `v03/overview.png`。场景 SHA256 `08635c02a2a4f87e953a936ed5ce834873df0f8116ebf5e4cfa8d75614e9830e`；PNG SHA256 `a47417101c64de02457e69f3e53fed9e5aaaad9f9ed30804d104dee3b75ccff7`。目标结构检查 `v03/target_audit.json` 14 项零 FAIL（作用面/身份局部检查）；它不验可视清晰、机械/光电功能。审阅者：AGH 对脚本与有限结构核查；**新图 AGH 读图服务失败，外部复核新版本待审**。本地源—被审旧版—新图画布 `../../demo-assets/08_biomedical/stage4_source_v02_v03_LOCAL.png` 不提交。相关尺寸、材料外观、不可见连接/载荷/密封仍是未知或假设。

### 第三轮外部复核：保留 `v03` 候选，不扩范围
审阅者：**外部复核**，实际逐张看当前源图/渲染，意见见 `../../EXTERNAL_HUMAN_REVIEW.md` 第三表；该版尚未最终验收。本轮不改模型、不重渲旧版。独立本地三栏 `../../demo-assets/08_biomedical/stage5_source_v02_v03_LOCAL.png` 仅供本地复核。有限结构 QA 不构成视觉通过。

### 第四轮外部复核：保留 `v03` 原候选
审阅者：**外部复核**，实际逐张目视 stage5 图/源，判词见 `../../EXTERNAL_HUMAN_REVIEW.md` 第四表；本轮**未改模型/PNG、不宣称验收**。本地源—旧—当前画布 `../../demo-assets/08_biomedical/stage6_source_v02_v03_LOCAL.png` 仅用于本地复核。
