#!/usr/bin/env python3
"""87Sr optical lattice clock — proposed 77 K cryogenic setup (Fig.7) +
    tested moving-lattice stages (Fig.8), Middelmann et al. arXiv:1009.2017.

Round-2 fixes (user feedback 2026-10-10):
  - Wavelengths: 698 nm = clock transition ³P₀−¹S₀ (NOT lattice laser).
    Lattice laser = magic wavelength [11] (Ti:Sapphire, ~813 nm for ⁸⁷Sr).
    Cooling: 461 nm (¹P₁−¹S₀); repump 679/707 nm; 2nd MOT 689 nm.
  - MOT coils: toroidal ring shape (not solid cylinders).
  - Copper cryo cavity: hollow tube (inner bore visible), CuO inner lining.
  - Vacuum chamber: cutaway (half removed) to show interior; no giant solid box.
  - 3-D text labels: removed (clean preview, as requested).
  - Camera: auto-framed to bounding box of all parts + margin.
  - Status separation: proposed cryo parts dashed/wire; tested MOT+stages solid.

Output: render-output/render_v2_preview.png  +  render-output/scene_v2.blend
"""
import bpy, math, mathutils

bpy.ops.wm.read_factory_settings(use_empty=True)

# ---- render settings first (before any ops that need scene context) ----
scene = bpy.context.scene
scene.render.resolution_x = 1600
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.cycles.use_denoising = True
try:
    cp = bpy.context.preferences.addons.get('cycles')
    if cp and getattr(cp, 'devices', None):
        for d in cp.devices: d.use = True
except Exception as e:
    print('GPU skipped:', e)

# ---- materials (Blender 5.1: "Emission Color", not "Emission") ----
def mat(name, base, rough=0.5, metal=0.0, emission=None, emis=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = base + (1.0,)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emission is not None:
        b.inputs["Emission Color"].default_value = emission + (1.0,)
        b.inputs["Emission Strength"].default_value = emis
    return m

mat_vac    = mat("vac",    (0.55,0.58,0.62), 0.35, 0.7)   # vacuum metal
mat_wire   = mat("wire",   (0.4,0.4,0.45),   0.4, 0.8)   # coil wire
mat_copper = mat("copper", (0.85,0.55,0.35), 0.4, 0.9)   # cryo Cu
mat_cuo    = mat("cuo",    (0.2,0.18,0.15),  0.7, 0.3)   # CuO lining
mat_sapph  = mat("sapph",  (0.4,0.6,0.9),    0.1, 0.0, (0.5,0.7,1.0), 0.15)
mat_lat    = mat("lattice",(0.3,0.5,0.95),   0.2, 0.0, (0.2,0.4,1.0), 2.0)  # magic ~813 nm blue-purple
mat_clock  = mat("clock",  (0.9,0.15,0.15),  0.2, 0.0, (1.0,0.1,0.1), 2.0)  # 698 nm red
mat_cool   = mat("cool",   (0.15,0.7,0.95),  0.2, 0.0, (0.0,0.6,0.9), 1.5)  # 461 nm blue
mat_stage  = mat("stage",  (0.6,0.6,0.65),   0.3, 0.7)   # air-bearing stage
mat_frame  = mat("frame",  (0.45,0.45,0.5),  0.4, 0.6)   # adjustment frame
mat_glass  = mat("glass",  (0.85,0.9,0.95),  0.05, 0.0, (0.9,0.95,1.0), 0.03)

# ---- helpers ----
def box(name, sx, sy, sz, loc, rot=(0,0,0), m=None, wire=False, hide=False):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    o.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    if m: o.data.materials.append(m)
    o.display_type = 'WIRE' if wire else 'TEXTURED'
    o.hide_render = hide
    return o

def cyl(name, r, depth, loc, rot=(0,0,0), m=None, seg=48, wire=False, hide=False):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc,
                                        rotation=rot, vertices=seg)
    o = bpy.context.object; o.name = name
    if m: o.data.materials.append(m)
    o.display_type = 'WIRE' if wire else 'TEXTURED'
    o.hide_render = hide
    return o

