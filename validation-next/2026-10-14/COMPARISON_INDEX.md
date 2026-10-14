# 全部十例｜源—首版—当前版索引（未验收）

每例输入图或文字来自 DOI，在 `demo-assets/<id>/source/` 保留原论文 PDF 页面/文字说明及 `SOURCE.md`；图像可公开再分发许可尚未核对。文字三例 v01 只依据所标正文；后续若引图，必须单独 v02 并留版本证据。`v01/scene.blend` 为可编辑低成本 3D，`render_report.json` 有独立重载/哈希，但**不替代视觉或功能检查**。

|案例/DOI|输入|依据|首版|前后/最新版|AGH 视觉状态|人工|
|---|---|---|---|---|---|---|
|[02_robotics](https://doi.org/10.1038/s41467-025-56025-3)|C|[源位置](demo-assets/02_robotics/source/SOURCE.md)：Fig. 3b，PDF p.4，拉伸夹具与柔性试样|[v01](cases/02_robotics/v01/overview.png) · [场景](cases/02_robotics/v01/scene.blend)|无修订（勿伪造）|v01 拼图粗看；未单例验收|未确认|
|[04_microfluidics](https://doi.org/10.1038/s41526-025-00470-3)|B|[源位置](demo-assets/04_microfluidics/source/SOURCE.md)：Fig. 3C，PDF p.4，面板安装注射器至芯片；Fig.3A仅核外形|[v01](cases/04_microfluidics/v01/overview.png) · [场景](cases/04_microfluidics/v01/scene.blend)|[比较](demo-assets/04_microfluidics/comparison_source_v01_v03_v04_v05_LOCAL.png) · [最新版](cases/04_microfluidics/v05/overview.png)|04 v03 FAIL；v04 起点 FAIL；v05 外边界 audit 0、像素未读|未确认|
|[08_biomedical](https://doi.org/10.3991/ijoe.v22i03.59657)|A|[源位置](demo-assets/08_biomedical/source/SOURCE.md)：Fig.3 left, PDF p.6, 三层装配示意（非严格爆炸）|[v01](cases/08_biomedical/v01/overview.png) · [场景](cases/08_biomedical/v01/scene.blend)|无修订（勿伪造）|v01 拼图粗看；未单例验收|未确认|
|[13_biomed_optics](https://doi.org/10.1038/s44303-026-00161-y)|B|[源位置](demo-assets/13_biomed_optics/source/SOURCE.md)：Fig. 1a,c，PDF p.3，内窥镜与三个照明口|[v01](cases/13_biomed_optics/v01/overview.png) · [场景](cases/13_biomed_optics/v01/scene.blend)|无修订（勿伪造）|v01 拼图粗看；未单例验收|未确认|
|[14_acoustic_alt](https://doi.org/10.1038/s41598-025-24666-5)|C|[源位置](demo-assets/14_acoustic_alt/source/SOURCE.md)：Fig. 1c（辅以 Fig.1a），PDF p.3，Tiny-Lev 与振动台|[v01](cases/14_acoustic_alt/v01/overview.png) · [场景](cases/14_acoustic_alt/v01/scene.blend)|无修订（勿伪造）|v01 拼图粗看；未单例验收|未确认|
|[15_biomed_energy](https://doi.org/10.1038/s41467-025-60911-1)|A|[源位置](demo-assets/15_biomed_energy/source/SOURCE.md)：Fig. 3a PDF p.5 图像、p.6 图注，穿戴传感器分层装配|[v01](cases/15_biomed_energy/v01/overview.png) · [场景](cases/15_biomed_energy/v01/scene.blend)|[比较](demo-assets/15_biomed_energy/comparison_source_v01_v02_v03_LOCAL.png) · [最新版](cases/15_biomed_energy/v03/overview.png)|15 v02 局部改善；v03 像素未读、整体未过|未确认|
|[16_energy_nature](https://doi.org/10.1038/s41467-025-64306-0)|D|[源位置](demo-assets/16_energy_nature/source/SOURCE.md)：Methods p.9|[v01](cases/16_energy_nature/v01/overview.png) · [场景](cases/16_energy_nature/v01/scene.blend)|无修订（勿伪造）|v01 拼图粗看；未单例验收|未确认|
|[17_rf_nature](https://doi.org/10.1038/s41598-026-39831-7)|A|[源位置](demo-assets/17_rf_nature/source/SOURCE.md)：Fig. 1a–d，PDF p.4，馈线/双椭圆槽/辐射体|[v01](cases/17_rf_nature/v01/overview.png) · [场景](cases/17_rf_nature/v01/scene.blend)|无修订（勿伪造）|v01 拼图粗看；未单例验收|未确认|
|[18_mechanical_nature](https://doi.org/10.1038/s41467-026-77199-4)|D|[源位置](demo-assets/18_mechanical_nature/source/SOURCE.md)：Methods p.9|[v01](cases/18_mechanical_nature/v01/overview.png) · [场景](cases/18_mechanical_nature/v01/scene.blend)|无修订（勿伪造）|v01 拼图粗看；未单例验收|未确认|
|[20_thermal](https://doi.org/10.1038/s41467-025-56960-1)|D|[源位置](demo-assets/20_thermal/source/SOURCE.md)：Materials p.11（辅以 p.2 正文）|[v01](cases/20_thermal/v01/overview.png) · [场景](cases/20_thermal/v01/scene.blend)|无修订（勿伪造）|v01 拼图粗看；未单例验收|未确认|

脚本：`render_core.py`、`build_cases.py`、`build_more.py`、`render_saved.py`；针对 04/15 的修订：`revise_cases.py`、`revise_micro_v03.py`；每例逐条说明/假设/人工核验表：`cases/<id>/CHECKPOINT.md`。总览拼图 `demo-assets/v01_contact_sheet.png`。AGH 真读图与失败史见 `VISUAL_REVIEW_V01.md`、`REVISIONS_04_15.md`。其余八例没有 v02，**并非全部十例前后修订已完成**。本轮 Computer Use 窗口发现故障，逐例源图–PNG 像素审查尚未完成，最新两版仅重载/数值核验。具体见 `INDIVIDUAL_REVIEW_TABLE.md`。

## 外部人工反馈后十例新的候选渲染（勿误判验收）
完整源—v01—新版本清单及私有逐例高清画布、全长 SHA256 见 [`NEW_VERSION_REVIEW_QUEUE.md`](NEW_VERSION_REVIEW_QUEUE.md)。旧版外部人工逐例读图差异见 [`EXTERNAL_HUMAN_REVIEW.md`](EXTERNAL_HUMAN_REVIEW.md)。上表初轮比较仍保留历史，不再以其“最新版”列当今天新版本；04 最新 v06、15 最新 v04、02 最新 v03、其余最新 v02。所有新图尚未经用户再次目视，AGH 图片捕获仍故障。

## 第二轮外部复核后
上面历史表中“最新版”已不是最新；准确逐例链接及不可公开本地源图三栏画布在 `STAGE4_REVIEW_QUEUE.md`。新图均未由 AGH/外部再次实际读像素，任何几何项零 FAIL 不等于接受。

第三轮外部复核后的十例最新文件清单/哈希和本地对照画布请以 `STAGE5_REVIEW_QUEUE.md` 为准；上方表是早期历史，不再是“最新”。

第四轮外部复核后的当前版/哈希/本地单例源—旧—新对照以 `STAGE6_REVIEW_QUEUE.md` 为准；此表先前版本保留历史，不误称最新版或视觉通过。
