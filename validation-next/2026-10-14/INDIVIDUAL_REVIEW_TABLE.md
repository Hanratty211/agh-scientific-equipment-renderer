# 十例独立图像审查台账｜外部人工看过旧版，新版待复核

本轮每篇单独生成 1800×760 本地对照画布 `demo-assets/<id>/source_and_current_LOCAL.png`（后对 04、15 的新版本应使用专门多栏图）；AGH GUI capture 故障未实读新图；随后用户报告十例旧版由外部人工逐例源图/文字与渲染视觉复核，详见 `EXTERNAL_HUMAN_REVIEW.md`。对应源与渲染路径、SHA 可复核。十例既有 v01 CHECKPOINT 差异属于上一轮粗看，不补写新像素判断。

|案例/类型|来源（本地，不入 Git）|当前自制渲染|现有差异/未知|本轮审阅者与状态|
|---|---|---|---|---|
|[02_robotics](cases/02_robotics/CHECKPOINT.md) / C|[Fig. 3b，PDF p.4，拉伸夹具与柔性试样](demo-assets/02_robotics/source/SOURCE.md) → `target_fig3b.png` SHA `13b9b26731c0`|[`v01` PNG](cases/02_robotics/v01/overview.png) SHA `de892287f84c` · [scene](cases/02_robotics/v01/scene.blend)|见 CHECKPOINT.md 的 v01 差异；单例高清差异待 AGH 读图|外部人工逐例目视旧版并判未通过；AGH 未实读，新版待审|
|[04_microfluidics](cases/04_microfluidics/CHECKPOINT.md) / B|[Fig. 3C，PDF p.4，面板安装注射器至芯片；Fig.3A仅核外形](demo-assets/04_microfluidics/source/SOURCE.md) → `target_fig3C.png` SHA `f1939b911d60`|[`v05` PNG](cases/04_microfluidics/v05/overview.png) SHA `030be22f9314` · [scene](cases/04_microfluidics/v05/scene.blend)|v03断连、假孔；v05只外部端点数值核对，实孔/内流未知|外部人工逐例目视旧版并判未通过；AGH 未实读，新版待审|
|[08_biomedical](cases/08_biomedical/CHECKPOINT.md) / A|[Fig.3 left, PDF p.6, 三层装配示意（非严格爆炸）](demo-assets/08_biomedical/source/SOURCE.md) → `target_region_context.png` SHA `fdbb608756c1`|[`v01` PNG](cases/08_biomedical/v01/overview.png) SHA `3a0be835b0aa` · [scene](cases/08_biomedical/v01/scene.blend)|见 CHECKPOINT.md 的 v01 差异；单例高清差异待 AGH 读图|外部人工逐例目视旧版并判未通过；AGH 未实读，新版待审|
|[13_biomed_optics](cases/13_biomed_optics/CHECKPOINT.md) / B|[Fig. 1a,c，PDF p.3，内窥镜与三个照明口](demo-assets/13_biomed_optics/source/SOURCE.md) → `figure_region_00.png` SHA `47ac4873e46e`|[`v01` PNG](cases/13_biomed_optics/v01/overview.png) SHA `3a5f39e8ed66` · [scene](cases/13_biomed_optics/v01/scene.blend)|见 CHECKPOINT.md 的 v01 差异；单例高清差异待 AGH 读图|外部人工逐例目视旧版并判未通过；AGH 未实读，新版待审|
|[14_acoustic_alt](cases/14_acoustic_alt/CHECKPOINT.md) / C|[Fig. 1c（辅以 Fig.1a），PDF p.3，Tiny-Lev 与振动台](demo-assets/14_acoustic_alt/source/SOURCE.md) → `target_fig1c.png` SHA `79c596831888`|[`v01` PNG](cases/14_acoustic_alt/v01/overview.png) SHA `29351e27a064` · [scene](cases/14_acoustic_alt/v01/scene.blend)|见 CHECKPOINT.md 的 v01 差异；单例高清差异待 AGH 读图|外部人工逐例目视旧版并判未通过；AGH 未实读，新版待审|
|[15_biomed_energy](cases/15_biomed_energy/CHECKPOINT.md) / A|[Fig. 3a PDF p.5 图像、p.6 图注，穿戴传感器分层装配](demo-assets/15_biomed_energy/source/SOURCE.md) → `target_fig3a.png` SHA `0b19c509e19d`|[`v03` PNG](cases/15_biomed_energy/v03/overview.png) SHA `54dfb2959a90` · [scene](cases/15_biomed_energy/v03/scene.blend)|v02仅开窗改善；v03真实效果和电连接未知|外部人工逐例目视旧版并判未通过；AGH 未实读，新版待审|
|[16_energy_nature](cases/16_energy_nature/CHECKPOINT.md) / D|[Methods PDF p.9 段落（每次单程蠕动泵供液）；Fig.1b仅后版核系统逻辑](demo-assets/16_energy_nature/source/SOURCE.md) → `text_p9.txt` SHA `8bf908248722`|[`v01` PNG](cases/16_energy_nature/v01/overview.png) SHA `c5e1b15c089f` · [scene](cases/16_energy_nature/v01/scene.blend)|见 CHECKPOINT.md 的 v01 差异；单例高清差异待 AGH 读图|外部人工逐例目视旧版并判未通过；AGH 未实读，新版待审|
|[17_rf_nature](cases/17_rf_nature/CHECKPOINT.md) / A|[Fig. 1a–d，PDF p.4，馈线/双椭圆槽/辐射体](demo-assets/17_rf_nature/source/SOURCE.md) → `target_region_context.png` SHA `676251463117`|[`v01` PNG](cases/17_rf_nature/v01/overview.png) SHA `dae806373087` · [scene](cases/17_rf_nature/v01/scene.blend)|见 CHECKPOINT.md 的 v01 差异；单例高清差异待 AGH 读图|外部人工逐例目视旧版并判未通过；AGH 未实读，新版待审|
|[18_mechanical_nature](cases/18_mechanical_nature/CHECKPOINT.md) / D|[Methods PDF p.9：ZwickRoell Z100 拉伸测试机与试样；Fig.2d仅后版核测量情境](demo-assets/18_mechanical_nature/source/SOURCE.md) → `text_p9.txt` SHA `6383d4d3188b`|[`v01` PNG](cases/18_mechanical_nature/v01/overview.png) SHA `26f54e1eee16` · [scene](cases/18_mechanical_nature/v01/scene.blend)|见 CHECKPOINT.md 的 v01 差异；单例高清差异待 AGH 读图|外部人工逐例目视旧版并判未通过；AGH 未实读，新版待审|
|[20_thermal](cases/20_thermal/CHECKPOINT.md) / D|[Materials PDF p.11 铝塑壳与铜网芯；Fig.1c仅后版核形态](demo-assets/20_thermal/source/SOURCE.md) → `text_p11.txt` SHA `1566e198b42d`|[`v01` PNG](cases/20_thermal/v01/overview.png) SHA `d24ecd05cc2c` · [scene](cases/20_thermal/v01/scene.blend)|见 CHECKPOINT.md 的 v01 差异；单例高清差异待 AGH 读图|外部人工逐例目视旧版并判未通过；AGH 未实读，新版待审|