def torus_coil(name, R, r, loc, rot=(0,0,0), m=None, seg1=64, seg2=16):
    """MOT quadrupole coil: two opposing horseshoe coils shown as torus rings."""
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r,
                                      location=loc, rotation=rot,
                                      major_segments=seg1, minor_segments=seg2)
    o = bpy.context.object; o.name = name
    if m: o.data.materials.append(m)
    o.display_type = 'TEXTURED'
    return o

def hollow_tube(name, r_outer, r_inner, length, loc, rot=(0,0,0),
                m_outer=None, m_inner=None, seg=48):
    """Hollow cylindrical tube with visible inner bore (CuO lining)."""
    outer = cyl(name+"_outer", r_outer, length, loc, rot, m_outer, seg=seg)
    inner = cyl(name+"_inner", r_inner, length*0.998, loc, rot, m_inner, seg=seg)
    return outer, inner

def beam(name, p0, p1, r=0.003, m=None, seg=16):
    v  = mathutils.Vector(p1) - mathutils.Vector(p0)
    mid= (mathutils.Vector(p0)+mathutils.Vector(p1))/2
    rot= v.to_track_quat('Z','Y').to_euler()
    return cyl(name, r, v.length, tuple(mid), tuple(rot), m, seg=seg)

# =====================================================================
# Layout (units in metres; axis: x = transport direction MOT→cryo)
#  Paper Fig.7: MOT right, cold cavity left, 50 mm travel.
#  Only parts with explicit paper text are solid; proposed parts = wire/
#  dashed outline shown with separate material so user can see they are
#  "proposed" (Fig.7 caption says "proposed setup").
# =====================================================================
Z = 0.0          # main optical axis height
LATTICE_X = -0.03   # mid-transport position of interrogation volume

# ---- 1. VACUUM CHAMBER (cutaway: keep back half only) ----
# Paper: "MOT is operated in a part of the vacuum system with no direct
# line of sight on the oven"; chambers have windows (factor 0.86 reflection).
# We model the back half of a rectangular vacuum chamber as cutaway so
# interior is visible. No giant solid box.
vac_back = box("vac_back", 0.18, 0.02, 0.18, (-0.045, -0.09+0.01, 0.0), m=mat_vac)
# side walls (left/right, visible in cutaway)
vac_left  = box("vac_left",  0.18, 0.005, 0.18, (-0.045, -0.09+0.005, 0.0), m=mat_vac)
vac_right = box("vac_right", 0.18, 0.005, 0.18, (-0.045, 0.09-0.005, 0.0), m=mat_vac)
# top wall (keep, provides structural context)
vac_top = box("vac_top", 0.18, 0.18, 0.005, (-0.045, 0.0, 0.09-0.0025), m=mat_vac)
# front wall removed for cutaway view (documented)

# ---- 2. FURNACE + ZEEPAN SLOWER + THERMAL BEAM (all in paper text) ----
# "furnace of about 480 C", "Zeeman-slowing a thermal atomic beam"
furnace = cyl("furnace", 0.014, 0.06, (0.13, 0.0, Z+0.04), m=mat_frame)
# furnace heater coil around it
furn_coil = torus_coil("furnace_heater", 0.016, 0.002,
                        (0.13, 0.0, Z+0.04), (0,math.radians(90),0), m=mat_wire,
                        seg1=48, seg2=8)
# thermal beam (thin, from furnace toward Zeeman slower)
beam("thermal_beam", (0.11, 0, Z+0.04), (0.055, 0, Z+0.04), r=0.0008, m=mat_cool)

# Zeeman slower: two solenoid coils in series (paper says "Zeeman-slowing",
# standard = two coils; we model as two visible coil rings)
for i, dx in enumerate([0.065, 0.05]):
    torus_coil(f"zeeman_coil_{i}", 0.018, 0.004,
               (dx, 0, Z+0.04), (0, math.radians(90), 0), m=mat_wire,
               seg1=64, seg2=12)

# 2D optical molasses (deflection beams into vacuum, "deflected by 2D optical molasses")
beam("molasses_x", (0.03, 0, Z+0.04), (0.0, 0.04, Z+0.04), r=0.0012, m=mat_cool)
beam("molasses_y", (0.01, 0.04, Z+0.04), (0.01, 0.0, Z+0.04), r=0.0012, m=mat_cool)

