# 18 补图核验｜先停建 PIM 新版本

公开补充材料下载自 `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-026-77199-4/MediaObjects/41467_2026_77199_MOESM1_ESM.pdf`，仅本地 `sources/18_supplementary_MOESM1_LOCAL.pdf`；其裁页 `demo-assets/18_mechanical_nature/source/supp_fig17_page32_LOCAL.png` 等 17–20 四张仅本地，不进 Git。PDF 51 页；标题/图注文本可提取并定位：Fig.17 = parent material evaluation，Fig.18 = PIM/CIM with different strengthening mechanisms，Fig.19 = PIM+CIM composites 多种拉/压工况，Fig.20 = humanoid tissue/finger/toe。原文 Methods p9 明确 ASTM D638 Type IV **只用于 parent materials**；v02 只表达其试片在 Z100 上的简化配置，不能拿来表示 PIM 的机械记忆结构。

前轮 AGH 图像窗口发现服务故障，AGH **尚未自行看见图版像素**。本轮用户作为“外部复核”实际逐张看本地补图并明确：Fig.17 parent-material Type IV；Fig.18 左栏 20×20 mm 交织 PIM/CIM 试样，中栏压缩夹持实拍，右栏 DIC 斑点样本；Fig.19 为 15×25 mm 复合结构拉/压/外骨骼/单指多场景；Fig.20 为人体组织样本及单指/脚趾弯曲。此报告足够**划定 Fig.18 独立候选范围**，不足以确定真实三维厚度、每个铰接/交织节点或力学性能；这些若建模仅作假设。v02 仍只代表 Fig.17；不得将 Fig.19/20 混成新候选或将其标验收。外部逐图反馈原表见 `EXTERNAL_HUMAN_REVIEW.md`。

本轮依外部复核 Fig.18 的像素描述新增**独立** `cases/18_mechanical_nature/v03_fig18_PIM_CIM/{scene.blend,overview.png,target_audit.json}`。Fig.18 左 20×20 mm 面与中压板作源锚，交织层的 7×7 条可编辑样条只是**可见面格构的代表性假设**，不等于真实交织节点或全部三维厚度；未叠右侧 DIC 斑点，也未引入 Fig.19/20。v02 Fig.17 parent-material 原样保留。独立重开/局部结构审计不是图像/力学认可。
