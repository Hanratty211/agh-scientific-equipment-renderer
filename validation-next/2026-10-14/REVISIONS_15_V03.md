# 15 Fig.3a 结构辨识改版 v03｜像素待审

DOI `10.1038/s41467-025-60911-1`，Fig.3a 图像 PDF p.5，图注 p.6。本地裁图 `demo-assets/15_biomed_energy/source/target_fig3a.png`。上轮 AGH 实读 v01 顶板挡 PV，v02 开窗后局部改善，但两电池/光学模块/板面总体仍像三块通用叠板，未过。v03 基于 v02 的真实开窗场景，抬升**建模中的**上封装层，缩小 fPCB 占地，增加 PV 边沿以独立显示两个 LiPo 电池、PPG 与 fPCB。坐标与爆炸距离、边沿非论文尺寸，只是源图分层关系的可编辑表达；电极/体表接触和电连接不被证明。旧版均未覆盖。

独立 Blender 5.1.2 重载 v03 `cases/15_biomed_energy/v03/scene.blend` 并渲染 `overview.png`；SHA scene `916c34984166b9f69ff2ac5105f1aba0020b24c7c0910922130a834e6000cd8d`，PNG `54dfb2959a90bb659ad4ab0044d4f3891a1f73421fc4fa606cd0f596761b89cf`。本地含出版方原图对照 `demo-assets/15_biomed_energy/comparison_source_v01_v02_v03_LOCAL.png` **不得提交**。

审查者：AGH 建模和重载状态审查；本轮 Computer Use windows/apps discovery 故障，v03 PNG **未实际读图**。上轮 AGH 仅实读到 v02，外部模型/用户未审。核心差异是否改善仍未知；后续必须单例实际读像素并复核整个层级、两电池、PV、PPG、fPCB 及体表界面，不能凭场景对象名推通过。