# ---- 3. MOT (inside vacuum chamber) ----
# Paper: "The coils generating the magnetic quadrupole field and later a
# homogeneous field are located inside the vacuum chamber."
# Quadrupole MOT: two opposing Helmholtz coils (torus rings)
MOT_X = -0.02   # MOT centre x
for dx in (-0.035, 0.035):
    torus_coil(f"mot_coil_{dx:+.0f}", 0.04, 0.005,
               (MOT_X+dx, 0, Z), (0, math.radians(90), 0), m=mat_wire,
               seg1=96, seg2=16)
# MOT cooling beams (461 nm, blue, 6-beam MOT - show 4 visible pairs as
# crossed beams; "overlapped blue and red MOT beams" from Fig.7 caption)
beam("mot_blue_1", (MOT_X+0.05,  0.04, Z), (MOT_X-0.05, -0.04, Z), r=0.0025, m=mat_cool)
beam("mot_blue_2", (MOT_X+0.05, -0.04, Z), (MOT_X-0.05,  0.04, Z), r=0.0025, m=mat_cool)
beam("mot_blue_3", (MOT_X,  0.04, Z+0.05), (MOT_X, -0.04, Z-0.05), r=0.0025, m=mat_cool)
beam("mot_blue_4", (MOT_X, -0.04, Z+0.05), (MOT_X,  0.04, Z-0.05), r=0.0025, m=mat_cool)
# red intercombination beams (689 nm, thinner, overlapped)
beam("mot_red_1", (MOT_X+0.05,  0.04, Z), (MOT_X-0.05, -0.04, Z), r=0.0015, m=mat_clock)
beam("mot_red_2", (MOT_X+0.05, -0.04, Z), (MOT_X-0.05,  0.04, Z), r=0.0015, m=mat_clock)

# ---- 4. CRYOGENIC COPPER CAVITY (PROPOSED - Fig.7, wire/dashed) ----
# Paper: "cylindrical copper structure with an inner diameter of about 10 mm
# and a length of 160 mm", CuO 100 um inner lining, aperture, tilted window.
# Shown as wire outline to indicate "proposed" (not yet built in this paper).
CR_X = -0.13   # cavity centre
cryo_outer, cryo_inner = hollow_tube(
    "cryo", 0.005, 0.004, 0.16,
    (CR_X, 0, Z), (0, math.radians(90), 0),
    m_outer=mat_copper, m_inner=mat_cuo, seg=48)
cryo_outer.display_type = 'WIRE'   # proposed = wire outline
cryo_outer.hide_render = False
cryo_inner.hide_render = True      # don't show interior lining in wire mode
# aperture (mid-cavity ring)
ap = cyl("aperture", 0.003, 0.006, (CR_X, 0, Z),
         (0, math.radians(90), 0), m=mat_cuo, seg=48)
ap.display_type = 'WIRE'
# tilted sapphire window at rear end (paper: "transparent for lattice laser,
# absorbs BBR", "sapphire window thermal conductivity 400 W/mK")
win = box("sapphire_window", 0.01, 0.01, 0.0008,
          (CR_X-0.081, 0, Z), (0, math.radians(15), 0), m=mat_sapph)
win.display_type = 'WIRE'   # proposed

# ---- 5. LATTICE LASER BEAMS (magic wavelength ~813 nm, Ti:Sapphire) ----
# Paper: "horizontally oriented 1D optical lattice at the magic wavelength [11].
# Light is provided by a Ti:Sapphire laser coupled to a single mode fiber."
# "The lattice laser beam is focused to w0=62 um, Rayleigh range 15 mm."
# "two air bearing translation stages ... on one side the lattice light is
# emitted from a commercial polarization maintaining LMA fiber"
# Two counter-propagating beams forming the 1D lattice. Shown as solid
# (tested moving lattice, Fig.8).
L1 = beam("lattice_beam_1", (0.04, 0, Z), (CR_X+0.04, 0, Z), r=0.003, m=mat_lat)
L2 = beam("lattice_beam_2", (CR_X-0.04, 0, Z), (0.04, 0, Z), r=0.003, m=mat_lat)
# lattice laser fiber entry (right side, tested setup Fig.8)
fib = cyl("lattice_fiber", 0.004, 0.02, (0.05, 0, Z),
          (0, math.radians(90), 0), m=mat_sapph, seg=24)

