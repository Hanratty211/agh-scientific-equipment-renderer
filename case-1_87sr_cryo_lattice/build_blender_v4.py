#!/usr/bin/env python3
"""v3 — 87Sr optical lattice clock, proposed 77 K cryo cavity + MOT
Focused on Fig.7 scope only: furnace/Zeeman slower/stages excluded this round.

Round-3 fixes (user feedback 2026-10-10, v2 failed = all-grey PNG):
  - v2 problem root cause: giant grey vacuum box surfaces + camera angle made
    interior invisible. Fixed by:
      1. Vacuum chamber: proper boolean-subtracted box with rectangular port
         openings, so walls are thin (2 mm) not solid slabs
      2. Cavity: proper boolean-subtracted hollow tube (wall 1.5 mm assumed,
         bore radius 5 mm = inner dia 10 mm per paper; length 160 mm per paper)
      3. Aperture: thin ring (ID 2 mm, OD 4 mm) with actual through-hole
      4. Sapphire window: thin tilted disc at rear, rendered solid (not wire)
      5. MOT coils: two toroidal rings, 64 mm diameter, 5 mm wire
      6. Lattice beams: two counter-propagating cylinders (magic wavelength
         [11], no numeric value labelled — see notes)
      7. Clock beam: red, 698 nm, enters via dichroic mirror (proposed)
      8. Two cameras: overview + cavity cross-section
      9. No 3D text labels in either render
    10. Cutaway: front 1/3 of vacuum chamber removed to show interior

Assumptions (recorded, not from paper):
  - Cavity wall thickness 1.5 mm (paper gives ID only)
  - Aperture disc: covers full bore, central through-hole 3 mm radius
    (paper says "aperture separates interrogation volume from rear part";
     hole geometry NOT specified — assumed, recorded here)
  - Vacuum chamber port openings 20 mm square (paper does not specify)
  - Chamber dimensions 200 × 150 × 150 mm (no paper value; schematic)

Output:
  render-output/render_v3_overview.png   (no text, all visible parts)
  render-output/render_v3_cavity_cut.png (cavity cross-section, interior visible)
  render-output/scene_v3.blend
"""
import bpy, math, mathutils

bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.render.resolution_x = 1600
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.engine = 'CYCLES'
scene.cycles.samples = 96
scene.cycles.use_denoising = True

# ---------- materials ----------
def mat(name, base, rough=0.5, metal=0.0, emis=None, es=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = base + (1.0,)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emis:
        b.inputs["Emission Color"].default_value = emis + (1.0,)
        b.inputs["Emission Strength"].default_value = es
    return m

M_VAC    = mat("vac_wall",  (0.50,0.52,0.56), 0.3, 0.8)
M_CU     = mat("copper",     (0.90,0.58,0.35), 0.35, 0.95)
M_CUO    = mat("cuo_inner",  (0.30,0.22,0.18), 0.6, 0.2)
M_SAPPH  = mat("sapphire",   (0.35,0.55,0.85), 0.1, 0.0, (0.4,0.6,0.9), 0.12)
M_BLAKE  = mat("black_anod", (0.08,0.08,0.09), 0.6, 0.5)   # coils / dark metal
M_WIRE   = mat("coil_wire",  (0.15,0.15,0.17), 0.4, 0.7)
M_LAT    = mat("lattice_bm", (0.15,0.45,0.95), 0.2, 0.0, (0.1,0.4,1.0), 2.5)
M_CLK    = mat("clock_bm",   (0.90,0.12,0.12), 0.2, 0.0, (1.0,0.1,0.1), 2.5)
M_Cool   = mat("cool_bm",    (0.10,0.65,0.95), 0.2, 0.0, (0.0,0.55,0.9), 1.8)
M_GLASS  = mat("port_glass", (0.80,0.88,0.95), 0.05, 0.0, (0.85,0.92,1.0), 0.02)
M_ILLUM  = mat("illum",      (1.0,1.0,1.0),    0.0, 0.0, (1.0,1.0,1.0), 4.0)

# ---------- helpers ----------
def box(name, sx, sy, sz, loc, rot=(0,0,0), m=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    o.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    if m: o.data.materials.append(m)
    return o

def cyl(name, r, depth, loc, rot=(0,0,0), m=None, seg=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc,
                                        rotation=rot, vertices=seg)
    o = bpy.context.object; o.name = name
    if m: o.data.materials.append(m)
    return o

def torus(name, R, r, loc, rot=(0,0,0), m=None, s1=96, s2=20):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r,
                                     location=loc, rotation=rot,
                                     major_segments=s1, minor_segments=s2)
    o = bpy.context.object; o.name = name
    if m: o.data.materials.append(m)
    return o

def beam(name, p0, p1, r=0.003, m=None, seg=16):
    v = mathutils.Vector(p1) - mathutils.Vector(p0)
    mid = (mathutils.Vector(p0)+mathutils.Vector(p1))/2
    rot = v.to_track_quat('Z','Y').to_euler()
    return cyl(name, r, v.length, tuple(mid), tuple(rot), m, seg=seg)

def boolean_cut(target, cutter, op='DIFFERENCE'):
    """Apply boolean modifier: target = target OP cutter."""
    md = target.modifiers.new("bool", 'BOOLEAN')
    md.operation = op
    md.object = cutter
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier="bool")
    bpy.data.objects.remove(cutter, do_unlink=True)

