"""V21 MIP twin-beam photothermal system build_v01.py
Twin-beam mid-infrared photothermal detection:
  1.5 um fs laser -> FBG -> fiber amplifier (EDFA)
  -> SHG/PPLN OPA -> seed filter + delay line -> QCL + AOM
  -> sample cell -> BPD (balanced photodetector) -> RFSA chain
Based on SELECTION.md entry arXiv:2610.10294 (B-class, public HTML/Methods already obtained).
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
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.04,0.04,0.06,1.0)
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

def wire(name, p0, p1, r=0.001, m=None):
    v = mathutils.Vector(p1)-mathutils.Vector(p0)
    mid = (mathutils.Vector(p0)+mathutils.Vector(p1))/2
    rot = v.to_track_quat('Z','Y').to_euler()
    o = cyl(name, r, v.length, tuple(mid), tuple(rot), m, seg=12)
    o['wire_p0'] = tuple(p0); o['wire_p1'] = tuple(p1)
    return o

def beam_obj(name, p0, p1, r=0.0008, m=None):
    v = mathutils.Vector(p1)-mathutils.Vector(p0)
    mid = (mathutils.Vector(p0)+mathutils.Vector(p1))/2
    rot = v.to_track_quat('Z','Y').to_euler()
    o = cyl(name, r, v.length, tuple(mid), tuple(rot), m, seg=12)
    o['beam_p0'] = tuple(p0); o['beam_p1'] = tuple(p1)
    return o

sc = setup()

# ==== Materials ====
M_table  = mat("table_top", (0.10,0.08,0.06), rough=0.7, metal=0.2)
M_laser  = mat("fs_laser",  (0.05,0.05,0.08), rough=0.4, metal=0.5)
M_fb     = mat("fbg",       (0.30,0.50,0.90), rough=0.2, alpha=0.6)
M_edfa   = mat("edfa_box",  (0.20,0.15,0.10), rough=0.4, metal=0.5)
M_opa    = mat("opa_ppln",  (0.40,0.70,0.95), rough=0.15, alpha=0.7)  # PPLN crystal
M_seedf  = mat("seed_filter",(0.60,0.40,0.80),rough=0.2, alpha=0.6)
M_delay  = mat("delay_line",(0.20,0.20,0.25), rough=0.4, metal=0.5)
M_qcl    = mat("qcl_box",   (0.05,0.10,0.30), rough=0.3, metal=0.4)
M_aom    = mat("aom_box",   (0.10,0.10,0.12), rough=0.4, metal=0.5)
M_cell   = mat("sample_cell",(0.10,0.10,0.15), rough=0.5, alpha=0.5)
M_bpd    = mat("bpd_box",   (0.08,0.08,0.10), rough=0.4, metal=0.5)
M_osa    = mat("rfsa_box",  (0.10,0.10,0.12), rough=0.5, metal=0.4)
M_scr    = mat("rfsa_scr",  (0.0,0.5,0.3), rough=0.1, emis=(0,0.5,0.3), es=1.5)
M_wire   = mat("rf_cable",  (0.08,0.08,0.10), rough=0.5, metal=0.4)
M_beam1  = mat("seed_beam", (0.9,0.3,0.1), rough=0.1, emis=(0.9,0.3,0.1), es=3.0)
M_beam2  = mat("qcl_beam",  (0.1,0.8,0.9), rough=0.1, emis=(0.1,0.8,0.9), es=3.0)
M_beam3  = mat("out_beam",  (0.9,0.9,0.2), rough=0.1, emis=(0.9,0.9,0.2), es=3.0)
M_fiber  = mat("fiber_gray",(0.10,0.10,0.10), rough=0.5)

# ==== Optical table ====
ZT = 0.04
box("table", 0.60, 0.35, ZT, (0, 0, ZT/2), M_table)
for i,(lx,ly) in enumerate([(-0.27,-0.15),(0.27,-0.15),(-0.27,0.15),(0.27,0.15)]):
    cyl(f"leg_{i}", 0.006, ZT, (lx, ly, ZT/2), (0,0,0), M_table, seg=16)

# Layout along x-axis: laser(left) -> FBG -> EDFA -> OPA -> seed filter -> delay -> QCL+AOM -> cell -> BPD -> RFSA(right)
# y: signal path at y=0; twin seed beam at y=+0.06

# 1. 1.5um fs laser
box("fs_laser", 0.08, 0.06, 0.04, (-0.24, 0.0, ZT+0.02), M_laser)
wire("laser_fiber", (-0.20, 0.0, ZT+0.02), (-0.17, 0.0, ZT+0.01), r=0.001, m=M_fiber)

# 2. FBG (Fiber Bragg Grating, small blue glass block)
box("fbg", 0.015, 0.015, 0.008, (-0.16, 0.0, ZT+0.01), M_fb)
wire("fbg_out", (-0.15, 0.0, ZT+0.01), (-0.13, 0.0, ZT+0.01), r=0.001, m=M_fiber)

# 3. EDFA
box("edfa", 0.06, 0.05, 0.04, (-0.10, 0.0, ZT+0.02), M_edfa)
wire("edfa_pump", (-0.10, -0.04, ZT+0.02), (-0.10, -0.04, ZT+0.02), r=0.001, m=M_fiber)
wire("edfa_out", (-0.07, 0.0, ZT+0.02), (-0.055, 0.0, ZT+0.01), r=0.001, m=M_beam1)

# 4. SHG/PPLN OPA (crystal in holder)
box("opa_holder", 0.04, 0.03, 0.025, (-0.035, 0.0, ZT+0.015), M_delay)
box("ppln_crystal", 0.03, 0.015, 0.012, (-0.035, 0.0, ZT+0.015), M_opa)
beam_obj("opa_seed", (-0.055, 0.0, ZT+0.01), (-0.035, 0.0, ZT+0.015), r=0.001, m=M_beam1)
beam_obj("opa_id",   (-0.035, 0.0, ZT+0.015), (-0.02, 0.0, ZT+0.015), r=0.001, m=M_beam2)

# 5. Seed filter + delay line
box("seed_filter", 0.012, 0.012, 0.008, (-0.015, 0.0, ZT+0.01), M_seedf)
wire("seed_to_delay", (-0.015, 0.0, ZT+0.01), (-0.008, 0.0, ZT+0.01), r=0.001, m=M_beam1)
# Delay line (spooled fiber in compact box)
box("delay_line", 0.035, 0.025, 0.02, (0.005, 0.0, ZT+0.01), M_delay)
wire("delay_out", (0.022, 0.0, ZT+0.01), (0.035, 0.0, ZT+0.01), r=0.001, m=M_beam1)

# 6. QCL (quantum cascade laser, compact box)
box("qcl", 0.04, 0.03, 0.02, (0.05, 0.0, ZT+0.01), M_qcl)
beam_obj("qcl_out", (0.07, 0.0, ZT+0.01), (0.085, 0.0, ZT+0.01), r=0.001, m=M_beam2)

# 7. AOM (acousto-optic modulator, small block)
box("aom", 0.02, 0.015, 0.012, (0.09, 0.0, ZT+0.01), M_aom)
wire("aom_rf", (0.09, 0.02, ZT+0.01), (0.12, 0.06, ZT+0.01), r=0.001, m=M_wire)

# 8. Sample cell (two parallel glass plates, open)
box("cell_base",  0.05, 0.04, 0.01, (0.13, 0.0, ZT+0.005), M_cell)
box("cell_top",   0.05, 0.04, 0.005, (0.13, 0.0, ZT+0.0175), M_cell)
box("cell_well",  0.04, 0.03, 0.01, (0.13, 0.0, ZT+0.01), M_cell)
# Absorber sample in cell
box("absorber", 0.03, 0.02, 0.005, (0.13, 0.0, ZT+0.01), mat("abs",(0.05,0.05,0.08),rough=0.6))

# 9. Twin beam paths: QCL + seed both enter cell
# Seed twin beam (from delay line, offset in y)
beam_obj("seed_to_cell", (0.022, 0.0, ZT+0.01), (0.11, 0.008, ZT+0.01), r=0.001, m=M_beam1)
# QCL beam enters cell
beam_obj("qcl_to_cell", (0.07, 0.0, ZT+0.01), (0.11, -0.008, ZT+0.01), r=0.001, m=M_beam2)

# 10. Photodetector (BPD - balanced, after cell)
box("bpd", 0.03, 0.025, 0.02, (0.16, 0.0, ZT+0.01), M_bpd)
beam_obj("cell_to_bpd", (0.15, 0.0, ZT+0.01), (0.16, 0.0, ZT+0.01), r=0.0008, m=M_beam3)
wire("bpd_signal", (0.16, 0.015, ZT+0.01), (0.19, 0.0, ZT+0.015), r=0.001, m=M_wire)

# 11. RFSA / analysis chain (oscilloscope / spectrum analyser)
box("rfsa", 0.08, 0.06, 0.05, (0.23, 0.0, ZT+0.025), M_osa)
box("rfsa_scr", 0.05, 0.002, 0.03, (0.23, 0.031, ZT+0.025), M_scr)
wire("rfsa_in", (0.19, 0.0, ZT+0.015), (0.20, 0.0, ZT+0.025), r=0.001, m=M_wire)

# ==== Render camera ====
cam_pos = (0.10, -0.30, 0.28)
cam_tgt = (0.05, 0.0, ZT+0.02)
d = mathutils.Vector(cam_tgt)-mathutils.Vector(cam_pos)
q = (-d).to_track_quat('Z','Y')
bpy.ops.object.camera_add(location=cam_pos, rotation=q.to_euler())
c = bpy.context.object
c.data.lens = 55; c.data.clip_start = 0.01; c.data.clip_end = 50
sc.camera = c

# Lights
for pos, e in [((0.30,0.1,0.35), 90), ((-0.25,0.2,0.30), 60), ((0.0,-0.25,0.25), 50)]:
    bpy.ops.object.light_add(location=pos, type='POINT')
    bpy.context.object.data.energy = e

# Save & render
out_blend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scene_v01.blend")
out_png   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overview_v01.png")
sc.render.filepath = out_png
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)

with open(out_png,'rb') as f: h = hashlib.sha256(f.read()).hexdigest()
print(f"V21_BUILD_OK blend={out_blend} png={out_png} sha256={h}")
