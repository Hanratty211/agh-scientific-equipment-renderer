"""V27 acoustic levitation liquid marble build_v01.py
Acoustic levitation cavity + liquid marble sample + BOS backlight + support stand.
Based on arXiv:2610.07703 (airborne liquid marble evaporation, 8-page PDF).
Key features from PDF text:
  - acoustic levitation cavity (quartz glass cell or metallic cavity with transducer)
  - liquid marble: droplet encapsulated by hydrophobic particle shell (LYCO spores)
  - BOS (Background Oriented Schlieren) measurement with back-light and camera
  - transducer generates standing wave at acoustic node
"""
import bpy, math, mathutils, os, hashlib

def setup():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    sc.render.resolution_x = 1280
    sc.render.resolution_y = 960
    sc.render.engine = 'BLENDER_EEVEE'
    sc.render.image_settings.file_format = 'PNG'
    w = bpy.data.worlds.new("W")
    bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.04, 0.04, 0.05, 1.0)
    return sc

def mat(name, base, rough=0.5, metal=0.0, emis=None, es=0.0, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    if alpha < 1.0:
        m.blend_method = 'BLEND'
        m.show_transparent_back = False
    n = m.node_tree.nodes.get("Principled BSDF")
    n.inputs["Base Color"].default_value = base + (alpha,)
    n.inputs["Roughness"].default_value = rough
    n.inputs["Metallic"].default_value = metal
    if emis:
        n.inputs["Emission Color"].default_value = emis + (1.0,)
        n.inputs["Emission Strength"].default_value = es
    tw = n.inputs.get("Transmission Weight")
    if tw: tw.default_value = 1.0 - alpha
    return m

def box(name, sx, sy, sz, loc, m=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object; o.name = name; o.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if m: o.data.materials.append(m)
    return o

def cyl(name, r, depth, loc, rot=(0,0,0), m=None, seg=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=seg)
    o = bpy.context.object; o.name = name
    if m: o.data.materials.append(m)
    return o

def sphere(name, r, loc, m=None, seg=24, rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=rings)
    o = bpy.context.object; o.name = name
    if m: o.data.materials.append(m)
    return o

sc = setup()

# ==== Dimensions (m, scene ~ cm/1000) ====
C_R = 0.04    # cavity radius
C_H = 0.10    # cavity height
Z0 = 0.05     # cavity bottom z (on stand)
Zmid = Z0 + C_H/2
Ztop = Z0 + C_H
LZ = Zmid + 0.015   # levitation z (slightly above center)
MR = 0.008          # marble radius

# ==== Materials ====
M_cav   = mat("cavity_wall", (0.70,0.70,0.75), rough=0.3, metal=0.4, alpha=0.15)  # quartz glass, very transparent
M_cav2  = mat("cav_dark",    (0.30,0.30,0.35), rough=0.4, metal=0.3)               # inner wall
M_trans = mat("transducer",  (0.10,0.10,0.12), rough=0.5, metal=0.7)              # PZT transducer
M_marb  = mat("marble_core", (0.05,0.30,0.60), rough=0.1, alpha=0.5, emis=(0.05,0.2,0.5), es=0.5)  # droplet
M_shell = mat("marble_shell",(0.85,0.70,0.40), rough=0.6, metal=0.0, emis=(0.8,0.6,0.2), es=0.3)   # particle shell
M_stand = mat("stand",       (0.20,0.18,0.15), rough=0.6, metal=0.4)
M_lens  = mat("lens_glass",  (0.90,0.92,0.95), rough=0.05, alpha=0.3)
M_bolts = mat("bolts",       (0.50,0.50,0.55), rough=0.3, metal=0.7)
M_back  = mat("backlight",   (1.00,0.95,0.80), rough=0.1, emis=(1.0,0.95,0.8), es=6.0)  # BOS backlight
M_cam   = mat("camera_body", (0.08,0.08,0.10), rough=0.4, metal=0.3)
M_beam  = mat("boos_beam",   (1.0,1.0,0.95), rough=0.05, emis=(1,1,0.95), es=4.0)

# ==== Acoustic cavity: two mirrored quarter-wave resonators (standard acoustic levitator) ====
# Top resonator (inverted cone/cylinder)
# Bottom cone (wide base → narrow top, forming standing wave node)
# Simplified: two vertical cylinders with conical transition
top_cyl = cyl("cav_top_cyl", C_R, C_H*0.4, (0, 0, Ztop - C_H*0.2), (0,0,0), M_cav, seg=64)
bot_cyl = cyl("cav_bot_cyl", C_R, C_H*0.4, (0, 0, Z0 + C_H*0.2), (0,0,0), M_cav, seg=64)
# Conical transition (top half)
# Use truncated cone: cylinder with scale trick — use a cone primitive
bpy.ops.mesh.primitive_cone_add(radius1=C_R*0.6, radius2=C_R, depth=C_H*0.2, location=(0, 0, Ztop - C_H*0.2 - C_H*0.1), vertices=64)
o = bpy.context.object; o.name = "cav_cone_top"; o.data.materials.append(M_cav)
# Bottom cone
bpy.ops.mesh.primitive_cone_add(radius1=C_R*0.6, radius2=C_R, depth=C_H*0.2, location=(0, 0, Z0 + C_H*0.2 + C_H*0.1), rotation=(math.pi,0,0), vertices=64)
o = bpy.context.object; o.name = "cav_cone_bot"; o.data.materials.append(M_cav)
# Narrow center (where standing wave node forms)
cyl("cav_narrow", C_R*0.6, C_H*0.1, (0, 0, Zmid), (0,0,0), M_cav, seg=48)

# Inner wall (slightly darker, not occluding)
cyl("cav_inner", C_R*0.58, C_H*0.6, (0, 0, Zmid), (0,0,0), mat("cav_inner_mat", (0.55,0.55,0.60), rough=0.5, metal=0.2), seg=48)

# ==== Transducer (PZT) on bottom face of lower resonator ====
trans = cyl("transducer", C_R*0.7, 0.005, (0, 0, Z0 - 0.0025), (0,0,0), M_trans, seg=48)
# Transducer wire connector
cyl("trans_wire", 0.003, 0.02, (C_R*0.5, 0, Z0 - 0.015), (0, math.pi/2, 0), M_trans, seg=16)

# ==== Liquid marble (levitating at acoustic node) ====
# Core droplet (semi-transparent water)
core = sphere("marble_core", MR*0.8, (0, 0, LZ), M_marb, seg=32, rings=16)
# Particle shell (lycopodium spores, slightly larger, textured look via emissive)
shell = sphere("marble_shell", MR, (0, 0, LZ), M_shell, seg=32, rings=16)

# ==== Support stand (cavity rests on this) ====
box("stand_base", C_R*3, C_R*3, 0.01, (0, 0, 0.005), M_stand)
# Stand legs
for i,(lx,ly) in enumerate([(-C_R*1.2,-C_R*1.2),(C_R*1.2,-C_R*1.2),(-C_R*1.2,C_R*1.2),(C_R*1.2,C_R*1.2)]):
    cyl(f"stand_leg_{i}", 0.008, Z0-0.01, (lx, ly, (Z0-0.01)/2), (0,0,0), M_stand, seg=16)

# ==== BOS back-light panel (behind cavity, -X direction) ====
# Rectangular LED panel
bl_x = -C_R - 0.06
box("backlight_panel", 0.005, C_H*1.5, C_H*1.5, (bl_x, 0, Zmid), M_back)
# BOS beam (horizontal, through cavity center)
# From backlight to opposite side
beam_end = (C_R + 0.05, 0, LZ)
p0 = (bl_x + 0.004, 0, LZ)
v = mathutils.Vector(beam_end) - mathutils.Vector(p0)
mid = (mathutils.Vector(p0) + mathutils.Vector(beam_end)) / 2
rot = v.to_track_quat('Z','Y').to_euler()
o = cyl("bos_beam", 0.015, v.length, tuple(mid), tuple(rot), M_beam, seg=16)
o['beam_p0'] = tuple(p0); o['beam_p1'] = tuple(beam_end)

# ==== Camera / optical path (perpendicular to BOS beam, +Y direction) ====
# Camera on +Y stand
cam_y = C_H + 0.08
box("cam_stand", 0.06, 0.02, Zmid - 0.01, (0, cam_y, (Zmid-0.01)/2 + 0.01), M_stand)
box("camera_body", 0.06, 0.04, 0.05, (0, cam_y, Zmid), M_cam)
cyl("camera_lens", 0.015, 0.02, (0, cam_y - 0.02, Zmid), (math.pi/2, 0, 0), M_lens, seg=32)
# Schlieren/lens in front of camera
cyl("schlieren_lens", 0.012, 0.01, (0, cam_y - 0.04, Zmid), (math.pi/2, 0, 0), M_lens, seg=32)

# ==== Control electronics (small box on stand) ====
box("ctrl_box", 0.08, 0.05, 0.03, (C_R + 0.06, -C_R - 0.04, 0.015), M_trans)
cyl("ctrl_wire", 0.003, 0.05, (C_R + 0.02, -C_R - 0.02, 0.03), (math.pi/4, 0, 0), M_trans, seg=12)

# ==== Render camera ====
cam_pos = (0.25, -0.22, 0.20)
cam_tgt = (0.0, 0.01, Zmid)
d = mathutils.Vector(cam_tgt) - mathutils.Vector(cam_pos)
q = (-d).to_track_quat('Z','Y')
bpy.ops.object.camera_add(location=cam_pos, rotation=q.to_euler())
c = bpy.context.object
c.data.lens = 55; c.data.clip_start = 0.01; c.data.clip_end = 50
sc.camera = c

# Lights
for pos, e in [((0.3, 0.1, 0.30), 80), ((-0.2, 0.3, 0.20), 50), ((0.0, -0.25, 0.15), 40)]:
    bpy.ops.object.light_add(location=pos, type='POINT')
    bpy.context.object.data.energy = e

# Save & render
out_blend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scene_v01.blend")
out_png   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overview_v01.png")
sc.render.filepath = out_png
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)

with open(out_png,'rb') as f: h = hashlib.sha256(f.read()).hexdigest()
print(f"V27_BUILD_OK blend={out_blend} png={out_png} sha256={h}")