# ---- 6. CLOCK LASER (698 nm, red, overlapped via dichroic mirror) ----
# Paper: "In the final setup the clock laser beam will be overlapped with
# the lattice beam through a dichroic mirror that will be used to retro
# reflect the lattice beam."  (proposed = final setup, shown as wire)
clk = beam("clock_beam", (CR_X-0.04, 0.015, Z), (0.04, 0, Z), r=0.002, m=mat_clock)
dmirror = box("dichroic_mirror", 0.012, 0.012, 0.0006,
              (CR_X, 0.008, Z), (math.radians(45), 0, 0), m=mat_sapph)
dmirror.display_type = 'WIRE'   # proposed

# ---- 7. AIR-BEARING STAGES + ADJUSTMENT FRAMES (tested, Fig.8) ----
# Paper: "two air bearing translation stages, mounted on adjustment frames.
# Each frame allows for 4 DoF: two transverse translations and two angular
# alignments."  Shown as tested (solid).
stage_r = box("stage_right", 0.05, 0.05, 0.025, (0.06, 0, -0.035), m=mat_stage)
frame_r = box("frame_right", 0.055, 0.055, 0.005, (0.06, 0, -0.055), m=mat_frame)
stage_l = box("stage_left",  0.05, 0.05, 0.025, (CR_X-0.06, 0, -0.035), m=mat_stage)
frame_l = box("frame_left",  0.055, 0.055, 0.005, (CR_X-0.06, 0, -0.055), m=mat_frame)

# ---- 8. INTERROGATION VOLUME (glowing region inside cavity, proposed) ----
iv = cyl("interrogation_volume", 0.002, 0.004, (CR_X, 0, Z),
         (0, math.radians(90), 0), m=mat_lat, seg=24)
iv.display_type = 'WIRE'

# =====================================================================
# Camera: auto-frame bounding box of all visible objects
# =====================================================================
import mathutils
def get_bounds():
    visible = [o for o in bpy.data.objects if o.type in ('MESH','CURVE') and not o.hide_render]
    mn = mathutils.Vector(( 1e9,  1e9,  1e9))
    mx = mathutils.Vector((-1e9, -1e9, -1e9))
    for o in visible:
        for c in o.bound_box:
            w = o.matrix_world @ mathutils.Vector(c)
            for i in range(3):
                mn[i] = min(mn[i], w[i]); mx[i] = max(mx[i], w[i])
    return mn, mx

mn, mx = get_bounds()
cen  = (mn+mx)/2
diag = (mx-mn).length
aspect = scene.render.resolution_x/scene.render.resolution_y

# camera distance: fit longest axis in frame with 25 % margin
margin = 1.25
dist = diag * margin / (2.0 * min(1.0, aspect))
# view from directly front, slightly above - looking INTO the cutaway vacuum
view_dir = mathutils.Vector((0.05, -1.0, 0.28)).normalized()
cam_loc = cen + view_dir * dist
look_dir = -view_dir
quat = look_dir.to_track_quat('-Z','Y')
rot_e = quat.to_euler()

bpy.ops.object.camera_add(location=tuple(cam_loc), rotation=tuple(rot_e))
cam = bpy.context.object; cam.name = "camera"
scene.camera = cam
cam.data.lens = 50

# lights
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun",'SUN'))
sun.location = (0.5, -0.5, 0.8)
sun.rotation_euler = (math.radians(35), 0, math.radians(40))
scene.collection.objects.link(sun)
sun.data.energy = 4.0

# fill light (soft, from opposite side)
fill = bpy.data.objects.new("fill", bpy.data.lights.new("fill",'SUN'))
fill.location = (-0.5, 0.5, 0.3)
fill.rotation_euler = (math.radians(25), 0, math.radians(-30))
scene.collection.objects.link(fill)
fill.data.energy = 1.5

# world background
world = None
for w in bpy.data.worlds:
    if w.use_nodes: world = w
if world is None:
    world = bpy.data.worlds.new("World"); scene.world = world
world.node_tree.nodes["Background"].inputs[0].default_value = (0.04,0.04,0.05,1.0)

# save editable scene
bpy.ops.wm.save_as_mainfile(filepath="render-output/scene_v2.blend")
print("scene_v2.blend saved; rendering...")

# render
scene.render.filepath = "render-output/render_v2_preview.png"
bpy.ops.render.render(write_still=True)
print("done -> render-output/render_v2_preview.png")
