#!/usr/bin/env python3
"""87Sr optical lattice clock with cryogenic (77 K) cavity + moving lattice
Physical 3-D rendering (Blender). All geometry/labels grounded in paper text
(arXiv:1009.2017, Middelmann et al. 2010). See source-facts notes below.

Output: case-1_87sr_cryo_lattice/render-output/render_preview.png
        case-1_87sr_cryo_lattice/render-output/scene.blend
"""
import bpy, math

bpy.ops.wm.read_factory_settings(use_empty=True)

# ---- scene render settings first ----
scene = bpy.context.scene
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.engine = 'CYCLES'
scene.cycles.samples = 32
scene.cycles.use_denoising = True
try:
    prefs = bpy.context.preferences
    cp = prefs.addons.get('cycles')
    if cp and getattr(cp, 'devices', None):
        for d in cp.devices:
            d.use = True
except Exception as e:
    print('GPU setup skipped:', e)

# ---------------- materials ----------------
def mat(name, base, rough=0.5, metal=0.0, emission=None, emis_str=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = base + (1.0,)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if emission is not None:
        bsdf.inputs["Emission Color"].default_value = emission + (1.0,)
        bsdf.inputs["Emission Strength"].default_value = emis_str
    return m

mat_vac   = mat("vacuum", (0.55,0.58,0.62), 0.35, 0.7)         # metal chamber
mat_vac_g = mat("vacuum_glass", (0.8,0.85,0.9), 0.05, 0.0, (0.9,0.95,1.0), 0.05)
mat_copper= mat("copper", (0.85,0.55,0.35), 0.4, 0.9)
mat_cuO   = mat("cuo", (0.25,0.22,0.2), 0.7, 0.3)
mat_sapph = mat("sapphire", (0.4,0.6,0.9), 0.1, 0.0, (0.5,0.7,1.0), 0.15)
mat_laser = mat("laser", (0.1,0.6,1.0), 0.2, 0.0, (0.0,0.5,1.0), 1.5)
mat_clock = mat("clock", (0.9,0.2,0.2), 0.2, 0.0, (1.0,0.1,0.1), 1.5)
mat_mot   = mat("mot", (0.2,0.2,0.25), 0.4, 0.8)               # coils/dark metal
mat_stage = mat("stage", (0.6,0.6,0.65), 0.3, 0.7)             # air-bearing stage
mat_beacon= mat("beacon", (0.9,0.9,0.9), 0.3, 0.0, (1,1,1), 0.6)
mat_furnace=mat("furnace",(0.4,0.35,0.3),0.5,0.4)

# ---------------- helper ----------------
def cyl(name, r, depth, loc, rot=(0,0,0), m=None, seg=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=seg)
    o = bpy.context.object; o.name = name
    o.display_type = 'TEXTURED'
    if m: o.data.materials.append(m)
    return o

def box(name, sx, sy, sz, loc, rot=(0,0,0), m=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    o.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    o.display_type = 'TEXTURED'
    if m: o.data.materials.append(m)
    return o

def add_beam(name, p0, p1, r=0.004, m=None):
    import mathutils
    v = mathutils.Vector(p1) - mathutils.Vector(p0)
    mid = (mathutils.Vector(p0)+mathutils.Vector(p1))/2
    length = v.length
    rot = v.to_track_quat('Z','Y').to_euler()
    return cyl(name, r, length, tuple(mid), tuple(rot), m)

def add_text(name, s, loc, size=0.016, rot=(0.45, 0.15, 0.35), align="CENTER"):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    o.data.body = s
    o.data.size = size
    o.data.align_x = align
    o.data.extrude = 0.001
    return o

# ---------------- layout (paper Fig.7: MOT right, cold cavity left, 50 mm) ----------------
X0 = 0.0
X1 = 0.05   # 50 mm transport distance
Y0 = 0.0
Z0 = 0.0

# vacuum chamber (large metal box)
box("vacuum", 0.22, 0.22, 0.22, (-0.11, 0.0, -0.11+0.11), m=mat_vac)
# open the front: use glass front panel
glass = box("vacuum_glass_front", 0.22, 0.02, 0.22, (-0.11, -0.11, 0.0), m=mat_vac_g)
glass.display_type = 'WIRE'

# furnace (480 C) on far right
furnace = cyl("furnace", 0.012, 0.05, (0.14, 0.0, 0.05), (0,0,0), m_furnace := mat_furnace)

# thermal atomic beam (dashed concept: thin cylinder, from furnace to Zeeman slower)
beam = add_beam("atomic_beam", (0.125,0,0.05), (0.05,0,0.05), r=0.0015, m=mat_beacon)

# Zeeman slower (cylindrical coil stack)
cyl("zeeman_slower", 0.02, 0.05, (0.045, 0.0, 0.05), (0, math.radians(90), 0), m=mat_mot)

# 2D optical molasses (deflection beams - shown as thin crossing lines)
add_beam("molasses_x", (0.0,0,0.05), (0.09,0.05,0.05), r=0.001, m=mat_laser)
add_beam("molasses_y", (0.045,0.0,0.05), (0.045,0.07,0.05), r=0.001, m=mat_laser)

# MOT region (right side) - coils
for dx in (-0.03, 0.03):
    cyl(f"mot_coil_{dx:+.0f}", 0.03, 0.015, (0.085+dx, 0.0, 0.05), (0, math.radians(90), 0), m=mat_mot)
# MOT beams (blue + red overlapped - 461 nm cooling)
add_beam("mot_beam_blue1", (0.14,0,0.05), (0.04,0,0.05), r=0.002, m=mat_laser)
add_beam("mot_beam_red1",  (0.14,0.03,0.05), (0.04,0.03,0.05), r=0.002, m=mat_clock)

# Air-bearing translation stages (two, on both sides of vacuum)
box("stage_right", 0.06, 0.06, 0.03, (0.13, 0.0, -0.04), m=mat_stage)
box("stage_left",  0.06, 0.06, 0.03, (-0.18, 0.0, -0.04), m=mat_stage)

# --- CRYOGENIC CAVITY (left side, Fig.7) ---
# cylindrical copper structure: inner dia 10 mm, length 160 mm
cyl("copper_cryo", 0.005, 0.16, (-0.06, 0.0, 0.05), (0, math.radians(90), 0), m=mat_copper)
# aperture (thinner ring)
ap = cyl("aperture", 0.003, 0.008, (-0.06, 0.0, 0.05), (0, math.radians(90), 0), m=mat_cuO)
ap.display_type = 'WIRE'
# tilted sapphire window at rear
win = box("sapphire_window", 0.012, 0.012, 0.001, (-0.14, 0.0, 0.05), rot=(0, math.radians(20), 0), m=mat_sapph)
# CuO inner lining hint (thin inner cylinder, wire)
cuo = cyl("cuo_lining", 0.0045, 0.16, (-0.06, 0.0, 0.05), (0, math.radians(90), 0), m=mat_cuO)
cuo.display_type = 'WIRE'

# interrogation volume (small glowing region inside cavity)
cyl("interrogation_volume", 0.002, 0.004, (-0.06, 0.0, 0.05), (0, math.radians(90), 0), m=mat_laser)

# --- OPTICS (lattice + clock laser) ---
# lattice laser (Ti:Sapphire) - thin blue beam going through cavity
add_beam("lattice_beam", (-0.19, 0.0, 0.05), (-0.035, 0.0, 0.05), r=0.0025, m=mat_laser)
# clock laser 698 nm - overlapping via dichroic mirror
add_beam("clock_beam", (-0.19, 0.02, 0.05), (-0.035, 0.0, 0.05), r=0.002, m=mat_clock)
# dichroic mirror
dm = box("dichroic_mirror", 0.012, 0.012, 0.001, (-0.16, 0.01, 0.05), rot=(math.radians(45),0,0), m=mat_sapph)

# ---------------- labels ----------------
add_text("lbl_cryo", "Cold CuO cavity (77 K)", (-0.06, 0.0, 0.075), 0.012)
add_text("lbl_mot", "MOT region", (0.085, 0.0, 0.075), 0.012)
add_text("lbl_stage_l", "Air-bearing stage", (-0.18, 0.0, -0.085), 0.01)
add_text("lbl_furnace", "Furnace 480 C", (0.14, 0.0, 0.09), 0.012)
add_text("lbl_lattice", "Lattice laser (698 nm)", (-0.19, 0.0, 0.06), 0.01, align="LEFT")
add_text("lbl_clock", "Clock laser", (-0.19, 0.025, 0.05), 0.01, align="LEFT")

# ---------------- camera / light / world ----------------
cam_loc = (0.18, -0.20, 0.15)
look = (-0.05, 0.0, 0.02)
import mathutils
d = mathutils.Vector(look) - mathutils.Vector(cam_loc)
rot = d.to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=cam_loc, rotation=tuple(rot))
cam = bpy.context.object; cam.name = "camera"
bpy.context.scene.camera = cam
cam.data.lens = 50

sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", 'SUN'))
sun.location = (0.2, -0.4, 0.5)
sun.rotation_euler = (math.radians(35), 0, math.radians(30))
bpy.context.scene.collection.objects.link(sun)
sun.data.energy = 5.0

world = None
for w in bpy.data.worlds:
    if w and w.use_nodes:
        world = w
if world is None:
    world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.03, 0.03, 0.04, 1.0)

# ---- render & save ----
scene.render.filepath = "case-1_87sr_cryo_lattice/render-output/render_preview.png"
bpy.ops.wm.save_as_mainfile(filepath="case-1_87sr_cryo_lattice/render-output/scene.blend")
print("scene saved; rendering preview...")
bpy.ops.render.render(write_still=True)
print("render done -> case-1_87sr_cryo_lattice/render-output/render_preview.png")
