#!/usr/bin/env python3
"""从 scene_case2_v2.blend 生成可编辑 SVG 标签层 + 叠加带标签预览。
标签与 3D 场景分离（3D 渲染本身无字）；每个标签一个 <text>+引线，可编辑。
"""
import bpy, mathutils, os
from mathutils import Vector
import bpy_extras
HERE = "/Users/wht/Desktop/黑客松/agh-research-figure-skill/case-2_D2NN_OAM2"
bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, "render-output", "scene_case2_v2.blend"))
bpy.context.view_layer.update()
scene = bpy.context.scene
cam = bpy.data.objects["cam_overview"]
W, H = scene.render.resolution_x, scene.render.resolution_y

# 用 Blender 官方 3D→2D 投影（处理相机朝向/焦距/传感器，比手算准）
def project(world_pt):
    res = bpy_extras.object_utils.world_to_camera_view(
        bpy.context.scene, cam, Vector(world_pt))
    # Blender 5.x 返回 [x, y] 浮点列表（归一化 0-1）
    if isinstance(res, (list, tuple)):
        co = res
    else:
        co = (res.x, res.y)
    px = co[0] * W
    py = (1 - co[1]) * H
    if not (-0.2 <= co[0] <= 1.2 and -0.2 <= co[1] <= 1.2):
        return None
    return px, py

labels = {
    "pulse_laser": "Pulse laser", "lens_L1": "L1", "lens_L2": "L2",
    "mirror_M1": "M1", "mirror_M2": "M2", "dmd": "DMD / Hologram",
    "lens_L3": "L3", "iris1": "Iris", "lens_L4": "L4", "bs_dichroic": "BS(dichroic)",
    "hwp": "HWP", "polarizer": "Polarizer", "slm": "Phase / SLM", "mirror_M3": "M3",
    "lens_L5": "L5", "iris2": "Iris", "lens_L6": "L6", "lens_L7": "L7", "holder": "Holder",
    "mmf_delay_1": "MMF 2m", "mmf_delay_2": "MMF 4m", "mmf_delay_3": "MMF 6m",
    "bc_combiner": "BC (3×1)", "mmf_single": "MMF", "pd": "PD", "oscilloscope": "Oscilloscope",
}
items = []
for nm, txt in labels.items():
    o = bpy.data.objects.get(nm)
    if not o:
        continue
    p = project(o.matrix_world.translation + Vector((0, 0, 0.08)))
    if p:
        items.append((p[0], p[1], txt, nm))
if not items:
    # 总览相机可能太窄：放宽并直接取所有件世界坐标投影
    for nm, txt in labels.items():
        o = bpy.data.objects.get(nm)
        if not o:
            continue
        p = project(o.matrix_world.translation)
        if p:
            items.append((p[0], p[1], txt, nm))

svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
       'font-family="Helvetica,Arial" font-size="22" fill="white" stroke="white" stroke-width="1.5">' % (W, H, W, H)]
svg.append('  <!-- 可编辑标签层：3D 场景无字；本 SVG 与 3D 分离。data-target 对应 3D 对象名。 -->')
for x, y, txt, nm in items:
    svg.append(f'  <line x1="{x:.0f}" y1="{y:.0f}" x2="{x:.0f}" y2="{y-18:.0f}" opacity="0.6"/>')
    svg.append(f'  <text x="{x+4:.0f}" y="{y-22:.0f}" data-target="{nm}">{txt}</text>')
svg.append('</svg>')
out = os.path.join(HERE, "render-output", "case2_v2_label_layer.svg")
open(out, "w").write("\n".join(svg))
print("SVG label layer written:", out, "labels:", len(items))

# 叠加到总览 PNG 生成带标签预览（PIL）
try:
    from PIL import Image, ImageDraw
    import xml.etree.ElementTree as ET
    base = Image.open(os.path.join(HERE, "render-output", "case2_v2_overview_wordless.png")).convert("RGB")
    root = ET.parse(out)
    draw = ImageDraw.Draw(base)
    for el in root:
        if el.tag == "text":
            t = el.text or ""
            x = float(el.get("x", 0)); y = float(el.get("y", 0))
            draw.text((x, y), t, fill=(255, 255, 255))
        elif el.tag == "line":
            x1 = float(el.get("x1")); y1 = float(el.get("y1"))
            x2 = float(el.get("x2")); y2 = float(el.get("y2"))
            draw.line((x1, y1, x2, y2), fill=(255, 255, 255), width=1)
    out2 = os.path.join(HERE, "render-output", "case2_v2_overview_labeled.png")
    base.save(out2)
    print("labeled preview written:", out2)
except Exception as e:
    print("label overlay skipped:", e)