# =====================================================================
# GEOMETRY
# Units: metres. Optical axis = x. MOT centre at x=0. Cavity centre at x=-0.08.
# Transport direction: x decreasing (MOT → cavity).
# =====================================================================
MOT_X  = 0.0
CAV_X  = -0.080   # cavity centre (50 mm travel from MOT → cavity mouth)
AXIS_Z = 0.020    # optical axis height above chamber floor

# ---- 1. VACUUM CHAMBER (rectangular, with port holes; front face cut away) ----
# Paper: "vacuum chamber ... windows ... reflection factor 0.86"
# Chamber dims not in paper — assume 200 × 150 × 150 mm (recorded as assumption).
CHAM_W, CHAM_D, CHAM_H = 0.200, 0.150, 0.150
CHAM_CX, CHAM_CY, CHAM_CZ = -0.040, 0.0, 0.0
T = 0.003   # wall thickness 3 mm

# main shell (hollow box)
shell = box("vac_shell", CHAM_W, CHAM_D, CHAM_H, (CHAM_CX, CHAM_CY, CHAM_CZ), m=M_VAC)
inner = box("vac_shell_inner", CHAM_W - 2*T, CHAM_D - 2*T, CHAM_H - 2*T,
            (CHAM_CX, CHAM_CY, CHAM_CZ))
boolean_cut(shell, inner)

# cutaway: remove front half AND top front quarter → interior visible from
# any camera in +y/+z/+x octants. (documented: vacuum shell open on front face)
cut1 = box("vac_cut_front", CHAM_W + 0.02, CHAM_D*0.52, CHAM_H + 0.02,
            (CHAM_CX, -CHAM_D*0.55, CHAM_CZ))
boolean_cut(shell, cut1)
cut2 = box("vac_cut_topfront", CHAM_W + 0.02, CHAM_D*0.35, CHAM_H*0.5,
            (CHAM_CX, -CHAM_D*0.25, CHAM_CZ + CHAM_H*0.35))
boolean_cut(shell, cut2)

# port holes: 20 mm square openings on top and bottom walls (assumed size)
PORT = 0.020
for name, pos, rot in [
    ("port_top",   (CHAM_CX,  0.0,  CHAM_CZ + CHAM_H/2 - T/2), (0,0,0)),
    ("port_bottom",(CHAM_CX,  0.0,  CHAM_CZ - CHAM_H/2 + T/2), (0,0,0)),
    ("port_right", (CHAM_CX + CHAM_W/2 - T/2, 0.0, CHAM_CZ),   (0, math.radians(90), 0)),
    ("port_left",  (CHAM_CX - CHAM_W/2 + T/2, 0.0, CHAM_CZ),   (0, math.radians(90), 0)),
]:
    hole = box(name+"_hole", PORT, PORT, T*3, pos, rot=rot)
    boolean_cut(shell, hole)

# glass windows at ports (thin, semi-transparent)
for name, pos, rot in [
    ("win_top",   (CHAM_CX, 0.0, CHAM_CZ + CHAM_H/2 - T/2), (0,0,0)),
    ("win_right", (CHAM_CX + CHAM_W/2 - T/2, 0.0, CHAM_CZ), (0, math.radians(90), 0)),
    ("win_left",  (CHAM_CX - CHAM_W/2 + T/2, 0.0, CHAM_CZ), (0, math.radians(90), 0)),
]:
    box(name, PORT, PORT, T*0.15, pos, rot=rot, m=M_GLASS)

# ---- 2. MOT COILS (two opposing toroidal rings, 64 mm dia, 5 mm wire) ----
# Paper: "MOT coils ... located inside the vacuum chamber"
# Fig.7 caption: "MOT coils" — two opposing quadrupole coils.
for label, dx in [("mot_coil_L", -0.040), ("mot_coil_R", 0.040)]:
    torus(label, R=0.032, r=0.003, loc=(MOT_X + dx, 0.0, AXIS_Z),
          rot=(0, math.radians(90), 0), m=M_WIRE)

