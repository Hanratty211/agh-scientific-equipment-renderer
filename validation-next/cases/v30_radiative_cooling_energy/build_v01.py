"""V30 UV Fluorescence Optoelectronic Chip build_v01.py
AlGaN VCSEL + UV-enhanced Si photodetector on transparent sapphire chip,
electronic chiplets (LD driver, TIA, ADC, MCU/ESP32, LiPo, USB-C, boost) on bottom face.
Based on arXiv:2610.13525 Figs. 4, 5, 10, 11, 12 (text-based reconstruction).
"""
import bpy, bmesh, math, mathutils, os, sys, hashlib

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
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.03, 0.05, 0.09, 1.0)
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
    if tw:
        tw.default_value = 1.0 - alpha
    return m

def box(name, sx, sy, sz, loc, m=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if m:
        o.data.materials.append(m)
    return o

def cyl(name, r, depth, loc, rot=(0,0,0), m=None, seg=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=seg)
    o = bpy.context.object
    o.name = name
    if m:
        o.data.materials.append(m)
    return o

def light_add(loc, energy=50):
    bpy.ops.object.light_add(location=loc, type='POINT')
    o = bpy.context.object
    o.data.energy = energy
    return o

sc = setup()

# --- Materials ---
# Sapphire chip body (transparent blue-violet)
M_sapphire = mat("sapphire", (0.55,0.60,0.90), rough=0.05, metal=0.0, alpha=0.15)
# VCSEL p-DBR (white, metallic)
M_vcsel    = mat("vcsel",    (0.90,0.90,0.95), rough=0.2, metal=0.3)
# VCSEL active mesa (AlGaN, pale)
M_algan    = mat("algan",    (0.75,0.80,0.85), rough=0.3, metal=0.1)
# AlN substrate (white)
M_aln      = mat("aln",      (0.92,0.92,0.92), rough=0.25, metal=0.0)
# Si PD (dark, metallic grey)
M_sipd     = mat("sipd",     (0.10,0.10,0.12), rough=0.4, metal=0.7)
# Longpass filter on PD (blue tint)
M_filter   = mat("filter",   (0.30,0.40,0.90), rough=0.1, metal=0.0, alpha=0.4)
# Electronic chiplets (IC die, dark green)
M_chiplet  = mat("chiplet",  (0.05,0.20,0.05), rough=0.4, metal=0.3)
# Chiplet substrate (ceramic, beige)
M_ceramic  = mat("ceramic",  (0.75,0.70,0.55), rough=0.5, metal=0.0)
# LiPo battery (purple, rounded)
M_lipo     = mat("lipo",     (0.35,0.20,0.60), rough=0.5, metal=0.1)
# USB-C connector (silver)
M_usb      = mat("usb",      (0.80,0.80,0.85), rough=0.3, metal=0.8)
# Gold trace/rail
M_gold     = mat("gold",     (0.95,0.80,0.20), rough=0.2, metal=0.8)
# Wi-Fi antenna trace (dark PCB)
M_ant      = mat("ant",      (0.05,0.05,0.08), rough=0.5, metal=0.5)
# Sample well (dark recess)
M_well     = mat("well",     (0.05,0.05,0.08), rough=0.6, metal=0.0)
# Housing enclosure
M_house    = mat("housing",  (0.15,0.15,0.18), rough=0.5, metal=0.4)
# Laser beam (UV glow)
M_beam     = mat("beam",     (0.40,0.20,0.95), rough=0.1, emis=(0.40,0.20,0.95), es=4.0, alpha=1.0)

# --- Dimensions (m, scene scale ~ mm/1000) ---
# Chip: 2cm x 5cm = 0.02 x 0.05 m, thickness ~ 0.004 m
CW, CD, CT = 0.020, 0.050, 0.004
Z0 = 0.0           # chip bottom face (z=0)
Zmid = CT/2        # chip mid z
Ztop = CT          # chip top face
H = 0.0012         # housing height below chip

# --- 1. Sapphire chip body (transparent, high alpha visibility) ---
sapphire = box("sapphire_chip", CW, CD, CT, (0, 0, Zmid), M_sapphire)

# --- 2. VCSEL bonded to chip BOTTOM face (Fig. 4/5/6) ---
# AlN substrate: 200um x 200um x 50um
VX, VY = -0.003, 0.0   # VCSEL center (offset from center)
alc_sub = box("vcsl_aln_substrate", 0.0002, 0.0002, 0.00005, (VX, VY, -0.000025), M_aln)
# p-type DBR (13 layers, white metallic)
alc_pdb = box("vcsl_p_dbr", 0.0002, 0.0002, 0.000001, (VX, VY, -0.00005 - 0.0000005), M_vcsel)
# MQW active mesa (AlGaN, cylindrical)
alc_mesa = cyl("vcsl_active_mesa", 0.00007, 0.000002, (VX, VY, -0.000051), (0,0,0), M_algan, seg=32)
# n-type DBR
alc_ndb = box("vcsl_n_dbr", 0.0002, 0.0002, 0.000001, (VX, VY, -0.000052), M_vcsel)

# p-pad (Pd/Au, small disc on mesa top)
alc_ppad = cyl("vcsl_p_pad", 0.00003, 0.0000005, (VX, VY, -0.0000505), (0,0,0), M_gold, seg=24)
# n-pad (Ti/Au, rectangular)
alc_npad = box("vcsl_n_pad", 0.00008, 0.00003, 0.0000005, (VX+0.00012, VY, -0.0000525), M_gold)

# Wire bonds (thin cylinders from pads to chip trace)
# p-wire
def wire(name, p0, p1, r=0.000008, m=None):
    v = mathutils.Vector(p1)-mathutils.Vector(p0)
    mid = (mathutils.Vector(p0)+mathutils.Vector(p1))/2
    rot = v.to_track_quat('Z','Y').to_euler()
    o = cyl(name, r, v.length, tuple(mid), tuple(rot), m, seg=12)
    o['wire_p0'] = tuple(p0)
    o['wire_p1'] = tuple(p1)
    return o

wire("wire_p", (VX, VY, -0.000050), (VX-0.0005, VY+0.002, -0.0002), r=0.000008, m=M_gold)
wire("wire_n", (VX+0.00012, VY, -0.000052), (VX+0.0005, VY+0.002, -0.0002), r=0.000008, m=M_gold)

# --- 3. Si photodetector (next to VCSEL, bonded to bottom) ---
PD_X, PD_Y = 0.003, 0.0   # offset opposite to VCSEL
pd_body = box("si_photodetector", 0.003, 0.005, 0.0005, (PD_X, PD_Y, -0.00025), M_sipd)
pd_filter = box("pd_longpass_filter", 0.003, 0.005, 0.0001, (PD_X, PD_Y, -0.00005), M_filter)

# --- 4. Electronic chiplets (bonded to bottom face) ---
def chiplet(name, x, y, w=0.002, d=0.002, z=-0.0004):
    c_sub = box(f"{name}_substrate", w+0.001, d+0.001, 0.0003, (x, y, z), M_ceramic)
    c_die = box(f"{name}_die", w, d, 0.00008, (x, y, z+0.00019), M_chiplet)
    # pins
    for i in range(3):
        cyl(f"{name}_pin_{i}", 0.00004, 0.00006, (x - w/3 + i*w/3, y, z-0.0002), (0,0,0), M_gold, seg=12)

# Layout along x-axis on bottom
chiplet("ld_driver", -0.006, 0.010)
chiplet("tia",       -0.006, -0.010)
chiplet("adc",        0.006, 0.010)
chiplet("mcu_esp32",  0.006, -0.010, w=0.003, d=0.004)

# --- 5. LiPo battery (rounded box, bottom face) ---
lipo_box = box("lipo_bat", 0.008, 0.004, 0.002, (-0.003, -0.020, -0.001), M_lipo)
# LiPo connector
box("lipo_conn", 0.004, 0.002, 0.0008, (-0.003, -0.024, -0.0004), M_gold)

# --- 6. USB-C charge port ---
usb_body = box("usb_c_port", 0.002, 0.001, 0.003, (0.007, -0.020, -0.0015), M_usb)
usb_shell = cyl("usb_c_shell", 0.0011, 0.004, (0.007, -0.020, -0.0015), (0,0,math.pi/2), M_usb, seg=16)
# TP4056 charger IC next to USB
chiplet("tp4056", 0.007, -0.010, w=0.0015, d=0.0015)

# Boost converter IC
chiplet("boost_3v7_7v", 0.007, 0.000, w=0.0015, d=0.0015)
# LDO 3.3V
chiplet("ldo_3v3", -0.003, 0.020, w=0.0015, d=0.0015)

# --- 7. Wi-Fi antenna trace (50 Ohm RF lead on chip top face) ---
# Meander pattern on top face
ant_x0, ant_y0 = 0.006, 0.018
for i in range(5):
    x = ant_x0 + i*0.0012
    seg_w = 0.0008
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, ant_y0 + (i%2)*seg_w, Ztop + 0.00005))
    o = bpy.context.object
    o.name = f"wifi_antenna_seg_{i}"
    o.scale = (0.0004, seg_w, 0.0001)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(M_ant)
