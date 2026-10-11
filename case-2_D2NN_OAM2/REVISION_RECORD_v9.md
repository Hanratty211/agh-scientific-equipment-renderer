# Fig. 2(a) v9｜低成本无字总览（草稿）

- **基线**：v8 文件保留；出光口按外部 v8 读图意见冻结，仅作为示意结构，孔位、尺寸未测定。未修改光路拓扑、公共轴、平凸透镜、BS 作用面、器件接口和光束中心线。
- **本轮改变**：L4→HWP→偏振片→BS 的展示半径统一为 10 mm（示意准直）；Iris2→L6→L7 展示扩束，L7→Holder 展示聚焦。束宽由相邻器件处的共享半径连续插值；把高光红棒材质换为红色着色透明＋弱自发光包络。激光器、PD、示波器仅补壳体接缝/正顶面材质层次；M1/M2 后部补暗色支撑，不动镜面。镜片仍透光。焦距、束腰、光束色彩及外观细节均为展示假设；1064 nm 不可据示意红色推定为可见红光。
- **取景**：同一相机位置与朝向；正交宽度 1.98→1.90 m、画布 1280×720→1280×660，扩大灰色桌面底板以避免边缘入镜；没有挪动器件。仅渲染一张 v9 PNG，不重渲出光口、不做正式图或标注。
- **本会话执行**：`/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_case2_v9_overview.py` 返回 0，生成 `render-output/scene_case2_v9_overview.blend` 与 `render-output/case2_v9_overview_wordless.png`（1280×660）。随后 `Blender -b --factory-startup --python verify_case2_v9_overview.py` 返回 0；`verify_case2_v9_overview_results.txt` 记载 275 PASS、0 FAIL。独立打开 v8/v9 保存场景比较：冻结器件的网格、世界位姿、光学接口和全部光束中心线指纹相同（两版均 `91ad0938da66b36a` 前 16 位）；主要器件全部角点入框、桌面覆盖相机四角、垂直范围 0.1052—0.8501。此处只证明几何与设置，不证明画面可读或与原图视觉等价。
- **文件 SHA-256**：PNG `91d0814d1280c8d0002d6b2f312d414a44ead49dd65c412e2192f52225b3a1ed`；.blend `4c9e02d82d9a9b5119e0e8fb6fe73ca81e6508c5f07cf28c38b1bd6a33489445`。
- **未完成**：本轮按要求没有调用 Preview、桌面截图或读取新 PNG 像素。实际视觉对应、红束透明度和仪器辨识度待外部读图；Skill 仍是草案，不声明通用验证通过。
