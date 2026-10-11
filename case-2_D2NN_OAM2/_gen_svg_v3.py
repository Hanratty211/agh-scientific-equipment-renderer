#!/usr/bin/env python3
"""v3：生成可编辑 SVG 标签层 + 真正渲染合成带标签 PNG。
标签锚点依据【当前世界空间几何位置】（对象 world 坐标，非对象默认原点/非光纤起点）。
核查带标签 vs 无字确有对应文字像素差异（PIL 实际合成，非"像素相同"）。
"""
import bpy, os
from mathutils import Vector
import bpy_extras
HERE = "/Users/wht/Desktop/黑客松/agh-research-figure-skill/case-2_D2NN_OAM2"
bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, "render-output", "scene_case2_v3.blend"))
bpy.context.view_layer.update()
scene = bpy.context.scene
cam = bpy.data.objects["cam_overview"]
W, H = scene.render.resolution_x, scene.render.resolution_y

def project(world_pt):
    co = bpy_extras.object_utils.world_to_camera_view(scene, cam, Vector(world_pt))
    if isinstance(co, (list, tuple)):
        co = co[0], co[1]
    px, py = co[0]*W, (1-co[1])*H
    if not (-0.15 <= co[0] <= 1.15 and -0.15 <= co[1] <= 1.15):
        return None
    return px, py

# 标签 → 世界锚点（用对象世界坐标，非默认原点；光纤用曲线首端点世界坐标）
def obj_anchor(nm):
    o = bpy.data.objects.get(nm)
    if not o:
        return None
    if o.type == 'CURVE':
        # 光纤锚点取曲线首控制点世界坐标（非对象原点）
        sp = o.data.splines[0]
        co = sp.bezier_points[0].co
        return o.matrix_world @ Vector(co)
    return o.matrix_world.translation

labels = {
    "pulse_laser":"Pulse laser","lens_L1":"L1","lens_L2":"L2",
    "mirror_M1":"M1","mirror_M2":"M2","dmd":"DMD / Hologram",
    "lens_L3":"L3","iris1":"Iris","lens_L4":"L4","bs_dichroic":"BS(dichroic)",
    "hwp":"HWP","polarizer":"Polarizer","slm":"Phase / SLM","mirror_M3":"M3",
    "lens_L5":"L5","iris2":"Iris","lens_L6":"L6","lens_L7":"L7","holder":"Holder",
    "mmf_delay_1":"MMF 2m","mmf_delay_2":"MMF 4m","mmf_delay_3":"MMF 6m",
    "bc_combiner":"BC (3×1)","mmf_single":"MMF","pd":"PD","oscilloscope":"Oscilloscope",
}
items = []
for nm, txt in labels.items():
    a = obj_anchor(nm)
    if a is None:
        continue
    p = project(a + Vector((0, 0, 0.06)))
    if p:
        items.append((p[0], p[1], txt, nm, a))
    else:
        p = project(a)
        if p:
            items.append((p[0], p[1], txt, nm, a))

# 生成 SVG
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
       'font-family="Helvetica,Arial" font-size="22" fill="white" stroke="white" stroke-width="1.5">' % (W, H, W, H)]
svg.append('  <!-- 可编辑标签层 v3：锚点=对象世界几何位置；3D 场景无字 -->')
for x, y, txt, nm, _a in items:
    svg.append(f'  <line x1="{x:.0f}" y1="{y:.0f}" x2="{x:.0f}" y2="{y-18:.0f}" opacity="0.6"/>')
    svg.append(f'  <text x="{x+4:.0f}" y="{y-22:.0f}" data-target="{nm}">{txt}</text>')
svg.append('</svg>')
out_svg = os.path.join(HERE, "render-output", "case2_v3_label_layer.svg")
open(out_svg, "w").write("\n".join(svg))
print("SVG v3 written:", out_svg, "labels:", len(items))
for it in items:
    print(f"   {it[3]:20s} 锚点world={tuple(round(v,3) for v in it[4])} -> px=({it[0]:.0f},{it[1]:.0f})")

# 真正渲染合成带标签 PNG（PIL）
from PIL import Image, ImageDraw, ImageFont
base = Image.open(os.path.join(HERE, "render-output", "case2_v3_overview_wordless.png")).convert("RGB")
ov = Image.new("RGBA", base.size, (0,0,0,0)); od = ImageDraw.Draw(ov)
font = None
for f in ["/System/Library/Fonts/Helvetica.ttc","/System/Library/Fonts/Supplemental/Arial.ttf"]:
    try: font = ImageFont.truetype(f, 24); break
    except: pass
import xml.etree.ElementTree as ET
root = ET.parse(out_svg).getroot()
for el in root:
    if el.tag == "line":
        od.line((float(el.get("x1")),float(el.get("y1")),float(el.get("x2")),float(el.get("y2"))),
                fill=(30,30,30,220), width=1)
    elif el.tag == "text":
        od.text((float(el.get("x")),float(el.get("y"))), el.text or "",
                font=font, fill=(255,255,255,255), stroke_width=2, stroke_fill=(20,20,20,255))
out_png = os.path.join(HERE, "render-output", "case2_v3_overview_labeled.png")
Image.alpha_composite(base.convert("RGBA"), ov).convert("RGB").save(out_png)
print("labeled PNG v3 written:", out_png)

# 核查带标签 vs 无字确有文字像素差异（不沿用 v2 "像素完全相同"）
import numpy as np
a0 = np.array(base.convert("RGB")).astype(np.int32)
a1 = np.array(Image.open(out_png).convert("RGB")).astype(np.int32)
diff = (np.abs(a0 - a1).max(axis=2) > 8).mean()
print(f"带标签 vs 无字 像素差异比例 = {diff:.4f}  (v2 为 0.0；v3 应 > 0 表示标签真实进入预览)")