# 50 Ohm RF feed line to MCU
wire("rf_feed_50ohm", (ant_x0, ant_y0, Ztop+0.00005), (0.006, -0.010, -0.0004), r=0.000008, m=M_gold)

# --- 8. 3.3V and 7V gold rails (thin strips on chip bottom) ---
rail_3v = box("rail_3v3", 0.016, 0.0005, 0.00005, (-0.003, 0.000, -0.0006), M_gold)
rail_7v = box("rail_7v",   0.008, 0.0005, 0.00005, (-0.006, 0.012, -0.0006), M_gold)

# --- 9. Sample well on top face (small recess) ---
well = box("sample_well", 0.001, 0.001, 0.0001, (0, 0, Ztop - 0.00005), M_well)

# --- 10. UV laser beam cone (VCSEL -> sample well -> PD) ---
# Cone from VCSEL mesa through sapphire to sample well
p0 = (VX, VY, -0.00005)
p1 = (0, 0, Ztop)
v = mathutils.Vector(p1)-mathutils.Vector(p0)
mid = (mathutils.Vector(p0)+mathutils.Vector(p1))/2
rot = v.to_track_quat('Z','Y').to_euler()
cone = cyl("uv_laser_cone", 0.0002, v.length, tuple(mid), tuple(rot), M_beam, seg=16)
cone['beam_p0'] = tuple(p0)
cone['beam_p1'] = tuple(p1)

