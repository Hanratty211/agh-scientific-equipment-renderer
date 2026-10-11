# Fig.2(a) v4 无字总览低成本草案（2026-10-11）

**交付**：`build_case2_v4_overview.py` → `render-output/scene_case2_v4_overview.blend`、`render-output/case2_v4_overview_wordless.png`（1200×750、Cycles 24 samples）；独立只读核查 `verify_case2_v4_overview.py` / `verify_case2_v4_overview_results.txt`。旧 v1/v2/v3 .blend 和 R10 标注文件均未改。本轮没有新参考图标注，不出正式图，Skill 保持草案。

## 依据与建模范围
- 原 Fig.2(a) 已通过 Preview 实际查看（先前成功的 `computer_use` capture）。器件粗相对关系：激光右下→L1/L2→M1→M2→左侧 DMD→L3/Iris/L4/HWP/Polarizer/BS→右侧反射式 SLM；回光到 BS 后折向 M3→L5/Iris/L6/L7→左上 Holder/3 根盘绕 MMF→BC→单 MMF→PD→示波器。**R10 偏移的青色描线点未导入建模脚本**；二维阻挡是再次参照原图按器件视觉区位建立的示意坐标，不是安装实测。
- PDF p.8：DMD 入射 12°；本模型参考宏观平面相对入射线旋转 12°，未解析微镜布拉格/衍射细节。PDF p.9：SLM 加载相位图加 blazed grating，使零级与目标光场空间分离；正文说 dichroic prism 与 M3 反射调制后的光。**不说 BS 按波长/偏振把零级分给 M3**。SLM 是反射式器件，路径 BS→SLM 正面→BS→M3，不穿 SLM 背面。BS 端口角度与零级支路细节未确认。
- 1064 nm 红色线是原图**示意配色**，不是肉眼可见激光。光学段穿过带厚度的透镜/波片，由正背面锚点连接；镜面及 SLM/BS 使用实际面求交，不用 bbox 极值。Iris 是带通孔的环体。三根光纤是带截面的连续曲线分别从 Holder 表面到 BC 表面，圈数/直径均仅视觉示意；BC→PD 单纤连续，PD→示波器是不同材质的电信号线。装置下缘高于地面真实顶面；3D 场景无字。

## 核验与视觉限制
- `Blender -b --factory-startup -P build_case2_v4_overview.py`：exit 0，保存 .blend 与 PNG。`Blender -b --factory-startup --python verify_case2_v4_overview.py`：exit 0；六个指定光学作用点到真实网格表面 <0.05 mm；M1/M2/M3 实际网格法向计算的反射方向与下游段同向（dot≈1）；反射式 SLM 返回 BS；三根可渲染曲线/BC→PD/PD→示波器连接存在；22 件关键件最低角点均高于地面顶面且全部角点投影入相机框。**几何检查不能证明遮挡、可读性或复刻通过。**
- **未完成新 PNG 的模型视觉审查**：本轮 `computer_use` 的 `list_windows`、`capture(app='预览')` 连续报 *Computer Use windows discovery failed*，无法实际看到新 PNG。PNG 文件的尺寸/sha256 仅证明版本，不能代替像素视觉比较。未以亮度或部件数量声称视觉通过。请外部读磁盘正确版本并反馈，之后再针对图片修明显问题。

## 与参考图预计最明显的三处差异（**设计差异，不是已完成的并排像素判词**）
1. 原图包含 Hologram/Phase 的示意图案和器件文字；本交付要求**无字**，只造 DMD/SLM 实体，不造独立的图案板或标签。
2. 激光器、镜座、探测器和示波器用可辨识的简化几何外形，未复刻参考图的具体品牌结构/面板细节。
3. 三根延迟 MMF 在局部用简化环绕线表达而非实际 2/4/6 m 长度；缆线走向和接口为视觉示意，不等同原图的具体卷绕形状。

## 仍未确认
BS/dichroic 的具体返回光端口、SLM 零级另一路是否可在该图中辨认；透镜焦距/间距和安装角度；真实镜座形状、光纤绕圈尺寸；**新图相对参考的真实视觉差异排名/遮挡与可读性**（等实际读图后确定）。
