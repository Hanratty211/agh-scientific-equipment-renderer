# v10 红束显示方案对比（未应用到总览）

**唯一交付预览**：`render-output/case2_v10_material_comparison.png`（3012×422；SHA-256 `65958f48e79f3c76d1450df026354d06916f1bdf7fb8d5a3491329c1f8d8e048`）。左／中／右依次是红色显示混合权重 0.6／0.8／1.0；对应 Emission 强度 0.90／0.70／0.56，近似协调显示通量，不能解读为测量值。各档 Transparent BSDF 都为中性白色，Emission 为较纯的显示红色 `(1,.002,.001)`；无光泽 BSDF、无合成泛光。权重 1.0 是不透明对照，可能遮挡镜片，不能因红色更纯就判定通过。

三档从**同一未改动的 v10 .blend** 临时渲染 Iris2—L6—L7—Holder（含 L6/L7 镜片），沿用其**同一 overview_camera、照明、曝光、场景、裁切边框**；只改变光束材质，三次仅裁切局部、不批量渲染总览。临时裁切文件在合成后删除；未保存新 .blend，未修改 v10 PNG。可重跑：`python3 compare_case2_v10_beam_material.py`（调用内部 `render_case2_material_tiles.py`）。

**本会话执行证据**：初次直接在 Blender 中 `import PIL` 因模块缺失而在渲染前失败；改为 Blender 裁切渲染＋系统 Python/Pillow 合成后返回 0。日志确认三个裁切共用相机 `overview_camera`、边框 `(0.3183,0.8328,0.4269,0.7461)`；PNG 像素检查显示红色优势像素约 8021／16344／16512，RGB 近白三通道饱和比例均 0。这是实际像素统计，**不证明镜片可读或色彩视觉通过**；具体候选由外部看图选择。本轮未调用 Preview 或桌面截图、未把候选应用至总览。1064 nm 并非真实可见红色光束。