# Fluorescence emission from sample well downward to PD
p2 = (0, 0, Ztop)
p3 = (PD_X, PD_Y, -0.00005)
v2 = mathutils.Vector(p3)-mathutils.Vector(p2)
mid2 = (mathutils.Vector(p2)+mathutils.Vector(p3))/2
rot2 = v2.to_track_quat('Z','Y').to_euler()
fluor = cyl("fluorescence_to_pd", 0.00025, v2.length, tuple(mid2), tuple(rot2), M_beam, seg=16)
fluor['beam_p0'] = tuple(p2)
fluor['beam_p1'] = tuple(p3)

# --- 11. Optional housing enclosure (thin shell, not occluding) ---
box("housing_shell", CW+0.006, CD+0.006, H, (0, 0, -H/2), M_house)

# --- Housing stand feet ---
for i, (fx, fy) in enumerate([(0.012, 0.022), (-0.012, 0.022), (0.012, -0.022), (-0.012, -0.022)]):
    cyl(f"housing_foot_{i}", 0.002, 0.004, (fx, fy, -H-0.002), (0,0,0), M_house, seg=16)

# --- Top-face glass cover (very thin, visible) ---
box("top_glass_cover", CW-0.002, CD-0.002, 0.0003, (0, 0, Ztop+0.00015), M_sapphire)

# --- Lighting ---
light_add((0.15, 0.15, 0.20), 80)
light_add((-0.10, -0.10, 0.10), 40)

# --- Camera ---
cam_pos = (0.12, -0.10, 0.08)
cam_target = (0.0, 0.0, -0.002)
d = mathutils.Vector(cam_target) - mathutils.Vector(cam_pos)
q = (-d).to_track_quat('Z','Y')
bpy.ops.object.camera_add(location=cam_pos, rotation=q.to_euler())
c = bpy.context.object
c.data.lens = 85
c.data.clip_start = 0.001
c.data.clip_end = 50
sc.camera = c

# Save & render
out_blend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scene_v01.blend")
out_png   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overview_v01.png")
sc.render.filepath = out_png
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)

with open(out_png,'rb') as f: h1 = hashlib.sha256(f.read()).hexdigest()
print(f"V30_BUILD_OK blend={out_blend} png={out_png} png_sha256={h1}")