图像失效症状见 `INDIVIDUAL_REVIEW_STATUS.md`。本地单例对照画布路径固定且只本地存放；源码出处见各 SOURCE.md/PDF。逐例具体旧版像素差异及审阅者为 `EXTERNAL_HUMAN_REVIEW.md`；新修订必须重新经图像审查，不能沿用旧版人工结论作新版通过。

## 第二轮外部目视后的最新队列
外部复核逐条判词、目视/自动核查分栏：`EXTERNAL_HUMAN_REVIEW.md`。本轮另存 8 个候选版；04 v06 不变、18 仍 parent-material v02；十例最新源依据→被审旧版→当前版→有限 QA/哈希/本地并排画布见 `STAGE4_REVIEW_QUEUE.md`，替代本表早期版本的“当前”列。**新 PNG 尚未再次目视验收。**

第三轮外部复核最新来源—旧版—当前版索引 `STAGE5_REVIEW_QUEUE.md`，旧本表保留历史。18 的输入此轮另以 Fig.18 作为有图锚点，旧 Type IV v02 不冒充 PIM。

第四轮外部复核后的当前版/哈希/本地单例源—旧—新对照以 `STAGE6_REVIEW_QUEUE.md` 为准；此表先前版本保留历史，不误称最新版或视觉通过。
