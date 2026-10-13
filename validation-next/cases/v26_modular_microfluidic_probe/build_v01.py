"""V26 microfluidic T-junction build_v01.py
T-junction channel with inflow/outflow ports, fluid medium, particle tracer,
and optical observation setup based on arXiv:2610.13796 Fig. 1 sketch.
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
    sc.render.film_transparent = False
    # world
    w = bpy.data.worlds.new("W")
    bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.04, 0.06, 0.10, 1.0)
    return sc

def mat(name, base, rough=0.5, metal=0.0, emis=None, es=0.0, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.blend_method = 'BLEND' if alpha < 1.0 else 'OPAQUE'
    if alpha < 1.0:
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

def sphere(name, r, loc, m=None, seg=16, rings=8):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=rings)
    o = bpy.context.object
    o.name = name
    if m:
        o.data.materials.append(m)
    return o

def cam(loc, look, lens=50):
    d = mathutils.Vector(look) - mathutils.Vector(loc)
    q = (-d).to_track_quat('Z','Y')
    bpy.ops.object.camera_add(location=loc, rotation=q.to_euler())
    c = bpy.context.object
    c.data.lens = lens
    c.data.clip_start = 0.01
    c.data.clip_end = 100
    return c

def light(loc, energy=50):
    bpy.ops.object.light_add(location=loc, type='POINT')
    o = bpy.context.object
    o.data.energy = energy
    return o

# --- scene ---
sc = setup()

# Materials
M_wafer   = mat("wafer",   (0.85,0.88,0.92), rough=0.15, metal=0.0, alpha=0.18)  # highly transparent
M_fluid   = mat("fluid",   (0.20,0.65,0.85), rough=0.15, metal=0.0, alpha=0.55)   # visible blue
M_wall    = mat("wall",    (0.45,0.48,0.55), rough=0.35, metal=0.2)              # channel walls (solid)
M_tracer  = mat("tracer",  (0.98,0.78,0.10), rough=0.2, metal=0.8)               # particle
M_port    = mat("port",    (0.12,0.12,0.15), rough=0.4, metal=0.7)               # port metal
M_portring= mat("portring",(0.85,0.85,0.90), rough=0.3, metal=0.5)              # port collar
M_optics  = mat("optics",  (0.92,0.94,0.98), rough=0.08, metal=0.0, alpha=0.35) # glass
M_support = mat("support", (0.18,0.18,0.22), rough=0.5, metal=0.5)              # base plate
M_beammat = mat("beam_mat",(0.2,1.0,0.25),  rough=0.1, emis=(0.2,1.0,0.25), es=3.0, alpha=1.0)

# Dimensions (m, scene scale ~ mm/1000)
W  = 0.02   # channel width (Y of main arms)
D  = 0.006  # channel depth
L_ = 0.08   # main arm length (X direction)
WB = 0.02   # branch width (X of branch arm)
LB = 0.06   # branch arm length (Y direction)
Z0 = 0.012   # base plate top
ZH = 0.055   # wafer top z
CZ = ZH - D/2 # channel fluid center z
BZ = CZ       # branch arm center z (same)

# Support base plate (solid, dark)
box("base_plate", L_*2.6, LB + W*2.2, Z0, (0, (LB-W)/2, Z0/2), M_support)

# Transparent wafer body — NOT occluding; very low alpha
box("wafer_substrate", L_*2 + W, LB + W*1.4, ZH - Z0, (0, (LB-W)/2, Z0 + (ZH-Z0)/2), M_wafer)

# ---- T-junction channel: main X-arm + branch Y-arm ----
# Main arm wall block (solid, visible) spanning full main arm
box("main_arm_wall", L_*2 + W, W + 0.004, D + 0.004, (0, W/2, CZ), M_wall)
# Branch arm wall block
box("branch_arm_wall", WB + 0.004, LB, D + 0.004, (WB/2, LB/2 + W/2, BZ), M_wall)

# Cut the channel interior out of the two wall blocks using boolean DIFFERENCE
# Main channel void
ch_main = box("_void_main", L_*2 + W*0.7, W*0.7, D*0.8, (0, W/2, CZ), None)
# Branch channel void
ch_br = box("_void_branch", WB*0.7, LB + W*0.5, D*0.8, (WB/2, LB/2 + W/2, BZ), None)
import bmesh
bpy.context.view_layer.objects.active = bpy.data.objects['main_arm_wall']
m1 = bpy.data.objects['main_arm_wall'].modifiers.new("_bool", 'BOOLEAN')
m1.operation = 'DIFFERENCE'; m1.object = ch_main; m1.solver = 'EXACT'
bpy.ops.object.modifier_apply(modifier="_bool")

bpy.context.view_layer.objects.active = bpy.data.objects['branch_arm_wall']
m2 = bpy.data.objects['branch_arm_wall'].modifiers.new("_bool", 'BOOLEAN')
m2.operation = 'DIFFERENCE'; m2.object = ch_br; m2.solver = 'EXACT'
bpy.ops.object.modifier_apply(modifier="_bool")

# Fluid volumes filling the channel voids (visible, semi-transparent blue)
box("fluid_main", L_*2 + W*0.7, W*0.7, D*0.8, (0, W/2, CZ), M_fluid)
box("fluid_branch", WB*0.7, LB + W*0.5, D*0.8, (WB/2, LB/2 + W/2, BZ), M_fluid)

# Particle tracer (gold sphere) sitting inside main arm near junction
tr = sphere("particle_tracer", 0.003, (-0.008, W/2, CZ), M_tracer, seg=24, rings=12)

# ---- 3 port fittings: flared collars + stem + visible bore hole into channel top ----
port_positions = [(-L_/2 + 0.01, W/2), (L_/2 - 0.01, W/2), (WB/2, LB + W/2 - 0.005)]
for i, (px, py) in enumerate(port_positions):
    ring = cyl(f"port_collar_{i}", 0.007, 0.006, (px, py, ZH + 0.003), (0,0,0), M_portring, seg=32)
    stem = cyl(f"port_stem_{i}",  0.004, 0.014, (px, py, ZH - 0.004), (0,0,0), M_port, seg=24)
    # visible bore hole through wafer into channel top
    bore = cyl(f"port_bore_{i}", 0.0028, 0.02, (px, py, CZ + 0.008), (0,0,0), M_beammat, seg=16)
    # label bore endpoints
    bore['port_idx'] = i

# ---- Observation beam: from -Y laser arm crossing through junction, hitting detector on +Y ----
laser_arm = box("laser_input_arm", 0.01, L_*0.5, D, (-L_/2 - 0.02, -W/2 - 0.02, CZ), M_optics)

# Beam cylinder
p0 = (-L_/2 - 0.02, -W/2 - 0.02, CZ)
p1 = (0, LB + W/2 + 0.04, CZ)
v = mathutils.Vector(p1) - mathutils.Vector(p0)
mid = (mathutils.Vector(p0) + mathutils.Vector(p1)) / 2
rot = v.to_track_quat('Z','Y').to_euler()
beam_obj = cyl("observation_beam", 0.0012, v.length, tuple(mid), tuple(rot), M_beammat, seg=12)
beam_obj['beam_p0'] = tuple(p0)
beam_obj['beam_p1'] = tuple(p1)

# Detector block + lens on +Y (fully inside frame)
det_block = box("detector_block", 0.045, 0.022, 0.024, (0, LB + W/2 + 0.06, CZ), M_support)
# cut front half of block for lens mount
lens_mount = cyl("detector_lens", 0.010, 0.006, (0, LB + W/2 + 0.048, CZ), (math.pi/2,0,0), M_optics, seg=32)

# Camera body (complete, not cropped)
cam_body  = box("camera_body",  0.05, 0.035, 0.035, (0, LB + W/2 + 0.115, CZ + 0.04), M_support)
cam_lens  = cyl("camera_lens", 0.013, 0.018, (0, LB + W/2 + 0.092, CZ + 0.04), (math.pi/2,0,0), M_port, seg=32)

# Small stand feet under base
for i, (fx, fy) in enumerate([(-L_*1.1, W*0.3), (L_*1.1, W*0.3), (0, LB + W)]):
    cyl(f"stand_foot_{i}", 0.006, 0.008, (fx, fy, -0.004), (0,0,0), M_support, seg=20)

# --- camera ---
cam_pos = (0.28, -0.28, 0.22)
cam_target = (0.02, 0.04, 0.02)
d = mathutils.Vector(cam_target) - mathutils.Vector(cam_pos)
q = (-d).to_track_quat('Z','Y')
bpy.ops.object.camera_add(location=cam_pos, rotation=q.to_euler())
c = bpy.context.object
c.data.lens = 50
c.data.clip_start = 0.01
c.data.clip_end = 100
sc.camera = c
light((0.35, 0.1, 0.35), 100)
light((-0.25, 0.45, 0.25), 55)

# Save & render
out_blend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scene_v02.blend")
out_png   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overview_v02.png")
sc.render.filepath = out_png
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)

with open(out_png,'rb') as f: h1 = hashlib.sha256(f.read()).hexdigest()
print(f"V26_V02_BUILD_OK blend={out_blend} png={out_png} png_sha256={h1}")
