"""V22 soft pneumatic skin actuator build_v01.py
Multilayer 3D pneumatic network flexible robot skin actuator:
  - multilayer soft pneumatic network (curved multi-layer soft body)
  - pneumatic channels in each layer (visible semi-transparent tubes)
  - air supply / pump + pressure control module
  - test rig / fixture
Based on SELECTION.md entry 10.1038/s41467-025-60496-9 (Nature Comm, C-class,
OA public; no local PDF - conservative reconstruction from SELECTION.md description).
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
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.06,0.06,0.07,1.0)
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

def torus(name, R, r, loc, m=None, s1=64, s2=16):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, major_segments=s1, minor_segments=s2)
    o = bpy.context.object; o.name = name
    if m: o.data.materials.append(m)
    return o

def sphere(name, r, loc, m=None, seg=24, rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=rings)
    o = bpy.context.object; o.name = name
    if m: o.data.materials.append(m)
    return o

def wire(name, p0, p1, r=0.003, m=None):
    v = mathutils.Vector(p1)-mathutils.Vector(p0)
    mid = (mathutils.Vector(p0)+mathutils.Vector(p1))/2
    rot = v.to_track_quat('Z','Y').to_euler()
    o = cyl(name, r, v.length, tuple(mid), tuple(rot), m, seg=12)
    o['wire_p0'] = tuple(p0); o['wire_p1'] = tuple(p1)
    return o

sc = setup()

# ==== Materials ====
M_fixture= mat("fixture",   (0.15,0.15,0.18), rough=0.5, metal=0.5)
M_table  = mat("table_top", (0.10,0.08,0.06), rough=0.7, metal=0.2)
# Soft pneumatic network - multi-layer transparent elastic body
# 3 layers, slightly offset, semi-transparent with soft blue/green/orange tint
M_layer1 = mat("soft_l1", (0.40,0.70,0.90), rough=0.4, alpha=0.45)
M_layer2 = mat("soft_l2", (0.90,0.60,0.30), rough=0.4, alpha=0.45)
M_layer3 = mat("soft_l3", (0.50,0.85,0.50), rough=0.4, alpha=0.45)
# Pneumatic channels within each layer (thin visible tubes)
M_chan1  = mat("chan1", (0.20,0.60,0.95), rough=0.2, alpha=0.55, emis=(0.2,0.6,0.95), es=0.3)
M_chan2  = mat("chan2", (0.95,0.55,0.20), rough=0.2, alpha=0.55, emis=(0.95,0.55,0.2), es=0.3)
M_chan3  = mat("chan3", (0.30,0.85,0.35), rough=0.2, alpha=0.55, emis=(0.3,0.85,0.35), es=0.3)
# Air supply / pump
M_pump   = mat("pump_body",(0.08,0.08,0.10), rough=0.4, metal=0.5)
M_press  = mat("press_ctr",(0.10,0.10,0.12), rough=0.4, metal=0.4)
M_gauge  = mat("gauge",   (0.90,0.90,0.92), rough=0.2, metal=0.2)
M_tube   = mat("air_tube",(0.15,0.15,0.15), rough=0.5, alpha=0.6, emis=(0.3,0.3,0.3), es=0.1)
# Port / fitting (PVC/PTFE look, solid)
M_port   = mat("port_fitting",(0.85,0.85,0.85), rough=0.3, metal=0.2)

# ==== Optical table ====
ZT = 0.04
box("table", 0.50, 0.30, ZT, (0, 0, ZT/2), M_table)
for i,(lx,ly) in enumerate([(-0.22,-0.12),(0.22,-0.12),(-0.22,0.12),(0.22,0.12)]):
    cyl(f"leg_{i}", 0.006, ZT, (lx, ly, ZT/2), (0,0,0), M_table, seg=16)

# ==== Fixture / mounting base for the soft actuator ====
box("fixture_base", 0.16, 0.12, 0.02, (0, 0, ZT+0.01), M_fixture)

# ==== Multilayer soft pneumatic network (curved body, 3 layers stacked) ====
# Simplified as 3 slightly curved layered slabs (arc-like via scaled/rotated boxes)
N_LAYERS = 3
layer_thick = 0.008
layer_gap   = 0.002
base_w, base_d = 0.12, 0.08   # layer size (m)

for i in range(N_LAYERS):
    z = ZT + 0.02 + i * (layer_thick + layer_gap)
    layer_mat = [M_layer1, M_layer2, M_layer3][i]
    chan_mat   = [M_chan1,  M_chan2,  M_chan3][i]
    # Slight curvature: use a torus segment as the main body
    # Simplified: scaled sphere (ellipsoid) for each layer to suggest curvature
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, z), segments=32, ring_count=16)
    o = bpy.context.object
    o.name = f"soft_layer_{i+1}"
    o.scale = (base_w/2, base_d/2, layer_thick/2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(layer_mat)
    # Pneumatic channel ring within each layer (visible torus)
    torus(f"channel_layer_{i+1}", base_w/4, 0.0015, (0, 0, z), chan_mat, s1=64, s2=12)

# Top layer surface (slightly flatter, represents the "skin" face)
z_top = ZT + 0.02 + 2 * (layer_thick + layer_gap)
bpy.ops.mesh.primitive_cylinder_add(radius=base_w/2.5, depth=layer_thick, location=(0, 0, z_top + layer_thick/2), vertices=48)
o = bpy.context.object; o.name = "skin_top"; o.data.materials.append(M_layer3)

# ==== Pneumatic inlet port / fittings (on side, visible solid connectors) ====
port_z = ZT + 0.02 + 1 * (layer_thick + layer_gap)
# 3 ports on +X side, one per layer
for i in range(N_LAYERS):
    pz = ZT + 0.02 + i * (layer_thick + layer_gap)
    px = base_w/2 - 0.005
    cyl(f"port_{i+1}", 0.006, 0.015, (px, 0, pz), (0, math.pi/2, 0), M_port, seg=24)
    cyl(f"port_thread_{i+1}", 0.007, 0.008, (px+0.006, 0, pz), (0, math.pi/2, 0), M_port, seg=24)

# ==== Air supply / pump + pressure control ====
pump_x, pump_y = -0.15, 0.08
box("pump_body", 0.06, 0.05, 0.05, (pump_x, pump_y, ZT+0.025), M_pump)
# Pressure regulator
box("pressure_ctr", 0.04, 0.03, 0.03, (pump_x+0.05, pump_y, ZT+0.015), M_press)
# Pressure gauge (small circle on regulator face)
cyl("gauge_body", 0.012, 0.004, (pump_x+0.06, pump_y+0.016, ZT+0.015), (0, math.pi/2, 0), M_gauge, seg=24)

# Air tubes from pump to each port
pump_out = (pump_x + 0.03, pump_y, ZT + 0.025)
for i in range(N_LAYERS):
    pz = ZT + 0.02 + i * (layer_thick + layer_gap)
    px = base_w/2 - 0.005 - 0.008
    p_end = (px, 0, pz)
    wire(f"air_tube_{i+1}", pump_out, p_end, r=0.0035, m=M_tube)

# ==== Test rig / vertical stand (simulates actuation direction) ====
# Small weight platform above the actuator to show bending
plat_z = z_top + 0.06
box("weight_plat", 0.10, 0.08, 0.005, (0, 0, plat_z), M_fixture)
# 4 struts from fixture to platform
for i,(sx,sy) in enumerate([(0.045,0.035),(-0.045,0.035),(0.045,-0.035),(-0.045,-0.035)]):
    cyl(f"strut_{i}", 0.003, plat_z - (ZT+0.02), (sx, sy, (ZT+0.02+plat_z)/2), (0,0,0), M_fixture, seg=12)
# Small test weight
box("test_weight", 0.03, 0.03, 0.02, (0, 0, plat_z + 0.01), M_fixture)

# ==== Render camera ====
cam_pos = (-0.18, -0.20, 0.20)
cam_tgt = (0.02, 0.0, ZT + 0.06)
d = mathutils.Vector(cam_tgt)-mathutils.Vector(cam_pos)
q = (-d).to_track_quat('Z','Y')
bpy.ops.object.camera_add(location=cam_pos, rotation=q.to_euler())
c = bpy.context.object
c.data.lens = 50; c.data.clip_start = 0.01; c.data.clip_end = 50
sc.camera = c

# Lights
for pos, e in [((0.25,0.1,0.30), 80), ((-0.20,0.25,0.25), 60), ((0.0,-0.20,0.20), 50)]:
    bpy.ops.object.light_add(location=pos, type='POINT')
    bpy.context.object.data.energy = e

# Save & render
out_blend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scene_v01.blend")
out_png   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overview_v01.png")
sc.render.filepath = out_png
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)

with open(out_png,'rb') as f: h = hashlib.sha256(f.read()).hexdigest()
print(f"V22_BUILD_OK blend={out_blend} png={out_png} sha256={h}")
