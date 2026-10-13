"""V29 acoustic black hole metamaterial beam build_v01.py
Bidirectional asymmetric ABH metamaterial beam + experimental setup
(excitation sensor, response sensor, support cradles, DAQ box).
Based on 10.1007/s42417-024-01645-0 Springer PDF Fig. 12/13.
Beam: aluminum alloy (ρ=1160 kg/m3, E=2.46 GPa), power-law tapered ABH cells
arranged in a row, with two identical profiles flipped 180° at head/tail.
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
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.05, 0.06, 1.0)
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

sc = setup()

# ==== Dimensions ====
# ABH beam: l1=50mm conical region, l2=5mm uniform region, h2=8mm uniform thickness, h1=1mm residual
# s=110mm between centers, m=2 power index, r=8mm rotary shaft
# We scale: scene ~ mm/1000
L_cone = 0.050   # conical taper length (m)
L_unif = 0.005   # uniform region length
H_main = 0.008   # main uniform thickness
H_res  = 0.001   # residual thickness at taper end
W_b    = 0.020   # beam width (Y)
# Total beam length: several periodic cells, assume 6 cells
N_CELLS = 6
CELL_W  = L_cone + L_unif   # 55mm per cell
BEAM_L  = N_CELLS * CELL_W   # 330mm total

# Z: beam sits on stand cradles
Z0   = 0.06   # beam center z (above stand)
Z_top = Z0 + H_main/2

# ==== Materials ====
M_beam  = mat("beam_al",    (0.75,0.75,0.80), rough=0.3, metal=0.7)     # aluminum alloy
M_stand = mat("stand_base", (0.15,0.13,0.10), rough=0.6, metal=0.4)     # optical table top
M_crack = mat("cradle",     (0.30,0.25,0.20), rough=0.5, metal=0.4)     # V-groove cradles
M_daq   = mat("daq_box",    (0.08,0.08,0.10), rough=0.5, metal=0.5)     # DAQ electronics
M_wire  = mat("wire",       (0.10,0.10,0.12), rough=0.4, metal=0.6)
M_laser = mat("laser_src",  (0.05,0.05,0.08), rough=0.3, metal=0.3)
M_sens  = mat("sensor_head",(0.10,0.10,0.12), rough=0.3, metal=0.7)
M_excit = mat("shaker_act", (0.05,0.05,0.08), rough=0.4, metal=0.7)
M_table = mat("opt_table",  (0.12,0.10,0.08), rough=0.7, metal=0.3)

# ==== Optical table (bench base) ====
box("optical_table", 0.50, 0.40, 0.02, (0, 0, 0.01), M_table)

# ==== Support cradles (V-groove style, spaced along beam) ====
for i in range(3):
    cx = -BEAM_L/2 + i * BEAM_L/2
    # Cradle base
    box(f"cradle_{i}", 0.06, W_b + 0.02, 0.04, (cx, 0, Z0 - H_main/2 - 0.02), M_crack)
    # V-groove support (two angled blocks forming V)
    block_l = box(f"cradle_l_{i}", 0.04, W_b+0.01, 0.03, (cx, -0.01, Z0 - H_main/2 - 0.005), M_crack)
    block_r = box(f"cradle_r_{i}", 0.04, W_b+0.01, 0.03, (cx,  0.01, Z0 - H_main/2 - 0.005), M_crack)

# ==== ABH Metamaterial Beam (the key object) ====
# The beam is a long box with periodic tapered sections.
# Simplified representation: main beam body + periodic taper notches
# Main beam body (uniform thickness)
beam = box("abhs_beam_main", BEAM_L, W_b, H_main, (0, 0, Z0), M_beam)

# Periodic ABH taper cells (conical tapers visible as wedge notches on top and bottom)
for i in range(N_CELLS):
    cx = -BEAM_L/2 + (i + 0.5) * CELL_W
    # Top taper (wedge shape: use a wedge prism approximated by a scaled+rotated box)
    # Simplified: two thin wedge blocks (one on top face, one on bottom, pointing opposite directions)
    # Top wedge (tapers inward)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, 0, Z_top + H_res/2 + 0.001))
    w_o = bpy.context.object
    w_o.name = f"abhs_top_wedge_{i}"
    w_o.scale = (L_cone/2, W_b/2 + 0.002, H_main/2 - H_res/2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    w_o.rotation_euler = (0, math.radians(-45 + (180 if i % 2 else 0)), 0)
    w_o.data.materials.append(M_beam)
    # Bottom wedge (opposite direction — this is what makes it "bidirectional asymmetric")
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, 0, Z0 - H_main/2 - H_res/2 - 0.001))
    w_o = bpy.context.object
    w_o.name = f"abhs_bot_wedge_{i}"
    w_o.scale = (L_cone/2, W_b/2 + 0.002, H_main/2 - H_res/2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    w_o.rotation_euler = (0, math.radians(45 - (180 if i % 2 else 0)), 0)
    w_o.data.materials.append(M_beam)

# ==== Excitation actuator (shaker) on left end ====
exc_x = -BEAM_L/2 - 0.01
box("shaker_body", 0.04, W_b, 0.06, (exc_x, 0, Z0), M_excit)
cyl("shaker_wire", 0.003, 0.03, (exc_x + 0.02, 0, Z0 - 0.03), (0,0,0), M_wire, seg=12)

# ==== Response sensor (laser vibrometer head) on right end ====
sens_x = BEAM_L/2 + 0.03
box("sensor_head", 0.04, 0.03, 0.05, (sens_x, 0, Z0), M_sens)
# Laser beam from sensor head to beam tip
beam_end = (BEAM_L/2 + 0.01, 0, Z0)
beam_start = (sens_x - 0.02, 0, Z0)
v = mathutils.Vector(beam_end) - mathutils.Vector(beam_start)
mid = (mathutils.Vector(beam_start) + mathutils.Vector(beam_end)) / 2
rot = v.to_track_quat('Z','Y').to_euler()
laser = cyl("sensor_laser", 0.0008, v.length, tuple(mid), tuple(rot),
            mat("laser_red",(1.0,0.0,0.0),rough=0.05,emis=(1,0,0),es=5.0), seg=12)
laser['beam_p0'] = tuple(beam_start)
laser['beam_p1'] = tuple(beam_end)

# ==== DAQ / control box on optical table ====
box("daq_box", 0.12, 0.08, 0.05, (0.12, -0.12, 0.02 + 0.025), M_daq)
# Wire from shaker to DAQ
daq_p0 = (exc_x + 0.01, 0, Z0 - 0.04)
daq_p1 = (0.10, -0.12, 0.025)
v2 = mathutils.Vector(daq_p1) - mathutils.Vector(daq_p0)
mid2 = (mathutils.Vector(daq_p0) + mathutils.Vector(daq_p1)) / 2
rot2 = v2.to_track_quat('Z','Y').to_euler()
o = cyl("daq_wire_shaker", 0.002, v2.length, tuple(mid2), tuple(rot2), M_wire, seg=12)
o['wire_p0'] = tuple(daq_p0); o['wire_p1'] = tuple(daq_p1)
# Wire from sensor to DAQ
s_p0 = (sens_x - 0.01, 0, Z0 - 0.03)
s_p1 = (0.10, -0.12, 0.025)
v3 = mathutils.Vector(s_p1) - mathutils.Vector(s_p0)
mid3 = (mathutils.Vector(s_p0) + mathutils.Vector(s_p1)) / 2
rot3 = v3.to_track_quat('Z','Y').to_euler()
o = cyl("daq_wire_sensor", 0.002, v3.length, tuple(mid3), tuple(rot3), M_wire, seg=12)
o['wire_p0'] = tuple(s_p0); o['wire_p1'] = tuple(s_p1)

# ==== Render camera ====
cam_pos = (0.25, -0.20, 0.22)
cam_tgt = (0.0, 0.0, Z0)
d = mathutils.Vector(cam_tgt) - mathutils.Vector(cam_pos)
q = (-d).to_track_quat('Z','Y')
bpy.ops.object.camera_add(location=cam_pos, rotation=q.to_euler())
c = bpy.context.object
c.data.lens = 55; c.data.clip_start = 0.01; c.data.clip_end = 50
sc.camera = c

# Lights
for pos, e in [((0.3, 0.1, 0.30), 80), ((-0.2, 0.3, 0.25), 50), ((0.0, -0.2, 0.20), 40)]:
    bpy.ops.object.light_add(location=pos, type='POINT')
    bpy.context.object.data.energy = e

# Save & render
out_blend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scene_v01.blend")
out_png   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overview_v01.png")
sc.render.filepath = out_png
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)

with open(out_png,'rb') as f: h = hashlib.sha256(f.read()).hexdigest()
print(f"V29_BUILD_OK blend={out_blend} png={out_png} sha256={h}")