# ---- 3. MOT COOLING BEAMS (blue 461 nm, 6-beam MOT — show 4 main pairs) ----
b1 = beam("cool_bm_1", (MOT_X + 0.060,  0.050, AXIS_Z),
                          (MOT_X - 0.010, -0.050, AXIS_Z), r=0.0025, m=M_Cool)
b2 = beam("cool_bm_2", (MOT_X + 0.060, -0.050, AXIS_Z),
                          (MOT_X - 0.010,  0.050, AXIS_Z), r=0.0025, m=M_Cool)
b3 = beam("cool_bm_3", (MOT_X + 0.010,  0.0, AXIS_Z + 0.050),
                          (MOT_X - 0.010,  0.0, AXIS_Z - 0.050), r=0.0025, m=M_Cool)
b4 = beam("cool_bm_4", (MOT_X - 0.010,  0.0, AXIS_Z + 0.050),
                          (MOT_X + 0.010,  0.0, AXIS_Z - 0.050), r=0.0025, m=M_Cool)

# ---- 4. 1D OPTICAL LATTICE BEAMS (magic wavelength [11], Ti:Sapphire) ----
# Paper: "horizontally oriented 1D optical lattice ... two air bearing stages
# ... lattice light emitted from LMA fiber ... retro-reflected"
# Two counter-propagating beams along x-axis, focused at MOT → cavity.
# Magic wavelength value NOT labelled (see notes: not numerically verified
# from paper body; [11] = Katori PRL 91:173005 2003).
lb1 = beam("lat_beam_1", (MOT_X + 0.055, 0.0, AXIS_Z),
                          (CAV_X - 0.045, 0.0, AXIS_Z), r=0.0028, m=M_LAT)
lb2 = beam("lat_beam_2", (CAV_X - 0.045, 0.0, AXIS_Z),
                          (MOT_X + 0.055, 0.0, AXIS_Z), r=0.0028, m=M_LAT)
# fiber entry (right side)
cyl("lat_fiber", 0.0035, 0.025, (MOT_X + 0.060, 0.0, AXIS_Z),
    (0, math.radians(90), 0), m=M_ILLUM, seg=24)

# ---- 5. CLOCK LASER BEAM (698 nm, red, via dichroic — proposed) ----
# Paper: "In the final setup the clock laser beam will be overlapped with
# the lattice beam through a dichroic mirror"
clk = beam("clock_bm", (MOT_X - 0.040, 0.028, AXIS_Z),
                         (CAV_X,        0.0,   AXIS_Z), r=0.0020, m=M_CLK)
# dichroic mirror (thin tilted disc, at cavity entrance region)
box("dichroic_mir", 0.018, 0.018, 0.0006,
    (CAV_X + 0.040, 0.014, AXIS_Z),
    rot=(0, math.radians(45), 0), m=M_SAPPH)

# ---- 6. CRYOGENIC COPPER CAVITY (proposed, Fig.7) ----
# Paper: "cylindrical copper structure ... inner diameter of about 10 mm
# and a length of 160 mm. An aperture separates the interrogation volume
# from the rear part. The inside will be covered by a CuO layer.
# The rear end will be closed by a tilted window that is transparent for
# the lattice laser light but absorbs BBR."
# Assumption (recorded, NOT in paper): wall thickness 1.5 mm → OD 13 mm
CAV_R_IN  = 0.005   # 5 mm = ID/2
CAV_WALL  = 0.0015  # 1.5 mm (assumption)
CAV_R_OUT = CAV_R_IN + CAV_WALL   # 6.5 mm
CAV_LEN   = 0.160   # 160 mm

# outer cylinder
cav_outer = cyl("cav_outer", CAV_R_OUT, CAV_LEN, (CAV_X, 0.0, AXIS_Z),
                (0, math.radians(90), 0), m=M_CU, seg=64)
# bore (inner cylinder to subtract)
bore = cyl("cav_bore", CAV_R_IN, CAV_LEN + 0.002, (CAV_X, 0.0, AXIS_Z),
           (0, math.radians(90), 0), m=M_CUO, seg=64)
boolean_cut(cav_outer, bore)
# CuO inner lining (thin shell inside bore)
lining = cyl("cuo_lining", CAV_R_IN - 0.0002, CAV_LEN * 0.98, (CAV_X, 0.0, AXIS_Z),
             (0, math.radians(90), 0), m=M_CUO, seg=64)
