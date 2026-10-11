# 图注标签层（与 3D 场景分离；3D 渲染本身无字 —— 需求 B5）
# 用法：在 Blender 中打开 scene_case2.blend 时，可把下列文字对象加到独立 Collection「labels」，
# 或导出为可编辑文本层（每个标签一个 3D 文本对象，定位到对应部件附近）。
# 标签词与 Fig.2(a) 参考图一致（记录命名差异：BS=图注泛指，正文该位置为 dichroic prism）。

对象 -> 标签词 -> 3D 文本位置(m, 近对应部件上方)
pulse_laser   -> "Pulse laser"    -> (0.00, 0, 0.06)
lens_L1       -> "L1"             -> (0.10, 0, 0.06)
lens_L2       -> "L2"             -> (0.20, 0, 0.06)
mirror_M1     -> "M1"             -> (0.30, 0, 0.06)
mirror_M2     -> "M2"             -> (0.40, 0, 0.06)
dmd           -> "DMD / Hologram" -> (0.50, 0, 0.06)
lens_L3       -> "L3"             -> (0.60, 0, 0.06)
iris1         -> "Iris"           -> (0.66, 0, 0.06)
lens_L4       -> "L4"             -> (0.72, 0, 0.06)
bs_dichroic   -> "BS(dichroic)"   -> (0.80, 0, 0.06)
hwp           -> "HWP"            -> (0.84, 0, 0.06)
polarizer     -> "Polarizer"      -> (0.87, 0, 0.06)
slm           -> "Phase / SLM"    -> (0.92, 0, 0.06)
mirror_M3     -> "M3"             -> (1.02, 0, 0.06)
lens_L5       -> "L5"             -> (1.12, 0, 0.06)
iris2         -> "Iris"           -> (1.18, 0, 0.06)
lens_L6       -> "L6"             -> (1.24, 0, 0.06)
lens_L7       -> "L7"             -> (1.32, 0, 0.06)
holder        -> "Holder"         -> (1.40, 0, 0.06)
mmf_delay_1/2/3 -> "MMF(2/4/6 m)" -> (1.40, ∓0.02/0, 0.05)  # 三条延迟线束，标注 2/4/6 m 折叠成束
bc_combiner   -> "BC (3×1)"       -> (1.50, 0, 0.06)
mmf_single    -> "MMF"            -> (1.56, 0, 0.05)
pd            -> "PD"             -> (1.62, 0, 0.06)
oscilloscope  -> "Oscilloscope"   -> (1.70, 0, 0.08)

说明：
- 3D 渲染保持无字（wordless）；本层为独立可编辑标签（每词一个文本对象，可开关/移动）。
- "Hologram"(DMD)、"Phase"(SLM) 是图案/相位分布示意，标签保留但不对应独立物理板。
- BS 标签注明 dichroic，如实记录图注/正文命名差异。
- 若用 Blender 文本对象：bpy.ops.object.text_add + data.body=标签词 + 3D 定位；放独立 Collection "labels"。
