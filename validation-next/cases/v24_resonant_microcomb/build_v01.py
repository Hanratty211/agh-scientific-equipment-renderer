"""V24 resonant microcomb build_v01.py
Broadband soliton microcombs via resonant coupler chip:
laser source, fiber coupler, chip package (microring resonator),
thermal tuning stage, OSA, optical table.
Based on SELECTION.md entry (arXiv:2610.12603, D-class text-driven).
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
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.04,0.05,0.08,1.0)
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

def torus(name, R, r, loc, m=None, s1=96, s2=20):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, major_segments=s1, minor_segments=s2)
    o = bpy.context.object; o.name = name
    if m: o.data.materials.append(m)
    return o

def wire(name, p0, p1, r=0.001, m=None):
    v = mathutils.Vector(p1)-mathutils.Vector(p0)
    mid = (mathutils.Vector(p0)+mathutils.Vector(p1))/2
    rot = v.to_track_quat('Z','Y').to_euler()
    o = cyl(name, r, v.length, tuple(mid), tuple(rot), m, seg=12)
    o['wire_p0'] = tuple(p0); o['wire_p1'] = tuple(p1)
    return o

sc = setup()

# ==== Materials ====
M_table  = mat("table_top", (0.10,0.08,0.06), rough=0.7, metal=0.2)
M_laser  = mat("laser_box", (0.05,0.05,0.08), rough=0.4, metal=0.5)
M_fiber  = mat("fiber",     (0.10,0.10,0.10), rough=0.5)
M_chip   = mat("chip_sub",  (0.85,0.85,0.88), rough=0.2, metal=0.1)  # Si substrate
M_ridge  = mat("waveguide",  (0.30,0.30,0.35), rough=0.3, metal=0.0, alpha=0.8)
M_ring   = mat("ring_res",   (0.20,0.25,0.90), rough=0.2, alpha=0.6, emis=(0.2,0.25,0.9), es=0.5)
M_heater = mat("heater",     (0.90,0.30,0.10), rough=0.3, emis=(0.9,0.3,0.1), es=1.0)
M_pack   = mat("package",   (0.15,0.15,0.18), rough=0.4, metal=0.5, alpha=0.7)  # transparent lid
M_osa    = mat("osa_box",   (0.05,0.05,0.08), rough=0.4, metal=0.5)
M_screen = mat("osa_scr",   (0.0,0.4,0.6), rough=0.1, emis=(0.0,0.4,0.6), es=1.5)
M_gold   = mat("gold_pad",  (1.0,0.8,0.1), rough=0.2, metal=0.8)
M_beam   = mat("optical",  (0.9,0.1,0.1), rough=0.1, emis=(0.9,0.1,0.1), es=3.0)
M_beam2  = mat("out_fiber",(0.0,0.8,0.2), rough=0.1, emis=(0,0.8,0.2), es=3.0)
M_ctrl   = mat("ctrl_box",  (0.10,0.10,0.12), rough=0.5, metal=0.4)

# ==== Optical table ====
ZT = 0.04
box("table", 0.50, 0.35, ZT, (0, 0, ZT/2), M_table)
for i,(lx,ly) in enumerate([(-0.22,-0.14),(0.22,-0.14),(-0.22,0.14),(0.22,0.14)]):
    cyl(f"leg_{i}", 0.006, ZT, (lx, ly, ZT/2), (0,0,0), M_table, seg=16)

# ==== 1. Tunable laser source (1550nm) ====
lx, ly = -0.18, -0.05
box("laser", 0.08, 0.06, 0.04, (lx, ly, ZT+0.02), M_laser)
cyl("laser_fiber_out", 0.0015, 0.03, (lx+0.04, ly, ZT+0.02), (0, math.pi/2, 0), M_fiber, seg=12)

# ==== 2. Fiber coupler (pump/drop) ====
cx2, cy2 = -0.08, -0.05
box("fiber_coupler", 0.03, 0.02, 0.015, (cx2, cy2, ZT+0.008), M_ctrl)
wire("laser_to_coupler", (lx+0.04, ly, ZT+0.02), (cx2-0.015, cy2, ZT+0.008), r=0.001, m=M_fiber)
# Drop fiber goes to chip
wire("coupler_drop", (cx2+0.015, cy2, ZT+0.008), (0.02, -0.03, ZT+0.01), r=0.001, m=M_beam)

# ==== 3. Micro-ring resonator chip ====
chip_x, chip_y = 0.04, 0.0
# Si substrate
box("chip_substrate", 0.03, 0.03, 0.001, (chip_x, chip_y, ZT+0.0005), M_chip)
# Waveguide access (straight channel to ring)
box("wg_in", 0.01, 0.001, 0.0005, (chip_x-0.012, chip_y, ZT+0.001), M_ridge)
box("wg_out", 0.01, 0.001, 0.0005, (chip_x+0.012, chip_y, ZT+0.001), M_ridge)
# Microring (torus)
torus("microring", 0.005, 0.0008, (chip_x, chip_y, ZT+0.001), M_ring, s1=128, s2=24)
# Thermal heater (gold spiral above ring)
bpy.ops.mesh.primitive_torus_add(major_radius=0.004, minor_radius=0.0003, location=(chip_x, chip_y, ZT+0.002), major_segments=64, minor_segments=8)
o = bpy.context.object; o.name = "heater_spiral"; o.data.materials.append(M_heater)
# Package lid (semi-transparent, shows internal ring)
box("package_lid", 0.032, 0.032, 0.008, (chip_x, chip_y, ZT+0.005), M_pack)
# Gold pads on chip
for i,(px,py) in enumerate([(chip_x-0.012, chip_y-0.01),(chip_x+0.012, chip_y+0.01)]):
    cyl(f"gold_pad_{i}", 0.002, 0.0002, (px, py, ZT+0.0012), (0,0,0), M_gold, seg=16)

# Fiber coupling to chip (side access)
wire("fiber_to_chip", (0.02, -0.03, ZT+0.01), (chip_x-0.015, chip_y, ZT+0.001), r=0.0008, m=M_fiber)
wire("fiber_chip_out", (chip_x+0.015, chip_y, ZT+0.001), (0.10, -0.02, ZT+0.01), r=0.0008, m=M_beam2)

# ==== 4. OSA (optical spectrum analyser) ====
osa_x, osa_y = 0.16, -0.08
box("osa", 0.10, 0.06, 0.05, (osa_x, osa_y, ZT+0.025), M_osa)
box("osa_screen", 0.06, 0.002, 0.03, (osa_x, osa_y+0.031, ZT+0.025), M_screen)
wire("osa_fiber_in", (0.10, -0.02, ZT+0.01), (osa_x-0.05, osa_y, ZT+0.025), r=0.001, m=M_beam2)

# ==== 5. Heater control circuit (small box on table) ====
box("heater_ctrl", 0.05, 0.03, 0.02, (chip_x, -0.06, ZT+0.01), M_ctrl)
wire("heater_w1", (chip_x-0.008, chip_y-0.01, ZT+0.001), (chip_x-0.02, -0.055, ZT+0.01), r=0.0006, m=M_gold)
wire("heater_w2", (chip_x+0.008, chip_y-0.01, ZT+0.001), (chip_x+0.02, -0.055, ZT+0.01), r=0.0006, m=M_gold)

# ==== 6. Heater wire to chip pads ====
wire("heater_to_chip", (chip_x, -0.05, ZT+0.01), (chip_x, chip_y-0.012, ZT+0.001), r=0.0005, m=M_gold)

# ==== Render camera ====
cam_pos = (0.15, -0.25, 0.25)
cam_tgt = (0.03, -0.02, ZT+0.01)
d = mathutils.Vector(cam_tgt)-mathutils.Vector(cam_pos)
q = (-d).to_track_quat('Z','Y')
bpy.ops.object.camera_add(location=cam_pos, rotation=q.to_euler())
c = bpy.context.object
c.data.lens = 55; c.data.clip_start = 0.01; c.data.clip_end = 50
sc.camera = c

# Lights
for pos, e in [((0.25,0.1,0.30), 80), ((-0.2,0.2,0.25), 50), ((0.0,-0.25,0.20), 40)]:
    bpy.ops.object.light_add(location=pos, type='POINT')
    bpy.context.object.data.energy = e

# Save & render
out_blend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scene_v01.blend")
out_png   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overview_v01.png")
sc.render.filepath = out_png
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)

with open(out_png,'rb') as f: h = hashlib.sha256(f.read()).hexdigest()
print(f"V24_BUILD_OK blend={out_blend} png={out_png} sha256={h}")
