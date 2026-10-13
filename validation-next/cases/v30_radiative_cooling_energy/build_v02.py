"""V30 build_v02.py — bottom-face up view (flipped), chip alpha=0.08,
VCSEL/PD/LiPo/USB-C/gold wires/UV beam all visible.
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
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.02, 0.03, 0.06, 1.0)
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

def wire(name, p0, p1, r=0.000008, m=None):
    v = mathutils.Vector(p1)-mathutils.Vector(p0)
    mid = (mathutils.Vector(p0)+mathutils.Vector(p1))/2
    rot = v.to_track_quat('Z','Y').to_euler()
    o = cyl(name, r, v.length, tuple(mid), tuple(rot), m, seg=12)
    o['wire_p0'] = tuple(p0); o['wire_p1'] = tuple(p1)
    return o

sc = setup()

# ==== Materials ====
# Chip: very low alpha so bottom components are clearly visible through it
M_sapphire = mat("sapphire_v2", (0.40,0.55,0.95), rough=0.05, metal=0.0, alpha=0.08)
M_vcsel    = mat("vcsel_white", (0.95,0.95,0.98), rough=0.15, metal=0.3)
M_algan    = mat("algan_mesa",  (0.70,0.80,0.90), rough=0.2, metal=0.1)
M_aln      = mat("aln_sub",     (0.98,0.98,0.98), rough=0.1, metal=0.0)
M_sipd     = mat("si_pd_dark",  (0.05,0.05,0.08), rough=0.3, metal=0.8)
M_filter   = mat("lp_filter",   (0.25,0.35,0.95), rough=0.1, metal=0.0, alpha=0.40)
M_chiplet  = mat("ic_chip",     (0.02,0.18,0.02), rough=0.3, metal=0.4)
M_ceramic  = mat("ic_substrate",(0.80,0.75,0.60), rough=0.4, metal=0.0)
M_lipo     = mat("lipo_purple", (0.45,0.20,0.75), rough=0.4, metal=0.1)
M_usb      = mat("usb_silver",  (0.85,0.85,0.90), rough=0.2, metal=0.9)
M_gold     = mat("gold_trace",  (1.00,0.80,0.10), rough=0.1, metal=0.9, emis=(1,0.8,0.1), es=0.4)
M_ant      = mat("antenna",     (0.08,0.08,0.10), rough=0.5, metal=0.6)
M_well     = mat("sample_well", (0.05,0.05,0.08), rough=0.6)
M_house    = mat("housing",     (0.20,0.20,0.22), rough=0.5, metal=0.4, alpha=0.30)
M_beams    = mat("uv_beam",     (0.55,0.20,1.00), rough=0.05, emis=(0.55,0.20,1.0), es=5.0)
M_flor     = mat("fl_r",        (0.20,0.90,0.30), rough=0.05, emis=(0.2,0.9,0.3), es=4.0)
M_base     = mat("bench",       (0.12,0.12,0.14), rough=0.5, metal=0.5)

# ==== Dimensions ====
CW, CD, CT = 0.020, 0.050, 0.004   # chip 20mm x 50mm x 4mm
Z0 = 0.0                            # bottom face z
Ztop = CT                           # top face z
H  = 0.012                         # housing depth below chip

# ==== Housing (semi-transparent, not fully occluding) ====
box("housing", CW+0.008, CD+0.008, H, (0, 0, -H/2), M_house)
# Bench base
box("bench_base", CW+0.04, CD+0.04, 0.005, (0, 0, -H-0.0025), M_base)

# ==== Sapphire chip (extremely transparent, alpha=0.08) ====
box("sapphire_chip", CW, CD, CT, (0, 0, CT/2), M_sapphire)

# ==== VCSEL on bottom face (centered slightly left) ====
VX, VY = -0.004, 0.0
# AlN substrate
box("vcsl_aln_sub", 0.0004, 0.0004, 0.00005, (VX, VY, -0.000025), M_aln)
# p-DBR
box("vcsl_p_dbr", 0.0004, 0.0004, 0.000008, (VX, VY, -0.000058), M_vcsel)
# Active mesa (cylinder, AlGaN)
cyl("vcsl_mesa", 0.00014, 0.000004, (VX, VY, -0.000063), (0,0,0), M_algan, seg=32)
# n-DBR
box("vcsl_n_dbr", 0.0004, 0.0004, 0.000008, (VX, VY, -0.000072), M_vcsel)
# p-pad (gold disc on mesa)
cyl("vcsl_p_pad", 0.00006, 0.000004, (VX, VY, -0.000065), (0,0,0), M_gold, seg=20)
# n-pad (gold rect)
box("vcsl_n_pad", 0.00015, 0.00008, 0.000004, (VX+0.00025, VY, -0.000073), M_gold)

# Wire bonds (gold, thin but visible with emis)
wire("wire_p", (VX, VY, -0.000065), (VX-0.0008, VY+0.003, -0.0002), r=0.000012, m=M_gold)
wire("wire_n", (VX+0.00025, VY, -0.000073), (VX+0.0008, VY+0.003, -0.0002), r=0.000012, m=M_gold)

# ==== Si photodetector (right of VCSEL) ====
PD_X, PD_Y = 0.004, 0.0
box("si_pd", 0.003, 0.006, 0.0005, (PD_X, PD_Y, -0.00025), M_sipd)
box("pd_filter", 0.0028, 0.0058, 0.0001, (PD_X, PD_Y, -0.00055), M_filter)

# ==== Electronic chiplets (IC dies on ceramic substrates) ====
def chiplet(name, x, y, w=0.002, d=0.002, z=-0.0004):
    box(f"{name}_sub", w+0.0008, d+0.0008, 0.0003, (x, y, z), M_ceramic)
    box(f"{name}_die", w, d, 0.00008, (x, y, z+0.00022), M_chiplet)
    for i in range(3):
        cyl(f"{name}_pin{i}", 0.00005, 0.00005, (x-w/3+i*2*w/3, y, z-0.00025), (0,0,0), M_gold, seg=12)

chiplet("ld_drv",  -0.007, 0.014)
chiplet("tia",     -0.007, -0.014)
chiplet("adc",       0.007, 0.014)
chiplet("esp32",     0.007, -0.014, w=0.003, d=0.004)
chiplet("tp4056",    0.007, -0.024, w=0.0015, d=0.0015)
chiplet("boost",    -0.007, -0.024, w=0.0015, d=0.0015)
chiplet("ldo",       0.007, 0.024, w=0.0015, d=0.0015)

# ==== LiPo battery (purple, prominent) ====
box("lipo", 0.010, 0.005, 0.003, (-0.004, -0.020, -0.0015), M_lipo)
box("lipo_conn", 0.005, 0.002, 0.0008, (-0.004, -0.025, -0.0004), M_gold)

# ==== USB-C port ====
box("usb_c", 0.002, 0.0012, 0.0035, (0.008, -0.020, -0.00175), M_usb)
cyl("usb_shell", 0.0011, 0.0045, (0.008, -0.020, -0.00175), (0,0,math.pi/2), M_usb, seg=16)

# ==== Wi-Fi antenna (5 meander segments on top face) ====
ant_x0, ant_y0 = 0.005, 0.019
for i in range(5):
    x = ant_x0 + i*0.0012
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, ant_y0 + (i%2)*0.0009, Ztop+0.00005))
    o = bpy.context.object
    o.name = f"wifi_seg_{i}"
    o.scale = (0.0004, 0.0009, 0.00008)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(M_ant)
wire("rf_feed", (ant_x0, ant_y0, Ztop+0.00005), (0.007, -0.014, -0.0004), r=0.000015, m=M_gold)

# ==== Gold rails on bottom face ====
box("rail_3v3", 0.018, 0.0006, 0.00004, (-0.002, 0.0, -0.0007), M_gold)
box("rail_7v",  0.009, 0.0006, 0.00004, (-0.007, 0.014, -0.0007), M_gold)

# ==== Sample well on top face (dark recess, visible through transparent chip) ====
box("sample_well", 0.002, 0.002, 0.0002, (0, 0, Ztop-0.0001), M_well)

# ==== UV laser beam: VCSEL mesa -> through chip -> sample well ====
p0 = (VX, VY, -0.000065)
p1 = (0, 0, Ztop)
wire("uv_cone", p0, p1, r=0.00025, m=M_beams)

# ==== Fluorescence: sample well -> Si PD (2pi cone simplified) ====
p2 = (0, 0, Ztop-0.0002)
p3 = (PD_X, PD_Y, -0.0005)
wire("fluo_beam", p2, p3, r=0.00035, m=M_flor)

# ==== Render camera: bottom-face up view ====
# Position camera below chip, looking up at bottom face
cam_pos = (0.12, -0.12, -0.10)
cam_tgt = (0.0, -0.005, -0.0005)
d = mathutils.Vector(cam_tgt) - mathutils.Vector(cam_pos)
q = (-d).to_track_quat('Z','Y')
bpy.ops.object.camera_add(location=cam_pos, rotation=q.to_euler())
c = bpy.context.object
c.data.lens = 80; c.data.clip_start = 0.001; c.data.clip_end = 50
sc.camera = c

# Also add a second camera at top-front for context
cam2_pos = (0.15, -0.15, 0.12)
d2 = mathutils.Vector((0,0,0.001)) - mathutils.Vector(cam2_pos)
q2 = (-d2).to_track_quat('Z','Y')
bpy.ops.object.camera_add(location=cam2_pos, rotation=q2.to_euler())
c2 = bpy.context.object
c2.name = "cam_top"
c2.data.lens = 60; c2.data.clip_start = 0.001; c2.data.clip_end = 50

# Lights (aimed from below to illuminate bottom face)
for pos, e in [((0.10, 0.0, -0.15), 120), ((-0.10, -0.05, -0.10), 60), ((0.0, 0.15, -0.12), 80)]:
    bpy.ops.object.light_add(location=pos, type='POINT')
    bpy.context.object.data.energy = e

# Save & render v02
out_blend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scene_v02.blend")
out_png   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overview_v02.png")
sc.render.filepath = out_png
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)

with open(out_png,'rb') as f: h = hashlib.sha256(f.read()).hexdigest()
print(f"V30_V02_OK blend={out_blend} png={out_png} sha256={h}")
