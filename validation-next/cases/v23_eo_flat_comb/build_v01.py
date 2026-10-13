"""V23 EO flat comb build_v01.py
Electro-optic frequency comb system: microwave source, EO modulators (AM+PM),
EDFA, resonant ring cavities (Ring A, Ring B), optical spectrum analyser (OSA).
Based on arXiv:2610.12867 Fig. 2(b) and text (8-page PDF, local).
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

def wire(name, p0, p1, r=0.0006, m=None):
    v = mathutils.Vector(p1)-mathutils.Vector(p0)
    mid = (mathutils.Vector(p0)+mathutils.Vector(p1))/2
    rot = v.to_track_quat('Z','Y').to_euler()
    o = cyl(name, r, v.length, tuple(mid), tuple(rot), m, seg=12)
    o['wire_p0'] = tuple(p0); o['wire_p1'] = tuple(p1)
    return o

sc = setup()

# ==== Dimensions ====
# Optical table top at z=0.04
ZT = 0.04
# Component positions (x, y) on table
# Layout: laser source on left, modulators center, rings right, OSA far right

# ==== Materials ====
M_table  = mat("table",    (0.10,0.08,0.06), rough=0.7, metal=0.2)
M_tablet = mat("tabletop",  (0.35,0.30,0.25), rough=0.6, metal=0.3)
M_laser  = mat("laser_box",(0.05,0.05,0.08), rough=0.4, metal=0.5)
M_mod    = mat("modulator",(0.15,0.15,0.18), rough=0.3, metal=0.5)
M_edfa   = mat("edfa",     (0.20,0.15,0.10), rough=0.4, metal=0.5)
M_ring   = mat("ring_chip",(0.05,0.08,0.25), rough=0.3, metal=0.0, alpha=0.7)  # glass ring
M_fiber  = mat("fiber",    (0.10,0.10,0.10), rough=0.5, metal=0.0)
M_sam    = mat("sample",   (0.05,0.05,0.08), rough=0.4, metal=0.5)
M_cable  = mat("cable",    (0.05,0.05,0.08), rough=0.5, metal=0.3)
M_bench  = mat("bench_leg",(0.15,0.15,0.18), rough=0.5, metal=0.5)
M_oscil  = mat("oscil_box",(0.10,0.10,0.12), rough=0.5, metal=0.4)
M_beam   = mat("green",    (0.0,0.9,0.2), rough=0.1, emis=(0,0.9,0.2), es=3.0)
M_beam2  = mat("blue",     (0.1,0.3,0.95), rough=0.1, emis=(0.1,0.3,0.95), es=3.0)
M_fiber_c= mat("fiber_col",(0.85,0.85,0.88), rough=0.3, metal=0.2)

# ==== Optical table ====
box("table_top", 0.60, 0.40, ZT, (0, 0, ZT/2), M_table)
# 4 legs
for i,(lx,ly) in enumerate([(-0.28,-0.18),(0.28,-0.18),(-0.28,0.18),(0.28,0.18)]):
    cyl(f"table_leg_{i}", 0.008, ZT, (lx, ly, ZT/2), (0,0,0), M_bench, seg=16)
# V-groove strips on top
for i,yy in enumerate([-0.10, 0.0, 0.10]):
    box(f"vgroove_{i}", 0.55, 0.004, 0.002, (0, yy, ZT+0.001), M_tablet)

# ==== 1. Laser source (1550nm CW laser, box) ====
laser_x, laser_y = -0.20, -0.05
box("laser_source", 0.08, 0.06, 0.04, (laser_x, laser_y, ZT+0.02), M_laser)
# Fiber output from laser
cyl("laser_fiber_out", 0.0015, 0.04, (laser_x+0.04, laser_y, ZT+0.02), (0, math.pi/2, 0), M_fiber_c, seg=12)

# ==== 2. Electro-optic modulator (PM) ====
pm_x, pm_y = -0.10, -0.05
box("pm_modulator", 0.05, 0.04, 0.03, (pm_x, pm_y, ZT+0.015), M_mod)
# Fiber input/output
cyl("pm_fiber_in",  0.0015, 0.03, (pm_x-0.025, pm_y, ZT+0.015), (0, math.pi/2, 0), M_fiber_c, seg=12)
cyl("pm_fiber_out", 0.0015, 0.03, (pm_x+0.025, pm_y, ZT+0.015), (0, math.pi/2, 0), M_fiber_c, seg=12)
# Bias T connector (RF)
cyl("pm_bias_T", 0.003, 0.01, (pm_x, pm_y+0.025, ZT+0.02), (0,0,0), M_cable, seg=12)

# ==== 3. Electro-optic modulator (AM) ====
am_x, am_y = -0.02, -0.05
box("am_modulator", 0.05, 0.04, 0.03, (am_x, am_y, ZT+0.015), M_mod)
cyl("am_fiber_in",  0.0015, 0.03, (am_x-0.025, am_y, ZT+0.015), (0, math.pi/2, 0), M_fiber_c, seg=12)
cyl("am_fiber_out", 0.0015, 0.03, (am_x+0.025, am_y, ZT+0.015), (0, math.pi/2, 0), M_fiber_c, seg=12)
cyl("am_bias_T", 0.003, 0.01, (am_x, am_y+0.025, ZT+0.02), (0,0,0), M_cable, seg=12)

# ==== 4. EDFA (Erbium Doped Fiber Amplifier) ====
edfa_x, edfa_y = 0.06, -0.05
box("edfa", 0.07, 0.05, 0.04, (edfa_x, edfa_y, ZT+0.02), M_edfa)
cyl("edfa_fiber_in",  0.0015, 0.03, (edfa_x-0.035, edfa_y, ZT+0.02), (0, math.pi/2, 0), M_fiber_c, seg=12)
cyl("edfa_fiber_out", 0.0015, 0.03, (edfa_x+0.035, edfa_y, ZT+0.02), (0, math.pi/2, 0), M_fiber_c, seg=12)
# Pump laser (1480nm, separate small box)
box("pump_laser", 0.04, 0.03, 0.02, (edfa_x, edfa_y-0.04, ZT+0.01), M_laser)
wire("pump_fiber", (edfa_x, edfa_y-0.025, ZT+0.01), (edfa_x-0.01, edfa_y-0.005, ZT+0.02), r=0.001, m=M_fiber_c)

# ==== 5. Ring A (micro-ring resonator chip) ====
ring_a_x, ring_a_y = 0.16, 0.0
# Chip substrate
box("ring_a_chip", 0.04, 0.04, 0.003, (ring_a_x, ring_a_y, ZT+0.0015), M_ring)
# Ring A torus
torus("ring_a", 0.008, 0.002, (ring_a_x, ring_a_y, ZT+0.004), M_ring)
# Fiber evanescent coupling (side access)
cyl("ring_a_fiber", 0.0012, 0.03, (ring_a_x-0.015, ring_a_y, ZT+0.004), (0, math.pi/2, 0), M_fiber_c, seg=12)

# ==== 6. Ring B (second ring, for dual comb) ====
ring_b_x, ring_b_y = 0.24, 0.0
box("ring_b_chip", 0.04, 0.04, 0.003, (ring_b_x, ring_b_y, ZT+0.0015), M_ring)
torus("ring_b", 0.008, 0.002, (ring_b_x, ring_b_y, ZT+0.004), M_ring)
cyl("ring_b_fiber", 0.0012, 0.03, (ring_b_x+0.015, ring_b_y, ZT+0.004), (0, math.pi/2, 0), M_fiber_c, seg=12)

# ==== 7. Optical Spectrum Analyser (OSA) ====
osa_x, osa_y = 0.20, -0.15
box("osa", 0.10, 0.06, 0.05, (osa_x, osa_y, ZT+0.025), M_sam)
# Screen on front face
box("osa_screen", 0.06, 0.002, 0.03, (osa_x, osa_y+0.031, ZT+0.025),
    mat("screen",(0.0,0.3,0.5),rough=0.1,emis=(0.0,0.3,0.5),es=1.5))
# Fiber input
cyl("osa_fiber", 0.0015, 0.03, (osa_x-0.05, osa_y, ZT+0.025), (0, math.pi/2, 0), M_fiber_c, seg=12)

# ==== 8. Microwave source / oscilloscope (control) ====
osc_x, osc_y = -0.15, 0.12
box("oscilloscope", 0.10, 0.08, 0.06, (osc_x, osc_y, ZT+0.03), M_oscil)
box("osc_screen", 0.06, 0.002, 0.04, (osc_x, osc_y+0.041, ZT+0.03),
    mat("osc_scr",(0.0,0.5,0.2),rough=0.1,emis=(0,0.5,0.2),es=1.5))
# RF cables to modulators
wire("rf_cable_am", (osc_x+0.02, osc_y-0.04, ZT+0.02), (am_x, am_y+0.025, ZT+0.025), r=0.002, m=M_cable)
wire("rf_cable_pm", (osc_x+0.04, osc_y-0.04, ZT+0.02), (pm_x, pm_y+0.025, ZT+0.025), r=0.002, m=M_cable)

# ==== 9. Fiber links between components (green glowing) ====
# laser -> PM -> AM -> EDFA -> Ring A -> Ring B -> OSA
fiber_links = [
    ("fiber_laser_pm",  (laser_x+0.04, laser_y, ZT+0.02), (pm_x-0.025, pm_y, ZT+0.015)),
    ("fiber_pm_am",     (pm_x+0.025, pm_y, ZT+0.015),    (am_x-0.025, am_y, ZT+0.015)),
    ("fiber_am_edfa",   (am_x+0.025, am_y, ZT+0.015),    (edfa_x-0.035, edfa_y, ZT+0.02)),
    ("fiber_edfa_ringA",(edfa_x+0.035, edfa_y, ZT+0.02), (ring_a_x-0.015, ring_a_y, ZT+0.004)),
    ("fiber_ringA_ringB",(ring_a_x+0.015, ring_a_y, ZT+0.004), (ring_b_x-0.015, ring_b_y, ZT+0.004)),
    ("fiber_ringB_osa", (ring_b_x+0.015, ring_b_y, ZT+0.004), (osa_x-0.05, osa_y, ZT+0.025)),
]
for nm, p0, p1 in fiber_links:
    v = mathutils.Vector(p1)-mathutils.Vector(p0)
    mid = (mathutils.Vector(p0)+mathutils.Vector(p1))/2
    rot = v.to_track_quat('Z','Y').to_euler()
    o = cyl(nm, 0.0012, v.length, tuple(mid), tuple(rot), M_fiber, seg=12)
    o['wire_p0'] = tuple(p0); o['wire_p1'] = tuple(p1)

# ==== Optical beam: EDFA output -> OSA input (green) ====
beam_end = (osa_x-0.05, osa_y, ZT+0.025)
beam_start = (edfa_x+0.035, edfa_y, ZT+0.02)
v = mathutils.Vector(beam_end)-mathutils.Vector(beam_start)
mid = (mathutils.Vector(beam_start)+mathutils.Vector(beam_end))/2
rot = v.to_track_quat('Z','Y').to_euler()
o = cyl("optical_beam", 0.0008, v.length, tuple(mid), tuple(rot), M_beam, seg=12)
o['beam_p0'] = tuple(beam_start); o['beam_p1'] = tuple(beam_end)

# ==== Render camera ====
cam_pos = (0.20, -0.35, 0.30)
cam_tgt = (0.05, -0.02, ZT+0.02)
d = mathutils.Vector(cam_tgt)-mathutils.Vector(cam_pos)
q = (-d).to_track_quat('Z','Y')
bpy.ops.object.camera_add(location=cam_pos, rotation=q.to_euler())
c = bpy.context.object
c.data.lens = 50; c.data.clip_start = 0.01; c.data.clip_end = 50
sc.camera = c

# Lights
for pos, e in [((0.3,0.1,0.35), 100), ((-0.25,0.25,0.30), 60), ((0.0,-0.30,0.25), 50)]:
    bpy.ops.object.light_add(location=pos, type='POINT')
    bpy.context.object.data.energy = e

# Save & render
out_blend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scene_v01.blend")
out_png   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overview_v01.png")
sc.render.filepath = out_png
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)

with open(out_png,'rb') as f: h = hashlib.sha256(f.read()).hexdigest()
print(f"V23_BUILD_OK blend={out_blend} png={out_png} sha256={h}")
