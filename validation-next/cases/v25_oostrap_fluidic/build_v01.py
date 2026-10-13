"""V25 OoTrap field-deployable fluidic device build_v01.py
OoTrap: oocyte collection + maturation microfluidic device
  - main fluidic body (rounded enclosure, PDMS-like translucent)
  - micro-pore array (capture zone)
  - inlet/outlet ports
  - culture chamber
  - mechanical/fluidic interfaces
Based on SELECTION.md entry 10.1039/d4lc00660g (C-class, RSC official HTML obtained).
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
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.06,0.07,0.08,1.0)
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

def torus(name, R, r, loc, m=None, s1=64, s2=16):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, major_segments=s1, minor_segments=s2)
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
M_pdms   = mat("pdms_body", (0.85,0.88,0.92), rough=0.25, metal=0.0, alpha=0.35)  # translucent PDMS
M_fluid  = mat("media",     (0.20,0.70,0.60), rough=0.15, metal=0.0, alpha=0.50)  # culture medium green-blue
M_por    = mat("pore_ring", (0.50,0.40,0.30), rough=0.5, metal=0.1)               # capture zone
M_oocyte = mat("oocyte",    (0.95,0.85,0.60), rough=0.2, emis=(0.95,0.8,0.5), es=0.4)
M_port   = mat("port_fitting",(0.90,0.90,0.92), rough=0.2, metal=0.3)
M_housing= mat("housing_rim",(0.40,0.40,0.45), rough=0.4, metal=0.4)
M_base   = mat("stand_base",(0.15,0.13,0.10), rough=0.6, metal=0.4)
M_table  = mat("table_top", (0.10,0.08,0.06), rough=0.7, metal=0.2)
M_syr    = mat("syringe",   (0.20,0.20,0.22), rough=0.4, metal=0.5)
M_plung  = mat("plunger",   (0.80,0.80,0.85), rough=0.3, metal=0.2)
M_tube   = mat("tube",      (0.70,0.85,0.95), rough=0.3, alpha=0.5)
M_beam   = mat("flow_arrow",(0.0,0.9,0.6), rough=0.1, emis=(0,0.9,0.6), es=2.0)

# ==== Optical table ====
ZT = 0.04
box("table", 0.40, 0.25, ZT, (0, 0, ZT/2), M_table)
for i,(lx,ly) in enumerate([(-0.18,-0.10),(0.18,-0.10),(-0.18,0.10),(0.18,0.10)]):
    cyl(f"leg_{i}", 0.006, ZT, (lx, ly, ZT/2), (0,0,0), M_table, seg=16)

# ==== Stand / mounting base ====
box("stand_base", 0.15, 0.12, 0.015, (0, 0, ZT+0.0075), M_base)

# ==== Main OoTrap body: rounded translucent PDMS housing ====
# Simplified as a rounded box (ellipsoid-ish)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, ZT+0.035), segments=32, ring_count=16)
o = bpy.context.object; o.name = "oostrap_body"
o.scale = (0.055, 0.040, 0.025)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
o.data.materials.append(M_pdms)

# Internal culture medium (smaller ellipsoid)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, ZT+0.035), segments=24, ring_count=12)
o = bpy.context.object; o.name = "culture_medium"
o.scale = (0.045, 0.032, 0.020)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
o.data.materials.append(M_fluid)

# Micro-pore array: 5×4 grid of small rings on bottom face of body
N_ROWS, N_COLS = 4, 5
por_x_span = 0.06
por_y_span = 0.04
for i in range(N_ROWS):
    for j in range(N_COLS):
        px = -por_x_span/2 + (j+0.5)*por_x_span/N_COLS
        py = -por_y_span/2 + (i+0.5)*por_y_span/N_ROWS
        pz = ZT + 0.012  # just below body surface
        cyl(f"pore_{i}_{j}", 0.002, 0.003, (px, py, pz), (0,0,0), M_por, seg=16)

# Oocytes captured at pores (small spheres)
oocyte_positions = [(0.0, 0.0), (por_x_span/8, -por_y_span/8), (-por_x_span/8, por_y_span/8)]
for k,(ox,oy) in enumerate(oocyte_positions):
    sphere(f"oocyte_{k}", 0.004, (ox, oy, ZT+0.016), M_oocyte, seg=16, rings=8)

# Inlet port (top-left, syringe connected)
inlet_x, inlet_y = -0.055, 0.03
cyl("inlet_port", 0.008, 0.015, (inlet_x, inlet_y, ZT+0.055), (0, math.pi/4, 0), M_port, seg=24)
# Inlet tube
wire("inlet_tube", (inlet_x, inlet_y, ZT+0.062), (inlet_x-0.02, inlet_y+0.01, ZT+0.075), r=0.004, m=M_tube)
# Syringe at end of tube
syr_x, syr_y = inlet_x-0.04, inlet_y+0.02
cyl("syringe_barrel", 0.010, 0.04, (syr_x, syr_y, ZT+0.085), (0, math.pi/3, math.pi/4), M_syr, seg=24)
cyl("syringe_plunger", 0.007, 0.03, (syr_x-0.01, syr_y+0.01, ZT+0.105), (0, math.pi/3, math.pi/4), M_plung, seg=16)

# Outlet port (bottom-right)
outlet_x, outlet_y = 0.055, -0.03
cyl("outlet_port", 0.008, 0.015, (outlet_x, outlet_y, ZT+0.045), (0, -math.pi/4, 0), M_port, seg=24)
# Outlet tube (drip collection)
wire("outlet_tube", (outlet_x, outlet_y, ZT+0.052), (outlet_x+0.04, outlet_y-0.03, ZT+0.03), r=0.004, m=M_tube)
# Collection vial
cyl("vial", 0.008, 0.025, (outlet_x+0.04, outlet_y-0.03, ZT+0.0175), (0,0,0), M_tube, seg=16)

# ==== Flow path visualization (arrows showing fluid direction) ====
# Inlet -> through body -> outlet
p0 = (inlet_x, inlet_y, ZT+0.050)
p1 = (0, 0, ZT+0.035)
p2 = (outlet_x, outlet_y, ZT+0.040)
wire("flow_in", p0, p1, r=0.002, m=M_beam)
wire("flow_out", p1, p2, r=0.002, m=M_beam)

# ==== Housing ring (metallic rim around body, provides mechanical support) ====
torus("housing_rim", 0.062, 0.005, (0, 0, ZT+0.035), M_housing, s1=96, s2=12)

# Support posts under housing
for i in range(4):
    a = math.radians(45 + i*90)
    px = 0.062*math.cos(a)
    py = 0.062*math.sin(a)
    cyl(f"support_post_{i}", 0.004, 0.015, (px, py, ZT+0.0075), (0,0,0), M_housing, seg=12)

# ==== Render camera ====
cam_pos = (-0.15, -0.18, 0.22)
cam_tgt = (0.0, 0.01, ZT+0.05)
d = mathutils.Vector(cam_tgt)-mathutils.Vector(cam_pos)
q = (-d).to_track_quat('Z','Y')
bpy.ops.object.camera_add(location=cam_pos, rotation=q.to_euler())
c = bpy.context.object
c.data.lens = 60; c.data.clip_start = 0.01; c.data.clip_end = 50
sc.camera = c

# Lights
for pos, e in [((0.20,0.15,0.30), 90), ((-0.20,0.10,0.25), 60), ((0.0,-0.20,0.20), 50)]:
    bpy.ops.object.light_add(location=pos, type='POINT')
    bpy.context.object.data.energy = e

# Save & render
out_blend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scene_v01.blend")
out_png   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overview_v01.png")
sc.render.filepath = out_png
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)

with open(out_png,'rb') as f: h = hashlib.sha256(f.read()).hexdigest()
print(f"V25_BUILD_OK blend={out_blend} png={out_png} sha256={h}")