lining_inner = cyl("cuo_lining_inner", CAV_R_IN - 0.0006, CAV_LEN * 0.98,
                   (CAV_X, 0.0, AXIS_Z), (0, math.radians(90), 0))
boolean_cut(lining, lining_inner)

# aperture disc (mid-cavity): disc covering full bore, small central through-hole
# (paper: "An aperture separates the interrogation volume from the rear part"
#  — actual geometry = disc with central hole for light/atoms, hole size NOT
#  specified in paper; assumption recorded)
AP_HOLE_R = 0.003   # 3 mm hole radius (assumption, not in paper)
ap_disc = cyl("ap_ring", CAV_R_IN - 0.0002, 0.004, (CAV_X, 0.0, AXIS_Z),
              (0, math.radians(90), 0), m=M_CUO, seg=64)
ap_hole = cyl("ap_hole", AP_HOLE_R, 0.005, (CAV_X, 0.0, AXIS_Z),
              (0, math.radians(90), 0))
boolean_cut(ap_disc, ap_hole)

# tilted sapphire window at rear end (paper: "tilted window ... transparent
# for lattice laser light but absorbs BBR")
box("sapph_window", 0.012, 0.012, 0.0006,
    (CAV_X - CAV_LEN/2 - 0.002, 0.0, AXIS_Z),
    rot=(0, math.radians(20), 0), m=M_SAPPH)

# interrogation volume: small glowing marker at MOT-end half of cavity
iv_x = CAV_X + CAV_LEN*0.18
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.003, location=(iv_x, 0.0, AXIS_Z),
                                     segments=32, ring_count=16)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.003, location=(CAV_X, 0.0, AXIS_Z),
                                     segments=32, ring_count=16)
iv = bpy.context.object; iv.name = "interrogation_vol"
iv.data.materials.append(M_ILLUM)

# =====================================================================
# CAMERAS
# =====================================================================
def make_cam(name, loc, look_at, lens=50):
    d = mathutils.Vector(look_at) - mathutils.Vector(loc)
    quat = (-d).to_track_quat('Z','Y')
    rot = quat.to_euler()
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    c = bpy.context.object; c.name = name
    c.data.lens = lens
    return c

# v4 修正：总览取景（v3 过近，铜腔被放大/截断）。场景实际范围 x∈[-0.168,0.073]，
# 对角线 ~0.32 m。把相机后移 + 缩短焦段，保证整个装置 + 四周余量入框。
# cam1 总览：从 -y 侧（剖切开口侧）对角看全场景
cam1 = make_cam("cam_overview", (0.22, -0.44, 0.28),
                look_at=(-0.045, 0.0, 0.02), lens=40)

# cam2 铜腔正面：从腔体左端(-x)沿轴看向腔内，看 aperture+内壁+后窗
cam2 = make_cam("cam_cavity", (-0.22, 0.0, AXIS_Z),
                look_at=(CAV_X + 0.05, 0.0, AXIS_Z), lens=60)

# cam3 侧视剖切：纯 -y 方向看腔体轴线（x-z 平面）
cam3 = make_cam("cam_cut", (CAV_X, -0.26, AXIS_Z + 0.015),
                look_at=(CAV_X, 0.0, AXIS_Z), lens=28)

scene.camera = cam1

# lights
sun1 = bpy.data.objects.new("key", bpy.data.lights.new("key",'SUN'))
sun1.location = (0.4, -0.3, 0.6); sun1.rotation_euler = (math.radians(45),0,math.radians(20))
scene.collection.objects.link(sun1); sun1.data.energy = 3.5

sun2 = bpy.data.objects.new("fill", bpy.data.lights.new("fill",'SUN'))
sun2.location = (-0.4, 0.3, 0.2); sun2.rotation_euler = (math.radians(25),0,math.radians(-20))
scene.collection.objects.link(sun2); sun2.data.energy = 1.2

# world
world = bpy.data.worlds[0] if bpy.data.worlds else bpy.data.worlds.new("W")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.05,0.05,0.06,1.0)

# =====================================================================
# RENDER — two outputs
# =====================================================================
bpy.ops.wm.save_as_mainfile(filepath="render-output/scene_v4.blend")
print("scene_v4.blend saved")

def render(cam_obj, out):
    scene.camera = cam_obj
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    print("rendered", out)

render(cam1, "render-output/render_v4_overview.png")
render(cam3, "render-output/render_v4_cavity_cut.png")
print("v4 renders done (overview + cavity cut, per delivery spec)")
print("all v3 renders done")
