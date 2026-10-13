"""V26 build_v01.py — v03: T-junction with OPEN-TOP channel (no top lid),
high-contrast fluid, orange particle, 3 visible port bores into channel,
optical bench stand feet (no floating blocks).
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
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.03, 0.04, 0.06, 1.0)
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

def sphere(name, r, loc, m=None, seg=20, rings=10):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=rings)
    o = bpy.context.object; o.name = name
    if m: o.data.materials.append(m)
    return o

def wire(name, p0, p1, r=0.0008, m=None):
    v = mathutils.Vector(p1)-mathutils.Vector(p0)
    mid = (mathutils.Vector(p0)+mathutils.Vector(p1))/2
    rot = v.to_track_quat('Z','Y').to_euler()
    o = cyl(name, r, v.length, tuple(mid), tuple(rot), m, seg=12)
    o['wire_p0'] = tuple(p0); o['wire_p1'] = tuple(p1)
    return o

sc = setup()

# ==== Dimensions (m) ====
W   = 0.03   # main arm width  (Y)
Lm  = 0.12   # main arm length (X)
Wb  = 0.03   # branch width    (X)
Lb  = 0.08   # branch length   (Y)
D   = 0.012  # channel depth
Zb  = 0.02   # base plate top z
Zt  = Zb + D # channel top z
CZ  = Zb + D/2
WbX = Wb/2   # branch center x (main arm right end)
Byy = Lb/2 + W/2  # branch center y (main arm top + branch/2)

# ==== Materials ====
M_base   = mat("base_plate",  (0.15,0.15,0.18), rough=0.5, metal=0.5)
M_wall   = mat("wall_solid",  (0.40,0.45,0.55), rough=0.3, metal=0.3)  # visible grey-blue
M_fluid  = mat("fluid_hi",    (0.00,0.55,0.95), rough=0.05, metal=0.0, alpha=0.45)  # high-contrast blue
M_tracer = mat("tracer_orange",(1.00,0.45,0.00), rough=0.15, metal=0.1, emis=(1.0,0.4,0), es=1.2)
M_port   = mat("port_metal",  (0.70,0.70,0.75), rough=0.2, metal=0.8)
M_bore   = mat("bore_ring",   (1.00,0.80,0.00), rough=0.3, metal=0.2, emis=(1,0.8,0), es=0.5)  # gold ring = visible bore
M_optic  = mat("optic_glass", (0.85,0.90,1.00), rough=0.05, metal=0.0, alpha=0.25)
M_beam   = mat("green_beam",  (0.00,1.00,0.20), rough=0.1, emis=(0,1,0.2), es=3.0)
M_stand  = mat("optical_bench",(0.25,0.20,0.15), rough=0.6, metal=0.3)  # dark wooden bench
M_lens   = mat("lens_dark",   (0.10,0.10,0.12), rough=0.1, metal=0.0)

# ==== Base plate (solid, dark) ====
box("base_plate", Lm + Wb + 0.04, Lb + W + 0.06, Zb, (WbX - Wb/2, Byy - (Lb+W)/2, Zb/2), M_base)

# ==== T-channel: THREE WALLS (bottom + 2 side walls), NO TOP LID ====
# Bottom of channel (flat plate the channel sits on)
box("channel_bottom", Lm + Wb, Lb + W, 0.004, (WbX - Wb/2, Byy - (Lb+W)/2, Zb + 0.002), M_wall)

# Main arm left wall
box("wall_main_left", Lm, 0.004, D, (WbX - Wb/2 - Lm/2, W/2 - 0.002, CZ), M_wall)
# Main arm right wall
box("wall_main_right", Lm, 0.004, D, (WbX - Wb/2 + Lm/2, W/2 + 0.002, CZ), M_wall)
# Branch arm front wall
box("wall_branch_front", Wb, 0.004, D, (WbX, Byy - Lb/2 - 0.002, CZ), M_wall)
# Branch arm back wall
box("wall_branch_back", Wb, 0.004, D, (WbX, Byy + Lb/2 + 0.002, CZ), M_wall)
# Outer walls: top of main arm (left side)
box("wall_main_outer_top", Lm + Wb, 0.004, D, (WbX - Wb/2 - Lm/2 - 0.002, W/2 + 0.002 + Lm/2, CZ), M_wall)

# ==== Fluid filling the T-channel (open top, high-contrast blue) ====
# Main arm fluid (no top lid so fluid surface visible from above)
box("fluid_main", Lm, W - 0.004, D - 0.006, (WbX - Wb/2, W/2, CZ - 0.003), M_fluid)
# Branch arm fluid
box("fluid_branch", Wb - 0.004, Lb, D - 0.006, (WbX, Byy, CZ - 0.003), M_fluid)

# ==== Orange particle (spherical, glowing, clearly visible) ====
particle = sphere("particle_tracer", 0.006, (WbX - 0.02, W/2, CZ), M_tracer, seg=32, rings=16)
# Small emissive core to ensure visibility
core = sphere("particle_core", 0.003, (WbX - 0.02, W/2, CZ), M_tracer, seg=16, rings=8)

# ==== 3 port fittings: flared collar + stem + GOLD BORE RING visible in channel top ====
port_pos = [
    (WbX - Wb/2 - Lm/2 + 0.015, W/2),        # inflow (left end of main arm)
    (WbX - Wb/2 + Lm/2 - 0.015, W/2),        # outflow (right end of main arm, before branch)
    (WbX, Byy + Lb/2 - 0.01),                 # branch outflow
]
for i, (px, py) in enumerate(port_pos):
    # Flared collar sits on top of channel wall
    cyl(f"port_collar_{i}", 0.010, 0.006, (px, py, Zt + 0.003), (0,0,0), M_port, seg=32)
    # Stem going down into channel
    cyl(f"port_stem_{i}",  0.005, 0.010, (px, py, Zt - 0.002), (0,0,0), M_port, seg=24)
    # GOLD bore ring at channel top surface — visible from above, marks the fluid connection
    cyl(f"port_bore_ring_{i}", 0.0065, 0.002, (px, py, Zt - 0.004), (0,0,0), M_bore, seg=32)

# ==== Laser input arm (from -Y side of main arm, visible glass block) ====
laser = box("laser_input_block", 0.025, 0.06, D, (WbX - Wb/2 - Lm/2, -0.04, CZ), M_optic)

# ==== Green observation beam: laser arm -> through T -> detector at +Y ====
p0 = (WbX - Wb/2 - Lm/2, -0.04, CZ)
p1 = (WbX, Byy + Lb/2 + 0.02, CZ)
wire("observation_beam", p0, p1, r=0.0015, m=M_beam)

# ==== Detector on optical bench (rests on bench, not floating) ====
# Bench top plate
bench_y = Byy + Lb/2 + 0.06
box("optical_bench", 0.20, 0.08, 0.01, (WbX, bench_y, Zb - 0.005), M_stand)
# Bench legs (4)
for i,(lx,ly) in enumerate([(WbX-0.09, bench_y-0.035),(WbX+0.09, bench_y-0.035),
                              (WbX-0.09, bench_y+0.035),(WbX+0.09, bench_y+0.035)]):
    cyl(f"bench_leg_{i}", 0.004, 0.08, (lx, ly, Zb - 0.005 - 0.04 - 0.04), (0,0,0), M_stand, seg=16)

# Detector block on bench (solid base, not floating)
det_base = box("detector_base", 0.06, 0.04, 0.015, (WbX, bench_y, Zb - 0.005 + 0.0075), M_stand)
det_body = box("detector_body", 0.05, 0.03, 0.035, (WbX, bench_y, Zb - 0.005 + 0.015 + 0.0175), M_stand)
# Detector lens (dark glass, visible)
cyl("detector_lens", 0.012, 0.015, (WbX, bench_y - 0.018, Zb - 0.005 + 0.03), (0, math.pi/2, 0), M_lens, seg=32)
# Lens face (slightly emissive to show it's a detection face)
cyl("detector_face", 0.010, 0.002, (WbX, bench_y - 0.022, Zb - 0.005 + 0.03), (0, math.pi/2, 0), M_beam, seg=32)

# Camera on bench, behind detector
cam_base = box("camera_base", 0.07, 0.05, 0.02, (WbX, bench_y + 0.04, Zb - 0.005 + 0.01), M_stand)
cam_body = box("camera_body",  0.06, 0.04, 0.04, (WbX, bench_y + 0.04, Zb - 0.005 + 0.02 + 0.02), M_stand)
cyl("camera_lens", 0.015, 0.025, (WbX, bench_y + 0.04 - 0.025, Zb - 0.005 + 0.04), (0, math.pi/2, 0), M_lens, seg=32)
# Camera lens face (slightly emissive)
cyl("camera_lens_face", 0.012, 0.002, (WbX, bench_y + 0.04 - 0.032, Zb - 0.005 + 0.04), (0, math.pi/2, 0), mat("cam_face",(0.2,0.4,0.9),rough=0.05,emis=(0.2,0.4,0.9),es=1.0), seg=32)

# ==== Camera for render ====
cam_pos = (0.25, bench_y + 0.15, 0.20)
cam_tgt = (WbX, Byy*0.3, Zt*0.5)
d = mathutils.Vector(cam_tgt) - mathutils.Vector(cam_pos)
q = (-d).to_track_quat('Z','Y')
bpy.ops.object.camera_add(location=cam_pos, rotation=q.to_euler())
c = bpy.context.object
c.data.lens = 55; c.data.clip_start = 0.01; c.data.clip_end = 50
sc.camera = c

# Lights
bpy.ops.object.light_add(location=(0.3, 0.1, 0.30), type='POINT')
bpy.context.object.data.energy = 80
bpy.ops.object.light_add(location=(-0.2, 0.4, 0.20), type='POINT')
bpy.context.object.data.energy = 40

# Save & render v03
out_blend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scene_v03.blend")
out_png   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overview_v03.png")
sc.render.filepath = out_png
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)

with open(out_png,'rb') as f: h = hashlib.sha256(f.read()).hexdigest()
print(f"V26_V03_OK blend={out_blend} png={out_png} sha256={h}")
